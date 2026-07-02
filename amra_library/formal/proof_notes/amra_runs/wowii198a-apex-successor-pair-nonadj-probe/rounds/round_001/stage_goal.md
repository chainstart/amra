# ARA Campaign Loop Stage Goal

Round: 1 of 1
Stage: `lean_formalizer`

## Main Objective

Verify the active Lean theorem longest_path_missed_vertex_two_attachments_successors_not_adj in Wowii198aLeftmost.lean, proving the successor-pair forbidden edge by reversing the predecessor rotation theorem.

## Targets

- Current stage theorem: `longest_path_missed_vertex_two_attachments_successors_not_adj`
- Final theorem: `longest_path_missed_vertex_two_attachments_successors_not_adj`
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
