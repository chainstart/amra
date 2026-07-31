#!/usr/bin/env python3
"""Tests for the complete OPG-1757 B_(2*s-10) layer."""

from __future__ import annotations

import unittest

import sympy as sp

import verify_sixth_q5 as verifier


class SixthAttackQ5Test(unittest.TestCase):
    def test_count_firewall(self) -> None:
        entries = verifier.q5_endpoint_entries()
        self.assertEqual(len(entries), 84)
        self.assertEqual(
            sum(
                verifier.rational_certificate_point_count(excess, components)
                for _, excess, components in entries
            ),
            924,
        )
        top_face_removed = [
            entry for entry in entries if entry[1:] != (6, 1)
        ]
        self.assertEqual(len(top_face_removed), 81)
        self.assertEqual(
            sum(
                verifier.rational_certificate_point_count(excess, components)
                for _, excess, components in top_face_removed
            ),
            867,
        )

    def test_complete_endpoint_certificate(self) -> None:
        rows = verifier.audit_q5_endpoint_table()
        self.assertEqual(len(rows), 84)
        self.assertEqual(sum(row[4] for row in rows), 924)
        self.assertEqual(
            max(
                verifier.Q5_ENDPOINT_SAMPLE_START + row[4] - 1
                for row in rows
            ),
            28,
        )

    def test_all_eleven_symbolic_offsets(self) -> None:
        rows = verifier.audit_symbolic_q5_layers()
        self.assertEqual(len(rows), 11)
        for offset, expected in enumerate(
            verifier.EXPECTED_Q5_NORMALIZED_LAYERS
        ):
            self.assertEqual(
                sp.cancel(
                    verifier.normalized_q5_layer(offset) - expected
                ),
                0,
            )

    def test_exact_boundary_and_strict_range(self) -> None:
        self.assertEqual(verifier.q5_coefficients(5), {})
        for s in range(6, 13):
            coefficients = verifier.q5_coefficients(s)
            self.assertEqual(len(coefficients), 11)
            self.assertTrue(all(value > 0 for value in coefficients.values()))

    def test_independent_rational_certificate(self) -> None:
        self.assertEqual(verifier.audit_independent_q5_coefficients(), 176)

    def test_certificate(self) -> None:
        certificate = verifier.build_certificate()
        self.assertEqual(certificate["status"], "PASS")
        self.assertEqual(certificate["theorem_status"], "PROVED")
        self.assertEqual(
            certificate["schema"],
            "amra.opg1757.sixth_attack_q5.v1",
        )
        self.assertEqual(certificate["endpoint_count"], 84)
        self.assertEqual(
            certificate["denominator_aware_endpoint_values"], 924
        )
        self.assertEqual(certificate["offset_count"], 11)
        self.assertEqual(
            certificate["independent_coefficient_values"], 176
        )
        self.assertEqual(len(certificate["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
