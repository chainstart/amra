#!/usr/bin/env python3
"""Exact exponent certificate for the 9/41 endpoint energy dichotomy."""

from fractions import Fraction


def endpoint_energy_ledger() -> dict[str, Fraction]:
    point_exponent = Fraction(105, 41)
    x_aspect = Fraction(41, 105)
    family_exponent = Fraction(64, 105)

    incidence_exponent = point_exponent * Fraction(4, 3)
    slope_count = point_exponent * (1 - family_exponent)
    lines_per_slope = point_exponent * family_exponent
    energy_product = point_exponent * (3 - x_aspect)
    additive_min = point_exponent * 2 * family_exponent
    additive_max = point_exponent * 3 * family_exponent
    multiplicative_min = 2 * slope_count
    multiplicative_max = 3 * slope_count
    improved_additive_min = energy_product - multiplicative_max

    assert x_aspect == Fraction(41, 105)
    assert family_exponent == Fraction(64, 105)
    assert incidence_exponent == Fraction(140, 41)
    assert slope_count == 1
    assert lines_per_slope == Fraction(64, 41)
    assert energy_product == Fraction(274, 41)
    assert additive_min == Fraction(128, 41)
    assert additive_max == Fraction(192, 41)
    assert multiplicative_min == 2
    assert multiplicative_max == 3
    assert improved_additive_min == Fraction(151, 41)

    eta_max = (
        Fraction(192, 41) - improved_additive_min
    ) * 41
    assert eta_max == 41

    # The parameterization e_add=(192-eta)/41 forces
    # e_mult >= (82+eta)/41.
    for eta in range(42):
        e_add = Fraction(192 - eta, 41)
        e_mult = energy_product - e_add
        assert e_mult == Fraction(82 + eta, 41)
        assert e_add >= improved_additive_min
        assert multiplicative_min <= e_mult <= multiplicative_max

    return {
        "point_exponent": point_exponent,
        "x_aspect": x_aspect,
        "parallel_family_beta": family_exponent,
        "incidence_exponent": incidence_exponent,
        "slope_count": slope_count,
        "lines_per_slope": lines_per_slope,
        "energy_product": energy_product,
        "additive_min_raw": additive_min,
        "additive_max": additive_max,
        "additive_min_feasible": improved_additive_min,
        "multiplicative_min": multiplicative_min,
        "multiplicative_max": multiplicative_max,
        "eta_max": eta_max,
    }


def main() -> None:
    print(endpoint_energy_ledger())
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
