#!/usr/bin/env python3
"""Launch the supervised CES75 sublinear-threshold stage for Erdos #866."""

from launch_erdos866_even_dichotomy_round10_20260710_4h import REPO, launch
import launch_erdos866_even_dichotomy_round10_20260710_4h as base


base.RUN_ROOT = (
    REPO
    / "artifacts/open_problem_screening/latest/erdos866_ffun_linear_round10_20260710_4h"
)
base.TARGET_THEOREM = "ces75_fFunPos_six_lt_linear"
base.SLUG = "erdos866-ffun-six-linear"
base.RUN_NAME = "erdos866-ffun-six-linear-supervised-4h"
base.STATEMENT = """\
# Erdos #866: eventual linear domination of the CES75 `k = 6` threshold

Prove the exact Lean theorem `ces75_fFunPos_six_lt_linear` in
`MathProject/ErdosProblem866Core.lean`.

This is the quantitative node needed to turn the already verified CES75 Lemma
A corollary `ceslemgeneral_pos` into the two direct branches of
`CES75EvenCountDichotomySource`.  The recursive threshold `fFunPos 6` is
sublinear, so for sufficiently large natural `n` it is strictly below `n/200`.

Required fidelity:
- unfold the actual recursive definition `fFunPos`; do not replace it by an
  unrelated asymptotic function or assume an unproved comparison theorem;
- an arbitrarily large explicit natural threshold is acceptable;
- intermediate lemmas for fourth-root bounds, square-root bounds, or the
  successive `fFunPos 3`, `4`, `5`, `6` estimates are encouraged;
- reuse the public verified theorem `ces75_fFunPos_mono` when useful;
- preserve the exact strict inequality and natural-cast statement.

The target is a genuine theorem, not a source/spec marker.  Do not weaken it,
add hypotheses beyond the displayed eventual threshold, or prove a `True`
placeholder.  Use the configured single-file verifier only.  Do not add
`sorry`, `admit`, axioms, constants, opaque declarations, source markers, or
new trusted assumptions.  The supervisor must review every round and may
retarget only to faithful quantitative intermediate lemmas that lead back to
this exact theorem.
"""
base.HEADER = """\
theorem ces75_fFunPos_six_lt_linear :
    ∃ Nlinear : Nat, ∀ n : Nat, Nlinear ≤ n →
      fFunPos 6 (n : Real) < (n : Real) / 200
"""


if __name__ == "__main__":
    import json

    print(json.dumps(launch(), indent=2, ensure_ascii=False, sort_keys=True))
