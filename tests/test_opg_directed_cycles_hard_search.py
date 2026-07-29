from __future__ import annotations

from pathlib import Path

import pytest

from amra.discovery import opg_directed_cycles_hard_search as hard
from amra.discovery.opg_coloring_search import EdgeGraph, SolverResult
from amra.discovery.opg_directed_cycles_hard_search import (
    novel_short_cycle_packing_clauses,
    search_missing_graph_hard,
)
from amra.discovery.opg_directed_cycles_search import build_orientation_model


def _four_triangles() -> tuple[tuple[int, int], ...]:
    return tuple(
        arc
        for offset in range(0, 12, 3)
        for arc in (
            (offset, offset + 1),
            (offset + 1, offset + 2),
            (offset + 2, offset),
        )
    )


def test_novel_short_packing_batches_are_globally_deduplicated() -> None:
    arcs = _four_triangles()
    present = {
        tuple(sorted(arc))
        for arc in arcs
    }
    missing = tuple(
        pair
        for left in range(12)
        for right in range(left + 1, 12)
        if (pair := (left, right)) not in present
    )
    model = build_orientation_model(EdgeGraph(12, missing, "four-triangles"))
    known: set[tuple[int, ...]] = set()

    first = novel_short_cycle_packing_clauses(
        model,
        arcs,
        known,
        limit=1,
        scan_limit=10,
    )
    assert len(first.clauses) == 1
    assert first.examined == 1
    assert len(known) == 1

    second = novel_short_cycle_packing_clauses(
        model,
        arcs,
        known,
        limit=1,
        scan_limit=10,
        cycle_offset=3,
    )
    assert second.clauses == ()
    assert second.examined == 1
    assert second.exhausted
    assert len(known) == 1


def test_novel_short_packing_batch_validates_its_bounds() -> None:
    model = build_orientation_model(EdgeGraph(1, (), "singleton"))
    try:
        novel_short_cycle_packing_clauses(
            model,
            (),
            set(),
            limit=0,
        )
    except ValueError as error:
        assert "limit" in str(error)
    else:
        raise AssertionError("zero batch limit should fail")


def test_unverified_initial_units_cannot_fabricate_an_exclusion() -> None:
    missing = EdgeGraph(
        16,
        tuple((2 * vertex, 2 * vertex + 1) for vertex in range(8)),
        "eight-missing-edges",
    )
    with pytest.raises(ValueError, match="verified symmetry plan"):
        search_missing_graph_hard(
            missing,
            timeout_seconds=1.0,
            max_cegar_iterations=1,
            initial_unit_literals=(1, -1),
        )


def test_excluded_main_path_records_post_search_proof_timing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class UnsatSolver:
        def __init__(self, _cnf: object) -> None:
            pass

        def __enter__(self) -> "UnsatSolver":
            return self

        def __exit__(self, *_args: object) -> None:
            pass

        def solve(self, _timeout: float) -> SolverResult:
            return SolverResult("unsat", 0.0, frozenset(), "", "")

    def fake_proof(
        directory: Path,
        _stem: str,
        _cnf: object,
        _metadata: dict[str, object],
    ) -> dict[str, object]:
        directory.mkdir(parents=True, exist_ok=True)
        return {"proof_status": "independently_verified"}

    monkeypatch.setattr(hard, "IncrementalSolver", UnsatSolver)
    monkeypatch.setattr(hard, "_save_unsat_proof", fake_proof)
    missing = EdgeGraph(
        16,
        tuple((2 * vertex, 2 * vertex + 1) for vertex in range(8)),
        "perfect-matching",
    )
    result = hard.search_missing_graph_hard(
        missing,
        catalogue_index=496,
        timeout_seconds=2.0,
        max_cegar_iterations=1,
        short_batch_size=1,
        short_scan_limit=1,
        proof_directory=tmp_path / "proofs",
    )
    assert result["status"] == "excluded"
    assert result["config"]["catalogue_index"] == 496
    assert result["proof"]["proof_status"] == "independently_verified"
    assert "hard_search_timings_after_proof" in result["proof"]
    assert result["timings"]["proof_seconds"] >= 0.0
