#!/usr/bin/env python3
"""Finite audit for the multiplicity-sensitive residue-chain certificate.

The general proof is algebraic.  This script only verifies, on supplied small
tuples, exact division P=(1-z^q)^m Q, the residue-chain decomposition, and
E(P) >= (2 ceil((m+1)/2) + 2 * 1[m>=3]) S_q(Q).
"""

from __future__ import annotations

import json
import math
from itertools import combinations_with_replacement


def multiply_binomial(coefficients: list[int], exponent: int) -> list[int]:
    out = [0] * (len(coefficients) + exponent)
    for index, value in enumerate(coefficients):
        out[index] += value
        out[index + exponent] -= value
    return out


def product(exponents: tuple[int, ...]) -> list[int]:
    coefficients = [1]
    for exponent in exponents:
        coefficients = multiply_binomial(coefficients, exponent)
    return coefficients


def divide_binomial(coefficients: list[int], exponent: int) -> list[int]:
    """Exact quotient by 1-z^exponent, verified by reconstruction."""
    degree = len(coefficients) - 1
    if degree < exponent:
        raise ValueError("divisor degree exceeds polynomial degree")
    quotient = [0] * (degree - exponent + 1)
    for index in range(len(quotient)):
        quotient[index] = coefficients[index]
        if index >= exponent:
            quotient[index] += quotient[index - exponent]
    assert multiply_binomial(quotient, exponent) == coefficients
    return quotient


def divisors(value: int):
    answer = set()
    for divisor in range(1, math.isqrt(value) + 1):
        if value % divisor == 0:
            answer.add(divisor)
            answer.add(value // divisor)
    return answer


def audit(exponents: tuple[int, ...]) -> dict[str, object]:
    coefficients = product(exponents)
    energy = sum(value * value for value in coefficients)
    rows = []
    for modulus in sorted(set().union(*(divisors(value) for value in exponents))):
        multiplicity = sum(value % modulus == 0 for value in exponents)
        quotient = coefficients
        for _ in range(multiplicity):
            quotient = divide_binomial(quotient, modulus)
        reconstructed = quotient
        for _ in range(multiplicity):
            reconstructed = multiply_binomial(reconstructed, modulus)
        active_residues = sorted({
            index % modulus for index, value in enumerate(quotient) if value
        })
        chain_energy = []
        chain_support = []
        for residue in active_residues:
            values = coefficients[residue::modulus]
            chain_energy.append(sum(value * value for value in values))
            chain_support.append(sum(value != 0 for value in values))
        support_certificate = (multiplicity + 1) * len(active_residues)
        per_chain_parity_bound = 2 * ((multiplicity + 2) // 2)
        per_chain_moment_bound = per_chain_parity_bound + (
            2 if multiplicity >= 3 else 0
        )
        certificate = per_chain_moment_bound * len(active_residues)
        rows.append({
            "q": modulus,
            "binomial_multiplicity": multiplicity,
            "division_exact": reconstructed == coefficients,
            "active_residue_count": len(active_residues),
            "each_active_chain_support_at_least_m_plus_1":
                all(value >= multiplicity + 1 for value in chain_support),
            "each_active_chain_energy_at_least_m_plus_1":
                all(value >= multiplicity + 1 for value in chain_energy),
            "each_active_chain_energy_even":
                all(value % 2 == 0 for value in chain_energy),
            "per_chain_parity_bound": per_chain_parity_bound,
            "per_chain_moment_bound": per_chain_moment_bound,
            "support_certificate": support_certificate,
            "certificate": certificate,
            "energy": energy,
            "pass": reconstructed == coefficients
                    and all(value >= multiplicity + 1 for value in chain_support)
                    and all(value >= multiplicity + 1 for value in chain_energy)
                    and all(value % 2 == 0 for value in chain_energy)
                    and energy >= certificate,
        })
    return {"exponents": exponents, "energy": energy, "rows": rows}


def main() -> None:
    examples = [
        (1, 2, 3, 4, 5, 7),
        (1, 2, 3, 5, 7, 8, 11, 13),
        (1, 2, 7, 10),
        (6, 10, 15, 21),
        (5, 1, 2, 4),
        (7, 1, 2, 3, 4),
    ]
    audits = [audit(example) for example in examples]
    systematic = [
        audit(example)
        for length in range(1, 6)
        for example in combinations_with_replacement(range(1, 9), length)
    ]
    systematic_rows = [row for item in systematic for row in item["rows"]]
    print(json.dumps({
        "status": "PASS" if all(
            row["pass"]
            for item in audits + systematic
            for row in item["rows"]
        ) else "FAIL",
        "scope": "finite identity audit only; not a proof of the general lemma",
        "systematic_scan": {
            "nondecreasing_tuples": len(systematic),
            "length_range": [1, 5],
            "exponent_range": [1, 8],
            "divisor_rows": len(systematic_rows),
            "even_multiplicity_rows": sum(
                row["binomial_multiplicity"] % 2 == 0
                for row in systematic_rows
            ),
            "strict_parity_improvements": sum(
                row["per_chain_parity_bound"]
                > row["binomial_multiplicity"] + 1
                for row in systematic_rows
            ),
            "strict_moment_improvements": sum(
                row["per_chain_moment_bound"]
                > row["per_chain_parity_bound"]
                for row in systematic_rows
            ),
            "failures": sum(not row["pass"] for row in systematic_rows),
        },
        "audits": audits,
    }, indent=2))


if __name__ == "__main__":
    main()
