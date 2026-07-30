#!/usr/bin/env python3
"""Regression for the exact dim(Q)=1 quadratic classification."""

import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name(
    "audit_dim11_q1_quadratic_commutativity.py"
)


class DimensionElevenQOneQuadraticAuditRegression(unittest.TestCase):
    def test_exact_q_one_relation_planes_are_commutative(self) -> None:
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
            "DIM11_Q1_QUADRATIC_AUDIT"
            "|field=F3"
            "|quadratic_relation_planes=130"
            "|d3_two_planes=34"
            "|qdim1_zero_lines1=4"
            "|qdim2_zero_lines0=12"
            "|qdim2_zero_lines1=12"
            "|qdim2_zero_lines2=6"
            "|qdim1_image_size=3"
            "|qdim1_contains_xy_minus_yx=4"
            "|qdim1_universal_dimensions_d2_to_d7=2,2,2,2,2,2",
            completed.stdout,
        )
        self.assertIn("DIM11_Q1_RELATION_PLANES|cases=", completed.stdout)
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
