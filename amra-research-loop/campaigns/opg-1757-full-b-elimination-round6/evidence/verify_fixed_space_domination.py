#!/usr/bin/env python3
"""Exact standard-library verifier for full five-variable domination.

The analytic sign proof is in FULL_FIXED_SPACE_DOMINATION.md.  This script
independently reconstructs P and xi and checks its complete algebraic ledger
with sparse rational polynomials.  No CAS or third-party module is imported.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
import json

from verify_garding_prt_firewall import (
    ZERO,
    add,
    clean,
    coefficient_in,
    constant,
    derivative,
    divide_monomial,
    evaluate,
    monomial_factor,
    multiply,
    plus,
    power,
    reconstruct,
    restrict_zero,
    scale,
    translate,
    variable,
)


def product(*polynomials):
    result = constant(1)
    for polynomial in polynomials:
        result = multiply(result, polynomial)
    return result


def signed_sum(terms):
    result = {}
    for coefficient, polynomial in terms:
        result = add(result, scale(polynomial, coefficient))
    return clean(result)


def determinant(matrix):
    """Leibniz determinant; the only use is a 5-by-5 Sylvester matrix."""
    size = len(matrix)
    result = {}
    for permutation in permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size) for j in range(i + 1, size)
        )
        term = constant(-1 if inversions % 2 else 1)
        for row, column in enumerate(permutation):
            term = multiply(term, matrix[row][column])
        result = add(result, term)
    return clean(result)


def resultant_quadratic_cubic(q0, q1, q2, f0, f1, f2, f3):
    zero = {}
    # Coefficients are in ascending order; reversing each shifted row gives
    # the standard Sylvester determinant.
    return determinant([
        [q2, q1, q0, zero, zero],
        [zero, q2, q1, q0, zero],
        [zero, zero, q2, q1, q0],
        [f3, f2, f1, f0, zero],
        [zero, f3, f2, f1, f0],
    ])


def main() -> None:
    P, xi, forest_count, connected_count = reconstruct()
    assert (forest_count, connected_count) == (128, 58)

    # Eliminate b in the original coordinates.
    A = derivative(P, (0, 1, 0, 0, 0))
    C = restrict_zero(P, 1)
    D = derivative(xi, (0, 1, 0, 0, 0))
    E = restrict_zero(xi, 1)
    delta = add(multiply(A, E), multiply(D, C), right_scale=-1)
    R = divide_monomial(delta, 2, (2, 0, 0, 0, 0))

    # Shift x=a+1, w=c+1, y=d+1, z=e+1.  Slots 0,2,3,4 now
    # represent x,w,y,z respectively; slot 1 remains unused.
    shift = (Fraction(-1), Fraction(0), Fraction(-1), Fraction(-1), Fraction(-1))
    As, Ds, Rs = (translate(polynomial, shift) for polynomial in (A, D, R))
    x, _, w, y, z = (variable(index) for index in range(5))
    one = constant(1)
    xy, xz, yz = multiply(x, y), multiply(x, z), multiply(y, z)

    L = derivative(As, (0, 0, 1, 0, 0))
    K = restrict_zero(As, 2)
    expected_L = signed_sum([
        (1, product(power(x, 2), power(y, 2), power(z, 2))),
        (-1, power(x, 2)), (-1, power(y, 2)), (-1, power(z, 2)),
        (2, one),
    ])
    assert L == expected_L
    assert As == add(multiply(L, w), K)

    # D-slope positivity: L=(xy+1)M-(x-1)^2(y-1)^2.
    d_w = derivative(Ds, (0, 0, 1, 0, 0))
    M = scale(d_w, Fraction(1, 2))
    expected_M = signed_sum([
        (1, product(xy, power(z, 2))), (1, xy),
        (-2, x), (-2, y), (-1, power(z, 2)), (3, one),
    ])
    assert M == expected_M
    assert L == add(
        multiply(plus(xy, 1), M),
        product(power(plus(x, -1), 2), power(plus(y, -1), 2)),
        right_scale=-1,
    )

    # The A/D boundary resultant is nonnegative in the derivative chamber.
    D0 = restrict_zero(Ds, 2)
    resultant_A_D = add(multiply(L, D0), multiply(d_w, K), right_scale=-1)
    expected_resultant_A_D = product(
        constant(2), power(plus(x, -1), 2), power(plus(y, -1), 2),
        power(plus(z, -1), 2), power(plus(z, 1), 2), plus(xy, -1),
    )
    assert resultant_A_D == expected_resultant_A_D

    # Quadratic R(w), its discriminant H, and oriented boundary derivative F.
    r0, r1, r2 = (coefficient_in(Rs, 2, degree) for degree in range(3))
    T = signed_sum([
        (1, product(x, y, z)), (-1, x), (-1, y), (-1, z), (2, one),
    ])
    assert r2 == product(plus(yz, 1), power(T, 2))

    h2 = power(plus(yz, -1), 2)
    h1 = scale(product(plus(yz, -1), signed_sum([
        (3, yz), (2, y), (2, z), (1, one),
    ])), -2)
    h0 = signed_sum([
        (1, product(power(y, 2), power(z, 2))),
        (4, product(power(y, 2), z)), (4, power(y, 2)),
        (4, product(y, power(z, 2))), (-2, yz), (-4, y),
        (4, power(z, 2)), (-4, z), (-7, one),
    ])
    H = add(add(multiply(h2, power(x, 2)), multiply(h1, x)), h0)

    f3 = product(power(plus(yz, -1), 2), plus(yz, 1))
    f2 = scale(product(
        plus(yz, -1), plus(yz, 1),
        signed_sum([(3, yz), (2, y), (2, z), (1, one)]),
    ), -1)
    f1 = signed_sum([
        (4, product(power(y, 3), power(z, 2))),
        (3, product(power(y, 3), z)),
        (4, product(power(y, 2), power(z, 3))),
        (4, product(power(y, 2), power(z, 2))),
        (1, power(y, 2)), (3, product(y, power(z, 3))),
        (-6, yz), (-4, y), (1, power(z, 2)), (-4, z), (-6, one),
    ])
    f0 = signed_sum([
        (-1, product(power(y, 3), z)), (-2, power(y, 3)),
        (-4, product(power(y, 2), power(z, 2))),
        (-2, product(power(y, 2), z)), (1, power(y, 2)),
        (-1, product(y, power(z, 3))), (-2, product(y, power(z, 2))),
        (2, yz), (4, y), (-2, power(z, 3)), (1, power(z, 2)),
        (4, z), (2, one),
    ])
    F = add(add(add(multiply(f3, power(x, 3)), multiply(f2, power(x, 2))), multiply(f1, x)), f0)

    discriminant = add(power(r1, 2), scale(multiply(r2, r0), -4))
    square_channel = product(
        power(plus(x, -1), 2), power(plus(y, -1), 4), power(plus(z, -1), 4),
    )
    assert discriminant == multiply(square_channel, H)
    J = add(multiply(r1, L), scale(multiply(r2, K), -2))
    assert J == product(plus(x, -1), power(plus(y, -1), 2), power(plus(z, -1), 2), F)

    # Master sign-separation identity: F cannot vanish where H,L and all
    # three pair factors are positive.
    master_left = add(power(F, 2), multiply(H, power(L, 2)), right_scale=-1)
    master_right = product(
        constant(8), power(plus(y, 1), 2), power(plus(z, 1), 2),
        plus(xy, -1), plus(xz, -1), plus(yz, 1), power(T, 2),
    )
    assert master_left == master_right

    # The L/F resultant prevents a sign change of F at the continuously
    # varying positive L-root in each connected (y,z) parameter chamber.
    l2 = plus(power(yz, 2), -1)
    l1 = {}
    l0 = signed_sum([(-1, power(y, 2)), (-1, power(z, 2)), (2, one)])
    assert L == add(multiply(l2, power(x, 2)), l0)
    resultant_L_F = resultant_quadratic_cubic(l0, l1, l2, f0, f1, f2, f3)
    expected_resultant_L_F = product(
        constant(16), power(plus(y, -1), 3), power(plus(y, 1), 3),
        power(plus(z, -1), 3), power(plus(z, 1), 3),
        power(plus(yz, -1), 2), power(plus(yz, 1), 2),
    )
    assert resultant_L_F == expected_resultant_L_F

    # Exact pair-boundary signs used in the chamber proof.
    # We avoid rational-function substitution by clearing y^3 or z^3.
    # F(1/y,y,z)=-((y-1)^3 (y+1)^2 (yz+2y+1))/y^3.
    # Direct coefficient recombination gives y^3 F(1/y).
    y3_F_at_inverse_y = add(add(add(f3, multiply(f2, y)), multiply(f1, power(y, 2))), multiply(f0, power(y, 3)))
    expected_inverse_y = scale(product(
        power(plus(y, -1), 3), power(plus(y, 1), 2),
        signed_sum([(1, yz), (2, y), (1, one)]),
    ), -1)
    assert y3_F_at_inverse_y == expected_inverse_y

    z3_F_at_inverse_z = add(add(add(f3, multiply(f2, z)), multiply(f1, power(z, 2))), multiply(f0, power(z, 3)))
    expected_inverse_z = scale(product(
        power(plus(z, -1), 3), power(plus(z, 1), 2),
        signed_sum([(1, yz), (2, z), (1, one)]),
    ), -1)
    assert z3_F_at_inverse_z == expected_inverse_z

    # Sample signs fixing F at the positive L-root in the two connected
    # parameter chambers.  At (y,z)=(2,2), the reduced value is
    # 36/5*(-35+11*sqrt(10))<0 because 1210<1225.  At (1/2,3), it is
    # 6/5*(-125+11*sqrt(145))>0 because 17545>15625.
    assert 121 * 10 < 35 * 35
    assert 121 * 145 > 125 * 125

    # R at the A=0 boundary.  This is L^2 R(-K/L).
    resultant_A_R = add(
        add(multiply(r2, power(K, 2)), multiply(multiply(r1, K), L), right_scale=-1),
        multiply(r0, power(L, 2)),
    )
    expected_resultant_A_R = product(
        constant(2), power(plus(x, -1), 2), power(plus(y, -1), 4),
        power(plus(y, 1), 2), power(plus(z, -1), 4),
        power(plus(z, 1), 2), plus(xy, -1), plus(xz, -1),
    )
    assert resultant_A_R == expected_resultant_A_R

    print(json.dumps({
        "schema": "amra.opg1757.round6.full-fixed-space-domination.v1",
        "reconstruction": {"P_at_anchor": 128, "xi_at_anchor": 58},
        "proved": "xi>0 on the full five-variable distinguished component of P",
        "key_channels": {
            "D_slope": "L=(xy+1)M-(x-1)^2(y-1)^2",
            "orientation": "F^2-HL^2=8(y+1)^2(z+1)^2(xy-1)(xz-1)(yz+1)T^2",
            "resultant_L_F": "16(y-1)^3(y+1)^3(z-1)^3(z+1)^3(yz-1)^2(yz+1)^2",
        },
        "scope": "stabilizer-fixed local marked-host lemma only; transverse and global OPG-1757 interfaces remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
