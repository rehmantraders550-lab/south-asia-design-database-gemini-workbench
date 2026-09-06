#!/usr/bin/env python3
"""Validate the private South Asia design pack and prepare Gemini's handoff.

This first-half workbench is intentionally offline: it reads only the bundled
JSON files and never fetches sources. Gemini can use the generated handoff to
complete source resolution and record enrichment in a later, user-authorized
step.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def load_pack(pack_dir: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    records = read_json(pack_dir / "records.json")
    sources = read_json(pack_dir / "sources.json")
    relationships = read_json(pack_dir / "relationships.json")
    return records, sources, relationships


def validate(pack_dir: Path) -> dict[str, Any]:
    records, sources, relationships = load_pack(pack_dir)
    record_items = records.get("records", [])
    source_items = sources.get("sources", [])
    relationship_items = relationships.get("relationships", [])
    record_ids = [item.get("record_id") for item in record_items]
    source_ids = {item.get("source_id") for item in source_items}
    duplicate_record_ids = sorted({item for item in record_ids if record_ids.count(item) > 1})
    duplicate_source_ids = sorted(
        {item.get("source_id") for item in source_items if [s.get("source_id") for s in source_items].count(item.get("source_id")) > 1}
    )
    missing_source_refs = sorted(
        {source_id for item in record_items for source_id in item.get("source_ids", []) if source_id not in source_ids}
    )
    record_id_set = set(record_ids)
    invalid_relationship_refs = [
        {"from": item.get("from_record_id"), "to": item.get("to_record_id")}
        for item in relationship_items
        if item.get("from_record_id") not in record_id_set or item.get("to_record_id") not in record_id_set
    ]
    needs_review = [item.get("record_id") for item in record_items if item.get("review_status") == "needs_review"]
    unresolved_sources = [item.get("source_id") for item in source_items if not item.get("url") and not item.get("local_path")]
    return {
        "record_count": len(record_items),
        "source_count": len(source_items),
        "relationship_count": len(relationship_items),
        "needs_review_count": len(needs_review),
        "needs_review_ids": needs_review,
        "unresolved_source_count": len(unresolved_sources),
        "unresolved_source_ids": unresolved_sources,
        "duplicate_record_ids": duplicate_record_ids,
        "duplicate_source_ids": duplicate_source_ids,
        "missing_source_refs": missing_source_refs,
        "invalid_relationship_refs": invalid_relationship_refs,
        "pass": not any(
            [duplicate_record_ids, duplicate_source_ids, missing_source_refs, invalid_relationship_refs]
        ),
    }


def prepare_gemini(pack_dir: Path, output_path: Path) -> None:
    report = validate(pack_dir)
    handoff = f"""# Gemini handoff — South Asia design database

Use this repository as the working copy. The private pack is the only baseline dataset.

## Completed first half

- Offline validation completed: {report['record_count']} records, {report['source_count']} sources, and {report['relationship_count']} relationships.
- Structural validation pass: `{str(report['pass']).lower()}`.
- The current review queue contains {report['needs_review_count']} records.
- {report['unresolved_source_count']} source entries have no URL or local path.

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
"""
    output_path.write_text(handoff, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and hand off the private South Asia design pack.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--pack", type=Path, default=Path("data-pack"))
    handoff_parser = subparsers.add_parser("prepare-gemini")
    handoff_parser.add_argument("--pack", type=Path, default=Path("data-pack"))
    handoff_parser.add_argument("--output", type=Path, default=Path("GEMINI_TASK.md"))
    args = parser.parse_args()
    if args.command == "validate":
        print(json.dumps(validate(args.pack), indent=2, ensure_ascii=False))
    else:
        prepare_gemini(args.pack, args.output)
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
