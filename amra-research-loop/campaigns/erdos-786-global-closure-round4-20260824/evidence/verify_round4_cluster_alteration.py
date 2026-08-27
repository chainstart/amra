#!/usr/bin/env python3
"""Finite guards for the projective-plane failure-cluster obstruction.

These checks corroborate the incidence and cover identities only.  The
all-K prime allocation, arithmetic path realization, and padding bounds are
proved symbolically in ROUND4_CLUSTER_ALTERATION.md.
"""

from __future__ import annotations

import json
from hashlib import sha256
from itertools import combinations
from pathlib import Path


Point = tuple[str, int, int] | tuple[str, int]


def plane(q: int) -> tuple[list[Point], list[frozenset[Point]]]:
    affine: list[Point] = [("a", x, y) for x in range(q) for y in range(q)]
    infinity: list[Point] = [("i", slope) for slope in range(q)] + [("v", 0)]
    points = affine + infinity
    lines: list[frozenset[Point]] = []
    for slope in range(q):
        for intercept in range(q):
            row = {("a", x, (slope * x + intercept) % q) for x in range(q)}
            row.add(("i", slope))
            lines.append(frozenset(row))
    for x in range(q):
        row = {("a", x, y) for y in range(q)}
        row.add(("v", 0))
        lines.append(frozenset(row))
    lines.append(frozenset(infinity))
    return points, lines


def check_order(q: int) -> dict[str, int]:
    points, lines = plane(q)
    expected = q * q + q + 1
    assert len(points) == len(lines) == expected
    assert all(len(line) == q + 1 for line in lines)
    for left, right in combinations(lines, 2):
        assert len(left & right) == 1
    point_degrees = {point: sum(point in line for line in lines) for point in points}
    assert set(point_degrees.values()) == {q + 1}

    # Abstract circuit supports add line-private vertices to the point roots.
    supports = []
    for index, line in enumerate(lines):
        private = {("private", index, slot) for slot in range(q + 2)}
        supports.append(set(line) | private)
    for left, right in combinations(supports, 2):
        assert len(left & right) == 1

    # Exact lower-bound count for every choice of at most q shared points and
    # arbitrary remaining line-private repairs.
    minimum = expected
    for size in range(q + 2):
        for chosen in combinations(points, size):
            covered = {i for i, line in enumerate(lines) if set(chosen) & line}
            cost = size + (expected - len(covered))
            minimum = min(minimum, cost)
    assert minimum == q + 1

    # Any fixed projective line is a cover by shared points.
    cover = set(lines[0])
    assert len(cover) == q + 1
    assert all(cover & line for line in lines)
    return {
        "q": q,
        "points": expected,
        "circuits": expected,
        "packing_number": 1,
        "transversal_number": minimum,
    }


def main() -> None:
    payload = {
        "status": "PASS",
        "orders": [check_order(q) for q in (2, 3, 5)],
        "scope": (
            "finite incidence and cover guards only; no finite-to-asymptotic "
            "inference is used"
        ),
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
