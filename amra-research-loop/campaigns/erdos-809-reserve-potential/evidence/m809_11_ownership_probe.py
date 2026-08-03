#!/usr/bin/env python3
"""Small exact ownership probe for the sole M809-11 survivor.

This is an abstract typed-incidence falsifier.  It does not assert that the
bad ownership pattern is realized by a hard BCM graph.
"""

from __future__ import annotations

import hashlib
import json
from itertools import combinations
from pathlib import Path


def neighbourhood(colours: frozenset[str], incidence: dict[str, frozenset[str]]) -> frozenset[str]:
    return frozenset().union(*(incidence[colour] for colour in colours)) if colours else frozenset()


def all_subsets(items: tuple[str, ...]):
    for size in range(len(items) + 1):
        for subset in combinations(items, size):
            yield frozenset(subset)


def hall(colours: tuple[str, ...], incidence: dict[str, frozenset[str]]) -> bool:
    return all(len(neighbourhood(subset, incidence)) >= len(subset) for subset in all_subsets(colours))


def maximum_matching_size(colours: tuple[str, ...], incidence: dict[str, frozenset[str]]) -> int:
    best = 0

    def search(index: int, used: frozenset[str], matched: int) -> None:
        nonlocal best
        if index == len(colours):
            best = max(best, matched)
            return
        search(index + 1, used, matched)
        for token in incidence[colours[index]] - used:
            search(index + 1, used | {token}, matched + 1)

    search(0, frozenset(), 0)
    return best


def coverage_rank(subset: frozenset[str], owners: dict[str, frozenset[str]]) -> int:
    return sum(bool(owner_set & subset) for owner_set in owners.values())


def main() -> None:
    colours = ("c1", "c2", "c3")
    base = {
        "c1": frozenset({"q1"}),
        "c2": frozenset({"q1", "q2"}),
        "c3": frozenset({"q2"}),
    }
    full = frozenset(colours)
    assert len(neighbourhood(full, base)) == len(full) - 1
    assert all(
        len(neighbourhood(subset, base)) >= len(subset)
        for subset in all_subsets(colours)
        if subset != full
    )

    good = {**base, "c2": base["c2"] | {"a1"}}
    bad = dict(base)
    assert hall(colours, good)
    assert not hall(colours, bad)

    owners_good = {
        "q1": frozenset({"c1", "c2"}),
        "q2": frozenset({"c2", "c3"}),
        "a1": frozenset({"c2"}),
    }
    owners_bad = {
        "q1": frozenset({"c1", "c2"}),
        "q2": frozenset({"c2", "c3"}),
        "a1": frozenset(),
    }
    subsets = tuple(all_subsets(colours))
    for owners in (owners_good, owners_bad):
        for left in subsets:
            for right in subsets:
                assert (
                    coverage_rank(left, owners) + coverage_rank(right, owners)
                    >= coverage_rank(left | right, owners) + coverage_rank(left & right, owners)
                )

    scalar_ledger = {
        "circuit_size": 3,
        "B_union_size": 2,
        "Hall_deficiency": 1,
        "colour_B_degrees": [1, 2, 1],
        "token_S_degrees": [2, 2],
        "branch": "B-opposite",
        "mu_algebraic_occurrences": 2,
        "mu_distinct_B_atoms": 1,
        "E_A_incidence_deficit": 1,
        "rectangle_side_sizes": [1, 1],
        "rectangle_product_atoms": 1,
        "S_m": 0,
    }
    payload = {
        "classification": "sharp_abstract_indistinguishability_no_go",
        "same_existing_scalar_ledger": scalar_ledger,
        "same_tight_B_circuit": {colour: sorted(tokens) for colour, tokens in base.items()},
        "chargeable_instance": {
            "new_A_atom": "a1",
            "owner_neighbourhood_in_S": ["c2"],
            "maximum_matching_size": maximum_matching_size(colours, good),
            "Hall": hall(colours, good),
            "full_set_pair_capacity": coverage_rank(full, owners_good),
        },
        "unchargeable_instance": {
            "new_A_atom": "a1",
            "owner_neighbourhood_in_S": [],
            "maximum_matching_size": maximum_matching_size(colours, bad),
            "Hall": hall(colours, bad),
            "full_set_pair_capacity": coverage_rank(full, owners_bad),
        },
        "distinguishing_datum": "owner neighbourhood of each actual A/B/slack resource atom inside the circuit",
        "coverage_rank_submodular_on_both_instances": True,
        "graph_realizability_claimed": False,
        "public_problem_changed": False,
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    output = Path(__file__).with_suffix(".json")
    output.write_bytes(encoded)
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("output_sha256", hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
