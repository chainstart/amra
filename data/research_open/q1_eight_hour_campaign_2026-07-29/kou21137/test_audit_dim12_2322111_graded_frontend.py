#!/usr/bin/env python3
"""Regression for the profile (2,3,2,2,1,1,1) graded front-end."""

import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name(
    "audit_dim12_2322111_graded_frontend.py"
)


class DimensionTwelve2322111FrontendRegression(unittest.TestCase):
    def test_exact_fail_closed_graded_ledger(self) -> None:
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
            "DIM12_2322111_GRADED_FRONTEND"
            "|field=F3"
            "|quadratic_relation_lines=40"
            "|A2_projective_directions=13"
            "|degree4_frontends=36"
            "|degree5_projective_extensions=144"
            "|collapsed_d6_d7_image1=96"
            "|target_d6_d7_image3=48"
            "|target_case_sha256="
            "80fd2b21a7b59d1b542b759b5f20a062"
            "f451cca9c6dcdf96191e4eef386183ef",
            completed.stdout,
        )
        self.assertIn(
            "|filtered_lift_checked=false"
            "|full_raw_closure_checked=false"
            "|status=necessary_graded_cases_only",
            completed.stdout,
        )
        self.assertIn(
            "DIM12_2322111_TARGET_CASES|cases=",
            completed.stdout,
        )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
