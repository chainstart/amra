#!/usr/bin/env python3
"""Regression for the exhaustive quadratic-relation plane audit."""

import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name(
    "audit_quadratic_relation_d3_bound.py"
)


class QuadraticRelationBoundRegression(unittest.TestCase):
    def test_all_130_relation_planes_have_d3_at_most_two(self) -> None:
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
            "QUADRATIC_RELATION_D3_AUDIT"
            "|field=F3"
            "|dim_V=2"
            "|dim_R=2"
            "|grassmannian_planes=130",
            completed.stdout,
        )
        self.assertIn(
            "|maximum_d3=2|profile_2231111_possible=false",
            completed.stdout,
        )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
