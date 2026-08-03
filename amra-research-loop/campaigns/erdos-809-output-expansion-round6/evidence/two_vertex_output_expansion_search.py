#!/usr/bin/env python3
"""Exact search for two distinct natural-switch outputs on an n=16 extension."""

from __future__ import annotations

from itertools import combinations
import json


def edge(u: str, v: str) -> tuple[str, str]:
    return tuple(sorted((u, v)))


X = tuple(f"x{i}" for i in range(1, 5))
Y = tuple(f"y{i}" for i in range(1, 5))
A = frozenset(("v",) + X + Y + ("r1", "r2"))
B0 = frozenset(("b", "c", "z"))
V0 = tuple(sorted(A | B0))
V = tuple(sorted(set(V0) | {"w", "u"}))
B = frozenset(("b", "c", "z", "w", "u"))

removed = {edge("x1", "x2"), edge("y1", "y2")}
E0 = {
    edge(p, q)
    for p, q in combinations(A, 2)
    if not ((p in X and q in Y) or (p in Y and q in X))
    and edge(p, q) not in removed
}
E0.update(edge("b", p) for p in X)
E0.update(edge("c", q) for q in Y)
E0.add(edge("b", "z"))
E0.update(edge("z", p) for p in X)
E0 = frozenset(E0)

REQUIRED = frozenset(
    {edge("w", p) for p in X} | {edge("u", p) for p in X}
)
FORBIDDEN = frozenset({
    edge("w", "z"), edge("u", "z"),
    edge("w", "c"), edge("u", "c"),
})
ALL_NEW = frozenset(
    {edge(q, p) for q in ("w", "u") for p in V0 if p != "v"}
    | {edge("w", "u")}
)
OPTIONAL = tuple(sorted(ALL_NEW - REQUIRED - FORBIDDEN))
assert len(E0) == 50 and len(REQUIRED) == 8 and len(OPTIONAL) == 15


def adjacency(E: frozenset[tuple[str, str]]) -> dict[str, frozenset[str]]:
    out = {p: set() for p in V}
    for p, q in E:
        out[p].add(q)
        out[q].add(p)
    return {p: frozenset(qs) for p, qs in out.items()}


def pair_occurs_in_c7(
    adj: dict[str, frozenset[str]], first: tuple[str, str], second: tuple[str, str]
) -> bool:
    # Fix first as the initial edge and enumerate the remaining six-edge
    # simple path back to its first endpoint.
    start, current = first

    def extend(path: tuple[str, ...], used_second: bool) -> bool:
        if len(path) == 7:
            closing = edge(path[-1], start)
            return start in adj[path[-1]] and (used_second or closing == second)
        for nxt in adj[path[-1]]:
            if nxt == start or nxt in path:
                continue
            if extend(path + (nxt,), used_second or edge(path[-1], nxt) == second):
                return True
        return False

    return extend((start, current), first == second)


def colour_pairs_safe(adj: dict[str, frozenset[str]]) -> bool:
    pairs = [(edge("b", f"x{i}"), edge("c", f"y{i}")) for i in range(1, 5)]
    pairs.extend([
        (edge("w", "x1"), edge("c", "y1")),
        (edge("u", "x2"), edge("c", "y2")),
    ])
    return all(not pair_occurs_in_c7(adj, p, q) for p, q in pairs)


COLOUR_PAIRS = tuple(
    [(edge("b", f"x{i}"), edge("c", f"y{i}")) for i in range(1, 5)]
    + [
        (edge("w", "x1"), edge("c", "y1")),
        (edge("u", "x2"), edge("c", "y2")),
    ]
)
REPEATED_OLD = frozenset(e for pair in COLOUR_PAIRS[:4] for e in pair)
DELETABLE_OLD = frozenset(
    e for e in E0 if "v" not in e and e not in REPEATED_OLD
)


def common_old_edge_hitting_all_bad_cycles(
    adj: dict[str, frozenset[str]]
) -> frozenset[tuple[str, str]]:
    """Old edges whose deletion destroys every bad cycle for all six pairs."""
    possible = set(DELETABLE_OLD)
    saw_bad = False
    for first, second in COLOUR_PAIRS:
        start, current = first

        def extend(path: tuple[str, ...], used_second: bool) -> bool:
            nonlocal possible, saw_bad
            if len(path) == 7:
                closing = edge(path[-1], start)
                if start not in adj[path[-1]] or not (used_second or closing == second):
                    return False
                saw_bad = True
                cycle_edges = {
                    edge(path[i], path[(i + 1) % 7]) for i in range(7)
                }
                possible.intersection_update(cycle_edges)
                return not possible
            for nxt in adj[path[-1]]:
                if nxt == start or nxt in path:
                    continue
                if extend(path + (nxt,), used_second or edge(path[-1], nxt) == second):
                    return True
            return False

        if extend((start, current), first == second):
            return frozenset()
    return frozenset(possible if saw_bad else DELETABLE_OLD)


def has_length_four_path(
    adj: dict[str, frozenset[str]], start: str, end: str, forbidden: frozenset[str]
) -> bool:
    def extend(path: tuple[str, ...]) -> bool:
        if len(path) == 5:
            return path[-1] == end
        for nxt in adj[path[-1]]:
            if nxt in forbidden or nxt in path:
                continue
            if len(path) < 4 and nxt == end:
                continue
            if extend(path + (nxt,)):
                return True
        return False
    return extend((start,))


def l4_2(adj: dict[str, frozenset[str]]) -> bool:
    for start, end in combinations(V, 2):
        available = [p for p in V if p not in (start, end)]
        for size in range(3):
            for deleted in combinations(available, size):
                if not has_length_four_path(adj, start, end, frozenset(deleted)):
                    return False
    return True


def reserve(E: frozenset[tuple[str, str]], base: tuple[str, str]):
    adj = adjacency(E)
    left, right = base
    nl, nr = adj[left] & B, adj[right] & B
    if any(q != r and r in adj[q] for q in nl for r in nr):
        return None
    missing = {edge(p, q) for p, q in combinations(B, 2) if edge(p, q) not in E}
    result = {f for f in missing if left in f or right in f}
    result.update(edge(q, r) for q in nl for r in nr if q != r)
    return frozenset(result)


def matching_rank(neighbourhoods: tuple[frozenset[tuple[str, str]], ...]) -> int:
    owner = {}
    def augment(i: int, seen: set[tuple[str, str]]) -> bool:
        for f in neighbourhoods[i]:
            if f in seen:
                continue
            seen.add(f)
            if f not in owner or augment(owner[f], seen):
                owner[f] = i
                return True
        return False
    return sum(augment(i, set()) for i in range(len(neighbourhoods)))


def all_states_safe(adj: dict[str, frozenset[str]]) -> dict[str, bool]:
    base = [(edge("b", f"x{i}"), edge("c", f"y{i}")) for i in range(1, 5)]
    states = {
        "base": base,
        "switch_w1": [(edge("w", "x1"), edge("c", "y1"))] + base[1:],
        "switch_u2": [base[0], (edge("u", "x2"), edge("c", "y2"))] + base[2:],
        "joint": [
            (edge("w", "x1"), edge("c", "y1")),
            (edge("u", "x2"), edge("c", "y2")),
        ] + base[2:],
    }
    return {
        name: all(not pair_occurs_in_c7(adj, p, q) for p, q in pairs)
        for name, pairs in states.items()
    }


def main() -> None:
    tested = pair_safe = l4_pass = 0
    witness = None
    for chosen in combinations(OPTIONAL, 7):
        tested += 1
        E = frozenset(set(E0) | set(REQUIRED) | set(chosen))
        assert len(E) == 65 == len(V)**2 // 4 + 1
        adj = adjacency(E)
        if not colour_pairs_safe(adj):
            continue
        pair_safe += 1
        if not l4_2(adj):
            continue
        l4_pass += 1
        states = all_states_safe(adj)
        assert all(states.values())
        kbc = reserve(E, edge("b", "c"))
        kcw = reserve(E, edge("c", "w"))
        kcu = reserve(E, edge("c", "u"))
        outputs = (edge("w", "z"), edge("u", "z"))
        if None in (kbc, kcw, kcu):
            continue
        if outputs[0] in kbc or outputs[1] in kbc:
            continue
        if outputs[0] not in kcw or outputs[1] not in kcu:
            continue
        old = (kbc,)*4
        augmented = (
            frozenset(set(kbc) | {outputs[0]}),
            frozenset(set(kbc) | {outputs[1]}),
            kbc,
            kbc,
        )
        witness = {
            "chosen_optional_edges": sorted(chosen),
            "new_edges": sorted(set(REQUIRED) | set(chosen)),
            "degrees": {p: len(adj[p]) for p in V},
            "K_bc": sorted(kbc),
            "K_cw": sorted(kcw),
            "K_cu": sorted(kcu),
            "distinct_outputs": [list(f) for f in outputs],
            "rainbow_states": states,
            "old_matching_rank": matching_rank(old),
            "augmented_matching_rank": matching_rank(augmented),
            "L4_2": True,
            "A_is_closed_neighbourhood": adj["v"] | {"v"} == A,
        }
        break

    exchange_tested = exchange_hittable = exchange_l4 = 0
    exchange_witness = None
    if witness is None:
        # One edge exchange means sixteen new edges and one old deletion.
        # In the symmetric subfamily this is REQUIRED plus eight OPTIONAL.
        for chosen in combinations(OPTIONAL, 8):
            exchange_tested += 1
            Eplus = frozenset(set(E0) | set(REQUIRED) | set(chosen))
            adj_plus = adjacency(Eplus)
            deletion_candidates = common_old_edge_hitting_all_bad_cycles(adj_plus)
            if not deletion_candidates:
                continue
            exchange_hittable += 1
            for deleted in sorted(deletion_candidates):
                E = frozenset(set(Eplus) - {deleted})
                assert len(E) == 65
                adj = adjacency(E)
                if not colour_pairs_safe(adj) or not l4_2(adj):
                    continue
                exchange_l4 += 1
                states = all_states_safe(adj)
                kbc = reserve(E, edge("b", "c"))
                kcw = reserve(E, edge("c", "w"))
                kcu = reserve(E, edge("c", "u"))
                outputs = (edge("w", "z"), edge("u", "z"))
                if None in (kbc, kcw, kcu):
                    continue
                if outputs[0] in kbc or outputs[1] in kbc:
                    continue
                if outputs[0] not in kcw or outputs[1] not in kcu:
                    continue
                old = (kbc,)*4
                augmented = (
                    frozenset(set(kbc) | {outputs[0]}),
                    frozenset(set(kbc) | {outputs[1]}),
                    kbc,
                    kbc,
                )
                exchange_witness = {
                    "deleted_old_edge": list(deleted),
                    "chosen_optional_edges": sorted(chosen),
                    "new_edges": sorted(set(REQUIRED) | set(chosen)),
                    "degrees": {p: len(adj[p]) for p in V},
                    "K_bc": sorted(kbc),
                    "K_cw": sorted(kcw),
                    "K_cu": sorted(kcu),
                    "distinct_outputs": [list(f) for f in outputs],
                    "rainbow_states": states,
                    "old_matching_rank": matching_rank(old),
                    "augmented_matching_rank": matching_rank(augmented),
                    "L4_2": True,
                    "A_is_closed_neighbourhood": adj["v"] | {"v"} == A,
                }
                break
            if exchange_witness is not None:
                break

    print(json.dumps({
        "schema": "amra.erdos809.output-expansion-round6.two-vertex-search.v1",
        "model": "add w,u to B; add all w-X,u-X plus seven of fifteen optional incident edges; forbid cw,cu,wz,uz; no old-edge deletion",
        "search_space": 6435,
        "assignments_tested": tested,
        "pair_safe_assignments": pair_safe,
        "L4_2_pass_assignments_before_first_witness": l4_pass,
        "first_witness": witness,
        "one_old_edge_exchange_search": {
            "search_space": 6435,
            "assignments_tested": exchange_tested,
            "assignments_with_common_old_edge_hitting_every_bad_C7": exchange_hittable,
            "L4_2_pass_before_first_witness": exchange_l4,
            "first_witness": exchange_witness
        },
        "joint_legality_note": "For fixed-graph recolouring of disjoint colour classes, a C7 is non-rainbow iff it contains both edges of at least one repeated pair; hence safety of all involved pairs implies every switch subset is safe.",
        "finite_scope": "Complete only for the displayed symmetric no-deletion n16 subfamily.",
        "public_problem_changed": False,
        "lean_used": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
