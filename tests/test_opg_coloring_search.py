from __future__ import annotations

import itertools

import pytest

import amra.discovery.opg_coloring_search as coloring_search
from amra.discovery.opg_coloring_search import (
    CNF,
    EdgeGraph,
    SolverResult,
    _semantic_certificate,
    bichromatic_cycle,
    circular_coloring_cnf,
    decode_graph6,
    decode_multig_text,
    four_edge_paths_and_cycles,
    is_three_sparse,
    proper_edge_coloring_cnf,
    star_edge_coloring_cnf,
    verify_acyclic_edge_coloring,
    verify_acyclic_cut_records,
    verify_circular_coloring,
)


def _brute_force_satisfiable(variable_count: int, clauses: list[tuple[int, ...]]) -> bool:
    for values in itertools.product((False, True), repeat=variable_count):
        if all(
            any(values[abs(literal) - 1] == (literal > 0) for literal in clause)
            for clause in clauses
        ):
            return True
    return False


def test_multig_parser_preserves_parallel_edge_identities() -> None:
    graph = decode_multig_text("4 4  0 2 2 0 3 1 1 2 1 1 3 2")
    assert graph.degrees == (3, 3, 3, 3)
    assert graph.edges.count((0, 2)) == 2
    assert graph.edges.count((1, 3)) == 2


@pytest.mark.parametrize("record", ("C", "C??", "D?@"))
def test_graph6_parser_rejects_truncation_excess_and_nonzero_padding(
    record: str,
) -> None:
    with pytest.raises(ValueError):
        decode_graph6(record)


def test_star_cnf_forbids_a_b_a_b_on_a_four_edge_path() -> None:
    path = EdgeGraph(
        5,
        ((0, 1), (1, 2), (2, 3), (3, 4)),
        "P4",
    )
    assert four_edge_paths_and_cycles(path) == ((0, 1, 2, 3),)
    two_colors = star_edge_coloring_cnf(path, 2)
    assert not _brute_force_satisfiable(two_colors.variable_count, two_colors.clauses)
    three_colors = star_edge_coloring_cnf(path, 3)
    assert _brute_force_satisfiable(three_colors.variable_count, three_colors.clauses)


def test_acyclic_cycle_oracle_and_cut_model_agree_on_c4() -> None:
    cycle = EdgeGraph(
        4,
        ((0, 1), (1, 2), (2, 3), (0, 3)),
        "C4",
    )
    coloring = (0, 1, 0, 1)
    assert bichromatic_cycle(cycle, coloring) == (0, 1, 2, 3)
    assert not verify_acyclic_edge_coloring(cycle, coloring)
    proper = proper_edge_coloring_cnf(cycle, 2)
    assert _brute_force_satisfiable(proper.variable_count, proper.clauses)
    proper.add(*(-(edge * 2 + coloring[edge] + 1) for edge in range(4)))
    assert not _brute_force_satisfiable(proper.variable_count, proper.clauses)
    assert verify_acyclic_cut_records(
        cycle,
        2,
        (
            {
                "edge_colors": [[edge, coloring[edge]] for edge in range(4)],
                "clause": [
                    -(edge * 2 + coloring[edge] + 1) for edge in range(4)
                ],
            },
        ),
    )
    assert not verify_acyclic_cut_records(cycle, 2, (object(),))  # type: ignore[arg-type]


def test_acyclic_semantic_certificate_binds_records_to_exact_cnf() -> None:
    cycle = EdgeGraph(
        4,
        ((0, 1), (1, 2), (2, 3), (0, 3)),
        "C4",
    )
    coloring = (0, 1, 0, 1)
    clause = tuple(-(edge * 7 + coloring[edge] + 1) for edge in range(4))
    records = (
        {
            "edge_colors": [[edge, coloring[edge]] for edge in range(4)],
            "clause": list(clause),
        },
    )
    exact = proper_edge_coloring_cnf(cycle, 7)
    exact.add(*clause)
    certificate = _semantic_certificate("opg145", cycle, exact, records)
    assert certificate is not None
    assert certificate["independently_replayed"] is True

    tampered = CNF(exact.variable_count, list(exact.clauses))
    tampered.add(1)
    tampered_certificate = _semantic_certificate(
        "opg145", cycle, tampered, records
    )
    assert tampered_certificate is not None
    assert tampered_certificate["records_semantically_valid"] is True
    assert tampered_certificate["independently_replayed"] is False


def test_circular_support_encoding_rejects_triangle_at_5_over_2() -> None:
    triangle = EdgeGraph(3, ((0, 1), (0, 2), (1, 2)), "K3")
    cnf = circular_coloring_cnf(triangle, modulus=5, distance=2)
    assert not _brute_force_satisfiable(cnf.variable_count, cnf.clauses)
    assert verify_circular_coloring(
        EdgeGraph(2, ((0, 1),), "K2"),
        (0, 2),
        modulus=5,
        distance=2,
    )


def test_three_sparse_filter_has_the_intended_direction() -> None:
    sparse = EdgeGraph(5, ((0, 1), (0, 2), (0, 3), (0, 4)), "K1,4")
    dense_edge = EdgeGraph(
        6,
        (
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 2),
            (1, 3),
            (1, 5),
        ),
        "two-degree-four endpoints",
    )
    assert is_three_sparse(sparse)
    assert not is_three_sparse(dense_edge)


def test_hard_queue_retry_obeys_max_cases_before_new_enumeration(
    tmp_path, monkeypatch
) -> None:
    graph = EdgeGraph(2, ((0, 1),), "2 1  0 1 1")
    monkeypatch.setattr(
        coloring_search, "iter_star_multigraphs", lambda order, lane: iter((graph, graph))
    )
    monkeypatch.setattr(
        coloring_search, "implementation_fingerprint", lambda *paths: "implementation"
    )
    monkeypatch.setattr(
        coloring_search, "toolchain_fingerprint", lambda names: {"tools": "fixed"}
    )
    calls = 0

    def evaluate(problem, candidate, timeout_seconds):
        nonlocal calls
        calls += 1
        status = "timeout" if calls == 1 else "sat"
        return (
            SolverResult(status, 0.0, frozenset(), "", ""),
            CNF(0, []),
            None,
            0,
            (),
        )

    monkeypatch.setattr(coloring_search, "evaluate_coloring_instance", evaluate)
    output = tmp_path / "retry"
    first = coloring_search.run_search(
        "opg37271", 2, 2, 60.0, 1.0, output, max_cases=1
    )
    assert first["generated"] == 1
    assert first["timeouts"] == 1
    assert len(first["hard_queue"]) == 1

    second = coloring_search.run_search(
        "opg37271", 2, 2, 60.0, 1.0, output, max_cases=1
    )
    assert second["status"] == "paused_budget"
    assert second["generated"] == 1
    assert second["sat"] == 1
    assert second["timeouts"] == 0
    assert second["hard_queue"] == []
    assert len(
        (output / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ) == 2


def test_candidate_checkpoint_is_terminal_by_default(tmp_path, monkeypatch) -> None:
    graph = EdgeGraph(2, ((0, 1),), "2 1  0 1 1")
    monkeypatch.setattr(
        coloring_search, "iter_star_multigraphs", lambda order, lane: iter((graph,))
    )
    monkeypatch.setattr(
        coloring_search, "implementation_fingerprint", lambda *paths: "implementation"
    )
    monkeypatch.setattr(
        coloring_search, "toolchain_fingerprint", lambda names: {"tools": "fixed"}
    )
    evaluations = 0

    def evaluate(problem, candidate, timeout_seconds):
        nonlocal evaluations
        evaluations += 1
        return (
            SolverResult("unsat", 0.0, frozenset(), "", ""),
            CNF(1, [(1,), (-1,)]),
            None,
            0,
            (),
        )

    monkeypatch.setattr(coloring_search, "evaluate_coloring_instance", evaluate)
    monkeypatch.setattr(
        coloring_search,
        "_save_unsat_bundle",
        lambda *args, **kwargs: {"bundle": "candidate"},
    )
    output = tmp_path / "candidate"
    first = coloring_search.run_search(
        "opg37271", 2, 2, 60.0, 1.0, output
    )
    second = coloring_search.run_search(
        "opg37271", 2, 2, 60.0, 1.0, output
    )
    assert first["status"] == "candidate_pending_independent_verification"
    assert second["status"] == "candidate_pending_independent_verification"
    assert evaluations == 1
