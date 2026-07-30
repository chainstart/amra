#!/usr/bin/env python3
"""Regression for H <= W' = Phi(W) and the exact p=3 index."""

import shutil
import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_structural_position_p3.g")
PACKAGED_GAP = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/"
    "usr/lib/x86_64-linux-gnu/gap/gap"
)
PACKAGED_GAP_ROOT = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap"
)


class StructuralPositionP3Regression(unittest.TestCase):
    def test_two_positive_seeds(self) -> None:
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
            timeout=120,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=completed.stdout + completed.stderr,
        )
        self.assertIn(
            "STRUCTURAL_P3|seed=C3|seed_order=3|B_order=3"
            "|H_order=3|derived_order=9|frattini_order=9"
            "|derived_over_H=3|quotient_order=27|quotient_class=2",
            completed.stdout,
        )
        self.assertIn(
            "STRUCTURAL_P3|seed=extraspecial_27_exp9|seed_order=27"
            "|B_order=9|H_order=243|derived_order=2187"
            "|frattini_order=2187|derived_over_H=9"
            "|quotient_order=243|quotient_class=2",
            completed.stdout,
        )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
