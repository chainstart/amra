#!/usr/bin/env python3
"""Regression test for the assertion-heavy GAP semi-extraspecial scan."""

import shutil
import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name(
    "validate_semiextraspecial_square_surjectivity.g"
)
PACKAGED_GAP = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/"
    "usr/lib/x86_64-linux-gnu/gap/gap"
)
PACKAGED_GAP_ROOT = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap"
)


class SemiExtraspecialGapRegression(unittest.TestCase):
    def test_smallgroups_scan(self) -> None:
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
            "ORDER|64|ids=[ 241, 242, 243, 244, 245 ]",
            completed.stdout,
        )
        self.assertIn(
            "DONE|groups=2665|semi_extraspecial=11|orders=8..128",
            completed.stdout,
        )


if __name__ == "__main__":
    unittest.main()
