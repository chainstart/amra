#!/usr/bin/env python3
"""Bounded exact recovery-rank profiles for small fixed (k,r) families."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import json


SOURCE = (Path(__file__).resolve().parents[2]
          / "erdos-776-adaptive-uniformity/evidence/search_c1_two_row_recovery.py")
spec = spec_from_file_location("c1_fixed_profiles", SOURCE)
c1 = module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(c1)


def profile(row, max_rank=12):
    signs = {5: row["gamma5"]}
    if row["gamma6"] is None:
        return signs, 6, None
    signs[6] = row["gamma6"]
    x = {3: row["p"], 4: row["P"]}
    y = {3: row["v"], 4: row["V"]}
    tau = row["tau"]
    borrow = None
    for rank in range(5, max_rank):
        x[rank] = c1.upper(x[rank - 1], rank - 1) - tau + 1
        y[rank] = c1.upper(y[rank - 1], rank - 1) - tau
        if min(x[rank], y[rank]) < 0:
            borrow = rank + 1
            break
        if rank >= 5:
            gamma_rank = rank + 2
            signs[gamma_rank] = (
                c1.upper(y[rank], rank) - c1.upper(x[rank], rank)
                - c1.upper(x[rank - 1], rank - 1) - 1
            )
    first_positive = next((m for m in sorted(signs) if signs[m] >= 0), None)
    return signs, borrow, first_positive


def main():
    js = [17, 25, 33, 41, 49, 57, 73, 101, 149, 305]
    tested = accepted = 0
    rows = []
    maxima = {}
    for j in js:
        for k in range(3, 13):
            for r in range(1, 51):
                tested += 1
                row = c1.candidate(j, k, r)
                if (row is None or row["transition"] != "-- -> ++"
                        or row["gamma5"] >= 0):
                    continue
                accepted += 1
                signs, borrow, first = profile(row)
                item = {
                    "j": j, "k": k, "r": r, "q": row["q"],
                    "borrow_rank": borrow, "first_nonnegative_rank": first,
                    "signs": {str(m): v for m, v in signs.items()},
                }
                rows.append(item)
                key = f"{k},{r}"
                old = maxima.get(key)
                score = first if first is not None else 99
                if old is None or score > old[0]:
                    maxima[key] = (score, item)
    rows.sort(key=lambda z: ((z["first_nonnegative_rank"] or 99), z["j"]), reverse=True)
    print(json.dumps({
        "schema": "amra.erdos776.adaptive-round4.fixed-parameter-profile-probe.v1",
        "domain": {"j": js, "k": [3, 12], "r": [1, 50], "max_rank": 12},
        "tested": tested,
        "accepted_gamma5_negative": accepted,
        "largest_profiles": rows[:30],
        "fixed_pair_count": len(maxima),
        "scope_warning": "finite profile search only; no absence or uniform recovery theorem",
    }, indent=2))


if __name__ == "__main__":
    main()
