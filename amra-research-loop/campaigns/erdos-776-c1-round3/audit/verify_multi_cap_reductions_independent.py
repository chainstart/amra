#!/usr/bin/env python3
"""Independent guards for the multi-cap carry-cell reductions.

Uses only Macaulay canonical-word definitions and the stated complement
constraints.  It proves no absence result beyond its finite loop bounds.
"""

from __future__ import annotations

from collections import defaultdict
from math import comb
import json


def C(n: int, k: int) -> int:
    return comb(n, k) if n >= k >= 0 else 0


def top(value: int, rank: int) -> int:
    assert value >= 0
    lo, hi = rank - 1, rank
    while C(hi, rank) <= value:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if C(mid, rank) <= value:
            lo = mid
        else:
            hi = mid
    return lo


def word2(value: int) -> tuple[int, int]:
    a = top(value, 2)
    e = value - C(a, 2)
    assert 0 <= e < a
    return a, e


def U2(value: int) -> int:
    a, e = word2(value)
    return C(a, 3) + C(e, 2)


def D_threshold(a: int, c: int) -> int:
    target = C(a + 1, 3)
    d = c + 2
    while C(d, 4) - C(c + 1, 4) < target:
        d += 1
    return d


def A_star(a: int, c: int) -> int:
    d = D_threshold(a, c)
    target = C(d, 3)
    A = a + 2
    while C(c, 3) + C(A, 3) - C(a + 1, 3) < target:
        A += 1
    return A


def state(r: int, s: int, a: int, e: int) -> dict[str, int]:
    R = C(r, 2)
    alpha = C(a, 2) + e
    delta = s*r + C(s, 2) - 1
    beta = alpha + delta
    A, E = word2(beta)
    K = delta + C(a, 2) - C(A, 2)
    tau = R - alpha + 1
    p = U2(alpha) - tau + 1
    v = U2(beta) - tau
    gamma4 = v - p - R
    return {
        "R": R, "alpha": alpha, "beta": beta, "A": A, "E": E,
        "K": K, "tau": tau, "p": p, "v": v, "gamma4": gamma4,
    }


def relaxed(state_: dict[str, int]) -> bool:
    return (
        state_["p"] > 0
        and state_["v"] > 0
        and state_["beta"] <= state_["R"]
        and state_["gamma4"] <= -1
    )


def finite_relaxed_scan(max_r: int = 180, max_s: int = 8):
    totals = {s: {"admissible": 0, "failures": 0, "first_failure": None} for s in range(1, max_s + 1)}
    for r in range(4, max_r + 1):
        R = C(r, 2)
        # alpha<R follows from beta>alpha and beta<=R; enumerate its unique
        # rank-two canonical words directly.
        for alpha in range(1, R):
            a, e = word2(alpha)
            for s in range(1, max_s + 1):
                st = state(r, s, a, e)
                if not relaxed(st):
                    continue
                totals[s]["admissible"] += 1
                c = top(st["p"], 3)
                d = top(st["v"], 3)
                margin = C(d, 4) - C(c + 1, 4) - C(a + 1, 3)
                if margin < 0:
                    totals[s]["failures"] += 1
                    if totals[s]["first_failure"] is None:
                        totals[s]["first_failure"] = {
                            "r": r, "s": s, "a": a, "e": e,
                            "alpha": alpha, "beta": st["beta"],
                            "tau": st["tau"], "p": st["p"], "v": st["v"],
                            "c": c, "d": d, "gamma4": st["gamma4"], "margin": margin,
                        }
    return totals


def fixed_cell_guards() -> dict[str, int]:
    cells: dict[tuple[int, int, int, int, int], list[int]] = defaultdict(list)
    difference_checks = 0
    carry_checks = 0
    top_branch_checks = 0

    for r in range(4, 61):
        R = C(r, 2)
        for s in range(1, 7):
            for alpha in range(1, R):
                a, e = word2(alpha)
                st = state(r, s, a, e)
                A, E, K = st["A"], st["E"], st["K"]
                assert E == e + K
                assert st["tau"] == R - C(a, 2) - e + 1
                assert st["p"] == C(a + 1, 3) + C(e + 1, 2) - R
                assert st["v"] == C(A, 3) + C(E, 2) - R + C(a, 2) + e - 1
                carry_checks += 1

                if e + 1 < a:
                    nxt = state(r, s, a, e + 1)
                    if nxt["A"] == A:
                        assert nxt["p"] - st["p"] == e + 1
                        assert nxt["v"] - st["v"] == E + 1
                        assert nxt["gamma4"] - st["gamma4"] == K
                        difference_checks += 1

                if relaxed(st):
                    c = top(st["p"], 3)
                    cells[(r, s, a, A, c)].append(e)
                    if s >= 2:
                        assert A >= a + s
                        lower = C(c, 3) + C(A, 3) - C(a + 1, 3)
                        assert st["v"] >= lower
                        astar = A_star(a, c)
                        if A >= astar:
                            assert st["v"] >= C(D_threshold(a, c), 3)
                        if C(a, 2) + s*r + C(s, 2) - 1 >= C(astar, 2):
                            assert A >= astar
                        top_branch_checks += 1

    interval_cells = endpoint_cells = 0
    for (r, s, a, A, c), values in cells.items():
        values = sorted(values)
        assert values == list(range(values[0], values[-1] + 1))
        interval_cells += 1
        e0 = values[0]
        st = state(r, s, a, e0)
        K = st["K"]

        def previous_fails_lower(expression: str) -> bool:
            if e0 == 0:
                return True
            prev = state(r, s, a, e0 - 1)
            if expression == "p":
                return prev["p"] < C(c, 3)
            if expression == "v":
                return prev["v"] < 1
            if expression == "gamma":
                return prev["gamma4"] > -1
            raise AssertionError(expression)

        endpoint_types = [
            e0 == 0,
            st["E"] == 0,
            previous_fails_lower("p"),
            previous_fails_lower("v"),
            K < 0 and previous_fails_lower("gamma"),
        ]
        assert any(endpoint_types)
        H = C(D_threshold(a, c), 3)
        assert (all(state(r, s, a, e)["v"] >= H for e in values)) == (st["v"] >= H)
        endpoint_cells += 1

    return {
        "carry_identity_states": carry_checks,
        "fixed_A_difference_pairs": difference_checks,
        "interval_cells": interval_cells,
        "five_endpoint_cells": endpoint_cells,
        "top_branch_states_s_ge_2": top_branch_checks,
    }


def counterfamily_guards() -> dict[str, object]:
    first_family = None
    for a in range(6, 501):
        s, r, e = 1, a + 2, a - 1
        st = state(r, s, a, e)
        c, d = top(st["p"], 3), top(st["v"], 3)
        assert st["tau"] == a + 3
        assert st["beta"] == C(r, 2) - 1
        assert st["beta"] - st["R"] == -1
        assert c == a and d == a + 1
        assert st["gamma4"] == -a - 3
        assert C(d, 4) - C(c + 1, 4) - C(a + 1, 3) == -C(a + 1, 3)
        if first_family is None:
            first_family = {"a": a, **st, "c": c, "d": d}

    boundary_checks = 0
    first_invalid_extension = None
    for s in range(1, 9):
        for a in range(max(s, 1), 501):
            r, e = a + s + 1, a - s
            st = state(r, s, a, e)
            corrected_beta = C(r, 2) - 1 + s*(s - 1)
            corrected_tau = a*s + (s*s + 3*s)//2 + 1
            corrected_p = C(a + 1, 3) - s*(2*a + 1)
            assert st["beta"] == corrected_beta
            assert st["tau"] == corrected_tau
            assert st["p"] == corrected_p
            if s == 1:
                assert st["beta"] == C(r, 2) - 1
            else:
                assert st["beta"] > C(r, 2)
                if first_invalid_extension is None:
                    first_invalid_extension = {
                        "a": a, "s": s, "r": r, "e": e,
                        "beta": st["beta"], "claimed_beta": C(r, 2) - 1,
                        "excess_over_claim": s*(s - 1),
                    }
            boundary_checks += 1
    return {
        "s1_family_checked_a": [6, 500],
        "first_s1_member": first_family,
        "gamma3_wall_checks": boundary_checks,
        "gamma3_wall_extension_verdict": "refuted for every s>=2: beta=C(r,2)-1+s(s-1)>C(r,2)",
        "first_invalid_extension": first_invalid_extension,
    }


def legality_guards() -> dict[str, object]:
    failures = []
    checked = 0
    for j in range(1, 11):
        h = 112 * 2**(j - 1)
        for s in (1, 2):
            for r in range(1, 400):
                numerator = 2*h - C(s, 2) - 2 + r
                if numerator % s:
                    continue
                q = numerator // s
                checked += 1
                if q + s + 1 < h:
                    failures.append((j, h, s, r, q))
    assert not failures
    return {
        "finite_guard_cases": checked,
        "symbolic_s1": "q=2h-2+r, so q+2>h",
        "symbolic_s2": "q=h+(r-3)/2, so q+3=h+(r+3)/2>h for actual positive r",
        "conclusion": "q+s+1<h forces s>=3; this does not say every s>=3 tuple is legal",
    }


def main() -> None:
    scan = finite_relaxed_scan()
    assert scan[1]["admissible"] == 876_058 and scan[1]["failures"] == 750_926
    assert scan[2]["admissible"] == 158_658 and scan[2]["failures"] == 0
    assert scan[3]["admissible"] == 17_085 and scan[3]["failures"] == 0
    assert all(scan[s]["admissible"] == 0 for s in range(4, 9))
    print(json.dumps({
        "schema": "amra.erdos776.multi-cap-reductions-independent-audit.v1",
        "engine": "independent canonical-word reconstruction; no author checker import",
        "finite_relaxed_scan": {str(s): data for s, data in scan.items()},
        "fixed_cell_guards": fixed_cell_guards(),
        "counterfamily_guards": counterfamily_guards(),
        "actual_legality": legality_guards(),
        "proved_reductions": [
            "complement and canonical-word identities",
            "exact D(a,c) top-cell equivalence",
            "s=1 infinite counterfamily for every a>=6",
            "actual inequality q+s+1<h forces s>=3",
            "fixed-A differences, interval intersection and five possible lower endpoints",
            "stronger upstream carry gap A>=a+s for s>=2 and the top-only sufficient branch",
        ],
        "conjectural_or_finite_only": [
            "relaxed carry theorem for every s>=2",
            "uniform success of all five endpoint branches",
            "absence of s=2 or s=3 failures beyond the finite scan",
            "global/public Erdos-776 closure",
        ],
        "refuted_claims": [
            "the proposed gamma3-wall extension has beta=C(r,2)-1 for s>=2",
            "its downstream tau, p, stable-top margin and gamma4 formulas as stated",
        ],
        "scope": "exact reductions plus bounded guards; no all-parameter absence inference",
        "public_status_changed": False,
        "lean_used": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
