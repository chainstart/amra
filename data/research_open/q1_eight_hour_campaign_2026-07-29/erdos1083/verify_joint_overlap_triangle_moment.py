#!/usr/bin/env python3
"""Verify exponent and finite-array claims for the joint moment audit."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction


def exponent_ledger(
    eta_numerator: int, eta_denominator: int
) -> dict[str, Fraction]:
    eta = Fraction(eta_numerator, eta_denominator)
    incidence = Fraction(3)
    overlap_mass = Fraction(10, 3) - eta
    triangle_mass = Fraction(3) - 3 * eta
    d_max = Fraction(1)
    tau_max = Fraction(2)
    joint_bound = overlap_mass
    joint_target = Fraction(11, 3) + eta
    return {
        "eta": eta,
        "incidence": incidence,
        "overlap_mass": overlap_mass,
        "triangle_mass": triangle_mass,
        "d_max": d_max,
        "tau_max": tau_max,
        "minimum_d_support": overlap_mass - d_max,
        "minimum_tau_support": triangle_mass - tau_max,
        "maximum_support_exponent": max(
            overlap_mass - d_max, triangle_mass - tau_max
        ),
        "joint_bound": joint_bound,
        "joint_average_per_incidence": joint_bound - incidence,
        "joint_target": joint_target,
        "joint_gap": joint_target - joint_bound,
        "weighted_triangle_target": Fraction(1, 3) + 2 * eta,
        "hub_size": Fraction(2, 3) + eta,
        "hub_incidence": Fraction(11, 3) + eta,
        "hub_pair_count": Fraction(4, 3) + 2 * eta,
        "overlap_block_support": overlap_mass - 2,
    }


def disjoint_support_arrays(
    incidence_count: int,
    overlap_total: int,
    triangle_total: int,
    d_max: int,
    tau_max: int,
) -> dict[str, object]:
    d_support = (overlap_total + d_max - 1) // d_max
    tau_support = (triangle_total + tau_max - 1) // tau_max
    if d_support + tau_support > incidence_count:
        raise ValueError("the requested disjoint supports do not fit")
    d_values = [0] * incidence_count
    tau_values = [0] * incidence_count
    remaining = overlap_total
    for index in range(d_support):
        value = min(d_max, remaining)
        d_values[index] = value
        remaining -= value
    remaining = triangle_total
    for offset in range(tau_support):
        index = d_support + offset
        value = min(tau_max, remaining)
        tau_values[index] = value
        remaining -= value
    return {
        "d_sum": sum(d_values),
        "tau_sum": sum(tau_values),
        "joint_sum": sum(
            first * second
            for first, second in zip(d_values, tau_values)
        ),
        "d_support": sum(value > 0 for value in d_values),
        "tau_support": sum(value > 0 for value in tau_values),
    }


def random_survival_lower_bound(
    radius_count: int, height_count: int, selected_count: int
) -> Fraction:
    usable_third_vertices = max(radius_count - 4, 0)
    distinct_links_per_vertex = Fraction(height_count, 2)
    pair_survival = Fraction(selected_count, height_count**2) ** 2
    return (
        usable_third_vertices
        * distinct_links_per_vertex
        * pair_survival
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta-numerator", type=int, default=1)
    parser.add_argument("--eta-denominator", type=int, default=30)
    args = parser.parse_args()
    result = {
        "exponent_ledger": exponent_ledger(
            args.eta_numerator, args.eta_denominator
        ),
        "finite_disjoint_support": disjoint_support_arrays(
            incidence_count=100,
            overlap_total=120,
            triangle_total=70,
            d_max=5,
            tau_max=4,
        ),
        "random_survival_lower_bound": random_survival_lower_bound(
            radius_count=100,
            height_count=100,
            selected_count=50,
        ),
    }
    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
            default=lambda value: (
                int(value)
                if isinstance(value, Fraction) and value.denominator == 1
                else str(value)
            ),
        )
    )


if __name__ == "__main__":
    main()
