"""Regression tests for the cyclotomic simultaneous-positive bound."""

import unittest

from verify_cyclotomic_simultaneous_positive_multiple_bound import (
    divisor_family_certificate,
    endpoint_gap_certificate,
    positive_multiple_mass_certificate,
    signed_cyclic_shadow_certificate,
)


class CyclotomicSimultaneousPositiveMultipleBoundTests(unittest.TestCase):
    def test_sharp_positive_multiple_mass_bound(self) -> None:
        result = positive_multiple_mass_certificate()
        self.assertGreater(result["matrix_profiles_checked"], 1000)
        self.assertGreater(result["subminimum_residue_masks_checked"], 100)
        self.assertEqual(result["subminimum_divisible_masks"], 0)
        self.assertTrue(result["matrix_rectangle_bound"])
        for record in result["records"]:
            self.assertTrue(record["exact_H"])
            self.assertTrue(record["a_sharp_identity"])
            self.assertTrue(record["s_sharp_identity"])
            self.assertEqual(
                min(record["a_sharp_terms"], record["s_sharp_terms"]),
                record["predicted_minimum"],
            )
        self.assertTrue(result["pass"])

    def test_signed_quotient_cyclic_shadow(self) -> None:
        result = signed_cyclic_shadow_certificate()
        self.assertTrue(result["signed_regularizer"])
        self.assertTrue(result["positive_product_is_mask"])
        self.assertTrue(result["equal_cyclic_residue_counts"])
        self.assertTrue(result["shadow_identity"])
        self.assertEqual(result["shadow_mass"], result["quotient_augmentation"])
        self.assertTrue(result["strict_C_below_S"])
        self.assertTrue(result["H_divides_shadow"])
        self.assertTrue(result["pass"])

    def test_exact_nonempty_divisor_family_and_pair_rigidity(self) -> None:
        result = divisor_family_certificate()
        self.assertTrue(result["strict_C_below_S"])
        self.assertEqual(len(result["divisors"]), 4)
        for record in result["row_records"]:
            self.assertTrue(record["residual_is_mask"])
            self.assertEqual(record["residual_terms"], result["C"])
            self.assertTrue(record["switched_is_mask"])
        for record in result["pair_records"]:
            self.assertTrue(record["factors_coprime"])
            self.assertTrue(record["cross_divisibility"])
            self.assertTrue(record["ratio_bound"])
        self.assertLessEqual(
            result["exact_coprime_pair_bound"], result["quadratic_bound"]
        )
        self.assertTrue(result["pass"])

    def test_endpoint_polynomial_exclusion(self) -> None:
        result = endpoint_gap_certificate()
        self.assertEqual(result["quadratic_bound_exponent"], "1/9")
        self.assertEqual(result["polynomial_gap"], "4/9")
        self.assertTrue(result["strict_exclusion"])
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
