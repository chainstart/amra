# ARA Global Reassessment Trigger

The Lean formalizer made no strict-audit progress on the current stage target.
Before continuing, the campaign supervisor must reassess the proof decomposition and choose the next theorem-level blocker.

## Main Objective

Lean verification probe for source_bound_b_eq_diam_add_two_forces_longest_path_refined_apex_pattern_frontier in Wowii198aLeftmost.lean.

## Current Targets

- Current stage theorem: `source_bound_b_eq_diam_add_two_forces_longest_path_refined_apex_pattern_frontier`
- Final theorem: `source_bound_b_eq_diam_add_two_forces_longest_path_refined_apex_pattern_frontier`
- Formalizer status: `partial`
- Formalizer stop reason: `attempts_exhausted`
- Attempts completed: 8
- Needs reassessment: True

## Strict-Audit Blockers

- Lean build status is `failed`, not `passed`.

## Backend Next-Target Signals

- rerun with backend=codex

## Attempt Score Trace

- Attempt 1: progress_delta=0, build=failed, verified=False
- Attempt 2: progress_delta=0, build=failed, verified=False
- Attempt 3: progress_delta=0, build=failed, verified=False
- Attempt 4: progress_delta=0, build=failed, verified=False
- Attempt 5: progress_delta=0, build=failed, verified=False
- Attempt 6: progress_delta=0, build=failed, verified=False
- Attempt 7: progress_delta=0, build=failed, verified=False
- Attempt 8: progress_delta=0, build=failed, verified=False

## Required Global Decision

- Decide whether the current stage theorem is still the right immediate target.
- If it is too broad, replace it with the first smaller theorem that directly plugs into the final proof chain.
- The replacement must be a theorem-level target, not another loose local lemma.
- Provide the replacement as a Lean declaration in a `Formalization target:` or `open_continuation_target` field.
- Explain how the replacement theorem will be used to close the prior stage theorem.
- Freeze or demote routes that only add build-clean local lemmas without changing the main target state.
