"""Regression tests for the coherent-theta Euclidean no-go model."""

import unittest

from verify_coherent_theta_euclidean_nogo import (
    build_certificate,
    endpoint_exponent_certificate,
)


class CoherentThetaEuclideanNoGoTests(unittest.TestCase):
    def test_small_model(self) -> None:
        result = build_certificate(5, 1)
        self.assertTrue(result["pass"])
        self.assertEqual(result["orientation_word"], "+-")
        self.assertEqual(result["fixed_difference_values"], ["1", "1"])

    def test_intermediate_model(self) -> None:
        result = build_certificate(7, 4)
        self.assertTrue(result["points_distinct"])
        self.assertTrue(result["every_selected_cell_injective"])
        self.assertTrue(result["every_endpoint_internal_ratio_irrational"])
        self.assertTrue(result["selected_distances_all_common"])
        self.assertTrue(result["pass"])

    def test_maximal_width_model(self) -> None:
        source_size = 10
        result = build_certificate(source_size, source_size - 1)
        self.assertEqual(result["arm_count"], source_size - 1)
        self.assertEqual(result["point_count"], 2 * source_size + 1)
        self.assertTrue(result["interiors_pairwise_disjoint"])
        self.assertTrue(result["endpoint_formula_bound_holds"])
        self.assertTrue(result["pass"])

    def test_invalid_quantifiers(self) -> None:
        with self.assertRaises(ValueError):
            build_certificate(1, 1)
        with self.assertRaises(ValueError):
            build_certificate(5, 0)
        with self.assertRaises(ValueError):
            build_certificate(5, 5)
        with self.assertRaises(ValueError):
            build_certificate(5, 2, tangent=0)

    def test_endpoint_exponents(self) -> None:
        result = endpoint_exponent_certificate()
        self.assertEqual(result["local_complete_distance_upper_exponent"], "14/9")
        self.assertEqual(result["budget_margin"], "13/9")
        self.assertTrue(result["maximal_width_dominates_inherited_theta"])
        self.assertTrue(result["local_distance_bound_below_global_budget"])
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
