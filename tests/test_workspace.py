"""Exercise actual local stores and migration failure boundaries in isolation."""

import copy
from contextlib import closing
import importlib.util
import itertools
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/evidence-first"
sys.path.insert(0, str(SKILL / "scripts"))
spec = importlib.util.spec_from_file_location("workspace", SKILL / "scripts/workspace.py")
workspace = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = workspace
spec.loader.exec_module(workspace)
RECORDS = json.loads((SKILL / "examples/evidence-ledger.json").read_text(encoding="utf-8"))
CONFIG_SCHEMA = json.loads((SKILL / "assets/workspace.schema.json").read_text(encoding="utf-8"))


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.root = Path(self.folder.name)
        self.addCleanup(self.folder.cleanup)

    def seed(self):
        workspace.initialize(self.root, "wiki")
        path = self.root / "knowledge/wiki/records.json"
        path.write_text(json.dumps(RECORDS, ensure_ascii=False), encoding="utf-8")
        shared = self.root / "knowledge/shared"
        (shared / "source.txt").write_text("가상 원천 자료. 유지할 원문.", encoding="utf-8")
        (shared / "definition.md").write_text("가상 공통 의미 정의 v1", encoding="utf-8")
        (shared / "assessment.md").write_text("가상 독립 해석", encoding="utf-8")

    def test_each_initial_selection_creates_only_selected_storage(self):
        Draft202012Validator.check_schema(CONFIG_SCHEMA)
        for mode, components in workspace.MODES.items():
            with self.subTest(mode=mode):
                root = self.root / mode
                config = workspace.initialize(root, mode, "db" if mode == "hybrid" else None)
                Draft202012Validator(CONFIG_SCHEMA).validate(config)
                self.assertEqual(config["enabled_components"], components)
                self.assertEqual((root / "knowledge/wiki").exists(), "wiki" in components)
                self.assertEqual((root / "knowledge/db/evidence.sqlite3").exists(), "db" in components)
                if mode == "behavior":
                    self.assertFalse((root / "knowledge").exists())

    def test_hybrid_requires_primary_and_existing_config_is_preserved(self):
        with self.assertRaises(ValueError):
            workspace.initialize(self.root, "hybrid")
        self.assertEqual(snapshot(self.root), {})
        workspace.initialize(self.root, "behavior")
        before = snapshot(self.root)
        with self.assertRaises(ValueError):
            workspace.initialize(self.root, "db")
        self.assertEqual(snapshot(self.root), before)

    def test_behavior_can_add_db_directly_and_add_is_idempotent(self):
        workspace.initialize(self.root, "behavior")
        config = workspace.add(self.root, "db")
        self.assertEqual(config["primary_store"], "db")
        self.assertFalse((self.root / "knowledge/wiki").exists())
        before = snapshot(self.root)
        self.assertEqual(workspace.add(self.root, "db"), config)
        self.assertEqual(snapshot(self.root), before)

    def test_add_preserves_primary_and_does_not_copy_records(self):
        self.seed()
        before = (self.root / "knowledge/wiki/records.json").read_bytes()
        config = workspace.add(self.root, "db")
        self.assertEqual(config["primary_store"], "wiki")
        self.assertEqual(workspace.read_store(self.root, "db"), [])
        self.assertEqual((self.root / "knowledge/wiki/records.json").read_bytes(), before)

    def test_preview_has_no_filesystem_side_effects(self):
        self.seed()
        before = snapshot(self.root)
        plan = workspace.migrate(self.root, "db")
        self.assertFalse(plan["applied"])
        self.assertEqual(plan["records"], len(RECORDS))
        self.assertEqual(snapshot(self.root), before)
        self.assertEqual(workspace.load_config(self.root)["primary_store"], "wiki")
        workspace.migrate(self.root, "db", apply=True)
        before = snapshot(self.root)
        workspace.migrate(self.root, "wiki")
        self.assertEqual(snapshot(self.root), before)

    def test_wiki_db_and_back_preserve_all_record_fields_and_shared_files(self):
        self.seed()
        before = snapshot(self.root)
        result = workspace.migrate(self.root, "db", apply=True)
        self.assertTrue(result["applied"])
        self.assertEqual(workspace.load_config(self.root)["primary_store"], "db")
        self.assertEqual(workspace.read_store(self.root, "wiki"), workspace.read_store(self.root, "db"))
        after = snapshot(self.root)
        for name, content in before.items():
            if not name.startswith(".evidence-first/"):
                self.assertEqual(after[name], content)
        self.assertTrue(list((self.root / ".evidence-first/history").glob("*.json")))
        workspace.migrate(self.root, "wiki", apply=True)
        self.assertEqual(workspace.load_config(self.root)["primary_store"], "wiki")
        self.assertEqual(len(workspace.read_store(self.root, "db")), len(RECORDS))

    def test_db_to_new_wiki_creates_readable_pages(self):
        workspace.initialize(self.root, "db")
        workspace.write_empty_store(self.root, "db", RECORDS)
        workspace.migrate(self.root, "wiki", apply=True)
        self.assertEqual(workspace.read_store(self.root, "wiki"), sorted(RECORDS, key=lambda r: r["id"]))
        page = (self.root / "knowledge/wiki/index.md").read_text(encoding="utf-8")
        self.assertIn(RECORDS[0]["statement"], page)
        decision = next(record for record in RECORDS if record["id"] == "DECISION-DEMO-1")
        section = page.split("## DECISION-DEMO-1\n", 1)[1].split("\n## ", 1)[0]
        self.assertIn("official_decision", section)
        self.assertIn("disputed", section)
        self.assertIn(decision["verification"]["scope"], section)

    def test_conflicting_destination_never_overwrites_or_switches(self):
        self.seed()
        workspace.add(self.root, "db")
        different = copy.deepcopy(RECORDS)
        different[0]["statement"] = "가상 충돌 기록"
        workspace.write_empty_store(self.root, "db", different)
        before = snapshot(self.root)
        with self.assertRaises(ValueError):
            workspace.migrate(self.root, "db", apply=True)
        self.assertEqual(snapshot(self.root), before)
        self.assertEqual(workspace.load_config(self.root)["primary_store"], "wiki")

    def test_failure_before_config_switch_keeps_source_and_old_primary(self):
        self.seed()
        original = (self.root / "knowledge/wiki/records.json").read_bytes()
        with patch.object(workspace, "save_config", side_effect=OSError("simulated config write failure")):
            with self.assertRaises(OSError):
                workspace.migrate(self.root, "db", apply=True)
        self.assertEqual(workspace.load_config(self.root)["primary_store"], "wiki")
        self.assertEqual((self.root / "knowledge/wiki/records.json").read_bytes(), original)
        self.assertFalse((self.root / ".evidence-first/write.lock").exists())

    def test_source_change_during_copy_prevents_primary_switch(self):
        self.seed()
        original_writer = workspace.write_empty_store

        def concurrent_change(root, component, records, **kwargs):
            original_writer(root, component, records, **kwargs)
            changed = copy.deepcopy(RECORDS)
            changed[0]["version"] = "2"
            (self.root / "knowledge/wiki/records.json").write_text(json.dumps(changed), encoding="utf-8")

        with patch.object(workspace, "write_empty_store", side_effect=concurrent_change):
            with self.assertRaises(ValueError):
                workspace.migrate(self.root, "db", apply=True)
        self.assertEqual(workspace.load_config(self.root)["primary_store"], "wiki")
        self.assertNotEqual(workspace.read_store(self.root, "wiki"), workspace.read_store(self.root, "db"))

    def test_bad_records_and_db_payload_disagreement_stop_migration(self):
        self.seed()
        path = self.root / "knowledge/wiki/records.json"
        path.write_text(json.dumps([RECORDS[0], RECORDS[0]]), encoding="utf-8")
        with self.assertRaises(ValueError):
            workspace.migrate(self.root, "db", apply=True)
        self.assertFalse((self.root / "knowledge/db/evidence.sqlite3").exists())
        path.write_text(json.dumps(RECORDS), encoding="utf-8")
        workspace.migrate(self.root, "db", apply=True)
        with closing(sqlite3.connect(self.root / workspace.STORES["db"])) as connection, connection:
            connection.execute("UPDATE assertions SET verification_status = 'disputed' WHERE id = ?", (RECORDS[0]["id"],))
        with self.assertRaises(ValueError):
            workspace.migrate(self.root, "wiki", apply=True)
        self.assertEqual(workspace.load_config(self.root)["primary_store"], "db")

    def test_sqlite_supports_all_twenty_independent_combinations(self):
        workspace.initialize(self.root, "db")
        schema = json.loads((SKILL / "assets/assertion.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(set(workspace.TYPES), set(schema["properties"]["information_type"]["enum"]))
        self.assertEqual(set(workspace.STATUSES), set(schema["properties"]["verification_status"]["enum"]))
        records = []
        for number, (info_type, status) in enumerate(itertools.product(workspace.TYPES, workspace.STATUSES)):
            record = copy.deepcopy(RECORDS[0])
            record.update(id=str(number), information_type=info_type, verification_status=status)
            records.append(record)
        workspace.write_empty_store(self.root, "db", records)
        self.assertEqual(len(workspace.read_store(self.root, "db")), 20)
        with closing(sqlite3.connect(self.root / workspace.STORES["db"])) as connection, connection:
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute("INSERT INTO assertions VALUES ('bad', 'fact', 'verified', '{}')")
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute("INSERT INTO assertions VALUES ('bad', 'observation', 'approved', '{}')")

    def test_unregistered_store_lock_and_escaping_paths_are_preserved(self):
        workspace.initialize(self.root, "behavior")
        existing = self.root / "knowledge/wiki"
        existing.mkdir(parents=True)
        note = existing / "important.md"
        note.write_text("가상 기존 문서", encoding="utf-8")
        before = snapshot(self.root)
        with self.assertRaises(ValueError):
            workspace.add(self.root, "wiki")
        self.assertEqual(snapshot(self.root), before)
        lock = self.root / ".evidence-first/write.lock"
        lock.write_text("existing writer", encoding="utf-8")
        with self.assertRaises(ValueError):
            workspace.add(self.root, "db")
        self.assertEqual(lock.read_text(encoding="utf-8"), "existing writer")
        with self.assertRaises(ValueError):
            workspace.path_at(self.root, "../outside")

    def test_cli_works_from_an_installed_copy_and_needs_no_test_dependencies(self):
        installed = self.root / "installed-skill"
        shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns("__pycache__"))
        project = self.root / "project"
        result = subprocess.run([sys.executable, "-S", str(installed / "scripts/workspace.py"), "--root", str(project), "init", "--mode", "behavior"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["enabled_components"], [])
        result = subprocess.run([sys.executable, "-S", str(installed / "scripts/workspace.py"), "--root", str(project), "status"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
