#!/usr/bin/env python3
"""Independent finite sanity check for the minimal Hall-deficiency lemma."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def neighbourhood(rows: tuple[int, ...], colours: int) -> int:
    result = 0
    bit = 0
    while colours:
        if colours & 1:
            result |= rows[bit]
        colours >>= 1
        bit += 1
    return result


def main() -> None:
    graphs = 0
    minimal_deficient_sets = 0
    counterexamples: list[dict[str, object]] = []
    for colour_count in range(1, 5):
        for token_count in range(0, 5):
            edge_count = colour_count * token_count
            token_mask = (1 << token_count) - 1
            for graph_mask in range(1 << edge_count):
                graphs += 1
                rows = tuple(
                    (graph_mask >> (c * token_count)) & token_mask
                    for c in range(colour_count)
                )
                for colours in range(1, 1 << colour_count):
                    neighbours = neighbourhood(rows, colours)
                    size_s = colours.bit_count()
                    if neighbours.bit_count() >= size_s:
                        continue
                    is_minimal = True
                    proper = (colours - 1) & colours
                    while proper:
                        if neighbourhood(rows, proper).bit_count() < proper.bit_count():
                            is_minimal = False
                            break
                        proper = (proper - 1) & colours
                    if not is_minimal:
                        continue
                    minimal_deficient_sets += 1
                    deletion_stable = all(
                        neighbourhood(rows, colours ^ (1 << c)) == neighbours
                        for c in range(colour_count)
                        if colours & (1 << c)
                    )
                    degree_two = all(
                        sum(bool(rows[c] & (1 << token)) for c in range(colour_count) if colours & (1 << c)) >= 2
                        for token in range(token_count)
                        if neighbours & (1 << token)
                    )
                    if not (
                        neighbours.bit_count() == size_s - 1
                        and deletion_stable
                        and degree_two
                    ):
                        counterexamples.append(
                            {
                                "colour_count": colour_count,
                                "token_count": token_count,
                                "rows": rows,
                                "S": colours,
                                "N": neighbours,
                            }
                        )

    payload = {
        "classification": "finite_sanity_check_not_unbounded_evidence",
        "domain": "all bipartite incidence graphs with 1..4 colours and 0..4 tokens",
        "graphs_checked": graphs,
        "inclusion_minimal_deficient_sets_checked": minimal_deficient_sets,
        "counterexamples": counterexamples,
        "lemma_verified_in_domain": not counterexamples,
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    output = Path(__file__).with_name("tight_deficiency_finite_check.json")
    output.write_bytes(encoded)
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("output_sha256", hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
