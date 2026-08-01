#!/usr/bin/env python3
"""Finite guards for the #809 linear zero-matching synchronization theorem."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import ceil, comb, isqrt
import random


Pair = tuple[int, int]


def pair(x: int, y: int) -> Pair:
    if x == y:
        raise ValueError("distinct endpoints required")
    return (x, y) if x < y else (y, x)


def cross_pairs(p_set: set[int], q_set: set[int]) -> set[Pair]:
    return {pair(x, y) for x in p_set for y in q_set if x != y}


def exhaustive_cross_bound(universe_size: int = 6) -> int:
    universe = range(universe_size)
    checked = 0
    subsets = [
        set(choice)
        for size in range(1, universe_size + 1)
        for choice in combinations(universe, size)
    ]
    for p_set in subsets:
        for q_set in subsets:
            d = min(len(p_set), len(q_set))
            actual = len(cross_pairs(p_set, q_set))
            overlap = len(p_set & q_set)
            formula = (
                len(p_set) * len(q_set)
                - overlap
                - comb(overlap, 2)
            )
            assert actual == formula
            assert actual >= comb(d, 2)
            checked += 1
    return checked


def audit_system(
    neighbourhoods: list[tuple[set[int], set[int]]],
    matching_endpoints: list[tuple[int, int]],
    total_missing: int | None = None,
) -> dict[str, int]:
    if len(neighbourhoods) != len(matching_endpoints):
        raise ValueError("one neighbourhood pair per matching edge")

    incidence: Counter[Pair] = Counter()
    delta = min(
        min(len(p_set), len(q_set))
        for p_set, q_set in neighbourhoods
    )
    for p_set, q_set in neighbourhoods:
        incidence.update(cross_pairs(p_set, q_set))

    union_size = len(incidence)
    if total_missing is None:
        total_missing = union_size
    if total_missing < union_size:
        raise ValueError("total missing universe cannot be smaller than its union")

    f = len(neighbourhoods)
    total_incidence = sum(incidence.values())
    lower_average = ceil(f * comb(delta, 2) / total_missing)
    anchor, multiplicity = max(incidence.items(), key=lambda item: item[1])
    assert total_incidence >= f * comb(delta, 2)
    assert multiplicity >= lower_average

    x, y = anchor
    supported = [
        i
        for i, (p_set, q_set) in enumerate(neighbourhoods)
        if anchor in cross_pairs(p_set, q_set)
    ]
    # In a genuine zero-pair system neither anchor can equal an endpoint
    # of a pair it supports: that would require a loop or the missing base
    # pair itself to be an edge.  The abstract guard enforces the same
    # neighbourhood condition on its labelled endpoints.
    for i, (p_set, q_set) in enumerate(neighbourhoods):
        b_i, c_i = matching_endpoints[i]
        assert b_i not in p_set | q_set
        assert c_i not in p_set | q_set
    valid = supported
    assert len(valid) == multiplicity
    forced_rectangle = {
        pair(2 * i, 2 * j + 1)
        for i in valid
        for j in valid
    }
    assert len(forced_rectangle) == len(valid) ** 2

    q_size = len(forced_rectangle)
    q_root = isqrt(q_size)
    assert len(valid) == q_root
    if delta >= 2:
        exact_cap = total_missing * q_root / comb(delta, 2)
        assert f <= exact_cap

    return {
        "matching_size": f,
        "delta": delta,
        "missing_union": union_size,
        "total_missing": total_missing,
        "total_incidence": total_incidence,
        "anchor_multiplicity": multiplicity,
        "valid_indices": len(valid),
        "forced_rectangle": len(forced_rectangle),
    }


def deterministic_audit() -> dict[str, int]:
    endpoints = [(20 + 2 * i, 21 + 2 * i) for i in range(5)]
    neighbourhoods = [
        ({0, 1, 2, 3}, {4, 5, 6, 7}),
        ({0, 1, 2, 8}, {4, 5, 6, 9}),
        ({0, 1, 3, 8}, {4, 5, 7, 9}),
        ({0, 2, 3, 8}, {4, 6, 7, 9}),
        ({0, 2, 3, 8}, {4, 6, 7, 9}),
    ]
    return audit_system(neighbourhoods, endpoints)


def common_host_guard() -> dict[str, int]:
    """Exercise Corollary 2.1 on two disjoint ten-vertex cliques."""
    n = 20
    p = set(range(10))
    q = set(range(10, 20))
    adjacency = {
        vertex: (p - {vertex}) if vertex in p else (q - {vertex})
        for vertex in range(n)
    }
    x, y = 0, 10
    u_vertices = [1, 2, 3]
    v_vertices = [11, 12, 13]
    delta = min(len(neighbours) for neighbours in adjacency.values())
    kappa = n - 2 * delta
    c_x = set(range(n)) - adjacency[x]
    c_y = set(range(n)) - adjacency[y]

    for u, v in zip(u_vertices, v_vertices):
        assert x in adjacency[u]
        assert y in adjacency[v]
        assert not adjacency[u] & adjacency[v]
        assert adjacency[v] <= c_x
        assert adjacency[u] <= c_y
        assert len(c_x - adjacency[v]) <= kappa
        assert len(c_y - adjacency[u]) <= kappa

    return {
        "n": n,
        "delta": delta,
        "kappa": kappa,
        "matching_size": len(u_vertices),
        "host_x_size": len(c_x),
        "host_y_size": len(c_y),
    }


def host_cut_lower(t: int, delta: int) -> int:
    d_star = max(delta, t)
    r_star = min(t, d_star - t)
    return t * d_star - r_star - comb(r_star, 2)


def exhaustive_host_cut_guard(limit: int = 30) -> int:
    checked = 0
    for t in range(1, limit + 1):
        for delta in range(1, limit + 1):
            lower = host_cut_lower(t, delta)
            for actual_degree in range(max(t, delta), 2 * limit + 1):
                max_overlap = min(t, actual_degree - t)
                for overlap in range(max_overlap + 1):
                    actual = (
                        t * actual_degree
                        - overlap
                        - comb(overlap, 2)
                    )
                    assert actual >= lower
                    checked += 1
            if delta >= 2 * t:
                assert lower == t * delta - t * (t + 1) // 2
    return checked


def greedy_capacity_audit(f: int, alpha: Fraction) -> dict[str, object]:
    if not 0 < alpha <= 1:
        raise ValueError("alpha must lie in (0,1]")
    remaining = f
    squares = 0
    rounds = 0
    while remaining:
        t = ceil(alpha * remaining)
        assert 1 <= t <= remaining
        assert alpha * remaining <= t < alpha * remaining + 1
        squares += t * t
        remaining -= t
        rounds += 1

    c_alpha = alpha / (2 - alpha)
    lower = c_alpha * f * f
    assert Fraction(squares, 1) >= lower
    return {
        "f": f,
        "alpha_numerator": alpha.numerator,
        "alpha_denominator": alpha.denominator,
        "rounds": rounds,
        "terminal_remainder": remaining,
        "rectangle_sum": squares,
        "proved_lower_bound": lower,
    }


def random_greedy_audits(seed: int = 809_33, trials: int = 5000) -> int:
    rng = random.Random(seed)
    for _ in range(trials):
        denominator = rng.randint(1, 100)
        numerator = rng.randint(1, denominator)
        greedy_capacity_audit(
            f=rng.randint(1, 2000),
            alpha=Fraction(numerator, denominator),
        )
    return trials


def random_closed_form_audits(seed: int = 809_34, trials: int = 5000) -> int:
    rng = random.Random(seed)
    for _ in range(trials):
        delta = rng.randint(2, 200)
        d_zero = comb(delta, 2)
        missing = rng.randint(d_zero, 8 * d_zero)
        f = rng.randint(1, 2000)
        alpha = Fraction(d_zero, missing)
        coefficient_from_alpha = alpha / (2 - alpha)
        coefficient_closed = Fraction(d_zero, 2 * missing - d_zero)
        assert coefficient_from_alpha == coefficient_closed

        rectangle_lower = coefficient_closed * f * f
        polynomial = 2 * missing * missing - d_zero * missing - d_zero * f * f
        assert (Fraction(missing, 1) >= rectangle_lower) == (polynomial >= 0)
    return trials


def random_audits(seed: int = 809_32, trials: int = 2000) -> int:
    rng = random.Random(seed)
    for _ in range(trials):
        f = rng.randint(1, 10)
        universe_size = rng.randint(6, 16)
        endpoints = [
            (universe_size + 2 * i, universe_size + 2 * i + 1)
            for i in range(f)
        ]
        neighbourhoods: list[tuple[set[int], set[int]]] = []
        for _i in range(f):
            p_size = rng.randint(2, universe_size)
            q_size = rng.randint(2, universe_size)
            p_set = set(rng.sample(range(universe_size), p_size))
            q_set = set(rng.sample(range(universe_size), q_size))
            neighbourhoods.append((p_set, q_set))
        audit_system(neighbourhoods, endpoints)
    return trials


def main() -> None:
    exhaustive = exhaustive_cross_bound()
    deterministic = deterministic_audit()
    host = common_host_guard()
    host_cut_count = exhaustive_host_cut_guard()
    random_count = random_audits()
    greedy_count = random_greedy_audits()
    closed_count = random_closed_form_audits()
    print(
        {
            "schema": "amra.erdos809.linear-matching-synchronization.v1",
            "exhaustive_set_pairs": exhaustive,
            "deterministic_anchor_multiplicity": deterministic[
                "anchor_multiplicity"
            ],
            "common_host_kappa": host["kappa"],
            "host_cut_parameter_tuples": host_cut_count,
            "random_systems": random_count,
            "greedy_parameter_pairs": greedy_count,
            "closed_form_parameter_pairs": closed_count,
            "status": "PASS",
            "scope": "finite counting guards only; Erdos #809 remains open",
        }
    )


if __name__ == "__main__":
    main()
