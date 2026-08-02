"""Regression tests for the exact mixed-high outer-low identity."""

import unittest

from verify_erdos809_outer_low_mixed_high_identity import (
    exhaustive_certificate,
    profile,
)


class OuterLowMixedHighIdentityTests(unittest.TestCase):
    def test_all_four_profile_types(self) -> None:
        for args in (
            (4, 3, "cross"),
            (0, 3, "internal"),
            (4, 3, "internal"),
            (4, 3, "none"),
            (0, 3, "none"),
        ):
            result = profile(*args)
            self.assertTrue(result["low_localization_matches"])
            self.assertTrue(result["identity_matches"])

    def test_mixed_internal_high_is_the_only_positive_correction(self) -> None:
        mixed = profile(5, 2, "internal")
        self.assertEqual(mixed["mixed"], 1)
        self.assertEqual(
            mixed["residue"], mixed["low_internal"] + 1
        )

    def test_internal_only_low_is_the_only_negative_correction(self) -> None:
        internal_only = profile(0, 5, "none")
        self.assertEqual(internal_only["internal_only_low"], 1)
        self.assertEqual(
            internal_only["residue"], internal_only["low_internal"] - 1
        )

    def test_exhaustive_profiles(self) -> None:
        result = exhaustive_certificate(limit=24)
        self.assertTrue(result["all_colourwise_identities"])
        self.assertTrue(result["all_aggregate_identities"])
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
