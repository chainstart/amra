#!/usr/bin/env python3
"""Tests for the complete OPG-1757 B_(2*s-9) layer."""

from __future__ import annotations

import unittest

import sympy as sp

import verify_fifth_q4 as verifier


class FifthAttackQ4Test(unittest.TestCase):
    def test_complete_endpoint_certificate(self) -> None:
        rows = verifier.audit_q4_endpoint_table()
        self.assertEqual(len(rows), 63)
        self.assertEqual(sum(row[4] for row in rows), 588)
        self.assertEqual(
            max(
                verifier.Q4_ENDPOINT_SAMPLE_START + row[4] - 1
                for row in rows
            ),
            24,
        )

    def test_all_nine_symbolic_offsets(self) -> None:
        rows = verifier.audit_symbolic_q4_layers()
        self.assertEqual(len(rows), 9)
        for offset, expected in enumerate(
            verifier.EXPECTED_Q4_NORMALIZED_LAYERS
        ):
            self.assertEqual(
                sp.cancel(
                    verifier.normalized_q4_layer(offset) - expected
                ),
                0,
            )

    def test_exact_boundary_and_strict_range(self) -> None:
        self.assertEqual(verifier.q4_coefficients(5), {})
        for s in range(6, 14):
            coefficients = verifier.q4_coefficients(s)
            self.assertEqual(len(coefficients), 9)
            self.assertTrue(all(value > 0 for value in coefficients.values()))

    def test_independent_rational_certificate(self) -> None:
        self.assertEqual(verifier.audit_independent_q4_coefficients(), 135)

    def test_certificate(self) -> None:
        certificate = verifier.build_certificate()
        self.assertEqual(certificate["status"], "PASS")
        self.assertEqual(certificate["theorem_status"], "PROVED")
        self.assertEqual(
            certificate["schema"],
            "amra.opg1757.fifth_attack_q4.v1",
        )
        self.assertEqual(certificate["endpoint_count"], 63)
        self.assertEqual(
            certificate["denominator_aware_endpoint_values"], 588
        )
        self.assertEqual(certificate["offset_count"], 9)
        self.assertEqual(
            certificate["independent_coefficient_values"], 135
        )
        self.assertEqual(len(certificate["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
