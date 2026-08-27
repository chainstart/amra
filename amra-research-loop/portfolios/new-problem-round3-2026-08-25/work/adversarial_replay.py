#!/usr/bin/env python3
"""Cross-campaign adversarial replay for portfolio round 3."""

from __future__ import annotations

import itertools
import json
import math
import os
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGNS = ROOT / "campaigns"
PORTFOLIO = Path(__file__).resolve().parent.parent


def replay_317() -> dict[str, object]:
    path = CAMPAIGNS / "erdos-317-residue-tail-20260825/evidence/cofactor_route_test_100000.json"
    payload = json.loads(path.read_text())
    for case in payload["crt_cases"]:
        primes = case["primes"]
        signs = case["signs"]
        multiplier = case["multiplier_mod_product"]
        product = math.prod(primes)
        if math.gcd(multiplier, product) != 1:
            raise AssertionError("non-coprime CRT multiplier")
        for p, sign in zip(primes, signs):
            if multiplier * (product // p) % p != sign % p:
                raise AssertionError("CRT sign replay failed")
    if payload["all_sign_patterns_replayed"] != 28:
        raise AssertionError("unexpected CRT case count")
    return {
        "crt_sign_patterns_replayed": payload["all_sign_patterns_replayed"],
        "largest_prime_counterinstances_through": payload["limit"],
        "largest_prime_allowed_count": payload["largest_prime_allowed_count"],
    }


def reachable(values: list[int], modulus: int) -> set[int]:
    result = {0}
    for value in values:
        old = tuple(result)
        result.update((item + value) % modulus for item in old)
    return result


def replay_354() -> dict[str, object]:
    path = CAMPAIGNS / "erdos-354-floor-precomplete-20260825/evidence/carry_residue_replay.json"
    payload = json.loads(path.read_text())
    for row in payload["rows"]:
        values = row["values"]
        carries = [values[i + 1] - 2 * values[i] for i in range(len(values) - 1)]
        if carries != row["carries"] or any(bit not in (0, 1) for bit in carries):
            raise AssertionError("carry replay failed")
        for q in range(2, payload["max_modulus"] + 1):
            count = len(reachable(values, q))
            if count != row["residue_coverage_counts"][str(q)]:
                raise AssertionError("residue replay failed")
    return {
        "samples_replayed": len(payload["rows"]),
        "carry_depth": payload["depth"],
        "moduli_replayed_through": payload["max_modulus"],
    }


def replay_25() -> dict[str, object]:
    moduli = (2, 3, 5)
    period = math.prod(moduli)
    expected = math.prod((Fraction(m - 1, m) for m in moduli), start=Fraction(1))
    assignments = 0
    for residues in itertools.product(*(range(m) for m in moduli)):
        good = sum(
            all(n % m != a for m, a in zip(moduli, residues))
            for n in range(period)
        )
        if Fraction(good, period) != expected:
            raise AssertionError("coprime density depends on residues")
        assignments += 1
    return {
        "all_residue_assignments_replayed": assignments,
        "moduli": moduli,
        "exact_density": f"{expected.numerator}/{expected.denominator}",
    }


def replay_states() -> dict[str, str]:
    result = {}
    for campaign_id in (
        "erdos-317-residue-tail-20260825",
        "erdos-354-floor-precomplete-20260825",
        "erdos-25-log-density-tail-20260825",
    ):
        state = json.loads((CAMPAIGNS / campaign_id / "campaign_state.json").read_text())
        decision = json.loads((CAMPAIGNS / campaign_id / "decision.json").read_text())
        if state["phase"] != "frozen" or decision["outcome"] != "freeze":
            raise AssertionError(f"campaign not fail-closed: {campaign_id}")
        result[campaign_id] = state["phase"]
    return result


def main() -> None:
    cgroup = Path("/proc/self/cgroup").read_text().strip()
    payload = {
        "schema_version": "amra.new-problem-round3-replay.v1",
        "claim_scope": "adversarial computational replay, not independent mathematical reconstruction",
        "erdos_317": replay_317(),
        "erdos_354": replay_354(),
        "erdos_25": replay_25(),
        "campaign_states": replay_states(),
        "resource_guard": {
            "observed_cgroup": cgroup,
            "inside_openmath_slice": "openmath.slice" in cgroup,
        },
        "pid": os.getpid(),
    }
    output = PORTFOLIO / "evidence/adversarial_replay.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
