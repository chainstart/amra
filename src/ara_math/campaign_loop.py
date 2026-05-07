from __future__ import annotations

import re
import shlex
import time
from pathlib import Path
from typing import Any

from ara_math.lean_formalizer import LeanFormalizerRunner, collect_proof_lab_context_paths
from ara_math.proof_lab import AIProofLabRunner
from ara_math.workspace import read_text, slugify, utc_now_iso, write_json, write_text


TARGET_DECL_PATTERN = re.compile(r"\b(?:theorem|lemma)\s+([A-Za-z_][A-Za-z0-9_'.]*)")


def extract_first_theorem_name(text: str) -> str:
    """Return the first Lean theorem/lemma name mentioned in a text blob."""

    match = TARGET_DECL_PATTERN.search(text)
    return match.group(1) if match else ""


def extract_formalization_target_from_run(run_dir: Path) -> str:
    """Find a likely Lean target theorem from a proof-lab run.

    This intentionally uses a simple source-order heuristic.  Proof-lab outputs
    are free-form Markdown, so the loop treats this as a stage suggestion, not
    a trusted theorem statement.
    """

    candidates: list[Path] = []
    for subdir in ("audits", "attempts"):
        directory = run_dir / subdir
        if directory.exists():
            candidates.extend(sorted(directory.glob("*_output.md"), reverse=True))
    candidates.extend([run_dir / "summary.md", run_dir / "grounding" / "source_grounding_output.md"])
    for path in candidates:
        if not path.exists():
            continue
        name = extract_first_theorem_name(read_text(path))
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
            summary_path = Path(str(entry.get("summary_path") or ""))
            if not summary_path.exists():
                continue
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
        history: str,
    ) -> str:
        target_lines = [
            f"- Current stage theorem: `{current_target_theorem or '<none yet>'}`",
            f"- Final theorem: `{final_target_theorem or '<not fixed; derive theorem-level targets>'}`",
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
        if mode == "proof-lab":
            return "proof_lab"
        if mode == "lean-formalizer":
            return "lean_formalizer" if workspace and current_target_theorem else "proof_lab"
        if mode == "hybrid":
            if not previous_entry:
                return "proof_lab"
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

    def _loop_context_paths(self, base_context_paths: list[Path], round_entries: list[dict[str, Any]]) -> list[Path]:
        paths = list(base_context_paths)
        for entry in round_entries[-4:]:
            run_dir = Path(str(entry.get("run_dir") or ""))
            if not run_dir.exists():
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
            lines.append(
                f"- Round {entry.get('round')}: {entry.get('stage')} -> "
                f"{entry.get('status')} ({entry.get('stop_reason') or entry.get('next_action') or ''})"
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
        enable_search: bool = False,
        output_root: Path | None = None,
        run_name: str | None = None,
        max_stalled_rounds: int = 0,
    ) -> dict[str, Any]:
        if not statement.strip():
            raise ValueError("Campaign loop statement must not be empty.")
        if mode not in {"auto", "hybrid", "proof-lab", "lean-formalizer"}:
            raise ValueError(f"Unsupported campaign loop mode: {mode}")

        output_root = output_root or (self.repo_root / "artifacts" / "campaign_loop")
        run_dir = self._new_run_dir(output_root=output_root, run_name=run_name)
        rounds_dir = run_dir / "rounds"
        rounds_dir.mkdir(parents=True, exist_ok=True)
        write_text(run_dir / "statement.md", statement.strip() + "\n")

        started = time.monotonic()
        deadline = started + max(1, time_budget_sec)
        round_entries: list[dict[str, Any]] = []
        current_target_theorem = initial_target_theorem.strip() or final_target_theorem.strip()
        stop_reason = "rounds_exhausted"
        stalled_rounds = 0

        for offset in range(max(0, rounds)):
            remaining = int(deadline - time.monotonic())
            if remaining <= 0:
                stop_reason = "time_budget_exhausted"
                break
            round_number = offset + 1
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
                history=history,
            )
            stage_goal_path = round_dir / "stage_goal.md"
            write_text(stage_goal_path, stage_goal)
            context_for_round = self._loop_context_paths(list(context_paths or []), round_entries)

            if stage == "lean_formalizer" and workspace and current_target_theorem:
                child = self.lean_formalizer_runner.run(
                    workspace=workspace,
                    statement=stage_goal,
                    context_paths=context_for_round,
                    target_theorem=current_target_theorem,
                    target_file=target_file,
                    build_command=build_command or ["lake", "build"],
                    backend=backend,
                    attempts=formalizer_attempts,
                    time_budget_sec=min(max(1, remaining), max(1, time_budget_sec // max(1, rounds))),
                    attempt_timeout_sec=formalizer_attempt_timeout_sec,
                    build_timeout_sec=formalizer_build_timeout_sec,
                    output_root=run_dir / "lean_formalizer",
                    run_name=f"round-{round_number:03d}-{current_target_theorem}",
                    enable_search=enable_search,
                    max_stalled_attempts=None,
                )
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
                }
                if entry["verified"] and final_target_theorem.strip() and current_target_theorem == final_target_theorem.strip():
                    round_entries.append(entry)
                    stop_reason = "final_target_verified"
                    write_json(round_dir / "decision.json", entry)
                    break
                if entry["verified"]:
                    current_target_theorem = ""
            else:
                child = self.proof_lab_runner.run(
                    statement=stage_goal,
                    context_paths=context_for_round,
                    backend=backend,
                    attempts=proof_attempts,
                    audits=proof_audits,
                    time_budget_sec=min(max(1, remaining), max(1, time_budget_sec // max(1, rounds))),
                    attempt_timeout_sec=proof_attempt_timeout_sec,
                    audit_timeout_sec=proof_audit_timeout_sec,
                    source_first=source_first or round_number == 1,
                    grounding_timeout_sec=proof_grounding_timeout_sec,
                    output_root=run_dir / "proof_lab",
                    run_name=f"round-{round_number:03d}",
                    enable_search=enable_search,
                )
                suggested_target = extract_formalization_target_from_run(Path(str(child.get("run_dir"))))
                if suggested_target and not current_target_theorem:
                    current_target_theorem = suggested_target
                entry = {
                    "round": round_number,
                    "stage": "proof_lab",
                    "status": child.get("status"),
                    "stop_reason": child.get("stop_reason"),
                    "run_dir": child.get("run_dir"),
                    "summary_path": child.get("summary_path"),
                    "suggested_target_theorem": suggested_target,
                    "target_theorem": current_target_theorem,
                    "next_action": child.get("next_action"),
                    "verified": False,
                }

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
            else "Continue the campaign loop from the latest round summary and current target theorem."
        )
        payload = {
            "generated_at": utc_now_iso(),
            "status": status,
            "stop_reason": stop_reason,
            "mode": mode,
            "backend": backend,
            "run_dir": str(run_dir),
            "statement_path": str(run_dir / "statement.md"),
            "workspace": str(workspace or ""),
            "target_file": str(target_file or ""),
            "current_target_theorem": current_target_theorem,
            "final_target_theorem": final_target_theorem.strip(),
            "rounds_requested": rounds,
            "rounds_completed": len(round_entries),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "rounds": round_entries,
            "summary_path": str(run_dir / "summary.md"),
            "next_action": next_action,
        }
        write_json(run_dir / "report.json", payload)
        write_json(run_dir / "state.json", payload)
        self._write_summary(path=run_dir / "summary.md", payload=payload)
        return payload
