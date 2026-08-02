#!/usr/bin/env python3
"""Exact finite atlas for the multi-promotion no-borrow chamber of #776.

This is a falsifier and a frozen finite census, not an unbounded proof.  The
enumeration uses the exact triangular coordinates

    n = C(q,2) + r,
    n+b-1 = C(q+c,2) + u,

where c is the number of rank-two promotions.  Only c >= 2 is scanned.
"""

from __future__ import annotations

from collections import Counter
from collections import defaultdict
from functools import cache
import json
from math import comb


Q_MAX = 60
PROMOTION_MAX = 14


@cache
def canonical(number: int, rank: int) -> tuple[tuple[int, int], ...]:
    """Return the greedy rank-``rank`` Macaulay word by binary search."""
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    remaining = number
    ceiling: int | None = None
    word: list[tuple[int, int]] = []
    for lower in range(rank, 0, -1):
        if remaining == 0:
            break
        left = lower - 1
        if ceiling is None:
            right = lower
            while comb(right, lower) <= remaining:
                left = right
                right *= 2
        else:
            right = ceiling
        while left + 1 < right:
            middle = (left + right) // 2
            if comb(middle, lower) <= remaining:
                left = middle
            else:
                right = middle
        if left >= lower:
            word.append((left, lower))
            remaining -= comb(left, lower)
            ceiling = left
    if remaining:
        raise AssertionError((number, rank, remaining, word))
    return tuple(word)


@cache
def upper(number: int, rank: int) -> int:
    """Macaulay upper shadow U_rank(number)."""
    return sum(comb(top, lower + 1) for top, lower in canonical(number, rank))


def leading_remainder(number: int, rank: int) -> tuple[int, int]:
    """Write number=C(a,rank)+tail with 0<=tail<C(a,rank-1)."""
    word = canonical(number, rank)
    top = word[0][0] if word else rank - 1
    tail = number - comb(top, rank)
    assert 0 <= tail < comb(top, rank - 1)
    return top, tail


def loss(rank: int, cap: int, deficit: int) -> int:
    """Full-block loss Lambda_{rank,cap}(deficit)."""
    assert 0 <= deficit <= comb(cap, rank)
    return comb(cap, rank + 1) - upper(comb(cap, rank) - deficit, rank)


def rank_two_closed(top: int, remainder: int) -> int:
    """Independent closed form for U_2(C(top,2)+remainder)."""
    assert 0 <= remainder < top
    return comb(top, 3) + comb(remainder, 2)


def finite_atlas(
    q_max: int = Q_MAX,
    promotion_max: int = PROMOTION_MAX,
) -> dict[str, object]:
    """Enumerate the stated finite box and verify every exact identity."""
    promotion_counts: Counter[int] = Counter()
    gap_counts: Counter[int] = Counter()
    checked = 0
    negative_gamma_four = 0
    minimum: tuple[int, dict[str, int]] | None = None
    forward_oriented = 0
    forward_bound_positive = 0
    deficit_oriented = 0
    deficit_bound_positive = 0
    either_bound_positive = 0
    dual_deficit_bound_positive = 0
    second_level_bound_positive = 0
    second_level_residual: list[dict[str, int]] = []
    uncovered_counts: Counter[str] = Counter()
    uncovered_by_promotions: dict[str, Counter[int]] = defaultdict(Counter)
    uncovered_gaps: dict[str, dict[int, set[int]]] = defaultdict(
        lambda: defaultdict(set)
    )

    for q_value in range(2, q_max + 1):
        for promotions in range(2, promotion_max + 1):
            for r_value in range(q_value):
                for u_value in range(q_value + promotions):
                    n_value = comb(q_value, 2) + r_value
                    b_value = (
                        promotions * q_value
                        + comb(promotions, 2)
                        + u_value
                        - r_value
                        + 1
                    )
                    twice_h = comb(b_value - 1, 2) + 2 - n_value
                    if twice_h % 2:
                        continue
                    h_value = twice_h // 2
                    if b_value < 31 or h_value < 224 or b_value >= h_value:
                        continue

                    # Recover and independently check both triangular words.
                    assert n_value + b_value - 1 == (
                        comb(q_value + promotions, 2) + u_value
                    )
                    z_value = rank_two_closed(q_value, r_value)
                    w_value = rank_two_closed(
                        q_value + promotions,
                        u_value,
                    )
                    assert z_value == upper(n_value, 2)
                    assert w_value == upper(n_value + b_value - 1, 2)
                    assert n_value == comb(b_value - 1, 2) + 2 - 2 * h_value

                    h_cap = comb(b_value, 2) + 1
                    tau = h_cap - n_value
                    gamma_three = w_value - z_value - h_cap
                    x_value = n_value + z_value - h_cap + 1
                    y_value = n_value + z_value + gamma_three
                    if gamma_three >= 0 or x_value < 0:
                        continue
                    assert y_value == x_value + (w_value - z_value - 1)
                    assert y_value >= x_value >= 0

                    gamma_four = (
                        upper(y_value, 3)
                        - upper(x_value, 3)
                        - x_value
                        - tau
                    )
                    # The tax cancellation is exact, not an estimate.
                    assert x_value + tau == z_value + 1
                    assert gamma_four == (
                        upper(y_value, 3)
                        - upper(x_value, 3)
                        - z_value
                        - 1
                    )

                    a_value, alpha = leading_remainder(x_value, 3)
                    t_value, beta = leading_remainder(y_value, 3)
                    assert gamma_four == (
                        comb(t_value, 4)
                        - comb(a_value, 4)
                        + upper(beta, 2)
                        - upper(alpha, 2)
                        - z_value
                        - 1
                    )

                    # One further canonical level retains the positive
                    # remainder instead of replacing the whole difference
                    # by superadditivity.
                    s_value, rho = leading_remainder(alpha, 2)
                    v_value, sigma = leading_remainder(beta, 2)
                    second_level_exact = (
                        comb(t_value, 4)
                        - comb(a_value, 4)
                        + comb(v_value, 3)
                        - comb(s_value, 3)
                        + comb(sigma, 2)
                        - comb(rho, 2)
                        - z_value
                        - 1
                    )
                    assert second_level_exact == gamma_four
                    # rho<s, so C(rho,2)<=C(s-1,2).  Crucially, the
                    # nonnegative C(sigma,2) term is retained.
                    second_level_lower = (
                        comb(t_value, 4)
                        - comb(a_value, 4)
                        + comb(v_value, 3)
                        - comb(s_value, 3)
                        + comb(sigma, 2)
                        - comb(s_value - 1, 2)
                        - z_value
                        - 1
                    )
                    assert gamma_four >= second_level_lower
                    second_level_positive = second_level_lower > 0
                    second_level_bound_positive += int(second_level_positive)

                    # The equivalent full-cap/deficit normalization.
                    a_cap = a_value + 1
                    b_cap = t_value + 1
                    cap_gap = b_cap - a_cap
                    assert cap_gap >= 1
                    d_value = comb(a_cap, 3) - x_value
                    e_value = comb(b_cap, 3) - y_value
                    assert 0 <= d_value <= comb(a_cap, 3)
                    assert 0 <= e_value <= comb(b_cap, 3)
                    cap_term = (
                        comb(b_cap, 4)
                        - comb(a_cap, 4)
                        - comb(a_cap, 3)
                    )
                    deficit_exact = (
                        cap_term
                        + d_value
                        + loss(3, a_cap, d_value)
                        - loss(3, b_cap, e_value)
                        - tau
                    )
                    assert deficit_exact == gamma_four

                    # Dualize only the rank-two tail alpha.  The previously
                    # proved Lambda>=U inequality gives a second independent
                    # lower certificate.
                    alpha_deficit = comb(a_value, 2) - alpha
                    rank_two_cap_term = (
                        comb(t_value, 4)
                        - comb(a_value, 4)
                        - comb(a_value, 3)
                    )
                    dual_exact = (
                        rank_two_cap_term
                        + upper(beta, 2)
                        + loss(2, a_value, alpha_deficit)
                        - z_value
                        - 1
                    )
                    assert dual_exact == gamma_four
                    dual_lower = (
                        rank_two_cap_term
                        + upper(beta, 2)
                        + upper(alpha_deficit, 2)
                        - z_value
                        - 1
                    )
                    assert gamma_four >= dual_lower
                    dual_deficit_bound_positive += int(dual_lower > 0)

                    forward_positive = False
                    if beta >= alpha:
                        forward_oriented += 1
                        forward_lower = (
                            comb(t_value, 4)
                            - comb(a_value, 4)
                            + upper(beta - alpha, 2)
                            - z_value
                            - 1
                        )
                        assert gamma_four >= forward_lower
                        forward_positive = forward_lower > 0
                        forward_bound_positive += int(forward_positive)

                    deficit_positive = False
                    if d_value >= e_value:
                        deficit_oriented += 1
                        # Iterated vertical transport:
                        # Lambda_A(D)-Lambda_{A+g}(E)
                        # >= U_3(D-E)-gE.
                        deficit_lower = (
                            cap_term
                            + d_value
                            + upper(d_value - e_value, 3)
                            - cap_gap * e_value
                            - tau
                        )
                        assert gamma_four >= deficit_lower
                        deficit_positive = deficit_lower > 0
                        deficit_bound_positive += int(deficit_positive)

                    covered = forward_positive or deficit_positive
                    either_bound_positive += int(covered)
                    if not covered:
                        if beta < alpha and d_value < e_value:
                            template = "reverse_remainders: beta<alpha and D<E"
                        elif beta >= alpha and d_value >= e_value:
                            template = "forward_boundary: beta>=alpha and D>=E"
                        else:
                            template = "mixed_orientation"
                        uncovered_counts[template] += 1
                        uncovered_by_promotions[template][promotions] += 1
                        uncovered_gaps[template][promotions].add(cap_gap)
                    checked += 1
                    promotion_counts[promotions] += 1
                    gap_counts[cap_gap] += 1
                    negative_gamma_four += int(gamma_four <= 0)
                    row = {
                        "q": q_value,
                        "promotions": promotions,
                        "r": r_value,
                        "u": u_value,
                        "b": b_value,
                        "h": h_value,
                        "gamma3": gamma_three,
                        "x0": x_value,
                        "y0": y_value,
                    }
                    if not second_level_positive:
                        second_level_residual.append(
                            row
                            | {
                                "gamma4": gamma_four,
                                "second_level_lower": second_level_lower,
                                "a": a_value,
                                "t": t_value,
                                "alpha": alpha,
                                "beta": beta,
                                "s": s_value,
                                "rho": rho,
                                "v": v_value,
                                "sigma": sigma,
                            }
                        )
                    if minimum is None or gamma_four < minimum[0]:
                        minimum = (gamma_four, row)

    assert minimum is not None
    uncovered_templates: dict[str, object] = {}
    for template, count in sorted(uncovered_counts.items()):
        uncovered_templates[template] = {
            "count": count,
            "by_promotions": dict(
                sorted(uncovered_by_promotions[template].items())
            ),
            "cap_gap_range_by_promotions": {
                promotion: [min(gaps), max(gaps)]
                for promotion, gaps in sorted(uncovered_gaps[template].items())
            },
        }

    return {
        "domain": {
            "q": [2, q_max],
            "promotions": [2, promotion_max],
            "r": "0 <= r < q",
            "u": "0 <= u < q+promotions",
            "filters": "b>=31, h>=224, b<h, gamma3<0, x0>=0",
        },
        "checked_states": checked,
        "states_by_promotions": dict(sorted(promotion_counts.items())),
        "gamma4_nonpositive_states": negative_gamma_four,
        "minimum_gamma4": minimum[0],
        "minimum_state": minimum[1],
        "rank3_cap_gap": [min(gap_counts), max(gap_counts)],
        "conditional_lower_bounds": {
            "beta_at_least_alpha": forward_oriented,
            "forward_bound_positive": forward_bound_positive,
            "D_at_least_E": deficit_oriented,
            "deficit_bound_positive": deficit_bound_positive,
            "positive_by_either_bound": either_bound_positive,
            "uncovered_states": checked - either_bound_positive,
            "dual_deficit_bound_positive": dual_deficit_bound_positive,
            "second_level_bound_positive": second_level_bound_positive,
            "second_level_residual_count": len(second_level_residual),
        },
        "second_level_residual": second_level_residual,
        "uncovered_templates": uncovered_templates,
    }


def shallow_two_cap_base(q_max: int = 89) -> dict[str, object]:
    """Finite base for the proved c=2 shallow two-cap template.

    The manuscript proves positivity for q>=90.  This routine checks every
    smaller lattice point in the same symbolic phase.
    """
    rows: list[dict[str, int]] = []
    for q_value in range(2, q_max + 1):
        promotions = 2
        r_value = q_value - 1
        for u_value in range(q_value + promotions):
            n_value = comb(q_value, 2) + r_value
            b_value = q_value + u_value + 3
            twice_h = comb(b_value - 1, 2) + 2 - n_value
            if twice_h % 2:
                continue
            h_value = twice_h // 2
            if b_value < 31 or h_value < 224 or b_value >= h_value:
                continue

            h_cap = comb(b_value, 2) + 1
            z_value = rank_two_closed(q_value, r_value)
            w_value = rank_two_closed(q_value + 2, u_value)
            gamma_three = w_value - z_value - h_cap
            x_value = n_value + z_value - h_cap + 1
            y_value = n_value + z_value + gamma_three
            if gamma_three >= 0 or x_value < 0:
                continue
            a_value, alpha = leading_remainder(x_value, 3)
            t_value, beta = leading_remainder(y_value, 3)
            delta = comb(a_value, 2) - alpha
            if not (
                a_value == q_value - 1
                and t_value == q_value + 1
                and 1 <= delta <= q_value - 2
            ):
                continue

            assert delta == comb(b_value, 2) - 2 * comb(q_value, 2)
            assert beta == comb(u_value, 2) + 2 * q_value - 2 - delta
            shallow_loss = (
                delta * (q_value - 2) - comb(delta + 1, 2)
            )
            assert shallow_loss == loss(2, q_value - 1, delta)
            gamma_four = upper(y_value, 3) - upper(x_value, 3) - z_value - 1
            shallow_exact = (
                upper(beta, 2)
                + shallow_loss
                - comb(q_value - 1, 2)
                - 1
            )
            assert shallow_exact == gamma_four > 0
            rows.append(
                {
                    "q": q_value,
                    "u": u_value,
                    "b": b_value,
                    "h": h_value,
                    "gamma3": gamma_three,
                    "delta": delta,
                    "beta": beta,
                    "gamma4": gamma_four,
                }
            )

    minimum = min(rows, key=lambda row: row["gamma4"])
    return {
        "domain": "2<=q<=89 in the c=2,r=q-1,(a,t)=(q-1,q+1),1<=delta<=q-2 phase",
        "checked_states": len(rows),
        "minimum": minimum,
    }


def main() -> None:
    result = finite_atlas()
    assert result["checked_states"] == 85_278
    assert result["states_by_promotions"] == {
        2: 36_288,
        3: 33_620,
        4: 14_921,
        5: 449,
    }
    assert result["gamma4_nonpositive_states"] == 0
    assert result["minimum_gamma4"] == 69
    assert result["conditional_lower_bounds"][
        "dual_deficit_bound_positive"
    ] == 84_743
    assert result["conditional_lower_bounds"][
        "second_level_bound_positive"
    ] == 85_276
    assert result["conditional_lower_bounds"][
        "second_level_residual_count"
    ] == 2
    assert result["uncovered_templates"] == {
        "forward_boundary: beta>=alpha and D>=E": {
            "count": 120,
            "by_promotions": {2: 120},
            "cap_gap_range_by_promotions": {2: [1, 1]},
        },
        "reverse_remainders: beta<alpha and D<E": {
            "count": 31_815,
            "by_promotions": {2: 15_463, 3: 12_418, 4: 3_881, 5: 53},
            "cap_gap_range_by_promotions": {
                2: [2, 14],
                3: [3, 22],
                4: [5, 28],
                5: [12, 28],
            },
        },
    }
    assert result["minimum_state"] == {
        "q": 16,
        "promotions": 2,
        "r": 0,
        "u": 3,
        "b": 37,
        "h": 256,
        "gamma3": -408,
        "x0": 14,
        "y0": 272,
    }
    base = shallow_two_cap_base()
    assert base == {
        "domain": "2<=q<=89 in the c=2,r=q-1,(a,t)=(q-1,q+1),1<=delta<=q-2 phase",
        "checked_states": 20,
        "minimum": {
            "q": 39,
            "u": 13,
            "b": 55,
            "h": 327,
            "gamma3": -590,
            "delta": 3,
            "beta": 151,
            "gamma4": 186,
        },
    }
    print(
        json.dumps(
            {"finite_atlas": result, "shallow_two_cap_base": base},
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
