#!/usr/bin/env python3
"""Regression checks for the localized dimension-nine solver core."""

from __future__ import annotations

import shutil
import unittest

from humanize_dim9_iteration_zero import (
    ARCHIVED_CORE,
    build_blocks,
    solve,
)


class HumanizedDimensionNineCoreTest(unittest.TestCase):
    @unittest.skipUnless(shutil.which("z3"), "z3 is required")
    def test_archived_core_is_deletion_minimal(self) -> None:
        _, _, _, assertions, background = build_blocks()

        def query(names):
            return background + [assertions[name] for name in names]

        self.assertEqual(
            solve("z3", query(list(ARCHIVED_CORE)), 10), "unsat"
        )
        for removed in ARCHIVED_CORE:
            remaining = [
                name for name in ARCHIVED_CORE if name != removed
            ]
            self.assertEqual(
                solve("z3", query(remaining), 10),
                "sat",
                msg=f"core was still UNSAT after removing {removed}",
            )

    def test_archived_core_ledger(self) -> None:
        self.assertEqual(len(ARCHIVED_CORE), 18)
        self.assertEqual(
            sum(name.startswith("assoc_") for name in ARCHIVED_CORE), 14
        )
        self.assertEqual(
            sum(name.startswith("surj_") for name in ARCHIVED_CORE), 3
        )
        self.assertEqual(ARCHIVED_CORE.count("witness"), 1)


if __name__ == "__main__":
    unittest.main()
