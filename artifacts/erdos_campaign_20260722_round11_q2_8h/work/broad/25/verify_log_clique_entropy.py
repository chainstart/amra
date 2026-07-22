#!/usr/bin/env python3
"""Exact finite regression for LOG_AVERAGED_CLIQUE_ENTROPY.md.

This checks global redundancy removal, generalized-CRT clique counting, the
pointwise endpoint bound, and the discrete Abel identity.  It is a falsifier
for the algebra only; it cannot certify an asymptotic hypothesis.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import gcd
import json
import random


def compatible(a: int, b: int, residues: dict[int, int]) -> bool:
    return (residues[a] - residues[b]) % gcd(a, b) == 0


def effective(moduli: tuple[int, ...], residues: dict[int, int]) -> tuple[int, ...]:
    kept = []
    for modulus in moduli:
        # The class modulo `modulus` is contained in an earlier class exactly
        # in this divisibility-and-residue situation.
        if any(modulus % earlier == 0 and compatible(modulus, earlier, residues)
               for earlier in kept):
            continue
        kept.append(modulus)
    return tuple(kept)


def clique_count(vertices: tuple[int, ...], residues: dict[int, int]) -> int:
    answer = 0
    for size in range(len(vertices) + 1):
        answer += sum(
            all(compatible(a, b, residues) for a, b in combinations(subset, 2))
            for subset in combinations(vertices, size)
        )
    return answer


def full_density(moduli: tuple[int, ...], residues: dict[int, int]) -> Fraction:
    # Exact CRT inclusion-exclusion avoids enumerating a potentially huge lcm
    # period.  With at most seven classes this is also an independent check of
    # the clique interpretation.
    answer = Fraction(0)
    for size in range(len(moduli) + 1):
        for subset in combinations(moduli, size):
            residue, period = 0, 1
            possible = True
            for modulus in subset:
                common = gcd(period, modulus)
                if (residues[modulus] - residue) % common:
                    possible = False
                    break
                left, right = period // common, modulus // common
                step = ((residues[modulus] - residue) // common
                        * pow(left, -1, right)) % right
                residue = (residue + period * step) % (period * right)
                period *= right
            if possible:
                answer += (-1 if size % 2 else 1) * Fraction(1, period)
    return answer


def is_active_survivor(value: int, moduli: tuple[int, ...], residues: dict[int, int]) -> bool:
    return all(value < modulus or value % modulus != residues[modulus]
               for modulus in moduli)


def main() -> None:
    rng = random.Random(25072026)
    cases = 100
    cutoffs = 0
    maximum_endpoint_ratio = Fraction(0)
    for _ in range(cases):
        size = rng.randint(1, 7)
        moduli = tuple(sorted(rng.sample(range(2, 19), size)))
        residues = {modulus: rng.randrange(modulus) for modulus in moduli}
        maximum = 4 * max(moduli) + 12
        prefix_count = 0
        harmonic_sum = Fraction(0)
        delta: dict[int, Fraction] = {}
        eta: dict[int, Fraction] = {}
        count: dict[int, int] = {}

        for x in range(1, maximum + 1):
            if is_active_survivor(x, moduli, residues):
                prefix_count += 1
                harmonic_sum += Fraction(1, x)
            count[x] = prefix_count
            active_moduli = tuple(modulus for modulus in moduli if modulus <= x)
            reduced = effective(active_moduli, residues)
            # Removing a contained forbidden class changes neither survivor.
            assert full_density(reduced, residues) == full_density(active_moduli, residues)
            delta[x] = full_density(reduced, residues)
            kappa = clique_count(reduced, residues)
            discrepancy = abs(Fraction(prefix_count, x) - delta[x])
            eta[x] = min(Fraction(1), Fraction(2 * kappa, x))
            assert discrepancy <= eta[x]
            if kappa:
                maximum_endpoint_ratio = max(
                    maximum_endpoint_ratio,
                    abs(Fraction(prefix_count) - x * delta[x]) / kappa,
                )
            cutoffs += 1

        # Exact Abel summation, followed by the theorem's accumulated error.
        abel_actual = Fraction(count[maximum], maximum) + sum(
            Fraction(count[x], x * (x + 1)) for x in range(1, maximum)
        )
        assert abel_actual == harmonic_sum
        delta_main = Fraction(count[maximum], maximum) + sum(
            delta[x] / (x + 1) for x in range(1, maximum)
        )
        error_budget = sum(eta[x] / (x + 1) for x in range(1, maximum))
        assert abs(harmonic_sum - delta_main) <= error_budget

    print(json.dumps({
        "schema": "amra.erdos25.log-clique-entropy.v1",
        "status": "PASS",
        "random_seed": 25072026,
        "systems": cases,
        "cutoffs": cutoffs,
        "checks": [
            "global contained-class removal preserves full periodic density",
            "compatible subsets are counted as graph cliques",
            "pointwise activated-count error obeys min(1,2*kappa/x)",
            "discrete Abel identity is exact",
            "summed Abel error is bounded by the eta budget",
        ],
        "maximum_count_discrepancy_over_kappa": [
            maximum_endpoint_ratio.numerator,
            maximum_endpoint_ratio.denominator,
        ],
        "scope_warning": "Finite exact regression only; asymptotics are proved in markdown.",
    }, indent=2))


if __name__ == "__main__":
    main()
