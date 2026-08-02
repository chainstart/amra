"""Regression tests for the augmentation-unit subset-sum height atlas."""

import unittest

from verify_unit_switch_width_atlas import (
    cyclotomic_scalar_switch_certificate,
    divisor_class_certificate,
    signed_width_additivity_certificate,
    width_and_distance_certificate,
)


class UnitSwitchWidthAtlasTests(unittest.TestCase):
    def test_divisor_classes(self) -> None:
        result = divisor_class_certificate()
        self.assertLessEqual(
            result["divisor_associate_classes"], result["binary_upper_bound"]
        )
        self.assertTrue(result["pass"])

    def test_width_and_distance(self) -> None:
        result = width_and_distance_certificate()
        self.assertEqual(
            result["fixed_base_distances"],
            result["expected_fixed_base_distances"],
        )
        self.assertTrue(result["pass"])

    def test_signed_width_additivity(self) -> None:
        result = signed_width_additivity_certificate()
        self.assertTrue(result["interior_cancellation"])
        self.assertEqual(
            result["product_width"],
            result["left_width"] + result["right_width"],
        )
        self.assertTrue(result["pass"])

    def test_cyclotomic_scalar_switch(self) -> None:
        result = cyclotomic_scalar_switch_certificate()
        self.assertEqual(result["source_size"], result["large_mask_support_size"])
        self.assertEqual(result["scalar_copy_count"], result["expected_copy_count"])
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
