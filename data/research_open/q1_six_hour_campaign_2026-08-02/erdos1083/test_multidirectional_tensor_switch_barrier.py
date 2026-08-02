"""Regression tests for the multidirectional tensor-switch barrier."""

import unittest

from verify_multidirectional_tensor_switch_barrier import (
    direction_and_factor_certificate,
    endpoint_calibration_certificate,
    homothety_class_certificate,
    tensor_family_certificate,
)


class MultidirectionalTensorSwitchBarrierTests(unittest.TestCase):
    def test_every_tensor_subset(self) -> None:
        result = tensor_family_certificate()
        self.assertEqual(result["family_size"], 2 ** result["rank"])
        self.assertEqual(result["distinct_residual_signatures"], result["family_size"])
        self.assertTrue(result["base_switch_identities"])
        self.assertTrue(result["common_positive_mask"])
        for record in result["records"]:
            self.assertTrue(record["B_factorization"])
            self.assertTrue(record["source_is_mask"])
            self.assertTrue(record["complement_is_mask"])
            self.assertTrue(record["signed_exactly_when_nonempty"])
        self.assertTrue(result["pass"])

    def test_exact_endpoint_calibration(self) -> None:
        result = endpoint_calibration_certificate()
        self.assertTrue(result["C_power_14_equals_S"])
        self.assertTrue(result["U_equals_SC"])
        self.assertTrue(result["S_endpoint"])
        self.assertTrue(result["C_endpoint"])
        self.assertTrue(result["U_endpoint"])
        self.assertTrue(result["family_dominates_required"])
        self.assertTrue(result["pass"])

    def test_homothety_classes_have_sharp_k_plus_one_bound(self) -> None:
        result = homothety_class_certificate()
        self.assertGreater(result["patterns_checked"], 6000)
        for record in result["sharp_records"]:
            self.assertEqual(record["maximum_class"], record["rank"] + 1)
            self.assertEqual(record["sharp_prefix_class_size"], record["rank"] + 1)
            self.assertTrue(record["prefix_patterns_exact"])
            self.assertTrue(record["pass"])
        for record in result["general_records"]:
            self.assertLessEqual(record["maximum_class"], record["bound"])
            self.assertTrue(record["pass"])
        self.assertTrue(result["pass"])

    def test_signed_contaminated_and_divisor_counts(self) -> None:
        result = direction_and_factor_certificate()
        self.assertEqual(result["distinct_divisor_vectors"], 2 ** result["rank"])
        self.assertEqual(result["signed_contaminated_rows"], 2 ** result["rank"] - 1)
        self.assertEqual(result["clean_rows"], 1)
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
