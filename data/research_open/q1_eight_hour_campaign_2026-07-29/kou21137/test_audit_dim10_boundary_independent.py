#!/usr/bin/env python3
"""Regression tests for the independent dimension-ten boundary ledger."""

import unittest

from audit_dim10_boundary_independent import audit


class IndependentDimensionTenBoundaryTest(unittest.TestCase):
    def test_exact_partition_and_no_survivor(self) -> None:
        result = audit()
        self.assertEqual(result["profile_count"], 92)
        self.assertEqual(
            result["count_by_length"], {6: 56, 7: 28, 8: 8}
        )
        self.assertEqual(result["survivors"], [])
        self.assertEqual(
            sum(result["first_exclusion_counts"].values()), 92
        )


if __name__ == "__main__":
    unittest.main()
