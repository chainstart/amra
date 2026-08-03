#!/usr/bin/env python3
"""Blind reconstruction of the round-four n=14 carrier certificate.

This checker is written from the prose graph description and imports no
author checker or generated author evidence.  Standard-library exact finite
enumeration only; intended external bound is 2 GiB / 120 seconds.
"""

from __future__ import annotations

from itertools import combinations, product
import json


def edge(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


VERTICES = tuple(
    ["v"]
    + [f"x{i}" for i in range(1, 5)]
    + [f"y{i}" for i in range(1, 5)]
    + ["r1", "r2", "b", "c", "z"]
)
X = frozenset(f"x{i}" for i in range(1, 5))
Y = frozenset(f"y{i}" for i in range(1, 5))
A = frozenset(VERTICES[:11])
B = frozenset(("b", "c", "z"))


def build_graph() -> frozenset[tuple[str, str]]:
    removed_inside_a = {edge("x1", "x2"), edge("y1", "y2")}
    edges = {
        edge(left, right)
        for left, right in combinations(A, 2)
        if not ({left, right} & X and {left, right} & Y)
        and edge(left, right) not in removed_inside_a
    }
    edges.update(edge("b", item) for item in X)
    edges.update(edge("c", item) for item in Y)
    edges.add(edge("b", "z"))
    edges.update(edge("z", item) for item in X)
    return frozenset(edges)


EDGES = build_graph()


def adjacent(left: str, right: str) -> bool:
    return left != right and edge(left, right) in EDGES


def neighbours(vertex: str) -> frozenset[str]:
    return frozenset(other for other in VERTICES if adjacent(vertex, other))


def colour(item: tuple[str, str]) -> str:
    for index in range(1, 5):
        if item in (edge("b", f"x{index}"), edge("c", f"y{index}")):
            return f"gamma{index}"
    return "unique:" + "-".join(item)


def canonical_seven_cycles() -> frozenset[tuple[str, ...]]:
    cycles: set[tuple[str, ...]] = set()

    def search(path: tuple[str, ...]) -> None:
        if len(path) == 7:
            if adjacent(path[-1], path[0]):
                representatives = []
                for direction in (path, tuple(reversed(path))):
                    representatives.extend(direction[i:] + direction[:i] for i in range(7))
                cycles.add(min(representatives))
            return
        for nxt in VERTICES:
            if nxt not in path and adjacent(path[-1], nxt):
                search(path + (nxt,))

    for start in VERTICES:
        search((start,))
    return frozenset(cycles)


def has_length_four_path(start: str, end: str, forbidden: frozenset[str]) -> bool:
    def extend(path: tuple[str, ...]) -> bool:
        if len(path) == 5:
            return path[-1] == end
        for nxt in VERTICES:
            if nxt in forbidden or nxt in path or not adjacent(path[-1], nxt):
                continue
            if len(path) < 4 and nxt == end:
                continue
            if extend(path + (nxt,)):
                return True
        return False

    return extend((start,))


def verify_l4_2() -> int:
    checks = 0
    for start, end in combinations(VERTICES, 2):
        available = [item for item in VERTICES if item not in (start, end)]
        for size in range(3):
            for forbidden in combinations(available, size):
                assert has_length_four_path(start, end, frozenset(forbidden))
                checks += 1
    return checks


def canonical_reserve(base: tuple[str, str]) -> frozenset[tuple[str, str]]:
    left, right = base
    missing_b = {
        edge(u, w) for u, w in combinations(B, 2) if not adjacent(u, w)
    }
    reserve = {item for item in missing_b if left in item or right in item}
    reserve.update(
        edge(p, q)
        for p in neighbours(left) & B
        for q in neighbours(right) & B
        if p != q
    )
    assert reserve <= missing_b
    return frozenset(reserve)


def matching_number(rows: tuple[frozenset[tuple[str, str]], ...]) -> int:
    states = {frozenset()}
    for row in rows:
        nxt = set(states)
        for used in states:
            for carrier in row - used:
                nxt.add(used | {carrier})
        states = nxt
    return max(len(used) for used in states)


def hall_deficiency(rows: tuple[frozenset[tuple[str, str]], ...]) -> tuple[int, list[int]]:
    best = 0
    deficient_masks = []
    for mask in range(1 << len(rows)):
        union: set[tuple[str, str]] = set()
        size = 0
        for index, row in enumerate(rows):
            if mask >> index & 1:
                size += 1
                union.update(row)
        deficit = size - len(union)
        if deficit > best:
            best = deficit
        if deficit > 0:
            deficient_masks.append(mask)
    return best, deficient_masks


def locked_circuit_parameter_check() -> int:
    checked = 0
    for demands in range(9):
        for reserve_size in range(9):
            carriers = frozenset(("K", str(index)) for index in range(reserve_size))
            rows = tuple(carriers for _ in range(demands))
            rank = matching_number(rows)
            deficiency, _ = hall_deficiency(rows)
            assert rank == min(demands, reserve_size)
            assert deficiency == max(0, demands - reserve_size)
            checked += 1
    return checked


def main() -> None:
    assert len(VERTICES) == 14
    assert len(EDGES) == 50 == len(VERTICES) ** 2 // 4 + 1
    degrees = {vertex: len(neighbours(vertex)) for vertex in VERTICES}
    assert min(degrees.values()) == 4 and max(degrees.values()) == 10
    assert A == neighbours("v") | {"v"}

    l4_checks = verify_l4_2()
    cycles = canonical_seven_cycles()
    nonrainbow = []
    for cycle in cycles:
        cycle_colours = [colour(edge(cycle[i], cycle[(i + 1) % 7])) for i in range(7)]
        if len(set(cycle_colours)) < 7:
            nonrainbow.append(cycle)
    assert len(cycles) == 11_136 and not nonrainbow

    repeated_pairs = tuple(
        (edge("b", f"x{index}"), edge("c", f"y{index}"))
        for index in range(1, 5)
    )
    assert all(left in EDGES and right in EDGES for left, right in repeated_pairs)
    owned_diagonals = frozenset(edge(f"x{i}", f"y{i}") for i in range(1, 5))
    assert owned_diagonals.isdisjoint(EDGES) and len(owned_diagonals) == 4

    missing_b = frozenset(
        edge(left, right) for left, right in combinations(B, 2) if not adjacent(left, right)
    )
    base = edge("b", "c")
    reserve = canonical_reserve(base)
    assert missing_b == reserve == frozenset((edge("b", "c"), edge("c", "z")))

    demands = tuple(f"gamma{i}" for i in range(1, 5))
    rows = tuple(reserve for _ in demands)
    rank = matching_number(rows)
    deficiency, deficient_masks = hall_deficiency(rows)
    assert rank == 2 and deficiency == 2

    root_states = tuple(product(("b", "c"), repeat=4))
    assert len(root_states) == 16
    for state in root_states:
        bases = tuple(edge(root, "c" if root == "b" else "b") for root in state)
        assert all(item == base for item in bases)
        assert all(canonical_reserve(item) == reserve for item in bases)

    minimal_deficient = []
    for mask in deficient_masks:
        strict_deficient = any(
            sub != mask and sub & mask == sub and sub in deficient_masks
            for sub in range(1 << len(rows))
        )
        if not strict_deficient:
            minimal_deficient.append(mask)
    assert len(minimal_deficient) == 4
    assert all(mask.bit_count() == 3 for mask in minimal_deficient)
    crossing = (minimal_deficient[0], minimal_deficient[1])
    assert crossing[0] & crossing[1] and crossing[0] & ~crossing[1] and crossing[1] & ~crossing[0]

    pair_codegrees = []
    for left, right in combinations(range(4), 2):
        pair_codegrees.append(len(rows[left] & rows[right]))
    assert set(pair_codegrees) == {2}
    assert all(len(row) == 2 for row in rows)

    locked_parameter_checks = locked_circuit_parameter_check()

    statement_match = {
        "M809R4-01": {
            "verdict": "passed",
            "reason": "minimal deficient triples have no actual B-edge outside their common full reserve, so no root-state path can reach a free sink"
        },
        "M809R4-02": {
            "verdict": "qualified",
            "reason": "root reversal revisits the identical reserve with a different root state; this kills the claim only if root state is explicitly part of the asserted ownership state"
        },
        "M809R4-03": {
            "verdict": "passed",
            "reason": "four owned A diagonals exist but the original graph has no missing B-edge outside K(bc)"
        },
        "M809R4-05": {
            "verdict": "qualified",
            "reason": "the intended A-owner-to-new-B-element rank gain is impossible, but literal matroid augmentation on the two-element B ground set is not refuted and the A-to-B extension map is ill-typed"
        },
        "M809R4-06": {
            "verdict": "passed",
            "reason": "deficiency two coexists with no free actual B-edge sink, hence source-to-free-sink capacity zero"
        },
        "M809R4-07": {
            "verdict": "passed",
            "reason": "all 16 root states preserve base and reserve, so every minimal deficient triple is rank-neutral under root rotation"
        },
        "M809R4-08": {
            "verdict": "passed",
            "reason": "crossing minimal deficient triples exist and no root rotation can release an external actual edge"
        },
        "M809R4-09": {
            "verdict": "passed",
            "reason": "every pair codegree is two while every individual degree is two, contradicting the at-most-half premise"
        }
    }

    print(json.dumps({
        "schema": "amra.erdos809.carrier-round4-independent-audit.v1",
        "engine": "independent reconstruction from prose; no author-checker import",
        "full_graph": {
            "n": len(VERTICES),
            "edges": len(EDGES),
            "threshold": len(VERTICES) ** 2 // 4 + 1,
            "degrees": degrees,
            "minimum_degree": min(degrees.values()),
            "maximum_degree": max(degrees.values()),
            "A_is_closed_neighbourhood": True,
            "L4_2": True,
            "L4_2_cases": l4_checks,
            "C7_count": len(cycles),
            "rainbow_C7": True,
            "repeated_colours": 4,
            "colour_count": len(EDGES) - 4,
            "owned_A_diagonals": [list(item) for item in sorted(owned_diagonals)],
            "missing_B_edges": [list(item) for item in sorted(missing_b)],
            "K_bc": [list(item) for item in sorted(reserve)]
        },
        "locked_realization": {
            "demands": len(demands),
            "rank": rank,
            "deficiency": deficiency,
            "root_states": len(root_states),
            "minimal_deficient_triples": [
                [index for index in range(4) if mask >> index & 1]
                for mask in minimal_deficient
            ],
            "pair_codegrees": pair_codegrees,
            "external_actual_B_edges": []
        },
        "locked_theorem": {
            "finite_parameter_pairs_checked": locked_parameter_checks,
            "rank_formula": "min(d,|K(e)|)",
            "deficiency_formula": "max(0,d-|K(e)|)",
            "external_necessity": "a perfect matching uses d distinct right vertices, at most |K(e)| internal, hence at least d-|K(e)| external",
            "legality_boundary": "external objects count only after graph-proved arcs exist; saturation is equivalent to every augmented Hall cut"
        },
        "strict_kill_statement_match": statement_match,
        "survivor_boundaries": {
            "M809R4-04": "not killed: the graph has no absorber catalogue and misses the conditional catalogue antecedent; no bounded-overlap theorem is proved",
            "M809R4-10": "not killed: two actual carriers are fewer than four demands, so the actual-carrier-rich antecedent fails; no contraction or cleanup theorem is proved"
        },
        "verdict": "graph_and_locked_theorem_pass; six_literal_kills_pass; two_kills_require_statement_repairs",
        "scope": "local negative interface only; no external carrier, outer-A closure, public theorem, or 1/8 change",
        "lean_used": False,
        "main_term_changed": False,
        "public_problem_changed": False
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
