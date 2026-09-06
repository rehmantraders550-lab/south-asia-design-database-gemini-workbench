# Gemini handoff — South Asia design database

## Session requirement

Start a brand-new Gemini CLI chat/session for this repository. Do not continue an older Gemini conversation. Treat this file as the complete task brief.

## Private data

The private `data-pack` is intentionally excluded from GitHub. Use the local pack supplied by the user, placed beside this file. Do not upload the pack or any sensitive research and permissions metadata to a public location.

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

## Required return to the originating assistant

When finished, write `GEMINI_COMPLETION.md` in the repository. Include:

- every changed record and source ID;
- evidence used and canonical URLs;
- all rights, consent, and AI-training permission decisions;
- records that remain uncertain or need review;
- the final validator result.

Commit the completion report and enriched files to this private repository. Then send a concise findings summary in this new Gemini chat and include the commit hash so the originating assistant can read the report back. Do not claim completion if the private pack was unavailable or validation failed.
