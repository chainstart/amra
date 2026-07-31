#!/usr/bin/env python3
"""Exact finite audit of the adaptive forest-reserve theorem.

The theorem itself is proved by matroid intersection.  This program is an
independent small-instance guard: it compares the partition min--max
condition with direct enumeration of all coloured spanning trees and all
distinct-charge matchings.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from random import Random
from typing import Hashable, Iterable, Mapping, Sequence


Vertex = Hashable
Charge = Hashable
Edge = tuple[Vertex, Vertex]
Partition = tuple[frozenset[Vertex], ...]


def edge(x: Vertex, y: Vertex) -> Edge:
    if x == y:
        raise ValueError("loops are not base pairs")
    return tuple(sorted((x, y), key=repr))  # type: ignore[return-value]


@dataclass(frozen=True)
class Colour:
    vertices: tuple[Vertex, ...]
    reserves: Mapping[Edge, frozenset[Charge]]

    def __post_init__(self) -> None:
        expected = {
            edge(x, y) for x, y in combinations(self.vertices, 2)
        }
        if set(self.reserves) != expected:
            raise ValueError("reserves must be specified for every base pair")


def set_partitions(vertices: Sequence[Vertex]) -> tuple[Partition, ...]:
    """Generate every unlabelled set partition exactly once."""

    if not vertices:
        return ((),)
    first = vertices[0]
    result: list[Partition] = []
    for tail_partition in set_partitions(vertices[1:]):
        result.append((frozenset((first,)),) + tail_partition)
        for index in range(len(tail_partition)):
            blocks = list(tail_partition)
            blocks[index] = blocks[index] | {first}
            result.append(tuple(blocks))
    return tuple(result)


def cross_edges(partition: Partition) -> frozenset[Edge]:
    block_of = {
        vertex: block_index
        for block_index, block in enumerate(partition)
        for vertex in block
    }
    return frozenset(
        edge(x, y)
        for x, y in combinations(block_of, 2)
        if block_of[x] != block_of[y]
    )


def spanning_trees(vertices: Sequence[Vertex]) -> tuple[tuple[Edge, ...], ...]:
    """Enumerate all spanning trees by the defining forest condition."""

    if len(vertices) <= 1:
        return ((),)
    pairs = tuple(edge(x, y) for x, y in combinations(vertices, 2))
    answer: list[tuple[Edge, ...]] = []
    for candidate in combinations(pairs, len(vertices) - 1):
        parent = {vertex: vertex for vertex in vertices}

        def find(vertex: Vertex) -> Vertex:
            while parent[vertex] != vertex:
                parent[vertex] = parent[parent[vertex]]
                vertex = parent[vertex]
            return vertex

        acyclic = True
        for x, y in candidate:
            root_x, root_y = find(x), find(y)
            if root_x == root_y:
                acyclic = False
                break
            parent[root_x] = root_y
        if acyclic:
            answer.append(candidate)
    return tuple(answer)


def has_distinct_representatives(options: Iterable[frozenset[Charge]]) -> bool:
    """Test whether the option sets have a system of distinct representatives."""

    candidate_sets = sorted((set(option) for option in options), key=len)
    charge_to_token: dict[Charge, int] = {}

    def augment(token: int, seen: set[Charge]) -> bool:
        for charge in candidate_sets[token]:
            if charge in seen:
                continue
            seen.add(charge)
            previous = charge_to_token.get(charge)
            if previous is None or augment(previous, seen):
                charge_to_token[charge] = token
                return True
        return False

    return all(augment(token, set()) for token in range(len(candidate_sets)))


def adaptive_feasible(colours: Sequence[Colour]) -> bool:
    """Directly enumerate tree choices, then solve the charge matching."""

    tree_families = [spanning_trees(colour.vertices) for colour in colours]
    for trees in product(*tree_families):
        options = [
            colours[colour_index].reserves[base_pair]
            for colour_index, tree in enumerate(trees)
            for base_pair in tree
        ]
        if has_distinct_representatives(options):
            return True
    return False


def global_defect(colours: Sequence[Colour]) -> int:
    return sum(max(len(colour.vertices) - 1, 0) for colour in colours)


def global_reserve_union(colours: Sequence[Colour]) -> frozenset[Charge]:
    return frozenset(
        charge
        for colour in colours
        for reserve in colour.reserves.values()
        for charge in reserve
    )


def global_union_closes(colours: Sequence[Colour]) -> bool:
    return len(global_reserve_union(colours)) >= global_defect(colours)


def partition_condition(colours: Sequence[Colour]) -> bool:
    """Evaluate every partition-family inequality in Theorem 3.1."""

    partition_families = [set_partitions(colour.vertices) for colour in colours]
    for partitions in product(*partition_families):
        union: set[Charge] = set()
        debt = 0
        for colour, partition in zip(colours, partitions):
            debt += max(len(partition) - 1, 0)
            for base_pair in cross_edges(partition):
                union.update(colour.reserves[base_pair])
        if len(union) < debt:
            return False
    return True


def partition_union(
    colours: Sequence[Colour], partitions: Sequence[Partition]
) -> frozenset[Charge]:
    union: set[Charge] = set()
    for colour, partition in zip(colours, partitions):
        for base_pair in cross_edges(partition):
            union.update(colour.reserves[base_pair])
    return frozenset(union)


def minimum_debt_obstruction(
    colours: Sequence[Colour],
) -> tuple[tuple[Partition, ...], frozenset[Charge]] | None:
    """Return a violating partition family of minimum positive debt."""

    partition_families = [set_partitions(colour.vertices) for colour in colours]
    candidates = []
    for partitions in product(*partition_families):
        debt = sum(max(len(partition) - 1, 0) for partition in partitions)
        union = partition_union(colours, partitions)
        if len(union) < debt:
            candidates.append((debt, partitions, union))
    if not candidates:
        return None
    _, partitions, union = min(candidates, key=lambda item: item[0])
    return tuple(partitions), union


def check_minimal_obstruction_rigidity(colours: Sequence[Colour]) -> bool:
    """Audit the unit-deficiency and merge-redundancy conclusions."""

    obstruction = minimum_debt_obstruction(colours)
    if obstruction is None:
        return True
    partitions, union = obstruction
    debt = sum(max(len(partition) - 1, 0) for partition in partitions)
    if all(reserve for colour in colours for reserve in colour.reserves.values()):
        assert debt >= 2
    assert len(union) == debt - 1
    for colour_index, partition in enumerate(partitions):
        for left, right in combinations(range(len(partition)), 2):
            merged_block = partition[left] | partition[right]
            merged = tuple(
                block
                for index, block in enumerate(partition)
                if index not in (left, right)
            ) + (merged_block,)
            coarsened = list(partitions)
            coarsened[colour_index] = merged
            assert partition_union(colours, coarsened) == union
    return True


def fixed_star_feasible(colours: Sequence[Colour], roots: Sequence[Vertex]) -> bool:
    """Test the older construction after fixing one root for each colour."""

    options = [
        colour.reserves[edge(root, vertex)]
        for colour, root in zip(colours, roots)
        for vertex in colour.vertices
        if vertex != root
    ]
    return has_distinct_representatives(options)


def strict_separation_instance() -> tuple[Colour, ...]:
    """One colour where a path works but every fixed root-star fails."""

    vertices = (1, 2, 3, 4)
    reserves = {
        edge(1, 2): frozenset({"a"}),
        edge(1, 3): frozenset({"b"}),
        edge(1, 4): frozenset({"a"}),
        edge(2, 3): frozenset({"b"}),
        edge(2, 4): frozenset({"a"}),
        edge(3, 4): frozenset({"c"}),
    }
    return (Colour(vertices, reserves),)


def global_over_adaptive_instance() -> tuple[Colour, ...]:
    """Global counting closes although the adaptive-tree criterion fails."""

    vertices = (1, 2, 3, 4)
    reserves = {
        edge(1, 2): frozenset({"b", "c"}),
        edge(1, 3): frozenset({"a"}),
        edge(1, 4): frozenset({"a"}),
        edge(2, 3): frozenset({"a"}),
        edge(2, 4): frozenset({"a"}),
        edge(3, 4): frozenset({"a"}),
    }
    return (Colour(vertices, reserves),)


def base_only_instance(order: int, multiplicity: int) -> tuple[Colour, ...]:
    vertices = tuple(range(order))
    reserves = {
        edge(x, y): frozenset({edge(x, y)})
        for x, y in combinations(vertices, 2)
    }
    return tuple(Colour(vertices, reserves) for _ in range(multiplicity))


def exhaustive_tiny_audit() -> int:
    """Exhaust three complete finite model classes."""

    checks = 0
    charge_subsets = tuple(
        frozenset(combination)
        for size in range(1, 3)
        for combination in combinations(("a", "b"), size)
    )

    # One triangle, arbitrary nonempty reserves in a two-charge universe.
    triangle_pairs = tuple(combinations((0, 1, 2), 2))
    for choices in product(charge_subsets, repeat=len(triangle_pairs)):
        reserves = {
            edge(*base_pair): reserve
            for base_pair, reserve in zip(triangle_pairs, choices)
        }
        colours = (Colour((0, 1, 2), reserves),)
        assert adaptive_feasible(colours) == partition_condition(colours)
        checks += 1

    # Two independent two-vertex colours sharing the same charge universe.
    for left, right in product(charge_subsets, repeat=2):
        colours = (
            Colour((0, 1), {edge(0, 1): left}),
            Colour((2, 3), {edge(2, 3): right}),
        )
        assert adaptive_feasible(colours) == partition_condition(colours)
        checks += 1

    # One K4 with singleton reserves in a two-charge universe.
    k4_pairs = tuple(combinations((0, 1, 2, 3), 2))
    for choices in product(("a", "b"), repeat=len(k4_pairs)):
        reserves = {
            edge(*base_pair): frozenset({charge})
            for base_pair, charge in zip(k4_pairs, choices)
        }
        colours = (Colour((0, 1, 2, 3), reserves),)
        assert adaptive_feasible(colours) == partition_condition(colours)
        checks += 1
    return checks


def random_audit(seed: int = 809, instances: int = 1000) -> int:
    rng = Random(seed)
    universe = tuple("abcd")
    for _ in range(instances):
        colour_count = rng.randint(1, 3)
        colours: list[Colour] = []
        for colour_index in range(colour_count):
            order = rng.randint(2, 4)
            vertices = tuple((colour_index, index) for index in range(order))
            reserves = {}
            for x, y in combinations(vertices, 2):
                reserve = frozenset(
                    charge for charge in universe if rng.random() < 0.5
                )
                reserves[edge(x, y)] = reserve
            colours.append(Colour(vertices, reserves))
        assert adaptive_feasible(colours) == partition_condition(colours)
    return instances


def rigidity_audit(seed: int = 810, instances: int = 300) -> int:
    rng = Random(seed)
    universe = tuple("abc")
    obstructions = 0
    for _ in range(instances):
        colours = []
        for colour_index in range(rng.randint(1, 3)):
            order = rng.randint(2, 4)
            vertices = tuple((colour_index, index) for index in range(order))
            reserves = {}
            for x, y in combinations(vertices, 2):
                reserve = frozenset(
                    charge for charge in universe if rng.random() < 0.45
                )
                reserves[edge(x, y)] = reserve or frozenset({rng.choice(universe)})
            colours.append(Colour(vertices, reserves))
        if minimum_debt_obstruction(colours) is not None:
            obstructions += 1
        assert check_minimal_obstruction_rigidity(colours)
    assert obstructions > 0
    return obstructions


def run() -> dict[str, object]:
    strict = strict_separation_instance()
    assert adaptive_feasible(strict)
    assert partition_condition(strict)
    assert all(
        not fixed_star_feasible(strict, roots)
        for roots in product(*(colour.vertices for colour in strict))
    )

    global_strict = global_over_adaptive_instance()
    assert global_union_closes(global_strict)
    assert not adaptive_feasible(global_strict)
    assert not partition_condition(global_strict)

    # Nash-Williams' familiar complete-graph thresholds appear as guards.
    assert adaptive_feasible(base_only_instance(4, 2))
    assert not adaptive_feasible(base_only_instance(4, 3))
    assert adaptive_feasible(base_only_instance(5, 2))
    assert not adaptive_feasible(base_only_instance(5, 3))

    tiny_checks = exhaustive_tiny_audit()
    random_checks = random_audit()
    rigidity_obstructions = rigidity_audit()
    return {
        "schema": "amra.erdos809.adaptive-forest-reserve.v1",
        "exact_tiny_instances": tiny_checks,
        "deterministic_random_instances": random_checks,
        "strict_fixed_root_separation": "PASS",
        "strict_global_over_adaptive_separation": "PASS",
        "base_only_tree_packing_guards": "PASS",
        "minmax_equivalence": "PASS",
        "minimal_obstruction_rigidity": "PASS",
        "rigidity_obstructions_checked": rigidity_obstructions,
        "status": "PASS",
        "boundary": "finite audit only; theorem proof is matroid intersection",
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))
