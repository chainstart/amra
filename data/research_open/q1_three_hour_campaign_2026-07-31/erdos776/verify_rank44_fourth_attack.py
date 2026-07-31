#!/usr/bin/env python3
"""Independent exact guard and optional deep scan for #776 round four.

The symbolic implications are proved in FOURTH_ATTACK.md.  Parameter scans
remain computational falsifier searches, even when every integer in the
displayed finite interval is checked.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from fractions import Fraction
from math import comb, sqrt
from multiprocessing import get_context
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ENGINE_PATH = (
    ROOT
    / "artifacts"
    / "erdos_master_rotation"
    / "R002"
    / "core_776_635"
    / "776"
    / "verify_rank5_rotation.py"
)


def load_engine():
    spec = importlib.util.spec_from_file_location("r002_rank5", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(ENGINE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical(number: int, rank: int) -> list[tuple[int, int]]:
    """Independent ordinary greedy Macaulay expansion."""
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    result: list[tuple[int, int]] = []
    remaining = number
    cap: int | None = None
    for lower in range(rank, 0, -1):
        if remaining == 0:
            break
        low = lower - 1
        high = cap if cap is not None else max(lower + 1, 2 * lower)
        if cap is None:
            while comb(high, lower) <= remaining:
                high *= 2
        while low + 1 < high:
            middle = (low + high) // 2
            if comb(middle, lower) <= remaining:
                low = middle
            else:
                high = middle
        upper = low if cap is None else min(low, cap - 1)
        while upper >= lower and comb(upper, lower) > remaining:
            upper -= 1
        if upper >= lower:
            result.append((upper, lower))
            remaining -= comb(upper, lower)
            cap = upper
    if remaining:
        raise AssertionError((number, rank, result, remaining))
    return result


def kk(number: int, rank: int) -> int:
    return sum(
        comb(upper, lower - 1)
        for upper, lower in canonical(number, rank)
    )


def upper_raise(number: int, rank: int) -> int:
    return sum(
        comb(upper, lower + 1)
        for upper, lower in canonical(number, rank)
    )


def ordinary_state(parameter: int, target_rank: int) -> int:
    rank = parameter - 12
    value = 0
    while rank > target_rank:
        value = parameter + kk(value, rank)
        rank -= 1
    return value


def compressed_states(engine, parameter: int) -> dict[int, tuple[int, list]]:
    rank = parameter - 12
    runs = []
    result: dict[int, tuple[int, list]] = {}
    while rank >= 43:
        if rank in {248, 59, 46, 45, 44, 43}:
            result[rank] = (engine.runs_value(runs), list(runs))
        if rank == 43:
            break
        runs = engine.defect_step(runs, rank, parameter)
        rank -= 1
    return result


def j44(parameter: int) -> int:
    return (
        comb(parameter - 12, 44)
        + sum(
            comb(parameter - 57 + lower, lower)
            for lower in range(31, 44)
        )
        + sum(
            comb(parameter - 58 + lower, lower)
            for lower in range(3, 31)
        )
    )


def j43(parameter: int) -> int:
    return (
        comb(parameter - 12, 43)
        + sum(
            comb(parameter - 56 + lower, lower)
            for lower in range(30, 43)
        )
        + sum(
            comb(parameter - 57 + lower, lower)
            for lower in range(2, 30)
        )
    )


def j45(parameter: int) -> int:
    return (
        comb(parameter - 12, 45)
        + sum(
            comb(parameter - 58 + lower, lower)
            for lower in range(32, 45)
        )
        + sum(
            comb(parameter - 59 + lower, lower)
            for lower in range(4, 32)
        )
    )


def j46(parameter: int) -> int:
    return (
        comb(parameter - 12, 46)
        + sum(
            comb(parameter - 59 + lower, lower)
            for lower in range(33, 46)
        )
        + sum(
            comb(parameter - 60 + lower, lower)
            for lower in range(5, 33)
        )
    )


def moving_h(parameter: int, residual_rank: int) -> int:
    rank = residual_rank + 15
    return comb(parameter - 12, rank) + sum(
        comb(parameter - 28 + index, residual_rank + index)
        for index in range(1, 15)
    )


def expand_runs(runs: list[tuple[int, int, int]]) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    for high, low, offset in runs:
        result.extend(
            (lower + offset, lower)
            for lower in range(high, low - 1, -1)
        )
    return result


def expected_rank44_template(
    engine,
    parameter: int,
    residual: int,
) -> list[tuple[int, int]]:
    result = [(parameter - 12, 44)]
    result.extend(
        (parameter - 57 + lower, lower)
        for lower in range(43, 30, -1)
    )
    result.extend(
        (parameter - 58 + lower, lower)
        for lower in range(30, 2, -1)
    )
    result.extend(engine.canonical(residual, 2))
    return result


def expected_rank45_template(
    engine,
    parameter: int,
    residual: int,
) -> list[tuple[int, int]]:
    result = [(parameter - 12, 45)]
    result.extend(
        (parameter - 58 + lower, lower)
        for lower in range(44, 31, -1)
    )
    result.extend(
        (parameter - 59 + lower, lower)
        for lower in range(31, 3, -1)
    )
    result.extend(engine.canonical(residual, 3))
    return result


def expected_rank46_template(
    engine,
    parameter: int,
    residual: int,
) -> list[tuple[int, int]]:
    result = [(parameter - 12, 46)]
    result.extend(
        (parameter - 59 + lower, lower)
        for lower in range(45, 32, -1)
    )
    result.extend(
        (parameter - 60 + lower, lower)
        for lower in range(32, 4, -1)
    )
    result.extend(engine.canonical(residual, 4))
    return result


def diagonal_row(engine, parameter: int) -> dict[str, int]:
    current = compressed_states(engine, parameter)
    following = compressed_states(engine, parameter + 1)
    d43 = current[43][0]
    d44 = current[44][0]
    next_d44 = following[44][0]
    next_d45 = following[45][0]

    residual = d44 - j44(parameter)
    next_residual = next_d44 - j44(parameter + 1)
    suspension = d44 + upper_raise(d44, 44)
    gap = suspension - next_d45
    assert gap >= 0
    total_shadow = kk(suspension, 45)
    loss = total_shadow - kk(suspension - gap, 45)
    required_loss = d43 - j43(parameter) - 6

    assert next_d44 - d44 == d43 + 1 - loss
    assert next_residual - residual == d43 - j43(parameter) + 1 - loss

    galois_requirement = max(0, required_loss)
    gap_threshold = 0
    if galois_requirement:
        gap_threshold = suspension - upper_raise(
            total_shadow - galois_requirement,
            44,
        )
        assert (loss >= galois_requirement) == (gap >= gap_threshold)

    simplified_threshold = None
    if parameter - 6 <= residual < comb(parameter - 55, 2):
        simplified_threshold = (
            residual
            + upper_raise(residual, 2)
            - upper_raise(residual - parameter + 6, 2)
        )
        assert simplified_threshold == gap_threshold

    return {
        "V": parameter,
        "R2": residual,
        "R2_next": next_residual,
        "R2_jump": next_residual - residual,
        "G45": gap,
        "G45_threshold": gap_threshold,
        "G45_surplus": gap - gap_threshold,
        "L45": loss,
        "L45_required": required_loss,
        "L45_surplus": loss - required_loss,
        "simplified_threshold": simplified_threshold or 0,
    }


def rank45_row(engine, parameter: int) -> dict[str, object]:
    states = compressed_states(engine, parameter)
    value, runs = states[45]
    residual = value - j45(parameter)
    template = expand_runs(runs) == expected_rank45_template(
        engine,
        parameter,
        residual,
    )
    return {
        "V": parameter,
        "Z3": residual,
        "Z3_minus_108V": residual - 108 * parameter,
        "109V_minus_Z3": 109 * parameter - residual,
        "template": template,
    }


def rank46_row(engine, parameter: int) -> dict[str, object]:
    states = compressed_states(engine, parameter)
    value, runs = states[46]
    residual = value - j46(parameter)
    template = expand_runs(runs) == expected_rank46_template(
        engine,
        parameter,
        residual,
    )
    return {
        "V": parameter,
        "Z4": residual,
        "Z4_minus_affine_gate": residual - (2 * parameter + 424_222),
        "Z4_minus_loose_affine_gate": (
            residual - (458 * parameter + 292_894)
        ),
        "Z4_minus_anchor_slope_one": residual - (parameter + 424_510),
        "template": template,
    }


def rank45_finite_scan(engine, limit: int) -> dict[str, object]:
    """Exact finite falsifier scan for the rank-45 and rank-46 gates."""
    best_ratio: tuple[int, int] | None = None
    worst_margin: tuple[int, int, int] | None = None
    rank45_template_failures: list[int] = []
    worst_rank46: tuple[int, int, int] | None = None
    worst_rank46_loose: tuple[int, int, int] | None = None
    first_slope_one_failure: tuple[int, int, int] | None = None
    rank46_template_failures: list[int] = []
    minimum_rank59_margin: tuple[int, int] | None = None
    for parameter in range(288, limit + 1):
        states = compressed_states(engine, parameter)
        rank45_value, rank45_runs = states[45]
        residual = rank45_value - j45(parameter)
        if best_ratio is None or (
            residual * best_ratio[0] > best_ratio[1] * parameter
        ):
            best_ratio = (parameter, residual)
        margin = residual - 109 * parameter
        if worst_margin is None or margin > worst_margin[1]:
            worst_margin = (parameter, margin, residual)
        if expand_runs(rank45_runs) != expected_rank45_template(
            engine,
            parameter,
            residual,
        ):
            rank45_template_failures.append(parameter)

        rank46_value, rank46_runs = states[46]
        rank46_residual = rank46_value - j46(parameter)
        rank46_excess = rank46_residual - (2 * parameter + 424_222)
        if worst_rank46 is None or rank46_excess > worst_rank46[1]:
            worst_rank46 = (parameter, rank46_excess, rank46_residual)
        rank46_loose_excess = (
            rank46_residual - (458 * parameter + 292_894)
        )
        if (
            worst_rank46_loose is None
            or rank46_loose_excess > worst_rank46_loose[1]
        ):
            worst_rank46_loose = (
                parameter,
                rank46_loose_excess,
                rank46_residual,
            )
        slope_one_excess = rank46_residual - (parameter + 424_510)
        if first_slope_one_failure is None and slope_one_excess > 0:
            first_slope_one_failure = (
                parameter,
                slope_one_excess,
                rank46_residual,
            )
        if expand_runs(rank46_runs) != expected_rank46_template(
            engine,
            parameter,
            rank46_residual,
        ):
            rank46_template_failures.append(parameter)

        rank59_margin = (
            moving_h(parameter, 44) - states[59][0]
        )
        if (
            minimum_rank59_margin is None
            or rank59_margin < minimum_rank59_margin[1]
        ):
            minimum_rank59_margin = (parameter, rank59_margin)
    return {
        "range": [288, limit],
        "rank45_best_ratio": best_ratio,
        "rank45_worst_Z3_minus_109V": worst_margin,
        "rank45_template_failures": rank45_template_failures,
        "rank46_worst_Z4_minus_affine_gate": worst_rank46,
        "rank46_worst_Z4_minus_loose_affine_gate": worst_rank46_loose,
        "rank46_first_anchor_slope_one_failure": first_slope_one_failure,
        "rank46_template_failures": rank46_template_failures,
        "minimum_H59_minus_D59": minimum_rank59_margin,
    }


def scan_chunk(bounds: tuple[int, int]) -> dict[str, object]:
    start, stop = bounds
    engine = load_engine()
    best_ratio: tuple[int, int] | None = None
    worst_seven: tuple[int, int, int] | None = None
    max_jump: tuple[int, int, int, int] | None = None
    min_jump: tuple[int, int, int, int] | None = None
    first: tuple[int, int] | None = None
    last: tuple[int, int] | None = None
    previous: int | None = None
    template_failures: list[int] = []

    for parameter in range(start, stop):
        states = compressed_states(engine, parameter)
        value, runs = states[44]
        residual = value - j44(parameter)
        if best_ratio is None or (
            residual * best_ratio[0]
            > best_ratio[1] * parameter
        ):
            best_ratio = (parameter, residual)
        excess = residual - 7 * parameter
        if worst_seven is None or excess > worst_seven[1]:
            worst_seven = (parameter, excess, residual)
        if expand_runs(runs) != expected_rank44_template(
            engine,
            parameter,
            residual,
        ):
            template_failures.append(parameter)
        if previous is None:
            first = (parameter, residual)
        else:
            jump = residual - previous
            row = (parameter - 1, jump, previous, residual)
            if max_jump is None or jump > max_jump[1]:
                max_jump = row
            if min_jump is None or jump < min_jump[1]:
                min_jump = row
        previous = residual
        last = (parameter, residual)

    return {
        "range": [start, stop - 1],
        "best_ratio": best_ratio,
        "worst_R2_minus_7V": worst_seven,
        "max_jump": max_jump,
        "min_jump": min_jump,
        "first": first,
        "last": last,
        "template_failures": template_failures,
    }


def combine_scans(rows: list[dict[str, object]]) -> dict[str, object]:
    rows.sort(key=lambda row: int(row["range"][0]))  # type: ignore[index]
    best: tuple[int, int] | None = None
    worst: tuple[int, int, int] | None = None
    maximum: tuple[int, int, int, int] | None = None
    minimum: tuple[int, int, int, int] | None = None
    failures: list[int] = []
    previous_last: tuple[int, int] | None = None

    for row in rows:
        candidate = tuple(row["best_ratio"])  # type: ignore[arg-type]
        if best is None or candidate[1] * best[0] > best[1] * candidate[0]:
            best = candidate  # type: ignore[assignment]
        candidate_worst = tuple(row["worst_R2_minus_7V"])  # type: ignore[arg-type]
        if worst is None or candidate_worst[1] > worst[1]:
            worst = candidate_worst  # type: ignore[assignment]
        for key, is_maximum in (("max_jump", True), ("min_jump", False)):
            item = row[key]
            if item is None:
                continue
            jump_row = tuple(item)  # type: ignore[arg-type]
            if is_maximum and (maximum is None or jump_row[1] > maximum[1]):
                maximum = jump_row  # type: ignore[assignment]
            if not is_maximum and (minimum is None or jump_row[1] < minimum[1]):
                minimum = jump_row  # type: ignore[assignment]
        first = tuple(row["first"])  # type: ignore[arg-type]
        if previous_last is not None:
            boundary = (
                previous_last[0],
                first[1] - previous_last[1],
                previous_last[1],
                first[1],
            )
            if maximum is None or boundary[1] > maximum[1]:
                maximum = boundary
            if minimum is None or boundary[1] < minimum[1]:
                minimum = boundary
        previous_last = tuple(row["last"])  # type: ignore[arg-type,assignment]
        failures.extend(row["template_failures"])  # type: ignore[arg-type]

    return {
        "range": [rows[0]["range"][0], rows[-1]["range"][1]],  # type: ignore[index]
        "best_ratio": best,
        "worst_R2_minus_7V": worst,
        "max_jump": maximum,
        "min_jump": minimum,
        "last": previous_last,
        "template_failures": failures,
    }


def run_parallel_scan(limit: int, workers: int) -> dict[str, object]:
    start = 288
    stop = limit + 1
    boundaries = [
        round(sqrt(start * start + index * (stop * stop - start * start) / workers))
        for index in range(workers + 1)
    ]
    boundaries[0] = start
    boundaries[-1] = stop
    chunks = [
        (boundaries[index], boundaries[index + 1])
        for index in range(workers)
        if boundaries[index] < boundaries[index + 1]
    ]
    with get_context("fork").Pool(len(chunks)) as pool:
        rows = list(pool.imap_unordered(scan_chunk, chunks))
    return combine_scans(rows)


def slope_lemma_regression() -> dict[str, int]:
    start = comb(58, 3)
    stop = comb(65, 3)
    minimum_margin: tuple[int, int] | None = None
    for value in range(start, stop + 1):
        margin = 6 * value - 109 * kk(value, 3)
        assert margin > 0
        if minimum_margin is None or margin < minimum_margin[1]:
            minimum_margin = (value, margin)
    assert minimum_margin is not None
    return {
        "checked_x_start": start,
        "checked_x_stop": stop,
        "minimum_6x_minus_109KK3x": minimum_margin[1],
        "minimum_at_x": minimum_margin[0],
    }


def affine_lift_regression() -> dict[str, int]:
    """Check the exact constants used by the two affine lift lemmas."""
    base = 288
    rank2_input = 6 * base - 46
    rank3_gate = 109 * base - 130
    assert canonical(rank2_input, 2) == [(58, 2), (29, 1)]
    assert upper_raise(rank2_input, 2) == rank3_gate

    # The proof splits at the leading rank-two index a=58 versus a>=59.
    leading_at_58 = comb(58, 2) * (2 * 58 - 113)
    tail_at_29 = 29 * (3 * 29 - 112)
    assert leading_at_58 + tail_at_29 == 4_234
    assert comb(59, 2) * (2 * 59 - 113) - 1_045 > 4_234

    rank3_input = 108 * base - 130
    rank4_gate = 2 * base + 424_222
    rank4_cap = upper_raise(rank3_input, 3)
    assert rank4_cap == 424_803
    assert rank4_cap - rank4_gate == 5
    assert upper_raise(108, 3) == 164
    assert upper_raise(108, 2) == 458

    # Finite regression only; the markdown proves the unbounded statements.
    for parameter in [288, 289, 379, 1_000, 10_000, 10**6]:
        assert kk(109 * parameter - 130, 3) <= 6 * parameter - 46
        assert (
            2 * parameter + 424_222
            <= upper_raise(108 * parameter - 130, 3)
        )
        assert (
            458 * parameter + 292_894
            <= upper_raise(108 * parameter - 130, 3)
        )
        if parameter > 288:
            previous = 108 * (parameter - 1) - 130
            assert (
                upper_raise(previous + 108, 3)
                - upper_raise(previous, 3)
                >= 458
            )
    return {
        "base": base,
        "rank3_gate_at_base": rank3_gate,
        "rank4_gate_at_base": rank4_gate,
        "rank4_cap_at_base": rank4_cap,
        "U3_of_108": upper_raise(108, 3),
        "U2_of_108": upper_raise(108, 2),
    }


def ceiling_fraction(value: Fraction) -> int:
    return (
        value.numerator + value.denominator - 1
    ) // value.denominator


def entry_certificate(top_rank: int) -> dict[str, object]:
    """Exact fixed-depth subadditive certificate at the base V=288."""
    base = 288
    constants: dict[int, Fraction] = {top_rank: Fraction(1)}
    for rank in range(top_rank, 3, -1):
        block = ceiling_fraction(constants[rank] * base)
        constants[rank - 1] = (
            Fraction(1)
            + Fraction(2 * kk(block, rank), base)
        )

    margins = [
        (
            comb(base - 27, rank)
            - ceiling_fraction(constants[rank] * base),
            rank,
        )
        for rank in range(3, top_rank + 1)
    ]
    minimum = min(margins)
    return {
        "top_rank": top_rank,
        "K3": str(constants[3]),
        "minimum_base_margin": minimum[0],
        "minimum_margin_rank": minimum[1],
        "passes": minimum[0] > 0,
    }


def extended_entry_gate_regression() -> dict[str, object]:
    rank43 = entry_certificate(43)
    rank44 = entry_certificate(44)
    assert rank43 == {
        "top_rank": 43,
        "K3": "167965/18",
        "minimum_base_margin": 241_850,
        "minimum_margin_rank": 3,
        "passes": True,
    }
    assert rank44 == {
        "top_rank": 44,
        "K3": "1499497/144",
        "minimum_base_margin": -69_704,
        "minimum_margin_rank": 3,
        "passes": False,
    }
    return {
        "proved_uniform_entry_gate": rank43,
        "first_failed_same_certificate": rank44,
        "equivalent_open_fixed_rank_target": "D59(V)<H59(V)",
    }


def remainder_entry_certificate(top_rank: int) -> dict[str, object]:
    """Quotient-remainder subadditive certificate for every V>=288."""
    base = 288
    constants: dict[int, Fraction] = {top_rank: Fraction(1)}
    for rank in range(top_rank, 3, -1):
        current = constants[rank]
        block = ceiling_fraction(current * base)
        block_shadow = kk(block, rank)
        best = Fraction(block_shadow, base)
        for remainder in range(1, base):
            tail = ceiling_fraction(current * remainder)
            tail_shadow = kk(tail, rank)
            candidate = Fraction(
                block_shadow + tail_shadow,
                base + remainder,
            )
            if candidate > best:
                best = candidate
        constants[rank - 1] = Fraction(1) + best

    margins = [
        (
            comb(base - 27, rank)
            - ceiling_fraction(constants[rank] * base),
            rank,
        )
        for rank in range(3, top_rank + 1)
    ]
    minimum = min(margins)
    return {
        "top_rank": top_rank,
        "K3": str(constants[3]),
        "ceil_288K3": ceiling_fraction(constants[3] * base),
        "minimum_base_margin": minimum[0],
        "minimum_margin_rank": minimum[1],
        "passes": minimum[0] > 0,
        "transition_count": top_rank - 3,
        "remainders_per_transition": base,
    }


def remainder_entry_gate_regression(
    check_failed_boundary: bool,
) -> dict[str, object]:
    rank233 = remainder_entry_certificate(233)
    assert rank233 == {
        "top_rank": 233,
        "K3": "903709/89",
        "ceil_288K3": 2_924_362,
        "minimum_base_margin": 4_928,
        "minimum_margin_rank": 3,
        "passes": True,
        "transition_count": 230,
        "remainders_per_transition": 288,
    }
    result = {
        "proved_uniform_entry_gate": rank233,
        "equivalent_open_fixed_rank_target": "D248(V)<H248(V)",
    }
    if check_failed_boundary:
        rank234 = remainder_entry_certificate(234)
        assert rank234 == {
            "top_rank": 234,
            "K3": "3629632/353",
            "ceil_288K3": 2_961_287,
            "minimum_base_margin": -31_997,
            "minimum_margin_rank": 3,
            "passes": False,
            "transition_count": 231,
            "remainders_per_transition": 288,
        }
        result["first_failed_same_certificate"] = rank234
    return result


def sparse_row(engine, parameter: int) -> dict[str, object]:
    states = compressed_states(engine, parameter)
    value, runs = states[44]
    residual = value - j44(parameter)
    return {
        "V": parameter,
        "R2": residual,
        "R2_minus_7V": residual - 7 * parameter,
        "template": expand_runs(runs) == expected_rank44_template(
            engine,
            parameter,
            residual,
        ),
    }


def residual_only_reverse_anchor() -> dict[str, int]:
    """Reproduce the exact anchor obstruction to the scalar reverse route."""
    parameter = 288
    value = upper_raise(6 * parameter, 2)
    states = {3: value}
    for rank in range(3, 57):
        if value < parameter:
            raise AssertionError((rank, value, parameter))
        value = upper_raise(value - parameter, rank)
        states[rank + 1] = value
    assert states[56] == 1_549
    assert states[57] == 29
    assert states[56] >= parameter > states[57]
    return {
        "V": parameter,
        "B56": states[56],
        "B57": states[57],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan-limit", type=int, default=1_000)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--deep", action="store_true")
    args = parser.parse_args()
    if args.deep:
        args.scan_limit = 20_000
        args.workers = max(args.workers, 8)

    engine = load_engine()

    # Ordinary and compressed arithmetic are independent implementations.
    crosschecks = []
    for parameter in [100, 128, 288, 379]:
        ordinary = ordinary_state(parameter, 44)
        compressed = compressed_states(engine, parameter)[44][0]
        assert ordinary == compressed
        crosschecks.append(parameter)

    # Pure binomial identities used by the adjacent theorem.
    for parameter in [288, 379, 1_000, 17_423]:
        assert j44(parameter + 1) - j44(parameter) == j43(parameter)

    diagonal_rows = [
        diagonal_row(engine, parameter)
        for parameter in [288, 379, 1_000, 1_361, 6_329, 10_000, 17_423]
    ]
    expected_jumps = {
        288: 2,
        379: 1,
        1_000: 1,
        1_361: 3,
        6_329: 1,
        10_000: 1,
        17_423: 5,
    }
    assert {
        row["V"]: row["R2_jump"] for row in diagonal_rows
    } == expected_jumps
    assert all(row["L45_surplus"] >= 2 for row in diagonal_rows)

    rank45_rows = [
        rank45_row(engine, parameter)
        for parameter in [288, 379, 1_000, 6_329, 10_000]
    ]
    assert rank45_rows[0]["Z3"] == 31_262
    assert rank45_rows[0]["Z3_minus_108V"] == 158
    assert rank45_rows[0]["109V_minus_Z3"] == 130
    assert all(bool(row["template"]) for row in rank45_rows)

    rank46_rows = [
        rank46_row(engine, parameter)
        for parameter in [288, 290, 1_000, 10_000, 100_000]
    ]
    assert rank46_rows[0]["Z4"] == 424_798
    assert rank46_rows[0]["Z4_minus_affine_gate"] == 0
    assert rank46_rows[0]["Z4_minus_loose_affine_gate"] == 0
    assert rank46_rows[1]["Z4_minus_anchor_slope_one"] == 1
    assert all(bool(row["template"]) for row in rank46_rows)

    rank248_rows = []
    for parameter in [288, 379, 1_000]:
        margin = (
            moving_h(parameter, 233)
            - compressed_states(engine, parameter)[248][0]
        )
        assert margin > 0
        rank248_rows.append(
            {
                "V": parameter,
                "H248_minus_D248": margin,
            }
        )

    rank45_scan_limit = 2_000 if args.deep else min(args.scan_limit, 1_000)
    rank45_scan = rank45_finite_scan(engine, rank45_scan_limit)
    assert not rank45_scan["rank45_template_failures"]
    assert not rank45_scan["rank46_template_failures"]
    assert rank45_scan["rank45_worst_Z3_minus_109V"][1] < 0  # type: ignore[index]
    assert rank45_scan["rank46_worst_Z4_minus_affine_gate"][1] <= 0  # type: ignore[index]
    assert rank45_scan["rank46_worst_Z4_minus_loose_affine_gate"][1] <= 0  # type: ignore[index]
    assert rank45_scan["minimum_H59_minus_D59"][1] > 0  # type: ignore[index]
    if args.deep:
        assert rank45_scan == {
            "range": [288, 2_000],
            "rank45_best_ratio": (288, 31_262),
            "rank45_worst_Z3_minus_109V": (288, -130, 31_262),
            "rank45_template_failures": [],
            "rank46_worst_Z4_minus_affine_gate": (288, 0, 424_798),
            "rank46_worst_Z4_minus_loose_affine_gate": (
                288,
                0,
                424_798,
            ),
            "rank46_first_anchor_slope_one_failure": (290, 1, 424_801),
            "rank46_template_failures": [],
            "minimum_H59_minus_D59": (
                288,
                27_182_131_121_200_991_691_886_495,
            ),
        }

    reverse_anchor = residual_only_reverse_anchor()

    # Exact finite regression for the paper proof of the uniform slope lemma.
    slope_regression = slope_lemma_regression()
    affine_regression = affine_lift_regression()
    extended_entry_regression = extended_entry_gate_regression()
    remainder_entry_regression = remainder_entry_gate_regression(
        check_failed_boundary=args.deep,
    )
    for parameter in [288, 379, 1_000, 10_000, 10**6]:
        assert 109 * parameter >= comb(58, 3)
        assert kk(109 * parameter, 3) <= 6 * parameter

    scan = run_parallel_scan(args.scan_limit, args.workers)
    assert not scan["template_failures"]
    assert scan["worst_R2_minus_7V"][1] < 0  # type: ignore[index]
    if args.deep:
        assert scan == {
            "range": [288, 20_000],
            "best_ratio": (288, 1_970),
            "worst_R2_minus_7V": (288, -46, 1_970),
            "max_jump": (17_423, 5, 19_701, 19_706),
            "min_jump": (289, 1, 1_972, 1_973),
            "last": (20_000, 22_398),
            "template_failures": [],
        }

    sparse_parameters = [25_000, 50_000, 100_000]
    if args.deep:
        sparse_parameters.extend([200_000, 500_000, 1_000_000])
    sparse_rows = [sparse_row(engine, value) for value in sparse_parameters]
    assert all(row["R2_minus_7V"] < 0 for row in sparse_rows)
    assert all(bool(row["template"]) for row in sparse_rows)
    if args.deep:
        assert [(row["V"], row["R2"]) for row in sparse_rows] == [
            (25_000, 27_546),
            (50_000, 53_267),
            (100_000, 104_486),
            (200_000, 206_522),
            (500_000, 511_305),
            (1_000_000, 1_017_530),
        ]

    result = {
        "status": "PASS",
        "scope": (
            "DEEP FINITE FALSIFIER SCAN"
            if args.deep
            else "QUICK SYMBOLIC REGRESSION AND FINITE FALSIFIER SCAN"
        ),
        "ordinary_compressed_crosschecks": crosschecks,
        "proved_in_markdown": {
            "adjacent_identity": (
                "R2(V+1)-R2(V)=D43(V)-J43(V)+1-L45(V)"
            ),
            "propagation_loss_gate": "L45>=D43-J43-6",
            "separated_gap_gate": (
                "G45>=S2(R2)-U2(R2-V+6)"
            ),
            "rank45_linear_lift": (
                "D45<=J45+109V implies D44<=J44+7V"
            ),
            "rank3_slope_lemma": (
                "109 KK3(x)<=6x for x>=C(58,3)"
            ),
            "affine_rank3_shadow": (
                "KK3(109V-130)<=6V-46 for every V>=288"
            ),
            "upper_shift_superadditivity": (
                "U_p(x+y)>=U_p(x)+U_p(y)"
            ),
            "large_leading_increment": (
                "U_p(x+y)-U_p(x)>=U_(p-1)(y) when "
                "y<=C(a,p-1) and x has leading C(a,p)"
            ),
            "rank46_affine_lift": (
                "D46<=J46+2V+424222 implies D44<=J44+7V-46"
            ),
            "rank46_loose_affine_lift": (
                "D46<=J46+458V+292894 implies D44<=J44+7V-46"
            ),
            "extended_entry_gate": (
                "first moving-block entry s<=43 implies D18<P18"
            ),
            "fixed_rank59_reduction": (
                "D59<H59 implies the zero-slack premise"
            ),
            "remainder_entry_gate": (
                "first moving-block entry s<=233 implies D18<P18"
            ),
            "fixed_rank248_reduction": (
                "D248<H248 implies the zero-slack premise"
            ),
        },
        "diagonal_rows_falsifier_only": diagonal_rows,
        "rank45_rows_falsifier_only": rank45_rows,
        "rank46_rows_falsifier_only": rank46_rows,
        "rank248_rows_falsifier_only": rank248_rows,
        "rank45_contiguous_scan_falsifier_only": rank45_scan,
        "residual_only_reverse_route_counterexample": reverse_anchor,
        "slope_lemma_regression": slope_regression,
        "affine_lift_regression": affine_regression,
        "extended_entry_gate_regression": extended_entry_regression,
        "remainder_entry_gate_regression": remainder_entry_regression,
        "contiguous_scan_falsifier_only": scan,
        "sparse_rows_falsifier_only": sparse_rows,
        "open": [
            "R2(V)<=7V for every V>=288",
            "R2(V+1)-R2(V)<=7 for every V>=288",
            "D45(V)<=J45(V)+109V for every V>=288",
            "D46(V)<=J46(V)+458V+292894 for every V>=288",
            "D59(V)<H59(V) for every V>=288",
            "D248(V)<H248(V) for every V>=288",
            "the rank-45 shadow-loss gate for every V>=288",
        ],
        "warning": (
            "Every parameter range in this output is finite.  No scan is "
            "used as an unbounded-parameter proof."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
