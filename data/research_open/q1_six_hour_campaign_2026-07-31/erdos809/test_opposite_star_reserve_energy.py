#!/usr/bin/env python3
"""Regression test for opposite-star reserve energy."""

import unittest

import verify_opposite_star_reserve_energy as verifier


class OppositeStarReserveEnergyTests(unittest.TestCase):
    def test_exhaustive_small_graphs(self) -> None:
        report = verifier.exhaustive_guard(limit=5)
        self.assertEqual(report["graphs"], 1098)
        self.assertGreater(report["active_leaf_subsets"], 0)


if __name__ == "__main__":
    unittest.main()
