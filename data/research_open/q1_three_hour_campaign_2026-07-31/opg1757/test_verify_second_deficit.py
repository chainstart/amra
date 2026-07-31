#!/usr/bin/env python3
"""Tests for the complete B_(2s-7) layer."""

from __future__ import annotations

import unittest

import sympy as sp

import verify_second_deficit as verifier


class SecondDeficitTest(unittest.TestCase):
    def test_component_endpoint_polynomials(self) -> None:
        rows = verifier.audit_component_polynomial_table()
        self.assertEqual(len(rows), 30)
        self.assertEqual(sum(row[5] for row in rows), 180)
        self.assertEqual(max(7 + row[5] - 1 for row in rows), 16)

    def test_independent_denominator_aware_certificate(self) -> None:
        self.assertEqual(
            verifier.audit_independent_rational_certificate(),
            180,
        )

    def test_fixed_deficit_finite_reduction_counts(self) -> None:
        self.assertEqual(
            len(verifier.fixed_deficit_endpoint_entries(0)),
            6,
        )
        self.assertEqual(
            verifier.fixed_deficit_endpoint_certificate_points(0),
            12,
        )
        self.assertEqual(
            len(verifier.fixed_deficit_endpoint_entries(2)),
            30,
        )
        self.assertEqual(
            verifier.fixed_deficit_endpoint_certificate_points(2),
            180,
        )
        self.assertEqual(
            [
                verifier.fixed_deficit_coefficient_degree_bound(2, offset)
                for offset in range(5)
            ],
            [6, 7, 8, 9, 10],
        )
        self.assertEqual(
            [
                verifier.fixed_deficit_coefficient_certificate_points(
                    2, offset
                )
                for offset in range(5)
            ],
            [7, 8, 9, 10, 11],
        )
        self.assertEqual(
            verifier.fixed_deficit_boundary_roots(0),
            (),
        )
        self.assertEqual(
            verifier.fixed_deficit_boundary_roots(3),
            (4,),
        )
        self.assertEqual(
            verifier.fixed_deficit_boundary_roots(5),
            (4, 5),
        )
        self.assertEqual(
            [
                verifier
                .fixed_deficit_reduced_coefficient_certificate_points(
                    5, offset
                )
                for offset in range(11)
            ],
            list(range(11, 22)),
        )

    def test_species_against_primitive_chains(self) -> None:
        self.assertGreater(verifier.audit_chain_species(5, 9), 100)

    def test_symbolic_master_formula(self) -> None:
        rows = verifier.audit_symbolic_layer_formulas()
        self.assertEqual(len(rows), 5)
        for offset in range(4):
            self.assertEqual(
                sp.cancel(
                    verifier.normalized_layer_polynomial(offset)
                    - verifier.EXPECTED_NORMALIZED_LAYERS[offset]
                ),
                0,
            )

    def test_previous_attack_algebra_gap_is_filled(self) -> None:
        certificate = verifier.previous_attack_algebra_certificate()
        self.assertEqual(
            certificate["normalized_C"],
            "4*(s**2 + 4*s - 24)",
        )
        self.assertEqual(
            certificate["normalized_Q"],
            "-8*(5*s - 16)",
        )
        self.assertEqual(
            certificate["middle_sum"],
            "8*(s**2 - s - 8)",
        )

    def test_complete_layer_against_primitive_transfer(self) -> None:
        rows = verifier.audit_primitive_second_deficit(4, 16)
        self.assertEqual(len(rows), 12 * 5)
        self.assertTrue(all(row[3] > 0 for row in rows))

    def test_certificate(self) -> None:
        certificate = verifier.build_certificate(4, 12)
        self.assertEqual(certificate["status"], "PASS")
        self.assertEqual(
            certificate["schema"],
            "amra.opg1757.second_depth_deficit.v2",
        )
        self.assertEqual(certificate["theorem_status"], "PROVED")
        self.assertEqual(
            certificate["denominator_aware_component_points"],
            180,
        )
        self.assertEqual(
            certificate[
                "independent_denominator_aware_component_points"
            ],
            180,
        )
        self.assertEqual(len(certificate["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
