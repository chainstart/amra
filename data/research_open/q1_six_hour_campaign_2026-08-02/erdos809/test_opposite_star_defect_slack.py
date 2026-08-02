"""Regression tests for the opposite-star defect-slack energy."""

import unittest

from verify_opposite_star_defect_slack import exhaustive_certificate, profile


class OppositeStarDefectSlackTests(unittest.TestCase):
    def test_scalar_min_identity(self) -> None:
        result = profile(3, (2, 4, 9), 6, 12, 1, 11)
        self.assertTrue(result["exact_identity"])

    def test_large_residual_surcharge_is_live(self) -> None:
        result = profile(2, (3, 8), 4, 10, 2, 9)
        self.assertGreater(result["surcharge"], 0)
        self.assertTrue(result["pass"])

    def test_exact_boundary(self) -> None:
        result = profile(1, (4,), 2, 4, 1, 3)
        self.assertTrue(result["antecedent"])
        self.assertTrue(result["conclusion"])

    def test_simultaneous_tight_endpoint_is_infeasible(self) -> None:
        result = profile(1, (2,), 2, 2, 0, 1)
        self.assertFalse(result["antecedent"])
        self.assertTrue(result["tight_endpoint_excluded"])

    def test_exhaustive_profiles(self) -> None:
        result = exhaustive_certificate()
        self.assertGreater(result["antecedents"], 0)
        self.assertGreater(result["strict_improvements"], 0)
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
