# ARA Campaign Loop Stage Goal

Round: 1 of 1
Stage: `lean_formalizer`

## Main Objective

Verify the public Lean theorem source_bound_b_eq_diam_add_two_forces_longest_path_apex_obstruction_frontier in Wowii198aLeftmost.lean, upgrading the source-bound frontier from local apex nonadjacency to apex forced-obstruction disjunctions.

## Targets

- Current stage theorem: `source_bound_b_eq_diam_add_two_forces_longest_path_apex_obstruction_frontier`
- Final theorem: `source_bound_b_eq_diam_add_two_forces_longest_path_apex_obstruction_frontier`
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
