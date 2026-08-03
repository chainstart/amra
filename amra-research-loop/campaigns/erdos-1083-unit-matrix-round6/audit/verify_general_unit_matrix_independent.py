#!/usr/bin/env python3
"""Blind checker: constructs the matrices from the displayed equations only."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form


def fresh_matrices(m: int) -> tuple[Matrix, Matrix, list[str]]:
    # Column order is independently fixed here, not imported from author code.
    names = ["g", "f", "b"] + [f"r{i}" for i in range(m)] + [f"q{i}" for i in range(m)]
    pos = {name: j for j, name in enumerate(names)}

    def row(**terms: int) -> list[int]:
        out = [0] * len(names)
        for name, coefficient in terms.items():
            out[pos[name]] = coefficient
        return out

    source = [row(g=1, **{f"r{i}": 1}) for i in range(m)]
    fixed_f = [row(f=1)]
    complement = [row(f=1, **{f"q{i}": 1}) for i in range(m)]
    fixed_b = [row(g=1, b=1)]
    identity = [row(b=1, **{f"r{i}": -1, f"q{i}": -1}) for i in range(m)]
    full = Matrix(source + fixed_f + complement + fixed_b + identity)
    source_identity = Matrix(source + fixed_f + identity)
    return full, source_identity, names


def smith_diagonal(matrix: Matrix) -> list[int]:
    form = smith_normal_form(matrix, domain=ZZ)
    return [abs(int(form[i, i])) for i in range(min(form.rows, form.cols)) if form[i, i] != 0]


def verify_one(m: int) -> dict:
    full, source, names = fresh_matrices(m)
    g = names.index("g")
    b = names.index("b")
    full_minor = full[: 2 * m + 2, :]
    full_minor = full_minor[:, [j for j in range(len(names)) if j != g]]
    source_minor = source[:, [j for j in range(len(names)) if j not in (g, b)]]

    gauge = Matrix([1, 0, -1] + [-1] * m + [0] * m)
    shift = Matrix([0, 0, 1] + [0] * m + [1] * m)
    full_rank = full.rank()
    source_rank = source.rank()
    full_smith = smith_diagonal(full)
    source_smith = smith_diagonal(source)

    assert full_rank == 2 * m + 2
    assert source_rank == 2 * m + 1
    assert full_minor.det() in (-1, 1)
    assert source_minor.det() in (-1, 1)
    assert full * gauge == Matrix.zeros(full.rows, 1)
    assert source * gauge == Matrix.zeros(source.rows, 1)
    assert source * shift == Matrix.zeros(source.rows, 1)
    assert full * shift != Matrix.zeros(full.rows, 1)
    assert full_smith == [1] * full_rank
    assert source_smith == [1] * source_rank

    # The last m full rows are literal dependencies:
    # I_i = B - S_i - C_i + F.
    for i in range(m):
        source_i = full.row(i)
        fixed_f = full.row(m)
        complement_i = full.row(m + 1 + i)
        fixed_b = full.row(2 * m + 1)
        identity_i = full.row(2 * m + 2 + i)
        assert identity_i == fixed_b - source_i - complement_i + fixed_f

    # An extra unrecorded coefficient-unit coordinate is a concrete firewall:
    # the old primitive scalar block survives, but an additional kernel line does too.
    augmented = full.row_join(Matrix.zeros(full.rows, 1))
    assert augmented.rank() == full_rank
    assert len(augmented.nullspace()) == 2

    return {
        "m": m,
        "variables": len(names),
        "full_shape": list(full.shape),
        "full_rank": full_rank,
        "full_nullity": len(names) - full_rank,
        "full_unit_minor": int(full_minor.det()),
        "full_smith": full_smith,
        "source_shape": list(source.shape),
        "source_rank": source_rank,
        "source_nullity": len(names) - source_rank,
        "source_unit_minor": int(source_minor.det()),
        "source_smith": source_smith,
        "identity_dependencies_checked": m,
        "augmented_unrecorded_unit_nullity": len(augmented.nullspace()),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-m", type=int, default=12)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    rows = [verify_one(m) for m in range(1, args.max_m + 1)]
    result = {
        "schema": "amra.audit.erdos1083.general-unit-matrix-independent.v1",
        "construction": "fresh rows from equations; no author module or matrix function imported",
        "checked_m": [1, args.max_m],
        "results": rows,
        "conclusions": {
            "full": "rank 2m+2, primitive gauge line, every nonzero Smith factor 1",
            "source_identity": "rank 2m+1, primitive gauge plus spectrum-shift plane, every nonzero Smith factor 1",
            "ambient_firewall": "one unrecorded zero column preserves scalar primitivity but adds an independent kernel line",
        },
    }
    target = Path(args.output)
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print("output_sha256", hashlib.sha256(target.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
