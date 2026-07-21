#!/usr/bin/env python3
"""Launch the supervised large-even CES75 branch for Erdos #866."""

from launch_erdos866_even_dichotomy_round10_20260710_4h import REPO, launch
import launch_erdos866_even_dichotomy_round10_20260710_4h as base


base.RUN_ROOT = (
    REPO
    / "artifacts/open_problem_screening/latest/erdos866_large_even_branch_round10_20260710_4h"
)
base.TARGET_THEOREM = "ces75_large_even_count_hasPairwiseSums"
base.SLUG = "erdos866-large-even-branch"
base.RUN_NAME = "erdos866-large-even-branch-supervised-4h"
base.STATEMENT = """\
# Erdos #866: close the CES75 large-even direct branch

Prove the exact Lean theorem `ces75_large_even_count_hasPairwiseSums` in
`MathProject/ErdosProblem866Core.lean`.

This theorem closes the first direct alternative in the source-faithful
even-count dichotomy: for sufficiently large `n`, if at least `n/100` elements
of `A` are even, the already verified CES75 Lemma A corollary supplies six
distinct positive witnesses whose pairwise sums lie in `A`.

Required route:
- let `B := A.filter fun x => Even x`;
- use `ces75_fFunPos_six_lt_linear` at `2*n` and
  `ces75_fFunPos_mono` to bound the threshold at
  `B.max' - B.min'`;
- derive nonemptiness and diameter at least `2` from the large cardinality and
  evenness of `B`;
- derive positivity from `A ⊆ Icc 1 (2*n)` and evenness;
- apply the imported verified theorem `ceslemgeneral_pos 6` to `B`;
- convert `HasPosPairwiseSums B 6` to `HasPairwiseSums A 6` using the existing
  conversion and monotonicity lemmas.

An oversized explicit `Nlarge` is acceptable.  Do not assume a Lemma A source
contract: use the actual Lean theorem `ceslemgeneral_pos`.  Do not weaken the
conclusion or change `n/100` to a stronger hypothesis.  Use the configured
single-file verifier only.  Do not add `sorry`, `admit`, axioms, constants,
opaque declarations, source markers, or new trusted assumptions.  The
supervisor must review every round and keep retargeting faithful to this exact
branch.
"""
base.HEADER = """\
theorem ces75_large_even_count_hasPairwiseSums :
    ∃ Nlarge : Nat, ∀ (A : Finset Int) (n t : Nat),
      Nlarge ≤ n →
      A ⊆ Finset.Icc (1 : Int) (2 * (n : Int)) →
      t = (A.filter fun x => Even x).card →
      (n : Real) / 100 ≤ (t : Real) →
      HasPairwiseSums A 6
"""


if __name__ == "__main__":
    import json

    print(json.dumps(launch(), indent=2, ensure_ascii=False, sort_keys=True))
