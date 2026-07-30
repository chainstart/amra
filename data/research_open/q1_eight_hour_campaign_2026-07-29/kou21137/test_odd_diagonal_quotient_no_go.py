#!/usr/bin/env python3
"""p=3 regression for the general odd diagonal-quotient no-go theorem."""

import shutil
import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name(
    "validate_odd_diagonal_quotient_no_go.g"
)
PACKAGED_GAP = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/"
    "usr/lib/x86_64-linux-gnu/gap/gap"
)
PACKAGED_GAP_ROOT = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap"
)


class OddDiagonalNoGoRegression(unittest.TestCase):
    def test_exact_moment_scan(self) -> None:
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
            "ORDER|729|admissible=234|proper_targets=147"
            "|wreath_closed=[ 471, 472, 473, 474 ]",
            completed.stdout,
        )
        self.assertIn(
            "NO_GO|orders=27,81,243,729|proper_targets=165"
            "|proper_target_closures=0",
            completed.stdout,
        )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
