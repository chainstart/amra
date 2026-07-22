#!/usr/bin/env python3
"""Exact finite audit for the strengthened residue root-energy lemma in #256.

The general argument in REPORT.md proves that a nonzero integer polynomial
with a root of multiplicity m at 1 has coefficient-square energy at least
2m.  Applied independently to the active residue chains of

    P(z) = (1-z^q)^m Q(z)

this gives E(P) >= 2m S_q(Q).  This program is only a finite regression test.
"""

from __future__ import annotations

import argparse
import json
import math
from itertools import combinations_with_replacement


def multiply_binomial(coefficients: list[int], exponent: int) -> list[int]:
    answer = [0] * (len(coefficients) + exponent)
    for index, coefficient in enumerate(coefficients):
        answer[index] += coefficient
        answer[index + exponent] -= coefficient
    return answer


def product(exponents: tuple[int, ...]) -> list[int]:
    answer = [1]
    for exponent in exponents:
        answer = multiply_binomial(answer, exponent)
    return answer


def divide_binomial(coefficients: list[int], exponent: int) -> list[int]:
    degree = len(coefficients) - 1
    quotient = [0] * (degree - exponent + 1)
    for index in range(len(quotient)):
        quotient[index] = coefficients[index]
        if index >= exponent:
            quotient[index] += quotient[index - exponent]
    assert multiply_binomial(quotient, exponent) == coefficients
    return quotient


def divisors(value: int) -> set[int]:
    answer: set[int] = set()
    for divisor in range(1, math.isqrt(value) + 1):
        if value % divisor == 0:
            answer.add(divisor)
            answer.add(value // divisor)
    return answer


def audit_tuple(exponents: tuple[int, ...]) -> tuple[list[dict[str, object]], int]:
    coefficients = product(exponents)
    total_energy = sum(coefficient * coefficient for coefficient in coefficients)
    rows = []
    for modulus in sorted(set().union(*(divisors(value) for value in exponents))):
        multiplicity = sum(exponent % modulus == 0 for exponent in exponents)
        quotient = coefficients
        for _ in range(multiplicity):
            quotient = divide_binomial(quotient, modulus)
        active = sorted({
            index % modulus
            for index, coefficient in enumerate(quotient)
            if coefficient
        })
        chains = [coefficients[residue::modulus] for residue in active]
        chain_energies = [
            sum(coefficient * coefficient for coefficient in chain)
            for chain in chains
        ]
        chain_l1 = [sum(abs(coefficient) for coefficient in chain) for chain in chains]
        equality_inverse_checks = []
        for chain, energy in zip(chains, chain_energies):
            if energy != 2 * multiplicity:
                continue
            positive = [index for index, value in enumerate(chain) if value == 1]
            negative = [index for index, value in enumerate(chain) if value == -1]
            equality_inverse_checks.append(
                all(abs(value) <= 1 for value in chain)
                and len(positive) == len(negative) == multiplicity
                and all(
                    sum(index**degree for index in positive)
                    == sum(index**degree for index in negative)
                    for degree in range(multiplicity)
                )
            )
        certificate = 2 * multiplicity * len(active)
        passed = (
            sum(chain_energies) == total_energy
            and all(value >= 2 * multiplicity for value in chain_energies)
            and all(value >= 2 * multiplicity for value in chain_l1)
            and all(equality_inverse_checks)
            and total_energy >= certificate
        )
        rows.append({
            "q": modulus,
            "m_q": multiplicity,
            "S_q": len(active),
            "chain_energies": chain_energies,
            "chain_l1_norms": chain_l1,
            "equality_chains": len(equality_inverse_checks),
            "equality_inverse_pass": all(equality_inverse_checks),
            "certificate_2mS": certificate,
            "total_energy": total_energy,
            "pass": passed,
        })
    return rows, total_energy


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=6)
    parser.add_argument("--max-exponent", type=int, default=9)
    args = parser.parse_args()

    tuple_count = 0
    row_count = 0
    strict_over_round8 = 0
    equality_rows = 0
    equality_chains = 0
    failures: list[dict[str, object]] = []
    for length in range(1, args.max_length + 1):
        for exponents in combinations_with_replacement(
            range(1, args.max_exponent + 1), length
        ):
            tuple_count += 1
            rows, _ = audit_tuple(exponents)
            for row in rows:
                row_count += 1
                m = int(row["m_q"])
                old_eta = 2 * ((m + 2) // 2) + (2 if m >= 3 else 0)
                strict_over_round8 += 2 * m > old_eta
                equality_rows += row["total_energy"] == row["certificate_2mS"]
                equality_chains += int(row["equality_chains"])
                if not row["pass"]:
                    failures.append({"exponents": exponents, **row})

    # Sharpness for m=1,...,4.  The m=3 example is a degree-2 Prouhet pair.
    sharp_examples = {
        "m1": [1, -1],
        "m2": [1, -1, -1, 1],
        "m3": [1, -1, -1, 0, 1, 1, -1],
    }
    sharp_energies = {
        name: sum(value * value for value in coefficients)
        for name, coefficients in sharp_examples.items()
    }

    print(json.dumps({
        "status": "PASS" if not failures else "FAIL",
        "scope": "finite regression only; the Newton-multiset proof is in REPORT.md",
        "scan": {
            "max_length": args.max_length,
            "max_exponent": args.max_exponent,
            "nondecreasing_tuples": tuple_count,
            "divisor_rows": row_count,
            "rows_strictly_stronger_than_round8_eta": strict_over_round8,
            "equality_rows": equality_rows,
            "equality_chains_with_inverse_structure_checked": equality_chains,
            "failures": failures,
        },
        "sharp_small_chain_energies": sharp_energies,
    }, indent=2))


if __name__ == "__main__":
    main()
