from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from amra.discovery import opg_directed_cycles_search as directed
from amra.discovery.opg_coloring_search import CNF, EdgeGraph
from amra.discovery.opg_directed_cycles_search import (
    add_at_most,
    build_orientation_model,
    directed_short_cycles,
    extract_cycle_packing,
    pack_four_cycles_cnf,
    run_n16_search,
    solve_incremental_once,
    short_cycle_packing_clauses,
    strong_connectivity_cut,
)


def _has_extension(cnf: CNF, prefix: tuple[bool, ...]) -> bool:
    remaining = cnf.variable_count - len(prefix)
    for suffix in itertools.product((False, True), repeat=remaining):
        values = prefix + suffix
        if all(
            any(values[abs(literal) - 1] == (literal > 0) for literal in clause)
            for clause in cnf.clauses
        ):
            return True
    return False


def test_sequential_at_most_counter_has_the_right_projection() -> None:
    cnf = CNF(3, [])
    add_at_most(cnf, (1, 2, 3), 1)
    for values in itertools.product((False, True), repeat=3):
        assert _has_extension(cnf, values) == (sum(values) <= 1)


def test_strong_connectivity_cut_blocks_the_current_sink_component() -> None:
    missing = EdgeGraph(4, (), "empty missing graph")
    model = build_orientation_model(missing)
    transitive = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    cut = strong_connectivity_cut(model, transitive)
    assert cut is not None
    assignment = {
        model.arc_literal(source, target)
        for source, target in transitive
    }
    assert not any(literal in assignment for literal in cut)


def test_short_cycle_oracle_finds_four_disjoint_directed_triangles() -> None:
    n = 12
    triangle_arcs = tuple(
        arc
        for offset in range(0, n, 3)
        for arc in (
            (offset, offset + 1),
            (offset + 1, offset + 2),
            (offset + 2, offset),
        )
    )
    all_pairs = set(itertools.combinations(range(n), 2))
    present_pairs = {
        (min(source, target), max(source, target))
        for source, target in triangle_arcs
    }
    missing = EdgeGraph(n, tuple(sorted(all_pairs - present_pairs)), "four triangles")
    model = build_orientation_model(missing)
    cycles = directed_short_cycles(n, triangle_arcs)
    assert len(cycles) == 4
    clauses = short_cycle_packing_clauses(model, triangle_arcs, limit=10)
    assert len(clauses) == 1
    current_true = {
        model.arc_literal(source, target) for source, target in triangle_arcs
    }
    assert all(-literal in current_true for literal in clauses[0])


def test_pack_four_cycles_cnf_is_sat_exactly_for_four_disjoint_cycles() -> None:
    four_triangles = tuple(
        arc
        for offset in range(0, 12, 3)
        for arc in (
            (offset, offset + 1),
            (offset + 1, offset + 2),
            (offset + 2, offset),
        )
    )
    encoding = pack_four_cycles_cnf(12, four_triangles)
    result = solve_incremental_once(encoding.cnf, 5.0)
    assert result.status == "sat"
    packing = extract_cycle_packing(four_triangles, encoding, result.assignment)
    vertex_sets = [{vertex for edge in cycle for vertex in edge} for cycle in packing]
    assert len(vertex_sets) == 4
    assert all(
        vertex_sets[first].isdisjoint(vertex_sets[second])
        for first in range(4)
        for second in range(first)
    )

    three_triangles = four_triangles[:9]
    impossible = pack_four_cycles_cnf(9, three_triangles)
    assert solve_incremental_once(impossible.cnf, 5.0).status == "unsat"


def test_triangle_dominator_encoding_has_the_exact_projection() -> None:
    model = build_orientation_model(EdgeGraph(4, (), "K4"))
    cnf = CNF(len(model.allowed_edges), [])
    directed._add_triangle_dominator_constraints(cnf, model)
    for values in itertools.product((False, True), repeat=len(model.allowed_edges)):
        assignment = {
            (left, right) if values[index] else (right, left)
            for index, (left, right) in enumerate(model.allowed_edges)
        }
        expected = True
        for triple in itertools.combinations(range(4), 3):
            first, second, third = triple
            orientations = (
                ((first, second), (second, third), (third, first)),
                ((second, first), (first, third), (third, second)),
            )
            for cycle in orientations:
                if all(arc in assignment for arc in cycle):
                    expected = any(
                        all((outside, target) in assignment for target in triple)
                        for outside in range(4)
                        if outside not in triple
                    )
        assert _has_extension(cnf, values) is expected


def _fake_runtime_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        directed,
        "_tool_identity",
        lambda name: {
            "name": name,
            "path": f"/fake/{name}",
            "sha256": f"{name}-sha256",
            "version": "test",
            "version_command": [name, "--version"],
            "version_output": "test",
        },
    )
    monkeypatch.setattr(
        directed,
        "_solver_identity",
        lambda: {"backend": "test-solver", "sha256": "solver-sha256"},
    )


def test_checkpoint_retries_hard_queue_and_replays_write_ahead_event(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    catalogue = (
        EdgeGraph(16, (), "fake-even"),
        EdgeGraph(16, (), "fake-odd"),
    )
    monkeypatch.setattr(directed, "_load_n16_catalogue", lambda: catalogue)
    _fake_runtime_contract(monkeypatch)
    outcomes = iter(({"status": "timeout"}, {"status": "excluded"}))
    monkeypatch.setattr(
        directed,
        "search_missing_graph",
        lambda *_args, **_kwargs: next(outcomes),
    )
    output = tmp_path / "run"
    arguments = {
        "output": output,
        "wall_seconds": 30.0,
        "per_missing_graph_seconds": 1.0,
        "max_cegar_iterations": 10,
        "max_missing_graphs": 1,
        "proofs": False,
        "shard": (1, 2),
    }

    first = run_n16_search(**arguments)
    assert first["processed"] == 1
    assert first["attempts"] == 1
    assert first["hard_queue"][0]["catalogue_index"] == 1
    assert first["hard_queue"][0]["attempts"] == 1

    real_atomic_json = directed._atomic_json

    def crash_after_retry_event(path: Path, payload: object) -> None:
        if (
            path.name == "state.json"
            and isinstance(payload, dict)
            and payload.get("attempts") == 2
        ):
            raise RuntimeError("simulated crash")
        real_atomic_json(path, payload)

    monkeypatch.setattr(directed, "_atomic_json", crash_after_retry_event)
    with pytest.raises(RuntimeError, match="simulated crash"):
        run_n16_search(**arguments)

    monkeypatch.setattr(directed, "_atomic_json", real_atomic_json)
    monkeypatch.setattr(
        directed,
        "search_missing_graph",
        lambda *_args, **_kwargs: pytest.fail(
            "write-ahead event should be replayed without solving again"
        ),
    )
    resumed = run_n16_search(**arguments)
    assert resumed["status"] == "complete"
    assert resumed["processed"] == 1
    assert resumed["attempts"] == 2
    assert resumed["excluded"] == 1
    assert resumed["hard_queue"] == []

    events = [
        json.loads(line)
        for line in (output / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(events) == 2
    assert len({event["event_id"] for event in events}) == 2
    assert [event["attempt"] for event in events] == [1, 2]
    assert all(event["shard"] == [1, 2] for event in events)
    assert all(event["catalogue_index"] == 1 for event in events)


def test_checkpoint_rejects_config_and_catalogue_drift(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    catalogue = (EdgeGraph(16, (), "first"),)
    monkeypatch.setattr(directed, "_load_n16_catalogue", lambda: catalogue)
    _fake_runtime_contract(monkeypatch)
    monkeypatch.setattr(
        directed,
        "search_missing_graph",
        lambda *_args, **_kwargs: {"status": "excluded"},
    )
    output = tmp_path / "strict"
    run_n16_search(
        output,
        30.0,
        1.0,
        10,
        max_missing_graphs=1,
    )

    with pytest.raises(ValueError, match="contract changed"):
        run_n16_search(
            output,
            30.0,
            2.0,
            10,
            max_missing_graphs=1,
        )

    monkeypatch.setattr(
        directed,
        "_load_n16_catalogue",
        lambda: (EdgeGraph(16, (), "changed"),),
    )
    with pytest.raises(ValueError, match="contract changed"):
        run_n16_search(
            output,
            30.0,
            1.0,
            10,
            max_missing_graphs=1,
        )


def test_checkpoint_rejects_implementation_tool_and_event_drift(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    catalogue = (EdgeGraph(16, (), "only"),)
    monkeypatch.setattr(directed, "_load_n16_catalogue", lambda: catalogue)
    _fake_runtime_contract(monkeypatch)
    monkeypatch.setattr(
        directed,
        "search_missing_graph",
        lambda *_args, **_kwargs: {"status": "excluded"},
    )

    tool_output = tmp_path / "tool"
    run_n16_search(tool_output, 30.0, 1.0, 10)
    monkeypatch.setattr(
        directed,
        "_tool_identity",
        lambda name: {
            "name": name,
            "path": f"/changed/{name}",
            "sha256": f"changed-{name}",
            "version": "changed",
        },
    )
    with pytest.raises(ValueError, match="contract changed"):
        run_n16_search(tool_output, 30.0, 1.0, 10)

    _fake_runtime_contract(monkeypatch)
    implementation_output = tmp_path / "implementation"
    run_n16_search(implementation_output, 30.0, 1.0, 10)
    monkeypatch.setattr(directed, "file_sha256", lambda _path: "changed-source")
    with pytest.raises(ValueError, match="contract changed"):
        run_n16_search(implementation_output, 30.0, 1.0, 10)

    monkeypatch.undo()
    monkeypatch.setattr(directed, "_load_n16_catalogue", lambda: catalogue)
    _fake_runtime_contract(monkeypatch)
    monkeypatch.setattr(
        directed,
        "search_missing_graph",
        lambda *_args, **_kwargs: {"status": "excluded"},
    )
    event_output = tmp_path / "event"
    run_n16_search(event_output, 30.0, 1.0, 10)
    event_path = event_output / "events.jsonl"
    event = json.loads(event_path.read_text(encoding="utf-8"))
    event["event_id"] = "0" * 64
    event_path.write_text(json.dumps(event) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid event_id"):
        run_n16_search(event_output, 30.0, 1.0, 10)


def test_unsat_proof_manifest_records_hashes_tools_commands_and_revision(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tool_records = {
        name: {
            "name": name,
            "path": str(tmp_path / name),
            "sha256": f"{name}-binary-hash",
            "version": f"{name}-test-version",
            "version_command": [name, "--version"],
            "version_output": f"{name}-test-version",
        }
        for name in ("cadical", "drat-trim")
    }
    monkeypatch.setattr(
        directed, "_tool_identity", lambda name: tool_records[name]
    )
    monkeypatch.setattr(
        directed,
        "_code_revision",
        lambda: {
            "git_commit": "test-commit",
            "source_path": "/test/source.py",
            "source_sha256": "source-hash",
            "source_dirty": False,
        },
    )
    calls = 0

    def fake_run(command: list[str], **_kwargs: object) -> SimpleNamespace:
        nonlocal calls
        calls += 1
        if calls == 1:
            Path(command[-1]).write_bytes(b"test proof\n")
            return SimpleNamespace(
                returncode=20,
                stdout="s UNSATISFIABLE\n",
                stderr="",
            )
        # drat-trim returns 1 for a trivially UNSAT input while still
        # reporting the authoritative VERIFIED status.
        return SimpleNamespace(returncode=1, stdout="s VERIFIED\n", stderr="")

    monkeypatch.setattr(directed.subprocess, "run", fake_run)
    cnf = CNF(1, [()])
    manifest = directed._save_unsat_proof(
        tmp_path / "proofs",
        "instance",
        cnf,
        {"status": "excluded"},
    )
    formula = tmp_path / "proofs" / "instance.cnf"
    proof = tmp_path / "proofs" / "instance.drat"
    assert manifest["proof_manifest_schema"] == "amra.unsat-proof-manifest.v2"
    assert manifest["formula_sha256"] == hashlib.sha256(
        formula.read_bytes()
    ).hexdigest()
    assert manifest["proof_sha256"] == hashlib.sha256(
        proof.read_bytes()
    ).hexdigest()
    assert manifest["tools"]["proof_generator"]["version"] == "cadical-test-version"
    assert manifest["commands"]["proof_checker"][0] == str(tmp_path / "drat-trim")
    assert manifest["code_revision"]["git_commit"] == "test-commit"
    assert manifest["proof_status"] == "independently_verified"
