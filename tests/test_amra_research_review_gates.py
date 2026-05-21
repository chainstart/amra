from __future__ import annotations

import json
from pathlib import Path

from amra.modeling import (
    MODEL_CALIBRATION_REPORT_FILE,
    MODEL_SENSITIVITY_REPORT_FILE,
    MODEL_SPEC_FILE,
    MODEL_VALIDATION_REPORT_FILE,
    run_model_validation_fixture,
)
from amra.research_review import evaluate_model_validation_gate
from amra.research_review import evaluate_ml_theory_gate
from amra.research_review import evaluate_research_object_review
from amra.research_review import evaluate_security_gate
from amra.research_review import run_research_review_fixture


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "modeling_fixture.json"
RESEARCH_REVIEW_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "research_review_fixture.json"


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_model_validation_gate_accepts_separated_calibration_and_warns_on_extrapolation(tmp_path: Path) -> None:
    output = tmp_path / "model-validation"
    run_model_validation_fixture(fixture=FIXTURE, output_dir=output)

    gate = evaluate_model_validation_gate(
        model_spec=_read_json(output / MODEL_SPEC_FILE),
        calibration_report=_read_json(output / MODEL_CALIBRATION_REPORT_FILE),
        validation_report=_read_json(output / MODEL_VALIDATION_REPORT_FILE),
        sensitivity_report=_read_json(output / MODEL_SENSITIVITY_REPORT_FILE),
        failure_modes=[],
    )
    payload = gate.to_dict()

    assert payload["approved"] is True
    assert payload["decision"] == "model_validated_with_extrapolation_warning"
    assert payload["checks"]["variables_declared"] is True
    assert payload["checks"]["units_declared"] is True
    assert payload["checks"]["assumptions_declared"] is True
    assert payload["checks"]["parameters_traceable"] is True
    assert payload["warnings"][0]["code"] == "extrapolation_risk"


def test_model_validation_gate_blocks_untraceable_parameters_and_missing_sensitivity(tmp_path: Path) -> None:
    output = tmp_path / "model-validation"
    run_model_validation_fixture(fixture=FIXTURE, output_dir=output)
    model_spec = _read_json(output / MODEL_SPEC_FILE)
    sensitivity_report = _read_json(output / MODEL_SENSITIVITY_REPORT_FILE)
    model_spec["parameters"][0]["source"] = ""
    model_spec["parameters"][0]["calibration_method"] = ""
    sensitivity_report["scenarios"] = []

    gate = evaluate_model_validation_gate(
        model_spec=model_spec,
        calibration_report=_read_json(output / MODEL_CALIBRATION_REPORT_FILE),
        validation_report=_read_json(output / MODEL_VALIDATION_REPORT_FILE),
        sensitivity_report=sensitivity_report,
        failure_modes=[],
    ).to_dict()

    assert gate["approved"] is False
    assert gate["decision"] == "untraceable_parameters"
    assert {"untraceable_parameters", "missing_sensitivity_report"} <= set(gate["statuses"])


def test_security_gate_accepts_bounded_attack_failure_as_non_proof_evidence() -> None:
    gate = evaluate_security_gate(
        threat_model={
            "threat_model_id": "threat-1",
            "assets": ["shared_secret"],
            "adversary_goals": ["distinguish"],
            "capabilities": ["chosen_ciphertext_queries"],
        },
        security_game={
            "game_id": "game-1",
            "scheme": "toy-kem",
            "oracle_access": ["decapsulation_except_challenge"],
            "winning_condition": "advantage above threshold",
        },
        assumptions=[
            {
                "assumption_id": "assumption-1",
                "statement": "Fixture hardness assumption.",
            }
        ],
        reductions=[
            {
                "reduction_id": "reduction-1",
                "game_id": "game-1",
                "assumption_id": "assumption-1",
                "statement": "Fixture reduction.",
            }
        ],
        attack_report={
            "attack_report_id": "attack-report-1",
            "search_bound": {"max_trials": 2, "max_oracle_queries": 4},
            "found_attacks": [],
            "bounded_evidence_only": True,
            "proof_status": "not_proof",
        },
        evidence={
            "evidence_id": "security-evidence-1",
            "kind": "security_evidence",
            "confidence": "medium",
            "metadata": {"proof_status": "not_proof"},
        },
    ).to_dict()

    assert gate["approved"] is True
    assert gate["decision"] == "security_reviewed_bounded_evidence"
    assert gate["warnings"][0]["code"] == "bounded_evidence_not_proof"
    assert gate["checks"]["attack_failure_bounded_evidence_only"] is True


def test_security_gate_blocks_missing_reduction_and_proof_misclassification() -> None:
    gate = evaluate_security_gate(
        threat_model={
            "threat_model_id": "threat-1",
            "assets": ["shared_secret"],
            "adversary_goals": ["distinguish"],
            "capabilities": ["chosen_ciphertext_queries"],
        },
        security_game={
            "game_id": "game-1",
            "scheme": "toy-kem",
            "oracle_access": ["decapsulation_except_challenge"],
            "winning_condition": "advantage above threshold",
        },
        assumptions=[
            {
                "assumption_id": "assumption-1",
                "statement": "Fixture hardness assumption.",
            }
        ],
        reductions=[],
        attack_report={
            "attack_report_id": "attack-report-1",
            "search_bound": {"max_trials": 2, "max_oracle_queries": 4},
            "found_attacks": [],
            "bounded_evidence_only": False,
            "proof_status": "proof",
        },
        evidence={
            "evidence_id": "security-evidence-1",
            "kind": "security_evidence",
            "confidence": "theorem_grade",
            "metadata": {"proof_status": "proof"},
        },
    ).to_dict()

    assert gate["approved"] is False
    assert gate["decision"] == "missing_reduction"
    assert {"missing_reduction", "attack_failure_misclassified_as_proof"} <= set(gate["statuses"])


def test_ml_theory_gate_accepts_empirical_boundary_as_non_proof() -> None:
    gate = evaluate_ml_theory_gate(
        claim={
            "object_id": "claim-1",
            "statement": "Validation loss decreases across a bounded fixture sweep.",
            "confidence": "medium",
        },
        experiment_manifest={
            "experiment_id": "exp-1",
            "deterministic": True,
            "seed": 7,
            "budget": {"max_train_runs": 2, "max_epochs": 3},
        },
        dataset_ledger=[
            {"dataset_id": "train", "role": "train", "checksum": "sha256:train"},
            {"dataset_id": "validation", "role": "validation", "checksum": "sha256:validation"},
        ],
        model_config_ledger=[{"config_id": "model-small", "architecture": "fixture_transformer"}],
        training_config_ledger=[
            {"config_id": "train-small", "model_config_id": "model-small", "optimizer": "adamw"}
        ],
        metric_schema=[
            {
                "metric_id": "validation-loss",
                "name": "validation_loss",
                "value": 0.9,
                "threshold": {"max": 1.0},
                "passed": True,
            }
        ],
        scaling_probes=[{"probe_id": "scaling", "status": "supports_claim"}],
        optimization_probes=[{"probe_id": "optimization", "status": "supports_claim"}],
        theorem_empirical_boundary={
            "boundary_id": "boundary-1",
            "claim_id": "claim-1",
            "empirical_status": "bounded_empirical_support",
            "theorem_status": "not_theorem",
            "not_theorem_grade": True,
        },
    ).to_dict()

    assert gate["approved"] is True
    assert gate["decision"] == "ml_theory_empirically_supported"
    assert gate["checks"]["scaling_probes_declared"] is True
    assert gate["checks"]["optimization_probes_declared"] is True
    assert gate["warnings"][0]["code"] == "bounded_empirical_evidence_not_proof"


def test_ml_theory_gate_blocks_theorem_grade_misclassification() -> None:
    gate = evaluate_ml_theory_gate(
        claim={
            "object_id": "claim-1",
            "statement": "Validation loss decreases across all model families.",
            "confidence": "theorem_grade",
        },
        experiment_manifest={
            "experiment_id": "exp-1",
            "deterministic": True,
            "seed": 7,
            "budget": {"max_train_runs": 2},
        },
        dataset_ledger=[{"dataset_id": "validation", "role": "validation", "checksum": "sha256:validation"}],
        model_config_ledger=[{"config_id": "model-small", "architecture": "fixture_transformer"}],
        training_config_ledger=[
            {"config_id": "train-small", "model_config_id": "model-small", "optimizer": "adamw"}
        ],
        metric_schema=[
            {
                "metric_id": "validation-loss",
                "name": "validation_loss",
                "value": 0.9,
                "threshold": {"max": 1.0},
                "passed": True,
            }
        ],
        scaling_probes=[{"probe_id": "scaling", "status": "supports_claim"}],
        optimization_probes=[{"probe_id": "optimization", "status": "supports_claim"}],
        theorem_empirical_boundary={
            "boundary_id": "boundary-1",
            "claim_id": "claim-1",
            "empirical_status": "bounded_empirical_support",
            "theorem_status": "proof",
            "proof_artifact_ids": [],
            "not_theorem_grade": False,
        },
    ).to_dict()

    assert gate["approved"] is False
    assert gate["decision"] == "empirical_claim_misclassified_as_theorem"
    assert "empirical_claim_misclassified_as_theorem" in gate["statuses"]


def test_research_object_review_approves_fixture_with_all_non_proof_gates(tmp_path: Path) -> None:
    payload = run_research_review_fixture(fixture=RESEARCH_REVIEW_FIXTURE, output_dir=tmp_path / "review")
    gates = {item["gate"]: item for item in payload["gates"]}

    assert payload["schema_version"] == "amra.research_object_review.v1"
    assert payload["approved"] is True
    assert payload["decision"] == "approved"
    assert set(gates) == {
        "novelty",
        "reproducibility",
        "statistical",
        "benchmark",
        "model_validation",
        "security",
        "theory_coherence",
    }
    assert gates["novelty"]["decision"] == "novelty_reviewed"
    assert gates["reproducibility"]["checks"]["rerun_passed"] is True
    assert gates["statistical"]["checks"]["not_theorem_grade"] is True
    assert gates["benchmark"]["checks"]["traceable_to_baseline"] is True
    assert gates["model_validation"]["approved"] is True
    assert gates["security"]["approved"] is True
    assert gates["theory_coherence"]["approved"] is True
    assert (tmp_path / "review" / "research_review_report.json").exists()


def test_research_object_review_blocks_duplicate_unreproducible_and_bad_statistics() -> None:
    payload = _read_json(RESEARCH_REVIEW_FIXTURE)
    payload["novelty_report"]["status"] = "duplicate"
    payload["reproducibility_report"]["status"] = "not_rerun"
    payload["statistical_evidence"]["confidence"] = "theorem_grade"
    payload["benchmark_gate_inputs"]["decision"] = "baseline_unfair"
    payload["benchmark_gate_inputs"]["checks"]["baseline_fair"] = False

    report = evaluate_research_object_review(payload).to_dict()
    blocker_codes = {item["code"] for item in report["blocking_decisions"]}

    assert report["approved"] is False
    assert report["decision"] == "blocked"
    assert {
        "duplicate_claim",
        "reproduction_not_passed",
        "statistical_claim_misclassified_as_proof",
        "baseline_unfair",
    } <= blocker_codes
