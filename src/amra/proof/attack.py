from __future__ import annotations

import fcntl
import hashlib
import re
import shlex
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from amra.agents.source_policy import apply_codex_source_policy, mark_policy_violation, source_policy_prompt
from amra.infra.runtime import env_int, env_str, run_guarded_command, wait_for_system_headroom
from amra.core.workspace import load_project_manifest, read_json, read_text, utc_now_iso, write_json, write_text


GENERIC_ATTACK_DOCTRINE: tuple[str, ...] = (
    "Represent the proof route as a dependency graph: named facts, source imports, formal obligations, and verifier/certificate nodes.",
    "Each iteration must state the dependency-graph delta: node closed, node sharpened, branch refuted, route changed, or no material progress.",
    "Classify the active blocker as one of: mathematical lemma, source/provenance gap, definition-alignment gap, formalization gap, executable-certificate gap, policy/checkpoint gap, or counterexample/search gap.",
    "A local lemma is useful only if it removes or strictly sharpens a blocker on the main dependency graph.",
    "If the current route is structurally insufficient, stop optimizing it and switch to source acquisition, evaluator construction, counterexample search, or a new route.",
    "Freeze a branch when the available facts imply only a terminal external dependency, the same exact missing node repeats without new evidence, or a structural obstruction shows local refinements cannot close the theorem.",
    "When freezing, output a freeze package: exact missing theorem/certificate/policy, why current facts cannot imply it, and the minimal external evidence needed to reopen the branch.",
    "Treat evidence as a canonical carrier plus verifier: an exact cited theorem, a Lean/kernel check, an executable certificate validator, or a reproducible computation. Grep hits, prose echoes, and token coincidences are not proof.",
)


class MathAttackRunner:
    """Run a math-only attack loop against one project target.

    This is intentionally separate from Lean proof repair. It is for the stage
    where the system must discover or stress-test a real mathematical route
    before turning it into formal obligations.
    """

    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.backend_max_memory_mb = env_int("ARA_MATH_ATTACK_BACKEND_MAX_MEMORY_MB", 6144)
        self.backend_max_cpu_seconds = env_int("ARA_MATH_ATTACK_BACKEND_MAX_CPU_SECONDS", 420)
        # Codex/Node may create worker threads, and RLIMIT_NPROC is counted
        # against the whole Unix user on Linux. A low cap can fail before the
        # backend starts when multiple attacks run in parallel.
        self.backend_max_processes = env_int("ARA_MATH_ATTACK_BACKEND_MAX_PROCESSES", 4096)
        self.backend_niceness = env_int("ARA_MATH_ATTACK_BACKEND_NICENESS", 10)
        self.backend_model = env_str("ARA_MATH_ATTACK_MODEL", env_str("ARA_MATH_BACKEND_MODEL", ""))
        self.backend_reasoning_effort = env_str(
            "ARA_MATH_ATTACK_REASONING_EFFORT",
            env_str("ARA_MATH_BACKEND_REASONING_EFFORT", "high"),
        )
        self.evidence_max_memory_mb = env_int("ARA_MATH_ATTACK_EVIDENCE_MAX_MEMORY_MB", 4096)
        self.evidence_max_cpu_seconds = env_int("ARA_MATH_ATTACK_EVIDENCE_MAX_CPU_SECONDS", 180)
        self.evidence_max_processes = env_int("ARA_MATH_ATTACK_EVIDENCE_MAX_PROCESSES", 512)
        self.evidence_niceness = env_int("ARA_MATH_ATTACK_EVIDENCE_NICENESS", 10)
        self.min_available_memory_mb = env_int("ARA_MATH_MIN_AVAILABLE_MEMORY_MB", 2048)
        self.wait_max_seconds = env_int("ARA_MATH_SYSTEM_WAIT_SECONDS", 30)
        self.wait_poll_seconds = env_int("ARA_MATH_SYSTEM_WAIT_POLL_SECONDS", 5)
        self.default_min_sleep_seconds = env_int("ARA_MATH_ATTACK_MIN_SLEEP_SECONDS", 60)
        self.default_sleep_jitter_seconds = env_int("ARA_MATH_ATTACK_SLEEP_JITTER_SECONDS", 30)
        self.default_launch_spacing_seconds = env_int("ARA_MATH_ATTACK_LAUNCH_SPACING_SECONDS", 0)

    def _attack_root(self, project_dir: Path) -> Path:
        return project_dir / "proof" / "math_attack"

    def _status_path(self, project_dir: Path) -> Path:
        return project_dir / "proof" / "math_attack_status.json"

    def _new_run_dir(self, project_dir: Path, run_name: str | None) -> Path:
        attack_root = self._attack_root(project_dir)
        attack_root.mkdir(parents=True, exist_ok=True)
        base_name = run_name.strip() if run_name and run_name.strip() else f"attack_{utc_now_iso().replace(':', '').replace('+', 'Z')}"
        candidate = attack_root / base_name
        if not candidate.exists():
            return candidate
        suffix = 2
        while True:
            candidate = attack_root / f"{base_name}_{suffix}"
            if not candidate.exists():
                return candidate
            suffix += 1

    def _read_context_file(self, path: Path, *, max_chars: int) -> dict[str, Any]:
        resolved = path.expanduser()
        text = read_text(resolved)
        truncated = len(text) > max_chars
        if truncated:
            text = text[:max_chars] + "\n\n[truncated]\n"
        return {
            "path": str(resolved),
            "exists": resolved.exists(),
            "truncated": truncated,
            "content": text,
        }

    def _tail_recent_outputs(self, run_dir: Path, *, keep: int = 3, chars_each: int = 6000) -> str:
        outputs = sorted((run_dir / "iterations").glob("iter_*_output.md"))
        selected = outputs[-keep:]
        if not selected:
            return "No previous math-attack outputs yet.\n"
        chunks: list[str] = []
        for output_path in selected:
            text = read_text(output_path)
            if len(text) > chars_each:
                text = text[-chars_each:]
            chunks.append(f"### {output_path.name}\n{text.strip()}\n")
        return "\n".join(chunks).strip() + "\n"

    def _run_evidence_command(
        self,
        *,
        command: list[str],
        cwd: Path,
        timeout_sec: int,
    ) -> dict[str, Any]:
        if not command:
            return {
                "status": "skipped",
                "command": [],
                "cwd": str(cwd),
                "elapsed_seconds": 0.0,
                "stdout": "",
                "stderr": "",
            }
        started = time.monotonic()
        try:
            completed = run_guarded_command(
                command,
                cwd=cwd,
                timeout=timeout_sec,
                memory_mb=self.evidence_max_memory_mb,
                cpu_seconds=min(self.evidence_max_cpu_seconds, max(timeout_sec + 5, timeout_sec)),
                max_processes=self.evidence_max_processes,
                niceness=self.evidence_niceness,
            )
        except subprocess.TimeoutExpired as exc:
            return {
                "status": "timeout",
                "command": command,
                "cwd": str(cwd),
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "stdout": str(exc.stdout or exc.output or ""),
                "stderr": str(exc.stderr or ""),
            }
        return {
            "status": "completed" if completed.returncode == 0 else "failed",
            "returncode": completed.returncode,
            "command": command,
            "cwd": str(cwd),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }

    def _format_context_bundle(
        self,
        *,
        project_dir: Path,
        target: str,
        context_files: list[dict[str, Any]],
        evidence_report: dict[str, Any],
    ) -> str:
        manifest = load_project_manifest(project_dir)
        exact_statement = read_text(project_dir / "idea" / "exact_statement.md").strip()
        selected_route = read_text(project_dir / "proof" / "selected_route.md").strip()
        current_focus = read_text(project_dir / "proof" / "current_focus.md").strip()
        proof_gap_notes = read_text(project_dir / "proof" / "proof_gap_notes.md").strip()
        checkpoint_contract = read_json(project_dir / "proof" / "checkpoint_contract.json", default={})
        counterexample_contract = read_json(project_dir / "proof" / "counterexample_search_contract.json", default={})

        lines = [
            "# Math Attack Context Bundle",
            "",
            f"- Project: {manifest.get('project_name', project_dir.name)}",
            f"- Problem ID: {(manifest.get('problem') or {}).get('problem_id', '')}",
            f"- Target: {target}",
            "",
            "## Exact Statement",
            "",
            exact_statement or "<missing>",
            "",
            "## Selected Route",
            "",
            selected_route or "<missing>",
            "",
            "## Current Focus",
            "",
            current_focus or "<missing>",
            "",
            "## Proof Gap Notes",
            "",
            proof_gap_notes or "<missing>",
            "",
            "## Checkpoint Contract",
            "",
            "```json",
            str(checkpoint_contract),
            "```",
            "",
            "## Counterexample/Search Contract",
            "",
            "```json",
            str(counterexample_contract),
            "```",
            "",
            "## Local Evidence Command",
            "",
            f"- Status: {evidence_report.get('status', '')}",
            f"- Command: {shlex.join([str(item) for item in evidence_report.get('command', [])]) if evidence_report.get('command') else '<none>'}",
            f"- CWD: {evidence_report.get('cwd', '')}",
            "",
            "### Evidence STDOUT",
            "",
            "```",
            str(evidence_report.get("stdout", "")).strip() or "<empty>",
            "```",
            "",
            "### Evidence STDERR",
            "",
            "```",
            str(evidence_report.get("stderr", "")).strip() or "<empty>",
            "```",
        ]
        for item in context_files:
            lines.extend(
                [
                    "",
                    f"## Context File: {item['path']}",
                    "",
                    f"- Exists: {item['exists']}",
                    f"- Truncated: {item['truncated']}",
                    "",
                    "```text",
                    item["content"].strip() or "<empty>",
                    "```",
                ]
            )
        return "\n".join(lines).rstrip() + "\n"

    def _build_prompt(
        self,
        *,
        run_dir: Path,
        iteration: int,
        target: str,
        context_bundle: str,
    ) -> str:
        recent_outputs = self._tail_recent_outputs(run_dir)
        write_text(run_dir / "recent_outputs_excerpt.md", recent_outputs)
        write_text(run_dir / "latest_context_bundle.md", context_bundle)
        doctrine_lines = [f"- {item}" for item in GENERIC_ATTACK_DOCTRINE]
        return "\n".join(
            [
                "You are running an iterative pure-mathematics attack loop inside ARA Math.",
                "",
                "Hard constraints:",
                "- Work on the mathematical proof chain, not on repository maintenance.",
                "- Do not edit repository files.",
                "- Do not write Lean code unless the target explicitly requests a formal statement sketch.",
                "- Prefer rigorous deductions over speculation.",
                "- If an idea is heuristic, label it explicitly as heuristic.",
                "- Do not claim the main theorem is solved unless every dependency is stated precisely.",
                "- Materially strengthen the current route; do not merely restate existing notes.",
                "- After every iteration, re-evaluate the global proof route before proposing local refinements.",
                "- Reject local optimizations that do not reduce the main theorem's remaining dependency graph.",
                "- If the route is becoming an external-dependency statement rather than a proof, say so explicitly.",
                "",
                "Generic proof-attack doctrine (problem-independent):",
                *doctrine_lines,
                "",
                f"Current target: {target}",
                f"Current iteration: {iteration}",
                "",
                "Read and use these run artifacts:",
                f"- {run_dir / 'latest_context_bundle.md'}",
                f"- {run_dir / 'recent_outputs_excerpt.md'}",
                "",
                "Task for this iteration:",
                "1. Propose the single strongest next lemma, obstruction, or route correction.",
                "2. State it precisely.",
                "3. Give the best rigorous proof attempt from the available facts.",
                "4. If the proof does not close, isolate the exact missing step.",
                "5. Suggest one short local check or evidence command improvement for the next iteration.",
                "6. Audit whether this iteration materially moves the main theorem, or only optimizes a local subproblem.",
                "7. Decide whether the branch should continue, switch route, or freeze under the generic freeze criteria.",
                "",
                "Output format:",
                "- Title",
                "- Global route audit",
                "- Dependency graph delta",
                "- Blocker classification",
                "- Target lemma or obstruction",
                "- Proof attempt",
                "- Status: rigorous / partial / heuristic",
                "- Missing step",
                "- Main-theorem distance update",
                "- Next local check",
                "- Continue / switch / freeze decision",
                "- Priority for next iteration",
            ]
        ).strip() + "\n"

    def _invoke_backend(
        self,
        *,
        backend: str,
        run_dir: Path,
        prompt: str,
        output_path: Path,
        timeout_sec: int,
        enable_search: bool,
    ) -> dict[str, Any]:
        prompt = source_policy_prompt(enable_search=enable_search) + "\n\n" + prompt
        if backend == "none":
            output_path.write_text("No math-attack backend selected.\n", encoding="utf-8")
            return {
                "backend": backend,
                "status": "skipped",
                "returncode": 0,
                "elapsed_seconds": 0.0,
                "command": [],
            }

        backend_bin = shutil.which(backend)
        if not backend_bin:
            output_path.write_text(f"Backend `{backend}` is not available.\n", encoding="utf-8")
            return {
                "backend": backend,
                "status": "unavailable",
                "returncode": None,
                "elapsed_seconds": 0.0,
                "command": [],
            }

        if backend != "codex":
            output_path.write_text(f"Backend `{backend}` is not implemented for math-attack runs.\n", encoding="utf-8")
            return {
                "backend": backend,
                "status": "unsupported",
                "returncode": None,
                "elapsed_seconds": 0.0,
                "command": [],
            }

        command = [
            backend_bin,
            "-s",
            "read-only",
            "-a",
            "never",
        ]
        apply_codex_source_policy(command, enable_search=enable_search)
        if self.backend_model:
            command.extend(["-m", self.backend_model])
        if self.backend_reasoning_effort:
            command.extend(["-c", f'model_reasoning_effort="{self.backend_reasoning_effort}"'])
        resolved_run_dir = run_dir.resolve()
        resolved_output_path = output_path.resolve()
        command.extend(
            [
                "exec",
                "-C",
                str(resolved_run_dir),
                "--output-last-message",
                str(resolved_output_path),
            ]
        )
        command.append(prompt)

        started = time.monotonic()
        try:
            completed = run_guarded_command(
                command,
                cwd=resolved_run_dir,
                timeout=timeout_sec,
                memory_mb=self.backend_max_memory_mb,
                cpu_seconds=min(self.backend_max_cpu_seconds, max(timeout_sec + 10, timeout_sec)),
                max_processes=self.backend_max_processes,
                niceness=self.backend_niceness,
            )
        except subprocess.TimeoutExpired as exc:
            if not output_path.exists():
                output_path.write_text("Timed out before producing a final backend message.\n", encoding="utf-8")
            stdout = str(exc.stdout or exc.output or "")
            stderr = str(exc.stderr or "")
            return mark_policy_violation(
                report={
                    "backend": backend,
                    "status": "timeout",
                    "returncode": None,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "command": command,
                    "stdout_tail": stdout[-4000:],
                    "stderr_tail": stderr[-4000:],
                    "resource_policy": self._backend_resource_policy(timeout_sec),
                },
                output_path=output_path,
                stdout=stdout,
                stderr=stderr,
                enable_search=enable_search,
            )

        if not output_path.exists():
            output_path.write_text((completed.stdout + "\n\nSTDERR\n" + completed.stderr).strip() + "\n", encoding="utf-8")
        return mark_policy_violation(
            report={
                "backend": backend,
                "status": "completed" if completed.returncode == 0 else "failed",
                "returncode": completed.returncode,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "command": command,
                "stdout_tail": completed.stdout[-4000:],
                "stderr_tail": completed.stderr[-4000:],
                "resource_policy": self._backend_resource_policy(timeout_sec),
            },
            output_path=output_path,
            stdout=completed.stdout,
            stderr=completed.stderr,
            enable_search=enable_search,
        )

    def _backend_resource_policy(self, timeout_sec: int) -> dict[str, Any]:
        return {
            "memory_mb": self.backend_max_memory_mb,
            "cpu_seconds": min(self.backend_max_cpu_seconds, max(timeout_sec + 10, timeout_sec)),
            "max_processes": self.backend_max_processes,
            "niceness": self.backend_niceness,
            "model": self.backend_model,
            "reasoning_effort": self.backend_reasoning_effort,
        }

    def _deterministic_jitter(self, *, run_dir: Path, iteration: int, jitter_seconds: int) -> int:
        if jitter_seconds <= 0:
            return 0
        token = f"{run_dir}:{iteration}".encode("utf-8")
        digest = hashlib.sha256(token).hexdigest()
        return int(digest[:8], 16) % (jitter_seconds + 1)

    def _backend_report_wants_backoff(self, backend_report: dict[str, Any]) -> bool:
        fields = [
            str(backend_report.get("status", "")),
            str(backend_report.get("stdout_tail", "")),
            str(backend_report.get("stderr_tail", "")),
        ]
        text = "\n".join(fields).lower()
        if any(
            marker in text
            for marker in (
                "rate limit",
                "ratelimit",
                "too many requests",
                "usage limit",
                "quota",
                "temporarily unavailable",
            )
        ):
            return True
        # Avoid treating timestamps/paths such as 20260429 as HTTP 429.
        return bool(
            re.search(r"\b(?:http|status|code|error)[^\n]{0,30}\b429\b", text)
            or re.search(r"\b429\b[^\n]{0,30}\b(?:too many requests|rate limit|ratelimit)\b", text)
        )

    def _sleep_plan(
        self,
        *,
        run_dir: Path,
        iteration: int,
        iterations: int,
        deadline: float,
        sleep_mode: str,
        sleep_seconds: int,
        min_sleep_seconds: int | None,
        max_sleep_seconds: int | None,
        sleep_jitter_seconds: int | None,
        backend_report: dict[str, Any],
    ) -> dict[str, Any]:
        normalized_mode = sleep_mode if sleep_mode in {"adaptive", "fixed", "none"} else "adaptive"
        remaining = max(0, int(deadline - time.monotonic()))
        if iteration >= iterations or remaining <= 0:
            return {"mode": normalized_mode, "seconds": 0, "reason": "last_iteration_or_deadline"}
        if normalized_mode == "none":
            return {"mode": normalized_mode, "seconds": 0, "reason": "disabled"}

        configured_sleep = max(0, int(sleep_seconds))
        cap = max_sleep_seconds if max_sleep_seconds is not None else configured_sleep
        cap = max(0, int(cap or 0))
        if cap <= 0:
            return {
                "mode": normalized_mode,
                "seconds": 0,
                "reason": "no_sleep_budget",
                "configured_sleep_seconds": configured_sleep,
                "max_sleep_seconds": cap,
            }

        if normalized_mode == "fixed":
            seconds = min(cap, remaining)
            return {
                "mode": normalized_mode,
                "seconds": seconds,
                "reason": "fixed",
                "configured_sleep_seconds": configured_sleep,
                "max_sleep_seconds": cap,
            }

        minimum = min_sleep_seconds if min_sleep_seconds is not None else self.default_min_sleep_seconds
        minimum = max(0, min(int(minimum), cap))
        jitter_budget = (
            self.default_sleep_jitter_seconds if sleep_jitter_seconds is None else int(sleep_jitter_seconds)
        )
        jitter_budget = max(0, min(jitter_budget, max(0, cap - minimum)))
        elapsed = float(backend_report.get("elapsed_seconds") or 0.0)
        status = str(backend_report.get("status", ""))
        wants_backoff = self._backend_report_wants_backoff(backend_report)
        if status == "timeout" or wants_backoff:
            raw_seconds = cap
            reason = "backend_backoff"
        elif status == "failed":
            raw_seconds = max(minimum, min(cap, int(max(elapsed, minimum * 2))))
            reason = "backend_failed"
        else:
            raw_seconds = max(minimum, min(cap, int(max(elapsed * 0.5, minimum))))
            reason = "adaptive_elapsed"
        jitter = 0 if raw_seconds >= cap else self._deterministic_jitter(
            run_dir=run_dir,
            iteration=iteration,
            jitter_seconds=min(jitter_budget, cap - raw_seconds),
        )
        seconds = min(cap, raw_seconds + jitter, remaining)
        return {
            "mode": normalized_mode,
            "seconds": seconds,
            "reason": reason,
            "configured_sleep_seconds": configured_sleep,
            "min_sleep_seconds": minimum,
            "max_sleep_seconds": cap,
            "jitter_seconds": jitter,
            "backend_elapsed_seconds": elapsed,
            "backend_status": status,
            "rate_or_usage_backoff": wants_backoff,
        }

    def _wait_for_backend_launch_slot(self, *, run_dir: Path, spacing_seconds: int) -> dict[str, Any]:
        spacing = max(0, spacing_seconds)
        if spacing <= 0:
            return {"status": "disabled", "spacing_seconds": 0, "waited_seconds": 0.0}
        runtime_dir = self.repo_root / "artifacts" / "runtime"
        runtime_dir.mkdir(parents=True, exist_ok=True)
        lock_path = runtime_dir / "math_attack_backend_launch.lock"
        stamp_path = runtime_dir / "math_attack_backend_launch_last.txt"
        started = time.monotonic()
        with lock_path.open("a+", encoding="utf-8") as lock_file:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            last_launch = 0.0
            try:
                last_launch = float(stamp_path.read_text(encoding="utf-8").strip() or "0")
            except (OSError, ValueError):
                last_launch = 0.0
            now = time.monotonic()
            wait_seconds = max(0.0, spacing - (now - last_launch))
            if wait_seconds > 0:
                time.sleep(wait_seconds)
            stamp_path.write_text(str(time.monotonic()), encoding="utf-8")
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        return {
            "status": "waited" if time.monotonic() - started > 0.01 else "ready",
            "spacing_seconds": spacing,
            "waited_seconds": round(time.monotonic() - started, 3),
            "run_dir": str(run_dir),
        }

    def _append_journal(self, *, run_dir: Path, iteration: int, output_path: Path, context_bundle: str) -> None:
        journal_path = run_dir / "journal.md"
        existing = read_text(journal_path)
        output = read_text(output_path).strip()
        context_tail = context_bundle[-5000:]
        entry = "\n".join(
            [
                f"## Iteration {iteration:03d} ({utc_now_iso()})",
                "",
                "### Context Bundle Tail",
                "",
                "```",
                context_tail.rstrip(),
                "```",
                "",
                "### Backend Output",
                "",
                output,
                "",
            ]
        )
        write_text(journal_path, (existing.rstrip() + "\n\n" + entry).strip() + "\n")

    def run(
        self,
        *,
        project_dir: Path,
        target: str,
        context_paths: list[Path] | None = None,
        evidence_command: list[str] | None = None,
        evidence_cwd: Path | None = None,
        evidence_timeout_sec: int = 120,
        backend: str = "codex",
        iterations: int = 3,
        time_budget_sec: int = 900,
        iteration_timeout_sec: int = 180,
        sleep_seconds: int = 0,
        sleep_mode: str = "adaptive",
        min_sleep_seconds: int | None = None,
        max_sleep_seconds: int | None = None,
        sleep_jitter_seconds: int | None = None,
        launch_spacing_seconds: int | None = None,
        run_name: str | None = None,
        enable_search: bool = True,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        project_dir = project_dir.resolve()
        run_dir = self._new_run_dir(project_dir, run_name)
        iterations_dir = run_dir / "iterations"
        iterations_dir.mkdir(parents=True, exist_ok=True)

        target = target.strip() or str((load_project_manifest(project_dir).get("problem") or {}).get("statement", "")).strip()
        deadline = time.monotonic() + max(1, time_budget_sec)
        processed = 0
        last_backend_status = "not_started"
        last_evidence_status = "not_started"
        started_at = utc_now_iso()
        sleep_policy = {
            "mode": sleep_mode,
            "sleep_seconds": sleep_seconds,
            "min_sleep_seconds": min_sleep_seconds,
            "max_sleep_seconds": max_sleep_seconds,
            "sleep_jitter_seconds": sleep_jitter_seconds,
            "launch_spacing_seconds": launch_spacing_seconds,
        }
        write_json(
            run_dir / "state.json",
            {
                "status": "running",
                "started_at": started_at,
                "project_dir": str(project_dir),
                "target": target,
                "backend": backend,
                "iterations_requested": iterations,
                "time_budget_sec": time_budget_sec,
                "iteration_timeout_sec": iteration_timeout_sec,
                "sleep_policy": sleep_policy,
                "dry_run": dry_run,
            },
        )

        context_paths = context_paths or []
        evidence_command = evidence_command or []
        evidence_cwd = (evidence_cwd or project_dir).resolve()

        for iteration in range(1, max(1, iterations) + 1):
            if time.monotonic() >= deadline:
                break
            headroom = wait_for_system_headroom(
                min_available_memory_mb=self.min_available_memory_mb,
                max_load_per_cpu=1.5,
                max_wait_seconds=self.wait_max_seconds,
                poll_seconds=self.wait_poll_seconds,
            )
            if headroom["status"] != "ready":
                last_backend_status = "blocked"
                break

            evidence_report = self._run_evidence_command(
                command=evidence_command,
                cwd=evidence_cwd,
                timeout_sec=evidence_timeout_sec,
            )
            last_evidence_status = str(evidence_report.get("status", ""))
            context_files = [self._read_context_file(path, max_chars=12000) for path in context_paths]
            context_bundle = self._format_context_bundle(
                project_dir=project_dir,
                target=target,
                context_files=context_files,
                evidence_report=evidence_report,
            )
            write_text(run_dir / "latest_context_bundle.md", context_bundle)
            prompt = self._build_prompt(
                run_dir=run_dir,
                iteration=iteration,
                target=target,
                context_bundle=context_bundle,
            )

            prompt_path = iterations_dir / f"iter_{iteration:03d}_prompt.txt"
            output_path = iterations_dir / f"iter_{iteration:03d}_output.md"
            meta_path = iterations_dir / f"iter_{iteration:03d}_meta.json"
            write_text(prompt_path, prompt)
            if dry_run:
                output_path.write_text("Dry run: backend was not invoked.\n", encoding="utf-8")
                backend_report = {
                    "backend": backend,
                    "status": "dry_run",
                    "returncode": 0,
                    "elapsed_seconds": 0.0,
                    "command": [],
                }
            else:
                remaining = max(1, int(deadline - time.monotonic()))
                launch_spacing_report = self._wait_for_backend_launch_slot(
                    run_dir=run_dir,
                    spacing_seconds=(
                        self.default_launch_spacing_seconds
                        if launch_spacing_seconds is None
                        else int(launch_spacing_seconds)
                    ),
                )
                backend_report = self._invoke_backend(
                    backend=backend,
                    run_dir=run_dir,
                    prompt=prompt,
                    output_path=output_path,
                    timeout_sec=min(iteration_timeout_sec, remaining),
                    enable_search=enable_search,
                )
            if dry_run:
                launch_spacing_report = {"status": "skipped", "spacing_seconds": 0, "waited_seconds": 0.0}
            last_backend_status = str(backend_report.get("status", ""))
            sleep_plan = self._sleep_plan(
                run_dir=run_dir,
                iteration=iteration,
                iterations=max(1, iterations),
                deadline=deadline,
                sleep_mode=sleep_mode,
                sleep_seconds=sleep_seconds,
                min_sleep_seconds=min_sleep_seconds,
                max_sleep_seconds=max_sleep_seconds,
                sleep_jitter_seconds=sleep_jitter_seconds,
                backend_report=backend_report,
            )
            write_json(
                meta_path,
                {
                    "iteration": iteration,
                    "started_at": utc_now_iso(),
                    "prompt_path": str(prompt_path),
                    "output_path": str(output_path),
                    "context_bundle_path": str(run_dir / "latest_context_bundle.md"),
                    "evidence_report": {
                        **evidence_report,
                        "stdout": str(evidence_report.get("stdout", ""))[-12000:],
                        "stderr": str(evidence_report.get("stderr", ""))[-4000:],
                    },
                    "launch_spacing_report": launch_spacing_report,
                    "backend_report": backend_report,
                    "sleep_plan": sleep_plan,
                    "system_headroom": headroom,
                },
            )
            self._append_journal(run_dir=run_dir, iteration=iteration, output_path=output_path, context_bundle=context_bundle)
            processed += 1
            if sleep_plan["seconds"] > 0:
                time.sleep(int(sleep_plan["seconds"]))

        status = "completed" if processed > 0 and last_backend_status in {"completed", "skipped", "dry_run"} else last_backend_status
        payload = {
            "generated_at": utc_now_iso(),
            "project_dir": str(project_dir),
            "run_dir": str(run_dir),
            "target": target,
            "status": status,
            "backend": backend,
            "iterations_completed": processed,
            "last_backend_status": last_backend_status,
            "last_evidence_status": last_evidence_status,
            "journal_path": str(run_dir / "journal.md"),
            "latest_context_bundle_path": str(run_dir / "latest_context_bundle.md"),
            "sleep_policy": sleep_policy,
        }
        write_json(run_dir / "state.json", {**payload, "started_at": started_at})
        write_json(self._status_path(project_dir), payload)
        return payload
