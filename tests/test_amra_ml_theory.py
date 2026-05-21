from __future__ import annotations

import json
from pathlib import Path

from amra.cli import main
from amra.ml_theory import (
    ML_THEORY_BOUNDARY_FILE,
    ML_THEORY_CLAIM_RECORD_FILE,
    ML_THEORY_DATASET_LEDGER_FILE,
    ML_THEORY_EXPERIMENT_MANIFEST_FILE,
    ML_THEORY_GATE_INPUTS_FILE,
    ML_THEORY_METRIC_SCHEMA_FILE,
    ML_THEORY_MODEL_CONFIG_LEDGER_FILE,
    ML_THEORY_OPTIMIZATION_PROBES_FILE,
    ML_THEORY_RUN_FILE,
    ML_THEORY_SCALING_PROBES_FILE,
    ML_THEORY_TRAINING_CONFIG_LEDGER_FILE,
    MLDatasetLedgerEntry,
    MLModelConfigEntry,
    MLTheoryExperimentManifest,
    MLTheoryMetric,
    MLTrainingConfigEntry,
    run_ml_theory_experiment_fixture,
)
from amra.research import MLTheoryClaimRecord, ResearchObjectRecord


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "ml_theory_fixture.json"


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_ml_theory_run_persists_claim_ledgers_probes_and_boundary(tmp_path: Path) -> None:
    output = tmp_path / "ml-theory"

    payload = run_ml_theory_experiment_fixture(fixture=FIXTURE, output_dir=output)

    claim = _read_json(output / ML_THEORY_CLAIM_RECORD_FILE)
    manifest = _read_json(output / ML_THEORY_EXPERIMENT_MANIFEST_FILE)
    datasets = _read_json(output / ML_THEORY_DATASET_LEDGER_FILE)
    model_configs = _read_json(output / ML_THEORY_MODEL_CONFIG_LEDGER_FILE)
    training_configs = _read_json(output / ML_THEORY_TRAINING_CONFIG_LEDGER_FILE)
    metrics = _read_json(output / ML_THEORY_METRIC_SCHEMA_FILE)
    scaling_probes = _read_json(output / ML_THEORY_SCALING_PROBES_FILE)
    optimization_probes = _read_json(output / ML_THEORY_OPTIMIZATION_PROBES_FILE)
    boundary = _read_json(output / ML_THEORY_BOUNDARY_FILE)
    gate = _read_json(output / ML_THEORY_GATE_INPUTS_FILE)

    restored_claim = ResearchObjectRecord.from_dict(claim)

    assert payload["schema_version"] == "amra.ml_theory_run.v1"
    assert payload["status"] == "succeeded"
    assert isinstance(restored_claim, MLTheoryClaimRecord)
    assert restored_claim.confidence.value == "medium"
    assert MLTheoryExperimentManifest.from_dict(manifest, claim_id="ml-theory-scaling-001").experiment_id == "exp-ml-theory-scaling-001"
    assert MLDatasetLedgerEntry.from_dict(datasets[0]).dataset_id == "dataset-toy-language-train"
    assert MLModelConfigEntry.from_dict(model_configs[0]).parameter_count == 64000
    assert MLTrainingConfigEntry.from_dict(training_configs[0]).optimizer == "adamw"
    assert MLTheoryMetric.from_dict(metrics[0]).passed is True
    assert scaling_probes[0]["fit"]["law"] == "power_law"
    assert optimization_probes[0]["improvement_pct"] > 0
    assert boundary["theorem_status"] == "not_theorem"
    assert gate["approved"] is True
    assert gate["decision"] == "ml_theory_empirically_supported"
    assert gate["checks"]["empirical_not_theorem_grade"] is True
    assert gate["warnings"][0]["code"] == "bounded_empirical_evidence_not_proof"
    assert (output / ML_THEORY_RUN_FILE).exists()


def test_ml_theory_gate_blocks_failed_metric_threshold(tmp_path: Path) -> None:
    fixture_payload = _read_json(FIXTURE)
    fixture_payload["metrics"][0]["value"] = 1.5
    fixture = tmp_path / "failed_metric_fixture.json"
    fixture.write_text(json.dumps(fixture_payload), encoding="utf-8")

    payload = run_ml_theory_experiment_fixture(fixture=fixture, output_dir=tmp_path / "out")

    assert payload["status"] == "needs_review"
    assert payload["ml_theory_gate_inputs"]["decision"] == "metric_threshold_failed"
    assert "metric_threshold_failed" in payload["ml_theory_gate_inputs"]["statuses"]


def test_ml_theory_cli_accepts_required_smoke_shape(tmp_path: Path, capsys) -> None:
    output = tmp_path / "cli-ml-theory"

    exit_code = main(["ml-theory", "run-experiment", "--fixture", str(FIXTURE), "--out", str(output), "--json"])
    printed = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert printed["schema_version"] == "amra.ml_theory_run.v1"
    assert printed["ml_theory_gate_inputs"]["decision"] == "ml_theory_empirically_supported"
    assert printed["claim"]["object_type"] == "ml_theory_claim"
    assert printed["theorem_empirical_boundary"]["theorem_status"] == "not_theorem"
    assert (output / ML_THEORY_GATE_INPUTS_FILE).exists()
