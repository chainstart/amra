#!/usr/bin/env python3
"""Exact guards for Round 4 LTJ diagonal-loss identities.

Finite actual-orbit rows are identity checks only.  The canonical-plateau
family is symbolic and all-parameter; it refutes lower bounds on propagated
loss which depend only on a positive diagonal gap.
"""

from __future__ import annotations

from hashlib import sha256
from math import comb
from pathlib import Path
import json


def canonical(number: int, rank: int) -> list[tuple[int, int]]:
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    result: list[tuple[int, int]] = []
    remainder = number
    cap: int | None = None
    for lower in range(rank, 0, -1):
        if remainder == 0:
            break
        lo = lower - 1
        hi = cap if cap is not None else max(lower + 1, 2 * lower)
        if cap is None:
            while comb(hi, lower) <= remainder:
                hi *= 2
        while lo + 1 < hi:
            middle = (lo + hi) // 2
            if comb(middle, lower) <= remainder:
                lo = middle
            else:
                hi = middle
        upper = lo if cap is None else min(lo, cap - 1)
        if upper >= lower:
            result.append((upper, lower))
            remainder -= comb(upper, lower)
            cap = upper
    if remainder:
        raise AssertionError((number, rank, remainder, result))
    return result


def kk(number: int, rank: int) -> int:
    return sum(comb(upper, lower - 1) for upper, lower in canonical(number, rank))


def upper(number: int, rank: int) -> int:
    return sum(comb(upper_index, lower + 1) for upper_index, lower in canonical(number, rank))


def suspension(number: int, rank: int) -> int:
    return number + upper(number, rank)


def zero_seed_orbit(parameter: int, target: int) -> dict[int, int]:
    rank = parameter - 26
    value = 0
    rows = {rank: value}
    while rank > target:
        value = parameter + kk(value, rank)
        rank -= 1
        rows[rank] = value
    return rows


def actual_residual_row(parameter: int) -> dict[str, object]:
    orbit = zero_seed_orbit(parameter, 4)
    n = parameter - 25
    z3 = orbit[5] - comb(n - 1, 5) - comb(n - 2, 4)
    b2 = orbit[4] - comb(n - 1, 4) - comb(n - 2, 3)
    assert b2 == parameter + kk(z3, 3)
    word = canonical(b2, 2)
    return {
        "V": parameter,
        "Z3": z3,
        "B2": b2,
        "B2_word": word,
        "a": word[0][0],
    }


def diagonal_recurrence_guard(parameter: int) -> dict[str, object]:
    x = zero_seed_orbit(parameter, 4)
    y = zero_seed_orbit(parameter + 1, 5)
    top_rank = parameter - 26
    losses = {top_rank: 0}
    minimum_tax = 10**100
    minimum_propagated = 10**100
    for rank in range(top_rank, 4, -1):
        xq = x[rank]
        yq1 = y[rank + 1]
        loss = suspension(xq, rank) - yq1
        assert loss == losses[rank] and loss >= 0

        m = x[rank - 1]
        tax_capacity = upper(m, rank - 1) - xq - 1
        propagated = (
            kk(suspension(xq, rank), rank + 1)
            - kk(yq1, rank + 1)
        )
        next_loss = suspension(m, rank - 1) - y[rank]
        assert next_loss == tax_capacity + propagated
        assert tax_capacity >= parameter // rank - 1 >= 0
        assert propagated >= 0
        losses[rank - 1] = next_loss
        minimum_tax = min(minimum_tax, tax_capacity)
        minimum_propagated = min(minimum_propagated, propagated)

    before = actual_residual_row(parameter)
    after = actual_residual_row(parameter + 1)
    b2 = int(before["B2"])
    z3 = int(before["Z3"])
    z3_next = int(after["Z3"])
    assert losses[4] == suspension(b2, 2) - z3_next

    tax5 = upper(b2, 2) - z3 - 1
    propagated5 = b2 + z3 + 1 - z3_next
    assert losses[4] == tax5 + propagated5
    return {
        "V": parameter,
        "top_aligned_loss": losses[top_rank],
        "rank4_loss": losses[4],
        "rank5_tax_capacity": tax5,
        "rank5_propagated_loss": propagated5,
        "minimum_tax_capacity": minimum_tax,
        "minimum_propagated_loss": minimum_propagated,
        "B2_jump": int(after["B2"]) - b2,
        "LTJ_allowance": int(before["a"]),
    }


def plateau_guard() -> dict[str, object]:
    cases = 0
    samples = []
    for rank in range(2, 9):
        for upper_index in range(rank + 2, 31):
            x = comb(upper_index - 1, rank)
            suspended = suspension(x, rank)
            assert suspended == comb(upper_index, rank + 1)
            full_shadow = kk(suspended, rank + 1)
            assert full_shadow == comb(upper_index, rank)

            below_shadow = full_shadow - 1
            adjoint = upper(below_shadow, rank)
            assert adjoint == suspended - (upper_index - rank)

            for gap in range(1, upper_index - rank):
                y = suspended - gap
                assert kk(y, rank + 1) == full_shadow
                cases += 1
            if upper_index in (rank + 5, 30):
                samples.append(
                    {
                        "rank": rank,
                        "upper_index": upper_index,
                        "maximum_zero_loss_gap": upper_index - rank - 1,
                    }
                )
    return {
        "checked_cases": cases,
        "samples": samples,
        "symbolic_formula": (
            "For every A>=q+2 and 1<=L<=A-q-1, "
            "KK_(q+1)(C(A,q+1))-KK_(q+1)(C(A,q+1)-L)=0."
        ),
    }


def main() -> None:
    selected_rows = {
        str(parameter): actual_residual_row(parameter)
        for parameter in (125, 126, 300, 301, 500)
    }
    before = selected_rows["300"]
    after = selected_rows["301"]
    assert int(after["B2"]) - int(before["B2"]) == 3
    assert int(before["a"]) == 39

    payload = {
        "status": "PASS",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "selected_actual_rows": selected_rows,
        "diagonal_recurrence": [
            diagonal_recurrence_guard(parameter) for parameter in (125, 300)
        ],
        "canonical_plateau": plateau_guard(),
        "scope": (
            "Selected actual rows are finite guards only. "
            "The diagonal recurrence and canonical plateau formula are "
            "proved symbolically for all parameters in the accompanying note."
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
