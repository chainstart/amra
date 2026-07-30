from __future__ import annotations

import time
from itertools import combinations

import pytest

from amra.discovery.opg_coloring_search import EdgeGraph
from amra.discovery.opg_directed_cycles_long_packing import (
    separate_long_cycle_packings,
)
from amra.discovery.opg_directed_cycles_search import (
    OrientationModel,
    build_orientation_model,
    directed_short_cycles,
    extract_cycle_packing,
    pack_four_cycles_cnf,
    packing_block_clause,
    solve_incremental_once,
)


def _model_for_arcs(
    arcs: tuple[tuple[int, int], ...],
) -> tuple[EdgeGraph, OrientationModel]:
    present = {tuple(sorted(arc)) for arc in arcs}
    missing = tuple(
        pair
        for pair in combinations(range(16), 2)
        if pair not in present
    )
    graph = EdgeGraph(16, missing, "long-packing-regression")
    return graph, build_orientation_model(graph)


def _three_triangles() -> set[tuple[int, int]]:
    return {
        arc
        for offset in (7, 10, 13)
        for arc in (
            (offset, offset + 1),
            (offset + 1, offset + 2),
            (offset + 2, offset),
        )
    }


def _long_only_arcs() -> tuple[tuple[int, int], ...]:
    # The component on 0..6 has four directed cycles of lengths five/six
    # and no directed triangle or quadrangle.
    long_component = {
        (0, 4),
        (1, 3),
        (1, 6),
        (2, 0),
        (3, 2),
        (4, 1),
        (4, 5),
        (5, 1),
        (6, 2),
    }
    return tuple(sorted(long_component | _three_triangles()))


def _cycle_vertices(
    cycle: tuple[tuple[int, int], ...],
) -> frozenset[int]:
    return frozenset(vertex for arc in cycle for vertex in arc)


def test_long_only_separator_returns_multiple_pack4_block_clauses() -> None:
    arcs = _long_only_arcs()
    _, model = _model_for_arcs(arcs)

    short_cycles = directed_short_cycles(16, arcs)
    assert sorted(len(cycle) for cycle in short_cycles) == [3, 3, 3]

    packing = pack_four_cycles_cnf(16, arcs)
    packing_result = solve_incremental_once(packing.cnf, 5.0)
    assert packing_result.status == "sat"
    oracle_cycles = extract_cycle_packing(
        arcs,
        packing,
        packing_result.assignment,
    )
    assert sorted(len(cycle) for cycle in oracle_cycles) in (
        [3, 3, 3, 5],
        [3, 3, 3, 6],
    )

    known: set[tuple[int, ...]] = set()
    batch = separate_long_cycle_packings(
        model,
        arcs,
        known,
        batch_limit=3,
        scan_limit=50_000,
    )

    assert len(batch.clauses) == 3
    assert len(batch.packings) == 3
    assert batch.batch_limit_reached
    assert batch.scan_steps <= 50_000
    assert known == set(batch.clauses)
    assert batch.long_cycles_found >= 3
    assert batch.packings_examined == 3

    arc_set = set(arcs)
    for clause, witness in zip(batch.clauses, batch.packings):
        assert len(witness) == 4
        assert any(len(cycle) >= 5 for cycle in witness)
        vertex_sets = [_cycle_vertices(cycle) for cycle in witness]
        assert all(
            not vertex_sets[first] & vertex_sets[second]
            for first in range(4)
            for second in range(first + 1, 4)
        )
        assert all(arc in arc_set for cycle in witness for arc in cycle)
        assert clause == tuple(
            sorted(set(packing_block_clause(model, witness)))
        )
        # Each returned master clause is false in precisely the current
        # orientation that contains its four-cycle packing.
        assert all(
            -literal
            in {
                model.arc_literal(source, target)
                for source, target in arcs
            }
            for literal in clause
        )


def test_long_only_clauses_are_globally_deduplicated() -> None:
    arcs = _long_only_arcs()
    _, model = _model_for_arcs(arcs)
    known: set[tuple[int, ...]] = set()

    first = separate_long_cycle_packings(
        model,
        arcs,
        known,
        batch_limit=8,
        scan_limit=100_000,
    )
    assert len(first.clauses) == 4
    assert first.exhausted

    second = separate_long_cycle_packings(
        model,
        arcs,
        known,
        batch_limit=8,
        scan_limit=100_000,
    )
    assert second.clauses == ()
    assert second.exhausted
    assert second.known_duplicates == 4
    assert len(known) == 4


def test_two_long_cycle_length_shape_is_separated() -> None:
    arcs = tuple(
        sorted(
            {
                arc
                for cycle in (
                    (0, 1, 2, 3, 4),
                    (5, 6, 7, 8, 9),
                    (10, 11, 12),
                    (13, 14, 15),
                )
                for arc in zip(cycle, cycle[1:] + cycle[:1])
            }
        )
    )
    _, model = _model_for_arcs(arcs)
    assert sorted(
        len(cycle) for cycle in directed_short_cycles(16, arcs)
    ) == [3, 3]

    packing = pack_four_cycles_cnf(16, arcs)
    packing_result = solve_incremental_once(packing.cnf, 5.0)
    assert packing_result.status == "sat"

    batch = separate_long_cycle_packings(
        model,
        arcs,
        set(),
        batch_limit=1,
        scan_limit=50_000,
    )
    assert len(batch.clauses) == 1
    assert sorted(len(cycle) for cycle in batch.packings[0]) == [
        3,
        3,
        5,
        5,
    ]
    assert batch.batch_limit_reached


def test_separator_and_pack4_both_reject_a_three_cycle_instance() -> None:
    arcs = tuple(
        arc
        for arc in _long_only_arcs()
        if not ({arc[0], arc[1]} <= {13, 14, 15})
    )
    _, model = _model_for_arcs(arcs)

    packing = pack_four_cycles_cnf(16, arcs)
    packing_result = solve_incremental_once(packing.cnf, 5.0)
    assert packing_result.status == "unsat"

    batch = separate_long_cycle_packings(
        model,
        arcs,
        set(),
        batch_limit=8,
        scan_limit=100_000,
    )
    assert batch.clauses == ()
    assert batch.exhausted


def test_separator_respects_past_deadline_and_scan_limit() -> None:
    arcs = _long_only_arcs()
    _, model = _model_for_arcs(arcs)

    expired = separate_long_cycle_packings(
        model,
        arcs,
        set(),
        deadline=time.monotonic() - 1.0,
    )
    assert expired.clauses == ()
    assert expired.scan_steps == 0
    assert expired.deadline_reached

    bounded = separate_long_cycle_packings(
        model,
        arcs,
        set(),
        scan_limit=10,
    )
    assert bounded.clauses == ()
    assert bounded.scan_steps == 10
    assert bounded.scan_limit_reached


@pytest.mark.parametrize(
    ("keyword", "value", "message"),
    (
        ("batch_limit", 0, "batch_limit"),
        ("scan_limit", 0, "scan_limit"),
        ("cycle_offset", 1.5, "cycle_offset"),
        ("deadline", float("inf"), "deadline"),
    ),
)
def test_separator_validates_bounds(
    keyword: str,
    value: object,
    message: str,
) -> None:
    arcs = _long_only_arcs()
    _, model = _model_for_arcs(arcs)
    with pytest.raises(ValueError, match=message):
        separate_long_cycle_packings(
            model,
            arcs,
            set(),
            **{keyword: value},
        )
