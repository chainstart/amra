"""Finite certificates for the Round 30 escape-route audit."""

from __future__ import annotations

from fractions import Fraction
from math import prod

import sympy as sp

from verify_resonant_ansatz_no_go import first_prime_product


def actual_quadratic_gap_certificate(side_length: int) -> dict:
    """Exact H for A={i+jY:0<=i,j<L} at the actual SAT parameters."""
    if side_length < 2:
        raise ValueError("side length must be at least two")
    length = side_length
    n = length * length
    overlap_u_three = length * max(length - 3, 0)
    overlap_v_minus_two_y = length * max(length - 2, 0)
    total = (n + overlap_u_three) * (n + overlap_v_minus_two_y)
    supported = [(0, 0)]
    if length >= 3:
        supported.append((0, -2))
    if length >= 4:
        supported.extend(((3, 0), (3, -2)))
    return {
        "side_length": length,
        "n": n,
        "supported_coefficient_pairs": tuple(supported),
        "H": total,
        "average_degree": Fraction(total, n * n),
        "limit": 4,
    }


def direct_actual_quadratic_gap_energy(side_length: int) -> dict:
    """Enumerate all weighted difference pairs in the quadratic GAP."""
    length = side_length
    differences = [
        ((a, b), (length - abs(a)) * (length - abs(b)))
        for a in range(-length + 1, length)
        for b in range(-length + 1, length)
    ]
    total = 0
    supported = []
    for (a, b), first_weight in differences:
        for (c, d), second_weight in differences:
            rational_times_four = (
                4 * a * a
                + 12285 * b * b
                - 4 * c * c
                - 12285 * d * d
                - 12 * a
                - 24570 * d
            )
            radical_coefficient = (
                2 * a * b - 2 * c * d - 3 * b - 2 * c
            )
            if rational_times_four == 0 and radical_coefficient == 0:
                total += first_weight * second_weight
                supported.append(((a, b), (c, d)))
    return {"H": total, "supported": tuple(supported)}


def generic_rank_two_gap_lemma() -> dict:
    """Coefficient comparison for A={i+j theta}.

    If theta is transcendental or has degree >2 over Q(Y), the theta^2,
    theta, and constant coefficients vanish separately.  Nondegeneracy
    X!=+-Y forces the theta coefficients of u and v to vanish.
    """
    return {
        "degree_condition": "[Q(Y,theta):Q(Y)]>2 or theta transcendental",
        "supported_pairs": ((0, 0), (3, 0)),
        "average_upper_bound": "2-1/n",
        "reason": (
            "theta^2 gives y^2=w^2; theta coefficient and X!=+-Y "
            "force y=w=0"
        ),
    }


def quadratic_unit_orbit_count(coefficient_bound: int) -> dict:
    """Count powers of 3+2sqrt(2) with both coefficients bounded."""
    if coefficient_bound < 1:
        raise ValueError("bound must be positive")
    a, b = 1, 0
    positive = []
    exponent = 0
    while abs(a) <= coefficient_bound and abs(b) <= coefficient_bound:
        positive.append((exponent, a, b))
        a, b = 3 * a + 4 * b, 2 * a + 3 * b
        exponent += 1
    # Include negative exponents; conjugation changes b to -b.
    count = 2 * len(positive) - 1
    return {
        "bound": coefficient_bound,
        "nonnegative_powers": tuple(positive),
        "signed_power_count": count,
        "logarithmic_comparison": count <= 3 + 4 * coefficient_bound.bit_length(),
    }


def rational_s_unit_lattice_certificate(prime_count: int) -> dict:
    """A rational multiplicative subgroup collapses to divisor scale.

    Parameters are all positive divisors t of the primorial D.  Clearing
    denominators with the one-dimensional lattice step 1/(2D) makes both
    u(t) and c(t) integer shifts.  A box twice their maximum magnitude
    makes every shift popular by a constant proportion.
    """
    denominator = first_prime_product(prime_count)
    parameters = tuple(int(value) for value in sp.divisors(denominator))
    shift_pairs = []
    maximum = 0
    for parameter in parameters:
        # Coordinates relative to g=1/(2D).
        u_coordinate = (
            denominator * parameter
            - 3069 * denominator // parameter
            + 3 * denominator
        )
        c_coordinate = (
            denominator * parameter
            + 3069 * denominator // parameter
        )
        maximum = max(maximum, abs(u_coordinate), abs(c_coordinate))
        shift_pairs.append((parameter, u_coordinate, c_coordinate))
    p_size = 2 * maximum + 1
    n = 2 * p_size
    extra = 0
    for _, u_coordinate, c_coordinate in shift_pairs:
        overlap_u = 2 * (p_size - abs(u_coordinate))
        overlap_v = p_size - abs(c_coordinate)
        extra += 2 * overlap_u * overlap_v
    total = n * n + extra
    return {
        "prime_count": prime_count,
        "denominator": denominator,
        "parameter_count": len(parameters),
        "parameters": parameters,
        "shift_pairs": tuple(shift_pairs),
        "n": n,
        "H_lower_bound": total,
        "average_lower_bound": Fraction(total, n * n),
        "uniform_average_lower_bound": 1 + Fraction(len(parameters), 4),
        "growth_class": "exp(Theta(log(n)/loglog(n)))",
    }


def multiple_layer_mass_ledger(layer_sizes, layer_average_degrees) -> dict:
    """Generic-union and independent-tensor composition rules."""
    sizes = tuple(layer_sizes)
    degrees = tuple(layer_average_degrees)
    if len(sizes) != len(degrees) or not sizes:
        raise ValueError("need equally sized nonempty inputs")
    total_size = sum(sizes)
    union_gain = sum(
        size * size * (degree - 1)
        for size, degree in zip(sizes, degrees)
    ) / (total_size * total_size)
    tensor_size = prod(sizes)
    tensor_degree = 1 + sum(degree - 1 for degree in degrees)
    return {
        "union_size": total_size,
        "union_average_degree": 1 + union_gain,
        "union_upper_bound": max(degrees),
        "tensor_size": tensor_size,
        "tensor_average_degree": tensor_degree,
    }


def breakthrough_target_ledger() -> dict:
    return {
        "target_average_degree": "n^(2/5)",
        "equivalent_weighted_incidence": (
            "sum_t r_A(u(t))*(r_A(c(t)-Y)+r_A(-c(t)-Y)) >= n^(12/5)"
        ),
        "uncovered_candidate": (
            "growing-degree/growing-rank noncommensurable multiplicative "
            "set whose hyperbola image lies in the popular difference set "
            "of one small-doubling A"
        ),
        "fixed_density_requirement": (
            "if all relevant overlaps are >=rho*n, need "
            "|T| >= (1/(2*rho^2))*n^(2/5)"
        ),
        "currently_observed": (
            "fixed fields: ideal divisors times units; rational S-units: "
            "divisor scale; generic rank-two GAP: constant"
        ),
    }


if __name__ == "__main__":
    print("quadratic SAT GAP")
    for length in range(2, 13):
        result = actual_quadratic_gap_certificate(length)
        print(length, result["H"], result["average_degree"])
    print("quadratic units")
    for bound in (10, 100, 10_000, 10**8):
        result = quadratic_unit_orbit_count(bound)
        print(bound, result["signed_power_count"])
    print("rational S-unit grids")
    for prime_count in (3, 5, 7):
        result = rational_s_unit_lattice_certificate(prime_count)
        print(
            prime_count,
            result["parameter_count"],
            result["n"],
            result["average_lower_bound"],
        )
    print(breakthrough_target_ledger())
