#!/usr/bin/env python3
"""Regression for the filtered CEGIS core and layer-rank exclusion."""

import hashlib
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("cegis_dim9_profile_2111121.py")


class DimensionNineCEGISRegression(unittest.TestCase):
    def test_profile_fails_before_closure_iterations(self) -> None:
        if shutil.which("z3") is None:
            self.skipTest("z3 is not installed")
        with tempfile.TemporaryDirectory() as directory:
            certificate_directory = Path(directory) / "certificates"
            completed = subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    "--max-iterations",
                    "40",
                    "--solver-timeout",
                    "90",
                    "--certificate-dir",
                    str(certificate_directory),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=180,
            )
            certificate_bytes = (
                certificate_directory / "iteration_000.smt2"
            ).read_bytes()

        self.assertEqual(
            completed.returncode,
            0,
            msg=completed.stdout + completed.stderr,
        )
        self.assertIn(
            "CEGIS_START|profile=2,1,1,1,1,2,1"
            "|structure_variables=134|associativity=288"
            "|surjectivity=21|relevant_dimension=6|cube_inputs=729"
            "|witness_variables=12|max_iterations=40|solver_timeout=90",
            completed.stdout,
        )
        self.assertIn(
            "CEGIS_UNSAT|iteration=0|root_constraints=0",
            completed.stdout,
        )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))
        self.assertEqual(len(certificate_bytes), 98733)
        self.assertEqual(certificate_bytes.count(b"\n"), 607)
        self.assertEqual(
            hashlib.sha256(certificate_bytes).hexdigest(),
            "91ef847a401829cd96129500a63d317"
            "02f9fecdbc58afb1bac61818309acccfd",
        )


if __name__ == "__main__":
    unittest.main()
