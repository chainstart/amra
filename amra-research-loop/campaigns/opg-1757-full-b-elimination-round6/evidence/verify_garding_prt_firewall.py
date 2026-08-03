#!/usr/bin/env python3
"""Exact PRT/derivative firewall for the K5-e cross-edge fixed space.

Only Python's standard library is used.  The script reconstructs the two
polynomials by forest enumeration and checks every displayed algebraic
identity over the integers/rationals.  C-Garding closure and the general
PRT/derivative-nesting theorem are explicitly recorded dependencies, not
claims proved by this computation.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json
from math import comb


VERTICES = tuple(range(5))
MARKED = (0, 3)
K4_EDGES = {
    (0, 1), (0, 2), (0, 4), (1, 2), (1, 4), (2, 4),
}
PATH_EDGES = {(1, 3), (2, 3)}
DELETION_EDGES = tuple(sorted(K4_EDGES | PATH_EDGES))
ORBIT_INDEX = {
    (0, 1): 0, (0, 2): 0,
    (0, 4): 1,
    (1, 2): 2,
    (1, 3): 3, (2, 3): 3,
    (1, 4): 4, (2, 4): 4,
}
NAMES = ("a", "b", "c", "d", "e")
ZERO = (0,) * len(NAMES)

# Sparse exact polynomial: exponent tuple -> integer/Fraction coefficient.
Poly = dict[tuple[int, ...], Fraction]


def clean(poly: Poly) -> Poly:
    return {m: Fraction(v) for m, v in poly.items() if v}


def add(left: Poly, right: Poly, right_scale: int = 1) -> Poly:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, Fraction(0)) + right_scale * coefficient
    return clean(result)


def scale(poly: Poly, scalar: int | Fraction) -> Poly:
    return clean({m: Fraction(scalar) * value for m, value in poly.items()})


def multiply(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for lm, lv in left.items():
        for rm, rv in right.items():
            monomial = tuple(x + y for x, y in zip(lm, rm))
            result[monomial] = result.get(monomial, Fraction(0)) + lv * rv
    return clean(result)


def derivative(poly: Poly, orders: tuple[int, ...]) -> Poly:
    result = dict(poly)
    for index, order in enumerate(orders):
        for _ in range(order):
            next_result: Poly = {}
            for monomial, coefficient in result.items():
                if monomial[index] == 0:
                    continue
                reduced = list(monomial)
                multiplier = reduced[index]
                reduced[index] -= 1
                key = tuple(reduced)
                next_result[key] = next_result.get(key, Fraction(0)) + multiplier * coefficient
            result = clean(next_result)
    return result


def restrict_zero(poly: Poly, index: int) -> Poly:
    return clean({m: value for m, value in poly.items() if m[index] == 0})


def evaluate(poly: Poly, point: tuple[int | Fraction, ...]) -> Fraction:
    return sum(
        coefficient
        * __import__("functools").reduce(
            lambda x, y: x * y,
            (Fraction(value) ** exponent for value, exponent in zip(point, monomial)),
            Fraction(1),
        )
        for monomial, coefficient in poly.items()
    )


def variable(index: int) -> Poly:
    exponent = [0] * len(NAMES)
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def constant(value: int) -> Poly:
    return {ZERO: Fraction(value)} if value else {}


def plus(poly: Poly, value: int) -> Poly:
    return add(poly, constant(value))


def power(poly: Poly, exponent: int) -> Poly:
    result = constant(1)
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def translate(poly: Poly, shifts: tuple[int | Fraction, ...]) -> Poly:
    """Substitute x_i -> x_i + shifts[i] using exact sparse arithmetic."""
    assert len(shifts) == len(NAMES)
    result: Poly = {}
    for monomial, coefficient in poly.items():
        term = constant(1)
        for index, exponent in enumerate(monomial):
            term = multiply(term, power(plus(variable(index), Fraction(shifts[index])), exponent))
        result = add(result, scale(term, coefficient))
    return clean(result)


def monomial_factor(exponents: tuple[int, ...], coefficient: int = 1) -> Poly:
    return {exponents: Fraction(coefficient)}


def coefficient_in(poly: Poly, index: int, exponent: int) -> Poly:
    result: Poly = {}
    for monomial, value in poly.items():
        if monomial[index] != exponent:
            continue
        reduced = list(monomial)
        reduced[index] = 0
        result[tuple(reduced)] = value
    return clean(result)


def divide_monomial(poly: Poly, coefficient: int, exponents: tuple[int, ...]) -> Poly:
    result: Poly = {}
    for monomial, value in poly.items():
        assert value % coefficient == 0
        assert all(x >= y for x, y in zip(monomial, exponents))
        result[tuple(x - y for x, y in zip(monomial, exponents))] = value / coefficient
    return clean(result)


def is_forest(edges: tuple[tuple[int, int], ...]) -> bool:
    parent = list(VERTICES)

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        left_root, right_root = find(left), find(right)
        if left_root == right_root:
            return False
        parent[left_root] = right_root
    return True


def connected(edges: tuple[tuple[int, int], ...], source: int, target: int) -> bool:
    adjacency = {vertex: [] for vertex in VERTICES}
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    stack, seen = [source], {source}
    while stack:
        vertex = stack.pop()
        for neighbour in adjacency[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return target in seen


def reconstruct() -> tuple[Poly, Poly, int, int]:
    deletion: Poly = {}
    xi: Poly = {}
    forest_count = connected_count = 0
    for size in range(len(DELETION_EDGES) + 1):
        for chosen in combinations(DELETION_EDGES, size):
            if not is_forest(chosen):
                continue
            forest_count += 1
            chosen_set = set(chosen)
            exponent = [0] * len(NAMES)
            for edge in DELETION_EDGES:
                if edge not in chosen_set:
                    exponent[ORBIT_INDEX[edge]] += 1
            monomial = tuple(exponent)
            deletion[monomial] = deletion.get(monomial, Fraction(0)) + 1
            if connected(chosen, *MARKED):
                connected_count += 1
                xi[monomial] = xi.get(monomial, Fraction(0)) + 1
    return clean(deletion), clean(xi), forest_count, connected_count


def affine_a_slice(poly: Poly, base: tuple[Fraction, ...]) -> dict[int, Fraction]:
    """Substitute a=base[0]+t and all other coordinates from base."""
    result: dict[int, Fraction] = {}
    for monomial, coefficient in poly.items():
        tail = coefficient
        for value, exponent in zip(base[1:], monomial[1:]):
            tail *= value**exponent
        a_exponent = monomial[0]
        for t_exponent in range(a_exponent + 1):
            value = tail * comb(a_exponent, t_exponent) * base[0] ** (a_exponent - t_exponent)
            result[t_exponent] = result.get(t_exponent, Fraction(0)) + value
    return {degree: value for degree, value in result.items() if value}


def main() -> None:
    # Graph ledger: K4 on 0,1,2,4 plus a second 1--2 route subdivided at 3.
    assert len(K4_EDGES) == 6
    assert PATH_EDGES == {(1, 3), (2, 3)}
    assert set(DELETION_EDGES) == K4_EDGES | PATH_EDGES

    P, xi, forest_count, connected_count = reconstruct()
    anchor = (Fraction(1),) * 5
    assert (forest_count, connected_count) == (128, 58)
    assert (evaluate(P, anchor), evaluate(xi, anchor)) == (128, 58)

    # Theorem 1.1 derivative-nesting channels.  Once the external C-Garding
    # dependency is invoked, every polynomial below is strictly positive on
    # C_P.  The linear channels give x_i>-1 there.
    linear_channels = {
        "a": (1, 1, 1, 2, 2),
        "b": (2, 0, 1, 2, 2),
        "c": (2, 1, 0, 2, 2),
        "d": (2, 1, 1, 1, 2),
        "e": (2, 1, 1, 2, 1),
    }
    for name, orders in linear_channels.items():
        index = NAMES.index(name)
        assert derivative(P, orders) == scale(plus(variable(index), 1), 8)

    a, _, _, d, e = (variable(index) for index in range(5))
    q_ad = add(add(multiply(a, d), a), d)
    q_ae = add(add(multiply(a, e), a), e)
    q_de = add(add(multiply(d, e), d), e)
    pair_channels = {
        "ad+a+d": ((0, 1, 1, 0, 2), q_ad),
        "ae+a+e": ((0, 1, 1, 2, 0), q_ae),
        "de+d+e": ((2, 1, 1, 0, 0), q_de),
    }
    for _, (orders, q) in pair_channels.items():
        expected = scale(multiply(q, plus(q, 2)), 2)
        assert derivative(P, orders) == expected
        assert evaluate(q, anchor) == 3

    # The b-slope itself is a nonzero derivative, hence A>0 throughout C_P.
    A = derivative(P, (0, 1, 0, 0, 0))
    assert A

    # Exact rejection of the old P>0, xi<0 candidate by two independent
    # necessary conditions: PRT along +e_a and first-derivative positivity.
    z = tuple(Fraction(value) for value in (-7, -30, -25, -15, -25))
    z = (z[0] / 5, z[1] / 5, z[2] / 5, z[3] / 5, z[4] / 5)
    assert z == (Fraction(-7, 5), -6, -5, -3, -5)
    assert evaluate(P, z) == 65
    assert evaluate(xi, z) == Fraction(-1588, 5)
    partial_a = derivative(P, (1, 0, 0, 0, 0))
    assert evaluate(partial_a, z) == -1240
    slice_polynomial = affine_a_slice(P, z)
    assert slice_polynomial == {0: Fraction(65), 1: Fraction(-1240), 2: Fraction(1350)}
    assert sum(value * Fraction(1, 2) ** degree for degree, value in slice_polynomial.items()) == Fraction(-435, 2)
    # The two roots (124 +/- sqrt(11866))/270 are both strictly positive.
    assert 124 * 124 > 11866 > 0

    # Recheck the full-b determinant and the new second-elimination wall.
    C = restrict_zero(P, 1)
    D = derivative(xi, (0, 1, 0, 0, 0))
    E = restrict_zero(xi, 1)
    delta = add(multiply(A, E), multiply(D, C), right_scale=-1)
    R = divide_monomial(delta, 2, (2, 0, 0, 0, 0))
    assert len(R) == 41 and all(value > 0 for value in R.values())

    Ac = derivative(A, (0, 0, 1, 0, 0))
    A0 = restrict_zero(A, 2)
    expected_A0 = multiply(
        monomial_factor((1, 0, 0, 1, 1)),
        multiply(plus(a, 2), multiply(plus(d, 2), plus(e, 2))),
    )
    assert A0 == expected_A0

    r0, r1, r2 = (coefficient_in(R, 2, degree) for degree in range(3))
    resultant_A_R = add(
        add(multiply(r2, power(A0, 2)), multiply(multiply(r1, A0), Ac), right_scale=-1),
        multiply(r0, power(Ac, 2)),
    )
    expected_resultant_A_R = multiply(
        monomial_factor((2, 0, 0, 4, 4), 2),
        multiply(
            power(plus(d, 2), 2),
            multiply(power(plus(e, 2), 2), multiply(q_ad, q_ae)),
        ),
    )
    assert resultant_A_R == expected_resultant_A_R

    D0 = restrict_zero(D, 2)
    Dc = derivative(D, (0, 0, 1, 0, 0))
    resultant_A_D = add(multiply(Ac, D0), multiply(Dc, A0), right_scale=-1)
    expected_resultant_A_D = multiply(
        monomial_factor((2, 0, 0, 2, 2), 2),
        multiply(power(plus(e, 2), 2), q_ad),
    )
    assert resultant_A_D == expected_resultant_A_D

    print(json.dumps({
        "schema": "amra.opg1757.round6.garding-prt-firewall.v1",
        "reconstruction": {
            "deletion_edges": [list(edge) for edge in DELETION_EDGES],
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "P_at_anchor": 128,
            "xi_at_anchor": 58,
        },
        "external_dependency": {
            "source": "Fang--Ma, Garding polynomials, arXiv:2604.27755v2",
            "url": "https://arxiv.org/html/2604.27755",
            "matroid_step": "Theorem 13.13 plus duality and Proposition 13.12 make the deletion matroid C-Garding",
            "pullback_step": "orbit repetition is a strictly positive linear pullback (Definition 4.9)",
            "component_step": "Theorem 1.1 gives PRT and nesting in every nonzero partial-derivative component",
            "non_dependency": "ordinary Garding components are not assumed convex (Example 11.7)",
        },
        "graph_decomposition": "M(K4) on 0,1,2,4; parallel-extend edge 12, then subdivide that copy into 13 and 23",
        "component_necessary_conditions": [
            "a,b,c,d,e > -1",
            "ad+a+d > 0",
            "ae+a+e > 0",
            "de+d+e > 0",
            "A=partial_b(P) > 0",
        ],
        "rejected_point": {
            "coordinates": ["-7/5", "-6", "-5", "-3", "-5"],
            "P": "65",
            "xi": "-1588/5",
            "partial_a_P": "-1240",
            "P_after_positive_a_shift": "5*(270*t^2-248*t+13)",
            "P_at_t_half": "-435/2",
            "conclusion": "outside the distinguished component by PRT and independently by derivative nesting",
        },
        "second_elimination": {
            "resultant_c_A_R": "2*a^2*d^4*e^4*(d+2)^2*(e+2)^2*(ad+a+d)*(ae+a+e)",
            "consequence": "nonnegative on the distinguished component, and strictly positive off a*d*e=0",
        },
        "scope": "exact fixed-space topology firewall; xi positivity on the whole component and OPG-1757 remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
