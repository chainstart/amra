#!/usr/bin/env python3
"""Regression for the odd-prime nilpotency-class barrier."""

import shutil
import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_odd_kou_nilpotency_barrier.g")
PACKAGED_GAP = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/"
    "usr/lib/x86_64-linux-gnu/gap/gap"
)
PACKAGED_GAP_ROOT = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap"
)


class OddKouNilpotencyBarrierRegression(unittest.TestCase):
    def test_smallgroups_scan_and_ut7_witness(self) -> None:
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
        expected_rows = (
            "ODD_KOU_CLASS|p=3|class=1|exp9=9|power_nonabelian=0"
            "|power_closed=9|closed_nonabelian=0|first_nonabelian=fail",
            "ODD_KOU_CLASS|p=3|class=2|exp9=118|power_nonabelian=0"
            "|power_closed=118|closed_nonabelian=0|first_nonabelian=fail",
            "ODD_KOU_CLASS|p=3|class=3|exp9=270|power_nonabelian=0"
            "|power_closed=155|closed_nonabelian=0|first_nonabelian=fail",
            "ODD_KOU_CLASS|p=3|class=4|exp9=66|power_nonabelian=0"
            "|power_closed=30|closed_nonabelian=0|first_nonabelian=fail",
            "ODD_KOU_SCAN|p=3|orders=3..729|groups=594|exp9=463"
            "|power_nonabelian=0|closed_nonabelian=0",
            "UT7_WITNESS|p=3|ambient_class=6|ambient_exponent=9"
            "|x_order=9|y_order=9|cubes_commute=false",
        )
        for row in expected_rows:
            self.assertIn(row, completed.stdout)
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
