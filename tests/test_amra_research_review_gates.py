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


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "modeling_fixture.json"


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
