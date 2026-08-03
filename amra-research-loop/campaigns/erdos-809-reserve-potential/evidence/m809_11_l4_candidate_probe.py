#!/usr/bin/env python3
"""Exact n=14 L4(2) candidate extending the three-colour tight circuit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import m809_11_hard_graph_probe as core


core.V = tuple(
    ["v"]
    + [f"x{i}" for i in range(1, 5)]
    + [f"y{i}" for i in range(1, 5)]
    + ["r1", "r2", "b", "c", "z"]
)
core.X = tuple(f"x{i}" for i in range(1, 5))
core.Y = tuple(f"y{i}" for i in range(1, 5))
core.A = frozenset(core.V[:11])
core.B = frozenset(("b", "c", "z"))

removed_A_edges = {core.edge("x1", "x2"), core.edge("y1", "y2")}
edges = {
    core.edge(left, right)
    for left, right in __import__("itertools").combinations(core.A, 2)
    if not (left in core.X and right in core.Y)
    and not (left in core.Y and right in core.X)
    and core.edge(left, right) not in removed_A_edges
}
edges.update(core.edge("b", x) for x in core.X)
edges.update(core.edge("c", y) for y in core.Y)
edges.add(core.edge("b", "z"))
edges.update(core.edge("z", x) for x in core.X)
core.E = frozenset(edges)


def colour(edge0: tuple[str, str]) -> str:
    for index in range(1, 4):
        if edge0 in (core.edge("b", f"x{index}"), core.edge("c", f"y{index}")):
            return f"gamma{index}"
    return "unique:" + "-".join(edge0)


core.colour = colour


def main() -> None:
    degrees = {vertex: len(core.neighbours(vertex)) for vertex in core.V}
    cycles = core.canonical_cycles(7)
    nonrainbow = []
    for cycle in cycles:
        colours = [core.colour(core.edge(cycle[i], cycle[(i + 1) % 7])) for i in range(7)]
        if len(set(colours)) < 7:
            nonrainbow.append({"cycle": cycle, "colours": colours})
            if len(nonrainbow) >= 20:
                break
    reserve = core.b_reserve(core.edge("b", "c"))
    owned = [core.edge(f"x{i}", f"y{i}") for i in range(1, 4)]
    n = len(core.V)
    failures = core.l4_2_failures()
    payload = {
        "classification": "exact_full_hard_local_realisation_probe",
        "n": n,
        "edge_count": len(core.E),
        "required_edge_count": n * n // 4 + 1,
        "minimum_degree": min(degrees.values()),
        "maximum_degree": max(degrees.values()),
        "degrees": degrees,
        "A_equals_closed_neighbourhood_of_v": core.A == core.neighbours("v") | {"v"},
        "B_opposite_pair_bc": (
            not (core.neighbours("b") & core.neighbours("c"))
            and all(not core.adjacent(left, right) for left in core.neighbours("b") for right in core.neighbours("c"))
        ),
        "B_reserve_bc": sorted(reserve),
        "three_colour_full_reserve_tight_circuit": len(reserve) == 2,
        "owned_A_atoms": owned,
        "owned_A_atoms_distinct_and_missing": len(set(owned)) == 3 and all(item not in core.E for item in owned),
        "C7_count": len(cycles),
        "nonrainbow_C7_capped_at_20": nonrainbow,
        "rainbow_C7": not nonrainbow,
        "L4_2_failures_capped_at_20": failures,
        "L4_2": not failures,
        "public_problem_counterexample_claimed": False,
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    output = Path(__file__).with_suffix(".json")
    output.write_bytes(encoded)
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("output_sha256", hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
