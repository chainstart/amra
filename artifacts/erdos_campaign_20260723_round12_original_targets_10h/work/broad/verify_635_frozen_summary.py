#!/usr/bin/env python3
"""Recompute the full fixed-A=2 audit and check the frozen compact JSON."""

from __future__ import annotations

import json
from pathlib import Path

import verify_635_fixed_A2_cycles as audit


def main() -> None:
    root = Path(__file__).resolve().parent
    frozen = json.loads((root / "verify_635_fixed_A2_cycles.json").read_text())
    audits = [audit.audit_length(length) for length in range(2, audit.MAX_LENGTH + 1)]

    counts = {str(item["length"]): item["multiplier_tuples"] for item in audits}
    nonbacktracking = {
        str(item["length"]): item["nonbacktracking_candidates"] for item in audits
    }
    closed_walks = {item["length"]: item["prime_closed_walks"] for item in audits}

    assert frozen["status"] == "PASS"
    assert frozen["A"] == audit.A
    assert frozen["complete_lengths"] == [2, audit.MAX_LENGTH]
    assert frozen["multiplier_tuple_counts"] == counts
    assert frozen["nonbacktracking_candidates_by_length"] == nonbacktracking
    for length, walks in closed_walks.items():
        assert len(walks) == (2 if length % 2 == 0 else 0)
        assert all(item["immediate_return"] for item in walks)
        assert all(not item["valid_distinct_prime_edges"] or item["immediate_return"] for item in walks)

    print("PASS: frozen fixed-A=2 summary matches a fresh complete enumeration")


if __name__ == "__main__":
    main()
