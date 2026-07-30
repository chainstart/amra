#!/usr/bin/env python3
"""Independent ledger audit for the dimension-ten algebra boundary.

This file deliberately does not import ``search_dim10_algebra_profiles``.
It enumerates bounded tuples by Cartesian product rather than recursive
compositions and records the first applicable human lemma for every
profile that survives the elementary rank conditions.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json


Profile = tuple[int, ...]


def profiles() -> list[Profile]:
    answer: list[Profile] = []
    for length in (6, 7, 8):
        for values in product(range(1, 6), repeat=length):
            if values[0] >= 2 and sum(values) == 10:
                answer.append(values)
    return answer


def layer_rank(profile: Profile) -> bool:
    # A_i A_j = A_{i+j} gives d_{i+j} <= d_i d_j.
    return all(
        profile[i + j - 1] <= profile[i - 1] * profile[j - 1]
        for i in range(1, len(profile))
        for j in range(1, len(profile))
        if i + j <= len(profile)
    )


def first_exclusion(profile: Profile) -> str | None:
    if not layer_rank(profile):
        return "layer-rank"
    if profile[1] == 1 and profile[2] > 1:
        return "d2-line"
    if len(profile) == 6 and profile[2] == 1:
        return "degree-six"
    if any(
        profile[index] == 1 and profile[index + 1] > 1
        for index in range(1, len(profile) - 1)
    ):
        return "line-propagation"
    if len(profile) == 6 and profile[4:] == (1, 1):
        return "sixfold-tail-tensor"
    if (
        len(profile) == 7
        and profile[2] == profile[3] == profile[5] == 1
    ):
        return "seven-layer-power"
    if len(profile) == 7 and profile[3:] == (1, 1, 1, 1):
        return "cyclic-J3"
    if len(profile) == 8 and profile[2:] == (1, 1, 1, 1, 1, 1):
        return "cyclic-basis"
    return None


def audit() -> dict[str, object]:
    all_profiles = profiles()
    survivors = [
        profile for profile in all_profiles if first_exclusion(profile) is None
    ]
    reason_counts = Counter(
        first_exclusion(profile) for profile in all_profiles
    )
    assert len(all_profiles) == 92
    assert Counter(map(len, all_profiles)) == {6: 56, 7: 28, 8: 8}
    assert reason_counts == {
        "layer-rank": 63,
        "d2-line": 6,
        "degree-six": 9,
        "line-propagation": 4,
        "sixfold-tail-tensor": 4,
        "seven-layer-power": 3,
        "cyclic-J3": 1,
        "cyclic-basis": 2,
    }
    assert survivors == []
    payload = {
        "schema": "amra.kou21137.dim10-independent-ledger.v1",
        "scope": {
            "dimension": 10,
            "minimum_length": 6,
            "maximum_length": 8,
            "first_layer_minimum": 2,
            "J9_zero": True,
        },
        "profile_count": len(all_profiles),
        "count_by_length": dict(sorted(Counter(map(len, all_profiles)).items())),
        "first_exclusion_counts": dict(sorted(reason_counts.items())),
        "survivors": survivors,
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()
    payload["sha256"] = sha256(canonical).hexdigest()
    return payload


def main() -> None:
    result = audit()
    print(
        "DIM10_INDEPENDENT_AUDIT"
        f"|profiles={result['profile_count']}"
        "|lengths=6:56,7:28,8:8"
        "|survivors=0"
        f"|sha256={result['sha256']}"
    )
    print("DONE")


if __name__ == "__main__":
    main()
