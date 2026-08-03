#!/usr/bin/env python3
"""Bounded replay of the round-three far domain through ranks seven/eight."""

from importlib.util import module_from_spec, spec_from_file_location
from math import comb, isqrt
from pathlib import Path
import hashlib
import json


SOURCE = (Path(__file__).resolve().parents[2]
          / "erdos-776-adaptive-uniformity/evidence/search_c1_two_row_recovery.py")
spec = spec_from_file_location("c1_source_round4", SOURCE)
c1 = module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(c1)


def main() -> None:
    scales = [56, 60, 64, 80, 100, 120]
    double6 = negative7 = negative8 = 0
    borrow7 = borrow8 = 0
    minimum7 = minimum8 = None
    first_negative7 = []
    for j in scales:
        h = 112 * (1 << (j - 1))
        for k in range(2, 81):
            step = k - 1
            base = 2 * h - comb(k - 1, 2) - 2
            residue = (-base) % step
            rs = set(range(residue, 1001, step))
            q0 = max(0, base // step)
            wall = isqrt(max(0, 2 * k * q0 + k * (k - 1)))
            wall_index = round((wall - residue) / step)
            for offset in range(-8, 9):
                r = residue + (wall_index + offset) * step
                if r >= 0:
                    rs.add(r)
            for r in rs:
                row = c1.candidate(j, k, r)
                if (row is None or row["transition"] != "-- -> ++"
                        or row["gamma5"] >= 0 or row["gamma6"] is None
                        or row["gamma6"] >= 0):
                    continue
                double6 += 1
                P, V, tau = row["P"], row["V"], row["tau"]
                X = c1.upper(P, 4) - tau + 1
                Y = c1.upper(V, 4) - tau
                if min(X, Y) < 0:
                    borrow7 += 1
                    continue
                gamma7 = c1.upper(Y, 5) - c1.upper(X, 5) - c1.upper(P, 4) - 1
                enriched = {**row, "X": X, "Y": Y, "gamma7": gamma7}
                if minimum7 is None or gamma7 < minimum7["gamma7"]:
                    minimum7 = enriched
                if gamma7 >= 0:
                    continue
                negative7 += 1
                if len(first_negative7) < 5:
                    first_negative7.append(enriched)
                R = c1.upper(X, 5) - tau + 1
                S = c1.upper(Y, 5) - tau
                if min(R, S) < 0:
                    borrow8 += 1
                    continue
                gamma8 = c1.upper(S, 6) - c1.upper(R, 6) - c1.upper(X, 5) - 1
                enriched8 = {**enriched, "R": R, "S": S, "gamma8": gamma8}
                if minimum8 is None or gamma8 < minimum8["gamma8"]:
                    minimum8 = enriched8
                if gamma8 < 0:
                    negative8 += 1

    result = {
        "schema": "amra.erdos776.adaptive-round4.far-rank7-rank8-probe.v1",
        "domain": {"j": scales, "k": [2, 80],
                   "r": "compatible r<=1000 plus 17 first-tail-wall probes"},
        "gamma5_gamma6_double_negative": double6,
        "rank7_borrow": borrow7,
        "gamma7_negative": negative7,
        "rank8_borrow_among_gamma7_negative": borrow8,
        "gamma8_negative": negative8,
        "minimum_gamma7": minimum7,
        "minimum_gamma8_on_gamma7_negative": minimum8,
        "first_gamma7_negative": first_negative7,
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope_warning": "finite mechanism falsification only; absence of gamma8 failures is not a theorem",
    }
    assert double6 == 2304
    assert borrow7 == 0 and negative7 == 30
    assert borrow8 == 0 and negative8 == 0
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
