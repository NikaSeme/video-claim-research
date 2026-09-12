# Third-party projects and credits

No third-party source repository is vendored here. The workflow calls or recommends the projects below, which remain under their own licences. Canonical repository names, URLs, default-branch commits, and GitHub licence files were checked on 6 September 2026. A checked commit records the review snapshot; it is not a required installation version.

| Role | Project | Checked commit | Licence note |
|---|---|---|---|
| Social-platform routing | [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | `da5044d26fc6adddb6554d5679c94ac22e76e428` | MIT |
| Authorised browser-backed platform CLI | [jackwener/OpenCLI](https://github.com/jackwener/OpenCLI) | `8271afc67e8504bda94c147f446ee29775d08274` | Apache-2.0 |
| MCP command runner used by Agent Reach routes | [openclaw/mcporter](https://github.com/openclaw/mcporter) | `8644694338db8f30624d07933e8a68141cfcc7f8` | MIT; the former `steipete/mcporter` URL currently redirects here. |
| Exa search MCP server | [exa-labs/exa-mcp-server](https://github.com/exa-labs/exa-mcp-server) | `15ffb50519e719dc791cdc750ce5ed1934c0a1ed` | MIT |
| Public-page rendering and extraction fallback | [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) | `862f6bccb9c063f49b9d42701baa0eea17a4993f` | Apache-2.0 |
| Ordinary public-page reading | [Jina Reader](https://jina.ai/reader/) | Hosted service | No Jina source code is redistributed here. |
| Public-media download where permitted | [yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp) | `bbc809a1161d3bfca51fa36f59dda35556ee85a0` | Unlicense |
| Media inspection and extraction | [FFmpeg/FFmpeg](https://github.com/FFmpeg/FFmpeg) | `f93cd72dde3056c2efb39e11589745d78cd24409` | Licence depends on build options; FFmpeg documents LGPL/GPL combinations. No FFmpeg code is redistributed here. |
| Local transcription | [openai/whisper](https://github.com/openai/whisper) | `86098128c0b4f24f0e2aa2994de830614b474227` | MIT |
| Faster local transcription | [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) | `ed9a06cd89a93e47838f564998a6c09b655d7f43` | MIT |
| Scene detection | [Breakthrough/PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | `24953b0bf76af17c450bc143d330eea48fc5e276` | BSD-3-Clause |
| OCR | [tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract) | `fb87a84b6e3384b424b2169c76de9031046861e9` | Apache-2.0 |
| Browser automation through MCP | [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | `8a13ef8e9f7385a0f89477922127f31cbfde9761` | Apache-2.0 |
| Browser inspection through MCP | [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | `086299a69e6d322df43d7e54417fce25b3a2fc08` | Apache-2.0 |
| Optional Instagram helper | [instaloader/instaloader](https://github.com/instaloader/instaloader) | `543469296ec61e49c4e1d34edac39f043b16a5f1` | MIT |
| Optional gallery/social helper | [mikf/gallery-dl](https://github.com/mikf/gallery-dl) | `2adf2a8e0041ec55afdcc2211fd5c7ca239a9352` | GPL-2.0; referenced only and not linked into this repository. |
| PDF rendering and inspection during QA | [Poppler](https://poppler.freedesktop.org/) | Installed tool | GPL-2.0-only or GPL-3.0-only in the checked Homebrew metadata; not redistributed here. |

The offline smoke-test PDF is generated with [ReportLab](https://www.reportlab.com/), version 4.4.9 in the checked environment, under its BSD-style license. Poppler is used only to render and inspect PDFs during QA.

## Public case-study content

`examples/elu-mcp-claim-check/` contains an original report, two original explanatory SVG diagrams, and four rendered report pages. The September publication revision contains no source-video imagery or personal ratings. The eight source links support textual attribution and verification, not a licence to reuse those works. See `CONTENT_NOTICE.md` and `publication-manifest.json` in that folder.

Listing a tool does not grant permission to download or process a particular item. Platform rules, copyright, privacy, and user authorisation still apply.
