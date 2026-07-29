from __future__ import annotations

from itertools import combinations

import pytest

from amra.discovery.opg611_orbit_cuts import (
    canonical_clause,
    map_orientation_clause,
    orbit_lift_packing_block_clause,
)
from amra.discovery.opg_coloring_search import EdgeGraph
from amra.discovery.opg_directed_cycles_search import (
    build_orientation_model,
    packing_block_clause,
)


def _transposition(order: int, left: int, right: int) -> tuple[int, ...]:
    permutation = list(range(order))
    permutation[left], permutation[right] = (
        permutation[right],
        permutation[left],
    )
    return tuple(permutation)


def _four_directed_triangles() -> tuple[tuple[tuple[int, int], ...], ...]:
    return tuple(
        (
            (offset, offset + 1),
            (offset + 1, offset + 2),
            (offset + 2, offset),
        )
        for offset in range(0, 12, 3)
    )


def _directed_arcs_from_block_clause(
    model: object,
    clause: tuple[int, ...],
) -> frozenset[tuple[int, int]]:
    variable_pairs = {
        variable: pair
        for pair, variable in model.arc_variables.items()  # type: ignore[attr-defined]
    }
    arcs = set()
    for literal in clause:
        # A packing block contains the negation of each required cycle arc.
        required = -literal
        left, right = variable_pairs[abs(required)]
        arcs.add((left, right) if required > 0 else (right, left))
    return frozenset(arcs)


def test_literal_orbit_maps_four_disjoint_cycles_safely() -> None:
    model = build_orientation_model(EdgeGraph(12, (), "K12 missing graph"))
    cycles = _four_directed_triangles()
    base = canonical_clause(packing_block_clause(model, cycles))
    swap = _transposition(12, 0, 3)
    image = map_orientation_clause(model, base, swap)
    expected_arcs = {
        (swap[source], swap[target])
        for cycle in cycles
        for source, target in cycle
    }
    assert _directed_arcs_from_block_clause(model, image) == expected_arcs
    assert len(image) == len(base) == 12

    vertex_sets = [
        {swap[vertex] for arc in cycle for vertex in arc}
        for cycle in cycles
    ]
    assert all(
        vertex_sets[first].isdisjoint(vertex_sets[second])
        for first, second in combinations(range(4), 2)
    )


def test_limit_can_resume_without_global_duplicates() -> None:
    model = build_orientation_model(EdgeGraph(12, (), "K12 missing graph"))
    base = packing_block_clause(model, _four_directed_triangles())
    generators = tuple(
        _transposition(12, vertex, vertex + 1)
        for vertex in range(11)
    )
    known: set[tuple[int, ...]] = set()

    first = orbit_lift_packing_block_clause(
        model,
        base,
        generators,
        known,
        limit=3,
    )
    second = orbit_lift_packing_block_clause(
        model,
        base,
        generators,
        known,
        limit=4,
    )
    assert len(first) == 3
    assert len(second) == 4
    assert set(first).isdisjoint(second)
    assert known == set(first) | set(second)

    before = set(known)
    assert (
        orbit_lift_packing_block_clause(
            model,
            base,
            generators,
            known,
            limit=0,
        )
        == ()
    )
    assert known == before


def test_known_clauses_are_canonicalized_for_global_deduplication() -> None:
    model = build_orientation_model(EdgeGraph(12, (), "K12 missing graph"))
    base = canonical_clause(
        packing_block_clause(model, _four_directed_triangles())
    )
    swap = _transposition(12, 0, 3)
    image = map_orientation_clause(model, base, swap)
    known = {tuple(reversed(base)), tuple(reversed(image))}
    generated = orbit_lift_packing_block_clause(
        model,
        base,
        (swap,),
        known,
        limit=5,
    )
    assert generated == ()


def test_invalid_generator_and_nonorientation_literal_are_rejected() -> None:
    missing = EdgeGraph(4, ((0, 1),), "one missing edge")
    model = build_orientation_model(missing)
    variable = next(iter(model.arc_variables.values()))
    bad_generator = _transposition(4, 1, 2)
    with pytest.raises(ValueError, match="not an automorphism"):
        orbit_lift_packing_block_clause(
            model,
            (-variable,),
            (bad_generator,),
            set(),
            limit=1,
        )
    with pytest.raises(ValueError, match="not an orientation variable"):
        orbit_lift_packing_block_clause(
            model,
            (max(model.arc_variables.values()) + 1,),
            (),
            set(),
            limit=1,
        )


def test_sign_flip_is_preserved_when_an_edge_endpoint_is_swapped() -> None:
    model = build_orientation_model(EdgeGraph(4, (), "K4 missing graph"))
    variable = model.arc_literal(0, 1)
    assert variable is not None and variable > 0
    swap = _transposition(4, 0, 1)
    assert map_orientation_clause(model, (variable,), swap) == (-variable,)
    assert map_orientation_clause(model, (-variable,), swap) == (variable,)
