#!/usr/bin/env python3
"""Independent exact audit of the round-five n=15 absorber search.

Written from the published prose construction.  It imports no author search
code or generated evidence.  The exhaustive pass streams all C(13,7)
expansions and retains only aggregate counts and finite witnesses.
"""

from __future__ import annotations

from itertools import combinations
import json
import math


def edge(u: str, v: str) -> tuple[str, str]:
    return tuple(sorted((u, v)))


OLD_VERTICES = tuple(
    ["v"]
    + [f"x{i}" for i in range(1, 5)]
    + [f"y{i}" for i in range(1, 5)]
    + ["r1", "r2", "b", "c", "z"]
)
VERTICES = OLD_VERTICES + ("w",)
X = frozenset(f"x{i}" for i in range(1, 5))
Y = frozenset(f"y{i}" for i in range(1, 5))
A = frozenset(OLD_VERTICES[:11])
B = frozenset(("b", "c", "z", "w"))
EXPANSION_CHOICES = tuple(item for item in OLD_VERTICES if item != "v")


def old_graph() -> frozenset[tuple[str, str]]:
    removed = {edge("x1", "x2"), edge("y1", "y2")}
    result = {
        edge(u, v)
        for u, v in combinations(A, 2)
        if not ({u, v} & X and {u, v} & Y) and edge(u, v) not in removed
    }
    result.update(edge("b", x) for x in X)
    result.update(edge("c", y) for y in Y)
    result.add(edge("b", "z"))
    result.update(edge("z", x) for x in X)
    return frozenset(result)


OLD_EDGES = old_graph()


def expansion(neighbours: tuple[str, ...]) -> frozenset[tuple[str, str]]:
    return OLD_EDGES | frozenset(edge("w", item) for item in neighbours)


def adjacency(edges: frozenset[tuple[str, str]]) -> dict[str, tuple[str, ...]]:
    rows = {vertex: [] for vertex in VERTICES}
    for u, v in edges:
        rows[u].append(v)
        rows[v].append(u)
    return {vertex: tuple(sorted(row)) for vertex, row in rows.items()}


def cycle_with_pair(
    adj: dict[str, tuple[str, ...]],
    first: tuple[str, str],
    second: tuple[str, str],
) -> tuple[str, ...] | None:
    """Return a simple C7 containing both named edges, if one exists."""
    start, nxt = first
    if nxt not in adj[start]:
        return None
    path = [start, nxt]

    def visit() -> tuple[str, ...] | None:
        if len(path) == 7:
            if start not in adj[path[-1]]:
                return None
            cycle_edges = {
                edge(path[index], path[(index + 1) % 7]) for index in range(7)
            }
            return tuple(path) if second in cycle_edges else None
        for candidate in adj[path[-1]]:
            if candidate == start or candidate in path:
                continue
            path.append(candidate)
            answer = visit()
            if answer is not None:
                return answer
            path.pop()
        return None

    return visit()


def repeated_pairs(switched: frozenset[int]) -> tuple[tuple[tuple[str, str], tuple[str, str]], ...]:
    return tuple(
        (
            edge("w" if index in switched else "b", f"x{index}"),
            edge("c", f"y{index}"),
        )
        for index in range(1, 5)
    )


def first_nonrainbow_witness(
    edges: frozenset[tuple[str, str]], switched: frozenset[int]
) -> dict[str, object] | None:
    adj = adjacency(edges)
    for index, pair in enumerate(repeated_pairs(switched), start=1):
        if pair[0] not in edges or pair[1] not in edges:
            return {"invalid_switch_colour": index, "missing_edge": list(pair[0])}
        witness = cycle_with_pair(adj, *pair)
        if witness is not None:
            return {"repeated_colour": f"gamma{index}", "cycle": list(witness)}
    return None


def canonical_cycles(edges: frozenset[tuple[str, str]], length: int) -> frozenset[tuple[str, ...]]:
    adj = adjacency(edges)
    found: set[tuple[str, ...]] = set()

    def normalize(path: tuple[str, ...]) -> tuple[str, ...]:
        variants = []
        for direction in (path, tuple(reversed(path))):
            variants.extend(direction[k:] + direction[:k] for k in range(length))
        return min(variants)

    def visit(path: tuple[str, ...]) -> None:
        if len(path) == length:
            if path[0] in adj[path[-1]]:
                found.add(normalize(path))
            return
        for candidate in adj[path[-1]]:
            if candidate not in path:
                visit(path + (candidate,))

    for vertex in VERTICES:
        visit((vertex,))
    return frozenset(found)


def length_path_count(
    adj: dict[str, tuple[str, ...]], start: str, end: str, length: int
) -> int:
    count = 0

    def visit(path: tuple[str, ...]) -> None:
        nonlocal count
        if len(path) == length + 1:
            count += path[-1] == end
            return
        for candidate in adj[path[-1]]:
            if candidate in path or (candidate == end and len(path) != length):
                continue
            visit(path + (candidate,))

    visit((start,))
    return count


def has_length_four_path(
    adj: dict[str, tuple[str, ...]], start: str, end: str, forbidden: frozenset[str]
) -> bool:
    path = [start]

    def visit() -> bool:
        if len(path) == 5:
            return path[-1] == end
        for candidate in adj[path[-1]]:
            if candidate in forbidden or candidate in path:
                continue
            if candidate == end and len(path) != 4:
                continue
            path.append(candidate)
            if visit():
                return True
            path.pop()
        return False

    return visit()


def l4_2_cases(edges: frozenset[tuple[str, str]]) -> int:
    adj = adjacency(edges)
    checked = 0
    for start, end in combinations(VERTICES, 2):
        remaining = [v for v in VERTICES if v not in (start, end)]
        for size in range(3):
            for deleted in combinations(remaining, size):
                assert has_length_four_path(adj, start, end, frozenset(deleted))
                checked += 1
    return checked


def canonical_reserve(
    edges: frozenset[tuple[str, str]], base: tuple[str, str]
) -> frozenset[tuple[str, str]]:
    adj = adjacency(edges)
    missing = {edge(u, v) for u, v in combinations(B, 2) if edge(u, v) not in edges}
    left, right = base
    result = {item for item in missing if left in item or right in item}
    result.update(
        edge(p, q)
        for p in set(adj[left]) & B
        for q in set(adj[right]) & B
        if p != q and edge(p, q) in missing
    )
    return frozenset(result)


def main() -> None:
    assert len(OLD_VERTICES) == 14 and len(OLD_EDGES) == 50
    assert len(EXPANSION_CHOICES) == 13
    assert math.comb(13, 7) == 1716

    named_neighbours = ("x1", "x2", "x3", "x4", "r1", "r2", "b")
    named_edges = expansion(named_neighbours)
    assert len(named_edges) == 57 == len(VERTICES) ** 2 // 4 + 1
    assert edge("v", "w") not in named_edges
    assert first_nonrainbow_witness(named_edges, frozenset()) is None
    l4_checks = l4_2_cases(named_edges)
    cycles = canonical_cycles(named_edges, 7)

    reserve_bc = canonical_reserve(named_edges, edge("b", "c"))
    reserve_cw = canonical_reserve(named_edges, edge("c", "w"))
    external = reserve_cw - reserve_bc
    assert reserve_bc == frozenset((edge("b", "c"), edge("c", "w"), edge("c", "z")))
    assert external == frozenset((edge("w", "z"),))

    adj = adjacency(named_edges)
    path4 = length_path_count(adj, "w", "z", 4)
    path5 = length_path_count(adj, "w", "z", 5)
    assert (path4, path5) == (128, 608)

    subset_results = []
    for mask in range(1, 16):
        switched = frozenset(index for index in range(1, 5) if mask >> (index - 1) & 1)
        witness = first_nonrainbow_witness(named_edges, switched)
        assert witness is not None and "cycle" in witness
        subset_results.append({"switched": sorted(switched), "witness": witness})

    aggregate = {
        "expansions": 0,
        "original_rainbow": 0,
        "external_output_nonempty": 0,
        "both_original_rainbow_and_external": 0,
        "with_at_least_two_available_natural_switches": 0,
        "with_at_least_two_individually_rainbow_switches": 0,
        "target_instances": 0,
    }
    earliest_valid = None
    maximum_individually_legal = 0
    histogram = {str(k): 0 for k in range(5)}

    for neighbours in combinations(EXPANSION_CHOICES, 7):
        aggregate["expansions"] += 1
        edges = expansion(neighbours)
        original_rainbow = first_nonrainbow_witness(edges, frozenset()) is None
        aggregate["original_rainbow"] += int(original_rainbow)
        old_reserve = canonical_reserve(edges, edge("b", "c"))
        new_reserve = canonical_reserve(edges, edge("c", "w"))
        has_external = bool(new_reserve - old_reserve)
        aggregate["external_output_nonempty"] += int(has_external)
        aggregate["both_original_rainbow_and_external"] += int(original_rainbow and has_external)

        available = [i for i in range(1, 5) if edge("w", f"x{i}") in edges]
        aggregate["with_at_least_two_available_natural_switches"] += int(len(available) >= 2)
        individually_legal = []
        if original_rainbow and has_external:
            for index in available:
                if first_nonrainbow_witness(edges, frozenset((index,))) is None:
                    individually_legal.append(index)
        histogram[str(len(individually_legal))] += 1
        maximum_individually_legal = max(maximum_individually_legal, len(individually_legal))
        if len(individually_legal) >= 2:
            aggregate["with_at_least_two_individually_rainbow_switches"] += 1
            # This is the exact target; L4(2) could only filter it further.
            aggregate["target_instances"] += 1

        if earliest_valid is None and original_rainbow and has_external:
            try:
                cases = l4_2_cases(edges)
            except AssertionError:
                cases = 0
            if cases:
                earliest_valid = {
                    "neighbours_in_declared_order": list(neighbours),
                    "neighbours_sorted": sorted(neighbours),
                    "L4_2_cases": cases,
                }

    assert aggregate["expansions"] == 1716
    assert aggregate["target_instances"] == 0
    assert maximum_individually_legal < 2

    result = {
        "schema": "amra.erdos809.absorber-round5-independent-audit.v1",
        "engine": "independent prose reconstruction; no author-checker import",
        "base_graph": {"n": 14, "edges": 50},
        "named_expansion": {
            "n": 15,
            "edges": 57,
            "neighbours_of_w": sorted(named_neighbours),
            "A_is_closed_neighbourhood_of_v": set(adjacency(named_edges)["v"]) | {"v"} == A,
            "rainbow_C7": True,
            "C7_count": len(cycles),
            "L4_2": True,
            "L4_2_cases": l4_checks,
            "K_bc": [list(item) for item in sorted(reserve_bc)],
            "K_cw": [list(item) for item in sorted(reserve_cw)],
            "external_outputs": [list(item) for item in sorted(external)],
            "simple_paths_w_to_z": {"length_4": path4, "length_5": path5, "total": path4 + path5},
            "nonempty_switch_subsets": len(subset_results),
            "rainbow_nonempty_switch_subsets": 0,
            "nonrainbow_witnesses": subset_results,
        },
        "exhaustive_expansion_search": {
            **aggregate,
            "choice_set_size": len(EXPANSION_CHOICES),
            "neighbourhood_size": 7,
            "maximum_individually_rainbow_natural_switches": maximum_individually_legal,
            "individually_legal_histogram_over_all_expansions": histogram,
            "earliest_valid_under_declared_vertex_order": earliest_valid,
            "logical_strength": "target is absent before imposing L4(2), so adding L4(2) cannot create an instance",
        },
        "verdict": "finite certificate reproduced; no two-switch instance in the stated n15 natural-switch class",
        "scope": "finite one-vertex expansion and one switch type only; no larger-gadget exclusion and no public 1/8 change",
        "lean_used": False,
        "main_term_changed": False,
        "public_problem_changed": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
