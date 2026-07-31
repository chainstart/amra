#!/usr/bin/env python3
"""Tests for the OPG-1757 pooled top-face verifier."""

from __future__ import annotations

import math
import unittest

import verify_pooled_top_face as verifier


class PooledTopFaceTest(unittest.TestCase):
    def test_stirling_difference_and_newton_inversion_agree(self) -> None:
        for s in range(4, 13):
            for depth in range(0, 2 * s):
                self.assertEqual(
                    verifier.top_face_coefficient(s, depth),
                    verifier.finite_difference_top(s, depth),
                )

    def test_top_face_has_exact_positive_depth_range(self) -> None:
        for s in range(4, 20):
            coefficients = [
                verifier.top_face_coefficient(s, depth)
                for depth in range(0, 2 * s + 2)
            ]
            self.assertEqual(coefficients[0], 0)
            self.assertEqual(coefficients[1], 0)
            self.assertTrue(all(value > 0 for value in coefficients[2 : 2 * s - 4]))
            self.assertTrue(all(value == 0 for value in coefficients[2 * s - 4 :]))
            self.assertEqual(
                coefficients[2 * s - 5],
                4 * s ** (2 * s - 8) * math.factorial(2 * s - 5),
            )

    def test_component_endpoint_outside_old_stable_range(self) -> None:
        # Includes many pages > s-3, where the old stable-range K_k
        # endpoint argument could not be used directly.
        for s in range(4, 8):
            for pages in range(2, 10):
                self.assertEqual(
                    verifier.direct_determinant_top(s, pages),
                    verifier.predicted_determinant_top(s, pages),
                )

    def test_second_deepest_binary_and_ternary_endpoints(self) -> None:
        for s in range(4, 13):
            self.assertEqual(
                verifier.second_deepest_endpoint_data(s),
                verifier.predicted_second_deepest_endpoint_data(s),
            )

    def test_second_deepest_layer_against_primitive_engine(self) -> None:
        for s in range(4, 13):
            depth = 2 * s - 6
            primitive = {
                degree: coefficient
                for (row_depth, degree), coefficient in (
                    verifier.primitive_pooled_rows(s)
                ).items()
                if row_depth == depth
            }
            self.assertEqual(
                primitive,
                verifier.second_deepest_coefficients(s),
            )
            self.assertTrue(all(value > 0 for value in primitive.values()))

    def test_primitive_pooled_engine(self) -> None:
        theorem_rows, finite_rows = verifier.audit_pooled_top_face(4, 9)
        self.assertEqual(len(theorem_rows), sum(2 * s - 2 for s in range(4, 10)))
        self.assertGreater(len(finite_rows), 0)

    def test_certificate(self) -> None:
        certificate = verifier.build_certificate(4, 8, 8)
        self.assertEqual(certificate["status"], "PASS")
        self.assertEqual(
            certificate["schema"],
            "amra.opg1757.pooled_all_depth_top_face.v1",
        )
        self.assertEqual(len(certificate["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
