#!/usr/bin/env python3
"""Regression for the dimension-twelve closure-triage ledger."""

import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("triage_dim12_closure_profiles.py")


class DimensionTwelveClosureTriageRegression(unittest.TestCase):
    def test_exact_status_ledger(self) -> None:
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
            "DIM12_CLOSURE_TRIAGE"
            "|frontier_inputs=8"
            "|proved_excluded=3"
            "|human_excluded=2"
            "|finite_audit_excluded=1"
            "|branch_contracts=5"
            "|existence_certificates=0"
            "|status=necessary_conditions_only",
            completed.stdout,
        )
        self.assertEqual(
            completed.stdout.count("DIM12_TRIAGE_CASE|"), 8
        )
        self.assertIn(
            "DIM12_TRIAGE_CASE|profile=2,2,2,2,2,2"
            "|result=excluded_generalized_length6_fibre_lemma",
            completed.stdout,
        )
        self.assertIn(
            "DIM12_TRIAGE_CASE|profile=2,2,2,2,2,1,1"
            "|result=excluded_cross_relation_commutator",
            completed.stdout,
        )
        self.assertIn(
            "DIM12_TRIAGE_CASE|profile=2,2,2,3,1,1,1"
            "|result=excluded_qbijective_d4_bound",
            completed.stdout,
        )
        self.assertTrue(completed.stdout.rstrip().endswith("DONE"))


if __name__ == "__main__":
    unittest.main()
