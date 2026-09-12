# Publication policy

Applies to every delivered research report and public website, PDF, preview, repository, download, and archive made with this workflow.

## Original visuals only

Never export imagery from a source video: frames, screenshots, thumbnails, clips, faces, logos, crops, traces, or generated recreations. A quotation purpose, public source, attribution, or experimental label does not override this project rule.

Use original diagrams, charts, timelines, and tables that explain relationships in the analysis. Label them as original explanatory visuals, not observed results or source evidence. Keep their editable source and provenance. Do not invent measurements, reproduce the video's visual composition, or imitate its interface.

Lawfully acquired video, audio, transcript, OCR, and frames may remain in the private research packet for verification. Inspect them there; never copy them into a delivered PDF, website asset, repository, or ZIP. Public source links and necessary, proportionate textual quotations or paraphrases remain possible after a separate rights and privacy review. Attribution alone is not permission.

## Evaluate the claim

Assess evidence relevance, independence, methods, limitations, claim likelihood, and confidence. Keep the source link and minimal attribution needed to locate it. Vendor documentation establishes what a vendor states, not independent performance proof.

Do not score a person's reputation or credibility, investigate unrelated biography, infer honesty from audience size, or speculate about motives. Identify a documented commercial relationship only when directly necessary to explain a specific source's evidential limitations. An experimental label describes test status; it does not excuse unsupported factual allegations or rights violations.

## Delivery review

1. Inspect every final PDF page and public asset, including previews, thumbnails and embedded files. Search extracted report text for personal ratings and unnecessary personal information.
2. Record source, purpose, and rights for textual citations and any third-party code. Keep a monitored correction route.
3. Complete `publication-review.json` in the private topic folder only after review. Record `policy_version: 1`, `original_visuals_only: true`, `claim_focused: true`, `rights_privacy_reviewed: true`, `reviewer`, `reviewed_at`, and the exact `report_sha256`. A scaffold's false values are intentional blockers.
4. Run the packet audit. It verifies the recorded review and exact file hash, not copyright entitlement or the accuracy of human judgment. Rebuilding the PDF invalidates the previous review.
5. For the portable public example, also run the public-release checker. It checks every visual against `publication-manifest.json`; a changed hash or unregistered file blocks packaging. A manifest is provenance evidence, not proof of originality by itself.

Keep a private rollback snapshot outside the publish directory before replacing previous public assets. Historical private source packets need not be erased. Never describe a historical audit as approval of newly changed content or as legal clearance.
