#!/usr/bin/env python3
"""Exact checks for the R003 capped rank-8 reduction for Erdős #776.

The symbolic identities justified in REPORT.md are audited here with exact
integer Macaulay expansions.  Strategic evaluations are regression evidence,
not an infinite-parameter proof.
"""

from __future__ import annotations

import importlib.util
import json
from math import comb
from pathlib import Path


def canonical(number: int, rank: int) -> list[tuple[int, int]]:
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    answer: list[tuple[int, int]] = []
    remainder = number
    cap: int | None = None
    for lower in range(rank, 0, -1):
        if remainder == 0:
            break
        lo = lower - 1
        hi = cap if cap is not None else max(2 * lower, lower + 1)
        if cap is None:
            while comb(hi, lower) <= remainder:
                hi *= 2
        while lo + 1 < hi:
            middle = (lo + hi) // 2
            if comb(middle, lower) <= remainder:
                lo = middle
            else:
                hi = middle
        upper = lo
        if cap is not None:
            upper = min(upper, cap - 1)
            while upper >= lower and comb(upper, lower) > remainder:
                upper -= 1
        if upper >= lower:
            answer.append((upper, lower))
            remainder -= comb(upper, lower)
            cap = upper
    if remainder:
        raise AssertionError((number, rank, remainder, answer))
    return answer


def kk(number: int, rank: int) -> int:
    return sum(comb(upper, lower - 1) for upper, lower in canonical(number, rank))


def upper(number: int, rank: int) -> int:
    return sum(comb(upper, lower + 1) for upper, lower in canonical(number, rank))


def suspension(number: int, rank: int) -> int:
    return number + upper(number, rank)


def minimum_input_loss(number: int, rank: int, requested_shadow_loss: int) -> int:
    """Exact Galois threshold for kk_rank(number)-kk_rank(number-delta).

    It returns the least delta for which the loss is at least the requested
    amount.  Here ``number`` is viewed at ``rank``.
    """
    shadow = kk(number, rank)
    if not 0 <= requested_shadow_loss <= shadow:
        raise ValueError((number, rank, requested_shadow_loss, shadow))
    return number - upper(shadow - requested_shadow_loss, rank - 1)


def h8(parameter: int) -> int:
    v = parameter
    return (
        comb(v + 1, 8)
        + comb(v - 1, 7)
        + comb(v - 3, 6)
        + comb(v - 5, 5)
        + comb(v - 7, 4)
        + comb(v - 9, 3)
    )


def f5(parameter: int) -> int:
    v = parameter
    return comb(v + 1, 5) + comb(v - 1, 4) + comb(v - 2, 3)


def stable_states(parameter: int, residual: int) -> dict[str, int]:
    """Descend exactly from E8=H8+residual and return ranks 8 through 5."""
    v = parameter
    if v < 40 or not 0 <= residual < comb(v - 18, 2):
        raise ValueError((v, residual))
    e8 = h8(v) + residual
    e7 = v + kk(e8, 8)
    e6 = v + kk(e7, 7)
    e5 = v + kk(e6, 6)
    k = kk(residual, 2)
    c = 9 + k

    expected_e7 = (
        comb(v + 1, 7)
        + comb(v - 1, 6)
        + comb(v - 3, 5)
        + comb(v - 5, 4)
        + comb(v - 7, 3)
        + comb(v - 8, 2)
        + c
    )
    expected_e6 = (
        comb(v + 1, 6)
        + comb(v - 1, 5)
        + comb(v - 3, 4)
        + comb(v - 4, 3)
        + comb(4, 2)
    )
    expected_e5 = f5(v) + 8
    assert (e7, e6, e5) == (expected_e7, expected_e6, expected_e5)
    return {"E8": e8, "E7": e7, "E6": e6, "E5": e5, "k": k, "c": c}


def audit_parameter(parameter: int, residual: int) -> dict[str, int]:
    v = parameter
    state = stable_states(v, residual)
    e8, e7, e6 = state["E8"], state["E7"], state["E6"]
    k, c = state["k"], state["c"]

    # First cap: the exact G7 needed to make L6 >= V+5.
    n6 = suspension(e6, 6)
    g7_threshold = minimum_input_loss(n6, 7, v + 5)
    assert g7_threshold == comb(v - 5, 2) + 10
    assert kk(n6, 7) - kk(n6 - g7_threshold, 7) >= v + 5
    assert kk(n6, 7) - kk(n6 - g7_threshold + 1, 7) < v + 5

    p7 = upper(e6, 6) - e7
    assert p7 == comb(v - 6, 2) + v - 4 - c
    required_l7 = g7_threshold - (p7 - 1)
    assert required_l7 == c + 9

    # Second cap: the exact G8 needed to make L7 >= c+9.
    n7 = suspension(e7, 7)
    g8_threshold_for_rank6 = minimum_input_loss(n7, 8, required_l7)
    assert g8_threshold_for_rank6 == comb(c + 1, 2) + 8 * v - 100

    p8 = upper(e7, 7) - e8
    assert p8 == comb(v - 9, 2) + comb(c, 2) - residual
    required_l8_for_rank6 = max(
        0, g8_threshold_for_rank6 - (p8 - 1)
    )
    assert required_l8_for_rank6 == max(
        0, residual + k - comb(v - 17, 2) + 18
    )
    assert required_l8_for_rank6 <= 17
    g9_threshold_for_rank6 = 0
    if required_l8_for_rank6:
        n8 = suspension(e8, 8)
        g9_threshold_for_rank6 = minimum_input_loss(
            n8, 9, required_l8_for_rank6
        )
        shortfall = comb(v - 18, 2) - residual
        assert 1 <= shortfall <= 17
        assert required_l8_for_rank6 == 18 - shortfall
        assert g9_threshold_for_rank6 == (
            comb(v - 18 - shortfall, 2) - comb(v - 36, 2)
        )
        assert g9_threshold_for_rank6 <= 17 * v - 476

    # A stronger requirement makes the one-sided rank-8 barrier propagate
    # to parameter V+1.  At the cap endpoint this costs exactly V+1, so the
    # nonquantitative bound L8>=0 cannot prove the full carry block.
    next_cap = comb(v - 17, 2)
    g8_threshold_for_next_barrier = (
        comb(v - 8, 2) + comb(c + 1, 2) - next_cap + 1
    )
    required_l8_for_next_barrier = max(
        0, g8_threshold_for_next_barrier - (p8 - 1)
    )
    assert required_l8_for_next_barrier == max(
        0, residual + k + v + 2 - next_cap
    )
    assert required_l8_for_next_barrier <= v + 1

    # If that loss is positive, the next exact Galois threshold is a rank-2
    # expression.  This exposes, rather than hides, the repeated carry cost.
    g9_threshold = 0
    if required_l8_for_next_barrier:
        n8 = suspension(e8, 8)
        g9_threshold = minimum_input_loss(
            n8, 9, required_l8_for_next_barrier
        )
        w = residual + k
        assert required_l8_for_next_barrier <= w
        expected_g9_threshold = (
            suspension(residual, 2)
            - upper(w - required_l8_for_next_barrier, 2)
        )
        assert g9_threshold == expected_g9_threshold
        assert kk(n8, 9) - kk(n8 - g9_threshold, 9) >= (
            required_l8_for_next_barrier
        )
        assert kk(n8, 9) - kk(n8 - g9_threshold + 1, 9) < (
            required_l8_for_next_barrier
        )

    return {
        "V": v,
        "R": residual,
        "k_KK2_R": k,
        "c": c,
        "E5_minus_F5": state["E5"] - f5(v),
        "G7_threshold_for_L6_ge_Vplus5": g7_threshold,
        "G8_threshold_for_L7_ge_cplus9": g8_threshold_for_rank6,
        "L8_needed_for_rank6": required_l8_for_rank6,
        "G9_threshold_for_rank6_L8": g9_threshold_for_rank6,
        "L8_needed_for_next_rank8_barrier": required_l8_for_next_barrier,
        "G9_threshold_for_that_L8": g9_threshold,
    }


def load_r002_engine():
    root = Path(__file__).resolve().parents[3]
    source = (
        root
        / "R002"
        / "core_776_635"
        / "776"
        / "verify_rank5_rotation.py"
    )
    spec = importlib.util.spec_from_file_location("r002_rank5", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, source


def exact_e8_from_r002(engine, parameter: int) -> int:
    rank = parameter
    runs = engine.canonical_runs(parameter - 3, rank)
    while rank > 8:
        runs = engine.defect_step(runs, rank, parameter)
        rank -= 1
    return engine.runs_value(runs)


def main() -> None:
    symbolic_audits: list[dict[str, int]] = []
    for v in (40, 100, 6_328, 66_843):
        cap = comb(v - 18, 2)
        candidates = sorted(
            {
                0,
                1,
                min(cap - 1, v),
                max(0, cap - v - 2),
                max(0, cap - 20),
                max(0, cap - 17),
                cap - 1,
            }
        )
        for residual in candidates:
            symbolic_audits.append(audit_parameter(v, residual))

    # The cap endpoint is the strict falsifier for the coarse L8>=0 route.
    cap_endpoint_checks = []
    for v in (40, 100, 6_328, 66_843):
        residual = comb(v - 18, 2) - 1
        row = audit_parameter(v, residual)
        assert row["L8_needed_for_next_rank8_barrier"] == v + 1
        cap_endpoint_checks.append(row)

    # Strategic evaluations only: they check that the actual orbit enters the
    # sufficient rank-8 barrier at known diagnostic points.
    engine, dependency = load_r002_engine()
    strategic = []
    for v in (6_328, 6_329, 66_843, 66_844, 70_501, 74_997, 200_000):
        e8 = exact_e8_from_r002(engine, v)
        cap_value = h8(v) + comb(v - 18, 2) - 1
        assert e8 <= cap_value
        residual = e8 - h8(v)
        row = {
            "V": v,
            "E8_minus_H8": residual,
            "rank8_barrier_margin": cap_value - e8,
        }
        if residual >= 0:
            row["conditional_E5_minus_F5"] = (
                stable_states(v, residual)["E5"] - f5(v)
            )
        strategic.append(row)

    result = {
        "schema": "amra.erdos776.r003-capped-rank8.v1",
        "status": "PASS",
        "strict_results": {
            "rank8_descent": (
                "For V>=40 and 0<=R<C(V-18,2), "
                "E8=H8(V)+R descends exactly to E5=F5(V)+8."
            ),
            "rank6_loss_threshold": (
                "L6>=V+5 iff G7>=C(V-5,2)+10."
            ),
            "rank7_loss_threshold": (
                "L7>=c+9 iff G8>=C(c+1,2)+8V-100, "
                "where c=9+KK2(R)."
            ),
            "coarse_full_block_no_go": (
                "At R=C(V-18,2)-1, propagation of the one-sided "
                "rank-8 barrier to V+1 requires L8>=V+1; L8>=0 "
                "alone is insufficient."
            ),
        },
        "symbolic_integer_audits": symbolic_audits,
        "cap_endpoint_checks": cap_endpoint_checks,
        "strategic_finite_orbit_checks": strategic,
        "r002_engine_dependency": str(dependency),
        "scope": (
            "The identities and strict synthetic boundary are proved by "
            "canonical/Galois algebra in REPORT.md.  The strategic orbit "
            "checks are finite regression evidence.  No all-V rank-8 "
            "entrance/barrier propagation theorem is claimed."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
