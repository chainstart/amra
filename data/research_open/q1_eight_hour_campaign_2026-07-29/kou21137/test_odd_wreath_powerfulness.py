#!/usr/bin/env python3
"""Regression for powerfulness of closed odd-prime wreath power sets."""

import shutil
import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_odd_wreath_powerfulness.g")
PACKAGED_GAP = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/"
    "usr/lib/x86_64-linux-gnu/gap/gap"
)
PACKAGED_GAP_ROOT = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap"
)


class OddWreathPowerfulnessRegression(unittest.TestCase):
    def test_p3_and_p5_positive_seeds(self) -> None:
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
            timeout=240,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=completed.stdout + completed.stderr,
        )
        self.assertIn(
            "ODD_WREATH_POWERFUL|p=3|seed=extraspecial_27_exp9",
            completed.stdout,
        )
        self.assertIn(
            "ODD_WREATH_POWERFUL|p=5|seed=extraspecial_125_exp25",
            completed.stdout,
        )
        self.assertEqual(
            completed.stdout.count("|classified_closed=true|powerful=true"),
            2,
        )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
