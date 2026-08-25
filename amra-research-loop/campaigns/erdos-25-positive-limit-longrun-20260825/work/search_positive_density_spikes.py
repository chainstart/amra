#!/usr/bin/env python3
"""Exact finite search for aggregate onset spikes over positive-density stages."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import time
from fractions import Fraction
from pathlib import Path


DENSITY_BANDS = (Fraction(1, 100), Fraction(1, 20), Fraction(1, 10), Fraction(1, 4))


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def random_previous_stage(rng: random.Random, period_cap: int) -> dict:
    moduli: list[int] = []
    residues: list[int] = []
    period = 1
    candidates = list(range(2, 81))
    rng.shuffle(candidates)
    for modulus in candidates:
        if len(moduli) >= rng.randint(5, 12):
            break
        new_period = math.lcm(period, modulus)
        if new_period > period_cap:
            continue
        moduli.append(modulus)
        residues.append(rng.randrange(modulus))
        period = new_period
    order = sorted(range(len(moduli)), key=moduli.__getitem__)
    moduli = [moduli[index] for index in order]
    residues = [residues[index] for index in order]
    survivor = bytearray(b"\x01") * period
    for modulus, residue in zip(moduli, residues):
        survivor[residue:period:modulus] = b"\x00" * len(survivor[residue:period:modulus])
    count = survivor.count(1)
    return {
        "moduli": moduli,
        "residues": residues,
        "period": period,
        "survivor": survivor,
        "survivor_count": count,
        "density": Fraction(count, period),
    }


def candidate_layer(stage: dict, modulus: int, residue: int) -> dict | None:
    period = stage["period"]
    survivor = stage["survivor"]
    gcd = math.gcd(period, modulus)
    compatible = sum(survivor[index] for index in range(residue % gcd, period, gcd))
    if compatible == 0:
        return None
    mixing_period = math.lcm(period, modulus)
    eventual_density = Fraction(compatible, mixing_period)
    point = residue
    if point < modulus:
        point += ((modulus - point + modulus - 1) // modulus) * modulus
    for _ in range(period // gcd + 1):
        if survivor[point % period]:
            break
        point += modulus
    else:
        raise AssertionError("CRT-compatible layer had no point in one mixing period")
    normalised_spike = 1.0 / (point * math.log(max(3, point)))
    return {
        "modulus": modulus,
        "residue": residue,
        "first_active_survivor": point,
        "compatible_previous_residues": compatible,
        "mixing_period": mixing_period,
        "eventual_density_numerator": eventual_density.numerator,
        "eventual_density_denominator": eventual_density.denominator,
        "individual_amplification": normalised_spike / float(eventual_density),
    }


def isolated(left: dict, right: dict) -> bool:
    return (
        left["first_active_survivor"] % right["modulus"] != right["residue"]
        and right["first_active_survivor"] % left["modulus"] != left["residue"]
    )


def pack_layers(candidates: list[dict], rng: random.Random) -> dict | None:
    best: dict | None = None
    orderings = [sorted(candidates, key=lambda item: item["individual_amplification"], reverse=True)]
    for _ in range(12):
        shuffled = candidates.copy()
        rng.shuffle(shuffled)
        orderings.append(shuffled)
    for ordering in orderings:
        selected: list[dict] = []
        used_moduli: set[int] = set()
        for candidate in ordering:
            if candidate["modulus"] in used_moduli:
                continue
            if all(isolated(candidate, previous) for previous in selected):
                selected.append(candidate)
                used_moduli.add(candidate["modulus"])
            if len(selected) < 2:
                continue
            cutoff = max(item["first_active_survivor"] for item in selected)
            harmonic = sum(Fraction(1, item["first_active_survivor"]) for item in selected)
            density_sum = sum(
                (Fraction(item["eventual_density_numerator"], item["eventual_density_denominator"]) for item in selected),
                Fraction(0, 1),
            )
            normalised_harmonic = float(harmonic) / math.log(max(3, cutoff))
            amplification_lower_bound = normalised_harmonic / float(density_sum)
            record = {
                "layers": sorted(selected, key=lambda item: item["modulus"]),
                "layer_count": len(selected),
                "cutoff": cutoff,
                "harmonic_target_mass_numerator": harmonic.numerator,
                "harmonic_target_mass_denominator": harmonic.denominator,
                "sum_eventual_density_numerator": density_sum.numerator,
                "sum_eventual_density_denominator": density_sum.denominator,
                "normalised_harmonic_target_mass": normalised_harmonic,
                "aggregate_amplification_lower_bound": amplification_lower_bound,
                "certificate_logic": "Targets lie in the previous survivor and are pairwise excluded from every other selected class; union density is at most the sum of individual densities.",
            }
            if best is None or record["aggregate_amplification_lower_bound"] > best["aggregate_amplification_lower_bound"]:
                best = record
    return best


def public_stage(stage: dict) -> dict:
    survivor = stage["survivor"]
    return {
        "moduli": stage["moduli"],
        "residues": stage["residues"],
        "period": stage["period"],
        "survivor_count": stage["survivor_count"],
        "density_numerator": stage["density"].numerator,
        "density_denominator": stage["density"].denominator,
        "survivor_sha256": hashlib.sha256(survivor).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=2700)
    parser.add_argument("--seed", type=int, default=250825)
    parser.add_argument("--period-cap", type=int, default=250000)
    parser.add_argument("--candidate-moduli", type=int, default=90)
    parser.add_argument("--candidate-offset", type=int, default=0)
    parser.add_argument("--residues-per-modulus", type=int, default=8)
    parser.add_argument("--checkpoint-seconds", type=int, default=300)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    started_wall = time.time()
    started = time.monotonic()
    deadline = started + args.seconds
    next_checkpoint = started + min(args.checkpoint_seconds, args.seconds)
    next_report = started + 60
    stages = candidates_tested = blocks = 0
    best_by_band: dict[str, dict | None] = {str(float(band)): None for band in DENSITY_BANDS}
    best_individual: dict | None = None

    def snapshot(status: str) -> dict:
        elapsed = time.monotonic() - started
        return {
            "schema_version": "erdos-25.positive-density-spikes.v1",
            "status": status,
            "guard_required": True,
            "seed": args.seed,
            "period_cap": args.period_cap,
            "candidate_offset": args.candidate_offset,
            "requested_seconds": args.seconds,
            "started_unix": started_wall,
            "elapsed_seconds": elapsed,
            "stages": stages,
            "candidates_tested": candidates_tested,
            "pairwise_isolated_blocks": blocks,
            "best_individual": best_individual,
            "best_aggregate_by_minimum_previous_density": best_by_band,
            "interpretation_limit": "Finite aggregate certificates test transient amplification; they do not create an infinite logarithmic-density counterexample."
        }

    while time.monotonic() < deadline:
        stage = random_previous_stage(rng, args.period_cap)
        stages += 1
        if stage["survivor_count"] == 0 or not stage["moduli"]:
            continue
        start_modulus = max(stage["moduli"]) + 1 + args.candidate_offset
        candidate_records: list[dict] = []
        for modulus in range(start_modulus, start_modulus + args.candidate_moduli):
            residues = rng.sample(range(modulus), min(args.residues_per_modulus, modulus))
            for residue in residues:
                candidate = candidate_layer(stage, modulus, residue)
                candidates_tested += 1
                if candidate is None:
                    continue
                candidate_records.append(candidate)
                if best_individual is None or candidate["individual_amplification"] > best_individual["layer"]["individual_amplification"]:
                    best_individual = {"previous_stage": public_stage(stage), "layer": candidate}
        packed = pack_layers(candidate_records, rng)
        if packed is not None:
            blocks += 1
            for band in DENSITY_BANDS:
                if stage["density"] < band:
                    continue
                key = str(float(band))
                current = best_by_band[key]
                if current is None or packed["aggregate_amplification_lower_bound"] > current["block"]["aggregate_amplification_lower_bound"]:
                    best_by_band[key] = {"previous_stage": public_stage(stage), "block": packed}

        now = time.monotonic()
        if now >= next_checkpoint:
            atomic_json(args.output, snapshot("running"))
            next_checkpoint = now + args.checkpoint_seconds
        if now >= next_report:
            best_dense = best_by_band[str(float(Fraction(1, 10)))]
            print(json.dumps({"elapsed_seconds": round(now-started, 1), "stages": stages, "candidates_tested": candidates_tested, "best_aggregate_density_ge_0.1": None if best_dense is None else best_dense["block"]["aggregate_amplification_lower_bound"]}, sort_keys=True), flush=True)
            next_report = now + 60

    payload = snapshot("completed") | {"completed_unix": time.time()}
    atomic_json(args.output, payload)
    print(json.dumps({"status": "completed", "elapsed_seconds": payload["elapsed_seconds"], "stages": stages, "candidates_tested": candidates_tested}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
