#!/usr/bin/env python3
"""Independent red-team verifier for GROWING_DEPTH_ATTACK.md.

This file intentionally does not import any OPG-1757 verifier.
"""

from __future__ import annotations

import json
import math
import random
from fractions import Fraction
from functools import lru_cache

import sympy as sp


def multiply(left, right, maximum):
    result = [Fraction(0)] * (maximum + 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            if i + j <= maximum:
                result[i + j] += a * b
    return result


def product_series(low, high, maximum):
    result = [Fraction(1)] + [Fraction(0)] * maximum
    for value in range(low, high + 1):
        for degree in range(maximum, 0, -1):
            result[degree] -= value * result[degree - 1]
    return result


def g(rho):
    return Fraction(1, 2**rho * math.factorial(rho))


@lru_cache(maxsize=None)
def f0_series(rho, maximum):
    result = [Fraction(0)] * (maximum + 1)
    for j in range(rho + 1):
        scalar = Fraction(
            (-1)**j * (rho + j + 1),
            2**j * math.factorial(j) * math.factorial(rho-j),
        )
        product = product_series(1, rho+j, maximum)
        for degree in range(maximum + 1):
            result[degree] += scalar * product[degree]
    return tuple(value/g(rho) for value in result)


@lru_cache(maxsize=None)
def fa_series(rho, maximum):
    result = [Fraction(0)] * (maximum + 1)
    for j in range(rho + 1):
        scalar = Fraction(
            (-1)**j * (rho + j + 3),
            2**j * math.factorial(j) * math.factorial(rho-j),
        )
        product = product_series(3, rho+j+2, maximum)
        for degree in range(maximum + 1):
            result[degree] += scalar * product[degree]
    return tuple(value/g(rho) for value in result)


@lru_cache(maxsize=None)
def f1_series(rho, maximum):
    multiplier = [Fraction(2)] + [Fraction(-2*rho)] * maximum
    return tuple(multiply(f0_series(rho, maximum), multiplier, maximum))


@lru_cache(maxsize=None)
def f2_series(rho, maximum):
    inverse = multiply(
        multiply(
            [Fraction(1)] * (maximum + 1),
            [Fraction(2**j) for j in range(maximum + 1)],
            maximum,
        ),
        [Fraction(3**j) for j in range(maximum + 1)],
        maximum,
    )
    numerator = [
        Fraction(1),
        Fraction(-(2*rho+3)),
        Fraction((rho+1)*(rho+2)),
    ] + [Fraction(0)] * max(0, maximum-2)
    first = multiply(
        multiply(numerator[:maximum+1], inverse, maximum),
        f0_series(rho, maximum),
        maximum,
    )
    adjacent = [Fraction(0)] + multiply(
        [Fraction(3**j) for j in range(maximum + 1)],
        fa_series(rho, maximum),
        maximum,
    )[:maximum]
    return tuple(
        4*first[degree] - 4*adjacent[degree]
        for degree in range(maximum + 1)
    )


def evaluate(series, n):
    return sum(
        (value * Fraction(1, n**degree)
         for degree, value in enumerate(series)),
        Fraction(0),
    )


def finite_f0(rho, n):
    return evaluate(f0_series(rho, 2*rho+1), n)


def finite_fa(rho, n):
    return evaluate(fa_series(rho, 2*rho+1), n)


def finite_components(rho, n):
    u = Fraction(1, n)
    f0 = finite_f0(rho, n)
    fa = finite_fa(rho, n)
    f1 = 2 * (1-(rho+1)*u) / (1-u) * f0
    f2 = (
        4*(1-(rho+1)*u)*(1-(rho+2)*u)
        / ((1-u)*(1-2*u)*(1-3*u))*f0
        - 4*u/(1-3*u)*fa
    )
    return f0, fa, f1, f2


def heat_coefficient(a, b, rho, n):
    # Direct implementation of rho!^{-1} f(D)q(s)^rho at s=0.
    q_power = [Fraction(1)]
    for _ in range(rho):
        q_power = multiply(q_power, [0, 1, Fraction(-1, 2)], 2*rho)
    f = [Fraction(0)] * (2*rho + 1)
    for degree in range(2*rho + 1):
        if degree <= n-b:
            f[degree] += (
                a * Fraction(math.comb(n-b, degree), n**degree)
            )
        if degree >= 1 and degree-1 <= n-b:
            f[degree] += Fraction(
                math.comb(n-b, degree-1), n**(degree-1)
            )
    return sum(
        (
            f[degree] * math.factorial(degree) * q_power[degree]
            for degree in range(2*rho + 1)
        ),
        Fraction(0),
    ) / math.factorial(rho)


def determinant_normalized(R, n):
    result = Fraction(0)
    for rho in range(R + 1):
        sigma = R-rho
        f0r, _, f1r, _ = finite_components(rho, n)
        _, _, f1s, f2s = finite_components(sigma, n)
        result += g(rho)*g(sigma)*(f1r*f1s-f0r*f2s)
    return result


def component_formula_audit(maximum_rho=18):
    for rho in range(maximum_rho + 1):
        f0 = f0_series(rho, 3)
        fa = fa_series(rho, 3)
        f1 = f1_series(rho, 3)
        f2 = f2_series(rho, 3)
        assert f0[:3] == (
            Fraction(1),
            Fraction(5*rho),
            Fraction(rho*(35*rho-47), 2),
        )
        assert fa[:3] == (
            Fraction(3),
            Fraction(11*rho),
            Fraction(5*rho*(13*rho-37), 2),
        )
        assert f1[:3] == (
            Fraction(2),
            Fraction(8*rho),
            Fraction(rho*(25*rho-49)),
        )
        assert f2[:3] == (
            Fraction(4),
            Fraction(12*rho),
            Fraction(2*rho*(17*rho-57)),
        )

    # Heat/operator normalization versus finite products, with no shared
    # intermediate expression.
    for n in range(12, 31):
        for rho in range(min(7, n-4)):
            assert heat_coefficient(1, 2, rho, n) == g(rho)*finite_f0(rho, n)
            assert heat_coefficient(3, 4, rho, n) == g(rho)*finite_fa(rho, n)


def majorant_audit(maximum_rho=28):
    worst_component_ratio = Fraction(0)
    worst_tail_ratio = Fraction(0)
    for rho in range(maximum_rho + 1):
        # Equation (25), independently evaluated from finite products.
        for series in (f0_series(rho, 2*rho+1), fa_series(rho, 2*rho+1)):
            for J in range(3, len(series)):
                bound = 2**(7*J) * (rho+1)**J * J**J
                assert abs(series[J]) <= bound

        n = 4096*(rho+1)**2
        f0, fa, f1, f2 = finite_components(rho, n)
        t0 = (
            Fraction(1) + Fraction(5*rho, n)
            + Fraction(rho*(35*rho-47), 2*n*n)
        )
        ta = (
            Fraction(3) + Fraction(11*rho, n)
            + Fraction(5*rho*(13*rho-37), 2*n*n)
        )
        t1 = (
            Fraction(2) + Fraction(8*rho, n)
            + Fraction(rho*(25*rho-49), n*n)
        )
        t2 = (
            Fraction(4) + Fraction(12*rho, n)
            + Fraction(2*rho*(17*rho-57), n*n)
        )
        b17 = Fraction(2**28*(rho+1)**3, n**3)
        b19 = Fraction(2**34*(rho+1)**3, n**3)
        assert abs(f0-t0)+abs(fa-ta) <= b17
        assert abs(f1-t1)+abs(f2-t2) <= b19
        if b17:
            worst_component_ratio = max(
                worst_component_ratio,
                (abs(f0-t0)+abs(fa-ta))/b17,
            )

    # Exact audit of the numerical series in (27).
    for rho in range(maximum_rho + 1):
        n = 4096*(rho+1)**2
        lhs = sum(
            (
                Fraction(2**(7*J)*(rho+1)**J*J**J, n**J)
                for J in range(3, 2*rho+2)
            ),
            Fraction(0),
        )
        rhs = Fraction(2**27*(rho+1)**3, n**3)
        assert lhs <= rhs
        if rhs:
            worst_tail_ratio = max(worst_tail_ratio, lhs/rhs)
    return float(worst_component_ratio), float(worst_tail_ratio)


def determinant_audit(maximum_R=24):
    worst_ratio = Fraction(0)
    rng = random.Random(1757)
    cases = []
    for R in range(1, maximum_R + 1):
        threshold = 4096*(R+1)**2
        cases.extend((R, threshold*factor) for factor in (1, 2, 7))
    for _ in range(30):
        R = rng.randint(1, maximum_R)
        cases.append((R, 4096*(R+1)**2*rng.randint(1, 20)))

    for R, n in cases:
        exact = determinant_normalized(R, n)
        main = Fraction(4*R, math.factorial(R)*n*n)
        bound = Fraction(2**50*(R+1)**3, math.factorial(R)*n**3)
        assert abs(exact-main) <= bound
        worst_ratio = max(worst_ratio, abs(exact-main)/bound)

    # Equation (32), checked as exact binomial moments.
    for R in range(maximum_R + 1):
        for i in range(4):
            for j in range(4):
                lhs = sum(
                    (
                        g(rho)*g(R-rho)
                        *(rho+1)**i*(R-rho+1)**j
                        for rho in range(R+1)
                    ),
                    Fraction(0),
                )
                rhs = Fraction((R+1)**(i+j), math.factorial(R))
                assert lhs <= rhs
    return float(worst_ratio)


def support_and_newton_audit():
    # Directly check C_0=C_1=C_2=0 and the odd/even first support.
    for n in range(8, 20):
        assert determinant_normalized(0, n) == 0
        assert determinant_normalized(1, n) > 0
        assert determinant_normalized(2, n) > 0

    # Check (35) for both parity classes and every admissible ell.
    for depth in range(0, 30):
        for parity_offset in (1, 2):
            R = parity_offset + 2*depth
            N = 50 + depth
            main = Fraction(4*R, math.factorial(R))*N**(2*N-8)
            for ell in range(depth + 1):
                rl = R-2*ell
                nl = N-ell
                earlier = (
                    Fraction(4*rl, math.factorial(rl))
                    * nl**(2*nl-8)
                )
                assert earlier/main <= Fraction(R*R, N*N)**ell

    # Independent exact Newton stress, reconstructed only from determinant
    # finite products.
    values = {}
    for k in range(8, 45):
        q0 = (k-2)//2
        n0 = q0+4
        t0 = 3 if k % 2 else 4
        for depth in range(min(7, int(math.sqrt(k))) + 1):
            raw = Fraction(0)
            for j in range(depth + 1):
                n = n0+j
                R = t0+2*j-2
                component = determinant_normalized(R, n)*n**(2*n-6)
                raw += (
                    (-1)**(depth-j)
                    * math.comb(q0+depth, depth-j)
                    * component
                )
            coefficient = Fraction(math.factorial(k-2), 2)*raw
            assert coefficient.denominator == 1 and coefficient > 0
            values[(k, depth)] = coefficient.numerator
    return len(values)


def explicit_constant_audit(maximum_depth=80):
    # Audit (38a)--(40) without constructing astronomical graph counts.
    largest_relative_error = Fraction(0)
    for depth in range(maximum_depth + 1):
        for parity_offset in (1, 2):
            R = parity_offset + 2*depth
            N = 2**52*(R+1)**2
            for ell in range(depth + 1):
                rl = R-2*ell
                nl = N-ell
                relative_error = Fraction(
                    2**48*(rl+1)**3, rl*nl
                )
                assert relative_error < 1
                largest_relative_error = max(
                    largest_relative_error, relative_error
                )

            n54 = 2**54*(R+1)**2
            assert Fraction(2**51*(R+1)**2, n54) <= Fraction(1, 8)
            x = Fraction(R*R, n54)
            assert x <= Fraction(1, 2**54)
            # e^x-1 <= x/(1-x), since 1/j! <= 1.
            assert Fraction(1, 8) + 2*x/(1-x) < 1
    return float(largest_relative_error)


NVAR = sp.symbols("n", integer=True, positive=True)


def falling(x, length):
    return sp.prod(x-i for i in range(length))


@lru_cache(maxsize=None)
def raw_w0(c):
    return sp.factor(sum(
        sp.Rational((-1)**j, 2**j)
        * (c+j)*falling(NVAR-1, c+j-1)
        * NVAR**(NVAR-c-j-1)
        / (math.factorial(j)*math.factorial(c-j-1))
        for j in range(c)
    ))


@lru_cache(maxsize=None)
def raw_adjacent(c):
    return sp.factor(sum(
        sp.Rational((-1)**j, 2**j)
        * (c+j+2)*falling(NVAR-3, c+j-1)
        * NVAR**(NVAR-c-j-3)
        / (math.factorial(j)*math.factorial(c-j-1))
        for j in range(c)
    ))


@lru_cache(maxsize=None)
def raw_w1(c):
    return sp.factor(2*(NVAR-c)*raw_w0(c)/(NVAR*(NVAR-1)))


@lru_cache(maxsize=None)
def raw_w2(c):
    adjacent_orbits = NVAR*(NVAR-1)*(NVAR-2)/2
    disjoint_orbits = NVAR*(NVAR-1)*(NVAR-2)*(NVAR-3)/8
    return sp.factor(
        (
            (NVAR-c)*(NVAR-c-1)*raw_w0(c)/2
            - adjacent_orbits*raw_adjacent(c)
        ) / disjoint_orbits
    )


@lru_cache(maxsize=None)
def raw_determinant(total):
    return sp.factor(sum(
        raw_w1(c)*raw_w1(total-c)-raw_w0(c)*raw_w2(total-c)
        for c in range(1, total)
    ))


P15 = sp.Poly(
    NVAR**18 + 87*NVAR**17 + 3800*NVAR**16 + 105360*NVAR**15
    + 1891421*NVAR**14 + 17289777*NVAR**13 - 118116085*NVAR**12
    - 6505709265*NVAR**11 - 86775284431*NVAR**10
    - 38284278087*NVAR**9 + 14371618346075*NVAR**8
    + 155474888000475*NVAR**7 - 622230464754476*NVAR**6
    - 21941798038092942*NVAR**5 - 34808916839991345*NVAR**4
    + 1685933108025287175*NVAR**3 + 3008726132139045000*NVAR**2
    - 82118619319287127500*NVAR + 197196338202113250000,
    NVAR,
).as_expr()
P16 = sp.Poly(
    NVAR**20 + 91*NVAR**19 + 4172*NVAR**18 + 121628*NVAR**17
    + 2284643*NVAR**16 + 20698691*NVAR**15 - 230561653*NVAR**14
    - 11319430447*NVAR**13 - 162404702239*NVAR**12
    - 80646884461*NVAR**11 + 34321800795503*NVAR**10
    + 457838031840137*NVAR**9 - 1167527280504428*NVAR**8
    - 82905605421055196*NVAR**7 - 398108708754400437*NVAR**6
    + 8161447984576101657*NVAR**5 + 64714964045818304358*NVAR**4
    - 630805618098807641100*NVAR**3
    - 3720646386150579275400*NVAR**2
    + 41502191820112083060000*NVAR
    - 86322277727720274240000,
    NVAR,
).as_expr()


SEVENTH_BOUNDARY = {
    6: 40320,
    7: 129024000,
    8: 56384294400,
    9: 38466105189120,
    10: 19172585464704000,
    11: 8459995287334752000,
    12: 5588121248292596428800,
    13: 2057634945868538561817600,
    14: 1840898547634306585990118400,
    15: 629013092157326490510651955200,
    16: 755656377559846704218640358195200,
    17: 252902104918288632975645944603136000,
    18: 400885200400329152324178964122673152000,
    19: 135348119377829575229021244569109135360000,
    20: 277750473779994027112715979465152548577280000,
    21: 96199130980722253989938072808952931562455040000,
    22: 250969416726626124614385322827257976884593950720000,
    23: 90040892954791322663935009017638461713607966064640000,
    24: 293723920454657044846124904241982585080107921372610560000,
    25: 109772406518111164968414347516075482376452480344698388480000,
    26: 441147474656488554818915934918954526505848409795275134074880000,
    28: 841661100888739666797729646999468711983328248818691755627249664000000,
    30: 2018953119324318711635469624199863166244074241113792840348866938142720000000,
    32: 6028234524723186002881797176873713285862791239328168109189458928525723566080000000,
}


def seventh_layer_audit():
    expected15 = falling(NVAR-4, 6)*P15*NVAR**(2*NVAR-32)/119750400
    expected16 = falling(NVAR-4, 6)*P16*NVAR**(2*NVAR-34)/1556755200
    assert sp.simplify(raw_determinant(15)-expected15) == 0
    assert sp.simplify(raw_determinant(16)-expected16) == 0

    boundary = {}
    for k in SEVENTH_BOUNDARY:
        q0 = (k-2)//2
        n0 = q0+4
        t0 = 3 if k % 2 else 4
        raw = Fraction(0)
        for j in range(7):
            n = n0+j
            R = t0+2*j-2
            component = determinant_normalized(R, n)*n**(2*n-6)
            raw += (
                (-1)**(6-j)*math.comb(q0+6, 6-j)*component
            )
        value = Fraction(math.factorial(k-2), 2)*raw
        assert value.denominator == 1
        boundary[k] = value.numerator
    assert boundary == SEVENTH_BOUNDARY
    return boundary


def audit():
    component_formula_audit()
    component_ratio, tail_ratio = majorant_audit()
    determinant_ratio = determinant_audit()
    stress_count = support_and_newton_audit()
    explicit_error = explicit_constant_audit()
    boundary = seventh_layer_audit()
    return {
        "schema": "amra.opg1757.independent-growing-depth-audit.v1",
        "verdict": "PASS",
        "imports_existing_opg_verifier": False,
        "maximum_component_rho": 28,
        "maximum_determinant_R": 24,
        "worst_component_bound_ratio": component_ratio,
        "worst_majorant_series_ratio": tail_ratio,
        "worst_determinant_bound_ratio": determinant_ratio,
        "exact_newton_stress_count": stress_count,
        "largest_38a_relative_error_bound": explicit_error,
        "seventh_boundary_values_checked": len(boundary),
        "C15_denominator": 119750400,
        "C16_denominator": 1556755200,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
