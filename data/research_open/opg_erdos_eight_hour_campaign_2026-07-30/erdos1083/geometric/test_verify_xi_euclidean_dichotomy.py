#!/usr/bin/env python3
"""Tests for the Xi/parameter-energy certificate."""

from __future__ import annotations

import unittest
from fractions import Fraction

from verify_xi_euclidean_dichotomy import (
    critical_metrics,
    critical_parameter_formula,
    energy_threshold_exponent,
    exponent_ledger,
    interval_square_union_count,
    parameter_exponents,
    parameter_multiplicities,
    square_offset_overlap,
    xi_exponent,
    xi_inverse_lower,
    xi_lower,
)


class XiEuclideanDichotomyTests(unittest.TestCase):
    def test_parameter_closed_forms_match_enumeration(self) -> None:
        for t in range(2, 5):
            multiplicities = parameter_multiplicities(t)
            formula = critical_parameter_formula(t)
            self.assertEqual(len(multiplicities), formula["parameter_lines"])
            self.assertEqual(sum(multiplicities.values()), formula["raw_pairs"])
            self.assertEqual(
                sum(value * value for value in multiplicities.values()),
                formula["parameter_energy"],
            )

    def test_exact_exponent_ledger(self) -> None:
        ledger = exponent_ledger()
        self.assertEqual(ledger["parameter_line_m"], "4/5")
        self.assertEqual(ledger["sparse_Xi"], "3/5")
        self.assertEqual(ledger["sparse_parameter_distance"], "1/2")
        self.assertEqual(ledger["sparse_combined"], "3/5")
        self.assertEqual(ledger["full_Xi"], "4/5")
        self.assertEqual(ledger["full_parameter_distance"], "3/5")
        self.assertEqual(ledger["full_combined"], "4/5")
        self.assertEqual(
            ledger["sparse_energy_threshold_at_epsilon_zero"], "7/5"
        )
        self.assertEqual(
            ledger["full_energy_threshold_at_epsilon_zero"], "8/5"
        )

    def test_symbolic_exponent_functions(self) -> None:
        self.assertEqual(
            xi_exponent(Fraction(3, 5), Fraction(1, 5), Fraction(0)),
            Fraction(3, 5),
        )
        self.assertEqual(
            xi_exponent(Fraction(4, 5), Fraction(2, 5), Fraction(0)),
            Fraction(4, 5),
        )
        self.assertEqual(
            parameter_exponents(
                Fraction(6, 5), Fraction(8, 5), Fraction(1, 5)
            ),
            (Fraction(4, 5), Fraction(1, 2)),
        )
        epsilon = Fraction(1, 100)
        self.assertEqual(
            energy_threshold_exponent(
                Fraction(6, 5),
                Fraction(1, 5),
                Fraction(3, 5) + epsilon,
            ),
            Fraction(7, 5) - 2 * epsilon,
        )

    def test_xi_inverse_implication(self) -> None:
        for incidences in range(4, 30):
            for columns in range(1, 7):
                for overlap in range(0, 9):
                    value = xi_lower(incidences, columns, overlap)
                    target = value + Fraction(1, 17)
                    self.assertLess(value, target)
                    self.assertGreater(
                        Fraction(overlap),
                        xi_inverse_lower(incidences, columns, target),
                    )

    def test_square_interval_union_has_column_starvation_scale(self) -> None:
        for height_count in range(3, 30):
            for columns in range(1, height_count + 1):
                count = interval_square_union_count(height_count, columns)
                first_disjoint = (columns + 2) // 2
                disjoint_count = max(0, height_count - first_disjoint)
                self.assertGreaterEqual(count, disjoint_count * columns)
                self.assertLessEqual(count, height_count * columns)

    def test_finite_critical_metrics(self) -> None:
        for t in range(2, 9):
            metrics = critical_metrics(t)
            self.assertEqual(metrics["N"], t**5)
            self.assertEqual(metrics["F"], t**3)
            self.assertEqual(metrics["sparse_incidences_I"], t**3)
            self.assertGreaterEqual(
                metrics["sparse_actual_interval_union"], t**3 // 3
            )
            self.assertLessEqual(
                metrics["sparse_actual_interval_union"], t**3
            )
            self.assertGreaterEqual(
                metrics["full_actual_interval_union"], t**4 // 3
            )
            self.assertLessEqual(
                square_offset_overlap(t * t), t * t
            )


if __name__ == "__main__":
    unittest.main()
