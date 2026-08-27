#!/usr/bin/env python3
"""Finite off-by-one checks for the exact fibre-phase identities.

The audit note contains the proofs.  This exhausts arbitrary subsets on
small coprime periods and checks the average, boundary, and centered-energy
formulas without using any M10 author code.
"""

from __future__ import annotations

import json
import math
from collections import Counter


def energy(values: list[int]) -> int:
    return sum(value * value for value in Counter(values).values())


def main() -> None:
    systems = 0
    phase_rows = 0
    for q in range(2, 11):
        for r in range(2, 11):
            if math.gcd(q, r) != 1:
                continue
            invq = pow(q, -1, r)
            for mask in range(1, 1 << q):
                aa = [a for a in range(q) if mask >> a & 1]
                e_values = []
                residue_energy = energy([a % r for a in aa])
                for xi in range(q):
                    phases = [(invq * a + (1 if a < xi else 0)) % r for a in aa]
                    exact = energy(phases)
                    e_values.append(exact)

                    left = Counter(a % r for a in aa if a < xi)
                    right = Counter(a % r for a in aa if a >= xi)
                    boundary = residue_energy + 2 * sum(
                        left[y] * (right[(y + q) % r] - right[y]) for y in range(r)
                    )
                    assert exact == boundary
                    assert exact <= 2 * residue_energy
                    phase_rows += 1

                average_numerator = q * len(aa)
                for m in range(1, (q - 1) // r + 1):
                    shift = m * r
                    cyclic_correlation = sum(
                        1 for a in aa for b in aa if (a - b) % q == shift % q
                    )
                    average_numerator += 2 * (q - shift) * cyclic_correlation
                assert sum(e_values) == average_numerator
                systems += 1

    centered_cases = 0
    for r in range(2, 80):
        for n in range(1, r + 1):
            for d in range(1, r):
                lhs = r * n - n * n
                # Cross-multiply the strict centered Parseval threshold.
                cauchy_succeeds = lhs * (r - d) < n * n * d
                assert cauchy_succeeds == (n + d > r)
                centered_cases += 1

    print(
        json.dumps(
            {
                "classification": "finite_off_by_one_diagnostic_only",
                "subset_systems": systems,
                "phase_rows": phase_rows,
                "centered_threshold_cases": centered_cases,
                "status": "pass",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
