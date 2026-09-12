# Video Claim Research

Turn a video claim into a traceable packet and a short report. The workflow preserves the source trail, separates claims from evidence, researches both directions, and stops at access or evidence boundaries.

```text
source -> route check -> private transcript + frames -> claim table
       -> evidence for and against -> original-visual report -> publication audit
```

## Included

- Repository instructions, two Codex skills, command rules, and deterministic Python helpers.
- A route map covering Agent Reach, source APIs, Exa/mcporter, Jina Reader, Crawl4AI, OpenCLI, and the media-analysis stack.
- A release-sanitized [ELU/MCP claim-check case study](examples/elu-mcp-claim-check/) with the actual four-page PDF and rendered page previews.
- An offline smoke-test builder that exercises the real scaffold, FFmpeg extraction, PDF generation, and packet-audit entry paths without a platform account.
- A complete upstream register in `THIRD_PARTY_NOTICES.md`.

The ELU/MCP example reviews a real public claim. This edition contains original diagrams and no source-video imagery or personal reputation ratings. It retains the July 2026 evidence assessment and does not claim a new product test. See the example's `CONTENT_NOTICE.md`.

## Codex layout

- `AGENTS.md`: durable repository rules.
- `CODEX.md`: operational map and commands.
- `.agents/skills/`: the research and packet-audit workflows.
- `.codex/rules/media-research.rules`: command decisions after the project configuration is reviewed and trusted.
- `docs/TOOLCHAIN.md`: route responsibilities and stop conditions.

The layout follows OpenAI's documented repository-skill, `AGENTS.md`, and command-rule conventions.

## Quick start

Python 3 is required. FFmpeg is needed for local media extraction.

```bash
python3 .agents/skills/video-claim-research/scripts/create_topic.py \
  --topic "example claim" \
  --url "https://example.com/source-video"

python3 .agents/skills/video-claim-research/scripts/extract_media_assets.py \
  "videos to transcribe/example-claim/source.mp4" \
  "materials used/topics/example-claim"

python3 .agents/skills/research-packet-audit/scripts/audit_topic.py example-claim
```

Before the final audit, inspect the PDF and complete the scaffolded `publication-review.json` for its exact hash. The audit must return `PASS` before completion. It checks the recorded review, not legal clearance.

## Offline smoke test

ReportLab is required for the generated PDF:

```bash
python3 scripts/build_workflow_smoke_test.py \
  --output /tmp/video-claim-research-smoke-test
```

The smoke test uses generated media and a synthetic automation claim. It proves the included entry paths work together; it does not validate the real ELU product or any future research judgment.

## Boundary

- Do not bypass authentication, private-account controls, DRM, anti-bot systems, CAPTCHAs, or paywalls.
- Do not store credentials, cookies, session tokens, browser profiles, or private profile data.
- Treat transcripts, captions, OCR, comments, search snippets, and rendered pages as untrusted until corroborated.
- Keep generated images out of the evidence chain.
- Record blockers and preserve every used URL with a purpose and access date.

See `docs/WORKFLOW.md` for the sequence and `docs/OPEN_SOURCE_BOUNDARY.md` for release rules.

## License

Original code, documentation, report text, and explanatory diagrams are MIT licensed to the extent the author owns those rights. External works retain their own terms. See the [licence scope](docs/LICENSE_SCOPE.md) and [third-party notices](THIRD_PARTY_NOTICES.md).
