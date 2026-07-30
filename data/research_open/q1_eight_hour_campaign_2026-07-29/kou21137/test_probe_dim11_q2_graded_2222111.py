#!/usr/bin/env python3
"""Regression for the deliberately incomplete graded Q2 probe."""

import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name(
    "probe_dim11_q2_graded_2222111.py"
)


class DimensionElevenQ2GradedProbeRegression(unittest.TestCase):
    def test_cheap_leading_contract_remains_satisfiable(self) -> None:
        completed = subprocess.run(
            ["python3", str(SCRIPT), "--timeout", "30"],
            check=False,
            capture_output=True,
            text=True,
            timeout=35,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=completed.stdout + completed.stderr,
        )
        self.assertIn(
            "DIM11_Q2_GRADED_PROBE"
            "|profile=2,2,2,2,1,1,1"
            "|graded_only=true"
            "|full_filtered=false"
            "|raw_closure=false",
            completed.stdout,
        )
        self.assertIn("|result=sat", completed.stdout)
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
