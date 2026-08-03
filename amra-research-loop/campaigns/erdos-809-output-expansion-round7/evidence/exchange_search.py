#!/usr/bin/env python3
"""Exact natural-switch exchange search for the locked Erdos-809 graph.

Usage: ``python3 exchange_search.py 2`` reproduces the binary starting
firewall; ``python3 exchange_search.py 3`` searches the threshold-preserving
eighteen-new-edge/three-old-edge domain.
"""

from __future__ import annotations

from itertools import combinations
import json
import sys


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

ALL_NEW = frozenset(
    {edge(q, p) for q in ("w", "u") for p in V0 if p != "v"}
    | {edge("w", "u")}
)
REQUIRED = frozenset({edge("w", "x1"), edge("u", "x2")})
FORBIDDEN = frozenset({
    edge("w", "c"), edge("u", "c"),
    edge("w", "z"), edge("u", "z"),
    edge("w", "y1"), edge("u", "y2"),
})
OPTIONAL = tuple(sorted(ALL_NEW - REQUIRED - FORBIDDEN))
COLOUR_PAIRS = tuple(
    [(edge("b", f"x{i}"), edge("c", f"y{i}")) for i in range(1, 5)]
    + [(edge("w", "x1"), edge("c", "y1")),
       (edge("u", "x2"), edge("c", "y2"))]
)
REPEATED_OLD = frozenset(e for pair in COLOUR_PAIRS[:4] for e in pair)
DELETABLE_OLD = tuple(sorted(
    e for e in E0 if "v" not in e and e not in REPEATED_OLD
))

assert len(V) == 16 and len(E0) == 50
assert len(OPTIONAL) == 19 and len(DELETABLE_OLD) == 32


def adjacency(edges: frozenset[tuple[str, str]]) -> dict[str, frozenset[str]]:
    out = {p: set() for p in V}
    for p, q in edges:
        out[p].add(q)
        out[q].add(p)
    return {p: frozenset(qs) for p, qs in out.items()}


def pair_occurs_in_c7(adj, first, second) -> bool:
    start, current = first

    def extend(path: tuple[str, ...], used_second: bool) -> bool:
        if len(path) == 7:
            closing = edge(path[-1], start)
            return start in adj[path[-1]] and (used_second or closing == second)
        for nxt in sorted(adj[path[-1]]):
            if nxt == start or nxt in path:
                continue
            if extend(path + (nxt,), used_second or edge(path[-1], nxt) == second):
                return True
        return False

    return extend((start, current), first == second)


def colour_pairs_safe(adj) -> bool:
    return all(not pair_occurs_in_c7(adj, p, q) for p, q in COLOUR_PAIRS)


def all_states_safe(adj) -> dict[str, bool]:
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


def has_length_four_path(adj, start: str, end: str, forbidden: frozenset[str]) -> bool:
    def extend(path: tuple[str, ...]) -> bool:
        if len(path) == 5:
            return path[-1] == end
        for nxt in sorted(adj[path[-1]]):
            if nxt in forbidden or nxt in path:
                continue
            if len(path) < 4 and nxt == end:
                continue
            if extend(path + (nxt,)):
                return True
        return False

    return extend((start,))


def l4_2(adj) -> bool:
    for start, end in combinations(V, 2):
        available = [p for p in V if p not in (start, end)]
        for size in range(3):
            for deleted in combinations(available, size):
                if not has_length_four_path(adj, start, end, frozenset(deleted)):
                    return False
    return True


def reserve(edges: frozenset[tuple[str, str]], base: tuple[str, str]):
    adj = adjacency(edges)
    left, right = base
    nl, nr = adj[left] & B, adj[right] & B
    if any(q != r and r in adj[q] for q in nl for r in nr):
        return None
    missing = {edge(p, q) for p, q in combinations(B, 2) if edge(p, q) not in edges}
    result = {f for f in missing if left in f or right in f}
    result.update(edge(q, r) for q in nl for r in nr if q != r)
    return frozenset(result)


def matching_rank(neighbourhoods) -> int:
    owner = {}

    def augment(i: int, seen: set[tuple[str, str]]) -> bool:
        for output in sorted(neighbourhoods[i]):
            if output in seen:
                continue
            seen.add(output)
            if output not in owner or augment(owner[output], seen):
                owner[output] = i
                return True
        return False

    return sum(augment(i, set()) for i in range(len(neighbourhoods)))


def transversal_masks(size: int):
    deletion_sets = tuple(combinations(DELETABLE_OLD, size))
    bits_by_edge = {old: 0 for old in DELETABLE_OLD}
    for index, deletion_set in enumerate(deletion_sets):
        bit = 1 << index
        for old in deletion_set:
            bits_by_edge[old] |= bit
    return deletion_sets, bits_by_edge, (1 << len(deletion_sets)) - 1


def exact_hitting_sets(adj, bits_by_edge, all_bits):
    """Return exact surviving deletion-set bits and obstruction statistics."""
    possible = all_bits
    traces = 0
    protected = False

    for first, second in COLOUR_PAIRS:
        start, current = first

        def extend(path: tuple[str, ...], used_second: bool) -> bool:
            nonlocal possible, traces, protected
            if len(path) == 7:
                closing = edge(path[-1], start)
                if start not in adj[path[-1]] or not (used_second or closing == second):
                    return False
                traces += 1
                hit_bits = 0
                for i in range(7):
                    old = edge(path[i], path[(i + 1) % 7])
                    hit_bits |= bits_by_edge.get(old, 0)
                if hit_bits == 0:
                    protected = True
                possible &= hit_bits
                # Continue after transversal failure until protected-cycle
                # existence is also decided exactly.
                return possible == 0 and protected
            for nxt in sorted(adj[path[-1]]):
                if nxt == start or nxt in path:
                    continue
                if extend(path + (nxt,), used_second or edge(path[-1], nxt) == second):
                    return True
            return False

        if extend((start, current), first == second):
            break
    return possible, traces, protected


def selected_indices(bits: int):
    while bits:
        low = bits & -bits
        yield low.bit_length() - 1
        bits ^= low


def search(deletion_count: int) -> dict:
    if deletion_count not in (2, 3):
        raise ValueError("deletion count must be 2 or 3")
    choose_optional = 13 + deletion_count
    deletion_sets, bits_by_edge, all_bits = transversal_masks(deletion_count)
    expected_assignments = 3876 if deletion_count == 2 else 969

    counters = {
        "assignments_tested": 0,
        "bad_C7_traces_processed": 0,
        "assignments_with_protected_bad_C7": 0,
        "assignments_with_exact_hitting_set": 0,
        "exact_hitting_sets_total": 0,
        "pair_safe_after_deletion": 0,
        "base_singleton_joint_pass": 0,
        "L4_2_pass": 0,
        "reserve_defined": 0,
        "canonical_output_pass": 0,
        "matching_rank_four_pass": 0,
    }
    first_witness = None
    unprotected_empty_assignments = []

    for chosen in combinations(OPTIONAL, choose_optional):
        counters["assignments_tested"] += 1
        eplus = frozenset(set(E0) | set(REQUIRED) | set(chosen))
        assert len(eplus) == 65 + deletion_count
        bits, traces, protected = exact_hitting_sets(
            adjacency(eplus), bits_by_edge, all_bits
        )
        counters["bad_C7_traces_processed"] += traces
        counters["assignments_with_protected_bad_C7"] += int(protected)
        if bits == 0:
            if not protected:
                unprotected_empty_assignments.append({
                    "chosen_optional_edges": sorted(chosen),
                    "omitted_optional_edges": sorted(set(OPTIONAL) - set(chosen)),
                    "certified_transversal_number_lower_bound": deletion_count + 1,
                })
            continue
        counters["assignments_with_exact_hitting_set"] += 1
        counters["exact_hitting_sets_total"] += bits.bit_count()

        for deletion_index in selected_indices(bits):
            deleted = deletion_sets[deletion_index]
            edges = frozenset(set(eplus) - set(deleted))
            assert len(edges) == 65
            adj = adjacency(edges)
            if not colour_pairs_safe(adj):
                continue
            counters["pair_safe_after_deletion"] += 1
            states = all_states_safe(adj)
            if not all(states.values()):
                continue
            counters["base_singleton_joint_pass"] += 1
            if not l4_2(adj):
                continue
            counters["L4_2_pass"] += 1
            kbc = reserve(edges, edge("b", "c"))
            kcw = reserve(edges, edge("c", "w"))
            kcu = reserve(edges, edge("c", "u"))
            if None in (kbc, kcw, kcu):
                continue
            counters["reserve_defined"] += 1
            outputs = (edge("w", "z"), edge("u", "z"))
            if outputs[0] in kbc or outputs[1] in kbc:
                continue
            if outputs[0] not in kcw or outputs[1] not in kcu:
                continue
            counters["canonical_output_pass"] += 1
            old = (kbc,) * 4
            augmented = (
                frozenset(set(kbc) | {outputs[0]}),
                frozenset(set(kbc) | {outputs[1]}),
                kbc,
                kbc,
            )
            old_rank = matching_rank(old)
            new_rank = matching_rank(augmented)
            if new_rank != 4:
                continue
            counters["matching_rank_four_pass"] += 1
            if first_witness is None:
                first_witness = {
                    "deleted_old_edges": [list(e) for e in deleted],
                    "new_edges": sorted(set(REQUIRED) | set(chosen)),
                    "degrees": {p: len(adj[p]) for p in V},
                    "rainbow_states": states,
                    "L4_2": True,
                    "A_is_closed_neighbourhood": adj["v"] | {"v"} == A,
                    "K_bc": sorted(kbc),
                    "K_cw": sorted(kcw),
                    "K_cu": sorted(kcu),
                    "outputs": [list(f) for f in outputs],
                    "old_matching_rank": old_rank,
                    "augmented_matching_rank": new_rank,
                }

    assert counters["assignments_tested"] == expected_assignments
    return {
        "schema": f"amra.erdos809.output-expansion-round7.exchange-{deletion_count}.v1",
        "deletion_count": deletion_count,
        "new_edge_count": 15 + deletion_count,
        "optional_edges_chosen": choose_optional,
        "new_edge_assignments": expected_assignments,
        "admissible_old_edges": len(DELETABLE_OLD),
        "deletion_sets_per_assignment": len(deletion_sets),
        "raw_assignment_deletion_sets": expected_assignments * len(deletion_sets),
        **counters,
        "unprotected_assignments_with_empty_hitting_set": unprotected_empty_assignments,
        "first_witness": first_witness,
        "model": "require wx1,ux2; forbid cw,cu,wz,uz,wy1,uy2; retain A=N[v] and all named base-colour edges",
        "completeness": "Complete for the displayed natural-switch exchange domain. The excluded cross edges contradict L4(2) plus switched rainbow-C7 legality; v-incident and repeated-colour old edges cannot be deleted while retaining the frozen interface.",
        "finite_result_only": True,
        "public_problem_changed": False,
        "lean_used": False,
    }


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) == 2 else 3
    print(json.dumps(search(count), indent=2, sort_keys=True))
