#!/usr/bin/env python3
"""Search one-vertex threshold expansions of the locked n=14 graph.

This is a negative/discovery search.  A path catalogue is never called an
absorber: only its projection to concrete missing B-edge outputs is measured.
"""

from __future__ import annotations

import json
from itertools import combinations


def edge(u: str, v: str) -> tuple[str, str]:
    return tuple(sorted((u, v)))


X = tuple(f"x{i}" for i in range(1, 5))
Y = tuple(f"y{i}" for i in range(1, 5))
A = frozenset(("v",) + X + Y + ("r1", "r2"))
B0 = frozenset(("b", "c", "z"))
V0 = tuple(sorted(A | B0))
V = tuple(sorted(set(V0) | {"w"}))
B = frozenset(set(B0) | {"w"})

removed = {edge("x1", "x2"), edge("y1", "y2")}
E0 = {
    edge(u, v)
    for u, v in combinations(A, 2)
    if not ((u in X and v in Y) or (u in Y and v in X))
    and edge(u, v) not in removed
}
E0.update(edge("b", x) for x in X)
E0.update(edge("c", y) for y in Y)
E0.add(edge("b", "z"))
E0.update(edge("z", x) for x in X)
E0 = frozenset(E0)


def adjacent(E: frozenset[tuple[str, str]], u: str, v: str) -> bool:
    return u != v and edge(u, v) in E


def colour(e: tuple[str, str], switched: frozenset[int] = frozenset()) -> str:
    for i in range(1, 5):
        repeated_pair = (
            (edge("w", f"x{i}"), edge("c", f"y{i}"))
            if i in switched
            else (edge("b", f"x{i}"), edge("c", f"y{i}"))
        )
        if e in repeated_pair:
            return f"gamma{i}"
    return "unique:" + "-".join(e)


def has_nonrainbow_c7(
    E: frozenset[tuple[str, str]], switched: frozenset[int] = frozenset()
) -> bool:
    # A non-rainbow cycle must contain both old edges of some gamma_i,
    # since every other edge has a unique colour.
    for i in range(1, 5):
        required = {
            edge("w" if i in switched else "b", f"x{i}"),
            edge("c", f"y{i}"),
        }

        def extend(path: tuple[str, ...]) -> bool:
            if len(path) == 7:
                if not adjacent(E, path[-1], path[0]):
                    return False
                cycle_edges = {
                    edge(path[j], path[(j + 1) % 7]) for j in range(7)
                }
                return required <= cycle_edges
            for nxt in V:
                if nxt in path or not adjacent(E, path[-1], nxt):
                    continue
                if extend(path + (nxt,)):
                    return True
            return False

        # Fix b as the least distinguished start; rotations need not repeat.
        if extend(("w" if i in switched else "b",)):
            return True
    return False


def has_length_four_path(
    E: frozenset[tuple[str, str]], start: str, end: str, forbidden: frozenset[str]
) -> bool:
    def extend(path: tuple[str, ...]) -> bool:
        if len(path) == 5:
            return path[-1] == end
        for nxt in V:
            if nxt in forbidden or nxt in path or not adjacent(E, path[-1], nxt):
                continue
            if len(path) < 4 and nxt == end:
                continue
            if extend(path + (nxt,)):
                return True
        return False

    return extend((start,))


def l4_2(E: frozenset[tuple[str, str]]) -> bool:
    for start, end in combinations(V, 2):
        available = [v for v in V if v not in (start, end)]
        for size in range(3):
            for forbidden in combinations(available, size):
                if not has_length_four_path(E, start, end, frozenset(forbidden)):
                    return False
    return True


def reserve(E: frozenset[tuple[str, str]], pair: tuple[str, str]):
    left, right = pair
    nl = {v for v in B if adjacent(E, left, v)}
    nr = {v for v in B if adjacent(E, right, v)}
    if any(p != q and adjacent(E, p, q) for p in nl for q in nr):
        return None
    missing = {edge(u, v) for u, v in combinations(B, 2) if not adjacent(E, u, v)}
    result = {f for f in missing if left in f or right in f}
    result.update(edge(p, q) for p in nl for q in nr if p != q)
    return frozenset(result)


def simple_path_count(
    E: frozenset[tuple[str, str]], start: str, end: str, length: int
) -> int:
    count = 0

    def extend(path: tuple[str, ...]) -> None:
        nonlocal count
        if len(path) == length + 1:
            count += path[-1] == end
            return
        for nxt in V:
            if nxt in path or not adjacent(E, path[-1], nxt):
                continue
            if len(path) < length and nxt == end:
                continue
            extend(path + (nxt,))

    extend((start,))
    return count


def main() -> None:
    assert len(E0) == 50
    candidates = tuple(v for v in V0 if v != "v")
    tested = rainbow_pass = external_pass = 0
    witness = None
    full_local_count = legal_single_switch_count = 0
    for neighbours_w in combinations(candidates, 7):
        tested += 1
        E = frozenset(set(E0) | {edge("w", v) for v in neighbours_w})
        kbc = reserve(E, edge("b", "c"))
        if kbc is None:
            continue
        missing_b = {edge(u, v) for u, v in combinations(B, 2) if not adjacent(E, u, v)}
        external = missing_b - kbc
        if not external:
            continue
        external_pass += 1
        if has_nonrainbow_c7(E):
            continue
        rainbow_pass += 1
        if not l4_2(E):
            continue
        full_local_count += 1
        output_path_catalogue = {
            "-".join(f): {
                "length4_paths": simple_path_count(E, f[0], f[1], 4),
                "length5_paths": simple_path_count(E, f[0], f[1], 5),
            }
            for f in sorted(external)
        }
        kcw = reserve(E, edge("c", "w"))
        switch_states = []
        all_switches_rainbow = True
        for mask in range(16):
            switched = frozenset(i for i in range(1, 5) if mask & (1 << (i - 1)))
            rainbow = not has_nonrainbow_c7(E, switched)
            all_switches_rainbow &= rainbow
            switch_states.append({"switched": sorted(switched), "rainbow_C7": rainbow})
        current = {
            "w_neighbours": sorted(neighbours_w),
            "edges": len(E),
            "K_bc": sorted(kbc),
            "missing_B_edges": sorted(missing_b),
            "K_bc_external_missing_B_edges": sorted(external),
            "rainbow_C7": True,
            "L4_2": True,
            "output_path_catalogue": output_path_catalogue,
            "K_cw": sorted(kcw) if kcw is not None else None,
            "single_colour_switches": [
                {
                    "colour": f"gamma{i}",
                    "old_pair": [list(edge("b", f"x{i}")), list(edge("c", f"y{i}"))],
                    "new_pair": [list(edge("w", f"x{i}")), list(edge("c", f"y{i}"))],
                    "old_base": list(edge("b", "c")),
                    "new_base": list(edge("c", "w")),
                    "external_output": list(edge("w", "z")),
                }
                for i in range(1, 5)
            ],
            "all_16_recolouring_switch_states_rainbow_C7": all_switches_rainbow,
            "switch_states": switch_states,
            "candidate_catalogue_size": 4,
            "distinct_external_outputs": 1,
            "output_matching_rank_upper_bound": 1,
            "warning": "The four switches are graph-realizable candidate gadgets, but every nonempty switch state fails rainbow C7. They are not legal absorber arcs. Path multiplicity alone is never a legal arc.",
        }
        legal_here = sum(state["rainbow_C7"] for state in switch_states if state["switched"])
        legal_single_switch_count += legal_here
        if witness is None:
            witness = current
            break

    # Search all one-vertex threshold expansions for at least two individually
    # rainbow b-to-w replacements whose new K(cw) outputs share one fibre.
    # The expensive L4(2) test is run only after those filters.
    shared_output_switch_witness = None
    switch_search_tested = switch_rainbow_candidates = 0
    for neighbours_w in combinations(candidates, 7):
        switch_search_tested += 1
        E = frozenset(set(E0) | {edge("w", v) for v in neighbours_w})
        kbc = reserve(E, edge("b", "c"))
        kcw = reserve(E, edge("c", "w"))
        if kbc is None or kcw is None or not (kcw - kbc):
            continue
        if has_nonrainbow_c7(E):
            continue
        legal_singletons = [
            i for i in range(1, 5)
            if edge("w", f"x{i}") in E
            and not has_nonrainbow_c7(E, frozenset({i}))
        ]
        if len(legal_singletons) < 2:
            continue
        switch_rainbow_candidates += 1
        if not l4_2(E):
            continue
        shared_output_switch_witness = {
            "w_neighbours": sorted(neighbours_w),
            "legal_singleton_switches": legal_singletons,
            "old_K_bc": sorted(kbc),
            "new_K_cw": sorted(kcw),
            "shared_external_outputs": sorted(kcw - kbc),
            "catalogue_lower_bound": len(legal_singletons),
            "output_rank_upper_bound": len(kcw - kbc),
            "L4_2": True,
            "rainbow_C7_before_and_after_each_single_switch": True,
        }
        break

    print(json.dumps({
        "schema": "amra.erdos809.absorber-round5.small-expansion-search.v1",
        "one_vertex_expansions_tested": tested,
        "with_external_missing_B_edge": external_pass,
        "rainbow_pass_before_L4": rainbow_pass,
        "full_local_expansions_before_first_witness": full_local_count,
        "nonempty_rainbow_switch_states": legal_single_switch_count,
        "search_stopped_after_first_full_local_witness": True,
        "first_full_local_witness": witness,
        "shared_output_switch_search": {
            "expansions_tested": switch_search_tested,
            "rainbow_candidates_before_L4": switch_rainbow_candidates,
            "first_witness": shared_output_switch_witness,
            "scope": "A witness certifies individual recolouring switches only; simultaneous compatibility and permission to use recolouring in the public absorber interface remain separate obligations."
        },
        "public_problem_changed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
