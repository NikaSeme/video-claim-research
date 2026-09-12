#!/usr/bin/env python3
"""Fail when a release tree contains common private-data or packaging hazards."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


TEXT_SUFFIXES = {
    "",
    ".css",
    ".html",
    ".js",
    ".jsx",
    ".mjs",
    ".ts",
    ".tsx",
    ".json",
    ".md",
    ".py",
    ".rules",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
SKIP_DIR_NAMES = {".git"}
PRIVATE_DIR_NAMES = {
    ".idea",
    ".pytest_cache",
    ".vscode",
    "__pycache__",
    "node_modules",
    "state",
}
BINARY_SUFFIXES = {
    ".avi",
    ".jpeg",
    ".jpg",
    ".m4a",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp3",
    ".mp4",
    ".pdf",
    ".png",
    ".wav",
    ".webm",
    ".webp",
}
APPROVED_BINARY_PREFIXES = (Path("examples/elu-mcp-claim-check"),)
VISUAL_SUFFIXES = BINARY_SUFFIXES | {".svg", ".gif", ".avif", ".heic", ".ico"}


def check_visual_manifest(root: Path) -> list[str]:
    """Verify recorded review and provenance; human visual/rights review is still required."""
    issues = []
    for prefix in APPROVED_BINARY_PREFIXES:
        folder = root / prefix
        actual = {p.relative_to(folder).as_posix(): p for p in folder.rglob("*")
                  if p.is_file() and p.suffix.lower() in VISUAL_SUFFIXES}
        if not actual:
            continue
        try:
            manifest = json.loads((folder / "publication-manifest.json").read_text())
            if not isinstance(manifest, dict):
                raise ValueError("not an object")
        except (ValueError, OSError):
            issues.append(f"visual publication manifest missing or invalid: {prefix}")
            continue
        if (manifest.get("policy_version") != 1 or manifest.get("review_status") != "reviewed"
                or manifest.get("original_visuals_only") is not True or manifest.get("claim_focused") is not True
                or not manifest.get("reviewer") or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(manifest.get("reviewed_at", "")))):
            issues.append(f"visual publication review incomplete: {prefix}")
        assets = manifest.get("assets")
        if not isinstance(assets, list):
            issues.append(f"visual asset list invalid: {prefix}")
            continue
        listed = set()
        expected_kinds = {".pdf": "original_report", ".png": "report_render", ".svg": "original_diagram"}
        for entry in assets:
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
                issues.append(f"visual asset entry invalid: {prefix}")
                continue
            name = entry["path"]
            rel = Path(name)
            if rel.is_absolute() or ".." in rel.parts or name in listed:
                issues.append(f"visual asset path invalid or duplicated: {name}")
                continue
            listed.add(name)
            path = actual.get(name)
            if path is None or path.is_symlink():
                issues.append(f"reviewed visual missing or unsafe: {name}")
                continue
            if entry.get("kind") != expected_kinds.get(path.suffix.lower()) or path.suffix.lower() not in expected_kinds:
                issues.append(f"forbidden visual kind: {name}")
            if not entry.get("source"):
                issues.append(f"visual provenance missing: {name}")
            if entry.get("sha256") != hashlib.sha256(path.read_bytes()).hexdigest():
                issues.append(f"visual hash changed since review: {name}")
            if path.suffix.lower() == ".svg" and re.search(r"<(?:image|script|foreignObject)\b|(?:href|src)\s*=", path.read_text(), re.I):
                issues.append(f"original diagram contains an embedded resource: {name}")
        for name in sorted(set(actual) - listed):
            issues.append(f"unreviewed visual: {prefix / name}")
    return issues


def content_patterns() -> list[tuple[str, re.Pattern[str]]]:
    home_path = "/" + "Users" + "/"
    mobile_documents = "Mobile" + " Documents"
    cloud_docs = "com" + "~apple~CloudDocs"
    return [
        ("absolute macOS home path", re.compile(re.escape(home_path))),
        (
            "iCloud workspace path",
            re.compile(f"{re.escape(mobile_documents)}|{re.escape(cloud_docs)}", re.I),
        ),
        ("private key block", re.compile(r"BEGIN [A-Z ]*PRIVATE KEY")),
        (
            "likely secret assignment",
            re.compile(
                r"(?i)(api[_-]?key|auth[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"][^'\"]{8,}"
            ),
        ),
        ("GitHub token", re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b")),
    ]


def inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def inside_any(path: Path, parents: tuple[Path, ...]) -> bool:
    return any(inside(path, parent) for parent in parents)


def scan(root: Path) -> list[str]:
    issues: list[str] = check_visual_manifest(root)
    reported_private_dirs: set[Path] = set()
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIR_NAMES for part in rel.parts):
            continue
        private_index = next(
            (index for index, part in enumerate(rel.parts) if part in PRIVATE_DIR_NAMES),
            None,
        )
        if private_index is not None:
            private_dir = Path(*rel.parts[: private_index + 1])
            if private_dir not in reported_private_dirs:
                issues.append(f"private/generated directory present: {private_dir}")
                reported_private_dirs.add(private_dir)
            continue
        if path.is_symlink():
            issues.append(f"symlink requires manual review: {rel}")
            continue
        if not path.is_file():
            continue
        if path.stat().st_size > 2_000_000:
            issues.append(f"file exceeds 2 MB release limit: {rel}")
        if path.suffix.lower() in VISUAL_SUFFIXES and not inside_any(rel, APPROVED_BINARY_PREFIXES):
            issues.append(f"binary outside approved public example: {rel}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in content_patterns():
            if pattern.search(text):
                issues.append(f"{label}: {rel}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root to scan.")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    issues = scan(root)
    if issues:
        print("PUBLIC_RELEASE_CHECK: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("PUBLIC_RELEASE_CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
