# AMRA NL/Lean Faithfulness Audit

`python3 -m amra formalization audit-faithfulness` checks whether AMRA's exported Lean declarations faithfully model the natural-language proof obligations in a result bundle. It is deterministic and does not call live model backends.

## Inputs

The audit accepts either:

- An AMRA result bundle containing `problem_metadata.json`, `natural_language_proof_sketches.json`, `verified_declarations.json`, and `lean_build_report.json`.
- A proof-stability benchmark output containing `proof_stability_report.json`.

For result bundles, the strongest check compares the recorded exact Lean formal statement from `problem_metadata.json` or sketch metadata against Lean-verified declaration headers in `verified_declarations.json`.

## Outputs

The audit writes:

- `faithfulness_report.json`: schema `amra.nl_lean_faithfulness.report.v1`, taxonomy counts, checks, and blocked formalization evidence.
- `blocked_formalization_evidence.json`: extracted evidence from Lean build reports, unresolved blockers, proof-attempt ledgers, or proof-stability cases.
- `faithfulness_summary.md`: short human-readable summary.

AMRA result bundle export also writes `faithful_modeling_report.json` into the bundle and links it from `artifact_manifest.json` under `faithful_modeling.audit_report`.

## Taxonomy

- `faithfully_modeled`: a recorded Lean formal statement matches exactly one Lean-verified declaration header.
- `lean_statement_mismatch`: a Lean-verified declaration exists, but no declaration header matches the recorded formal statement.
- `missing_lean_declaration`: an exact formal statement is recorded but no Lean-verified declaration is available.
- `blocked_formalization_gap`: Lean build, blocker, ledger, or proof-stability evidence explains why formalization is blocked.
- `missing_formal_statement`: natural-language obligations exist but no exact Lean formal statement was exported.
- `missing_natural_language_obligation`: Lean declarations exist without an exported natural-language theorem obligation.
- `ambiguous_lean_declaration`: multiple declarations match the same formal statement.
- `informal_only`: natural-language proof evidence exists without Lean verification.
- `budget_guarded`: deterministic budget controls stopped a proof-stability case before unbounded search.
- `proof_search_unresolved` and `unsupported_bundle`: guard classifications for unresolved or invalid audit inputs.

`lean_statement_mismatch` is an audit failure. Blocked formalization evidence is reported as actionable evidence and does not by itself fail the audit.

## Local Command

```bash
python3 -m amra formalization audit-faithfulness \
  --bundle /tmp/amra_proof_stability \
  --out /tmp/amra_faithfulness \
  --json
```

The proof-stability audit should report `status: passed`, distinguish `faithfully_modeled`, `blocked_formalization_gap`, and `budget_guarded`, and record zero live-model calls through the source proof-stability report.
