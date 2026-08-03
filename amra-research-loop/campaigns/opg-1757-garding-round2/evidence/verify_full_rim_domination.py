#!/usr/bin/env python3
"""Exact symbolic verifier for full four-variable W4 rim domination."""

import json
from pathlib import Path
import sympy as sp


a, b, c, d = sp.symbols("a b c d")
x, y, z, w, u = sp.symbols("x y z w u")
old = Path(__file__).parents[2] / "opg-1757-mechanism-reset" / "evidence" / "w4_garding_orbit_probe.json"
rim = json.loads(old.read_text())["rim_orbit"]
P = sp.sympify(rim["C_delete"])
Q = sp.sympify(rim["xi"])


def main() -> None:
    shifted = {a: x - 1, b: y - 1, c: z - 1, d: w - 1}
    Ps = sp.expand(P.subs(shifted))
    Qs = sp.expand(Q.subs(shifted))
    T = x * y * z - 1
    L = x * z + y - 2
    K = x + y * z - 2
    assert sp.expand(Ps - (w * T**2 - L**2)) == 0
    Q0 = sp.expand(Qs.subs(w, 0))
    assert sp.expand(Qs - (w * K**2 + Q0)) == 0

    boundary_numerator = sp.expand(T**2 * Q0 + K**2 * L**2)
    A = (
        x**2 * y**2 + 2*x**2*y + x**2 + 2*x*y**2
        - 4*x*y - 2*x + y**2 - 2*y + 5
    )
    B = (
        2*u**3 + A*u**2
        + 2*u*((x - 1)**2 + (y - 1)**2)
        + (x - 1)**2*(y - 1)**2
    )
    substituted = sp.together(
        boundary_numerator.subs(z, (u + 1)/(x*y)) * x**4 * y**4
    )
    expected = x**2*y**2*(x - 1)**2*(y - 1)**2*B
    assert sp.factor(substituted - expected) == 0
    assert sp.expand(sp.discriminant(A, x) + 16*(y**3 + y + 1)) == 0
    assert sp.expand(A.subs(x, 0) - (y**2 - 2*y + 5)) == 0

    # The coarse negative endpoint is rigorously in the T<0 component.
    endpoint = {
        x: sp.Rational(-13, 20),  # a=-33/20
        y: sp.Rational(12, 25),   # b=-13/25
        z: sp.Rational(11, 2),    # c=9/2
        w: sp.Rational(79, 10),   # d=69/10
    }
    assert T.subs(endpoint) == sp.Rational(-679, 250)
    assert Ps.subs(endpoint) == sp.Rational(161582787, 5000000)
    assert Qs.subs(endpoint) == sp.Rational(-346833, 500000)
    assert T.subs({x: 2, y: 2, z: 2}) == 7

    print(json.dumps({
        "schema": "amra.opg1757.full-w4-rim-domination.v1",
        "P_shifted": "w*(x*y*z-1)^2-(x*z+y-2)^2",
        "xi_shifted": "w*(x+y*z-2)^2+Q0",
        "distinguished_component": "x,y,z>0; x*y*z>1; w>(x*z+y-2)^2/(x*y*z-1)^2",
        "boundary_certificate": "(x-1)^2*(y-1)^2*B/(x^2*y^2), with B>0 for u=x*y*z-1>0",
        "A_discriminant": "-16*(y^3+y+1)",
        "coarse_endpoint_T": "-679/250",
        "conclusion": "xi>0 on the full four-variable distinguished rim component",
        "public_problem_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
