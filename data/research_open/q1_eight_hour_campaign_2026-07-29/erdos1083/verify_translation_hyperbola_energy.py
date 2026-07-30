"""Exact certificates for the resonant translation-hyperbola audit."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from typing import Iterable

import sympy as sp


def difference_counts(values: Iterable[object]) -> Counter:
    values = tuple(values)
    return Counter(a - b for a in values for b in values)


def compatibility(u, v, X, Y):
    return u * u - v * v + 2 * X * u - 2 * Y * v


def hyperbola_energy(values: Iterable[object], X, Y) -> dict:
    """Compute H, additive energy, and both capacity bounds."""
    values = tuple(values)
    counts = difference_counts(values)
    solutions = tuple(
        (u, v)
        for u in counts
        for v in counts
        if compatibility(u, v, X, Y) == 0
    )
    energy = sum(m * m for m in counts.values())
    total = sum(counts[u] * counts[v] for u, v in solutions)
    n = len(values)
    mu_nonzero = max(
        (m for difference, m in counts.items() if difference != 0), default=0
    )
    return {
        "n": n,
        "difference_counts": counts,
        "difference_solutions": solutions,
        "H": total,
        "average_degree": Fraction(total, n * n),
        "additive_energy": energy,
        "mu_nonzero": mu_nonzero,
        "energy_bound": 2 * energy,
        "popular_difference_bound": (
            n * n + 2 * mu_nonzero * n * n + mu_nonzero * n
        ),
    }


def partner_degrees(values: Iterable[object], X, Y) -> dict:
    """Compute every first-edge partner degree directly."""
    values = tuple(values)
    degrees = {}
    for s in values:
        for delta in values:
            degrees[(s, delta)] = sum(
                compatibility(s - beta, gamma - delta, X, Y) == 0
                for beta in values
                for gamma in values
            )
    return {
        "degrees": degrees,
        "sum_degrees": sum(degrees.values()),
        "maximum_degree": max(degrees.values(), default=0),
    }


def arithmetic_progression_certificate(
    n: int, X=Fraction(2), Y=Fraction(1)
) -> dict:
    values = tuple(Fraction(i) for i in range(n))
    result = hyperbola_energy(values, X, Y)
    result.update(partner_degrees(values, X, Y))
    return result


def geometric_progression_certificate(
    n: int, base: int = 2, X=Fraction(2), Y=Fraction(1)
) -> dict:
    values = tuple(Fraction(base**i) for i in range(n))
    result = hyperbola_energy(values, X, Y)
    result.update(partner_degrees(values, X, Y))
    return result


def convex_square_certificate(
    n: int, X=Fraction(2), Y=Fraction(1)
) -> dict:
    values = tuple(Fraction(i * i) for i in range(n))
    result = hyperbola_energy(values, X, Y)
    result.update(partner_degrees(values, X, Y))
    return result


def sat_base_resonant_star(parameter_count: int) -> dict:
    """Build a high-degree resonant star over the exact q=3 SAT base field."""
    X = -sp.Rational(3, 2)
    Y = sp.sqrt(12285) / 2
    R = sp.simplify(X * X - Y * Y)
    values = {sp.Integer(0)}
    witnesses = []
    for parameter in range(1, parameter_count + 1):
        t = sp.Integer(parameter)
        u = sp.simplify((t + R / t) / 2 - X)
        v = sp.simplify((t - R / t) / 2 - Y)
        assert sp.simplify(compatibility(u, v, X, Y)) == 0
        values.add(sp.simplify(-u))
        values.add(sp.simplify(v))
        witnesses.append((t, u, v))

    fixed_degree = sum(
        sp.simplify(compatibility(-beta, gamma, X, Y)) == 0
        for beta in values
        for gamma in values
    )
    return {
        "X": X,
        "Y": Y,
        "R": R,
        "values": values,
        "witnesses": tuple(witnesses),
        "size": len(values),
        "fixed_edge_degree": fixed_degree,
    }


def exponent_ledger() -> dict:
    target_degree = Fraction(2, 5)
    return {
        "target_average_degree": target_degree,
        "forced_total_additive_energy": 2 + target_degree,
        "forced_nonzero_popular_difference": target_degree,
        "ap_average_degree": Fraction(0),
        "difference_sidon_average_degree": Fraction(0),
        "classical_convex_energy_average_bound": Fraction(1, 2),
    }


if __name__ == "__main__":
    for family, builder in (
        ("AP", arithmetic_progression_certificate),
        ("GP", geometric_progression_certificate),
        ("squares", convex_square_certificate),
    ):
        sample = builder(10)
        print(
            family,
            "H=", sample["H"],
            "average=", sample["average_degree"],
            "maximum=", sample["maximum_degree"],
        )
    star = sat_base_resonant_star(5)
    print(
        "SAT resonant star",
        "size=", star["size"],
        "fixed degree=", star["fixed_edge_degree"],
    )
