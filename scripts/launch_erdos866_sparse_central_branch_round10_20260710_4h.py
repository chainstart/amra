#!/usr/bin/env python3
"""Launch the supervised sparse-central CES75 branch for Erdos #866."""

from launch_erdos866_even_dichotomy_round10_20260710_4h import REPO, launch
import launch_erdos866_even_dichotomy_round10_20260710_4h as base


base.RUN_ROOT = (
    REPO
    / "artifacts/open_problem_screening/latest/erdos866_sparse_central_branch_round10_20260710_4h"
)
base.TARGET_THEOREM = "ces75_sparse_central_even_hasPairwiseSums"
base.SLUG = "erdos866-sparse-central-branch"
base.RUN_NAME = "erdos866-sparse-central-branch-supervised-4h"
base.STATEMENT = """\
# Erdos #866: close the CES75 sparse-central-even direct branch

Prove the exact Lean theorem `ces75_sparse_central_even_hasPairwiseSums` in
`MathProject/ErdosProblem866Core.lean`.

This theorem closes the second direct alternative in the source-faithful
even-count dichotomy.  If fewer than half of the even elements lie in the
central interval `[40*t, 2*n - 40*t]`, then more than half lie in the union of
the two endpoint windows.  One endpoint window therefore contains more than
`t/4` even elements and has diameter at most `40*t`; eventual linear domination
of `fFunPos 6` lets the verified CES75 Lemma A corollary produce six witnesses.

Required route:
- let `B := A.filter fun x => Even x`;
- define the lower endpoint subset by `x < 40*t` and the upper endpoint subset
  by `2*n - 40*t < x`;
- prove `Ecent ⊆ B` and bound the noncentral part of `B` by the union of those
  endpoint sets;
- from `2 * Ecent.card < t` and `B.card = t`, prove that one endpoint set has
  cardinality strictly greater than `t/4` (over `Real` or an equivalent exact
  natural inequality);
- prove the selected endpoint set is nonempty, consists of positive even
  integers, and has diameter between `2` and `40*t`;
- use `ces75_fFunPos_six_lt_linear` at `40*t`, then
  `ces75_fFunPos_mono`, and apply the actual theorem
  `ceslemgeneral_pos 6`;
- transport the resulting pairwise-sum witnesses from the endpoint subset to
  `A`.

An oversized explicit `Touter` is acceptable.  The theorem must handle both
endpoint branches; do not assume which side is dense.  Do not replace
`2 * Ecent.card < t` by a stronger condition, and do not introduce a source
contract in place of `ceslemgeneral_pos`.  Use the configured single-file
verifier only.  Do not add `sorry`, `admit`, axioms, constants, opaque
declarations, source markers, or new trusted assumptions.  The supervisor must
review every round and may split only into faithful finite-cardinality helpers
that lead back to this exact theorem.
"""
base.HEADER = """\
theorem ces75_sparse_central_even_hasPairwiseSums :
    ∃ Touter : Nat, ∀ (A Ecent : Finset Int) (n t : Nat),
      Touter ≤ t →
      A ⊆ Finset.Icc (1 : Int) (2 * (n : Int)) →
      t = (A.filter fun x => Even x).card →
      Ecent =
        A.filter (fun x =>
          Even x ∧ 40 * (t : Int) ≤ x ∧
            x ≤ 2 * (n : Int) - 40 * (t : Int)) →
      2 * Ecent.card < t →
      HasPairwiseSums A 6
"""


if __name__ == "__main__":
    import json

    print(json.dumps(launch(), indent=2, ensure_ascii=False, sort_keys=True))
