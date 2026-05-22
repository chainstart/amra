from __future__ import annotations

import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from amra.agents.source_policy import apply_codex_source_policy, mark_policy_violation, source_policy_prompt
from amra.core.workspace import read_text, write_json, write_text
from amra.infra.runtime import env_float, env_int, env_str, run_guarded_command, wait_for_system_headroom
from amra.proof.lab import parse_labeled_fields


SUPERVISOR_LABELS: tuple[str, ...] = (
    "Supervisor decision",
    "Reason",
    "Next target",
    "Formalization target",
    "Instructions",
    "Route risk",
)

VALID_SUPERVISOR_DECISIONS = {
    "continue_current_target",
    "switch_target",
    "return_to_proof_lab",
    "freeze_route",
    "final_target",
}

LEAN_DECL_PATTERN = re.compile(
    r"(?m)^\s*(?:noncomputable\s+)?(?:theorem|lemma)\s+"
    r"([A-Za-z_][A-Za-z0-9_'.]*|«[^»]+»)(?=\s|:|\(|\{|\[|$)"
)
LEAN_FENCE_PATTERN = re.compile(r"```(?:lean|lean4)?\s*\n(.*?)```", re.IGNORECASE | re.DOTALL)
BACKTICK_NAME_PATTERN = re.compile(r"`([A-Za-z_][A-Za-z0-9_'.]*)`")

LEAN_STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "by",
    "def",
    "do",
    "else",
    "end",
    "example",
    "for",
    "from",
    "have",
    "if",
    "in",
    "is",
    "lemma",
    "let",
    "match",
    "namespace",
    "of",
    "on",
    "or",
    "proof",
    "route",
    "show",
    "structure",
    "the",
    "then",
    "theorem",
    "to",
    "using",
    "via",
    "where",
    "with",
}


def _strip_escaped_identifier(name: str) -> str:
    stripped = name.strip()
    if stripped.startswith("«") and stripped.endswith("»"):
        return stripped[1:-1].strip()
    return stripped


def _valid_lean_name(name: str, *, excluded_names: set[str] | None = None) -> str:
    normalized = _strip_escaped_identifier(name)
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_'.]*", normalized):
        return ""
    if normalized.lower() in LEAN_STOPWORDS:
        return ""
    if excluded_names and normalized in excluded_names:
        return ""
    return normalized


def _extract_decl_name(text: str, *, excluded_names: set[str] | None = None) -> str:
    for fence in LEAN_FENCE_PATTERN.finditer(text):
        for match in LEAN_DECL_PATTERN.finditer(fence.group(1)):
            name = _valid_lean_name(match.group(1), excluded_names=excluded_names)
            if name:
                return name
    for match in LEAN_DECL_PATTERN.finditer(text):
        name = _valid_lean_name(match.group(1), excluded_names=excluded_names)
        if name:
            return name
    return ""


def _extract_backtick_name(text: str, *, excluded_names: set[str] | None = None) -> str:
    for match in BACKTICK_NAME_PATTERN.finditer(text):
        name = _valid_lean_name(match.group(1), excluded_names=excluded_names)
        if name:
            return name
    return ""


def extract_supervisor_target(fields: dict[str, str], *, excluded_names: set[str] | None = None) -> str:
    """Extract the next theorem name from a structured supervisor answer."""

    for key in ("formalization_target", "next_target"):
        value = fields.get(key, "")
        target = _extract_decl_name(value, excluded_names=excluded_names)
        if target:
            return target
    for key in ("next_target", "formalization_target"):
        value = fields.get(key, "")
        target = _extract_backtick_name(value, excluded_names=excluded_names)
        if target:
            return target
    return ""


def parse_supervisor_decision(text: str, *, excluded_names: set[str] | None = None) -> dict[str, Any]:
    fields = parse_labeled_fields(text, SUPERVISOR_LABELS)
    raw_decision = fields.get("supervisor_decision", "")
    decision = raw_decision.strip().lower().replace("-", "_").replace(" ", "_")
    decision = re.sub(r"[^a-z0-9_]+", "", decision)
    if decision not in VALID_SUPERVISOR_DECISIONS:
        decision = "continue_current_target"
    route_risk = fields.get("route_risk", "").strip().lower()
    if route_risk not in {"low", "medium", "high"}:
        route_risk = ""
    return {
        "decision": decision,
        "target_theorem": extract_supervisor_target(fields, excluded_names=excluded_names),
        "reason": fields.get("reason", "").strip(),
        "instructions": fields.get("instructions", "").strip(),
        "route_risk": route_risk,
        "parsed_fields": fields,
    }


class GlobalProofSupervisor:
    """Read-only global route reviewer for long proof campaigns."""

    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.backend_max_memory_mb = env_int("ARA_GLOBAL_SUPERVISOR_BACKEND_MAX_MEMORY_MB", 8192)
        self.backend_max_cpu_seconds = env_int("ARA_GLOBAL_SUPERVISOR_BACKEND_MAX_CPU_SECONDS", 1200)
        self.backend_max_processes = env_int("ARA_GLOBAL_SUPERVISOR_BACKEND_MAX_PROCESSES", 4096)
        self.backend_niceness = env_int("ARA_GLOBAL_SUPERVISOR_BACKEND_NICENESS", 10)
        self.backend_model = env_str("ARA_GLOBAL_SUPERVISOR_MODEL", env_str("ARA_MATH_BACKEND_MODEL", ""))
        self.backend_reasoning_effort = env_str(
            "ARA_GLOBAL_SUPERVISOR_REASONING_EFFORT",
            env_str("ARA_MATH_BACKEND_REASONING_EFFORT", "high"),
        )
        self.min_available_memory_mb = env_int("ARA_MATH_MIN_AVAILABLE_MEMORY_MB", 2048)
        self.max_load_per_cpu = env_float("ARA_MATH_MAX_LOAD_PER_CPU", 1.5)
        self.wait_max_seconds = env_int("ARA_MATH_SYSTEM_WAIT_SECONDS", 30)
        self.wait_poll_seconds = env_int("ARA_MATH_SYSTEM_WAIT_POLL_SECONDS", 5)

    def _read_context_bundle(self, context_paths: list[Path], *, max_chars_each: int = 12000) -> str:
        if not context_paths:
            return "No external context files supplied.\n"
        chunks: list[str] = []
        for path in context_paths:
            resolved = path.expanduser().resolve()
            if not resolved.exists():
                chunks.extend([f"## Context File: {resolved}", "", "- Missing", ""])
                continue
            text = read_text(resolved)
            truncated = len(text) > max_chars_each
            if truncated:
                text = text[-max_chars_each:]
            chunks.extend(
                [
                    f"## Context File: {resolved}",
                    "",
                    f"- Truncated to tail: {truncated}",
                    "",
                    "```text",
                    text.strip() or "<empty>",
                    "```",
                    "",
                ]
            )
        return "\n".join(chunks).rstrip() + "\n"

    def _read_workspace_outline(self, workspace: Path | None, target_file: Path | None) -> str:
        if workspace is None:
            return "No Lean workspace supplied.\n"
        resolved_workspace = workspace.expanduser().resolve()
        if not resolved_workspace.exists():
            return f"Lean workspace is missing: {resolved_workspace}\n"
        candidate_files: list[Path] = []
        if target_file is not None:
            explicit = target_file if target_file.is_absolute() else resolved_workspace / target_file
            candidate_files.append(explicit)
        candidate_files.extend(sorted(resolved_workspace.rglob("*.lean"))[:20])
        seen: set[Path] = set()
        chunks: list[str] = []
        for path in candidate_files:
            try:
                resolved = path.expanduser().resolve()
            except OSError:
                continue
            if resolved in seen or not resolved.exists() or not resolved.is_file():
                continue
            seen.add(resolved)
            text = resolved.read_text(encoding="utf-8", errors="ignore")
            declarations = [
                line.strip()
                for line in text.splitlines()
                if re.match(r"^\s*(?:noncomputable\s+)?(?:theorem|lemma|def|instance)\s+", line)
            ][:80]
            tail = text[-8000:]
            rel = resolved.relative_to(resolved_workspace) if resolved.is_relative_to(resolved_workspace) else resolved
            chunks.extend(
                [
                    f"## Lean File: {rel}",
                    "",
                    "### Declaration Outline",
                    "",
                    "\n".join(f"- {item}" for item in declarations) or "- none",
                    "",
                    "### Tail",
                    "",
                    "```lean",
                    tail.strip() or "<empty>",
                    "```",
                    "",
                ]
            )
        return "\n".join(chunks).rstrip() + "\n" if chunks else "No Lean files found in workspace.\n"

    def _round_trace(self, round_entries: list[dict[str, Any]], *, max_entries: int = 8) -> str:
        if not round_entries:
            return "- no completed rounds yet\n"
        lines: list[str] = []
        for entry in round_entries[-max_entries:]:
            lines.extend(
                [
                    f"## Round {entry.get('round')} `{entry.get('stage')}`",
                    "",
                    f"- Status: `{entry.get('status')}`",
                    f"- Stop reason: `{entry.get('stop_reason')}`",
                    f"- Target theorem: `{entry.get('target_theorem') or entry.get('suggested_target_theorem') or ''}`",
                    f"- Verified: `{entry.get('verified')}`",
                    f"- Attempts completed: `{entry.get('attempts_completed')}`",
                    f"- Needs global reassessment: `{entry.get('needs_global_reassessment')}`",
                    f"- Next action: {entry.get('next_action') or ''}",
                ]
            )
            summary_path_text = str(entry.get("summary_path") or "")
            summary_path = Path(summary_path_text) if summary_path_text else None
            if summary_path is not None and summary_path.exists():
                lines.extend(["", "### Summary Tail", "", "```text", read_text(summary_path)[-4000:].strip(), "```"])
            assessment_path_text = str(entry.get("global_assessment_path") or "")
            assessment_path = Path(assessment_path_text) if assessment_path_text else None
            if assessment_path is not None and assessment_path.exists():
                lines.extend(["", "### Global Assessment Tail", "", "```text", read_text(assessment_path)[-4000:].strip(), "```"])
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    def _build_prompt(
        self,
        *,
        statement: str,
        round_number: int,
        current_target_theorem: str,
        final_target_theorem: str,
        completed_target_theorems: set[str],
        latest_entry: dict[str, Any],
        round_entries: list[dict[str, Any]],
        context_paths: list[Path],
        workspace: Path | None,
        target_file: Path | None,
        trigger_reason: str,
    ) -> str:
        return "\n".join(
            [
                "# AMRA Global Proof Supervisor",
                "",
                "You are the outer strategy reviewer for a long Lean formalization campaign.",
                "Do not edit files. Read the global state and decide the next theorem-level move.",
                "",
                "## Required Output Format",
                "",
                "Return exactly these labeled fields:",
                "",
                "- Supervisor decision: continue_current_target | switch_target | return_to_proof_lab | freeze_route | final_target",
                "- Reason: one concise paragraph explaining the strategic basis",
                "- Next target: a Lean theorem/lemma name in backticks, or `<none>`",
                "- Formalization target: a fenced Lean theorem/lemma declaration when switching targets, or `<unchanged>`",
                "- Instructions: concrete next-round instructions for the formalizer or proof-lab",
                "- Route risk: low | medium | high",
                "",
                "## Decision Semantics",
                "",
                "- continue_current_target: keep the current target and give better instructions.",
                "- switch_target: replace the current target with a smaller or better theorem-level target that directly advances the final proof.",
                "- return_to_proof_lab: the current route is underspecified; run mathematical route discovery before more Lean editing.",
                "- freeze_route: the current route is likely wrong or exhausted; force route re-selection.",
                "- final_target: the final theorem itself is the correct immediate target.",
                "",
                "## Trigger",
                "",
                trigger_reason.strip() or "manual supervision",
                "",
                "## Main Objective",
                "",
                statement.strip(),
                "",
                "## Current State",
                "",
                f"- Supervisor round: `{round_number}`",
                f"- Current stage theorem: `{current_target_theorem or '<none>'}`",
                f"- Final theorem: `{final_target_theorem or '<not fixed>'}`",
                f"- Completed theorem targets: `{', '.join(sorted(completed_target_theorems)) or '<none>'}`",
                "",
                "## Latest Round Entry",
                "",
                "```json",
                _compact_json(latest_entry),
                "```",
                "",
                "## Round Trace",
                "",
                self._round_trace(round_entries),
                "",
                "## Context Bundle",
                "",
                self._read_context_bundle(context_paths),
                "",
                "## Lean Workspace Outline",
                "",
                self._read_workspace_outline(workspace, target_file),
                "",
                "## Strategy Rules",
                "",
                "- Do not reward progress that only cleans local syntax while leaving the main target structurally unchanged.",
                "- If the current target is absent, too broad, or repeatedly unaffected, switch to the first missing theorem-level blocker.",
                "- Prefer a target already represented in the Lean file when the formalizer is close to closing it.",
                "- The replacement target must be a theorem/lemma name, not prose.",
                "- Do not choose a completed target.",
                "- Keep the target close enough that one formalizer round can plausibly make measurable progress.",
                "",
            ]
        )

    def _redacted_command(self, command: list[str]) -> list[str]:
        redacted: list[str] = []
        skip_next = False
        for item in command:
            if skip_next:
                redacted.append("<omitted>")
                skip_next = False
                continue
            redacted.append(item)
            if item == "--output-last-message":
                skip_next = True
        return redacted

    def _invoke_backend(
        self,
        *,
        backend: str,
        prompt: str,
        run_dir: Path,
        output_path: Path,
        timeout_sec: int,
        enable_search: bool,
    ) -> dict[str, Any]:
        prompt = source_policy_prompt(enable_search=enable_search) + "\n\n" + prompt
        if backend == "none":
            write_text(
                output_path,
                "\n".join(
                    [
                        "Supervisor decision: continue_current_target",
                        "Reason: backend disabled; keep the existing campaign decision.",
                        "Next target: <none>",
                        "Formalization target: <unchanged>",
                        "Instructions: rerun with --supervisor-backend codex for global strategy review.",
                        "Route risk: medium",
                        "",
                    ]
                ),
            )
            return {"backend": backend, "status": "skipped", "returncode": 0, "elapsed_seconds": 0.0, "command": []}

        backend_bin = shutil.which(backend)
        if not backend_bin:
            write_text(output_path, f"Supervisor decision: continue_current_target\nReason: Backend `{backend}` is not available.\n")
            return {"backend": backend, "status": "unavailable", "returncode": None, "elapsed_seconds": 0.0, "command": []}
        if backend != "codex":
            write_text(output_path, f"Supervisor decision: continue_current_target\nReason: Backend `{backend}` is not implemented.\n")
            return {"backend": backend, "status": "unsupported", "returncode": None, "elapsed_seconds": 0.0, "command": []}

        command = [backend_bin, "-s", "read-only", "-a", "never"]
        apply_codex_source_policy(command, enable_search=enable_search)
        if self.backend_model:
            command.extend(["-m", self.backend_model])
        if self.backend_reasoning_effort:
            command.extend(["-c", f'model_reasoning_effort="{self.backend_reasoning_effort}"'])
        resolved_run_dir = run_dir.resolve()
        resolved_output_path = output_path.resolve()
        command.extend(["exec", "-C", str(resolved_run_dir), "--output-last-message", str(resolved_output_path), "-"])

        wait_for_system_headroom(
            min_available_memory_mb=self.min_available_memory_mb,
            max_load_per_cpu=self.max_load_per_cpu,
            max_wait_seconds=self.wait_max_seconds,
            poll_seconds=self.wait_poll_seconds,
        )
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
                input_text=prompt,
            )
        except subprocess.TimeoutExpired as exc:
            if not output_path.exists():
                write_text(output_path, "Supervisor decision: continue_current_target\nReason: supervisor timed out.\n")
            stdout = str(exc.stdout or exc.output or "")
            stderr = str(exc.stderr or "")
            return mark_policy_violation(
                report={
                    "backend": backend,
                    "status": "timeout",
                    "returncode": None,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "command": self._redacted_command(command),
                    "stdout_tail": stdout[-4000:],
                    "stderr_tail": stderr[-4000:],
                },
                output_path=output_path,
                stdout=stdout,
                stderr=stderr,
                enable_search=enable_search,
            )

        return mark_policy_violation(
            report={
                "backend": backend,
                "status": "completed" if completed.returncode == 0 else "failed",
                "returncode": completed.returncode,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "command": self._redacted_command(command),
                "stdout_tail": completed.stdout[-4000:],
                "stderr_tail": completed.stderr[-4000:],
            },
            output_path=output_path,
            stdout=completed.stdout,
            stderr=completed.stderr,
            enable_search=enable_search,
        )

    def run(
        self,
        *,
        run_dir: Path,
        statement: str,
        round_number: int,
        current_target_theorem: str,
        final_target_theorem: str,
        completed_target_theorems: set[str],
        latest_entry: dict[str, Any],
        round_entries: list[dict[str, Any]],
        context_paths: list[Path] | None = None,
        workspace: Path | None = None,
        target_file: Path | None = None,
        trigger_reason: str = "",
        backend: str = "codex",
        timeout_sec: int = 900,
        enable_search: bool = True,
    ) -> dict[str, Any]:
        supervisor_dir = run_dir / "supervisor" / f"round-{round_number:03d}"
        supervisor_dir.mkdir(parents=True, exist_ok=True)
        prompt_path = supervisor_dir / "prompt.md"
        output_path = supervisor_dir / "decision.md"
        decision_path = supervisor_dir / "decision.json"
        prompt = self._build_prompt(
            statement=statement,
            round_number=round_number,
            current_target_theorem=current_target_theorem,
            final_target_theorem=final_target_theorem,
            completed_target_theorems=completed_target_theorems,
            latest_entry=latest_entry,
            round_entries=round_entries,
            context_paths=list(context_paths or []),
            workspace=workspace,
            target_file=target_file,
            trigger_reason=trigger_reason,
        )
        write_text(prompt_path, prompt)
        invocation = self._invoke_backend(
            backend=backend,
            prompt=prompt,
            run_dir=supervisor_dir,
            output_path=output_path,
            timeout_sec=max(1, timeout_sec),
            enable_search=enable_search,
        )
        text = read_text(output_path)
        parsed = parse_supervisor_decision(text, excluded_names=completed_target_theorems)
        payload = {
            "round": round_number,
            "trigger_reason": trigger_reason,
            "prompt_path": str(prompt_path),
            "decision_path": str(output_path),
            "parsed_decision_path": str(decision_path),
            "backend_invocation": invocation,
            **parsed,
        }
        write_json(decision_path, payload)
        return payload


def _compact_json(payload: dict[str, Any]) -> str:
    import json

    return json.dumps(payload, indent=2, ensure_ascii=False, default=str)
