#!/usr/bin/env python3
"""Regression for the finite dim-11 branch audit."""

import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("analyze_dim11_closure_branches.py")


class DimensionElevenBranchAuditRegression(unittest.TestCase):
    def test_exact_leading_map_and_kernel_counts(self) -> None:
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
            "DIM11_Q1_LEADING_MAPS"
            "|nonzero_homogeneous_cubic_functions=80"
            "|zero_projective_lines_0=16"
            "|zero_projective_lines_1=32"
            "|zero_projective_lines_2=24"
            "|zero_projective_lines_3=8"
            "|closure_noncommuting_excludes_zero_free=16"
            "|after_zero_free_exclusion=64"
            "|tail_pure_linear_maps=8"
            "|tail_pure_normal_forms=1"
            "|status=leading_data_not_excluded",
            completed.stdout,
        )
        self.assertIn(
            "DIM11_Q2_LEADING_MAPS"
            "|odd_bijections=384"
            "|tail_pure_leading_cube_normal_forms=2"
            "|A2_to_A6_nonzero_scalar_cubics=80"
            "|tail_pure_A2_to_A6_linear_maps=8"
            "|tail_pure_cube_normal_forms=2"
            "|status=leading_data_not_excluded",
            completed.stdout,
        )
        self.assertIn(
            "DIM11_Q2_KERNEL_CONTRACT|K=J6|H_order=81",
            completed.stdout,
        )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
