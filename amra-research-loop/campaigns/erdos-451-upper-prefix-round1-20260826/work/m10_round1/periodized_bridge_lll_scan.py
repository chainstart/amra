#!/usr/bin/env sage
"""LLL falsification scan for the L=2 periodized small-CRT bridge.

This is a finite diagnostic.  It looks for unusually short canonical CRT
lifts in the anisotropically scaled lattice

    {(2b H, 2h a_1, ..., 2h a_q): a_i == H (mod p_i)}.

An LLL row is not a proof that no worse vector exists.  Conversely, every
reported row is checked exactly before its floating weight is evaluated.
Run this file with Sage, behind ``openmath-memory-guard``.
"""

from __future__ import annotations

import argparse
import json
import math

from sage.all import ZZ, matrix


def primes_below(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * n
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(n - 1) + 1):
        if sieve[p]:
            sieve[p * p : n : p] = b"\x00" * (((n - 1 - p * p) // p) + 1)
    return [p for p in range(2, n) if sieve[p]]


def actual_blocks(min_k: int, max_k: int, step: int, min_rank: int,
                  max_rank: int, max_systems: int) -> list[dict[str, object]]:
    plist = primes_below(2 * max_k)
    rows: list[dict[str, object]] = []
    for k in range(min_k, max_k + 1, step):
        blocks: dict[int, list[int]] = {}
        for p in plist:
            if p <= k:
                continue
            if p >= 2 * k:
                break
            d = p - k
            delta = 1 << (d.bit_length() - 1)
            blocks.setdefault(delta, []).append(p)
        for delta, block in blocks.items():
            if min_rank <= len(block) <= max_rank:
                rows.append(
                    {
                        "k": k,
                        "delta": delta,
                        "moduli": tuple(block),
                        "offsets": tuple(p - k for p in block),
                    }
                )
    rows.sort(key=lambda row: (-len(row["moduli"]), row["k"], row["delta"]))
    if len(rows) <= max_systems:
        return rows
    head = rows[: max_systems // 2]
    tail = rows[max_systems // 2 :]
    slots = max_systems - len(head)
    head.extend(tail[(i * len(tail)) // slots] for i in range(slots))
    return head


def analyze(row: dict[str, object], poly_b: int, exponential_c: int,
            delta_lll: float, rows_to_keep: int) -> dict[str, object]:
    k = int(row["k"])
    delta = int(row["delta"])
    moduli = tuple(int(p) for p in row["moduli"])
    offsets = tuple(int(d) for d in row["offsets"])
    q = len(moduli)
    period = math.prod(moduli)
    width_product = math.prod(offsets)
    # b is a half-integer and b2=2b is integral.
    b2 = 2 * ((delta - 1) // 2) + 1
    h_numerator = (k**poly_b) * (exponential_c**q) * period
    h = (h_numerator + width_product - 1) // width_product
    if 2 * h >= period:
        return {
            "classification": "actual_451_prime_block",
            "label": f"k{k}-D{delta}",
            "rank": q,
            "skipped": "h_not_below_P_over_2",
            "h_over_P": h / period,
        }

    scale = 2 * h
    basis_rows = [[b2] + [scale] * q]
    for i, p in enumerate(moduli):
        vector = [0] * (q + 1)
        vector[i + 1] = -scale * p
        basis_rows.append(vector)
    reduced = matrix(ZZ, basis_rows).LLL(delta=delta_lll)

    candidates: list[dict[str, object]] = []
    for vector in reduced.rows():
        first = int(vector[0])
        if first % b2:
            raise AssertionError("scaled H coordinate is not integral")
        global_lift = first // b2
        locals_: list[int] = []
        for coordinate in vector[1:]:
            coordinate = int(coordinate)
            if coordinate % scale:
                raise AssertionError("scaled local coordinate is not integral")
            locals_.append(coordinate // scale)
        if any((global_lift - a) % p for a, p in zip(locals_, moduli)):
            raise AssertionError("LLL row left the congruence lattice")
        inside = abs(global_lift) < h and all(2 * abs(a) < b2 for a in locals_)
        trivial_diagonal = 2 * abs(global_lift) < b2 and all(
            a == global_lift for a in locals_
        )
        log_term = None
        if inside:
            log_term = math.log(period / h)
            log_term -= q * math.log(b2 / 2)
            log_term += math.log1p(-abs(global_lift) / h)
            log_term += sum(math.log1p(-2 * abs(a) / b2) for a in locals_)
        normalized_max = max(
            abs(global_lift) / h,
            *(2 * abs(a) / b2 for a in locals_),
        )
        candidates.append(
            {
                "H": global_lift,
                "inside_bridge_box": inside,
                "trivial_diagonal": trivial_diagonal,
                "normalized_max": normalized_max,
                "support": sum(a != 0 for a in locals_),
                "local_max_abs": max(abs(a) for a in locals_),
                "local_l1": sum(abs(a) for a in locals_),
                "log_single_S_term": log_term,
                "locals": locals_ if q <= 24 else None,
            }
        )
    candidates.sort(key=lambda item: item["normalized_max"])
    nontrivial = [item for item in candidates if not item["trivial_diagonal"]]
    return {
        "classification": "actual_451_prime_block",
        "label": f"k{k}-D{delta}",
        "k": k,
        "delta": delta,
        "rank": q,
        "b_twice": b2,
        "P_digits": len(str(period)),
        "h_digits": len(str(h)),
        "h_over_P": h / period,
        "lll_delta": delta_lll,
        "inside_rows": sum(item["inside_bridge_box"] for item in candidates),
        "best_nontrivial_row": nontrivial[0] if nontrivial else None,
        "best_rows": candidates[:rows_to_keep],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-k", type=int, default=500)
    parser.add_argument("--max-k", type=int, default=5000)
    parser.add_argument("--step", type=int, default=137)
    parser.add_argument("--min-rank", type=int, default=8)
    parser.add_argument("--max-rank", type=int, default=40)
    parser.add_argument("--max-systems", type=int, default=18)
    parser.add_argument("--poly-b", type=int, default=2)
    parser.add_argument("--exponential-c", type=int, default=6)
    parser.add_argument("--lll-delta", type=float, default=0.99)
    parser.add_argument("--rows-to-keep", type=int, default=5)
    parser.add_argument("--aggregate-only", action="store_true")
    args = parser.parse_args()

    systems = actual_blocks(
        args.min_k,
        args.max_k,
        args.step,
        args.min_rank,
        args.max_rank,
        args.max_systems,
    )
    results = [
        analyze(
            row,
            args.poly_b,
            args.exponential_c,
            args.lll_delta,
            args.rows_to_keep,
        )
        for row in systems
    ]
    if args.aggregate_only:
        compact = []
        for row in results:
            if "skipped" in row:
                compact.append(row)
                continue
            best = row["best_nontrivial_row"]
            compact.append(
                {
                    key: row[key]
                    for key in (
                        "label",
                        "k",
                        "delta",
                        "rank",
                        "b_twice",
                        "P_digits",
                        "h_digits",
                        "h_over_P",
                        "inside_rows",
                    )
                }
                | {
                    "best_nontrivial_normalized_max": None
                    if best is None else best["normalized_max"],
                    "best_nontrivial_support": None
                    if best is None else best["support"],
                    "best_nontrivial_log_single_S_term": None
                    if best is None else best["log_single_S_term"],
                }
            )
        results = compact
    payload = {
        "classification": "finite_lll_falsification_diagnostic_only",
        "parameters": vars(args),
        "systems": len(results),
        "systems_with_inside_lll_row": sum(
            bool(row.get("inside_rows")) for row in results
        ),
        "systems_with_inside_nontrivial_lll_row": sum(
            row.get("best_nontrivial_log_single_S_term") is not None
            if args.aggregate_only
            else row.get("best_nontrivial_row") is not None
            and row["best_nontrivial_row"]["inside_bridge_box"]
            for row in results
        ),
        "results": results,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
