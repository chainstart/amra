#!/usr/bin/env python3
"""Regression tests for weighted synchronization transference."""

import unittest

import verify_weighted_synchronization_transference as verifier


class WeightedSynchronizationTransferenceTests(unittest.TestCase):
    def test_deterministic_system(self) -> None:
        report = verifier.deterministic_audit()
        self.assertEqual(report["matching_size"], 3)
        self.assertEqual(report["sum_h"], 14)
        self.assertGreaterEqual(report["best_weighted_support"], 12)

    def test_random_systems(self) -> None:
        self.assertEqual(verifier.random_audits(trials=1000), 1000)


if __name__ == "__main__":
    unittest.main()
