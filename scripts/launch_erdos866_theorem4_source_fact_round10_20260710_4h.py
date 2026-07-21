#!/usr/bin/env python3
"""Launch the final unconditional CES75 Theorem 4 source assembly."""

from launch_erdos866_even_dichotomy_round10_20260710_4h import REPO, launch
import launch_erdos866_even_dichotomy_round10_20260710_4h as base


base.RUN_ROOT = (
    REPO
    / "artifacts/open_problem_screening/latest/erdos866_theorem4_source_fact_round10_20260710_4h"
)
base.TARGET_FILE = base.WORKSPACE / "MathProject/ErdosFiveQueue20260704.lean"
base.TARGET_THEOREM = "CES75Theorem4IntegerSixWitnessUpperSourceFact"
base.SLUG = "erdos866-theorem4-source-fact"
base.RUN_NAME = "erdos866-theorem4-source-fact-supervised-4h"
base.STATEMENT = """\
# Erdos #866: unconditional CES75 Theorem 4 integer source fact

Prove the exact Lean theorem
`CES75Theorem4IntegerSixWitnessUpperSourceFact` in
`MathProject/ErdosFiveQueue20260704.lean`.

The complete even-count source statement is now verified by
`CES75EvenCountDichotomySourceExistsFact`.  Compose it with the already
verified local theorems:
- `CES75EvenCountDichotomySourceImpliesFinalWindowCertificate`;
- `CES75K5DichotomyToIntegerSixWitnessUpperSourceChain`;
- `CES75K5CertificateFeedsEvenCountDichotomyWrapper`.

The result must inhabit the exact proposition
`CES75Theorem4IntegerSixWitnessUpperSourceStatement` with no hypotheses.  This
is the final audit that the former external `hsrc` dependency has disappeared
from the source-facing upper theorem.

Do not weaken the proposition, add assumptions, or reproduce source/spec
markers.  Use the configured single-file verifier only.  Do not add `sorry`,
`admit`, axioms, constants, opaque declarations, source markers, or new trusted
assumptions.  The supervisor must review every round.
"""
base.HEADER = """\
theorem CES75Theorem4IntegerSixWitnessUpperSourceFact :
    CES75Theorem4IntegerSixWitnessUpperSourceStatement
"""


if __name__ == "__main__":
    import json

    print(json.dumps(launch(), indent=2, ensure_ascii=False, sort_keys=True))
