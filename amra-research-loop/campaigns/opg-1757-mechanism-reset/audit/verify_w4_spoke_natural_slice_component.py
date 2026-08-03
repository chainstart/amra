#!/usr/bin/env python3
"""Independent algebra checks for the W4 spoke natural-slice proof."""

import json
import sympy as sp


a, c, x = sp.symbols("a c x", real=True)
A = (c + 2) * (c**2 + 2*c + 2)
H = c**2 + 4*c + 6
P = sp.expand(A*x**3 - 2*H*x + 2*(c + 4))
Q = sp.expand(H*x**2 - 3*(c + 4)*x + 6 - c)


def main():
    disc_p = sp.factor(sp.discriminant(P, x))
    disc_q = sp.factor(sp.discriminant(Q, x))
    resultant = sp.factor(sp.resultant(P, Q, x))
    assert disc_p == (
        4*c**2*(c+2)*(c**2+2*c+2)
        *(8*c**4+69*c**3+204*c**2+206*c+36)
    )
    assert disc_q == c**2*(4*c+1)
    assert resultant == -c**7*(c**2+2*c+2)

    # For c>0 every displayed factor has the asserted strict sign.
    positive_factor_coefficients = [8, 69, 204, 206, 36]
    assert all(value > 0 for value in positive_factor_coefficients)
    assert sp.discriminant(c**2+2*c+2, c) < 0

    p_one = sp.factor(P.subs(x, 1))
    derivative_lower_bound = sp.factor(3*A - 2*H)
    assert p_one == c**2*(c+2)
    assert derivative_lower_bound == c*(3*c**2+10*c+10)

    p_base = sp.expand(P.subs(c, 1))
    q_base = sp.expand(Q.subs(c, 1))
    q2 = (15 + sp.sqrt(5))/22
    p_at_q2 = sp.factor(p_base.subs(x, q2))
    assert p_base == 15*x**3-22*x+10
    assert q_base == 11*x**2-15*x+5
    assert sp.simplify(q_base.subs(x, q2)) == 0
    assert sp.simplify(p_at_q2 - (95-56*sp.sqrt(5))/1331) == 0
    assert 56**2 * 5 > 95**2
    assert sp.ask(sp.Q.negative(p_at_q2)) is True
    assert q2 > 0 and p_base.subs(x, 0) > 0

    # Recheck the earlier boundary identity in a=x-1 coordinates.
    p_ac = sp.expand(P.subs(x, a+1))
    q_ac = sp.expand(Q.subs(x, a+1))
    identity = sp.expand(
        (a+1)*p_ac - (a**2*c+2*a*c+3*a+c+2)*q_ac
        - a**2*(4*a**2-2*a-c)
    )
    assert identity == 0

    # Rational fibers guard the labelled-root ordering and p3(c)<1; the
    # universal step is the simple-root/resultant continuity proof.
    fibers = []
    for c_value in (sp.Rational(1, 10), sp.Rational(1, 2), 1, 2, 10):
        p_roots = sorted((float(sp.re(root)) for root in sp.nroots(P.subs(c, c_value))))
        q_roots = sorted((float(sp.re(root)) for root in sp.nroots(Q.subs(c, c_value))))
        assert q_roots[-1] < p_roots[-1] < 1
        fibers.append({"c": str(c_value), "q2": q_roots[-1], "p3": p_roots[-1]})

    print(json.dumps({
        "schema": "amra.opg1757.w4-spoke-natural-slice-independent-check.v1",
        "discriminant_P": str(disc_p),
        "discriminant_Q": str(disc_q),
        "resultant": str(resultant),
        "base_order_certificate": {
            "q2": str(q2),
            "P_at_q2": str(p_at_q2),
            "consequence": "p2(1)<q2(1)<p3(1)",
        },
        "continuity_certificate": "simple roots for c>0 and nonzero P-Q resultant prevent labelled crossings",
        "component_certificate": {
            "P_at_x_1": str(p_one),
            "derivative_lower_bound_on_x_ge_1": str(derivative_lower_bound),
            "path": "(x,c)->(1,c)->(1,1)->(2,1) inside c*P>0",
        },
        "rational_fiber_checks": fibers,
        "result": "pass",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
