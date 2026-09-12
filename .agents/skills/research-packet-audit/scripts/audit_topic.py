#!/usr/bin/env python3
"""Audit a video claim research packet."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path


def has_url_with_table_row(path: Path) -> bool:
    if not path.exists():
        return False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "http" in line and "|" in line:
            return True
    return False


def has_blocker(topic_dir: Path) -> bool:
    patterns = [re.compile(r"\bBLOCKER\b", re.I), re.compile(r"\bblocked\b", re.I)]
    for name in ["audit.md", "research-notes.md", "links.md", "transcript.md"]:
        path = topic_dir / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if any(pattern.search(text) for pattern in patterns):
            return True
    return False


def has_any_file(directory: Path) -> bool:
    return directory.exists() and any(path.is_file() for path in directory.rglob("*"))


def publication_issues(topic_dir: Path, report: Path) -> list[str]:
    review_path = topic_dir / "publication-review.json"
    if not review_path.is_file():
        return ["publication review missing"]
    try:
        review = json.loads(review_path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return ["publication review unreadable"]
    if not isinstance(review, dict):
        return ["publication review must be an object"]
    issues = []
    if review.get("policy_version") != 1:
        issues.append("publication policy version missing or unsupported")
    for field in ("original_visuals_only", "claim_focused", "rights_privacy_reviewed"):
        if review.get(field) is not True:
            issues.append(f"publication review incomplete: {field}")
    if not str(review.get("reviewer", "")).strip() or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(review.get("reviewed_at", ""))):
        issues.append("publication reviewer/date missing")
    if not report.is_file() or review.get("report_sha256") != hashlib.sha256(report.read_bytes()).hexdigest():
        issues.append("publication review does not match final PDF")
    return issues


def display_path(path: Path, root: Path) -> str:
    """Format an audit path without writing an absolute home path into the packet."""
    try:
        return path.resolve().relative_to(root).as_posix()
    except (OSError, ValueError):
        return path.name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", help="Topic slug or topic directory path.")
    parser.add_argument("--root", default=".", help="Workspace root.")
    parser.add_argument("--skip-pdf", action="store_true", help="Do not require final PDF.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    candidate = Path(args.topic)
    topic_dir = candidate.resolve() if candidate.exists() else root / "materials used" / "topics" / args.topic
    topic = topic_dir.name

    required_files = [
        topic_dir / "links.md",
        topic_dir / "claims.md",
        topic_dir / "transcript.md",
        topic_dir / "source-profile.md",
        topic_dir / "research-notes.md",
        topic_dir / "report-outline.md",
    ]
    required_dirs = [
        topic_dir / "audio",
        topic_dir / "frames",
        topic_dir / "evidence",
        topic_dir / "ocr",
        root / "videos to transcribe" / topic,
    ]
    required_root_files = [
        root / "transcripts" / f"{topic}.md",
    ]
    if not args.skip_pdf:
        required_root_files.append(root / "pdfs" / f"{topic}.pdf")

    missing: list[str] = []
    warnings = []

    if not args.skip_pdf:
        missing.extend(publication_issues(topic_dir, root / "pdfs" / f"{topic}.pdf"))

    if not topic_dir.exists():
        missing.append(display_path(topic_dir, root))

    for path in required_files + required_root_files:
        if not path.exists():
            missing.append(display_path(path, root))
    for path in required_dirs:
        if not path.exists():
            missing.append(display_path(path, root))

    links = topic_dir / "links.md"
    if links.exists() and not has_url_with_table_row(links):
        missing.append(f"{display_path(links, root)} (no logged URL rows found)")

    blocker = has_blocker(topic_dir)

    claims = topic_dir / "claims.md"
    if claims.exists() and claims.read_text(encoding="utf-8", errors="replace").count("\n|") <= 2:
        missing.append(f"{display_path(claims, root)} (no filled claim rows found)")

    transcript = topic_dir / "transcript.md"
    if transcript.exists() and "not transcribed yet" in transcript.read_text(encoding="utf-8", errors="replace").lower():
        missing.append(f"{display_path(transcript, root)} (still marked not transcribed)")

    root_transcript = root / "transcripts" / f"{topic}.md"
    if root_transcript.exists() and "not transcribed yet" in root_transcript.read_text(encoding="utf-8", errors="replace").lower():
        missing.append(f"{display_path(root_transcript, root)} (still marked not transcribed)")

    source_media_dir = root / "videos to transcribe" / topic
    if not blocker and source_media_dir.exists() and not has_any_file(source_media_dir):
        missing.append(f"{display_path(source_media_dir, root)} (no source media file found)")

    evidence_dirs = [topic_dir / "audio", topic_dir / "frames", topic_dir / "evidence", topic_dir / "ocr"]
    if not blocker and all(not has_any_file(directory) for directory in evidence_dirs):
        missing.append(
            f"{display_path(topic_dir, root)} (no extracted audio, frame, OCR, or evidence files found)"
        )

    status = "PASS"
    exit_code = 0
    if missing:
        status = "BLOCKED" if blocker else "NO_GO"
        exit_code = 2 if blocker else 1
    elif warnings and blocker:
        status = "BLOCKED"
        exit_code = 2

    audit = topic_dir / "audit.md"
    topic_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Audit",
        "",
        f"- Date: {dt.date.today().isoformat()}",
        f"- Topic: {topic}",
        f"- Status: {status}",
        "",
        "## Missing Required Items",
    ]
    lines.extend([f"- `{item}`" for item in missing] or ["- None"])
    lines.extend(["", "## Warnings"])
    lines.extend([f"- {item}" for item in warnings] or ["- None"])
    if status == "BLOCKED":
        lines.extend(["", "## Blocker", "- A blocker is documented in the topic notes. State it clearly to the user."])
    audit.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{status}: {audit}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
