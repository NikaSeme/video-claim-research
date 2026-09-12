#!/usr/bin/env python3
"""Scaffold a video claim research topic folder."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "topic"


def ensure_file(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def append_link(path: Path, row: str, url: str) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if url and url not in text:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(row)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True, help="Topic name or slug.")
    parser.add_argument("--url", action="append", default=[], help="Source URL to log. Repeatable.")
    parser.add_argument("--root", default=".", help="Workspace root.")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="Access date.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    topic = slugify(args.topic)
    topic_dir = root / "materials used" / "topics" / topic

    for directory in [
        root / "pdfs",
        root / "transcripts",
        root / "incoming links",
        root / "videos to transcribe" / topic,
        topic_dir / "audio",
        topic_dir / "frames",
        topic_dir / "evidence",
        topic_dir / "ocr",
    ]:
        directory.mkdir(parents=True, exist_ok=True)

    incoming = root / "incoming links" / "links.md"
    ensure_file(
        incoming,
        "# Incoming Links\n\n| Date added | Link | Topic | Purpose | Status |\n|---|---|---|---|---|\n",
    )

    links = topic_dir / "links.md"
    ensure_file(
        links,
        f"# Links: {topic}\n\n| Date accessed | Link | Purpose | Notes |\n|---|---|---|---|\n",
    )

    for url in args.url:
        append_link(
            incoming,
            f"| {args.date} | {url} | {topic} | User-provided source link. | Stored. |\n",
            url,
        )
        append_link(
            links,
            f"| {args.date} | {url} | User-provided source video link. | Stored for processing. |\n",
            url,
        )

    ensure_file(
        topic_dir / "claims.md",
        "# Claims\n\n| Timestamp | Claim | Type | Evidence needed | Status |\n|---|---|---|---|---|\n",
    )
    ensure_file(topic_dir / "transcript.md", "# Transcript\n\nStatus: not transcribed yet.\n")
    ensure_file(root / "transcripts" / f"{topic}.md", f"# Transcript: {topic}\n\nStatus: not transcribed yet.\n")
    ensure_file(
        topic_dir / "source-profile.md",
        "# Source Attribution\n\n- Source link and date:\n- Minimal attribution:\n- Evidence cited:\n- Scope and limits of verification:\n- Independence of evidence (not a rating of the person):\n",
    )
    ensure_file(
        topic_dir / "research-notes.md",
        "# Research Notes\n\n## Acquisition\n\n## Evidence For\n\n## Evidence Against\n\n## Gaps And Blockers\n",
    )
    ensure_file(
        topic_dir / "report-outline.md",
        "# Report Outline\n\n## Bottom Line\n\n## Claims\n\n## Evidence\n\n## Opinion\n\n## Questions\n",
    )
    ensure_file(topic_dir / "audit.md", "# Audit\n\nStatus: not audited yet.\n")
    ensure_file(topic_dir / "publication-review.json", json.dumps({
        "policy_version": 1, "original_visuals_only": False,
        "claim_focused": False, "rights_privacy_reviewed": False,
        "reviewer": "", "reviewed_at": "", "report_sha256": ""
    }, indent=2) + "\n")

    print(f"topic={topic}")
    print(f"topic_dir={topic_dir.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
