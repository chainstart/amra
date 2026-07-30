#!/usr/bin/env python3
"""Regression for the exact Q2 graded front-end."""

import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name(
    "audit_dim11_q2_graded_frontend.py"
)


class DimensionElevenQ2FrontendRegression(unittest.TestCase):
    def test_exact_130_plane_reduction(self) -> None:
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
            "DIM11_Q2_GRADED_FRONTEND"
            "|field=F3"
            "|quadratic_relation_planes=130"
            "|q_bijective_relation_planes=12"
            "|q_bijective_d4_one_planes=3"
            "|q_bijective_d4_two_planes=9"
            "|q_bijective_maximum_d4=2"
            "|q_bijective_d4_two_commutative=9"
            "|commutative_irreducible_quadratics=3"
            "|commutative_split_quadratics=6"
            "|universal_full_tail_planes=13"
            "|degree5_projective_extensions=52"
            "|target_profile_cases=16"
            "|Q2_target_cases=12"
            "|non_Q2_target_cases=4"
            "|collapsed_A6_cases=36",
            completed.stdout,
        )
        self.assertIn("DIM11_Q2_TARGET_CASES|cases=", completed.stdout)
        self.assertIn(
            "DIM11_Q2_NINE_POINT_CASES|cases=", completed.stdout
        )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
