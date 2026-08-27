#!/usr/bin/env python3
"""Finite guards for CR.1 identities and the endpoint-only CR.2 obstruction.

The universal density statements are proved symbolically in
ROUND4_COHERENT_RECOURSE.md; this script only guards the exact set identities
and the advertised finite instances of the counterexample.
"""

from __future__ import annotations

from fractions import Fraction
import json


def endpoint_only_obstruction(max_k: int = 32) -> dict[str, object]:
    decisions: set[int] = set()
    union_changes: set[int] = set()
    rates: list[Fraction] = []
    histories = {n: [] for n in range(2, 33)}

    for k in range(1, max_k + 1):
        cutoff = 2 ** (k // 2)
        changes = set(range(2, cutoff + 1))
        eta = Fraction(1, 2 ** ((k + 1) // 2))
        assert len(changes) <= eta * (2**k)
        rates.append(eta)

        decisions.symmetric_difference_update(changes)
        union_changes.update(changes)
        assert len(decisions) <= cutoff
        for n in histories:
            histories[n].append(n in decisions)

    # Each tested fixed integer changes at every sufficiently late step.
    for n, history in histories.items():
        first_forced = 2 * (n.bit_length())
        tail = history[first_forced:]
        assert len(tail) >= 2
        assert all(a != b for a, b in zip(tail, tail[1:]))

    # The infinite sum is exactly 2; every finite partial sum is below it.
    partial_rate_sum = sum(rates, Fraction())
    assert partial_rate_sum < 2
    assert union_changes == set(range(2, 2 ** (max_k // 2) + 1))

    return {
        "scales": max_k,
        "partial_rate_sum": str(partial_rate_sum),
        "infinite_rate_sum": "2",
        "largest_revised_prefix": max(union_changes),
        "all_tested_fixed_decisions_keep_toggling": True,
    }


def construction_identity(max_k: int = 20) -> dict[str, object]:
    # A deliberately nonnested synthetic sequence.  New block representatives
    # are inserted, while one high old representative is toggled at each step.
    transversals: dict[int, set[int]] = {1: {2}}
    for k in range(1, max_k):
        nxt = set(transversals[k])
        nxt.add(2**k + 1)
        nxt.symmetric_difference_update({2 ** max(1, k - 1)})
        transversals[k + 1] = nxt

    entry: set[int] = set()
    revisions: set[int] = set()
    previous_ground: set[int] = set()
    for k in range(1, max_k + 1):
        ground = set(range(2, 2**k + 1))
        entry.update(transversals[k] & (ground - previous_ground))
        if k < max_k:
            revisions.update((transversals[k + 1] ^ transversals[k]) & ground)
        previous_ground = ground

    permanent = entry | revisions
    assert all(transversals[k] <= permanent for k in transversals)
    assert any(
        ((transversals[k + 1] ^ transversals[k]) & set(range(2, 2**k + 1)))
        for k in range(1, max_k)
    )
    return {
        "scales": max_k,
        "entry_size": len(entry),
        "revision_reserve_size": len(revisions),
        "all_finite_sets_retained": True,
        "sequence_is_nonnested": True,
    }


def main() -> None:
    print(json.dumps({
        "status": "PASS",
        "scope": (
            "finite guards for CR.1 set containment and CR.2; "
            "asymptotic quantifiers are proved symbolically in the evidence note"
        ),
        "endpoint_only_obstruction": endpoint_only_obstruction(),
        "construction_identity": construction_identity(),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
