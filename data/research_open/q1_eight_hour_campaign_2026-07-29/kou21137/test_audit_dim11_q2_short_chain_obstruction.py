#!/usr/bin/env python3
"""Regression for the exact dim(Q)=2 short-chain obstruction."""

import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name(
    "audit_dim11_q2_short_chain_obstruction.py"
)


class DimensionElevenQTwoShortChainAuditRegression(unittest.TestCase):
    def test_all_frontend_cases_have_short_chain_obstruction(self) -> None:
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
            "DIM11_Q2_SHORT_CHAIN_AUDIT"
            "|field=F3"
            "|nine_point_frontend_cases=12"
            "|quadratic_planes=6"
            "|extensions_per_plane=2"
            "|mixed_quadratic_products_zero=12"
            "|short_square_nonzero=12"
            "|short_fifth_zero_in_A5=12"
            "|long_sixth_nonzero_in_A6=12"
            "|long_sixth_times_short_zero_in_A7=12",
            completed.stdout,
        )
        self.assertIn("DIM11_Q2_SHORT_CHAIN_CASES|cases=", completed.stdout)
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
