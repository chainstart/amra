#!/usr/bin/env python3
"""Verify the KOU-21.137 candidate using only an exported Cayley table."""

from __future__ import annotations

import base64
import hashlib
import json
import math
import sys
import zlib
from typing import Any


CERTIFICATE_SCHEMA = "amra.kou-21.137.cayley-certificate.v1"
EXPECTED_CATALOG_ID = [128, 928]
EXPECTED_ORDER = 128
EXPECTED_EXPONENT = 8
SOURCE_STATEMENT = (
    "If the $p$-th powers in a finite $p$-group form a subgroup, must that "
    "subgroup be powerful? That is, for $p\\ne 2$, if the $p$-th powers in "
    "a $p$-group of exponent $p^2$ form a subgroup, must that subgroup be "
    "abelian? For a 2-group of exponent 8, if the squares form a subgroup, "
    "must that subgroup be abelian?"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("ascii")


def verify_export(export: dict[str, Any]) -> dict[str, Any]:
    require(export.get("schema") == "amra.cayley-export.v1", "unknown export schema")
    catalog = export.get("catalog")
    indexing = export.get("element_indexing")
    table = export.get("cayley_table")
    square_map = export.get("square_indices")
    require(isinstance(catalog, dict), "catalog metadata is missing")
    require(isinstance(indexing, dict), "element indexing metadata is missing")
    require(catalog.get("id") == EXPECTED_CATALOG_ID, "unexpected SmallGroups ID")
    require(indexing.get("count") == EXPECTED_ORDER, "unexpected element count")
    require(isinstance(table, list) and len(table) == EXPECTED_ORDER, "wrong table height")
    require(
        all(isinstance(row, list) and len(row) == EXPECTED_ORDER for row in table),
        "wrong table width",
    )
    require(
        all(
            isinstance(value, int) and 0 <= value < EXPECTED_ORDER
            for row in table
            for value in row
        ),
        "Cayley table contains an out-of-range index",
    )
    require(
        isinstance(square_map, list)
        and len(square_map) == EXPECTED_ORDER
        and all(
            isinstance(value, int) and 0 <= value < EXPECTED_ORDER
            for value in square_map
        ),
        "invalid square-index map",
    )

    def multiply(left: int, right: int) -> int:
        return table[left][right]

    identity_candidates = [
        candidate
        for candidate in range(EXPECTED_ORDER)
        if all(
            multiply(candidate, value) == value
            and multiply(value, candidate) == value
            for value in range(EXPECTED_ORDER)
        )
    ]
    require(len(identity_candidates) == 1, "the table does not have a unique identity")
    identity = identity_candidates[0]
    require(
        indexing.get("identity_index") == identity,
        "exported identity index disagrees with the table",
    )

    for left in range(EXPECTED_ORDER):
        for middle in range(EXPECTED_ORDER):
            left_middle = multiply(left, middle)
            for right in range(EXPECTED_ORDER):
                require(
                    multiply(left_middle, right)
                    == multiply(left, multiply(middle, right)),
                    f"associativity fails at ({left},{middle},{right})",
                )

    inverse_indices: list[int] = []
    for element in range(EXPECTED_ORDER):
        inverses = [
            candidate
            for candidate in range(EXPECTED_ORDER)
            if multiply(element, candidate) == identity
            and multiply(candidate, element) == identity
        ]
        require(len(inverses) == 1, f"element {element} lacks a unique two-sided inverse")
        inverse_indices.append(inverses[0])

    element_orders: list[int] = []
    for element in range(EXPECTED_ORDER):
        power = identity
        order = None
        for exponent in range(1, EXPECTED_ORDER + 1):
            power = multiply(power, element)
            if power == identity:
                order = exponent
                break
        require(order is not None, f"element {element} has no order at most 128")
        element_orders.append(order)
    exponent = math.lcm(*element_orders)
    require(exponent == EXPECTED_EXPONENT, f"group exponent is {exponent}, not 8")
    require(
        any(order == EXPECTED_EXPONENT for order in element_orders),
        "no element attains order 8",
    )
    order_cofactor = EXPECTED_ORDER
    order_2_valuation = 0
    while order_cofactor % 2 == 0:
        order_cofactor //= 2
        order_2_valuation += 1
    require(order_cofactor == 1, "group order is not a power of 2")

    diagonal_squares = [
        multiply(element, element) for element in range(EXPECTED_ORDER)
    ]
    require(square_map == diagonal_squares, "square map disagrees with table diagonal")
    square_set = sorted(set(square_map))
    require(identity in square_set, "identity is absent from the square set")

    multiplication_closed = all(
        multiply(left, right) in square_set
        for left in square_set
        for right in square_set
    )
    inverse_closed = all(inverse_indices[element] in square_set for element in square_set)
    require(multiplication_closed, "square set is not closed under multiplication")
    require(inverse_closed, "square set is not closed under inversion")

    generated = {identity}
    frontier = set(square_set)
    while frontier:
        generated.update(frontier)
        expanded = {
            multiply(left, right)
            for left in generated
            for right in generated
        }
        expanded.update(inverse_indices[element] for element in generated)
        frontier = expanded - generated
    require(
        generated == set(square_set),
        "square set differs from the subgroup it generates",
    )

    noncommuting_pair = None
    for left in square_set:
        for right in square_set:
            left_right = multiply(left, right)
            right_left = multiply(right, left)
            if left_right != right_left:
                noncommuting_pair = (left, right, left_right, right_left)
                break
        if noncommuting_pair is not None:
            break
    require(noncommuting_pair is not None, "square subgroup is abelian")
    left, right, left_right, right_left = noncommuting_pair
    left_preimage = square_map.index(left)
    right_preimage = square_map.index(right)

    canonical_export = canonical_json_bytes(export)
    compressed_export = zlib.compress(canonical_export, level=9)
    order_histogram = {
        str(order): element_orders.count(order) for order in sorted(set(element_orders))
    }
    return {
        "schema": CERTIFICATE_SCHEMA,
        "problem": {
            "problem_id": "unsolvedmath-kou-21.137",
            "source_id": "KOU-21.137",
            "source_url": "https://www.unsolvedmath.com/problems/KOU-21.137",
            "source_statement": SOURCE_STATEMENT,
            "source_page_sha256": (
                "9953da0dfbb22c9b6934429334fb27e795e0889f4b4a800669467d790eb94d30"
            ),
            "bank_content_fingerprint": (
                "130f1e813257c7a72dd4f35ea90f0bf4363f61232349f55aa2913798cf1fb617"
            ),
            "tested_subclaim": (
                "For a finite 2-group of exponent 8, if its set of squares "
                "is a subgroup, then that subgroup is abelian."
            ),
        },
        "candidate": {
            "catalog": catalog,
            "order": EXPECTED_ORDER,
            "prime": 2,
            "catalog_id": EXPECTED_CATALOG_ID,
        },
        "verification": {
            "implementation": (
                "standalone Python standard-library checker over the exported "
                "Cayley table; no AMRA executor/verifier imports"
            ),
            "group_axioms": {
                "closure": True,
                "associativity": True,
                "associativity_triples_checked": EXPECTED_ORDER**3,
                "unique_identity": True,
                "identity_index_zero_based": identity,
                "unique_two_sided_inverse_for_every_element": True,
                "inverse_count_checked": EXPECTED_ORDER,
            },
            "group_order": EXPECTED_ORDER,
            "group_order_is_power_of_2": True,
            "group_order_2_valuation": order_2_valuation,
            "element_order_histogram": order_histogram,
            "exponent": exponent,
            "has_element_of_order_8": True,
            "square_map_matches_table_diagonal": True,
            "square_set_size": len(square_set),
            "square_set_indices_zero_based": square_set,
            "square_set_multiplication_closed": multiplication_closed,
            "square_set_inverse_closed": inverse_closed,
            "generated_subgroup_size": len(generated),
            "square_set_equals_generated_subgroup": generated == set(square_set),
            "square_subgroup_abelian": False,
            "noncommuting_squares": {
                "left_square_index_zero_based": left,
                "right_square_index_zero_based": right,
                "left_times_right_index_zero_based": left_right,
                "right_times_left_index_zero_based": right_left,
                "left_square_preimage_index_zero_based": left_preimage,
                "right_square_preimage_index_zero_based": right_preimage,
                "left_preimage_squared_index_zero_based": square_map[left_preimage],
                "right_preimage_squared_index_zero_based": square_map[right_preimage],
            },
        },
        "conclusion": {
            "status": "verified_counterexample_to_explicit_subclaim",
            "statement": (
                "SmallGroup(128,928) is a 2-group of exponent exactly 8; its "
                "squares form a 16-element subgroup that is not abelian."
            ),
            "scope": (
                "This refutes the explicit exponent-8 2-group subclaim. It does "
                "not separately decide the broader powerful-subgroup question "
                "or the odd-prime exponent-p^2 subclaim."
            ),
        },
        "evidence_payload": {
            "format": "canonical JSON",
            "encoding": "zlib level 9 + base64",
            "uncompressed_bytes": len(canonical_export),
            "compressed_bytes": len(compressed_export),
            "uncompressed_sha256": hashlib.sha256(canonical_export).hexdigest(),
            "compressed_sha256": hashlib.sha256(compressed_export).hexdigest(),
            "data": base64.b64encode(compressed_export).decode("ascii"),
        },
    }


def main() -> int:
    try:
        export = json.load(sys.stdin)
        require(isinstance(export, dict), "top-level GAP export must be an object")
        certificate = verify_export(export)
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        return 1
    json.dump(certificate, sys.stdout, ensure_ascii=True, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
