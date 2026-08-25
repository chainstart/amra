#!/usr/bin/env python3
"""Selected exact guards for the actual-orbit B2 coupling in round 3.

This script deliberately does not scan a larger cutoff.  It guards exact
identities and the sharp actual wall V=300->301 only.
"""

from __future__ import annotations

from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from math import comb
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location("round2_guard", HERE / "verify_round2_rank14.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load round-2 arithmetic guard")
R2 = module_from_spec(SPEC)
SPEC.loader.exec_module(R2)


def upper(number: int, rank: int) -> int:
    return sum(
        comb(upper_index, lower + 1)
        for upper_index, lower in R2.canonical(number, rank)
    )


def suspension(number: int, rank: int) -> int:
    return number + upper(number, rank)


def actual_row(parameter: int) -> dict[str, int]:
    v = parameter
    n = v - 25
    e = R2.zero_seed_orbit(v, 26, 4)
    z3 = e[5] - comb(n - 1, 5) - comb(n - 2, 4)
    b2 = v + R2.kk(z3, 3)
    assert b2 == e[4] - comb(n - 1, 4) - comb(n - 2, 3)
    w14 = 27 + R2.kk(b2, 2)
    return {"V": v, "Z3": z3, "B2": b2, "W14": w14}


def sharp_wall() -> dict[str, object]:
    before = actual_row(300)
    after = actual_row(301)
    assert after["Z3"] - before["Z3"] == 2
    assert after["B2"] - before["B2"] == 3
    assert after["W14"] - before["W14"] == 0

    z = before["Z3"]
    z_next = after["Z3"]
    b = before["B2"]
    k = R2.kk(b, 2)
    z_cap = upper(R2.kk(z, 3) + 2, 2)
    assert z_next == z_cap
    delta_plus = max(0, z_next - z)
    assert 1 + 3 * delta_plus <= k

    diagonal_loss = suspension(b, 2) - z_next
    required_loss = suspension(b, 2) - z_cap
    assert diagonal_loss == required_loss
    return {
        "before": before,
        "after": after,
        "Delta_Z3": delta_plus,
        "Delta_B2": after["B2"] - before["B2"],
        "Delta_W14": after["W14"] - before["W14"],
        "rank3_Galois_cap": z_cap,
        "k_KK2_B2": k,
        "one_sided_sufficient_lhs": 1 + 3 * delta_plus,
        "diagonal_loss": diagonal_loss,
        "required_diagonal_loss": required_loss,
        "scope": "exact actual-orbit counterexample to Delta B2<=2 and equality case for the proposed Delta B2<=3 theorem",
    }


def exact_equivalence_guards() -> dict[str, int]:
    cases = 0
    for z in range(0, 301):
        shadow = R2.kk(z, 3)
        cap = upper(shadow + 2, 2)
        for z_next in range(0, 301):
            assert (R2.kk(z_next, 3) - shadow <= 2) == (z_next <= cap)
            cases += 1
    return {"checked_cases": cases}


def main() -> None:
    payload = {
        "status": "PASS",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "sharp_actual_wall": sharp_wall(),
        "rank3_galois_equivalence_guards": exact_equivalence_guards(),
        "scope": (
            "Exact identities and one exact actual counterexample to the stronger "
            "Delta B2<=2 claim. No bounded scan is used to assert Delta B2<=3."
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
