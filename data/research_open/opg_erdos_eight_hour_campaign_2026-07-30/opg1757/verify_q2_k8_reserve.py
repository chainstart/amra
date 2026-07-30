#!/usr/bin/env python3
"""Compact-CSR finite audit of the final q=2 layer k=8."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from independent_verify_multiedge_and_k6 import (
    all_forests_by_size,
    direct_single_targets,
    enumerate_layer,
    matching_hash,
    reserve_targets,
)
from verify_q2_k7_reserve import (
    CompactCSR,
    augment,
    compact_adjacency_hash,
    degree_profile,
    hall_witness,
)


K = 8
CONSERVATIVE_MAXIMUM_ROW_DEGREE = 126


def prior_layer_coverage() -> list[dict[str, object]]:
    directory = Path(__file__).resolve().parent
    global_saved = json.loads(
        (directory / "global_cycle_opening_certificate.json").read_text(
            encoding="utf-8"
        )
    )
    rows: list[dict[str, object]] = []
    for layer in global_saved["q2_finite_audit"]["layer_rows"]:
        if layer["k"] > 4:
            continue
        if (
            layer["direct_or_single_exchange_matching_size"]
            != layer["negative_count"]
        ):
            raise AssertionError("saved base layer is not fully matched")
        rows.append(
            {
                "k": layer["k"],
                "negative_count": layer["negative_count"],
                "matching_size": (
                    layer["direct_or_single_exchange_matching_size"]
                ),
                "deficiency": 0,
                "move_family": "direct_or_single",
                "certificate": "global_cycle_opening_certificate.json",
                "certificate_payload_sha256": (
                    global_saved["sha256_payload"]
                ),
            }
        )

    for k, filename in (
        (5, "multiedge_recoloring_attack_certificate.json"),
        (6, "q2_k6_extension_certificate.json"),
        (7, "q2_k7_extension_certificate.json"),
    ):
        saved = json.loads(
            (directory / filename).read_text(encoding="utf-8")
        )
        layer = saved["layer"]
        if (
            layer["k"] != k
            or layer["expanded_matching_size"] != layer["negative_count"]
            or layer["expanded_deficiency"] != 0
        ):
            raise AssertionError(f"saved k={k} layer is not fully matched")
        rows.append(
            {
                "k": k,
                "negative_count": layer["negative_count"],
                "matching_size": layer["expanded_matching_size"],
                "deficiency": layer["expanded_deficiency"],
                "move_family": "reserve_expanded",
                "certificate": filename,
                "certificate_payload_sha256": saved["sha256_payload"],
            }
        )
    if [row["k"] for row in rows] != list(range(1, 8)):
        raise AssertionError("prior q=2 layer coverage is incomplete")
    return rows


def build_audit() -> dict[str, object]:
    forests_by_size, forest_set = all_forests_by_size()
    positives, negatives = enumerate_layer(forests_by_size, K)
    positive_index = {
        pair: index for index, pair in enumerate(positives)
    }

    # Before constructing the graph: two forests have ten edge copies.
    # Protecting red E and blue F leaves at most eight outgoing reserve
    # choices; each tests 15 incoming K6 edges.  Add at most six direct/
    # single candidates.  This deliberately loose bound gives 126.
    estimated_expanded_csr_upper_bound = (
        (len(negatives) + 1) * 8
        + len(negatives) * CONSERVATIVE_MAXIMUM_ROW_DEGREE * 4
    )

    base = CompactCSR()
    expanded = CompactCSR()
    for source in negatives:
        base_targets = direct_single_targets(source, positive_index)
        reserves = reserve_targets(source, positive_index, forest_set)
        base.append(sorted(base_targets))
        expanded.append(sorted(base_targets | set(reserves)))

    base_source, base_target, base_match = augment(
        base, len(positives)
    )
    hall_sources, hall_targets = hall_witness(
        base, base_source, base_target
    )
    expanded_source, expanded_target, completion = augment(
        expanded,
        len(positives),
        initial=(base_source, base_target),
        base=base,
    )
    if completion["matching_size"] != len(negatives):
        expanded_hall = hall_witness(
            expanded, expanded_source, expanded_target
        )
    else:
        expanded_hall = (0, 0)

    payload = {
        "scope": (
            "Complete final q=2 layer k=8 on K6, using every valid direct/"
            "single E exchange and every protected one-basis reserve after "
            "deterministic global opening."
        ),
        "model_range": {
            "maximum_forest_size_on_six_vertices": 5,
            "total_colored_copies": K + 2,
            "maximum_possible_k": 8,
        },
        "prior_certified_layers": prior_layer_coverage(),
        "layer": {
            "k": K,
            "negative_count": len(negatives),
            "positive_count": len(positives),
            "direct_or_single_edge_count": base.edge_count,
            "direct_or_single_adjacency_sha256": (
                compact_adjacency_hash(base)
            ),
            "direct_or_single_degree_profile": degree_profile(
                base, len(positives)
            ),
            "direct_or_single_matching_size": (
                base_match["matching_size"]
            ),
            "direct_or_single_matching_sha256": matching_hash(
                base_source
            ),
            "direct_or_single_deficiency": (
                len(negatives) - int(base_match["matching_size"])
            ),
            "direct_or_single_hall_source_count": hall_sources,
            "direct_or_single_hall_target_count": hall_targets,
            "expanded_edge_count": expanded.edge_count,
            "expanded_adjacency_sha256": (
                compact_adjacency_hash(expanded)
            ),
            "expanded_degree_profile": degree_profile(
                expanded, len(positives)
            ),
            "expanded_matching_size": completion["matching_size"],
            "expanded_matching_sha256": matching_hash(expanded_source),
            "expanded_deficiency": (
                len(negatives) - int(completion["matching_size"])
            ),
            "expanded_hall_source_count": expanded_hall[0],
            "expanded_hall_target_count": expanded_hall[1],
            "base_to_expanded_completion": completion,
        },
        "resource_accounting": {
            "preconstruction_maximum_candidate_degree_bound": (
                CONSERVATIVE_MAXIMUM_ROW_DEGREE
            ),
            "preconstruction_expanded_csr_upper_bound_bytes": (
                estimated_expanded_csr_upper_bound
            ),
            "representation": (
                "uint64 row offsets plus uint32 target indices"
            ),
            "base_csr_bytes": base.storage_bytes,
            "expanded_csr_bytes": expanded.storage_bytes,
            "combined_csr_bytes": (
                base.storage_bytes + expanded.storage_bytes
            ),
            "python_list_adjacency_not_materialized": True,
        },
    }
    return {
        "schema": "amra.opg1757.q2_k8_extension.v1",
        "claim_labels": {
            "q2_k8_candidate_graph_completeness": "finite_exhaustion",
            "q2_k8_expanded_untagged_injection": "finite_evidence",
            "q2_all_possible_k_computationally_certified": (
                "finite_evidence_in_current_model"
            ),
            "q2_uniform_symbolic_hall_theorem": "open_gap",
            "full_first_coefficient_positivity": "open_gap",
        },
        **payload,
        "sha256_payload": hashlib.sha256(
            json.dumps(
                payload, separators=(",", ":"), sort_keys=True
            ).encode()
        ).hexdigest(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name(
            "q2_k8_extension_certificate.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    audit = build_audit()
    args.output.write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    print(f"CERTIFICATE|sha256={audit['sha256_payload']}")


if __name__ == "__main__":
    main()
