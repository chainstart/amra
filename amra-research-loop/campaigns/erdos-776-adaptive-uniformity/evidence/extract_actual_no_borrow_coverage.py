#!/usr/bin/env python3
"""Extract actual dyadic no-borrow states and their relaxed coordinates."""

from collections import Counter
from math import comb, isqrt
import json


def upper(number: int, rank: int) -> int:
    assert number >= 0
    remainder = number
    ceiling = None
    answer = 0
    for lower in range(rank, 0, -1):
        if remainder == 0:
            break
        lo = lower - 1
        hi = ceiling if ceiling is not None else max(2, lower + 1)
        if ceiling is None:
            while comb(hi, lower) <= remainder:
                hi *= 2
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if comb(mid, lower) <= remainder:
                lo = mid
            else:
                hi = mid
        if lo >= lower:
            remainder -= comb(lo, lower)
            answer += comb(lo, lower + 1)
            ceiling = lo
    assert remainder == 0
    return answer


def rank_two_coordinates(number: int):
    q = (1 + isqrt(1 + 8 * number)) // 2
    while comb(q + 1, 2) <= number:
        q += 1
    while comb(q, 2) > number:
        q -= 1
    remainder = number - comb(q, 2)
    assert 0 <= remainder < q
    return q, remainder


def main() -> None:
    counts = Counter()
    minimum_by_c = {}
    negative_gamma4 = Counter()
    equality_checks = 0
    first_small_c = None
    first_negative_c1 = None
    first_negative_gamma5_c1 = None
    c1_transition_counts = Counter()
    first_by_c1_transition = {}
    for j in range(2, 11):
        half = 112 * (1 << (j - 1))
        for offset in range(5, half):
            n = comb(offset - 1, 2) + 2 - 2 * half
            if n < 0:
                continue
            m = offset - 1
            H = comb(offset, 2) + 1
            z = upper(n, 2)
            w = upper(n + m, 2)
            gamma3 = w - z - H
            if gamma3 >= 0:
                continue
            x = n + z - H + 1
            y = n + w - H
            if x < 0:
                continue
            q, r = rank_two_coordinates(n)
            q2, u = rank_two_coordinates(n + m)
            c = q2 - q
            reconstructed_offset = c * q + comb(c, 2) + u - r + 1
            assert reconstructed_offset == offset
            gamma4 = upper(y, 3) - upper(x, 3) - z - 1

            # Direct actual low orbit from its rank-three leading blocks.
            top = half + offset - 2
            tax = 2 * half + offset - 3
            x3 = comb(top, 3) + n
            y3 = comb(top + 1, 3) + n + m
            x4 = upper(x3, 3) - tax
            y4 = upper(y3, 3) - tax - 1
            actual_gamma3 = y4 - x3 - upper(x3, 3)
            assert actual_gamma3 == gamma3
            x5 = upper(x4, 4) - tax
            y5 = upper(y4, 4) - tax - 1
            actual_gamma4 = y5 - x4 - upper(x4, 4)
            assert actual_gamma4 == gamma4
            x6 = upper(x5, 5) - tax
            y6 = upper(y5, 5) - tax - 1
            actual_gamma5 = y6 - x5 - upper(x5, 5)
            x7 = upper(x6, 6) - tax
            y7 = upper(y6, 6) - tax - 1
            actual_gamma6 = y7 - x6 - upper(x6, 6)
            equality_checks += 1

            counts[c] += 1
            negative_gamma4[c] += int(gamma4 < 0)
            row = {"j": j, "half": half, "offset": offset, "q": q, "c": c,
                   "r": r, "u": u, "x": x, "y": y, "gamma4": gamma4}
            if c not in minimum_by_c or (j, offset) < (minimum_by_c[c]["j"], minimum_by_c[c]["offset"]):
                minimum_by_c[c] = row
            if c < 2 and first_small_c is None:
                first_small_c = row
            if c == 1 and gamma4 < 0:
                k_value = offset - q
                r_tail = comb(r + 1, 2) - k_value * q - comb(k_value, 2)
                s_tail = r_tail + comb(u, 2) - comb(r, 2) - 1
                eps_x = int(r_tail < 0)
                eps_y = int(s_tail < 0)
                a_value = q - eps_x
                gap = 1 + eps_x - eps_y
                alpha = r_tail + eps_x * comb(q - 1, 2)
                beta = s_tail + eps_y * comb(q, 2)
                assert 0 <= alpha < comb(a_value, 2)
                assert 0 <= beta < comb(a_value + gap, 2)
                p_raw = upper(alpha, 2) - (H - n) + 1
                q_raw = upper(beta, 2) - (H - n)
                transition = (("-" if r_tail < 0 else "+") +
                              ("-" if s_tail < 0 else "+") + " -> " +
                              ("-" if p_raw < 0 else "+") +
                              ("-" if q_raw < 0 else "+"))
                c1_transition_counts[transition] += 1
                detailed = {**row, "k": k_value, "r_tail": r_tail,
                            "s_tail": s_tail, "a": a_value, "gap": gap,
                            "alpha": alpha, "beta": beta, "p_raw": p_raw,
                            "q_raw": q_raw, "transition": transition,
                            "gamma5": actual_gamma5, "gamma6": actual_gamma6}
                first_by_c1_transition.setdefault(transition, detailed)
                if first_negative_c1 is None:
                    first_negative_c1 = detailed
                if actual_gamma5 < 0 and first_negative_gamma5_c1 is None:
                    first_negative_gamma5_c1 = detailed

    assert equality_checks > 0
    print(json.dumps({
        "schema": "amra.erdos776.actual-no-borrow-coverage-extractor.v1",
        "dyadic_strips": [2, 10],
        "actual_states": equality_checks,
        "counts_by_promotion_c": dict(sorted(counts.items())),
        "negative_gamma4_by_c": dict(sorted(negative_gamma4.items())),
        "minimum_actual_row_by_c": {str(c): minimum_by_c[c] for c in sorted(minimum_by_c)},
        "first_actual_c_below_2": first_small_c,
        "first_actual_negative_gamma4_c1": first_negative_c1,
        "first_actual_negative_gamma5_c1": first_negative_gamma5_c1,
        "c1_negative_gamma4_transition_counts": dict(sorted(c1_transition_counts.items())),
        "first_by_c1_transition": {key: first_by_c1_transition[key] for key in sorted(first_by_c1_transition)},
        "all_surplus_equalities_checked": True,
        "unbounded_claim_from_computation": False,
        "public_problem_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
