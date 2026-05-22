from __future__ import annotations

import json
import os
import shlex
from pathlib import Path
from typing import Any

from amra.agents.episode_loop import (
    CodexEpisodeConfig,
    CodexEpisodeLoopAgent,
    EpisodeObserver,
    _count_lean_pattern,
    _extract_lean_target_name,
    _extract_next,
    _extract_status,
    _iter_project_lean_files,
    _lean_target_exists,
    _resolve_loose,
    _run_command,
    _tail,
    read_text,
    utc_now_iso,
    write_json,
    write_text,
)
from amra.agents.lean import LeanFromNaturalProofAgent
from amra.agents.tools import ToolRegistry
from amra.proof.state import ProofArtifactTracker


class NaturalLanguageTheoremProverAgent:
    """Compatibility wrapper for proof-note-first theorem proving."""

    SYSTEM_PROMPT = """
You are a proof-note-first theorem-proving agent working in natural language and mathematical notation.
You own the inner action loop for this episode: inspect available files, run computations, run small Lean/Python/Z3 probes if useful, write notes, and refine the proof.
Do not edit repository source files. Write durable proof artifacts under the run directory; Lean scratch/probe files under the run directory are allowed.
You are not following a fixed workflow; choose actions from the current mathematical state.
Before any long computation or deep proof search, create or update at least one durable artifact such as dependency_graph.md or blocker.md so timeout still leaves a useful state.
Durable recovery contract: if you cannot complete proof_package.md and formalizer_handoff.md in this episode, write at least one recovery artifact before ending or before any risky long search: blocker.md, partial_lemmas.md, failed_routes.md, or invariant_candidates.md.
If the latest host observation says recovery_required, your first task is to synthesize current notes, logs, and context into blocker.md plus any useful partial_lemmas.md, failed_routes.md, or invariant_candidates.md; do not start a fresh broad proof search until those artifacts exist.
If the context bundle already contains a plausible proof package, do not spend the episode reproving it from scratch. First write formalizer_handoff.md with a theorem statement, definitions, lemma boundaries, construction obligations, impossibility obligations, and known blockers.
If a proof is plausible, produce a formalizer handoff with the exact statement, definitions, dependencies, and lemmas.
"""

    TERMINAL_STATUSES = {"proved_candidate", "counterexample_suspected", "failed"}
    ARTIFACT_NAMES = [
        "proof_package.md",
        "formalizer_handoff.md",
        "dependency_graph.md",
        "blocker.md",
        "partial_lemmas.md",
        "failed_routes.md",
        "invariant_candidates.md",
        "counterexample_report.md",
        "external_source_policy_violation.md",
    ]
    RECOVERY_ARTIFACTS = [
        "blocker.md",
        "partial_lemmas.md",
        "failed_routes.md",
        "invariant_candidates.md",
    ]
    RECOVERY_DETAIL_ARTIFACTS = [
        "partial_lemmas.md",
        "failed_routes.md",
        "invariant_candidates.md",
    ]

    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = _resolve_loose(repo_root)

    def run(
        self,
        *,
        statement: str,
        workspace: Path | None = None,
        context_paths: list[Path] | None = None,
        backend: str = "codex",
        max_steps: int = 16,
        time_budget_sec: int = 3600,
        step_timeout_sec: int = 300,
        command_timeout_sec: int = 120,
        output_root: Path | None = None,
        run_name: str | None = None,
        enable_search: bool = True,
        model: str | None = None,
        reasoning_effort: str | None = None,
        math_tools_profile: str = "full",
        install_missing_math_tools: bool | None = None,
        run_math_tool_smoke: bool | None = None,
    ) -> dict[str, Any]:
        del command_timeout_sec
        workspace = workspace or self.repo_root
        output_root = output_root or (self.repo_root / "artifacts" / "pure_theorem_prover")
        config = CodexEpisodeConfig(
            name="natural-language-theorem-prover",
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
            math_tools_profile=math_tools_profile,
            install_missing_math_tools=install_missing_math_tools,
        )
        tool_snapshot = registry.write_artifacts(
            loop.run_dir,
            workspace=workspace,
            run_math_tool_smoke=run_math_tool_smoke,
        )
        write_text(loop.run_dir / "statement.md", statement.strip() + "\n")
        write_text(loop.run_dir / "context_bundle.md", self._context_bundle(context_paths or []))
        goal = "\n".join(
            [
                "Attack the theorem with proof notes as the primary artifact.",
                "You may use Lean/Python/Z3/shell probes to test local ideas, but this compatibility wrapper does not manage a full Lean workspace.",
                "Your writable workspace for proof artifacts is the run directory.",
                "",
                "Theorem statement file:",
                str(loop.run_dir / "statement.md"),
                "",
                "Context bundle file:",
                str(loop.run_dir / "context_bundle.md"),
                "",
                "AMRA math tools report:",
                str(loop.run_dir / "math_tools_report.md"),
                "",
                "Before committing to a long proof route, use the available Python/Z3/CAS/Lean tools for quick falsification, finite search, modular checks, or theorem-shape probes when relevant.",
                "",
                "Durable artifacts to create when justified:",
                "- proof_package.md",
                "- formalizer_handoff.md",
                "- dependency_graph.md",
                "- blocker.md",
                "- partial_lemmas.md",
                "- failed_routes.md",
                "- invariant_candidates.md",
                "- counterexample_report.md",
                "",
                "Persistence rule: write an initial dependency_graph.md or blocker.md before spending significant time on search.",
                "Recovery rule: if a complete proof is not ready, write blocker.md and at least one of partial_lemmas.md, failed_routes.md, or invariant_candidates.md before continuing broad proof search.",
                "If context_bundle.md already includes a proof candidate, write formalizer_handoff.md before rewriting proof_package.md.",
                "",
                "Do not wait for the host to perform single tool actions. Use your own tools inside the episode.",
            ]
        )
        report = loop.run(
            goal=goal,
            episode_cwd=loop.run_dir,
            observer=self._observe_episode(loop.run_dir),
            initial_observation=self._artifact_observation(loop.run_dir, "", {"status": "initial"}),
        )
        report["statement_path"] = str(loop.run_dir / "statement.md")
        report["context_bundle_path"] = str(loop.run_dir / "context_bundle.md")
        report["tool_registry_path"] = str(loop.run_dir / "tool_registry.md")
        report["math_tools_report_path"] = str(loop.run_dir / "math_tools_report.md")
        report["tool_snapshot"] = tool_snapshot
        write_json(loop.run_dir / "report.json", report)
        return report

    def _context_bundle(self, context_paths: list[Path]) -> str:
        if not context_paths:
            return "No context files supplied.\n"
        chunks: list[str] = []
        for raw_path in context_paths:
            path = _resolve_loose(raw_path)
            text = read_text(path, max_chars=20000)
            chunks.extend(
                [
                    f"## {path}",
                    "",
                    f"- Exists: {path.exists()}",
                    "",
                    "```text",
                    text.strip() or "<empty>",
                    "```",
                    "",
                ]
            )
        return "\n".join(chunks).rstrip() + "\n"

    def _observe_episode(self, run_dir: Path) -> EpisodeObserver:
        def observe(episode: int, episode_dir: Path, last_message: str, backend_report: dict[str, Any]) -> dict[str, Any]:
            del episode_dir
            return self._artifact_observation(run_dir, last_message, backend_report, episode=episode)

        return observe

    def _artifact_observation(
        self,
        run_dir: Path,
        last_message: str,
        backend_report: dict[str, Any],
        *,
        episode: int = 0,
    ) -> dict[str, Any]:
        status = _extract_status(last_message, fallback="partial")
        next_action = _extract_next(last_message)
        if backend_report.get("status") == "policy_violation":
            status = "failed"
            next_action = "needs_human"
        elif backend_report.get("status") in {"skipped", "unsupported", "unavailable"}:
            status = "blocked"
        self._ensure_recovery_artifact(run_dir, status, last_message, backend_report, episode=episode)
        artifacts = self._artifact_snapshot(run_dir)
        has_recovery_artifacts = any(artifacts[name]["exists"] for name in self.RECOVERY_ARTIFACTS)
        if artifacts["external_source_policy_violation.md"]["exists"]:
            status = "failed"
            next_action = "needs_human"
        elif artifacts["counterexample_report.md"]["exists"]:
            status = "counterexample_suspected"
        elif (
            artifacts["proof_package.md"]["exists"]
            and artifacts["formalizer_handoff.md"]["exists"]
            and not has_recovery_artifacts
        ):
            status = "proved_candidate" if status == "partial" else status
        terminal = status in self.TERMINAL_STATUSES
        if status == "blocked":
            terminal = backend_report.get("status") in {"skipped", "unsupported", "unavailable"} or next_action in {
                "needs_human",
                "stop",
            }
        if status == "proved_candidate":
            terminal = artifacts["proof_package.md"]["exists"] and artifacts["formalizer_handoff.md"]["exists"]
        recovery_required = (
            episode > 0
            and not terminal
            and not artifacts["proof_package.md"]["exists"]
            and not artifacts["counterexample_report.md"]["exists"]
            and not any(artifacts[name]["exists"] for name in self.RECOVERY_ARTIFACTS)
        )
        directive = ""
        if recovery_required:
            directive = (
                "Recovery is required before broad proof search: first write blocker.md, then write any useful "
                "partial_lemmas.md, failed_routes.md, or invariant_candidates.md from the previous episode."
            )
        elif not terminal and artifacts["blocker.md"]["exists"] and not artifacts["proof_package.md"]["exists"]:
            directive = (
                "Continue from the existing recovery artifacts. First refine partial_lemmas.md, failed_routes.md, "
                "or invariant_candidates.md if they are missing or thin; then attack the named blocker."
            )
        return {
            "episode": episode,
            "generated_at": utc_now_iso(),
            "status": status,
            "next": next_action,
            "terminal": terminal,
            "stop_reason": f"{status}_reported" if terminal else "",
            "backend_status": backend_report.get("status"),
            "artifacts": artifacts,
            "recovery_required": recovery_required,
            "next_episode_directive": directive,
            "last_message_tail": _tail(last_message, 4000),
        }

    def _artifact_snapshot(self, run_dir: Path) -> dict[str, dict[str, Any]]:
        return {
            name: {
                "exists": (run_dir / name).exists(),
                "size": (run_dir / name).stat().st_size if (run_dir / name).exists() else 0,
            }
            for name in self.ARTIFACT_NAMES
        }

    def _ensure_recovery_artifact(
        self,
        run_dir: Path,
        status: str,
        last_message: str,
        backend_report: dict[str, Any],
        *,
        episode: int,
    ) -> None:
        if episode <= 0:
            return
        artifacts = self._artifact_snapshot(run_dir)
        has_complete_proof = artifacts["proof_package.md"]["exists"] and artifacts["formalizer_handoff.md"]["exists"]
        has_recovery = any(artifacts[name]["exists"] for name in self.RECOVERY_ARTIFACTS)
        has_recovery_detail = any(artifacts[name]["exists"] for name in self.RECOVERY_DETAIL_ARTIFACTS)
        has_counterexample = artifacts["counterexample_report.md"]["exists"]
        if has_complete_proof or has_recovery or has_counterexample:
            if (
                not has_complete_proof
                and not has_counterexample
                and has_recovery
                and not has_recovery_detail
                and artifacts["blocker.md"]["exists"]
                and episode > 1
                and status in {"partial", "blocked", "failed"}
            ):
                self._write_fallback_failed_routes(run_dir, status, last_message, backend_report, episode=episode)
            return
        if status not in {"partial", "blocked", "failed"}:
            return
        backend_status = str(backend_report.get("status") or "unknown")
        content = "\n".join(
            [
                f"# Host Fallback Blocker After Episode {episode}",
                "",
                "The episode did not leave a complete proof package or a recovery artifact.",
                "",
                "## Host observation",
                f"- Backend status: `{backend_status}`",
                f"- Reported status: `{status}`",
                "- Complete proof package present: no",
                "- Counterexample report present: no",
                "",
                "## Required next step",
                "Before broad proof search continues, synthesize the previous attempt into:",
                "- `partial_lemmas.md` for statements that appear reusable;",
                "- `failed_routes.md` for attempted routes and why they failed;",
                "- `invariant_candidates.md` for candidate invariants and small-case checks.",
                "",
                "## Last message tail",
                "```text",
                _tail(last_message.strip(), 3000) or "<empty>",
                "```",
                "",
            ]
        )
        write_text(run_dir / "blocker.md", content)

    def _write_fallback_failed_routes(
        self,
        run_dir: Path,
        status: str,
        last_message: str,
        backend_report: dict[str, Any],
        *,
        episode: int,
    ) -> None:
        backend_status = str(backend_report.get("status") or "unknown")
        content = "\n".join(
            [
                f"# Host Fallback Failed Routes After Episode {episode}",
                "",
                "A blocker existed, but the episode still did not leave partial lemmas, failed routes, or invariant candidates.",
                "",
                "## Host observation",
                f"- Backend status: `{backend_status}`",
                f"- Reported status: `{status}`",
                "",
                "## Required next step",
                "The next episode should convert this placeholder into mathematical content:",
                "- attempted routes and where they fail;",
                "- reusable partial lemmas;",
                "- candidate invariants with checked small cases or counterchecks.",
                "",
                "## Last message tail",
                "```text",
                _tail(last_message.strip(), 3000) or "<empty>",
                "```",
                "",
            ]
        )
        write_text(run_dir / "failed_routes.md", content)



class UnifiedProofAgentLoop:
    """Unified proof-development loop with shared natural-language and Lean tools."""

    SYSTEM_PROMPT = """
You are a unified mathematical proof-development agent.
You do not split the work into isolated natural-language and Lean phases. Instead, iterate like a proof engineer:
state a proof idea, test it with the available tools, record the result, refine definitions or lemmas, and repeat.
Your outputs may include natural-language lemmas, theorem statements, experiments, Lean scratch files, and verified Lean declarations.
Lean is available during exploration. Use small Lean probes early to test definitions, boundary conditions, and lemma shapes before a large formalization attempt.
Python, Z3, local search, and literature/source search are also available when they clarify the mathematical state.
You are not following a fixed workflow; choose actions from the current blocker and evidence.
Do not invent trusted assumptions such as axiom, constant, opaque, admit, or sorry unless the user explicitly permits them.
Before any long proof search, create or update durable artifacts so timeout still leaves useful state.
"""

    TERMINAL_STATUSES = {"verified", "proved_candidate", "counterexample_suspected", "failed"}

    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = _resolve_loose(repo_root)

    def run(
        self,
        *,
        statement: str,
        workspace: Path | None = None,
        context_paths: list[Path] | None = None,
        build_command: list[str] | None = None,
        target_name: str | None = None,
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
        resolved_workspace = _resolve_loose(workspace) if workspace is not None else None
        if resolved_workspace is not None and not resolved_workspace.exists():
            raise FileNotFoundError(f"Lean workspace does not exist: {resolved_workspace}")
        build_command = build_command or ["lake", "build"]
        output_root = output_root or (self.repo_root / "artifacts" / "pure_proof_agent")
        config = CodexEpisodeConfig(
            name="unified-proof-agent-loop",
            system_prompt=self.SYSTEM_PROMPT,
            workspace=resolved_workspace or self.repo_root,
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
        tracker = ProofArtifactTracker(loop.run_dir)
        registry = ToolRegistry(
            build_command=build_command,
            math_tools_profile=math_tools_profile,
            install_missing_math_tools=install_missing_math_tools,
        )
        tool_snapshot = registry.write_artifacts(
            loop.run_dir,
            workspace=resolved_workspace,
            run_math_tool_smoke=run_math_tool_smoke,
        )
        write_text(loop.run_dir / "statement.md", statement.strip() + "\n")
        write_text(loop.run_dir / "context_bundle.md", self._context_bundle(context_paths or []))
        extracted_target = (target_name or "").strip() or _extract_lean_target_name(statement)
        tracker.bootstrap(
            statement=statement,
            workspace=resolved_workspace,
            build_command=build_command,
            target_name=extracted_target,
            tool_registry_path=loop.run_dir / "tool_registry.md",
        )
        initial_observation = self._observe_state(
            episode=0,
            run_dir=loop.run_dir,
            workspace=resolved_workspace,
            build_command=build_command,
            build_timeout_sec=command_timeout_sec,
            target_name=extracted_target,
            last_message="",
            backend_report={"status": "initial"},
            tool_snapshot=tool_snapshot,
        )
        goal = self._build_goal(
            statement=statement,
            run_dir=loop.run_dir,
            workspace=resolved_workspace,
            build_command=build_command,
            target_name=extracted_target,
        )
        report = loop.run(
            goal=goal,
            episode_cwd=self._episode_cwd(run_dir=loop.run_dir, workspace=resolved_workspace),
            observer=self._observe_episode(
                run_dir=loop.run_dir,
                workspace=resolved_workspace,
                build_command=build_command,
                build_timeout_sec=command_timeout_sec,
                target_name=extracted_target,
                tool_snapshot=tool_snapshot,
            ),
            initial_observation=initial_observation,
        )
        report["statement_path"] = str(loop.run_dir / "statement.md")
        report["context_bundle_path"] = str(loop.run_dir / "context_bundle.md")
        report["tool_registry_path"] = str(loop.run_dir / "tool_registry.md")
        report["proof_state_path"] = str(loop.run_dir / "proof_state.json")
        report["workspace"] = str(resolved_workspace) if resolved_workspace is not None else ""
        report["build_command"] = build_command
        write_json(loop.run_dir / "report.json", report)
        return report

    def _context_bundle(self, context_paths: list[Path]) -> str:
        if not context_paths:
            return "No context files supplied.\n"
        chunks: list[str] = []
        for raw_path in context_paths:
            path = _resolve_loose(raw_path)
            text = read_text(path, max_chars=20000)
            chunks.extend(
                [
                    f"## {path}",
                    "",
                    f"- Exists: {path.exists()}",
                    "",
                    "```text",
                    text.strip() or "<empty>",
                    "```",
                    "",
                ]
            )
        return "\n".join(chunks).rstrip() + "\n"

    def _build_goal(
        self,
        *,
        statement: str,
        run_dir: Path,
        workspace: Path | None,
        build_command: list[str],
        target_name: str,
    ) -> str:
        workspace_lines = ["Lean workspace:", str(workspace)] if workspace is not None else ["Lean workspace:", "<not supplied>"]
        target_line = target_name or "<not supplied; create one if formalization becomes possible>"
        return "\n".join(
            [
                "Develop a proof through one unified proof loop.",
                "",
                "Primary rule: natural-language proof notes and Lean formalization are not separate phases. Use Lean/Python/Z3/search tools during exploration, then turn stable ideas into clearer notes and Lean artifacts.",
                "",
                "Run directory:",
                str(run_dir),
                "",
                *workspace_lines,
                "",
                "Target Lean declaration:",
                target_line,
                "",
                "Verifier command the host will run after each episode when a Lean workspace exists:",
                shlex.join(build_command),
                "",
                "Tool registry:",
                str(run_dir / "tool_registry.md"),
                "",
                "AMRA math tools report:",
                str(run_dir / "math_tools_report.md"),
                "",
                "Before deep proof search, use these tools for initial verification when they can cheaply test a route, find a counterexample, or validate a theorem shape.",
                "",
                "Required durable artifacts to maintain when relevant:",
                "- proof_notes.md",
                "- lemma_backlog.md",
                "- blockers.md",
                "- experiments.jsonl",
                "- lean_probe_log.md",
                "- verified_lean_declarations.md",
                "- source_notes.md",
                "- proof_package.md",
                "- formalizer_handoff.md",
                "",
                "First episode action: update proof_notes.md and lemma_backlog.md before running any broad search.",
                "",
                "Theorem statement:",
                "",
                statement.strip(),
                "",
                "At the end of this episode, include these plain-text lines in your final response:",
                "STATUS: verified|proved_candidate|partial|blocked|counterexample_suspected|failed",
                "NEXT: continue|stop|needs-human",
                "CHANGED: <files or artifacts changed>",
                "BLOCKER: <current first blocker, or none>",
            ]
        )

    def _episode_cwd(self, *, run_dir: Path, workspace: Path | None) -> Path:
        if workspace is None:
            return run_dir
        try:
            common = Path(os.path.commonpath([str(run_dir), str(workspace)]))
        except ValueError:
            return self.repo_root
        return common if common.exists() and common.is_dir() else self.repo_root

    def _observe_episode(
        self,
        *,
        run_dir: Path,
        workspace: Path | None,
        build_command: list[str],
        build_timeout_sec: int,
        target_name: str,
        tool_snapshot: dict[str, Any],
    ) -> EpisodeObserver:
        def observe(episode: int, episode_dir: Path, last_message: str, backend_report: dict[str, Any]) -> dict[str, Any]:
            del episode_dir
            return self._observe_state(
                episode=episode,
                run_dir=run_dir,
                workspace=workspace,
                build_command=build_command,
                build_timeout_sec=build_timeout_sec,
                target_name=target_name,
                last_message=last_message,
                backend_report=backend_report,
                tool_snapshot=tool_snapshot,
            )

        return observe

    def _observe_state(
        self,
        *,
        episode: int,
        run_dir: Path,
        workspace: Path | None,
        build_command: list[str],
        build_timeout_sec: int,
        target_name: str,
        last_message: str,
        backend_report: dict[str, Any],
        tool_snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        tracker = ProofArtifactTracker(run_dir)
        artifacts = tracker.snapshot(workspace=workspace)
        build_report: dict[str, Any] | None = None
        counts = {"sorry": 0, "axiom": 0, "admit": 0, "constant_or_opaque": 0}
        target_exists: bool | None = None
        if workspace is not None:
            build_report = _run_command(build_command, cwd=workspace, timeout_sec=build_timeout_sec)
            counts = {
                "sorry": _count_lean_pattern(workspace, LeanFromNaturalProofAgent.SORRY_PATTERN),
                "axiom": _count_lean_pattern(workspace, LeanFromNaturalProofAgent.AXIOM_PATTERN),
                "admit": _count_lean_pattern(workspace, LeanFromNaturalProofAgent.ADMIT_PATTERN),
                "constant_or_opaque": _count_lean_pattern(workspace, LeanFromNaturalProofAgent.CONSTANT_PATTERN),
            }
            target_exists = _lean_target_exists(workspace, target_name) if target_name else None
        forbidden_total = sum(counts.values())
        status = _extract_status(last_message, fallback="partial")
        backend_status = str(backend_report.get("status") or "")
        if backend_status == "policy_violation" or (run_dir / "external_source_policy_violation.md").exists():
            status = "failed"
        elif (
            workspace is not None
            and target_name
            and build_report is not None
            and build_report["status"] == "passed"
            and forbidden_total == 0
            and target_exists is True
        ):
            status = "verified"
        elif backend_status in {"skipped", "unsupported", "unavailable"}:
            status = "blocked"
        elif (run_dir / "counterexample_report.md").exists():
            status = "counterexample_suspected"
        elif (
            status == "partial"
            and (run_dir / "proof_package.md").exists()
            and (run_dir / "formalizer_handoff.md").exists()
            and not (run_dir / "blockers.md").exists()
        ):
            status = "proved_candidate"

        terminal = status in self.TERMINAL_STATUSES
        if status == "blocked":
            terminal = backend_status in {"skipped", "unsupported", "unavailable"} or _extract_next(last_message) in {
                "needs_human",
                "stop",
            }
        directive = self._next_directive(
            status=status,
            artifacts=artifacts,
            build_report=build_report,
            target_name=target_name,
            target_exists=target_exists,
        )
        state_payload = {
            "status": status,
            "episode": episode,
            "target_name": target_name,
            "target_exists": target_exists,
            "artifacts": artifacts,
            "latest_directive": directive,
        }
        tracker.write_state(state_payload)
        return {
            "episode": episode,
            "generated_at": utc_now_iso(),
            "status": status,
            "terminal": terminal,
            "stop_reason": f"{status}_reported" if terminal else "",
            "backend_status": backend_status,
            "tool_snapshot": tool_snapshot,
            "artifacts": artifacts,
            "build": build_report,
            "counts": counts,
            "target_name": target_name,
            "target_exists": target_exists,
            "next_episode_directive": directive,
            "last_message_tail": _tail(last_message, 4000),
        }

    def _next_directive(
        self,
        *,
        status: str,
        artifacts: dict[str, Any],
        build_report: dict[str, Any] | None,
        target_name: str,
        target_exists: bool | None,
    ) -> str:
        if status in self.TERMINAL_STATUSES:
            return ""
        run_artifacts = artifacts.get("run_artifacts", {})
        notes_size = int(run_artifacts.get("proof_notes.md", {}).get("size", 0) or 0)
        backlog_size = int(run_artifacts.get("lemma_backlog.md", {}).get("size", 0) or 0)
        if notes_size <= len(ProofArtifactTracker.BOOTSTRAP_FILES["proof_notes.md"]) and backlog_size <= len(
            ProofArtifactTracker.BOOTSTRAP_FILES["lemma_backlog.md"]
        ):
            return (
                "Start by writing proof_notes.md and lemma_backlog.md, then run one cheap Lean/Python/Z3 probe "
                "to test the most fragile idea."
            )
        if build_report is not None and build_report.get("status") == "failed":
            return "Lean build is failing. Use a small Lean probe or direct build diagnostics to repair definitions before broad search."
        if target_name and target_exists is False:
            return "The target Lean declaration is not present. Either create a precise target theorem or explain why a smaller lemma is the next target."
        return "Continue the unified loop: refine one lemma, test it with a tool, and record the result in durable artifacts."


__all__ = [
    "CodexEpisodeConfig",
    "CodexEpisodeLoopAgent",
    "EpisodeObserver",
    "NaturalLanguageTheoremProverAgent",
    "LeanFromNaturalProofAgent",
    "UnifiedProofAgentLoop",
    "_extract_lean_target_name",
]
