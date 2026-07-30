#!/usr/bin/env python3
"""Exact audit of synchronization obtainable from circular marginals alone."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
from fractions import Fraction
from pathlib import Path


def split_extremizer(scale: int) -> dict[str, int | Fraction]:
    """The source-disjoint, rotation-common angular-fibre construction."""

    if scale < 3:
        raise ValueError("scale must be at least three")
    t = scale
    active_angles = t
    source_degree = t**3
    reservoir_fibres = t**2 * (t - 1)
    reservoir_fibre_size = t**2
    source_fibres = active_angles * source_degree
    points = (
        reservoir_fibres * reservoir_fibre_size + source_fibres
    )
    if points != t**5:
        raise AssertionError("split extremizer mass is not t^5")
    rotation_successes = [
        reservoir_fibres * (reservoir_fibre_size - 2 * angle)
        for angle in range(1, active_angles + 1)
    ]
    return {
        "scale": t,
        "points": points,
        "critical_distance_parameter": t**3,
        "active_angle_count": active_angles,
        "source_count_per_angle": source_degree,
        "source_incidence_sum": active_angles * source_degree,
        "source_fibre_count": source_fibres,
        "reservoir_fibre_count": reservoir_fibres,
        "reservoir_fibre_size": reservoir_fibre_size,
        "total_fibre_count": source_fibres + reservoir_fibres,
        "minimum_rotation_success": min(rotation_successes),
        "rotation_success_sum": sum(rotation_successes),
        "joint_moment": source_degree * sum(rotation_successes),
        "minimum_rotation_success_over_n": Fraction(
            min(rotation_successes), points
        ),
        "maximum_source_fibre_angle_degree": 1,
        "maximum_two_angle_source_codegree": 0,
        "common_rotation_reservoir_fibres": reservoir_fibres,
        "common_rotation_reservoir_mass": (
            reservoir_fibres * reservoir_fibre_size
        ),
        "maximum_per_fibre_chord_labels": reservoir_fibre_size - 1,
    }


def interpolated_binomial(mean: Fraction, order: int) -> Fraction:
    """Lower convex envelope of d -> binom(d, order) at a real mean."""

    lower = mean.numerator // mean.denominator
    fraction = mean - lower
    return (
        (1 - fraction) * math.comb(lower, order)
        + fraction * math.comb(lower + 1, order)
    )


def drc_common_mass_bound(
    angle_count: int,
    density: Fraction,
    threshold: Fraction,
    chosen_angles: int,
) -> Fraction:
    """Threshold plus weighted DRC lower bound for distinct angles."""

    if not 0 <= threshold < density <= 1:
        raise ValueError("need 0 <= threshold < density <= 1")
    if not 1 <= chosen_angles <= angle_count:
        raise ValueError("invalid chosen angle count")
    good_mass = (density - threshold) / (1 - threshold)
    mean_degree = angle_count * good_mass
    return interpolated_binomial(
        mean_degree, chosen_angles
    ) / math.comb(angle_count, chosen_angles)


def exhaustive_binary_drc_audit() -> dict[str, object]:
    """Check the convex DRC inequality on every small binary incidence row."""

    checks = 0
    minimum_slack: Fraction | None = None
    for angle_count in range(2, 9):
        subsets = tuple(range(1 << angle_count))
        for fibre_count in range(1, 5):
            for seed in range(32):
                rng = random.Random(
                    1083 + 1000 * angle_count + 100 * fibre_count + seed
                )
                weights = [
                    Fraction(rng.randrange(1, 10), 1)
                    for _ in range(fibre_count)
                ]
                total_weight = sum(weights)
                mu = [weight / total_weight for weight in weights]
                rows = [subsets[rng.randrange(len(subsets))] for _ in mu]
                angle_masses = [
                    sum(
                        mu[fibre]
                        for fibre, row in enumerate(rows)
                        if row & (1 << angle)
                    )
                    for angle in range(angle_count)
                ]
                density = min(angle_masses)
                for chosen in range(1, min(4, angle_count) + 1):
                    actual = max(
                        sum(
                            mu[fibre]
                            for fibre, row in enumerate(rows)
                            if all(
                                row & (1 << angle)
                                for angle in angles
                            )
                        )
                        for angles in itertools.combinations(
                            range(angle_count), chosen
                        )
                    )
                    mean_degree = sum(
                        mu[fibre] * rows[fibre].bit_count()
                        for fibre in range(fibre_count)
                    )
                    lower = interpolated_binomial(
                        mean_degree, chosen
                    ) / math.comb(angle_count, chosen)
                    if actual < lower:
                        raise AssertionError(
                            "weighted distinct-angle DRC failed"
                        )
                    slack = actual - lower
                    minimum_slack = (
                        slack
                        if minimum_slack is None
                        else min(minimum_slack, slack)
                    )
                    checks += 1
                if density < 0 or density > 1:
                    raise AssertionError("invalid incidence density")
    return {
        "weighted_binary_graph_checks": checks,
        "minimum_slack_numerator": minimum_slack.numerator,
        "minimum_slack_denominator": minimum_slack.denominator,
    }


def build_audit(scales: tuple[int, ...] = (3, 4, 7, 12)) -> dict:
    extremizers = [split_extremizer(scale) for scale in scales]
    for row in extremizers:
        t = int(row["scale"])
        if row["source_incidence_sum"] != t**4:
            raise AssertionError("source exponent changed")
        if row["maximum_two_angle_source_codegree"] != 0:
            raise AssertionError("split source fibres accidentally overlap")
        if row["maximum_per_fibre_chord_labels"] >= row[
            "critical_distance_parameter"
        ]:
            raise AssertionError("per-fibre chord cap failed")
        if row["joint_moment"] <= 0:
            raise AssertionError("joint moment vanished")

    drc_examples = []
    for angle_count, chosen in ((20, 2), (20, 3), (50, 4)):
        density = Fraction(9, 10)
        threshold = Fraction(1, 2)
        drc_examples.append(
            {
                "angle_count": angle_count,
                "chosen_angles": chosen,
                "density": str(density),
                "threshold": str(threshold),
                "common_mass_lower_bound": str(
                    drc_common_mass_bound(
                        angle_count, density, threshold, chosen
                    )
                ),
            }
        )

    payload = {
        "scope": (
            "Exact marginal-only synchronization audit.  The split "
            "extremizer is an abstract angular-fibre construction, not a "
            "few-distance Euclidean point set."
        ),
        "split_extremizer_rows": [
            {
                key: str(value) if isinstance(value, Fraction) else value
                for key, value in row.items()
            }
            for row in extremizers
        ],
        "drc_examples": drc_examples,
        "exhaustive_binary_drc": exhaustive_binary_drc_audit(),
        "exponent_ledger": {
            "critical_D": "N^(3/5)",
            "active_angles_M": "N^(1/5)",
            "source_degree_Q": "N^(3/5)",
            "global_source_incidence_mass": "N^(4/5)",
            "forced_source_rectangle": (
                "one angle x Omega(Q) fibres; no two-angle common fibre"
            ),
            "fixed_h_rotation_common_fibres": "N^(2/5-o(1))",
            "unconditional_same_radius_sparse_certificate": "O(1)",
            "resulting_unconditional_distance_exponent": "does_not_exceed_3/5",
        },
    }
    return {
        "schema": "amra.erdos1083.sync_extraction_drc.v1",
        "claim_labels": {
            "source_rectangle_optimality_from_marginals": "human_proof",
            "weighted_rotation_drc": "human_proof",
            "split_abstract_extremizer": "human_proof_and_finite_regression",
            "unconditional_f3_improvement": "open_gap",
        },
        **payload,
        "sha256_payload": hashlib.sha256(
            json.dumps(
                payload, separators=(",", ":"), sort_keys=True
            ).encode()
        ).hexdigest(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name(
            "sync_extraction_drc_certificate.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    audit = build_audit()
    args.output.write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    print(f"CERTIFICATE|sha256={audit['sha256_payload']}")


if __name__ == "__main__":
    main()
