"""Regression tests for the zero-star defect-mass ledger."""

import unittest

from verify_erdos809_zero_star_defect_mass import (
    exhaustive_certificate,
    ledger,
)


class ZeroStarDefectMassTests(unittest.TestCase):
    def test_overlapping_colour_supports(self) -> None:
        result = ledger(
            leaf_count=4,
            supports=(0b1111, 0b0111, 0b0101),
            extra_outer=(0, 0, 0),
        )
        self.assertEqual(result["star_mass"], result["defect"])
        self.assertTrue(result["pass"])

    def test_extra_outer_endpoints_only_add_defect(self) -> None:
        bare = ledger(3, (0b111, 0b001), (0, 0))
        enlarged = ledger(3, (0b111, 0b001), (2, 1))
        self.assertEqual(bare["star_mass"], enlarged["star_mass"])
        self.assertGreater(enlarged["defect"], bare["defect"])
        self.assertEqual(enlarged["slack"], enlarged["predicted_slack"])
        self.assertTrue(enlarged["pass"])

    def test_colours_disjoint_from_the_star(self) -> None:
        result = ledger(2, (0b11, 0, 0b01), (0, 2, 1))
        self.assertTrue(result["pass"])

    def test_exhaustive_support_systems(self) -> None:
        result = exhaustive_certificate(max_leaves=4, max_colours=3)
        self.assertGreater(result["equality_systems"], 0)
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
