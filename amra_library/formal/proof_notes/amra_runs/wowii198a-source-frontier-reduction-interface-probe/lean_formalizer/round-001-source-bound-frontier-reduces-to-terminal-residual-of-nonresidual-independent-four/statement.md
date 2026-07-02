# ARA Campaign Loop Stage Goal

Round: 1 of 1
Stage: `lean_formalizer`

## Main Objective

WOWII198a global reduction interface: under the original source-bound branch, if both non-residual two-sided local-nonadjacency branches yield an independent set of size four, then only the terminal residual branch remains.

## Targets

- Current stage theorem: `source_bound_frontier_reduces_to_terminal_residual_of_nonresidual_independent_four`
- Final theorem: `source_bound_frontier_reduces_to_terminal_residual_of_nonresidual_independent_four`
- Already verified/excluded stage theorems: `<none yet>`

## Loop Discipline

- Start by reviewing the prior-round history.
- Re-state the current first blocker before doing local work.
- Prefer theorem-level progress over local simplification.
- Freeze or demote routes that repeatedly fail the global audit.
- Do not select any already verified stage theorem as the next target.
- End with a concrete next-stage target.

## Stage Directive

This round is Lean write/verify.
Edit the Lean workspace only as needed to prove the current stage theorem.
If the stage theorem is too broad, introduce proved intermediate lemmas but do not weaken the requested theorem or add trusted assumptions.
Run the configured verifier and report the exact next blocker if not verified.

## Prior History

No prior loop history.
