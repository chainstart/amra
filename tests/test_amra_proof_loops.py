from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest

from amra.proof import ProofLoopRegistry, ProofRunRequest, normalize_proof_status, run_proof_loop


class _FakeRunner:
    def __init__(self, *, contract_route: str, calls: list[dict[str, Any]]) -> None:
        self.contract_route = contract_route
        self.calls = calls

    def __getattr__(self, name: str):
        def _method(**parameters: Any) -> dict[str, Any]:
            self.calls.append(
                {
                    "route": self.contract_route,
                    "method": name,
                    "parameters": parameters,
                }
            )
            return {
                "status": "converged",
                "route_echo": self.contract_route,
                "parameter_keys": sorted(parameters),
            }

        return _method


def _fake_registry(calls: list[dict[str, Any]]) -> ProofLoopRegistry:
    def factory(contract, repo_root: Path) -> _FakeRunner:
        calls.append({"route": contract.route, "repo_root": repo_root, "factory": True})
        return _FakeRunner(contract_route=contract.route, calls=calls)

    return ProofLoopRegistry(runner_factory=factory)


def test_registry_declares_all_canonical_proof_loop_routes() -> None:
    registry = ProofLoopRegistry()

    routes = {contract.route: contract for contract in registry.contracts()}

    assert set(routes) == {
        "proof_lab",
        "proof_search",
        "math_attack",
        "campaign_loop",
        "goal_campaign",
        "closure",
        "focused_attack",
    }
    assert routes["proof_lab"].adapter_id == "ara_math.proof_lab:AIProofLabRunner.run"
    assert routes["proof_search"].method_name == "run_project"
    assert routes["focused_attack"].required_parameters == ("workspace", "attack_targets")
    assert routes["closure"].required_parameters == ("project_dir", "orchestrator")
    assert routes["math_attack"].required_parameters == ("project_dir",)


@pytest.mark.parametrize(
    ("parameters", "expected"),
    [
        ({"manifest_path": Path("goals.json")}, "goal_campaign"),
        ({"workspace": Path("formal"), "attack_targets": ["main"]}, "focused_attack"),
        ({"project_dir": Path("p"), "orchestrator": object(), "target_theorem": "main"}, "closure"),
        ({"project_dir": Path("p"), "orchestrator": object()}, "proof_search"),
        ({"project_dir": Path("p"), "target": "route A"}, "math_attack"),
        ({"statement": "prove T", "workspace": Path("formal")}, "campaign_loop"),
        ({"statement": "prove T"}, "proof_lab"),
    ],
)
def test_auto_route_selection_is_deterministic(parameters: dict[str, Any], expected: str) -> None:
    registry = ProofLoopRegistry()

    assert registry.select_route(parameters).route == expected


def test_explicit_route_aliases_are_normalized_and_validated() -> None:
    registry = ProofLoopRegistry()

    assert registry.select_route({"statement": "prove T"}, route="run-ai-proof-lab").route == "proof_lab"
    assert registry.select_route({"workspace": Path("formal"), "attack_targets": ["main"]}, route="focused-lean-attack").route == "focused_attack"

    with pytest.raises(ValueError, match="missing required parameter"):
        registry.select_route({"statement": "prove T"}, route="proof-search")


@pytest.mark.parametrize(
    ("raw_status", "expected"),
    [
        ("converged", "verified"),
        ("root_goal_verified", "verified"),
        ("completed", "completed"),
        ("rounds_exhausted", "partial"),
        ("needs_target", "blocked"),
        ("unavailable", "blocked"),
        ("timeout", "failed"),
        ("dry_run", "skipped"),
        ("running", "running"),
        ("not-a-known-status", "unknown"),
    ],
)
def test_status_normalization(raw_status: str, expected: str) -> None:
    assert normalize_proof_status(raw_status) == expected


def test_status_normalization_can_read_nested_focused_attack_report() -> None:
    report = {
        "final_observation": {
            "status": "verified",
            "contract_satisfied": True,
        }
    }

    assert normalize_proof_status(report=report) == "verified"


def test_registry_run_wraps_report_with_canonical_metadata(tmp_path: Path) -> None:
    calls: list[dict[str, Any]] = []
    registry = _fake_registry(calls)

    result = registry.run(
        ProofRunRequest.from_kwargs(
            repo_root=tmp_path,
            route="proof-search",
            request_id="unit-request",
            metadata={"harness_task": "amra-proof-loop-consolidation"},
            project_dir=tmp_path / "project",
            orchestrator=object(),
            backend="none",
        )
    )
    payload = result.to_dict()

    assert result.route == "proof_search"
    assert result.raw_status == "converged"
    assert result.canonical_status == "verified"
    assert payload["schema_version"] == "amra.proof_loop.result.v1"
    assert payload["metadata"]["request_id"] == "unit-request"
    assert payload["metadata"]["harness_task"] == "amra-proof-loop-consolidation"
    assert payload["metadata"]["adapter_id"] == "ara_math.proof_search:ProofSearchRunner.run_project"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T.*Z", payload["metadata"]["generated_at"])
    assert calls[0]["factory"] is True
    assert calls[1]["method"] == "run_project"
    assert calls[1]["parameters"]["backend"] == "none"


def test_registry_supplies_legacy_defaults_for_optional_runner_arguments(tmp_path: Path) -> None:
    calls: list[dict[str, Any]] = []
    registry = _fake_registry(calls)

    registry.run(
        ProofRunRequest.from_kwargs(
            repo_root=tmp_path,
            route="math_attack",
            project_dir=tmp_path / "project",
        )
    )
    registry.run(
        ProofRunRequest.from_kwargs(
            repo_root=tmp_path,
            route="closure",
            project_dir=tmp_path / "project",
            orchestrator=object(),
        )
    )

    assert calls[1]["parameters"]["target"] == ""
    assert calls[3]["parameters"]["target_theorem"] is None


def test_run_proof_loop_can_delegate_to_existing_proof_lab_without_live_backend(tmp_path: Path, monkeypatch) -> None:
    import ara_math.proof_lab as proof_lab

    monkeypatch.setattr(
        proof_lab,
        "wait_for_system_headroom",
        lambda **_: {"status": "ready", "waited_seconds": 0.0},
    )

    result = run_proof_loop(
        "proof_lab",
        repo_root=tmp_path,
        statement="For every n, prove P(n).",
        backend="none",
        attempts=1,
        audits=0,
        time_budget_sec=60,
        output_root=tmp_path / "proof_lab_runs",
        run_name="adapter-proof-lab",
    )

    assert result.route == "proof_lab"
    assert result.canonical_status == "completed"
    assert result.report["attempts_completed"] == 1
    assert Path(result.report["run_dir"]).joinpath("report.json").exists()
