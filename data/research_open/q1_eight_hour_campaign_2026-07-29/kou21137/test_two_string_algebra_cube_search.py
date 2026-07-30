#!/usr/bin/env python3
"""Compile and run the exact 3^15 two-string algebra cube audit."""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SOURCE = Path(__file__).with_name("two_string_algebra_cube_search.cpp")


class TwoStringAlgebraCubeSearchRegression(unittest.TestCase):
    def test_exact_cube_image(self) -> None:
        compiler = shutil.which("g++")
        if compiler is None:
            self.skipTest("g++ is not installed")

        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "two_string_algebra_cube_search"
            compiled = subprocess.run(
                [
                    compiler,
                    "-O3",
                    "-std=c++17",
                    str(SOURCE),
                    "-o",
                    str(executable),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(
                compiled.returncode,
                0,
                msg=compiled.stdout + compiled.stderr,
            )
            completed = subprocess.run(
                [str(executable)],
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
        self.assertEqual(
            completed.stdout.strip(),
            "TWO_STRING_ALGEBRA|dimension=15|elements=14348907"
            "|cube_values=1947|noncommuting_pair=true|closed=false"
            "|noncommuting_left=9|noncommuting_right=243"
            "|closure_left=9|closure_right=243"
            "|missing_product=4783221|witness=A3,B3"
            "|missing=A3+B3+M33",
        )


if __name__ == "__main__":
    unittest.main()
