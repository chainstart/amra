#!/usr/bin/env python3
"""Exact finite falsifier for M303's nested-binomial G++ envelope."""

from importlib.util import module_from_spec, spec_from_file_location
from math import comb
from pathlib import Path
import hashlib
import json


SOURCE = (Path(__file__).resolve().parents[2]
          / "erdos-776-adaptive-uniformity/evidence/search_gpp_moving_boundary.py")
spec = spec_from_file_location("gpp_source", SOURCE)
source = module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(source)


def top_two(n: int) -> int:
    lo, hi = 1, 2
    while comb(hi, 2) <= n:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if comb(mid, 2) <= n:
            lo = mid
        else:
            hi = mid
    return lo


def envelope_index(a: int) -> int:
    target = comb(a + 1, 3)
    lo, hi = 3, 4
    while comb(hi, 4) < target:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if comb(mid, 4) >= target:
            hi = mid
        else:
            lo = mid
    return hi


def main() -> None:
    scales = list(range(6, 61)) + [70, 80, 90, 100]
    accepted = 0
    minimum = None
    counterexamples = []
    for j in scales:
        for k in range(4, 301):
            start = source.first_target_r(j, k)
            if start is None:
                continue
            for offset in range(-3, 301):
                data = source.row(j, k, start + offset * (k - 1))
                if data is None or not data.get("target") or data["gamma4"] >= 0:
                    continue
                accepted += 1
                a = top_two(data["alpha"])
                t = envelope_index(a)
                gap = data["e"] - comb(t, 3)
                record = {**data, "a": a, "t": t,
                          "required_e": comb(t, 3), "envelope_gap": gap,
                          "upper_alpha_cap": comb(a + 1, 3),
                          "lower_e_raise": comb(t, 4)}
                assert comb(a, 2) <= data["alpha"] < comb(a + 1, 2)
                assert source.upper(data["alpha"], 2) < comb(a + 1, 3)
                assert comb(t, 4) >= comb(a + 1, 3)
                if minimum is None or gap < minimum["envelope_gap"]:
                    minimum = record
                if gap < 0:
                    counterexamples.append(record)
                    break

    script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps({
        "schema": "amra.erdos776.round3-nested-binomial-envelope-probe.v1",
        "mechanism": "M303-nested-binomial-envelope",
        "domain": {"j": scales, "k": [4, 300],
                   "offsets_from_first_target_boundary": [-3, 300]},
        "accepted_actual_target_rows": accepted,
        "minimum_exact_gap": minimum,
        "counterexample_count": len(counterexamples),
        "first_counterexample": counterexamples[:1],
        "script_sha256": script_hash,
        "classification": "finite exact falsifier only; the universal actual-lattice lower bound remains open",
        "public_problem_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
