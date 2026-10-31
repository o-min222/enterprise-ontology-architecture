"""Build a reproducible plugin ZIP from the Git index, never a directory crawl."""

import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path, PurePosixPath


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def package(root, output):
    root = Path(root).resolve()
    # Staging defines the reviewed package. Never silently package older staged code.
    if subprocess.run(["git", "-C", str(root), "diff", "--quiet"], check=False).returncode:
        raise ValueError("Unstaged tracked changes: review and stage them before packaging")
    files = {}
    for entry in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, sha, stage = metadata.decode("ascii").split()
        name = raw_path.decode("utf-8")
        parts = PurePosixPath(name).parts
        if mode not in {"100644", "100755"} or stage != "0":
            raise ValueError(f"Unsupported file mode or unresolved merge: {name}")
        if (name == "BUILD-INFO.json" or not parts or name.startswith("/")
                or "\\" in name or ":" in name
                or any(p in {"..", ".git", ".venv", "__pycache__"} or p.startswith(".env") for p in parts)
                or parts[0] in {".evidence-first", "knowledge", "dist"}
                or name.endswith((".pyc", ".sqlite3", ".db"))):
            raise ValueError(f"Runtime, private, or unsafe path cannot be packaged: {name}")
        files[name] = git(root, "cat-file", "blob", sha)
    manifest = json.loads(files["plugin.json"])
    required = {".claude-plugin/plugin.json", "skills/evidence-first/SKILL.md",
                "skills/evidence-first-setup/SKILL.md"}
    if not required <= files.keys():
        raise ValueError("Incomplete plugin package")
    files["BUILD-INFO.json"] = (json.dumps({
        "name": manifest["name"], "version": manifest["version"],
        "source_tree": git(root, "write-tree").decode().strip(),
        "files": {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())},
    }, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    output = Path(output)
    if output.resolve() in {(root / name).resolve() for name in files}:
        raise ValueError("Package output cannot overwrite a tracked source file")
    output.parent.mkdir(parents=True, exist_ok=True)
    # Uncompressed ZIP keeps bytes stable across zlib versions and platforms.
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return hashlib.sha256(output.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("dist/evidence-first.zip"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        digest = package(root, args.output)
    except (ValueError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Package failed: {error}\n")
    print(json.dumps({"output": str(args.output), "sha256": digest}))


if __name__ == "__main__":
    main()
