from __future__ import annotations

import inspect
import json
import shlex
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Protocol

from ara_math.artifact_graph import load_artifact_graph, save_artifact_graph
from ara_math.coordinator import (
    comath_paths,
    initialize_comath_project,
    load_project_state,
    render_project_dashboard,
    save_project_state,
)
from ara_math.models import ProblemRecord
from ara_math.workspace import append_jsonl, read_json, read_text, record_event, slugify, write_json, write_text
from ara_math.workstreams import ProjectState, WorkstreamKind, WorkstreamRecord, WorkstreamStatus, utc_now_iso


RUNNER_BLOCKER_PREFIX = "[runner:"
SUCCESS_STATUSES = {
    "completed",
    "ok",
    "passed",
    "ready",
    "verified",
    "linked",
    "copied",
    "existing_cold",
    "not_needed",
}

_PROJECT_WRITE_LOCKS: dict[str, threading.RLock] = {}
_PROJECT_WRITE_LOCKS_GUARD = threading.Lock()


def _project_write_lock(project_dir: Path) -> threading.RLock:
    key = str(Path(project_dir).resolve())
    with _PROJECT_WRITE_LOCKS_GUARD:
        lock = _PROJECT_WRITE_LOCKS.get(key)
        if lock is None:
            lock = threading.RLock()
            _PROJECT_WRITE_LOCKS[key] = lock
        return lock


def _jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "value") and isinstance(value.value, str):
        return value.value
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    try:
        json.dumps(value)
    except TypeError:
        return str(value)
    return value


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped


def _as_path_list(values: Any) -> list[Path]:
    if values is None:
        return []
    if isinstance(values, (str, Path)):
        values = [values]
    return [Path(item).expanduser() for item in values if str(item).strip()]


def _safe_options(options: dict[str, Any]) -> dict[str, Any]:
    unsafe_keys = {"runner", "orchestrator", "harvester", "source_runner", "problem"}
    return {key: _jsonable(value) for key, value in options.items() if key not in unsafe_keys}


def _call_with_supported_kwargs(method: Callable[..., Any], **kwargs: Any) -> Any:
    signature = inspect.signature(method)
    parameters = signature.parameters
    if any(parameter.kind == inspect.Parameter.VAR_KEYWORD for parameter in parameters.values()):
        return method(**kwargs)
    accepted = {key: value for key, value in kwargs.items() if key in parameters}
    return method(**accepted)


def _path_string(path: str | Path, project_dir: Path | None = None) -> str:
    candidate = Path(path).expanduser()
    if not candidate.is_absolute() and project_dir is not None:
        candidate = project_dir / candidate
    return str(candidate)


def _looks_like_path(value: str) -> bool:
    if not value or value.startswith(("http://", "https://")):
        return False
    return "/" in value or "\\" in value or "." in Path(value).name


def _collect_artifact_paths(payload: Any, *, project_dir: Path, extra_paths: list[str] | None = None) -> list[str]:
    paths: list[str] = []
    path_keys = {
        "path",
        "artifact_path",
        "artifact_paths",
        "prompt",
        "output",
        "meta",
        "report",
        "summary",
        "state",
        "report_path",
        "summary_path",
        "statement_path",
        "context_bundle_path",
        "prompt_path",
        "output_path",
        "meta_path",
        "status_path",
        "backend_last_message_path",
        "local_path",
    }

    def visit(value: Any, key: str = "") -> None:
        if isinstance(value, Path):
            paths.append(_path_string(value, project_dir))
            return
        if isinstance(value, str):
            if key.endswith("_path") or key.endswith("_paths") or key in path_keys:
                paths.append(_path_string(value, project_dir))
            return
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                visit(child_value, str(child_key))
            return
        if isinstance(value, list):
            for item in value:
                visit(item, key)

    visit(payload)
    for path in extra_paths or []:
        paths.append(_path_string(path, project_dir))
    existing_or_named = []
    for path in paths:
        if path.startswith(("http://", "https://")):
            continue
        if Path(path).exists() or _looks_like_path(path):
            existing_or_named.append(path)
    return _unique(existing_or_named)


def _collect_blockers(payload: dict[str, Any], *, status: str, stop_reason: str = "") -> list[str]:
    blockers: list[str] = []

    def add(value: Any) -> None:
        if value is None:
            return
        if isinstance(value, str):
            text = value.strip()
            if text:
                blockers.append(text)
            return
        if isinstance(value, list):
            for item in value:
                add(item)
            return
        if isinstance(value, dict):
            message = value.get("message") or value.get("reason") or value.get("title")
            if message:
                add(message)

    add(payload.get("blockers"))
    for key in ("best_audit", "initial_audit", "last_attempt", "best_attempt", "system_guard"):
        nested = payload.get(key)
        if isinstance(nested, dict):
            add(nested.get("blockers"))
    if status and status not in SUCCESS_STATUSES:
        message = str(payload.get("message") or "").strip()
        if message:
            add(message)
    if stop_reason and stop_reason not in {"completed", "verified", "verified_initially"}:
        add(f"Runner stopped with reason `{stop_reason}`.")
    return _unique(blockers)


def _workstream_status_for(status: str, blockers: list[str], *, exception: bool = False) -> WorkstreamStatus:
    if exception:
        return WorkstreamStatus.ESCALATED
    if status in SUCCESS_STATUSES and not blockers:
        return WorkstreamStatus.NEEDS_REVIEW
    return WorkstreamStatus.REVISION


def _read_project_statement(project_dir: Path, state: ProjectState, workstream: WorkstreamRecord, options: dict[str, Any]) -> str:
    if str(options.get("statement", "")).strip():
        return str(options["statement"]).strip()
    statement_file = options.get("statement_file")
    if statement_file:
        text = read_text(Path(statement_file).expanduser())
        if text.strip():
            return text.strip()
    metadata_statement = str(workstream.metadata.get("statement", "")).strip()
    if metadata_statement:
        return metadata_statement
    exact_statement = read_text(project_dir / "idea" / "exact_statement.md").strip()
    if exact_statement and "ARA_MATH_PLACEHOLDER_EXACT_STATEMENT" not in exact_statement:
        return exact_statement
    return state.original_goal.strip() or workstream.goal.strip()


def _context_paths(workstream: WorkstreamRecord, options: dict[str, Any]) -> list[Path]:
    values: list[Any] = []
    values.extend(options.get("context_paths") or [])
    values.extend(options.get("context_files") or [])
    values.extend(workstream.metadata.get("context_paths") or [])
    values.extend(workstream.metadata.get("artifact_paths") or [])
    return _as_path_list(values)


def _run_root(project_dir: Path, workstream_id: str, executor_name: str) -> Path:
    return comath_paths(project_dir).workstream_dir(workstream_id) / "runs" / executor_name


@dataclass(slots=True)
class WorkstreamExecutionContext:
    project_dir: Path
    workstream: WorkstreamRecord
    state: ProjectState
    options: dict[str, Any] = field(default_factory=dict)

    @property
    def paths(self) -> Any:
        return comath_paths(self.project_dir)


@dataclass(slots=True)
class WorkstreamExecutionResult:
    workstream_id: str
    executor: str
    status: str
    workstream_status: WorkstreamStatus | str
    run_dir: str = ""
    artifact_paths: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    payload: dict[str, Any] = field(default_factory=dict)
    started_at: str = field(default_factory=utc_now_iso)
    completed_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.workstream_status = WorkstreamStatus.coerce(self.workstream_status)
        self.artifact_paths = _unique([str(path) for path in self.artifact_paths])
        self.blockers = _unique([str(blocker) for blocker in self.blockers if str(blocker).strip()])
        self.payload = _jsonable(self.payload)
        self.metadata = _jsonable(self.metadata)

    def to_dict(self) -> dict[str, Any]:
        return {
            "workstream_id": self.workstream_id,
            "executor": self.executor,
            "status": self.status,
            "workstream_status": self.workstream_status.value,
            "run_dir": self.run_dir,
            "artifact_paths": list(self.artifact_paths),
            "blockers": list(self.blockers),
            "payload": dict(self.payload),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "metadata": dict(self.metadata),
        }


class WorkstreamExecutor(Protocol):
    executor_name: str

    def execute(self, context: WorkstreamExecutionContext) -> WorkstreamExecutionResult:
        ...


class ProofStrategyWorkstreamExecutor:
    executor_name = "proof_strategy"

    def __init__(self, *, runner: Any | None = None, repo_root: Path | None = None) -> None:
        self.runner = runner
        self.repo_root = repo_root

    def execute(self, context: WorkstreamExecutionContext) -> WorkstreamExecutionResult:
        from ara_math.proof_lab import AIProofLabRunner

        started_at = utc_now_iso()
        options = context.options
        statement = _read_project_statement(context.project_dir, context.state, context.workstream, options)
        output_root = Path(options.get("output_root") or _run_root(context.project_dir, context.workstream.workstream_id, self.executor_name))
        runner = options.get("runner") or self.runner or AIProofLabRunner(repo_root=self.repo_root or context.project_dir)
        payload = _call_with_supported_kwargs(
            runner.run,
            statement=statement,
            context_paths=_context_paths(context.workstream, options),
            backend=str(options.get("backend", context.workstream.metadata.get("backend", "none"))),
            attempts=int(options.get("attempts", context.workstream.metadata.get("attempts", 1))),
            audits=int(options.get("audits", context.workstream.metadata.get("audits", 0))),
            time_budget_sec=int(options.get("time_budget_sec", options.get("time_budget", 300))),
            attempt_timeout_sec=int(options.get("attempt_timeout_sec", options.get("attempt_timeout", 120))),
            audit_timeout_sec=int(options.get("audit_timeout_sec", options.get("audit_timeout", 120))),
            source_first=bool(options.get("source_first", context.workstream.metadata.get("source_first", False))),
            grounding_timeout_sec=int(options.get("grounding_timeout_sec", options.get("grounding_timeout", 120))),
            output_root=output_root,
            run_name=options.get("run_name"),
            enable_search=bool(options.get("enable_search", options.get("search", False))),
        )
        payload = _jsonable(payload)
        status = str(payload.get("status", "completed")).strip().lower() or "completed"
        stop_reason = str(payload.get("stop_reason", "")).strip().lower()
        run_dir = str(payload.get("run_dir") or output_root)
        artifact_paths = _collect_artifact_paths(
            payload,
            project_dir=context.project_dir,
            extra_paths=[
                str(Path(run_dir) / "report.json"),
                str(Path(run_dir) / "state.json"),
                str(Path(run_dir) / "summary.md"),
                str(Path(run_dir) / "statement.md"),
                str(Path(run_dir) / "context_bundle.md"),
            ],
        )
        blockers = _collect_blockers(payload, status=status, stop_reason=stop_reason)
        return WorkstreamExecutionResult(
            workstream_id=context.workstream.workstream_id,
            executor=self.executor_name,
            status=status,
            workstream_status=_workstream_status_for(status, blockers),
            run_dir=run_dir,
            artifact_paths=artifact_paths,
            blockers=blockers,
            payload=payload,
            started_at=started_at,
            metadata={"options": _safe_options(options), "statement_source": "co_math_project"},
        )


class LeanFormalizationWorkstreamExecutor:
    executor_name = "lean_formalization"

    def __init__(self, *, runner: Any | None = None, repo_root: Path | None = None) -> None:
        self.runner = runner
        self.repo_root = repo_root

    def execute(self, context: WorkstreamExecutionContext) -> WorkstreamExecutionResult:
        from ara_math.lean_formalizer import LeanFormalizerRunner

        started_at = utc_now_iso()
        options = context.options
        workspace = Path(options.get("workspace") or context.workstream.metadata.get("workspace") or context.project_dir / "formal")
        statement = _read_project_statement(context.project_dir, context.state, context.workstream, options)
        output_root = Path(options.get("output_root") or _run_root(context.project_dir, context.workstream.workstream_id, self.executor_name))
        build_command = options.get("build_command", context.workstream.metadata.get("build_command"))
        if isinstance(build_command, str):
            build_command = shlex.split(build_command)
        runner = options.get("runner") or self.runner or LeanFormalizerRunner(repo_root=self.repo_root or context.project_dir)
        payload = _call_with_supported_kwargs(
            runner.run,
            workspace=workspace,
            statement=statement,
            context_paths=_context_paths(context.workstream, options),
            target_theorem=options.get("target_theorem", context.workstream.metadata.get("target_theorem")),
            target_file=Path(options["target_file"]) if options.get("target_file") else (
                Path(context.workstream.metadata["target_file"]) if context.workstream.metadata.get("target_file") else None
            ),
            build_command=build_command,
            backend=str(options.get("backend", context.workstream.metadata.get("backend", "none"))),
            attempts=int(options.get("attempts", context.workstream.metadata.get("attempts", 1))),
            time_budget_sec=int(options.get("time_budget_sec", options.get("time_budget", 300))),
            attempt_timeout_sec=int(options.get("attempt_timeout_sec", options.get("attempt_timeout", 120))),
            build_timeout_sec=int(options.get("build_timeout_sec", options.get("build_timeout", 120))),
            output_root=output_root,
            run_name=options.get("run_name"),
            enable_search=bool(options.get("enable_search", options.get("search", False))),
            max_stalled_attempts=options.get("max_stalled_attempts", context.workstream.metadata.get("max_stalled_attempts")),
            rollback_failed_attempts=bool(
                options.get("rollback_failed_attempts", context.workstream.metadata.get("rollback_failed_attempts", False))
            ),
        )
        payload = _jsonable(payload)
        status = str(payload.get("status", "completed")).strip().lower() or "completed"
        stop_reason = str(payload.get("stop_reason", "")).strip().lower()
        run_dir = str(payload.get("run_dir") or output_root)
        artifact_paths = _collect_artifact_paths(
            payload,
            project_dir=context.project_dir,
            extra_paths=[
                str(Path(run_dir) / "report.json"),
                str(Path(run_dir) / "state.json"),
                str(Path(run_dir) / "summary.md"),
                str(Path(run_dir) / "statement.md"),
                str(Path(run_dir) / "context_bundle.md"),
                str(Path(run_dir) / "initial_build.json"),
                str(Path(run_dir) / "initial_audit.json"),
            ],
        )
        blockers = _collect_blockers(payload, status=status, stop_reason=stop_reason)
        return WorkstreamExecutionResult(
            workstream_id=context.workstream.workstream_id,
            executor=self.executor_name,
            status=status,
            workstream_status=_workstream_status_for(status, blockers),
            run_dir=run_dir,
            artifact_paths=artifact_paths,
            blockers=blockers,
            payload=payload,
            started_at=started_at,
            metadata={"options": _safe_options(options), "workspace": str(workspace)},
        )


class ClosureWorkstreamExecutor:
    executor_name = "closure"

    def __init__(self, *, orchestrator: Any | None = None, repo_root: Path | None = None) -> None:
        self.orchestrator = orchestrator
        self.repo_root = repo_root

    def execute(self, context: WorkstreamExecutionContext) -> WorkstreamExecutionResult:
        started_at = utc_now_iso()
        options = context.options
        orchestrator = options.get("orchestrator") or self.orchestrator
        if orchestrator is None:
            from ara_math.orchestrator import MathResearchOrchestrator

            orchestrator = MathResearchOrchestrator(repo_root=self.repo_root or context.project_dir)
        target_file = options.get("target_file", context.workstream.metadata.get("target_file"))
        if target_file:
            target_file = Path(target_file)
        payload = _call_with_supported_kwargs(
            orchestrator.run_closure_prover,
            project_dir=context.project_dir,
            target_theorem=options.get("target_theorem", context.workstream.metadata.get("target_theorem")),
            target_file=target_file,
            backend=str(options.get("backend", context.workstream.metadata.get("backend", "none"))),
            max_attempts=int(options.get("max_attempts", options.get("attempts", context.workstream.metadata.get("attempts", 1)))),
            max_runtime_sec=int(options.get("max_runtime_sec", options.get("time_budget_sec", options.get("time_budget", 300)))),
            attempt_timeout_sec=int(options.get("attempt_timeout_sec", options.get("attempt_timeout", 120))),
            build_timeout_sec=int(options.get("build_timeout_sec", options.get("build_timeout", 120))),
            max_stalled_attempts=int(options.get("max_stalled_attempts", context.workstream.metadata.get("max_stalled_attempts", 1))),
            rollback_failed_attempts=bool(
                options.get("rollback_failed_attempts", context.workstream.metadata.get("rollback_failed_attempts", False))
            ),
        )
        payload = _jsonable(payload)
        status = str(payload.get("status", "completed")).strip().lower() or "completed"
        run_dir = str(context.project_dir / "proof" / "closure_prover")
        extra_paths = [
            str(context.project_dir / "proof" / "closure_prover" / "closure_status.json"),
            str(context.project_dir / "proof" / "closure_prover" / "initial_audit.json"),
            str(context.project_dir / "proof" / "closure_prover" / "closure_attempts.jsonl"),
        ]
        artifact_paths = _collect_artifact_paths(payload, project_dir=context.project_dir, extra_paths=extra_paths)
        blockers = _collect_blockers(payload, status=status)
        return WorkstreamExecutionResult(
            workstream_id=context.workstream.workstream_id,
            executor=self.executor_name,
            status=status,
            workstream_status=_workstream_status_for(status, blockers),
            run_dir=run_dir,
            artifact_paths=artifact_paths,
            blockers=blockers,
            payload=payload,
            started_at=started_at,
            metadata={"options": _safe_options(options)},
        )


class SourceLiteratureWorkstreamExecutor:
    executor_name = "source_literature"

    def __init__(self, *, harvester: Any | None = None, repo_root: Path | None = None) -> None:
        self.harvester = harvester
        self.repo_root = repo_root

    def _problem_from_project(self, context: WorkstreamExecutionContext) -> ProblemRecord:
        manifest = read_json(context.project_dir / "project_manifest.json", default={}) or {}
        problem = manifest.get("problem", {}) if isinstance(manifest.get("problem"), dict) else {}
        if {"problem_id", "title", "statement"} <= set(problem):
            payload = {
                "source": "",
                "domain": "unknown",
                **problem,
            }
            return ProblemRecord.from_dict(payload)
        return ProblemRecord(
            problem_id=context.state.project_id,
            title=context.state.project_name,
            source=str(problem.get("source", "")),
            statement=_read_project_statement(context.project_dir, context.state, context.workstream, context.options),
            domain=str(problem.get("domain", "unknown")),
            references=[str(item) for item in problem.get("references", [])] if isinstance(problem.get("references"), list) else [],
            open_problem=bool(problem.get("open_problem", True)),
        )

    def _local_report(self, context: WorkstreamExecutionContext) -> dict[str, Any]:
        evidence = read_json(context.project_dir / "idea" / "literature_evidence.json", default={}) or {}
        recovered = read_json(context.project_dir / "idea" / "statement_recovery.json", default={}) or {}
        snapshots = read_json(context.project_dir / "idea" / "reference_snapshots.json", default={}) or {}
        return {
            "generated_at": utc_now_iso(),
            "project_name": context.state.project_name,
            "problem_id": context.state.project_id,
            "allow_network": False,
            "status": "completed",
            "source_count": int(snapshots.get("source_count", 0) or 0) if isinstance(snapshots, dict) else 0,
            "snapshot_count": int(snapshots.get("snapshot_count", 0) or 0) if isinstance(snapshots, dict) else 0,
            "skipped_source_count": int(snapshots.get("skipped_source_count", 0) or 0) if isinstance(snapshots, dict) else 0,
            "recovered_statement": recovered if isinstance(recovered, dict) else {},
            "evidence": evidence if isinstance(evidence, dict) else {},
            "snapshots": snapshots.get("snapshots", []) if isinstance(snapshots, dict) else [],
            "skipped_sources": snapshots.get("skipped_sources", []) if isinstance(snapshots, dict) else [],
            "mode": "local_existing_artifacts",
        }

    def _source_blockers(self, payload: dict[str, Any]) -> list[str]:
        blockers = _collect_blockers(payload, status=str(payload.get("status", "completed")).lower())
        evidence = payload.get("evidence") if isinstance(payload.get("evidence"), dict) else {}
        recovered = payload.get("recovered_statement") if isinstance(payload.get("recovered_statement"), dict) else {}
        source_attribution_count = int(evidence.get("source_attribution_count", 0) or 0)
        evidence_counts = evidence.get("counts", {}) if isinstance(evidence.get("counts"), dict) else {}
        evidence_total = sum(int(value or 0) for value in evidence_counts.values())
        recovered_status = str(recovered.get("status", "")).strip()
        if source_attribution_count == 0 and evidence_total == 0 and recovered_status in {"", "not_found"}:
            blockers.append("No source-grounded statement or literature evidence has been recorded.")
        return _unique(blockers)

    def execute(self, context: WorkstreamExecutionContext) -> WorkstreamExecutionResult:
        from ara_math.literature import LiteratureHarvester

        started_at = utc_now_iso()
        options = context.options
        allow_network = bool(options.get("allow_network", context.workstream.metadata.get("allow_network", False)))
        run_dir = Path(options.get("output_root") or _run_root(context.project_dir, context.workstream.workstream_id, self.executor_name))
        run_name = slugify(str(options.get("run_name") or f"source-literature-{utc_now_iso()}"))
        run_dir = run_dir / run_name
        run_dir.mkdir(parents=True, exist_ok=True)
        runner = options.get("runner") or options.get("source_runner") or self.harvester
        if runner is not None and hasattr(runner, "harvest_literature"):
            payload = _call_with_supported_kwargs(
                runner.harvest_literature,
                project_dir=context.project_dir,
                allow_network=allow_network,
            )
        elif runner is not None and hasattr(runner, "harvest"):
            payload = _call_with_supported_kwargs(
                runner.harvest,
                project_dir=context.project_dir,
                problem=options.get("problem") or self._problem_from_project(context),
                allow_network=allow_network,
            )
        elif runner is not None and hasattr(runner, "run"):
            payload = _call_with_supported_kwargs(
                runner.run,
                project_dir=context.project_dir,
                workstream=context.workstream,
                state=context.state,
                allow_network=allow_network,
                output_root=run_dir,
                run_name=options.get("run_name"),
            )
        elif (context.project_dir / "project_manifest.json").exists():
            harvester = LiteratureHarvester(formal_math_root=options.get("formal_math_root"))
            payload = harvester.harvest(
                context.project_dir,
                options.get("problem") or self._problem_from_project(context),
                allow_network=allow_network,
            )
        else:
            payload = self._local_report(context)
        payload = _jsonable(payload)
        payload.setdefault("status", "completed")
        payload["run_dir"] = str(run_dir)
        write_json(run_dir / "report.json", payload)
        write_text(
            run_dir / "summary.md",
            "\n".join(
                [
                    "# Source/Literature Workstream Run",
                    "",
                    f"- Status: `{payload.get('status')}`",
                    f"- Sources inspected: `{payload.get('source_count', 0)}`",
                    f"- Snapshots collected: `{payload.get('snapshot_count', 0)}`",
                    "",
                ]
            ),
        )
        status = str(payload.get("status", "completed")).strip().lower() or "completed"
        extra_paths = [
            str(run_dir / "report.json"),
            str(run_dir / "summary.md"),
            str(context.project_dir / "idea" / "reference_snapshots.json"),
            str(context.project_dir / "idea" / "literature_digest.md"),
            str(context.project_dir / "idea" / "literature_evidence.json"),
            str(context.project_dir / "idea" / "statement_recovery.json"),
            str(context.project_dir / "idea" / "paper_inventory.json"),
            str(context.project_dir / "idea" / "paper_theorem_inventory.json"),
        ]
        artifact_paths = _collect_artifact_paths(payload, project_dir=context.project_dir, extra_paths=extra_paths)
        blockers = self._source_blockers(payload)
        return WorkstreamExecutionResult(
            workstream_id=context.workstream.workstream_id,
            executor=self.executor_name,
            status=status,
            workstream_status=_workstream_status_for(status, blockers),
            run_dir=str(run_dir),
            artifact_paths=artifact_paths,
            blockers=blockers,
            payload=payload,
            started_at=started_at,
            metadata={"options": _safe_options(options), "allow_network": allow_network},
        )


def _callable_executor(name: str, func: Callable[[WorkstreamExecutionContext], Any]) -> WorkstreamExecutor:
    class CallableWorkstreamExecutor:
        executor_name = name

        def execute(self, context: WorkstreamExecutionContext) -> WorkstreamExecutionResult:
            started_at = utc_now_iso()
            payload = _call_with_supported_kwargs(func, context=context, project_dir=context.project_dir, workstream=context.workstream)
            if isinstance(payload, WorkstreamExecutionResult):
                return payload
            payload = _jsonable(payload)
            if not isinstance(payload, dict):
                payload = {"status": "completed", "value": payload}
            status = str(payload.get("status", "completed")).strip().lower() or "completed"
            run_dir = str(payload.get("run_dir") or "")
            artifact_paths = _collect_artifact_paths(payload, project_dir=context.project_dir)
            blockers = _collect_blockers(payload, status=status)
            return WorkstreamExecutionResult(
                workstream_id=context.workstream.workstream_id,
                executor=name,
                status=status,
                workstream_status=_workstream_status_for(status, blockers),
                run_dir=run_dir,
                artifact_paths=artifact_paths,
                blockers=blockers,
                payload=payload,
                started_at=started_at,
            )

    return CallableWorkstreamExecutor()


def get_workstream_executor(
    workstream: WorkstreamRecord,
    *,
    executor_name: str | None = None,
    repo_root: Path | None = None,
) -> WorkstreamExecutor:
    raw_name = executor_name or str(workstream.metadata.get("executor") or workstream.metadata.get("runner") or "")
    normalized = raw_name.strip().lower().replace("-", "_")
    if not normalized:
        if workstream.kind == WorkstreamKind.PROOF:
            normalized = "proof_strategy"
        elif workstream.kind == WorkstreamKind.LEAN:
            normalized = "lean_formalization"
        elif workstream.kind == WorkstreamKind.SOURCE:
            normalized = "source_literature"
        elif workstream.kind == WorkstreamKind.COMPUTE:
            normalized = "closure"
        else:
            normalized = "proof_strategy"
    aliases = {
        "proof": "proof_strategy",
        "strategy": "proof_strategy",
        "proof_lab": "proof_strategy",
        "ai_proof_lab": "proof_strategy",
        "lean": "lean_formalization",
        "formalization": "lean_formalization",
        "lean_formalizer": "lean_formalization",
        "formalizer": "lean_formalization",
        "closure_prover": "closure",
        "formal_closure": "closure",
        "source": "source_literature",
        "literature": "source_literature",
        "source_checks": "source_literature",
        "source_check": "source_literature",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized == "proof_strategy":
        return ProofStrategyWorkstreamExecutor(repo_root=repo_root)
    if normalized == "lean_formalization":
        return LeanFormalizationWorkstreamExecutor(repo_root=repo_root)
    if normalized == "closure":
        return ClosureWorkstreamExecutor(repo_root=repo_root)
    if normalized == "source_literature":
        return SourceLiteratureWorkstreamExecutor(repo_root=repo_root)
    raise ValueError(f"Unsupported CoMath workstream executor: {raw_name or normalized}")


def mark_workstream_running(project_dir: Path, workstream_id: str, *, executor_name: str, options: dict[str, Any]) -> WorkstreamRecord:
    with _project_write_lock(project_dir):
        state = load_project_state(project_dir)
        workstream = state.get_workstream(workstream_id)
        if workstream is None:
            raise KeyError(f"Unknown workstream: {workstream_id}")
        workstream.mark_status(WorkstreamStatus.RUNNING)
        workstream.metadata["active_runner"] = {
            "executor": executor_name,
            "started_at": utc_now_iso(),
            "options": _safe_options(options),
        }
        state.upsert_workstream(workstream)
        save_project_state(project_dir, state)
        write_json(comath_paths(project_dir).workstream_dir(workstream_id) / "status.json", workstream.to_dict())
        return workstream


def _artifact_node_id(workstream_id: str, executor: str, path: str, existing_ids: set[str]) -> str:
    base = f"{workstream_id}:{executor}:{slugify(Path(path).name or 'artifact')}"
    candidate = base
    suffix = 2
    while candidate in existing_ids:
        candidate = f"{base}-{suffix}"
        suffix += 1
    existing_ids.add(candidate)
    return candidate


def persist_workstream_execution_result(project_dir: Path, result: WorkstreamExecutionResult) -> WorkstreamRecord:
    with _project_write_lock(project_dir):
        paths = comath_paths(project_dir)
        state = load_project_state(project_dir)
        workstream = state.get_workstream(result.workstream_id)
        if workstream is None:
            raise KeyError(f"Unknown workstream: {result.workstream_id}")

        graph = load_artifact_graph(paths.artifact_graph)
        existing_node_ids = {node.node_id for node in graph.nodes}
        artifact_ids: list[str] = []
        for artifact_path in result.artifact_paths:
            node_id = _artifact_node_id(result.workstream_id, result.executor, artifact_path, existing_node_ids)
            graph.record_file(
                node_id=node_id,
                path=artifact_path,
                label=Path(artifact_path).name,
                workstream_id=result.workstream_id,
                metadata={"executor": result.executor, "run_dir": result.run_dir},
            )
            artifact_ids.append(node_id)
        if artifact_ids:
            save_artifact_graph(paths.artifact_graph, graph)

        workstream.status = result.workstream_status
        workstream.updated_at = utc_now_iso()
        workstream.run_dirs = _unique([*workstream.run_dirs, result.run_dir] if result.run_dir else list(workstream.run_dirs))
        workstream.artifact_paths = _unique([*workstream.artifact_paths, *result.artifact_paths])
        workstream.artifact_ids = _unique([*workstream.artifact_ids, *artifact_ids])
        blocker_prefix = f"{RUNNER_BLOCKER_PREFIX}{result.executor}] "
        workstream.blockers = [blocker for blocker in workstream.blockers if not blocker.startswith(blocker_prefix)]
        workstream.blockers.extend(f"{blocker_prefix}{blocker}" for blocker in result.blockers)
        run_entry = result.to_dict()
        run_entry["artifact_ids"] = artifact_ids
        runs = list(workstream.metadata.get("runner_runs", []))
        runs.append(run_entry)
        workstream.metadata["runner_runs"] = runs
        workstream.metadata["latest_runner"] = run_entry
        workstream.metadata["latest_run_dir"] = result.run_dir
        workstream.metadata["latest_executor"] = result.executor
        workstream.metadata.pop("active_runner", None)

        state.upsert_workstream(workstream)
        save_project_state(project_dir, state)

        workstream_dir = paths.workstream_dir(result.workstream_id)
        write_json(workstream_dir / "status.json", workstream.to_dict())
        append_jsonl(workstream_dir / "run_history.jsonl", run_entry)
        write_json(
            workstream_dir / "artifacts" / "index.json",
            {
                "generated_at": utc_now_iso(),
                "workstream_id": result.workstream_id,
                "artifact_ids": workstream.artifact_ids,
                "artifact_paths": workstream.artifact_paths,
                "run_dirs": workstream.run_dirs,
            },
        )
        blocker_lines = [f"- {blocker}" for blocker in workstream.blockers] or ["- No blockers recorded."]
        write_text(workstream_dir / "blockers.md", "# Blockers\n\n" + "\n".join(blocker_lines) + "\n")
        append_jsonl(
            paths.messages,
            {
                "ts": utc_now_iso(),
                "type": "workstream_runner_completed",
                "workstream_id": result.workstream_id,
                "executor": result.executor,
                "status": result.status,
                "workstream_status": result.workstream_status.value,
                "run_dir": result.run_dir,
                "artifact_count": len(result.artifact_paths),
                "blocker_count": len(result.blockers),
            },
        )
        record_event(
            project_dir,
            stage="comath",
            event="workstream_runner_completed",
            details={
                "workstream_id": result.workstream_id,
                "executor": result.executor,
                "status": result.status,
                "workstream_status": result.workstream_status.value,
            },
        )
        render_project_dashboard(project_dir)
        return workstream


def execute_workstream(
    project_dir: Path,
    workstream_id: str,
    *,
    executor: WorkstreamExecutor | Callable[..., Any] | None = None,
    executor_name: str | None = None,
    options: dict[str, Any] | None = None,
    repo_root: Path | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    project_dir = Path(project_dir)
    with _project_write_lock(project_dir):
        initialize_comath_project(project_dir)
    merged_options = {**(options or {}), **kwargs}
    with _project_write_lock(project_dir):
        state = load_project_state(project_dir)
        workstream = state.get_workstream(workstream_id)
    if workstream is None:
        raise KeyError(f"Unknown workstream: {workstream_id}")

    if executor is None:
        selected_executor = get_workstream_executor(workstream, executor_name=executor_name, repo_root=repo_root)
    elif callable(executor) and not hasattr(executor, "execute"):
        selected_executor = _callable_executor(executor_name or getattr(executor, "__name__", "callable"), executor)
    else:
        selected_executor = executor
    selected_name = executor_name or getattr(selected_executor, "executor_name", "workstream_runner")
    mark_workstream_running(project_dir, workstream_id, executor_name=selected_name, options=merged_options)

    with _project_write_lock(project_dir):
        state = load_project_state(project_dir)
        running_workstream = state.get_workstream(workstream_id)
    if running_workstream is None:
        raise KeyError(f"Unknown workstream after running mark: {workstream_id}")
    context = WorkstreamExecutionContext(
        project_dir=project_dir,
        workstream=running_workstream,
        state=state,
        options=merged_options,
    )
    try:
        result = selected_executor.execute(context)
    except Exception as exc:
        result = WorkstreamExecutionResult(
            workstream_id=workstream_id,
            executor=selected_name,
            status="failed",
            workstream_status=WorkstreamStatus.ESCALATED,
            run_dir="",
            artifact_paths=[],
            blockers=[f"{type(exc).__name__}: {exc}"],
            payload={"status": "failed", "error_type": type(exc).__name__, "error": str(exc)},
            metadata={"options": _safe_options(merged_options), "exception": True},
        )
    persisted = persist_workstream_execution_result(project_dir, result)
    return {
        "project_dir": str(project_dir),
        "workstream_id": workstream_id,
        "executor": result.executor,
        "result": result.to_dict(),
        "workstream": persisted.to_dict(),
    }


def execute_next_workstreams(
    project_dir: Path,
    *,
    limit: int | None = None,
    executor_options: dict[str, dict[str, Any]] | None = None,
    repo_root: Path | None = None,
) -> list[dict[str, Any]]:
    from ara_math.coordinator import select_next_workstreams

    results: list[dict[str, Any]] = []
    for workstream in select_next_workstreams(project_dir, limit=limit):
        options = (executor_options or {}).get(workstream.workstream_id, {})
        results.append(execute_workstream(project_dir, workstream.workstream_id, options=options, repo_root=repo_root))
    return results
