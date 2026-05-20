# AMRA Proof Stability Benchmark

`python3 -m amra proof-stability benchmark` runs a deterministic local proof-loop stability suite. It is a harness regression target for bounded natural-language and mixed proof search; it does not call live model backends and it does not run unbounded proof search.

The default local fixture suite is `tests/fixtures/proof_stability_suite.yaml`.

## Contract

- Suite schema: `amra.proof_stability.suite.v1`.
- Report schema: `amra.proof_stability.report.v1`.
- Resume record schema: `amra.proof_stability.resume_record.v1`.
- Allowed fixture backends: `none`, `fake`, `deterministic_fixture`.
- Each case must define finite `max_steps` and `time_budget_seconds`.
- Mixed proof-search coverage is tracked through `kind: mixed` cases and route counts for `proof_search`, `closure`, and `focused_attack`.

## Outputs

The benchmark writes:

- `proof_stability_report.json`: suite summary, route counts, taxonomy counts, budget use, and per-case results.
- `proof_stability_resume.jsonl`: start/completion records that make interrupted suite position explicit.
- `cases/<case-id>/result.json`: normalized proof-loop result or budget guard result for each fixture.
- `summary.md`: short human-readable summary.

## Failure Taxonomy

The local taxonomy is intentionally small and stable:

- `none`: expected completed or verified deterministic fixture.
- `budget_exhausted`: case or suite simulated work exceeded its finite budget before dispatch.
- `blocked_formalization_gap`: the route is blocked on a target/formalization gap.
- `partial_proof` and `proof_search_exhausted`: bounded search produced a non-final proof state.
- `runner_failure`: deterministic runner raised or returned a failed status.
- `route_selection_regression`: route selection changed from the expected fixture route.
- `status_mismatch`: reserved for status regression reports.
- `fixture_invalid`, `unexpected_live_backend`, `unbounded_budget`, `unknown_status`: fixture or guard failures.

## Local Command

```bash
python3 -m amra proof-stability benchmark \
  --suite tests/fixtures/proof_stability_suite.yaml \
  --out /tmp/amra_proof_stability \
  --json
```

The command should report `status: passed`, `llm_calls: 0`, and `live_model_calls: false`.
