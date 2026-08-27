#!/usr/bin/env python3
"""Search Bernstein-block binomial-square certificates for the RLP tau core."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path
import sys


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from verify_negative_c_direct_chambers import bernstein_transform  # noqa: E402
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_nonshared_same_side_gram import positive_route_data  # noqa: E402
from explore_opg_round7_rlp_tau import build  # noqa: E402


BOUNDED = (2, 6, 7)
POSITIVE = (0, 1, 5)


def blocks(poly):
    result = defaultdict(dict)
    for monomial, value in poly.items():
        bounded = tuple(monomial[slot] for slot in BOUNDED)
        positive = tuple(monomial[slot] for slot in POSITIVE)
        result[bounded][positive] = value
    return result


def homogeneous_bernstein(poly):
    degrees = {
        slot: max(monomial[slot] for monomial in poly)
        for slot in BOUNDED
    }
    transformed = bernstein_transform(poly, list(BOUNDED))
    result = {}
    for monomial, value in transformed.items():
        exponent = [monomial[slot] for slot in POSITIVE]
        scalar = value
        for slot in BOUNDED:
            index = monomial[slot]
            degree = degrees[slot]
            exponent.extend((index, degree - index))
            scalar *= comb(degree, index)
        exponent = tuple(exponent)
        result[exponent] = result.get(exponent, Fraction()) + scalar
    return {monomial: value for monomial, value in result.items() if value}


def elevate_pair(poly, left_slot, right_slot, times):
    result = dict(poly)
    for _ in range(times):
        elevated = {}
        for monomial, value in result.items():
            for slot in (left_slot, right_slot):
                target = list(monomial)
                target[slot] += 1
                target = tuple(target)
                elevated[target] = elevated.get(target, Fraction()) + value
        result = {monomial: value for monomial, value in elevated.items() if value}
    return result


def elevate(poly, amounts):
    result = dict(poly)
    for pair, times in zip(((3, 4), (5, 6), (7, 8)), amounts):
        result = elevate_pair(result, *pair, times)
    return result


def midpoint_pairs(negative, positive_support):
    result = []
    seen = set()
    for left in positive_support:
        right = tuple(2 * middle - degree for middle, degree in zip(negative, left))
        pair = tuple(sorted((left, right)))
        if right in positive_support and left != right and pair not in seen:
            seen.add(pair)
            result.append(pair)
    return result


def solve_block(poly):
    import numpy as np
    from scipy.optimize import linprog

    positives = {monomial: value for monomial, value in poly.items() if value > 0}
    negatives = {monomial: value for monomial, value in poly.items() if value < 0}
    variables = []
    for negative in negatives:
        for pair in midpoint_pairs(negative, positives):
            variables.append((negative, pair))
    if any(not any(item[0] == negative for item in variables) for negative in negatives):
        return None, "missing_pair"

    negative_rows = list(negatives)
    positive_rows = list(positives)
    a_equal = np.zeros((len(negative_rows), len(variables)))
    b_equal = np.array([float(-negatives[item] / 2) for item in negative_rows])
    for column, (negative, _) in enumerate(variables):
        a_equal[negative_rows.index(negative), column] = 1
    a_upper = np.zeros((len(positive_rows), len(variables)))
    b_upper = np.array([float(positives[item]) for item in positive_rows])
    for column, (_, pair) in enumerate(variables):
        for endpoint in pair:
            a_upper[positive_rows.index(endpoint), column] += 1
    result = linprog(
        np.zeros(len(variables)),
        A_ub=a_upper,
        b_ub=b_upper,
        A_eq=a_equal,
        b_eq=b_equal,
        bounds=(0, None),
        method="highs",
    )
    if not result.success:
        return None, result.message
    rational = [Fraction(float(value)).limit_denominator(1000000) for value in result.x]
    return [
        (weight, negative, pair)
        for weight, (negative, pair) in zip(rational, variables)
        if weight
    ], "ok"


def verify_block(poly, certificate):
    residual = dict(poly)
    for weight, negative, pair in certificate:
        left, right = pair
        residual[left] -= weight
        residual[right] -= weight
        residual[negative] += 2 * weight
    residual = {monomial: value for monomial, value in residual.items() if value}
    assert all(value > 0 for value in residual.values())
    return residual


def solve_atoms(target, atoms):
    import numpy as np
    from scipy.optimize import linprog

    support = sorted(set(target).union(*(set(atom) for atom in atoms)))
    matrix = np.zeros((len(support), len(atoms)))
    for column, atom in enumerate(atoms):
        for monomial, value in atom.items():
            matrix[support.index(monomial), column] = float(value)
    bound = np.array([float(target.get(monomial, Fraction())) for monomial in support])
    result = linprog(
        np.ones(len(atoms)),
        A_ub=matrix,
        b_ub=bound,
        bounds=(0, None),
        method="highs",
        options={"dual_feasibility_tolerance": 1e-9, "primal_feasibility_tolerance": 1e-9},
    )
    return result, support


def multi_square_atoms():
    c, q0, s0, q4, s4, tau = (variable(slot) for slot in (0, 1, 2, 5, 6, 7))
    _, _, determinant_sum = positive_route_data(1)
    one_minus_tau = add(constant(1), tau, -1)
    a = add(
        add(
            add(
                multiply(multiply(multiply(q0, q4), s0), s4),
                multiply(multiply(q0, q4), power(s4, 2)),
            ),
            multiply(multiply(q0, q4), s4),
            -1,
        ),
        add(
            add(multiply(q0, s0), multiply(q4, multiply(power(s0, 2), power(s4, 2)))),
            power(s0, 2),
        ),
    )
    atoms = []
    for monomial, value in power(determinant_sum, 3).items():
        route_weight = {monomial: value}
        polynomial = multiply(
            multiply(route_weight, c),
            multiply(power(a, 2), power(one_minus_tau, 3)),
        )
        atoms.append(homogeneous_bernstein(polynomial))
        k0_root = multiply(
            add(q0, s0),
            add(constant(1), multiply(q4, power(s4, 2))),
        )
        k0_polynomial = multiply(
            multiply(route_weight, multiply(q4, power(s0, 2))),
            multiply(power(k0_root, 2), power(one_minus_tau, 3)),
        )
        atoms.append(homogeneous_bernstein(k0_polynomial))

    one_minus_s4 = add(constant(1), s4, -1)
    j8 = add(
        power(add(multiply(q0, one_minus_s4), s0), 2),
        multiply(
            power(s0, 2),
            multiply(
                power(s4, 2),
                add(add(multiply(q0, q4), q0), q4),
            ),
        ),
    )
    for route_weight in (
        multiply(power(c, 4), power(q4, 3)),
        multiply(power(c, 3), power(q4, 4)),
    ):
        atoms.append(homogeneous_bernstein(
            multiply(route_weight, multiply(power(j8, 2), power(tau, 3)))
        ))
    return atoms


def main():
    h1884 = build()[0]
    transformed = bernstein_transform(h1884, list(BOUNDED))
    grouped = blocks(transformed)
    failures = []
    total_squares = 0
    for bounded, polynomial in sorted(grouped.items()):
        if all(value > 0 for value in polynomial.values()):
            continue
        certificate, status = solve_block(polynomial)
        if certificate is None:
            failures.append((bounded, status, len(polynomial), sum(v < 0 for v in polynomial.values())))
            continue
        try:
            verify_block(polynomial, certificate)
        except AssertionError:
            failures.append((bounded, "rationalization", len(polynomial), sum(v < 0 for v in polynomial.values())))
            continue
        total_squares += len(certificate)
        print("BLOCK", bounded, "terms", len(polynomial), "squares", len(certificate))
    print("SUMMARY", "blocks", len(grouped), "squares", total_squares, "failures", len(failures))
    for failure in failures:
        print("FAIL", failure)

    homogeneous = homogeneous_bernstein(h1884)
    print(
        "HOMOGENEOUS",
        "terms", len(homogeneous),
        "negative", sum(value < 0 for value in homogeneous.values()),
    )
    certificate, status = solve_block(homogeneous)
    if certificate is None:
        print("HOMOGENEOUS_FAIL", status)
    else:
        residual = verify_block(homogeneous, certificate)
        print(
            "HOMOGENEOUS_OK",
            "squares", len(certificate),
            "residual", len(residual),
            "minimum", min(residual.values()),
        )
    candidates = (
        (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 0, 1), (2, 0, 1), (1, 0, 2),
        (1, 1, 0), (0, 1, 1), (2, 1, 1),
        (1, 1, 1), (2, 2, 2),
    )
    for amounts in candidates:
        elevated = elevate(homogeneous, amounts)
        positives = {m for m, value in elevated.items() if value > 0}
        missing = [
            m for m, value in elevated.items()
            if value < 0 and not midpoint_pairs(m, positives)
        ]
        print(
            "ELEVATED", amounts,
            "terms", len(elevated),
            "negative", sum(value < 0 for value in elevated.values()),
            "missing", len(missing),
        )
        if missing:
            if len(missing) <= 3:
                print("ELEVATED_MISSING", amounts, [(item, elevated[item]) for item in missing])
            continue
        certificate, status = solve_block(elevated)
        print("ELEVATED_SOLVE", amounts, status, 0 if certificate is None else len(certificate))
        if certificate is not None:
            residual = verify_block(elevated, certificate)
            print("ELEVATED_OK", amounts, len(certificate), len(residual), min(residual.values()))
            break

    base_atoms = multi_square_atoms()
    positives = {m for m, value in homogeneous.items() if value > 0}
    binomial_atoms = []
    for negative, value in homogeneous.items():
        if value >= 0:
            continue
        for left, right in midpoint_pairs(negative, positives):
            binomial_atoms.append({left: Fraction(1), right: Fraction(1), negative: Fraction(-2)})
    atoms = base_atoms + binomial_atoms
    print("ATOM_LP", "multi", len(base_atoms), "binomial", len(binomial_atoms))
    result, _ = solve_atoms(homogeneous, atoms)
    print("ATOM_LP_RESULT", result.success, result.message)
    if result.success:
        print("ATOM_LP_NONZERO", sum(value > 1e-8 for value in result.x))


if __name__ == "__main__":
    main()
