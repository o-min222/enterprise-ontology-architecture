"""Package and exchange-format checks, not an evaluation of model judgment."""

import copy
import itertools
import json
import re
import shutil
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "evidence-first"
SCHEMA = json.loads((SKILL / "assets/assertion.schema.json").read_text(encoding="utf-8"))
RECORDS = json.loads((SKILL / "examples/evidence-ledger.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)
TYPES = {"observation", "hypothesis", "reviewed_assessment", "official_decision", "execution_result"}
STATUSES = {"unverified", "in_review", "verified", "disputed"}


def local_links(path):
    """Our authored Markdown uses inline links without spaces in targets."""
    for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", path.read_text(encoding="utf-8")):
        parsed = urlsplit(target)
        if not parsed.scheme and not parsed.netloc and parsed.path:
            yield (path.parent / unquote(parsed.path)).resolve()


class PackageTests(unittest.TestCase):
    def test_standard_frontmatter(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = yaml.safe_load(text.split("---", 2)[1])
        self.assertEqual(frontmatter["name"], SKILL.name)
        self.assertRegex(frontmatter["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertLessEqual(len(frontmatter["name"]), 64)
        self.assertIsInstance(frontmatter["description"], str)
        self.assertTrue(0 < len(frontmatter["description"]) <= 1024)
        self.assertLessEqual(set(frontmatter), {"name", "description", "license", "compatibility", "metadata", "allowed-tools"})
        self.assertNotIn("allowed-tools", frontmatter, "This portable skill must not preapprove tools")
        korean = yaml.safe_load((SKILL / "SKILL.ko.md").read_text(encoding="utf-8").split("---", 2)[1])
        self.assertEqual(korean["name"], frontmatter["name"])
        self.assertEqual(list(SKILL.rglob("SKILL.md")), [SKILL / "SKILL.md"])

    def test_copied_skill_is_self_contained(self):
        # Exercise the documented installation unit, without the repository docs.
        with tempfile.TemporaryDirectory() as folder:
            installed = Path(folder) / "evidence-first"
            shutil.copytree(SKILL, installed)
            for path in installed.rglob("*.md"):
                for target in local_links(path):
                    with self.subTest(path=path.relative_to(installed), target=target):
                        self.assertTrue(target.is_relative_to(installed.resolve()))
                        self.assertTrue(target.is_file())

    def test_repository_links_and_claude_import(self):
        for path in [*ROOT.glob("README*.md"), *ROOT.glob("AGENTS*.md"), *ROOT.glob("CLAUDE*.md"), *(ROOT / "docs").glob("*.md"), *(ROOT / "prompts").glob("*.md"), *(ROOT / "tests").glob("*.md")]:
            for target in local_links(path):
                self.assertTrue(target.is_file(), f"Broken local link in {path}: {target}")
        imports = re.findall(r"^@([^\s]+)$", (ROOT / "CLAUDE.md").read_text(encoding="utf-8"), re.M)
        self.assertEqual(imports, ["AGENTS.md"])
        self.assertTrue((ROOT / imports[0]).is_file())

    def test_schema_and_all_twenty_independent_combinations(self):
        Draft202012Validator.check_schema(SCHEMA)
        self.assertEqual(set(SCHEMA["properties"]["information_type"]["enum"]), TYPES)
        self.assertEqual(set(SCHEMA["properties"]["verification_status"]["enum"]), STATUSES)
        for info_type, status in itertools.product(TYPES, STATUSES):
            record = copy.deepcopy(RECORDS[0])
            record.update(information_type=info_type, verification_status=status)
            with self.subTest(information_type=info_type, verification_status=status):
                VALIDATOR.validate(record)

    def test_invalid_axes_are_rejected_independently(self):
        for field, values in {"information_type": ["fact", "approved", "", None], "verification_status": ["official_decision", "approved", "", None]}.items():
            for value in values:
                record = copy.deepcopy(RECORDS[0])
                record[field] = value
                with self.subTest(field=field, value=value):
                    self.assertFalse(VALIDATOR.is_valid(record))

    def test_verified_requires_scope_method_and_evidence(self):
        for field in ["scope", "method", "evidence_refs"]:
            record = copy.deepcopy(RECORDS[0])
            del record["verification"][field]
            self.assertFalse(VALIDATOR.is_valid(record))
        for field, value in [("scope", ""), ("method", ""), ("evidence_refs", [])]:
            record = copy.deepcopy(RECORDS[0])
            record["verification"][field] = value
            self.assertFalse(VALIDATOR.is_valid(record))
        record = copy.deepcopy(RECORDS[0])
        record["source_refs"] = []
        self.assertFalse(VALIDATOR.is_valid(record))

    def test_missing_sources_can_remain_unverified(self):
        record = copy.deepcopy(RECORDS[1])
        record["source_refs"] = []
        VALIDATOR.validate(record)
        record["verification_status"] = "verified"
        self.assertFalse(VALIDATOR.is_valid(record))

    def test_unavailable_sources_do_not_claim_access(self):
        record = copy.deepcopy(RECORDS[1])
        record["source_refs"][0].update(availability="unavailable", accessed_at=None)
        VALIDATOR.validate(record)
        record["source_refs"][0]["accessed_at"] = "2026-01-10T12:00:00Z"
        self.assertFalse(VALIDATOR.is_valid(record))

    def test_unknown_authority_field_is_not_an_assertion_attribute(self):
        record = copy.deepcopy(RECORDS[0])
        record["execution_authorized"] = True
        self.assertFalse(VALIDATOR.is_valid(record))

    def test_examples_and_provenance_resolve(self):
        self.assertEqual({r["information_type"] for r in RECORDS}, TYPES)
        self.assertEqual(len({r["id"] for r in RECORDS}), len(RECORDS))
        for record in RECORDS:
            with self.subTest(record=record["id"]):
                VALIDATOR.validate(record)
                self.assertIsNotNone(datetime.fromisoformat(record["created_at"].replace("Z", "+00:00")).tzinfo)
                source_ids = {s["source_id"] for s in record["source_refs"]}
                self.assertEqual(len(source_ids), len(record["source_refs"]))
                self.assertLessEqual(set(record["verification"]["evidence_refs"]), source_ids)
                for source in record["source_refs"]:
                    location = urlsplit(source["locator"])
                    source_path = SKILL / "examples" / location.path
                    self.assertTrue(source_path.is_file())
                    headings = re.findall(r"^## (.+)$", source_path.read_text(encoding="utf-8"), re.M)
                    self.assertIn(location.fragment, [h.lower() for h in headings])
                    self.assertIn(source["source_id"], headings)
                context = record["semantic_context"]
                if context:
                    source_text = (SKILL / "examples/synthetic-sources.md").read_text(encoding="utf-8")
                    self.assertIn(f'## {context["model_id"]}', source_text)


if __name__ == "__main__":
    unittest.main()
