#!/usr/bin/env python3
"""Finite adversarial search for the high-support weighted A-shell.

Actual systems use all primes in a 451 dyadic offset block.  Synthetic
systems are explicitly labelled general pairwise-coprime offset diagnostics.
No finite output is promoted to an asymptotic statement.
"""

from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import math
from fractions import Fraction


def primes_below(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * n
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(n - 1) + 1):
        if sieve[p]:
            sieve[p * p : n : p] = b"\x00" * (((n - 1 - p * p) // p) + 1)
    return [p for p in range(2, n) if sieve[p]]


def centered(value: int, modulus: int) -> int:
    value %= modulus
    return value if 2 * value <= modulus else value - modulus


def sinc_abs(x: float) -> float:
    if x == 0:
        return 1.0
    return abs(math.sin(x) / x)


def logaddexp(left: float, right: float) -> float:
    if left == -math.inf:
        return right
    if right == -math.inf:
        return left
    top = max(left, right)
    return top + math.log(math.exp(left - top) + math.exp(right - top))


def derivative_inverses(offsets: tuple[int, ...], moduli: tuple[int, ...]) -> tuple[int, ...]:
    answer = []
    for i, (d, p) in enumerate(zip(offsets, moduli)):
        derivative = 1
        for j, other in enumerate(offsets):
            if i != j:
                derivative = derivative * (d - other) % p
        if math.gcd(derivative, p) != 1:
            raise ValueError("F'(d_i) is not a unit")
        answer.append(pow(derivative, -1, p))
    return tuple(answer)


def push_top(heap: list[tuple[float, int, dict[str, object]]], score: float, serial: int,
             row: dict[str, object], keep: int = 6) -> None:
    item = (score, serial, row)
    if len(heap) < keep:
        heapq.heappush(heap, item)
    elif score > heap[0][0]:
        heapq.heapreplace(heap, item)


def exact_top_record(system: dict[str, object], row: dict[str, object]) -> dict[str, object]:
    k = int(system["k"])
    scale = int(system["scale"])
    offsets = tuple(int(x) for x in system["offsets"])
    moduli = tuple(int(x) for x in system["moduli"])
    vector = tuple(int(x) for x in row.pop("_vector"))
    period = math.prod(moduli)
    numerator = sum(z * (period // p) for z, p in zip(vector, moduli))
    assert numerator == int(row["A"])

    e_nodes = tuple(2 * d - 3 * scale for d in offsets)
    base = 2 * k + 3 * scale
    moments = [sum(z * e**m for z, e in zip(vector, e_nodes)) for m in range(min(9, len(vector)))]
    alpha = Fraction(numerator, period)
    leading = Fraction(2 * moments[0], base)
    tail = alpha - leading
    cancellation_ratio = None if not leading else float(abs(tail / leading))
    encoded = ",".join(str(z) for z in vector).encode()
    row.update(
        {
            "exact_numerator_verified": True,
            "minus_log_abs_alpha": math.log(period) - math.log(abs(numerator)),
            "centered_base": base,
            "max_geometric_ratio": max(abs(e) for e in e_nodes) / base,
            "centered_moments_0_to_8": moments,
            "initial_exact_zero_moments": next(
                (i for i, value in enumerate(moments) if value != 0), len(moments)
            ),
            "tail_to_leading_m0_ratio": cancellation_ratio,
            "vector_sha256": hashlib.sha256(encoded).hexdigest(),
            "vector": vector if len(vector) <= 20 else None,
            "vector_l1": sum(abs(z) for z in vector),
            "vector_max_abs": max(abs(z) for z in vector),
        }
    )
    return row


def analyze_system(system: dict[str, object], a_cap: int, smoothing: int, poly_b: int,
                   exponential_c: float, epsilon: float) -> dict[str, object]:
    k = int(system["k"])
    scale = int(system["scale"])
    offsets = tuple(int(x) for x in system["offsets"])
    moduli = tuple(int(x) for x in system["moduli"])
    q = len(moduli)
    b = math.floor((scale - 1) / 2) + 0.5
    inverses = derivative_inverses(offsets, moduli)
    sign = -1 if (q - 1) % 2 else 1
    e_nodes = tuple(2 * d - 3 * scale for d in offsets)
    centered_base = 2 * k + 3 * scale

    local_means = []
    for p in moduli:
        mass = 0.0
        for residue in range(p):
            z = centered(residue, p)
            x = 2 * math.pi * b * z / (smoothing * p)
            mass += sinc_abs(x) ** smoothing
        local_means.append(mass / p)
    log_product_mean = sum(math.log(value) for value in local_means)

    log_period = sum(math.log(p) for p in moduli)
    log_width_product = sum(math.log(d) for d in offsets)
    log_h = poly_b * math.log(k) + q * math.log(exponential_c) + log_period - log_width_product
    log_x = log_width_product - poly_b * math.log(k) - q * math.log(exponential_c)
    available_a = int(math.exp(log_x)) if log_x < math.log(a_cap + 1) else a_cap
    max_a = min(a_cap, max(0, available_a))
    r_epsilon = min(q, math.floor((1 - epsilon) * log_h / math.log(2 * k)))
    h_over_p = math.exp(poly_b * math.log(k) + q * math.log(exponential_c) - log_width_product)

    zero_carries = 0
    high_zero_carries = 0
    serial = 0
    top_joint: list[tuple[float, int, dict[str, object]]] = []
    top_total: list[tuple[float, int, dict[str, object]]] = []
    max_small_coordinates = 0
    carry_histogram: dict[int, int] = {}
    zero_prefix_histogram: dict[int, int] = {}
    longest_positive_zero_prefix: dict[str, object] | None = None
    log_scanned_high_joint_mass = -math.inf
    log_scanned_high_total_mass = -math.inf

    for a_value in range(1, max_a + 1):
        vector = tuple(
            centered(sign * a_value * inverse, p)
            for inverse, p in zip(inverses, moduli)
        )
        alpha_float = sum(z / p for z, p in zip(vector, moduli))
        carry = round(alpha_float)
        carry_histogram[carry] = carry_histogram.get(carry, 0) + 1
        if carry != 0:
            continue
        zero_carries += 1
        sigma = sum(z != 0 for z in vector)
        if sigma <= r_epsilon:
            continue
        high_zero_carries += 1
        prefix = 0
        prefix_moments = []
        for order in range(min(6, q)):
            moment = sum(z * e**order for z, e in zip(vector, e_nodes))
            prefix_moments.append(moment)
            if moment != 0:
                break
            prefix += 1
        zero_prefix_histogram[prefix] = zero_prefix_histogram.get(prefix, 0) + 1
        if prefix and (
            longest_positive_zero_prefix is None
            or prefix > int(longest_positive_zero_prefix["zero_prefix_length"])
        ):
            period = math.prod(moduli)
            numerator = sum(z * (period // p) for z, p in zip(vector, moduli))
            assert numerator == a_value
            longest_positive_zero_prefix = {
                "A": a_value,
                "zero_prefix_length": prefix,
                "first_moments": prefix_moments,
                "centered_base": centered_base,
                "max_geometric_ratio": max(abs(e) for e in e_nodes) / centered_base,
                "vector": vector if q <= 20 else None,
                "vector_sha256": hashlib.sha256(
                    ",".join(str(z) for z in vector).encode()
                ).hexdigest(),
            }
        log_joint = 0.0
        small_coordinates = 0
        shells = []
        for z, p in zip(vector, moduli):
            x = 2 * math.pi * b * z / (smoothing * p)
            value = sinc_abs(x)
            log_joint += smoothing * math.log(max(value, 1e-300))
            natural_scale = p / b
            ratio = abs(z) / natural_scale
            shell = 0 if ratio <= 1 else math.ceil(math.log2(ratio))
            shells.append(shell)
            if ratio <= 1:
                small_coordinates += 1
        max_small_coordinates = max(max_small_coordinates, small_coordinates)
        diagonal = sinc_abs(2 * math.pi * h_over_p * a_value / smoothing) ** smoothing
        log_diagonal = math.log(max(diagonal, 1e-300))
        log_scanned_high_joint_mass = logaddexp(log_scanned_high_joint_mass, log_joint)
        log_scanned_high_total_mass = logaddexp(
            log_scanned_high_total_mass, log_joint + log_diagonal
        )
        row = {
            "A": a_value,
            "sigma": sigma,
            "small_coordinate_count": small_coordinates,
            "coordinate_shell_sum": sum(shells),
            "log_joint_weight": log_joint,
            "log_joint_over_centered_core_residue_mean": log_joint - log_product_mean,
            "log_diagonal_weight": log_diagonal,
            "log_total_weight": log_joint + log_diagonal,
            "_vector": vector,
        }
        serial += 1
        push_top(top_joint, log_joint - log_product_mean, serial, row.copy())
        push_top(top_total, log_joint + log_diagonal, serial, row.copy())

    joint_rows = [exact_top_record(system, item[2]) for item in sorted(top_joint, reverse=True)]
    total_rows = [exact_top_record(system, item[2]) for item in sorted(top_total, reverse=True)]
    return {
        "classification": system["classification"],
        "label": system["label"],
        "k": k,
        "scale": scale,
        "rank": q,
        "offset_range": (min(offsets), max(offsets)),
        "max_A_scanned": max_a,
        "log_P_over_h": log_x,
        "r_epsilon": r_epsilon,
        "zero_carries": zero_carries,
        "high_support_zero_carries": high_zero_carries,
        "zero_carry_fraction": zero_carries / max(1, max_a),
        "max_small_coordinate_count": max_small_coordinates,
        "log_centered_core_residue_product_mean": log_product_mean,
        "carry_histogram": dict(sorted(carry_histogram.items())),
        "zero_prefix_histogram": dict(sorted(zero_prefix_histogram.items())),
        "longest_positive_zero_prefix": longest_positive_zero_prefix,
        "log_scanned_high_joint_mass": log_scanned_high_joint_mass,
        "log_scanned_high_total_mass": log_scanned_high_total_mass,
        "top_normalized_joint_weights": joint_rows,
        "top_total_weights": total_rows,
    }


def compact_row(row: dict[str, object]) -> dict[str, object]:
    """Keep replay output auditable without printing every retained vector."""
    joint = row["top_normalized_joint_weights"]
    total = row["top_total_weights"]

    def compact_top(top: dict[str, object] | None) -> dict[str, object] | None:
        if top is None:
            return None
        moments = top["centered_moments_0_to_8"]
        return {
            key: top[key]
            for key in (
                "A",
                "sigma",
                "small_coordinate_count",
                "coordinate_shell_sum",
                "log_joint_weight",
                "log_joint_over_centered_core_residue_mean",
                "log_diagonal_weight",
                "log_total_weight",
                "minus_log_abs_alpha",
                "max_geometric_ratio",
                "initial_exact_zero_moments",
                "tail_to_leading_m0_ratio",
                "vector_l1",
                "vector_max_abs",
                "vector_sha256",
                "vector",
            )
        } | {
            "centered_moment_m0": moments[0],
            "centered_moment_m1": moments[1] if len(moments) > 1 else None,
        }
    return {
        key: row[key]
        for key in (
            "classification",
            "label",
            "k",
            "scale",
            "rank",
            "offset_range",
            "max_A_scanned",
            "log_P_over_h",
            "r_epsilon",
            "zero_carries",
            "high_support_zero_carries",
            "zero_carry_fraction",
            "max_small_coordinate_count",
            "log_centered_core_residue_product_mean",
            "zero_prefix_histogram",
            "longest_positive_zero_prefix",
            "log_scanned_high_joint_mass",
            "log_scanned_high_total_mass",
        )
    } | {
        "top_normalized_joint_weight": compact_top(joint[0] if joint else None),
        "top_total_weight": compact_top(total[0] if total else None),
    }


def actual_systems(min_k: int, max_k: int, step: int, min_rank: int,
                   max_systems: int) -> list[dict[str, object]]:
    plist = primes_below(2 * max_k)
    candidates = []
    for k in range(min_k, max_k + 1, step):
        blocks: dict[int, list[int]] = {}
        for p in plist:
            if p <= k:
                continue
            if p >= 2 * k:
                break
            d = p - k
            scale = 1 << (d.bit_length() - 1)
            blocks.setdefault(scale, []).append(p)
        for scale, block in blocks.items():
            if len(block) >= min_rank:
                candidates.append(
                    {
                        "classification": "actual_451_prime_block",
                        "label": f"actual-k{k}-D{scale}",
                        "k": k,
                        "scale": scale,
                        "offsets": tuple(p - k for p in block),
                        "moduli": tuple(block),
                    }
                )
    candidates.sort(key=lambda row: (-len(row["moduli"]), row["k"], row["scale"]))
    if len(candidates) <= max_systems:
        return candidates
    # Keep extremes in rank plus an evenly spaced cross-section.
    selected = candidates[: max_systems // 2]
    remainder = candidates[max_systems // 2 :]
    slots = max_systems - len(selected)
    selected.extend(remainder[(i * len(remainder)) // slots] for i in range(slots))
    return selected


def synthetic_system(label: str, offsets: tuple[int, ...], start_k: int) -> dict[str, object]:
    for k in range(start_k, start_k + 20000):
        moduli = tuple(k + d for d in offsets)
        if any(math.gcd(a, b) != 1 for i, a in enumerate(moduli) for b in moduli[i + 1 :]):
            continue
        try:
            derivative_inverses(offsets, moduli)
        except ValueError:
            continue
        return {
            "classification": "synthetic_pairwise_coprime_not_asserted_prime",
            "label": label,
            "k": k,
            "scale": 1 << (min(offsets).bit_length() - 1),
            "offsets": offsets,
            "moduli": moduli,
        }
    raise RuntimeError(f"no coprime realization for {label}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-k", type=int, default=300)
    parser.add_argument("--max-k", type=int, default=3000)
    parser.add_argument("--step", type=int, default=137)
    parser.add_argument("--min-rank", type=int, default=8)
    parser.add_argument("--max-systems", type=int, default=24)
    parser.add_argument("--a-cap", type=int, default=30000)
    parser.add_argument("--smoothing", type=int, default=2)
    parser.add_argument("--poly-b", type=int, default=2)
    parser.add_argument("--exponential-c", type=float, default=6.0)
    parser.add_argument("--epsilon", type=float, default=0.25)
    parser.add_argument("--aggregate-only", action="store_true")
    args = parser.parse_args()

    systems = actual_systems(
        args.min_k, args.max_k, args.step, args.min_rank, args.max_systems
    )
    systems.extend(
        [
            synthetic_system(
                "synthetic-arithmetic-step-210",
                tuple(2049 + 210 * j for j in range(8)),
                10000,
            ),
            synthetic_system(
                "synthetic-two-cluster-step-210",
                tuple(2049 + 210 * j for j in (0, 1, 2, 3, 6, 7, 8, 9)),
                10000,
            ),
            synthetic_system(
                "synthetic-irregular-step-210",
                tuple(2049 + 210 * j for j in (0, 1, 2, 4, 5, 7, 8, 9)),
                10000,
            ),
        ]
    )
    rows = [
        analyze_system(
            system,
            args.a_cap,
            args.smoothing,
            args.poly_b,
            args.exponential_c,
            args.epsilon,
        )
        for system in systems
    ]
    compact = [compact_row(row) for row in rows]
    usable = [row for row in compact if row["high_support_zero_carries"]]
    if args.aggregate_only:
        actual = [row for row in compact if row["classification"].startswith("actual")]
        synthetic = [row for row in compact if row["classification"].startswith("synthetic")]

        def extremum(group: list[dict[str, object]], field: str, *, top_field: str | None = None):
            if not group:
                return None
            if top_field is None:
                row = max(group, key=lambda item: item[field])
                value = row[field]
            else:
                row = max(group, key=lambda item: item[field][top_field])
                value = row[field][top_field]
            return {"label": row["label"], "rank": row["rank"], "value": value}

        combined_prefix: dict[int, int] = {}
        for row in actual:
            for prefix, count in row["zero_prefix_histogram"].items():
                prefix = int(prefix)
                combined_prefix[prefix] = combined_prefix.get(prefix, 0) + int(count)
        longest = max(
            (row for row in actual if row["longest_positive_zero_prefix"] is not None),
            key=lambda row: row["longest_positive_zero_prefix"]["zero_prefix_length"],
            default=None,
        )
        payload = {
            "classification": "finite_weighted_A_shell_falsification_only",
            "parameters": vars(args),
            "systems": len(rows),
            "actual_systems": len(actual),
            "synthetic_systems": len(synthetic),
            "actual_rank_range": [
                min(row["rank"] for row in actual),
                max(row["rank"] for row in actual),
            ] if actual else None,
            "actual_combined_zero_prefix_histogram": dict(sorted(combined_prefix.items())),
            "actual_longest_zero_prefix_example": None if longest is None else {
                "label": longest["label"],
                "rank": longest["rank"],
                "example": longest["longest_positive_zero_prefix"],
            },
            "max_actual_log_normalized_joint": extremum(
                actual,
                "top_normalized_joint_weight",
                top_field="log_joint_over_centered_core_residue_mean",
            ),
            "max_synthetic_log_normalized_joint": extremum(
                synthetic,
                "top_normalized_joint_weight",
                top_field="log_joint_over_centered_core_residue_mean",
            ),
            "max_actual_log_scanned_high_total_mass": extremum(
                actual, "log_scanned_high_total_mass"
            ),
            "max_synthetic_log_scanned_high_total_mass": extremum(
                synthetic, "log_scanned_high_total_mass"
            ),
            "systems_with_normalized_joint_above_one": sum(
                row["top_normalized_joint_weight"] is not None
                and row["top_normalized_joint_weight"][
                    "log_joint_over_centered_core_residue_mean"
                ] > 0
                for row in compact
            ),
        }
    else:
        payload = {
                "classification": "finite_weighted_A_shell_falsification_only",
                "parameters": vars(args),
                "systems": len(rows),
                "actual_systems": sum(row["classification"].startswith("actual") for row in rows),
                "synthetic_systems": sum(row["classification"].startswith("synthetic") for row in rows),
                "largest_normalized_joint": sorted(
                    usable,
                    key=lambda row: row["top_normalized_joint_weight"][
                        "log_joint_over_centered_core_residue_mean"
                    ],
                    reverse=True,
                )[:8],
                "largest_total_weight": sorted(
                    usable,
                    key=lambda row: row["top_total_weight"]["log_total_weight"],
                    reverse=True,
                )[:8],
                "rows": compact,
                "actual_positive_zero_prefix_examples": [
                    {
                        "label": row["label"],
                        "rank": row["rank"],
                        "example": row["longest_positive_zero_prefix"],
                    }
                    for row in compact
                    if row["classification"].startswith("actual")
                    and row["longest_positive_zero_prefix"] is not None
                ],
                "systems_with_normalized_joint_above_one": sum(
                    row["top_normalized_joint_weight"] is not None
                    and row["top_normalized_joint_weight"][
                        "log_joint_over_centered_core_residue_mean"
                    ] > 0
                    for row in compact
                ),
            }
    print(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
