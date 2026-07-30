#!/usr/bin/env python3
"""Regression for the complete two-string UT(7,3) subquotient no-go."""

import shutil
import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_ut7_two_string_no_go.g")
PACKAGED_GAP = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/"
    "usr/lib/x86_64-linux-gnu/gap/gap"
)
PACKAGED_GAP_ROOT = Path(
    "/home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap"
)


class UT7TwoStringNoGoRegression(unittest.TestCase):
    def test_all_subgroups_and_normal_quotients(self) -> None:
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
            timeout=180,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=completed.stdout + completed.stderr,
        )
        self.assertIn(
            "UT7_TWO_STRING|order=1594323|class=6|exponent=9"
            "|raw_cubes=649|cube_group=59049|cube_group_class=2"
            "|cube_group_exponent=3|cube_derived=3|centre=3"
            "|raw_closed=false|cube_group_powerful=false",
            completed.stdout,
        )
        self.assertIn(
            "NORMAL_QUOTIENTS|normal_subgroups=641|nontrivial=640"
            "|all_nontrivial_kill_cube_derived=true"
            "|trivial_quotient_raw_closed=false|kou_hits=0",
            completed.stdout,
        )
        self.assertEqual(completed.stdout.count("MAXIMAL|"), 4)
        self.assertEqual(
            completed.stdout.count(
                "|order=531441|raw_cubes=163|cube_group=243"
                "|raw_closed=false|cube_group_abelian=true"
                "|cube_group_powerful=true"
            ),
            4,
        )
        self.assertIn(
            "PROPER_SUBGROUPS|maximal_subgroups=4"
            "|all_maximal_cube_groups_abelian=true"
            "|all_closed_raw_cube_subgroups_powerful=true|kou_hits=0",
            completed.stdout,
        )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
