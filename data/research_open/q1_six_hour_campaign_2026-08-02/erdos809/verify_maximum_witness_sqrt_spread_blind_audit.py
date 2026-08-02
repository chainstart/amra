#!/usr/bin/env python3
"""Independent hostile audit for the maximum-witness square-root theorem.

This file deliberately imports nothing from
``verify_maximum_witness_degree_spread.py``.  It reconstructs the scalar
algebra, the endpoint graphs, their recolouring, and the advertised L4(2)
templates from the definitions used in the note under audit.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def c2(x: int) -> int:
    return x * (x - 1) // 2


def edge(x: int, y: int) -> tuple[int, int]:
    assert x != y
    return (x, y) if x < y else (y, x)


def missing_count(n: int) -> int:
    return c2(n) - (n * n // 4 + 1)


def exact_degree_cap_lower(
    n: int, p: int, maximum: int, d: int, ell: int
) -> int:
    w = d - 1
    return (
        p * (n - p - d)
        + n
        - p
        - 1
        + w * ell
        + max(0, w * max(0, n - ell - 2 - maximum) - c2(w))
    )


def relaxed_lower(n: int, delta: int, g: int, d: int) -> int:
    return (
        delta * (n - d - 1 - delta)
        + n
        - 1
        + (d - 1) * (n - 2 - delta - g)
        - c2(d - 1)
    )


def ceil_div(numerator: int, denominator: int) -> int:
    assert denominator > 0
    return -(-numerator // denominator)


def four_charge_certificate() -> dict[str, int | bool]:
    """Check disjoint universes and the only double-count correction.

    In the one-leaf specialization the vertex partition is
    P,Q,{b,c},W.  The fourth family lives on W--(P union Q union W),
    whereas the first three live on P--(Q union {c}), the b-star, and
    W--{c}.  We also exhaust all fourth-family missing graphs up to four
    W vertices and verify that subtracting C(|W|,2) is sufficient.
    """
    rows = 0
    for w_size in range(1, 5):
        b, c = 0, 1
        pset = {2}
        qset = {3}
        wset = set(range(4, 4 + w_size))
        vertices = {b, c} | pset | qset | wset
        f1 = {edge(x, y) for x in pset for y in qset | {c}}
        f2 = {edge(b, y) for y in vertices - pset - {b}}
        f3 = {edge(w, c) for w in wset}
        f4_universe = {
            edge(w, z)
            for w in wset
            for z in pset | qset | wset
            if w != z
        }
        families = (f1, f2, f3, f4_universe)
        for left, right in combinations(families, 2):
            assert left.isdisjoint(right)

        universe = sorted(f4_universe)
        for mask in range(1 << len(universe)):
            absent = {
                item for bit, item in enumerate(universe) if mask >> bit & 1
            }
            incidences = {
                w: sum(w in item for item in absent) for w in wset
            }
            total_incidence = sum(incidences.values())
            internal = sum(
                item[0] in wset and item[1] in wset for item in absent
            )
            assert total_incidence - len(absent) == internal
            assert len(absent) >= max(0, total_incidence - c2(w_size))
            for forced in range(len(pset) + len(qset) + w_size):
                if all(value >= forced for value in incidences.values()):
                    assert len(absent) >= max(
                        0, w_size * forced - c2(w_size)
                    )
            rows += 1
    return {"four_charge_subgraphs": rows, "pass": True}


def symbolic_certificate(max_g: int = 120) -> dict[str, int | bool]:
    """Verify concavity, both exact factorizations, signs, and roots."""
    n, delta, d, p, g, kappa, h, a = sp.symbols(
        "n delta d p g kappa h a", integer=True
    )
    centre = p * (n - d - 1 - p) + n - 1
    other_endpoint = n - delta - d - 1
    assert sp.expand(centre.subs(p, delta) - centre.subs(p, other_endpoint)) == 0
    assert sp.diff(centre, p, 2) == -2

    n0 = 2 * delta + kappa
    d0 = kappa - h - 1
    l0 = (
        delta * (n0 - d0 - 1 - delta)
        + n0
        - 1
        + (d0 - 1) * (n0 - 2 - delta - g)
        - (d0 - 1) * (d0 - 2) / 2
    )
    even_missing = n0**2 / 4 - n0 / 2 - 1
    odd_missing = (n0**2 - 2 * n0 - 3) / 4
    even_rhs = (
        delta
        - g**2
        + 2 * g
        + 2
        + (a**2 - 4 + 2 * h * (2 * g - h - 1)) / 4
    )
    odd_rhs = (
        delta
        - g**2
        + 2 * g
        + 1
        + (a**2 - 1 + 2 * h * (2 * g - h - 1)) / 4
    )
    assert sp.simplify(
        (l0 - even_missing).subs(kappa, 2 * g - a) - even_rhs
    ) == 0
    assert sp.simplify(
        (l0 - odd_missing).subs(kappa, 2 * g - a) - odd_rhs
    ) == 0

    rows = 0
    endpoint_rows = 0
    root_rows = 0
    for spread in range(3, max_g + 1):
        for parity in (0, 1):
            cap = 2 * spread - (2 if parity == 0 else 1)
            for kap in range(4 if parity == 0 else 3, cap + 1, 2):
                aa = 2 * spread - kap
                for common in range(2, kap):
                    hh = kap - common - 1
                    remainder = (
                        aa * aa
                        - (4 if parity == 0 else 1)
                        + 2 * hh * (2 * spread - hh - 1)
                    )
                    assert remainder >= 0
                    rows += 1

        if spread >= 4:
            for parity in (0, 1):
                dd = spread * spread - 2 * spread - (2 if parity == 0 else 1)
                kap = 2 * spread - (2 if parity == 0 else 1)
                nn = 2 * dd + kap
                common = kap - 1
                assert relaxed_lower(nn, dd, spread, common) == missing_count(nn)
                assert exact_degree_cap_lower(
                    nn, dd, dd + spread, common, 1
                ) == missing_count(nn)
                endpoint_rows += 1

    for nn in range(7, 2 * max_g * max_g + 1):
        parity = nn & 1
        constant = 3 if parity else 6
        first = next(
            spread
            for spread in range(0, max_g + 2)
            if nn <= 2 * spread * spread - 2 * spread - constant
        )
        discriminant = 2 * nn + (7 if parity else 13)
        root = 0
        while (2 * root - 1) ** 2 < discriminant:
            root += 1
        assert first == root
        root_rows += 1

    return {
        "factor_sign_rows": rows,
        "sharp_scalar_rows": endpoint_rows,
        "root_rows": root_rows,
        "pass": True,
    }


def small_spread_certificate(max_m: int = 180) -> dict[str, int | bool]:
    """Independent finite guard for the g<=2 and both g=3 layers."""
    low_rows = 0
    even_rows = 0
    odd_rows = 0
    for n in range(7, 2 * max_m + 2):
        edges = n * n // 4 + 1
        average_ceiling = ceil_div(2 * edges, n)
        missing = c2(n) - edges
        for delta in range(3, n):
            kappa = n - 2 * delta
            for g in range(3):
                if delta + g < average_ceiling or kappa < 3:
                    continue
                root = ceil_div(
                    delta * delta + delta * kappa + n - 3 - missing,
                    delta - 1,
                )
                assert root > kappa
                low_rows += 1

    for m in range(6, max_m + 1):
        n = 2 * m
        delta = m - 2
        maximum = m + 1
        kappa = 4
        missing = m * m - m - 1
        # This deliberately includes the loose full B-size range.  The
        # aggregate root itself then removes ell >= m-2.
        for ell in range(1, m - 1):
            root = ceil_div(
                delta * delta
                + delta * kappa
                + delta
                - 1
                + ell
                - missing,
                delta - 1,
            )
            for d in range(2, kappa + 1):
                if d < root or (3 - d) * ell < 0:
                    continue
                assert exact_degree_cap_lower(
                    n, delta, maximum, d, ell
                ) > missing
                even_rows += 1

    for m in range(5, max_m + 1):
        n = 2 * m + 1
        delta = m - 2
        maximum = m + 1
        missing = m * m - 1
        # Again retain the manuscript's looser ell <= |B| range.
        for ell in range(1, m):
            for p in (m - 2, m - 1):
                high_counts = range(ell + 1) if p == m - 2 else (0,)
                for high_count in high_counts:
                    for d in range(2, 6):
                        if (3 - d) * ell + high_count < 0:
                            continue
                        assert exact_degree_cap_lower(
                            n, p, maximum, d, ell
                        ) > missing
                        odd_rows += 1
    return {
        "g_le_two_rows": low_rows,
        "even_g_three_rows": even_rows,
        "odd_g_three_rows": odd_rows,
        "pass": True,
    }


def endpoint_graph(g: int, parity: str) -> dict[str, object]:
    assert g >= 4 and parity in {"even", "odd"}
    even = parity == "even"
    delta = g * g - 2 * g - (2 if even else 1)
    kappa = 2 * g - (2 if even else 1)
    maximum = delta + g
    n = 2 * delta + kappa
    b, c = 0, 1
    pset = set(range(2, 2 + delta))
    uset = set(range(2 + delta, 2 + 2 * delta))
    wset = set(range(2 + 2 * delta, n))
    edges: set[tuple[int, int]] = set()

    for x in pset:
        edges.add(edge(b, x))
    for x, y in combinations(pset, 2):
        edges.add(edge(x, y))
    for x in uset:
        edges.add(edge(c, x))
    for x, y in combinations(uset, 2):
        edges.add(edge(x, y))

    right = sorted(pset) + sorted(uset)
    for i, w in enumerate(sorted(wset)):
        for step in range(maximum):
            edges.add(edge(w, right[(i * maximum + step) % len(right)]))

    adjacency = [set() for _ in range(n)]
    for x, y in edges:
        adjacency[x].add(y)
        adjacency[y].add(x)
    types = {b: "b", c: "c"}
    types.update({x: "P" for x in pset})
    types.update({x: "U" for x in uset})
    types.update({x: "W" for x in wset})
    return {
        "g": g,
        "parity": parity,
        "n": n,
        "delta": delta,
        "kappa": kappa,
        "maximum": maximum,
        "b": b,
        "c": c,
        "P": pset,
        "U": uset,
        "W": wset,
        "edges": edges,
        "adj": adjacency,
        "types": types,
    }


def graph_geometry_certificate(max_g: int = 12) -> dict[str, int | bool]:
    rows = 0
    witnesses = 0
    for g in range(4, max_g + 1):
        for parity in ("even", "odd"):
            graph = endpoint_graph(g, parity)
            n = int(graph["n"])
            delta = int(graph["delta"])
            maximum = int(graph["maximum"])
            edges = graph["edges"]
            adj = graph["adj"]
            pset = graph["P"]
            uset = graph["U"]
            wset = graph["W"]
            b, c = int(graph["b"]), int(graph["c"])
            degrees = [len(row) for row in adj]
            assert len(edges) == n * n // 4 + 1
            assert min(degrees) == delta and max(degrees) == maximum
            assert adj[b] == pset and adj[c] == uset
            assert pset.isdisjoint(uset)
            assert all(edge(x, y) not in edges for x in pset for y in uset)
            right_degrees = [len(adj[x] & wset) for x in pset | uset]
            assert set(right_degrees) <= {g - 1, g}
            assert max(right_degrees) <= g and min(right_degrees) >= g - 1
            for w in wset:
                assert len(adj[w]) == maximum
                assert len(adj[w] & pset) >= g
                assert len(adj[w] & uset) >= g
                assert b not in adj[w] and c not in adj[w]
                assert adj[b].isdisjoint(adj[c])
                assert not any(
                    edge(x, y) in edges for x in adj[b] for y in adj[c]
                )
                witnesses += 1
            rows += 1
    return {"endpoint_graphs": rows, "witness_rows": witnesses, "pass": True}


def exact_paths(
    adjacency: list[set[int]],
    start: int,
    finish: int,
    length: int,
    forbidden: set[int],
    banned_edges: set[tuple[int, int]],
) -> list[tuple[int, ...]]:
    paths: list[tuple[int, ...]] = []

    def visit(path: tuple[int, ...]) -> None:
        if len(path) - 1 == length:
            if path[-1] == finish:
                paths.append(path)
            return
        if path[-1] == finish:
            return
        for nxt in adjacency[path[-1]]:
            if nxt in forbidden or nxt in path:
                continue
            if edge(path[-1], nxt) in banned_edges:
                continue
            visit(path + (nxt,))

    visit((start,))
    return paths


def c7_contains_both(
    adjacency: list[set[int]], first: tuple[int, int], second: tuple[int, int]
) -> bool:
    """Exact two-path characterization after deleting two cycle edges."""
    b, x = first
    c, y = second
    banned = {edge(*first), edge(*second)}
    pairings = (((b, c), (x, y)), ((b, y), (x, c)))
    for one, two in pairings:
        for first_length in (2, 3):
            second_length = 5 - first_length
            paths_one = exact_paths(
                adjacency,
                one[0],
                one[1],
                first_length,
                set(two),
                banned,
            )
            paths_two = exact_paths(
                adjacency,
                two[0],
                two[1],
                second_length,
                set(one),
                banned,
            )
            for path_one in paths_one:
                interior_one = set(path_one[1:-1])
                if any(interior_one.isdisjoint(path_two[1:-1]) for path_two in paths_two):
                    return True
    return False


def recolouring_certificate(max_g: int = 8) -> dict[str, int | bool]:
    graph_rows = 0
    colour_rows = 0
    exhaustive_cycle_rows = 0
    reserve_rows = 0
    for g in range(4, max_g + 1):
        for parity in ("even", "odd"):
            graph = endpoint_graph(g, parity)
            adj = graph["adj"]
            edges = graph["edges"]
            b, c = int(graph["b"]), int(graph["c"])
            pset, uset, wset = graph["P"], graph["U"], graph["W"]
            for witness_index, witness in enumerate(sorted(wset)):
                aset = {witness} | adj[witness]
                bset = set(range(int(graph["n"]))) - aset
                assert b in bset and c in bset
                reserve = (
                    len(bset) - 1 - len(adj[b] & bset)
                    + len(bset) - 1 - len(adj[c] & bset)
                    - 1
                )
                expected = (
                    int(graph["delta"]) + 2 * int(graph["kappa"]) - g - 5
                )
                assert reserve == expected and reserve >= g
                reserve_rows += 1

                # One explicit recolouring is enough for existence; checking
                # all witnesses above separately guards the reserve identity.
                if witness_index:
                    continue
                xs = sorted(adj[witness] & pset)[:g]
                ys = sorted(adj[witness] & uset)[:g]
                assert len(xs) == len(ys) == g
                recoloured = {
                    edge(b, xs[i]): ("gamma", i) for i in range(g)
                }
                recoloured.update(
                    {edge(c, ys[i]): ("gamma", i) for i in range(g)}
                )
                colours = {
                    item: recoloured.get(item, ("unique", item)) for item in edges
                }
                crossing_counts: Counter[object] = Counter()
                for item, colour in colours.items():
                    if (item[0] in aset) ^ (item[1] in aset):
                        crossing_counts[colour] += 1
                defect_b = sum(max(value - 1, 0) for value in crossing_counts.values())
                assert defect_b == g
                multiplicity = 0
                for i in range(g):
                    members = [item for item, col in colours.items() if col == ("gamma", i)]
                    outer = {
                        endpoint
                        for item in members
                        for endpoint in item
                        if endpoint in bset
                    }
                    assert len(members) == 2 and outer == {b, c}
                    multiplicity += 1
                    # Structural short-shore checks explain the C7 guard.
                    x, y = xs[i], ys[i]
                    assert not (adj[b] & adj[c])
                    assert not (adj[b] & adj[y])
                    assert not (adj[x] & adj[c])
                    assert not any(u in adj[p] for p in adj[b] for u in adj[c])
                    if g <= 5:
                        assert not c7_contains_both(
                            adj, (b, x), (c, y)
                        )
                        exhaustive_cycle_rows += 1
                assert multiplicity == g
                colour_rows += g
                graph_rows += 1
    return {
        "recoloured_graphs": graph_rows,
        "two_edge_colour_classes": colour_rows,
        "exact_c7_pair_checks": exhaustive_cycle_rows,
        "reserve_witness_rows": reserve_rows,
        "pass": True,
    }


TEMPLATES: dict[tuple[str, str], tuple[str, ...]] = {
    ("b", "c"): ("b", "P", "W", "U", "c"),
    ("b", "P"): ("b", "P", "P", "P", "P"),
    ("b", "U"): ("b", "P", "P", "W", "U"),
    ("b", "W"): ("b", "P", "P", "P", "W"),
    ("c", "U"): ("c", "U", "U", "U", "U"),
    ("c", "P"): ("c", "U", "U", "W", "P"),
    ("c", "W"): ("c", "U", "U", "U", "W"),
    ("P", "P"): ("P", "P", "P", "P", "P"),
    ("U", "U"): ("U", "U", "U", "U", "U"),
    ("P", "U"): ("P", "P", "W", "U", "U"),
    ("P", "W"): ("P", "P", "P", "P", "W"),
    ("U", "W"): ("U", "U", "U", "U", "W"),
    ("W", "W"): ("W", "P", "P", "P", "W"),
}


def oriented_template(first_type: str, second_type: str) -> tuple[str, ...]:
    if (first_type, second_type) in TEMPLATES:
        return TEMPLATES[(first_type, second_type)]
    return tuple(reversed(TEMPLATES[(second_type, first_type)]))


def template_internal_sets(
    graph: dict[str, object], first: int, second: int
) -> set[frozenset[int]]:
    types = graph["types"]
    adjacency = graph["adj"]
    sequence = oriented_template(types[first], types[second])
    assert sequence[0] == types[first] and sequence[-1] == types[second]
    blocks: dict[str, set[int]] = {
        "b": {int(graph["b"])},
        "c": {int(graph["c"])},
        "P": graph["P"],
        "U": graph["U"],
        "W": graph["W"],
    }
    states = [(first,)]
    for wanted in sequence[1:-1]:
        states = [
            path + (nxt,)
            for path in states
            for nxt in blocks[wanted]
            if nxt not in path
            and nxt != second
            and nxt in adjacency[path[-1]]
        ]
    return {
        frozenset(path[1:])
        for path in states
        if second not in path and second in adjacency[path[-1]]
    }


def l4_template_certificate() -> dict[str, int | bool]:
    endpoint_rows = 0
    path_sets = 0
    for parity in ("even", "odd"):
        graph = endpoint_graph(5, parity)
        n = int(graph["n"])
        types = graph["types"]
        for first, second in combinations(range(n), 2):
            # No pair consists of two vertices of singleton type b or c.
            assert (types[first], types[second]) in TEMPLATES or (
                types[second], types[first]
            ) in TEMPLATES
            paths = template_internal_sets(graph, first, second)
            assert paths
            eligible = set(range(n)) - {first, second}
            assert not set.intersection(*(set(item) for item in paths))
            for deleted in eligible:
                avoiding = [set(item) for item in paths if deleted not in item]
                assert avoiding
                assert not set.intersection(*avoiding)
            endpoint_rows += 1
            path_sets += len(paths)
    return {
        "template_endpoint_pairs": endpoint_rows,
        "template_internal_sets": path_sets,
        "pass": True,
    }


def n32_certificate(max_g: int = 200) -> dict[str, int | bool]:
    rows = 0
    for g in range(4, max_g + 1):
        for parity in ("even", "odd"):
            rho = 2 * g - (2 if parity == "even" else 1)
            xi = rho - 2
            # N25 at ell=1 is rho+Xi <= 2(g+1)+2Z-2.
            minimum_z = rho - 1 - g
            assert 2 * rho - 2 <= 2 * g + 2 * minimum_z
            assert minimum_z == g - (3 if parity == "even" else 2)
            rows += 1
    return {"n32_endpoint_rows": rows, "pass": True}


def firewall_certificate() -> dict[str, bool]:
    theorem = (HERE / "MAXIMUM_WITNESS_OPPOSITE_DEGREE_SPREAD.md").read_text()
    normal = (HERE / "MAXIMUM_WITNESS_CANONICAL_HARDNESS_NORMAL_FORM.md").read_text()
    readme = (HERE / "README.md").read_text()
    theorem_flat = " ".join(theorem.split())
    normal_flat = " ".join(normal.split())
    readme_flat = " ".join(readme.split())
    assert "Erdős #809 remains open" in theorem_flat
    assert "does not eliminate" in theorem_flat
    assert "not a proof" in normal_flat
    assert "OPEN / NOT CLAIMED" in readme_flat
    return {"pass": True}


def main() -> int:
    result = {
        "four_charges": four_charge_certificate(),
        "symbolic": symbolic_certificate(),
        "small_spread": small_spread_certificate(),
        "graph_geometry": graph_geometry_certificate(),
        "recolouring": recolouring_certificate(),
        "l4_templates": l4_template_certificate(),
        "n32": n32_certificate(),
        "firewall": firewall_certificate(),
    }
    assert all(bool(section["pass"]) for section in result.values())
    result["pass"] = True
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
