# ARA Campaign Loop Stage Goal

Round: 1 of 1
Stage: `lean_formalizer`

## Main Objective

WOWII198a main-source frontier: from the original source-bound branch b(G)=diam(G)+2 and b(G)<=2+average eccentricity, derive indepNum<=3 together with the active longest-path two-sided local-nonadjacency trichotomy or terminal residual, using only single-file Lean checking.

## Targets

- Current stage theorem: `source_bound_b_eq_diam_add_two_forces_longest_path_two_sided_local_nonadj_frontier`
- Final theorem: `source_bound_b_eq_diam_add_two_forces_longest_path_two_sided_local_nonadj_frontier`
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
