#!/usr/bin/env python3
r"""Exact elimination proof for the natural two-variable W4 spoke slice.

The script checks the algebraic factors used to prove Q>0 on the connected
{C_delete>0} slice component containing the positive orthant.  It does not
claim four-variable domination or characterize every point in the
intersection of the full component with the slice.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


a, c, x = sp.symbols("a c x", real=True)
A = (c + 2) * (c**2 + 2*c + 2)
H = c**2 + 4*c + 6
k = c + 4

# x=a+1.  On b=a,d=c, C_delete=c*P and xi=2*c*Q.
P = sp.expand(A*x**3 - 2*H*x + 2*k)
Q = sp.expand(H*x**2 - 3*k*x + 6 - c)

disc_P = sp.factor(sp.discriminant(P, x))
disc_Q = sp.factor(sp.discriminant(Q, x))
resultant = sp.factor(sp.resultant(P, Q, x))

expected_disc_P = (
    4*c**2*(c + 2)*(c**2 + 2*c + 2)
    * (8*c**4 + 69*c**3 + 204*c**2 + 206*c + 36)
)
expected_disc_Q = c**2*(4*c + 1)
expected_resultant = -c**7*(c**2 + 2*c + 2)
assert sp.expand(disc_P - expected_disc_P) == 0
assert sp.expand(disc_Q - expected_disc_Q) == 0
assert sp.expand(resultant - expected_resultant) == 0

# The rightmost P root is below x=1 for every c>0: P(1)>0 and P is strictly
# increasing on [1,infinity).
P_at_one = sp.factor(P.subs(x, 1))
P_derivative_at_one = sp.factor(sp.diff(P, x).subs(x, 1))
assert P_at_one == c**2*(c + 2)
assert P_derivative_at_one == c*(3*c**2 + 10*c + 10)

# Establish the root order at one parameter value c=1.  Q has largest root
# q_plus=(15+sqrt(5))/22.  P(q_plus)<0, while q_plus>0 and P(0)>0;
# since P has three simple real roots and positive leading coefficient, q_plus
# lies between P's middle and largest roots.
q_plus = (15 + sp.sqrt(5))/22
P_base = sp.expand(P.subs(c, 1))
Q_base = sp.expand(Q.subs(c, 1))
P_at_q_plus = sp.factor(P_base.subs(x, q_plus))
assert P_base == 15*x**3 - 22*x + 10
assert Q_base == 11*x**2 - 15*x + 5
assert sp.simplify(Q_base.subs(x, q_plus)) == 0
assert sp.simplify(P_at_q_plus - (95 - 56*sp.sqrt(5))/1331) == 0
assert sp.ask(sp.Q.negative(P_at_q_plus)) is True

# Recover the earlier boundary identity after substituting x=a+1.
P_ac = sp.expand(P.subs(x, a + 1))
Q_ac = sp.expand(Q.subs(x, a + 1))
identity = sp.expand(
    (a + 1)*P_ac - (a**2*c + 2*a*c + 3*a + c + 2)*Q_ac
    - a**2*(4*a**2 - 2*a - c)
)
assert identity == 0

result = {
    "host": "W4",
    "marked_orbit": "spoke",
    "slice": "b=a, d=c, with x=a+1",
    "C_delete": "c*P(x,c)",
    "xi": "2*c*Q(x,c)",
    "P": str(P),
    "Q": str(Q),
    "discriminant_P": str(disc_P),
    "discriminant_Q": str(disc_Q),
    "resultant_x_P_Q": str(resultant),
    "base_parameter": {
        "c": 1,
        "P": str(P_base),
        "Q": str(Q_base),
        "largest_Q_root": "(15+sqrt(5))/22",
        "P_at_largest_Q_root": "(95-56*sqrt(5))/1331 < 0",
    },
    "component": {
        "description": "c>0 and x>p3(c), where p3 is the largest P root",
        "explicit_path": (
            "move x to 1 at fixed c; vary c to 1 at x=1; "
            "then increase x to 2"
        ),
        "path_signs": (
            "P stays positive in the rightmost root interval; "
            "at x=1, C_delete=c^3*(c+2)>0"
        ),
    },
    "root_order": "q2(c) < p3(c) for every c>0",
    "conclusion": (
        "Q>0 and hence xi>0 on the entire connected two-variable "
        "C_delete-positive slice component containing the positive orthant"
    ),
    "scope_limit": (
        "This proves the natural two-variable slice survivor only, not "
        "full four-variable domination and not equality with the entire "
        "intersection of the full distinguished component and the slice."
    ),
}

output = Path(__file__).with_suffix(".json")
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
