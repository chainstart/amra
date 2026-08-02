"""Regression tests for the exact-block transverse-star theorem."""

import unittest

from verify_exact_block_transverse_star_cluster import (
    endpoint_certificate,
    exhaustive_triangle_free_neighbourhood_certificate,
    quotient_identity_certificate,
    rank_two_examples_certificate,
)


class ExactBlockTransverseStarClusterTests(unittest.TestCase):
    def test_endpoint_exponents(self) -> None:
        result = endpoint_certificate()
        self.assertEqual(result["S2_over_U_margin"], "13/18")
        self.assertEqual(result["star_leaf_exponent"], "1/6")
        self.assertEqual(result["common_tangent_leaf_exponent"], "5/9")
        self.assertTrue(result["U_strictly_below_S2"])
        self.assertTrue(result["pass"])

    def test_triangle_free_neighbourhoods(self) -> None:
        result = exhaustive_triangle_free_neighbourhood_certificate(6)
        self.assertGreater(result["graph_count"], 0)
        self.assertGreater(result["triangle_free_graph_count"], 0)
        self.assertGreater(result["neighbourhood_checks"], 0)
        self.assertTrue(result["all_triangle_free_neighbourhoods_independent"])
        self.assertTrue(result["pass"])

    def test_rank_two_star_and_top_are_both_real(self) -> None:
        result = rank_two_examples_certificate()
        self.assertEqual(result["star_total_intersection_dimension"], 1)
        self.assertEqual(result["star_total_span_dimension"], 4)
        self.assertEqual(result["top_total_intersection_dimension"], 0)
        self.assertEqual(result["top_total_span_dimension"], 3)
        self.assertTrue(result["pass"])

    def test_quotient_identity(self) -> None:
        result = quotient_identity_certificate()
        self.assertEqual(result["pair_count"], 3)
        self.assertTrue(result["all_ratios_in_quadratic_quotient_field"])
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
