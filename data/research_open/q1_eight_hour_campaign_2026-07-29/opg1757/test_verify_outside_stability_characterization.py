#!/usr/bin/env python3
"""Regression for the universal outside-stability characterization."""

import unittest

from verify_outside_stability_characterization import audit_boundary


class OutsideStabilityCharacterizationTest(unittest.TestCase):
    def test_all_local_forests_through_four_boundary_vertices(self) -> None:
        expected = {
            1: (1, 1),
            2: (2, 3),
            3: (7, 28),
            4: (38, 717),
        }
        for boundary_size, (forest_count, stable_count) in expected.items():
            with self.subTest(boundary_size=boundary_size):
                result = audit_boundary(boundary_size)
                self.assertEqual(result["local_forests"], forest_count)
                self.assertEqual(result["stable_pairs"], stable_count)


if __name__ == "__main__":
    unittest.main()
