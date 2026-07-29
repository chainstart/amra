from __future__ import annotations

import itertools

import pytest

from amra.discovery.opg611_symmetry import (
    add_pack_color_minimum_order_clauses,
    add_unit_arc_clauses,
    build_unit_arc_symmetry_plan,
    compose_permutations,
    dreadnaut_automorphism_generators,
    identity_permutation,
    inverse_permutation,
    is_missing_graph_automorphism,
    point_stabilizer_generators,
    verify_unit_arc_symmetry_plan,
)
from amra.discovery.opg_coloring_search import CNF, EdgeGraph
from amra.discovery.opg_directed_cycles_search import build_orientation_model
from amra.discovery.opg_directed_cycles_search import (
    extract_cycle_packing,
    pack_four_cycles_cnf,
    solve_incremental_once,
)


def _transposition(order: int, left: int, right: int) -> tuple[int, ...]:
    permutation = list(range(order))
    permutation[left], permutation[right] = (
        permutation[right],
        permutation[left],
    )
    return tuple(permutation)


def _all_permutations(order: int) -> tuple[tuple[int, ...], ...]:
    return tuple(itertools.permutations(range(order)))


def _transform_orientation(
    edges: tuple[tuple[int, int], ...],
    values: tuple[bool, ...],
    permutation: tuple[int, ...],
) -> tuple[bool, ...]:
    directions = {
        (left, right) if value else (right, left)
        for (left, right), value in zip(edges, values)
    }
    image = {
        (permutation[source], permutation[target])
        for source, target in directions
    }
    return tuple((left, right) in image for left, right in edges)


def test_permutation_composition_and_schreier_stabilizer() -> None:
    generators = (
        _transposition(4, 0, 1),
        _transposition(4, 1, 2),
        _transposition(4, 2, 3),
    )
    stabilizer = point_stabilizer_generators(generators, 0, 4)
    assert stabilizer
    assert all(generator[0] == 0 for generator in stabilizer)
    assert any(generator[1] == 2 and generator[2] == 1 for generator in stabilizer)
    for generator in generators:
        assert compose_permutations(
            generator, inverse_permutation(generator)
        ) == identity_permutation(4)


def test_sequential_unit_plan_preserves_one_representative_per_orbit() -> None:
    missing = EdgeGraph(4, (), "empty-missing")
    generators = (
        _transposition(4, 0, 1),
        _transposition(4, 1, 2),
        _transposition(4, 2, 3),
    )
    plan = build_unit_arc_symmetry_plan(missing, generators)
    assert len(plan.units) == 2
    assert verify_unit_arc_symmetry_plan(missing, plan)

    allowed = tuple(itertools.combinations(range(4), 2))
    forced = {(unit.left, unit.right): False for unit in plan.units}
    for values in itertools.product((False, True), repeat=len(allowed)):
        orbit = (
            _transform_orientation(allowed, values, permutation)
            for permutation in _all_permutations(4)
        )
        assert any(
            all(
                image[allowed.index(edge)] is required
                for edge, required in forced.items()
            )
            for image in orbit
        )


def test_unit_plan_rejects_a_nonautomorphism() -> None:
    missing = EdgeGraph(4, ((0, 1),), "single-edge")
    bad = _transposition(4, 1, 2)
    assert not is_missing_graph_automorphism(missing, bad)
    with pytest.raises(ValueError, match="not an automorphism"):
        build_unit_arc_symmetry_plan(missing, (bad,))


def test_unit_clauses_use_the_orientation_model_literals() -> None:
    missing = EdgeGraph(4, (), "empty-missing")
    generators = (
        _transposition(4, 0, 1),
        _transposition(4, 1, 2),
        _transposition(4, 2, 3),
    )
    plan = build_unit_arc_symmetry_plan(missing, generators)
    model = build_orientation_model(missing)
    cnf = CNF(len(model.allowed_edges), [])
    clauses = add_unit_arc_clauses(cnf, model, plan)
    assert clauses == tuple(
        (-model.arc_literal(unit.left, unit.right),)
        for unit in plan.units
    )
    assert cnf.clauses == list(clauses)


def test_dreadnaut_adapter_returns_verified_generators_and_plan() -> None:
    # The three leaves of this missing star are interchangeable, and every
    # leaf pair is an allowed edge in its complement.
    missing = EdgeGraph(
        4,
        ((0, 3), (1, 3), (2, 3)),
        "three-leaf-star",
    )
    try:
        generators = dreadnaut_automorphism_generators(missing)
    except FileNotFoundError:
        pytest.skip("dreadnaut is unavailable")
    assert generators
    assert all(
        is_missing_graph_automorphism(missing, generator)
        for generator in generators
    )
    plan = build_unit_arc_symmetry_plan(missing, generators)
    assert plan.units
    assert verify_unit_arc_symmetry_plan(missing, plan)


def test_pack_color_minimum_order_removes_only_color_permutations() -> None:
    arcs = tuple(
        arc
        for offset in range(0, 12, 3)
        for arc in (
            (offset, offset + 1),
            (offset + 1, offset + 2),
            (offset + 2, offset),
        )
    )
    encoding = pack_four_cycles_cnf(12, arcs)
    clauses = add_pack_color_minimum_order_clauses(encoding.cnf, 12)
    assert len(clauses) == 36
    result = solve_incremental_once(encoding.cnf, 5.0)
    assert result.status == "sat"
    packing = extract_cycle_packing(arcs, encoding, result.assignment)
    minima = [
        min(vertex for arc in cycle for vertex in arc)
        for cycle in packing
    ]
    assert minima == sorted(minima)

    impossible = pack_four_cycles_cnf(12, arcs[:9])
    add_pack_color_minimum_order_clauses(impossible.cnf, 12)
    assert solve_incremental_once(impossible.cnf, 5.0).status == "unsat"
