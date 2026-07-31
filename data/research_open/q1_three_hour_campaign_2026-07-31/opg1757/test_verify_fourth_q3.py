#!/usr/bin/env python3
"""Tests for the complete OPG-1757 B_(2*s-8) layer."""

from __future__ import annotations

import unittest

import sympy as sp

import verify_fourth_q3 as verifier


class FourthAttackQ3Test(unittest.TestCase):
    def test_complete_endpoint_certificate(self) -> None:
        rows = verifier.audit_q3_endpoint_table()
        self.assertEqual(len(rows), 45)
        self.assertEqual(sum(row[4] for row in rows), 345)
        self.assertEqual(
            max(
                verifier.Q3_ENDPOINT_SAMPLE_START + row[4] - 1
                for row in rows
            ),
            20,
        )

    def test_independent_endpoint_certificate(self) -> None:
        self.assertEqual(verifier.audit_independent_q3_endpoints(), 345)

    def test_all_seven_symbolic_offsets(self) -> None:
        rows = verifier.audit_symbolic_q3_layers()
        self.assertEqual(len(rows), 7)
        for offset, expected in enumerate(
            verifier.EXPECTED_Q3_NORMALIZED_LAYERS
        ):
            self.assertEqual(
                sp.cancel(
                    verifier.normalized_q3_layer(offset) - expected
                ),
                0,
            )

    def test_exact_boundary_and_strict_range(self) -> None:
        self.assertEqual(verifier.q3_coefficients(4), {})
        for s in range(5, 13):
            coefficients = verifier.q3_coefficients(s)
            self.assertEqual(len(coefficients), 7)
            self.assertTrue(all(value > 0 for value in coefficients.values()))

    def test_independent_primitive_pooling(self) -> None:
        rows = verifier.audit_primitive_q3_rows(4, 12)
        self.assertEqual(len(rows), 8 * 7)
        self.assertTrue(all(row[2] > 0 for row in rows))

    def test_certificate(self) -> None:
        certificate = verifier.build_certificate(4, 12)
        self.assertEqual(certificate["status"], "PASS")
        self.assertEqual(certificate["theorem_status"], "PROVED")
        self.assertEqual(
            certificate["schema"],
            "amra.opg1757.fourth_attack_q3.v1",
        )
        self.assertEqual(certificate["endpoint_count"], 45)
        self.assertEqual(
            certificate["denominator_aware_endpoint_values"], 345
        )
        self.assertEqual(certificate["independent_endpoint_values"], 345)
        self.assertEqual(len(certificate["normalized_layers"]), 7)
        self.assertEqual(len(certificate["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
