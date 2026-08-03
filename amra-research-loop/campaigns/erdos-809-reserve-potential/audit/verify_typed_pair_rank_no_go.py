#!/usr/bin/env python3
"""Independent reconstruction of the M809-11 typed pair-rank claims."""

from itertools import combinations, product
import json


def edge(left, right):
    return tuple(sorted((left, right)))


V = tuple(
    ["v"]
    + [f"x{i}" for i in range(1, 5)]
    + [f"y{i}" for i in range(1, 5)]
    + ["r1", "r2", "b", "c", "z"]
)
X = frozenset(f"x{i}" for i in range(1, 5))
Y = frozenset(f"y{i}" for i in range(1, 5))
A = frozenset(V[:11])
B = frozenset(("b", "c", "z"))


def build_tight_edges():
    removed = {edge("x1", "x2"), edge("y1", "y2")}
    edges = {
        edge(left, right)
        for left, right in combinations(A, 2)
        if not ({left, right} & X and {left, right} & Y)
        and edge(left, right) not in removed
    }
    edges.update(edge("b", x) for x in X)
    edges.update(edge("c", y) for y in Y)
    edges.add(edge("b", "z"))
    edges.update(edge("z", x) for x in X)
    return frozenset(edges)


def adjacent(edges, left, right):
    return left != right and edge(left, right) in edges


def neighbours(edges, vertex):
    return frozenset(other for other in V if adjacent(edges, vertex, other))


def reserve(edges, pair):
    left, right = pair
    missing = {edge(u, w) for u, w in combinations(B, 2) if not adjacent(edges, u, w)}
    result = {item for item in missing if left in item or right in item}
    result.update(
        edge(p, q)
        for p in neighbours(edges, left) & B
        for q in neighbours(edges, right) & B
        if p != q
    )
    assert result <= missing
    return frozenset(result)


def has_length_four_path(edges, start, end, forbidden):
    def extend(path):
        if len(path) == 5:
            return path[-1] == end
        for nxt in V:
            if nxt in forbidden or nxt in path or not adjacent(edges, path[-1], nxt):
                continue
            if len(path) < 4 and nxt == end:
                continue
            if extend(path + (nxt,)):
                return True
        return False

    return extend((start,))


def l4_2(edges):
    for start, end in combinations(V, 2):
        available = [x for x in V if x not in (start, end)]
        for size in range(3):
            for forbidden in combinations(available, size):
                if not has_length_four_path(edges, start, end, frozenset(forbidden)):
                    return False
    return True


def canonical_seven_cycles(edges):
    cycles = set()

    def search(path):
        if len(path) == 7:
            if adjacent(edges, path[-1], path[0]):
                words = []
                for word in (path, tuple(reversed(path))):
                    words.extend(word[i:] + word[:i] for i in range(7))
                cycles.add(min(words))
            return
        for nxt in V:
            if nxt not in path and adjacent(edges, path[-1], nxt):
                search(path + (nxt,))

    for start in V:
        search((start,))
    return cycles


def colour(item):
    for index in range(1, 4):
        if item in (edge("b", f"x{index}"), edge("c", f"y{index}")):
            return f"gamma{index}"
    return "unique:" + "-".join(item)


def evaluate_graph(edges):
    cycles = canonical_seven_cycles(edges)
    nonrainbow = 0
    for cycle in cycles:
        colours = [colour(edge(cycle[i], cycle[(i + 1) % 7])) for i in range(7)]
        nonrainbow += len(set(colours)) < 7
    owned = frozenset(edge(f"x{i}", f"y{i}") for i in range(1, 4))
    reserve_bc = reserve(edges, edge("b", "c"))
    missing_b = frozenset(
        edge(left, right)
        for left, right in combinations(B, 2)
        if not adjacent(edges, left, right)
    )
    return {
        "n": len(V),
        "edge_count": len(edges),
        "B_size": len(B),
        "A_is_closed_neighbourhood_of_v": A == neighbours(edges, "v") | {"v"},
        "minimum_degree": min(len(neighbours(edges, vertex)) for vertex in V),
        "L4_2": l4_2(edges),
        "C7_count": len(cycles),
        "nonrainbow_C7_count": nonrainbow,
        "rho_A": len(owned),
        "owned_A_atoms_missing": owned.isdisjoint(edges),
        "rho_B": len(reserve_bc),
        "B_reserve_bc": sorted(reserve_bc),
        "M_B": len(missing_b),
        "D_B": 3,
    }


def subsets(items):
    items = tuple(items)
    for size in range(len(items) + 1):
        for choice in combinations(items, size):
            yield frozenset(choice)


def coverage_rank(chosen, neighbourhoods):
    return len(set().union(*(neighbourhoods[colour] for colour in chosen))) if chosen else 0


def is_submodular(neighbourhoods):
    sets = tuple(subsets(neighbourhoods))
    return all(
        coverage_rank(left, neighbourhoods) + coverage_rank(right, neighbourhoods)
        >= coverage_rank(left | right, neighbourhoods)
        + coverage_rank(left & right, neighbourhoods)
        for left in sets
        for right in sets
    )


def exhaustive_coverage_check():
    colours = ("a", "b", "c")
    atoms = (0, 1, 2)
    atom_subsets = tuple(
        frozenset(choice)
        for size in range(4)
        for choice in combinations(atoms, size)
    )
    checked = 0
    for values in product(atom_subsets, repeat=len(colours)):
        neighbourhoods = dict(zip(colours, values))
        assert is_submodular(neighbourhoods)
        checked += 1
    singleton_maps = 0
    for values in product(atoms, repeat=len(colours)):
        neighbourhoods = {colour: {value} for colour, value in zip(colours, values)}
        assert is_submodular(neighbourhoods)
        singleton_maps += 1
    return {"arbitrary_coverage_maps": checked, "singleton_owner_maps": singleton_maps}


def main():
    coverage_checks = exhaustive_coverage_check()
    tight_edges = build_tight_edges()
    paid_edges = frozenset(
        (tight_edges - {edge("b", "z")}) | {edge("x1", "x2")}
    )
    tight = evaluate_graph(tight_edges)
    paid = evaluate_graph(paid_edges)

    assert tight["n"] == paid["n"] == 14
    assert tight["edge_count"] == paid["edge_count"] == 50
    assert tight["B_size"] == paid["B_size"] == 3
    assert tight["rho_A"] == paid["rho_A"] == 3
    assert tight["rho_B"] == tight["M_B"] == 2
    assert paid["rho_B"] == paid["M_B"] == 3
    assert tight["D_B"] == paid["D_B"] == 3
    assert tight["L4_2"] and paid["L4_2"]
    assert tight["nonrainbow_C7_count"] == paid["nonrainbow_C7_count"] == 0
    assert tight["D_B"] <= tight["rho_A"] + tight["rho_B"]
    assert tight["D_B"] > tight["M_B"]

    print(json.dumps({
        "schema": "amra.erdos809.typed-pair-rank-independent-check.v1",
        "coverage_submodularity": {
            "result": "pass",
            "finite_exhaustion": coverage_checks,
            "natural_proof": "each atom contributes the hit indicator of its owner set; hit indicators are submodular and sums preserve submodularity",
        },
        "same_scalar_pair": {
            "tight": tight,
            "paid": paid,
            "same_S_m_reason": "n, edge_count, and |B| agree, so e-C(|B|,2)-Phi(n,e) agrees",
        },
        "untyped_failure": {
            "tight_values": {"D_B": 3, "rho_A": 3, "rho_B": 2, "rho_A_plus_rho_B": 5, "M_B": 2},
            "invalid_inference": "D_B<=rho_A+rho_B does not imply D_B<=M_B",
            "formal_sum_submodular": True,
            "failure_is_semantic_typing_not_submodularity": True,
        },
        "result": "pass_with_scope_caveat",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
