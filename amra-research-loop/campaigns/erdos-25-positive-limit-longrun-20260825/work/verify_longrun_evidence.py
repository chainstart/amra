#!/usr/bin/env python3
"""Mechanical replay of transient-amplifier certificates for Erdős #25."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

from search_positive_density_spikes import candidate_layer


def rebuild_stage(public: dict) -> dict:
    period = public["period"]
    survivor = bytearray(b"\x01") * period
    for modulus, residue in zip(public["moduli"], public["residues"]):
        survivor[residue:period:modulus] = b"\x00" * len(survivor[residue:period:modulus])
    count = survivor.count(1)
    assert count == public["survivor_count"]
    return {
        "period": period,
        "survivor": survivor,
        "survivor_count": count,
        "density": Fraction(count, period),
    }


def replay_block(document: Path, band: str) -> dict:
    payload = json.loads(document.read_text())
    record = payload["best_aggregate_by_minimum_previous_density"][band]
    public = record["previous_stage"]
    stored = record["block"]
    stage = rebuild_stage(public)
    replayed = []
    for layer in stored["layers"]:
        current = candidate_layer(stage, layer["modulus"], layer["residue"])
        assert current is not None
        for key in (
            "first_active_survivor",
            "compatible_previous_residues",
            "mixing_period",
            "eventual_density_numerator",
            "eventual_density_denominator",
        ):
            assert current[key] == layer[key]
        replayed.append(current)
    for left_index, left in enumerate(replayed):
        for right in replayed[left_index + 1:]:
            assert left["first_active_survivor"] % right["modulus"] != right["residue"]
            assert right["first_active_survivor"] % left["modulus"] != left["residue"]
    cutoff = max(layer["first_active_survivor"] for layer in replayed)
    harmonic = sum((Fraction(1, layer["first_active_survivor"]) for layer in replayed), Fraction())
    density_sum = sum((Fraction(layer["eventual_density_numerator"], layer["eventual_density_denominator"]) for layer in replayed), Fraction())
    amplification = float(harmonic) / math.log(cutoff) / float(density_sum)
    assert abs(amplification - stored["aggregate_amplification_lower_bound"]) < 1e-12
    return {
        "document": document.name,
        "previous_density": float(stage["density"]),
        "layer_count": len(replayed),
        "cutoff": cutoff,
        "aggregate_amplification_lower_bound": amplification,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    checks = []
    for power in range(2, 21):
        q = 1 << power
        first = 2 * q - 1
        density = Fraction(1, q * (q + 1))
        ratio = (1.0 / (first * math.log(first))) / float(density)
        checks.append({"kind": "power_tower", "Q": q, "first_active": first, "density_numerator": density.numerator, "density_denominator": density.denominator, "amplification": ratio})
    checks.extend(
        replay_block(args.campaign / "evidence" / filename, "0.1")
        for filename in (
            "positive_density_spike_search.json",
            "asymptotic_positive_density_spike_search.json",
            "asymptotic_offset_100000_spike_search.json",
        )
    )
    payload = {
        "schema_version": "erdos-25.longrun-replay.v1",
        "status": "passed",
        "checks": checks,
        "scope": "Mechanical replay only; not an independent mathematical audit."
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
