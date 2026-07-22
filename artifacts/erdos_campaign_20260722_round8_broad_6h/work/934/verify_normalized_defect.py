#!/usr/bin/env python3
"""Finite exact falsification check for the normalized defect lemma.

The universal proof is in the accompanying markdown.  This script only
checks the set identities on S_3 exhaustively and on a deterministic sample
of subsets of S_4.
"""

from __future__ import annotations

import itertools
import json
import random


Permutation = tuple[int, ...]


def compose(p: Permutation, q: Permutation) -> Permutation:
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p: Permutation) -> Permutation:
    ans = [0] * len(p)
    for i, image in enumerate(p):
        ans[image] = i
    return tuple(ans)


def product(left: set[Permutation], right: set[Permutation]) -> set[Permutation]:
    return {compose(x, y) for x in left for y in right}


def conjugate_set(x: Permutation, values: set[Permutation]) -> set[Permutation]:
    xi = inverse(x)
    return {compose(compose(x, value), xi) for value in values}


def check(group: list[Permutation], b: set[Permutation]) -> tuple[bool, bool]:
    bi = {inverse(x) for x in b}
    u = product(b, bi)
    v = product(bi, b)
    c = set(group) - u
    premise = len(u) == len(v) and product(product(bi, c), b) <= v
    if not premise:
        return False, False

    b0 = min(b)
    b0i = inverse(b0)
    a = {compose(x, b0i) for x in b}
    ai = {inverse(x) for x in a}
    ua = product(a, ai)
    va = product(ai, a)
    assert tuple(range(len(b0))) in a
    assert ua == u
    assert va == conjugate_set(b0, v)
    assert product(product(ai, c), a) <= va
    assert c <= va
    assert ua | va == set(group)
    assert a <= ua & va
    assert len(group) <= 2 * len(ua) - len(a)
    assert len(ua) <= len(a) ** 2 - len(a) + 1
    return True, bool(c)


def main() -> None:
    rng = random.Random(934)
    records = []
    for n in (3, 4):
        group = list(itertools.permutations(range(n)))
        if n == 3:
            subsets = [
                set(combo)
                for size in range(1, len(group) + 1)
                for combo in itertools.combinations(group, size)
            ]
            method = "exhaustive_nonempty_subsets"
        else:
            subsets = [
                set(rng.sample(group, rng.randint(1, len(group))))
                for _ in range(25000)
            ]
            method = "deterministic_random_subsets"
        premises = proper = 0
        for subset in subsets:
            holds, has_defect = check(group, subset)
            premises += int(holds)
            proper += int(holds and has_defect)
        records.append({
            "group": f"S_{n}",
            "method": method,
            "tested": len(subsets),
            "premise_holds": premises,
            "proper_defect_premise_holds": proper,
        })
    print(json.dumps({
        "schema": "amra.erdos934.round8.normalized_defect.v1",
        "records": records,
        "warning": "finite falsification only; the markdown proof is universal",
        "result": "PASS",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
