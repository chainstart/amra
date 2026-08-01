#!/usr/bin/env python3
"""Finite guards for the #809 matching-rectangle transference theorem.

The objects here are abstract colour rectangles carried by a matching of
zero-shore pairs.  For every shared A-coordinate we materialize the B-side
complete missing rectangle forced by the zero-shore argument.  The script
checks the exact incidence identities and all displayed capacity bounds;
it is not a proof of the graph-theoretic theorem or of Erdős #809.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt
import random


@dataclass(frozen=True)
class Rectangle:
    left: frozenset[int]
    right: frozenset[int]

    def __post_init__(self) -> None:
        if len(self.left) != len(self.right):
            raise ValueError("rectangle sides must have equal size")
        if self.left & self.right:
            raise ValueError("rectangle sides must be disjoint")

    @property
    def height(self) -> int:
        return len(self.left)


def unordered_pair(x: int, y: int) -> tuple[int, int]:
    if x == y:
        raise ValueError("pair endpoints must be distinct")
    return (x, y) if x < y else (y, x)


def endpoint_pair(
    x: tuple[int, int], y: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    if x == y:
        raise ValueError("B endpoints must be distinct")
    return (x, y) if x < y else (y, x)


def audit(rectangles: list[Rectangle], a_size: int) -> dict[str, int]:
    """Audit a matching-indexed family of A-side rectangles.

    B endpoints are represented by (0,i) and (1,i).  Whenever an
    A-coordinate occurs in rectangle i, the theorem forces every cross
    pair between the two endpoint classes of all such i to be missing.
    Their union is a certified subset of the global reserve union Q.
    """

    coordinate_support: dict[int, set[int]] = {a: set() for a in range(a_size)}
    coordinate_side: dict[tuple[int, int], int] = {}
    pair_support: dict[tuple[int, int], set[int]] = {}
    for i, rectangle in enumerate(rectangles):
        for a in rectangle.left:
            coordinate_support[a].add(i)
            coordinate_side[(a, i)] = 0
        for a in rectangle.right:
            coordinate_support[a].add(i)
            coordinate_side[(a, i)] = 1
        for x in rectangle.left:
            for y in rectangle.right:
                pair_support.setdefault(unordered_pair(x, y), set()).add(i)

    forced_q: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for a, support in coordinate_support.items():
        for i in support:
            for j in support:
                # Reorient pair i independently for this anchor.  Its
                # U endpoint is the side incident with a, and its V
                # endpoint is the opposite side.
                u_i = (coordinate_side[(a, i)], i)
                v_j = (1 - coordinate_side[(a, j)], j)
                forced_q.add(endpoint_pair(u_i, v_j))

    q_size = len(forced_q)
    heights = [rectangle.height for rectangle in rectangles]
    total_h = sum(heights)
    square_h = sum(h * h for h in heights)
    m_a = len(pair_support)
    f = len(rectangles)
    max_coordinate_overlap = max((len(s) for s in coordinate_support.values()), default=0)
    max_pair_overlap = max((len(s) for s in pair_support.values()), default=0)

    assert sum(len(s) for s in coordinate_support.values()) == 2 * total_h
    assert sum(len(s) for s in pair_support.values()) == square_h
    assert max_coordinate_overlap * max_coordinate_overlap <= q_size
    assert max_pair_overlap * max_pair_overlap <= q_size
    assert 2 * total_h <= a_size * isqrt(q_size)
    assert square_h <= m_a * isqrt(q_size)
    if f:
        assert total_h * total_h <= f * square_h
        assert total_h * total_h <= f * m_a * isqrt(q_size)

    return {
        "rectangles": f,
        "a_size": a_size,
        "M_A": m_a,
        "Q": q_size,
        "sum_h": total_h,
        "sum_h2": square_h,
        "max_coordinate_overlap": max_coordinate_overlap,
        "max_pair_overlap": max_pair_overlap,
    }


def deterministic_audits() -> list[dict[str, int]]:
    systems = [
        [Rectangle(frozenset({0, 1}), frozenset({2, 3}))],
        [
            Rectangle(frozenset({0, 1}), frozenset({2, 3})),
            Rectangle(frozenset({0, 4}), frozenset({2, 5})),
            # The common missing pair {0,2} appears with the reverse
            # initial orientation.  The proof is allowed to reorient it.
            Rectangle(frozenset({2, 6}), frozenset({0, 7})),
        ],
        [
            Rectangle(frozenset({0, 1, 2}), frozenset({3, 4, 5})),
            Rectangle(frozenset({0, 1, 6}), frozenset({3, 4, 7})),
            Rectangle(frozenset({0, 2, 6}), frozenset({3, 5, 7})),
            Rectangle(frozenset({1, 2, 6}), frozenset({4, 5, 7})),
        ],
        [
            # Anchor 1 occurs on opposite sides.  The literal
            # anchor-dependent union has six B-edges; a fixed global
            # orientation would materialize only four.
            Rectangle(frozenset({0}), frozenset({1})),
            Rectangle(frozenset({0, 1}), frozenset({2, 3})),
        ],
    ]
    reports = [audit(system, 8) for system in systems]
    assert reports[-1]["Q"] == 6
    return reports


def random_audits(seed: int = 809_31, trials: int = 2000) -> int:
    rng = random.Random(seed)
    for _ in range(trials):
        a_size = rng.randint(4, 14)
        f = rng.randint(1, 10)
        rectangles: list[Rectangle] = []
        for _i in range(f):
            h = rng.randint(1, a_size // 2)
            chosen = rng.sample(range(a_size), 2 * h)
            rng.shuffle(chosen)
            rectangles.append(
                Rectangle(frozenset(chosen[:h]), frozenset(chosen[h:]))
            )
        audit(rectangles, a_size)
    return trials


def main() -> None:
    deterministic = deterministic_audits()
    random_count = random_audits()
    print(
        {
            "schema": "amra.erdos809.matching-rectangle-transference.v1",
            "deterministic_systems": len(deterministic),
            "random_systems": random_count,
            "reverse_orientation_guard": True,
            "status": "PASS",
            "scope": "finite incidence guards only; Erdos #809 remains open",
        }
    )


if __name__ == "__main__":
    main()
