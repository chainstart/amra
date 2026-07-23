#!/usr/bin/env python3
"""Finite check of the moving-rho ANOVA identities.

This verifies finite algebra only.  It is not evidence for an asymptotic
claim or for Erdős #679.
"""

from __future__ import annotations

import cmath
import itertools
import json
import math


H = 2
PRIMES = (5, 7, 11)
RHO = 0.2
B = 1.0 - RHO
K = 3
Q = math.prod(PRIMES)
CONDUCTOR_CUTOFF = 1.2


def hit(p: int, n: int) -> bool:
    return any((n - K - j) % p == 0 for j in range(H))


def local_g(p: int, n: int) -> float:
    return RHO if hit(p, n) else 1.0


MEAN = {p: 1.0 - B * H / p for p in PRIMES}
VAR = {p: B * B * (H / p) * (1.0 - H / p) for p in PRIMES}
THETA = {p: VAR[p] / (MEAN[p] ** 2 + VAR[p]) for p in PRIMES}


def conductor(mask: int) -> int:
    return math.prod(p for i, p in enumerate(PRIMES) if mask & (1 << i))


def component(mask: int, n: int) -> float:
    out = 1.0
    for i, p in enumerate(PRIMES):
        centred = local_g(p, n) - MEAN[p]
        out *= centred if mask & (1 << i) else MEAN[p]
    return out


def fourier_energy(mask: int) -> float:
    c = conductor(mask)
    hats = []
    for u in range(c):
        hats.append(
            sum(
                component(mask, n)
                * cmath.exp(-2j * math.pi * u * n / c)
                for n in range(c)
            )
            / c
        )
    return sum(abs(value) ** 2 for value in hats)


def main() -> None:
    masks = tuple(range(1 << len(PRIMES)))
    energies = {mask: fourier_energy(mask) for mask in masks}
    exact_m2 = math.prod(
        1.0 - (1.0 - RHO * RHO) * H / p for p in PRIMES
    )
    direct_m2 = sum(
        math.prod(local_g(p, n) for p in PRIMES) ** 2 for n in range(Q)
    ) / Q

    reconstruction_error = max(
        abs(
            math.prod(local_g(p, n) for p in PRIMES)
            - sum(component(mask, n) for mask in masks)
        )
        for n in range(Q)
    )
    energy_product_error = max(
        abs(
            energies[mask] / exact_m2
            - math.prod(
                THETA[p] if mask & (1 << i) else 1.0 - THETA[p]
                for i, p in enumerate(PRIMES)
            )
        )
        for mask in masks
    )

    low_probability = sum(
        energies[mask] / exact_m2
        for mask in masks
        if conductor(mask) <= CONDUCTOR_CUTOFF
    )
    lam = sum(THETA.values())
    r0 = math.log(CONDUCTOR_CUTOFF) / math.log(H)
    chernoff = math.exp(-lam + r0 + r0 * math.log(lam / r0))

    primitive_error = 0.0
    duplicate_fractions = False
    seen: set[tuple[int, int]] = set()
    for mask in masks[1:]:
        c = conductor(mask)
        for u in range(c):
            coeff = sum(
                component(mask, n)
                * cmath.exp(-2j * math.pi * u * n / c)
                for n in range(c)
            ) / c
            if math.gcd(u, c) != 1:
                primitive_error = max(primitive_error, abs(coeff))
            elif abs(coeff) > 1e-13:
                reduced = (u, c)
                duplicate_fractions |= reduced in seen
                seen.add(reduced)

    entropy = 1.0 - RHO + RHO * math.log(RHO)
    entropy_identity_error = abs(
        (B - entropy) - RHO * math.log(1.0 / RHO)
    )
    tolerance = 1e-11
    checks = {
        "anova_reconstruction": reconstruction_error < tolerance,
        "exact_second_moment": abs(direct_m2 - exact_m2) < tolerance,
        "parseval_energy": abs(sum(energies.values()) - exact_m2) < tolerance,
        "energy_is_product_bernoulli": energy_product_error < tolerance,
        "conductor_implies_cardinality_chernoff": low_probability <= chernoff + tolerance,
        "nonprimitive_coefficients_vanish": primitive_error < tolerance,
        "primitive_fractions_do_not_collide": not duplicate_fractions,
        "entropy_identity": entropy_identity_error < tolerance,
    }
    print(
        json.dumps(
            {
                "parameters": {
                    "H": H,
                    "primes": PRIMES,
                    "rho": RHO,
                    "cutoff": CONDUCTOR_CUTOFF,
                    "period": Q,
                },
                "checks": checks,
                "diagnostics": {
                    "reconstruction_error": reconstruction_error,
                    "exact_second_moment": exact_m2,
                    "direct_second_moment": direct_m2,
                    "energy_product_error": energy_product_error,
                    "lambda": lam,
                    "cardinality_cutoff": r0,
                    "low_energy_probability": low_probability,
                    "chernoff_bound": chernoff,
                    "max_nonprimitive_coefficient": primitive_error,
                    "entropy_I_rho": entropy,
                    "entropy_identity_error": entropy_identity_error,
                },
                "result": "PASS" if all(checks.values()) else "FAIL",
                "scope": "finite algebra and normalization only",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

