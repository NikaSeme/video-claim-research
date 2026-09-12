from __future__ import annotations

import importlib.util
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.create_topic = load_module(
            "create_topic",
            ROOT / ".agents/skills/video-claim-research/scripts/create_topic.py",
        )
        cls.extract_assets = load_module(
            "extract_assets",
            ROOT / ".agents/skills/video-claim-research/scripts/extract_media_assets.py",
        )

    def test_slugify_is_stable(self) -> None:
        self.assertEqual(self.create_topic.slugify("AI: Assisted vs Autonomous"), "ai-assisted-vs-autonomous")
        self.assertEqual(self.create_topic.slugify("---"), "topic")

    def test_portable_path_hides_external_parent(self) -> None:
        base = Path("/tmp/release-root").resolve()
        external = Path("/private/example/source.mp4").resolve()
        self.assertEqual(self.extract_assets.portable_path(external, base), "source.mp4")

    def test_scaffold_uses_relative_output(self) -> None:
        script = ROOT / ".agents/skills/video-claim-research/scripts/create_topic.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--topic",
                    "Safe Topic",
                    "--root",
                    temp_dir,
                    "--url",
                    "https://example.com/video",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("topic_dir=materials used/topics/safe-topic", result.stdout)
            self.assertNotIn(temp_dir, result.stdout)
            topic = Path(temp_dir) / "materials used/topics/safe-topic"
            profile = (topic / "source-profile.md").read_text()
            self.assertNotIn("Reputation notes", profile)
            self.assertIn("Evidence cited", profile)
            review = json.loads((topic / "publication-review.json").read_text())
            self.assertIs(review["original_visuals_only"], False)

    def test_publication_review_is_required_and_hash_bound(self):
        audit = load_module("audit_topic", ROOT / ".agents/skills/research-packet-audit/scripts/audit_topic.py")
        with tempfile.TemporaryDirectory() as temp_dir:
            topic = Path(temp_dir)
            report = topic / "report.pdf"
            report.write_bytes(b"%PDF original fixture")
            self.assertEqual(audit.publication_issues(topic, report), ["publication review missing"])
            review = {"policy_version": 1, "original_visuals_only": True,
                      "claim_focused": True, "rights_privacy_reviewed": True,
                      "reviewer": "synthetic fixture", "reviewed_at": "2026-09-10",
                      "report_sha256": hashlib.sha256(report.read_bytes()).hexdigest()}
            (topic / "publication-review.json").write_text(json.dumps(review))
            self.assertEqual(audit.publication_issues(topic, report), [])
            report.write_bytes(b"replacement")
            self.assertIn("publication review does not match final PDF", audit.publication_issues(topic, report))
            review["claim_focused"] = False
            (topic / "publication-review.json").write_text(json.dumps(review))
            self.assertIn("publication review incomplete: claim_focused", audit.publication_issues(topic, report))


if __name__ == "__main__":
    unittest.main()
