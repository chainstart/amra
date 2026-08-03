#!/usr/bin/env python3
"""Condition on the moving gamma4 wall instead of uniformly sampling r."""

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
independent = load("canonical_source", Path(__file__).with_name("verify_gpp_pfree_counterexample.py"))


def main() -> None:
    scales = list(range(6, 61)) + [70, 80, 90, 100]
    tested_rows = set()
    accepted = 0
    minimum_leading = None
    minimum_top_index = None
    first_pfree = None
    leading_counterexamples = []
    top_index_counterexamples = []
    fibre_summaries = []

    for j in scales:
        for k in range(4, 301):
            start_r = gpp.first_target_r(j, k)
            if start_r is None:
                continue
            step = k - 1

            def raw(offset: int):
                if offset < 0:
                    return None
                tested_rows.add((j, k, offset))
                return gpp.row(j, k, start_r + offset * step)

            first = raw(0)
            if first is None or not first.get("target") or first["gamma4"] >= 0:
                continue

            lo, hi = 0, 1
            while hi < (1 << 50):
                probe = raw(hi)
                if probe is None or not probe.get("target") or probe["gamma4"] >= 0:
                    break
                lo, hi = hi, 2 * hi
            if hi >= (1 << 50):
                continue

            # Locate one sign-change wall. Carries can spoil monotonicity, so
            # the result is used only to centre an exact local window.
            while lo + 1 < hi:
                mid = (lo + hi) // 2
                probe = raw(mid)
                if probe is not None and probe.get("target") and probe["gamma4"] < 0:
                    lo = mid
                else:
                    hi = mid

            fibre_min = None
            for offset in sorted(set(range(0, 65)) | set(range(max(0, lo - 96), hi + 97))):
                r = start_r + offset * step
                row = c1.candidate(j, k, r)
                if row is None or row["transition"] != "++ -> ++":
                    continue
                accepted += 1
                cp = independent.canonical(row["p"], 3)[0][0]
                cv = independent.canonical(row["v"], 3)[0][0]
                a = independent.canonical(row["alpha"], 2)[0][0]
                leading = (comb(cv, 4) - comb(cp + 1, 4)
                           - c1.upper(row["alpha"], 2))
                top_index = (comb(cv, 4) - comb(cp + 1, 4)
                             - comb(a + 1, 3))
                pfree = (c1.upper(row["v"] - row["p"], 3)
                         - c1.upper(row["alpha"], 2) - 1)
                record = {**row, "offset": offset, "top_p": cp,
                          "top_v": cv, "top_alpha": a,
                          "leading_block_margin": leading,
                          "top_index_margin": top_index,
                          "p_free_margin": pfree}
                if fibre_min is None or leading < fibre_min["leading_block_margin"]:
                    fibre_min = record
                if minimum_leading is None or leading < minimum_leading["leading_block_margin"]:
                    minimum_leading = record
                if minimum_top_index is None or top_index < minimum_top_index["top_index_margin"]:
                    minimum_top_index = record
                if pfree < 0 and (first_pfree is None or (j, k, offset) <
                                  (first_pfree["j"], first_pfree["k"], first_pfree["offset"])):
                    first_pfree = record
                if leading < 0 and len(leading_counterexamples) < 3:
                    leading_counterexamples.append(record)
                if top_index < 0 and len(top_index_counterexamples) < 3:
                    top_index_counterexamples.append(record)
            if fibre_min is not None:
                fibre_summaries.append({"j": j, "k": k,
                                        "located_wall_offset": lo,
                                        "minimum_leading_margin": fibre_min["leading_block_margin"]})

    print(json.dumps({
        "schema": "amra.erdos776.round3-adaptive-gamma4-wall-probe.v1",
        "domain": {"j": scales, "k": [4, 300],
                   "conditioning": "exponential/binary location of a gamma4 sign change plus exact windows at the target and located wall"},
        "raw_rows_evaluated": len(tested_rows),
        "accepted_actual_pp_rows": accepted,
        "minimum_base_leading_margin": minimum_leading,
        "minimum_top_index_margin": minimum_top_index,
        "base_leading_counterexample_count": len(leading_counterexamples),
        "first_base_leading_counterexample": leading_counterexamples,
        "top_index_counterexample_count": len(top_index_counterexamples),
        "first_top_index_counterexample": top_index_counterexamples,
        "first_p_free_counterexample_in_scan": first_pfree,
        "fibre_summary_count": len(fibre_summaries),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "classification": "finite exact moving-wall falsifier; binary centring is not an exhaustiveness proof when carries cause re-entry",
        "public_problem_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
