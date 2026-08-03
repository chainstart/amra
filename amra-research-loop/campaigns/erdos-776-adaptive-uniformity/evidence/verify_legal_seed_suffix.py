#!/usr/bin/env python3
"""Independent finite guard for the actual adjacent-orbit seed sets."""

from math import comb
import json


def upper(number: int, rank: int) -> int:
    if number < 0:
        raise ValueError(number)
    remainder = number
    ceiling = None
    answer = 0
    for lower in range(rank, 0, -1):
        if remainder == 0:
            break
        lo = lower - 1
        hi = ceiling if ceiling is not None else max(2, lower + 1)
        if ceiling is None:
            while comb(hi, lower) <= remainder:
                hi *= 2
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if comb(mid, lower) <= remainder:
                lo = mid
            else:
                hi = mid
        if lo >= lower:
            remainder -= comb(lo, lower)
            answer += comb(lo, lower + 1)
            ceiling = lo
    assert remainder == 0
    return answer


def seed_signs(ambient: int):
    tax = ambient + 221
    f_value = ambient
    g_value = ambient + 1
    signs = []
    for rank in range(1, ambient - 42 + 1):
        uf = upper(f_value, rank)
        g_next = upper(g_value, rank) - (tax + 1)
        gamma = g_next - (f_value + uf)
        signs.append(1 if gamma >= 0 else 0)
        f_value = uf - tax
        g_value = g_next
        assert f_value >= 0 and g_value >= 0
    return signs


def main() -> None:
    first_seeds = {}
    for ambient in range(67, 161):
        signs = seed_signs(ambient)
        assert 1 in signs
        first = signs.index(1) + 1
        assert signs == [0] * (first - 1) + [1] * (len(signs) - first + 1)
        first_seeds[str(ambient)] = first
    print(json.dumps({
        "schema": "amra.erdos776.legal-seed-suffix-guard.v1",
        "ambient_range": [67, 160],
        "every_seed_set_nonempty": True,
        "every_seed_set_is_suffix": True,
        "minimum_first_seed": min(first_seeds.values()),
        "maximum_first_seed": max(first_seeds.values()),
        "sample_first_seeds": {key: first_seeds[key] for key in ("67", "100", "160")},
        "unbounded_claim_from_computation": False,
        "public_problem_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
