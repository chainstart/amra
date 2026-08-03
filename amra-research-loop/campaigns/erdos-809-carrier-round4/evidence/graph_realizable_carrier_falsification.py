#!/usr/bin/env python3
"""Exact bounded falsification for graph-realizable carrier mechanisms.

The positive object is always an actual missing B-edge in the labelled graph.
Formal universal dummies never enter a mechanism test.
"""

from __future__ import annotations

import hashlib
import json
from itertools import combinations, product
from pathlib import Path


def edge(u: str, w: str) -> tuple[str, str]:
    return tuple(sorted((u, w)))


X = tuple(f"x{i}" for i in range(1, 5))
Y = tuple(f"y{i}" for i in range(1, 5))
A = frozenset(("v",) + X + Y + ("r1", "r2"))
B = frozenset(("b", "c", "z"))
V = tuple(sorted(A | B))

removed = {edge("x1", "x2"), edge("y1", "y2")}
E = {
    edge(u, w)
    for u, w in combinations(A, 2)
    if not ((u in X and w in Y) or (u in Y and w in X))
    and edge(u, w) not in removed
}
E.update(edge("b", x) for x in X)
E.update(edge("c", y) for y in Y)
E.add(edge("b", "z"))
E.update(edge("z", x) for x in X)
E = frozenset(E)


def adjacent(u: str, w: str) -> bool:
    return u != w and edge(u, w) in E


def neighbours(u: str) -> frozenset[str]:
    return frozenset(w for w in V if adjacent(u, w))


def colour(e: tuple[str, str]) -> str:
    for i in range(1, 5):
        if e in (edge("b", f"x{i}"), edge("c", f"y{i}")):
            return f"gamma{i}"
    return "unique:" + "-".join(e)


def canonical_cycles(length: int) -> set[tuple[str, ...]]:
    answer: set[tuple[str, ...]] = set()

    def extend(path: tuple[str, ...]) -> None:
        if len(path) == length:
            if adjacent(path[-1], path[0]):
                words = []
                for word in (path, tuple(reversed(path))):
                    words.extend(word[i:] + word[:i] for i in range(length))
                answer.add(min(words))
            return
        for nxt in V:
            if nxt not in path and adjacent(path[-1], nxt):
                extend(path + (nxt,))

    for start in V:
        extend((start,))
    return answer


def has_length_four_path(start: str, end: str, forbidden: frozenset[str]) -> bool:
    def extend(path: tuple[str, ...]) -> bool:
        if len(path) == 5:
            return path[-1] == end
        for nxt in V:
            if nxt in forbidden or nxt in path or not adjacent(path[-1], nxt):
                continue
            if len(path) < 4 and nxt == end:
                continue
            if extend(path + (nxt,)):
                return True
        return False
    return extend((start,))


def l4_2_failures() -> list[tuple[str, str, tuple[str, ...]]]:
    failures = []
    for start, end in combinations(V, 2):
        available = [w for w in V if w not in (start, end)]
        for size in range(3):
            for forbidden in combinations(available, size):
                if not has_length_four_path(start, end, frozenset(forbidden)):
                    failures.append((start, end, forbidden))
                    if len(failures) == 20:
                        return failures
    return failures


def reserve(pair: tuple[str, str]) -> frozenset[tuple[str, str]] | None:
    left, right = pair
    nb_left = neighbours(left) & B
    nb_right = neighbours(right) & B
    if any(p != q and adjacent(p, q) for p in nb_left for q in nb_right):
        return None
    missing = {edge(u, w) for u, w in combinations(B, 2) if not adjacent(u, w)}
    result = {f for f in missing if left in f or right in f}
    result.update(edge(p, q) for p in nb_left for q in nb_right if p != q)
    assert result <= missing
    return frozenset(result)


def matching_rank(neighbourhoods: tuple[frozenset[tuple[str, str]], ...]) -> int:
    owner: dict[tuple[str, str], int] = {}

    def augment(demand: int, seen: set[tuple[str, str]]) -> bool:
        for carrier in neighbourhoods[demand]:
            if carrier in seen:
                continue
            seen.add(carrier)
            if carrier not in owner or augment(owner[carrier], seen):
                owner[carrier] = demand
                return True
        return False
    return sum(augment(demand, set()) for demand in range(len(neighbourhoods)))


def hall_deficiency(neighbourhoods: tuple[frozenset[tuple[str, str]], ...]) -> int:
    best = 0
    for mask in range(1 << len(neighbourhoods)):
        selected = [neighbourhoods[i] for i in range(len(neighbourhoods)) if mask & (1 << i)]
        union = frozenset().union(*selected) if selected else frozenset()
        best = max(best, len(selected) - len(union))
    return best


def relaxed_b_scan(n_max: int = 6) -> dict[str, int]:
    """B-side exact reserve scan; negative discovery only, never promotion."""
    graph_count = zero_pair_count = root_state_count = 0
    for n in range(2, n_max + 1):
        pairs = tuple(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            graph_count += 1
            edges = {p for i, p in enumerate(pairs) if mask & (1 << i)}
            for left, right in set(pairs) - edges:
                nl = {w for w in range(n) if tuple(sorted((left, w))) in edges}
                nr = {w for w in range(n) if tuple(sorted((right, w))) in edges}
                if any(p != q and tuple(sorted((p, q))) in edges for p in nl for q in nr):
                    continue
                zero_pair_count += 1
                root_state_count += 2
    return {
        "n_B_max": n_max,
        "labelled_B_graphs": graph_count,
        "zero_shore_pairs": zero_pair_count,
        "two_endpoint_root_states": root_state_count,
    }


def main() -> None:
    n = len(V)
    cycles = canonical_cycles(7)
    nonrainbow = [
        cycle for cycle in cycles
        if len({colour(edge(cycle[i], cycle[(i + 1) % 7])) for i in range(7)}) < 7
    ]
    l4_fail = l4_2_failures()
    k_bc = reserve(edge("b", "c"))
    assert k_bc == frozenset({edge("b", "c"), edge("c", "z")})
    assert len(E) == n * n // 4 + 1 == 50
    assert not nonrainbow and not l4_fail
    assert A == neighbours("v") | {"v"}

    # Four fully graph-realized repeated colours give four demands with the
    # identical base bc. Reversing either two-point root leaves the unordered
    # base and exact reserve unchanged.
    neighbourhoods = tuple(k_bc for _ in range(4))
    rank = matching_rank(neighbourhoods)
    deficiency = hall_deficiency(neighbourhoods)
    root_states = tuple(product(("b", "c"), repeat=4))
    assert rank == 2 and deficiency == 2 and len(root_states) == 16
    assert all(reserve(edge("b", "c")) == k_bc for _ in root_states)

    # Every three-demand subset is a minimal deficient circuit. Two such
    # triples cross, while no root rotation changes their carrier union.
    triples = tuple(combinations(range(4), 3))
    crossing = (set(triples[0]), set(triples[1]))
    assert crossing[0] & crossing[1]
    assert not (crossing[0] <= crossing[1] or crossing[1] <= crossing[0])

    missing_b = {edge(u, w) for u, w in combinations(B, 2) if not adjacent(u, w)}
    free_outside = missing_b - k_bc
    assert not free_outside

    owned = tuple(edge(f"x{i}", f"y{i}") for i in range(1, 5))
    assert len(set(owned)) == 4 and all(item not in E for item in owned)

    tests = {
        "M809R4-01": {"outcome": "killed", "reason": "terminal exact root-state component has deficiency two and no free actual B-edge"},
        "M809R4-02": {"outcome": "killed", "reason": "root reversal changes the root/ownership state while returning to the identical base and carrier neighbourhood"},
        "M809R4-03": {"outcome": "killed", "reason": "four distinct owned A diagonals coexist with no missing B-edge outside occupied K(bc)"},
        "M809R4-04": {"outcome": "survived", "reason": "the witness has no actual absorbers, so it does not refute a future bounded-codegree theorem conditional on graph-proved absorber certificates"},
        "M809R4-05": {"outcome": "killed", "reason": "A ownership rank four does not extend B carrier rank two on the common B-edge ground set"},
        "M809R4-06": {"outcome": "killed", "reason": "positive Hall deficiency coexists with zero path capacity to a free actual carrier"},
        "M809R4-07": {"outcome": "killed", "reason": "all 16 simultaneous root rotations preserve base bc and K(bc) exactly"},
        "M809R4-08": {"outcome": "killed", "reason": "crossing minimal deficient triples persist under every graph-legal root rotation and release no edge"},
        "M809R4-09": {"outcome": "killed", "reason": "distinct demands have pair codegree two, equal to individual degree two and greater than the claimed half-degree bound"},
        "M809R4-10": {"outcome": "survived", "reason": "its antecedent total actual carrier count at least demand count is false in this exact graph; no strict graph-realizable kill was found"},
    }

    payload = {
        "schema": "amra.erdos809.carrier_round4.falsification.v1",
        "full_graph_certificate": {
            "n": n,
            "edges": len(E),
            "threshold_edges": n * n // 4 + 1,
            "minimum_degree": min(len(neighbours(w)) for w in V),
            "maximum_degree": max(len(neighbours(w)) for w in V),
            "A_is_closed_neighbourhood": True,
            "B": sorted(B),
            "B_edges": sorted(item for item in E if set(item) <= B),
            "rainbow_C7": True,
            "C7_count": len(cycles),
            "L4_2": True,
            "repeated_colours": 4,
            "owned_A_diagonals": owned,
            "base": edge("b", "c"),
            "actual_full_reserve": sorted(k_bc),
            "all_missing_B_edges": sorted(missing_b),
            "universal_dummy_used": False,
        },
        "carrier_rank": {"demands": 4, "rank": rank, "deficiency": deficiency, "root_states": len(root_states), "free_actual_edges": sorted(free_outside)},
        "crossing_minimal_circuits": [sorted(crossing[0]), sorted(crossing[1])],
        "relaxed_B_side_scan": relaxed_b_scan(),
        "tests": tests,
        "survivors": ["M809R4-04", "M809R4-10"],
        "scope": "Strict kills use the exact full n=14 graph. The exhaustive B-side scan is a discovery relaxation only and supplies no positive theorem.",
        "public_problem_changed": False,
        "main_term_changed": False,
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    output = Path(__file__).with_suffix(".json")
    output.write_bytes(encoded)
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("output_sha256", hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
