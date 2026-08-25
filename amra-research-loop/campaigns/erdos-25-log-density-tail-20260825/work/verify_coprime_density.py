#!/usr/bin/env python3
"""Exact finite CRT replay for the pairwise-coprime subcase of #25."""

from __future__ import annotations

import argparse
import json
import math
import os
from fractions import Fraction
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cases = [
        ([2, 3, 5, 7], [0, 1, 2, 3]),
        ([3, 5, 7, 11], [2, 0, 6, 4]),
        ([5, 7, 11, 13], [4, 1, 8, 2]),
    ]
    rows = []
    for moduli, residues in cases:
        period = math.prod(moduli)
        good = sum(
            all(n % modulus != residue % modulus for modulus, residue in zip(moduli, residues))
            for n in range(period)
        )
        density = Fraction(good, period)
        expected = math.prod((Fraction(modulus - 1, modulus) for modulus in moduli), start=Fraction(1))
        if density != expected:
            raise AssertionError("CRT density product failed")
        rows.append({
            "moduli": moduli,
            "residues": residues,
            "period": period,
            "good_residues": good,
            "density_numerator": density.numerator,
            "density_denominator": density.denominator,
        })
    cgroup = Path("/proc/self/cgroup").read_text().strip()
    payload = {
        "schema_version": "amra.erdos25-coprime-density-replay.v1",
        "claim_scope": "finite replay supporting a separately proved universal coprime theorem",
        "rows": rows,
        "resource_guard": {
            "observed_cgroup": cgroup,
            "inside_openmath_slice": "openmath.slice" in cgroup,
        },
        "pid": os.getpid(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"cases": len(rows), "all_exact": True}))


if __name__ == "__main__":
    main()
