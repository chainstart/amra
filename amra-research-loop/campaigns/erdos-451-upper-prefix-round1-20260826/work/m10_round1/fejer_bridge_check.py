#!/usr/bin/env python3
"""Finite numerical consistency checks for the L=2 Fejer bridge.

This script is evidence only.  The note proves all identities symbolically.
"""

from __future__ import annotations

import cmath
import json
import math
from collections import defaultdict


def sinc(x: float) -> float:
    return 1.0 if x == 0.0 else math.sin(x) / x


def centered(a: int, modulus: int) -> int:
    r = a % modulus
    return r - modulus if r > modulus // 2 else r


def crt_from_residues(residues: tuple[int, ...], primes: tuple[int, ...]) -> int:
    modulus = math.prod(primes)
    value = 0
    for residue, prime in zip(residues, primes):
        cofactor = modulus // prime
        value += residue * cofactor * pow(cofactor, -1, prime)
    return centered(value, modulus)


def main() -> None:
    primes = (5, 7)
    modulus = math.prod(primes)
    b = 1.5
    h = 3

    beta = {
        a: (1.0 / b) * max(0.0, 1.0 - abs(a) / b)
        for a in range(-math.floor(b), math.floor(b) + 1)
    }

    def omega(r: int) -> float:
        if r % modulus == 0:
            return 1.0
        rr = centered(r, modulus)
        return (
            math.sin(math.pi * h * rr / modulus)
            / (h * math.sin(math.pi * rr / modulus))
        ) ** 2

    coeffs: dict[int, float] = defaultdict(float)
    for a0, beta0 in beta.items():
        for a1, beta1 in beta.items():
            lift = crt_from_residues((a0, a1), primes)
            coeffs[lift] += beta0 * beta1

    def v(r: int) -> complex:
        return sum(
            weight * cmath.exp(2j * math.pi * lift * r / modulus)
            for lift, weight in coeffs.items()
        )

    real_side = sum(omega(r) * v(r).real for r in range(modulus))
    spectral_side = (modulus / h) * sum(
        weight * max(0.0, 1.0 - abs(lift) / h)
        for lift, weight in coeffs.items()
        if abs(lift) < h
    )

    dft_error = 0.0
    for j in range(modulus):
        jj = centered(j, modulus)
        actual = sum(
            omega(r) * cmath.exp(-2j * math.pi * j * r / modulus)
            for r in range(modulus)
        ) / modulus
        expected = (1.0 / h) * max(0.0, 1.0 - abs(jj) / h)
        dft_error = max(dft_error, abs(actual - expected))

    # A finite truncation checks the purely combinatorial carry identity and
    # the one-sided E <= S comparison without using Fourier inversion.
    cutoff = 40
    local = []
    for prime in primes:
        local.append(
            {
                n: sinc(math.pi * b * n / prime) ** 2
                for n in range(-cutoff, cutoff + 1)
            }
        )
    fibres: dict[int, float] = defaultdict(float)
    for n0, w0 in local[0].items():
        for n1, w1 in local[1].items():
            numerator = n0 * (modulus // primes[0]) + n1 * (
                modulus // primes[1]
            )
            fibres[numerator] += w0 * w1

    residue_mass: dict[int, float] = defaultdict(float)
    for numerator, weight in fibres.items():
        residue_mass[numerator % modulus] += weight
    carry_error = 0.0
    for residue in range(modulus):
        product_mass = 1.0
        for prime, weights in zip(primes, local):
            cofactor = modulus // prime
            c = pow(cofactor, -1, prime)
            product_mass *= sum(
                weight for n, weight in weights.items() if n % prime == c * residue % prime
            )
        carry_error = max(carry_error, abs(product_mass - residue_mass[residue]))

    exact_truncated = sum(
        sinc(math.pi * h * numerator / modulus) ** 2 * weight
        for numerator, weight in fibres.items()
    )
    majorant_truncated = sum(
        omega(residue) * weight for residue, weight in residue_mass.items()
    )

    print(
        json.dumps(
            {
                "parameters": {
                    "primes": primes,
                    "P": modulus,
                    "b": b,
                    "h": h,
                    "carry_cutoff": cutoff,
                },
                "real_side_S": real_side,
                "spectral_side_S": spectral_side,
                "parseval_abs_error": abs(real_side - spectral_side),
                "omega_dft_max_abs_error": dft_error,
                "finite_carry_identity_max_abs_error": carry_error,
                "finite_exact_E": exact_truncated,
                "finite_majorant_S": majorant_truncated,
                "majorant_minus_exact": majorant_truncated - exact_truncated,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
