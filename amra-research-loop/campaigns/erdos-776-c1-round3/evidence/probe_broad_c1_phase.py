#!/usr/bin/env python3
"""Broad phase-space falsifier for the two surviving c=1 inequalities."""

from importlib.util import module_from_spec, spec_from_file_location
from math import comb
from pathlib import Path
import hashlib
import json


BASE = Path(__file__).resolve().parents[2]


def load(name: str, path: Path):
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


c1 = load("c1_source", BASE / "erdos-776-adaptive-uniformity/evidence/search_c1_two_row_recovery.py")
gpp = load("gpp_source", BASE / "erdos-776-adaptive-uniformity/evidence/search_gpp_moving_boundary.py")
envelope = load("envelope_source", Path(__file__).with_name("probe_nested_binomial_envelope.py"))


def main() -> None:
    scales = list(range(8, 41)) + [50, 60, 80, 100]
    k_choices = list(range(4, 201)) + [256, 384, 512, 768, 1024]
    tested = 0
    target_rows = 0
    gpp_rows = 0
    final_rows = 0
    min_envelope = None
    envelope_counterexamples = []
    negative5 = 0
    borrowed_negative5 = []
    double_negative = []

    for j in scales:
        h = 112 * (1 << (j - 1))
        for k in k_choices:
            step = k - 1
            base = 2 * h - comb(k - 1, 2) - 2
            if base <= 0:
                continue
            residue = (-base) % step
            # u=r+k-1<q+1 gives the sharper legal upper endpoint.
            max_r = (base - step * (k - 2) - 1) // (k - 2)
            if max_r < residue:
                continue
            indices = (max_r - residue) // step
            sample_indices = {indices * s // 400 for s in range(401)}
            for index in sample_indices:
                r = residue + index * step
                tested += 1

                grow = gpp.row(j, k, r)
                if grow is not None and grow.get("target") and grow["gamma4"] < 0:
                    target_rows += 1
                    if grow["alpha"] >= 0:
                        gpp_rows += 1
                        a = envelope.top_two(grow["alpha"])
                        t = envelope.envelope_index(a)
                        gap = grow["e"] - comb(t, 3)
                        record = {**grow, "a": a, "t": t,
                                  "required_e": comb(t, 3), "envelope_gap": gap}
                        if min_envelope is None or gap < min_envelope["envelope_gap"]:
                            min_envelope = record
                        if gap < 0 and len(envelope_counterexamples) < 3:
                            envelope_counterexamples.append(record)

                row = c1.candidate(j, k, r)
                if row is None or row["transition"] != "-- -> ++":
                    continue
                final_rows += 1
                if row["gamma5"] >= 0:
                    continue
                negative5 += 1
                if row["gamma6"] is None and len(borrowed_negative5) < 3:
                    borrowed_negative5.append(row)
                if row["gamma6"] is not None and row["gamma6"] < 0 and len(double_negative) < 3:
                    double_negative.append(row)

    print(json.dumps({
        "schema": "amra.erdos776.round3-broad-c1-phase-probe.v1",
        "domain": {"j": scales, "k": k_choices,
                   "r_sampling": "401 evenly spaced residue-compatible indices over the full legal r interval"},
        "tested_actual_parameter_triples": tested,
        "negative_gamma4_target_rows": target_rows,
        "gpp_rows": gpp_rows,
        "minimum_nested_envelope_gap": min_envelope,
        "nested_envelope_counterexample_count": len(envelope_counterexamples),
        "first_nested_envelope_counterexample": envelope_counterexamples,
        "final_chamber_rows": final_rows,
        "gamma5_negative_final_rows": negative5,
        "negative_gamma5_with_rank6_borrow_count": len(borrowed_negative5),
        "first_borrowed_negative_gamma5": borrowed_negative5,
        "double_negative_count_stored": len(double_negative),
        "first_double_negative": double_negative,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "classification": "finite broad phase-space falsifier only",
        "public_problem_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
