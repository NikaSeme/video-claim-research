# Open-source boundary

## Included

- General workflow instructions.
- Reusable Codex skills and deterministic scripts.
- Command safety rules.
- Empty folder contracts and templates.
- A release-reviewed public case-study report and rendered report pages.
- Canonical public source URLs used by that report.
- A generated offline smoke-test builder; generated smoke-test media is not committed.
- Upstream credits, licenses, and pinned repository references.

## Excluded

- User-submitted or downloaded source media.
- Full source transcripts, extracted frame folders, OCR, comments, or private working notes.
- Names or profiles of private people.
- Credentials, API keys, cookies, browser sessions, and local configuration.
- Absolute local paths, shell histories, task histories, and workspace logs.
- Full third-party repository clones and their Git histories.
- Live deployment metadata and account identifiers.

## Before each release

1. Run `scripts/check_public_release.py` from the repository root.
2. Inspect `git status --short` and `git diff --cached`.
3. Check binary metadata with `pdfinfo`, `ffprobe`, and `exiftool` when available.
4. Confirm every delivered visual is original explanatory work. Never include source-video imagery, even with a quotation rationale or attribution. Inspect text and code rights separately. Complete the publication manifest; no personal reputation ratings are allowed.
5. Re-check links, dependency licenses, and repository pins.
6. Have another person review the staged release if the repository will represent professional work.
