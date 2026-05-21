from __future__ import annotations

import json
from pathlib import Path

from amra.algorithms import (
    ALGORITHM_BENCHMARK_GATE_INPUTS_FILE,
    ALGORITHM_BENCHMARK_RESULTS_FILE,
    ALGORITHM_BENCHMARK_RUN_FILE,
    ALGORITHM_OPTIMIZATION_TRACES_FILE,
    ALGORITHM_PROFILING_METADATA_FILE,
    ALGORITHM_REGRESSION_RISKS_FILE,
    ALGORITHM_SPEC_FILE,
    AlgorithmProblemSpec,
    AlgorithmVariantBenchmark,
    run_algorithm_benchmark_fixture,
)
from amra.cli import main
from amra.research import AlgorithmRecord, ResearchObjectRecord


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "algorithm_benchmark_fixture.json"


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_algorithm_benchmark_persists_schema_pack_and_gate_inputs(tmp_path: Path) -> None:
    output = tmp_path / "algorithm-benchmark"

    payload = run_algorithm_benchmark_fixture(fixture=FIXTURE, output_dir=output)

    algorithm_spec = _read_json(output / ALGORITHM_SPEC_FILE)
    benchmark_results = _read_json(output / ALGORITHM_BENCHMARK_RESULTS_FILE)
    profiling = _read_json(output / ALGORITHM_PROFILING_METADATA_FILE)
    traces = _read_json(output / ALGORITHM_OPTIMIZATION_TRACES_FILE)
    risks = _read_json(output / ALGORITHM_REGRESSION_RISKS_FILE)
    gate = _read_json(output / ALGORITHM_BENCHMARK_GATE_INPUTS_FILE)

    restored_algorithm = ResearchObjectRecord.from_dict(algorithm_spec["algorithm_record"])
    baseline = AlgorithmVariantBenchmark.from_dict(benchmark_results["baselines"][0], role="baseline")
    candidate = AlgorithmVariantBenchmark.from_dict(benchmark_results["candidates"][0], role="candidate")

    assert payload["schema_version"] == "amra.algorithm_benchmark_run.v1"
    assert payload["status"] == "succeeded"
    assert isinstance(restored_algorithm, AlgorithmRecord)
    assert AlgorithmProblemSpec.from_dict(algorithm_spec).object_id == "algorithm-sparse-dp-001"
    assert baseline.variant_id == "baseline-dense-dp"
    assert candidate.baseline_id == "baseline-dense-dp"
    assert benchmark_results["comparisons"][0]["improvement_pct"] == 40.0
    assert {item["variant_id"] for item in profiling} == {"baseline-dense-dp", "candidate-sparse-dp"}
    assert traces[0]["baseline_id"] == "baseline-dense-dp"
    assert traces[0]["improvement_pct"] == 40.0
    assert {item["severity"] for item in risks} == {"low", "medium"}
    assert all(item["gate_blocking"] is False for item in risks)
    assert gate["decision"] == "benchmark_passed"
    assert gate["checks"]["benchmark_fixed"] is True
    assert gate["checks"]["traceable_to_baseline"] is True
    assert gate["traces"] == ["trace-sparse-dp-fixture"]
    assert (output / ALGORITHM_BENCHMARK_RUN_FILE).exists()


def test_algorithm_benchmark_gate_blocks_unfair_baseline(tmp_path: Path) -> None:
    fixture_payload = _read_json(FIXTURE)
    fixture_payload["candidates"][0]["baseline_id"] = "missing-baseline"
    fixture = tmp_path / "unfair_fixture.json"
    fixture.write_text(json.dumps(fixture_payload), encoding="utf-8")

    payload = run_algorithm_benchmark_fixture(fixture=fixture, output_dir=tmp_path / "out")

    assert payload["status"] == "needs_review"
    assert payload["benchmark_gate_inputs"]["decision"] == "baseline_unfair"
    assert "baseline_unfair" in payload["benchmark_gate_inputs"]["statuses"]


def test_algorithms_run_benchmark_cli_accepts_required_smoke_shape(tmp_path: Path, capsys) -> None:
    output = tmp_path / "cli-algorithm-benchmark"

    exit_code = main(["algorithms", "run-benchmark", "--fixture", str(FIXTURE), "--out", str(output), "--json"])
    printed = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert printed["schema_version"] == "amra.algorithm_benchmark_run.v1"
    assert printed["benchmark_gate_inputs"]["decision"] == "benchmark_passed"
    assert printed["algorithm"]["object_type"] == "algorithm"
    assert (output / ALGORITHM_BENCHMARK_GATE_INPUTS_FILE).exists()
