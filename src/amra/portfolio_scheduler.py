from __future__ import annotations

import json
import os
import shutil
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

from amra.core.workspace import slugify, utc_now_iso, write_json


LOCK_FILE_NAMES = {
    "state": "state.lock",
    "formal": "formal.lock",
    "library": "library-promotion.lock",
}
APPROVED_REVIEW_STATUSES = {"approved", "accepted", "pass", "passed", "reviewed"}


class LockAcquisitionError(RuntimeError):
    """Raised when another worker holds a non-expired portfolio lock."""


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _parse_started_at(value: str) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _lock_is_expired(payload: dict[str, Any]) -> bool:
    started_at = _parse_started_at(str(payload.get("started_at") or ""))
    timeout_seconds = int(payload.get("timeout_seconds") or payload.get("timeout") or 0)
    if started_at is None or timeout_seconds <= 0:
        return False
    return datetime.now(timezone.utc) >= started_at + timedelta(seconds=timeout_seconds)


def _safe_copy_formal_workspace(source: Path, destination: Path) -> None:
    if not source.exists():
        destination.mkdir(parents=True, exist_ok=True)
        return
    ignore = shutil.ignore_patterns(".locks")
    shutil.copytree(source, destination, dirs_exist_ok=True, ignore=ignore)


def calculate_progress_velocity(
    *,
    started_at_monotonic: float | None = None,
    elapsed_seconds: float | None = None,
    attempts_completed: int = 0,
    episodes_completed: int = 0,
    progress_deltas: Iterable[int | float] = (),
    verified_target_count: int = 0,
    target_count: int = 0,
) -> dict[str, Any]:
    """Return stable progress-per-hour metrics for run reports."""

    if elapsed_seconds is None:
        elapsed_seconds = max(0.0, time.monotonic() - started_at_monotonic) if started_at_monotonic else 0.0
    elapsed_seconds = max(0.0, float(elapsed_seconds))
    hours = elapsed_seconds / 3600.0 if elapsed_seconds > 0 else 0.0
    deltas = [float(delta) for delta in progress_deltas]
    positive_delta = sum(delta for delta in deltas if delta > 0)
    total_delta = sum(deltas)

    def per_hour(value: float) -> float:
        return round(value / hours, 6) if hours > 0 else 0.0

    return {
        "schema_version": "amra.progress_velocity.v1",
        "elapsed_seconds": round(elapsed_seconds, 3),
        "attempts_completed": int(attempts_completed),
        "episodes_completed": int(episodes_completed),
        "positive_progress_delta": round(positive_delta, 6),
        "net_progress_delta": round(total_delta, 6),
        "progress_delta_per_hour": per_hour(positive_delta),
        "attempts_per_hour": per_hour(float(attempts_completed)),
        "episodes_per_hour": per_hour(float(episodes_completed)),
        "verified_target_count": int(verified_target_count),
        "target_count": int(target_count),
        "verified_targets_per_hour": per_hour(float(verified_target_count)),
    }


@dataclass
class PortfolioFileLock:
    path: Path
    owner: str
    timeout_seconds: int = 3600
    resource: str = ""
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        self.path = self.path.expanduser().resolve()
        self.timeout_seconds = max(1, int(self.timeout_seconds))
        self._token = f"{os.getpid()}:{time.monotonic_ns()}"
        self._acquired = False

    def _payload(self) -> dict[str, Any]:
        return {
            "schema_version": "amra.portfolio_lock.v1",
            "owner": self.owner,
            "pid": os.getpid(),
            "started_at": utc_now_iso(),
            "timeout": self.timeout_seconds,
            "timeout_seconds": self.timeout_seconds,
            "resource": self.resource,
            "token": self._token,
            "metadata": self.metadata or {},
        }

    def acquire(self) -> dict[str, Any]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = self._payload()
        text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
        while True:
            try:
                fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            except FileExistsError as exc:
                current = _read_json(self.path, {})
                if isinstance(current, dict) and _lock_is_expired(current):
                    try:
                        self.path.unlink()
                    except FileNotFoundError:
                        pass
                    continue
                holder = current.get("owner", "unknown") if isinstance(current, dict) else "unknown"
                raise LockAcquisitionError(f"Lock is already held by {holder}: {self.path}") from exc
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(text)
            self._acquired = True
            return payload

    def release(self) -> None:
        if not self._acquired:
            return
        try:
            current = _read_json(self.path, {})
            if not isinstance(current, dict) or current.get("token") == self._token:
                self.path.unlink(missing_ok=True)
        finally:
            self._acquired = False

    def __enter__(self) -> "PortfolioFileLock":
        self.acquire()
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        del exc_type, exc, traceback
        self.release()


@dataclass(frozen=True)
class WorkspaceReservation:
    problem_id: str
    run_id: str
    project_dir: Path
    canonical_workspace: Path
    isolated_workspace: Path
    locks_dir: Path

    def as_payload(self, *, repo_root: Path | None = None) -> dict[str, Any]:
        root = repo_root or self.project_dir.parent.parent
        return {
            "problem_id": self.problem_id,
            "run_id": self.run_id,
            "project_dir": _relative(self.project_dir, root),
            "canonical_workspace": _relative(self.canonical_workspace, root),
            "isolated_workspace": _relative(self.isolated_workspace, root),
            "workspace_policy": "isolated",
            "locks": {
                "state": _relative(self.locks_dir / LOCK_FILE_NAMES["state"], root),
                "formal": _relative(self.locks_dir / LOCK_FILE_NAMES["formal"], root),
                "library_promotion": _relative(self.locks_dir / LOCK_FILE_NAMES["library"], root),
            },
        }


class PortfolioAttackScheduler:
    """Schedule promoted AMRA targets without sharing writable Lean workspaces."""

    def __init__(self, *, repo_root: Path, owner: str | None = None, lock_timeout_seconds: int = 3600) -> None:
        self.repo_root = repo_root.expanduser().resolve()
        self.owner = owner or f"pid-{os.getpid()}"
        self.lock_timeout_seconds = max(1, int(lock_timeout_seconds))

    def lock(self, lock_root: Path, name: str, *, owner: str | None = None, resource: str = "") -> PortfolioFileLock:
        if name not in LOCK_FILE_NAMES:
            raise ValueError(f"Unknown portfolio lock name: {name}")
        return PortfolioFileLock(
            path=lock_root / ".locks" / LOCK_FILE_NAMES[name],
            owner=owner or self.owner,
            timeout_seconds=self.lock_timeout_seconds,
            resource=resource,
        )

    def state_lock(self, project_dir: Path, *, owner: str | None = None) -> PortfolioFileLock:
        return self.lock(project_dir, "state", owner=owner, resource=str(project_dir))

    def formal_lock(self, project_dir: Path, *, owner: str | None = None) -> PortfolioFileLock:
        return self.lock(project_dir, "formal", owner=owner, resource=str(project_dir / "formal"))

    def library_promotion_lock(
        self,
        project_dir: Path,
        *,
        module: str,
        owner: str | None = None,
    ) -> PortfolioFileLock:
        return self.lock(project_dir, "library", owner=owner, resource=f"library:{module}")

    def promoted_problem_ids(self, campaign_dir: Path) -> set[str]:
        payload = _read_json(campaign_dir / "promotion_queue.json", {"items": []})
        items = payload.get("items", []) if isinstance(payload, dict) else []
        return {str(item.get("problem_id", "")).strip() for item in items if str(item.get("problem_id", "")).strip()}

    def can_allocate_attack_budget(self, *, problem_id: str, promoted_problem_ids: Iterable[str]) -> bool:
        return problem_id.strip() in {item.strip() for item in promoted_problem_ids if item.strip()}

    def reserve_formal_workspace(
        self,
        *,
        project_dir: Path,
        problem_id: str,
        run_id: str,
        canonical_workspace: Path | None = None,
    ) -> WorkspaceReservation:
        problem_name = problem_id.strip()
        run_slug = slugify(run_id)
        project_dir = project_dir.expanduser().resolve()
        canonical = (canonical_workspace or (project_dir / "formal")).expanduser().resolve()
        isolated = project_dir / "workspaces" / run_slug / "formal"
        locks_dir = project_dir / ".locks"
        project_dir.mkdir(parents=True, exist_ok=True)
        canonical.mkdir(parents=True, exist_ok=True)
        locks_dir.mkdir(parents=True, exist_ok=True)
        _safe_copy_formal_workspace(canonical, isolated)
        return WorkspaceReservation(
            problem_id=problem_name,
            run_id=run_slug,
            project_dir=project_dir,
            canonical_workspace=canonical,
            isolated_workspace=isolated,
            locks_dir=locks_dir,
        )

    def build_active_assignments(
        self,
        *,
        campaign_dir: Path,
        promotion_queue: list[dict[str, Any]],
        attack_budget_seconds: int,
        campaign_id: str,
    ) -> dict[str, Any]:
        assignments: list[dict[str, Any]] = []
        for index, item in enumerate(promotion_queue, start=1):
            problem_id = str(item.get("problem_id", "")).strip()
            if not problem_id:
                continue
            run_id = slugify(f"{campaign_id}-{index:03d}-{problem_id}")
            project_dir = campaign_dir / "projects" / slugify(problem_id)
            reservation = self.reserve_formal_workspace(
                project_dir=project_dir,
                problem_id=problem_id,
                run_id=run_id,
            )
            assignments.append(
                {
                    **reservation.as_payload(repo_root=self.repo_root),
                    "priority": item.get("priority"),
                    "recommendation": item.get("recommendation", "promote"),
                    "budget_seconds": max(0, int(attack_budget_seconds)),
                    "status": "queued",
                    "source": "promotion_queue",
                    "progress_velocity": calculate_progress_velocity(),
                }
            )
        return {
            "schema_version": "amra.active_assignments.v2",
            "generated_at": utc_now_iso(),
            "campaign_id": campaign_id,
            "policy": {
                "focused_attack_budget": "promoted_targets_only",
                "workspace_policy": "isolated",
                "canonical_merge_policy": "verified_and_reviewed_only",
            },
            "assignments": assignments,
        }

    def schedule_from_campaign(
        self,
        *,
        campaign_dir: Path,
        attack_budget_seconds: int,
        campaign_id: str | None = None,
    ) -> dict[str, Any]:
        campaign_dir = campaign_dir.expanduser().resolve()
        payload = _read_json(campaign_dir / "promotion_queue.json", {"items": []})
        promotion_queue = payload.get("items", []) if isinstance(payload, dict) else []
        resolved_campaign_id = campaign_id or campaign_dir.name
        with self.state_lock(campaign_dir):
            active = self.build_active_assignments(
                campaign_dir=campaign_dir,
                promotion_queue=list(promotion_queue),
                attack_budget_seconds=attack_budget_seconds,
                campaign_id=resolved_campaign_id,
            )
            write_json(campaign_dir / "active_assignments.json", active)
            return active

    def merge_reviewed_formal_workspace(
        self,
        *,
        project_dir: Path,
        run_id: str,
        status: str,
        review_status: str,
        library_module: str = "",
    ) -> dict[str, Any]:
        review_status_normalized = review_status.strip().lower()
        verified = status == "verified"
        approved = review_status_normalized in APPROVED_REVIEW_STATUSES
        project_dir = project_dir.expanduser().resolve()
        isolated = project_dir / "workspaces" / slugify(run_id) / "formal"
        canonical = project_dir / "formal"
        report = {
            "schema_version": "amra.formal_workspace_merge.v1",
            "generated_at": utc_now_iso(),
            "project_dir": str(project_dir),
            "run_id": slugify(run_id),
            "status": status,
            "review_status": review_status,
            "verified": verified,
            "review_approved": approved,
            "merged": False,
            "canonical_workspace": str(canonical),
            "isolated_workspace": str(isolated),
            "library_module": library_module,
            "blockers": [],
        }
        if not verified:
            report["blockers"].append("formalization_not_verified")
        if not approved:
            report["blockers"].append("review_not_approved")
        if not isolated.exists():
            report["blockers"].append("isolated_workspace_missing")
        if report["blockers"]:
            write_json(project_dir / "review" / f"formal_merge_{slugify(run_id)}.json", report)
            return report

        with self.formal_lock(project_dir):
            if library_module:
                with self.library_promotion_lock(project_dir, module=library_module):
                    _safe_copy_formal_workspace(isolated, canonical)
            else:
                _safe_copy_formal_workspace(isolated, canonical)
        report["merged"] = True
        write_json(project_dir / "review" / f"formal_merge_{slugify(run_id)}.json", report)
        return report


PortfolioScheduler = PortfolioAttackScheduler
AttackScheduler = PortfolioAttackScheduler
FileLock = PortfolioFileLock
