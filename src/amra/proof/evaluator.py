from __future__ import annotations

import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from amra.infra.runtime import env_int, run_guarded_command
from amra.core.workspace import read_json, utc_now_iso, write_json


PLACEHOLDER_SEARCH_CONTRACT = "Specify the exact finite search assumptions before running any computational search."


class EvaluatorPlanner:
    """Synthesize evaluator-first guidance for search-friendly math problems."""

    def _search_friendly(self, *, tags: list[str], seed_family: str) -> bool:
        tag_set = {item.strip() for item in tags if item and item.strip()}
        if tag_set.intersection({"computational_search", "finite_case", "counterexample_search"}):
            return True
        return seed_family in {"weird_numbers", "minimum_overlap", "prime_plus_two_powers", "triangle_dissection"}

    def _command_preview(self, raw_command: Any) -> list[str]:
        if isinstance(raw_command, list):
            return [str(item).strip() for item in raw_command if str(item).strip()]
        if isinstance(raw_command, str) and raw_command.strip():
            return shlex.split(raw_command.strip())
        return []

    def build_plan(
        self,
        *,
        manifest: dict[str, Any],
        seed_family: str,
        route_scaffold: dict[str, Any],
        checkpoint_contract: dict[str, Any],
        script_inventory: list[dict[str, Any]],
        counterexample_contract: dict[str, Any],
    ) -> dict[str, Any]:
        problem = manifest.get("problem") or {}
        tags = list(problem.get("tags", []))
        search_friendly = self._search_friendly(tags=tags, seed_family=seed_family)
        raw_contract = str(counterexample_contract.get("search_contract", "")).strip()
        has_specific_contract = bool(raw_contract and raw_contract != PLACEHOLDER_SEARCH_CONTRACT)
        command_preview = self._command_preview(counterexample_contract.get("command"))

        if not search_friendly:
            evaluator_mode = "theorem_import_only"
        elif script_inventory:
            evaluator_mode = "script_backed_search"
        elif has_specific_contract:
            evaluator_mode = "contract_defined_search"
        else:
            evaluator_mode = "contract_first_search"

        candidate_scripts = [
            {
                "name": item.get("name", ""),
                "path": item.get("path", ""),
                "source_root": item.get("source_root", ""),
            }
            for item in script_inventory[:8]
        ]
        selected_script = candidate_scripts[0] if candidate_scripts else {}
        execution_kind = "none"
        if command_preview:
            execution_kind = "contract_command"
        elif selected_script:
            execution_kind = "candidate_script"
        elif has_specific_contract:
            execution_kind = "manual_contract"

        ready_to_run = search_friendly and execution_kind in {"contract_command", "candidate_script"}
        auto_run_allowed = bool(counterexample_contract.get("auto_run_allowed", False))

        recommended_workflow = [
            "Use theorem import and explicit theorem-chain narrowing before any broad natural-language proof attempt."
        ]
        if search_friendly:
            recommended_workflow = [
                "Start with the evaluator or search contract if it can quickly reject bad branches or certify a bounded checkpoint.",
                "Preserve every bound, assumption, and output as a project artifact before translating conclusions into Lean.",
                "Treat evaluator output as checkpoint evidence, not as a solved main theorem claim.",
            ]
            if execution_kind == "candidate_script":
                recommended_workflow.append("Prefer the strongest local bounded-search script before writing a new one.")
            elif execution_kind == "contract_command":
                recommended_workflow.append("The search contract already contains an executable command; keep its outputs tied to the checkpoint theorem.")
            elif evaluator_mode == "contract_defined_search":
                recommended_workflow.append("The search contract is specific, but it still needs an executable command or script hook.")
            else:
                recommended_workflow.append("Write a tighter finite contract before trusting any computational branch.")

        next_actions = []
        if search_friendly and not has_specific_contract:
            next_actions.append("Replace the placeholder counterexample/search contract with a precise finite range and explicit assumptions.")
        if search_friendly and execution_kind == "none":
            next_actions.append("Attach or write one bounded evaluator script or add an explicit command to the search contract.")
        if search_friendly and execution_kind != "none" and not auto_run_allowed:
            next_actions.append("Mark the search contract as `auto_run_allowed` once the command is safe to run in the default loop.")
        if checkpoint_contract.get("checkpoint_statement"):
            next_actions.append("Tie every evaluator output back to the current checkpoint theorem rather than to the full open target.")
        if not next_actions:
            next_actions.append("Run the current evaluator-first loop against the strongest checkpoint artifact.")

        stop_conditions = [
            "Stop if the evaluator only confirms an easier variant than the current checkpoint contract.",
            "Stop if a script produces raw output without a project-local statement of assumptions and interpretation.",
            "Stop if evaluator work no longer improves the checkpoint contract or theorem chain.",
        ]
        if evaluator_mode == "theorem_import_only":
            stop_conditions.append("Do not invent an evaluator where the problem currently looks theorem-import dominated.")

        return {
            "generated_at": utc_now_iso(),
            "project_name": str(manifest.get("project_name", "")),
            "problem_id": str(problem.get("problem_id", "")),
            "seed_family": seed_family,
            "search_friendly": search_friendly,
            "evaluator_mode": evaluator_mode,
            "execution_kind": execution_kind,
            "ready_to_run": ready_to_run,
            "auto_run_allowed": auto_run_allowed,
            "checkpoint_statement": str(checkpoint_contract.get("checkpoint_statement", "")),
            "counterexample_contract_status": str(counterexample_contract.get("status", "not_started")),
            "has_specific_search_contract": has_specific_contract,
            "candidate_script_count": len(candidate_scripts),
            "candidate_scripts": candidate_scripts,
            "selected_script": selected_script,
            "command_preview": command_preview,
            "working_directory_hint": str(counterexample_contract.get("working_directory", "")).strip(),
            "expected_output_paths": [str(item) for item in counterexample_contract.get("expected_output_paths", [])],
            "recommended_workflow": recommended_workflow,
            "next_actions": next_actions,
            "stop_conditions": stop_conditions,
            "preferred_artifacts": [
                "proof/counterexample_search_contract.json",
                "proof/checkpoint_contract.json",
                "proof/evaluator_plan.json",
                "proof/evaluator_report.json",
            ],
            "route_first_targets": list(route_scaffold.get("first_edit_targets", [])),
        }


class EvaluatorRunner:
    """Execute a bounded evaluator command or local search script and persist a structured report."""

    def __init__(self) -> None:
        self.max_memory_mb = env_int("ARA_MATH_EVALUATOR_MAX_MEMORY_MB", 4096)
        self.max_cpu_seconds = env_int("ARA_MATH_EVALUATOR_MAX_CPU_SECONDS", 180)
        self.max_processes = env_int("ARA_MATH_EVALUATOR_MAX_PROCESSES", 128)
        self.niceness = env_int("ARA_MATH_EVALUATOR_NICENESS", 10)
        self.default_timeout_sec = env_int("ARA_MATH_EVALUATOR_TIMEOUT_SECONDS", 120)

    def _normalize_command(self, raw_command: Any) -> list[str]:
        if isinstance(raw_command, list):
            return [str(item).strip() for item in raw_command if str(item).strip()]
        if isinstance(raw_command, str) and raw_command.strip():
            return shlex.split(raw_command.strip())
        return []

    def _resolve_workdir(self, project_dir: Path, raw_value: str) -> Path:
        if not raw_value.strip():
            return project_dir
        path = Path(raw_value)
        return path if path.is_absolute() else (project_dir / path)

    def _default_script_command(self, script_path: Path) -> list[str]:
        suffix = script_path.suffix.lower()
        if suffix == ".py":
            return [sys.executable, str(script_path)]
        if suffix == ".sh":
            return ["/bin/bash", str(script_path)]
        return [str(script_path)]

    def _resolve_execution(
        self,
        *,
        project_dir: Path,
        evaluator_plan: dict[str, Any],
        counterexample_contract: dict[str, Any],
    ) -> dict[str, Any]:
        contract_command = self._normalize_command(counterexample_contract.get("command"))
        if contract_command:
            workdir = self._resolve_workdir(project_dir, str(counterexample_contract.get("working_directory", "")))
            return {
                "ready": True,
                "command_source": "contract_command",
                "command": contract_command,
                "workdir": workdir,
            }

        selected_script = evaluator_plan.get("selected_script") or {}
        script_path_raw = str(selected_script.get("path", "")).strip()
        if script_path_raw:
            script_path = Path(script_path_raw)
            workdir_hint = str(selected_script.get("source_root", "")).strip()
            workdir = self._resolve_workdir(project_dir, workdir_hint) if workdir_hint else script_path.parent
            return {
                "ready": True,
                "command_source": "candidate_script",
                "command": self._default_script_command(script_path),
                "workdir": workdir,
            }

        return {
            "ready": False,
            "command_source": "none",
            "command": [],
            "workdir": project_dir,
            "reason": "No executable evaluator command or candidate script is available.",
        }

    def _expected_outputs(self, project_dir: Path, workdir: Path, counterexample_contract: dict[str, Any]) -> list[dict[str, Any]]:
        expected = []
        for raw_path in counterexample_contract.get("expected_output_paths", []):
            text = str(raw_path).strip()
            if not text:
                continue
            path = Path(text)
            if not path.is_absolute():
                path = workdir / path
            expected.append({"path": str(path), "exists": path.exists()})
        return expected

    def run(
        self,
        project_dir: Path,
        *,
        evaluator_plan: dict[str, Any] | None = None,
        counterexample_contract: dict[str, Any] | None = None,
        timeout_sec: int | None = None,
        auto: bool = False,
    ) -> dict[str, Any]:
        project_dir = project_dir.resolve()
        proof_dir = project_dir / "proof"
        evaluator_plan = evaluator_plan or read_json(proof_dir / "evaluator_plan.json", default={})
        counterexample_contract = counterexample_contract or read_json(
            proof_dir / "counterexample_search_contract.json",
            default={},
        )

        report_base = {
            "generated_at": utc_now_iso(),
            "project_dir": str(project_dir),
            "project_name": project_dir.name,
            "mode": "auto" if auto else "manual",
            "evaluator_mode": str(evaluator_plan.get("evaluator_mode", "")),
            "execution_kind": str(evaluator_plan.get("execution_kind", "")),
            "ready_to_run": bool(evaluator_plan.get("ready_to_run", False)),
        }

        if not evaluator_plan.get("search_friendly", False):
            report = {
                **report_base,
                "status": "skipped",
                "reason": "Evaluator execution skipped because the current project is theorem-import dominated.",
            }
            write_json(proof_dir / "evaluator_report.json", report)
            return report

        if auto and not evaluator_plan.get("auto_run_allowed", False):
            report = {
                **report_base,
                "status": "skipped",
                "reason": "Evaluator execution is ready, but auto-run is disabled in the current search contract.",
            }
            write_json(proof_dir / "evaluator_report.json", report)
            return report

        execution = self._resolve_execution(
            project_dir=project_dir,
            evaluator_plan=evaluator_plan,
            counterexample_contract=counterexample_contract,
        )
        if not execution["ready"]:
            report = {
                **report_base,
                "status": "blocked",
                "reason": execution["reason"],
                "command_source": execution["command_source"],
                "command": execution["command"],
                "workdir": str(execution["workdir"]),
            }
            write_json(proof_dir / "evaluator_report.json", report)
            return report

        command = list(execution["command"])
        workdir = Path(execution["workdir"])
        timeout = timeout_sec or int(counterexample_contract.get("timeout_sec", 0) or 0) or self.default_timeout_sec
        if not workdir.exists():
            report = {
                **report_base,
                "status": "blocked",
                "reason": f"Evaluator working directory does not exist: {workdir}",
                "command_source": execution["command_source"],
                "command": command,
                "workdir": str(workdir),
            }
            write_json(proof_dir / "evaluator_report.json", report)
            return report

        started = time.monotonic()
        try:
            completed = run_guarded_command(
                command,
                cwd=workdir,
                timeout=timeout,
                memory_mb=self.max_memory_mb,
                cpu_seconds=min(self.max_cpu_seconds, max(timeout + 10, timeout)),
                max_processes=self.max_processes,
                niceness=self.niceness,
            )
            status = "completed" if completed.returncode == 0 else "failed"
            stdout_tail = "\n".join(completed.stdout.splitlines()[-20:])
            stderr_tail = "\n".join(completed.stderr.splitlines()[-20:])
            returncode: int | None = completed.returncode
        except subprocess.TimeoutExpired as exc:
            status = "timeout"
            stdout_tail = str(exc.output or "")[-6000:]
            stderr_tail = str(exc.stderr or "")[-6000:]
            returncode = None

        expected_outputs = self._expected_outputs(project_dir, workdir, counterexample_contract)
        report = {
            **report_base,
            "status": status,
            "command_source": execution["command_source"],
            "command": command,
            "workdir": str(workdir),
            "timeout_sec": timeout,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "returncode": returncode,
            "stdout_tail": stdout_tail,
            "stderr_tail": stderr_tail,
            "expected_outputs": expected_outputs,
            "resource_policy": {
                "memory_mb": self.max_memory_mb,
                "cpu_seconds": min(self.max_cpu_seconds, max(timeout + 10, timeout)),
                "max_processes": self.max_processes,
                "niceness": self.niceness,
            },
        }
        write_json(proof_dir / "evaluator_report.json", report)

        updated_contract = dict(counterexample_contract)
        updated_contract["generated_at"] = utc_now_iso()
        updated_contract["last_run_status"] = status
        updated_contract["last_run_at"] = report["generated_at"]
        updated_contract["last_run_mode"] = report["mode"]
        updated_contract["last_command"] = command
        write_json(proof_dir / "counterexample_search_contract.json", updated_contract)
        return report
