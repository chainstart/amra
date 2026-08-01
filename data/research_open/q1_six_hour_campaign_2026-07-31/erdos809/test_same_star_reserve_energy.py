#!/usr/bin/env python3
"""Regression tests for same-star reserve energy."""

import unittest

import verify_same_star_reserve_energy as verifier


class SameStarReserveEnergyTests(unittest.TestCase):
    def test_exhaustive_small_graphs(self) -> None:
        report = verifier.exhaustive_guard(limit=5)
        self.assertEqual(report["graphs"], 1098)
        self.assertGreater(report["leaf_subsets"], 0)

    def test_weighted_parameters(self) -> None:
        self.assertGreater(verifier.weighted_guard(limit=30), 0)
        self.assertGreater(verifier.closed_form_guard(limit=30), 0)


if __name__ == "__main__":
    unittest.main()
