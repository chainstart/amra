#!/usr/bin/env python3
"""Exact guards for ROUND3_MULTISCALE_CARRY.md.

Finite loops are corroborative only.  The infinite dyadic counterfamily is
proved symbolically in the accompanying note by the base inequality and the
binomial ratio bound.
"""

from __future__ import annotations

import importlib.util
import json
from hashlib import sha256
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "verify_rank8_obstructions.py"
SPEC = importlib.util.spec_from_file_location("rank8_guard", SOURCE)
assert SPEC is not None and SPEC.loader is not None
RANK8 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RANK8)


def first_tax_checks() -> dict[str, object]:
    checked = []
    for v in (40, 41, 64, 100, 128, 256, 512):
        first_only = RANK8.shadow_to_rank8(v, v - 13)
        baseline = comb(v - 12, 8) + comb(v - 13, 7)
        assert first_only == baseline
        checked.append(v)
    return {
        "parameters": checked,
        "identity": "iterated first-tax shadow = C(V-12,8)+C(V-13,7)",
        "scope": "finite guard for the all-V hockey-stick proof",
    }


def actual_floor_checks() -> dict[str, object]:
    checked = []
    for v in (40, 41, 50, 64, 100, 128, 256, 512):
        w6 = int(RANK8.rank8_row(v)["W6"])
        assert w6 >= v
        checked.append({"V": v, "W6": w6})
    return {
        "rows": checked,
        "scope": "finite guard; the universal W6>=V proof uses KK monotonicity",
    }


def canonical_top_checks() -> dict[str, object]:
    cases = 0
    for top in range(6, 25):
        threshold = comb(top + 1, 6)
        for x in (comb(top, 6), threshold - 1):
            word = RANK8.canonical(x, 6)
            assert word and word[0][0] <= top
            cases += 1
        word = RANK8.canonical(threshold, 6)
        assert word[0][0] == top + 1
        cases += 1
    return {
        "cases": cases,
        "identity": "top<=B iff x<C(B+1,6) for positive six-canonical x",
        "scope": "finite guard for the defining combinadic interval",
    }


def dyadic_guard() -> dict[str, object]:
    m = 21
    power = 2**m
    cap = comb(m + 14, 6)
    assert power > cap
    assert m + 15 < 2 * (m + 9)
    return {
        "base_m": m,
        "two_to_m": power,
        "binomial": cap,
        "gap": power - cap,
        "induction": "C(m+15,6)/C(m+14,6)=(m+15)/(m+9)<2 for all m>=21",
    }


def main() -> None:
    payload = {
        "status": "PASS",
        "first_tax": first_tax_checks(),
        "actual_floor": actual_floor_checks(),
        "canonical_top": canonical_top_checks(),
        "dyadic_counterfamily": dyadic_guard(),
        "classification": "M776G-02 refuted by a symbolic infinite actual-orbit family; no finite-to-infinite inference",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
