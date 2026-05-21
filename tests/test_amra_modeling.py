from __future__ import annotations

import json
from pathlib import Path

from amra.cli import main
from amra.modeling import (
    MODEL_CALIBRATION_REPORT_FILE,
    MODEL_FAILURE_MODE_LEDGER_FILE,
    MODEL_SENSITIVITY_REPORT_FILE,
    MODEL_SPEC_FILE,
    MODEL_VALIDATION_GATE_INPUTS_FILE,
    MODEL_VALIDATION_REPORT_FILE,
    MODEL_VALIDATION_RUN_FILE,
    AppliedModelSpec,
    CalibrationReport,
    SensitivityReport,
    ValidationReport,
    run_model_validation_fixture,
)
from amra.research import ModelRecord, ResearchObjectRecord


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "modeling_fixture.json"


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_modeling_validate_persists_model_schema_and_gate_inputs(tmp_path: Path) -> None:
    output = tmp_path / "model-validation"

    payload = run_model_validation_fixture(fixture=FIXTURE, output_dir=output)

    model_spec = _read_json(output / MODEL_SPEC_FILE)
    calibration = _read_json(output / MODEL_CALIBRATION_REPORT_FILE)
    validation = _read_json(output / MODEL_VALIDATION_REPORT_FILE)
    sensitivity = _read_json(output / MODEL_SENSITIVITY_REPORT_FILE)
    failure_modes = _read_json(output / MODEL_FAILURE_MODE_LEDGER_FILE)
    gate = _read_json(output / MODEL_VALIDATION_GATE_INPUTS_FILE)

    restored_model = ResearchObjectRecord.from_dict(model_spec["model_record"])

    assert payload["schema_version"] == "amra.model_validation_run.v1"
    assert payload["status"] == "succeeded"
    assert isinstance(restored_model, ModelRecord)
    assert AppliedModelSpec.from_dict(model_spec).object_id == "model-heat-adoption-001"
    assert CalibrationReport.from_payload({"calibration": calibration}, model_id="model-heat-adoption-001").dataset_ids == [
        "calibration-dataset-2025"
    ]
    assert ValidationReport.from_payload(
        {"validation": validation},
        model_id="model-heat-adoption-001",
        validity_ranges=AppliedModelSpec.from_dict(model_spec).validity_ranges,
    ).dataset_ids == ["validation-dataset-2026"]
    assert SensitivityReport.from_payload({"sensitivity": sensitivity}, model_id="model-heat-adoption-001").dominant_parameters[0] == "beta_temperature"
    assert calibration["datasets"][0]["dataset_id"] != validation["datasets"][0]["dataset_id"]
    assert validation["status"] == "validated"
    assert validation["extrapolation_cases"][0]["case_id"] == "case-heat-extrapolation"
    assert {item["failure_mode"] for item in failure_modes} >= {
        "cohort_shift",
        "extrapolation_outside_validity_range",
    }
    assert gate["approved"] is True
    assert gate["decision"] == "model_validated_with_extrapolation_warning"
    assert gate["checks"]["calibration_validation_separated"] is True
    assert gate["checks"]["extrapolation_detected"] is True
    assert gate["warnings"][0]["code"] == "extrapolation_risk"
    assert (output / MODEL_VALIDATION_RUN_FILE).exists()


def test_modeling_gate_blocks_calibration_validation_overlap(tmp_path: Path) -> None:
    fixture_payload = _read_json(FIXTURE)
    fixture_payload["validation"]["datasets"][0]["dataset_id"] = "calibration-dataset-2025"
    fixture = tmp_path / "overlap_fixture.json"
    fixture.write_text(json.dumps(fixture_payload), encoding="utf-8")

    payload = run_model_validation_fixture(fixture=fixture, output_dir=tmp_path / "out")

    assert payload["status"] == "needs_review"
    assert payload["model_validation_gate_inputs"]["decision"] == "calibration_validation_overlap"
    assert "calibration_validation_overlap" in payload["model_validation_gate_inputs"]["statuses"]


def test_modeling_validate_cli_accepts_required_smoke_shape(tmp_path: Path, capsys) -> None:
    output = tmp_path / "cli-model-validation"

    exit_code = main(["modeling", "validate", "--fixture", str(FIXTURE), "--out", str(output), "--json"])
    printed = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert printed["schema_version"] == "amra.model_validation_run.v1"
    assert printed["model_validation_gate_inputs"]["approved"] is True
    assert printed["model"]["object_type"] == "model"
    assert (output / MODEL_VALIDATION_GATE_INPUTS_FILE).exists()
