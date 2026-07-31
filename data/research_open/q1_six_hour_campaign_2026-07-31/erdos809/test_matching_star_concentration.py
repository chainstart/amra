#!/usr/bin/env python3
"""Regression test for matching--star concentration."""

import unittest

import verify_matching_star_concentration as verifier


class MatchingStarConcentrationTests(unittest.TestCase):
    def test_random_weighted_graphs(self) -> None:
        self.assertEqual(verifier.random_audits(trials=1000), 1000)


if __name__ == "__main__":
    unittest.main()
