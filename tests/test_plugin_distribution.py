"""Plugin discovery, installed layout, and source-only archive invariants."""

import hashlib
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("package_plugin", ROOT / "scripts/package_plugin.py")
distribution = importlib.util.module_from_spec(spec)
spec.loader.exec_module(distribution)


def git(root, *args):
    return distribution.git(root, *args)


def fixture(root):
    git(root, "init", "--quiet")
    git(root, "config", "core.autocrlf", "false")
    for name in ("plugin.json", ".claude-plugin/plugin.json", "skills/evidence-first/SKILL.md",
                 "skills/evidence-first-setup/SKILL.md", "skills/evidence-first/assets/icon.png"):
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dest)
    git(root, "add", ".")


class PluginDistributionTests(unittest.TestCase):
    def test_identity_and_host_entrypoints(self):
        portable = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(portable["name"], claude["name"])
        self.assertEqual(portable["version"], claude["version"])
        self.assertIn(portable["version"], (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
        extension = portable["extensions"]["com.openai"]
        for target in [extension["onboardingSkill"], extension["interface"]["composerIcon"],
                       extension["interface"]["logo"]]:
            self.assertTrue(target.startswith("./"))
            path = (ROOT / target).resolve()
            self.assertTrue(path.is_relative_to(ROOT.resolve()))
            self.assertTrue(path.is_file())

    def test_marketplace_sources_resolve_same_package(self):
        codex = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        claude = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(codex["name"], claude["name"])
        self.assertEqual(codex["plugins"][0]["name"], claude["plugins"][0]["name"])
        self.assertEqual((ROOT / codex["plugins"][0]["source"]["path"]).resolve(), ROOT.resolve())
        self.assertEqual((ROOT / claude["plugins"][0]["source"]).resolve(), ROOT.resolve())

    def test_installed_companion_and_ui_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            skills = Path(temp) / "skills"
            shutil.copytree(ROOT / "skills", skills)
            for folder in skills.iterdir():
                body = (folder / "SKILL.md").read_text(encoding="utf-8")
                header = yaml.safe_load(body.split("---", 2)[1])
                self.assertEqual(header["name"], folder.name)
                interface = yaml.safe_load((folder / "agents/openai.yaml").read_text(encoding="utf-8"))["interface"]
                self.assertIn("$" + folder.name, interface["default_prompt"])
                self.assertTrue(25 <= len(interface["short_description"]) <= 64)
                for key in ("icon_small", "icon_large"):
                    if key in interface:
                        self.assertTrue((folder / interface[key]).is_file())
            self.assertTrue((skills / "evidence-first/references/workspace-lifecycle.en.md").is_file())

    def test_reproducible_archive_integrity_and_untracked_exclusion(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root)
            (root / "private-untracked.txt").write_text("synthetic private marker", encoding="utf-8")
            one, two = root / "one.zip", root / "two.zip"
            self.assertEqual(distribution.package(root, one), distribution.package(root, two))
            self.assertEqual(one.read_bytes(), two.read_bytes())
            with zipfile.ZipFile(one) as archive:
                self.assertNotIn("private-untracked.txt", archive.namelist())
                build = json.loads(archive.read("BUILD-INFO.json"))
                self.assertEqual(build["source_tree"], git(root, "write-tree").decode().strip())
                self.assertEqual(set(archive.namelist()), set(build["files"]) | {"BUILD-INFO.json"})
                for name, digest in build["files"].items():
                    self.assertEqual(hashlib.sha256(archive.read(name)).hexdigest(), digest)
                self.assertEqual(archive.read("skills/evidence-first/assets/icon.png"),
                                 (ROOT / "skills/evidence-first/assets/icon.png").read_bytes())

    def test_runtime_paths_fail_closed_without_output(self):
        for name in (".evidence-first/config.json", "knowledge/wiki/a.md", ".env", "nested/.env.local",
                     "private.sqlite3", "dist/old.zip"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                fixture(root)
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("synthetic marker", encoding="utf-8")
                git(root, "add", name)
                with self.assertRaisesRegex(ValueError, "cannot be packaged"):
                    distribution.package(root, root / "out.zip")
                self.assertFalse((root / "out.zip").exists())

    def test_unstaged_edit_is_not_silently_omitted(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root)
            with (root / "plugin.json").open("a", encoding="utf-8") as stream:
                stream.write("\n")
            with self.assertRaisesRegex(ValueError, "Unstaged"):
                distribution.package(root, root / "out.zip")

    def test_archive_cannot_overwrite_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root)
            original = (root / "plugin.json").read_bytes()
            with self.assertRaisesRegex(ValueError, "overwrite"):
                distribution.package(root, root / "plugin.json")
            self.assertEqual((root / "plugin.json").read_bytes(), original)

    def test_symlink_index_entry_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root)
            # Use Git's index directly, so Windows symlink privileges are unnecessary.
            blob = git(root, "hash-object", "-w", "plugin.json").decode().strip()
            git(root, "update-index", "--add", "--cacheinfo", f"120000,{blob},alias")
            # A staged missing file is an unstaged change and must already fail closed.
            with self.assertRaises(ValueError):
                distribution.package(root, root / "out.zip")


if __name__ == "__main__":
    unittest.main()
