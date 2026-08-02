#!/usr/bin/env python3
"""Finite arithmetic guard for the mixed-high outer-low identity."""

from __future__ import annotations

import json


def profile(t_cross: int, a_internal: int, high_type: str) -> dict[str, int | bool]:
    if t_cross + a_internal <= 0:
        raise ValueError("the good colour class must be nonempty")
    if high_type not in {"none", "cross", "internal"}:
        raise ValueError("invalid high type")
    if high_type == "cross" and t_cross == 0:
        raise ValueError("a cross high edge requires a cross edge")
    if high_type == "internal" and a_internal == 0:
        raise ValueError("an internal high edge requires an internal edge")

    cross_high = int(high_type == "cross")
    internal_high = int(high_type == "internal")
    low_cross = t_cross - cross_high
    low_internal = a_internal - internal_high
    wholly_low = int(high_type == "none")

    defect_a = t_cross + a_internal - 1
    defect_b = max(0, t_cross - 1)
    residue = defect_a - defect_b

    mixed = int(high_type == "internal" and t_cross >= 1)
    internal_only_low = int(high_type == "none" and t_cross == 0)
    reconstructed = low_internal + mixed - internal_only_low

    low_localization = low_cross + low_internal - wholly_low
    return {
        "defect_a": defect_a,
        "defect_b": defect_b,
        "residue": residue,
        "low_cross": low_cross,
        "low_internal": low_internal,
        "wholly_low": wholly_low,
        "mixed": mixed,
        "internal_only_low": internal_only_low,
        "low_localization_matches": low_localization == defect_a,
        "identity_matches": reconstructed == residue,
    }


def exhaustive_certificate(limit: int = 40) -> dict[str, int | bool]:
    profiles = 0
    aggregates = 0
    records = []
    for t_cross in range(limit + 1):
        for a_internal in range(limit + 1):
            if t_cross + a_internal == 0:
                continue
            for high_type in ("none", "cross", "internal"):
                if high_type == "cross" and t_cross == 0:
                    continue
                if high_type == "internal" and a_internal == 0:
                    continue
                result = profile(t_cross, a_internal, high_type)
                assert result["low_localization_matches"]
                assert result["identity_matches"]
                records.append(result)
                profiles += 1

    # Aggregate prefixes guard that the colourwise identity sums without
    # an accidental global correction.
    for stop in range(1, min(len(records), 500) + 1):
        chosen = records[:stop]
        left = sum(int(record["residue"]) for record in chosen)
        right = (
            sum(int(record["low_internal"]) for record in chosen)
            + sum(int(record["mixed"]) for record in chosen)
            - sum(int(record["internal_only_low"]) for record in chosen)
        )
        assert left == right
        aggregates += 1

    return {
        "limit": limit,
        "profiles": profiles,
        "aggregate_prefixes": aggregates,
        "all_colourwise_identities": True,
        "all_aggregate_identities": True,
        "pass": True,
    }


def main() -> int:
    result = exhaustive_certificate()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
