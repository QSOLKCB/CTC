import hashlib
from pathlib import Path
import unittest

from ctc.scenarios import render_reference, scenario_payload

ROOT = Path(__file__).resolve().parents[1]


class ScenarioTests(unittest.TestCase):
    def test_exact_seven_synthetic_scenarios(self):
        payload = scenario_payload()
        self.assertFalse(payload["forecast"])
        self.assertEqual(len(payload["scenarios"]), 7)
        self.assertTrue(all(s["forecast"] is False for s in payload["scenarios"]))
        self.assertTrue(all(s["classification"] == "SYNTHETIC_REFERENCE_FIXTURE" for s in payload["scenarios"]))

    def test_checked_in_reference_is_reproducible(self):
        expected = (ROOT / "reference/scenarios-v0.1.json").read_text(encoding="utf-8")
        self.assertEqual(render_reference(), expected)

    def test_reference_hash_matches_manifest(self):
        expected = (ROOT / "reference/scenarios-v0.1.json").read_bytes()
        digest = hashlib.sha256(expected).hexdigest()
        manifest = (ROOT / "reference/SHA256SUMS").read_text(encoding="utf-8").strip().split()
        self.assertEqual(manifest, [digest, "scenarios-v0.1.json"])


if __name__ == "__main__":
    unittest.main()
