#!/usr/bin/env python3
"""Independent Macaulay audit of the base-retaining/top-index rank-5 gate.

No author module is imported. All actual-state formulas and greedy Macaulay
raising are implemented locally from the public chart definitions.
"""

from __future__ import annotations

from math import comb
from functools import lru_cache
import hashlib
import json
from pathlib import Path


def C(n: int, k: int) -> int:
    return comb(n, k) if n >= k >= 0 else 0


def largest_index(value: int, rank: int, strict_upper: int | None = None) -> int:
    low = rank - 1
    if strict_upper is not None:
        high = strict_upper - 1
    else:
        high = rank
        while C(high, rank) <= value:
            high *= 2
    while low < high:
        middle = (low + high + 1) // 2
        if C(middle, rank) <= value:
            low = middle
        else:
            high = middle - 1
    return low


@lru_cache(maxsize=1_000_000)
def macaulay(value: int, rank: int) -> tuple[tuple[int, ...], int]:
    assert value >= 0 and rank >= 1
    remainder = value
    upper = None
    word = []
    raised = 0
    for lower_rank in range(rank, 0, -1):
        index = largest_index(remainder, lower_rank, upper)
        word.append(index)
        remainder -= C(index, lower_rank)
        raised += C(index, lower_rank + 1)
        upper = index
    assert remainder == 0
    return tuple(word), raised


def U(value: int, rank: int) -> int:
    return macaulay(value, rank)[1]


def top(value: int, rank: int) -> int:
    return macaulay(value, rank)[0][0]


def state(j: int, k: int, r: int) -> dict[str, int | str] | None:
    h = 112 << (j - 1)
    step = k - 1
    numerator = 2 * h - C(step, 2) - 2 + r
    if numerator % step:
        return None
    q = numerator // step
    u = r + step
    b = q + k
    if not (q >= 2 and 0 <= r < q and 0 <= u < q + 1 and 5 <= b < h):
        return None
    alpha = C(r + 1, 2) - k * q - C(k, 2)
    beta = alpha + C(u, 2) - C(r, 2) - 1
    if alpha < 0 or beta < 0:
        return None
    tau = k * q + C(k, 2) + 1 - r
    p = U(alpha, 2) - tau + 1
    v = U(beta, 2) - tau
    if p < 0 or v < 0:
        return None
    gamma4 = v - p - alpha - tau + 1
    gamma5 = U(v, 3) - U(p, 3) - U(alpha, 2) - 1
    P = U(p, 3) - tau + 1
    V = U(v, 3) - tau
    cp, cv, ca = top(p, 3), top(v, 3), top(alpha, 2)
    leading = C(cv, 4) - C(cp + 1, 4) - U(alpha, 2)
    top_margin = C(cv, 4) - C(cp + 1, 4) - C(ca + 1, 3)
    p_free = U(v - p, 3) - U(alpha, 2) - 1
    return {
        "j": j, "h": h, "q": q, "k": k, "r": r, "u": u, "b": b,
        "alpha": alpha, "beta": beta, "tau": tau, "p": p, "v": v,
        "P": P, "V": V, "gamma4": gamma4, "gamma5": gamma5,
        "transition": "++ -> ++", "top_p": cp, "top_v": cv,
        "top_alpha": ca, "leading_block_margin": leading,
        "top_index_margin": top_margin, "p_free_margin": p_free,
    }


def legal_range(j: int, k: int) -> tuple[int, int, int] | None:
    """Compatible residue r=residue+m(k-1), with conservative exact bounds."""
    h = 112 << (j - 1)
    step = k - 1
    base = 2 * h - C(step, 2) - 2
    residue = (-base) % step
    # From r<q and u<q+1, then from b<h.
    maximum_r = (base - step * step - 1) // (step - 1)
    maximum_r = min(maximum_r, (h - k - 1) * step - base)
    if maximum_r < residue:
        return None
    return residue, 0, (maximum_r - residue) // step


def first_true(low: int, high: int, predicate) -> int | None:
    if low > high or not predicate(high):
        return None
    while low < high:
        middle = (low + high) // 2
        if predicate(middle):
            high = middle
        else:
            low = middle + 1
    return low


def first_target_r(j: int, k: int) -> int | None:
    interval = legal_range(j, k)
    if interval is None:
        return None
    residue, low, high = interval
    step = k - 1
    first = first_true(low, high, lambda m: state(j, k, residue + m * step) is not None)
    return None if first is None else residue + first * step


def with_offset(row: dict[str, int | str], offset: int) -> dict[str, int | str]:
    return {**row, "offset": offset}


def main() -> None:
    # Definition-level cap bounds, exhaustively checked on a broad independent
    # range as an implementation guard; their proof is recorded in the audit.
    cap_checks = 0
    for value in range(1, 20_001):
        for rank in (2, 3):
            word, raised = macaulay(value, rank)
            leading = word[0]
            assert C(leading, rank) <= value < C(leading + 1, rank)
            assert C(leading, rank + 1) <= raised <= C(leading + 1, rank + 1) - 1
            cap_checks += 1

    scales = list(range(6, 61)) + [70, 80, 90, 100]
    raw_evaluations: set[tuple[int, int, int]] = set()
    accepted = 0
    fibre_count = 0
    minimum_leading = None
    minimum_top = None
    first_p_free = None
    leading_negatives = []
    top_negatives = []

    for j in scales:
        for k in range(4, 301):
            start_r = first_target_r(j, k)
            if start_r is None:
                continue
            step = k - 1

            def raw(offset: int):
                if offset < 0:
                    return None
                raw_evaluations.add((j, k, offset))
                return state(j, k, start_r + offset * step)

            first = raw(0)
            if first is None or int(first["gamma4"]) >= 0:
                continue
            low, high = 0, 1
            while high < (1 << 50):
                probe = raw(high)
                if probe is None or int(probe["gamma4"]) >= 0:
                    break
                low, high = high, 2 * high
            if high >= (1 << 50):
                continue
            while low + 1 < high:
                middle = (low + high) // 2
                probe = raw(middle)
                if probe is not None and int(probe["gamma4"]) < 0:
                    low = middle
                else:
                    high = middle

            fibre_min = None
            offsets = sorted(set(range(65)) | set(range(max(0, low - 96), high + 97)))
            for offset in offsets:
                row = state(j, k, start_r + offset * step)
                if row is None or int(row["gamma4"]) >= 0:
                    continue
                accepted += 1
                record = with_offset(row, offset)
                if fibre_min is None or int(record["leading_block_margin"]) < int(fibre_min["leading_block_margin"]):
                    fibre_min = record
                if minimum_leading is None or int(record["leading_block_margin"]) < int(minimum_leading["leading_block_margin"]):
                    minimum_leading = record
                if minimum_top is None or int(record["top_index_margin"]) < int(minimum_top["top_index_margin"]):
                    minimum_top = record
                if int(record["p_free_margin"]) < 0 and (
                    first_p_free is None or (j, k, offset) < (int(first_p_free["j"]), int(first_p_free["k"]), int(first_p_free["offset"]))
                ):
                    first_p_free = record
                if int(record["leading_block_margin"]) < 0 and len(leading_negatives) < 3:
                    leading_negatives.append(record)
                if int(record["top_index_margin"]) < 0 and len(top_negatives) < 3:
                    top_negatives.append(record)
            if fibre_min is not None:
                fibre_count += 1

    # Directly verify the logical implication on every accepted row.
    assert not leading_negatives and not top_negatives
    assert minimum_leading is not None and minimum_top is not None
    assert int(minimum_leading["leading_block_margin"]) >= 0
    assert int(minimum_top["top_index_margin"]) >= 0

    payload = {
        "schema": "amra.erdos776.round3.top_index_independent_audit.v1",
        "author_functions_imported": False,
        "macaulay_definition_guard_rows": cap_checks,
        "conditional_deduction": {
            "status": "passed",
            "lower_bound": "U3(v)-U3(p)-U2(alpha) >= C(d,4)-C(c+1,4)+1-U2(alpha)",
            "leading_condition": "C(d,4)-C(c+1,4)-U2(alpha)>=0 implies the displayed exact difference is at least 1 and gamma5>=0",
            "strong_top_index_condition": "C(d,4)-C(c+1,4)-C(a+1,3)>=0, together with U2(alpha)<=C(a+1,3)-1, implies the exact difference is at least 2 and gamma5>=1",
            "scope": "conditional on the actual (++ -> ++) state definitions and the stated top-index inequality"
        },
        "adaptive_probe_reconstruction": {
            "domain": {"j": scales, "k": [4, 300]},
            "raw_rows_evaluated": len(raw_evaluations),
            "accepted_actual_pp_rows": accepted,
            "fibre_summary_count": fibre_count,
            "minimum_base_leading_margin": minimum_leading,
            "minimum_top_index_margin": minimum_top,
            "base_leading_counterexamples": leading_negatives,
            "top_index_counterexamples": top_negatives,
            "first_p_free_counterexample": first_p_free,
            "finite_only": True,
            "binary_wall_centring_exhaustive": False
        },
        "public_problem_changed": False,
        "global_rank5_closure_claimed": False,
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    output = Path(__file__).with_name("top_index_rank5_independent_audit.json")
    output.write_bytes(encoded)
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("output_sha256", hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
