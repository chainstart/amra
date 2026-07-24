#!/usr/bin/env python3
"""Verify the shared-path identities and their exact gradient collapse."""

from __future__ import annotations

import json
from fractions import Fraction


def oriented_edge(scale: int, p: int, q: int) -> dict[str, object]:
    """Orient the edge from x-p to x-q; p and q need not be ordered."""
    label = scale * p * q
    start = label - p
    end = label - q
    additive_weight = p - q
    euler_weight = Fraction(scale * p - 1, scale * p) / Fraction(
        scale * q - 1, scale * q
    )
    assert end - start == additive_weight
    assert euler_weight == Fraction(end, start)
    return {
        "A": scale,
        "p": p,
        "q": q,
        "label": label,
        "start": start,
        "end": end,
        "additive_weight": additive_weight,
        "euler_weight": [euler_weight.numerator, euler_weight.denominator],
    }


def verify_path(edges: list[dict[str, object]]) -> dict[str, object]:
    for left, right in zip(edges, edges[1:]):
        assert left["end"] == right["start"]
    additive = sum(int(edge["additive_weight"]) for edge in edges)
    euler = Fraction(1)
    for edge in edges:
        numerator, denominator = edge["euler_weight"]
        euler *= Fraction(int(numerator), int(denominator))
    start = int(edges[0]["start"])
    end = int(edges[-1]["end"])
    assert additive == end - start
    assert euler == Fraction(end, start)
    return {
        "start": start,
        "end": end,
        "edge_count": len(edges),
        "additive_sum": additive,
        "euler_product": [euler.numerator, euler.denominator],
    }


def main() -> None:
    # The two mixed-valuation parallel-edge cycles are exact controls: both
    # alternative one-edge paths have the same endpoint gradient.
    path_273_a = [oriented_edge(8, 5, 7)]
    path_273_b = [oriented_edge(2, 11, 13)]
    audit_273_a = verify_path(path_273_a)
    audit_273_b = verify_path(path_273_b)
    assert audit_273_a == audit_273_b == {
        "start": 275,
        "end": 273,
        "edge_count": 1,
        "additive_sum": -2,
        "euler_product": [273, 275],
    }

    path_5355_a = [oriented_edge(16, 5, 67)]
    path_5355_b = [oriented_edge(4, 17, 79)]
    audit_5355_a = verify_path(path_5355_a)
    audit_5355_b = verify_path(path_5355_b)
    assert audit_5355_a == audit_5355_b == {
        "start": 5355,
        "end": 5293,
        "edge_count": 1,
        "additive_sum": -62,
        "euler_product": [5293, 5355],
    }

    result = {
        "schema": "amra.erdos635.r004-shared-path-gradient.v1",
        "status": "PASS",
        "edge_identities": [
            "(x-q)-(x-p)=p-q",
            (
                "(1-1/(A*p))/(1-1/(A*q)) "
                "=(x-q)/(x-p)"
            ),
        ],
        "path_consequence": (
            "For every oriented path, sum(p-q)=v-u and the Euler ratio "
            "product equals v/u.  Thus subtracting two shared-endpoint paths "
            "gives 0 and 1 tautologically."
        ),
        "route_verdict": (
            "The R003 first-moment and Euler-product identities are correct, "
            "but shared-path subtraction adds no coupling capable of forcing "
            "compatible majorization or primality."
        ),
        "parallel_cycle_controls": {
            "component_273": audit_273_a,
            "component_5355": audit_5355_a,
        },
        "scope": (
            "This kills the proposed shared-path-invariant proof route.  It "
            "does not prove that the swap graph is a pseudoforest."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
