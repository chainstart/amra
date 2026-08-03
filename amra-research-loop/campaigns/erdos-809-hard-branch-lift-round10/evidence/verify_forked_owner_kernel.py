#!/usr/bin/env python3
"""Complete finite-support verifier for the forked-owner theorem."""

from forked_owner_probe import instance

checked = 0
for m in range(3, 7):
    for r in range(4):
        row = instance(m, r)
        expected = r * (m + 1) + (m - 2) * (m + 3) // 2
        assert row["empty_trace"] is False
        assert set(row["trace_sizes"]) <= {"1", "3", 1, 3}
        assert row["formula_minus_singleton"] == []
        assert row["singleton_minus_formula"] == []
        assert row["formula_count"] == expected
        assert row["singleton_count"] == expected
        assert row["formula_hits_all"]
        assert row["singleton_hits_all"]
        checked += 1

print(f"forked-owner kernel: PASS; support representatives={checked}")
