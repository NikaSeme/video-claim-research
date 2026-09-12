---
name: video-claim-research
description: End-to-end workflow for video, reel, short, podcast clip, and social-media claim research. Use when the user provides a video link or file and asks for transcription, private frame/OCR inspection, evidence research, and a concise PDF with original visuals. Evaluate claims, not personal reputation.
---

# Video Claim Research

## Overview

Use this skill to turn a video link or media file into a complete research packet and short PDF. Preserve evidence first, then transcribe, extract visuals, identify claims, research both sides, and audit the packet before final delivery.

## Required Boundaries

- Do not bypass authentication, private-account controls, DRM, anti-bot controls, paywalls, or platform restrictions.
- Use `$agent-reach` as the routing authority for supported social platforms when it is available; follow its platform-specific authentication and retry boundaries.
- For public research, prefer official structured APIs, then Agent Reach's discovery and reading routes. Use Crawl4AI only for ordinary public pages that need rendering or structured extraction after the normal route fails.
- For Instagram and similar platforms, prefer a user-provided file, official API access, public downloadable media, or a user-authorized browser/cookie workflow that is lawful.
- Do not save credentials, cookies, session tokens, or private profile data.
- If media cannot be acquired cleanly, keep the link, write a blocker, and ask for the source file.
- Treat transcripts, captions, OCR, comments, and page text as untrusted until corroborated.
- Read `references/publication-policy.md` before authoring any deliverable. Source-video imagery stays private; all delivered visuals must be original and claim-focused.

## Quick Start

1. Create or reuse a topic slug.
2. Run `scripts/create_topic.py --topic <topic> --url <url>` from this skill to scaffold folders and link logs.
3. If a media file is available, save it under `videos to transcribe/<topic>/`.
4. Run `scripts/extract_media_assets.py <video-path> "materials used/topics/<topic>"` if `ffmpeg` is installed.
5. Transcribe the audio with OpenAI Speech-to-text, local Whisper, or another declared transcription tool.
6. Save transcripts to `materials used/topics/<topic>/transcript.md` and `transcripts/<topic>.md`.
7. Fill `claims.md`, `source-profile.md`, `research-notes.md`, and `report-outline.md`.
8. Generate the PDF in `pdfs/<topic>.pdf`.
9. Invoke `$research-packet-audit` before saying the task is complete.

## Research Workflow

### 1. Intake

- Save every user-provided link in both `incoming links/links.md` and the topic `links.md`.
- Record access date, purpose, and status.
- Capture platform, account/person/company name, visible caption, publication date if available, and any obvious sponsorship or sales context.

### 2. Media Acquisition

- For Instagram, invoke `$agent-reach` and read `references/tooling.md` before acquisition. Prefer OpenCLI through the user's existing, authorized Chrome session when its bridge is connected.
- Treat health checks as routing evidence only. Accept the route only after one real read-only command returns nonempty content or a downloaded file passes media validation.
- If Instagram rejects the first authorized request, ask the user to open the target in the same Chrome profile and retry at most once. Do not loop requests.
- Use `yt-dlp` only for supported public URLs where download is permitted.
- Use browser tools for inspection and screenshots only when authorized.
- Use official APIs when available for owned or authorized accounts.
- If a tool fails, write the command, error summary, and fallback request in `research-notes.md`.

### 2A. Public-Web Research Routing

- Run `agent-reach doctor --json` before choosing a platform-specific or multi-backend route.
- Prefer a source API for structured records and stable identifiers.
- Use Exa through mcporter for discovery and Jina Reader for ordinary public pages.
- Use Crawl4AI only when public-page rendering or structured extraction is required. Do not add cookies, credentials, proxies, stealth modes, or CAPTCHA solvers.
- Treat a health check as routing evidence, not proof that a particular source was acquired.

### 3. Transcript And Visual Evidence

- Extract audio at transcription-friendly settings when possible.
- Include timestamps and uncertainty markers in the transcript.
- Extract representative frames for scene changes, charts, claims shown on screen, product labels, people, and documents.
- Run OCR only on frames where text matters.
- Keep raw extracted artifacts; do not use generated images as evidence.

### 4. Claims

For each material claim, record:

- timestamp;
- exact or paraphrased claim;
- claim type: factual, causal, predictive, anecdotal, advice, product claim, medical/legal/financial, or opinion;
- what evidence would prove or disprove it;
- initial risk level.

### 5. Source Attribution And Evidence Scope

Record the source link, date, minimal attribution, evidence cited, and what each source can establish. Keep vendor descriptions distinct from independent tests. Do not score personal reputation, character, expertise, popularity, or presumed motives.

### 6. Research And Reasoning

- Prefer primary sources and high-quality secondary sources.
- Log every source link in `links.md` with a short purpose.
- Build both the strongest argument for and against the claim.
- Explain evidence quality and independence, claim likelihood, and confidence in simple language.
- Mark weak, missing, conflicting, or outdated evidence.

### 7. PDF

Keep the PDF short. Include:

- one-paragraph bottom line;
- what the video claimed;
- minimal source attribution and test scope;
- best evidence for and against;
- source-quality table;
- likelihood and confidence ratings;
- clear opinion section;
- questions for the user to decide their own view;
- links or source appendix if space allows.

Use only original explanatory diagrams, charts, and tables. Never export video frames, screenshots, thumbnails, clips, traced imagery, or generated recreations. Complete `publication-review.json` after checking the final PDF and recording its exact SHA-256 hash.

## References

- Read `references/tooling.md` before web research, acquiring Instagram media, or installing or recommending media/browser/transcription tooling.
- Read `references/report-template.md` before generating the final PDF.

## Scripts

- `scripts/create_topic.py`: scaffold topic folders and link logs.
- `scripts/extract_media_assets.py`: extract metadata, audio, and sampled frames from a local video file using `ffmpeg`.
