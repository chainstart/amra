#!/usr/bin/env python3
"""Exact guards for the K4,r9 stable-tail no-fixed-rank theorem."""

from math import comb
import json
import sympy as sp


def C(n, k):
    return comb(n, k) if n >= k >= 0 else 0


def value(w):
    return sum(C(t, k) for t, k in w)


def upper(w):
    return sum(C(t, k + 1) for t, k in w)


def constants(last_rank):
    A, B = {4: 25}, {4: 58}
    for n in range(4, last_rank):
        A[n + 1] = C(A[n], 2) - (20 * n - 49)
        B[n + 1] = C(B[n], 2) - (20 * n - 52)
    return A, B


def stable_word(q, n, constant, side):
    H = 5 * q // 2
    if side == "x":
        w = [(H, n)]
        w += [(q - (1 + 5 * ((n - 1) - k)), k) for k in range(n - 1, 2, -1)]
        w += [(q - (5 * n - 15), 2), (constant, 1)]
    else:
        w = [(H + 1, n)]
        w += [(q - 5 * ((n - 1) - k), k) for k in range(n - 1, 2, -1)]
        w += [(q - (5 * n - 16), 2), (constant, 1)]
    return tuple(w)


def strict_word(w):
    return all(t >= k for t, k in w) and all(w[i][0] > w[i + 1][0] for i in range(len(w) - 1))


def symbolic_transition_guards():
    q, n, A, B = sp.symbols("q n A B", integer=True)
    cb = sp.binomial
    dx = 5 * n - 15
    dy = 5 * n - 16
    # The only nontrivial part of the rank transition is the bottom borrow.
    x_bottom = (
        cb(q - dx, 3) + cb(A, 2) - 4 * q + 3
        - cb(q - dx - 1, 3) - cb(q - dx - 5, 2)
        - (cb(A, 2) - (20 * n - 49))
    )
    y_bottom = (
        cb(q - dy, 3) + cb(B, 2) - 4 * q + 2
        - cb(q - dy - 1, 3) - cb(q - dy - 5, 2)
        - (cb(B, 2) - (20 * n - 52))
    )
    assert sp.expand_func(x_bottom).expand() == 0
    assert sp.expand_func(y_bottom).expand() == 0
    Anext = cb(A, 2) - (20 * n - 49)
    Bnext = cb(B, 2) - (20 * n - 52)
    gamma_constant = cb(B, 2) - cb(A + 1, 2) + 2
    assert sp.expand_func(
        gamma_constant - (Bnext - Anext - A - 1)
    ).expand() == 0
    positivity_margin = sp.factor(
        sp.binomial(4 * n + 9, 2) - (20 * n - 49) - (4 * (n + 1) + 9)
    )
    assert sp.expand_func(positivity_margin).expand() == 2 * (4 * n*n + 5*n + 36)
    return {
        "x_bottom_pascal_borrow": "identity",
        "y_bottom_pascal_borrow": "identity",
        "gamma_constant_recurrence": "C(B_n,2)-C(A_n+1,2)+2=B_(n+1)-A_(n+1)-A_n-1",
        "constant_positivity_induction": "A_n,B_n>=4n+9 for every n>=4",
    }


def main():
    symbolic = symbolic_transition_guards()
    A, B = constants(12)
    # A large even q checks simultaneous word order and exact transition for
    # several ranks.  The theorem itself uses unbounded actual q_j, not this
    # non-dyadic guard value.
    q = 10**1000
    tau = 4 * q - 2
    rows = []
    for n in range(4, 12):
        wx = stable_word(q, n, A[n], "x")
        wy = stable_word(q, n, B[n], "y")
        assert strict_word(wx) and strict_word(wy)
        assert upper(wx) - tau + 1 == value(stable_word(q, n + 1, A[n + 1], "x"))
        assert upper(wy) - tau == value(stable_word(q, n + 1, B[n + 1], "y"))
        gamma_constant = C(B[n], 2) - C(A[n] + 1, 2) + 2
        assert gamma_constant == B[n + 1] - A[n + 1] - A[n] - 1
        rows.append({
            "n": n, "A_n": A[n], "B_n": B[n],
            "gamma_n": f"{gamma_constant}-4q",
            "A_digits": len(str(A[n])), "B_digits": len(str(B[n])),
        })
    assert A[5] == 269 and B[5] == 1625
    assert A[6] == 35995 and B[6] == 1319452
    assert A[7] == 647801944 and B[7] == 870476130358
    print(json.dumps({
        "schema": "amra.erdos776.adaptive-round4.k4r9-no-fixed-rank.v1",
        "symbolic_induction": symbolic,
        "constant_rows": rows,
        "actual_q_recurrence": "q_(j+2)=4q_j-4 is unbounded on odd j",
        "theorem": "for every fixed R>=4, some actual odd j has stable words through R and gamma_3,...,gamma_R<0",
        "scope_warning": "refutes fixed-rank recovery for this orbit; not the public antichain statement",
    }, indent=2))


if __name__ == "__main__":
    main()
