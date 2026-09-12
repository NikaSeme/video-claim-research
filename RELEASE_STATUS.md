# Release status

Initial GitHub release prepared on 12 September 2026 for
[NikaSeme/video-claim-research](https://github.com/NikaSeme/video-claim-research).
The owner approved public MIT publication of the original work.

## Included in this release

Reusable workflow instructions, two repository skills, deterministic Python
helpers, tests, and the original-visual ELU/MCP research example. The example is
a public excerpt, not the complete private research packet or a new product test.

The report's evidence assessment is dated 9 July 2026. Its September publication
revision removed source-video imagery and personal reputation ratings. The
current PDF SHA-256 is
`2ec7b2130afdb96ea26b5f3b3f85be0a4761a2e56d7f781b32e7fb96407c4f4f`.
All seven public visual assets are listed in the example's hash-bound manifest.

## Checks for this release

- Thirteen unit tests pass, including the real scaffold entry point and the
  publication-review, hash-mismatch, extra-frame, embedded-image, and forbidden
  video checks.
- `scripts/check_public_release.py` passes on the exact export prepared for Git.
- A separate release preflight checks every allowlisted file, decoded PDF text,
  PDF and PNG metadata, symlinks, private paths, credential patterns, and email
  addresses. It found no sensitive information in the reviewed export.
- All four current PDF pages were rendered and visually inspected. They contain
  original explanatory diagrams and no source-video imagery.
- This folder starts with clean Git history. Git commit identity uses the owner's
  GitHub noreply address rather than a private mailbox.

The FFmpeg/ReportLab end-to-end smoke test was checked in earlier revisions; it
was not rerun for these release-documentation and ignore-rule changes. No live
transcription, authenticated acquisition, provider connection, or ELU integration
was tested for this release.

## Privacy and licensing boundaries

Source videos, full transcripts, raw frames, browser state, credentials, private
notes, local configuration, and parent-workspace history are excluded. Only the
intended public author credit and contact address are retained. Ignore rules are
a precaution, not a substitute for reviewing every future staged change.

MIT covers original work to the extent the author holds the rights. Referenced
third-party material retains its own terms; see `THIRD_PARTY_NOTICES.md` and the
example's `CONTENT_NOTICE.md`.

These are authoring-assistant checks, not independent security review, legal
clearance, or a guarantee that a scanner will catch every future disclosure.
GitHub publication does not authorize or perform a portfolio website deployment.
