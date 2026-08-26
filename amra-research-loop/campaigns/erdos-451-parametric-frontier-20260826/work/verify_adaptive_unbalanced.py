#!/usr/bin/env python3
"""Log-domain sanity replay for the adaptive unbalanced parameter choice.

This script checks exact algebraic identities and representative asymptotic
inequalities.  It is not a proof of the quantified theorem in the companion
Markdown note.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction


def check_case(theta: Fraction, c: Fraction, q: Fraction, a: Fraction) -> dict:
    assert 0 < theta < 1
    assert 0 < c < a
    assert 3 * q * a < 1 - theta
    assert q > 1

    # L=log(k); choosing L directly avoids constructing an enormous k.
    L = 100_000.0
    ell = math.log(L)
    log_n_max = float(c) * L * L / ell
    log_n_min = (2.0 + float(theta)) * L - math.log(2.0)
    samples = []

    for step in range(41):
        t = step / 40
        log_n = (1 - t) * log_n_min + t * log_n_max
        r = 1
        while True:
            log_nr = log_n + math.lgamma(r + 1)
            log_u = (r + 1) * L - float(q) * (2 * r - 1) * ell
            if log_nr <= log_u:
                break
            r += 1

        assert r >= 2
        log_v = (r + float(theta)) * L + float(q) * (r - 1) * ell
        log_z = max(log_nr, log_v)
        log_lambda = (log_z - log_nr) / r
        log_A = (log_z - (r + 1) * L) / (2 * r - 1)
        log_B = ((r + float(theta)) * L - log_z) / (r - 1)
        log_T3 = (math.log(r + 1) + log_lambda - L) / (2 * r)
        log_additive_ratio = (
            math.log(2 * r) + log_lambda - float(theta) * L + ell
        )

        tolerance = 1e-7
        assert log_A <= -float(q) * ell + tolerance
        assert log_B <= -float(q) * ell + tolerance
        assert log_T3 < -ell
        assert log_additive_ratio < 0
        assert r <= math.ceil(float(a) * L / ell)

        if step in (0, 20, 40):
            samples.append(
                {
                    "position": step,
                    "r": r,
                    "log_lambda": log_lambda,
                    "log_A_over_loglogk": log_A / ell,
                    "log_B_over_loglogk": log_B / ell,
                    "log_T3_over_loglogk": log_T3 / ell,
                    "log_additive_ratio": log_additive_ratio,
                }
            )

    # Exact coefficient bookkeeping behind the invariant and feasibility.
    for r in range(2, 50):
        assert (2 * r - 1) + (r - 1) == 3 * r - 2
        assert q * (r - 1) + q * (2 * r - 1) == q * (3 * r - 2)
        assert q * (r - 1) + q * (2 * r - 3) == q * (3 * r - 4)

    return {
        "theta": str(theta),
        "c": str(c),
        "q": str(q),
        "a": str(a),
        "samples": samples,
    }


def main() -> None:
    cases = [
        (Fraction(21, 40), Fraction(3, 20), Fraction(101, 100), Fraction(31, 200)),
        (Fraction(1, 10), Fraction(7, 25), Fraction(101, 100), Fraction(29, 100)),
        (Fraction(9, 10), Fraction(3, 100), Fraction(101, 100), Fraction(4, 125)),
    ]
    print(
        json.dumps(
            {
                "status": "pass",
                "role": "finite log-domain sanity replay; not theorem evidence",
                "L": 100_000,
                "cases": [check_case(*case) for case in cases],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
