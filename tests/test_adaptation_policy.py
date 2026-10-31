"""Check the optional agent-interpreted policy contract, not permission enforcement."""

import copy
import json
from pathlib import Path
import tempfile
import unittest

from jsonschema import Draft202012Validator
from test_workspace import SKILL, snapshot, workspace


SCHEMA = json.loads((SKILL / "assets/adaptation-policy.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)
EXAMPLE = json.loads((SKILL / "examples/adaptation-local-auto.json").read_text(encoding="utf-8"))


class AdaptationPolicyTests(unittest.TestCase):
    def test_supported_modes_and_example_are_well_formed(self):
        Draft202012Validator.check_schema(SCHEMA)
        VALIDATOR.validate(EXAMPLE)
        for mode in ("task_scoped", "propose_only"):
            VALIDATOR.validate({"policy_version": "1.0", "mode": mode, "allowed_actions": []})

    def test_policy_does_not_encode_implicit_or_unbounded_grants(self):
        policy = copy.deepcopy(EXAMPLE)
        del policy["authorization_ref"]
        self.assertFalse(VALIDATOR.is_valid(policy))
        for action in ("delete_sources", "change_own_policy", "upload_data", "*", "install_packages"):
            policy = copy.deepcopy(EXAMPLE)
            policy["allowed_actions"] = [action]
            self.assertFalse(VALIDATOR.is_valid(policy))
        for mode in ("task_scoped", "propose_only"):
            policy = copy.deepcopy(EXAMPLE)
            policy["mode"] = mode
            self.assertFalse(VALIDATOR.is_valid(policy))
        policy = copy.deepcopy(EXAMPLE)
        policy["allowed_actions"] = []
        self.assertFalse(VALIDATOR.is_valid(policy))

    def test_adaptation_preference_is_separate_from_storage_and_features(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before = workspace.initialize(root, "behavior")
            config_bytes = (root / workspace.CONFIG).read_bytes()
            policy = {"policy_version": "1.0", "mode": "propose_only", "allowed_actions": []}
            (root / ".evidence-first/adaptation.json").write_text(json.dumps(policy), encoding="utf-8")
            state = snapshot(root)
            self.assertEqual(workspace.load_config(root), before)
            self.assertEqual((root / workspace.CONFIG).read_bytes(), config_bytes)
            self.assertFalse((root / "knowledge").exists())
            self.assertEqual(snapshot(root), state)


if __name__ == "__main__":
    unittest.main()
