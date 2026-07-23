#!/usr/bin/env python3
"""Exact finite checks for exponent-vector routes to Erdős problem #536.

Pairwise LCM equality for three integers becomes equality of the three
coordinatewise joins of their prime-exponent vectors.  The checks below:

* reproduce the exact extremal size 2k+1 in the two-prime box [0,k]^2 for
  k <= 3; and
* show that the naive three-prime generalisation "inject into the
  one-dimensional skeleton" is false already in {0,1}^3.

This is an obstruction certificate, not an asymptotic result.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


Point = tuple[int, ...]


def is_lcm_triangle(points: tuple[Point, Point, Point]) -> bool:
    left, middle, right = points
    if len({left, middle, right}) != 3:
        return False
    dimension = len(left)
    return all(
        max(left[index], middle[index])
        == max(left[index], right[index])
        == max(middle[index], right[index])
        for index in range(dimension)
    )


def hyperedges(vertices: list[Point]) -> list[int]:
    result: list[int] = []
    for indices in itertools.combinations(range(len(vertices)), 3):
        triple = tuple(vertices[index] for index in indices)
        if is_lcm_triangle(triple):
            mask = sum(1 << index for index in indices)
            result.append(mask)
    return result


def exact_independence_number(vertices: list[Point]) -> tuple[int, list[Point]]:
    edges = hyperedges(vertices)
    best_mask = 0
    best_size = 0
    for mask in range(1 << len(vertices)):
        size = mask.bit_count()
        if size <= best_size:
            continue
        if any(mask & edge == edge for edge in edges):
            continue
        best_mask = mask
        best_size = size
    witness = [
        vertex for index, vertex in enumerate(vertices) if best_mask & (1 << index)
    ]
    return best_size, witness


def verify() -> dict[str, object]:
    two_prime_rows: list[dict[str, object]] = []
    for side in range(1, 4):
        vertices = list(itertools.product(range(side + 1), repeat=2))
        maximum, witness = exact_independence_number(vertices)
        two_prime_rows.append(
            {
                "box": f"[0,{side}]^2",
                "vertex_count": len(vertices),
                "hyperedge_count": len(hyperedges(vertices)),
                "independence_number": maximum,
                "axis_count": 2 * side + 1,
                "matches_axis_bound": maximum == 2 * side + 1,
                "witness": witness,
            }
        )

    cube = list(itertools.product(range(2), repeat=3))
    cube_maximum, cube_witness = exact_independence_number(cube)
    one_skeleton = [point for point in cube if sum(value > 0 for value in point) <= 1]
    cube_witness_is_independent = not any(
        is_lcm_triangle(triple)
        for triple in itertools.combinations(cube_witness, 3)
    )
    passed = (
        all(bool(row["matches_axis_bound"]) for row in two_prime_rows)
        and cube_maximum == 5
        and len(one_skeleton) == 4
        and cube_witness_is_independent
    )
    return {
        "schema_version": "amra.erdos536.exponent_obstruction.v1",
        "problem_id": "536",
        "two_prime_boxes": two_prime_rows,
        "three_prime_binary_cube": {
            "vertex_count": len(cube),
            "hyperedge_count": len(hyperedges(cube)),
            "independence_number": cube_maximum,
            "one_skeleton_size": len(one_skeleton),
            "one_skeleton_injection_false": cube_maximum > len(one_skeleton),
            "witness": cube_witness,
            "integer_witness_for_primes_2_3_5": [
                2 ** point[0] * 3 ** point[1] * 5 ** point[2]
                for point in cube_witness
            ],
        },
        "passed": passed,
        "scope_note": (
            "The certificate rules out one naive higher-dimensional projection. "
            "It neither improves the 5/6 bound nor proves f(N)=o(N)."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = verify()
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
