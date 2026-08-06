#!/usr/bin/env python3
"""Float Bernstein scan of the second PNL Newton fan."""

from __future__ import annotations

import argparse
from fractions import Fraction
from math import comb, lcm
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from explore_opg_round7_pnl_a_root_accumulation import (  # noqa: E402
    LOCAL_SLOTS,
    centered_chart,
    face_record,
)
from search_opg_round7_rlp_bernstein_boxes import split_axis  # noqa: E402
from verify_negative_c_direct_chambers import bernstein_transform  # noqa: E402
from verify_negative_page_direct_chambers import digest  # noqa: E402
from verify_pnl_double_corner_blowup import radial_projective_chart  # noqa: E402


NAMES = {
    "r": 0,
    "z": 2,
    "ratio1def": 1,
    "H": 4,
    "ratio2def": 5,
    "edef": 6,
    "d": 7,
}


def float_bernstein_tensor(poly, slots):
    shape = tuple(max(m[slot] for m in poly) + 1 for slot in slots)
    tensor = np.zeros(shape)
    for monomial, value in poly.items():
        tensor[tuple(monomial[slot] for slot in slots)] = float(value)
    for axis, degree_plus_one in enumerate(shape):
        degree = degree_plus_one - 1
        transform = np.zeros((degree_plus_one, degree_plus_one))
        for index in range(degree_plus_one):
            for power in range(index + 1):
                transform[index, power] = comb(index, power) / comb(degree, power)
        moved = np.moveaxis(tensor, axis, 0)
        moved = np.tensordot(transform, moved, axes=(1, 0))
        tensor = np.moveaxis(moved, 0, axis)
    return tensor


def exact_control(poly, slots, index):
    degrees = [max(m[slot] for m in poly) for slot in slots]
    value = Fraction()
    for monomial, coefficient in poly.items():
        powers = [monomial[slot] for slot in slots]
        if any(power > target for power, target in zip(powers, index)):
            continue
        weight = Fraction(1)
        for target, power, degree in zip(index, powers, degrees):
            weight *= Fraction(comb(target, power), comb(degree, power))
        value += coefficient * weight
    return value


def integer_scale_stats(poly, slots):
    degrees = [max(m[slot] for m in poly) for slot in slots]
    common_denominator = 1
    normalized = []
    for monomial, coefficient in poly.items():
        denominator_weight = 1
        for slot, degree in zip(slots, degrees):
            denominator_weight *= comb(degree, monomial[slot])
        value = coefficient / denominator_weight
        normalized.append((monomial, value))
        common_denominator = lcm(common_denominator, value.denominator)
    maximum_scaled_bits = 0
    absolute_endpoint_bound = 0
    for monomial, value in normalized:
        scaled = int(value * common_denominator)
        maximum_scaled_bits = max(maximum_scaled_bits, abs(scaled).bit_length())
        binomial_weight = 1
        for slot, degree in zip(slots, degrees):
            binomial_weight *= comb(degree, monomial[slot])
        absolute_endpoint_bound += abs(scaled) * binomial_weight
    print(
        "integer_scale", "denominator_bits", common_denominator.bit_length(),
        "maximum_scaled_bits", maximum_scaled_bits,
        "absolute_endpoint_bound_bits", absolute_endpoint_bound.bit_length(),
        "degrees", degrees,
        flush=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--side", choices=("below", "above"), required=True)
    parser.add_argument("--maximum", choices=tuple(NAMES), required=True)
    parser.add_argument("--scale-stats-only", action="store_true")
    parser.add_argument("--exact", action="store_true")
    parser.add_argument("--candidate-count", type=int, default=20)
    parser.add_argument("--chain-axis", type=int)
    parser.add_argument("--chain-direction", choices=("left", "right"), default="right")
    parser.add_argument("--chain-depth", type=int, default=12)
    args = parser.parse_args()

    centered = centered_chart(args.side)
    order, _ = face_record(centered)
    maximum_slot = NAMES[args.maximum]
    radial = radial_projective_chart(centered, LOCAL_SLOTS, maximum_slot, order)
    slots = (maximum_slot, *(slot for slot in LOCAL_SLOTS if slot != maximum_slot))
    if args.scale_stats_only:
        integer_scale_stats(radial, slots)
        return
    if args.exact:
        controls = bernstein_transform(radial, list(slots))
        print(
            "exact", "side", args.side, "maximum", args.maximum,
            "slots", slots, "nonzero", len(controls),
            "negative", sum(value < 0 for value in controls.values()),
            "minimum_nonzero", min(controls.values()),
            "maximum", max(controls.values()),
            "sha256", digest(controls),
            flush=True,
        )
        return
    controls = float_bernstein_tensor(radial, slots)
    scale = max(1.0, float(np.max(np.abs(controls))))
    tolerance = 1e-12 * scale
    negative = np.argwhere(controls < -tolerance)
    print(
        "side", args.side, "maximum", args.maximum, "slots", slots,
        "shape", controls.shape, "scale", scale, "negative", len(negative),
        "minimum_scaled", float(np.min(controls)) / scale,
        flush=True,
    )
    for axis, slot in enumerate(slots):
        if not len(negative):
            break
        values, counts = np.unique(negative[:, axis], return_counts=True)
        histogram = ",".join(f"{int(v)}:{int(c)}" for v, c in zip(values, counts))
        print("negative_axis", axis, "slot", slot, histogram, flush=True)
    if args.chain_axis is not None:
        tensor = controls
        for depth in range(1, args.chain_depth + 1):
            left, right = split_axis(tensor, args.chain_axis)
            child_rows = []
            for child in (left, right):
                child_scale = max(1.0, float(np.max(np.abs(child))))
                child_rows.append((
                    int(np.sum(child < -1e-12 * child_scale)),
                    float(np.min(child)) / child_scale,
                ))
            print(
                "chain", depth, "axis", args.chain_axis,
                "left", child_rows[0], "right", child_rows[1],
                flush=True,
            )
            tensor = left if args.chain_direction == "left" else right
    flat = controls.ravel()
    count = min(args.candidate_count, flat.size)
    if not count:
        return
    candidates = np.argpartition(flat, count - 1)[:count]
    candidates = candidates[np.argsort(flat[candidates])]
    for flat_index in candidates:
        index = tuple(int(item) for item in np.unravel_index(flat_index, controls.shape))
        print(
            "minimum_candidate", index, float(flat[flat_index]),
            "exact", exact_control(radial, slots, index),
            flush=True,
        )


if __name__ == "__main__":
    main()
