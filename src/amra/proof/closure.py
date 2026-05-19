from __future__ import annotations

import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from amra.lean.executor import LeanExecutor
from amra.infra.runtime import env_float, env_int, env_str, run_guarded_command, wait_for_system_headroom
from amra.core.workspace import append_jsonl, load_project_manifest, read_json, read_text, utc_now_iso, write_json, write_text


class ClosureProverRunner:
    """Strict Lean-first proof closure loop.

    This runner is intentionally narrower than proof-search: it only treats a
    target theorem as closed when project-owned Lean files build and contain no
    unfinished or trust-eroding declarations.
    """

    CONSTANT_PATTERN = re.compile(r"^\s*(constant|opaque)\b", re.MULTILINE)

    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.lean_executor = LeanExecutor()
        self.backend_max_memory_mb = env_int("ARA_MATH_BACKEND_MAX_MEMORY_MB", 6144)
        self.backend_max_cpu_seconds = env_int("ARA_MATH_BACKEND_MAX_CPU_SECONDS", 240)
        self.backend_max_processes = env_int("ARA_MATH_BACKEND_MAX_PROCESSES", 256)
        self.backend_niceness = env_int("ARA_MATH_BACKEND_NICENESS", 10)
        self.backend_model = env_str("ARA_MATH_BACKEND_MODEL", "")
        self.backend_reasoning_effort = env_str("ARA_MATH_BACKEND_REASONING_EFFORT", "medium")
        self.min_available_memory_mb = env_int("ARA_MATH_MIN_AVAILABLE_MEMORY_MB", 2048)
        self.max_load_per_cpu = env_float("ARA_MATH_MAX_LOAD_PER_CPU", 1.5)
        self.wait_max_seconds = env_int("ARA_MATH_SYSTEM_WAIT_SECONDS", 30)
        self.wait_poll_seconds = env_int("ARA_MATH_SYSTEM_WAIT_POLL_SECONDS", 5)

    def _closure_root(self, project_dir: Path) -> Path:
        return project_dir / "proof" / "closure_prover"

    def _attempts_root(self, project_dir: Path) -> Path:
        return self._closure_root(project_dir) / "attempts"

    def _status_path(self, project_dir: Path) -> Path:
        return self._closure_root(project_dir) / "closure_status.json"

    def _wait_for_headroom(self) -> dict[str, Any]:
        return wait_for_system_headroom(
            min_available_memory_mb=self.min_available_memory_mb,
            max_load_per_cpu=self.max_load_per_cpu,
            max_wait_seconds=self.wait_max_seconds,
            poll_seconds=self.wait_poll_seconds,
        )

    def _next_attempt_index(self, project_dir: Path) -> int:
        attempts_root = self._attempts_root(project_dir)
        highest = 0
        for attempt_dir in attempts_root.glob("attempt_*"):
            if not attempt_dir.is_dir():
                continue
            suffix = attempt_dir.name.removeprefix("attempt_")
            if suffix.isdigit():
                highest = max(highest, int(suffix))
        return highest + 1

    def _formal_snapshot(self, project_dir: Path) -> dict[str, str]:
        formal_dir = project_dir / "formal"
        snapshot: dict[str, str] = {}
        if not formal_dir.exists():
            return snapshot
        for path in formal_dir.rglob("*.lean"):
            if ".lake" in path.parts:
                continue
            snapshot[str(path.relative_to(project_dir))] = path.read_text(encoding="utf-8")
        return snapshot

    def _restore_formal_snapshot(self, project_dir: Path, snapshot: dict[str, str]) -> None:
        if not snapshot:
            return
        for relative_path, content in snapshot.items():
            path = project_dir / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def _target_file_path(self, project_dir: Path, target_file: Path | None) -> Path | None:
        if target_file is None:
            return None
        if target_file.is_absolute():
            return target_file
        return project_dir / target_file

    def _target_declaration(
        self,
        project_dir: Path,
        *,
        target_theorem: str | None,
        target_file: Path | None,
    ) -> dict[str, Any]:
        theorem = (target_theorem or "").strip()
        if not theorem:
            return {"found": False, "reason": "target_theorem_unspecified"}

        formal_dir = project_dir / "formal"
        if not formal_dir.exists():
            return {"found": False, "reason": "missing_formal_workspace"}

        explicit_file = self._target_file_path(project_dir, target_file)
        if explicit_file is not None:
            if not explicit_file.exists():
                return {"found": False, "reason": "target_file_missing", "path": str(explicit_file)}
            candidates = [explicit_file]
        else:
            candidates = [path for path in sorted(formal_dir.rglob("*.lean")) if ".lake" not in path.parts]

        pattern = re.compile(rf"^\s*(theorem|lemma)\s+{re.escape(theorem)}(?:\s|:|\(|\{{|\[|$)")
        for path in candidates:
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except OSError:
                continue
            for line_number, line in enumerate(lines, start=1):
                match = pattern.match(line)
                if match:
                    return {
                        "found": True,
                        "kind": match.group(1),
                        "name": theorem,
                        "path": str(path),
                        "relative_path": str(path.relative_to(project_dir)) if path.is_relative_to(project_dir) else str(path),
                        "line": line_number,
                        "declaration_line": line.strip(),
                    }
        return {"found": False, "reason": "target_declaration_not_found", "name": theorem}

    def _count_pattern(self, formal_dir: Path, pattern: re.Pattern[str]) -> int:
        if not formal_dir.exists():
            return 0
        total = 0
        for lean_file in self.lean_executor.iter_project_lean_files(formal_dir):
            text = self.lean_executor.strip_lean_comments(lean_file.read_text(encoding="utf-8", errors="ignore"))
            total += len(pattern.findall(text))
        return total

    def _audit(
        self,
        project_dir: Path,
        *,
        build_report: dict[str, Any],
        target_theorem: str | None,
        target_file: Path | None,
    ) -> dict[str, Any]:
        formal_dir = project_dir / "formal"
        target = self._target_declaration(project_dir, target_theorem=target_theorem, target_file=target_file)
        sorry_count = int(build_report.get("sorry_count", 0) or 0)
        if formal_dir.exists():
            sorry_count = self.lean_executor.count_sorries(formal_dir)
        axiom_count = self.lean_executor.count_pattern(formal_dir, LeanExecutor.AXIOM_PATTERN, strip_comments=True) if formal_dir.exists() else 0
        admit_count = self.lean_executor.count_pattern(formal_dir, LeanExecutor.ADMIT_PATTERN, strip_comments=True) if formal_dir.exists() else 0
        placeholder_count = (
            self.lean_executor.count_pattern(formal_dir, LeanExecutor.PLACEHOLDER_PATTERN, strip_comments=True)
            if formal_dir.exists()
            else 0
        )
        constant_count = self._count_pattern(formal_dir, self.CONSTANT_PATTERN)
        diagnostics = [str(item) for item in build_report.get("diagnostics", [])]

        blockers: list[str] = []
        build_status = str(build_report.get("status", "not_run"))
        if build_status != "passed":
            blockers.append(f"Lean build status is `{build_status}`, not `passed`.")
        if not target_theorem:
            blockers.append("No target theorem was supplied; strict closure cannot certify the intended theorem.")
        elif not target.get("found"):
            blockers.append(f"Target theorem `{target_theorem}` was not found in project-owned Lean files.")
        if sorry_count:
            blockers.append(f"Project-owned Lean files still contain {sorry_count} `sorry` placeholder(s).")
        if axiom_count:
            blockers.append(f"Project-owned Lean files still contain {axiom_count} `axiom` declaration(s).")
        if constant_count:
            blockers.append(f"Project-owned Lean files still contain {constant_count} `constant`/`opaque` declaration(s).")
        if admit_count:
            blockers.append(f"Project-owned Lean files still contain {admit_count} `admit` placeholder(s).")
        if placeholder_count:
            blockers.append(f"Project-owned Lean files still contain {placeholder_count} ARA placeholder marker(s).")

        build_penalty = 0 if build_status == "passed" else 1_000_000
        target_penalty = 0 if target.get("found") else 50_000
        defect_score = (
            build_penalty
            + target_penalty
            + sorry_count * 10_000
            + axiom_count * 50_000
            + constant_count * 50_000
            + admit_count * 50_000
            + placeholder_count * 10_000
            + len(diagnostics)
        )
        return {
            "generated_at": utc_now_iso(),
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
            "defect_score": defect_score,
            "verified": not blockers,
            "blockers": blockers,
            "build_summary": str(build_report.get("summary", "")),
        }

    def _build_prompt(
        self,
        *,
        project_dir: Path,
        attempt_index: int,
        target_theorem: str,
        target_file: Path | None,
        before_audit: dict[str, Any],
        build_report: dict[str, Any],
    ) -> str:
        manifest = load_project_manifest(project_dir)
        recovered_statement = read_text(project_dir / "idea" / "exact_statement.md")
        proof_gap_notes = read_text(project_dir / "proof" / "proof_gap_notes.md")
        current_focus = read_text(project_dir / "proof" / "current_focus.md")
        target_file_text = ""
        target_path = self._target_file_path(project_dir, target_file) if target_file else None
        if target_path and target_path.exists():
            target_file_text = target_path.read_text(encoding="utf-8", errors="ignore")[-12000:]

        lines = [
            f"You are running ARA Math's strict closure prover in {project_dir.resolve()}.",
            f"Closure attempt: {attempt_index}.",
            "",
            "Objective:",
            f"- Make the Lean theorem `{target_theorem}` formally verify.",
            "- A closure is accepted only when Lean builds and project-owned Lean files contain no `sorry`, `axiom`, `constant`, `opaque`, `admit`, or ARA placeholder markers.",
            "- Do not replace the theorem by an easier statement. If the target statement is wrong or under-specified, write a precise blocker instead of faking a proof.",
            "",
            "Edit policy:",
            f"- Edit only files under `{project_dir / 'formal'}` and `{project_dir / 'proof'}`.",
            "- Prefer the smallest Lean edit that removes the current verifier blocker.",
            "- Do not add `axiom`, `constant`, `opaque`, `admit`, `sorry`, or placeholder markers.",
            "- Do not spend the attempt on broad literature discussion. This is a formal closure loop, not route discovery.",
            "",
            "Required verification command:",
            f"- Run `cd {self.repo_root} && python3 run.py --json build-lean --project {project_dir}` after Lean edits.",
            "",
            "Current strict audit:",
            f"- Build status: {before_audit.get('build_status')}",
            f"- Defect score: {before_audit.get('defect_score')}",
            f"- Counts: {before_audit.get('counts')}",
            f"- Target: {before_audit.get('target')}",
            "",
            "Current build diagnostics:",
        ]
        diagnostics = before_audit.get("diagnostics", []) or build_report.get("diagnostics", [])
        if diagnostics:
            for item in diagnostics[-20:]:
                lines.append(f"- {item}")
        else:
            lines.append("- none")
        if target_file:
            lines.extend(["", f"Requested target file: `{target_file}`"])
        if recovered_statement.strip():
            lines.extend(["", "Project exact-statement context:", recovered_statement.strip()[-5000:]])
        if current_focus.strip():
            lines.extend(["", "Current project focus:", current_focus.strip()[-5000:]])
        if proof_gap_notes.strip():
            lines.extend(["", "Recent proof-gap notes excerpt:", proof_gap_notes.strip()[:6000]])
        if target_file_text:
            lines.extend(["", "Target file tail:", "```lean", target_file_text, "```"])
        lines.extend(
            [
                "",
                "Return requirements:",
                "- State whether the attempt closed the target theorem.",
                "- If not closed, name the exact remaining Lean error or mathematical lemma.",
                "- Report the command you ran and whether it passed.",
            ]
        )
        return "\n".join(lines) + "\n"

    def _invoke_backend(
        self,
        *,
        backend: str,
        prompt_path: Path,
        output_path: Path,
        timeout_sec: int,
    ) -> dict[str, Any]:
        prompt = prompt_path.read_text(encoding="utf-8")
        if backend == "none":
            output_path.write_text("No closure backend selected.\n", encoding="utf-8")
            return {"backend": backend, "status": "skipped", "returncode": 0, "elapsed_seconds": 0.0, "command": []}

        backend_bin = shutil.which(backend)
        if not backend_bin:
            output_path.write_text(f"Backend `{backend}` is not available.\n", encoding="utf-8")
            return {"backend": backend, "status": "unavailable", "returncode": None, "elapsed_seconds": 0.0, "command": []}

        if backend != "codex":
            output_path.write_text(f"Backend `{backend}` is not implemented.\n", encoding="utf-8")
            return {"backend": backend, "status": "unsupported", "returncode": None, "elapsed_seconds": 0.0, "command": []}

        resolved_repo_root = self.repo_root.resolve()
        resolved_output_path = output_path.resolve()
        command = [backend_bin, "exec", "-C", str(resolved_repo_root), "--full-auto"]
        if self.backend_model:
            command.extend(["-m", self.backend_model])
        if self.backend_reasoning_effort:
            command.extend(["-c", f'model_reasoning_effort="{self.backend_reasoning_effort}"'])
        command.extend(["--output-last-message", str(resolved_output_path), prompt])

        started = time.monotonic()
        try:
            completed = run_guarded_command(
                command,
                cwd=resolved_repo_root,
                timeout=timeout_sec,
                memory_mb=self.backend_max_memory_mb,
                cpu_seconds=min(self.backend_max_cpu_seconds, max(timeout_sec + 10, timeout_sec)),
                max_processes=self.backend_max_processes,
                niceness=self.backend_niceness,
            )
        except subprocess.TimeoutExpired as exc:
            output_path.write_text((str(exc.stdout or exc.output or "")) + "\n" + (str(exc.stderr or "")), encoding="utf-8")
            return {
                "backend": backend,
                "status": "timeout",
                "returncode": None,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "command": command,
                "resource_policy": self._backend_resource_policy(timeout_sec),
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
            "command": command,
            "stdout_tail": "\n".join(completed.stdout.splitlines()[-20:]),
            "stderr_tail": "\n".join(completed.stderr.splitlines()[-20:]),
            "resource_policy": self._backend_resource_policy(timeout_sec),
        }

    def _backend_resource_policy(self, timeout_sec: int) -> dict[str, Any]:
        return {
            "memory_mb": self.backend_max_memory_mb,
            "cpu_seconds": min(self.backend_max_cpu_seconds, max(timeout_sec + 10, timeout_sec)),
            "max_processes": self.backend_max_processes,
            "niceness": self.backend_niceness,
            "model": self.backend_model,
            "reasoning_effort": self.backend_reasoning_effort,
        }

    def run(
        self,
        *,
        project_dir: Path,
        orchestrator: Any,
        target_theorem: str | None,
        target_file: Path | None = None,
        backend: str = "codex",
        max_attempts: int = 3,
        max_runtime_sec: int = 900,
        attempt_timeout_sec: int = 180,
        build_timeout_sec: int = 90,
        max_stalled_attempts: int = 2,
        rollback_failed_attempts: bool = False,
    ) -> dict[str, Any]:
        project_dir = project_dir.resolve()
        closure_root = self._closure_root(project_dir)
        attempts_root = self._attempts_root(project_dir)
        attempts_root.mkdir(parents=True, exist_ok=True)
        manifest = load_project_manifest(project_dir)
        started = time.monotonic()

        initial_build = orchestrator.build_lean(project_dir, timeout_sec=build_timeout_sec)
        current_audit = self._audit(
            project_dir,
            build_report=initial_build,
            target_theorem=target_theorem,
            target_file=target_file,
        )
        write_json(closure_root / "initial_audit.json", current_audit)

        if current_audit["verified"]:
            final_report = {
                "generated_at": utc_now_iso(),
                "project_name": manifest["project_name"],
                "problem_id": manifest["problem"]["problem_id"],
                "status": "verified",
                "backend": backend,
                "target_theorem": target_theorem or "",
                "target_file": str(target_file or ""),
                "attempts_completed": 0,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "best_audit": current_audit,
                "message": "Target theorem is Lean-verified under the strict closure gate.",
            }
            write_json(self._status_path(project_dir), final_report)
            return final_report

        if not target_theorem:
            final_report = {
                "generated_at": utc_now_iso(),
                "project_name": manifest["project_name"],
                "problem_id": manifest["problem"]["problem_id"],
                "status": "needs_target",
                "backend": backend,
                "target_theorem": "",
                "target_file": str(target_file or ""),
                "attempts_completed": 0,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "best_audit": current_audit,
                "message": "Strict closure requires an explicit target theorem name.",
            }
            write_json(self._status_path(project_dir), final_report)
            return final_report

        current_build = initial_build
        best_audit = current_audit
        stalled_attempts = 0
        next_attempt_index = self._next_attempt_index(project_dir)
        final_report: dict[str, Any] | None = None

        for offset in range(max_attempts):
            elapsed = time.monotonic() - started
            if elapsed >= max_runtime_sec:
                final_report = {
                    "generated_at": utc_now_iso(),
                    "project_name": manifest["project_name"],
                    "problem_id": manifest["problem"]["problem_id"],
                    "status": "timeout",
                    "backend": backend,
                    "target_theorem": target_theorem,
                    "target_file": str(target_file or ""),
                    "attempts_completed": offset,
                    "elapsed_seconds": round(elapsed, 3),
                    "best_audit": best_audit,
                    "message": "Closure runtime budget expired before the next attempt.",
                }
                break

            headroom_report = self._wait_for_headroom()
            if headroom_report["status"] != "ready":
                final_report = {
                    "generated_at": utc_now_iso(),
                    "project_name": manifest["project_name"],
                    "problem_id": manifest["problem"]["problem_id"],
                    "status": "deferred",
                    "backend": backend,
                    "target_theorem": target_theorem,
                    "target_file": str(target_file or ""),
                    "attempts_completed": offset,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "best_audit": best_audit,
                    "system_guard": headroom_report,
                    "message": "Closure prover was deferred because local resource thresholds stayed blocked.",
                }
                break

            attempt_index = next_attempt_index + offset
            attempt_dir = attempts_root / f"attempt_{attempt_index:03d}"
            attempt_dir.mkdir(parents=True, exist_ok=True)
            write_json(attempt_dir / "before_audit.json", current_audit)
            prompt_path = attempt_dir / "prompt.txt"
            output_path = attempt_dir / "backend_last_message.txt"
            write_text(
                prompt_path,
                self._build_prompt(
                    project_dir=project_dir,
                    attempt_index=attempt_index,
                    target_theorem=target_theorem,
                    target_file=target_file,
                    before_audit=current_audit,
                    build_report=current_build,
                ),
            )
            snapshot = self._formal_snapshot(project_dir) if rollback_failed_attempts else {}
            backend_report = self._invoke_backend(
                backend=backend,
                prompt_path=prompt_path,
                output_path=output_path,
                timeout_sec=min(attempt_timeout_sec, max(1, int(max_runtime_sec - elapsed))),
            )
            after_build = orchestrator.build_lean(project_dir, timeout_sec=build_timeout_sec)
            after_audit = self._audit(
                project_dir,
                build_report=after_build,
                target_theorem=target_theorem,
                target_file=target_file,
            )
            progress_delta = int(current_audit["defect_score"]) - int(after_audit["defect_score"])
            accepted = after_audit["verified"] or progress_delta > 0
            rollback_applied = False
            if rollback_failed_attempts and not accepted and snapshot:
                self._restore_formal_snapshot(project_dir, snapshot)
                rollback_applied = True
                restored_build = orchestrator.build_lean(project_dir, timeout_sec=build_timeout_sec)
                after_audit = self._audit(
                    project_dir,
                    build_report=restored_build,
                    target_theorem=target_theorem,
                    target_file=target_file,
                )
                after_build = restored_build

            if after_audit["defect_score"] < best_audit["defect_score"]:
                best_audit = after_audit
            attempt_payload = {
                "generated_at": utc_now_iso(),
                "attempt_index": attempt_index,
                "backend": backend_report["backend"],
                "backend_status": backend_report["status"],
                "backend_returncode": backend_report.get("returncode"),
                "backend_elapsed_seconds": backend_report.get("elapsed_seconds", 0.0),
                "backend_resource_policy": backend_report.get("resource_policy", {}),
                "prompt_path": str(prompt_path),
                "backend_last_message_path": str(output_path),
                "system_guard": headroom_report,
                "before_defect_score": current_audit["defect_score"],
                "after_defect_score": after_audit["defect_score"],
                "progress_delta": progress_delta,
                "accepted": accepted,
                "rollback_applied": rollback_applied,
                "build_status": after_audit["build_status"],
                "verified": after_audit["verified"],
                "blockers": after_audit["blockers"],
                "counts": after_audit["counts"],
            }
            write_json(attempt_dir / "after_audit.json", after_audit)
            write_json(attempt_dir / "attempt_report.json", attempt_payload)
            append_jsonl(closure_root / "closure_attempts.jsonl", attempt_payload)

            current_audit = after_audit
            current_build = after_build
            if after_audit["verified"]:
                final_report = {
                    "generated_at": utc_now_iso(),
                    "project_name": manifest["project_name"],
                    "problem_id": manifest["problem"]["problem_id"],
                    "status": "verified",
                    "backend": backend,
                    "target_theorem": target_theorem,
                    "target_file": str(target_file or ""),
                    "attempts_completed": offset + 1,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "best_audit": after_audit,
                    "best_attempt": attempt_payload,
                    "message": "Target theorem is Lean-verified under the strict closure gate.",
                }
                break

            if progress_delta <= 0:
                stalled_attempts += 1
            else:
                stalled_attempts = 0
            if stalled_attempts >= max_stalled_attempts:
                final_report = {
                    "generated_at": utc_now_iso(),
                    "project_name": manifest["project_name"],
                    "problem_id": manifest["problem"]["problem_id"],
                    "status": "blocked",
                    "backend": backend,
                    "target_theorem": target_theorem,
                    "target_file": str(target_file or ""),
                    "attempts_completed": offset + 1,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "best_audit": best_audit,
                    "last_attempt": attempt_payload,
                    "message": "Closure loop stopped because strict Lean defects did not decrease.",
                }
                break

        if final_report is None:
            final_report = {
                "generated_at": utc_now_iso(),
                "project_name": manifest["project_name"],
                "problem_id": manifest["problem"]["problem_id"],
                "status": "exhausted",
                "backend": backend,
                "target_theorem": target_theorem,
                "target_file": str(target_file or ""),
                "attempts_completed": max_attempts,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "best_audit": best_audit,
                "message": "Closure attempts were exhausted without strict Lean verification.",
            }
        write_json(self._status_path(project_dir), final_report)
        return final_report
