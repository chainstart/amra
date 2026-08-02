"""Regression tests for the mask-factor sunflower inverse theorem."""

import unittest

from verify_mask_factor_sunflower_inverse import (
    augmentation_certificate,
    cyclotomic_obstruction_certificate,
    endpoint_certificate,
    factor_sunflower_certificate,
)


class MaskFactorSunflowerInverseTests(unittest.TestCase):
    def test_endpoint(self) -> None:
        result = endpoint_certificate()
        self.assertEqual(result["common_tangent_leaf_exponent"], "5/9")
        self.assertEqual(result["fixed_difference_leaf_exponent"], "1/6")
        self.assertTrue(result["pass"])

    def test_factor_sunflower(self) -> None:
        result = factor_sunflower_certificate()
        self.assertTrue(result["pairwise_intersecting"])
        self.assertTrue(result["global_intersection_empty"])
        self.assertTrue(result["every_sunflower_bound_holds"])
        self.assertTrue(result["pass"])

    def test_augmentation_count(self) -> None:
        result = augmentation_certificate()
        self.assertEqual(result["source_size"], 6)
        self.assertTrue(result["large_factor_count_bound_holds"])
        self.assertTrue(result["pass"])

    def test_cyclotomic_factor_richness(self) -> None:
        result = cyclotomic_obstruction_certificate()
        self.assertEqual(result["mask_support_size"], 2)
        self.assertEqual(result["irreducible_factor_count"], 16)
        self.assertEqual(result["augmentation_unit_factor_count"], 15)
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
