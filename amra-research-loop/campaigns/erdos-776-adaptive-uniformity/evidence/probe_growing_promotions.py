#!/usr/bin/env python3
"""Bounded exact falsifier for finite-promotion shortcuts in Erdős #776.

This only scans the relaxed no-borrow coordinates.  It records exact integer
states; it does not extrapolate a finite scan to an unbounded theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from math import comb
from pathlib import Path


def rank_two_upper(top: int, remainder: int) -> int:
    assert 0 <= remainder < top
    return comb(top, 3) + comb(remainder, 2)


def admissible(q: int, c: int, r: int, u: int) -> dict[str, int] | None:
    n = comb(q, 2) + r
    b = c * q + comb(c, 2) + u - r + 1
    twice_h = comb(b - 1, 2) + 2 - n
    if twice_h % 2:
        return None
    h = twice_h // 2
    if b < 31 or h < 224 or b >= h:
        return None
    z = rank_two_upper(q, r)
    w = rank_two_upper(q + c, u)
    cap = comb(b, 2) + 1
    gamma3 = w - z - cap
    x = n + z - cap + 1
    y = n + w - cap
    if gamma3 >= 0 or x < 0:
        return None
    assert y >= x >= 0
    return {
        "q": q,
        "c": c,
        "r": r,
        "u": u,
        "b": b,
        "h": h,
        "gamma3": gamma3,
        "x": x,
        "y": y,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q-max", type=int, default=220)
    parser.add_argument("--c-max", type=int, default=24)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    first_by_c: dict[int, dict[str, int]] = {}
    checked = 0
    for q in range(2, args.q_max + 1):
        for c in range(2, args.c_max + 1):
            if c in first_by_c:
                continue
            for r in range(q):
                for u in range(q + c):
                    checked += 1
                    state = admissible(q, c, r, u)
                    if state is not None:
                        first_by_c[c] = state
                        break
                if c in first_by_c:
                    break

    payload = {
        "classification": "finite_exact_falsifier",
        "domain": {"q_max": args.q_max, "c_max": args.c_max},
        "tuples_checked_until_first_hit_per_c": checked,
        "first_admissible_state_by_promotion": {
            str(c): first_by_c[c] for c in sorted(first_by_c)
        },
        "finite_promotion_alphabet_c_le_5_refuted": any(c >= 6 for c in first_by_c),
        "unbounded_claim_made": False,
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    args.output.write_bytes(encoded)
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("output_sha256", hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
