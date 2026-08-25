#!/usr/bin/env python3
"""Exact finite replay of the target-irredundant multiplication-table batch."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=2048)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = []
    value = 64
    while value <= args.max_n:
        sizes.append(value)
        value *= 2
    rows = []
    final_encoded = b""
    for n in sizes:
        moduli = range(n + 1, 2 * n + 1)
        for later in moduli:
            target = later - 1
            if any(target % earlier == earlier - 1 for earlier in range(n + 1, later)):
                raise AssertionError("annular target was covered by an earlier class")
        products = {quotient * modulus for quotient in range(1, n + 1) for modulus in moduli}
        translated = {product - 1 for product in products}
        if len(translated) != len(products):
            raise AssertionError("translation changed cardinality")
        final_encoded = b"".join(value.to_bytes(8, "little") for value in sorted(products))
        rows.append({
            "N": n,
            "progressions": n,
            "terms_per_progression": n,
            "incidences": n * n,
            "distinct_union_points": len(products),
            "distinct_fraction": len(products) / (n * n),
            "all_targets_irredundant": True,
            "minimum_target": n,
            "maximum_target": 2 * n - 1,
            "minimum_step": n + 1,
            "maximum_step": 2 * n,
            "maximum_step_to_target_ratio": (n + 1) / n,
        })
    payload = {
        "schema_version": "erdos-25.multiplication-table-obstruction.v1",
        "status": "passed",
        "rows": rows,
        "largest_union_sha256": hashlib.sha256(final_encoded).hexdigest(),
        "proved_asymptotic_dependency": "The distinct fraction tends to zero by the Erdos multiplication-table theorem; Kevin Ford, Annals of Mathematics 168 (2008), DOI 10.4007/annals.2008.168.367.",
        "interpretation": "A scale-uniform quadratic one-generation packing bound is false even for target-irredundant r=d-1 batches with C<2.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "passed",
        "sizes": len(rows),
        "max_N": rows[-1]["N"],
        "last_distinct_fraction": rows[-1]["distinct_fraction"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
