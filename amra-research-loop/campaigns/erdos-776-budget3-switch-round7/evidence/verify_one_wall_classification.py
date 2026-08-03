#!/usr/bin/env python3
"""Symbolic guard for the one-wall bottom-budget classification."""

import json
import sympy as sp


def main() -> None:
    t, b, q, m, bprev = sp.symbols(
        "t b q m bprev", integer=True
    )
    cb = sp.binomial
    increments = {}
    for s in range(5):
        inc = sp.expand_func(cb(t + s, 2) - cb(t, 2)).expand()
        expected = s * t + s * (s - 1) // 2
        assert sp.expand(inc - expected) == 0
        increments[str(s)] = str(expected)

    # On D_s<=b<D_(s+1), the residual is exactly canonical at rank one.
    # The algebraic implication is D_(s+1)-D_s=t+s.
    for s in range(4):
        gap = sp.expand(
            (s + 1) * t + s * (s + 1) // 2
            - (s * t + s * (s - 1) // 2)
        )
        assert gap == t + s

    # At s=3, substitute t=q-(5m-16) and the stable B recurrence.
    bnext = cb(bprev, 2) - (20 * (m - 1) - 52)
    residual = bnext - (3 * (q - (5 * m - 16)) + 3)
    target = cb(bprev, 2) - 3 * q - (5 * m - 21)
    assert sp.expand_func(residual - target).expand() == 0

    # The preceding rank-three top is t+4.  Strict ordering admits t+s
    # exactly for s<=3 and rejects s=4 by equality.
    assert all(t + s < t + 4 for s in range(4))
    assert sp.expand((t + 4) - (t + 4)) == 0

    # Dense small integer replay of every half-open wall interval.
    checked = 0
    for tv in range(10, 80):
        for s in range(4):
            low = s * tv + s * (s - 1) // 2
            high = (s + 1) * tv + s * (s + 1) // 2
            for bv in (low, (low + high - 1) // 2, high - 1):
                rv = bv - low
                assert 0 <= rv < tv + s
                assert sp.binomial(tv, 2) + bv == sp.binomial(tv + s, 2) + rv
                checked += 1

    # Equality of slopes is not a sign theorem in the abstract round-six
    # affine model.  This exact integer point has alpha=3, delta=0 and a
    # canonical nonnegative next digit, but negative current surplus.
    q0, b0, a0, v0 = 100, 20, 0, 0
    beta0 = int(sp.binomial(b0, 2)) - 3 * q0
    bnext0 = int(sp.binomial(b0, 2)) - 3 * q0 - beta0
    gamma0 = int(sp.binomial(b0, 2) - sp.binomial(a0 + 1, 2) + 2 - 4 * q0 + v0)
    assert bnext0 == 0 < q0 - 1
    assert gamma0 == -208 < 0

    print(json.dumps({
        "schema": "amra.erdos776.round7.one-wall-classification.v1",
        "verdict": "PASS",
        "triangular_increments": increments,
        "legal_rank_two_shifts": [0, 1, 2, 3],
        "max_bottom_budget": 3,
        "equality_residual": "C(B_(m-1),2)-3q-(5m-21)",
        "dense_integer_checks": checked,
        "critical_slope_not_sufficient_counterexample": {
            "q": q0,
            "A": a0,
            "B": b0,
            "alpha": 3,
            "delta": 0,
            "beta": beta0,
            "B_next": bnext0,
            "canonical_bound": "B_next<q-1",
            "gamma": gamma0
        },
    }, indent=2))


if __name__ == "__main__":
    main()
