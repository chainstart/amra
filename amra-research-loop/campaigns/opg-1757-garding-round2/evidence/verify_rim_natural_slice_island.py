#!/usr/bin/env python3
"""Exact Sturm/resultant certificate for the W4 rim natural-slice island."""

import json
from pathlib import Path
import sympy as sp


a, c = sp.symbols("a c")
old = Path(__file__).parents[2] / "opg-1757-mechanism-reset" / "evidence" / "w4_garding_orbit_probe.json"
rim = json.loads(old.read_text())["rim_orbit"]["natural_two_variable"]
P = sp.sympify(rim["C_delete"])
Q = sp.sympify(rim["xi"])


def main() -> None:
    assert P.subs({a: -1, c: 10}) == 7
    assert Q.subs({a: -1, c: 10}) == -3
    assert sp.factor(P.subs(a, -1)) == c - 3
    assert sp.factor(P.subs(a, 0)) == c**3

    pc = sp.Poly(P, c)
    assert sp.expand(pc.LC() - (a + 1) ** 4) == 0
    discriminant = sp.factor(sp.discriminant(P, c))
    resultant = sp.factor(sp.resultant(P, sp.diff(P, c), c))
    expected_discriminant = -a**6 * (a + 1)**4 * (27*a**2 - 32)
    assert discriminant == expected_discriminant
    assert resultant == a**6 * (a + 1)**8 * (27*a**2 - 32)

    # Sturm-isolate all three roots on a representative regular fibre.
    fibre = sp.Poly(P.subs(a, sp.Rational(-1, 2)), c)
    isolating_intervals = [(0, 1), (2, 3), (6, 7)]
    assert [fibre.count_roots(lo, hi) for lo, hi in isolating_intervals] == [1, 1, 1]
    assert fibre.count_roots(-sp.oo, sp.oo) == 3
    # Positive signs alternate as (root1,root2) and above root3.
    assert fibre.eval(sp.Rational(1, 2)) > 0
    assert fibre.eval(2) > 0
    assert fibre.eval(4) < 0
    assert fibre.eval(6) < 0
    assert fibre.eval(7) > 0

    boundary_a = -4 * sp.sqrt(6) / 9
    double_c = sp.Rational(152, 25) + 72 * sp.sqrt(6) / 25
    assert sp.simplify(P.subs({a: boundary_a, c: double_c})) == 0
    assert sp.simplify(sp.diff(P, c).subs({a: boundary_a, c: double_c})) == 0
    # The remaining root is strictly above the double root; polynomial
    # division leaves a positive linear separation in Q(sqrt(6)).
    quotient = sp.div(
        sp.Poly(P.subs(a, boundary_a), c, extension=sp.sqrt(6)),
        sp.Poly((c - double_c) ** 2, c, extension=sp.sqrt(6)),
    )[0]
    remaining_root = sp.solve(quotient.as_expr(), c)[0]
    assert sp.ask(sp.Q.positive(remaining_root - double_c)) is True

    print(json.dumps({
        "schema": "amra.opg1757.rim-natural-slice-island-audit.v1",
        "negative_point": {"a": -1, "c": 10, "P": 7, "xi": -3},
        "discriminant_c": str(discriminant),
        "resultant_P_dPdc": str(resultant),
        "double_root_boundary": {"a": str(boundary_a), "c": str(double_c)},
        "sturm_fibre": {"a": "-1/2", "root_intervals": isolating_intervals},
        "conclusion": "The negative-xi point lies in the middle positive component, not the distinguished component above the largest c-root.",
        "public_problem_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
