#!/usr/bin/env python3
"""Regression for the exact dimension-eight graded-algebra constraint audit."""

import hashlib
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("search_dim8_algebra_profiles.py")


class DimensionEightAlgebraProfilesRegression(unittest.TestCase):
    def test_no_noncommuting_cube_layers(self) -> None:
        if shutil.which("z3") is None:
            self.skipTest("z3 is not installed")
        with tempfile.TemporaryDirectory() as directory:
            certificate = Path(directory) / "dim8_noncommuting.smt2"
            completed = subprocess.run(
                ["python3", str(SCRIPT), "--emit-smt", str(certificate)],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
            )
            certificate_bytes = certificate.read_bytes()
        self.assertEqual(
            completed.returncode,
            0,
            msg=completed.stdout + completed.stderr,
        )
        self.assertEqual(
            completed.stdout,
            "DIM8_PROFILES|total=7|degree_forced_commuting=5"
            "|d2_one_d3_two_impossible=1"
            "|exceptional=2,1,1,1,1,1,1\n"
            "DIM8_EXCEPTIONAL_SMT|variables=34|associativity=96"
            "|generation=21|field=3|profile_consistent=sat"
            "|noncommuting=unsat\n"
            "DIM8_RESULT|J3_commutative=true"
            "|minimum_candidate_dimension=9\n"
            "DONE\n",
        )
        self.assertEqual(len(certificate_bytes), 9722)
        self.assertEqual(certificate_bytes.count(b"\n"), 188)
        self.assertEqual(
            hashlib.sha256(certificate_bytes).hexdigest(),
            "19f252a9fda4c93e8da8919e9ef0f1d8"
            "e47a42d046548eca18541c280e9dca00",
        )


if __name__ == "__main__":
    unittest.main()
