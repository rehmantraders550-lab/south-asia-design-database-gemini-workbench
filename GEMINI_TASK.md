# Gemini handoff — South Asia design database

Use this repository as the working copy. The private pack is the only baseline dataset.

## Completed first half

- Offline validation completed: 45 records, 46 sources, and 43 relationships.
- Structural validation pass: `true`.
- The current review queue contains 19 records.
- 20 source entries have no URL or local path.

## Complete the remaining work

1. Resolve source labels only when a canonical source can be verified. Never guess a URL.
2. Enrich queued records with locality, maker, technique, provenance, rights, consent, and AI-training permission.
3. Keep observation, interpretation, inference, and recommendation separate.
4. Keep `review_status=needs_review` until evidence supports promotion.
5. Update the JSON, JSONL, manifest, catalogue index, and QA outputs together.
6. Run `python south_asia_workbench.py validate --pack data-pack` before committing.

## Hard boundary

Do not invent cultural meanings, attribution, dates, permissions, or source URLs. Do not authorize model training or reuse when permission is `not_determined`. Do not broaden beyond India, Pakistan, Bangladesh, Sri Lanka, Nepal, Bhutan, and Maldives without explicit user instruction.

## Expected completion

Commit the enriched pack and a short `GEMINI_COMPLETION.md` describing every changed record, source, permission decision, and remaining uncertainty.
