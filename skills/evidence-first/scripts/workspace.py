"""Local setup and lossless assertion transport. Python 3.10+, standard library only.

This helper does not enforce access control or schedule AI work. External stores
need an explicit mapping and migration procedure; see workspace-lifecycle.md.
"""

import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import uuid


TYPES = ("observation", "hypothesis", "reviewed_assessment", "official_decision", "execution_result")
STATUSES = ("unverified", "in_review", "verified", "disputed")
MODES = {"behavior": [], "wiki": ["wiki"], "db": ["db"], "hybrid": ["wiki", "db"]}
CONFIG = ".evidence-first/config.json"
STORES = {"wiki": "knowledge/wiki", "db": "knowledge/db/evidence.sqlite3"}


def path_at(root, relative):
    root = Path(root).resolve()
    path = root / relative
    if not path.resolve().is_relative_to(root):
        raise ValueError("Managed path escapes workspace")
    # Refuse indirection even when a symlink resolves inside the workspace.
    for item in [path, *path.parents]:
        if item == root:
            break
        if item.is_symlink() or (hasattr(item, "is_junction") and item.is_junction()):
            raise ValueError("Managed paths must not be symlinks or junctions")
    return path


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def load_config(root):
    config = json.loads(path_at(root, CONFIG).read_text(encoding="utf-8"))
    if not isinstance(config, dict) or set(config) != {"config_version", "behavior", "enabled_components", "primary_store"}:
        raise ValueError("Unsupported workspace configuration fields")
    enabled = config.get("enabled_components")
    primary = config.get("primary_store")
    if (config.get("config_version") != "1.0" or config.get("behavior") != "evidence-first"
            or not isinstance(enabled, list) or any(not isinstance(c, str) or c not in STORES for c in enabled)
            or len(enabled) != len(set(enabled))
            or (enabled and primary not in enabled) or (not enabled and primary is not None)):
        raise ValueError("Unsupported or inconsistent workspace configuration")
    return config


def save_config(root, config):
    path = path_at(root, CONFIG)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = path_at(root, f".evidence-first/history/{uuid.uuid4().hex}.json")
        backup.parent.mkdir(exist_ok=True)
        backup.write_bytes(path.read_bytes())
    temporary = path.with_name(f"config-{uuid.uuid4().hex}.tmp")
    try:
        temporary.write_text(encoded(config), encoding="utf-8")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


@contextlib.contextmanager
def writer(root):
    lock = path_at(root, ".evidence-first/write.lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        handle = lock.open("x", encoding="utf-8")
    except FileExistsError:
        raise ValueError("Workspace is locked; inspect the writer before retrying") from None
    try:
        with handle:
            handle.write(str(os.getpid()))
        yield
    finally:
        lock.unlink()


def prepare(root, component):
    path = path_at(root, STORES[component])
    if path.exists():
        raise ValueError(f"Existing {component} store requires inspection and mapping")
    path_at(root, "knowledge/shared").mkdir(parents=True, exist_ok=True)
    if component == "wiki":
        path.mkdir(parents=True)
        (path / "records.json").write_text("[]\n", encoding="utf-8")
        (path / "index.md").write_text("# Evidence-First Wiki\n\n공유 근거·정의·독립 해석은 `../shared/`에서 관리합니다.\n", encoding="utf-8")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        with contextlib.closing(sqlite3.connect(path)) as connection:
            connection.execute(
                "CREATE TABLE assertions (id TEXT PRIMARY KEY, information_type TEXT NOT NULL "
                f"CHECK (information_type IN {TYPES!r}), verification_status TEXT NOT NULL "
                f"CHECK (verification_status IN {STATUSES!r}), payload TEXT NOT NULL)"
            )
            connection.commit()


def read_store(root, component):
    # ponytail: local ledgers fit in memory; large stores need a streaming adapter.
    path = path_at(root, STORES[component])
    if component == "wiki":
        records = json.loads(path_at(root, f"{STORES['wiki']}/records.json").read_text(encoding="utf-8"))
    else:
        with contextlib.closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as connection:
            rows = connection.execute("SELECT id, information_type, verification_status, payload FROM assertions").fetchall()
        records = []
        for identity, info_type, status, payload in rows:
            record = json.loads(payload)
            if not isinstance(record, dict) or (record.get("id"), record.get("information_type"), record.get("verification_status")) != (identity, info_type, status):
                raise ValueError("DB projection disagrees with payload")
            records.append(record)
    if not isinstance(records, list):
        raise ValueError("Expected an assertion list")
    identities = set()
    for record in records:
        if (not isinstance(record, dict) or not isinstance(record.get("id"), str) or not record["id"]
                or record.get("information_type") not in TYPES or record.get("verification_status") not in STATUSES):
            raise ValueError("Invalid assertion identity or classification")
        if record["id"] in identities:
            raise ValueError("Duplicate assertion ID")
        identities.add(record["id"])
    # Transport checks identity/classification, not full schema validity or truth.
    return sorted(records, key=lambda record: record["id"])


def digest(records):
    return hashlib.sha256(encoded(records).encode("utf-8")).hexdigest()


def write_empty_store(root, component, records):
    if read_store(root, component):
        raise ValueError("Destination is not empty")
    path = path_at(root, STORES[component])
    if component == "wiki":
        path_at(root, f"{STORES['wiki']}/records.json").write_text(encoded(records), encoding="utf-8")
        # The index is derived; user-authored prose belongs under shared/.
        lines = ["# Evidence-First Wiki", "", "가져온 기록의 원문·출처·정의는 records.json 및 ../shared/를 확인하세요.", ""]
        for record in records:
            verification = record.get("verification")
            scope = verification.get("scope", "미기록") if isinstance(verification, dict) else "미기록"
            lines.extend([
                f'## {record["id"]}', "",
                f'- 정보 유형: `{record["information_type"]}`',
                f'- 검증 상태: **{record["verification_status"]}**',
                f'- 검증 범위: {scope}', "",
                "주장:", "", str(record.get("statement", "")), "",
            ])
        path_at(root, f"{STORES['wiki']}/index.md").write_text("\n".join(lines), encoding="utf-8")
    else:
        with contextlib.closing(sqlite3.connect(path)) as connection:
            with connection:
                connection.executemany("INSERT INTO assertions VALUES (?, ?, ?, ?)", [
                    (r["id"], r["information_type"], r["verification_status"], encoded(r)) for r in records
                ])


def initialize(root, mode, primary=None):
    if mode not in MODES:
        raise ValueError("Unknown mode")
    components = MODES[mode].copy()
    if mode == "hybrid" and primary is None:
        raise ValueError("Hybrid mode requires an explicit primary store")
    primary = primary or (components[0] if components else None)
    if (components and primary not in components) or (not components and primary is not None):
        raise ValueError("Primary store must be enabled")
    if path_at(root, CONFIG).exists():
        raise ValueError("Workspace already configured; use add or migrate")
    with writer(root):
        if path_at(root, CONFIG).exists():
            raise ValueError("Workspace already configured")
        for component in components:
            if path_at(root, STORES[component]).exists():
                raise ValueError("Existing store requires inspection and mapping")
        for component in components:
            prepare(root, component)
        config = {"config_version": "1.0", "behavior": "evidence-first", "enabled_components": components, "primary_store": primary}
        save_config(root, config)
    return config


def add(root, component):
    if component not in STORES:
        raise ValueError("Unknown component")
    with writer(root):
        config = load_config(root)
        if component in config["enabled_components"]:
            return config
        prepare(root, component)
        config["enabled_components"].append(component)
        config["primary_store"] = config["primary_store"] or component
        save_config(root, config)
    return config


def migrate(root, target, apply=False):
    if target not in STORES:
        raise ValueError("Unknown target")
    # A preview never creates files, including a lock or a database.
    with writer(root) if apply else contextlib.nullcontext():
        config = load_config(root)
        source = config["primary_store"]
        if source is None or source == target:
            raise ValueError("Migration needs a different active source; use add for behavior-only")
        records = read_store(root, source)
        fingerprint = digest(records)
        if target in config["enabled_components"]:
            destination = read_store(root, target)
            if destination and digest(destination) != fingerprint:
                raise ValueError("Destination differs; map conflicts or archive it before migration")
        elif path_at(root, STORES[target]).exists():
            raise ValueError("Unregistered destination requires inspection and mapping")
        result = {"source": source, "target": target, "records": len(records), "sha256": fingerprint,
                  "applied": False, "source_retained": True, "shared_root": "knowledge/shared"}
        if not apply:
            return result
        if target not in config["enabled_components"]:
            prepare(root, target)
        if not read_store(root, target):
            write_empty_store(root, target, records)
        if digest(read_store(root, target)) != fingerprint or digest(read_store(root, source)) != fingerprint:
            raise ValueError("Verification failed or source changed; primary store not switched")
        if target not in config["enabled_components"]:
            config["enabled_components"].append(target)
        config["primary_store"] = target
        save_config(root, config)
        return dict(result, applied=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--mode", choices=MODES, required=True)
    init.add_argument("--primary", choices=STORES)
    commands.add_parser("status")
    extra = commands.add_parser("add")
    extra.add_argument("component", choices=STORES)
    move = commands.add_parser("migrate")
    move.add_argument("--to", choices=STORES, required=True)
    move.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "init":
            result = initialize(args.root, args.mode, args.primary)
        elif args.command == "add":
            result = add(args.root, args.component)
        elif args.command == "migrate":
            result = migrate(args.root, args.to, args.apply)
        else:
            result = load_config(args.root)
        print(encoded(result), end="")
    except (ValueError, OSError, sqlite3.Error) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
