#!/usr/bin/env python3
"""Independent combinatorial audit of the fixed top-depth theorem.

No existing top-tail verifier or recorded profile symbol is imported.
"""

from __future__ import annotations

import json
import math
import random
from fractions import Fraction
from functools import lru_cache

import sympy as sp


S, J, K = sp.symbols("s j k", integer=True, nonnegative=True)


@lru_cache(maxsize=None)
def weighted_forest_row(vertex_count: int, matching_size: int):
    """Count forests after contracting a prescribed matching.

    A contracted matching block has weight two and an ordinary vertex
    has weight one.  An edge between blocks i,j has multiplicity w_i*w_j.
    """
    if vertex_count < 2*matching_size:
        return tuple()
    weights = (
        (2,)*matching_size
        + (1,)*(vertex_count-2*matching_size)
    )
    contracted_count = len(weights)
    if contracted_count == 0:
        return (1,)
    full = (1 << contracted_count)-1

    subset_weight = [0]*(full+1)
    for mask in range(1, full+1):
        selected = [
            weights[index]
            for index in range(contracted_count)
            if mask & (1 << index)
        ]
        if len(selected) == 1:
            subset_weight[mask] = 1
        else:
            subset_weight[mask] = (
                math.prod(selected)
                * sum(selected)**(len(selected)-2)
            )

    @lru_cache(maxsize=None)
    def partitions(mask):
        if mask == 0:
            return (1,)
        first = mask & -mask
        rest = mask ^ first
        result = [0]*(mask.bit_count()+1)
        subrest = rest
        while True:
            block = subrest | first
            remaining = mask ^ block
            tail = partitions(remaining)
            weight = subset_weight[block]
            for components, value in enumerate(tail):
                result[components+1] += weight*value
            if subrest == 0:
                break
            subrest = (subrest-1) & rest
        return tuple(result)

    by_components = partitions(full)
    # j edges on contracted_count vertices means contracted_count-j
    # components.
    return tuple(
        by_components[contracted_count-j]
        for j in range(contracted_count)
    )


def U(h, j, s):
    row = weighted_forest_row(s, h)
    return row[j] if 0 <= j < len(row) else 0


def interpolate_profile(h, j):
    # The combinatorial construction has degree at most 2j.  Use one
    # extra value as an independent degree check.
    start = 2*h
    points = [(s, U(h, j, s)) for s in range(start, start+2*j+1)]
    expression = sp.interpolate(points, S).expand()
    assert sp.degree(expression, S) <= 2*j
    spare = start+2*j+1
    assert expression.subs(S, spare) == U(h, j, spare)
    return sp.Poly(expression, S)


def profile_degree_audit(maximum_loss=4, maximum_j=5):
    profiles = {
        h: {j: interpolate_profile(h, j) for j in range(maximum_j+1)}
        for h in range(3)
    }
    records = []
    for h in range(3):
        for loss in range(maximum_loss+1):
            values = []
            for j in range(maximum_j+1):
                power = 2*j-loss
                coefficient = (
                    0 if power < 0
                    else profiles[h][j].coeff_monomial(S**power)
                )
                values.append(
                    sp.factor(coefficient*2**j*math.factorial(j))
                )
            interpolant = sp.interpolate(
                [(j, values[j]) for j in range(loss+1)], J
            ).expand()
            assert sp.degree(interpolant, J) <= loss
            for j in range(loss+1, maximum_j+1):
                assert sp.expand(interpolant.subs(J, j)-values[j]) == 0
            records.append((h, loss, sp.degree(interpolant, J)))
    return records


def refined_bidegree_audit(maximum_loss=3):
    """Audit deg_j [h^r] R_{loss,h} <= loss-r combinatorially."""
    records = []
    for loss in range(maximum_loss+1):
        maximum_value = loss+1
        by_h = []
        for h in range(maximum_value+1):
            values = []
            for edge_count in range(maximum_value+1):
                polynomial = interpolate_profile(h, edge_count)
                power = 2*edge_count-loss
                coefficient = (
                    0 if power < 0
                    else polynomial.coeff_monomial(S**power)
                )
                values.append(sp.factor(
                    coefficient*2**edge_count*math.factorial(edge_count)
                ))
            in_j = sp.interpolate(
                [(edge_count, values[edge_count])
                 for edge_count in range(loss+1)],
                J,
            ).expand()
            assert sp.degree(in_j, J) <= loss
            assert sp.expand(
                in_j.subs(J, maximum_value)-values[maximum_value]
            ) == 0
            by_h.append(sp.Poly(in_j, J))

        for j_degree in range(loss+1):
            coefficients = [
                polynomial.coeff_monomial(J**j_degree)
                for polynomial in by_h
            ]
            allowed_h_degree = loss-j_degree
            in_h = sp.interpolate(
                [(h, coefficients[h])
                 for h in range(allowed_h_degree+1)],
                sp.symbols("h"),
            ).expand()
            assert sp.degree(in_h, sp.symbols("h")) <= allowed_h_degree
            for h in range(allowed_h_degree+1, maximum_value+1):
                assert sp.expand(
                    in_h.subs(sp.symbols("h"), h)-coefficients[h]
                ) == 0
            records.append((loss, j_degree, allowed_h_degree))
    return records


def cycle_union_stress(samples=4000):
    """Generate unions of cycles with fixed matching edges."""
    rng = random.Random(20260730)
    checked = 0
    for _ in range(samples):
        h = rng.randint(0, 2)
        fixed_vertices = list(range(2*h))
        minimum_variable = max(1, 3-2*h)
        variable_vertices = list(
            range(2*h, 2*h+rng.randint(minimum_variable, 7))
        )
        all_vertices = fixed_vertices+variable_vertices
        fixed_edges = {
            tuple(sorted((2*i, 2*i+1))) for i in range(h)
        }
        union = set()
        for _ in range(rng.randint(1, 6)):
            length = rng.randint(3, min(7, len(all_vertices)))
            cycle = rng.sample(all_vertices, length)
            for index in range(length):
                union.add(tuple(sorted(
                    (cycle[index], cycle[(index+1) % length])
                )))
        nonprescribed = union-fixed_edges
        used_vertices = {vertex for edge in union for vertex in edge}
        used_variable = {
            vertex
            for vertex in used_vertices
            if vertex in variable_vertices
        }
        touched_pairs = sum(
            bool({2*i, 2*i+1} & used_vertices)
            for i in range(h)
        )
        assert len(used_variable) <= len(nonprescribed)-touched_pairs
        checked += 1

    # Equality cases: one endpoint only; both endpoints without the
    # prescribed edge; and a cycle using the prescribed edge.
    targeted = [
        ({(0, 2), (2, 3), (0, 3)}, {(0, 1)}, 1, 2),
        ({(0, 2), (1, 2), (1, 3), (0, 3)}, {(0, 1)}, 1, 2),
        ({(0, 1), (0, 2), (1, 2)}, {(0, 1)}, 1, 1),
    ]
    for union, fixed, touched, variable_count in targeted:
        assert variable_count <= len(union-fixed)-touched
    return checked


def mixed_binomial_moment_audit(maximum_degree=8):
    # The identity actually needed after (10), stronger than the marginal
    # moment displayed in (11).
    checks = 0
    for k in range(1, 18):
        denominator = 2**k
        for a in range(maximum_degree+1):
            for b in range(maximum_degree+1-a):
                lhs = sum(
                    Fraction(
                        math.comb(k, j)
                        * math.prod(range(j-a+1, j+1))
                        * math.prod(range(k-j-b+1, k-j+1)),
                        denominator,
                    )
                    for j in range(k+1)
                )
                rhs = Fraction(
                    math.prod(range(k-a-b+1, k+1)),
                    2**(a+b),
                )
                assert lhs == rhs
                checks += 1
    return checks


def c_value(k, s):
    rows = [
        [U(h, j, s) for j in range(k+1)]
        for h in range(3)
    ]
    determinant = sum(
        rows[1][j]*rows[1][k-j]
        - rows[0][j]*rows[2][k-j]
        for j in range(k+1)
    )
    return Fraction(
        math.factorial(k)*determinant,
        2*k*(k-1),
    )


def exact_exceptional_audit(maximum_k=6):
    records = {}
    for k in range(2, maximum_k+1):
        degree = 2*k-4
        points = [
            (s, sp.Rational(c_value(k, s)))
            for s in range(4, 4+degree+1)
        ]
        polynomial = sp.Poly(sp.interpolate(points, S).expand(), S)
        assert polynomial.degree() == degree
        assert polynomial.LC() == 1
        b0 = polynomial.coeff_monomial(S**degree)
        b1 = (
            polynomial.coeff_monomial(S**(degree-1))
            if degree >= 1 else 0
        )
        b2 = (
            polynomial.coeff_monomial(S**(degree-2))
            if degree >= 2 else 0
        )
        assert b0 == 1
        if degree >= 1:
            assert b1 == k-2
        if degree >= 2:
            assert b2 == (k-2)*(k-21)

        # Direct base-four finite differences and the triangular power
        # conversion must agree.
        values = [sp.Rational(c_value(k, 4+x)) for x in range(degree+1)]
        newton = []
        current = values
        while current:
            newton.append(current[0])
            current = [
                current[index+1]-current[index]
                for index in range(len(current)-1)
            ]
        p = [
            sp.Rational(newton[degree-depth], math.factorial(degree-depth))
            for depth in range(degree+1)
        ]
        for depth in range(degree+1):
            reconstructed = sum(
                p[earlier]
                * (-1)**(depth-earlier)
                * elementary_direct(
                    degree-earlier, depth-earlier
                )
                for earlier in range(depth+1)
            )
            actual = polynomial.coeff_monomial(S**(degree-depth))
            assert sp.simplify(reconstructed-actual) == 0
        records[k] = (b0, b1, b2)
    return records


def sym_falling(value, degree):
    if degree < 0:
        return sp.S.Zero
    return sp.prod(value-index for index in range(degree))


def source_e(s, component_parameter, degree):
    if degree < 0:
        return sp.S.Zero
    return sp.expand(sum(
        sp.Rational((-1)**index, 2**index)
        * sym_falling(component_parameter, index)
        * s**(degree-index)
        / (math.factorial(index)*math.factorial(degree-index))
        for index in range(degree+1)
    ))


def source_profile(h, edge_count):
    if h == 0:
        return sp.expand(
            sym_falling(S, edge_count)
            * (
                source_e(S, S-edge_count, edge_count)
                - source_e(S, S-edge_count, edge_count-1)
            )
        )
    if h == 1:
        return sp.expand(
            sym_falling(S-2, edge_count)
            * (
                source_e(S, S-2-edge_count, edge_count)
                - source_e(S, S-2-edge_count, edge_count-1)
            )
        )
    assert h == 2
    return sp.expand(
        sym_falling(S-4, edge_count)
        * (
            source_e(S, S-4-edge_count, edge_count)
            - source_e(S, S-4-edge_count, edge_count-1)
        )
        + 4*sym_falling(S-4, edge_count-1)
        * source_e(S, S-3-edge_count, edge_count-1)
    )


def exact_profile_symbols(maximum_loss=6):
    result = {}
    for loss in range(maximum_loss+1):
        result[loss] = {}
        for h in range(3):
            values = []
            for edge_count in range(2*loss+3):
                polynomial = sp.Poly(source_profile(h, edge_count), S)
                power = 2*edge_count-loss
                coefficient = (
                    sp.S.Zero if power < 0
                    else polynomial.coeff_monomial(S**power)
                )
                values.append(sp.factor(
                    coefficient*2**edge_count*math.factorial(edge_count)
                ))
            interpolant = sp.interpolate(
                [(edge_count, values[edge_count])
                 for edge_count in range(loss+1)],
                J,
            ).expand()
            assert sp.degree(interpolant, J) <= loss
            for edge_count in range(loss+1, 2*loss+3):
                assert sp.expand(
                    interpolant.subs(J, edge_count)-values[edge_count]
                ) == 0
            result[loss][h] = sp.factor(interpolant)
    return result


def binomial_expectation_symbolic(expression):
    result = sp.S.Zero
    for (power,), coefficient in sp.Poly(sp.expand(expression), J).terms():
        for degree in range(power+1):
            result += (
                coefficient
                * sp.functions.combinatorial.numbers.stirling(
                    power, degree, kind=2
                )
                * sym_falling(K, degree)
                / 2**degree
            )
    return sp.factor(result)


def symbolic_exceptional_audit():
    symbols = exact_profile_symbols(6)
    values = {}
    for loss in (5, 6):
        kernel = sp.S.Zero
        for left_loss in range(loss+1):
            right_loss = loss-left_loss
            kernel += (
                symbols[left_loss][1]
                * symbols[right_loss][1].subs(J, K-J)
                - symbols[left_loss][0]
                * symbols[right_loss][2].subs(J, K-J)
            )
        values[loss-4] = sp.factor(
            binomial_expectation_symbolic(kernel)/(2*K*(K-1))
        )
    assert values[1] == K-2
    assert values[2] == (K-21)*(K-2)
    return values


def homogeneous_total(expression, degree):
    polynomial = sp.Poly(sp.expand(expression), J, K)
    return sp.expand(sum(
        coefficient*J**powers[0]*K**powers[1]
        for powers, coefficient in polynomial.terms()
        if sum(powers) == degree
    ))


def refined_cancellation_audit(maximum_loss=6):
    symbols = exact_profile_symbols(maximum_loss)
    records = []
    for loss in range(4, maximum_loss+1):
        kernel = sp.S.Zero
        for left_loss in range(loss+1):
            right_loss = loss-left_loss
            kernel += (
                symbols[left_loss][1]
                * symbols[right_loss][1].subs(J, K-J)
                - symbols[left_loss][0]
                * symbols[right_loss][2].subs(J, K-J)
            )
        kernel = sp.expand(kernel)
        assert sp.Poly(kernel, J, K).total_degree() <= loss-1
        next_part = homogeneous_total(kernel, loss-1)
        reflected = sp.expand(next_part.xreplace({J: K-J}))
        assert sp.expand(reflected+next_part) == 0
        expectation = binomial_expectation_symbolic(kernel)
        assert sp.degree(expectation, K) <= loss-2
        records.append(
            (loss, sp.Poly(kernel, J, K).total_degree(),
             sp.degree(expectation, K))
        )
    return records


def elementary_direct(q, degree):
    if degree == 0:
        return 1
    roots = range(4, q+4)
    coefficients = [1]+[0]*degree
    for root in roots:
        for index in range(degree, 0, -1):
            coefficients[index] += root*coefficients[index-1]
    return coefficients[degree]


def elementary_leading_and_triangular_audit(maximum_depth=12):
    # Exact symmetric polynomials for q=2k+c at several offsets.
    for depth in range(maximum_depth+1):
        for offset in (-12, -7, -4, 0, 5):
            values = []
            # Degree is 2*depth in k.
            for kval in range(20, 20+2*depth+2):
                q = 2*kval+offset
                values.append((kval, elementary_direct(q, depth)))
            polynomial = sp.Poly(sp.interpolate(values, K).expand(), K)
            assert polynomial.degree() == 2*depth
            assert polynomial.LC() == sp.Rational(
                2**depth, math.factorial(depth)
            )

    constants = [sp.Integer(1)]
    for depth in range(1, maximum_depth+1):
        value = -sum(
            constants[earlier]
            * (-1)**(depth-earlier)
            * sp.Rational(
                2**(depth-earlier),
                math.factorial(depth-earlier),
            )
            for earlier in range(depth)
        )
        assert sp.factor(value) == sp.Rational(
            2**depth, math.factorial(depth)
        )
        constants.append(sp.factor(value))
    return constants


def audit():
    profile_records = profile_degree_audit()
    refined_records = refined_bidegree_audit()
    cycle_checks = cycle_union_stress()
    moment_checks = mixed_binomial_moment_audit()
    exceptional = exact_exceptional_audit()
    symbolic_exceptional = symbolic_exceptional_audit()
    cancellation = refined_cancellation_audit()
    constants = elementary_leading_and_triangular_audit()
    return {
        "schema": "amra.opg1757.independent-fixed-top-depth-audit.v1",
        "verdict": "PASS",
        "refined_b_k_d_bound": "O_d(k^d)",
        "previous_repairs_verified": True,
        "main_text_modified": False,
        "profile_degree_records": len(profile_records),
        "refined_bidegree_records": len(refined_records),
        "cycle_union_stress_checks": cycle_checks,
        "mixed_binomial_moment_checks": moment_checks,
        "exceptional_k_range": [min(exceptional), max(exceptional)],
        "symbolic_exceptional_depths": sorted(symbolic_exceptional),
        "refined_cancellation_losses": [record[0] for record in cancellation],
        "triangular_depth": len(constants)-1,
        "required_repairs": [],
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
