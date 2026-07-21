#!/usr/bin/env python3
"""Launch the final supervised CES75 even-count dichotomy assembly."""

from launch_erdos866_even_dichotomy_round10_20260710_4h import REPO, launch
import launch_erdos866_even_dichotomy_round10_20260710_4h as base


base.RUN_ROOT = (
    REPO
    / "artifacts/open_problem_screening/latest/erdos866_even_dichotomy_fact_round10_20260710_4h"
)
base.TARGET_FILE = base.WORKSPACE / "MathProject/ErdosFiveQueue20260704.lean"
base.TARGET_THEOREM = "CES75EvenCountDichotomySourceExistsFact"
base.SLUG = "erdos866-even-dichotomy-fact"
base.RUN_NAME = "erdos866-even-dichotomy-fact-supervised-4h"
base.STATEMENT = """\
# Erdos #866: close the complete CES75 even-count dichotomy source statement

Prove the exact Lean theorem `CES75EvenCountDichotomySourceExistsFact` in
`MathProject/ErdosFiveQueue20260704.lean`.

All mathematical branches needed by the source statement are now genuinely
Lean-verified in `ErdosProblem866Core.lean`:
- `ces75_even_count_ge_excess` proves `m <= t`;
- `ces75_large_even_count_hasPairwiseSums` closes the branch
  `n/100 <= t` using the formalized CES75 Lemma A corollary;
- `ces75_sparse_central_even_hasPairwiseSums` closes the branch
  `2 * Ecent.card < t` using endpoint density and the same actual corollary;
- the remaining branch has `t < n/100` and `t <= 2 * Ecent.card`.

Required route:
- extract the thresholds from the two verified direct-branch theorems;
- choose an explicit coefficient, preferably `cCES = 25`, and a sufficiently
  large natural `Nsource` that also forces the sparse-central threshold
  `Touter <= t` from `25 * sqrt n < m` and `m <= t`;
- split on `n/100 <= t`, then on `t <= 2 * Ecent.card`;
- dispatch the two direct cases to the verified branch theorems;
- in the residual case prove
  `12 * sqrt n < Ecent.card` arithmetically from `25 * sqrt n < m`,
  `m <= t`, and `t <= 2 * Ecent.card`;
- return the exact proposition `CES75EvenCountDichotomySourceExistsStatement`.

Do not retain any external source hypothesis: this target must inhabit the
source statement unconditionally from the verified local Lean development.
Do not weaken definitions, add assumptions, or prove a marker proposition.
Use the configured single-file verifier only.  Do not add `sorry`, `admit`,
axioms, constants, opaque declarations, source markers, or new trusted
assumptions.  The supervisor must review every round and keep all intermediate
work directed to this exact final theorem.
"""
base.HEADER = """\
theorem CES75EvenCountDichotomySourceExistsFact :
    CES75EvenCountDichotomySourceExistsStatement
"""


if __name__ == "__main__":
    import json

    print(json.dumps(launch(), indent=2, ensure_ascii=False, sort_keys=True))
