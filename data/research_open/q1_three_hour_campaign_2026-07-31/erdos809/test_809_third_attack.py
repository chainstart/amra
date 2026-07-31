#!/usr/bin/env python3
"""Regression tests for the third 2026-07-31 Erdős #809 attack."""

from __future__ import annotations

import unittest

import verify_809_third_attack as verifier


class ThirdAttackGuards(unittest.TestCase):
    def test_complement_energy_identities(self) -> None:
        result = verifier.random_energy_guard()
        self.assertTrue(result["passed"])
        self.assertGreater(result["nontrivial_crossing_profiles"], 0)

    def test_excess_degree_cleaning(self) -> None:
        result = verifier.cleaning_guard()
        self.assertTrue(result["passed"])
        self.assertGreater(
            result["concentrated_profile"]["removed_vertices"], 0
        )
        self.assertEqual(
            result["dispersed_profile"]["removed_vertices"], 0
        )

    def test_rotated_maximum_witness(self) -> None:
        result = verifier.rotated_witness_guard()
        self.assertTrue(result["passed"])
        self.assertEqual(result["good_edge_defect"], 0)
        self.assertFalse(result["paired_edges_share_C7"])
        self.assertGreater(result["L4_endpoint_pairs"], 0)

    def test_rich_outer_compatibility(self) -> None:
        result = verifier.rich_outer_guard()
        self.assertTrue(result["passed"])
        self.assertGreater(result["rich_edges"], 0)
        self.assertTrue(result["local_centered_rectangle"])


if __name__ == "__main__":
    unittest.main()
