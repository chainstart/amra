#!/usr/bin/env python3
"""Exact guard for the Ramsey-palette transfer test on #809 sharp graphs.

The certificate is deliberately self-contained.  It rebuilds the cyclic
sharp endpoint graphs instead of importing the earlier six-hour verifier.
"""

from __future__ import annotations

import argparse
import json
from collections import deque


def choose2(value: int) -> int:
    return value * (value - 1) // 2


def matching_outer_label_words(edge_count: int) -> set[tuple[int, ...]]:
    """Enumerate outer words of all proper labels of an oriented matching."""
    if edge_count < 0:
        raise ValueError("edge_count must be nonnegative")
    words: set[tuple[int, ...]] = set()
    for mask in range(1 << edge_count):
        outer = tuple((mask >> index) & 1 for index in range(edge_count))
        inner = tuple(1 - label for label in outer)
        assert all(left != right for left, right in zip(inner, outer, strict=True))
        words.add(outer)
    assert len(words) == 1 << edge_count
    return words


def distance(
    neighbours: list[set[int]], source: int, target: int
) -> int:
    """Return the ordinary graph distance (the constructed graph is connected)."""
    queue = deque([(source, 0)])
    seen = {source}
    while queue:
        vertex, depth = queue.popleft()
        if vertex == target:
            return depth
        for nxt in neighbours[vertex] - seen:
            seen.add(nxt)
            queue.append((nxt, depth + 1))
    raise AssertionError("sharp graph unexpectedly disconnected")


def sharp_palette_row(g: int, parity: str) -> dict[str, int | str | bool]:
    if g < 4 or parity not in {"even", "odd"}:
        raise ValueError("requires g>=4 and parity even/odd")

    is_even = parity == "even"
    delta = g * g - 2 * g - (2 if is_even else 1)
    kappa = 2 * g - (2 if is_even else 1)
    maximum = delta + g
    n = 2 * delta + kappa

    b, c = 0, 1
    pset = list(range(2, 2 + delta))
    uset = list(range(2 + delta, 2 + 2 * delta))
    wset = list(range(2 + 2 * delta, n))
    edges: set[tuple[int, int]] = set()

    def edge(x: int, y: int) -> tuple[int, int]:
        assert x != y
        return min(x, y), max(x, y)

    def add_edge(x: int, y: int) -> None:
        edges.add(edge(x, y))

    for index, x in enumerate(pset):
        add_edge(b, x)
        for y in pset[index + 1 :]:
            add_edge(x, y)
    for index, x in enumerate(uset):
        add_edge(c, x)
        for y in uset[index + 1 :]:
            add_edge(x, y)

    right = pset + uset
    for index, x in enumerate(wset):
        for offset in range(maximum):
            add_edge(x, right[(index * maximum + offset) % len(right)])

    neighbours = [set() for _ in range(n)]
    for x, y in edges:
        neighbours[x].add(y)
        neighbours[y].add(x)
    degrees = [len(row) for row in neighbours]

    assert len(edges) == n * n // 4 + 1
    assert min(degrees) == delta
    assert max(degrees) == maximum
    assert neighbours[b] == set(pset)
    assert neighbours[c] == set(uset)
    assert all(edge(x, y) not in edges for x in pset for y in uset)

    # Freeze one maximum witness and choose g supports on each shore.
    witness = wset[0]
    aset = {witness} | neighbours[witness]
    bset = set(range(n)) - aset
    p_support = sorted(aset & set(pset))[:g]
    u_support = sorted(aset & set(uset))[:g]
    assert len(p_support) == len(u_support) == g

    repeated_classes: list[set[tuple[int, int]]] = []
    label_classes: list[tuple[set[int], set[int]]] = []
    repeated_edges: set[tuple[int, int]] = set()
    for x, y in zip(p_support, u_support, strict=True):
        colour_class = {edge(b, x), edge(c, y)}
        assert len(colour_class) == 2
        assert not repeated_edges & colour_class
        repeated_edges |= colour_class
        repeated_classes.append(colour_class)

        # This is an explicit proper two-labeling of the colour graph 2K2.
        zero_label = {b, c}
        one_label = {x, y}
        assert zero_label.isdisjoint(one_label)
        assert all(
            (left in zero_label and right in one_label)
            or (right in zero_label and left in one_label)
            for left, right in colour_class
        )
        label_classes.append((zero_label, one_label))

        # Removing the two equal-colour edges from a putative C7 leaves
        # one of two path pairings with total length five.  The shortest
        # distances in either pairing already total at least six.
        direct_pairing = distance(neighbours, b, c) + distance(
            neighbours, x, y
        )
        crossed_pairing = distance(neighbours, b, y) + distance(
            neighbours, x, c
        )
        assert direct_pairing >= 6
        assert crossed_pairing >= 6

    # Every non-repeated edge receives a fresh colour.  Consequently all
    # colour graphs have chromatic number at most two, maximum degree one,
    # and degeneracy one.  The exact number of colour savings is g.
    colour_count = len(edges) - g
    defect = sum(len(colour_class) - 1 for colour_class in repeated_classes)
    assert defect == g

    # The actual missing-star reserve in B is independent of how the g
    # supports were paired.  Enumerating it supplies a literal injection
    # from repeated colour classes to distinct reserve tokens.
    reserve = {
        edge(center, vertex)
        for center in (b, c)
        for vertex in bset - {center}
        if edge(center, vertex) not in edges
    }
    reserve_formula = delta + 2 * kappa - g - 5
    assert len(reserve) == reserve_formula
    assert len(reserve) >= g
    reserve_tokens = sorted(reserve)[:g]
    palette_reserve_injection = dict(enumerate(reserve_tokens))
    assert len(palette_reserve_injection) == g
    assert len(set(palette_reserve_injection.values())) == g

    return {
        "g": g,
        "parity": parity,
        "n": n,
        "edges": len(edges),
        "delta": delta,
        "maximum": maximum,
        "repeated_classes": len(repeated_classes),
        "largest_colour_class": 2,
        "maximum_colour_degree": 1,
        "maximum_colour_chromatic_number": 2,
        "maximum_colour_degeneracy": 1,
        "defect": defect,
        "colours": colour_count,
        "reserve": len(reserve),
        "injected_reserve_tokens": len(palette_reserve_injection),
        "pass": True,
    }


def certificate(max_g: int = 20) -> dict[str, int | bool]:
    rows = 0
    vertices = 0
    edges = 0
    repeated_classes = 0
    reserve_tokens = 0
    gauge_words = 0
    for edge_count in range(11):
        gauge_words += len(matching_outer_label_words(edge_count))
    for g in range(4, max_g + 1):
        for parity in ("even", "odd"):
            row = sharp_palette_row(g, parity)
            assert row["pass"]
            rows += 1
            vertices += int(row["n"])
            edges += int(row["edges"])
            repeated_classes += int(row["repeated_classes"])
            reserve_tokens += int(row["injected_reserve_tokens"])
    return {
        "max_g": max_g,
        "parameter_rows": rows,
        "vertices_rebuilt": vertices,
        "edges_rebuilt": edges,
        "repeated_classes_checked": repeated_classes,
        "reserve_injections_checked": reserve_tokens,
        "matching_gauge_words_checked": gauge_words,
        "pass": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-g", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(certificate(args.max_g), sort_keys=True))


if __name__ == "__main__":
    main()
