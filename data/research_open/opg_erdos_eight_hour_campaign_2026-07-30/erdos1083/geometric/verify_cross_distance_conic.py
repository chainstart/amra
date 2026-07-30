#!/usr/bin/env python3
"""Verification for the cross-fibre distance-conic attack."""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from fractions import Fraction


def squared_distances(
    alpha: float,
    gamma: float,
    rho: float,
    sigma: float,
    z: float,
    w: float,
    *,
    antipodal_source: bool = False,
) -> tuple[float, float, float, float]:
    """Return C, p, d_minus, d_plus for a source/success flag."""
    source_angle = alpha + (math.pi if antipodal_source else 0.0)
    constant = (z - w) ** 2 + rho**2 + sigma**2
    product = 2 * rho * sigma
    d_minus = constant - product * math.cos(gamma - source_angle)
    d_plus = constant - product * math.cos(
        gamma + 2 * alpha - source_angle
    )
    return constant, product, d_minus, d_plus


def conic_residual(
    alpha: float,
    constant: float,
    product: float,
    d_minus: float,
    d_plus: float,
) -> float:
    """Residual in the proposed conic identity."""
    return (
        (2 * constant - d_plus - d_minus) ** 2
        * math.sin(alpha) ** 2
        + (d_plus - d_minus) ** 2 * math.cos(alpha) ** 2
        - product**2 * math.sin(2 * alpha) ** 2
    )


def quotient_curve_value(
    alpha: float,
    constant: float,
    product: float,
    total_distance: float,
) -> float:
    """Value s=(d_plus-d_minus)^2 on the quotient parabola."""
    return (
        4 * product**2 * math.sin(alpha) ** 2
        - math.tan(alpha) ** 2
        * (2 * constant - total_distance) ** 2
    )


def random_identity_audit(
    trials: int = 1000, seed: int = 1083
) -> dict[str, object]:
    rng = random.Random(seed)
    maximum_residual = 0.0
    maximum_quotient_residual = 0.0
    for _ in range(trials):
        alpha = rng.uniform(0.15, 1.35)
        gamma = rng.uniform(-math.pi, math.pi)
        rho = rng.uniform(0.1, 5.0)
        sigma = rng.uniform(0.1, 5.0)
        z = rng.uniform(-4.0, 4.0)
        w = rng.uniform(-4.0, 4.0)
        antipodal = bool(rng.randrange(2))
        constant, product, d_minus, d_plus = squared_distances(
            alpha,
            gamma,
            rho,
            sigma,
            z,
            w,
            antipodal_source=antipodal,
        )
        residual = abs(
            conic_residual(
                alpha,
                constant,
                product,
                d_minus,
                d_plus,
            )
        )
        scale = max(1.0, product**2, constant**2)
        maximum_residual = max(maximum_residual, residual / scale)

        total = d_plus + d_minus
        square_difference = (d_plus - d_minus) ** 2
        quotient_residual = abs(
            square_difference
            - quotient_curve_value(
                alpha, constant, product, total
            )
        )
        maximum_quotient_residual = max(
            maximum_quotient_residual,
            quotient_residual / scale,
        )
    if maximum_residual > 2e-13:
        raise AssertionError(maximum_residual)
    if maximum_quotient_residual > 2e-13:
        raise AssertionError(maximum_quotient_residual)
    return {
        "trials": trials,
        "maximum_scaled_conic_residual": maximum_residual,
        "maximum_scaled_quotient_residual": maximum_quotient_residual,
    }


def collision_audit(modulus: int = 17, alpha_index: int = 2) -> dict[str, int]:
    """Enumerate angular collisions for one fixed generic circle pair."""
    alpha = 2 * math.pi * alpha_index / modulus
    rho, sigma, z, w = 2.0, 3.0, -1.0, 4.0
    ordered = defaultdict(list)
    quotient = defaultdict(list)
    for gamma_index in range(modulus):
        gamma = 2 * math.pi * gamma_index / modulus
        _, _, d_minus, d_plus = squared_distances(
            alpha, gamma, rho, sigma, z, w
        )
        ordered_key = (round(d_minus, 11), round(d_plus, 11))
        quotient_key = (
            round(d_minus + d_plus, 11),
            round((d_plus - d_minus) ** 2, 11),
        )
        ordered[ordered_key].append(gamma_index)
        quotient[quotient_key].append(gamma_index)
    maximum_ordered = max(map(len, ordered.values()))
    maximum_quotient = max(map(len, quotient.values()))
    if maximum_ordered != 1:
        raise AssertionError(("ordered collision", ordered))
    if maximum_quotient > 2:
        raise AssertionError(("quotient collision", quotient))
    return {
        "modulus": modulus,
        "ordered_distance_pairs": len(ordered),
        "quotient_points": len(quotient),
        "maximum_ordered_gamma_multiplicity": maximum_ordered,
        "maximum_quotient_gamma_multiplicity": maximum_quotient,
    }


def physical_capacity_barrier(
    curve_count: int = 25,
    alpha: float = 0.7,
    distance: float = 10.0,
) -> dict[str, object]:
    """Construct many physical (C,p) curves through one distance point."""
    cosine = math.cos(alpha)
    lower = distance / (1 + cosine)
    upper = distance / (1 - cosine)
    parameters = []
    maximum_residual = 0.0
    for index in range(1, curve_count + 1):
        constant = lower + (upper - lower) * index / (curve_count + 1)
        product = abs(constant - distance) / cosine
        if not (0 < product <= constant):
            raise AssertionError((constant, product))
        radius = math.sqrt(product / 2)
        height_gap = math.sqrt(constant - product)
        reconstructed_constant = height_gap**2 + 2 * radius**2
        reconstructed_product = 2 * radius**2
        residual = abs(
            conic_residual(
                alpha,
                reconstructed_constant,
                reconstructed_product,
                distance,
                distance,
            )
        )
        maximum_residual = max(maximum_residual, residual)
        parameters.append((round(constant, 12), round(product, 12)))
    if len(set(parameters)) != curve_count:
        raise AssertionError("capacity-barrier curves are not distinct")
    if maximum_residual > 1e-10:
        raise AssertionError(maximum_residual)
    return {
        "curve_count": curve_count,
        "common_distance_point": [distance, distance],
        "distinct_physical_parameters": len(set(parameters)),
        "maximum_residual": maximum_residual,
    }


def parameter_multiplicity(
    circles: list[tuple[Fraction, Fraction]]
) -> dict[str, object]:
    """Count collisions of exact (C,p) among ordered circle pairs."""
    counts: Counter[tuple[Fraction, Fraction]] = Counter()
    for left, (rho, z) in enumerate(circles):
        for right, (sigma, w) in enumerate(circles):
            if left == right:
                continue
            constant = (z - w) ** 2 + rho**2 + sigma**2
            product = 2 * rho * sigma
            counts[(constant, product)] += 1
    return {
        "ordered_circle_pairs": len(circles) * (len(circles) - 1),
        "distinct_parameters": len(counts),
        "maximum_parameter_multiplicity": max(counts.values(), default=0),
    }


def exponent_ledger(
    delta: Fraction = Fraction(3, 5),
    active_angle: Fraction = Fraction(1, 5),
    source: Fraction = Fraction(3, 5),
    success: Fraction = Fraction(1, 1),
) -> dict[str, str]:
    """Critical exponents for the conditional incidence estimate."""
    point_exponent = 2 * delta
    forced_joint = active_angle + source + success
    return {
        "distance_delta": str(delta),
        "distance_pair_points": str(point_exponent),
        "active_angles": str(active_angle),
        "source_q": str(source),
        "success_r": str(success),
        "forced_joint_mass": str(forced_joint),
        "target_nD": str(1 + delta),
        "conditional_upper_mu_term": str(active_angle + 2 * delta),
        "conditional_upper_rich_curve_term_before_mu_lambda": str(
            active_angle + 4 * delta
        ),
        "global_three_degree_mu_term": str(2 * delta),
        "global_three_degree_rich_term_before_mu_lambda": str(
            6 * delta
        ),
        "critical_contradiction_conditions": (
            "u<2/5 and ell>2/5+u/2"
        ),
        "target_J_conditions": "u<=1/5 and ell>=1/2+u/2",
        "global_critical_contradiction_conditions": (
            "u<3/5 and ell>9/20+u/4"
        ),
        "global_target_J_conditions": (
            "u<=2/5 and ell>=1/2+u/4"
        ),
    }


def audit(trials: int = 1000) -> dict[str, object]:
    circles = [
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(2)),
        (Fraction(2), Fraction(0)),
        (Fraction(2), Fraction(1)),
    ]
    return {
        "schema": "amra.erdos1083.cross-distance-conic.v1",
        "scope": "Identity, collision, capacity, and exponent regressions.",
        "identity": random_identity_audit(trials=trials),
        "collisions": collision_audit(),
        "capacity_barrier": physical_capacity_barrier(),
        "parameter_multiplicity": parameter_multiplicity(circles),
        "exponent_ledger": exponent_ledger(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=1000)
    args = parser.parse_args()
    print(json.dumps(audit(args.trials), indent=2, sort_keys=True))
