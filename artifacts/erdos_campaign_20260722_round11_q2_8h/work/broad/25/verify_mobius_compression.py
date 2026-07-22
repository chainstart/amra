#!/usr/bin/env python3
"""Exact audit of the squarefree-block Möbius compression example."""

from __future__ import annotations

from itertools import combinations
from fractions import Fraction
import json
from math import gcd, lcm, prod
import random


def audit(primes: list[int]) -> dict[str, int | bool]:
    L = prod(primes)
    moduli = [L // p for p in primes]
    assert all(a % b and b % a for a, b in combinations(moduli, 2))
    coefficient = 0
    raw = 0
    for size in range(2, len(moduli) + 1):
        for subset in combinations(moduli, size):
            joint = 1
            for modulus in subset:
                joint = joint * modulus // gcd(joint, modulus)
            assert joint == L
            coefficient += (-1) ** size
            raw += 1
    assert coefficient == len(primes) - 1
    assert raw == 2 ** len(primes) - len(primes) - 1
    return {
        "k": len(primes),
        "L": L,
        "compressed_absolute_coefficient": abs(coefficient),
        "uncompressed_cliques_of_size_at_least_two": raw,
        "identity_pass": True,
    }


def merge_crt(state: tuple[int, int], congruence: tuple[int, int]) -> tuple[int, int] | None:
    residue, modulus = state
    target, new_modulus = congruence
    common = gcd(modulus, new_modulus)
    if (target - residue) % common:
        return None
    left = modulus // common
    right = new_modulus // common
    step = ((target - residue) // common * pow(left, -1, right)) % right
    joint = modulus * right
    return ((residue + modulus * step) % joint, joint)


def randomized_grouping_audit() -> dict[str, int | bool]:
    rng = random.Random(20260722)
    systems = 80
    tested_points = 0
    for _ in range(systems):
        moduli = sorted(rng.sample(range(2, 15), rng.randint(3, 8)))
        classes = [(rng.randrange(n), n) for n in moduli]
        X = 40
        triples: dict[tuple[int, int, int], int] = {}
        complete: dict[tuple[int, int], int] = {}
        deleted: dict[tuple[int, int], int] = {}
        for size in range(1, len(classes) + 1):
            for indices in combinations(range(len(classes)), size):
                state = (0, 1)
                for index in indices:
                    merged = merge_crt(state, classes[index])
                    if merged is None:
                        state = None
                        break
                    state = merged
                if state is None:
                    continue
                residue0, L = state
                r = residue0 or L
                M = max(classes[index][1] for index in indices)
                epsilon = int(r < M)
                sign = (-1) ** size
                triples[L, r, epsilon] = triples.get((L, r, epsilon), 0) + sign
                complete[L, r] = complete.get((L, r), 0) + sign
                if epsilon:
                    deleted[L, r] = deleted.get((L, r), 0) + sign

        direct_harmonic = Fraction(0)
        grouped_harmonic = sum((Fraction(1, m) for m in range(1, X + 1)), Fraction(0))
        for m in range(1, X + 1):
            direct = int(all(m < n or m % n != a for a, n in classes))
            grouped = 1
            for (L, r, epsilon), coefficient in triples.items():
                grouped += coefficient * int(m >= r + epsilon * L and m % L == r % L)
            assert direct == grouped
            if direct:
                direct_harmonic += Fraction(1, m)
            tested_points += 1
        for (L, r), coefficient in complete.items():
            grouped_harmonic += coefficient * sum(
                (Fraction(1, m) for m in range(r, X + 1, L)), Fraction(0)
            )
            grouped_harmonic -= Fraction(deleted.get((L, r), 0), r)
        assert direct_harmonic == grouped_harmonic

        period = lcm(*moduli)
        direct_density = Fraction(sum(
            all(m % n != a for a, n in classes) for m in range(1, period + 1)
        ), period)
        grouped_density = Fraction(1)
        for (L, _r), coefficient in complete.items():
            grouped_density += Fraction(coefficient, L)
        assert direct_density == grouped_density

    return {
        "random_systems": systems,
        "point_identities_checked": tested_points,
        "grouped_harmonic_identity_pass": True,
        "grouped_periodic_density_identity_pass": True,
    }


def main() -> None:
    rows = [audit(primes) for primes in (
        [2, 3, 5],
        [2, 3, 5, 7],
        [2, 3, 5, 7, 11],
        [2, 3, 5, 7, 11, 13, 17, 19],
    )]
    print(json.dumps({
        "schema": "amra.erdos25.mobius-compression.v1",
        "status": "PASS",
        "rows": rows,
        "randomized_grouping_audit": randomized_grouping_audit(),
        "scope_warning": "Finite audit of the realised separation example; the theorem has a separate algebraic proof.",
    }, indent=2))


if __name__ == "__main__":
    main()
