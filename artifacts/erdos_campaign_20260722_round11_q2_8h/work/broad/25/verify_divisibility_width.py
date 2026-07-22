#!/usr/bin/env python3
"""Finite exact regression for both round-11 Erdős #25 theorems.

The computation checks chain atomisation, cutoff-dependent re-partitioning,
the CRT inclusion-exclusion density, the compatibility-clique count and
degeneracy bound, and the uniform endpoint bound.  It is only a falsifier for
the paper proofs, not evidence for their asymptotic quantifiers.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from math import gcd, lcm
import json
import random


def comparable(a: int, b: int) -> bool:
    return a % b == 0 or b % a == 0


def minimum_chain_partition(moduli: tuple[int, ...]) -> list[list[int]]:
    """Exact branch-and-bound chain partition for the small regression box."""
    ordered = sorted(moduli)
    best: list[list[int]] = [[value] for value in ordered]

    def search(index: int, chains: list[list[int]]) -> None:
        nonlocal best
        if len(chains) >= len(best):
            return
        if index == len(ordered):
            best = [chain[:] for chain in chains]
            return
        value = ordered[index]
        for chain in chains:
            if value % chain[-1] == 0:
                chain.append(value)
                search(index + 1, chains)
                chain.pop()
        chains.append([value])
        search(index + 1, chains)
        chains.pop()

    search(0, [])
    return best


def width_bruteforce(moduli: tuple[int, ...]) -> int:
    answer = 0
    for size in range(1, len(moduli) + 1):
        if any(all(not comparable(a, b) for a, b in combinations(subset, 2))
               for subset in combinations(moduli, size)):
            answer = size
    return answer


def atomise(chain: list[int], residues: dict[int, int]) -> list[int]:
    kept: list[int] = []
    for modulus in chain:
        redundant = any(residues[modulus] % earlier
                        == residues[earlier] % earlier
                        for earlier in kept)
        if not redundant:
            kept.append(modulus)
    return kept


def crt_pair(r: int, modulus: int, a: int, n: int) -> tuple[int, int] | None:
    g = gcd(modulus, n)
    if (a - r) % g:
        return None
    left = modulus // g
    right = n // g
    step = ((a - r) // g * pow(left, -1, right)) % right
    new_modulus = modulus * right
    return (r + modulus * step) % new_modulus, new_modulus


def compatible_pair(a: int, b: int, residues: dict[int, int]) -> bool:
    return (residues[a] - residues[b]) % gcd(a, b) == 0


def graph_degeneracy(vertices: list[int], residues: dict[int, int]) -> int:
    adjacency = {
        vertex: {
            other for other in vertices
            if other != vertex and compatible_pair(vertex, other, residues)
        }
        for vertex in vertices
    }
    remaining = set(vertices)
    degeneracy = 0
    while remaining:
        vertex = min(remaining, key=lambda item: len(adjacency[item] & remaining))
        degeneracy = max(degeneracy, len(adjacency[vertex] & remaining))
        remaining.remove(vertex)
    return degeneracy


def ie_density(
    atoms: list[list[int]], residues: dict[int, int]
) -> tuple[Fraction, int, int]:
    density = Fraction(0)
    term_bound = 1
    compatible_terms = 0
    choices = []
    for chain in atoms:
        term_bound *= 1 + len(chain)
        choices.append([None, *chain])
    for selection in product(*choices):
        selected = [modulus for modulus in selection if modulus is not None]
        pairwise = all(compatible_pair(a, b, residues)
                       for a, b in combinations(selected, 2))
        congruence = (0, 1)
        parity = 0
        compatible = True
        for modulus in selection:
            if modulus is None:
                continue
            parity += 1
            merged = crt_pair(*congruence, residues[modulus], modulus)
            if merged is None:
                compatible = False
                break
            congruence = merged
        # This is the finite generalized-CRT/2-Helly assertion used in the
        # compatibility-clique proof.
        assert compatible == pairwise
        if compatible:
            compatible_terms += 1
            density += (-1 if parity % 2 else 1) * Fraction(1, congruence[1])
    return density, term_bound, compatible_terms


def direct_period_density(moduli: tuple[int, ...], residues: dict[int, int]) -> Fraction:
    period = lcm(*moduli) if moduli else 1
    survivors = sum(all(value % modulus != residues[modulus] % modulus
                        for modulus in moduli)
                    for value in range(1, period + 1))
    return Fraction(survivors, period)


def activated_count(cutoff: int, moduli: tuple[int, ...], residues: dict[int, int]) -> int:
    return sum(all(value < modulus
                   or value % modulus != residues[modulus] % modulus
                   for modulus in moduli)
               for value in range(1, cutoff + 1))


def main() -> None:
    rng = random.Random(20260722)
    cases = 0
    maximum_endpoint_ratio = Fraction(0)
    maximum_clique_endpoint_ratio = Fraction(0)
    for _ in range(400):
        size = rng.randint(1, 7)
        # Keeping moduli small makes a direct full-period check independent.
        moduli = tuple(sorted(rng.sample(range(2, 19), size)))
        residues = {modulus: rng.randrange(modulus) for modulus in moduli}
        partition = minimum_chain_partition(moduli)
        assert len(partition) == width_bruteforce(moduli)
        atoms = [atomise(chain, residues) for chain in partition]
        density, term_bound, clique_count = ie_density(atoms, residues)
        assert density == direct_period_density(moduli, residues)
        vertices = [modulus for chain in atoms for modulus in chain]
        degeneracy = graph_degeneracy(vertices, residues)
        assert clique_count <= 1 + len(vertices) * 2 ** degeneracy

        cutoff = rng.randint(max(moduli), 4 * max(moduli) + 30)
        count = activated_count(cutoff, moduli, residues)
        discrepancy = abs(Fraction(count) - cutoff * density)
        assert discrepancy <= 2 * term_bound
        assert discrepancy <= 2 * clique_count
        maximum_endpoint_ratio = max(
            maximum_endpoint_ratio, discrepancy / term_bound
        )
        maximum_clique_endpoint_ratio = max(
            maximum_clique_endpoint_ratio, discrepancy / clique_count
        )
        cases += 1

    print(json.dumps({
        "schema": "amra.erdos25.width-and-clique-entropy.v2",
        "status": "PASS",
        "random_seed": 20260722,
        "cases": cases,
        "max_modulus": 18,
        "checks": [
            "minimum chain count equals brute-force width",
            "chain CRT inclusion-exclusion equals direct period density",
            "pairwise compatibility is equivalent to joint CRT compatibility",
            "actual compatible term count obeys the degeneracy clique bound",
            "activated cutoff discrepancy is at most twice the IE term bound",
            "activated cutoff discrepancy is at most twice the compatible-clique count",
        ],
        "maximum_discrepancy_over_term_bound": [
            maximum_endpoint_ratio.numerator,
            maximum_endpoint_ratio.denominator,
        ],
        "maximum_discrepancy_over_clique_count": [
            maximum_clique_endpoint_ratio.numerator,
            maximum_clique_endpoint_ratio.denominator,
        ],
        "scope_warning": "Finite exact regression only; the theorem is proved in markdown.",
    }, indent=2))


if __name__ == "__main__":
    main()
