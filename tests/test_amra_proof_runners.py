from __future__ import annotations

import importlib
from pathlib import Path

from amra.proof import ProofLoopRegistry, run_proof_loop
from amra.proof.lab import AIProofLabRunner
from amra.proof.planning import MathPlanner
from amra.proof.proof_system import ProofSearchAgendaPlanner, ProofSystemPlanner
from amra.proof.retrieval import PremiseRetriever


def test_canonical_proof_runner_modules_are_importable() -> None:
    assert AIProofLabRunner.__module__ == "amra.proof.lab"
    assert MathPlanner.__module__ == "amra.proof.planning"
    assert PremiseRetriever.__module__ == "amra.proof.retrieval"
    assert ProofSystemPlanner.__module__ == "amra.proof.proof_system"
    assert ProofSearchAgendaPlanner.__module__ == "amra.proof.proof_system"


def test_legacy_proof_runner_modules_alias_canonical_modules() -> None:
    aliases = {
        "ara_math.proof_lab": "amra.proof.lab",
        "ara_math.proof_search": "amra.proof.search",
        "ara_math.math_attack": "amra.proof.attack",
        "ara_math.closure": "amra.proof.closure",
        "ara_math.campaign_loop": "amra.proof.campaign_loop",
        "ara_math.goal_campaign": "amra.proof.goal_campaign",
        "ara_math.retrieval": "amra.proof.retrieval",
        "ara_math.planning": "amra.proof.planning",
        "ara_math.proof_system": "amra.proof.proof_system",
    }

    for legacy_name, canonical_name in aliases.items():
        assert importlib.import_module(legacy_name) is importlib.import_module(canonical_name)


def test_proof_loop_registry_legacy_adapter_modules_resolve_to_canonical_modules() -> None:
    registry = ProofLoopRegistry()

    routes = {contract.route: contract for contract in registry.contracts()}

    assert importlib.import_module(routes["proof_lab"].runner_module) is importlib.import_module("amra.proof.lab")
    assert importlib.import_module(routes["proof_search"].runner_module) is importlib.import_module("amra.proof.search")
    assert importlib.import_module(routes["math_attack"].runner_module) is importlib.import_module("amra.proof.attack")
    assert importlib.import_module(routes["campaign_loop"].runner_module) is importlib.import_module(
        "amra.proof.campaign_loop"
    )
    assert importlib.import_module(routes["goal_campaign"].runner_module) is importlib.import_module(
        "amra.proof.goal_campaign"
    )
    assert importlib.import_module(routes["closure"].runner_module) is importlib.import_module("amra.proof.closure")


def test_canonical_proof_lab_backend_none_writes_durable_run_dir(tmp_path: Path) -> None:
    result = run_proof_loop(
        "proof_lab",
        repo_root=tmp_path,
        statement="Prove that True is true.",
        backend="none",
        attempts=1,
        audits=0,
        time_budget_sec=60,
        output_root=tmp_path / "proof_lab_runs",
        run_name="canonical-proof-lab",
    )

    run_dir = Path(result.report["run_dir"])
    assert result.route == "proof_lab"
    assert result.canonical_status == "completed"
    assert run_dir.exists()
    assert run_dir.joinpath("report.json").exists()
    assert run_dir.joinpath("summary.md").exists()
