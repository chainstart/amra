from __future__ import annotations

import json
from pathlib import Path

from amra.cli import main
from amra.research import (
    RESEARCH_EXECUTOR_REQUEST_FILE,
    RESEARCH_EXPERIMENT_RECORD_FILE,
    RESEARCH_EXPERIMENT_RESULT_FILE,
    RESEARCH_REPRODUCIBILITY_REPORT_FILE,
    ExperimentRecord,
    ResearchExecutorRequest,
    ResearchExecutorResult,
    run_research_executor_fixture,
)


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "research_experiment_fixture.json"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_research_executor_persists_request_result_record_and_reproducibility_report(tmp_path: Path) -> None:
    output = tmp_path / "experiment"

    payload = run_research_executor_fixture(fixture=FIXTURE, output_dir=output)

    request = _read_json(output / RESEARCH_EXECUTOR_REQUEST_FILE)
    result = _read_json(output / RESEARCH_EXPERIMENT_RESULT_FILE)
    record = _read_json(output / RESEARCH_EXPERIMENT_RECORD_FILE)
    report = _read_json(output / RESEARCH_REPRODUCIBILITY_REPORT_FILE)

    request_record = ResearchExecutorRequest.from_dict(request)
    result_record = ResearchExecutorResult.from_dict(result)

    assert payload["status"] == "succeeded"
    assert request_record.request_hash == report["request_sha256"]
    assert result_record.status == "succeeded"
    assert ExperimentRecord.from_dict(record).object_id == "experiment-fixture-001"
    assert record["rerun_status"] == "reproduced"
    assert record["reproducibility_report"]["rerun_key"] == report["rerun_key"]
    assert report["deterministic"] is True
    assert report["fixture"]["sha256"]
    assert report["request_sha256"]
    assert (output / "observations.json").exists()
    assert (output / "summary.md").exists()
    assert {item["path"] for item in result["artifacts"]} == {"observations.json", "summary.md"}


def test_research_executor_rerun_key_is_stable_across_output_directories(tmp_path: Path) -> None:
    first = run_research_executor_fixture(fixture=FIXTURE, output_dir=tmp_path / "first")
    second = run_research_executor_fixture(fixture=FIXTURE, output_dir=tmp_path / "second")

    assert first["reproducibility_report"]["rerun_key"] == second["reproducibility_report"]["rerun_key"]
    assert first["reproducibility_report"]["request_sha256"] == second["reproducibility_report"]["request_sha256"]


def test_research_run_executor_cli_accepts_required_smoke_shape(tmp_path: Path, capsys) -> None:
    output = tmp_path / "cli-experiment"

    exit_code = main(["research", "run-executor", "--fixture", str(FIXTURE), "--out", str(output), "--json"])
    printed = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert printed["status"] == "succeeded"
    assert printed["experiment_record"]["object_type"] == "experiment"
    assert (output / RESEARCH_REPRODUCIBILITY_REPORT_FILE).exists()
