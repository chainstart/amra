#!/usr/bin/env python3
"""Regression tests for the finite #809 guards."""

from __future__ import annotations

import unittest

import verify_809_near_dirac as verifier


class NearDiracGuards(unittest.TestCase):
    def test_four_path_obstruction_identities(self) -> None:
        result = verifier.exhaustive_four_path_guard(max_n=5)
        self.assertTrue(result["passed"])
        self.assertGreater(result["obstructed_pairs"], 0)
        self.assertGreater(result["property_pairs_checked"], 0)

    def test_distance_two_splice(self) -> None:
        result = verifier.distance_two_splice_guard(seeds=120)
        self.assertTrue(result["passed"])
        self.assertGreater(result["actual_three_path_splices_checked"], 0)

    def test_dense_clique_compatibility(self) -> None:
        self.assertTrue(verifier.dense_clique_guard()["passed"])

    def test_nonindependent_core_hub_union(self) -> None:
        result = verifier.core_hub_bruteforce_guard()
        self.assertTrue(result["passed"])
        self.assertEqual(result["covered_pairs"], result["family_pairs"])

    def test_rectangle_count(self) -> None:
        result = verifier.rectangle_optimization_guard(denominator=120)
        self.assertTrue(result["passed"])
        self.assertEqual(result["minimum"], "1/2")


if __name__ == "__main__":
    unittest.main()
