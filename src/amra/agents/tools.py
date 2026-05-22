from __future__ import annotations

import importlib.util
import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from amra.math_tools import ensure_math_tools, selected_tool_specs
from amra.agents.env import (
    AMRA_AGENT_RUN_DIR_ENV,
    AMRA_AGENT_WORKSPACE_ENV,
    LEGACY_AGENT_RUN_DIR_ENV,
    LEGACY_AGENT_WORKSPACE_ENV,
    agent_environment,
)


@dataclass(frozen=True)
class ToolSpec:
    name: str
    purpose: str
    when_to_use: str
    command_templates: list[str]
    artifact_contract: str
    notes: list[str]


class ToolRegistry:
    """Describes the proof agent's available environment actions.

    The unified proof loop deliberately keeps the LLM in charge of deciding and
    executing actions. The registry is a durable contract: it names the expected
    tools, gives command recipes, and tells the agent where to persist evidence.
    """

    PYTHON_MODULES = ("sympy", "numpy", "scipy", "networkx", "z3", "mpmath", "requests")
    EXECUTABLES = ("codex", "lean", "lake", "python3", "rg", "git", "curl", "wget", "z3")

    def __init__(
        self,
        *,
        build_command: list[str] | None = None,
        math_tools_profile: str = "full",
        install_missing_math_tools: bool | None = None,
    ) -> None:
        self.build_command = build_command or ["lake", "build"]
        self.math_tools_profile = math_tools_profile
        self.install_missing_math_tools = install_missing_math_tools
        self.tools = self._default_tools()

    def _default_tools(self) -> list[ToolSpec]:
        build_command = " ".join(self.build_command)
        run_dir = f"${AMRA_AGENT_RUN_DIR_ENV}"
        workspace = f"${AMRA_AGENT_WORKSPACE_ENV}"
        return [
            ToolSpec(
                name="lean_quick_check",
                purpose="Check a small Lean definition, theorem statement, or local lemma before committing to a route.",
                when_to_use="Use during proof exploration whenever a definition, boundary case, or lemma shape might fail in Lean.",
                command_templates=[
                    f"mkdir -p \"{run_dir}/lean_probes\"",
                    f"cd \"{workspace}\" && lake env lean \"{run_dir}/lean_probes/<probe>.lean\"",
                ],
                artifact_contract=(
                    "Store every probe as lean_probes/<probe>.lean and append the command result to lean_probe_log.md."
                ),
                notes=[
                    "Prefer tiny probes that import MathProject or Mathlib and test one idea.",
                    "A failed probe is useful evidence; record the error and the mathematical lesson.",
                ],
            ),
            ToolSpec(
                name="lean_build",
                purpose="Run the verifier on the current Lean workspace.",
                when_to_use="Use after editing Lean files or before claiming a formal checkpoint.",
                command_templates=[f"cd \"{workspace}\" && {build_command}"],
                artifact_contract="Record build command, exit status, and relevant diagnostics in lean_probe_log.md or proof_notes.md.",
                notes=[
                    "Final verification still comes from the host observer.",
                    "Do not treat a build with sorry/admit/axiom/constant/opaque as complete.",
                ],
            ),
            ToolSpec(
                name="mathlib_search",
                purpose="Find existing Lean declarations and examples in the local mathlib checkout.",
                when_to_use="Use before re-proving a standard algebra, order, number theory, graph, or finite-set lemma.",
                command_templates=[
                    "rg -n \"<keyword>\" .lake/packages/mathlib/Mathlib",
                    "rg -n \"theorem .*<name>|lemma .*<name>\" .lake/packages/mathlib/Mathlib",
                ],
                artifact_contract="Copy declaration names and source paths into proof_notes.md or lemma_backlog.md.",
                notes=[
                    "Use local search first; web search is optional and should not replace exact Lean names.",
                ],
            ),
            ToolSpec(
                name="python_explore",
                purpose="Run finite searches, sanity checks, symbolic computations, or small counterexample probes.",
                when_to_use="Use for combinatorics, inequalities, recurrences, graph checks, and example generation.",
                command_templates=[
                    f"mkdir -p \"{run_dir}/experiments\"",
                    f"python3 \"{run_dir}/experiments/<experiment>.py\"",
                ],
                artifact_contract=(
                    "Store scripts under experiments/ and append JSONL-style summaries to experiments.jsonl."
                ),
                notes=[
                    "Make experiments deterministic and include parameters, seed, and conclusion.",
                    "A computation is evidence for route selection, not a proof unless separately certified.",
                ],
            ),
            ToolSpec(
                name="z3_check",
                purpose="Check finite logical constraints or search for countermodels.",
                when_to_use="Use for bounded arithmetic, incidence, graph, or ordering constraints.",
                command_templates=[
                    "python3 - <<'PY'\nfrom z3 import *\n# bounded model check here\nPY",
                ],
                artifact_contract="Record model, unsat core if available, and translation assumptions in experiments.jsonl.",
                notes=[
                    "Keep the mathematical encoding explicit; hidden encoding choices are common failure points.",
                ],
            ),
            ToolSpec(
                name="cas_and_smt_tools",
                purpose="Use installed AMRA math tools such as SymPy, NumPy/SciPy, Z3, PARI/GP, GAP, Singular, Maxima, SageMath, or cvc5 when available in the selected profile.",
                when_to_use="Use before long proof search whenever a finite computation, CAS simplification, modular check, SMT model, or counterexample probe can validate or falsify the route cheaply.",
                command_templates=[
                    f"cat \"{run_dir}/math_tools_report.md\"",
                    f"python3 \"{run_dir}/experiments/<experiment>.py\"",
                    "z3 <problem>.smt2",
                    "gp -q <script.gp>",
                    "gap -q <script.g>",
                    "Singular -q <script.sing>",
                    "sage <script.sage>",
                ],
                artifact_contract="Record commands, parameters, outputs, and interpretation in experiments.jsonl or proof_notes.md.",
                notes=[
                    "The selected tools are installed/checked before the agent starts; see math_tools_report.md.",
                    "External computation is evidence until checked by Lean or turned into a verifiable certificate.",
                ],
            ),
            ToolSpec(
                name="literature_search",
                purpose="Find source statements, known results, and related papers.",
                when_to_use="Use when the problem may depend on an external theorem, known olympiad solution, or paper.",
                command_templates=[
                    "rg -n \"<keyword>\" artifacts projects ara_library data",
                    "python3 run.py harvest-literature --project <project> --allow-network",
                ],
                artifact_contract="Record sources, theorem statements, and assumptions in source_notes.md.",
                notes=[
                    "For standalone IMO runs, prefer local artifacts first unless --search is enabled.",
                    "Do not import a literature claim into the proof without its exact assumptions.",
                ],
            ),
            ToolSpec(
                name="proof_memory_search",
                purpose="Retrieve previous blockers, failed routes, partial lemmas, and formalization handoffs.",
                when_to_use="Use before restarting a route or when a host observation mentions a blocker.",
                command_templates=[
                    f"rg -n \"<keyword>\" \"{run_dir}\" artifacts projects",
                    "find artifacts -name 'blocker.md' -o -name 'partial_lemmas.md' -o -name 'failed_routes.md'",
                ],
                artifact_contract="Cite reused memory paths in proof_notes.md and update blockers.md if the same blocker remains.",
                notes=[
                    "Reuse precise failed-route information instead of rediscovering it.",
                ],
            ),
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "build_command": self.build_command,
            "math_tools_profile": self.math_tools_profile,
            "install_missing_math_tools": self.install_missing_math_tools,
            "environment_variables": {
                "run_dir": AMRA_AGENT_RUN_DIR_ENV,
                "workspace": AMRA_AGENT_WORKSPACE_ENV,
                "legacy_run_dir": LEGACY_AGENT_RUN_DIR_ENV,
                "legacy_workspace": LEGACY_AGENT_WORKSPACE_ENV,
            },
            "math_tool_specs": [spec.to_dict() for spec in selected_tool_specs(self.math_tools_profile)],
            "tools": [asdict(tool) for tool in self.tools],
        }

    def to_markdown(self) -> str:
        lines = ["# Proof Agent Tool Registry", ""]
        lines.extend(
            [
                "The agent decides which tool to use and executes commands directly inside its Codex episode.",
                "Every nontrivial tool call should leave a durable artifact in the run directory.",
                f"The canonical runtime variables are `${AMRA_AGENT_RUN_DIR_ENV}` and `${AMRA_AGENT_WORKSPACE_ENV}`; legacy ARA aliases remain available for old prompts.",
                "Math tool availability, auto-install results, and smoke checks are recorded in `math_tools_report.md`.",
                "",
            ]
        )
        for tool in self.tools:
            lines.extend(
                [
                    f"## {tool.name}",
                    "",
                    f"- Purpose: {tool.purpose}",
                    f"- Use when: {tool.when_to_use}",
                    f"- Artifact contract: {tool.artifact_contract}",
                    "- Command templates:",
                    *(f"  - `{template}`" for template in tool.command_templates),
                    "- Notes:",
                    *(f"  - {note}" for note in tool.notes),
                    "",
                ]
            )
        return "\n".join(lines).rstrip() + "\n"

    def environment_snapshot(self, *, workspace: Path | None = None) -> dict[str, Any]:
        executables = {
            name: {
                "available": shutil.which(name) is not None,
                "path": shutil.which(name) or "",
            }
            for name in self.EXECUTABLES
        }
        python_modules = {
            name: importlib.util.find_spec(name) is not None
            for name in self.PYTHON_MODULES
        }
        workspace_payload: dict[str, Any] = {}
        if workspace is not None:
            workspace_payload = {
                "path": str(workspace),
                "exists": workspace.exists(),
                "lakefile_exists": (workspace / "lakefile.lean").exists(),
                "toolchain": (workspace / "lean-toolchain").read_text(encoding="utf-8").strip()
                if (workspace / "lean-toolchain").exists()
                else "",
            }
        return {
            "executables": executables,
            "python_modules": python_modules,
            "workspace": workspace_payload,
            "registry_tool_count": len(self.tools),
            "environment_variables": {
                "run_dir": AMRA_AGENT_RUN_DIR_ENV,
                "workspace": AMRA_AGENT_WORKSPACE_ENV,
                "legacy_run_dir": LEGACY_AGENT_RUN_DIR_ENV,
                "legacy_workspace": LEGACY_AGENT_WORKSPACE_ENV,
            },
        }

    def write_artifacts(
        self,
        run_dir: Path,
        *,
        workspace: Path | None = None,
        install_missing_math_tools: bool | None = None,
        math_tools_profile: str | None = None,
        run_math_tool_smoke: bool | None = None,
    ) -> dict[str, Any]:
        run_dir.mkdir(parents=True, exist_ok=True)
        registry_payload = self.to_dict()
        math_tools_report = ensure_math_tools(
            output_dir=run_dir,
            profile=math_tools_profile or self.math_tools_profile,
            install_missing=(
                self.install_missing_math_tools
                if install_missing_math_tools is None
                else install_missing_math_tools
            ),
            run_smoke=run_math_tool_smoke,
            workspace=workspace,
        )
        snapshot = self.environment_snapshot(workspace=workspace)
        (run_dir / "tool_registry.json").write_text(
            json.dumps(
                {"registry": registry_payload, "environment": snapshot, "math_tools": math_tools_report},
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        (run_dir / "tool_registry.md").write_text(self.to_markdown(), encoding="utf-8")
        snapshot["math_tools"] = {
            "profile": math_tools_report.get("profile"),
            "report_path": math_tools_report.get("report_path"),
            "summary_path": math_tools_report.get("summary_path"),
            "available_tool_ids": math_tools_report.get("available_tool_ids", []),
            "unavailable_tool_ids": math_tools_report.get("unavailable_tool_ids", []),
            "all_selected_available": math_tools_report.get("all_selected_available"),
        }
        return snapshot


__all__ = [
    "AMRA_AGENT_RUN_DIR_ENV",
    "AMRA_AGENT_WORKSPACE_ENV",
    "LEGACY_AGENT_RUN_DIR_ENV",
    "LEGACY_AGENT_WORKSPACE_ENV",
    "ToolSpec",
    "ToolRegistry",
    "agent_environment",
]
