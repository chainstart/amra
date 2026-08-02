"""Regression tests for the near-full heavy-factor hub theorem."""

import unittest

from verify_heavy_factor_hub_ruled_chart import (
    endpoint_certificate,
    heavy_hub_certificate,
    reciprocal_chart_certificate,
)


class HeavyFactorHubRuledChartTests(unittest.TestCase):
    def test_endpoint(self) -> None:
        result = endpoint_certificate()
        self.assertEqual(result["hub_exponent"], "5/9")
        self.assertTrue(result["division_by_log_U_is_subpower"])
        self.assertTrue(result["pass"])

    def test_heavy_hub(self) -> None:
        result = heavy_hub_certificate()
        self.assertTrue(result["every_leaf_has_heavy_factor"])
        self.assertGreaterEqual(
            result["hub_leaf_count"], result["pigeonhole_lower_bound"]
        )
        self.assertTrue(result["pass"])

    def test_reciprocal_chart(self) -> None:
        result = reciprocal_chart_certificate()
        self.assertTrue(result["all_direction_and_chart_identities"])
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
