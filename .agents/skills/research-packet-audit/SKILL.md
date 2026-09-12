---
name: research-packet-audit
description: Validate video claim research packets before final delivery. Use when a topic folder, transcript, links log, evidence set, source notes, or PDF should be checked for missing artifacts, incomplete link purposes, undocumented blockers, or completion claims.
---

# Research Packet Audit

## Overview

Use this skill before saying a video research packet is complete. It checks that the workspace contains the required evidence, source logs, transcript files, research notes, and final PDF or a clear blocker.

## Audit Rule

Do not claim completion when the audit reports `NO_GO`. If it reports `BLOCKED`, state the blocker and the exact missing user input or external access needed.

## Workflow

1. Identify the topic slug.
2. Run:

   ```bash
   python3 .agents/skills/research-packet-audit/scripts/audit_topic.py <topic>
   ```

3. Before a final-PDF audit, inspect every PDF page and complete `publication-review.json` under the video skill's publication policy. Private source frames must not enter deliverables. Record the exact PDF hash and check that ratings concern the claim and evidence, never the person.
4. Read the generated `materials used/topics/<topic>/audit.md`.
5. Fix missing artifacts and rerun the audit.
6. Only final-report the task as done when status is `PASS`.

## What The Audit Checks

- topic folder exists under `materials used/topics/<topic>/`;
- `links.md` exists and contains at least one URL with a purpose;
- required research files exist;
- root transcript exists in `transcripts/`;
- source media folder exists in `videos to transcribe/<topic>/`;
- final PDF exists in `pdfs/<topic>.pdf`, unless the audit is run with `--skip-pdf`;
- the final PDF has a completed original-visuals, claim-focus, and rights/privacy review tied to its exact hash; this verifies a review record, not legal clearance or research accuracy;
- any blocker is explicit and visible in `audit.md` or topic notes.

## Script

- `scripts/audit_topic.py`: writes a markdown audit report and exits nonzero for `NO_GO` or `BLOCKED`.
