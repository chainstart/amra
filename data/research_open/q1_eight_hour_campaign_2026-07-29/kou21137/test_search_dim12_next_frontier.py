#!/usr/bin/env python3
"""Regression for the dimension-twelve necessary-profile frontier."""

import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("search_dim12_next_frontier.py")


class DimensionTwelveFrontierRegression(unittest.TestCase):
    def test_exact_human_filter_ledger_and_profiles(self) -> None:
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
            "DIM12_PROFILE_FRONTIER"
            "|total=582"
            "|length6=252"
            "|length7=210"
            "|length8=120"
            "|length9=0"
            "|after_layer_rank=136"
            "|after_quadratic_relation=117"
            "|after_one_layer=42"
            "|after_degree=37"
            "|after_tail_tensor=24"
            "|after_length7_power=20"
            "|after_cyclic_j3_tail=15"
            "|after_length8_cyclic_basis=11"
            "|after_length6_closure=8"
            "|profile_candidates=8"
            "|status=necessary_profiles_only",
            completed.stdout,
        )
        expected = (
            "2,2,2,2,2,2",
            "3,2,2,2,2,1",
            "2,2,2,2,2,1,1",
            "2,2,2,3,1,1,1",
            "2,3,2,2,1,1,1",
            "2,3,3,1,1,1,1",
            "3,2,2,2,1,1,1",
            "2,2,2,2,1,1,1,1",
        )
        self.assertEqual(
            completed.stdout.count("DIM12_BRANCH_INPUT|"), len(expected)
        )
        for profile in expected:
            self.assertIn(
                f"DIM12_BRANCH_INPUT|profile={profile}"
                "|status=requires_new_closure_branch_analysis",
                completed.stdout,
            )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
