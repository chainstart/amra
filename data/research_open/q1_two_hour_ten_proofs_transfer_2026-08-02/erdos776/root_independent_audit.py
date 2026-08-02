#!/usr/bin/env python3
"""Root-side independent arithmetic audit for the #776 transfer lane.

This file imports none of the author implementation.  It uses a direct
linear Macaulay decomposition and independently rebuilds the frozen census,
the second-level remainder count, small multi-cap domains, and the new
two-promotion boundary coordinates.
"""

from __future__ import annotations

from collections import Counter
from functools import cache
import json
from math import comb


def c(n: int, r: int) -> int:
    return comb(n, r) if n >= r >= 0 else 0


@cache
def word(number: int, rank: int) -> tuple[tuple[int, int], ...]:
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    remainder = number
    ceiling: int | None = None
    answer: list[tuple[int, int]] = []
    for lower in range(rank, 0, -1):
        if remainder == 0:
            break
        top = lower - 1
        while (
            (ceiling is None or top + 1 < ceiling)
            and c(top + 1, lower) <= remainder
        ):
            top += 1
        if top >= lower:
            answer.append((top, lower))
            remainder -= c(top, lower)
            ceiling = top
    if remainder:
        raise AssertionError((number, rank, remainder, answer))
    return tuple(answer)


@cache
def up(number: int, rank: int) -> int:
    return sum(c(top, lower + 1) for top, lower in word(number, rank))


def head(number: int, rank: int) -> tuple[int, int]:
    expansion = word(number, rank)
    top = expansion[0][0] if expansion else rank - 1
    tail = number - c(top, rank)
    assert 0 <= tail < c(top, rank - 1)
    return top, tail


def loss(rank: int, cap: int, deficit: int) -> int:
    assert 0 <= deficit <= c(cap, rank)
    return c(cap, rank + 1) - up(c(cap, rank) - deficit, rank)


def audit_atlas() -> dict[str, object]:
    counts: Counter[int] = Counter()
    checked = 0
    nonpositive = 0
    minimum: tuple[int, tuple[int, ...]] | None = None
    second_positive = 0
    residual: list[tuple[int, ...]] = []
    for q in range(2, 61):
        for promotions in range(2, 15):
            for r in range(q):
                for u in range(q + promotions):
                    n = c(q, 2) + r
                    b = promotions * q + c(promotions, 2) + u - r + 1
                    twice_h = c(b - 1, 2) + 2 - n
                    if twice_h % 2:
                        continue
                    h = twice_h // 2
                    if b < 31 or h < 224 or b >= h:
                        continue
                    z = c(q, 3) + c(r, 2)
                    w = c(q + promotions, 3) + c(u, 2)
                    big_h = c(b, 2) + 1
                    gamma3 = w - z - big_h
                    x = n + z - big_h + 1
                    y = n + z + gamma3
                    if gamma3 >= 0 or x < 0:
                        continue
                    gamma4 = up(y, 3) - up(x, 3) - z - 1
                    a, alpha = head(x, 3)
                    t, beta = head(y, 3)
                    s, rho = head(alpha, 2)
                    v, sigma = head(beta, 2)
                    exact = (
                        c(t, 4) - c(a, 4) + c(v, 3) - c(s, 3)
                        + c(sigma, 2) - c(rho, 2) - z - 1
                    )
                    assert exact == gamma4
                    lower = (
                        c(t, 4) - c(a, 4) + c(v, 3) - c(s, 3)
                        + c(sigma, 2) - c(s - 1, 2) - z - 1
                    )
                    assert gamma4 >= lower
                    second_positive += int(lower > 0)
                    if lower <= 0:
                        residual.append((q, promotions, r, u, gamma4, lower))
                    row = (q, promotions, r, u, b, h)
                    if minimum is None or gamma4 < minimum[0]:
                        minimum = (gamma4, row)
                    checked += 1
                    counts[promotions] += 1
                    nonpositive += int(gamma4 <= 0)
    assert minimum is not None
    return {
        "checked": checked,
        "counts": dict(sorted(counts.items())),
        "nonpositive": nonpositive,
        "minimum": minimum,
        "second_positive": second_positive,
        "residual": residual,
    }


def audit_multicap() -> int:
    rows = 0
    for rank in range(1, 5):
        for cap in range(rank, 11):
            for gap in range(5):
                for large in range(c(cap, rank) + 1):
                    for small in range(large + 1):
                        left = loss(rank, cap, large) - loss(
                            rank, cap + gap, small
                        )
                        right = up(large - small, rank) - gap * small
                        assert left >= right
                        rows += 1
    return rows


def audit_boundary() -> dict[str, int]:
    rows = 0
    for q in range(40, 181):
        for k in range(1, min(q, 9)):
            r = q - k
            for u in range(9):
                b = q + u + k + 2
                n = c(q, 2) + r
                z = c(q, 3) + c(r, 2)
                w = c(q + 2, 3) + c(u, 2)
                big_h = c(b, 2) + 1
                x = n + z - big_h + 1
                y = n + w - big_h
                d = (u + 2 * k + 1) * (2 * q + u + 2) // 2
                e = (
                    2 * q * (u + k) + k * k + 2 * k * u
                    + 5 * k + 4 * u + 4
                ) // 2
                f = (-k * k + 2 * k * q - k + 2 * q + u * u - u - 2) // 2
                assert d - e == f
                assert x == c(q + 1, 3) - d
                assert y == c(q + 1, 3) + c(q, 2) - e
                if 0 <= e <= d <= c(q, 2):
                    gamma = up(y, 3) - up(x, 3) - z - 1
                    exact = loss(2, q, d) - loss(2, q, e) - c(q - k, 2) - 1
                    assert gamma == exact
                    assert gamma >= up(f, 2) - c(q - k, 2) - 1
                    rows += 1
    return {"exact_boundary_rows": rows}


def audit_shallow_base() -> dict[str, object]:
    rows: list[tuple[int, int, int, int, int]] = []
    for q in range(2, 90):
        r = q - 1
        for u in range(q + 2):
            b = q + u + 3
            n = c(q, 2) + r
            twice_h = c(b - 1, 2) + 2 - n
            if twice_h % 2:
                continue
            h = twice_h // 2
            if b < 31 or h < 224 or b >= h:
                continue
            z = c(q, 3) + c(r, 2)
            w = c(q + 2, 3) + c(u, 2)
            big_h = c(b, 2) + 1
            gamma3 = w - z - big_h
            x = n + z - big_h + 1
            y = n + z + gamma3
            if gamma3 >= 0 or x < 0:
                continue
            a, alpha = head(x, 3)
            t, beta = head(y, 3)
            delta = c(q - 1, 2) - alpha
            if (a, t) != (q - 1, q + 1) or not 1 <= delta <= q - 2:
                continue
            gamma4 = up(y, 3) - up(x, 3) - z - 1
            shallow_loss = delta * (q - 2) - c(delta + 1, 2)
            assert shallow_loss == loss(2, q - 1, delta)
            assert gamma4 == up(beta, 2) + shallow_loss - c(q - 1, 2) - 1
            assert gamma4 > 0
            rows.append((gamma4, q, u, b, h))
    return {"rows": len(rows), "minimum": min(rows)}


def main() -> None:
    atlas = audit_atlas()
    assert atlas["checked"] == 85_278
    assert atlas["counts"] == {2: 36_288, 3: 33_620, 4: 14_921, 5: 449}
    assert atlas["nonpositive"] == 0
    assert atlas["minimum"] == (69, (16, 2, 0, 3, 37, 256))
    assert atlas["second_positive"] == 85_276
    assert atlas["residual"] == [
        (36, 2, 35, 12, 354, -3),
        (38, 2, 37, 13, 489, -51),
    ]
    result = {
        "schema": "amra.erdos776.root-independent-audit.v1",
        "atlas": atlas,
        "multicap_small_rows": audit_multicap(),
        "shallow_base": audit_shallow_base(),
        "boundary": audit_boundary(),
        "pass": True,
        "original_problem_proved": False,
    }
    assert result["shallow_base"] == {
        "rows": 20,
        "minimum": (186, 39, 13, 55, 327),
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
