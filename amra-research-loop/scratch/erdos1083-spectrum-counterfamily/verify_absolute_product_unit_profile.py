#!/usr/bin/env python3
"""Bounded guard for the absolute product-unit profile interface.

Finite checks only guard the exact formulas.  The theorem is the elementary
minimum-of-a-sum proof in the accompanying note.
"""

from fractions import Fraction
import hashlib
import json


def direct_sum(a, b):
    vals = [x + y for x in a for y in b]
    assert len(vals) == len(set(vals)), (a, b)
    return tuple(sorted(vals))


def profile(x, lam, a_j, f0, a0):
    fj = tuple(lam * y for y in x)
    v = direct_sum(a_j, fj)
    return (min(fj), min(f0), min(a_j), min(a0)), v


def interval_rows(s, c, shift):
    """Mixed-radix exact rows from the archived interval family."""
    beta = Fraction(1, s - 1)
    x = tuple(beta * i + shift for i in range(s))
    v0 = tuple(Fraction(i, 1) for i in range(s * c))
    # Translate the common spectrum far enough only for readability; its
    # minimum is irrelevant to the identity.
    v_shift = Fraction(97, 1)
    rows = []
    for m in range(1, c + 1):
        if c % m:
            continue
        b_m = sorted({r + s * m * k for r in range(m) for k in range(c // m)})
        assert len(b_m) == c
        lam = Fraction(m, 1)
        # m*beta*I_S plus beta*B_m is beta*I_SC.  Translating X by
        # shift requires translating A_m back by m*shift.
        a_m = tuple(v_shift + beta * b - lam * shift for b in b_m)
        vv = direct_sum(a_m, tuple(lam * y for y in x))
        expected = tuple(v_shift + beta * i for i in range(s * c))
        assert vv == expected
        rows.append((lam, a_m, vv))
    return x, rows


def main():
    checks = 0
    witnesses = []
    for s in range(3, 10):
        for c in range(2, s):
            # Zero-anchor branch.
            x0, rows0 = interval_rows(s, c, Fraction(0))
            p0 = []
            for lam, a_j, v in rows0:
                phi = min(lam * y for y in x0)
                pi = (phi, min(a_j))
                assert pi == (Fraction(0), min(v))
                p0.append(pi)
                checks += 1
            assert len(set(p0)) == 1

            # Nonzero-anchor branch on the same exact additive tilings.
            shift = Fraction(1, 7)
            x1, rows1 = interval_rows(s, c, shift)
            p1 = []
            for lam, a_j, v in rows1:
                phi = min(lam * y for y in x1)
                assert phi == lam * min(x1)
                pi = (phi, min(a_j))
                assert pi[0] + pi[1] == min(v)
                p1.append(pi)
                checks += 1
            assert len(set(p1)) == len(rows1)
            witnesses.append({
                "S": s,
                "C": c,
                "rows": len(rows1),
                "zero_anchor_profiles": len(set(p0)),
                "nonzero_anchor_profiles": len(set(p1)),
            })

    # Direct sign formula, including the negative class.
    x = (Fraction(-3, 2), Fraction(1, 4), Fraction(5, 2))
    for lam in [Fraction(-9), Fraction(-2), Fraction(1), Fraction(7)]:
        got = min(lam * y for y in x)
        want = lam * (max(x) if lam < 0 else min(x))
        assert got == want
        checks += 1

    result = {
        "schema": "amra.erdos1083.absolute-product-unit-profile.scratch.v1",
        "status": "pass",
        "finite_checks": checks,
        "theorem_source": "minimum of a Minkowski sum and same-sign scalar injectivity",
        "sample_witnesses": witnesses[-8:],
        "scope": {
            "round7_modified": False,
            "power_large_counterfamily_constructed": False,
            "public_exponent_changed": False,
        },
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
