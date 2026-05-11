from __future__ import annotations

import re
import shlex
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from ara_math.lean import LeanExecutor
from ara_math.runtime import env_float, env_int, env_str, run_guarded_command, wait_for_system_headroom
from ara_math.workspace import read_text, slugify, utc_now_iso, write_json, write_text


class LeanFormalizerRunner:
    """Write-and-verify Lean loop downstream of proof-lab route discovery.

    `AIProofLabRunner` is intentionally read-only and produces mathematical
    routes. This runner is the next stage: it lets a backend edit Lean files in a
    target workspace, runs the verifier after every attempt, and feeds the
    verifier errors into the next attempt. It stops only on strict Lean
    verification, attempt exhaustion, time-budget exhaustion, or an explicitly
    configured stall guard.
    """

    AXIOM_PATTERN = re.compile(r"^\s*axiom\b", re.MULTILINE)
    CONSTANT_PATTERN = re.compile(r"^\s*(constant|opaque)\b", re.MULTILINE)

    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.lean_executor = LeanExecutor()
        self.backend_max_memory_mb = env_int("ARA_LEAN_FORMALIZER_BACKEND_MAX_MEMORY_MB", 8192)
        self.backend_max_cpu_seconds = env_int("ARA_LEAN_FORMALIZER_BACKEND_MAX_CPU_SECONDS", 1800)
        self.backend_max_processes = env_int("ARA_LEAN_FORMALIZER_BACKEND_MAX_PROCESSES", 4096)
        self.backend_niceness = env_int("ARA_LEAN_FORMALIZER_BACKEND_NICENESS", 10)
        self.backend_model = env_str("ARA_LEAN_FORMALIZER_MODEL", env_str("ARA_MATH_BACKEND_MODEL", ""))
        self.backend_reasoning_effort = env_str(
            "ARA_LEAN_FORMALIZER_REASONING_EFFORT",
            env_str("ARA_MATH_BACKEND_REASONING_EFFORT", "high"),
        )
        forbidden_header_patterns = env_str("ARA_LEAN_FORMALIZER_FORBIDDEN_TARGET_HEADER_PATTERNS", "")
        self.forbidden_target_header_patterns = [
            item.strip() for item in forbidden_header_patterns.split(",") if item.strip()
        ]
        self.min_available_memory_mb = env_int("ARA_MATH_MIN_AVAILABLE_MEMORY_MB", 2048)
        self.max_load_per_cpu = env_float("ARA_MATH_MAX_LOAD_PER_CPU", 1.5)
        self.wait_max_seconds = env_int("ARA_MATH_SYSTEM_WAIT_SECONDS", 30)
        self.wait_poll_seconds = env_int("ARA_MATH_SYSTEM_WAIT_POLL_SECONDS", 5)

    def _new_run_dir(self, *, output_root: Path, run_name: str | None) -> Path:
        base = slugify(run_name or f"lean-formalizer-{utc_now_iso()}")
        output_root.mkdir(parents=True, exist_ok=True)
        candidate = output_root / base
        if not candidate.exists():
            return candidate
        suffix = 2
        while True:
            candidate = output_root / f"{base}-{suffix}"
            if not candidate.exists():
                return candidate
            suffix += 1

    def _read_context_bundle(self, context_paths: list[Path], *, max_chars_each: int = 20000) -> str:
        if not context_paths:
            return "No upstream proof-lab or formalization context supplied.\n"
        chunks: list[str] = []
        for path in context_paths:
            resolved = path.expanduser().resolve()
            text = read_text(resolved)
            truncated = len(text) > max_chars_each
            if truncated:
                text = text[:max_chars_each] + "\n\n[truncated]\n"
            chunks.extend(
                [
                    f"## Context File: {resolved}",
                    "",
                    f"- Exists: {resolved.exists()}",
                    f"- Truncated: {truncated}",
                    "",
                    "```text",
                    text.strip() or "<empty>",
                    "```",
                    "",
                ]
            )
        return "\n".join(chunks).rstrip() + "\n"

    def _resolve_target_file(self, workspace: Path, target_file: Path | None) -> Path | None:
        if target_file is None:
            return None
        if target_file.is_absolute():
            return target_file
        return workspace / target_file

    def _workspace_snapshot(self, workspace: Path) -> dict[str, str]:
        snapshot: dict[str, str] = {}
        for path in self.lean_executor.iter_project_lean_files(workspace):
            snapshot[str(path.relative_to(workspace))] = path.read_text(encoding="utf-8", errors="ignore")
        return snapshot

    def _restore_workspace_snapshot(self, workspace: Path, snapshot: dict[str, str]) -> None:
        for relative_path, content in snapshot.items():
            path = workspace / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def _target_declaration(
        self,
        workspace: Path,
        *,
        target_theorem: str | None,
        target_file: Path | None,
    ) -> dict[str, Any]:
        theorem = (target_theorem or "").strip()
        if not theorem:
            return {"found": False, "reason": "target_theorem_unspecified"}
        explicit_file = self._resolve_target_file(workspace, target_file)
        if explicit_file is not None:
            if not explicit_file.exists():
                return {"found": False, "reason": "target_file_missing", "path": str(explicit_file)}
            candidates = [explicit_file]
        else:
            candidates = [path for path in sorted(self.lean_executor.iter_project_lean_files(workspace))]
        pattern = re.compile(rf"^\s*(theorem|lemma)\s+{re.escape(theorem)}(?:\s|:|\(|\{{|\[|$)")
        for path in candidates:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for line_number, line in enumerate(text.splitlines(), start=1):
                match = pattern.match(line)
                if match:
                    return {
                        "found": True,
                        "kind": match.group(1),
                        "name": theorem,
                        "path": str(path),
                        "relative_path": str(path.relative_to(workspace)) if path.is_relative_to(workspace) else str(path),
                        "line": line_number,
                        "declaration_line": line.strip(),
                    }
        return {"found": False, "reason": "target_declaration_not_found", "name": theorem}

    def _target_header_text(self, target: dict[str, Any]) -> str:
        if not target.get("found"):
            return ""
        path = Path(str(target.get("path") or ""))
        line_number = int(target.get("line") or 0)
        if not path.exists() or line_number <= 0:
            return ""
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        start = max(0, line_number - 1)
        header_lines: list[str] = []
        for line in lines[start : start + 40]:
            header_lines.append(line)
            stripped = line.strip()
            if ":= by" in stripped or stripped.endswith(":= by"):
                break
            if " := " in stripped or stripped.endswith(" :="):
                break
        return "\n".join(header_lines)

    def _run_build(self, *, workspace: Path, build_command: list[str], timeout_sec: int) -> dict[str, Any]:
        started = time.monotonic()
        if not build_command:
            return {
                "status": "not_run",
                "returncode": None,
                "elapsed_seconds": 0.0,
                "command": [],
                "stdout_tail": "",
                "stderr_tail": "",
                "diagnostics": ["No build command configured."],
            }
        try:
            completed = run_guarded_command(
                build_command,
                cwd=workspace,
                timeout=timeout_sec,
                memory_mb=self.lean_executor.max_memory_mb,
                cpu_seconds=min(self.lean_executor.max_cpu_seconds, max(timeout_sec + 10, timeout_sec)),
                max_processes=self.lean_executor.max_processes,
                niceness=self.lean_executor.niceness,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = str(exc.stdout or exc.output or "")
            stderr = str(exc.stderr or "")
            return {
                "status": "timeout",
                "returncode": None,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "command": build_command,
                "stdout_tail": stdout[-8000:],
                "stderr_tail": stderr[-8000:],
                "diagnostics": self.lean_executor.extract_diagnostics(stdout, stderr),
            }
        diagnostics = self.lean_executor.extract_diagnostics(completed.stdout, completed.stderr)
        return {
            "status": "passed" if completed.returncode == 0 else "failed",
            "returncode": completed.returncode,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "command": build_command,
            "stdout_tail": completed.stdout[-8000:],
            "stderr_tail": completed.stderr[-8000:],
            "diagnostics": diagnostics,
        }

    def _count_pattern(self, workspace: Path, pattern: re.Pattern[str], *, strip_comments: bool = True) -> int:
        total = 0
        for path in self.lean_executor.iter_project_lean_files(workspace):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if strip_comments:
                text = self.lean_executor.strip_lean_comments(text)
            total += len(pattern.findall(text))
        return total

    def _audit(
        self,
        *,
        workspace: Path,
        build_report: dict[str, Any],
        target_theorem: str | None,
        target_file: Path | None,
    ) -> dict[str, Any]:
        target = self._target_declaration(workspace, target_theorem=target_theorem, target_file=target_file)
        sorry_count = self.lean_executor.count_sorries(workspace)
        axiom_count = self._count_pattern(workspace, self.AXIOM_PATTERN)
        constant_count = self._count_pattern(workspace, self.CONSTANT_PATTERN)
        admit_count = self._count_pattern(workspace, LeanExecutor.ADMIT_PATTERN)
        placeholder_count = self._count_pattern(workspace, LeanExecutor.PLACEHOLDER_PATTERN)
        diagnostics = [str(item) for item in build_report.get("diagnostics", [])]
        build_status = str(build_report.get("status", "not_run"))

        blockers: list[str] = []
        if build_status != "passed":
            blockers.append(f"Lean build status is `{build_status}`, not `passed`.")
        if target_theorem and not target.get("found"):
            blockers.append(f"Target theorem `{target_theorem}` was not found in the Lean workspace.")
        if not target_theorem:
            blockers.append("No target theorem was supplied; final theorem verification cannot be certified.")
        if sorry_count:
            blockers.append(f"Lean workspace still contains {sorry_count} `sorry` placeholder(s).")
        if axiom_count:
            blockers.append(f"Lean workspace still contains {axiom_count} `axiom` declaration(s).")
        if constant_count:
            blockers.append(f"Lean workspace still contains {constant_count} `constant`/`opaque` declaration(s).")
        if admit_count:
            blockers.append(f"Lean workspace still contains {admit_count} `admit` placeholder(s).")
        if placeholder_count:
            blockers.append(f"Lean workspace still contains {placeholder_count} ARA placeholder marker(s).")
        target_header = self._target_header_text(target)
        forbidden_header_hits = [
            pattern for pattern in self.forbidden_target_header_patterns if pattern in target_header
        ]
        for pattern in forbidden_header_hits:
            blockers.append(
                "Target theorem header contains forbidden assumption pattern "
                f"`{pattern}`."
            )

        defect_score = (
            (0 if build_status == "passed" else 1_000_000)
            + (0 if target.get("found") else 50_000)
            + sorry_count * 10_000
            + axiom_count * 50_000
            + constant_count * 50_000
            + admit_count * 50_000
            + placeholder_count * 10_000
            + len(forbidden_header_hits) * 50_000
            + len(diagnostics)
        )
        return {
            "generated_at": utc_now_iso(),
            "workspace": str(workspace),
            "target_theorem": target_theorem or "",
            "target_file": str(target_file or ""),
            "target": target,
            "build_status": build_status,
            "returncode": build_report.get("returncode"),
            "diagnostics": diagnostics,
            "diagnostic_count": len(diagnostics),
            "counts": {
                "sorry": sorry_count,
                "axiom": axiom_count,
                "constant": constant_count,
                "admit": admit_count,
                "placeholder": placeholder_count,
            },
            "target_header": target_header,
            "forbidden_target_header_patterns": self.forbidden_target_header_patterns,
            "forbidden_target_header_hits": forbidden_header_hits,
            "defect_score": defect_score,
            "verified": not blockers,
            "blockers": blockers,
        }

    def _build_prompt(
        self,
        *,
        workspace: Path,
        run_dir: Path,
        statement: str,
        context_bundle_path: Path,
        iteration: int,
        attempts: int,
        target_theorem: str | None,
        target_file: Path | None,
        build_command: list[str],
        before_audit: dict[str, Any],
        before_build: dict[str, Any],
        previous_backend_message: str,
    ) -> str:
        target_path = self._resolve_target_file(workspace, target_file)
        target_file_text = ""
        if target_path is not None and target_path.exists():
            target_file_text = target_path.read_text(encoding="utf-8", errors="ignore")[-16000:]
        lean_files = [
            str(path.relative_to(workspace))
            for path in sorted(self.lean_executor.iter_project_lean_files(workspace))
            if ".lake" not in path.parts
        ][:80]
        diagnostics = before_audit.get("diagnostics") or before_build.get("diagnostics") or []
        blockers = before_audit.get("blockers") or []
        return "\n".join(
            [
                "You are running ARA Lean Formalizer, the write-and-verify stage downstream of ARA Proof Lab.",
                "",
                f"Iteration: {iteration} of {attempts}",
                f"Lean workspace: {workspace}",
                f"Run artifact directory: {run_dir}",
                "",
                "Final objective:",
                "- Write Lean code that proves the target theorem as stated.",
                "- The target is accepted only when the configured build command passes and the workspace has no `sorry`, `admit`, `axiom`, `constant`, `opaque`, or ARA placeholder markers.",
                "- Do not weaken the theorem, change definitions to make the theorem trivial, or introduce new trusted assumptions.",
                "- Each iteration must evaluate the previous state, choose the next most important Lean blocker, edit code, run the verifier, and report the next blocker.",
                "",
                "Allowed edits:",
                f"- Edit Lean/proof-support files under `{workspace}`.",
                "- Do not edit generated run artifacts except through normal command output.",
                "",
                "Required verifier command:",
                f"- `{' '.join(shlex.quote(part) for part in build_command)}` from `{workspace}`.",
                "",
                "Target theorem:",
                f"- `{target_theorem or '<unspecified>'}`",
                f"- Target file: `{target_file or '<search all Lean files>'}`",
                "",
                "Mathematical/proof-lab upstream context:",
                f"- Read `{context_bundle_path}` before editing.",
                "",
                "Current statement/implementation target:",
                "```text",
                statement.strip() or "<no statement supplied>",
                "```",
                "",
                "Current strict audit:",
                f"- Verified: {before_audit.get('verified')}",
                f"- Build status: {before_audit.get('build_status')}",
                f"- Defect score: {before_audit.get('defect_score')}",
                f"- Counts: {before_audit.get('counts')}",
                f"- Target declaration: {before_audit.get('target')}",
                "",
                "Current blockers:",
                *(f"- {item}" for item in blockers[-20:]),
                "" if blockers else "- none",
                "",
                "Current build diagnostics:",
                *(f"- {item}" for item in diagnostics[-30:]),
                "" if diagnostics else "- none",
                "",
                "Lean files in workspace:",
                *(f"- {item}" for item in lean_files),
                "",
                "Previous iteration backend message:",
                "```text",
                previous_backend_message[-12000:] if previous_backend_message.strip() else "<none>",
                "```",
                "",
                "Target file tail:",
                "```lean",
                target_file_text or "<target file missing or not specified>",
                "```",
                "",
                "Required final response labels:",
                "Iteration status: <verified|progress|blocked|failed>",
                "Files changed: <paths>",
                "Verifier command: <command and pass/fail>",
                "Remaining blocker: <exact Lean error, missing lemma, or none>",
                "Next target: <what the next iteration should attack if not verified>",
            ]
        ).strip() + "\n"

    def _invoke_backend(
        self,
        *,
        backend: str,
        workspace: Path,
        prompt_path: Path,
        output_path: Path,
        timeout_sec: int,
        enable_search: bool,
    ) -> dict[str, Any]:
        prompt = prompt_path.read_text(encoding="utf-8")
        if backend == "none":
            output_path.write_text(
                "\n".join(
                    [
                        "Iteration status: blocked",
                        "Files changed: none",
                        "Verifier command: not run by backend=none",
                        "Remaining blocker: backend disabled",
                        "Next target: rerun with backend=codex",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            return {"backend": backend, "status": "skipped", "returncode": 0, "elapsed_seconds": 0.0, "command": []}

        backend_bin = shutil.which(backend)
        if not backend_bin:
            output_path.write_text(f"Backend `{backend}` is not available.\n", encoding="utf-8")
            return {"backend": backend, "status": "unavailable", "returncode": None, "elapsed_seconds": 0.0, "command": []}
        if backend != "codex":
            output_path.write_text(f"Backend `{backend}` is not implemented.\n", encoding="utf-8")
            return {"backend": backend, "status": "unsupported", "returncode": None, "elapsed_seconds": 0.0, "command": []}

        command = [backend_bin, "-s", "workspace-write", "-a", "never"]
        if enable_search:
            command.append("--search")
        if self.backend_model:
            command.extend(["-m", self.backend_model])
        if self.backend_reasoning_effort:
            command.extend(["-c", f'model_reasoning_effort="{self.backend_reasoning_effort}"'])
        resolved_workspace = workspace.resolve()
        resolved_output_path = output_path.resolve()
        command.extend(["exec", "-C", str(resolved_workspace), "--output-last-message", str(resolved_output_path), prompt])

        started = time.monotonic()
        try:
            completed = run_guarded_command(
                command,
                cwd=resolved_workspace,
                timeout=timeout_sec,
                memory_mb=self.backend_max_memory_mb,
                cpu_seconds=min(self.backend_max_cpu_seconds, max(timeout_sec + 10, timeout_sec)),
                max_processes=self.backend_max_processes,
                niceness=self.backend_niceness,
            )
        except subprocess.TimeoutExpired as exc:
            if not output_path.exists():
                output_path.write_text(
                    (str(exc.stdout or exc.output or "")) + "\n" + (str(exc.stderr or "")),
                    encoding="utf-8",
                )
            return {
                "backend": backend,
                "status": "timeout",
                "returncode": None,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "command": [*command[:-1], "<prompt omitted; see prompt artifact>"],
            }

        if not output_path.exists():
            output_path.write_text(
                "\n".join(
                    [
                        f"backend={backend}",
                        f"returncode={completed.returncode}",
                        "",
                        "STDOUT:",
                        completed.stdout,
                        "",
                        "STDERR:",
                        completed.stderr,
                    ]
                ).strip()
                + "\n",
                encoding="utf-8",
            )
        return {
            "backend": backend,
            "status": "completed" if completed.returncode == 0 else "failed",
            "returncode": completed.returncode,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "command": [*command[:-1], "<prompt omitted; see prompt artifact>"],
            "stdout_tail": completed.stdout[-4000:],
            "stderr_tail": completed.stderr[-4000:],
            "resource_policy": {
                "memory_mb": self.backend_max_memory_mb,
                "cpu_seconds": min(self.backend_max_cpu_seconds, max(timeout_sec + 10, timeout_sec)),
                "max_processes": self.backend_max_processes,
                "niceness": self.backend_niceness,
                "model": self.backend_model,
                "reasoning_effort": self.backend_reasoning_effort,
            },
        }

    def _write_summary(self, *, path: Path, payload: dict[str, Any]) -> None:
        best = payload.get("best_audit") or {}
        lines = [
            "# ARA Lean Formalizer Report",
            "",
            f"- Status: {payload.get('status')}",
            f"- Stop reason: {payload.get('stop_reason')}",
            f"- Workspace: `{payload.get('workspace')}`",
            f"- Target theorem: `{payload.get('target_theorem')}`",
            f"- Attempts completed: {payload.get('attempts_completed')}",
            f"- Elapsed seconds: {payload.get('elapsed_seconds')}",
            "",
            "## Best Audit",
            "",
            f"- Verified: {best.get('verified')}",
            f"- Build status: {best.get('build_status')}",
            f"- Defect score: {best.get('defect_score')}",
            f"- Counts: {best.get('counts')}",
            "",
            "## Blockers",
            "",
        ]
        blockers = best.get("blockers") or []
        if blockers:
            lines.extend(f"- {item}" for item in blockers)
        else:
            lines.append("- none")
        lines.extend(["", "## Next Action", "", str(payload.get("next_action") or ""), ""])
        write_text(path, "\n".join(lines))

    def run(
        self,
        *,
        workspace: Path,
        statement: str,
        context_paths: list[Path] | None = None,
        target_theorem: str | None = None,
        target_file: Path | None = None,
        build_command: list[str] | None = None,
        backend: str = "codex",
        attempts: int = 8,
        time_budget_sec: int = 3600,
        attempt_timeout_sec: int = 900,
        build_timeout_sec: int = 300,
        output_root: Path | None = None,
        run_name: str | None = None,
        enable_search: bool = False,
        max_stalled_attempts: int | None = None,
        rollback_failed_attempts: bool = False,
    ) -> dict[str, Any]:
        workspace = workspace.expanduser().resolve()
        if not workspace.exists():
            raise FileNotFoundError(f"Lean workspace does not exist: {workspace}")
        build_command = build_command or ["lake", "build"]
        output_root = output_root or (self.repo_root / "artifacts" / "lean_formalizer")
        run_dir = self._new_run_dir(output_root=output_root, run_name=run_name)
        attempts_dir = run_dir / "attempts"
        attempts_dir.mkdir(parents=True, exist_ok=True)

        started = time.monotonic()
        deadline = started + max(1, time_budget_sec)
        context_bundle = self._read_context_bundle(context_paths or [])
        statement_path = run_dir / "statement.md"
        context_bundle_path = run_dir / "context_bundle.md"
        write_text(statement_path, statement.strip() + "\n")
        write_text(context_bundle_path, context_bundle)

        initial_build = self._run_build(workspace=workspace, build_command=build_command, timeout_sec=build_timeout_sec)
        current_audit = self._audit(
            workspace=workspace,
            build_report=initial_build,
            target_theorem=target_theorem,
            target_file=target_file,
        )
        initial_audit = current_audit
        current_build = initial_build
        best_audit = current_audit
        write_json(run_dir / "initial_build.json", initial_build)
        write_json(run_dir / "initial_audit.json", current_audit)

        attempt_entries: list[dict[str, Any]] = []
        previous_message = ""
        stalled = 0
        stop_reason = "attempts_exhausted"

        if current_audit["verified"]:
            stop_reason = "verified_initially"
        else:
            for offset in range(max(0, attempts)):
                remaining = int(deadline - time.monotonic())
                if remaining <= 0:
                    stop_reason = "time_budget_exhausted"
                    break
                headroom = wait_for_system_headroom(
                    min_available_memory_mb=self.min_available_memory_mb,
                    max_load_per_cpu=self.max_load_per_cpu,
                    max_wait_seconds=self.wait_max_seconds,
                    poll_seconds=self.wait_poll_seconds,
                )
                if headroom["status"] != "ready":
                    stop_reason = "system_guard_blocked"
                    break
                iteration = offset + 1
                attempt_dir = attempts_dir / f"attempt_{iteration:03d}"
                attempt_dir.mkdir(parents=True, exist_ok=True)
                write_json(attempt_dir / "before_audit.json", current_audit)
                snapshot = self._workspace_snapshot(workspace) if rollback_failed_attempts else {}
                prompt_path = attempt_dir / "prompt.txt"
                output_path = attempt_dir / "backend_last_message.txt"
                write_text(
                    prompt_path,
                    self._build_prompt(
                        workspace=workspace,
                        run_dir=run_dir,
                        statement=statement,
                        context_bundle_path=context_bundle_path,
                        iteration=iteration,
                        attempts=max(0, attempts),
                        target_theorem=target_theorem,
                        target_file=target_file,
                        build_command=build_command,
                        before_audit=current_audit,
                        before_build=current_build,
                        previous_backend_message=previous_message,
                    ),
                )
                backend_report = self._invoke_backend(
                    backend=backend,
                    workspace=workspace,
                    prompt_path=prompt_path,
                    output_path=output_path,
                    timeout_sec=min(max(30, attempt_timeout_sec), max(1, remaining)),
                    enable_search=enable_search,
                )
                previous_message = read_text(output_path)
                after_build = self._run_build(
                    workspace=workspace,
                    build_command=build_command,
                    timeout_sec=min(max(10, build_timeout_sec), max(1, int(deadline - time.monotonic()))),
                )
                after_audit = self._audit(
                    workspace=workspace,
                    build_report=after_build,
                    target_theorem=target_theorem,
                    target_file=target_file,
                )
                progress_delta = int(current_audit["defect_score"]) - int(after_audit["defect_score"])
                rollback_applied = False
                if rollback_failed_attempts and progress_delta <= 0 and not after_audit["verified"] and snapshot:
                    self._restore_workspace_snapshot(workspace, snapshot)
                    rollback_applied = True
                    after_build = self._run_build(
                        workspace=workspace,
                        build_command=build_command,
                        timeout_sec=min(max(10, build_timeout_sec), max(1, int(deadline - time.monotonic()))),
                    )
                    after_audit = self._audit(
                        workspace=workspace,
                        build_report=after_build,
                        target_theorem=target_theorem,
                        target_file=target_file,
                    )
                    progress_delta = int(current_audit["defect_score"]) - int(after_audit["defect_score"])

                if after_audit["defect_score"] < best_audit["defect_score"]:
                    best_audit = after_audit
                if progress_delta <= 0:
                    stalled += 1
                else:
                    stalled = 0
                attempt_payload = {
                    "generated_at": utc_now_iso(),
                    "iteration": iteration,
                    "backend": backend_report.get("backend"),
                    "backend_status": backend_report.get("status"),
                    "backend_returncode": backend_report.get("returncode"),
                    "backend_elapsed_seconds": backend_report.get("elapsed_seconds"),
                    "before_defect_score": current_audit["defect_score"],
                    "after_defect_score": after_audit["defect_score"],
                    "progress_delta": progress_delta,
                    "stalled_attempts": stalled,
                    "rollback_applied": rollback_applied,
                    "verified": after_audit["verified"],
                    "build_status": after_audit["build_status"],
                    "blockers": after_audit["blockers"],
                    "counts": after_audit["counts"],
                    "prompt_path": str(prompt_path),
                    "backend_last_message_path": str(output_path),
                    "system_headroom": headroom,
                }
                write_json(attempt_dir / "backend_report.json", backend_report)
                write_json(attempt_dir / "after_build.json", after_build)
                write_json(attempt_dir / "after_audit.json", after_audit)
                write_json(attempt_dir / "attempt_report.json", attempt_payload)
                attempt_entries.append(attempt_payload)

                current_audit = after_audit
                current_build = after_build
                if after_audit["verified"]:
                    stop_reason = "verified"
                    break
                if max_stalled_attempts is not None and max_stalled_attempts > 0 and stalled >= max_stalled_attempts:
                    stop_reason = "stalled"
                    break

        status = "verified" if best_audit.get("verified") else ("partial" if attempt_entries else "blocked")
        if stop_reason == "verified_initially":
            status = "verified"
        next_action = "Target theorem is Lean-verified." if status == "verified" else "Continue Lean implementation from the best audit blockers."
        payload = {
            "generated_at": utc_now_iso(),
            "status": status,
            "stop_reason": stop_reason,
            "backend": backend,
            "workspace": str(workspace),
            "run_dir": str(run_dir),
            "statement_path": str(statement_path),
            "context_bundle_path": str(context_bundle_path),
            "target_theorem": target_theorem or "",
            "target_file": str(target_file or ""),
            "build_command": build_command,
            "attempts_requested": attempts,
            "attempts_completed": len(attempt_entries),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "initial_audit": initial_audit,
            "best_audit": best_audit,
            "attempts": attempt_entries,
            "summary_path": str(run_dir / "summary.md"),
            "next_action": next_action,
        }
        write_json(run_dir / "report.json", payload)
        self._write_summary(path=run_dir / "summary.md", payload=payload)
        write_json(run_dir / "state.json", payload)
        return payload


def collect_proof_lab_context_paths(run_dir: Path) -> list[Path]:
    """Collect high-signal proof-lab artifacts for the Lean formalizer."""

    run_dir = run_dir.expanduser().resolve()
    candidates = [
        run_dir / "summary.md",
        run_dir / "manual_summary.md",
        run_dir / "grounding" / "source_grounding_output.md",
    ]
    for subdir in ("audits", "attempts"):
        directory = run_dir / subdir
        if not directory.exists():
            continue
        candidates.extend(sorted(directory.glob("*_output.md"), reverse=True)[:4])
    return [path for path in candidates if path.exists()]
