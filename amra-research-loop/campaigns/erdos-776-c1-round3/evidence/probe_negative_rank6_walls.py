#!/usr/bin/env python3
"""Targeted finite falsifier for the c=1 rank-six survivor pair.

This deliberately samples actual residue-compatible points, not relaxed
tuples.  It is finite evidence only; it cannot prove either survivor.
"""

from importlib.util import module_from_spec, spec_from_file_location
from math import comb, isqrt
from pathlib import Path
import json


SOURCE = (Path(__file__).resolve().parents[2]
          / "erdos-776-adaptive-uniformity/evidence/search_c1_two_row_recovery.py")
spec = spec_from_file_location("c1_source", SOURCE)
source = module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(source)


def k_values(h: int) -> list[int]:
    values = set(range(2, 401))
    root = isqrt(2 * h)
    for numerator, denominator in [(1, 8), (1, 4), (1, 2), (1, 1), (3, 2)]:
        center = max(2, numerator * root // denominator)
        values.update(range(max(2, center - 12), center + 13))
    for power in range(9, 16):
        values.add(1 << power)
    return sorted(k for k in values if comb(k - 1, 2) < 2 * h)


def main() -> None:
    tested = 0
    accepted = 0
    negative5 = 0
    borrowed_negative5 = []
    double_negative = []
    minimum_gamma6 = None
    widest = {"k": 0, "r": 0}

    for j in range(15, 56):
        h = 112 * (1 << (j - 1))
        for k in k_values(h):
            step = k - 1
            base = 2 * h - comb(k - 1, 2) - 2
            residue = (-base) % step
            rs = set(range(residue, 10001, step))

            q0 = max(0, base // step)
            first_tail_wall = isqrt(max(0, 2 * k * q0 + k * (k - 1)))
            wall_index = round((first_tail_wall - residue) / step)
            for offset in range(-40, 41):
                r = residue + (wall_index + offset) * step
                if r >= 0:
                    rs.add(r)

            for r in rs:
                tested += 1
                row = source.candidate(j, k, r)
                if row is None or row["transition"] != "-- -> ++":
                    continue
                accepted += 1
                if row["gamma5"] >= 0:
                    continue
                negative5 += 1
                widest["k"] = max(widest["k"], row["k"])
                widest["r"] = max(widest["r"], row["r"])
                if row["gamma6"] is None:
                    if len(borrowed_negative5) < 3:
                        borrowed_negative5.append(row)
                else:
                    if minimum_gamma6 is None or row["gamma6"] < minimum_gamma6["gamma6"]:
                        minimum_gamma6 = row
                    if row["gamma6"] < 0 and len(double_negative) < 3:
                        double_negative.append(row)

    print(json.dumps({
        "schema": "amra.erdos776.round3-negative-rank6-wall-probe.v1",
        "domain": {
            "j": [15, 55],
            "k": "2..400 plus neighborhoods of sqrt(2h)/8, /4, /2, 1, 3/2 and powers of two",
            "r": "all compatible r<=10000 plus 81 compatible probes around the first-tail wall",
            "tested_parameter_triples": tested,
        },
        "accepted_final_chamber_states": accepted,
        "gamma5_negative_states": negative5,
        "largest_negative_coordinates": widest,
        "negative_gamma5_with_rank6_borrow_count": len(borrowed_negative5),
        "first_borrowed_negative_gamma5": borrowed_negative5,
        "negative_gamma5_and_gamma6_count": len(double_negative),
        "first_double_negative": double_negative,
        "minimum_gamma6_on_tested_negative_branch": minimum_gamma6,
        "interpretation": "A counterexample would kill M304 or M305. Absence is finite falsification evidence only.",
        "public_problem_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
