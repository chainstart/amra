#!/usr/bin/env python3
"""Exactly close the small components of the first parametric cycles."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def load_search_engine():
    source = Path(__file__).with_name("search_bicyclic_components.py")
    spec = importlib.util.spec_from_file_location("r004_component_search", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    engine = load_search_engine()
    arithmetic = engine.Arithmetic(2_000_002)
    seeds = [
        273,
        5_293,
        24_485,
        39_783,
        1_244_919,
        2_457_013,
        4_029_489,
        4_799_379,
        5_389_035,
        8_984_469,
        9_279_291,
        15_580_867,
    ]
    globally_seen: set[int] = set()
    rows: list[dict[str, int]] = []
    for seed in seeds:
        if seed in globally_seen:
            continue
        vertices, edges = engine.closed_component(
            arithmetic, seed, safety_limit=100_000
        )
        globally_seen.update(vertices)
        cyclomatic = len(edges) - len(vertices) + 1
        assert cyclomatic == 1
        rows.append(
            {
                "seed": seed,
                "vertex_count": len(vertices),
                "edge_count": len(edges),
                "cyclomatic_number": cyclomatic,
                "minimum_vertex": min(vertices),
                "maximum_vertex": max(vertices),
            }
        )
    assert len(rows) == len(seeds)
    result = {
        "schema": "amra.erdos635.r004-targeted-cycle-components.v1",
        "status": "PASS",
        "components": rows,
        "bicyclic_components_found": 0,
        "completeness": (
            "Each listed seed's entire connected component was expanded by "
            "exact incident-edge inversion; no label cutoff was imposed."
        ),
        "scope": (
            "This closes only the twelve listed parametric-cycle components."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
