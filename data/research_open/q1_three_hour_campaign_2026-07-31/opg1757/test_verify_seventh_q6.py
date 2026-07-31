#!/usr/bin/env python3
"""Tests for the complete OPG-1757 B_(2*s-11) layer."""

from __future__ import annotations

import unittest

import sympy as sp

import verify_seventh_q6 as verifier


class SeventhAttackQ6Test(unittest.TestCase):
    def test_count_firewall(self) -> None:
        entries = verifier.q6_endpoint_entries()
        self.assertEqual(len(entries), 108)
        self.assertEqual(
            sum(
                verifier.rational_certificate_point_count(
                    excess, components
                )
                for _, excess, components in entries
            ),
            1368,
        )
        inherited = [entry for entry in entries if entry[2] < 8 - entry[1]]
        boundary = [entry for entry in entries if entry[2] == 8 - entry[1]]
        self.assertEqual(len(inherited), 84)
        self.assertEqual(len(boundary), 24)

    def test_fast_forest_recurrence(self) -> None:
        self.assertEqual(verifier.audit_fast_forest_recurrence(), 24)

    def test_complete_endpoint_certificate(self) -> None:
        rows = verifier.audit_q6_endpoint_table()
        self.assertEqual(len(rows), 108)
        self.assertEqual(sum(row[4] for row in rows), 1368)
        self.assertEqual(
            max(
                verifier.Q6_ENDPOINT_SAMPLE_START + row[4] - 1
                for row in rows
            ),
            32,
        )

    def test_all_thirteen_symbolic_offsets(self) -> None:
        rows = verifier.audit_symbolic_q6_layers()
        self.assertEqual(len(rows), 13)
        for offset, expected in enumerate(
            verifier.EXPECTED_Q6_NORMALIZED_LAYERS
        ):
            self.assertEqual(
                sp.cancel(verifier.normalized_q6_layer(offset) - expected),
                0,
            )

    def test_exact_boundary_and_strict_range(self) -> None:
        self.assertEqual(verifier.q6_coefficients(6), {})
        for s in range(7, 13):
            coefficients = verifier.q6_coefficients(s)
            self.assertEqual(len(coefficients), 13)
            self.assertTrue(all(value > 0 for value in coefficients.values()))

    def test_independent_rational_certificate(self) -> None:
        self.assertEqual(verifier.audit_independent_q6_coefficients(), 208)

    def test_certificate(self) -> None:
        certificate = verifier.build_certificate()
        self.assertEqual(certificate["status"], "PASS")
        self.assertEqual(certificate["theorem_status"], "PROVED")
        self.assertEqual(
            certificate["schema"],
            "amra.opg1757.seventh_attack_q6.v1",
        )
        self.assertEqual(certificate["endpoint_count"], 108)
        self.assertEqual(
            certificate["denominator_aware_endpoint_values"], 1368
        )
        self.assertEqual(certificate["offset_count"], 13)
        self.assertEqual(certificate["independent_coefficient_values"], 208)
        self.assertEqual(len(certificate["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
