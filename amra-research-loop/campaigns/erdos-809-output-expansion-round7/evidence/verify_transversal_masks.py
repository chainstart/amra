#!/usr/bin/env python3
"""Direct sampled check of bitset transversal pruning equivalence."""

from itertools import combinations
from pathlib import Path
import runpy


m = runpy.run_path(str(Path(__file__).with_name("exchange_search.py")))


def direct_indices(eplus, deletion_sets, indices):
    result = {}
    for index in indices:
        deleted = deletion_sets[index]
        edges = frozenset(set(eplus) - set(deleted))
        result[index] = m["colour_pairs_safe"](m["adjacency"](edges))
    return result


def check(deletion_count: int, assignment_indices: tuple[int, ...], full: bool) -> None:
    choose_optional = 13 + deletion_count
    choices = tuple(combinations(m["OPTIONAL"], choose_optional))
    deletion_sets, bits_by_edge, all_bits = m["transversal_masks"](deletion_count)
    for assignment_index in assignment_indices:
        chosen = choices[assignment_index]
        eplus = frozenset(set(m["E0"]) | set(m["REQUIRED"]) | set(chosen))
        bits, _, _ = m["exact_hitting_sets"](
            m["adjacency"](eplus), bits_by_edge, all_bits
        )
        if full:
            indices = tuple(range(len(deletion_sets)))
        else:
            indices = tuple(sorted({
                0, len(deletion_sets) - 1,
                *(i * (len(deletion_sets) - 1) // 63 for i in range(64)),
            }))
        direct = direct_indices(eplus, deletion_sets, indices)
        for index, safe in direct.items():
            assert bool(bits & (1 << index)) == safe, (
                deletion_count, assignment_index, index
            )
        print(deletion_count, assignment_index, len(indices), bits.bit_count())


check(2, (0, 511, 3875), full=True)
# Index 964 is the unique triple-domain assignment without a protected C7;
# it is the most informative direct comparison.
check(3, (964,), full=False)
print("full binary and sampled triple direct delete-and-replay checks passed")
