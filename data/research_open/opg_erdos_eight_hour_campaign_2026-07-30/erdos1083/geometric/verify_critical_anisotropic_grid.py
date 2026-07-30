#!/usr/bin/env python3
"""Exact certificate for the critical coaxial affine-line barrier."""

from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from math import comb


def circles(radius_count: int, height_count: int, ratio: int = 2):
    """Integer coaxial-circle parameters (radius, height)."""

    if radius_count < 1 or height_count < 1 or ratio < 2:
        raise ValueError("need positive counts and an integer ratio >= 2")
    # The scale height_count separates radial-offset blocks:
    # nonzero differences of squared radial offsets are >= height_count^2,
    # whereas squared height differences are < height_count^2.
    return tuple(
        (height_count * ratio**u, z)
        for u in range(radius_count)
        for z in range(height_count)
    )


def parameter_multiplicities(
    radius_count: int, height_count: int, ratio: int = 2
) -> Counter[tuple[int, int]]:
    points = circles(radius_count, height_count, ratio)
    multiplicities: Counter[tuple[int, int]] = Counter()
    for i, (r, z) in enumerate(points):
        for s, w in points[i:]:
            multiplicities[((r - s) ** 2 + (z - w) ** 2, 2 * r * s)] += 1
    return multiplicities


def exact_formula(radius_count: int, height_count: int) -> dict[str, int]:
    """Closed forms for the number of lines and their collision energy."""

    L = radius_count
    m = height_count
    square_sum = (m - 1) * m * (2 * m - 1) // 6
    diagonal_energy = m * m + square_sum
    cross_energy = m * m + 4 * square_sum
    return {
        "circle_count": L * m,
        "raw_unordered_pairs": L * m * (L * m + 1) // 2,
        "distinct_parameter_lines": m * comb(L + 1, 2),
        "parameter_energy": (
            L * diagonal_energy + comb(L, 2) * cross_energy
        ),
        "maximum_multiplicity": (
            m if L == 1 else max(m, 2 * (m - 1))
        ),
    }


def enumerated_ledger(
    radius_count: int, height_count: int, ratio: int = 2
) -> dict[str, int]:
    multiplicities = parameter_multiplicities(
        radius_count, height_count, ratio
    )
    return {
        "circle_count": radius_count * height_count,
        "raw_unordered_pairs": sum(multiplicities.values()),
        "distinct_parameter_lines": len(multiplicities),
        "parameter_energy": sum(value * value for value in multiplicities.values()),
        "maximum_multiplicity": max(multiplicities.values()),
    }


def critical_family(t: int) -> dict[str, int | str]:
    """L=t, m=S=t^2, hence N=t^5 and all audited bounds have scale t^3."""

    if t < 2:
        raise ValueError("need t >= 2")
    L = t
    m = t * t
    formula = exact_formula(L, m)
    return {
        "t": t,
        "radius_count_L": L,
        "height_multiplicity_m": m,
        "angular_pattern_size_S": m,
        "circle_count_F": formula["circle_count"],
        "point_count_N": formula["circle_count"] * m,
        "distinct_parameter_lines_M": formula["distinct_parameter_lines"],
        "parameter_energy": formula["parameter_energy"],
        "maximum_line_multiplicity": formula["maximum_multiplicity"],
        "all_pairs_ST_scale_sqrt_SM": (
            "sqrt(t^2 * (t^4+t^3)/2)=Theta(t^3)=Theta(N^(3/5))"
        ),
        "equal_radius_scale_S_sqrt_m": "t^3=N^(3/5)",
        "line_threshold": "M=Theta(t^4)=Theta(F^(4/3))",
        "energy_threshold": "E=Theta(t^8)=Theta(F^(8/3))",
    }


def chebyshev_value(cosine: Fraction, index: int) -> Fraction:
    """Return T_index(cosine) by the exact three-term recurrence."""

    if index < 0:
        raise ValueError("index must be nonnegative")
    if index == 0:
        return Fraction(1)
    if index == 1:
        return cosine
    left, right = Fraction(1), cosine
    for _ in range(2, index + 1):
        left, right = right, 2 * cosine * right - left
    return right


def exact_affine_union_count(t: int, cosine: Fraction) -> int | None:
    """Count A+B(1-cos(k theta)), including zero.

    The value zero occurs once as a distinct value (at zero angular and
    height/radius difference).  Thus the corresponding count of nonzero
    distances is exactly one smaller.  Return ``None`` if angular values
    repeat.
    """

    S = t * t
    angular = tuple(
        Fraction(1) - chebyshev_value(cosine, k) for k in range(S)
    )
    if len(set(angular)) != S:
        return None
    parameters = parameter_multiplicities(t, t * t)
    return len(
        {
            Fraction(intercept) + Fraction(slope) * x
            for intercept, slope in parameters
            for x in angular
        }
    )


def rational_cosine_search(t: int, maximum_denominator: int = 20) -> dict:
    """Finite exact pressure test; it is not used in either theorem."""

    candidates = []
    for denominator in range(2, maximum_denominator + 1):
        cosine = Fraction(denominator - 1, denominator)
        count = exact_affine_union_count(t, cosine)
        if count is not None:
            candidates.append((count, denominator))
    if not candidates:
        raise AssertionError("no distinct angular progression was tested")
    best_count, best_denominator = min(candidates)
    return {
        "t": t,
        "cosine": f"{best_denominator - 1}/{best_denominator}",
        "affine_union_count": best_count,
        "nonzero_distance_count": best_count - 1,
        "parameter_line_count": exact_formula(t, t * t)[
            "distinct_parameter_lines"
        ],
        "angular_size": t * t,
        "critical_N_three_fifths": t**3,
        "status": (
            "finite exact evidence that the line-count extremizer need not "
            "extremize the full affine union"
        ),
    }


def two_adic_angular_escape(height_count: int, angular_size: int) -> dict:
    """Certified lower bound for cos(theta)=3/4 from reduced denominators."""

    if height_count < 1 or angular_size < 1:
        raise ValueError("counts must be positive")
    valuation = 0
    remaining = height_count
    while remaining % 2 == 0:
        valuation += 1
        remaining //= 2
    usable_angles = max(0, angular_size - 1 - 2 * valuation)
    return {
        "height_count": height_count,
        "angular_size": angular_size,
        "two_adic_valuation_of_height_count": valuation,
        "usable_nonzero_angles": usable_angles,
        "certified_distances": height_count * usable_angles,
    }


def odd_prime_angular_escape(
    height_count: int,
    angular_size: int,
    denominator: int,
    prime: int,
) -> dict:
    """Certified bound when an odd prime divides the reduced cosine denominator."""

    if height_count < 1 or angular_size < 1:
        raise ValueError("counts must be positive")
    if denominator < 2 or prime < 3 or prime % 2 == 0:
        raise ValueError("need a positive denominator and an odd prime")

    denominator_valuation = 0
    remaining_denominator = denominator
    while remaining_denominator % prime == 0:
        denominator_valuation += 1
        remaining_denominator //= prime
    if denominator_valuation == 0:
        raise ValueError("prime must divide the denominator")

    height_valuation = 0
    remaining_height = height_count
    while remaining_height % prime == 0:
        height_valuation += 1
        remaining_height //= prime

    discarded_angles = (2 * height_valuation) // denominator_valuation
    usable_angles = max(0, angular_size - 1 - discarded_angles)
    return {
        "height_count": height_count,
        "angular_size": angular_size,
        "denominator": denominator,
        "prime": prime,
        "prime_valuation_of_denominator": denominator_valuation,
        "prime_valuation_of_height_count": height_valuation,
        "usable_nonzero_angles": usable_angles,
        "certified_distances": height_count * usable_angles,
    }


def exponent_ledger() -> dict[str, str]:
    """Critical exponents and the strongest surviving off-balance gain."""

    return {
        "critical_scaling": "L=t,m=S=t^2,F=t^3,N=t^5,M=Theta(t^4)",
        "in_N": "S=N^(2/5),F=N^(3/5),M=Theta(N^(4/5))",
        "all_pairs_ST": "sqrt(SM)=N^(3/5)",
        "equal_radius": "S*sqrt(m)=N^(3/5)",
        "planar_slice": "F/log(F)=N^(3/5-o(1))",
        "general_alpha_M": (
            "if m=F^alpha,L=F^(1-alpha), then M=Theta(F^(2-alpha))"
        ),
        "general_alpha_ST_exponent": "4/5-(3/10)alpha",
        "general_alpha_equal_radius_exponent": "2/5+(3/10)alpha",
        "combined_exponent": "3/5+(3/10)*abs(alpha-2/3)",
        "fixed_gain_condition": (
            "|alpha-2/3|>=delta gives f_3(N)>=N^(3/5+3delta/10-o(1)) "
            "inside this synchronized structured family"
        ),
        "threshold_duality": str(
            (
                Fraction(2, 5)
                + Fraction(3, 5) * Fraction(4, 3)
            )
            / 2
        ),
    }


def main() -> None:
    records = []
    for t in range(2, 7):
        formula = exact_formula(t, t * t)
        enumerated = enumerated_ledger(t, t * t)
        if formula != enumerated:
            raise AssertionError((t, formula, enumerated))
        records.append(critical_family(t))
    print(
        json.dumps(
            {
                "schema": "amra.erdos1083.critical_anisotropic_grid.v1",
                "records": records,
                "rational_cosine_searches": [
                    rational_cosine_search(t) for t in range(2, 6)
                ],
                "two_adic_escape": [
                    {
                        "t": t,
                        **two_adic_angular_escape(t * t, t * t),
                    }
                    for t in range(2, 13)
                ],
                "odd_prime_escape": [
                    {
                        "t": t,
                        **odd_prime_angular_escape(t * t, t * t, 3, 3),
                    }
                    for t in range(2, 13)
                ],
                "exponent_ledger": exponent_ledger(),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
