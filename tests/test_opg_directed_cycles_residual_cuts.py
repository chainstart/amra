from __future__ import annotations

import itertools

import pytest

from amra.discovery.opg_coloring_search import CNF, EdgeGraph
from amra.discovery.opg_directed_cycles_residual_cuts import (
    add_residual_degree_cut,
    canonical_packing_key,
    residual_cross_arc_count_identity,
    residual_witness_is_automatic,
    separate_residual_degree_cuts,
)
from amra.discovery.opg_directed_cycles_search import (
    OrientationModel,
    build_orientation_model,
    solve_incremental_once,
)


def _cycle(offset: int) -> tuple[tuple[int, int], ...]:
    return (
        (offset, offset + 1),
        (offset + 1, offset + 2),
        (offset + 2, offset),
    )


def _model_with_edges(
    vertex_count: int,
    edges: set[tuple[int, int]],
) -> OrientationModel:
    all_pairs = set(itertools.combinations(range(vertex_count), 2))
    missing = tuple(sorted(all_pairs - edges))
    return build_orientation_model(EdgeGraph(vertex_count, missing, "test"))


def _has_extension_with_arcs(
    cnf: CNF,
    model: OrientationModel,
    arcs: set[tuple[int, int]],
) -> bool:
    constrained = CNF(cnf.variable_count, list(cnf.clauses))
    for left, right in model.allowed_edges:
        literal = model.arc_literal(left, right)
        assert literal is not None
        constrained.add(literal if (left, right) in arcs else -literal)
    return solve_incremental_once(constrained, 5.0).status == "sat"


@pytest.mark.parametrize(
    ("packing_size", "outside", "threshold"),
    ((1, 3, 3), (2, 6, 5), (3, 9, 7)),
)
def test_residual_cut_has_exact_triggered_projection_and_nontrigger_is_free(
    packing_size: int,
    outside: int,
    threshold: int,
) -> None:
    cycles = tuple(_cycle(3 * index) for index in range(packing_size))
    selected = tuple(range(3 * packing_size))
    cycle_pairs = {
        (min(source, target), max(source, target))
        for cycle in cycles
        for source, target in cycle
    }
    spoke_pairs = {
        (min(outside, target), max(outside, target)) for target in selected
    }
    model = _model_with_edges(outside + 1, cycle_pairs | spoke_pairs)
    cnf = CNF(len(model.allowed_edges), [])
    encoding = add_residual_degree_cut(cnf, model, cycles)
    assert encoding.threshold == threshold
    assert len(encoding.witnesses) == 1

    for mask in range(1 << len(selected)):
        arcs = {arc for cycle in cycles for arc in cycle}
        outgoing_count = 0
        for index, target in enumerate(selected):
            if mask & (1 << index):
                arcs.add((outside, target))
                outgoing_count += 1
            else:
                arcs.add((target, outside))
        assert _has_extension_with_arcs(cnf, model, arcs) == (
            outgoing_count >= threshold
        )

        # Reversing one trigger edge makes the implication inactive.  Every
        # assignment of the witness arcs must then have an extension.
        nontrigger = set(arcs)
        source, target = cycles[0][0]
        nontrigger.remove((source, target))
        nontrigger.add((target, source))
        assert _has_extension_with_arcs(cnf, model, nontrigger)


def test_canonical_packing_key_ignores_rotation_and_packing_order() -> None:
    first = _cycle(0)
    rotated = (first[1], first[2], first[0])
    second = _cycle(3)
    assert canonical_packing_key((first, second)) == canonical_packing_key(
        (second, rotated)
    )
    with pytest.raises(ValueError, match="vertex-disjoint"):
        canonical_packing_key((first, rotated))


def test_cut_arc_identity_prefilter_has_the_exact_strict_boundary() -> None:
    selected = tuple(range(8))
    residual = tuple(range(8, 16))
    missing = tuple(itertools.combinations(residual, 2))[:5]
    model = build_orientation_model(EdgeGraph(16, missing, "five in R"))
    cycles = (
        ((0, 1), (1, 2), (2, 3), (3, 0)),
        ((4, 5), (5, 6), (6, 7), (7, 4)),
    )
    assert residual_cross_arc_count_identity(model, selected) == 33
    assert residual_witness_is_automatic(model, cycles)

    four_missing = missing[:4]
    boundary_model = build_orientation_model(
        EdgeGraph(16, four_missing, "four in R")
    )
    assert residual_cross_arc_count_identity(boundary_model, selected) == 32
    assert not residual_witness_is_automatic(boundary_model, cycles)


def test_short_cycle_separator_limits_and_globally_deduplicates() -> None:
    cycles = (_cycle(0), _cycle(3), _cycle(6))
    edge_pairs = {
        (min(source, target), max(source, target))
        for cycle in cycles
        for source, target in cycle
    }
    model = _model_with_edges(10, edge_pairs)
    arcs = tuple(arc for cycle in cycles for arc in cycle)
    cnf = CNF(len(model.allowed_edges), [])
    known: set[tuple[tuple[int, ...], ...]] = set()

    first = separate_residual_degree_cuts(
        cnf,
        model,
        arcs,
        known,
        pack_sizes=(2,),
        limit=2,
        use_cut_identity_prefilter=False,
    )
    assert len(first.cuts) == 2
    assert first.records == first.cuts
    assert first.keys == tuple(cut.packing_key for cut in first.cuts)
    assert first.generated_clauses == tuple(
        clause for cut in first.cuts for clause in cut.clauses
    )
    assert len(known) == 2
    assert first.limit_reached

    second = separate_residual_degree_cuts(
        cnf,
        model,
        arcs,
        known,
        pack_sizes=(2,),
        limit=10,
        use_cut_identity_prefilter=False,
    )
    assert len(second.cuts) == 1
    assert second.duplicate_packings == 2
    assert len(known) == 3

    third = separate_residual_degree_cuts(
        cnf,
        model,
        arcs,
        known,
        pack_sizes=(2,),
        limit=10,
        use_cut_identity_prefilter=False,
    )
    assert third.cuts == ()
    assert third.duplicate_packings == 3

    triple = separate_residual_degree_cuts(
        cnf,
        model,
        arcs,
        known,
        pack_sizes=(3,),
        limit=1,
        use_cut_identity_prefilter=False,
    )
    assert len(triple.cuts) == 1
    assert triple.cuts[0].threshold == 7


def test_identity_prefilter_rejects_non_fixed_outdegree_input() -> None:
    cycles = (_cycle(0), _cycle(3))
    edge_pairs = {
        (min(source, target), max(source, target))
        for cycle in cycles
        for source, target in cycle
    }
    model = _model_with_edges(7, edge_pairs)
    arcs = tuple(arc for cycle in cycles for arc in cycle)
    with pytest.raises(ValueError, match="fixed outdegree"):
        separate_residual_degree_cuts(
            CNF(len(model.allowed_edges), []),
            model,
            arcs,
            pack_sizes=(2,),
            limit=1,
        )


def test_separator_consideration_limit_bounds_the_scan() -> None:
    cycles = (_cycle(0), _cycle(3), _cycle(6))
    edge_pairs = {
        (min(source, target), max(source, target))
        for cycle in cycles
        for source, target in cycle
    }
    model = _model_with_edges(10, edge_pairs)
    arcs = tuple(arc for cycle in cycles for arc in cycle)
    result = separate_residual_degree_cuts(
        CNF(len(model.allowed_edges), []),
        model,
        arcs,
        pack_sizes=(2,),
        limit=10,
        consideration_limit=1,
        use_cut_identity_prefilter=False,
    )
    assert result.considered_packings == 1
    assert result.limit_reached

    prefix_bounded = separate_residual_degree_cuts(
        CNF(len(model.allowed_edges), []),
        model,
        arcs,
        pack_sizes=(3,),
        limit=10,
        consideration_limit=10,
        traversal_limit=1,
        use_cut_identity_prefilter=False,
    )
    assert prefix_bounded.considered_packings == 0
    assert prefix_bounded.limit_reached
