#!/usr/bin/env python3
"""Independent exact guard for CRITICAL_ELLIPSE_FINAL_SCRATCH.md.

No author verifier or helper is imported.
"""

from __future__ import annotations

from math import comb

import sympy as sp


def u2(n: int) -> int:
    v = 1
    while comb(v + 1, 2) <= n:
        v += 1
    rho = n - comb(v, 2)
    assert 0 <= rho < v
    return comb(v, 3) + comb(rho, 2)


def lam(q: int, d: int) -> int:
    return comb(q, 3) - u2(comb(q, 2) - d)


def depth(q: int, value: int) -> tuple[int, int]:
    s = 0
    while s * q - comb(s + 1, 2) < value:
        s += 1
    rho = s * q - comb(s + 1, 2) - value
    assert 0 <= rho < q - s
    return s, rho


def symbolic_checks() -> None:
    q, u, h = sp.symbols("q u h", integer=True)
    rd = (
        2 * h * q - h**2 - 2 * h * u - 7 * h
        - 2 * u**2 - 12 * u - 18
    ) / 2
    re = (
        2 * h * q - h**2 - 2 * h * u - 3 * h
        - u**2 - 9 * u - 12
    ) / 2
    assert sp.expand(re - rd - (2*h + 2*h + 2 + 2*u + 4 + u**2 + u)/2) == 0

    expected = {
        1: (4*q**2 + 4*q*u**2 - 4*q*u - 12*q - 3*u**4
            - 34*u**3 - 141*u**2 - 318*u - 328) / 8,
        2: (4*q**2 + 8*q*u**2 + 8*q*u + 44*q - 3*u**4
            - 38*u**3 - 181*u**2 - 506*u - 656) / 8,
    }
    for correction in (1, 2):
        vd = q - u - 3 - correction
        ve = q - u - 1 - correction
        rd_h = rd.subs(h, correction)
        re_h = re.subs(h, correction)
        gamma = (
            sp.binomial(ve, 3) - sp.binomial(vd, 3)
            + sp.binomial(re_h, 2) - sp.binomial(rd_h, 2)
            - sp.binomial(q - 1, 2) - 1
        )
        assert sp.simplify(sp.expand_func(gamma) - expected[correction]) == 0


def finite_guard() -> dict[str, int]:
    rows = 0
    m_ge_3 = 0
    rigid_m_2 = 0
    for q in range(12, 181):
        for k in range(1, min(q, 12)):
            for u in range(0, min(q, 28)):
                d = ((u + 2*k + 1) * (2*q + u + 2)) // 2
                e = (2*q*(u+k) + k*k + 2*k*u + 5*k + 4*u + 4) // 2
                if not (0 < e < d < comb(q, 2)):
                    continue
                sd, rhod = depth(q, d)
                se, rhoe = depth(q, e)
                hd = sd - (u + 2*k + 1)
                he = se - (u + k)
                if hd <= 0 or he <= 0:
                    continue
                assert he <= hd
                vd, ve = q - sd, q - se
                m = ve - vd
                assert m == k + 1 + hd - he >= k + 1
                word_difference = (
                    comb(ve, 3) - comb(vd, 3)
                    + comb(rhoe, 2) - comb(rhod, 2)
                )
                assert word_difference == lam(q, d) - lam(q, e)
                if m >= 3:
                    assert word_difference >= vd * (vd + 3)
                    m_ge_3 += 1
                elif m == 2:
                    assert k == 1 and hd == he
                    rigid_m_2 += 1
                rows += 1
    assert rows and m_ge_3 and rigid_m_2
    return {"exact_rows": rows, "m_ge_3_rows": m_ge_3, "rigid_m_2_rows": rigid_m_2}


def main() -> None:
    symbolic_checks()
    counts = finite_guard()
    print("ERDOS776 CRITICAL-ELLIPSE INDEPENDENT AUDIT: PROMOTE")
    print(counts)
    print("fixed_c2_eventual_only", True)
    print("growing_c_open", True)
    print("original_problem_proved", False)


if __name__ == "__main__":
    main()
