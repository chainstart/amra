#!/usr/bin/env python3
"""Regression for the strict dimension-eleven profile ledger."""

import subprocess
import unittest
from pathlib import Path

from search_dim11_algebra_profiles import quadratic_relation_valid


SCRIPT = Path(__file__).with_name("search_dim11_algebra_profiles.py")


class DimensionElevenProfilesRegression(unittest.TestCase):
    def test_two_quadratic_normal_words_bound_d3_for_any_d1(self) -> None:
        self.assertFalse(quadratic_relation_valid((3, 2, 3, 1, 1, 1)))
        self.assertTrue(quadratic_relation_valid((3, 2, 2, 1, 1, 1, 1)))

    def test_exact_counts_and_survivors(self) -> None:
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
            "DIM11_PROFILES|total=246|length6=126|length7=84"
            "|length8=36|length9=0",
            completed.stdout,
        )
        self.assertIn(
            "|after_layer_rank=65"
            "|after_quadratic_relation=59"
            "|after_one_layer=23"
            "|after_degree=19",
            completed.stdout,
        )
        self.assertIn(
            "|structural_survivors=2"
            "|profile_candidates_after_length6_closure=1"
            "|after_qdim_branches=0"
            "|closure_survivors=0",
            completed.stdout,
        )
        self.assertIn(
            "DIM11_CLOSURE_EXCLUDED|profile=2,2,2,2,2,1"
            "|reason=A3_bijection_and_fibre_kernel_force_cube_commutativity",
            completed.stdout,
        )
        self.assertEqual(completed.stdout.count("DIM11_BRANCH_INPUT|"), 1)
        for profile in (
            "2,2,2,2,1,1,1",
        ):
            self.assertIn(
                f"DIM11_BRANCH_INPUT|profile={profile}|",
                completed.stdout,
            )
        self.assertEqual(
            completed.stdout.count(
                "|closure_contract=Q_dim1_or_Q_dim2_K_eq_J6_H_order81"
            ),
            1,
        )
        self.assertIn(
            "|status=excluded_by_qdim_branch_theorems",
            completed.stdout,
        )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
