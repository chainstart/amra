#!/usr/bin/env python3
"""Independent tests for the ruled Cartesian escape audit."""

from __future__ import annotations

import random
import unittest
from fractions import Fraction

from verify_ruled_cartesian_escape_independent import (
    anchored_label_counts,
    anchored_sets,
    finite_audit,
    full_squared_distances,
    rational_scaling_bug,
    tau,
    theorem_lower_bound,
)


class RuledCartesianIndependentAuditTests(unittest.TestCase):
    def test_product_fibres_and_no_zero(self) -> None:
        generator = random.Random(1083)
        for T in range(2, 10):
            universe_slopes = list(range(-T, T + 1))
            universe_radial = list(range(1, T + 1))
            universe_heights = list(range(-T, T + 1))
            for _ in range(20):
                slopes = tuple(
                    sorted(generator.sample(universe_slopes, generator.randint(2, 5)))
                )
                radial = tuple(
                    sorted(
                        generator.sample(
                            universe_radial,
                            generator.randint(1, min(5, T)),
                        )
                    )
                )
                heights = tuple(
                    sorted(
                        generator.sample(
                            universe_heights,
                            generator.randint(1, 5),
                        )
                    )
                )
                x_values, _, products = anchored_sets(slopes, radial, heights)
                self.assertGreater(min(x_values), 0)
                for value, multiplicity in products.items():
                    self.assertLessEqual(multiplicity, tau(value))

    def test_sum_of_squares_fibres_and_range(self) -> None:
        generator = random.Random(630)
        for T in range(2, 9):
            for _ in range(20):
                slopes = tuple(
                    sorted(
                        generator.sample(
                            list(range(-T, T + 1)), generator.randint(2, 5)
                        )
                    )
                )
                radial = tuple(
                    sorted(
                        generator.sample(
                            list(range(1, T + 1)),
                            generator.randint(1, min(5, T)),
                        )
                    )
                )
                heights = tuple(
                    sorted(
                        generator.sample(
                            list(range(-T, T + 1)), generator.randint(1, 5)
                        )
                    )
                )
                labels, _ = anchored_label_counts(slopes, radial, heights)
                self.assertGreater(min(labels), 0)
                self.assertLessEqual(max(labels), 8 * T**4)
                for value, multiplicity in labels.items():
                    self.assertLessEqual(multiplicity, 4 * tau(value))
                    self.assertLessEqual(multiplicity, 2 * tau(value))

    def test_anchored_labels_are_actual_distances(self) -> None:
        for T in range(2, 8):
            slopes = (-T, -1, T)
            radial = tuple(range(1, T + 1))
            heights = (-T, 0, T)
            labels, _ = anchored_label_counts(slopes, radial, heights)
            full = full_squared_distances(slopes, radial, heights)
            self.assertTrue(set(labels).issubset(full))

    def test_theorem_bound_with_constants_four_and_two(self) -> None:
        for T in range(2, 7):
            slopes = (-T, 0, T)
            radial = tuple(range(1, T + 1))
            heights = (-T, 0, T)
            actual = len(full_squared_distances(slopes, radial, heights))
            stated = theorem_lower_bound(T, slopes, radial, heights)
            improved = theorem_lower_bound(
                T, slopes, radial, heights, improved_constant=True
            )
            self.assertGreaterEqual(Fraction(actual), stated)
            self.assertGreaterEqual(Fraction(actual), improved)
            self.assertEqual(improved, 2 * stated)

    def test_boundary_range_and_finite_report(self) -> None:
        for T in range(2, 9):
            report = finite_audit(T)
            self.assertTrue(report["anchored_subset_of_full"])
            self.assertGreater(report["minimum_anchored_label"], 0)
            self.assertLessEqual(
                report["maximum_anchored_label"], report["range_bound_8T4"]
            )
            self.assertLessEqual(
                report["maximum_product_fibre_minus_tau"], 0
            )
            self.assertLessEqual(
                report["maximum_square_fibre_minus_4tau"], 0
            )
            self.assertLessEqual(
                report["maximum_square_fibre_minus_2tau"], 0
            )

    def test_rational_scaling_claim_fails_and_square_repairs(self) -> None:
        report = rational_scaling_bug()
        self.assertFalse(report["scaled_once_integral"])
        self.assertTrue(report["scaled_twice_integral"])
        self.assertEqual(report["scaled_once"], ["1", "1/2", "1"])
        self.assertEqual(report["scaled_twice"], ["2", "1", "2"])

    def test_revised_common_denominator_scaling_identity(self) -> None:
        generator = random.Random(729)
        for _ in range(200):
            denominator = generator.randint(2, 20)
            radial_numerator = generator.randint(1, 40)
            slope_left_numerator = generator.randint(-40, 40)
            slope_right_numerator = generator.randint(-40, 40)
            height_left_numerator = generator.randint(-40, 40)
            height_right_numerator = generator.randint(-40, 40)
            radial = Fraction(radial_numerator, denominator)
            slope_left = Fraction(slope_left_numerator, denominator)
            slope_right = Fraction(slope_right_numerator, denominator)
            height_left = Fraction(height_left_numerator, denominator)
            height_right = Fraction(height_right_numerator, denominator)
            original_squared = (
                radial * (slope_left - slope_right)
            ) ** 2 + (height_left - height_right) ** 2
            scaled_horizontal = radial_numerator * (
                slope_left_numerator - slope_right_numerator
            )
            scaled_vertical = denominator * (
                height_left_numerator - height_right_numerator
            )
            scaled_squared = scaled_horizontal**2 + scaled_vertical**2
            self.assertEqual(
                Fraction(scaled_squared),
                denominator**4 * original_squared,
            )

    def test_critical_exponent(self) -> None:
        self.assertEqual(Fraction(1, 5) + Fraction(3, 5), Fraction(4, 5))


if __name__ == "__main__":
    unittest.main()
