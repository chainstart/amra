from __future__ import annotations

import json
import re
import shlex
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from amra.lean.contract import (
    compare_lean_declaration_headers,
    extract_lean_declaration_header,
    normalize_lean_declaration_header,
    trim_lean_proof_from_header,
)
from amra.agents.episode_loop import CodexEpisodeConfig, CodexEpisodeLoopAgent, EpisodeObserver
from amra.portfolio_scheduler import PortfolioAttackScheduler, calculate_progress_velocity
from amra.core.workspace import slugify, utc_now_iso


DECL_RE = re.compile(r"^\s*(theorem|lemma)\s+(`[^`]+`|[A-Za-z_][A-Za-z0-9_'.!?]*)\b")
NAMESPACE_RE = re.compile(r"^\s*namespace\s+(.+?)\s*$")
END_RE = re.compile(r"^\s*end(?:\s+(.+?))?\s*$")
SORRY_RE = re.compile(r"\bsorry\b")
AXIOM_RE = re.compile(r"^\s*axiom\b", re.MULTILINE)
ADMIT_RE = re.compile(r"\badmit\b")
CONSTANT_RE = re.compile(r"^\s*(constant|opaque)\b", re.MULTILINE)


def _resolve(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _read_text(path: Path, *, max_chars: int | None = None) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if max_chars is not None and len(text) > max_chars:
        return text[:max_chars] + "\n[truncated]\n"
    return text


def _tail(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[-limit:]


def _strip_lean_comments(text: str) -> str:
    text = re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)
    return re.sub(r"--.*$", "", text, flags=re.MULTILINE)


def _iter_project_lean_files(workspace: Path) -> list[Path]:
    if not workspace.exists():
        return []
    return sorted(path for path in workspace.rglob("*.lean") if ".lake" not in path.parts)


def _unquote_identifier(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def _target_name_matches(actual: str, target: str) -> bool:
    actual = _unquote_identifier(actual.strip())
    target = _unquote_identifier(target.strip())
    return actual == target or actual.endswith(f".{target}") or target.endswith(f".{actual}")


def _relative_to_workspace(path: Path, workspace: Path) -> str:
    try:
        return str(path.relative_to(workspace))
    except ValueError:
        return str(path)


def _normalize_relative_file(path: Path, workspace: Path) -> str:
    candidate = path.expanduser()
    if candidate.is_absolute():
        return _relative_to_workspace(candidate.resolve(strict=False), workspace)
    return str(candidate)


def _run_command(command: list[str], *, cwd: Path, timeout_sec: int) -> dict[str, Any]:
    if not command:
        return {
            "status": "not_run",
            "returncode": None,
            "elapsed_seconds": 0.0,
            "command": [],
            "stdout_tail": "",
            "stderr_tail": "",
        }
    started = time.monotonic()
    try:
        completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=max(1, timeout_sec))
    except subprocess.TimeoutExpired as exc:
        return {
            "status": "timeout",
            "returncode": None,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "command": command,
            "stdout_tail": _tail(str(exc.stdout or exc.output or ""), 8000),
            "stderr_tail": _tail(str(exc.stderr or ""), 8000),
        }
    return {
        "status": "passed" if completed.returncode == 0 else "failed",
        "returncode": completed.returncode,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "command": command,
        "stdout_tail": _tail(completed.stdout, 8000),
        "stderr_tail": _tail(completed.stderr, 8000),
    }


def _extract_status(text: str, fallback: str = "partial") -> str:
    match = re.search(r"(?im)^\s*STATUS\s*:\s*([a-zA-Z_ -]+)\s*$", text)
    if not match:
        return fallback
    return match.group(1).strip().lower().replace("-", "_").replace(" ", "_")


def _header_from_lines(lines: list[str], start: int) -> str:
    header_lines: list[str] = []
    for current in lines[start : start + 80]:
        if header_lines and DECL_RE.match(current):
            break
        if header_lines and not current.strip():
            break
        header_lines.append(current.rstrip())
        if ":=" in current:
            break
    return trim_lean_proof_from_header("\n".join(header_lines))


def _declaration_key(declaration: dict[str, Any]) -> tuple[str, str]:
    name = str(declaration.get("full_name") or declaration.get("name") or "")
    header = normalize_lean_declaration_header(str(declaration.get("header") or ""))
    return (name, header)


def _collect_declarations(workspace: Path) -> list[dict[str, Any]]:
    declarations: list[dict[str, Any]] = []
    for path in _iter_project_lean_files(workspace):
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        namespace_stack: list[str] = []
        for index, line in enumerate(lines):
            stripped = line.strip()
            namespace_match = NAMESPACE_RE.match(line)
            if namespace_match:
                namespace_stack.extend(part for part in namespace_match.group(1).split(".") if part)
                continue
            end_match = END_RE.match(line)
            if end_match and namespace_stack:
                end_name = (end_match.group(1) or "").strip()
                if end_name and namespace_stack and namespace_stack[-1] == end_name.split(".")[-1]:
                    namespace_stack.pop()
                elif not end_name:
                    namespace_stack.pop()
                continue
            if stripped.startswith("--"):
                continue
            match = DECL_RE.match(line)
            if not match:
                continue
            raw_name = _unquote_identifier(match.group(2))
            full_name = raw_name if "." in raw_name or not namespace_stack else ".".join([*namespace_stack, raw_name])
            declarations.append(
                {
                    "kind": match.group(1),
                    "name": raw_name,
                    "full_name": full_name,
                    "path": str(path),
                    "relative_path": _relative_to_workspace(path, workspace),
                    "line": index + 1,
                    "declaration_line": line.strip(),
                    "header": _header_from_lines(lines, index),
                }
            )
    return declarations


def _target_declaration(workspace: Path, target_name: str) -> dict[str, Any]:
    for declaration in _collect_declarations(workspace):
        if _target_name_matches(str(declaration.get("full_name") or ""), target_name) or _target_name_matches(
            str(declaration.get("name") or ""), target_name
        ):
            return {"found": True, **declaration, "target_name": target_name}
    return {"found": False, "name": target_name, "target_name": target_name, "reason": "target_declaration_not_found"}


def _workspace_snapshot(workspace: Path) -> dict[str, str]:
    return {
        _relative_to_workspace(path, workspace): path.read_text(encoding="utf-8", errors="ignore")
        for path in _iter_project_lean_files(workspace)
    }


def _workspace_changes(before: dict[str, str], after: dict[str, str]) -> list[dict[str, str]]:
    changes: list[dict[str, str]] = []
    for relative_path in sorted(set(before) | set(after)):
        if before.get(relative_path) == after.get(relative_path):
            continue
        if relative_path not in before:
            change_type = "added"
        elif relative_path not in after:
            change_type = "removed"
        else:
            change_type = "modified"
        changes.append({"path": relative_path, "change": change_type})
    return changes


def _count_pattern(workspace: Path, pattern: re.Pattern[str]) -> int:
    total = 0
    for path in _iter_project_lean_files(workspace):
        total += len(pattern.findall(_strip_lean_comments(path.read_text(encoding="utf-8", errors="ignore"))))
    return total


def _looks_conditional_wrapper(header: str) -> bool:
    normalized = normalize_lean_declaration_header(header)
    return bool(re.search(r"(?:->|→)", normalized))


def load_expected_target_headers(paths: list[Path], target_names: list[str]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for path in paths:
        text = path.read_text(encoding="utf-8")
        declaration = extract_lean_declaration_header(text)
        if declaration is None:
            raise ValueError(f"Expected target header file does not contain a theorem/lemma declaration: {path}")
        declared_name = str(declaration.get("name") or "")
        matches = [target for target in target_names if _target_name_matches(declared_name, target)]
        if not matches:
            raise ValueError(
                "Expected target header declaration "
                f"`{declared_name}` from {path} does not match any attack target: {target_names}"
            )
        headers[matches[0]] = str(declaration.get("header") or "").strip()
    return headers


@dataclass(frozen=True)
class FocusedAttackContract:
    attack_targets: list[str]
    statement: str = ""
    allowed_files: list[str] | None = None
    allowed_helper_declarations: list[str] | None = None
    expected_target_headers: dict[str, str] | None = None
    forbidden_new_declaration_regexes: list[str] | None = None
    forbid_new_conditional_wrappers: bool = False


class FocusedLeanAttackAgent:
    """Lean-focused attack loop with host-enforced target contracts."""

    SYSTEM_PROMPT = """
You are a focused Lean attack agent.
You own the inner action loop for this episode: inspect the Lean project, edit allowed Lean files, run Lean/lake and other local tools, and repair errors.
The host will independently enforce a focused proof contract after every episode.
Your success condition is not a weaker theorem, a conditional wrapper, or a nearby reformulation. The required Lean declarations listed in the contract must exist and compile without sorry/admit/axiom/constant/opaque.
If a required declaration is blocked, attack that exact blocker with the smallest useful lemma or experiment. Do not broaden into general formalization work unless it directly supports a listed target.
Before spending significant time, leave a durable note in the run directory that identifies the current target, blocker, and next local lemma.
"""

    TERMINAL_STATUSES = {"verified", "blocked", "failed", "counterexample_suspected"}

    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = _resolve(repo_root)

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
            project = _resolve(project_dir)
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

    def run(
        self,
        *,
        workspace: Path,
        attack_targets: list[str],
        statement: str = "",
        context_paths: list[Path] | None = None,
        allowed_files: list[Path] | None = None,
        allowed_helper_declarations: list[str] | None = None,
        expected_target_headers: dict[str, str] | None = None,
        forbidden_new_declaration_regexes: list[str] | None = None,
        forbid_new_conditional_wrappers: bool = False,
        build_command: list[str] | None = None,
        backend: str = "codex",
        max_steps: int = 20,
        time_budget_sec: int = 3600,
        step_timeout_sec: int = 300,
        command_timeout_sec: int = 300,
        output_root: Path | None = None,
        run_name: str | None = None,
        enable_search: bool = False,
        model: str | None = None,
        reasoning_effort: str | None = None,
        project_dir: Path | None = None,
        problem_id: str = "",
        workspace_run_id: str | None = None,
        use_isolated_workspace: bool = False,
        merge_to_canonical: bool = False,
        review_status: str = "",
        library_module: str = "",
    ) -> dict[str, Any]:
        workspace = _resolve(workspace)
        if not workspace.exists():
            raise FileNotFoundError(f"Lean workspace does not exist: {workspace}")
        targets = [target.strip() for target in attack_targets if target.strip()]
        if not targets:
            raise ValueError("At least one focused attack target is required.")
        canonical_workspace = workspace
        workspace_reservation = None
        scheduler: PortfolioAttackScheduler | None = None
        if use_isolated_workspace:
            isolation = self._isolated_workspace(
                workspace=canonical_workspace,
                problem_id=problem_id or canonical_workspace.parent.name,
                run_id=workspace_run_id or run_name or f"focused-lean-attack-{utc_now_iso()}",
                project_dir=project_dir,
            )
            workspace = isolation["workspace"]
            workspace_reservation = isolation["reservation"]
            scheduler = isolation["scheduler"]

        build_command = build_command or ["lake", "build"]
        allowed_file_names = [
            _normalize_relative_file(path, workspace)
            for path in (allowed_files or [])
            if str(path).strip()
        ]
        contract = FocusedAttackContract(
            attack_targets=targets,
            statement=statement.strip(),
            allowed_files=allowed_file_names,
            allowed_helper_declarations=[item.strip() for item in (allowed_helper_declarations or []) if item.strip()],
            expected_target_headers=expected_target_headers or {},
            forbidden_new_declaration_regexes=[
                item.strip() for item in (forbidden_new_declaration_regexes or []) if item.strip()
            ],
            forbid_new_conditional_wrappers=forbid_new_conditional_wrappers,
        )

        initial_snapshot = _workspace_snapshot(workspace)
        initial_declarations = _collect_declarations(workspace)
        output_root = output_root or (self.repo_root / "artifacts" / "focused_lean_attack")
        config = CodexEpisodeConfig(
            name="focused-lean-attack",
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
        context_bundle = self._context_bundle(context_paths or [])
        _write_json(loop.run_dir / "focus_contract.json", self._contract_payload(contract, workspace, build_command))
        _write_text(loop.run_dir / "focus_contract.md", self._render_contract(contract, workspace, build_command))
        _write_text(loop.run_dir / "statement.md", statement.strip() + "\n")
        _write_text(loop.run_dir / "context_bundle.md", context_bundle)

        initial_observation = self._focused_observation(
            episode=0,
            last_message="",
            backend_report={"status": "initial"},
            workspace=workspace,
            contract=contract,
            build_command=build_command,
            build_timeout_sec=command_timeout_sec,
            initial_snapshot=initial_snapshot,
            initial_declarations=initial_declarations,
        )
        goal = "\n".join(
            [
                "Carry out a focused Lean attack under the host contract.",
                "",
                "Lean workspace:",
                str(workspace),
                "",
                "Contract file:",
                str(loop.run_dir / "focus_contract.md"),
                "",
                "Context bundle:",
                str(loop.run_dir / "context_bundle.md"),
                "",
                "Verifier command the host will run after each episode:",
                shlex.join(build_command),
                "",
                "Work only toward the required declarations. If the current route is blocked, record the blocker and attack the next smallest exact lemma.",
            ]
        )
        report = loop.run(
            goal=goal,
            episode_cwd=workspace,
            observer=self._observe_episode(
                workspace=workspace,
                contract=contract,
                build_command=build_command,
                build_timeout_sec=command_timeout_sec,
                initial_snapshot=initial_snapshot,
                initial_declarations=initial_declarations,
            ),
            initial_observation=initial_observation,
        )
        report["focus_contract_path"] = str(loop.run_dir / "focus_contract.json")
        report["focus_contract_markdown_path"] = str(loop.run_dir / "focus_contract.md")
        report["statement_path"] = str(loop.run_dir / "statement.md")
        report["context_bundle_path"] = str(loop.run_dir / "context_bundle.md")
        report["build_command"] = build_command
        final_observation = dict(report.get("final_observation") or {})
        final_targets = dict(final_observation.get("target_reports") or {})
        verified_target_count = sum(1 for item in final_targets.values() if item.get("found"))
        report["progress_velocity"] = calculate_progress_velocity(
            elapsed_seconds=float(report.get("elapsed_seconds") or 0.0),
            episodes_completed=int(report.get("episodes_completed") or 0),
            verified_target_count=verified_target_count if final_observation.get("contract_satisfied") else 0,
            target_count=len(targets),
        )
        report["workspace_isolated"] = bool(workspace_reservation)
        report["canonical_workspace"] = str(canonical_workspace) if workspace_reservation else str(workspace)
        report["isolated_workspace"] = str(workspace) if workspace_reservation else ""
        if workspace_reservation is not None:
            report["workspace_reservation"] = workspace_reservation.as_payload(repo_root=self.repo_root)
        if workspace_reservation is not None and scheduler is not None and merge_to_canonical:
            merge_report = scheduler.merge_reviewed_formal_workspace(
                project_dir=workspace_reservation.project_dir,
                run_id=workspace_reservation.run_id,
                status=str(report.get("status") or ""),
                review_status=review_status,
                library_module=library_module,
            )
            report["formal_workspace_merge"] = merge_report
        elif workspace_reservation is not None:
            report["formal_workspace_merge"] = {"merged": False, "reason": "merge_not_requested"}
        _write_json(loop.run_dir / "report.json", report)
        return report

    def _observe_episode(
        self,
        *,
        workspace: Path,
        contract: FocusedAttackContract,
        build_command: list[str],
        build_timeout_sec: int,
        initial_snapshot: dict[str, str],
        initial_declarations: list[dict[str, Any]],
    ) -> EpisodeObserver:
        def observe(episode: int, episode_dir: Path, last_message: str, backend_report: dict[str, Any]) -> dict[str, Any]:
            del episode_dir
            return self._focused_observation(
                episode=episode,
                last_message=last_message,
                backend_report=backend_report,
                workspace=workspace,
                contract=contract,
                build_command=build_command,
                build_timeout_sec=build_timeout_sec,
                initial_snapshot=initial_snapshot,
                initial_declarations=initial_declarations,
            )

        return observe

    def _focused_observation(
        self,
        *,
        episode: int,
        last_message: str,
        backend_report: dict[str, Any],
        workspace: Path,
        contract: FocusedAttackContract,
        build_command: list[str],
        build_timeout_sec: int,
        initial_snapshot: dict[str, str],
        initial_declarations: list[dict[str, Any]],
    ) -> dict[str, Any]:
        build_report = _run_command(build_command, cwd=workspace, timeout_sec=build_timeout_sec)
        counts = {
            "sorry": _count_pattern(workspace, SORRY_RE),
            "axiom": _count_pattern(workspace, AXIOM_RE),
            "admit": _count_pattern(workspace, ADMIT_RE),
            "constant_or_opaque": _count_pattern(workspace, CONSTANT_RE),
        }
        forbidden_total = sum(counts.values())
        target_reports = {
            target: self._target_report(workspace, target, (contract.expected_target_headers or {}).get(target, ""))
            for target in contract.attack_targets
        }
        missing_targets = [target for target, report in target_reports.items() if not report.get("found")]
        header_mismatches = [
            target
            for target, report in target_reports.items()
            if (contract.expected_target_headers or {}).get(target) and not report.get("expected_header_match", {}).get("matched")
        ]
        current_snapshot = _workspace_snapshot(workspace)
        changed_files = _workspace_changes(initial_snapshot, current_snapshot)
        allowed_file_set = set(contract.allowed_files or [])
        disallowed_file_changes = [
            change for change in changed_files if allowed_file_set and change["path"] not in allowed_file_set
        ]
        current_declarations = _collect_declarations(workspace)
        new_declarations = self._new_declarations(initial_declarations, current_declarations)
        new_declaration_violations = self._new_declaration_violations(contract, new_declarations)

        blockers: list[str] = []
        if build_report["status"] != "passed":
            blockers.append(f"Build status is {build_report['status']}.")
        if forbidden_total:
            blockers.append(f"Lean workspace contains {forbidden_total} forbidden placeholder/trust declaration(s).")
        if missing_targets:
            blockers.append("Missing required declaration(s): " + ", ".join(missing_targets))
        if header_mismatches:
            blockers.append("Declaration header mismatch for: " + ", ".join(header_mismatches))
        if disallowed_file_changes:
            blockers.append(
                "Disallowed Lean file changes: " + ", ".join(change["path"] for change in disallowed_file_changes)
            )
        if new_declaration_violations:
            blockers.append(
                "Forbidden new declaration(s): "
                + ", ".join(str(item.get("full_name") or item.get("name")) for item in new_declaration_violations)
            )

        contract_satisfied = (
            build_report["status"] == "passed"
            and forbidden_total == 0
            and not missing_targets
            and not header_mismatches
            and not disallowed_file_changes
            and not new_declaration_violations
        )
        backend_status = str(backend_report.get("status") or "")
        status = _extract_status(last_message, fallback="partial")
        if contract_satisfied:
            status = "verified"
        elif backend_status in {"skipped", "unsupported", "unavailable"}:
            status = "blocked"
        elif status == "verified":
            status = "partial"

        terminal = status in self.TERMINAL_STATUSES
        return {
            "episode": episode,
            "generated_at": utc_now_iso(),
            "status": status,
            "terminal": terminal,
            "stop_reason": f"{status}_reported" if terminal else "",
            "backend_status": backend_status,
            "contract_satisfied": contract_satisfied,
            "build": build_report,
            "counts": counts,
            "attack_targets": contract.attack_targets,
            "target_reports": target_reports,
            "missing_targets": missing_targets,
            "header_mismatches": header_mismatches,
            "changed_files": changed_files,
            "disallowed_file_changes": disallowed_file_changes,
            "new_declarations": new_declarations,
            "new_declaration_violations": new_declaration_violations,
            "blockers": blockers,
            "next_episode_directive": self._next_episode_directive(contract, blockers, target_reports),
            "last_message_tail": _tail(last_message, 4000),
        }

    def _target_report(self, workspace: Path, target: str, expected_header: str) -> dict[str, Any]:
        declaration = _target_declaration(workspace, target)
        if not declaration.get("found"):
            return declaration
        actual_header = str(declaration.get("header") or "")
        expected_match: dict[str, Any] = {"required": bool(expected_header), "matched": None}
        if expected_header:
            expected_match = {
                "required": True,
                **compare_lean_declaration_headers(
                    actual_header=actual_header,
                    expected_header=expected_header,
                    target_theorem=target,
                ),
            }
        return {
            **declaration,
            "expected_header_match": expected_match,
        }

    def _new_declarations(
        self,
        initial_declarations: list[dict[str, Any]],
        current_declarations: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        initial_keys = {_declaration_key(declaration) for declaration in initial_declarations}
        return [declaration for declaration in current_declarations if _declaration_key(declaration) not in initial_keys]

    def _new_declaration_violations(
        self,
        contract: FocusedAttackContract,
        new_declarations: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        allowed_names = set(contract.attack_targets)
        allowed_names.update(contract.allowed_helper_declarations or [])
        patterns = [re.compile(pattern) for pattern in (contract.forbidden_new_declaration_regexes or [])]
        violations: list[dict[str, Any]] = []
        for declaration in new_declarations:
            full_name = str(declaration.get("full_name") or "")
            raw_name = str(declaration.get("name") or "")
            if any(_target_name_matches(full_name, allowed) or _target_name_matches(raw_name, allowed) for allowed in allowed_names):
                continue
            reason = ""
            if patterns and any(pattern.search(full_name) or pattern.search(raw_name) for pattern in patterns):
                reason = "forbidden_regex"
            elif contract.forbid_new_conditional_wrappers and _looks_conditional_wrapper(str(declaration.get("header") or "")):
                reason = "new_conditional_wrapper"
            if reason:
                violations.append({**declaration, "violation_reason": reason})
        return violations

    def _next_episode_directive(
        self,
        contract: FocusedAttackContract,
        blockers: list[str],
        target_reports: dict[str, dict[str, Any]],
    ) -> str:
        if not blockers:
            return "Focused contract is satisfied; stop."
        missing = [target for target, report in target_reports.items() if not report.get("found")]
        lines = [
            "Continue the focused Lean attack.",
            "Do not add weaker substitute theorems or conditional wrappers for the target.",
            "Attack the first unsatisfied required declaration or its smallest direct lemma.",
            "",
            "Required declarations:",
            *[f"- {target}" for target in contract.attack_targets],
            "",
            "Current blockers:",
            *[f"- {blocker}" for blocker in blockers],
        ]
        if missing:
            lines.extend(["", "First missing target(s):", *[f"- {target}" for target in missing]])
        return "\n".join(lines)

    def _context_bundle(self, context_paths: list[Path]) -> str:
        if not context_paths:
            return "No context files supplied.\n"
        chunks: list[str] = []
        for raw_path in context_paths:
            path = _resolve(raw_path)
            text = _read_text(path, max_chars=30000)
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

    def _contract_payload(
        self,
        contract: FocusedAttackContract,
        workspace: Path,
        build_command: list[str],
    ) -> dict[str, Any]:
        return {
            "workspace": str(workspace),
            "attack_targets": contract.attack_targets,
            "statement": contract.statement,
            "allowed_files": contract.allowed_files or [],
            "allowed_helper_declarations": contract.allowed_helper_declarations or [],
            "expected_target_headers": contract.expected_target_headers or {},
            "forbid_new_conditional_wrappers": contract.forbid_new_conditional_wrappers,
            "forbidden_new_declaration_regexes": contract.forbidden_new_declaration_regexes or [],
            "build_command": build_command,
        }

    def _render_contract(
        self,
        contract: FocusedAttackContract,
        workspace: Path,
        build_command: list[str],
    ) -> str:
        lines = [
            "# Focused Lean Attack Contract",
            "",
            f"- Workspace: `{workspace}`",
            f"- Build command: `{shlex.join(build_command)}`",
            f"- Forbid new conditional wrappers: `{contract.forbid_new_conditional_wrappers}`",
            "",
            "## Required Declarations",
            "",
            *[f"- `{target}`" for target in contract.attack_targets],
            "",
            "## Allowed Lean Files",
            "",
        ]
        if contract.allowed_files:
            lines.extend(f"- `{path}`" for path in contract.allowed_files)
        else:
            lines.append("- `<all project Lean files>`")
        lines.extend(["", "## Allowed Helper Declarations", ""])
        if contract.allowed_helper_declarations:
            lines.extend(f"- `{name}`" for name in contract.allowed_helper_declarations)
        else:
            lines.append("- `<none explicitly allowed>`")
        lines.extend(["", "## Forbidden New Declaration Regexes", ""])
        if contract.forbidden_new_declaration_regexes:
            lines.extend(f"- `{pattern}`" for pattern in contract.forbidden_new_declaration_regexes)
        else:
            lines.append("- `<none>`")
        if contract.expected_target_headers:
            lines.extend(["", "## Expected Target Headers", ""])
            for target, header in contract.expected_target_headers.items():
                lines.extend([f"### `{target}`", "", "```lean", header.strip(), "```", ""])
        if contract.statement:
            lines.extend(["", "## Statement", "", "```text", contract.statement, "```", ""])
        return "\n".join(lines).rstrip() + "\n"
