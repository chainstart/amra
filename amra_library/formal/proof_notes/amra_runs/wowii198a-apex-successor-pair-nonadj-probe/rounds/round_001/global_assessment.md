# ARA Global Reassessment Trigger

The Lean formalizer made no strict-audit progress on the current stage target.
Before continuing, the campaign supervisor must reassess the proof decomposition and choose the next theorem-level blocker.

## Main Objective

Verify the active Lean theorem longest_path_missed_vertex_two_attachments_successors_not_adj in Wowii198aLeftmost.lean, proving the successor-pair forbidden edge by reversing the predecessor rotation theorem.

## Current Targets

- Current stage theorem: `longest_path_missed_vertex_two_attachments_successors_not_adj`
- Final theorem: `longest_path_missed_vertex_two_attachments_successors_not_adj`
- Formalizer status: `partial`
- Formalizer stop reason: `time_budget_exhausted`
- Attempts completed: 7
- Needs reassessment: True

## Strict-Audit Blockers

- Target theorem `longest_path_missed_vertex_two_attachments_successors_not_adj` was not found in the Lean workspace.

## Backend Next-Target Signals

- rerun with backend=codex

## Attempt Score Trace

- Attempt 1: progress_delta=-1000000, build=failed, verified=False
- Attempt 2: progress_delta=0, build=failed, verified=False
- Attempt 3: progress_delta=0, build=failed, verified=False
- Attempt 4: progress_delta=0, build=failed, verified=False
- Attempt 5: progress_delta=0, build=failed, verified=False
- Attempt 6: progress_delta=0, build=failed, verified=False
- Attempt 7: progress_delta=0, build=timeout, verified=False

## Required Global Decision

- Decide whether the current stage theorem is still the right immediate target.
- If it is too broad, replace it with the first smaller theorem that directly plugs into the final proof chain.
- The replacement must be a theorem-level target, not another loose local lemma.
- Provide the replacement as a Lean declaration in a `Formalization target:` or `open_continuation_target` field.
- Explain how the replacement theorem will be used to close the prior stage theorem.
- Freeze or demote routes that only add build-clean local lemmas without changing the main target state.
