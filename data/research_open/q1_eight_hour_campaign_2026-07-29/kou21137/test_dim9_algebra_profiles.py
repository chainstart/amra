#!/usr/bin/env python3
"""Regression for the minimal dimension-nine raw-closure obstruction."""

import hashlib
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("search_dim9_algebra_profiles.py")


class DimensionNineAlgebraProfilesRegression(unittest.TestCase):
    def test_minimal_length_six_profile(self) -> None:
        if shutil.which("z3") is None:
            self.skipTest("z3 is not installed")
        with tempfile.TemporaryDirectory() as directory:
            certificate = Path(directory) / "dim9_minimal.smt2"
            completed = subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    "--emit-smt",
                    str(certificate),
                    "--timeout",
                    "120",
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=180,
            )
            certificate_bytes = certificate.read_bytes()

        self.assertEqual(
            completed.returncode,
            0,
            msg=completed.stdout + completed.stderr,
        )
        self.assertEqual(
            completed.stdout,
            "DIM9_PROFILES|total=29|length6=21|length7=7|length8=1"
            "|length6_degree_pruned=20|minimal_direct=2,2,2,1,1,1\n"
            "DIM9_MINIMAL_MODEL|structure_variables=140|root_variables=9"
            "|associativity=276|surjectivity=15"
            "|projection_bijection=36|pair_closure_equations=9"
            "|full_raw_closure=false\n"
            "DIM9_SOLVER|result=unsat\n"
            "DONE\n",
        )
        self.assertEqual(len(certificate_bytes), 182311)
        self.assertEqual(certificate_bytes.count(b"\n"), 639)
        self.assertEqual(
            hashlib.sha256(certificate_bytes).hexdigest(),
            "88c1c37c45083469fa8ceb7d9d008688"
            "def27471573c1feb897b9b453fd193de",
        )


if __name__ == "__main__":
    unittest.main()
