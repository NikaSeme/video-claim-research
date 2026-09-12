# Toolchain map

The workflow is a router, not one downloader. It chooses the smallest lawful route that can preserve the source and produce inspectable evidence.

```text
source link or file
        |
        v
Agent Reach route check
        |
        +--> structured source API
        +--> Exa discovery -> Jina Reader
        +--> Crawl4AI public-page fallback
        +--> authorized OpenCLI browser route
        +--> permitted public media via yt-dlp
        |
        v
FFmpeg / ffprobe -> transcript -> frames / OCR
        |
        v
claim table -> evidence for and against -> PDF -> audit
```

## Route responsibilities

| Layer | Job | Stop condition |
|---|---|---|
| Agent Reach | Inspect available backends and select the documented route. | A health check cannot prove target access. |
| Source API | Preserve structured records and stable identifiers. | The API does not expose the required record or authorization is absent. |
| Exa + mcporter | Discover relevant public pages and primary sources. | Search results are leads, not evidence by themselves. |
| Jina Reader | Read an ordinary public page without browser state. | The returned page is incomplete or access-controlled. |
| Crawl4AI | Render or extract an ordinary public page when simpler reading fails. | Authentication, CAPTCHA, paywall, private access, or anti-bot boundary. |
| OpenCLI | Reuse a user-authorized existing browser session for a supported platform. | The bridge is disconnected or the user has not authorized the session. |
| yt-dlp | Acquire permitted public media from a supported source. | Platform, rights, or access restrictions prevent clean acquisition. |
| FFmpeg / ffprobe | Validate media and extract audio, frames, and metadata. | The file is not valid media. |
| Whisper / faster-whisper | Produce a draft transcript with uncertainty markers. | Audio quality is too weak for a reliable transcript. |
| PySceneDetect / Tesseract | Find useful visual transitions and on-screen text. | The output does not materially support a claim. |
| ReportLab / Poppler | Build and visually inspect the report. | The latest render has layout or legibility defects. |

## Evidence rule

A route can retrieve evidence without validating it. Transcripts, OCR, captions, comments, search snippets, and rendered pages remain untrusted until the research packet corroborates them. The packet audit checks structure; it does not certify the judgment.

See `THIRD_PARTY_NOTICES.md` for upstream repositories, canonical links, and license notes.
