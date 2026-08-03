#!/usr/bin/env python3
"""Exact general one-old-edge exchange search for two natural outputs."""

from __future__ import annotations

from itertools import combinations
import json
import runpy
from pathlib import Path


m = runpy.run_path(str(Path(__file__).with_name("two_vertex_output_expansion_search.py")))
edge = m["edge"]
E0, V0, V, A, B = m["E0"], m["V0"], m["V"], m["A"], m["B"]
ALL_NEW = m["ALL_NEW"]
adjacency = m["adjacency"]
common_hitter = m["common_old_edge_hitting_all_bad_cycles"]
colour_pairs_safe = m["colour_pairs_safe"]
l4_2 = m["l4_2"]
all_states_safe = m["all_states_safe"]
reserve = m["reserve"]
matching_rank = m["matching_rank"]

REQUIRED = frozenset({edge("w", "x1"), edge("u", "x2")})
FORBIDDEN = frozenset({
    edge("w", "c"), edge("u", "c"),
    edge("w", "z"), edge("u", "z"),
    edge("w", "y1"), edge("u", "y2"),
})
OPTIONAL = tuple(sorted(ALL_NEW - REQUIRED - FORBIDDEN))
assert len(OPTIONAL) == 19

def main() -> None:
    tested = hittable = exact_pair_safe = l4_pass = 0
    witness = None
    # Sixteen new edges and one old deletion preserve 65 total edges.
    for chosen in combinations(OPTIONAL, 14):
        tested += 1
        Eplus = frozenset(set(E0) | set(REQUIRED) | set(chosen))
        candidates = common_hitter(adjacency(Eplus))
        if not candidates:
            continue
        hittable += 1
        for deleted in sorted(candidates):
            E = frozenset(set(Eplus) - {deleted})
            adj = adjacency(E)
            if not colour_pairs_safe(adj):
                continue
            exact_pair_safe += 1
            if not l4_2(adj):
                continue
            l4_pass += 1
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
            witness = {
                "deleted_old_edge": list(deleted),
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
        if witness is not None:
            break

    print(json.dumps({
        "schema": "amra.erdos809.output-expansion-round6.general-one-exchange.v1",
        "model": "required wx1,ux2; forbid cw,cu,wz,uz and induced-matching cross edges wy1,uy2; choose fourteen of nineteen remaining new edges and delete one admissible old edge",
        "search_space": 11628,
        "assignments_tested": tested,
        "assignments_with_one_old_edge_hitting_every_bad_C7": hittable,
        "exact_pair_safe_after_deletion": exact_pair_safe,
        "L4_2_pass": l4_pass,
        "first_witness": witness,
        "finite_scope": "Complete for the displayed natural-switch one-exchange model; the two cross edges are necessarily absent in any L4(2) rainbow realization because each would join endpoints of a repeated pair.",
        "public_problem_changed": False,
        "lean_used": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
