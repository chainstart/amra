# ARA Campaign Loop Stage Goal

Round: 1 of 1
Stage: `lean_formalizer`

## Main Objective

WOWII198a current Lean target: strengthen the active longest-path dichotomy so each non-residual branch carries two-sided local nonadjacency around both separated attachment indices, without full project compilation.

## Targets

- Current stage theorem: `exists_long_separated_outside_path_or_missed_vertex_two_attachments_with_two_sided_local_nonadj_or_terminal_residual_of_connected_delete_connected`
- Final theorem: `exists_long_separated_outside_path_or_missed_vertex_two_attachments_with_two_sided_local_nonadj_or_terminal_residual_of_connected_delete_connected`
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
