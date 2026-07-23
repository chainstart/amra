#!/usr/bin/env python3
"""Exact coefficient checks for the reductions in the #521 report.

This script is a sanity certificate for algebraic identities only.  It does
not prove the probabilistic block-maximal lemma.
"""

from itertools import product


def reverse_coefficients(eps):
    """Ascending coefficients of x^n f(1/x)."""
    return tuple(reversed(eps))


def shift_by_x(coefficients):
    return (0,) + tuple(coefficients)


checked = 0
for degree in range(0, 11):
    for eps in product((-1, 1), repeat=degree + 2):
        gn = reverse_coefficients(eps[: degree + 1])
        gn1 = reverse_coefficients(eps[: degree + 2])

        # g_{n+1} = eps_{n+1} + x g_n, in ascending coefficient order.
        recurrence_rhs = list(shift_by_x(gn))
        recurrence_rhs[0] = eps[degree + 1]
        assert tuple(recurrence_rhs) == gn1

        # x^n f_n(1/x) reverses the coefficient vector exactly.
        assert gn == tuple(eps[degree::-1])
        assert gn[0] in (-1, 1)  # zero is never a root of g_n
        checked += 1

print(
    {
        "status": "PASS",
        "identity": "g_(n+1)(x)=epsilon_(n+1)+x*g_n(x)",
        "coefficient_instances_checked": checked,
        "max_degree": 10,
        "scope": "algebra only; no probabilistic claim",
    }
)

