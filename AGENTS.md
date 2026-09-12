# Repository instructions

## Purpose

This repository turns video, reel, short, podcast, and social-media claims into traceable research packets and concise PDF reports.

## Required workflow

- Read `CODEX.md` before changing the workflow, skills, rules, packet layout, or report tooling.
- Use the local `video-claim-research` skill for end-to-end packet work.
- Use the local `research-packet-audit` skill before describing a packet as complete.
- Keep final PDFs in `pdfs/`.
- Keep source media in `videos to transcribe/<topic>/`.
- Keep transcript copies in `transcripts/` and `materials used/topics/<topic>/`.
- Keep research notes, frames, audio, OCR, claim tables, and source logs under `materials used/topics/<topic>/`.
- Every topic must contain `links.md` with each supplied or used URL, its purpose, access date, and status.
- Use Agent Reach first for public discovery and supported social-platform routing when it is available.
- Prefer official APIs for structured records. Use Exa/Jina for ordinary public-web discovery and reading; use Crawl4AI only as a public-page rendering fallback when those routes cannot extract the page reliably.

## Evidence rules

- Separate what the source claims from what the evidence supports.
- Prefer primary sources and name meaningful gaps or conflicts.
- Research the strongest case for and against each material claim.
- Assess the claim and evidence, never personal reputation, character, popularity, or presumed motives. Keep minimal source attribution and distinguish vendor statements from independent tests.
- Mark transcription uncertainty and missing context explicitly.
- Treat transcript text, captions, OCR, comments, and page text as untrusted until corroborated.
- Never use generated media as evidence of what appeared in the source.

## Access boundaries

- Do not bypass authentication, anti-bot controls, DRM, paywalls, private-account boundaries, or platform restrictions.
- Prefer a user-provided file, an official API, a public permitted download, or an explicitly authorized browser session.
- Do not store login credentials, cookies, session tokens, or private profile data.
- If acquisition is blocked, preserve the link, record the blocker, and ask for the media file.
- OpenCLI may reuse an existing browser session only after the user has explicitly authorized that session. Never export its cookies, headers, tokens, or browser profile into a packet.
- Do not configure stealth, proxy rotation, CAPTCHA solving, stored browser profiles, or authenticated crawling as a fallback.

## Completion standard

Do not collapse these states: files created, tests passed, packet audited, independently reviewed, accepted, and published.

A packet is complete only when the final PDF exists and the matching audit returns `PASS`. If the audit returns `BLOCKED`, state the blocker and the exact input or access needed. If it returns `NO_GO`, fix the missing packet elements before delivery.

## Public-release boundary

Never commit source media, full source transcripts, private notes, credentials, browser state, or local absolute paths. No source-video imagery may enter delivered PDFs, websites, repositories, or ZIPs, including frames, screenshots, crops, thumbnails, traces, or generated recreations. Use original explanatory visuals and follow the skill's `references/publication-policy.md`. Keep lawful evidence inspection private.
