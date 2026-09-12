from __future__ import annotations

import importlib.util
import hashlib
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_release_check():
    path = ROOT / "scripts/check_public_release.py"
    spec = importlib.util.spec_from_file_location("check_public_release", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleaseCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.release = load_release_check()

    def test_git_metadata_is_not_part_of_release_scan(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            git_dir = root / ".git"
            git_dir.mkdir()
            (git_dir / "config").write_text("/" + "Users" + "/local/path", encoding="utf-8")
            self.assertEqual(self.release.scan(root), [])

    def test_generated_cache_is_reported_once(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            cache = root / "__pycache__"
            cache.mkdir()
            (cache / "one.pyc").write_bytes(b"cache")
            (cache / "two.pyc").write_bytes(b"cache")
            self.assertEqual(
                self.release.scan(root),
                ["private/generated directory present: __pycache__"],
            )

    def test_binary_is_limited_to_reviewed_case_study(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            outside = root / "pdfs" / "private.pdf"
            outside.parent.mkdir()
            outside.write_bytes(b"%PDF-1.4")
            self.assertEqual(
                self.release.scan(root),
                ["binary outside approved public example: pdfs/private.pdf"],
            )

            outside.unlink()
            reviewed = root / "examples" / "elu-mcp-claim-check" / "report.pdf"
            reviewed.parent.mkdir(parents=True)
            reviewed.write_bytes(b"%PDF-1.4")
            self.assertIn("visual publication manifest missing or invalid: examples/elu-mcp-claim-check", self.release.scan(root))

    def approved_visual(self, root, suffix=".pdf", kind="original_report"):
        folder = root / "examples/elu-mcp-claim-check"
        folder.mkdir(parents=True)
        asset = folder / ("report" + suffix)
        asset.write_bytes(b"original fixture")
        manifest = {"policy_version": 1, "review_status": "reviewed",
                    "reviewer": "test fixture", "reviewed_at": "2026-09-10",
                    "original_visuals_only": True, "claim_focused": True,
                    "assets": [{"path": asset.name, "kind": kind, "source": "test",
                                "sha256": hashlib.sha256(asset.read_bytes()).hexdigest()}]}
        (folder / "publication-manifest.json").write_text(json.dumps(manifest))
        return folder, asset, manifest

    def test_reviewed_visual_and_changed_hash(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _, asset, _ = self.approved_visual(root)
            self.assertEqual(self.release.scan(root), [])
            asset.write_bytes(b"changed content")
            self.assertIn("visual hash changed since review: report.pdf", self.release.scan(root))

    def test_extra_frame_inside_example_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            folder, _, _ = self.approved_visual(root)
            (folder / "source-frame.png").write_bytes(b"unreviewed")
            self.assertIn("unreviewed visual: examples/elu-mcp-claim-check/source-frame.png", self.release.scan(root))

    def test_video_is_forbidden_even_if_manifested(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.approved_visual(root, ".mp4", "original_report")
            self.assertIn("forbidden visual kind: report.mp4", self.release.scan(root))

    def test_pending_review_and_traversal_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            folder, _, manifest = self.approved_visual(root)
            manifest["review_status"] = "pending"
            manifest["assets"][0]["path"] = "../outside.pdf"
            (folder / "publication-manifest.json").write_text(json.dumps(manifest))
            issues = self.release.scan(root)
            self.assertIn("visual publication review incomplete: examples/elu-mcp-claim-check", issues)
            self.assertIn("visual asset path invalid or duplicated: ../outside.pdf", issues)

    def test_svg_cannot_embed_an_image(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            folder, asset, manifest = self.approved_visual(root, ".svg", "original_diagram")
            asset.write_text('<svg><image href="frame.png"/></svg>')
            manifest["assets"][0]["sha256"] = hashlib.sha256(asset.read_bytes()).hexdigest()
            (folder / "publication-manifest.json").write_text(json.dumps(manifest))
            self.assertIn("original diagram contains an embedded resource: report.svg", self.release.scan(root))


    def test_modern_javascript_sources_are_scanned(self) -> None:
        for suffix in (".jsx", ".mjs", ".ts", ".tsx"):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                (root / ("source" + suffix)).write_text("/" + "Users" + "/local/path", encoding="utf-8")
                self.assertEqual(
                    self.release.scan(root),
                    ["absolute macOS home path: source" + suffix],
                )


if __name__ == "__main__":
    unittest.main()
