#!/usr/bin/env python3
"""Regression tests for linear zero-matching synchronization."""

from fractions import Fraction
import unittest

import verify_linear_matching_synchronization as verifier


class LinearMatchingSynchronizationTests(unittest.TestCase):
    def test_exhaustive_cross_bound(self) -> None:
        self.assertEqual(verifier.exhaustive_cross_bound(), 3969)

    def test_deterministic_anchor(self) -> None:
        report = verifier.deterministic_audit()
        self.assertEqual(report["matching_size"], 5)
        self.assertGreaterEqual(report["anchor_multiplicity"], 5)
        self.assertEqual(report["valid_indices"], 5)
        self.assertEqual(report["forced_rectangle"], 25)

    def test_common_host(self) -> None:
        report = verifier.common_host_guard()
        self.assertEqual(report["delta"], 9)
        self.assertEqual(report["kappa"], 2)
        self.assertEqual(report["host_x_size"], 11)
        self.assertGreater(verifier.exhaustive_host_cut_guard(limit=8), 0)

    def test_random_systems(self) -> None:
        self.assertEqual(verifier.random_audits(trials=300), 300)

    def test_greedy_capacity(self) -> None:
        report = verifier.greedy_capacity_audit(1000, Fraction(1, 3))
        self.assertGreater(report["rounds"], 1)
        self.assertGreaterEqual(
            report["rectangle_sum"], report["proved_lower_bound"]
        )
        self.assertEqual(verifier.random_greedy_audits(trials=500), 500)

    def test_closed_forms(self) -> None:
        self.assertEqual(verifier.random_closed_form_audits(trials=500), 500)


if __name__ == "__main__":
    unittest.main()
