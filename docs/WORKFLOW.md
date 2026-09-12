# Workflow

## 1. Intake

Choose a stable topic slug. Log every supplied link in both `incoming links/links.md` and the topic's `links.md`. Record the platform, publication context, visible caption, date, speaker or company, and any sales or sponsorship context.

## 2. Choose the research route

Run Agent Reach's route check before a platform-specific or multi-backend task. Prefer a source API for structured records, Exa for discovery, and Jina Reader for ordinary public pages. Use Crawl4AI only when rendering or structured extraction is still needed on an ordinary public page.

OpenCLI is for an existing browser session the user has explicitly authorized. Do not export cookies, tokens, headers, or profile data. A route health check is not proof that the target source was acquired.

The detailed map and stop conditions are in `docs/TOOLCHAIN.md`.

## 3. Acquire media lawfully

Prefer a user-provided file or an official API for owned media. A public downloader is acceptable only where access and download are permitted. A signed-in browser route requires explicit authorization and must not export credentials or cookies into the packet.

Validate the resulting file with `file` and `ffprobe`. An HTML login response saved with a video extension is not media.

If acquisition fails, record the attempted route and a short error summary. Stop after the documented retry boundary and ask for the file.

## 4. Preserve transcript and visual evidence

Create a timestamped transcript and mark uncertain words. Keep a second transcript copy at the workspace root. Extract frames for scene changes, charts, labels, documents, products, and material on-screen claims. Run OCR only on frames where the text matters.

Keep lawful raw artifacts private. Do not edit evidence frames beyond documented private legibility adjustments. No source-video imagery may be included in any deliverable, website, repository, or archive.

## 5. Build the claim table

For each material claim, record:

- timestamp;
- exact quote or careful paraphrase;
- type, such as factual, causal, predictive, anecdotal, advice, product, medical, legal, financial, or opinion;
- evidence that would prove or disprove it;
- current status and uncertainty.

## 6. Check the evidence scope

Record minimal source attribution and what each cited source can establish. Separate vendor descriptions from independent tests. Assess relevance, methods, and missing evidence; do not score the person's reputation, character, popularity, or motives.

## 7. Research both directions

Prefer official records, papers, datasets, product documentation, court filings, regulator pages, and direct statements. Build the strongest support and the strongest counterargument. Keep every used source in `links.md` with a purpose and access date.

## 8. Write the report

Keep the PDF short. Include the bottom line, source claim, minimal attribution, evidence for and against, evidence quality, gaps, likelihood, confidence, and questions. Use original explanatory diagrams, never source-video imagery or recreations.

The report template lives at `.agents/skills/video-claim-research/references/report-template.md`.

## 9. Audit

Read the publication policy, inspect all final pages, and complete `publication-review.json` for the exact report hash. Run the packet audit. A nonzero exit is a real stop condition:

- `PASS`: required artifacts exist and no mechanical blocker was found.
- `BLOCKED`: a documented external blocker remains.
- `NO_GO`: required packet work is missing without a documented blocker.

The audit is a deterministic floor. It does not independently verify the research judgment.
