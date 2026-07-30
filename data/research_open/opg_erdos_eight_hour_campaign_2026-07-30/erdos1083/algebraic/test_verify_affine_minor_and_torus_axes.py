#!/usr/bin/env python3
"""Regression for affine-unit minors and norm-torus axis collapse."""

import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name(
    "verify_affine_minor_and_torus_axes.py"
)


class AffineMinorAndTorusAxesRegression(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        completed = subprocess.run(
            ["python3", str(SCRIPT)],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=completed.stdout + completed.stderr,
        )
        self.assertIn(
            "AFFINE_UNIT_MINOR"
            "|node_tests=5"
            "|offsets_per_test=4"
            "|consecutive_degrees=7"
            "|formula=4*abs(M)^(d-2)*abs(a2-a1)"
            "*abs(Vandermonde(a1..a_(d-2)))"
            "|integral_superfactorial_lower_bound=true",
            completed.stdout,
        )
        self.assertIn(
            "NORM_TORUS_AXIS_COLLAPSE"
            "|independent_axes=4"
            "|powers_per_axis=6"
            "|parameters=24"
            "|symmetrized_rows=48"
            "|additive_rank=5"
            "|first_forced_zero_minor_size=6"
            "|status=counterexample_to_rank_only_generalization",
            completed.stdout,
        )
        self.assertIn(
            "BOOLEAN_UNIT_WORD_MINOR"
            "|independent_axes=4"
            "|words=16"
            "|additive_rank=16"
            "|formula=|1-M^2|^(2^(r-1))"
            "*prod_i|B_i|^(2^(r-1))"
            "|status=exact_full_rank_obstruction",
            completed.stdout,
        )
        self.assertIn(
            "BOOLEAN_FAMILY_MINOR"
            "|families=3"
            "|max_words=8"
            "|formula=prod_(S in W)(1+M*(-1)^|S|)"
            "*prod_(i in S)B_i"
            "|all_nonzero=true",
            completed.stdout,
        )
        self.assertIn(
            "SUPPORT_DIVERSE_UNIT_WORD_MINOR"
            "|words=7"
            "|arbitrary_nonnegative_powers=true"
            "|pairwise_distinct_supports=true"
            "|full_row_rank=true",
            completed.stdout,
        )
        self.assertRegex(
            completed.stdout, r"CERTIFICATE\|sha256=[0-9a-f]{64}"
        )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
