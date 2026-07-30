#!/usr/bin/env python3
"""Exhaust all normal quotients of UT_3(F_3) wr C_3."""

import shutil
import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name(
    "validate_exponent_p_all_quotients_p3.g"
)
PACKAGED_GAP = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/"
    "usr/lib/x86_64-linux-gnu/gap/gap"
)
PACKAGED_GAP_ROOT = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap"
)


class ExponentPAllQuotientsP3Regression(unittest.TestCase):
    def test_every_normal_quotient(self) -> None:
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
            timeout=600,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=completed.stdout + completed.stderr,
        )
        self.assertIn(
            "EXP_P_ALL_QUOTIENTS_P3|wreath_order=59049"
            "|normal_subgroups=101|cube_values=219|cube_group_order=243"
            "|K_order=27|DeltaU_order=3|delta_killed=100|closed=98"
            "|closed_L_le_K=1|closed_L_outside_K=97"
            "|closed_nonabelian=0",
            completed.stdout,
        )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
