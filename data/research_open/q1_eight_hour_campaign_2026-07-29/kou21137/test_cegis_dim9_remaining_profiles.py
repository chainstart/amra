#!/usr/bin/env python3
"""Canonical iteration-zero certificates for the three live dim-9 profiles."""

import hashlib
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


DIRECTORY = Path(__file__).parent
CASES = (
    (
        "cegis_dim9_profile_2111211.py",
        "2,1,1,1,2,1,1",
        133,
        275,
        21,
        95305,
        596,
        "78e76ff9c8667c335df317f872501700"
        "dabb33e9299183aae71e73b697127841",
    ),
    (
        "cegis_dim9_profile_21111111.py",
        "2,1,1,1,1,1,1,1",
        147,
        363,
        28,
        164103,
        719,
        "f9ab4206a3f6657068e4f8e23622eb8a"
        "6195439a0f4f32fd9c6bfe91939d8a04",
    ),
    (
        "cegis_dim9_profile_2211111.py",
        "2,2,1,1,1,1,1",
        152,
        386,
        21,
        137682,
        745,
        "ce150591bbb66d3b03faf32f51dc1a64"
        "deda79d67147a50598d5ca82918bcb9c",
    ),
    (
        "cegis_dim9_profile_3111111.py",
        "3,1,1,1,1,1,1",
        164,
        500,
        21,
        176412,
        883,
        "d7838ce3a4e12d19db07ee136e087cb0"
        "ef889c890d0c2f7f5d380e8113c1d5bc",
    ),
)


class RemainingDimensionNineProfilesRegression(unittest.TestCase):
    def test_iteration_zero_unsat_certificates(self) -> None:
        if shutil.which("z3") is None:
            self.skipTest("z3 is not installed")
        for (
            script_name,
            profile,
            structure_variables,
            associativity,
            surjectivity,
            byte_count,
            line_count,
            digest,
        ) in CASES:
            with self.subTest(profile=profile):
                with tempfile.TemporaryDirectory() as directory:
                    certificate_directory = Path(directory) / "certificates"
                    completed = subprocess.run(
                        [
                            "python3",
                            str(DIRECTORY / script_name),
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
                    f"CEGIS_START|profile={profile}"
                    f"|structure_variables={structure_variables}"
                    f"|associativity={associativity}"
                    f"|surjectivity={surjectivity}"
                    "|relevant_dimension=7|cube_inputs=2187"
                    "|witness_variables=14",
                    completed.stdout,
                )
                self.assertIn(
                    "CEGIS_UNSAT|iteration=0|root_constraints=0",
                    completed.stdout,
                )
                self.assertTrue(completed.stdout.rstrip().endswith("DONE"))
                self.assertEqual(len(certificate_bytes), byte_count)
                self.assertEqual(
                    certificate_bytes.count(b"\n"), line_count
                )
                self.assertEqual(
                    hashlib.sha256(certificate_bytes).hexdigest(), digest
                )


if __name__ == "__main__":
    unittest.main()
