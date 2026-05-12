from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from ara_math.campaign_loop import CampaignLoopRunner, extract_formalization_target_from_run
from ara_math.proof_lab import AIProofLabRunner
from ara_math.workspace import read_json, slugify, utc_now_iso, write_json, write_text


TERMINAL_GOAL_STATUSES = {"verified"}
RETRYABLE_GOAL_STATUSES = {"pending", "ready", "partial", "blocked", "running"}


def _clean_id(value: str, fallback: str) -> str:
    cleaned = slugify(value).replace("-", "_")
    return cleaned or fallback


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _strings(value: Any) -> list[str]:
    return [str(item).strip() for item in _as_list(value) if str(item).strip()]


def _goal_target(goal: dict[str, Any]) -> str:
    return str(goal.get("target_theorem") or goal.get("lean_declaration") or "").strip()


def normalize_goal_manifest(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize a root-driven proof-goal manifest.

    The accepted schema is intentionally small and JSON-native:

    - ``root_goal_id`` points at the goal representing the original theorem.
    - ``goals`` is a list of root/subgoal records.
    - each goal may have ``dependencies``/``depends_on``, ``target_theorem``,
      ``target_file``, ``status``, ``priority``, and ``context_files``.

    Unknown fields are preserved so local campaigns can carry custom metadata.
    """

    manifest = dict(payload or {})
    root_goal_id = str(manifest.get("root_goal_id") or "").strip()
    goals = [dict(item) for item in list(manifest.get("goals") or []) if isinstance(item, dict)]

    root_payload = manifest.get("root_goal")
    if isinstance(root_payload, dict):
        root = dict(root_payload)
        root.setdefault("kind", "root")
        root.setdefault("id", root_goal_id or "root")
        if not any(str(goal.get("id") or "") == str(root["id"]) for goal in goals):
            goals.insert(0, root)
        root_goal_id = str(root["id"])

    if not root_goal_id:
        for goal in goals:
            if str(goal.get("kind") or "") == "root":
                root_goal_id = str(goal.get("id") or "root")
                break
    if not root_goal_id:
        root_goal_id = "root"

    normalized_goals: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw_goal in enumerate(goals):
        goal = dict(raw_goal)
        goal_id = str(goal.get("id") or "").strip()
        if not goal_id:
            seed = str(goal.get("target_theorem") or goal.get("title") or goal.get("statement") or "")
            goal_id = _clean_id(seed, f"goal_{index + 1}")
        if goal_id in seen:
            goal_id = f"{goal_id}_{index + 1}"
        seen.add(goal_id)

        dependencies = _strings(goal.get("dependencies", goal.get("depends_on", [])))
        status = str(goal.get("status") or "pending").strip().lower()
        if status not in TERMINAL_GOAL_STATUSES | RETRYABLE_GOAL_STATUSES | {"skipped"}:
            status = "pending"

        goal["id"] = goal_id
        goal["kind"] = str(goal.get("kind") or ("root" if goal_id == root_goal_id else "subgoal"))
        goal["dependencies"] = dependencies
        goal.pop("depends_on", None)
        goal["context_files"] = _strings(goal.get("context_files", goal.get("context_file", [])))
        goal.pop("context_file", None)
        goal["target_theorem"] = _goal_target(goal)
        goal["target_file"] = str(goal.get("target_file") or "").strip()
        goal["statement"] = str(goal.get("statement") or goal.get("goal") or goal.get("title") or "").strip()
        goal["status"] = status
        goal["priority"] = int(goal.get("priority") or (10_000 if goal["kind"] == "root" else 100 + index))
        goal["run_history"] = list(goal.get("run_history") or [])
        normalized_goals.append(goal)

    if root_goal_id not in {str(goal["id"]) for goal in normalized_goals}:
        normalized_goals.insert(
            0,
            {
                "id": root_goal_id,
                "kind": "root",
                "statement": str(manifest.get("statement") or manifest.get("root_statement") or "").strip(),
                "target_theorem": str(manifest.get("target_theorem") or "").strip(),
                "target_file": str(manifest.get("target_file") or "").strip(),
                "dependencies": [],
                "context_files": [],
                "status": "pending",
                "priority": 10_000,
                "run_history": [],
            },
        )

    settings = dict(manifest.get("settings") or {})
    settings["context_files"] = _strings(settings.get("context_files", settings.get("context_file", [])))
    settings.pop("context_file", None)
    manifest["version"] = int(manifest.get("version") or 1)
    manifest["root_goal_id"] = root_goal_id
    manifest["goals"] = normalized_goals
    manifest["settings"] = settings
    manifest.setdefault("gap_reviews", [])
    return manifest


class GoalDrivenCampaignRunner:
    """Root-goal driven loop over dependent proof obligations.

    This runner is a scheduling layer above ``CampaignLoopRunner``.  It keeps a
    durable goal graph, proves ready child goals first, then returns to the root
    theorem and records a root-gap review after each phase.
    """

    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.campaign_runner = CampaignLoopRunner(repo_root=repo_root)
        self.proof_lab_runner = AIProofLabRunner(repo_root=repo_root)

    def _new_run_dir(self, *, output_root: Path, run_name: str | None) -> Path:
        base = slugify(run_name or f"goal-campaign-{utc_now_iso()}")
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

    def _goals_by_id(self, manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
        return {str(goal["id"]): goal for goal in list(manifest.get("goals") or [])}

    def _root_goal(self, manifest: dict[str, Any]) -> dict[str, Any]:
        goals_by_id = self._goals_by_id(manifest)
        return goals_by_id[str(manifest["root_goal_id"])]

    def _dependency_status(self, goal: dict[str, Any], goals_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
        missing: list[str] = []
        unverified: list[str] = []
        for dependency in list(goal.get("dependencies") or []):
            dependency_goal = goals_by_id.get(str(dependency))
            if dependency_goal is None:
                missing.append(str(dependency))
            elif dependency_goal.get("status") != "verified":
                unverified.append(str(dependency))
        return {
            "ready": not missing and not unverified,
            "missing": missing,
            "unverified": unverified,
        }

    def _select_next_goal(
        self,
        manifest: dict[str, Any],
        *,
        max_goal_runs: int,
    ) -> dict[str, Any] | None:
        goals_by_id = self._goals_by_id(manifest)
        root_id = str(manifest["root_goal_id"])
        ready: list[dict[str, Any]] = []
        for goal in list(manifest.get("goals") or []):
            if goal.get("status") in TERMINAL_GOAL_STATUSES or goal.get("status") == "skipped":
                continue
            if max_goal_runs > 0 and len(list(goal.get("run_history") or [])) >= max_goal_runs:
                continue
            dependency_state = self._dependency_status(goal, goals_by_id)
            goal["dependency_state"] = dependency_state
            if dependency_state["ready"]:
                ready.append(goal)

        if not ready:
            return None

        non_root_ready = [goal for goal in ready if str(goal.get("id")) != root_id]
        candidates = non_root_ready or ready
        return sorted(candidates, key=lambda goal: (int(goal.get("priority") or 0), str(goal.get("id"))))[0]

    def _verified_target_theorems(self, manifest: dict[str, Any]) -> list[str]:
        names: list[str] = []
        for goal in list(manifest.get("goals") or []):
            if goal.get("status") == "verified" and _goal_target(goal):
                names.append(_goal_target(goal))
        return sorted(set(names))

    def _all_known_target_theorems(self, manifest: dict[str, Any]) -> set[str]:
        names = {_goal_target(goal) for goal in list(manifest.get("goals") or []) if _goal_target(goal)}
        return {name for name in names if name}

    def _goal_context_paths(
        self,
        manifest: dict[str, Any],
        goal: dict[str, Any],
        extra_context_paths: list[Path],
    ) -> list[Path]:
        paths: list[Path] = list(extra_context_paths)
        settings = dict(manifest.get("settings") or {})
        paths.extend(Path(path) for path in list(settings.get("context_files") or []))
        paths.extend(Path(path) for path in list(goal.get("context_files") or []))
        seen: set[str] = set()
        deduped: list[Path] = []
        for path in paths:
            key = str(path.expanduser().resolve()) if path.exists() else str(path)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(path)
        return deduped

    def _goal_statement(self, manifest: dict[str, Any], goal: dict[str, Any]) -> str:
        root = self._root_goal(manifest)
        goals_by_id = self._goals_by_id(manifest)
        verified = [item for item in list(manifest.get("goals") or []) if item.get("status") == "verified"]
        open_goals = [item for item in list(manifest.get("goals") or []) if item.get("status") != "verified"]
        dependency_lines = []
        for dependency in list(goal.get("dependencies") or []):
            dependency_goal = goals_by_id.get(str(dependency))
            dependency_lines.append(
                f"- `{dependency}`: {dependency_goal.get('status') if dependency_goal else 'missing'}"
            )
        if not dependency_lines:
            dependency_lines = ["- none"]

        return "\n".join(
            [
                "# ARA Root-Goal Driven Proof Campaign",
                "",
                "## Root Objective",
                "",
                str(root.get("statement") or "<root statement missing>").strip(),
                "",
                f"- Root goal id: `{root.get('id')}`",
                f"- Root Lean target: `{_goal_target(root) or '<none>'}`",
                "",
                "## Current Subgoal",
                "",
                str(goal.get("statement") or "<subgoal statement missing>").strip(),
                "",
                f"- Subgoal id: `{goal.get('id')}`",
                f"- Subgoal Lean target: `{_goal_target(goal) or '<none>'}`",
                f"- Target file: `{goal.get('target_file') or '<search all Lean files>'}`",
                "",
                "## Dependencies",
                "",
                *dependency_lines,
                "",
                "## Current Goal Graph Status",
                "",
                f"- Verified goals: `{', '.join(str(item.get('id')) for item in verified) or '<none>'}`",
                f"- Open goals: `{', '.join(str(item.get('id')) for item in open_goals) or '<none>'}`",
                "",
                "## Loop Discipline",
                "",
                "- Treat the root theorem as the total objective.",
                "- Prove the current subgoal only insofar as it removes a blocker on the root theorem.",
                "- Do not weaken any Lean declaration or introduce trusted assumptions.",
                "- When this subgoal closes, compare the remaining goal graph against the root objective and name the next missing theorem-level obligation.",
                "- If the current subgoal is not the right next blocker, state the replacement target exactly.",
                "",
            ]
        )

    def _write_gap_review(
        self,
        *,
        manifest: dict[str, Any],
        run_dir: Path,
        outer_round: int,
        latest_goal: dict[str, Any] | None,
        latest_report: dict[str, Any] | None,
        backend: str,
        context_paths: list[Path],
        time_budget_sec: int,
        attempt_timeout_sec: int,
        enable_search: bool,
        dynamic_goal_creation: bool,
    ) -> dict[str, Any]:
        root = self._root_goal(manifest)
        goals = list(manifest.get("goals") or [])
        verified = [goal for goal in goals if goal.get("status") == "verified"]
        open_goals = [goal for goal in goals if goal.get("status") != "verified"]
        prompt = "\n".join(
            [
                "# Root Gap Review",
                "",
                "Compare the current goal graph against the root objective.",
                "",
                "## Root Objective",
                "",
                str(root.get("statement") or "").strip(),
                "",
                f"- Root Lean target: `{_goal_target(root) or '<none>'}`",
                "",
                "## Latest Phase",
                "",
                f"- Latest goal: `{(latest_goal or {}).get('id', '<none>')}`",
                f"- Latest status: `{(latest_goal or {}).get('status', '<none>')}`",
                f"- Latest child stop reason: `{(latest_report or {}).get('stop_reason', '')}`",
                "",
                "## Verified Goals",
                "",
                *[
                    f"- `{goal.get('id')}` -> `{_goal_target(goal) or '<no Lean target>'}`"
                    for goal in verified
                ],
                "- none" if not verified else "",
                "",
                "## Open Goals",
                "",
                *[
                    f"- `{goal.get('id')}` [{goal.get('status')}] -> `{_goal_target(goal) or '<no Lean target>'}`"
                    for goal in open_goals
                ],
                "- none" if not open_goals else "",
                "",
                "Required output:",
                "- State whether the root theorem is now closed.",
                "- If not closed, identify the first missing theorem-level obligation.",
                "- If a new Lean target is needed, provide it as a Lean theorem/lemma declaration or in a `Formalization target:` field.",
                "",
            ]
        )
        review_dir = run_dir / "root_gap_reviews" / f"round_{outer_round:03d}"
        review_dir.mkdir(parents=True, exist_ok=True)
        write_text(review_dir / "prompt.md", prompt)

        review: dict[str, Any] = {
            "round": outer_round,
            "generated_at": utc_now_iso(),
            "backend": backend,
            "status": "recorded",
            "latest_goal_id": str((latest_goal or {}).get("id") or ""),
            "verified_goal_ids": [str(goal.get("id")) for goal in verified],
            "open_goal_ids": [str(goal.get("id")) for goal in open_goals],
            "suggested_target_theorem": "",
            "created_goal_id": "",
            "run_dir": str(review_dir),
        }

        if backend != "none":
            child = self.proof_lab_runner.run(
                statement=prompt,
                context_paths=context_paths,
                backend=backend,
                attempts=1,
                audits=1,
                time_budget_sec=max(1, time_budget_sec),
                attempt_timeout_sec=max(1, attempt_timeout_sec),
                audit_timeout_sec=max(1, min(300, attempt_timeout_sec)),
                grounding_timeout_sec=max(1, min(300, attempt_timeout_sec)),
                source_first=False,
                output_root=review_dir,
                run_name="proof-lab",
                enable_search=enable_search,
            )
            suggested_target = extract_formalization_target_from_run(
                Path(str(child.get("run_dir"))),
                excluded_names=self._all_known_target_theorems(manifest),
            )
            review.update(
                {
                    "status": child.get("status"),
                    "stop_reason": child.get("stop_reason"),
                    "proof_lab_run_dir": child.get("run_dir"),
                    "summary_path": child.get("summary_path"),
                    "suggested_target_theorem": suggested_target,
                }
            )
            if dynamic_goal_creation and suggested_target:
                created = self._create_dynamic_goal(manifest, suggested_target=suggested_target, root=root)
                review["created_goal_id"] = created["id"]

        write_json(review_dir / "review.json", review)
        manifest.setdefault("gap_reviews", []).append(review)
        return review

    def _create_dynamic_goal(
        self,
        manifest: dict[str, Any],
        *,
        suggested_target: str,
        root: dict[str, Any],
    ) -> dict[str, Any]:
        base_id = _clean_id(suggested_target, "dynamic_goal")
        existing_ids = {str(goal.get("id")) for goal in list(manifest.get("goals") or [])}
        goal_id = base_id
        suffix = 2
        while goal_id in existing_ids:
            goal_id = f"{base_id}_{suffix}"
            suffix += 1
        verified_non_root = [
            str(goal.get("id"))
            for goal in list(manifest.get("goals") or [])
            if goal.get("status") == "verified" and str(goal.get("id")) != str(root.get("id"))
        ]
        goal = {
            "id": goal_id,
            "kind": "subgoal",
            "statement": (
                "Root-gap review identified this as the next missing theorem-level obligation for "
                f"root goal `{root.get('id')}`."
            ),
            "target_theorem": suggested_target,
            "target_file": str(root.get("target_file") or ""),
            "dependencies": verified_non_root,
            "context_files": [],
            "status": "pending",
            "priority": 500 + len(list(manifest.get("goals") or [])),
            "created_by": "root_gap_review",
            "created_at": utc_now_iso(),
            "run_history": [],
        }
        manifest.setdefault("goals", []).append(goal)
        return goal

    def _write_summary(self, *, path: Path, payload: dict[str, Any]) -> None:
        lines = [
            "# ARA Goal-Driven Campaign Report",
            "",
            f"- Status: {payload.get('status')}",
            f"- Stop reason: {payload.get('stop_reason')}",
            f"- Root goal: `{payload.get('root_goal_id')}`",
            f"- Rounds completed: {payload.get('rounds_completed')} / {payload.get('rounds_requested')}",
            f"- Elapsed seconds: {payload.get('elapsed_seconds')}",
            "",
            "## Goals",
            "",
        ]
        for goal in list(payload.get("goals") or []):
            lines.append(
                f"- `{goal.get('id')}` [{goal.get('status')}]: "
                f"`{goal.get('target_theorem') or '<no Lean target>'}`"
            )
        lines.extend(["", "## Next Action", "", str(payload.get("next_action") or ""), ""])
        write_text(path, "\n".join(lines))

    def run(
        self,
        *,
        manifest_path: Path,
        workspace: Path | None = None,
        build_command: list[str] | None = None,
        context_paths: list[Path] | None = None,
        backend: str = "codex",
        rounds: int = 12,
        time_budget_sec: int = 7200,
        child_rounds: int = 2,
        child_time_budget_sec: int = 1800,
        child_attempts: int = 6,
        child_attempt_timeout_sec: int = 900,
        child_build_timeout_sec: int = 300,
        gap_review_time_budget_sec: int = 600,
        gap_review_attempt_timeout_sec: int = 300,
        mode: str = "hybrid",
        enable_search: bool = False,
        output_root: Path | None = None,
        run_name: str | None = None,
        max_goal_runs: int = 0,
        write_back_manifest: bool = True,
        dynamic_goal_creation: bool = True,
    ) -> dict[str, Any]:
        manifest_path = manifest_path.expanduser().resolve()
        if not manifest_path.exists():
            raise FileNotFoundError(f"Goal manifest does not exist: {manifest_path}")
        manifest = normalize_goal_manifest(read_json(manifest_path, default={}))
        settings = dict(manifest.get("settings") or {})
        if workspace is None and str(settings.get("workspace") or "").strip():
            workspace = Path(str(settings["workspace"]))
        if build_command is None:
            configured = settings.get("build_command")
            build_command = [str(item) for item in configured] if isinstance(configured, list) else ["lake", "build"]

        output_root = output_root or (self.repo_root / "artifacts" / "goal_campaigns")
        run_dir = self._new_run_dir(output_root=output_root, run_name=run_name)
        rounds_dir = run_dir / "rounds"
        rounds_dir.mkdir(parents=True, exist_ok=True)
        write_json(run_dir / "initial_manifest.json", manifest)
        write_text(run_dir / "manifest_source.txt", str(manifest_path) + "\n")

        started = time.monotonic()
        deadline = started + max(1, time_budget_sec)
        round_entries: list[dict[str, Any]] = []
        stop_reason = "rounds_exhausted"
        latest_goal: dict[str, Any] | None = None
        latest_report: dict[str, Any] | None = None
        extra_context_paths = list(context_paths or [])

        for offset in range(max(0, rounds)):
            remaining = int(deadline - time.monotonic())
            if remaining <= 0:
                stop_reason = "time_budget_exhausted"
                break
            outer_round = offset + 1
            selected = self._select_next_goal(manifest, max_goal_runs=max_goal_runs)
            if selected is None:
                stop_reason = "no_ready_goals"
                self._write_gap_review(
                    manifest=manifest,
                    run_dir=run_dir,
                    outer_round=outer_round,
                    latest_goal=latest_goal,
                    latest_report=latest_report,
                    backend=backend,
                    context_paths=extra_context_paths,
                    time_budget_sec=min(gap_review_time_budget_sec, max(1, remaining)),
                    attempt_timeout_sec=gap_review_attempt_timeout_sec,
                    enable_search=enable_search,
                    dynamic_goal_creation=dynamic_goal_creation,
                )
                selected = self._select_next_goal(manifest, max_goal_runs=max_goal_runs)
                if selected is None:
                    break

            selected["status"] = "running"
            round_dir = rounds_dir / f"round_{outer_round:03d}_{selected['id']}"
            round_dir.mkdir(parents=True, exist_ok=True)
            statement = self._goal_statement(manifest, selected)
            write_text(round_dir / "stage_goal.md", statement)
            context_for_goal = self._goal_context_paths(manifest, selected, extra_context_paths)
            child_budget = min(max(1, child_time_budget_sec), max(1, int(deadline - time.monotonic())))
            child_mode = mode
            if not workspace or not _goal_target(selected):
                child_mode = "proof-lab"

            child_report = self.campaign_runner.run(
                statement=statement,
                context_paths=context_for_goal,
                workspace=workspace,
                final_target_theorem=_goal_target(selected),
                initial_target_theorem=_goal_target(selected),
                completed_target_theorems=self._verified_target_theorems(manifest),
                target_file=Path(str(selected.get("target_file"))) if str(selected.get("target_file") or "") else None,
                build_command=build_command,
                backend=backend,
                mode=child_mode,
                rounds=max(1, child_rounds),
                time_budget_sec=max(1, child_budget),
                proof_attempts=1,
                proof_audits=1,
                proof_attempt_timeout_sec=gap_review_attempt_timeout_sec,
                proof_audit_timeout_sec=min(300, gap_review_attempt_timeout_sec),
                proof_grounding_timeout_sec=min(300, gap_review_attempt_timeout_sec),
                formalizer_attempts=max(0, child_attempts),
                formalizer_attempt_timeout_sec=max(1, child_attempt_timeout_sec),
                formalizer_build_timeout_sec=max(1, child_build_timeout_sec),
                enable_search=enable_search,
                output_root=run_dir / "child_campaigns",
                run_name=f"round-{outer_round:03d}-{selected['id']}",
                max_stalled_rounds=0,
                round_time_budget_sec=0,
            )
            verified = child_report.get("status") == "verified"
            selected["status"] = "verified" if verified else str(child_report.get("status") or "partial")
            selected["updated_at"] = utc_now_iso()
            run_record = {
                "round": outer_round,
                "run_dir": child_report.get("run_dir"),
                "summary_path": child_report.get("summary_path"),
                "status": child_report.get("status"),
                "stop_reason": child_report.get("stop_reason"),
                "target_theorem": _goal_target(selected),
            }
            selected.setdefault("run_history", []).append(run_record)
            latest_goal = selected
            latest_report = child_report
            entry = {
                "round": outer_round,
                "goal_id": selected["id"],
                "goal_status": selected["status"],
                "target_theorem": _goal_target(selected),
                "child_run_dir": child_report.get("run_dir"),
                "child_status": child_report.get("status"),
                "child_stop_reason": child_report.get("stop_reason"),
            }
            write_json(round_dir / "decision.json", entry)
            round_entries.append(entry)

            self._write_gap_review(
                manifest=manifest,
                run_dir=run_dir,
                outer_round=outer_round,
                latest_goal=selected,
                latest_report=child_report,
                backend=backend,
                context_paths=context_for_goal,
                time_budget_sec=min(gap_review_time_budget_sec, max(1, int(deadline - time.monotonic()))),
                attempt_timeout_sec=gap_review_attempt_timeout_sec,
                enable_search=enable_search,
                dynamic_goal_creation=dynamic_goal_creation,
            )

            if selected["id"] == manifest["root_goal_id"] and selected["status"] == "verified":
                stop_reason = "root_goal_verified"
                break

            if write_back_manifest:
                manifest["updated_at"] = utc_now_iso()
                write_json(manifest_path, manifest)
            write_json(run_dir / "state.json", manifest)

        root = self._root_goal(manifest)
        if root.get("status") == "verified":
            status = "verified"
            stop_reason = "root_goal_verified"
        elif round_entries:
            status = "partial"
        else:
            status = "blocked"

        if write_back_manifest:
            manifest["updated_at"] = utc_now_iso()
            write_json(manifest_path, manifest)
        write_json(run_dir / "final_manifest.json", manifest)

        next_ready = self._select_next_goal(manifest, max_goal_runs=max_goal_runs)
        next_action = (
            "Root goal is Lean-verified."
            if status == "verified"
            else (
                f"Continue with goal `{next_ready['id']}`."
                if next_ready is not None
                else "Run a root-gap review or add a new subgoal; no ready unverified goal is currently selectable."
            )
        )
        payload = {
            "generated_at": utc_now_iso(),
            "status": status,
            "stop_reason": stop_reason,
            "run_dir": str(run_dir),
            "manifest_path": str(manifest_path),
            "workspace": str(workspace or ""),
            "root_goal_id": str(manifest["root_goal_id"]),
            "rounds_requested": rounds,
            "rounds_completed": len(round_entries),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "rounds": round_entries,
            "goals": [
                {
                    "id": str(goal.get("id")),
                    "kind": str(goal.get("kind")),
                    "status": str(goal.get("status")),
                    "target_theorem": _goal_target(goal),
                    "dependencies": list(goal.get("dependencies") or []),
                    "run_count": len(list(goal.get("run_history") or [])),
                }
                for goal in list(manifest.get("goals") or [])
            ],
            "gap_reviews": list(manifest.get("gap_reviews") or []),
            "summary_path": str(run_dir / "summary.md"),
            "next_action": next_action,
        }
        write_json(run_dir / "report.json", payload)
        write_json(run_dir / "state.json", manifest)
        self._write_summary(path=run_dir / "summary.md", payload=payload)
        return payload


def write_goal_manifest_template(
    path: Path,
    *,
    root_statement: str,
    root_target_theorem: str = "",
    root_target_file: str = "",
    workspace: str = "",
    build_command: list[str] | None = None,
) -> dict[str, Any]:
    manifest = normalize_goal_manifest(
        {
            "version": 1,
            "root_goal_id": "root",
            "settings": {
                "workspace": workspace,
                "build_command": build_command or ["lake", "build"],
            },
            "goals": [
                {
                    "id": "root",
                    "kind": "root",
                    "statement": root_statement,
                    "target_theorem": root_target_theorem,
                    "target_file": root_target_file,
                    "dependencies": [],
                    "status": "pending",
                    "priority": 10_000,
                }
            ],
        }
    )
    write_json(path, manifest)
    return manifest
