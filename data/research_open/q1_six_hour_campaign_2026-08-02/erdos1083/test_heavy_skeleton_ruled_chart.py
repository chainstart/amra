"""Regression tests for the heavy-skeleton ruled-chart theorem."""

import unittest

from verify_heavy_skeleton_ruled_chart import (
    entropy_margin_certificate,
    omitted_pattern_certificate,
    reciprocal_chart_certificate,
    signed_quotient_firewall_certificate,
)


class HeavySkeletonRuledChartTests(unittest.TestCase):
    def test_entropy_margin(self) -> None:
        result = entropy_margin_certificate()
        self.assertEqual(result["entropy_ratio"], "1/15")
        self.assertTrue(result["positive_margin"])
        self.assertTrue(result["pass"])

    def test_omitted_pattern_pigeonhole(self) -> None:
        result = omitted_pattern_certificate()
        self.assertEqual(result["number_of_patterns"], result["binomial_tail"])
        self.assertGreaterEqual(
            result["largest_pattern_class"], result["pigeonhole_bound"]
        )
        self.assertTrue(result["pass"])

    def test_signed_quotient_firewall(self) -> None:
        result = signed_quotient_firewall_certificate()
        self.assertTrue(result["quotient_has_negative_coefficient"])
        self.assertTrue(result["x_product_is_mask"])
        self.assertTrue(result["y_product_is_mask"])
        self.assertTrue(result["double_product_is_mask"])
        self.assertTrue(result["pass"])

    def test_reciprocal_chart(self) -> None:
        result = reciprocal_chart_certificate()
        self.assertTrue(result["all_chart_identities_hold"])
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
