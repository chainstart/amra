#!/usr/bin/env python3
"""Discovery-only c-quadratic discriminant scan for the PPP chamber."""

from __future__ import annotations

from pathlib import Path
import sys


EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
sys.path.insert(0, str(EVIDENCE))

from verify_c_zero_fibre import (  # noqa: E402
    add,
    derivative,
    multiply,
    reconstruct_original,
    restrict_original_zero,
)
from verify_shared_page_discriminant import C_EDGE, coefficient  # noqa: E402


B_EDGE = (0, 4)


def row(poly):
    values = tuple(poly.values())
    return {
        "terms": len(poly),
        "positive": sum(value > 0 for value in values),
        "negative": sum(value < 0 for value in values),
        "minimum": min(values),
        "maximum": max(values),
    }


def main():
    deletion, connectivity, _, _ = reconstruct_original()
    A = derivative(deletion, (B_EDGE,))
    C = restrict_original_zero(deletion, B_EDGE)
    D = derivative(connectivity, (B_EDGE,))
    E = restrict_original_zero(connectivity, B_EDGE)
    delta = add(multiply(A, E), multiply(D, C), -1)
    c0, c1, c2 = (coefficient(delta, C_EDGE, degree) for degree in range(3))
    discriminant = add(multiply(c1, c1), multiply(c0, c2), -4)
    print({
        "c0": row(c0),
        "c1": row(c1),
        "c2": row(c2),
        "discriminant": row(discriminant),
    })


if __name__ == "__main__":
    main()
