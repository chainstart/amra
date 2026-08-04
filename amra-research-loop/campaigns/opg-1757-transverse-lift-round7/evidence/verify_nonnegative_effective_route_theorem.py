#!/usr/bin/env python3
"""Aggregate exact verifier for all 27 nonnegative-route sign chambers."""

from __future__ import annotations

from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import subprocess


EVIDENCE = Path(__file__).parent
CERTIFICATES = (
    ("nonnegative_route_chambers", "certified_chambers"),
    ("shared_page_discriminant", "nonnegative_route_sign_chambers_added"),
    ("nested_shared_discriminant", "certified_chambers_added"),
    ("opposite_nonshared_chambers", "certified_chambers_added"),
    ("same_side_three_negative", "certified_chambers_added"),
    ("mixed_three_negative", "certified_chambers_added"),
)


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(",", ":"))


def main():
    records = {}
    chamber_sources = {}
    partition = []
    for stem, chamber_key in CERTIFICATES:
        static = json.loads((EVIDENCE / f"{stem}.json").read_text())
        reproduced = json.loads(subprocess.check_output(
            ["python3", str(EVIDENCE / f"verify_{stem}.py")],
            cwd=EVIDENCE.parent,
            text=True,
        ))
        assert reproduced == static
        chambers = static[chamber_key]
        assert len(chambers) == len(set(chambers))
        for chamber in chambers:
            assert chamber not in chamber_sources
            chamber_sources[chamber] = stem
        partition.append({
            "certificate": stem,
            "count": len(chambers),
            "chambers": sorted(chambers),
        })
        records[stem] = {
            "schema": static["schema"],
            "sha256": sha256(canonical(static).encode()).hexdigest(),
        }

    expected = {"".join(state) for state in product("PLR", repeat=3)}
    assert set(chamber_sources) == expected
    assert sum(row["count"] for row in partition) == 27
    print(json.dumps({
        "schema": "amra.opg1757.round7.nonnegative-effective-route-theorem.v1",
        "domain": "q0,q3,q4,c>=0 with positive edge floors",
        "sign_partition": "P=both page activities nonnegative; L/R=left/right activity negative",
        "partition": partition,
        "certified_chambers": sorted(chamber_sources),
        "certified_count": len(chamber_sources),
        "expected_count": len(expected),
        "partition_exact_and_disjoint": True,
        "conclusion": "Delta_b>=0 throughout every nonnegative-effective-route activity-sign chamber",
        "records": records,
        "scope": "complete nonnegative-effective-route theorem only; K-positive cases with one negative diagonal route quantity and the global marked-host theorem remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
