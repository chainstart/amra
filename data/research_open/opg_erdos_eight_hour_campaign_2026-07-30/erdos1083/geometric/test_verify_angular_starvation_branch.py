#!/usr/bin/env python3
"""Tests for the angular-starvation branch certificate."""

from __future__ import annotations

import random
import unittest
from fractions import Fraction

from verify_angular_starvation_branch import (
    barrier_ledger,
    enumerate_square_difference_energy,
    exponent_ledger,
    normalized_rotation_codegree,
    rotation_cauchy_lower,
    square_difference_energy,
    transfer_exponents,
)


class AngularStarvationTests(unittest.TestCase):
    def test_square_difference_energy_formula(self) -> None:
        for size in range(1, 35):
            self.assertEqual(
                square_difference_energy(size),
                enumerate_square_difference_energy(size),
            )

    def test_rotation_second_moment_cauchy(self) -> None:
        generator = random.Random(1083)
        for _ in range(200):
            fibre_count = generator.randint(1, 12)
            angle_count = generator.randint(1, 8)
            masses = [generator.randint(1, 20) for _ in range(fibre_count)]
            weights = [
                [generator.randint(0, mass) for mass in masses]
                for _ in range(angle_count)
            ]
            self.assertGreaterEqual(
                normalized_rotation_codegree(masses, weights),
                rotation_cauchy_lower(masses, weights),
            )

    def test_barrier_exact_mass_and_marginals(self) -> None:
        for t in range(3, 10):
            ledger = barrier_ledger(t)
            self.assertEqual(ledger["N"], t**5)
            self.assertEqual(ledger["total_points"], t**5)
            self.assertEqual(ledger["M"], t)
            self.assertEqual(ledger["Q"], t**3)
            self.assertEqual(ledger["source_points"], t**4)
            self.assertEqual(ledger["reservoir_points"], t**5 - t**4)
            self.assertEqual(
                ledger["source_radius_angle_energy"], t**7
            )
            self.assertEqual(
                ledger["source_cross_angle_radius_codegree"], 0
            )
            self.assertEqual(
                ledger["critical_radius_xi_scale"], t**3
            )
            self.assertGreater(
                ledger["minimum_rotation_count"], t**5 // 10
            )

    def test_barrier_pair_energy_is_cauchy_sharp(self) -> None:
        for t in range(3, 10):
            ledger = barrier_ledger(t)
            q = t**3
            energy = ledger["one_plane_pair_energy"]
            self.assertGreaterEqual(energy, q**3)
            self.assertLessEqual(energy, 2 * q**3)
            self.assertEqual(ledger["one_plane_pair_distance_labels"], q)

    def test_exponent_ledger(self) -> None:
        ledger = exponent_ledger()
        self.assertEqual(ledger["forced_rotation_codegree"], "7/5")
        self.assertEqual(ledger["barrier_radius_angle_energy"], "7/5")
        self.assertEqual(ledger["forced_global_plane_energy"], "13/5")
        self.assertEqual(ledger["individual_pair_diagonal_upper"], "12/5")
        self.assertEqual(
            ledger["barrier_individual_pair_energy_sum"], "11/5"
        )
        self.assertEqual(ledger["transfer_capacity"], "6/5")

    def test_transfer_gives_same_xi_gain(self) -> None:
        for numerator in range(1, 10):
            eta = Fraction(numerator, 100)
            result = transfer_exponents(eta)
            self.assertEqual(
                result["radius_energy"], Fraction(7, 5) + eta
            )
            self.assertEqual(
                result["maximum_radius_mass"], Fraction(3, 5) + eta
            )
            self.assertEqual(result["Xi"], Fraction(3, 5) + eta)


if __name__ == "__main__":
    unittest.main()
