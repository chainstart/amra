#!/usr/bin/env python3
"""Arithmetic guard for the maximum-witness degree-spread barrier."""

from __future__ import annotations

import json
import math


def choose2(x: int) -> int:
    return x * (x - 1) // 2


def data(n: int, delta: int, degree_spread: int) -> dict[str, int | bool]:
    edges = n * n // 4 + 1
    missing = choose2(n) - edges
    kappa = n - 2 * delta
    maximum = delta + degree_spread
    average_ceiling = (2 * edges + n - 1) // n
    numerator = delta * delta + delta * kappa + n - 3 - missing
    residual_root = (numerator + delta - 2) // (delta - 1)
    parity_cap = 2 * degree_spread - (2 if n % 2 == 0 else 1)
    return {
        "n": n,
        "edges": edges,
        "missing": missing,
        "delta": delta,
        "maximum": maximum,
        "degree_spread": degree_spread,
        "kappa": kappa,
        "average_ceiling": average_ceiling,
        "residual_root": residual_root,
        "parity_cap": parity_cap,
        "maximality_legal": maximum >= average_ceiling,
        "parity_bound": (
            not maximum >= average_ceiling or kappa <= parity_cap
        ),
    }


def common_residual_root(n: int, delta: int, ell: int) -> int:
    if delta <= 1 or ell < 1:
        raise ValueError("the root requires delta>1 and ell>=1")
    edges = n * n // 4 + 1
    missing = choose2(n) - edges
    kappa = n - 2 * delta
    numerator = (
        delta * delta
        + delta * kappa
        + delta
        - 1
        + ell
        - missing
    )
    return (numerator + delta - 2) // (delta - 1)


def degree_cap_lower(
    n: int,
    centre_degree: int,
    maximum_degree: int,
    common_residual: int,
    ell: int,
) -> int:
    """Right-hand side of the disjoint missing-pair budget (4b)."""
    if not 1 <= ell or not 2 <= common_residual:
        raise ValueError("invalid star parameters")
    p = centre_degree
    d = common_residual
    residual_vertices = d - 1
    forced_per_residual = max(0, n - ell - 2 - maximum_degree)
    degree_cap_extra = max(
        0,
        residual_vertices * forced_per_residual
        - choose2(residual_vertices),
    )
    return (
        p * (n - p - d)
        + n
        - p
        - 1
        + residual_vertices * ell
        + degree_cap_extra
    )


def relaxed_degree_cap_lower(
    n: int,
    delta: int,
    degree_spread: int,
    common_residual: int,
) -> int:
    """The p- and ell-free lower bound (17)."""
    d = common_residual
    maximum = delta + degree_spread
    return (
        delta * (n - d - 1 - delta)
        + n
        - 1
        + (d - 1) * (n - 2 - maximum)
        - choose2(d - 1)
    )


def square_root_certificate(max_g: int = 250) -> dict[str, int | bool]:
    """Check the factored parity comparison and sharp scalar endpoints."""
    comparison_rows = 0
    endpoint_rows = 0
    for degree_spread in range(3, max_g + 1):
        g = degree_spread
        for parity in (0, 1):
            cap = 2 * g - (2 if parity == 0 else 1)
            first_kappa = 4 if parity == 0 else 3
            for kappa in range(first_kappa, cap + 1, 2):
                for d in range(2, kappa):
                    # Delta only needs to meet the exact average-degree cap;
                    # delta is otherwise free in the algebraic comparison.
                    delta = g + 3
                    n = 2 * delta + kappa
                    missing = choose2(n) - (n * n // 4 + 1)
                    relaxed = relaxed_degree_cap_lower(n, delta, g, d)
                    h = kappa - d - 1
                    a = 2 * g - kappa
                    if parity == 0:
                        base = delta - g * g + 2 * g + 2
                        factored_remainder = (
                            a * a - 4 + 2 * h * (2 * g - h - 1)
                        )
                    else:
                        base = delta - g * g + 2 * g + 1
                        factored_remainder = (
                            a * a - 1 + 2 * h * (2 * g - h - 1)
                        )
                    assert 4 * (relaxed - missing - base) == factored_remainder
                    assert factored_remainder >= 0
                    comparison_rows += 1

        if g < 4:
            continue
        for parity in (0, 1):
            delta = g * g - 2 * g - (2 if parity == 0 else 1)
            kappa = 2 * g - (2 if parity == 0 else 1)
            n = 2 * delta + kappa
            maximum = delta + g
            d = kappa - 1
            missing = choose2(n) - (n * n // 4 + 1)
            assert relaxed_degree_cap_lower(n, delta, g, d) == missing
            assert degree_cap_lower(n, delta, maximum, d, 1) == missing
            endpoint_rows += 1

    return {
        "max_g": max_g,
        "comparison_rows": comparison_rows,
        "sharp_scalar_endpoint_rows": endpoint_rows,
        "pass": True,
    }


def sharp_endpoint_graph(
    degree_spread: int, parity: str, audit_l4: bool = False
) -> dict[str, int | bool | str]:
    """Construct the graph-level sharp example for (19) or (21)."""
    if degree_spread < 4 or parity not in {"even", "odd"}:
        raise ValueError("requires g>=4 and an even/odd parity")
    g = degree_spread
    is_even = parity == "even"
    delta = g * g - 2 * g - (2 if is_even else 1)
    kappa = 2 * g - (2 if is_even else 1)
    maximum = delta + g
    n = 2 * delta + kappa
    w_size = kappa - 2

    b, c = 0, 1
    pset = list(range(2, 2 + delta))
    uset = list(range(2 + delta, 2 + 2 * delta))
    wset = list(range(2 + 2 * delta, n))
    assert len(wset) == w_size
    edges: set[tuple[int, int]] = set()

    def add_edge(x: int, y: int) -> None:
        assert x != y
        edges.add((min(x, y), max(x, y)))

    for i, x in enumerate(pset):
        add_edge(b, x)
        for y in pset[i + 1 :]:
            add_edge(x, y)
    for i, x in enumerate(uset):
        add_edge(c, x)
        for y in uset[i + 1 :]:
            add_edge(x, y)

    # Consecutive cyclic blocks make every W-degree exactly Delta and
    # balance the right degrees to floor/ceil(|W|Delta/(2delta)).
    right = pset + uset
    assert maximum < len(right)
    for i, x in enumerate(wset):
        for j in range(maximum):
            add_edge(x, right[(i * maximum + j) % len(right)])

    neighbours = [set() for _ in range(n)]
    for x, y in edges:
        neighbours[x].add(y)
        neighbours[y].add(x)
    degrees = [len(row) for row in neighbours]
    target_edges = n * n // 4 + 1
    assert len(edges) == target_edges
    assert min(degrees) == delta
    assert max(degrees) == maximum
    assert neighbours[b] == set(pset)
    assert neighbours[c] == set(uset)
    assert not set(pset) & set(uset)
    assert not any(
        (min(x, y), max(x, y)) in edges for x in pset for y in uset
    )

    witness = wset[0]
    assert degrees[witness] == maximum
    aset = {witness} | neighbours[witness]
    assert b not in aset and c not in aset
    p_support = aset & set(pset)
    u_support = aset & set(uset)
    assert len(p_support) >= g and len(u_support) >= g
    union = neighbours[c]
    complement_b = set(range(n)) - neighbours[b]
    residual = complement_b - union
    assert residual == {b, c} | set(wset)
    assert len(residual) == kappa
    assert degree_cap_lower(
        n, degrees[b], maximum, kappa - 1, 1
    ) == choose2(n) - len(edges)

    # Recolour g pairs b--p_i, c--u_i with g common colours and leave
    # all other edges injective.  The pair b,c is zero-shore, while the
    # elementary missing-star part of its reserve already pays D_B=g.
    bset = set(range(n)) - aset
    d_b_outer = len(neighbours[b] & bset)
    d_c_outer = len(neighbours[c] & bset)
    missing_star_reserve = (
        (len(bset) - 1 - d_b_outer)
        + (len(bset) - 1 - d_c_outer)
        - 1
    )
    assert missing_star_reserve == (
        delta + 2 * kappa - g - 5
    )
    assert missing_star_reserve >= g

    if audit_l4:
        vertices = range(n)
        for first in range(n):
            for second in range(first + 1, n):
                path_sets = {
                    frozenset((one, two, three))
                    for one in neighbours[first] - {second}
                    for two in neighbours[one] - {first, second}
                    for three in (
                        neighbours[two] & neighbours[second]
                    )
                    - {first, one, two}
                }
                assert path_sets
                eligible = [
                    item
                    for item in vertices
                    if item not in {first, second}
                ]
                assert not set.intersection(
                    *(set(path) for path in path_sets)
                )
                for deleted_first in eligible:
                    avoiding_first = [
                        set(path)
                        for path in path_sets
                        if deleted_first not in path
                    ]
                    assert avoiding_first
                    assert not set.intersection(*avoiding_first)

    return {
        "g": g,
        "parity": parity,
        "n": n,
        "delta": delta,
        "maximum": maximum,
        "kappa": kappa,
        "edges": len(edges),
        "repeated_pair_capacity": min(len(p_support), len(u_support)),
        "recoloured_defect": g,
        "missing_star_reserve": missing_star_reserve,
        "l4_checked": audit_l4,
        "pass": True,
    }


def sharp_graph_certificate(max_g: int = 20) -> dict[str, int | bool]:
    rows = 0
    for g in range(4, max_g + 1):
        for parity in ("even", "odd"):
            assert sharp_endpoint_graph(g, parity)["pass"]
            rows += 1
    return {"max_g": max_g, "graph_rows": rows, "pass": True}


def endpoint_conservation(
    parity: str,
    ell: int,
    common_residual: int,
    isolated: int,
    high_residual_count: int = 0,
) -> dict[str, int | bool]:
    if parity not in {"even", "odd"}:
        raise ValueError("parity must be even or odd")
    if not 1 <= ell or not 0 <= isolated <= ell:
        raise ValueError("invalid star sizes")
    residual_mass = (
        4 * ell if parity == "even" else 4 * ell + high_residual_count
    )
    synchronization = residual_mass - ell * common_residual
    conserved = (
        synchronization + ell * (isolated - 1)
    )
    closed_formula = (
        (3 - common_residual + isolated) * ell
        + (0 if parity == "even" else high_residual_count)
    )
    return {
        "residual_mass": residual_mass,
        "synchronization": synchronization,
        "conserved": conserved,
        "closed_formula": closed_formula,
        "basepoint_legal": common_residual >= isolated + 2,
        "pass": synchronization >= 0 and conserved == closed_formula,
    }


def exhaustive_certificate(max_n: int = 500) -> dict[str, int | bool]:
    arithmetic_rows = 0
    excluded_g_le_two = 0
    g_three_parameter_rows = 0
    g_three_excluded_rows = 0
    for n in range(7, max_n + 1):
        for delta in range(3, n):
            for degree_spread in range(0, 4):
                row = data(n, delta, degree_spread)
                assert row["parity_bound"]
                if not row["maximality_legal"]:
                    continue
                kappa = int(row["kappa"])
                root = int(row["residual_root"])
                if degree_spread <= 2 and root <= kappa and kappa >= 3:
                    raise AssertionError((n, delta, degree_spread, row))
                if degree_spread <= 2:
                    excluded_g_le_two += 1
                if degree_spread == 3 and root <= kappa and kappa >= 3:
                    if n % 2 == 0:
                        assert kappa == 4 and root == 4
                        m = n // 2
                        assert delta == m - 2
                        assert int(row["maximum"]) == m + 1
                        assert m >= 6
                        for ell in range(1, m - 1):
                            for d in range(2, kappa + 1):
                                if d < common_residual_root(n, delta, ell):
                                    continue
                                if (3 - d) * ell < 0:
                                    continue
                                lower = degree_cap_lower(
                                    n, delta, m + 1, d, ell
                                )
                                assert lower > int(row["missing"]), (
                                    row,
                                    ell,
                                    d,
                                    lower,
                                )
                                g_three_excluded_rows += 1
                    else:
                        assert kappa == 5 and root == 4
                        m = n // 2
                        assert delta == m - 2
                        assert int(row["maximum"]) == m + 1
                        assert m >= 5
                        for ell in range(1, m):
                            for p in (m - 2, m - 1):
                                high_counts = (
                                    range(ell + 1) if p == m - 2 else (0,)
                                )
                                for high_count in high_counts:
                                    for d in range(2, kappa + 1):
                                        if (3 - d) * ell + high_count < 0:
                                            continue
                                        lower = degree_cap_lower(
                                            n, p, m + 1, d, ell
                                        )
                                        assert lower > int(row["missing"]), (
                                            row,
                                            ell,
                                            p,
                                            high_count,
                                            d,
                                            lower,
                                        )
                                        g_three_excluded_rows += 1
                    g_three_parameter_rows += 1
                arithmetic_rows += 1

    endpoint_rows = 0
    for ell in range(1, 31):
        for common_residual in range(2, 6):
            for isolated in range(ell + 1):
                even = endpoint_conservation(
                    "even", ell, common_residual, isolated
                )
                if even["synchronization"] >= 0:
                    assert even["pass"]
                    endpoint_rows += 1
                for high_count in range(ell + 1):
                    odd = endpoint_conservation(
                        "odd",
                        ell,
                        common_residual,
                        isolated,
                        high_count,
                    )
                    if odd["synchronization"] >= 0:
                        assert odd["pass"]
                        endpoint_rows += 1

    return {
        "max_n": max_n,
        "arithmetic_rows": arithmetic_rows,
        "excluded_g_le_two_rows": excluded_g_le_two,
        "g_three_parameter_rows": g_three_parameter_rows,
        "g_three_excluded_scalar_rows": g_three_excluded_rows,
        "endpoint_rows": endpoint_rows,
        "pass": True,
    }


def main() -> int:
    result = exhaustive_certificate()
    result["square_root"] = square_root_certificate()
    result["sharp_graphs"] = sharp_graph_certificate()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
