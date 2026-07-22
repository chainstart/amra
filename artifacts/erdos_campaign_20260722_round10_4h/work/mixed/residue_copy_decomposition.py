#!/usr/bin/env python3
"""Exact finite audit for the #256 dissociated-residue copy theorem.

The general theorem is proved in REPORT.md.  This program independently
checks its polynomial identity/energy consequence on a finite multiset box.
Only Python integer arithmetic is used.
"""

from __future__ import annotations

import argparse
import itertools
import json


def multiply(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return out


def product(exponents: tuple[int, ...] | list[int]) -> list[int]:
    out = [1]
    for exponent in exponents:
        factor = [0] * (exponent + 1)
        factor[0] = 1
        factor[exponent] = -1
        out = multiply(out, factor)
    return out


def energy(coefficients: list[int]) -> int:
    return sum(value * value for value in coefficients)


def residues_are_dissociated(exponents: list[int], modulus: int) -> bool:
    seen: set[int] = set()
    for mask in range(1 << len(exponents)):
        residue = sum(
            exponents[index]
            for index in range(len(exponents))
            if mask >> index & 1
        ) % modulus
        if residue in seen:
            return False
        seen.add(residue)
    return True


def audit(max_length: int, max_exponent: int) -> dict[str, object]:
    checked_tuples = 0
    checked_directions = 0
    nontrivial_split_directions = 0
    failures: list[dict[str, object]] = []
    equality_obstruction_checks = 0
    for length in range(1, max_length + 1):
        for values in itertools.combinations_with_replacement(
            range(1, max_exponent + 1), length
        ):
            checked_tuples += 1
            full_energy = energy(product(values))
            for modulus in range(2, max_exponent + 1):
                divisible = [value // modulus for value in values if value % modulus == 0]
                outside = [value for value in values if value % modulus]
                if divisible and outside:
                    nontrivial_split_directions += 1
                    if full_energy < 4 * len(divisible):
                        failures.append({
                            "type": "two-residue lower bound failure",
                            "values": values,
                            "modulus": modulus,
                            "m": len(divisible),
                            "energy": full_energy,
                        })
                if not outside or not residues_are_dissociated(outside, modulus):
                    continue
                checked_directions += 1
                predicted = (1 << len(outside)) * energy(product(divisible))
                if full_energy != predicted:
                    failures.append({
                        "values": values,
                        "modulus": modulus,
                        "divided_core": divisible,
                        "outside": outside,
                        "actual_energy": full_energy,
                        "predicted_energy": predicted,
                    })
                if (
                    length >= 3
                    and divisible
                    and full_energy == 2 * length
                ):
                    equality_obstruction_checks += 1
                    failures.append({
                        "type": "forbidden Tang-equality split",
                        "values": values,
                        "modulus": modulus,
                    })

    # Sharpness: without dissociation, different subset copies may cancel.
    sharp = (1, 2, 3)
    sharp_energy = energy(product(sharp))
    sharp_copy_prediction = 4 * energy(product([1]))
    assert sharp_energy == 6 < sharp_copy_prediction == 8

    # Published small equality witnesses used as adversarial controls.
    controls = []
    for values in ((1, 2, 3, 4, 5, 7), (1, 2, 3, 5, 7, 8, 11, 13)):
        actual = energy(product(values))
        assert actual == 2 * len(values)
        bad_directions = []
        for modulus in range(2, max(values) + 1):
            inside = [a for a in values if a % modulus == 0]
            outside = [a for a in values if a % modulus]
            if inside and outside and residues_are_dissociated(outside, modulus):
                bad_directions.append(modulus)
        assert not bad_directions
        controls.append({"values": values, "energy": actual, "bad_directions": bad_directions})

    return {
        "status": "PASS" if not failures else "FAIL",
        "scope": "finite regression only; the all-parameter proof is in REPORT.md",
        "max_length": max_length,
        "max_exponent": max_exponent,
        "tuples_checked": checked_tuples,
        "nontrivial_modulus_splits_checked": nontrivial_split_directions,
        "dissociated_modulus_directions_checked": checked_directions,
        "forbidden_equality_splits_found": equality_obstruction_checks,
        "failures": failures,
        "non_dissociated_sharpness_control": {
            "values": sharp,
            "modulus": 2,
            "actual_energy": sharp_energy,
            "false_copy_prediction": sharp_copy_prediction,
        },
        "Tang_equality_controls": controls,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=6)
    parser.add_argument("--max-exponent", type=int, default=10)
    args = parser.parse_args()
    print(json.dumps(audit(args.max_length, args.max_exponent), indent=2))


if __name__ == "__main__":
    main()
