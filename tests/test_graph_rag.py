"""Native RDF storage, configuration upgrade, and local retrieval integration."""

import copy
from contextlib import closing
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
from test_workspace import CONFIG_SCHEMA, RECORDS, SKILL, snapshot, workspace
import graph_store
import rag
from pyoxigraph import Literal, NamedNode, Quad, Store


class GraphRagTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.root = Path(self.folder.name)
        self.addCleanup(self.folder.cleanup)

    def seed(self, store, root=None):
        root = self.root if root is None else root
        workspace.initialize(root, components=[store], features=["rag"])
        workspace.write_empty_store(root, store, RECORDS)
        return root

    def test_storage_and_features_are_independent_axes(self):
        validator = Draft202012Validator(CONFIG_SCHEMA)
        for size in (1, 2, 3):
            for components in itertools.combinations(workspace.STORES, size):
                root = self.root / "-".join(components)
                config = workspace.initialize(root, components=components, primary=components[0], features=["rag"])
                validator.validate(config)
                self.assertEqual(config["primary_store"], components[0])
                self.assertEqual(config["enabled_features"], ["rag"])
        with self.assertRaises(ValueError):
            workspace.initialize(self.root / "bad", "behavior", features=["rag"])
        with self.assertRaises(ValueError):
            workspace.initialize(self.root / "bad", "wiki", features=["graph_traversal"])
        config = workspace.load_config(self.root / "wiki")
        config["enabled_components"] = ["rag"]
        self.assertFalse(validator.is_valid(config))
        config = workspace.load_config(self.root / "wiki")
        config["enabled_features"] = ["graph_traversal"]
        self.assertFalse(validator.is_valid(config))

    def test_v1_config_is_read_without_rewriting_and_backed_up_on_upgrade(self):
        self.seed("wiki")
        config = workspace.load_config(self.root)
        config["config_version"] = "1.0"
        del config["enabled_features"]
        config_path = self.root / workspace.CONFIG
        config_path.write_text(workspace.encoded(config), encoding="utf-8")
        before = snapshot(self.root)
        Draft202012Validator(CONFIG_SCHEMA).validate(workspace.load_config(self.root))
        workspace.migrate(self.root, "db")
        self.assertEqual(snapshot(self.root), before)
        workspace.enable(self.root, "rag")
        upgraded = workspace.load_config(self.root)
        self.assertEqual(upgraded["config_version"], "2.0")
        self.assertEqual(upgraded["enabled_features"], ["rag"])
        Draft202012Validator(CONFIG_SCHEMA).validate(upgraded)
        backups = [json.loads(p.read_text(encoding="utf-8")) for p in (self.root / ".evidence-first/history").glob("*.json")]
        self.assertIn(config, backups)
        self.assertEqual(workspace.read_store(self.root, "wiki"), sorted(RECORDS, key=lambda r: r["id"]))

    def test_real_graph_roundtrip_and_fixed_sparql_query_preserve_scope(self):
        self.seed("wiki")
        source_bytes = (self.root / "knowledge/wiki/records.json").read_bytes()
        before = snapshot(self.root)
        workspace.migrate(self.root, "graph")
        self.assertEqual(snapshot(self.root), before)
        workspace.migrate(self.root, "graph", apply=True)
        self.assertEqual(workspace.read_store(self.root, "graph"), workspace.read_store(self.root, "wiki"))
        self.assertEqual((self.root / "knowledge/wiki/records.json").read_bytes(), source_bytes)
        before = snapshot(self.root)
        workspace.migrate(self.root, "db")
        self.assertEqual(snapshot(self.root), before)
        workspace.enable(self.root, "graph_traversal")
        result = workspace.graph_query(self.root, "MACHINE-DEMO")
        self.assertEqual(len(result["evidence"]), 5)
        self.assertTrue(result["is_primary"])
        self.assertEqual(next(r for r in result["evidence"] if r["id"] == "DECISION-DEMO-1")["verification_status"], "disputed")
        store = Store.read_only(str(self.root / workspace.STORES["graph"]))
        self.assertTrue(bool(store.query(f"ASK {{ ?a <{graph_store.NS}derivedFrom> ?source }}")))
        del store
        workspace.migrate(self.root, "db", apply=True)
        workspace.migrate(self.root, "wiki", apply=True)
        self.assertEqual(workspace.read_store(self.root, "db"), workspace.read_store(self.root, "graph"))
        self.assertEqual(workspace.load_config(self.root)["enabled_features"], ["rag", "graph_traversal"])

    def test_graph_does_not_silently_drop_unmapped_triples(self):
        self.seed("graph")
        path = self.root / workspace.STORES["graph"]
        store = Store(path)
        store.add(Quad(NamedNode("urn:unknown:node"), NamedNode("urn:unknown:predicate"), Literal("unmapped")))
        store.flush()
        del store
        with self.assertRaises(ValueError):
            workspace.migrate(self.root, "db", apply=True)
        self.assertEqual(workspace.load_config(self.root)["primary_store"], "graph")
        self.assertFalse((self.root / workspace.STORES["db"]).exists())

    def test_graph_accepts_all_twenty_type_status_combinations(self):
        workspace.initialize(self.root, "graph")
        records = []
        for number, (info_type, status) in enumerate(itertools.product(workspace.TYPES, workspace.STATUSES)):
            record = copy.deepcopy(RECORDS[0])
            record.update(id=str(number), information_type=info_type, verification_status=status)
            records.append(record)
        workspace.write_empty_store(self.root, "graph", records)
        self.assertEqual(workspace.read_store(self.root, "graph"), sorted(records, key=lambda r: r["id"]))

    def test_rag_retrieves_full_cited_context_from_each_store(self):
        for store in workspace.STORES:
            with self.subTest(store=store):
                root = self.seed(store, self.root / store)
                rag.build(root)
                before = snapshot(root)
                context = rag.retrieve(root, "냉각 원인")
                hypothesis = next(e for e in context["evidence"] if e["assertion_id"] == "HYP-DEMO-1")
                self.assertEqual(hypothesis["record"], RECORDS[1])
                self.assertEqual(hypothesis["citation_id"], "E1")
                self.assertFalse(context["originals_accessed_by_retriever"])
                self.assertEqual(context["source_store"], store)
                self.assertEqual(snapshot(root), before)
                disputed = rag.retrieve(root, "재가동 결정")
                decision = next(e for e in disputed["evidence"] if e["assertion_id"] == "DECISION-DEMO-1")
                self.assertEqual(decision["record"]["verification_status"], "disputed")

    def test_retrieval_requires_feature_and_explicit_index(self):
        workspace.initialize(self.root, "wiki")
        before = snapshot(self.root)
        with self.assertRaises(ValueError):
            rag.build(self.root)
        self.assertEqual(snapshot(self.root), before)
        workspace.enable(self.root, "rag")
        self.assertFalse((self.root / rag.INDEX).exists())
        with self.assertRaises(ValueError):
            rag.retrieve(self.root, "question")

    def test_empty_results_and_query_syntax_do_not_invent_evidence(self):
        self.seed("wiki")
        rag.build(self.root)
        self.assertEqual(rag.retrieve(self.root, "uniquemissingtoken123")["evidence"], [])
        self.assertEqual(rag.retrieve(self.root, "!!!")["evidence"], [])
        result = rag.retrieve(self.root, '" OR * ; DROP TABLE chunks -- 냉각')
        self.assertTrue(result["evidence_is_untrusted_data"])
        for limit in (0, 21):
            with self.assertRaises(ValueError):
                rag.retrieve(self.root, "냉각", limit)

    def test_changed_records_or_primary_store_require_reindexing(self):
        self.seed("wiki")
        rag.build(self.root)
        path = self.root / "knowledge/wiki/records.json"
        changed = copy.deepcopy(RECORDS)
        changed[0]["version"] = "2"
        path.write_text(json.dumps(changed), encoding="utf-8")
        with self.assertRaises(ValueError):
            rag.retrieve(self.root, "냉각")
        rag.build(self.root)
        workspace.migrate(self.root, "graph", apply=True)
        with self.assertRaises(ValueError):
            rag.retrieve(self.root, "냉각")
        rag.build(self.root)
        self.assertEqual(rag.retrieve(self.root, "냉각")["source_store"], "graph")

    def test_tampered_index_payload_is_not_used_as_source_truth(self):
        self.seed("db")
        rag.build(self.root)
        changed = copy.deepcopy(RECORDS[1])
        changed["verification_status"] = "verified"
        with closing(sqlite3.connect(self.root / rag.INDEX)) as connection, connection:
            connection.execute("UPDATE chunks SET payload = ? WHERE assertion_id = ?", (json.dumps(changed), changed["id"]))
        with self.assertRaises(ValueError):
            rag.retrieve(self.root, "냉각")

    def test_failed_index_rebuild_retains_previous_index(self):
        self.seed("wiki")
        rag.build(self.root)
        before = (self.root / rag.INDEX).read_bytes()
        original = rag.source
        count = 0

        def changed(root):
            nonlocal count
            count += 1
            store, records, fingerprint = original(root)
            return store, records, "changed" if count == 2 else fingerprint

        with patch.object(rag, "source", side_effect=changed):
            with self.assertRaises(ValueError):
                rag.build(self.root)
        self.assertEqual((self.root / rag.INDEX).read_bytes(), before)
        self.assertFalse(list((self.root / ".evidence-first").glob("rag-*.tmp")))

    def test_installed_local_rag_needs_no_model_or_graph_packages(self):
        installed = self.root / "installed"
        shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns("__pycache__"))
        project = self.seed("wiki", self.root / "project")
        for arguments in (["build"], ["retrieve", "--question", "냉각"]):
            result = subprocess.run([sys.executable, "-X", "utf8", "-S", str(installed / "scripts/rag.py"), "--root", str(project), *arguments], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["evidence"])
        destination = self.root / "no-graph-package"
        result = subprocess.run([sys.executable, "-S", str(installed / "scripts/workspace.py"), "--root", str(destination), "init", "--mode", "graph"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
