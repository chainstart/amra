"""Regression tests for the simultaneous-positive-complement no-go."""

import unittest

from verify_simultaneous_positive_complement_nogo import (
    euclidean_certificate,
    mask_identity_certificate,
)


class SimultaneousPositiveComplementNoGoTests(unittest.TestCase):
    def test_all_parameter_samples(self) -> None:
        result = mask_identity_certificate()
        self.assertTrue(result["pass"])
        for record in result["records"]:
            self.assertTrue(record["a0_is_mask"])
            self.assertTrue(record["a1_is_mask"])
            self.assertTrue(record["spectrum_is_mask"])
            self.assertTrue(record["strict_U_below_S_squared"])

    def test_minimal_strict_case(self) -> None:
        result = mask_identity_certificate(4, 4)
        record = result["records"][0]
        self.assertEqual(record["source_size"], 4)
        self.assertEqual(record["quotient_augmentation"], 3)
        self.assertEqual(record["complement_size_0"], 12)
        self.assertEqual(record["spectrum_size"], 48)
        self.assertTrue(result["pass"])

    def test_euclidean_realization(self) -> None:
        result = euclidean_certificate()
        self.assertEqual(result["alpha_over_beta"], "sqrt(2)")
        self.assertTrue(result["common_tangent_identity"])
        self.assertTrue(result["common_tangent_in_both_sets"])
        self.assertTrue(result["all_tangents_positive"])
        self.assertTrue(result["row0_equals_spectrum"])
        self.assertTrue(result["row1_equals_spectrum"])
        self.assertTrue(result["all_cartesian_distance_identities"])
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
