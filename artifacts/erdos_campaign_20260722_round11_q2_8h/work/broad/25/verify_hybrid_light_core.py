#!/usr/bin/env python3
"""Finite exact regression for HYBRID_LIGHT_CORE_THEOREM.md.

This tests the pointwise inequality and density squeeze on random finite
systems and non-nested random cores.  It is not evidence for an asymptotic
hypothesis.
"""

from __future__ import annotations

from fractions import Fraction
import json
import random

from verify_log_clique_entropy import (
    clique_count,
    effective,
    full_density,
    is_active_survivor,
)


def main() -> None:
    rng = random.Random(2511072026)
    cases = 600
    sharpest_ratio = Fraction(0)
    for _ in range(cases):
        size = rng.randint(2, 8)
        moduli = tuple(sorted(rng.sample(range(2, 27), size)))
        residues = {modulus: rng.randrange(modulus) for modulus in moduli}
        cutoff = rng.randint(max(moduli), 5 * max(moduli) + 20)
        h = rng.randint(1, size)
        core = tuple(
            modulus for index, modulus in enumerate(moduli)
            if index < h or rng.randrange(2)
        )
        tail = tuple(modulus for modulus in moduli if modulus not in core)
        reduced_core = effective(core, residues)

        active_count = sum(
            is_active_survivor(value, moduli, residues)
            for value in range(1, cutoff + 1)
        )
        core_density = full_density(reduced_core, residues)
        kappa = clique_count(reduced_core, residues)
        tail_mass = sum((Fraction(1, modulus) for modulus in tail), Fraction(0))
        error = abs(Fraction(active_count, cutoff) - core_density)
        budget = tail_mass + Fraction(2 * kappa, cutoff)
        assert error <= budget

        full_system_density = full_density(moduli, residues)
        initial_density = full_density(moduli[:h], residues)
        assert full_system_density <= core_density <= initial_density
        if budget:
            sharpest_ratio = max(sharpest_ratio, error / budget)

    print(json.dumps({
        "schema": "amra.erdos25.hybrid-light-core.v1",
        "status": "PASS",
        "random_seed": 2511072026,
        "cases": cases,
        "checks": [
            "non-nested core contains a prescribed initial segment",
            "full activated count differs from core density by tail mass plus clique error",
            "finite full-system density is below core density",
            "core density is below initial-segment density",
        ],
        "maximum_error_over_budget": [
            sharpest_ratio.numerator,
            sharpest_ratio.denominator,
        ],
        "scope_warning": "Finite exact regression only; asymptotics are proved in markdown.",
    }, indent=2))


if __name__ == "__main__":
    main()
