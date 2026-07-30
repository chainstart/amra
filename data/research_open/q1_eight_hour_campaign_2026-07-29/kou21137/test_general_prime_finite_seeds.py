#!/usr/bin/env python3
"""Regression for the all-prime finite-seed classification."""

import shutil
import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_general_prime_finite_seeds.g")
PACKAGED_GAP = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/"
    "usr/lib/x86_64-linux-gnu/gap/gap"
)
PACKAGED_GAP_ROOT = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap"
)


class GeneralPrimeFiniteSeedsRegression(unittest.TestCase):
    def test_all_groups_through_128_at_three_primes(self) -> None:
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
        expected = {
            2: "criterion=164|class_counts=[ 107, 7, 11, 38, 1 ]",
            3: "criterion=2990|class_counts=[ 2975, 4, 1, 10, 0 ]",
            5: "criterion=3401|class_counts=[ 3395, 3, 1, 2, 0 ]",
        }
        for prime, suffix in expected.items():
            self.assertIn(
                f"FINITE_PRIME_SEEDS|p={prime}|orders=1..128"
                f"|groups=3596|{suffix}",
                completed.stdout,
            )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
