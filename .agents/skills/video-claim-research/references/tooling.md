# Tooling Reference

Use this reference when choosing tools for video claim research.

## Agent Reach Routing

Use `$agent-reach` as the routing authority for supported social platforms and multi-backend public research. Do not infer that an installed command can reach a specific source.

Check routing first:

```bash
agent-reach doctor --json
```

`active_backend: null` is not by itself a failure because Doctor may avoid live calls. Choose the documented backend, then require one successful read-only result or a validated download before calling that route usable.

## Public Web Discovery And Reading

Use this order:

1. an official or source API when it exposes the needed structured record;
2. Exa through `mcporter` for discovery;
3. Jina Reader for an ordinary public page;
4. Crawl4AI when browser rendering or structured extraction is still required.

Example commands:

```bash
mcporter call exa.web_search_exa query="claim and primary source" numResults=5
curl -s "https://r.jina.ai/https://example.com/public-page"
crwl crawl "https://example.com/public-page"
```

Keep Crawl4AI unauthenticated and public-page-only. Do not configure stored browser profiles, cookies, credentials, proxies, stealth or undetected modes, CAPTCHA solvers, or authenticated crawling. Record a blocker when ordinary public access remains unavailable.

## OpenCLI

OpenCLI is a browser-backed route for platforms where the user has explicitly authorized an existing browser session. Never request, export, or store cookies, credentials, session headers, or browser-profile data.

```bash
opencli doctor
```

Require a connected bridge and a real read-only result. Follow any repository-local adapter verification rule when one exists.

## Media

- `ffmpeg`: extract audio, frames, metadata, clips, and thumbnails.
- `ffprobe`: inspect streams, duration, codecs, and metadata.
- `yt-dlp`: download supported public media where permitted.
- `gallery-dl` and `instaloader`: social/Instagram media helpers; unofficial and only for authorized use.

Common commands:

```bash
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4
ffmpeg -y -i input.mp4 -vn -ac 1 -ar 16000 audio.wav
ffmpeg -y -i input.mp4 -vf fps=1/5 frames/frame_%04d.jpg
```

## Transcription

- OpenAI Speech-to-text API is preferred when an API workflow is available.
- Local fallback: `openai/whisper` or `SYSTRAN/faster-whisper`.
- Always mark uncertainty for noisy audio, music-heavy clips, overlapping speech, or translated audio.
- Never treat auto-transcripts as perfect evidence.

## Browser Access

- Use Jina Reader or the Codex in-app browser for public pages that do not require sign-in.
- Use Chrome extension, Chrome DevTools MCP, or Playwright MCP only when a browser workflow is needed and authorized.
- For signed-in sites, avoid storing secrets and do not export cookies into the research packet.

## Instagram

Safe routes:

1. user provides the downloaded video file;
2. official Instagram Graph API is available for owned or authorized media;
3. user explicitly authorizes their existing browser session and OpenCLI reports its bridge connected;
4. public URL works with `yt-dlp` without bypassing restrictions.

For the authorized OpenCLI route:

```bash
opencli instagram download "INSTAGRAM_URL" --path "/tmp/agent-reach-instagram"
rg --files /tmp/agent-reach-instagram
file "/tmp/agent-reach-instagram/SHORTCODE/DOWNLOADED_FILE"
ffprobe -v error -show_format -show_streams -of json "/tmp/agent-reach-instagram/SHORTCODE/DOWNLOADED_FILE"
```

Require a nonempty video or image file rather than an HTML/login response. If the first request fails, ask the user to open the target in the same logged-in Chrome profile and retry once. Do not default to `instaloader` or `gallery-dl`, rotate undocumented Instagram query IDs, or loop requests.

If none of these applies, write a blocker and ask for the media file.
