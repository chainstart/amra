#!/usr/bin/env python3
"""Blind audit of the actual G++ p-free-gate counterexample.

No author verifier or generated evidence is imported.  This file implements
its own greedy Macaulay canonical expansion and reconstructs both the
normalized-tail identities and the full unnormalized orbit.
"""

from __future__ import annotations

import json
from math import comb


def choose(top: int, lower: int) -> int:
    if lower < 0 or top < lower:
        return 0
    return comb(top, lower)


def greatest_top(value: int, lower: int, strict_ceiling: int | None) -> int:
    """Largest t<ceiling (if supplied) with C(t,lower)<=value."""
    left = lower - 1
    if strict_ceiling is not None:
        right = strict_ceiling
    else:
        right = max(lower + 1, 2)
        while choose(right, lower) <= value:
            right *= 2
    while right - left > 1:
        middle = (left + right) // 2
        if choose(middle, lower) <= value:
            left = middle
        else:
            right = middle
    return left


def macaulay_word(value: int, rank: int) -> tuple[tuple[int, int], ...]:
    """Canonical value=sum C(top_i,i), top_rank>...>top_1."""
    assert value >= 0 and rank >= 1
    remainder = value
    ceiling: int | None = None
    word: list[tuple[int, int]] = []
    for lower in range(rank, 0, -1):
        if remainder == 0:
            break
        top = greatest_top(remainder, lower, ceiling)
        if top >= lower:
            word.append((top, lower))
            remainder -= choose(top, lower)
            ceiling = top
    assert remainder == 0
    assert all(word[i][0] > word[i + 1][0] for i in range(len(word) - 1))
    assert sum(choose(top, lower) for top, lower in word) == value
    return tuple(word)


def U(value: int, rank: int) -> int:
    return sum(choose(top, lower + 1) for top, lower in macaulay_word(value, rank))


def main() -> None:
    j, k, r = 21, 4, 26_466
    h = 112 * 2 ** (j - 1)

    # Solve the dyadic identity, retaining the divisibility check.
    numerator = 2*h - choose(k - 1, 2) - 2 + r
    assert numerator % (k - 1) == 0
    q = numerator // (k - 1)
    u = r + k - 1
    b = q + k
    n = choose(q, 2) + r
    H = choose(b, 2) + 1
    tau = H - n
    identity_left = choose(b - 1, 2) + 2 - n
    assert (h, q, u, b) == (117_440_512, 78_302_495, 26_469, 78_302_499)
    assert identity_left == 2*h
    assert 0 <= r < q and 0 <= u < q + 1 and 5 <= b < h

    # Full unnormalized orbit: start from the literal adjacent rank-two
    # values and apply the canonical engine before any leading-term removal.
    left2, right2 = n, n + b - 1
    shadow_left2, shadow_right2 = U(left2, 2), U(right2, 2)
    gamma3 = shadow_right2 - shadow_left2 - H
    left3 = shadow_left2 - tau + 1
    right3 = shadow_right2 - tau
    gamma4_full = U(right3, 3) - U(left3, 3) - shadow_left2 - 1
    left4 = U(left3, 3) - tau + 1
    right4 = U(right3, 3) - tau
    gamma5_full = U(right4, 4) - U(left4, 4) - U(left3, 3) - 1

    # Independent normalized chart from the exact residue formulas.
    alpha = choose(r + 1, 2) - k*q - choose(k, 2)
    beta = alpha + choose(u, 2) - choose(r, 2) - 1
    assert alpha >= 0 and beta >= 0
    assert left3 == choose(q, 3) + alpha
    assert right3 == choose(q + 1, 3) + beta
    assert alpha < choose(q, 2) and beta < choose(q + 1, 2)

    p = U(alpha, 2) - tau + 1
    v = U(beta, 2) - tau
    assert p >= 0 and v >= 0
    assert left4 == choose(q, 4) + p
    assert right4 == choose(q + 1, 4) + v
    assert p < choose(q, 3) and v < choose(q + 1, 3)
    transition = "++ -> ++"

    e = v - p
    gamma4_chart = U(beta, 2) - U(alpha, 2) - alpha - tau
    p_free_margin = U(e, 3) - U(alpha, 2) - 1
    gamma5_tail = U(v, 3) - U(p, 3) - U(alpha, 2) - 1

    assert gamma3 == -313_130_586
    assert gamma4_full == gamma4_chart == -13_858_416
    assert (alpha, beta) == (37_027_825, 37_107_225)
    assert (p, v, e) == (105_881_285_695, 106_217_638_624, 336_352_929)
    assert p_free_margin == -136_419_183
    assert gamma5_tail == gamma5_full == 859_354_068_710

    # M303's nested threshold, recomputed rather than taken from its output.
    alpha_scale = greatest_top(alpha, 2, None)
    assert choose(alpha_scale, 2) <= alpha < choose(alpha_scale + 1, 2)
    envelope_top = 4
    while choose(envelope_top, 4) < choose(alpha_scale + 1, 3):
        envelope_top += 1
    m303_threshold = choose(envelope_top, 3)
    m303_gap = e - m303_threshold
    assert m303_gap < 0

    selected_words = {
        name: [list(pair) for pair in macaulay_word(value, rank)]
        for name, value, rank in (
            ("n", n, 2), ("n_plus_b_minus_1", right2, 2),
            ("left3", left3, 3), ("right3", right3, 3),
            ("alpha", alpha, 2), ("beta", beta, 2),
            ("p", p, 3), ("v", v, 3), ("e", e, 3),
            ("left4", left4, 4), ("right4", right4, 4),
        )
    }

    print(json.dumps({
        "schema": "amra.erdos776.gpp-pfree-counterexample-independent-audit.v1",
        "engine": "new greedy canonical Macaulay engine; no author-verifier import",
        "parameters": {"j": j, "h": h, "q": q, "k": k, "r": r, "u": u, "b": b},
        "actuality": {
            "dyadic_left": identity_left,
            "dyadic_right": 2*h,
            "identity": "C(b-1,2)+2-(C(q,2)+r)=2h",
            "range_checks": True
        },
        "transition": {
            "first": "++",
            "second": "++",
            "combined": transition,
            "alpha": alpha,
            "beta": beta,
            "p": p,
            "v": v,
            "e": e
        },
        "surpluses": {
            "gamma3": gamma3,
            "gamma4_full": gamma4_full,
            "gamma4_chart": gamma4_chart,
            "p_free_margin": p_free_margin,
            "gamma5_normalized": gamma5_tail,
            "gamma5_full_unnormalized_orbit": gamma5_full,
            "base_cross_term_gain": gamma5_tail - p_free_margin
        },
        "m303": {
            "alpha_scale": alpha_scale,
            "least_t_with_C_t_4_at_least_C_alpha_scale_plus_1_3": envelope_top,
            "required_e_threshold": m303_threshold,
            "actual_e_minus_threshold": m303_gap,
            "killed": True
        },
        "canonical_words": selected_words,
        "verdict": "pass_scoped_counterexample_to_universal_p_free_coverage_gate_and_M303",
        "scope": {
            "refutes": [
                "the assertion that every actual G++ state passes U3(e)>=U2(alpha)+1",
                "M303-nested-binomial-envelope"
            ],
            "does_not_refute": [
                "the conditional implication from the p-free inequality when its antecedent holds",
                "exact base-retaining rank-five recovery",
                "the public Erdos-776 problem"
            ],
            "reason_exact_rank5_survives": "the independently reconstructed exact gamma5 is strictly positive"
        },
        "lean_used": False,
        "public_problem_changed": False
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
