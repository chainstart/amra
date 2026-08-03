#!/usr/bin/env python3
"""Independent guard for the gamma-four feedback reduction.

The exact-state part checks proved implications.  The rectangular kernel
check is explicitly finite and proves no infinite absence statement.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import comb, isqrt
from pathlib import Path


def C(n: int, k: int) -> int:
    return comb(n, k) if n >= k >= 0 else 0


def top(value: int, rank: int) -> int:
    lo, hi = rank - 1, max(rank, 2)
    while C(hi, rank) <= value:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if C(mid, rank) <= value:
            lo = mid
        else:
            hi = mid
    return lo


def first_tri_ge(value: int) -> int:
    r = max(1, (1 + isqrt(1 + 8 * value)) // 2)
    while C(r, 2) < value:
        r += 1
    while r > 1 and C(r - 1, 2) >= value:
        r -= 1
    return r


def first_tri_gt(value: int) -> int:
    return first_tri_ge(value + 1)


def D_threshold(a: int, c: int) -> int:
    d = c + 2
    while C(d, 4) - C(c + 1, 4) < C(a + 1, 3):
        d += 1
    return d


def A_star(a: int, c: int) -> int:
    d = D_threshold(a, c)
    A = a + 2
    while C(c, 3) + C(A, 3) - C(a + 1, 3) < C(d, 3):
        A += 1
    return A


def rho(a: int, c: int) -> int:
    gamma_bound = first_tri_ge(a * a + 3 * a)
    p_bound = first_tri_gt(C(a + 1, 3) - C(c + 1, 3))
    return max(gamma_bound, p_bound)


def B_threshold(a: int, c: int) -> int:
    return top(C(a, 2) + 3 * rho(a, c) + 2, 2)


def ceil_fourth_root(value: int) -> int:
    t = isqrt(isqrt(value))
    while t**4 < value:
        t += 1
    while t > 0 and (t - 1)**4 >= value:
        t -= 1
    return t


def exact_state_guard(max_r: int) -> dict[str, object]:
    checked = 0
    minimum_feedback_slack = None
    witness = None
    for r in range(4, max_r + 1):
        R = C(r, 2)
        for alpha in range(1, R):
            a = top(alpha, 2)
            e = alpha - C(a, 2)
            for s in range(3, 9):
                delta = s * r + C(s, 2) - 1
                beta = alpha + delta
                if beta > R:
                    continue
                A = top(beta, 2)
                E = beta - C(A, 2)
                p = C(a + 1, 3) + C(e + 1, 2) - R
                v = C(A, 3) + C(E, 2) - R + C(a, 2) + e - 1
                gamma4 = v - p - R
                if not (p > 0 and v > 0 and gamma4 <= -1):
                    continue
                checked += 1
                exact_gamma = (
                    C(A, 3) - C(a + 1, 3) + C(E, 2) - C(e, 2)
                    + C(a, 2) - 1 - R
                )
                assert gamma4 == exact_gamma
                assert A >= a + s
                feedback = C(a + s, 3) - C(a + 1, 3) + a - 1
                assert R >= feedback >= a * a + 3 * a
                c = top(p, 3)
                assert R > C(a + 1, 3) - C(c + 1, 3)
                assert r >= rho(a, c)
                B = B_threshold(a, c)
                assert A >= B
                slack = R - feedback
                if minimum_feedback_slack is None or slack < minimum_feedback_slack:
                    minimum_feedback_slack = slack
                    witness = {
                        "r": r, "s": s, "a": a, "e": e, "A": A,
                        "E": E, "c": c, "gamma4": gamma4,
                        "feedback_slack": slack, "B": B,
                    }
    return {
        "max_r": max_r,
        "exact_relaxed_s_ge_3_states": checked,
        "minimum_feedback_slack": minimum_feedback_slack,
        "minimum_feedback_witness": witness,
    }


def finite_kernel_guard(max_a: int) -> dict[str, object]:
    checked = 0
    failures = 0
    first_failure = None
    minimum_gap = None
    minimum_witness = None
    active = {"gamma": 0, "p": 0, "tie": 0}
    high_half_certificate_failures = []
    low_half_fourth_root_failures = []
    for a in range(3, max_a + 1):
        rg = first_tri_ge(a * a + 3 * a)
        for c in range(3, a + 1):
            rp = first_tri_gt(C(a + 1, 3) - C(c + 1, 3))
            active["tie" if rg == rp else "gamma" if rg > rp else "p"] += 1
            B = B_threshold(a, c)
            astar = A_star(a, c)
            gap = B - astar
            checked += 1
            if minimum_gap is None or gap < minimum_gap:
                minimum_gap = gap
                minimum_witness = {
                    "a": a, "c": c, "rho": max(rg, rp),
                    "B": B, "A_star": astar, "gap": gap,
                }
            if gap < 0:
                failures += 1
                if first_failure is None:
                    first_failure = {
                        "a": a, "c": c, "rho": max(rg, rp),
                        "B": B, "A_star": astar, "gap": gap,
                    }
            if 2 * c >= a:
                q0 = (C(a + 1, 3) + C(c + 1, 3) - 1) // C(c + 1, 3)
                D0 = c + 1 + q0
                assert q0 <= 9
                assert C(D0, 4) - C(c + 1, 4) >= C(a + 1, 3)
                assert D_threshold(a, c) <= D0
                certificate_gap = (
                    C(c, 3) + C(B, 3) - C(a + 1, 3) - C(D0, 3)
                )
                if certificate_gap < 0:
                    high_half_certificate_failures.append({
                        "a": a, "c": c, "q0": q0, "B": B,
                        "D0": D0, "certificate_gap": certificate_gap,
                    })
            else:
                X = (c + 1)**4 + 4 * (a + 1)**3
                L = max(c + 2, 3 + ceil_fourth_root(X))
                assert C(L, 4) - C(c + 1, 4) >= C(a + 1, 3)
                assert D_threshold(a, c) <= L
                certificate_gap = (
                    C(c, 3) + C(B, 3) - C(a + 1, 3) - C(L, 3)
                )
                if certificate_gap < 0:
                    low_half_fourth_root_failures.append({
                        "a": a, "c": c, "B": B, "L": L,
                        "D": D_threshold(a, c),
                        "certificate_gap": certificate_gap,
                    })
    return {
        "domain": {"a": [3, max_a], "c": "3..a"},
        "pairs_checked": checked,
        "active_rho_branch": active,
        "failures": failures,
        "first_failure": first_failure,
        "minimum_gap": minimum_gap,
        "minimum_witness": minimum_witness,
        "high_half_explicit_D_certificate": {
            "failures": len(high_half_certificate_failures),
            "last_failure": (
                high_half_certificate_failures[-1]
                if high_half_certificate_failures else None
            ),
            "scope_warning": (
                "finite observation only; q0<=9 is proved, but eventual "
                "success of the certificate is not yet proved"
            ),
        },
        "low_half_fourth_root_certificate": {
            "failures": len(low_half_fourth_root_failures),
            "failure_points": [
                [row["a"], row["c"]]
                for row in low_half_fourth_root_failures
            ],
            "last_failure": (
                low_half_fourth_root_failures[-1]
                if low_half_fourth_root_failures else None
            ),
            "scope_warning": (
                "D<=L is proved; finite eventual success of the resulting "
                "target certificate is not an infinite proof"
            ),
        },
        "scope_warning": "finite rectangular check only; not an infinite proof",
    }


def high_half_proof_guard() -> dict[str, object]:
    base_pairs = 0
    base_failures = []
    for a in range(3, 69):
        for c in range(max(3, (a + 1) // 2), a + 1):
            base_pairs += 1
            gap = B_threshold(a, c) - A_star(a, c)
            if gap < 0:
                base_failures.append({"a": a, "c": c, "gap": gap})
    assert base_pairs == 1219
    assert not base_failures

    lambdas = {
        3: Fraction(4, 5), 4: Fraction(7, 10),
        5: Fraction(2, 3), 6: Fraction(3, 5),
        7: Fraction(14, 25), 8: Fraction(8, 15),
    }
    polynomial_checks = {}
    a = 69
    for q, lam in lambdas.items():
        x = lam * a
        domain_margin_times_6 = (
            (q - 1) * (x + 1) * x * (x - 1)
            - (a + 1) * a * (a - 1)
        )
        # Polynomial extension of E_q to rational c=x.
        def poly_C3(z: Fraction | int) -> Fraction:
            return Fraction(z * (z - 1) * (z - 2), 6)
        E_lower = (
            poly_C3(x) + C(a + 4, 3) - C(a + 1, 3)
            - poly_C3(x + q + 1)
        )
        assert domain_margin_times_6 > 0
        assert E_lower > 0
        polynomial_checks[str(q)] = {
            "lambda": str(lam),
            "domain_margin_times_6_at_69": str(domain_margin_times_6),
            "E_lower_at_69": str(E_lower),
        }

    assert Fraction(70 * 70 - 62 * 70 - 464, 4) > 0
    return {
        "theorem_scope": "all a>=3 and 2c>=a",
        "exact_base": {"a": [3, 68], "pairs": base_pairs, "failures": 0},
        "polynomial_branches_at_first_a": polynomial_checks,
        "q9_first_even_a": 70,
        "q9_E_at_first_even_a": str(Fraction(70 * 70 - 62 * 70 - 464, 4)),
        "verdict": "high-half chamber closed by finite base plus symbolic polynomial branches",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-r", type=int, default=180)
    ap.add_argument("--max-a", type=int, default=3000)
    ap.add_argument("--output")
    args = ap.parse_args()
    result = {
        "schema": "amra.erdos776.gamma4-feedback-reduction-audit.v1",
        "proved_reduction": (
            "Every relaxed s>=3 state has C(r,2)>=a^2+3a and "
            "r>=rho(a,c), hence A>=B(a,c)."
        ),
        "exact_state_guard": exact_state_guard(args.max_r),
        "finite_two_variable_kernel": finite_kernel_guard(args.max_a),
        "high_half_infinite_closure": high_half_proof_guard(),
        "verdict": (
            "reduction and high-half 2c>=a closure verified; low-half 2c<a "
            "remains an unproved infinite discrete kernel"
        ),
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
