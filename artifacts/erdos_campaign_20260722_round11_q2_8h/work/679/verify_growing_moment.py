#!/usr/bin/env python3
"""Finite algebra check for the growing-moment ANOVA/large-sieve lemma.

This checks identities only.  It is not evidence for an asymptotic claim.
"""

from __future__ import annotations

import cmath
import itertools
import json
import math


H = 2
PRIMES = (5, 7, 11)
K = 1
A = 13
N = 40
CUTOFF = 55
BASE_A = 0.07
MOMENT_Q = 17
T = 1.0 - BASE_A
B = 1.0 - T**MOMENT_Q
Q = math.prod(PRIMES)


def local_g(p: int, n: int) -> float:
    hit = any((n - K - j) % p == 0 for j in range(H))
    return 1.0 - B * int(hit)


MEANS = {p: 1.0 - B * H / p for p in PRIMES}
VARIANCES = {p: B**2 * (H / p) * (1.0 - H / p) for p in PRIMES}
THETAS = {
    p: VARIANCES[p] / (MEANS[p] ** 2 + VARIANCES[p]) for p in PRIMES
}


def local_d(p: int, n: int) -> float:
    return local_g(p, n) - MEANS[p]


def conductor(mask: int) -> int:
    return math.prod(p for i, p in enumerate(PRIMES) if mask & (1 << i))


def f_mask(mask: int, n: int) -> float:
    value = 1.0
    for i, p in enumerate(PRIMES):
        value *= local_d(p, n) if mask & (1 << i) else MEANS[p]
    return value


def fourier(mask: int) -> list[complex]:
    c = conductor(mask)
    return [
        sum(
            f_mask(mask, x) * cmath.exp(-2j * math.pi * u * x / c)
            for x in range(c)
        )
        / c
        for u in range(c)
    ]


def main() -> None:
    masks = range(1 << len(PRIMES))
    coeffs = {mask: fourier(mask) for mask in masks}

    reconstruction_error = max(
        abs(
            math.prod(local_g(p, n) for p in PRIMES)
            - sum(f_mask(mask, n) for mask in masks)
        )
        for n in range(Q)
    )

    nonprimitive_error = 0.0
    inversion_error = 0.0
    coefficient_energy = 0.0
    physical_anova_energy = 0.0
    mask_energies = {}
    for mask in masks:
        c = conductor(mask)
        hats = coeffs[mask]
        mask_energies[mask] = sum(abs(value) ** 2 for value in hats)
        coefficient_energy += mask_energies[mask]
        physical_anova_energy += sum(f_mask(mask, x) ** 2 for x in range(c)) / c
        inversion_error = max(
            inversion_error,
            max(
                abs(
                    f_mask(mask, x)
                    - sum(
                        hats[u] * cmath.exp(2j * math.pi * u * x / c)
                        for u in range(c)
                    )
                )
                for x in range(c)
            ),
        )
        if mask:
            nonprimitive_error = max(
                nonprimitive_error,
                max(
                    (
                        abs(hats[u])
                        if math.gcd(u, c) != 1
                        else 0.0
                    )
                    for u in range(c)
                ),
            )

    exact_second_moment = math.prod(
        1.0 - (1.0 - T ** (2 * MOMENT_Q)) * H / p for p in PRIMES
    )
    direct_second_moment = sum(
        math.prod(local_g(p, n) for p in PRIMES) ** 2 for n in range(Q)
    ) / Q

    normalized_energy_error = max(
        abs(
            mask_energies[mask] / exact_second_moment
            - math.prod(
                THETAS[p] if mask & (1 << i) else 1.0 - THETAS[p]
                for i, p in enumerate(PRIMES)
            )
        )
        for mask in masks
    )
    normalized_energy_total = sum(
        mask_energies[mask] / exact_second_moment for mask in masks
    )
    theta_upper_margin = min(H / p - THETAS[p] for p in PRIMES)

    low_masks = [
        mask
        for mask in masks
        if mask and conductor(mask) <= CUTOFF
    ]
    low_energy = sum(
        abs(coeffs[mask][u]) ** 2
        for mask in low_masks
        for u in range(conductor(mask))
    )
    low_values = [
        sum(f_mask(mask, n) for mask in low_masks)
        for n in range(A + 1, A + N + 1)
    ]
    large_sieve_lhs = sum(abs(value) ** 2 for value in low_values)
    large_sieve_rhs = (N - 1 + CUTOFF**2) * low_energy

    fractions = [
        (u / conductor(mask), mask, u)
        for mask in low_masks
        for u in range(conductor(mask))
        if math.gcd(u, conductor(mask)) == 1
    ]
    minimum_circular_spacing = min(
        min(abs(x[0] - y[0]), 1.0 - abs(x[0] - y[0]))
        for x, y in itertools.combinations(fractions, 2)
    )

    toler = 5e-12
    checks = {
        "anova_reconstruction": reconstruction_error < toler,
        "fourier_inversion": inversion_error < toler,
        "nonprimitive_coefficients_vanish": nonprimitive_error < toler,
        "parseval_anova": abs(coefficient_energy - physical_anova_energy) < toler,
        "exact_second_moment": abs(coefficient_energy - exact_second_moment) < toler,
        "direct_second_moment": abs(direct_second_moment - exact_second_moment) < toler,
        "normalized_energy_is_product_bernoulli": normalized_energy_error < toler,
        "normalized_energy_sums_to_one": abs(normalized_energy_total - 1.0) < toler,
        "theta_at_most_H_over_p": theta_upper_margin >= -toler,
        "farey_spacing": minimum_circular_spacing + toler >= CUTOFF**-2,
        "large_sieve_inequality": large_sieve_lhs <= large_sieve_rhs + toler,
    }
    payload = {
        "parameters": {
            "H": H,
            "primes": PRIMES,
            "K": K,
            "interval_start": A,
            "interval_length": N,
            "cutoff": CUTOFF,
            "base_a": BASE_A,
            "moment_q": MOMENT_Q,
            "full_period": Q,
        },
        "checks": checks,
        "diagnostics": {
            "reconstruction_error": reconstruction_error,
            "fourier_inversion_error": inversion_error,
            "max_nonprimitive_coefficient": nonprimitive_error,
            "coefficient_energy": coefficient_energy,
            "physical_anova_energy": physical_anova_energy,
            "exact_second_moment": exact_second_moment,
            "direct_second_moment": direct_second_moment,
            "normalized_energy_error": normalized_energy_error,
            "normalized_energy_total": normalized_energy_total,
            "theta_parameters": THETAS,
            "theta_upper_margin": theta_upper_margin,
            "minimum_circular_spacing": minimum_circular_spacing,
            "farey_lower_bound": CUTOFF**-2,
            "low_energy": low_energy,
            "large_sieve_lhs": large_sieve_lhs,
            "large_sieve_rhs": large_sieve_rhs,
        },
        "result": "PASS" if all(checks.values()) else "FAIL",
        "scope": "finite algebra and normalization only",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
