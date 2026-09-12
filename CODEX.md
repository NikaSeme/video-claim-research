# Operational map

`AGENTS.md` is the durable instruction layer. This file explains the working layout and commands.

## Skills

- `.agents/skills/video-claim-research/`: intake, media handling, transcription, frames, claim extraction, evidence research, and PDF planning.
- `.agents/skills/research-packet-audit/`: deterministic packet checks and completion status.

## Folder contract

```text
incoming links/
videos to transcribe/<topic>/
transcripts/<topic>.md
materials used/topics/<topic>/
  links.md
  claims.md
  transcript.md
  source-profile.md
  research-notes.md
  report-outline.md
  audit.md
  audio/
  frames/
  evidence/
  ocr/
pdfs/<topic>.pdf
```

## Commands

```bash
# Scaffold a topic and log source links.
python3 .agents/skills/video-claim-research/scripts/create_topic.py \
  --topic "topic name" --url "https://example.com/source"

# Extract metadata, mono audio, and sampled frames from a local video.
python3 .agents/skills/video-claim-research/scripts/extract_media_assets.py \
  "videos to transcribe/topic/source.mp4" \
  "materials used/topics/topic"

# Audit the completed packet.
python3 .agents/skills/research-packet-audit/scripts/audit_topic.py topic
```

The media command uses argument arrays with `shell=False`. Generated summaries store repository-relative paths when possible so committed examples do not expose a contributor's home directory.

## Tool selection

Use Agent Reach as the routing layer rather than guessing a platform command. For public research, prefer a source API when structured records are available, Exa for discovery, Jina Reader for ordinary pages, and Crawl4AI only when rendering or structured extraction is still needed. Use OpenCLI only for a user-authorized existing browser session.

Use FFmpeg for media processing, a declared speech-to-text system for transcription, and OCR only when visible text matters. The route map is in `docs/TOOLCHAIN.md`; every named upstream project and license is listed in `THIRD_PARTY_NOTICES.md`.
