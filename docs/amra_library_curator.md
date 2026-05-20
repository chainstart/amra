# AMRA Library Curator

`python3 -m amra library curate` reviews AMRA library candidates without mutating the checked-in Lean library. It is a verified-only promotion gate: accepted records must come from `verified_declarations.json`, must pass faithful-modeling checks when a faithfulness report is supplied, and must carry reusable Lean statement metadata.

## Inputs

The `--candidates` directory may be one of:

- a faithfulness audit directory containing `faithfulness_report.json`
- an AMRA result bundle containing `verified_declarations.json`
- a harvest directory containing `library_harvest_candidates.json`

Natural-language proof sketches, blocked formalization evidence, and budget-guarded proof-loop results are review context only. They are never promoted as library facts.

## Outputs

The curator writes these artifacts under `--out`:

- `library_curator_report.json`: summary, verified-only policy, accepted and rejected records
- `curator_review_records.jsonl`: one review decision per candidate
- `reusable_lemma_metadata.json`: reusable lemma metadata for accepted candidates
- `promoted_library_candidates.json`: promotion-ready candidate payload
- `rejection_reasons.json`: rejected candidates and reason counts
- `summary.md`: human-readable review summary

Result-bundle export copies these files when they are present in a project, and marks them as non-claim-source artifacts. Downstream consumers must still use `verified_declarations.json` as the only Lean-verified claim source.
