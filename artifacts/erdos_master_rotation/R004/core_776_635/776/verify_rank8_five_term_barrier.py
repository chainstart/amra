#!/usr/bin/env python3
"""Exact audits for the R004 rank-8 work on Erdős #776.

The algebraic identities checked here are exact integer statements.  The
strategic evaluations of the shortened defect orbit are regression/falsifier
evidence only and are not presented as an all-parameter proof.
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
        upper_index = lo
        if cap is not None:
            upper_index = min(upper_index, cap - 1)
            while (
                upper_index >= lower
                and comb(upper_index, lower) > remainder
            ):
                upper_index -= 1
        if upper_index >= lower:
            answer.append((upper_index, lower))
            remainder -= comb(upper_index, lower)
            cap = upper_index
    if remainder:
        raise AssertionError((number, rank, remainder, answer))
    return answer


def kk(number: int, rank: int) -> int:
    return sum(
        comb(upper_index, lower - 1)
        for upper_index, lower in canonical(number, rank)
    )


def upper(number: int, rank: int) -> int:
    return sum(
        comb(upper_index, lower + 1)
        for upper_index, lower in canonical(number, rank)
    )


def suspension(number: int, rank: int) -> int:
    return number + upper(number, rank)


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


def h8_five(parameter: int) -> int:
    v = parameter
    return (
        comb(v + 1, 8)
        + comb(v - 1, 7)
        + comb(v - 3, 6)
        + comb(v - 5, 5)
        + comb(v - 7, 4)
    )


def h9(parameter: int) -> int:
    v = parameter
    return (
        comb(v + 1, 9)
        + comb(v - 1, 8)
        + comb(v - 3, 7)
        + comb(v - 5, 6)
        + comb(v - 7, 5)
        + comb(v - 9, 4)
    )


def f5(parameter: int) -> int:
    v = parameter
    return (
        comb(v + 1, 5)
        + comb(v - 1, 4)
        + comb(v - 2, 3)
    )


def five_term_endpoint(parameter: int) -> dict[str, object]:
    v = parameter
    e8 = h8_five(v) + comb(v - 8, 3) - 1
    assert e8 == h8(v) + comb(v - 9, 2) - 1
    expected8 = [
        (v + 1, 8),
        (v - 1, 7),
        (v - 3, 6),
        (v - 5, 5),
        (v - 7, 4),
        (v - 9, 3),
        (v - 10, 2),
        (v - 11, 1),
    ]
    assert canonical(e8, 8) == expected8

    e7 = v + kk(e8, 8)
    e6 = v + kk(e7, 7)
    e5 = v + kk(e6, 6)
    assert canonical(e7, 7) == [
        (v + 1, 7),
        (v - 1, 6),
        (v - 3, 5),
        (v - 5, 4),
        (v - 6, 3),
        (4, 2),
        (2, 1),
    ]
    assert canonical(e6, 6) == [
        (v + 1, 6),
        (v - 1, 5),
        (v - 3, 4),
        (v - 4, 3),
        (5, 2),
        (1, 1),
    ]
    assert canonical(e5, 5) == [
        (v + 1, 5),
        (v - 1, 4),
        (v - 2, 3),
        (5, 2),
    ]
    assert e5 == f5(v) + 10
    return {
        "V": v,
        "barrier": e8,
        "E5_minus_F5_at_endpoint": e5 - f5(v),
        "canonical_E8": expected8,
    }


def top17_coupling(parameter: int, shortfall: int) -> dict[str, int]:
    v = parameter
    s = shortfall
    if v < 40 or not 1 <= s <= 17:
        raise ValueError((v, s))
    residual = comb(v - 18, 2) - s
    threshold = comb(v - 18 - s, 2) - comb(v - 36, 2)
    next_q_cap = upper(comb(v - 17, 2) - 18, 2)
    assert suspension(residual, 2) - threshold == next_q_cap

    # The full six-term baseline raises harmonically.
    assert suspension(h8(v), 8) == h9(v + 1)

    # Galois converts the Q' cap into the relaxed next rank-8 residual cap.
    maximum_next_residual = v + 1 + kk(next_q_cap, 3)
    assert maximum_next_residual == comb(v - 16, 2)
    assert kk(next_q_cap + 1, 3) > kk(next_q_cap, 3)
    return {
        "V": v,
        "s": s,
        "R": residual,
        "Delta_s": threshold,
        "Q_prime_cap": next_q_cap,
        "next_rank8_residual_cap": maximum_next_residual,
    }


def load_compressed_engine():
    source = (
        Path(__file__).resolve().parents[3]
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


def shortened_defect_endpoint(engine, parameter: int) -> dict[str, object]:
    """Dual form of the five-term reservoir survival condition.

    Put n=V-9 and start D_(V-12)=0.  Tail complementation gives
        D_(q-1)=V+KK_q(D_q).
    The desired reservoir survival is exactly D_2 <= C(V-9,2).
    """
    v = parameter
    rank = v - 12
    runs: list[tuple[int, int, int]] = []
    while rank > 2:
        runs = engine.defect_step(runs, rank, v)
        rank -= 1
    d2 = engine.runs_value(runs)
    cap = comb(v - 9, 2)
    expansion = canonical(d2, 2)
    assert d2 <= cap
    assert expansion[0] == (v - 10, 2)
    tail = d2 - comb(v - 10, 2)
    assert 0 <= tail < v - 10
    return {
        "V": v,
        "D2": d2,
        "cap_C_Vminus9_2": cap,
        "margin": cap - d2,
        "rank1_tail_after_C_Vminus10_2": tail,
        "compressed_runs": runs,
    }


def shortened_rank8_entry(engine, parameter: int) -> dict[str, object]:
    v = parameter
    rank = v - 12
    runs: list[tuple[int, int, int]] = []
    while rank > 8:
        runs = engine.defect_step(runs, rank, v)
        rank -= 1
    d8 = engine.runs_value(runs)
    first_two = comb(v - 12, 8) + comb(v - 13, 7)
    residual = d8 - first_two
    cap = comb(v - 11, 8)
    assert 0 <= residual < comb(v - 13, 6)
    assert cap - d8 == comb(v - 13, 6) - residual
    return {
        "V": v,
        "D8": d8,
        "D8_cap": cap,
        "margin": cap - d8,
        "residual_after_two_harmonic_terms": residual,
        "residual_cap_C_Vminus13_6": comb(v - 13, 6),
        "compressed_runs": runs,
    }


def rank8_cap_descent(parameter: int) -> dict[str, object]:
    """Audit the fixed-depth lemma D8<C(V-11,8) => D2<=C(V-9,2)."""
    v = parameter
    n = v - 11
    d = comb(n, 8) - 1
    assert kk(d, 8) == comb(n, 7)

    # After the first shadow, the large C(n,r) term is harmonic and all
    # additions are carried by this fixed-depth residual recurrence.
    residual = v
    residual_rows = [{"rank": 6, "value": residual}]
    d = v + kk(d, 8)
    assert d == comb(n, 7) + residual
    for rank in range(7, 2, -1):
        assert canonical(d, rank)[0] == (n, rank)
        d = v + kk(d, rank)
        if rank > 3:
            residual = v + kk(residual, rank - 1)
            residual_rows.append(
                {"rank": rank - 2, "value": residual}
            )
            assert d == comb(n, rank - 1) + residual

    cap = comb(v - 9, 2)
    assert d <= cap
    # Equivalently, the last small shadow pays no more than V-21.
    assert kk(residual, 2) <= v - 21
    assert d == comb(n, 2) + v + kk(residual, 2)
    return {
        "V": v,
        "synthetic_D8": comb(n, 8) - 1,
        "D2": d,
        "D2_cap": cap,
        "margin": cap - d,
        "fixed_depth_residuals": residual_rows,
        "final_KK2_residual": kk(residual, 2),
    }


def reverse_requirement(parameter: int) -> dict[str, object]:
    v = parameter
    z = 0
    for lower_rank in range(v - 12, 2, -1):
        z = kk(v + z, lower_rank + 1)
    cap = comb(v - 9, 3)
    assert z <= cap
    return {
        "V": v,
        "Z3": z,
        "cap_C_Vminus9_3": cap,
        "margin": cap - z,
        "canonical_Z3": canonical(z, 3),
    }


def main() -> None:
    five_term_checks = [
        five_term_endpoint(v) for v in (15, 16, 20, 40, 100, 379)
    ]
    top17_checks = [
        top17_coupling(v, s)
        for v in (40, 100, 379, 6_328)
        for s in (1, 2, 9, 17)
    ]

    engine, dependency = load_compressed_engine()
    shortened = [
        shortened_defect_endpoint(engine, v)
        for v in (40, 50, 100, 200, 379, 1_000, 10_000)
    ]
    rank8_entry = [
        shortened_rank8_entry(engine, v)
        for v in (40, 50, 100, 200, 379, 1_000, 10_000, 100_000)
    ]
    # This is a complete finite audit of the small range in the conditional
    # rank-8 descent lemma.  For V>=1000, the report gives the elementary
    # analytic proof from KK_r(x)<=r*x and KK_2(x)<=sqrt(2x)+2.
    rank8_small_range = [rank8_cap_descent(v) for v in range(40, 1_000)]
    rank8_strategic = [
        rank8_cap_descent(v) for v in (1_000, 10_000, 100_000)
    ]
    reverse = [reverse_requirement(v) for v in (40, 50, 100, 200, 379)]

    result = {
        "schema": "amra.erdos776.r004-five-term-rank8.v1",
        "status": "PASS",
        "strict_results": {
            "five_term_descent": (
                "For V>=15, the synthetic endpoint "
                "H8^(5)(V)+C(V-8,3)-1 = H8(V)+C(V-9,2)-1 "
                "descends exactly to E5=F5(V)+10."
            ),
            "top17_collapse": (
                "For R=C(V-18,2)-s, 1<=s<=17, the R003 G9 "
                "condition is exactly Q'<=U2(C(V-17,2)-18), "
                "equivalently the next residual is <=C(V-16,2); "
                "the condition is independent of s."
            ),
            "new_all_V_breakpoint": (
                "For V>=40, D8<C(V-11,8) implies D2<=C(V-9,2). "
                "Thus five-term entry over I8 is reduced to the single "
                "rank-8 cap for the shortened zero-seed defect orbit."
            ),
        },
        "five_term_endpoint_audits": five_term_checks,
        "top17_coupling_audits": top17_checks,
        "shortened_defect_falsifier_checks": shortened,
        "shortened_rank8_entry_falsifier_checks": rank8_entry,
        "rank8_cap_descent_complete_small_range": {
            "V_range": [40, 999],
            "checks": len(rank8_small_range),
            "minimum_margin": min(row["margin"] for row in rank8_small_range),
            "first_minimum_at_V": min(
                row["V"]
                for row in rank8_small_range
                if row["margin"]
                == min(item["margin"] for item in rank8_small_range)
            ),
        },
        "rank8_cap_descent_strategic_checks": rank8_strategic,
        "reverse_requirement_checks": reverse,
        "compressed_engine_dependency": str(dependency),
        "scope": (
            "The symbolic endpoint and coupling identities are exact.  "
            "The selected shortened-orbit evaluations are finite evidence "
            "only; an all-V proof of D2<=C(V-9,2) is still missing."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
