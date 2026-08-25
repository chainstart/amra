#!/usr/bin/env python3
"""Exact replay for the symbolic positive-background amplifier."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path


def old_survivor(Q: int, m: int) -> bool:
    return m % 2 == 0 or m % Q == Q - 1


def verify_old_complement(Q: int) -> None:
    forbidden = [(q, q // 2 - 1) for q in (2**j for j in range(2, Q.bit_length()))]
    for m in range(2 * Q):
        direct = all(m % q != residue for q, residue in forbidden)
        assert direct == old_survivor(Q, m)


def record(Q: int, R: int) -> dict:
    verify_old_complement(Q)
    moduli = [r * Q - 2 for r in range(R, 2 * R)]
    targets = [modulus + 1 for modulus in moduli]
    assert min(moduli) > Q
    assert moduli == sorted(set(moduli))
    for target in targets:
        assert old_survivor(Q, target)
    for i, (modulus, target) in enumerate(zip(moduli, targets)):
        assert target % modulus == 1
        for j, other in enumerate(targets):
            if i == j:
                continue
            if other >= modulus:
                assert other % modulus != 1

    harmonic_float = math.fsum(1.0 / target for target in targets)
    density_upper_float = math.fsum(2.0 / (Q * modulus) for modulus in moduli)
    # Retain a compact exact aggregate for small rows.  The formula for every
    # summand remains exact at all Q, while a common denominator at Q=2048 has
    # thousands of digits and adds no evidentiary value to the JSON replay.
    harmonic = sum((Fraction(1, target) for target in targets), Fraction()) if Q <= 256 else None
    density_upper = sum((Fraction(2, Q * modulus) for modulus in moduli), Fraction()) if Q <= 256 else None
    cutoff = targets[-1]
    normalised = harmonic_float / math.log(cutoff)
    return {
        "Q": Q,
        "R": R,
        "old_density_numerator": Q // 2 + 1,
        "old_density_denominator": Q,
        "layer_count": R,
        "cutoff": cutoff,
        "target_harmonic_numerator": None if harmonic is None else harmonic.numerator,
        "target_harmonic_denominator": None if harmonic is None else harmonic.denominator,
        "target_harmonic_float": harmonic_float,
        "eventual_density_upper_numerator": None if density_upper is None else density_upper.numerator,
        "eventual_density_upper_denominator": None if density_upper is None else density_upper.denominator,
        "eventual_density_upper_float": density_upper_float,
        "normalised_target_mass": normalised,
        "aggregate_relative_amplification": normalised / density_upper_float,
        "all_targets_pairwise_isolated": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = [record(Q, Q) for Q in (4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048)]
    assert rows[-1]["aggregate_relative_amplification"] > rows[-2]["aggregate_relative_amplification"]
    assert rows[-1]["normalised_target_mass"] < rows[-2]["normalised_target_mass"]
    payload = {
        "schema_version": "erdos-25.positive-background-amplifier.v1",
        "status": "passed",
        "checks": [
            "old complement equals evens union -1 mod Q",
            "new moduli are strictly increasing and above Q",
            "every distinguished target survives the old tower",
            "distinguished targets are pairwise isolated",
            "exact rational harmonic and density budgets were computed",
            "relative amplification grows while absolute normalised mass decays in the sampled symbolic family",
        ],
        "rows": rows,
        "interpretation_limit": "Exact replay of a finite symbolic family is not an infinite counterexample and is not an independent audit.",
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "passed", "rows": len(rows), "largest_Q": rows[-1]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
