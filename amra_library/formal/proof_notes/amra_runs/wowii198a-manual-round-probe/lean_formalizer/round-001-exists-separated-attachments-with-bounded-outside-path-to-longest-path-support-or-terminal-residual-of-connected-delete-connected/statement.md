# ARA Campaign Loop Stage Goal

Round: 1 of 1
Stage: `lean_formalizer`

## Main Objective

WOWII198a current Lean target: eliminate the remaining terminal residual or bounded separated outside path branch in AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean without full project compilation.

## Targets

- Current stage theorem: `exists_separated_attachments_with_bounded_outside_path_to_longest_path_support_or_terminal_residual_of_connected_delete_connected`
- Final theorem: `exists_separated_attachments_with_bounded_outside_path_to_longest_path_support_or_terminal_residual_of_connected_delete_connected`
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
