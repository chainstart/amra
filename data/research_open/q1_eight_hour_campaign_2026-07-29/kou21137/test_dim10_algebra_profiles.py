#!/usr/bin/env python3
"""Regression for the human-checkable dimension-ten profile reduction."""

import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("search_dim10_algebra_profiles.py")


class DimensionTenProfilesRegression(unittest.TestCase):
    def test_exact_profile_counts_and_minimum_model(self) -> None:
        completed = subprocess.run(
            ["python3", str(SCRIPT)],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=completed.stdout + completed.stderr,
        )
        self.assertIn(
            "DIM10_PROFILES|total=92|length6=56|length7=28"
            "|length8=8|length9=0|after_layer_rank=29"
            "|after_d2_d3=23|after_degree=14"
            "|after_one_layer=10|after_tail_tensor=6"
            "|after_length7_power=3"
            "|after_length7_cyclic_j3=2"
            "|after_length8_cyclic_tail=0|survivors=0",
            completed.stdout,
        )
        self.assertNotIn("DIM10_SURVIVOR|", completed.stdout)
        self.assertEqual(
            completed.stdout.count("DIM10_ONE_LAYER_EXCLUDED|"), 4
        )
        for profile in (
            "2,2,2,1,1,2",
            "2,2,2,1,2,1",
            "2,2,1,1,2,1,1",
            "2,2,1,2,1,1,1",
        ):
            self.assertIn(
                "DIM10_ONE_LAYER_EXCLUDED"
                f"|profile={profile}"
                "|reason=di_one_forces_di1_at_most_one",
                completed.stdout,
            )
        self.assertEqual(
            completed.stdout.count("DIM10_TAIL_TENSOR_EXCLUDED|"), 4
        )
        for profile in (
            "2,2,2,2,1,1",
            "2,2,3,1,1,1",
            "2,3,2,1,1,1",
            "3,2,2,1,1,1",
        ):
            self.assertIn(
                "DIM10_TAIL_TENSOR_EXCLUDED"
                f"|profile={profile}"
                "|reason=J7_zero_and_d5_d6_one",
                completed.stdout,
            )
        self.assertEqual(
            completed.stdout.count("DIM10_LENGTH7_POWER_EXCLUDED|"), 3
        )
        for profile in (
            "2,3,1,1,1,1,1",
            "3,2,1,1,1,1,1",
            "4,1,1,1,1,1,1",
        ):
            self.assertIn(
                "DIM10_LENGTH7_POWER_EXCLUDED"
                f"|profile={profile}"
                "|reason=J8_zero_and_d3_d4_d6_one",
                completed.stdout,
            )
        self.assertIn(
            "DIM10_LENGTH7_CYCLIC_J3_EXCLUDED"
            "|profile=2,2,2,1,1,1,1"
            "|reason=J8_zero_and_d4_through_d7_one",
            completed.stdout,
        )
        self.assertEqual(
            completed.stdout.count(
                "DIM10_LENGTH8_CYCLIC_TAIL_EXCLUDED|"
            ),
            2,
        )
        for profile in (
            "2,2,1,1,1,1,1,1",
            "3,1,1,1,1,1,1,1",
        ):
            self.assertIn(
                "DIM10_LENGTH8_CYCLIC_TAIL_EXCLUDED"
                f"|profile={profile}"
                "|reason=J9_zero_and_d3_through_d8_one",
                completed.stdout,
            )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
