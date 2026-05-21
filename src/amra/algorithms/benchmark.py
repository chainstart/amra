from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from amra.algorithms.complexity import empirical_complexity_summary
from amra.orchestration.workstreams import utc_now_iso
from amra.portfolio_memory import write_json
from amra.research.objects import AlgorithmRecord, ResearchConfidence, ResearchObjectStatus


ALGORITHM_SPEC_SCHEMA_VERSION = "amra.algorithm_spec.v1"
ALGORITHM_VARIANT_BENCHMARK_SCHEMA_VERSION = "amra.algorithm_variant_benchmark.v1"
ALGORITHM_BENCHMARK_RUN_SCHEMA_VERSION = "amra.algorithm_benchmark_run.v1"
ALGORITHM_BENCHMARK_GATE_SCHEMA_VERSION = "amra.algorithm_benchmark_gate.v1"

ALGORITHM_BENCHMARK_RUN_FILE = "algorithm_benchmark_run.json"
ALGORITHM_SPEC_FILE = "algorithm_spec.json"
ALGORITHM_BENCHMARK_RESULTS_FILE = "benchmark_results.json"
ALGORITHM_PROFILING_METADATA_FILE = "profiling_metadata.json"
ALGORITHM_OPTIMIZATION_TRACES_FILE = "optimization_traces.json"
ALGORITHM_REGRESSION_RISKS_FILE = "regression_risks.json"
ALGORITHM_BENCHMARK_GATE_INPUTS_FILE = "benchmark_gate_inputs.json"


def _dict_value(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _list_value(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    items = value if isinstance(value, list) else [value]
    return [str(item) for item in items]


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _slug(value: str) -> str:
    normalized = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    parts = [part for part in normalized.split("-") if part]
    return "-".join(parts) or "algorithm"


def _metric_direction(benchmark: dict[str, Any], metric_name: str) -> str:
    metrics = _list_value(benchmark.get("metrics"))
    for metric in metrics:
        if isinstance(metric, dict) and str(metric.get("name")) == metric_name:
            return str(metric.get("direction") or "lower_is_better")
    return str(benchmark.get("metric_direction") or "lower_is_better")


def _metric_improvement_pct(*, baseline: float, candidate: float, direction: str) -> float:
    if baseline == 0:
        return 0.0
    if direction == "higher_is_better":
        return ((candidate - baseline) / abs(baseline)) * 100.0
    return ((baseline - candidate) / abs(baseline)) * 100.0


@dataclass(slots=True)
class AlgorithmProblemSpec:
    object_id: str
    title: str
    problem_spec: str
    domain: str = ""
    tags: list[str] = field(default_factory=list)
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    constraints: dict[str, Any] = field(default_factory=dict)
    complexity_claims: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AlgorithmProblemSpec":
        object_id = str(payload.get("object_id") or payload.get("id") or _slug(str(payload.get("title") or "algorithm")))
        return cls(
            object_id=object_id,
            title=str(payload.get("title") or object_id),
            problem_spec=str(payload.get("problem_spec") or payload.get("statement") or ""),
            domain=str(payload.get("domain") or ""),
            tags=_string_list(payload.get("tags")),
            input_schema=_dict_value(payload.get("input_schema")),
            output_schema=_dict_value(payload.get("output_schema")),
            constraints=_dict_value(payload.get("constraints")),
            complexity_claims=_string_list(payload.get("complexity_claims")),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": ALGORITHM_SPEC_SCHEMA_VERSION,
            "object_id": self.object_id,
            "object_type": "algorithm",
            "title": self.title,
            "problem_spec": self.problem_spec,
            "domain": self.domain,
            "tags": list(self.tags),
            "input_schema": dict(self.input_schema),
            "output_schema": dict(self.output_schema),
            "constraints": dict(self.constraints),
            "complexity_claims": list(self.complexity_claims),
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class AlgorithmVariantBenchmark:
    variant_id: str
    role: str
    title: str
    metrics: dict[str, float]
    baseline_id: str = ""
    implementation: str = ""
    profile: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any], *, role: str) -> "AlgorithmVariantBenchmark":
        variant_id = str(payload.get("variant_id") or payload.get("id") or payload.get("object_id") or role)
        metrics: dict[str, float] = {}
        for key, value in _dict_value(payload.get("metrics")).items():
            number = _number(value)
            if number is not None:
                metrics[str(key)] = number
        return cls(
            variant_id=variant_id,
            role=role,
            title=str(payload.get("title") or variant_id),
            metrics=metrics,
            baseline_id=str(payload.get("baseline_id") or ""),
            implementation=str(payload.get("implementation") or ""),
            profile=_dict_value(payload.get("profile")),
            output_schema=_dict_value(payload.get("output_schema")),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": ALGORITHM_VARIANT_BENCHMARK_SCHEMA_VERSION,
            "variant_id": self.variant_id,
            "role": self.role,
            "title": self.title,
            "baseline_id": self.baseline_id,
            "implementation": self.implementation,
            "metrics": dict(self.metrics),
            "profile": dict(self.profile),
            "output_schema": dict(self.output_schema),
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ProfilingMetadataRecord:
    profile_id: str
    variant_id: str
    profiler: str
    metrics: dict[str, float]
    samples: int = 0
    environment: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "variant_id": self.variant_id,
            "profiler": self.profiler,
            "metrics": dict(self.metrics),
            "samples": self.samples,
            "environment": dict(self.environment),
            "notes": list(self.notes),
        }


@dataclass(slots=True)
class OptimizationTraceRecord:
    trace_id: str
    candidate_id: str
    baseline_id: str
    primary_metric: str
    direction: str
    before: float
    after: float
    improvement_pct: float
    steps: list[str] = field(default_factory=list)
    complexity_claims: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "candidate_id": self.candidate_id,
            "baseline_id": self.baseline_id,
            "primary_metric": self.primary_metric,
            "direction": self.direction,
            "before": self.before,
            "after": self.after,
            "improvement_pct": self.improvement_pct,
            "steps": list(self.steps),
            "complexity_claims": list(self.complexity_claims),
        }


@dataclass(slots=True)
class RegressionRiskRecord:
    risk_id: str
    candidate_id: str
    baseline_id: str
    metric: str
    severity: str
    description: str
    observed_delta_pct: float = 0.0
    mitigation: str = ""
    gate_blocking: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "risk_id": self.risk_id,
            "candidate_id": self.candidate_id,
            "baseline_id": self.baseline_id,
            "metric": self.metric,
            "severity": self.severity,
            "description": self.description,
            "observed_delta_pct": self.observed_delta_pct,
            "mitigation": self.mitigation,
            "gate_blocking": self.gate_blocking,
        }


@dataclass(slots=True)
class BenchmarkGateInput:
    benchmark_id: str
    primary_metric: str
    statuses: list[str]
    decision: str
    checks: dict[str, Any]
    traces: list[str] = field(default_factory=list)
    regression_risks: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": ALGORITHM_BENCHMARK_GATE_SCHEMA_VERSION,
            "benchmark_id": self.benchmark_id,
            "primary_metric": self.primary_metric,
            "statuses": list(self.statuses),
            "decision": self.decision,
            "checks": dict(self.checks),
            "traces": list(self.traces),
            "regression_risks": list(self.regression_risks),
        }


class AlgorithmBenchmarkRunner:
    def run_fixture(self, *, fixture: Path, output_dir: Path) -> dict[str, Any]:
        fixture_path = fixture.expanduser().resolve()
        output_dir = output_dir.expanduser().resolve()
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("algorithm benchmark fixture must be a JSON object")

        algorithm = AlgorithmProblemSpec.from_dict(_dict_value(payload.get("algorithm") or payload.get("algorithm_spec")))
        benchmark = _dict_value(payload.get("benchmark"))
        benchmark_id = str(benchmark.get("benchmark_id") or benchmark.get("id") or f"benchmark-{_slug(algorithm.object_id)}")
        primary_metric = str(benchmark.get("primary_metric") or "runtime_ms")
        direction = _metric_direction(benchmark, primary_metric)
        baselines = [
            AlgorithmVariantBenchmark.from_dict(item, role="baseline")
            for item in _list_value(payload.get("baselines"))
            if isinstance(item, dict)
        ]
        candidates = [
            AlgorithmVariantBenchmark.from_dict(item, role="candidate")
            for item in _list_value(payload.get("candidates"))
            if isinstance(item, dict)
        ]
        if not baselines:
            raise ValueError("algorithm benchmark fixture requires at least one baseline")
        if not candidates:
            raise ValueError("algorithm benchmark fixture requires at least one candidate")

        fixture_hash = _sha256_file(fixture_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        baseline_by_id = {item.variant_id: item for item in baselines}
        default_baseline_id = baselines[0].variant_id
        for candidate in candidates:
            if not candidate.baseline_id:
                candidate.baseline_id = default_baseline_id

        traces = self._optimization_traces(
            candidates=candidates,
            baseline_by_id=baseline_by_id,
            payload=payload,
            primary_metric=primary_metric,
            direction=direction,
        )
        risks = self._regression_risks(
            candidates=candidates,
            baseline_by_id=baseline_by_id,
            benchmark=benchmark,
            primary_metric=primary_metric,
        )
        profiling = self._profiling_metadata(
            variants=[*baselines, *candidates],
            payload=payload,
        )
        gate = self._benchmark_gate(
            benchmark=benchmark,
            benchmark_id=benchmark_id,
            primary_metric=primary_metric,
            baselines=baselines,
            candidates=candidates,
            traces=traces,
            risks=risks,
        )
        algorithm_record = self._algorithm_record(
            algorithm=algorithm,
            baselines=baselines,
            candidates=candidates,
            benchmark_id=benchmark_id,
            profiling=profiling,
            risks=risks,
            gate=gate,
        )
        comparisons = [
            self._comparison(candidate=item, baseline_by_id=baseline_by_id, primary_metric=primary_metric, direction=direction)
            for item in candidates
        ]
        benchmark_results = {
            "schema_version": "amra.algorithm_benchmark_results.v1",
            "benchmark_id": benchmark_id,
            "primary_metric": primary_metric,
            "direction": direction,
            "baselines": [item.to_dict() for item in baselines],
            "candidates": [item.to_dict() for item in candidates],
            "comparisons": comparisons,
            "empirical_complexity": empirical_complexity_summary(comparisons),
        }
        spec_payload = algorithm.to_dict()
        spec_payload["algorithm_record"] = algorithm_record.to_dict()
        gate_payload = gate.to_dict()
        run = {
            "schema_version": ALGORITHM_BENCHMARK_RUN_SCHEMA_VERSION,
            "status": "succeeded" if gate.decision == "benchmark_passed" else "needs_review",
            "generated_at": utc_now_iso(),
            "deterministic": True,
            "fixture": {"path": str(fixture_path), "sha256": fixture_hash},
            "output_dir": str(output_dir),
            "algorithm": algorithm_record.to_dict(),
            "benchmark_results": benchmark_results,
            "profiling_metadata": [item.to_dict() for item in profiling],
            "optimization_traces": [item.to_dict() for item in traces],
            "regression_risks": [item.to_dict() for item in risks],
            "benchmark_gate_inputs": gate_payload,
            "record_files": {
                "run": str(output_dir / ALGORITHM_BENCHMARK_RUN_FILE),
                "algorithm_spec": str(output_dir / ALGORITHM_SPEC_FILE),
                "benchmark_results": str(output_dir / ALGORITHM_BENCHMARK_RESULTS_FILE),
                "profiling_metadata": str(output_dir / ALGORITHM_PROFILING_METADATA_FILE),
                "optimization_traces": str(output_dir / ALGORITHM_OPTIMIZATION_TRACES_FILE),
                "regression_risks": str(output_dir / ALGORITHM_REGRESSION_RISKS_FILE),
                "benchmark_gate_inputs": str(output_dir / ALGORITHM_BENCHMARK_GATE_INPUTS_FILE),
            },
        }
        write_json(output_dir / ALGORITHM_SPEC_FILE, spec_payload)
        write_json(output_dir / ALGORITHM_BENCHMARK_RESULTS_FILE, benchmark_results)
        write_json(output_dir / ALGORITHM_PROFILING_METADATA_FILE, [item.to_dict() for item in profiling])
        write_json(output_dir / ALGORITHM_OPTIMIZATION_TRACES_FILE, [item.to_dict() for item in traces])
        write_json(output_dir / ALGORITHM_REGRESSION_RISKS_FILE, [item.to_dict() for item in risks])
        write_json(output_dir / ALGORITHM_BENCHMARK_GATE_INPUTS_FILE, gate_payload)
        write_json(output_dir / ALGORITHM_BENCHMARK_RUN_FILE, run)
        return run

    def _optimization_traces(
        self,
        *,
        candidates: list[AlgorithmVariantBenchmark],
        baseline_by_id: dict[str, AlgorithmVariantBenchmark],
        payload: dict[str, Any],
        primary_metric: str,
        direction: str,
    ) -> list[OptimizationTraceRecord]:
        declared = {str(item.get("candidate_id") or item.get("variant_id") or ""): item for item in _list_value(payload.get("optimization_traces")) if isinstance(item, dict)}
        traces: list[OptimizationTraceRecord] = []
        for candidate in candidates:
            baseline = baseline_by_id.get(candidate.baseline_id) or next(iter(baseline_by_id.values()))
            before = baseline.metrics.get(primary_metric)
            after = candidate.metrics.get(primary_metric)
            if before is None or after is None:
                continue
            spec = _dict_value(declared.get(candidate.variant_id))
            traces.append(
                OptimizationTraceRecord(
                    trace_id=str(spec.get("trace_id") or f"optimization-trace-{_slug(candidate.variant_id)}"),
                    candidate_id=candidate.variant_id,
                    baseline_id=baseline.variant_id,
                    primary_metric=primary_metric,
                    direction=direction,
                    before=before,
                    after=after,
                    improvement_pct=round(_metric_improvement_pct(baseline=before, candidate=after, direction=direction), 6),
                    steps=_string_list(spec.get("steps") or candidate.metadata.get("optimization_steps")),
                    complexity_claims=_string_list(spec.get("complexity_claims") or candidate.metadata.get("complexity_claims")),
                )
            )
        return traces

    def _regression_risks(
        self,
        *,
        candidates: list[AlgorithmVariantBenchmark],
        baseline_by_id: dict[str, AlgorithmVariantBenchmark],
        benchmark: dict[str, Any],
        primary_metric: str,
    ) -> list[RegressionRiskRecord]:
        max_allowed = float(_number(_dict_value(benchmark.get("gate")).get("max_allowed_regression_pct")) or 5.0)
        risks: list[RegressionRiskRecord] = []
        for candidate in candidates:
            baseline = baseline_by_id.get(candidate.baseline_id) or next(iter(baseline_by_id.values()))
            for metric, candidate_value in candidate.metrics.items():
                baseline_value = baseline.metrics.get(metric)
                if baseline_value is None:
                    continue
                direction = _metric_direction(benchmark, metric)
                improvement = _metric_improvement_pct(baseline=baseline_value, candidate=candidate_value, direction=direction)
                if improvement < 0:
                    delta = abs(improvement)
                    blocking = delta > max_allowed
                    risks.append(
                        RegressionRiskRecord(
                            risk_id=f"regression-risk-{_slug(candidate.variant_id)}-{_slug(metric)}",
                            candidate_id=candidate.variant_id,
                            baseline_id=baseline.variant_id,
                            metric=metric,
                            severity="high" if blocking else "medium",
                            description=f"{metric} regressed by {delta:.2f}% versus {baseline.variant_id}.",
                            observed_delta_pct=round(delta, 6),
                            mitigation="Require benchmark gate review before promotion.",
                            gate_blocking=blocking,
                        )
                    )
            if any(trace.candidate_id == candidate.variant_id and trace.improvement_pct > 0 for trace in self._optimization_traces(
                candidates=[candidate],
                baseline_by_id=baseline_by_id,
                payload={},
                primary_metric=primary_metric,
                direction=_metric_direction(benchmark, primary_metric),
            )):
                risks.append(
                    RegressionRiskRecord(
                        risk_id=f"regression-risk-{_slug(candidate.variant_id)}-overfit",
                        candidate_id=candidate.variant_id,
                        baseline_id=baseline.variant_id,
                        metric=primary_metric,
                        severity="low",
                        description="Primary metric improved; monitor for benchmark overfitting and hidden-case regressions.",
                        mitigation="Keep fixed benchmark inputs and require independent review before theory promotion.",
                        gate_blocking=False,
                    )
                )
        return risks

    def _profiling_metadata(
        self,
        *,
        variants: list[AlgorithmVariantBenchmark],
        payload: dict[str, Any],
    ) -> list[ProfilingMetadataRecord]:
        environment = _dict_value(payload.get("environment"))
        records: list[ProfilingMetadataRecord] = []
        for variant in variants:
            profile = _dict_value(variant.profile)
            profiler = str(profile.get("profiler") or payload.get("profiler") or "fixture_profiler")
            samples = int(_number(profile.get("samples")) or _number(profile.get("sample_count")) or 0)
            records.append(
                ProfilingMetadataRecord(
                    profile_id=f"profile-{_slug(variant.variant_id)}",
                    variant_id=variant.variant_id,
                    profiler=profiler,
                    metrics=dict(variant.metrics),
                    samples=samples,
                    environment=environment,
                    notes=_string_list(profile.get("notes")),
                )
            )
        return records

    def _benchmark_gate(
        self,
        *,
        benchmark: dict[str, Any],
        benchmark_id: str,
        primary_metric: str,
        baselines: list[AlgorithmVariantBenchmark],
        candidates: list[AlgorithmVariantBenchmark],
        traces: list[OptimizationTraceRecord],
        risks: list[RegressionRiskRecord],
    ) -> BenchmarkGateInput:
        fixed_inputs = _list_value(benchmark.get("fixed_inputs") or benchmark.get("cases"))
        metric_names = {
            str(metric.get("name"))
            for metric in _list_value(benchmark.get("metrics"))
            if isinstance(metric, dict) and metric.get("name")
        }
        baseline_ids = {item.variant_id for item in baselines}
        checks = {
            "baseline_fair": all((not item.baseline_id) or item.baseline_id in baseline_ids for item in candidates),
            "benchmark_fixed": bool(benchmark_id and fixed_inputs),
            "metric_valid": primary_metric in metric_names and all(primary_metric in item.metrics for item in [*baselines, *candidates]),
            "case_count": len(fixed_inputs),
            "candidate_count": len(candidates),
            "traceable_to_baseline": all(item.baseline_id in baseline_ids for item in candidates),
            "regression_count": sum(1 for item in risks if item.gate_blocking),
        }
        statuses: list[str] = []
        if not checks["baseline_fair"] or not checks["traceable_to_baseline"]:
            statuses.append("baseline_unfair")
        if not checks["benchmark_fixed"]:
            statuses.append("insufficient_cases")
        if not checks["metric_valid"]:
            statuses.append("metric_invalid")
        if checks["case_count"] < 2:
            statuses.append("insufficient_cases")
        if checks["regression_count"]:
            statuses.append("benchmark_regression")
        if not statuses:
            statuses.append("benchmark_passed")
        return BenchmarkGateInput(
            benchmark_id=benchmark_id,
            primary_metric=primary_metric,
            statuses=statuses,
            decision=statuses[0],
            checks=checks,
            traces=[item.trace_id for item in traces],
            regression_risks=[item.risk_id for item in risks],
        )

    def _algorithm_record(
        self,
        *,
        algorithm: AlgorithmProblemSpec,
        baselines: list[AlgorithmVariantBenchmark],
        candidates: list[AlgorithmVariantBenchmark],
        benchmark_id: str,
        profiling: list[ProfilingMetadataRecord],
        risks: list[RegressionRiskRecord],
        gate: BenchmarkGateInput,
    ) -> AlgorithmRecord:
        complexity_claims = list(algorithm.complexity_claims)
        for candidate in candidates:
            complexity_claims.extend(_string_list(candidate.metadata.get("complexity_claims")))
        return AlgorithmRecord(
            object_id=algorithm.object_id,
            title=algorithm.title,
            status=ResearchObjectStatus.EMPIRICALLY_SUPPORTED
            if gate.decision == "benchmark_passed"
            else ResearchObjectStatus.TESTING,
            statement=algorithm.problem_spec,
            domain=algorithm.domain,
            tags=sorted(set(["algorithm_benchmark", *algorithm.tags])),
            confidence=ResearchConfidence.MEDIUM if gate.decision == "benchmark_passed" else ResearchConfidence.LOW,
            problem_spec=algorithm.problem_spec,
            baseline_ids=[item.variant_id for item in baselines],
            candidate_ids=[item.variant_id for item in candidates],
            complexity_claims=complexity_claims,
            benchmark_ids=[benchmark_id],
            profiling_reports=[item.profile_id for item in profiling],
            regression_risks=[item.risk_id for item in risks],
            metadata={
                "benchmark_gate_decision": gate.decision,
                "benchmark_gate_statuses": list(gate.statuses),
                "input_schema": dict(algorithm.input_schema),
                "output_schema": dict(algorithm.output_schema),
            },
        )

    def _comparison(
        self,
        *,
        candidate: AlgorithmVariantBenchmark,
        baseline_by_id: dict[str, AlgorithmVariantBenchmark],
        primary_metric: str,
        direction: str,
    ) -> dict[str, Any]:
        baseline = baseline_by_id.get(candidate.baseline_id) or next(iter(baseline_by_id.values()))
        baseline_value = baseline.metrics.get(primary_metric)
        candidate_value = candidate.metrics.get(primary_metric)
        improvement = 0.0
        if baseline_value is not None and candidate_value is not None:
            improvement = _metric_improvement_pct(baseline=baseline_value, candidate=candidate_value, direction=direction)
        return {
            "candidate_id": candidate.variant_id,
            "baseline_id": baseline.variant_id,
            "primary_metric": primary_metric,
            "baseline_value": baseline_value,
            "candidate_value": candidate_value,
            "improvement_pct": round(improvement, 6),
        }


def run_algorithm_benchmark_fixture(*, fixture: Path, output_dir: Path) -> dict[str, Any]:
    return AlgorithmBenchmarkRunner().run_fixture(fixture=fixture, output_dir=output_dir)
