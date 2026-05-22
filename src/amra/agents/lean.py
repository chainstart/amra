from __future__ import annotations

import re
import shlex
from pathlib import Path
from typing import Any

from amra.agents.episode_loop import (
    CodexEpisodeConfig,
    CodexEpisodeLoopAgent,
    EpisodeObserver,
    _count_lean_pattern,
    _extract_lean_target_name,
    _extract_status,
    _iter_project_lean_files,
    _lean_target_exists,
    _resolve_loose,
    _run_command,
    _tail,
    utc_now_iso,
    write_json,
    write_text,
)
from amra.agents.tools import ToolRegistry


class LeanFromNaturalProofAgent:
    """Lean formalizer using Codex as the inner agent and host Lean audits."""

    SYSTEM_PROMPT = """
You are a pure Lean formalization agent.
You own the inner action loop for this episode: inspect the Lean project, edit Lean files, run verifier commands, and repair errors.
The host will independently run the verifier and audit forbidden placeholders after your episode.
Do not invent trusted assumptions such as axiom, constant, opaque, admit, or sorry unless the user explicitly permits them.
You are not following a fixed workflow; decide actions from the proof package, Lean errors, and current project state.
Before attempting a broad formalization, create a small compiling checkpoint or write a formalization plan under the run directory so timeout still leaves a useful state.
"""

    SORRY_PATTERN = re.compile(r"\bsorry\b")
    AXIOM_PATTERN = re.compile(r"^\s*axiom\b", re.MULTILINE)
    ADMIT_PATTERN = re.compile(r"\badmit\b")
    CONSTANT_PATTERN = re.compile(r"^\s*(constant|opaque)\b", re.MULTILINE)

    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = _resolve_loose(repo_root)

    def run(
        self,
        *,
        workspace: Path,
        proof_package: str,
        statement: str = "",
        build_command: list[str] | None = None,
        backend: str = "codex",
        max_steps: int = 20,
        time_budget_sec: int = 3600,
        step_timeout_sec: int = 300,
        command_timeout_sec: int = 300,
        output_root: Path | None = None,
        run_name: str | None = None,
        enable_search: bool = True,
        model: str | None = None,
        reasoning_effort: str | None = None,
        math_tools_profile: str = "full",
        install_missing_math_tools: bool | None = None,
        run_math_tool_smoke: bool | None = None,
    ) -> dict[str, Any]:
        workspace = _resolve_loose(workspace)
        if not workspace.exists():
            raise FileNotFoundError(f"Lean workspace does not exist: {workspace}")
        build_command = build_command or ["lake", "build"]
        output_root = output_root or (self.repo_root / "artifacts" / "pure_lean_formalizer")
        config = CodexEpisodeConfig(
            name="lean-from-natural-proof-formalizer",
            system_prompt=self.SYSTEM_PROMPT,
            workspace=workspace,
            output_root=output_root,
            run_name=run_name,
            backend=backend,
            model=model,
            reasoning_effort=reasoning_effort,
            enable_search=enable_search,
            max_episodes=max_steps,
            time_budget_sec=time_budget_sec,
            episode_timeout_sec=step_timeout_sec,
            sandbox="workspace-write",
        )
        loop = CodexEpisodeLoopAgent(config)
        registry = ToolRegistry(
            build_command=build_command,
            math_tools_profile=math_tools_profile,
            install_missing_math_tools=install_missing_math_tools,
        )
        tool_snapshot = registry.write_artifacts(
            loop.run_dir,
            workspace=workspace,
            run_math_tool_smoke=run_math_tool_smoke,
        )
        write_text(loop.run_dir / "proof_package.md", proof_package.strip() + "\n")
        write_text(loop.run_dir / "statement.md", statement.strip() + "\n")
        write_json(loop.run_dir / "formalizer_environment.json", {"build_command": build_command, "workspace": str(workspace)})
        target_name = _extract_lean_target_name(statement) or _extract_lean_target_name(proof_package)
        initial_observation = self._lean_observation(
            episode=0,
            last_message="",
            backend_report={"status": "initial"},
            workspace=workspace,
            build_command=build_command,
            build_timeout_sec=command_timeout_sec,
            target_name=target_name,
        )
        goal = "\n".join(
            [
                "Formalize the supplied natural-language proof package in Lean.",
                "",
                "Lean workspace:",
                str(workspace),
                "",
                "Proof package content:",
                "",
                "```text",
                proof_package.strip()[:40000] or "<empty>",
                "```",
                "",
                "Statement or target hint:",
                statement.strip() or "<not supplied>",
                "",
                "Verifier command the host will also run after each episode:",
                shlex.join(build_command),
                "",
                "AMRA math tools report:",
                str(loop.run_dir / "math_tools_report.md"),
                "",
                "Use these tools early for small Lean probes, Python/Z3/CAS counterchecks, and finite searches before committing to a large formalization route.",
                "",
                "Use your own tools inside the episode to inspect files, edit Lean, run the verifier, and repair errors.",
            ]
        )
        report = loop.run(
            goal=goal,
            episode_cwd=workspace,
            observer=self._observe_episode(workspace, build_command, command_timeout_sec, target_name),
            initial_observation=initial_observation,
        )
        report["proof_package_path"] = str(loop.run_dir / "proof_package.md")
        report["statement_path"] = str(loop.run_dir / "statement.md")
        report["tool_registry_path"] = str(loop.run_dir / "tool_registry.md")
        report["math_tools_report_path"] = str(loop.run_dir / "math_tools_report.md")
        report["tool_snapshot"] = tool_snapshot
        report["build_command"] = build_command
        write_json(loop.run_dir / "report.json", report)
        return report

    def _observe_episode(
        self,
        workspace: Path,
        build_command: list[str],
        build_timeout_sec: int,
        target_name: str,
    ) -> EpisodeObserver:
        def observe(episode: int, episode_dir: Path, last_message: str, backend_report: dict[str, Any]) -> dict[str, Any]:
            del episode_dir
            return self._lean_observation(
                episode=episode,
                last_message=last_message,
                backend_report=backend_report,
                workspace=workspace,
                build_command=build_command,
                build_timeout_sec=build_timeout_sec,
                target_name=target_name,
            )

        return observe

    def _lean_observation(
        self,
        *,
        episode: int,
        last_message: str,
        backend_report: dict[str, Any],
        workspace: Path,
        build_command: list[str],
        build_timeout_sec: int,
        target_name: str,
    ) -> dict[str, Any]:
        build_report = _run_command(build_command, cwd=workspace, timeout_sec=build_timeout_sec)
        counts = {
            "sorry": _count_lean_pattern(workspace, self.SORRY_PATTERN),
            "axiom": _count_lean_pattern(workspace, self.AXIOM_PATTERN),
            "admit": _count_lean_pattern(workspace, self.ADMIT_PATTERN),
            "constant_or_opaque": _count_lean_pattern(workspace, self.CONSTANT_PATTERN),
        }
        forbidden_total = sum(counts.values())
        target_exists = _lean_target_exists(workspace, target_name)
        backend_status = str(backend_report.get("status") or "")
        status = _extract_status(last_message, fallback="partial")
        if build_report["status"] == "passed" and forbidden_total == 0 and target_exists is not False:
            status = "verified"
        elif backend_status in {"skipped", "unsupported", "unavailable"}:
            status = "blocked"
        else:
            status = "partial" if status == "verified" else status
        terminal = status in {"verified", "blocked", "failed"}
        return {
            "episode": episode,
            "generated_at": utc_now_iso(),
            "status": status,
            "terminal": terminal,
            "stop_reason": f"{status}_reported" if terminal else "",
            "backend_status": backend_status,
            "build": build_report,
            "counts": counts,
            "target_name": target_name,
            "target_exists": target_exists,
            "lean_file_count": len(_iter_project_lean_files(workspace)),
            "last_message_tail": _tail(last_message, 4000),
        }



__all__ = ["LeanFromNaturalProofAgent"]
