# South Asia Design Database — Gemini workbench

This private repository contains the first half of an offline South Asia design database workflow and a handoff for Gemini CLI to complete the remaining evidence work.

## Run locally

```text
python south_asia_workbench.py validate --pack data-pack
python south_asia_workbench.py prepare-gemini --pack data-pack --output GEMINI_TASK.md
```

The validator reads only the bundled pack. It checks record, source, and relationship integrity and reports the review queue.

## Gemini handoff

Open `GEMINI_TASK.md` in Gemini CLI from this repository. Gemini should verify source URLs and enrich queued records with evidence, attribution, provenance, rights, consent, and AI-permission metadata. It must preserve uncertainty and update all pack files together.

No API key, external source, or automatic model-training action is embedded in this repository.
