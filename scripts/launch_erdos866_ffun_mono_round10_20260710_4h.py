#!/usr/bin/env python3
"""Launch the supervised CES75 threshold-monotonicity stage for Erdos #866."""

from launch_erdos866_even_dichotomy_round10_20260710_4h import (
    REPO,
    launch,
)
import launch_erdos866_even_dichotomy_round10_20260710_4h as base


base.RUN_ROOT = (
    REPO
    / "artifacts/open_problem_screening/latest/erdos866_ffun_mono_round10_20260710_4h"
)
base.TARGET_THEOREM = "ces75_fFunPos_mono"
base.SLUG = "erdos866-ffun-mono"
base.RUN_NAME = "erdos866-ffun-mono-supervised-4h"
base.STATEMENT = """\
# Erdos #866: public monotonicity of the CES75 Lemma A threshold

Prove the exact Lean theorem `ces75_fFunPos_mono` in
`MathProject/ErdosProblem866Core.lean`.

The core file now imports the already verified CES75 Lemma A development from
`MathProject/ErdosProblem866.lean`.  The imported development contains the
same induction as a private helper `fFunPos_mono_early`; do not attempt to
refer to that private name across modules.  Re-establish its exact public
counterpart so later even-count branches can compare the threshold at an
actual finite-set diameter with a larger endpoint-window bound.

Required route:
- induct on `k` from `3 <= k` using the recursive definition of `fFunPos`;
- handle the explicit `k = 3` branch by monotonicity of square root and real
  fourth powers;
- handle successor branches using square-root monotonicity and the induction
  hypothesis;
- preserve the lower-domain assumption `2 <= x` exactly.

Do not weaken the statement or add assumptions.  Use the configured
single-file verifier only.  Intermediate local lemmas are allowed, but the
final declaration must match the expected target header.  Do not add `sorry`,
`admit`, axioms, constants, opaque declarations, source markers, or new
trusted assumptions.  The supervisor must review every round.
"""
base.HEADER = """\
theorem ces75_fFunPos_mono
    (k : Nat) (hk : 3 ≤ k) (x y : Real)
    (hx : 2 ≤ x) (hxy : x ≤ y) :
    fFunPos k x ≤ fFunPos k y
"""


if __name__ == "__main__":
    import json

    print(json.dumps(launch(), indent=2, ensure_ascii=False, sort_keys=True))
