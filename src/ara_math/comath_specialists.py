from __future__ import annotations

import re
import shutil
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Protocol

from ara_math.artifact_graph import load_artifact_graph, save_artifact_graph
from ara_math.comath_capabilities import SPECIALIST_ROLE_DEFINITIONS, install_specialist_role_contracts
from ara_math.coordinator import (
    comath_paths,
    initialize_comath_project,
    load_project_state,
    render_project_dashboard,
    save_project_state,
    select_next_workstreams,
)
from ara_math.runtime import env_int, env_str, run_guarded_command
from ara_math.uncertainty import UncertaintyItem, UncertaintyKind, load_uncertainty_ledger, save_uncertainty_ledger
from ara_math.workspace import append_jsonl, read_json, read_text, slugify, write_json, write_text
from ara_math.workstreams import WorkstreamRecord, WorkstreamStatus, utc_now_iso


SUCCESS_PROVIDER_STATUSES = {"completed", "ok", "passed", "verified", "skipped"}
FAILED_PROVIDER_STATUSES = {"failed", "timeout", "unavailable", "unsupported"}
_PROJECT_SPECIALIST_LOCKS: dict[str, threading.RLock] = {}
_PROJECT_SPECIALIST_LOCKS_GUARD = threading.Lock()


def _project_specialist_lock(project_dir: Path) -> threading.RLock:
    key = str(Path(project_dir).resolve())
    with _PROJECT_SPECIALIST_LOCKS_GUARD:
        lock = _PROJECT_SPECIALIST_LOCKS.get(key)
        if lock is None:
            lock = threading.RLock()
            _PROJECT_SPECIALIST_LOCKS[key] = lock
        return lock


def _role_by_id(role_id: str) -> dict[str, Any]:
    normalized = role_id.strip()
    for role in SPECIALIST_ROLE_DEFINITIONS:
        if role["role_id"] == normalized:
            return dict(role)
    raise KeyError(f"Unknown CoMath specialist role: {role_id}")


def _safe_run_id(role_id: str, run_name: str | None = None) -> str:
    return slugify(run_name or f"{role_id}-{utc_now_iso()}")


def _truncate_text(text: str, max_chars: int) -> tuple[str, bool]:
    if len(text) <= max_chars:
        return text, False
    return text[:max_chars].rstrip() + "\n\n[truncated]\n", True


def _read_context_file(path: Path, *, max_chars: int) -> dict[str, Any]:
    resolved = path.expanduser()
    exists = resolved.exists()
    text = read_text(resolved, default="") if exists and resolved.is_file() else ""
    text, truncated = _truncate_text(text, max_chars)
    return {
        "path": str(resolved),
        "exists": exists,
        "truncated": truncated,
        "content": text,
    }


def _relative_or_absolute(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def parse_specialist_output(text: str) -> dict[str, Any]:
    fields: dict[str, str] = {}
    current_key = ""
    for line in text.splitlines():
        match = re.match(r"^([A-Za-z][A-Za-z0-9 _-]{1,48}):\s*(.*)$", line)
        if match:
            current_key = match.group(1).strip().lower().replace(" ", "_").replace("-", "_")
            fields[current_key] = match.group(2).strip()
            continue
        if current_key:
            fields[current_key] = (fields[current_key] + "\n" + line).strip()
    status = fields.get("status", "completed").strip().lower() or "completed"
    raw_blockers = fields.get("blockers", "").strip()
    blockers: list[str] = []
    if raw_blockers and raw_blockers.lower() not in {"none", "no", "n/a", "empty", "-"}:
        for item in re.split(r"\n+|;\s*|\s+-\s+", raw_blockers):
            item = item.strip(" -")
            if item:
                blockers.append(item)
    return {"status": status, "fields": fields, "blockers": blockers}


@dataclass(frozen=True, slots=True)
class SpecialistPromptBundle:
    project_dir: Path
    role_id: str
    workstream_id: str
    run_id: str
    run_dir: Path
    prompt_path: Path
    output_path: Path
    context_manifest_path: Path
    context_paths: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_dir": str(self.project_dir),
            "role_id": self.role_id,
            "workstream_id": self.workstream_id,
            "run_id": self.run_id,
            "run_dir": str(self.run_dir),
            "prompt_path": str(self.prompt_path),
            "output_path": str(self.output_path),
            "context_manifest_path": str(self.context_manifest_path),
            "context_paths": list(self.context_paths),
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class SpecialistProviderResult:
    provider: str
    status: str
    output_path: str
    command: list[str] = field(default_factory=list)
    returncode: int | None = None
    elapsed_seconds: float = 0.0
    stdout_tail: str = ""
    stderr_tail: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "status": self.status,
            "output_path": self.output_path,
            "command": list(self.command),
            "returncode": self.returncode,
            "elapsed_seconds": self.elapsed_seconds,
            "stdout_tail": self.stdout_tail,
            "stderr_tail": self.stderr_tail,
            "metadata": dict(self.metadata),
        }


class SpecialistProvider(Protocol):
    provider_name: str

    def run(self, bundle: SpecialistPromptBundle) -> SpecialistProviderResult:
        ...


class FakeSpecialistProvider:
    provider_name = "fake"

    def __init__(self, *, status: str = "completed", blocker: str = "") -> None:
        self.status = status
        self.blocker = blocker

    def run(self, bundle: SpecialistPromptBundle) -> SpecialistProviderResult:
        blockers = self.blocker or "none"
        write_text(
            bundle.output_path,
            "\n".join(
                [
                    f"Status: {self.status}",
                    f"Role: {bundle.role_id}",
                    f"Workstream: {bundle.workstream_id}",
                    "Summary: Fake specialist provider produced a deterministic test artifact.",
                    f"Blockers: {blockers}",
                    "Next actions: Route through review gate before promotion.",
                    "",
                ]
            ),
        )
        return SpecialistProviderResult(
            provider=self.provider_name,
            status=self.status,
            output_path=str(bundle.output_path),
            returncode=0 if self.status in SUCCESS_PROVIDER_STATUSES else 1,
            metadata={"mode": "test_fake"},
        )


class CodexCliSpecialistProvider:
    provider_name = "codex_cli"

    def __init__(
        self,
        *,
        model: str = "",
        reasoning_effort: str = "",
        timeout_seconds: int = 900,
        sandbox: str = "read-only",
        allow_search: bool = False,
        memory_mb: int | None = None,
        cpu_seconds: int | None = None,
        max_processes: int | None = None,
        niceness: int | None = None,
        command_runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    ) -> None:
        self.model = model or env_str("ARA_COMATH_SPECIALIST_MODEL", "")
        self.reasoning_effort = reasoning_effort or env_str("ARA_COMATH_SPECIALIST_REASONING_EFFORT", "")
        self.timeout_seconds = timeout_seconds
        self.sandbox = sandbox
        self.allow_search = allow_search
        self.memory_mb = memory_mb if memory_mb is not None else env_int("ARA_COMATH_SPECIALIST_MEMORY_MB", 6144)
        self.cpu_seconds = cpu_seconds if cpu_seconds is not None else env_int("ARA_COMATH_SPECIALIST_CPU_SECONDS", timeout_seconds + 30)
        self.max_processes = max_processes if max_processes is not None else env_int("ARA_COMATH_SPECIALIST_MAX_PROCESSES", 4096)
        self.niceness = niceness if niceness is not None else env_int("ARA_COMATH_SPECIALIST_NICENESS", 10)
        self.command_runner = command_runner

    def _redacted_command(self, command: list[str]) -> list[str]:
        if not command:
            return []
        return [*command[:-1], "<prompt omitted; see prompt artifact>"]

    def run(self, bundle: SpecialistPromptBundle) -> SpecialistProviderResult:
        codex_bin = shutil.which("codex")
        started = time.monotonic()
        if not codex_bin:
            write_text(bundle.output_path, "Codex CLI is not available on PATH.\n")
            return SpecialistProviderResult(
                provider=self.provider_name,
                status="unavailable",
                output_path=str(bundle.output_path),
                elapsed_seconds=round(time.monotonic() - started, 3),
            )
        prompt = read_text(bundle.prompt_path)
        command = [codex_bin, "-s", self.sandbox, "-a", "never"]
        if self.allow_search:
            command.append("--search")
        if self.model:
            command.extend(["-m", self.model])
        if self.reasoning_effort:
            command.extend(["-c", f'model_reasoning_effort="{self.reasoning_effort}"'])
        command.extend(["exec", "-C", str(bundle.run_dir), "--output-last-message", str(bundle.output_path), prompt])
        try:
            runner = self.command_runner or run_guarded_command
            completed = runner(
                command,
                cwd=bundle.run_dir,
                timeout=self.timeout_seconds,
                memory_mb=self.memory_mb,
                cpu_seconds=min(self.cpu_seconds, max(self.timeout_seconds + 10, self.timeout_seconds)),
                max_processes=self.max_processes,
                niceness=self.niceness,
            )
        except subprocess.TimeoutExpired as exc:
            if not bundle.output_path.exists():
                write_text(bundle.output_path, "Timed out before producing a final specialist message.\n")
            return SpecialistProviderResult(
                provider=self.provider_name,
                status="timeout",
                output_path=str(bundle.output_path),
                command=self._redacted_command(command),
                elapsed_seconds=round(time.monotonic() - started, 3),
                stdout_tail=str(exc.stdout or exc.output or "")[-4000:],
                stderr_tail=str(exc.stderr or "")[-4000:],
                metadata={"model": self.model, "reasoning_effort": self.reasoning_effort, "sandbox": self.sandbox},
            )
        if not bundle.output_path.exists():
            write_text(bundle.output_path, completed.stdout or completed.stderr or "Codex produced no final message.\n")
        status = "completed" if completed.returncode == 0 else "failed"
        return SpecialistProviderResult(
            provider=self.provider_name,
            status=status,
            output_path=str(bundle.output_path),
            command=self._redacted_command(command),
            returncode=completed.returncode,
            elapsed_seconds=round(time.monotonic() - started, 3),
            stdout_tail=(completed.stdout or "")[-4000:],
            stderr_tail=(completed.stderr or "")[-4000:],
            metadata={"model": self.model or "codex_config_default", "reasoning_effort": self.reasoning_effort or "codex_config_default", "sandbox": self.sandbox},
        )


def provider_from_backend(
    backend: str,
    *,
    model: str = "",
    reasoning_effort: str = "",
    timeout_seconds: int = 900,
    allow_search: bool = False,
) -> SpecialistProvider:
    normalized = backend.strip().lower().replace("-", "_")
    if normalized in {"fake", "none", "test"}:
        return FakeSpecialistProvider(status="completed")
    if normalized in {"codex", "codex_cli", "chatgpt"}:
        return CodexCliSpecialistProvider(
            model=model,
            reasoning_effort=reasoning_effort,
            timeout_seconds=timeout_seconds,
            allow_search=allow_search,
        )
    raise ValueError(f"Unsupported specialist backend: {backend}")


def _role_for_workstream(workstream: WorkstreamRecord | None, explicit_role: str) -> str:
    if explicit_role:
        return explicit_role
    if workstream is not None:
        role_id = str(workstream.metadata.get("role_id") or workstream.owner).strip()
        if role_id:
            return role_id
    raise ValueError("A role_id is required when the workstream does not declare metadata.role_id or owner.")


def _find_workstream_for_role(state: Any, role_id: str) -> WorkstreamRecord | None:
    for workstream in state.workstreams:
        if str(workstream.metadata.get("role_id") or "").strip() == role_id or workstream.owner == role_id:
            return workstream
    return None


def _build_context_manifest(
    project_dir: Path,
    *,
    workstream: WorkstreamRecord | None,
    extra_context_files: list[Path],
    max_chars_each: int,
) -> dict[str, Any]:
    paths = comath_paths(project_dir)
    base_files = [
        paths.dashboard,
        paths.project_state,
        paths.artifact_graph,
        paths.uncertainty_ledger,
        paths.root / "failed_routes.jsonl",
        paths.root / "theory_memory.json",
        paths.root / "intake_plan.json",
        paths.root / "specialist_roles.json",
    ]
    if workstream is not None:
        base_files.extend(
            [
                paths.workstream_dir(workstream.workstream_id) / "goal.md",
                paths.workstream_dir(workstream.workstream_id) / "report.md",
                paths.workstream_dir(workstream.workstream_id) / "blockers.md",
            ]
        )
        base_files.extend(Path(item) for item in workstream.artifact_paths)
        base_files.extend(Path(item) for item in workstream.metadata.get("context_paths", []))
    base_files.extend(extra_context_files)
    seen: set[str] = set()
    files: list[dict[str, Any]] = []
    for path in base_files:
        key = str(path.expanduser())
        if key in seen:
            continue
        seen.add(key)
        files.append(_read_context_file(path, max_chars=max_chars_each))
    return {"generated_at": utc_now_iso(), "files": files}


def _render_prompt(
    *,
    role: dict[str, Any],
    project_dir: Path,
    workstream: WorkstreamRecord | None,
    task: str,
    context_manifest_path: Path,
) -> str:
    workstream_lines = ["No workstream is attached; operate as a project-level specialist."]
    if workstream is not None:
        workstream_lines = [
            f"- Workstream id: `{workstream.workstream_id}`",
            f"- Kind: `{workstream.kind.value}`",
            f"- Status: `{workstream.status.value}`",
            f"- Goal: {workstream.goal}",
            f"- Existing blockers: {', '.join(workstream.blockers) if workstream.blockers else 'none'}",
        ]
    return "\n".join(
        [
            f"You are the CoMath `{role['role_id']}` specialist.",
            "",
            "This is a Codex CLI specialist run using the local ChatGPT login, not the OpenAI API.",
            "",
            "Hard constraints:",
            "- Do not edit files directly.",
            "- Write the requested analysis in your final response only.",
            "- Do not approve your own output; review gates must decide promotion.",
            "- Keep every claim connected to the original theorem or explicitly mark it as exploratory.",
            "- Convert unresolved assumptions into named blockers.",
            "- If source, computation, or Lean evidence is missing, say so explicitly.",
            "",
            "Role contract:",
            f"- Title: {role['title']}",
            f"- Paper capability: {role['paper_capability']}",
            f"- Input contract: {', '.join(role['input_contract'])}",
            f"- Output contract: {', '.join(role['output_contract'])}",
            f"- Review requirements: {', '.join(role['review_requirements'])}",
            "",
            "Project:",
            f"- Project dir: `{project_dir}`",
            "",
            "Workstream:",
            *workstream_lines,
            "",
            "Context manifest:",
            f"- `{context_manifest_path}`",
            "",
            "Task:",
            task.strip() or "Perform the role contract for the attached workstream and produce a review-ready artifact.",
            "",
            "Output exactly these labeled fields first, then concise supporting details:",
            "Status: <completed|partial|blocked|failed>",
            "Summary: <one paragraph>",
            "Claims: <claims made or inspected>",
            "Evidence: <files, sources, computations, Lean declarations, or missing evidence>",
            "Blockers: <none, or semicolon-separated blockers>",
            "Next actions: <one to five concrete follow-up actions>",
            "",
        ]
    )


def build_specialist_prompt_bundle(
    project_dir: Path,
    *,
    role_id: str,
    workstream_id: str = "",
    task: str = "",
    run_name: str | None = None,
    context_files: list[Path] | None = None,
    max_context_chars_each: int = 20000,
) -> SpecialistPromptBundle:
    project_dir = Path(project_dir)
    with _project_specialist_lock(project_dir):
        initialize_comath_project(project_dir)
        if not (comath_paths(project_dir).root / "specialist_roles.json").exists():
            install_specialist_role_contracts(project_dir)
        state = load_project_state(project_dir)
        workstream = state.get_workstream(workstream_id) if workstream_id else _find_workstream_for_role(state, role_id)
        role = _role_by_id(_role_for_workstream(workstream, role_id))
    run_id = _safe_run_id(role["role_id"], run_name)
    paths = comath_paths(project_dir)
    run_dir = paths.root / "specialists" / role["role_id"] / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    context_manifest = _build_context_manifest(
        project_dir,
        workstream=workstream,
        extra_context_files=context_files or [],
        max_chars_each=max_context_chars_each,
    )
    context_manifest_path = run_dir / "context_manifest.json"
    write_json(context_manifest_path, context_manifest)
    prompt_path = run_dir / "prompt.md"
    output_path = run_dir / "output.md"
    prompt = _render_prompt(
        role=role,
        project_dir=project_dir,
        workstream=workstream,
        task=task,
        context_manifest_path=context_manifest_path,
    )
    write_text(prompt_path, prompt)
    return SpecialistPromptBundle(
        project_dir=project_dir,
        role_id=role["role_id"],
        workstream_id=workstream.workstream_id if workstream is not None else "",
        run_id=run_id,
        run_dir=run_dir,
        prompt_path=prompt_path,
        output_path=output_path,
        context_manifest_path=context_manifest_path,
        context_paths=[str(item["path"]) for item in context_manifest["files"]],
        metadata={"role": role, "task": task},
    )


def _provider_workstream_status(provider_status: str, blockers: list[str]) -> WorkstreamStatus:
    normalized = provider_status.strip().lower()
    if normalized in FAILED_PROVIDER_STATUSES:
        return WorkstreamStatus.ESCALATED
    if normalized in SUCCESS_PROVIDER_STATUSES and not blockers:
        return WorkstreamStatus.NEEDS_REVIEW
    return WorkstreamStatus.REVISION


def persist_specialist_run(
    bundle: SpecialistPromptBundle,
    provider_result: SpecialistProviderResult,
) -> dict[str, Any]:
    project_dir = bundle.project_dir
    paths = comath_paths(project_dir)
    output = read_text(Path(provider_result.output_path), default="")
    parsed = parse_specialist_output(output)
    result_payload = {
        "generated_at": utc_now_iso(),
        "bundle": bundle.to_dict(),
        "provider": provider_result.to_dict(),
        "parsed_output": parsed,
    }
    with _project_specialist_lock(project_dir):
        write_json(bundle.run_dir / "result.json", result_payload)
        write_text(
            bundle.run_dir / "summary.md",
            "\n".join(
                [
                    f"# Specialist Run: {bundle.role_id}",
                    "",
                    f"- Run id: `{bundle.run_id}`",
                    f"- Workstream: `{bundle.workstream_id or '-'}`",
                    f"- Provider: `{provider_result.provider}`",
                    f"- Status: `{provider_result.status}`",
                    f"- Blockers: `{len(parsed['blockers'])}`",
                    "",
                ]
            ),
        )
        graph = load_artifact_graph(paths.artifact_graph)
        artifact_paths = [bundle.prompt_path, bundle.output_path, bundle.context_manifest_path, bundle.run_dir / "result.json"]
        artifact_ids: list[str] = []
        for artifact_path in artifact_paths:
            node_id = f"specialist:{bundle.role_id}:{bundle.run_id}:{slugify(artifact_path.name)}"
            graph.record_file(
                node_id=node_id,
                path=str(artifact_path),
                label=f"{bundle.role_id} {artifact_path.name}",
                workstream_id=bundle.workstream_id,
                metadata={"role_id": bundle.role_id, "run_id": bundle.run_id, "provider": provider_result.provider},
            )
            artifact_ids.append(node_id)
        save_artifact_graph(paths.artifact_graph, graph)

        state = load_project_state(project_dir)
        workstream = state.get_workstream(bundle.workstream_id) if bundle.workstream_id else None
        if workstream is not None:
            workstream.status = _provider_workstream_status(provider_result.status, parsed["blockers"])
            workstream.artifact_paths = sorted(set([*workstream.artifact_paths, *[str(path) for path in artifact_paths]]))
            workstream.artifact_ids = sorted(set([*workstream.artifact_ids, *artifact_ids]))
            run_entry = {
                "role_id": bundle.role_id,
                "run_id": bundle.run_id,
                "run_dir": str(bundle.run_dir),
                "provider": provider_result.provider,
                "provider_status": provider_result.status,
                "workstream_status": workstream.status.value,
                "blockers": parsed["blockers"],
                "artifact_ids": artifact_ids,
                "artifact_paths": [str(path) for path in artifact_paths],
                "generated_at": utc_now_iso(),
            }
            runs = list(workstream.metadata.get("specialist_runs", []))
            runs.append(run_entry)
            workstream.metadata["specialist_runs"] = runs
            workstream.metadata["latest_specialist_run"] = run_entry
            blocker_prefix = f"[specialist:{bundle.role_id}] "
            workstream.blockers = [item for item in workstream.blockers if not item.startswith(blocker_prefix)]
            workstream.blockers.extend(f"{blocker_prefix}{item}" for item in parsed["blockers"])
            state.upsert_workstream(workstream)
            save_project_state(project_dir, state)
            workstream_dir = paths.workstream_dir(workstream.workstream_id)
            write_json(workstream_dir / "status.json", workstream.to_dict())
            append_jsonl(workstream_dir / "messages.jsonl", {"ts": utc_now_iso(), "type": "specialist_run_completed", **run_entry})
        elif provider_result.status not in SUCCESS_PROVIDER_STATUSES:
            ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
            ledger.upsert_item(
                UncertaintyItem(
                    item_id=f"specialist-run:{bundle.role_id}:{bundle.run_id}",
                    kind=UncertaintyKind.STALLED_WORKSTREAM,
                    title=f"Specialist run failed for {bundle.role_id}",
                    description=f"Provider status: {provider_result.status}",
                    owner_workstream_id=bundle.workstream_id,
                    severity="medium",
                )
            )
            save_uncertainty_ledger(paths.uncertainty_ledger, ledger)
        append_jsonl(
            paths.messages,
            {
                "ts": utc_now_iso(),
                "type": "specialist_run_completed",
                "role_id": bundle.role_id,
                "workstream_id": bundle.workstream_id,
                "run_id": bundle.run_id,
                "provider": provider_result.provider,
                "status": provider_result.status,
                "blocker_count": len(parsed["blockers"]),
                "run_dir": str(bundle.run_dir),
            },
        )
        render_project_dashboard(project_dir)
    return result_payload


def run_specialist(
    project_dir: Path,
    *,
    role_id: str,
    workstream_id: str = "",
    task: str = "",
    backend: str = "codex",
    provider: SpecialistProvider | None = None,
    model: str = "",
    reasoning_effort: str = "",
    timeout_seconds: int = 900,
    allow_search: bool = False,
    run_name: str | None = None,
    context_files: list[Path] | None = None,
) -> dict[str, Any]:
    bundle = build_specialist_prompt_bundle(
        project_dir,
        role_id=role_id,
        workstream_id=workstream_id,
        task=task,
        run_name=run_name,
        context_files=context_files,
    )
    selected_provider = provider or provider_from_backend(
        backend,
        model=model,
        reasoning_effort=reasoning_effort,
        timeout_seconds=timeout_seconds,
        allow_search=allow_search,
    )
    provider_result = selected_provider.run(bundle)
    result = persist_specialist_run(bundle, provider_result)
    return {
        "project_dir": str(project_dir),
        "role_id": bundle.role_id,
        "workstream_id": bundle.workstream_id,
        "run_id": bundle.run_id,
        "run_dir": str(bundle.run_dir),
        "prompt_path": str(bundle.prompt_path),
        "output_path": str(bundle.output_path),
        "provider": provider_result.to_dict(),
        "result": result,
    }


def _select_roles_for_loop(project_dir: Path, roles: list[str] | None, limit: int) -> list[tuple[str, str]]:
    state = load_project_state(project_dir)
    if roles:
        selected: list[tuple[str, str]] = []
        for role_id in roles:
            workstream = _find_workstream_for_role(state, role_id)
            selected.append((role_id, workstream.workstream_id if workstream else ""))
        return selected[:limit]
    selected = []
    seen: set[str] = set()
    for workstream in select_next_workstreams(project_dir):
        role_id = str(workstream.metadata.get("role_id") or workstream.owner).strip()
        if not role_id or role_id in seen:
            continue
        try:
            _role_by_id(role_id)
        except KeyError:
            continue
        selected.append((role_id, workstream.workstream_id))
        seen.add(role_id)
        if len(selected) >= limit:
            break
    return selected


def run_specialist_loop(
    project_dir: Path,
    *,
    roles: list[str] | None = None,
    backend: str = "codex",
    provider: SpecialistProvider | None = None,
    model: str = "",
    reasoning_effort: str = "",
    timeout_seconds: int = 900,
    allow_search: bool = False,
    max_specialists: int = 3,
    max_parallel_specialists: int = 1,
    run_name: str | None = None,
    task: str = "",
) -> dict[str, Any]:
    project_dir = Path(project_dir)
    initialize_comath_project(project_dir)
    paths = comath_paths(project_dir)
    loop_id = slugify(run_name or f"specialist-loop-{utc_now_iso()}")
    loop_dir = paths.root / "specialist_loops" / loop_id
    loop_dir.mkdir(parents=True, exist_ok=True)
    selected = _select_roles_for_loop(project_dir, roles, max(1, max_specialists))
    started_at = utc_now_iso()
    results: list[dict[str, Any]] = []
    if selected:
        worker_count = max(1, min(max_parallel_specialists, len(selected)))
        with ThreadPoolExecutor(max_workers=worker_count) as pool:
            futures = {
                pool.submit(
                    run_specialist,
                    project_dir,
                    role_id=role_id,
                    workstream_id=workstream_id,
                    task=task,
                    backend=backend,
                    provider=provider,
                    model=model,
                    reasoning_effort=reasoning_effort,
                    timeout_seconds=timeout_seconds,
                    allow_search=allow_search,
                    run_name=f"{loop_id}-{role_id}",
                ): (role_id, workstream_id)
                for role_id, workstream_id in selected
            }
            for future in as_completed(futures):
                results.append(future.result())
    report = {
        "project_dir": str(project_dir),
        "loop_id": loop_id,
        "started_at": started_at,
        "completed_at": utc_now_iso(),
        "backend": backend,
        "model": model or "codex_config_default",
        "reasoning_effort": reasoning_effort or "codex_config_default",
        "max_specialists": max_specialists,
        "max_parallel_specialists": max_parallel_specialists,
        "selected": [{"role_id": role_id, "workstream_id": workstream_id} for role_id, workstream_id in selected],
        "results": results,
        "executed_count": len(results),
        "stop_reason": "no_ready_specialists" if not selected else "max_specialists_reached",
    }
    write_json(loop_dir / "report.json", report)
    write_text(
        loop_dir / "summary.md",
        "\n".join(
            [
                f"# Specialist Loop: {loop_id}",
                "",
                f"- Backend: `{backend}`",
                f"- Executed specialists: `{len(results)}`",
                f"- Max parallel specialists: `{max_parallel_specialists}`",
                "",
            ]
        ),
    )
    append_jsonl(
        paths.messages,
        {
            "ts": utc_now_iso(),
            "type": "specialist_loop_completed",
            "loop_id": loop_id,
            "executed_count": len(results),
            "report_path": str(loop_dir / "report.json"),
        },
    )
    render_project_dashboard(project_dir)
    return report
