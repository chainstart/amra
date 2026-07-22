#!/usr/bin/env python3
"""Finite audit for the #963 reachable-wrap clique packing lemma."""

from __future__ import annotations

import argparse
import itertools
import json


def subset_sums(gamma: tuple[int, ...], modulus: int) -> set[int]:
    return {
        sum(gamma[index] for index in range(len(gamma)) if mask >> index & 1)
        % modulus
        for mask in range(1 << len(gamma))
    }


def max_clique_size(modulus: int, allowed_differences: set[int]) -> int:
    """Bron--Kerbosch maximum clique in the Cayley graph on Z/modulus."""
    adjacency = []
    for x in range(modulus):
        bits = 0
        for y in range(modulus):
            if x != y and (x - y) % modulus in allowed_differences:
                bits |= 1 << y
        adjacency.append(bits)
    best = 0

    def visit(size: int, candidates: int) -> None:
        nonlocal best
        if size + candidates.bit_count() <= best:
            return
        while candidates:
            vertex_bit = candidates & -candidates
            vertex = vertex_bit.bit_length() - 1
            candidates ^= vertex_bit
            visit(size + 1, candidates & adjacency[vertex])
        if size > best:
            best = size

    visit(0, (1 << modulus) - 1)
    return best


def audit(max_modulus: int) -> dict[str, object]:
    checked = 0
    failures = []
    tight = []
    for modulus in range(3, max_modulus + 1, 2):
        max_rank = (modulus.bit_length() - 1)
        for rank in range(1, max_rank + 1):
            for gamma in itertools.combinations(range(1, modulus), rank):
                sums = subset_sums(gamma, modulus)
                if len(sums) != 1 << rank:
                    continue
                differences = {(x - y) % modulus for x in sums for y in sums}
                allowed = set(range(1, modulus)) - differences
                clique = max_clique_size(modulus, allowed)
                checked += 1
                product = len(sums) * clique
                if product > modulus:
                    failures.append({
                        "modulus": modulus,
                        "gamma": gamma,
                        "subset_sum_size": len(sums),
                        "reachable_difference_clique": clique,
                        "product": product,
                    })
                if clique > 1 and product == modulus:
                    tight.append({"modulus": modulus, "gamma": gamma, "clique": clique})
    large_sparse_clique_controls = []
    for modulus in (11, 17, 101):
        middle_third = {
            residue for residue in range(1, modulus)
            if 3 * residue > modulus and 3 * residue < 2 * modulus
        }
        clique = max_clique_size(modulus, middle_third)
        assert clique == 2
        rank = 0
        while 3 * (1 << (rank + 1)) <= modulus:
            rank += 1
        gamma = tuple(1 << index for index in range(rank))
        sums = subset_sums(gamma, modulus)
        assert len(sums) == 1 << rank
        assert not ({(x - y) % modulus for x in sums for y in sums} & middle_third)
        large_sparse_clique_controls.append({
            "modulus": modulus,
            "forbidden_set_size": len(middle_third),
            "clique_number": clique,
            "binary_decoder_rank": rank,
            "binary_decoder_avoids_forbidden_set": True,
        })
    return {
        "status": "PASS" if not failures else "FAIL",
        "scope": "finite cyclic audit; the finite-abelian-group proof is in REPORT.md",
        "max_odd_modulus": max_modulus,
        "dissociated_decoders_checked": checked,
        "failures": failures,
        "nontrivial_tight_examples": tight[:20],
        "tight_example_count": len(tight),
        "middle_third_controls": large_sparse_clique_controls,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-modulus", type=int, default=25)
    args = parser.parse_args()
    print(json.dumps(audit(args.max_modulus), indent=2))


if __name__ == "__main__":
    main()
