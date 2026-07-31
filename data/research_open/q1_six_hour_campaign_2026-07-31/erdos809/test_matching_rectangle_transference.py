#!/usr/bin/env python3
"""Regression tests for matching-rectangle transference."""

import unittest

import verify_matching_rectangle_transference as verifier


class MatchingRectangleTransferenceTests(unittest.TestCase):
    def test_deterministic_systems(self) -> None:
        reports = verifier.deterministic_audits()
        self.assertEqual(len(reports), 4)
        self.assertEqual(reports[1]["max_pair_overlap"], 3)
        self.assertGreaterEqual(reports[1]["Q"], 9)
        self.assertEqual(reports[3]["Q"], 6)

    def test_random_systems(self) -> None:
        self.assertEqual(verifier.random_audits(trials=300), 300)


if __name__ == "__main__":
    unittest.main()
