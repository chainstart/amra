#!/usr/bin/env python3
"""Regression checks for the closure-free dimension-nine core."""

from __future__ import annotations

import shutil
import unittest

from humanize_dim9_profile_222111 import build_groups, solve


class HumanizedProfile222111Test(unittest.TestCase):
    def test_group_ledger(self) -> None:
        groups, ledger = build_groups()
        self.assertEqual(ledger["structure_variables"], 140)
        self.assertEqual(len(groups["all_associativity"]), 276)
        self.assertEqual(len(groups["leading_associativity"]), 156)
        self.assertEqual(len(groups["surjectivity"]), 15)
        self.assertEqual(len(groups["projection_bijection"]), 36)
        self.assertEqual(len(groups["closure_equations"]), 9)

    @unittest.skipUnless(shutil.which("z3"), "z3 is required")
    def test_grouped_core_is_closure_free(self) -> None:
        groups, _ = build_groups()

        def query(*names):
            return [
                line for name in names for line in groups[name]
            ]

        self.assertEqual(
            solve(
                "z3",
                query(
                    "domain",
                    "leading_associativity",
                    "noncommuting",
                ),
                30,
            ),
            "unsat",
        )
        self.assertEqual(
            solve("z3", query("domain", "noncommuting"), 10),
            "sat",
        )
        self.assertEqual(
            solve(
                "z3",
                query("domain", "leading_associativity"),
                10,
            ),
            "sat",
        )


if __name__ == "__main__":
    unittest.main()
