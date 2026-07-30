#!/usr/bin/env python3
"""Direct p=3 and p=5 regression for the general prime-wreath theorem."""

import shutil
import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name(
    "validate_general_prime_wreath_criterion.g"
)
PACKAGED_GAP = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/"
    "usr/lib/x86_64-linux-gnu/gap/gap"
)
PACKAGED_GAP_ROOT = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap"
)


class GeneralPrimeWreathCriterionRegression(unittest.TestCase):
    def test_direct_wreath_scans(self) -> None:
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
            "PRIME_SCAN|p=3|orders=1..16|groups=42|hits=34",
            completed.stdout,
        )
        self.assertIn(
            "PRIME_SCAN|p=5|orders=1..10|groups=18|hits=16",
            completed.stdout,
        )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
