"""Independent red-team tests for the anisotropic-grid note."""

from fractions import Fraction
from math import gcd

from verify_critical_anisotropic_grid import (
    chebyshev_value,
    enumerated_ledger,
    exact_formula,
)


def denominator_valuation(value: Fraction, prime: int) -> int:
    denominator = value.denominator
    valuation = 0
    while denominator % prime == 0:
        denominator //= prime
        valuation += 1
    return valuation


def test_line_and_energy_formulas_for_all_small_integer_ratios() -> None:
    for ratio in range(2, 8):
        for radius_count in range(1, 6):
            for height_count in range(1, 8):
                assert enumerated_ledger(
                    radius_count, height_count, ratio
                ) == exact_formula(radius_count, height_count)


def test_every_reduced_odd_prime_denominator_in_small_range() -> None:
    for denominator in range(3, 31):
        odd_prime_divisors = tuple(
            prime
            for prime in (3, 5, 7, 11, 13, 17, 19, 23, 29)
            if denominator % prime == 0
        )
        if not odd_prime_divisors:
            continue
        for numerator in range(-denominator + 1, denominator):
            if gcd(numerator, denominator) != 1:
                continue
            cosine = Fraction(numerator, denominator)
            for prime in odd_prime_divisors:
                exponent = 0
                remaining = denominator
                while remaining % prime == 0:
                    exponent += 1
                    remaining //= prime
                for index in range(1, 21):
                    gap = Fraction(1) - chebyshev_value(
                        cosine, index
                    )
                    assert denominator_valuation(gap, prime) == (
                        exponent * index
                    )


def test_power_of_two_denominators_beyond_three_quarters() -> None:
    for exponent in range(2, 7):
        denominator = 2**exponent
        for numerator in range(-denominator + 1, denominator, 2):
            cosine = Fraction(numerator, denominator)
            for index in range(1, 31):
                value = chebyshev_value(cosine, index)
                assert value.denominator == 2 ** (
                    (exponent - 1) * index + 1
                )
                gap = Fraction(1) - value
                assert gap.denominator == value.denominator


def test_denominator_two_is_a_real_resonant_exception() -> None:
    for cosine in (Fraction(1, 2), Fraction(-1, 2)):
        values = tuple(chebyshev_value(cosine, index) for index in range(24))
        assert all(value.denominator == 1 or value.denominator == 2 for value in values)
        assert len(set(values)) <= 4
        assert values[12:] == values[:12]


def test_common_radius_distance_sets_meet_the_p_adic_bounds() -> None:
    cases = (
        Fraction(3, 4),
        Fraction(1, 4),
        Fraction(-5, 8),
        Fraction(2, 3),
        Fraction(3, 5),
        Fraction(4, 9),
    )
    for height_count in range(2, 9):
        for angular_size in range(2, 15):
            for cosine in cases:
                distances = {
                    Fraction(difference * difference)
                    + 2
                    * height_count
                    * height_count
                    * (
                        Fraction(1)
                        - chebyshev_value(cosine, index)
                    )
                    for difference in range(height_count)
                    for index in range(1, angular_size)
                }
                prime = 2
                denominator_exponent = 0
                remaining = cosine.denominator
                while remaining % 2 == 0:
                    denominator_exponent += 1
                    remaining //= 2
                if denominator_exponent >= 2:
                    growth = denominator_exponent - 1
                    shift = 1
                else:
                    prime = next(
                        candidate
                        for candidate in (3, 5, 7)
                        if cosine.denominator % candidate == 0
                    )
                    growth = 0
                    remaining = cosine.denominator
                    while remaining % prime == 0:
                        growth += 1
                        remaining //= prime
                    shift = 0
                height_valuation = 0
                remaining_height = height_count
                while remaining_height % prime == 0:
                    height_valuation += 1
                    remaining_height //= prime
                # The reduced denominator exponent of
                # 2*m^2*(1-T_k) is growth*k+shift-v_p(2*m^2).
                multiplier_valuation = 2 * height_valuation
                if prime == 2:
                    multiplier_valuation += 1
                discarded = max(
                    0,
                    (
                        multiplier_valuation - shift
                    )
                    // growth,
                )
                usable = max(0, angular_size - 1 - discarded)
                assert len(distances) >= height_count * usable
