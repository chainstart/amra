from __future__ import annotations

import re
import shlex
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from amra.agents.source_policy import apply_codex_source_policy, mark_policy_violation, source_policy_prompt
from amra.amra_library import AmraLibraryManager
from amra.portfolio_scheduler import PortfolioAttackScheduler, calculate_progress_velocity
from amra.lean.executor import LeanExecutor
from amra.lean.contract import compare_lean_declaration_headers, extract_lean_declaration_header
from amra.infra.runtime import env_float, env_int, env_str, run_guarded_command, wait_for_system_headroom
from amra.core.workspace import read_text, slugify, utc_now_iso, write_json, write_text
from amra.math_tools import ensure_math_tools


__all__ = ["LeanFormalizerRunner", "collect_proof_lab_context_paths"]


def _lean_module_component(value: str, fallback: str = "CuratedProof") -> str:
    words = re.findall(r"[A-Za-z0-9]+", value)
    component = "".join(word[:1].upper() + word[1:] for word in words) or fallback
    if component[0].isdigit():
        component = f"Proof{component}"
    return component


def _inferred_library_module(target_name: str, source_file: Path) -> str:
    stem = source_file.stem if source_file.name else target_name
    return "AmraLibrary.Curated." + _lean_module_component(target_name or stem)


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
    RESPONSE_LABELS = (
        "Iteration status",
        "Files changed",
        "Verifier command",
        "Remaining blocker",
        "Next target",
    )

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

    def _isolated_workspace(
        self,
        *,
        workspace: Path,
        problem_id: str,
        run_id: str,
        project_dir: Path | None,
    ) -> dict[str, Any]:
        scheduler = PortfolioAttackScheduler(repo_root=self.repo_root)
        if project_dir is not None:
            project = project_dir.expanduser().resolve()
        elif problem_id.strip() and workspace.parent.name != slugify(problem_id):
            project = self.repo_root / "projects" / slugify(problem_id)
        else:
            project = workspace.parent
        reservation = scheduler.reserve_formal_workspace(
            project_dir=project,
            problem_id=problem_id or project.name,
            run_id=run_id,
            canonical_workspace=workspace,
        )
        return {
            "scheduler": scheduler,
            "reservation": reservation,
            "workspace": reservation.isolated_workspace,
            "canonical_workspace": workspace,
        }

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

    def _response_label_section(self, text: str, label: str, *, max_chars: int = 2000) -> str:
        """Extract a labeled section from the backend's required final response."""

        wanted = label.strip().lower()
        known_labels = {item.lower() for item in self.RESPONSE_LABELS}
        lines = text.splitlines()
        for index, line in enumerate(lines):
            match = re.match(r"^\s*([A-Za-z ]+):\s*(.*)$", line)
            if not match or match.group(1).strip().lower() != wanted:
                continue
            section = [match.group(2).strip()]
            for next_line in lines[index + 1 :]:
                next_match = re.match(r"^\s*([A-Za-z ]+):\s*(.*)$", next_line)
                if next_match and next_match.group(1).strip().lower() in known_labels:
                    break
                section.append(next_line.rstrip())
            extracted = "\n".join(section).strip()
            if len(extracted) > max_chars:
                extracted = extracted[:max_chars].rstrip() + "\n[truncated]"
            return extracted
        return ""

    def _dedupe_texts(self, values: list[str]) -> list[str]:
        seen: set[str] = set()
        deduped: list[str] = []
        for value in values:
            cleaned = re.sub(r"\s+", " ", value).strip()
            if not cleaned or cleaned in seen:
                continue
            seen.add(cleaned)
            deduped.append(value.strip())
        return deduped

    def _needs_global_reassessment(
        self,
        *,
        status: str,
        attempt_entries: list[dict[str, Any]],
        best_audit: dict[str, Any],
    ) -> bool:
        if status == "verified" or not attempt_entries:
            return False
        no_defect_progress = all(int(entry.get("progress_delta") or 0) <= 0 for entry in attempt_entries)
        target_missing = any(
            "Target theorem" in str(blocker) and "not found" in str(blocker)
            for blocker in list(best_audit.get("blockers") or [])
        )
        repeated_backend_guidance = any(
            str(entry.get("suggested_next_target") or "").strip() for entry in attempt_entries
        )
        return no_defect_progress and (target_missing or repeated_backend_guidance)

    def _audit_failure_mode(self, blockers: list[str], target_statement_match: dict[str, Any]) -> str:
        if target_statement_match.get("required") and target_statement_match.get("matched") is False:
            return "model_mismatch"
        text = "\n".join(blockers).lower()
        if "target theorem" in text and "not found" in text:
            return "blocked_formalization_gap"
        if any(marker in text for marker in ("sorry", "admit", "placeholder", "build status")):
            return "blocked_formalization_gap"
        if any(marker in text for marker in ("axiom", "constant", "opaque", "forbidden assumption")):
            return "untrusted_formalization"
        return "" if not blockers else "blocked_formalization_gap"

    def _audit(
        self,
        *,
        workspace: Path,
        build_report: dict[str, Any],
        target_theorem: str | None,
        target_file: Path | None,
        expected_target_header: str | None = None,
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
        target_statement_match: dict[str, Any] = {"required": bool(expected_target_header), "matched": None}
        if expected_target_header:
            if target_header:
                target_statement_match = {
                    "required": True,
                    **compare_lean_declaration_headers(
                        actual_header=target_header,
                        expected_header=expected_target_header,
                        target_theorem=target_theorem,
                    ),
                }
                if not target_statement_match.get("matched"):
                    blockers.append("Target theorem header does not match the expected source Lean declaration.")
            else:
                target_statement_match = {
                    "required": True,
                    "matched": False,
                    "expected_normalized": "",
                    "actual_normalized": "",
                }

        defect_score = (
            (0 if build_status == "passed" else 1_000_000)
            + (0 if target.get("found") else 50_000)
            + sorry_count * 10_000
            + axiom_count * 50_000
            + constant_count * 50_000
            + admit_count * 50_000
            + placeholder_count * 10_000
            + len(forbidden_header_hits) * 50_000
            + (0 if not expected_target_header or target_statement_match.get("matched") else 100_000)
            + len(diagnostics)
        )
        failure_mode = self._audit_failure_mode(blockers, target_statement_match)
        proof_loop_state = (
            "lean_verified_declaration"
            if not blockers
            else "model_mismatch"
            if failure_mode == "model_mismatch"
            else "blocked_formalization_gap"
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
            "expected_target_header": expected_target_header or "",
            "target_statement_match": target_statement_match,
            "forbidden_target_header_patterns": self.forbidden_target_header_patterns,
            "forbidden_target_header_hits": forbidden_header_hits,
            "defect_score": defect_score,
            "verified": not blockers,
            "failure_mode": failure_mode,
            "proof_loop_state": proof_loop_state,
            "faithful_modeling_status": (
                "faithfully_modeled"
                if not blockers
                else "model_mismatch"
                if failure_mode == "model_mismatch"
                else "blocked_formalization_gap"
            ),
            "blockers": blockers,
        }

    def _build_prompt(
        self,
        *,
        workspace: Path,
        run_dir: Path,
        statement: str,
        context_bundle_path: Path,
        math_tools_report_path: Path,
        iteration: int,
        attempts: int,
        target_theorem: str | None,
        target_file: Path | None,
        build_command: list[str],
        before_audit: dict[str, Any],
        before_build: dict[str, Any],
        previous_backend_message: str,
        expected_target_header: str | None = None,
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
                "- Expected source declaration: "
                + ("must match exactly up to whitespace" if expected_target_header else "<not supplied>"),
                "```lean",
                expected_target_header.strip() if expected_target_header else "<none>",
                "```",
                "",
                "Mathematical/proof-lab upstream context:",
                f"- Read `{context_bundle_path}` before editing.",
                "",
                "AMRA math tools report:",
                f"- Read `{math_tools_report_path}` before broad proof repair.",
                "- Use Python/Z3/CAS/Lean probes early when a quick check can falsify a lemma shape, verify a finite obstruction, or identify the right algebraic normal form.",
                "- Record nontrivial tool checks in the run directory; final acceptance still requires the host Lean audit.",
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
        prompt = source_policy_prompt(enable_search=enable_search) + "\n\n" + prompt
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
        apply_codex_source_policy(command, enable_search=enable_search)
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
            stdout = str(exc.stdout or exc.output or "")
            stderr = str(exc.stderr or "")
            return mark_policy_violation(
                report={
                    "backend": backend,
                    "status": "timeout",
                    "returncode": None,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "command": [*command[:-1], "<prompt omitted; see prompt artifact>"],
                },
                output_path=output_path,
                stdout=stdout,
                stderr=stderr,
                enable_search=enable_search,
            )

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
        return mark_policy_violation(
            report={
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
            },
            output_path=output_path,
            stdout=completed.stdout,
            stderr=completed.stderr,
            enable_search=enable_search,
        )

    def _write_summary(self, *, path: Path, payload: dict[str, Any]) -> None:
        best = payload.get("best_audit") or {}
        suggested_next_targets = list(payload.get("suggested_next_targets") or [])
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
            f"- Source declaration match: {(best.get('target_statement_match') or {}).get('matched')}",
            f"- Failure mode: {best.get('failure_mode') or '<none>'}",
            f"- Proof loop state: {best.get('proof_loop_state') or '<none>'}",
            "",
            "## Blockers",
            "",
        ]
        blockers = best.get("blockers") or []
        if blockers:
            lines.extend(f"- {item}" for item in blockers)
        else:
            lines.append("- none")
        lines.extend(["", "## Global Reassessment", ""])
        lines.append(f"- Needed: {payload.get('needs_global_reassessment')}")
        lines.append(f"- Reason: {payload.get('global_reassessment_reason') or '<none>'}")
        lines.extend(["", "## Suggested Next Targets", ""])
        if suggested_next_targets:
            lines.extend(f"- {item}" for item in suggested_next_targets)
        else:
            lines.append("- none")
        velocity = payload.get("progress_velocity") or {}
        lines.extend(
            [
                "",
                "## Progress Velocity",
                "",
                f"- Positive delta per hour: {velocity.get('progress_delta_per_hour', 0.0)}",
                f"- Attempts per hour: {velocity.get('attempts_per_hour', 0.0)}",
            ]
        )
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
        enable_search: bool = True,
        max_stalled_attempts: int | None = None,
        rollback_failed_attempts: bool = False,
        expected_target_header: str | None = None,
        project_dir: Path | None = None,
        problem_id: str = "",
        workspace_run_id: str | None = None,
        use_isolated_workspace: bool = False,
        merge_to_canonical: bool = False,
        review_status: str = "",
        library_module: str = "",
        promote_to_library: bool = False,
        math_tools_profile: str = "full",
        install_missing_math_tools: bool | None = None,
        run_math_tool_smoke: bool | None = None,
    ) -> dict[str, Any]:
        workspace = workspace.expanduser().resolve()
        if not workspace.exists():
            raise FileNotFoundError(f"Lean workspace does not exist: {workspace}")
        canonical_workspace = workspace
        effective_run_name = run_name or f"lean-formalizer-{utc_now_iso()}"
        workspace_reservation = None
        scheduler: PortfolioAttackScheduler | None = None
        if use_isolated_workspace:
            isolation = self._isolated_workspace(
                workspace=canonical_workspace,
                problem_id=problem_id or canonical_workspace.parent.name,
                run_id=workspace_run_id or effective_run_name,
                project_dir=project_dir,
            )
            workspace = isolation["workspace"]
            workspace_reservation = isolation["reservation"]
            scheduler = isolation["scheduler"]
        source_contract = extract_lean_declaration_header(statement, target_theorem)
        if source_contract is None:
            source_contract = extract_lean_declaration_header(statement)
        if source_contract and not expected_target_header:
            expected_target_header = str(source_contract.get("header") or "").strip() or None
        if source_contract and not target_theorem:
            target_theorem = str(source_contract.get("name") or "").strip() or None
        build_command = build_command or ["lake", "build"]
        output_root = output_root or (self.repo_root / "artifacts" / "lean_formalizer")
        run_dir = self._new_run_dir(output_root=output_root, run_name=effective_run_name)
        attempts_dir = run_dir / "attempts"
        attempts_dir.mkdir(parents=True, exist_ok=True)

        started = time.monotonic()
        deadline = started + max(1, time_budget_sec)
        context_bundle = self._read_context_bundle(context_paths or [])
        statement_path = run_dir / "statement.md"
        context_bundle_path = run_dir / "context_bundle.md"
        write_text(statement_path, statement.strip() + "\n")
        write_text(context_bundle_path, context_bundle)
        math_tools_report = ensure_math_tools(
            output_dir=run_dir,
            profile=math_tools_profile,
            install_missing=install_missing_math_tools,
            run_smoke=run_math_tool_smoke,
            workspace=workspace,
        )
        math_tools_report_path = Path(str(math_tools_report.get("summary_path") or run_dir / "math_tools_report.md"))

        initial_build = self._run_build(workspace=workspace, build_command=build_command, timeout_sec=build_timeout_sec)
        current_audit = self._audit(
            workspace=workspace,
            build_report=initial_build,
            target_theorem=target_theorem,
            target_file=target_file,
            expected_target_header=expected_target_header,
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
                        math_tools_report_path=math_tools_report_path,
                        iteration=iteration,
                        attempts=max(0, attempts),
                        target_theorem=target_theorem,
                        target_file=target_file,
                        build_command=build_command,
                        before_audit=current_audit,
                        before_build=current_build,
                        previous_backend_message=previous_message,
                        expected_target_header=expected_target_header,
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
                suggested_next_target = self._response_label_section(previous_message, "Next target")
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
                    expected_target_header=expected_target_header,
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
                        expected_target_header=expected_target_header,
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
                    "suggested_next_target": suggested_next_target,
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
        suggested_next_targets = self._dedupe_texts(
            [
                str(entry.get("suggested_next_target") or "")
                for entry in attempt_entries
                if str(entry.get("suggested_next_target") or "").strip()
            ]
        )
        needs_global_reassessment = self._needs_global_reassessment(
            status=status,
            attempt_entries=attempt_entries,
            best_audit=best_audit,
        )
        global_reassessment_reason = ""
        if needs_global_reassessment:
            global_reassessment_reason = (
                "All completed attempts produced no strict-audit score improvement; "
                "a campaign-level supervisor should reassess the proof decomposition "
                "and choose a smaller theorem-level stage target before continuing."
            )
        next_action = (
            "Target theorem is Lean-verified."
            if status == "verified"
            else (
                "Run a global reassessment to choose or confirm a smaller theorem-level target."
                if needs_global_reassessment
                else "Continue Lean implementation from the best audit blockers."
            )
        )
        payload = {
            "generated_at": utc_now_iso(),
            "status": status,
            "stop_reason": stop_reason,
            "backend": backend,
            "workspace": str(workspace),
            "workspace_isolated": bool(workspace_reservation),
            "canonical_workspace": str(canonical_workspace),
            "isolated_workspace": str(workspace) if workspace_reservation is not None else "",
            "run_dir": str(run_dir),
            "statement_path": str(statement_path),
            "context_bundle_path": str(context_bundle_path),
            "math_tools_report": math_tools_report,
            "math_tools_report_path": str(math_tools_report_path),
            "target_theorem": target_theorem or "",
            "target_file": str(target_file or ""),
            "expected_target_header": expected_target_header or "",
            "build_command": build_command,
            "attempts_requested": attempts,
            "attempts_completed": len(attempt_entries),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "initial_audit": initial_audit,
            "best_audit": best_audit,
            "attempts": attempt_entries,
            "suggested_next_targets": suggested_next_targets,
            "needs_global_reassessment": needs_global_reassessment,
            "global_reassessment_reason": global_reassessment_reason,
            "summary_path": str(run_dir / "summary.md"),
            "next_action": next_action,
            "progress_velocity": calculate_progress_velocity(
                elapsed_seconds=round(time.monotonic() - started, 3),
                attempts_completed=len(attempt_entries),
                progress_deltas=[entry.get("progress_delta", 0) for entry in attempt_entries],
                verified_target_count=1 if status == "verified" and target_theorem else 0,
                target_count=1 if target_theorem else 0,
            ),
        }
        if workspace_reservation is not None:
            payload["workspace_reservation"] = workspace_reservation.as_payload(repo_root=self.repo_root)
        if workspace_reservation is not None and scheduler is not None and merge_to_canonical:
            payload["formal_workspace_merge"] = scheduler.merge_reviewed_formal_workspace(
                project_dir=workspace_reservation.project_dir,
                run_id=workspace_reservation.run_id,
                status=status,
                review_status=review_status,
                library_module=library_module,
            )
        elif workspace_reservation is not None:
            payload["formal_workspace_merge"] = {"merged": False, "reason": "merge_not_requested"}
        payload["library_promotion"] = self._promote_verified_target_to_library(
            workspace=workspace,
            audit=best_audit,
            target_theorem=target_theorem or "",
            library_module=library_module,
            promote_to_library=promote_to_library,
        )
        write_json(run_dir / "report.json", payload)
        self._write_summary(path=run_dir / "summary.md", payload=payload)
        write_json(run_dir / "state.json", payload)
        return payload

    def _promote_verified_target_to_library(
        self,
        *,
        workspace: Path,
        audit: dict[str, Any],
        target_theorem: str,
        library_module: str,
        promote_to_library: bool,
    ) -> dict[str, Any]:
        if not audit.get("verified"):
            return {"status": "skipped", "reason": "target_not_verified"}
        if not promote_to_library and not library_module.strip():
            return {"status": "skipped", "reason": "library_promotion_not_requested"}
        target = dict(audit.get("target") or {})
        if not target.get("found"):
            return {"status": "skipped", "reason": "target_source_not_found"}
        source_file = Path(str(target.get("path") or ""))
        if not source_file.is_absolute():
            source_file = workspace / source_file
        source_file = source_file.resolve(strict=False)
        module_name = library_module.strip() or _inferred_library_module(target_theorem, source_file)
        try:
            result = AmraLibraryManager(repo_root=self.repo_root).promote_verified_file(
                source_file=source_file,
                module_name=module_name,
                title=f"Verified proof artifact for {target_theorem or source_file.stem}",
                status="verified",
                tags=["auto_promoted", "lean_verified"],
                verification_basis={
                    "basis": "lean_formalizer_best_audit",
                    "target_theorem": target_theorem,
                    "workspace": str(workspace),
                    "audit_generated_at": str(audit.get("generated_at") or ""),
                },
            )
        except Exception as exc:
            return {"status": "failed", "module": module_name, "source_file": str(source_file), "error": str(exc)}
        return {"status": result.get("status", "promoted"), "result": result}


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
