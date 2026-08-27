#!/usr/bin/env python3
"""Exact rational checks for the Erdős #451 parametric frontier derivation.

This script checks algebraic identities and finite symbolic samples only.  The
all-k asymptotic theorem is proved in evidence/parametric_frontier_proof.md.
"""

from fractions import Fraction
import json


def u(theta: Fraction, r: int) -> Fraction:
    return 1 - (1 - theta) * Fraction(2 * r - 1, 3 * r - 2)


def additive_exponent(theta: Fraction, r: int) -> Fraction:
    return Fraction(1, r) + (1 - theta) * Fraction(r - 1, r * (3 * r - 2))


def checks() -> dict:
    theta = Fraction(21, 40)
    frontier = (1 - theta) / 3
    old_coarse_candidate = (1 - theta) / 6

    assert frontier == Fraction(19, 120)
    assert old_coarse_candidate == Fraction(19, 240)

    # Substitution identities for the two leading terms.  If
    # log_k(n r! lambda^r)=r+u, their exponents are equal.
    identities = []
    for th in (Fraction(2, 5), theta, Fraction(3, 5)):
        for r in range(3, 101):
            ur = u(th, r)
            exponent_a = (ur - 1) / (2 * r - 1)
            exponent_b = (th - ur) / (r - 1)
            target = -(1 - th) / (3 * r - 2)
            assert exponent_a == target
            assert exponent_b == target
        identities.append({"theta": str(th), "r_range": [3, 100], "status": "exact"})

    # The exponent controlling r*lambda is decreasing in integer r>=3.
    monotonicity = []
    for th in (Fraction(2, 5), theta, Fraction(3, 5)):
        values = [additive_exponent(th, r) for r in range(3, 1001)]
        assert all(a > b for a, b in zip(values, values[1:]))
        assert values[0] == Fraction(9, 21) - Fraction(2, 21) * th
        monotonicity.append(
            {
                "theta": str(th),
                "maximum_r": 3,
                "maximum": str(values[0]),
                "gap_to_theta": str(th - values[0]),
            }
        )

    assert theta - additive_exponent(theta, 3) == Fraction(41, 280)
    assert Fraction(2, 5) - additive_exponent(Fraction(2, 5), 3) == Fraction(1, 105)

    return {
        "status": "passed",
        "scope": "exact rational algebra and finite monotonicity samples; not an all-parameter proof",
        "theta_bhp": str(theta),
        "frontier": str(frontier),
        "decimal_frontier": float(frontier),
        "old_coarse_candidate": str(old_coarse_candidate),
        "leading_term_identities": identities,
        "additive_exponent_samples": monotonicity,
        "symbolic_monotonicity_numerator": "d/dr ((r-1)/(r(3r-2))) = (-3r^2+6r-2)/(r(3r-2))^2 < 0 for r>=2",
        "margins_at_theta_21_40": {
            "frontier_identity": "(1-theta)-3*(19/120)=0",
            "additive_theta_minus_h3": str(theta - additive_exponent(theta, 3)),
            "third_term_frontier_vs_one_half": str(Fraction(1, 2) - frontier),
        },
    }


if __name__ == "__main__":
    print(json.dumps(checks(), indent=2, sort_keys=True))
