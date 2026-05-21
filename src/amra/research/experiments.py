from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from amra.orchestration.workstreams import utc_now_iso
from amra.portfolio_memory import write_json
from amra.research.objects import ExperimentRecord, ResearchConfidence, ResearchObjectStatus


RESEARCH_EXECUTOR_REQUEST_SCHEMA_VERSION = "amra.research_executor_request.v1"
RESEARCH_EXECUTOR_RESULT_SCHEMA_VERSION = "amra.research_executor_result.v1"
RESEARCH_REPRODUCIBILITY_REPORT_SCHEMA_VERSION = "amra.research_reproducibility_report.v1"
RESEARCH_EXPERIMENT_FIXTURE_SCHEMA_VERSION = "amra.research_experiment_fixture.v1"

RESEARCH_EXECUTOR_REQUEST_FILE = "research_executor_request.json"
RESEARCH_EXPERIMENT_RESULT_FILE = "research_experiment_result.json"
RESEARCH_EXPERIMENT_RECORD_FILE = "research_experiment_record.json"
RESEARCH_REPRODUCIBILITY_REPORT_FILE = "research_reproducibility_report.json"


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    items = value if isinstance(value, (list, tuple, set)) else [value]
    return [str(item) for item in items]


def _dict_value(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_text_artifact(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_json_artifact(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


@dataclass(slots=True)
class ResearchExecutorRequest:
    request_id: str
    experiment_id: str
    title: str
    question: str = ""
    method: str = "fixture_replay"
    inputs: list[str] = field(default_factory=list)
    parameters: dict[str, Any] = field(default_factory=dict)
    seed: int | str | None = None
    budget: dict[str, Any] = field(default_factory=dict)
    environment: dict[str, Any] = field(default_factory=dict)
    command: list[str] = field(default_factory=list)
    expected_outputs: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.inputs = _string_list(self.inputs)
        self.parameters = _dict_value(self.parameters)
        self.budget = _dict_value(self.budget)
        self.environment = _dict_value(self.environment)
        self.command = _string_list(self.command)
        self.expected_outputs = _dict_value(self.expected_outputs)
        self.metadata = _dict_value(self.metadata)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ResearchExecutorRequest":
        experiment_id = str(payload.get("experiment_id") or payload.get("object_id") or payload["request_id"])
        return cls(
            request_id=str(payload["request_id"]),
            experiment_id=experiment_id,
            title=str(payload.get("title") or experiment_id),
            question=str(payload.get("question") or ""),
            method=str(payload.get("method") or "fixture_replay"),
            inputs=_string_list(payload.get("inputs")),
            parameters=_dict_value(payload.get("parameters")),
            seed=payload.get("seed"),
            budget=_dict_value(payload.get("budget")),
            environment=_dict_value(payload.get("environment")),
            command=_string_list(payload.get("command")),
            expected_outputs=_dict_value(payload.get("expected_outputs")),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": RESEARCH_EXECUTOR_REQUEST_SCHEMA_VERSION,
            "request_id": self.request_id,
            "experiment_id": self.experiment_id,
            "title": self.title,
            "question": self.question,
            "method": self.method,
            "inputs": list(self.inputs),
            "parameters": dict(self.parameters),
            "seed": self.seed,
            "budget": dict(self.budget),
            "environment": dict(self.environment),
            "command": list(self.command),
            "expected_outputs": dict(self.expected_outputs),
            "metadata": dict(self.metadata),
        }

    @property
    def request_hash(self) -> str:
        return _sha256_text(_canonical_json(self.to_dict()))


@dataclass(slots=True)
class ResearchExecutorResult:
    result_id: str
    request_id: str
    experiment_id: str
    status: str
    started_at: str
    completed_at: str
    deterministic: bool
    output_dir: str
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    observations: list[str] = field(default_factory=list)
    reproducibility_report: dict[str, Any] = field(default_factory=dict)
    stdout: str = ""
    stderr: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ResearchExecutorResult":
        return cls(
            result_id=str(payload["result_id"]),
            request_id=str(payload["request_id"]),
            experiment_id=str(payload["experiment_id"]),
            status=str(payload.get("status") or "unknown"),
            started_at=str(payload.get("started_at") or ""),
            completed_at=str(payload.get("completed_at") or ""),
            deterministic=bool(payload.get("deterministic")),
            output_dir=str(payload.get("output_dir") or ""),
            artifacts=[dict(item) for item in payload.get("artifacts", []) if isinstance(item, dict)],
            metrics=_dict_value(payload.get("metrics")),
            observations=_string_list(payload.get("observations")),
            reproducibility_report=_dict_value(payload.get("reproducibility_report")),
            stdout=str(payload.get("stdout") or ""),
            stderr=str(payload.get("stderr") or ""),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": RESEARCH_EXECUTOR_RESULT_SCHEMA_VERSION,
            "result_id": self.result_id,
            "request_id": self.request_id,
            "experiment_id": self.experiment_id,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "deterministic": self.deterministic,
            "output_dir": self.output_dir,
            "artifacts": [dict(item) for item in self.artifacts],
            "metrics": dict(self.metrics),
            "observations": list(self.observations),
            "reproducibility_report": dict(self.reproducibility_report),
            "stdout": self.stdout,
            "stderr": self.stderr,
            "metadata": dict(self.metadata),
        }


class ResearchExecutor:
    def run_fixture(self, *, fixture: Path, output_dir: Path) -> dict[str, Any]:
        fixture_path = fixture.expanduser().resolve()
        output_dir = output_dir.expanduser().resolve()
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("research experiment fixture must be a JSON object")
        request_payload = payload.get("request") if isinstance(payload.get("request"), dict) else payload
        request = ResearchExecutorRequest.from_dict(request_payload)

        output_dir.mkdir(parents=True, exist_ok=True)
        started_at = utc_now_iso()
        fixture_hash = _sha256_file(fixture_path)
        reproducibility_report = self._reproducibility_report(
            request=request,
            fixture_path=fixture_path,
            fixture_hash=fixture_hash,
        )
        artifact_records = self._materialize_artifacts(
            artifact_specs=payload.get("artifacts", []),
            output_dir=output_dir,
        )
        completed_at = utc_now_iso()
        result = ResearchExecutorResult(
            result_id=str(payload.get("result_id") or f"{request.experiment_id}-result"),
            request_id=request.request_id,
            experiment_id=request.experiment_id,
            status=str(payload.get("status") or "succeeded"),
            started_at=started_at,
            completed_at=completed_at,
            deterministic=True,
            output_dir=str(output_dir),
            artifacts=artifact_records,
            metrics=_dict_value(payload.get("metrics")),
            observations=_string_list(payload.get("observations")),
            reproducibility_report=reproducibility_report,
            stdout=str(payload.get("stdout") or ""),
            stderr=str(payload.get("stderr") or ""),
            metadata={
                "fixture_schema_version": str(payload.get("schema_version") or ""),
                "fixture_path": str(fixture_path),
                "fixture_sha256": fixture_hash,
            },
        )
        experiment_record = self._experiment_record(
            request=request,
            result=result,
            reproducibility_report=reproducibility_report,
        )

        write_json(output_dir / RESEARCH_EXECUTOR_REQUEST_FILE, request.to_dict())
        write_json(output_dir / RESEARCH_EXPERIMENT_RESULT_FILE, result.to_dict())
        write_json(output_dir / RESEARCH_EXPERIMENT_RECORD_FILE, experiment_record.to_dict())
        write_json(output_dir / RESEARCH_REPRODUCIBILITY_REPORT_FILE, reproducibility_report)
        return {
            "schema_version": "amra.research_executor_run.v1",
            "status": result.status,
            "request": request.to_dict(),
            "result": result.to_dict(),
            "experiment_record": experiment_record.to_dict(),
            "reproducibility_report": reproducibility_report,
            "output_dir": str(output_dir),
            "record_files": {
                "request": str(output_dir / RESEARCH_EXECUTOR_REQUEST_FILE),
                "result": str(output_dir / RESEARCH_EXPERIMENT_RESULT_FILE),
                "experiment_record": str(output_dir / RESEARCH_EXPERIMENT_RECORD_FILE),
                "reproducibility_report": str(output_dir / RESEARCH_REPRODUCIBILITY_REPORT_FILE),
            },
        }

    def _reproducibility_report(
        self,
        *,
        request: ResearchExecutorRequest,
        fixture_path: Path,
        fixture_hash: str,
    ) -> dict[str, Any]:
        rerun_key_payload = {
            "request": request.to_dict(),
            "fixture_sha256": fixture_hash,
        }
        return {
            "schema_version": RESEARCH_REPRODUCIBILITY_REPORT_SCHEMA_VERSION,
            "generated_at": utc_now_iso(),
            "request_id": request.request_id,
            "experiment_id": request.experiment_id,
            "deterministic": True,
            "runner": "fixture_replay",
            "fixture": {
                "path": str(fixture_path),
                "sha256": fixture_hash,
            },
            "request_sha256": request.request_hash,
            "rerun_key": _sha256_text(_canonical_json(rerun_key_payload)),
            "rerun_command": [
                "python3",
                "-m",
                "amra",
                "research",
                "run-executor",
                "--fixture",
                str(fixture_path),
                "--out",
                "<output-dir>",
                "--json",
            ],
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
            },
            "inputs": list(request.inputs),
            "parameters": dict(request.parameters),
            "seed": request.seed,
            "budget": dict(request.budget),
        }

    def _materialize_artifacts(self, *, artifact_specs: Any, output_dir: Path) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        specs = artifact_specs if isinstance(artifact_specs, list) else []
        for index, item in enumerate(specs, start=1):
            if not isinstance(item, dict):
                continue
            relative_path = str(item.get("path") or f"artifact_{index}.txt").strip()
            if not relative_path or Path(relative_path).is_absolute() or ".." in Path(relative_path).parts:
                raise ValueError(f"invalid research artifact path: {relative_path!r}")
            path = output_dir / relative_path
            if "json" in item:
                _write_json_artifact(path, item["json"])
            else:
                _write_text_artifact(path, str(item.get("content") or ""))
            records.append(
                {
                    "path": relative_path,
                    "kind": str(item.get("kind") or "research_experiment_artifact"),
                    "bytes": path.stat().st_size,
                    "sha256": _sha256_file(path),
                    "description": str(item.get("description") or ""),
                }
            )
        return records

    def _experiment_record(
        self,
        *,
        request: ResearchExecutorRequest,
        result: ResearchExecutorResult,
        reproducibility_report: dict[str, Any],
    ) -> ExperimentRecord:
        status = (
            ResearchObjectStatus.EMPIRICALLY_SUPPORTED
            if result.status in {"succeeded", "passed", "reproduced"}
            else ResearchObjectStatus.TESTING
        )
        return ExperimentRecord(
            object_id=request.experiment_id,
            title=request.title,
            status=status,
            question=request.question,
            method=request.method,
            inputs=request.inputs,
            parameters=request.parameters,
            seed=request.seed,
            budget=request.budget,
            environment=request.environment,
            command=" ".join(request.command),
            outputs=[item["path"] for item in result.artifacts],
            result_summary="; ".join(result.observations) or result.status,
            rerun_status="reproduced" if result.deterministic and result.status == "succeeded" else "recorded",
            reproducibility_report=reproducibility_report,
            confidence=ResearchConfidence.MEDIUM,
            metadata={
                "request_id": request.request_id,
                "result_id": result.result_id,
                "result_status": result.status,
                "metrics": dict(result.metrics),
            },
        )


def run_research_executor_fixture(*, fixture: Path, output_dir: Path) -> dict[str, Any]:
    return ResearchExecutor().run_fixture(fixture=fixture, output_dir=output_dir)
