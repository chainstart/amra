"""Regression tests for the power-large simultaneous-switch core."""

import unittest

from verify_power_large_simultaneous_switch_core import (
    branch_pigeonhole_certificate,
    clean_quotient_certificate,
    cyclotomic_barrier_certificate,
    divisor_width_certificate,
    endpoint_certificate,
    quotient_ledger_certificate,
    same_sign_distance_certificate,
)


class PowerLargeSimultaneousSwitchCoreTests(unittest.TestCase):
    def test_quotient_ledger(self) -> None:
        result = quotient_ledger_certificate()
        self.assertEqual(result["Q_at_one"], result["U"] // result["S"])
        self.assertTrue(result["strict_endpoint"])
        self.assertTrue(result["pass"])

    def test_divisor_width_atlas(self) -> None:
        result = divisor_width_certificate()
        self.assertGreaterEqual(result["omega"], result["log_bound"])
        self.assertTrue(result["all_binary_width_sums_distinct"])
        self.assertTrue(result["pass"])

    def test_clean_and_contaminated_examples(self) -> None:
        result = clean_quotient_certificate()
        self.assertTrue(result["clean_product_is_mask"])
        self.assertTrue(result["clean_support_sum_injective"])
        self.assertTrue(result["signed_quotient_has_negative_coefficient"])
        self.assertTrue(result["contaminated_product_is_mask"])
        self.assertTrue(result["pass"])

    def test_rowwise_branch_pigeonholes(self) -> None:
        result = branch_pigeonhole_certificate()
        self.assertEqual(result["boolean_partitions_checked"], 2**15 - 2)
        self.assertTrue(result["clean_contaminated_majority"])
        self.assertTrue(result["mask_signed_majority"])
        self.assertTrue(result["nonnegative_nonmask_rejected"])
        self.assertTrue(result["contaminated_does_not_imply_signed"])
        self.assertTrue(result["pass"])

    def test_same_sign_distance_and_literal_mixed_sign_boundary(self) -> None:
        result = same_sign_distance_certificate()
        self.assertTrue(result["same_sign_formula_holds"])
        self.assertTrue(result["literal_endpoint_strict"])
        self.assertTrue(result["literal_direct_exact_block"])
        self.assertTrue(result["literal_common_tangent"])
        self.assertTrue(result["all_literal_tangents_positive"])
        self.assertEqual(result["leaf_residual_widths"], [0, 0])
        self.assertEqual(result["mixed_sign_width_prediction"], "0")
        self.assertTrue(result["unrestricted_formula_fails"])
        self.assertTrue(result["pass"])

    def test_cyclotomic_prime_valuation_barrier(self) -> None:
        result = cyclotomic_barrier_certificate()
        self.assertTrue(result["pass"])
        self.assertTrue(result["boundary_M4_m2_phi12"])
        self.assertTrue(result["contains_gap_greater_than_one"])
        for record in result["records"]:
            self.assertLess(record["valuation_in_m"], record["valuation_in_M"])
            self.assertTrue(record["missing_cyclotomic_divides"])
            self.assertEqual(
                record["positive_multiple_terms"], record["predicted_minimum"]
            )

    def test_endpoint_exponents(self) -> None:
        result = endpoint_certificate()
        self.assertEqual(result["switch_family_exponent"], "5/9")
        self.assertEqual(result["source_size_exponent"], "7/9")
        self.assertEqual(result["complement_size_exponent"], "5/6")
        self.assertEqual(result["quotient_size_exponent"], "1/18")
        self.assertEqual(result["fixed_difference_star_exponent"], "1/6")
        self.assertTrue(result["quotient_is_exponent_difference"])
        self.assertTrue(result["source_not_star_exponent"])
        self.assertTrue(result["strict_C_below_S"])
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
