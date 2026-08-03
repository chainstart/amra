#!/usr/bin/env python3
"""Far-scale actual-lattice falsifier for M304 and later recovery."""

from importlib.util import module_from_spec, spec_from_file_location
from math import comb, isqrt
from pathlib import Path
import hashlib
import json


SOURCE = (Path(__file__).resolve().parents[2]
          / "erdos-776-adaptive-uniformity/evidence/search_c1_two_row_recovery.py")
spec = spec_from_file_location("c1_source", SOURCE)
c1 = module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(c1)


def main() -> None:
    scales = [56, 60, 64, 80, 100, 120]
    tested = accepted = negative5 = 0
    borrowed = []
    negative6 = 0
    minimum6 = None
    maximum_coordinates = {"j": 0, "k": 0, "r": 0}
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
                tested += 1
                row = c1.candidate(j, k, r)
                if row is None or row["transition"] != "-- -> ++":
                    continue
                accepted += 1
                if row["gamma5"] >= 0:
                    continue
                negative5 += 1
                maximum_coordinates = {
                    "j": max(maximum_coordinates["j"], j),
                    "k": max(maximum_coordinates["k"], k),
                    "r": max(maximum_coordinates["r"], r),
                }
                if row["gamma6"] is None:
                    if len(borrowed) < 3:
                        borrowed.append(row)
                else:
                    if minimum6 is None or row["gamma6"] < minimum6["gamma6"]:
                        minimum6 = row
                    if row["gamma6"] < 0:
                        negative6 += 1

    print(json.dumps({
        "schema": "amra.erdos776.round3-far-negative-rank6-wall-probe.v1",
        "domain": {"j": scales,
                   "k": [2, 80],
                   "r": "all compatible r<=1000 plus 17 probes around the first-tail wall"},
        "tested_parameter_triples": tested,
        "accepted_final_chamber_states": accepted,
        "gamma5_negative_states": negative5,
        "maximum_negative_coordinates": maximum_coordinates,
        "negative_gamma5_with_rank6_borrow_count": len(borrowed),
        "first_borrowed_negative_gamma5": borrowed,
        "gamma5_gamma6_double_negative_states": negative6,
        "minimum_gamma6": minimum6,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "classification": "finite exact far-scale falsifier only",
        "public_problem_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
