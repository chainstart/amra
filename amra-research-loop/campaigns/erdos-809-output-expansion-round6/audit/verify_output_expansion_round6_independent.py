#!/usr/bin/env python3
"""Blind exact audit of the round-six two-output finite models.

The checker reconstructs the locked graph and streams subset-DP summaries of
all bad C7 traces.  It imports no author search functions or result data.
"""

from __future__ import annotations

from itertools import combinations
import json
import math


def edge(u: str, v: str) -> tuple[str, str]:
    return tuple(sorted((u, v)))


OLD_VERTICES = tuple(
    ["v"] + [f"x{i}" for i in range(1, 5)] + [f"y{i}" for i in range(1, 5)]
    + ["r1", "r2", "b", "c", "z"]
)
VERTICES = OLD_VERTICES + ("w", "u")
X = frozenset(f"x{i}" for i in range(1, 5))
Y = frozenset(f"y{i}" for i in range(1, 5))
A = frozenset(OLD_VERTICES[:11])


def old_graph() -> frozenset[tuple[str, str]]:
    removed = {edge("x1", "x2"), edge("y1", "y2")}
    result = {
        edge(left, right)
        for left, right in combinations(A, 2)
        if not ({left, right} & X and {left, right} & Y)
        and edge(left, right) not in removed
    }
    result.update(edge("b", item) for item in X)
    result.update(edge("c", item) for item in Y)
    result.add(edge("b", "z"))
    result.update(edge("z", item) for item in X)
    return frozenset(result)


OLD_EDGES = old_graph()
OLD_EDGE_LIST = tuple(sorted(OLD_EDGES))
OLD_EDGE_INDEX = {item: index for index, item in enumerate(OLD_EDGE_LIST)}
ALL_OLD_MASK = (1 << len(OLD_EDGE_LIST)) - 1


COLOUR_PAIRS = (
    (edge("b", "x1"), edge("c", "y1")),
    (edge("b", "x2"), edge("c", "y2")),
    (edge("b", "x3"), edge("c", "y3")),
    (edge("b", "x4"), edge("c", "y4")),
    (edge("w", "x1"), edge("c", "y1")),
    (edge("u", "x2"), edge("c", "y2")),
)


def all_new_edges() -> frozenset[tuple[str, str]]:
    return frozenset(
        edge(left, right)
        for left, right in combinations(VERTICES, 2)
        if "w" in (left, right) or "u" in (left, right)
    )


NEW_EDGES = all_new_edges()
COMMON_FORBIDDEN = frozenset(
    (edge("v", "w"), edge("v", "u"), edge("c", "w"), edge("c", "u"), edge("w", "z"), edge("u", "z"))
)


def adjacency(edges: frozenset[tuple[str, str]]) -> dict[str, tuple[str, ...]]:
    rows = {vertex: [] for vertex in VERTICES}
    for left, right in edges:
        rows[left].append(right)
        rows[right].append(left)
    return {vertex: tuple(sorted(row)) for vertex, row in rows.items()}


def cycles_with_pair(
    graph_edges: frozenset[tuple[str, str]], pair: tuple[tuple[str, str], tuple[str, str]]
) -> frozenset[frozenset[tuple[str, str]]]:
    adj = adjacency(graph_edges)
    first, second = pair
    start, nxt = first
    assert nxt in adj[start] and second in graph_edges
    path = [start, nxt]
    found: set[frozenset[tuple[str, str]]] = set()

    def visit() -> None:
        if len(path) == 7:
            if start not in adj[path[-1]]:
                return
            cycle = frozenset(edge(path[index], path[(index + 1) % 7]) for index in range(7))
            if second in cycle:
                found.add(cycle)
            return
        for candidate in adj[path[-1]]:
            if candidate == start or candidate in path:
                continue
            path.append(candidate)
            visit()
            path.pop()

    visit()
    return frozenset(found)


def trace_table(
    required: frozenset[tuple[str, str]], optional: tuple[tuple[str, str], ...]
) -> tuple[list[bool], list[int], dict[str, int]]:
    optional_index = {item: index for index, item in enumerate(optional)}
    maximal = OLD_EDGES | required | frozenset(optional)
    size = 1 << len(optional)
    present = [False] * size
    intersection = [ALL_OLD_MASK] * size
    total_cycles = 0
    exact_traces: set[tuple[int, int]] = set()

    for pair in COLOUR_PAIRS:
        for cycle in cycles_with_pair(maximal, pair):
            new_part = cycle - OLD_EDGES
            assert new_part <= required | frozenset(optional)
            mask = 0
            for item in new_part - required:
                mask |= 1 << optional_index[item]
            old_mask = 0
            for item in cycle & OLD_EDGES:
                old_mask |= 1 << OLD_EDGE_INDEX[item]
            present[mask] = True
            intersection[mask] &= old_mask
            exact_traces.add((mask, old_mask))
            total_cycles += 1

    # Subset zeta transform: after processing, entry M summarizes all exact
    # bad cycles whose optional trace is a subset of M.
    for bit in range(len(optional)):
        step = 1 << bit
        for mask in range(size):
            if mask & step:
                below = mask ^ step
                present[mask] = present[mask] or present[below]
                intersection[mask] &= intersection[below]

    return present, intersection, {
        "pair_cycle_occurrences": total_cycles,
        "distinct_trace_oldmask_pairs": len(exact_traces),
        "optional_edges": len(optional),
    }


def choose_masks(count: int, selected: int):
    for indices in combinations(range(count), selected):
        mask = 0
        for index in indices:
            mask |= 1 << index
        yield mask


def symmetric_search() -> dict[str, object]:
    required = frozenset(edge(new, old) for new in ("w", "u") for old in X)
    allowed = NEW_EDGES - COMMON_FORBIDDEN
    optional = tuple(sorted(allowed - required))
    assert len(required) == 8 and len(optional) == 15
    present, intersections, trace_stats = trace_table(required, optional)

    no_deletion_total = no_deletion_safe = 0
    for mask in choose_masks(15, 7):
        no_deletion_total += 1
        no_deletion_safe += not present[mask]
    assert no_deletion_total == math.comb(15, 7) == 6435
    assert no_deletion_safe == 0

    exchange_total = exchange_with_any_old_hit = 0
    maximum_common_old_edges = 0
    for mask in choose_masks(15, 8):
        exchange_total += 1
        common = intersections[mask] if present[mask] else ALL_OLD_MASK
        hits = common.bit_count()
        maximum_common_old_edges = max(maximum_common_old_edges, hits)
        exchange_with_any_old_hit += hits > 0
    assert exchange_total == math.comb(15, 8) == 6435
    assert exchange_with_any_old_hit == 0

    return {
        "required_new_edges": [list(item) for item in sorted(required)],
        "optional_new_edges": [list(item) for item in optional],
        "trace_statistics": trace_stats,
        "no_deletion": {"assignments": no_deletion_total, "pair_safe": no_deletion_safe},
        "one_exchange": {
            "assignments": exchange_total,
            "with_any_old_edge_hitting_every_bad_C7": exchange_with_any_old_hit,
            "maximum_common_old_edges": maximum_common_old_edges,
            "logical_strength": "no old edge at all is a common hit, stronger than filtering to admissible deletions",
        },
    }


def general_search() -> dict[str, object]:
    required = frozenset((edge("w", "x1"), edge("u", "x2")))
    forbidden = COMMON_FORBIDDEN | frozenset((edge("w", "y1"), edge("u", "y2")))
    allowed = NEW_EDGES - forbidden
    optional = tuple(sorted(allowed - required))
    assert len(required) == 2 and len(optional) == 19
    present, intersections, trace_stats = trace_table(required, optional)

    total = with_any_old_hit = 0
    maximum_common_old_edges = 0
    for mask in choose_masks(19, 14):
        total += 1
        common = intersections[mask] if present[mask] else ALL_OLD_MASK
        hits = common.bit_count()
        maximum_common_old_edges = max(maximum_common_old_edges, hits)
        with_any_old_hit += hits > 0
    assert total == math.comb(19, 14) == 11628
    assert with_any_old_hit == 0
    return {
        "required_new_edges": [list(item) for item in sorted(required)],
        "forbidden_new_edges": [list(item) for item in sorted(forbidden)],
        "optional_new_edges": [list(item) for item in optional],
        "trace_statistics": trace_stats,
        "one_exchange": {
            "assignments": total,
            "with_any_old_edge_hitting_every_bad_C7": with_any_old_hit,
            "maximum_common_old_edges": maximum_common_old_edges,
            "logical_strength": "no old edge at all is a common hit, stronger than filtering to admissible deletions",
        },
    }


def length_four_path_avoiding_edge(
    start: str, end: str, forbidden_vertex: str, forbidden_edge: tuple[str, str]
) -> tuple[str, ...] | None:
    adj = adjacency(OLD_EDGES - {forbidden_edge})
    path = [start]

    def visit() -> tuple[str, ...] | None:
        if len(path) == 5:
            return tuple(path) if path[-1] == end else None
        for candidate in adj[path[-1]]:
            if candidate == forbidden_vertex or candidate in path:
                continue
            if candidate == end and len(path) != 4:
                continue
            path.append(candidate)
            answer = visit()
            if answer is not None:
                return answer
            path.pop()
        return None

    return visit()


def l4_exclusion() -> dict[str, object]:
    examples = {}
    protected_colour_edges = frozenset(
        edge("b", f"x{i}") for i in range(1, 5)
    ) | frozenset(edge("c", f"y{i}") for i in range(1, 5))
    admissible_for_colour_model = tuple(item for item in OLD_EDGE_LIST if item not in protected_colour_edges)
    for index, (x_i, y_i) in enumerate((("x1", "y1"), ("x2", "y2")), start=1):
        witnesses = []
        for deleted in admissible_for_colour_model:
            path = length_four_path_avoiding_edge(x_i, "c", y_i, deleted)
            assert path is not None
            witnesses.append(path)
        examples[f"switch_{index}"] = {
            "old_deletions_checked": len(witnesses),
            "example_path": list(witnesses[0]),
            "conclusion": f"adding the forbidden new edge to {y_i} always closes a bad C7 after any colour-preserving old-edge deletion",
        }
    return {
        "protected_repeated_colour_edges": [list(item) for item in sorted(protected_colour_edges)],
        "admissible_colour_preserving_old_deletions": len(admissible_for_colour_model),
        "switches": examples,
        "L4_argument": "for a deleted old edge choose one non-endpoint vertex of that edge and delete it together with y_i; L4(2) supplies an x_i-to-c four-path avoiding the deletion and y_i",
    }


def matching_audit() -> dict[str, object]:
    old = (frozenset(("bc", "cz")),) * 4
    augmented = (
        frozenset(("bc", "cz", "wz")),
        frozenset(("bc", "cz", "uz")),
        old[2], old[3],
    )

    def matching_number(rows: tuple[frozenset[str], ...]) -> int:
        states = {frozenset()}
        for row in rows:
            states |= {used | {item} for used in tuple(states) for item in row - used}
        return max(map(len, states))

    def max_deficiency(rows: tuple[frozenset[str], ...]) -> int:
        answer = 0
        for mask in range(1 << len(rows)):
            neighbours = set()
            for index, row in enumerate(rows):
                if mask >> index & 1:
                    neighbours.update(row)
            answer = max(answer, mask.bit_count() - len(neighbours))
        return answer

    assert matching_number(old) == 2 and max_deficiency(old) == 2
    assert matching_number(augmented) == 4 and max_deficiency(augmented) == 0
    return {
        "old_rank": 2, "old_maximum_deficiency": 2,
        "augmented_rank": 4, "augmented_maximum_deficiency": 0,
        "explicit_matching": ["wz", "uz", "bc", "cz"],
        "typing": "conditional augmentation of the frozen n14 K(4,2) carrier graph; it does not construct legal arcs",
    }


def main() -> None:
    assert len(OLD_EDGES) == 50
    result = {
        "schema": "amra.erdos809.output-expansion-round6-independent-audit.v1",
        "engine": "independent graph/C7 trace reconstruction; no author-checker import",
        "base_graph": {"vertices": 14, "edges": 50},
        "joint_legality": {
            "status": "proved",
            "proof": "a repeated colour on a joint-state C7 is either untouched and already bad in the base, or switched in one disjoint colour class and already bad in that singleton",
            "scope": "fixed graph and disjoint recoloured classes only",
        },
        "symmetric_models": symmetric_search(),
        "general_model": general_search(),
        "forbidden_wy1_uy2": l4_exclusion(),
        "conditional_matching": matching_audit(),
        "scope": "three exact finite natural-switch models and conditional K(4,2) allocation only",
        "public_one_eighth_changed": False,
        "lean_used": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
