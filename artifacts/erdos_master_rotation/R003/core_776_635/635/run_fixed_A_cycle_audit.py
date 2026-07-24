#!/usr/bin/env python3
"""Compile and run the complete R003 fixed-(A,length) cycle audits."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


EXPECTED = {
    (4, 2): (18, 7, 2, 2, 0),
    (4, 3): (188, 28, 3, 3, 0),
    (4, 4): (2_150, 103, 2, 2, 0),
    (4, 5): (25_137, 176, 0, 0, 0),
    (4, 6): (309_132, 4_840, 5, 5, 0),
    (4, 7): (3_806_784, 414, 0, 0, 0),
    (4, 8): (47_516_534, 5_391, 2, 2, 0),
    (4, 9): (599_502_248, 121_114, 3, 3, 0),
    (8, 2): (92, 11, 4, 4, 0),
    (8, 3): (2_530, 13, 0, 0, 0),
    (8, 4): (76_172, 731, 4, 4, 0),
    (8, 5): (2_346_639, 161, 0, 0, 0),
    (8, 6): (74_270_924, 12_599, 4, 4, 0),
    (16, 2): (456, 17, 4, 4, 0),
    (16, 3): (31_157, 190, 3, 3, 0),
    (16, 4): (2_276_664, 409, 4, 4, 0),
    (32, 2): (2_168, 19, 4, 4, 0),
    (32, 3): (352_210, 40, 3, 3, 0),
    (64, 2): (10_108, 41, 6, 6, 0),
    (64, 3): (3_789_131, 292, 0, 0, 0),
}


def main() -> None:
    source = Path(__file__).with_name("enumerate_fixed_A_cycles.cpp")
    with tempfile.TemporaryDirectory(prefix="erdos635-r003-") as directory:
        executable = Path(directory) / "enumerate"
        subprocess.run(
            ["g++", "-O3", "-std=c++17", str(source), "-o", str(executable)],
            check=True,
        )
        rows = []
        for (a_value, length), expected in EXPECTED.items():
            completed = subprocess.run(
                [str(executable), str(a_value), str(length)],
                check=True,
                text=True,
                capture_output=True,
            )
            row = json.loads(completed.stdout)
            observed = (
                row["multiplier_tuples"],
                row["integral_closed_walks"],
                row["prime_closed_walks"],
                row["immediate_returns"],
                row["nonbacktracking_candidates"],
            )
            assert observed == expected, ((a_value, length), observed, expected)
            rows.append(row)

    total_tuples = sum(row["multiplier_tuples"] for row in rows)
    result = {
        "schema": "amra.erdos635.r003-fixed-A-cycle-audit.v1",
        "status": "PASS",
        "complete_domains": rows,
        "total_multiplier_tuples": total_tuples,
        "all_nonbacktracking_candidates": 0,
        "bicyclic_core_consequence": {
            "A=4": "no fixed-A bicyclic core with at most 9 total edges",
            "A=8": "no fixed-A bicyclic core with at most 6 total edges",
            "A=16": "no fixed-A bicyclic core with at most 4 total edges",
            "A=32": "no fixed-A bicyclic core with at most 3 total edges",
            "A=64": "no fixed-A bicyclic core with at most 3 total edges",
        },
        "scope": (
            "For each listed (A,length), every positive odd multiplier tuple "
            "with product < A^length is enumerated; the two cyclic seeds are "
            "then forced.  This is complete in those finite domains and is "
            "not a theorem for unbounded A or length."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
