#!/usr/bin/env python3
"""Regression for the p=3,5 unitriangular class boundary."""

import shutil
import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_sharp_2p_matrix_boundary.g")
PACKAGED_GAP = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/"
    "usr/lib/x86_64-linux-gnu/gap/gap"
)
PACKAGED_GAP_ROOT = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap"
)


class Sharp2pMatrixBoundaryRegression(unittest.TestCase):
    def test_p3_and_p5_boundary_pairs(self) -> None:
        if PACKAGED_GAP.is_file() and PACKAGED_GAP_ROOT.is_dir():
            command = [
                str(PACKAGED_GAP),
                "-l",
                str(PACKAGED_GAP_ROOT),
                "-q",
                str(SCRIPT),
            ]
        else:
            gap = shutil.which("gap")
            if gap is None:
                self.skipTest("GAP is not installed")
            command = [gap, "-q", str(SCRIPT)]

        completed = subprocess.run(
            command,
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
        expected = (
            "UT_BOUNDARY|p=3|class_below=5|below_pair_commutes=true"
            "|witness_class=6|witness_pair_commutes=false"
            "|top_weight_nontrivial=true",
            "UT_BOUNDARY|p=5|class_below=9|below_pair_commutes=true"
            "|witness_class=10|witness_pair_commutes=false"
            "|top_weight_nontrivial=true",
        )
        for row in expected:
            self.assertIn(row, completed.stdout)
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
