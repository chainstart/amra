#!/usr/bin/env python3
"""Tests for the cross-plane-to-radius transfer verifier."""

from __future__ import annotations

import math
import random
import unittest

from verify_cross_plane_to_radius_transfer import (
    asymptotic_ledger,
    binary_form,
    binary_form_determinant,
    distinct_kernel_slopes,
    enumerated_metrics,
    family_points,
    four_plane_identity,
    radius_angle_energy,
    ruled_distance_subset,
    squarefree_kernel,
    squared_distance,
)


class CrossPlaneTransferTests(unittest.TestCase):
    def test_squarefree_kernel(self) -> None:
        for value in range(1, 500):
            kernel = squarefree_kernel(value)
            quotient = value // kernel
            self.assertEqual(math.isqrt(quotient) ** 2, quotient)
            for prime in range(2, math.isqrt(kernel) + 1):
                self.assertNotEqual(kernel % (prime * prime), 0)

    def test_selected_slopes_have_unique_kernels_and_radii(self) -> None:
        for limit in range(2, 80):
            slopes = distinct_kernel_slopes(limit)
            kernels = [squarefree_kernel(1 + slope * slope) for slope in slopes]
            self.assertEqual(len(kernels), len(set(kernels)))
            radii = {
                radial_parameter**2 * (1 + slope * slope)
                for slope in slopes
                for radial_parameter in range(1, limit + 1)
            }
            self.assertEqual(len(radii), len(slopes) * limit)

    def test_binary_form_determinant(self) -> None:
        for slope in range(1, 20):
            for other_slope in range(1, 20):
                determinant = (
                    (1 + slope * slope) * (1 + other_slope * other_slope)
                    - (1 + slope * other_slope) ** 2
                )
                self.assertEqual(
                    determinant,
                    binary_form_determinant(slope, other_slope),
                )

    def test_cylindrical_identity_matches_cartesian_distance(self) -> None:
        generator = random.Random(1083)
        for _ in range(500):
            x = generator.uniform(-5, 5)
            y = generator.uniform(-5, 5)
            z = generator.uniform(-5, 5)
            w = generator.uniform(-5, 5)
            alpha = generator.uniform(-math.pi, math.pi)
            beta = generator.uniform(-math.pi, math.pi)
            left = (x * math.cos(alpha), x * math.sin(alpha), z)
            right = (y * math.cos(beta), y * math.sin(beta), w)
            cartesian = sum(
                (left[index] - right[index]) ** 2 for index in range(3)
            )
            self.assertAlmostEqual(
                cartesian,
                four_plane_identity(x, alpha, z, y, beta, w),
                places=10,
            )

    def test_encoded_squared_distance(self) -> None:
        for slope in range(1, 8):
            for other_slope in range(1, 8):
                for a in range(1, 6):
                    for b in range(1, 6):
                        left = (slope, a, 3)
                        right = (other_slope, b, 11)
                        expected = (
                            (a - b) ** 2
                            + (slope * a - other_slope * b) ** 2
                            + 64
                        )
                        self.assertEqual(squared_distance(left, right), expected)
                        self.assertEqual(
                            binary_form(slope, other_slope, a, b),
                            expected - 64,
                        )

    def test_enumerated_energy_decomposition(self) -> None:
        for t in range(2, 6):
            metrics = enumerated_metrics(t)
            self.assertEqual(metrics["active_planes"], t)
            self.assertEqual(metrics["points_per_plane"], t**3)
            self.assertEqual(metrics["source_mass"], t**4)
            self.assertEqual(
                metrics["cross_plane_codegree"],
                metrics["total_distance_energy"]
                - metrics["plane_pair_diagonal_energy"],
            )
            self.assertLessEqual(metrics["distance_labels"], 3 * t**4 + 1)
            self.assertLessEqual(
                metrics["maximum_squared_distance"], 3 * t**4
            )
            self.assertGreater(metrics["cross_plane_codegree"], 0)

    def test_asymptotic_ledger_records_no_saving(self) -> None:
        ledger = asymptotic_ledger()
        self.assertEqual(
            ledger["unsaved_transfer_scale"],
            "S^(3/2)*E=t^(12-o(1))",
        )
        self.assertEqual(ledger["missing_factor"], "t=N^(1/5)")
        self.assertEqual(
            ledger["ruled_distance_lower"],
            "t^(4-o(1))=N^(4/5-o(1))",
        )

    def test_ruled_distance_subset_is_genuine(self) -> None:
        for t in range(3, 13):
            subset = ruled_distance_subset(t)
            self.assertGreater(subset["slope_differences"], 0)
            self.assertGreater(subset["distinct_products"], 0)
            self.assertGreater(subset["distinct_distance_labels"], 0)
            slopes = distinct_kernel_slopes(t)
            base = min(slopes)
            products = {
                a * (slope - base)
                for slope in slopes
                if slope > base
                for a in range(1, t + 1)
            }
            labels = {
                product**2 + difference**2
                for product in products
                for difference in range(t * t)
            }
            realized = {
                squared_distance(
                    (slope, a, difference),
                    (base, a, 0),
                )
                for slope in slopes
                if slope > base
                for a in range(1, t + 1)
                for difference in range(t * t)
            }
            self.assertEqual(labels, realized)


if __name__ == "__main__":
    unittest.main()
