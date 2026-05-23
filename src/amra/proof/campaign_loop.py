from __future__ import annotations

import json
import re
import shlex
import time
from pathlib import Path
from typing import Any

from amra.portfolio_scheduler import calculate_progress_velocity
from amra.lean.formalizer import LeanFormalizerRunner, collect_proof_lab_context_paths
from amra.proof.global_supervisor import GlobalProofSupervisor
from amra.proof.lab import AIProofLabRunner
from amra.core.workspace import read_text, slugify, utc_now_iso, write_json, write_text


LEAN_DECL_PATTERN = re.compile(
    r"(?m)^\s*(?:noncomputable\s+)?(?:theorem|lemma)\s+"
    r"([A-Za-z_][A-Za-z0-9_'.]*|«[^»]+»)(?=\s|:|\(|\{|\[|$)"
)
LEAN_FENCE_PATTERN = re.compile(r"```(?:lean|lean4)?\s*\n(.*?)```", re.IGNORECASE | re.DOTALL)
BACKTICK_NAME_PATTERN = re.compile(r"`([A-Za-z_][A-Za-z0-9_'.]*)`")

LEAN_KEYWORDS_AND_STOPWORDS = {
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

TARGET_FIELD_PRIORITY: tuple[tuple[str, str], ...] = (
    ("open_continuation_target", "first_decl"),
    ("recommended_attack_target", "backtick_then_first_decl"),
    ("formalization_consequence", "last_backtick"),
    ("formalization_target", "last_decl"),
    ("failure_mode", "last_decl"),
)


def _strip_escaped_identifier(name: str) -> str:
    stripped = name.strip()
    if stripped.startswith("«") and stripped.endswith("»"):
        return stripped[1:-1].strip()
    return stripped


def _is_valid_target_name(name: str, excluded_names: set[str] | None = None) -> bool:
    normalized = _strip_escaped_identifier(name)
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_'.]*", normalized):
        return False
    if normalized.lower() in LEAN_KEYWORDS_AND_STOPWORDS:
        return False
    if excluded_names and normalized in excluded_names:
        return False
    return True


def _valid_target_names(names: list[str], excluded_names: set[str] | None = None) -> list[str]:
    valid: list[str] = []
    for name in names:
        normalized = _strip_escaped_identifier(name)
        if _is_valid_target_name(normalized, excluded_names=excluded_names):
            valid.append(normalized)
    return valid


def _decl_names_from_text(text: str, excluded_names: set[str] | None = None) -> list[str]:
    return _valid_target_names([match.group(1) for match in LEAN_DECL_PATTERN.finditer(text)], excluded_names)


def _decl_names_from_lean_fences(text: str, excluded_names: set[str] | None = None) -> list[str]:
    names: list[str] = []
    for match in LEAN_FENCE_PATTERN.finditer(text):
        names.extend(_decl_names_from_text(match.group(1), excluded_names=excluded_names))
    return names


def _backtick_names_from_text(text: str, excluded_names: set[str] | None = None) -> list[str]:
    return _valid_target_names([match.group(1) for match in BACKTICK_NAME_PATTERN.finditer(text)], excluded_names)


def _choose_from_field(text: str, *, policy: str, excluded_names: set[str] | None = None) -> str:
    if not text.strip():
        return ""
    decl_names = _decl_names_from_lean_fences(text, excluded_names=excluded_names) or _decl_names_from_text(
        text, excluded_names=excluded_names
    )
    backtick_names = _backtick_names_from_text(text, excluded_names=excluded_names)
    if policy == "last_decl":
        return decl_names[-1] if decl_names else (backtick_names[-1] if backtick_names else "")
    if policy == "last_backtick":
        return backtick_names[-1] if backtick_names else (decl_names[-1] if decl_names else "")
    if policy == "backtick_then_first_decl":
        return backtick_names[0] if backtick_names else (decl_names[0] if decl_names else "")
    return decl_names[0] if decl_names else (backtick_names[0] if backtick_names else "")


def extract_first_theorem_name(text: str, *, excluded_names: set[str] | None = None) -> str:
    """Return the first Lean theorem/lemma name mentioned in a text blob."""

    # Prefer actual Lean declarations.  Natural-language phrases such as
    # "the theorem is ..." must not become formalization targets.
    names = _decl_names_from_lean_fences(text, excluded_names=excluded_names)
    if names:
        return names[0]
    names = _decl_names_from_text(text, excluded_names=excluded_names)
    return names[0] if names else ""


def _read_json_file(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _extract_from_parsed_fields(fields: dict[str, Any], *, excluded_names: set[str] | None = None) -> str:
    for key, policy in TARGET_FIELD_PRIORITY:
        target = _choose_from_field(str(fields.get(key) or ""), policy=policy, excluded_names=excluded_names)
        if target:
            return target
    return ""


def _extract_from_proof_lab_payload(payload: dict[str, Any], *, excluded_names: set[str] | None = None) -> str:
    grounding = payload.get("grounding") or {}
    target = _extract_from_parsed_fields(dict(grounding.get("parsed_fields") or {}), excluded_names=excluded_names)
    if target:
        return target

    attempts_by_number: dict[Any, dict[str, Any]] = {
        attempt.get("attempt"): attempt for attempt in list(payload.get("attempts") or [])
    }
    for audit in list(payload.get("audits") or []):
        parsed = dict(audit.get("parsed_fields") or {})
        status = str(parsed.get("audit_status") or "").lower()
        recommendation = str(parsed.get("recommendation") or "").lower()
        if "passes_initial_audit" not in status and recommendation != "formalize":
            continue
        target = _extract_from_parsed_fields(parsed, excluded_names=excluded_names)
        if target:
            return target
        attempt = attempts_by_number.get(audit.get("attempt")) or {}
        target = _extract_from_parsed_fields(dict(attempt.get("parsed_fields") or {}), excluded_names=excluded_names)
        if target:
            return target

    for cluster in list(payload.get("clusters") or []):
        attempt = attempts_by_number.get(cluster.get("representative_attempt")) or {}
        target = _extract_from_parsed_fields(dict(attempt.get("parsed_fields") or {}), excluded_names=excluded_names)
        if target:
            return target

    for attempt in list(payload.get("attempts") or []):
        target = _extract_from_parsed_fields(dict(attempt.get("parsed_fields") or {}), excluded_names=excluded_names)
        if target:
            return target
    return ""


def extract_formalization_target_from_run(run_dir: Path, *, excluded_names: set[str] | None = None) -> str:
    """Find a likely Lean target theorem from a proof-lab run.

    Prefer proof-lab's structured fields over free-form Markdown.  Fallback
    parsing only accepts real Lean declaration lines, preventing prose such as
    "the theorem is ..." from producing bogus targets like `is` or `in`.
    """

    for name in ("report.json", "state.json"):
        payload = _read_json_file(run_dir / name)
        if payload:
            target = _extract_from_proof_lab_payload(payload, excluded_names=excluded_names)
            if target:
                return target

    candidates: list[Path] = []
    for subdir in ("grounding", "audits", "attempts"):
        directory = run_dir / subdir
        if directory.exists():
            candidates.extend(sorted(directory.glob("*_output.md"), reverse=True))
    candidates.extend([run_dir / "summary.md", run_dir / "grounding" / "source_grounding_output.md"])
    for path in candidates:
        if not path.exists():
            continue
        name = extract_first_theorem_name(read_text(path), excluded_names=excluded_names)
        if name:
            return name
    return ""


class CampaignLoopRunner:
    """Outer self-iteration loop for long theorem-proving campaigns.

    The loop coordinates read-only mathematical route discovery with Lean
    write/verify attempts.  It keeps durable round artifacts so later rounds can
    reflect on prior results instead of restarting from scratch.
    """

    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.proof_lab_runner = AIProofLabRunner(repo_root=repo_root)
        self.lean_formalizer_runner = LeanFormalizerRunner(repo_root=repo_root)
        self.global_supervisor = GlobalProofSupervisor(repo_root=repo_root)

    def _new_run_dir(self, *, output_root: Path, run_name: str | None) -> Path:
        base = slugify(run_name or f"campaign-loop-{utc_now_iso()}")
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

    def _read_history_snippets(self, round_entries: list[dict[str, Any]], *, max_chars: int = 24000) -> str:
        snippets: list[str] = []
        for entry in round_entries[-6:]:
            summary_path_text = str(entry.get("summary_path") or "").strip()
            summary_path = Path(summary_path_text) if summary_path_text else None
            if summary_path is not None and summary_path.exists() and summary_path.is_file():
                text = read_text(summary_path)
                snippets.append(
                    "\n".join(
                        [
                            f"## Prior Round {entry.get('round')} ({entry.get('stage')})",
                            "",
                            text[-4000:].strip(),
                            "",
                        ]
                    )
                )
            assessment_path_text = str(entry.get("global_assessment_path") or "").strip()
            assessment_path = Path(assessment_path_text) if assessment_path_text else None
            if assessment_path is not None and assessment_path.exists() and assessment_path.is_file():
                snippets.append(
                    "\n".join(
                        [
                            f"## Prior Round {entry.get('round')} Global Assessment",
                            "",
                            read_text(assessment_path)[-4000:].strip(),
                            "",
                        ]
                    )
                )
            supervisor_path_text = str(entry.get("supervisor_decision_path") or "").strip()
            supervisor_path = Path(supervisor_path_text) if supervisor_path_text else None
            if supervisor_path is not None and supervisor_path.exists() and supervisor_path.is_file():
                snippets.append(
                    "\n".join(
                        [
                            f"## Prior Round {entry.get('round')} Supervisor Decision",
                            "",
                            read_text(supervisor_path)[-4000:].strip(),
                            "",
                        ]
                    )
                )
        history = "\n".join(snippets).strip()
        if len(history) > max_chars:
            history = history[-max_chars:]
        return history or "No prior loop history."

    def _build_stage_goal(
        self,
        *,
        statement: str,
        round_number: int,
        rounds: int,
        stage: str,
        current_target_theorem: str,
        final_target_theorem: str,
        completed_target_theorems: set[str],
        history: str,
    ) -> str:
        target_lines = [
            f"- Current stage theorem: `{current_target_theorem or '<none yet>'}`",
            f"- Final theorem: `{final_target_theorem or '<not fixed; derive theorem-level targets>'}`",
            f"- Already verified/excluded stage theorems: `{', '.join(sorted(completed_target_theorems)) or '<none yet>'}`",
        ]
        if stage == "proof_lab":
            stage_directive = [
                "This round is mathematical route discovery and target selection.",
                "Do not edit files.  Reassess the global proof objective, identify the current first blocker, and either repair the leading route or switch routes.",
                "If a route is viable, state the exact Lean theorem that the next formalizer round should prove.",
                "Avoid local optimization that does not move the main theorem.",
            ]
        else:
            stage_directive = [
                "This round is Lean write/verify.",
                "Edit the Lean workspace only as needed to prove the current stage theorem.",
                "If the stage theorem is too broad, introduce proved intermediate lemmas but do not weaken the requested theorem or add trusted assumptions.",
                "Run the configured verifier and report the exact next blocker if not verified.",
            ]
        return "\n".join(
            [
                "# ARA Campaign Loop Stage Goal",
                "",
                f"Round: {round_number} of {rounds}",
                f"Stage: `{stage}`",
                "",
                "## Main Objective",
                "",
                statement.strip(),
                "",
                "## Targets",
                "",
                *target_lines,
                "",
                "## Loop Discipline",
                "",
                "- Start by reviewing the prior-round history.",
                "- Re-state the current first blocker before doing local work.",
                "- Prefer theorem-level progress over local simplification.",
                "- Freeze or demote routes that repeatedly fail the global audit.",
                "- Do not select any already verified stage theorem as the next target.",
                "- End with a concrete next-stage target.",
                "",
                "## Stage Directive",
                "",
                *stage_directive,
                "",
                "## Prior History",
                "",
                history,
                "",
            ]
        )

    def _choose_stage(
        self,
        *,
        mode: str,
        round_number: int,
        workspace: Path | None,
        current_target_theorem: str,
        previous_entry: dict[str, Any] | None,
    ) -> str:
        if (
            mode in {"auto", "hybrid"}
            and previous_entry
            and previous_entry.get("needs_global_reassessment")
        ):
            return "proof_lab"
        if mode == "proof-lab":
            return "proof_lab"
        if mode == "lean-formalizer":
            return "lean_formalizer" if workspace and current_target_theorem else "proof_lab"
        if mode == "hybrid":
            if not previous_entry:
                return "lean_formalizer" if workspace and current_target_theorem else "proof_lab"
            if previous_entry.get("stage") == "lean_formalizer" and previous_entry.get("status") != "verified":
                return "lean_formalizer" if workspace and current_target_theorem else "proof_lab"
            if workspace and current_target_theorem:
                return "lean_formalizer"
            return "proof_lab"

        # auto
        if round_number == 1:
            return "proof_lab"
        if previous_entry and previous_entry.get("stage") == "lean_formalizer":
            if previous_entry.get("status") == "verified":
                return "proof_lab"
            return "lean_formalizer" if workspace and current_target_theorem else "proof_lab"
        next_action = str((previous_entry or {}).get("next_action") or "").lower()
        if workspace and current_target_theorem and (
            "formalize" in next_action or "promote" in next_action or "lean" in next_action
        ):
            return "lean_formalizer"
        return "proof_lab"

    def _formalizer_child_needs_global_reassessment(self, child: dict[str, Any]) -> bool:
        if bool(child.get("needs_global_reassessment")):
            return True
        if child.get("status") == "verified":
            return False
        attempts = list(child.get("attempts") or [])
        if not attempts:
            return False
        no_defect_progress = all(int(entry.get("progress_delta") or 0) <= 0 for entry in attempts)
        best = dict(child.get("best_audit") or {})
        target_missing = any(
            "Target theorem" in str(blocker) and "not found" in str(blocker)
            for blocker in list(best.get("blockers") or [])
        )
        return no_defect_progress and target_missing

    def _write_global_assessment(
        self,
        *,
        path: Path,
        statement: str,
        current_target_theorem: str,
        final_target_theorem: str,
        child: dict[str, Any],
    ) -> None:
        best = dict(child.get("best_audit") or {})
        blockers = list(best.get("blockers") or [])
        suggested_next_targets = list(child.get("suggested_next_targets") or [])
        attempts = list(child.get("attempts") or [])
        lines = [
            "# ARA Global Reassessment Trigger",
            "",
            "The Lean formalizer made no strict-audit progress on the current stage target.",
            "Before continuing, the campaign supervisor must reassess the proof decomposition and choose the next theorem-level blocker.",
            "",
            "## Main Objective",
            "",
            statement.strip(),
            "",
            "## Current Targets",
            "",
            f"- Current stage theorem: `{current_target_theorem or '<none>'}`",
            f"- Final theorem: `{final_target_theorem or '<not fixed>'}`",
            f"- Formalizer status: `{child.get('status')}`",
            f"- Formalizer stop reason: `{child.get('stop_reason')}`",
            f"- Attempts completed: {child.get('attempts_completed')}",
            f"- Needs reassessment: {child.get('needs_global_reassessment')}",
            "",
            "## Strict-Audit Blockers",
            "",
        ]
        lines.extend(f"- {item}" for item in blockers) if blockers else lines.append("- none")
        lines.extend(["", "## Backend Next-Target Signals", ""])
        lines.extend(f"- {item}" for item in suggested_next_targets) if suggested_next_targets else lines.append("- none")
        lines.extend(["", "## Attempt Score Trace", ""])
        if attempts:
            for entry in attempts[-8:]:
                lines.append(
                    "- Attempt {iteration}: progress_delta={progress_delta}, "
                    "build={build_status}, verified={verified}".format(
                        iteration=entry.get("iteration"),
                        progress_delta=entry.get("progress_delta"),
                        build_status=entry.get("build_status"),
                        verified=entry.get("verified"),
                    )
                )
        else:
            lines.append("- none")
        lines.extend(
            [
                "",
                "## Required Global Decision",
                "",
                "- Decide whether the current stage theorem is still the right immediate target.",
                "- If it is too broad, replace it with the first smaller theorem that directly plugs into the final proof chain.",
                "- The replacement must be a theorem-level target, not another loose local lemma.",
                "- Provide the replacement as a Lean declaration in a `Formalization target:` or `open_continuation_target` field.",
                "- Explain how the replacement theorem will be used to close the prior stage theorem.",
                "- Freeze or demote routes that only add build-clean local lemmas without changing the main target state.",
                "",
            ]
        )
        write_text(path, "\n".join(lines))

    def _stage_time_budget(
        self,
        *,
        stage: str,
        remaining_seconds: int,
        rounds_left: int,
        round_time_budget_sec: int,
    ) -> int:
        if remaining_seconds <= 0:
            return 0
        if round_time_budget_sec > 0:
            return min(remaining_seconds, round_time_budget_sec)
        fair_slice = max(1, remaining_seconds // max(1, rounds_left))
        if stage == "lean_formalizer":
            return min(remaining_seconds, max(fair_slice, 900), 2400)
        return min(remaining_seconds, max(fair_slice, 600), 1800)

    def _loop_context_paths(self, base_context_paths: list[Path], round_entries: list[dict[str, Any]]) -> list[Path]:
        paths = list(base_context_paths)
        for entry in round_entries[-4:]:
            assessment_path_text = str(entry.get("global_assessment_path") or "").strip()
            assessment_path = Path(assessment_path_text) if assessment_path_text else None
            if assessment_path is not None and assessment_path.exists() and assessment_path.is_file():
                paths.append(assessment_path)
            supervisor_path_text = str(entry.get("supervisor_decision_path") or "").strip()
            supervisor_path = Path(supervisor_path_text) if supervisor_path_text else None
            if supervisor_path is not None and supervisor_path.exists() and supervisor_path.is_file():
                paths.append(supervisor_path)
            run_dir_text = str(entry.get("run_dir") or "").strip()
            run_dir = Path(run_dir_text) if run_dir_text else None
            if run_dir is None or not run_dir.exists():
                continue
            if entry.get("stage") == "proof_lab":
                paths.extend(collect_proof_lab_context_paths(run_dir))
            else:
                for name in ("summary.md", "report.json"):
                    path = run_dir / name
                    if path.exists():
                        paths.append(path)
        seen: set[str] = set()
        deduped: list[Path] = []
        for path in paths:
            key = str(path.expanduser().resolve())
            if key in seen:
                continue
            seen.add(key)
            deduped.append(path)
        return deduped

    def _supervisor_trigger_reason(
        self,
        *,
        entry: dict[str, Any],
        previous_entry: dict[str, Any] | None,
        supervisor_every_rounds: int,
    ) -> str:
        round_number = int(entry.get("round") or 0)
        reasons: list[str] = []
        if entry.get("needs_global_reassessment"):
            reasons.append("latest round explicitly requested global reassessment")
        if supervisor_every_rounds > 0 and round_number > 0 and round_number % supervisor_every_rounds == 0:
            reasons.append(f"periodic global review every {supervisor_every_rounds} rounds")
        if previous_entry and previous_entry.get("status") == entry.get("status") and previous_entry.get("next_action") == entry.get("next_action"):
            reasons.append("round status and next action repeated from the previous round")
        if entry.get("stage") == "lean_formalizer" and not entry.get("verified"):
            velocity = dict(entry.get("progress_velocity") or {})
            if int(entry.get("attempts_completed") or 0) > 0 and int(velocity.get("net_progress_delta") or 0) <= 0:
                reasons.append("Lean formalizer attempts produced no net strict-audit progress")
        return "; ".join(reasons) or "manual/periodic global strategy review"

    def _should_run_supervisor(
        self,
        *,
        entry: dict[str, Any],
        previous_entry: dict[str, Any] | None,
        supervisor_backend: str,
        supervisor_on_stall: bool,
        supervisor_every_rounds: int,
    ) -> bool:
        if supervisor_backend == "none":
            return False
        if entry.get("verified"):
            return False
        round_number = int(entry.get("round") or 0)
        if supervisor_every_rounds > 0 and round_number > 0 and round_number % supervisor_every_rounds == 0:
            return True
        if not supervisor_on_stall:
            return False
        if entry.get("needs_global_reassessment"):
            return True
        if (
            previous_entry
            and previous_entry.get("stage") == entry.get("stage")
            and previous_entry.get("target_theorem") == entry.get("target_theorem")
            and previous_entry.get("status") == entry.get("status")
            and previous_entry.get("next_action") == entry.get("next_action")
        ):
            return True
        if entry.get("stage") == "lean_formalizer":
            velocity = dict(entry.get("progress_velocity") or {})
            return int(entry.get("attempts_completed") or 0) > 0 and int(velocity.get("net_progress_delta") or 0) <= 0
        return False

    def _apply_supervisor_decision(
        self,
        *,
        entry: dict[str, Any],
        decision: dict[str, Any],
        current_target_theorem: str,
        final_target_theorem: str,
        completed_target_theorems: set[str],
    ) -> str:
        action = str(decision.get("decision") or "continue_current_target")
        suggested_target = str(decision.get("target_theorem") or "").strip()
        next_target = current_target_theorem
        entry["supervisor"] = {
            "decision": action,
            "target_theorem": suggested_target,
            "reason": decision.get("reason") or "",
            "instructions": decision.get("instructions") or "",
            "route_risk": decision.get("route_risk") or "",
            "decision_path": decision.get("decision_path") or "",
            "parsed_decision_path": decision.get("parsed_decision_path") or "",
            "backend_status": (decision.get("backend_invocation") or {}).get("status"),
        }
        entry["supervisor_decision"] = action
        entry["supervisor_decision_path"] = decision.get("decision_path") or ""
        entry["supervisor_parsed_decision_path"] = decision.get("parsed_decision_path") or ""
        entry["supervisor_target_theorem"] = suggested_target
        entry["supervisor_target_replaced"] = False
        if action == "final_target":
            suggested_target = final_target_theorem.strip() or suggested_target
            if suggested_target and suggested_target not in completed_target_theorems:
                next_target = suggested_target
                entry["needs_global_reassessment"] = False
        elif action == "switch_target":
            if suggested_target and suggested_target not in completed_target_theorems:
                next_target = suggested_target
                entry["needs_global_reassessment"] = False
            else:
                entry["needs_global_reassessment"] = True
        elif action == "return_to_proof_lab":
            entry["needs_global_reassessment"] = True
        elif action == "freeze_route":
            entry["needs_global_reassessment"] = True
            next_target = ""

        if next_target != current_target_theorem:
            entry["supervisor_target_replaced"] = True
            entry["supervisor_previous_target_theorem"] = current_target_theorem
            entry["supervisor_next_target_theorem"] = next_target
        return next_target

    def _write_summary(self, *, path: Path, payload: dict[str, Any]) -> None:
        lines = [
            "# ARA Campaign Loop Report",
            "",
            f"- Status: {payload.get('status')}",
            f"- Stop reason: {payload.get('stop_reason')}",
            f"- Rounds completed: {payload.get('rounds_completed')} / {payload.get('rounds_requested')}",
            f"- Current target theorem: `{payload.get('current_target_theorem') or ''}`",
            f"- Final target theorem: `{payload.get('final_target_theorem') or ''}`",
            f"- Elapsed seconds: {payload.get('elapsed_seconds')}",
            "",
            "## Rounds",
            "",
        ]
        rounds = payload.get("rounds") or []
        if not rounds:
            lines.append("- none")
        for entry in rounds:
            suffix = ""
            if entry.get("needs_global_reassessment"):
                suffix = " [global reassessment requested]"
            elif entry.get("target_replaced"):
                suffix = (
                    f" [retargeted from `{entry.get('previous_target_theorem')}` "
                    f"to `{entry.get('target_theorem')}`]"
                )
            if entry.get("supervisor_target_replaced"):
                suffix += (
                    f" [supervisor retargeted to `{entry.get('supervisor_next_target_theorem')}`]"
                )
            elif entry.get("supervisor_decision"):
                suffix += f" [supervisor: {entry.get('supervisor_decision')}]"
            lines.append(
                f"- Round {entry.get('round')}: {entry.get('stage')} -> "
                f"{entry.get('status')} ({entry.get('stop_reason') or entry.get('next_action') or ''})"
                f"{suffix}"
            )
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
        statement: str,
        context_paths: list[Path] | None = None,
        workspace: Path | None = None,
        final_target_theorem: str = "",
        initial_target_theorem: str = "",
        target_file: Path | None = None,
        build_command: list[str] | None = None,
        backend: str = "codex",
        mode: str = "auto",
        rounds: int = 4,
        time_budget_sec: int = 3600,
        proof_attempts: int = 4,
        proof_audits: int = 2,
        proof_attempt_timeout_sec: int = 600,
        proof_audit_timeout_sec: int = 300,
        proof_grounding_timeout_sec: int = 300,
        formalizer_attempts: int = 8,
        formalizer_attempt_timeout_sec: int = 900,
        formalizer_build_timeout_sec: int = 300,
        source_first: bool = False,
        enable_search: bool = True,
        output_root: Path | None = None,
        run_name: str | None = None,
        max_stalled_rounds: int = 0,
        round_time_budget_sec: int = 0,
        completed_target_theorems: list[str] | None = None,
        expected_target_header: str | None = None,
        supervisor_backend: str = "none",
        supervisor_on_stall: bool = True,
        supervisor_every_rounds: int = 0,
        supervisor_timeout_sec: int = 900,
        library_module: str = "",
        promote_to_library: bool = False,
        math_tools_profile: str = "full",
        install_missing_math_tools: bool | None = None,
        run_math_tool_smoke: bool | None = None,
    ) -> dict[str, Any]:
        if not statement.strip():
            raise ValueError("Campaign loop statement must not be empty.")
        if mode not in {"auto", "hybrid", "proof-lab", "lean-formalizer"}:
            raise ValueError(f"Unsupported campaign loop mode: {mode}")
        if supervisor_backend not in {"codex", "none"}:
            raise ValueError(f"Unsupported supervisor backend: {supervisor_backend}")

        output_root = output_root or (self.repo_root / "artifacts" / "campaign_loop")
        run_dir = self._new_run_dir(output_root=output_root, run_name=run_name)
        rounds_dir = run_dir / "rounds"
        rounds_dir.mkdir(parents=True, exist_ok=True)
        write_text(run_dir / "statement.md", statement.strip() + "\n")

        started = time.monotonic()
        deadline = started + max(1, time_budget_sec)
        round_entries: list[dict[str, Any]] = []
        current_target_theorem = initial_target_theorem.strip() or final_target_theorem.strip()
        completed_target_theorem_set: set[str] = {
            theorem.strip() for theorem in (completed_target_theorems or []) if theorem.strip()
        }
        stop_reason = "rounds_exhausted"
        stalled_rounds = 0

        for offset in range(max(0, rounds)):
            remaining = int(deadline - time.monotonic())
            if remaining <= 0:
                stop_reason = "time_budget_exhausted"
                break
            round_number = offset + 1
            rounds_left = max(1, rounds - offset)
            previous = round_entries[-1] if round_entries else None
            stage = self._choose_stage(
                mode=mode,
                round_number=round_number,
                workspace=workspace,
                current_target_theorem=current_target_theorem,
                previous_entry=previous,
            )
            round_dir = rounds_dir / f"round_{round_number:03d}"
            round_dir.mkdir(parents=True, exist_ok=True)
            history = self._read_history_snippets(round_entries)
            stage_goal = self._build_stage_goal(
                statement=statement,
                round_number=round_number,
                rounds=rounds,
                stage=stage,
                current_target_theorem=current_target_theorem,
                final_target_theorem=final_target_theorem.strip(),
                completed_target_theorems=completed_target_theorem_set,
                history=history,
            )
            stage_goal_path = round_dir / "stage_goal.md"
            write_text(stage_goal_path, stage_goal)
            context_for_round = self._loop_context_paths(list(context_paths or []), round_entries)
            child_time_budget = self._stage_time_budget(
                stage=stage,
                remaining_seconds=remaining,
                rounds_left=rounds_left,
                round_time_budget_sec=round_time_budget_sec,
            )

            if stage == "lean_formalizer" and workspace and current_target_theorem:
                child_expected_target_header = (
                    expected_target_header
                    if expected_target_header and current_target_theorem == final_target_theorem.strip()
                    else None
                )
                child = self.lean_formalizer_runner.run(
                    workspace=workspace,
                    statement=stage_goal,
                    context_paths=context_for_round,
                    target_theorem=current_target_theorem,
                    target_file=target_file,
                    build_command=build_command or ["lake", "build"],
                    backend=backend,
                    attempts=formalizer_attempts,
                    time_budget_sec=max(1, child_time_budget),
                    attempt_timeout_sec=formalizer_attempt_timeout_sec,
                    build_timeout_sec=formalizer_build_timeout_sec,
                    output_root=run_dir / "lean_formalizer",
                    run_name=f"round-{round_number:03d}-{current_target_theorem}",
                    enable_search=enable_search,
                    max_stalled_attempts=None,
                    expected_target_header=child_expected_target_header,
                    library_module=(
                        library_module
                        if library_module.strip()
                        and final_target_theorem.strip()
                        and current_target_theorem == final_target_theorem.strip()
                        else ""
                    ),
                    promote_to_library=promote_to_library,
                    math_tools_profile=math_tools_profile,
                    install_missing_math_tools=install_missing_math_tools,
                    run_math_tool_smoke=run_math_tool_smoke,
                )
                needs_global_reassessment = self._formalizer_child_needs_global_reassessment(child)
                global_assessment_path = ""
                if needs_global_reassessment:
                    assessment_path = round_dir / "global_assessment.md"
                    self._write_global_assessment(
                        path=assessment_path,
                        statement=statement,
                        current_target_theorem=current_target_theorem,
                        final_target_theorem=final_target_theorem.strip(),
                        child=child,
                    )
                    global_assessment_path = str(assessment_path)
                entry = {
                    "round": round_number,
                    "stage": stage,
                    "status": child.get("status"),
                    "stop_reason": child.get("stop_reason"),
                    "run_dir": child.get("run_dir"),
                    "summary_path": child.get("summary_path"),
                    "target_theorem": current_target_theorem,
                    "next_action": child.get("next_action"),
                    "verified": bool((child.get("best_audit") or {}).get("verified")),
                    "expected_target_header_required": bool(child_expected_target_header),
                    "needs_global_reassessment": needs_global_reassessment,
                    "global_assessment_path": global_assessment_path,
                    "suggested_next_targets": list(child.get("suggested_next_targets") or []),
                    "library_promotion": child.get("library_promotion") or {},
                    "attempts_completed": child.get("attempts_completed"),
                    "progress_velocity": child.get("progress_velocity") or {},
                }
                if entry["verified"] and final_target_theorem.strip() and current_target_theorem == final_target_theorem.strip():
                    round_entries.append(entry)
                    stop_reason = "final_target_verified"
                    write_json(round_dir / "decision.json", entry)
                    break
                if entry["verified"]:
                    completed_target_theorem_set.add(current_target_theorem)
                    current_target_theorem = ""
            else:
                child = self.proof_lab_runner.run(
                    statement=stage_goal,
                    context_paths=context_for_round,
                    backend=backend,
                    attempts=proof_attempts,
                    audits=proof_audits,
                    time_budget_sec=max(1, child_time_budget),
                    attempt_timeout_sec=proof_attempt_timeout_sec,
                    audit_timeout_sec=proof_audit_timeout_sec,
                    source_first=source_first or round_number == 1,
                    grounding_timeout_sec=proof_grounding_timeout_sec,
                    output_root=run_dir / "proof_lab",
                    run_name=f"round-{round_number:03d}",
                    enable_search=enable_search,
                    math_tools_profile=math_tools_profile,
                    install_missing_math_tools=install_missing_math_tools,
                    run_math_tool_smoke=run_math_tool_smoke,
                )
                suggested_target = extract_formalization_target_from_run(
                    Path(str(child.get("run_dir"))),
                    excluded_names=completed_target_theorem_set,
                )
                replacing_after_reassessment = bool(previous and previous.get("needs_global_reassessment"))
                previous_target_theorem = current_target_theorem
                target_replaced = False
                if suggested_target and (not current_target_theorem or replacing_after_reassessment):
                    current_target_theorem = suggested_target
                    target_replaced = suggested_target != previous_target_theorem
                entry = {
                    "round": round_number,
                    "stage": "proof_lab",
                    "status": child.get("status"),
                    "stop_reason": child.get("stop_reason"),
                    "run_dir": child.get("run_dir"),
                    "summary_path": child.get("summary_path"),
                    "suggested_target_theorem": suggested_target,
                    "target_theorem": current_target_theorem,
                    "previous_target_theorem": previous_target_theorem,
                    "target_replaced": target_replaced,
                    "reassessment_of_round": previous.get("round") if replacing_after_reassessment and previous else None,
                    "next_action": child.get("next_action"),
                    "verified": False,
                    "needs_global_reassessment": False,
                    "attempts_completed": child.get("attempts_completed"),
                    "progress_velocity": child.get("progress_velocity") or {},
                }

            if self._should_run_supervisor(
                entry=entry,
                previous_entry=previous,
                supervisor_backend=supervisor_backend,
                supervisor_on_stall=supervisor_on_stall,
                supervisor_every_rounds=supervisor_every_rounds,
            ):
                supervisor_decision = self.global_supervisor.run(
                    run_dir=run_dir,
                    statement=statement,
                    round_number=round_number,
                    current_target_theorem=current_target_theorem,
                    final_target_theorem=final_target_theorem.strip(),
                    completed_target_theorems=completed_target_theorem_set,
                    latest_entry=entry,
                    round_entries=[*round_entries, entry],
                    context_paths=context_for_round,
                    workspace=workspace,
                    target_file=target_file,
                    trigger_reason=self._supervisor_trigger_reason(
                        entry=entry,
                        previous_entry=previous,
                        supervisor_every_rounds=supervisor_every_rounds,
                    ),
                    backend=supervisor_backend,
                    timeout_sec=supervisor_timeout_sec,
                    enable_search=enable_search,
                )
                current_target_theorem = self._apply_supervisor_decision(
                    entry=entry,
                    decision=supervisor_decision,
                    current_target_theorem=current_target_theorem,
                    final_target_theorem=final_target_theorem.strip(),
                    completed_target_theorems=completed_target_theorem_set,
                )

            write_json(round_dir / "decision.json", entry)
            round_entries.append(entry)
            if previous and previous.get("next_action") == entry.get("next_action") and previous.get("status") == entry.get("status"):
                stalled_rounds += 1
            else:
                stalled_rounds = 0
            if max_stalled_rounds > 0 and stalled_rounds >= max_stalled_rounds:
                stop_reason = "stalled"
                break

        status = "verified" if stop_reason == "final_target_verified" else ("partial" if round_entries else "blocked")
        if stop_reason == "rounds_exhausted" and len(round_entries) < max(0, rounds):
            status = "blocked"
        next_action = (
            "Final target theorem is Lean-verified."
            if status == "verified"
            else (
                "Continue with proof-lab global reassessment before the next Lean formalizer round."
                if round_entries and round_entries[-1].get("needs_global_reassessment")
                else "Continue the campaign loop from the latest round summary and current target theorem."
            )
        )
        global_reassessments = [
            {
                "round": entry.get("round"),
                "target_theorem": entry.get("target_theorem"),
                "path": entry.get("global_assessment_path"),
                "suggested_next_targets": list(entry.get("suggested_next_targets") or []),
            }
            for entry in round_entries
            if entry.get("needs_global_reassessment")
        ]
        child_velocities = [dict(entry.get("progress_velocity") or {}) for entry in round_entries]
        progress_velocity = calculate_progress_velocity(
            elapsed_seconds=round(time.monotonic() - started, 3),
            attempts_completed=sum(int(item.get("attempts_completed") or 0) for item in child_velocities),
            progress_deltas=[item.get("net_progress_delta", 0) for item in child_velocities],
            verified_target_count=len(completed_target_theorem_set),
            target_count=1 if final_target_theorem.strip() else len(completed_target_theorem_set),
        )
        payload = {
            "generated_at": utc_now_iso(),
            "status": status,
            "stop_reason": stop_reason,
            "mode": mode,
            "backend": backend,
            "supervisor_backend": supervisor_backend,
            "supervisor_on_stall": supervisor_on_stall,
            "supervisor_every_rounds": supervisor_every_rounds,
            "math_tools_profile": math_tools_profile,
            "install_missing_math_tools": install_missing_math_tools,
            "run_math_tool_smoke": run_math_tool_smoke,
            "run_dir": str(run_dir),
            "statement_path": str(run_dir / "statement.md"),
            "workspace": str(workspace or ""),
            "target_file": str(target_file or ""),
            "expected_target_header_required": bool(expected_target_header),
            "current_target_theorem": current_target_theorem,
            "final_target_theorem": final_target_theorem.strip(),
            "completed_target_theorems": sorted(completed_target_theorem_set),
            "rounds_requested": rounds,
            "rounds_completed": len(round_entries),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "rounds": round_entries,
            "global_reassessments": global_reassessments,
            "supervisor_decisions": [
                {
                    "round": entry.get("round"),
                    "decision": entry.get("supervisor_decision"),
                    "target_theorem": entry.get("supervisor_target_theorem"),
                    "decision_path": entry.get("supervisor_decision_path"),
                    "parsed_decision_path": entry.get("supervisor_parsed_decision_path"),
                    "target_replaced": entry.get("supervisor_target_replaced"),
                }
                for entry in round_entries
                if entry.get("supervisor_decision")
            ],
            "needs_global_reassessment": bool(round_entries and round_entries[-1].get("needs_global_reassessment")),
            "progress_velocity": progress_velocity,
            "summary_path": str(run_dir / "summary.md"),
            "next_action": next_action,
        }
        write_json(run_dir / "report.json", payload)
        write_json(run_dir / "state.json", payload)
        self._write_summary(path=run_dir / "summary.md", payload=payload)
        return payload
