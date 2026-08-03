#!/usr/bin/env python3
"""Independent carry-aware search for the base-leading top-index candidate.

This file deliberately implements the actual dyadic normal form and Macaulay
arithmetic from scratch.  It does not import any campaign probe.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path


def C(n: int, k: int) -> int:
    return math.comb(n, k) if n >= k >= 0 else 0


def largest_choose_leq(n: int, rank: int, upper: int | None = None) -> int:
    """Largest t (also t < upper when supplied) with C(t,rank) <= n."""
    lo = rank - 1
    hi = max(rank, 2 * rank)
    if upper is not None:
        hi = upper - 1
    else:
        while C(hi, rank) <= n:
            hi *= 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if C(mid, rank) <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def word_and_upper(n: int, rank: int) -> tuple[tuple[int, ...], int]:
    assert n >= 0 and rank >= 1
    rem = n
    upper = None
    word: list[int] = []
    shadow = 0
    for s in range(rank, 0, -1):
        t = largest_choose_leq(rem, s, upper)
        word.append(t)
        rem -= C(t, s)
        shadow += C(t, s + 1)
        upper = t
    assert rem == 0
    return tuple(word), shadow


@dataclass(frozen=True)
class State:
    j: int
    k: int
    r: int
    q: int
    alpha: int
    beta: int
    tau: int
    p: int
    v: int
    gamma3: int
    gamma4: int
    gamma5: int
    a: int
    c: int
    d: int
    wa: tuple[int, ...]
    wp: tuple[int, ...]
    wv: tuple[int, ...]
    candidate_margin: int


def actual_state(j: int, k: int, r: int) -> State | None:
    h = 112 << (j - 1)
    s = k - 1
    numerator = 2 * h - C(s, 2) - 2 + r
    if numerator % s:
        return None
    q = numerator // s
    u = r + s
    b = q + k
    if not (q >= 2 and 0 <= r < q and 0 <= u < q + 1 and 5 <= b < h):
        return None

    alpha = C(r + 1, 2) - k * q - C(k, 2)
    beta = alpha + C(u, 2) - C(r, 2) - 1
    if alpha < 0 or beta < 0:
        return None
    wa, ua = word_and_upper(alpha, 2)
    wb, ub = word_and_upper(beta, 2)
    tau = k * q + C(k, 2) + 1 - r
    p = ua - tau + 1
    v = ub - tau
    if p < 0 or v < 0:
        return None
    wp, up = word_and_upper(p, 3)
    wv, uv = word_and_upper(v, 3)

    # The first failed rank is part of the actual c=1 target normal form.
    gamma3 = beta - alpha - tau
    gamma4 = ub - ua - alpha - tau
    gamma5 = uv - up - ua - 1
    a, c, d = wa[0], wp[0], wv[0]
    margin = C(d, 4) - C(c + 1, 4) - C(a + 1, 3)
    return State(j, k, r, q, alpha, beta, tau, p, v, gamma3, gamma4,
                 gamma5, a, c, d, wa, wp, wv, margin)


def compatible_range(j: int, k: int) -> tuple[int, int, int] | None:
    """Return residue and inclusive compatible-index interval for legal r."""
    h = 112 << (j - 1)
    s = k - 1
    base = 2 * h - C(s, 2) - 2
    residue = (-base) % s
    # Obtain safe bounds algebraically, then trim endpoints exactly.
    max_r = (base - s * (s - 1) - 1) // (s - 1)
    max_r = min(max_r, (h - k - 1) * s - base)
    if max_r < residue:
        return None
    mlo, mhi = 0, (max_r - residue) // s
    while mlo <= mhi and actual_legal_only(j, k, residue + mlo * s) is None:
        mlo += 1
    while mhi >= mlo and actual_legal_only(j, k, residue + mhi * s) is None:
        mhi -= 1
    return (residue, mlo, mhi) if mlo <= mhi else None


def actual_legal_only(j: int, k: int, r: int) -> int | None:
    h = 112 << (j - 1)
    s = k - 1
    num = 2 * h - C(s, 2) - 2 + r
    if num % s:
        return None
    q = num // s
    if q >= 2 and 0 <= r < q and r + s < q + 1 and 5 <= q + k < h:
        return q
    return None


def raw_values(j: int, k: int, r: int) -> tuple[int, int, int, int] | None:
    q = actual_legal_only(j, k, r)
    if q is None:
        return None
    alpha = C(r + 1, 2) - k * q - C(k, 2)
    if alpha < 0:
        return (alpha, -1, -1, -1)
    u = r + k - 1
    beta = alpha + C(u, 2) - C(r, 2) - 1
    _, ua = word_and_upper(alpha, 2)
    _, ub = word_and_upper(beta, 2)
    tau = k * q + C(k, 2) + 1 - r
    p = ua - tau + 1
    v = ub - tau
    gamma4 = ub - ua - alpha - tau
    return alpha, p, v, gamma4


def first_true(lo: int, hi: int, predicate) -> int | None:
    if lo > hi or not predicate(hi):
        return None
    while lo < hi:
        mid = (lo + hi) // 2
        if predicate(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def state_dict(s: State) -> dict:
    return {
        "j": s.j, "k": s.k, "r": s.r, "q": s.q,
        "alpha": s.alpha, "beta": s.beta, "tau": s.tau,
        "p": s.p, "v": s.v, "gamma3": s.gamma3,
        "gamma4": s.gamma4, "gamma5": s.gamma5,
        "a": s.a, "c": s.c, "d": s.d,
        "alpha_word": s.wa, "p_word": s.wp, "v_word": s.wv,
        "candidate_margin": s.candidate_margin,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--max-j", type=int, default=72)
    ap.add_argument("--max-k", type=int, default=320)
    ap.add_argument("--radius", type=int, default=384)
    ap.add_argument("--seed", type=int, default=776043)
    args = ap.parse_args()
    started = time.time()
    rng = random.Random(args.seed)

    tested: set[tuple[int, int, int]] = set()
    accepted = 0
    target = 0
    carry_adjacent_target = 0
    fibres = 0
    target_fibres = 0
    negative: list[State] = []
    minimum: State | None = None
    gamma5_min: State | None = None
    partitions: dict[str, dict[str, int | None]] = {}

    def check(j: int, k: int, residue: int, m: int, mlo: int, mhi: int,
              carry_adjacent: bool = False) -> None:
        nonlocal accepted, target, carry_adjacent_target, minimum, gamma5_min
        if not (mlo <= m <= mhi) or (j, k, m) in tested:
            return
        tested.add((j, k, m))
        r = residue + m * (k - 1)
        st = actual_state(j, k, r)
        if st is None:
            return
        accepted += 1
        if not (st.gamma3 < 0 and st.gamma4 < 0):
            return
        target += 1
        if carry_adjacent:
            carry_adjacent_target += 1
        if minimum is None or st.candidate_margin < minimum.candidate_margin:
            minimum = st
        if gamma5_min is None or st.gamma5 < gamma5_min.gamma5:
            gamma5_min = st
        if st.candidate_margin < 0 and len(negative) < 20:
            negative.append(st)
        if st.d <= st.c + 1:
            key = "forbidden_or_counterexample_cell:d<=c+1"
        elif st.d >= max(st.a, st.c) + 2:
            key = "easy_single_cap_cell:d>=max(a,c)+2"
        elif st.c < st.a and st.c + 2 <= st.d <= st.a + 1:
            key = "hard_multi_cap_cell:c<a_and_c+2<=d<=a+1"
        else:
            key = "residual_order_cell"
        row = partitions.setdefault(key, {"count": 0, "min_margin": None})
        row["count"] = int(row["count"]) + 1
        old = row["min_margin"]
        row["min_margin"] = st.candidate_margin if old is None else min(int(old), st.candidate_margin)

    # Sparse exact grid plus sign-wall and canonical-carry neighborhoods.
    for j in list(range(5, args.max_j + 1)) + [80, 96, 112, 128]:
        h = 112 << (j - 1)
        for k in range(4, min(args.max_k, math.isqrt(2 * h) - 1) + 1):
            cr = compatible_range(j, k)
            if cr is None:
                continue
            fibres += 1
            residue, mlo, mhi = cr
            s = k - 1

            def rv(m: int):
                return raw_values(j, k, residue + m * s)

            # alpha and p are eventually strictly increasing in this region;
            # binary search is used only to centre windows, never for exhaustion.
            ma = first_true(mlo, mhi, lambda m: rv(m)[0] >= 0)
            mp = None if ma is None else first_true(ma, mhi, lambda m: rv(m)[1] >= 0)
            if mp is None:
                continue

            centres = {mp, ma if ma is not None else mp, mhi}
            span = mhi - mp
            # Logarithmic rays find narrow/far gamma4-negative bands without
            # presuming gamma4 monotonicity.
            off = 0
            while off <= span:
                centres.add(mp + off)
                off = 1 if off == 0 else 2 * off
            for den in (16, 12, 8, 6, 4, 3, 2):
                centres.add(mp + span // den)
            for _ in range(8):
                centres.add(rng.randint(mp, mhi))

            local_ms: set[int] = set()
            for centre in centres:
                lo = max(mp, centre - args.radius)
                hi = min(mhi, centre + args.radius)
                local_ms.update(range(lo, hi + 1))

            # First pass records exact word transitions.  A transition means
            # at least one canonical digit changed; resets/decreases in a lower
            # digit are genuine carry boundaries.  Test both sides plus radius 2.
            previous: tuple[int, tuple[int, ...], tuple[int, ...], tuple[int, ...]] | None = None
            carry_ms: set[int] = set()
            fibre_had_target = False
            for m in sorted(local_ms):
                st = actual_state(j, k, residue + m * s)
                if st is not None:
                    sig = (m, st.wa, st.wp, st.wv)
                    if previous is not None and m == previous[0] + 1:
                        old_words = previous[1:]
                        new_words = sig[1:]
                        reset = any(any(nw[t] < ow[t] for t in range(1, len(ow)))
                                    for ow, nw in zip(old_words, new_words))
                        top_change = any(ow[0] != nw[0] for ow, nw in zip(old_words, new_words))
                        if reset or top_change:
                            carry_ms.update(range(m - 2, m + 3))
                    previous = sig
                check(j, k, residue, m, mlo, mhi)
                if st is not None and st.gamma3 < 0 and st.gamma4 < 0:
                    fibre_had_target = True
            for m in carry_ms:
                check(j, k, residue, m, mlo, mhi, carry_adjacent=True)
            if fibre_had_target:
                target_fibres += 1

    result = {
        "schema": "amra.evidence.base-leading-top-index-search.v1",
        "claim_tested": "For actual (++ -> ++) states with gamma3<0 and gamma4<0, C(d,4)-C(c+1,4) >= C(a+1,3).",
        "independence": "Fresh normal-form and Macaulay implementation; imports no existing campaign probe.",
        "parameters": vars(args),
        "counts": {
            "fibres_considered": fibres,
            "fibres_with_target_in_sample": target_fibres,
            "distinct_compatible_points": len(tested),
            "actual_double_positive_points": accepted,
            "target_points": target,
            "carry_adjacent_target_points_newly_added": carry_adjacent_target,
            "negative_candidate_points": len(negative),
        },
        "minimum_candidate_margin": None if minimum is None else state_dict(minimum),
        "minimum_gamma5": None if gamma5_min is None else state_dict(gamma5_min),
        "counterexamples": [state_dict(s) for s in negative],
        "top_gap_partitions": dict(sorted(partitions.items())),
        "elapsed_seconds": time.time() - started,
        "scope_warning": "Finite carry-aware sampling only; absence is not a proof and binary centres do not exhaust fibres.",
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
