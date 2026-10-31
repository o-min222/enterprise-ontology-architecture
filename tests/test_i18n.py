"""Multilingual presentation/retrieval with unchanged canonical records."""

import copy
from contextlib import closing
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator
from test_workspace import RECORDS, SKILL, snapshot, workspace
import localization
import rag


ENGLISH = json.loads((SKILL / "examples/evidence-ledger.en.json").read_text(encoding="utf-8"))


class MultilingualTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.root = Path(self.folder.name)
        self.addCleanup(self.folder.cleanup)

    def seed(self, root=None, store="wiki"):
        root = self.root if root is None else root
        workspace.initialize(root, store, features=["rag"])
        workspace.write_empty_store(root, store, ENGLISH)
        return root

    def test_registered_catalogs_are_complete_and_have_language_fallback(self):
        registry = json.loads((localization.CATALOGS / "manifest.json").read_text(encoding="utf-8"))
        _, baseline = localization.messages("en")
        for tag in registry["locales"]:
            resolution, text = localization.messages(tag)
            self.assertEqual(resolution["messages"], tag)
            self.assertEqual(set(text), set(baseline))
            for key, value in text.items():
                self.assertIsInstance(value, type(baseline[key]))
                self.assertTrue(value)
                if isinstance(value, list):
                    self.assertTrue(all(isinstance(rule, str) and rule for rule in value))
        self.assertEqual(localization.messages("ko-KR")[0], {"requested": "ko-kr", "messages": "ko"})
        self.assertEqual(localization.messages("fr-CA")[0], {"requested": "fr-ca", "messages": "en"})

    def test_invalid_language_cannot_select_a_path_or_create_storage(self):
        for tag in ("../ko", "en/../../x", "ko.json", "", "ko_KR"):
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                workspace.initialize(self.root / "new", "wiki", language=tag)
            self.assertFalse((self.root / "new").exists())

    def test_english_fixture_preserves_ids_classification_and_resolves_sources(self):
        schema = json.loads((SKILL / "assets/assertion.schema.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        by_id = {record["id"]: record for record in RECORDS}
        for record in ENGLISH:
            validator.validate(record)
            original = by_id[record["id"]]
            for key in ("entity_ids", "information_type", "verification_status", "version", "created_at"):
                self.assertEqual(record[key], original[key])
            for source in record["source_refs"]:
                target = urlsplit(source["locator"])
                text = (SKILL / "examples" / target.path).read_text(encoding="utf-8")
                self.assertIn("## " + source["source_id"], text)
                self.assertEqual(target.fragment, source["source_id"].lower())

    def test_localized_wiki_migration_does_not_translate_payload_or_settings(self):
        for tag in ("en", "ko", "ja", "zh"):
            root = self.seed(self.root / tag, "db")
            before = workspace.read_store(root, "db")
            workspace.migrate(root, "wiki", apply=True, language=tag)
            self.assertEqual(workspace.read_store(root, "wiki"), before)
            self.assertEqual(workspace.read_store(root, "db"), before)
            self.assertNotIn("language", workspace.load_config(root))
            _, text = localization.messages(tag)
            page = (root / "knowledge/wiki/index.md").read_text(encoding="utf-8")
            self.assertIn(text["verification_status"], page)
            self.assertIn("disputed", page)
            self.assertIn(next(r for r in ENGLISH if r["id"] == "DECISION-DEMO-1")["statement"], page)

    def test_cross_language_question_and_output_keep_source_and_current_index(self):
        self.seed()
        rag.build(self.root)
        before = snapshot(self.root)
        result = rag.retrieve(self.root, "冷却原因は確認されましたか？", language="ja", search_query="cooling cause")
        self.assertEqual(result["question"], "冷却原因は確認されましたか？")
        self.assertEqual(result["search_query"], "cooling cause")
        self.assertTrue(result["query_was_rewritten"])
        self.assertEqual(result["language"]["messages"], "ja")
        record = next(e["record"] for e in result["evidence"] if e["assertion_id"] == "HYP-DEMO-1")
        self.assertEqual(record, ENGLISH[1])
        fallback = rag.retrieve(self.root, "Is the cooling cause verified?", language="es")
        self.assertEqual(fallback["language"], {"requested": "es", "messages": "en"})
        self.assertEqual(snapshot(self.root), before)

    def test_cjk_lexical_matching_without_spaces(self):
        workspace.initialize(self.root, "wiki", features=["rag"])
        records = []
        for tag, statement in (("ja", "冷却装置の原因は未確認です。"), ("zh", "冷却装置故障的原因尚未确认。"), ("ko", "냉각 장치 원인은 미확인입니다.")):
            record = copy.deepcopy(ENGLISH[1])
            record.update(id="HYP-" + tag, statement=statement)
            records.append(record)
        workspace.write_empty_store(self.root, "wiki", records)
        rag.build(self.root)
        hits = rag.retrieve(self.root, "冷却原因", language="ja")["evidence"]
        self.assertTrue({"HYP-ja", "HYP-zh"} <= {hit["assertion_id"] for hit in hits})
        self.assertIn("HYP-ko", {e["assertion_id"] for e in rag.retrieve(self.root, "냉각 원인", language="ko")["evidence"]})

    def test_old_index_format_requires_explicit_rebuild(self):
        self.seed()
        rag.build(self.root)
        with closing(sqlite3.connect(self.root / rag.INDEX)) as connection, connection:
            connection.execute("UPDATE metadata SET value='1' WHERE key='index_version'")
        with self.assertRaises(ValueError):
            rag.retrieve(self.root, "cooling")
        rag.build(self.root)
        self.assertTrue(rag.retrieve(self.root, "cooling")["evidence"])

    def test_installed_cli_utf8_and_fallback_without_test_packages(self):
        installed = self.root / "installed"
        shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns("__pycache__"))
        project = self.seed(self.root / "project")
        rag.build(project)
        result = subprocess.run([sys.executable, "-S", str(installed / "scripts/rag.py"), "--root", str(project), "--lang", "fr-CA", "retrieve", "--question", "原因は？", "--search-query", "cooling cause"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("using en", result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["question"], "原因は？")
        self.assertEqual(payload["language"]["requested"], "fr-ca")
        self.assertTrue(payload["evidence"])


if __name__ == "__main__":
    unittest.main()
