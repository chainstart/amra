from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

from amra.discovery.campaign_status import (
    CampaignStatusStore,
    ClaimedWork,
    ProblemNotFoundError,
)


BATCH_CAMPAIGN_SCHEMA_VERSION = "amra.batch_campaign.v1"
SECOND_BATCH_EXPECTED_PROBLEMS = 100

MODEL_AUDIT_STATUSES = frozenset(
    {"pending", "approved", "revision_required", "rejected"}
)
VERIFICATION_STATUSES = frozenset(
    {"not_required", "pending", "verified", "rejected", "inconclusive", "contested"}
)
VERIFICATION_VERDICTS = frozenset({"verified", "rejected", "inconclusive"})
STRATEGY_OUTCOMES = frozenset({"candidate", "no_candidate", "inconclusive"})


class BatchCampaignError(RuntimeError):
    pass


class BatchConfigurationError(BatchCampaignError):
    pass


class BatchStateError(BatchCampaignError):
    pass


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _fingerprint(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _normalized_id(value: str, *, label: str) -> str:
    normalized = str(value).strip()
    if not normalized:
        raise ValueError(f"{label} must not be empty")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:/+-]*", normalized):
        raise ValueError(f"{label} contains unsupported characters: {normalized!r}")
    return normalized


@dataclass(frozen=True)
class StrategyBudget:
    time_seconds: int
    max_cases: int | None = None
    memory_mb: int | None = None
    parameters: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.time_seconds <= 0:
            raise ValueError("time_seconds must be positive")
        if self.max_cases is not None and self.max_cases <= 0:
            raise ValueError("max_cases must be positive when provided")
        if self.memory_mb is not None and self.memory_mb <= 0:
            raise ValueError("memory_mb must be positive when provided")
        object.__setattr__(self, "parameters", dict(self.parameters))

    def as_dict(self) -> dict[str, Any]:
        return {
            "time_seconds": self.time_seconds,
            "max_cases": self.max_cases,
            "memory_mb": self.memory_mb,
            "parameters": dict(self.parameters),
        }


@dataclass(frozen=True)
class StrategyPlan:
    stage_id: str
    strategy_id: str
    executor_id: str
    executor_version: str
    budget: StrategyBudget
    launches: int = 1
    requires_independent_verification: bool = True
    config: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "stage_id", _normalized_id(self.stage_id, label="stage_id")
        )
        object.__setattr__(
            self, "strategy_id", _normalized_id(self.strategy_id, label="strategy_id")
        )
        object.__setattr__(
            self, "executor_id", _normalized_id(self.executor_id, label="executor_id")
        )
        object.__setattr__(
            self,
            "executor_version",
            _normalized_id(self.executor_version, label="executor_version"),
        )
        if self.launches <= 0:
            raise ValueError("launches must be positive")
        object.__setattr__(self, "config", dict(self.config))

    def as_dict(self) -> dict[str, Any]:
        return {
            "stage_id": self.stage_id,
            "strategy_id": self.strategy_id,
            "executor_id": self.executor_id,
            "executor_version": self.executor_version,
            "budget": self.budget.as_dict(),
            "launches": self.launches,
            "requires_independent_verification": self.requires_independent_verification,
            "config": dict(self.config),
        }


@dataclass(frozen=True)
class BatchProblemPlan:
    problem_id: str
    title: str
    statement_hash: str
    domain: str
    source: str
    model_contract: Mapping[str, Any]
    strategies: Sequence[StrategyPlan]
    model_audit_status: str = "pending"
    priority: float = 0

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "problem_id", _normalized_id(self.problem_id, label="problem_id")
        )
        title = str(self.title).strip()
        if not title:
            raise ValueError("title must not be empty")
        object.__setattr__(self, "title", title)
        statement_hash = str(self.statement_hash).strip()
        if not statement_hash:
            raise ValueError("statement_hash must not be empty")
        object.__setattr__(self, "statement_hash", statement_hash)
        if self.model_audit_status not in MODEL_AUDIT_STATUSES:
            raise ValueError(
                f"unsupported model_audit_status: {self.model_audit_status}"
            )
        strategies = tuple(self.strategies)
        if not strategies:
            raise ValueError("each problem must have at least one strategy")
        keys = [
            (strategy.stage_id, strategy.strategy_id)
            for strategy in strategies
        ]
        if len(keys) != len(set(keys)):
            raise ValueError(
                "strategy_id must be unique within each problem stage"
            )
        object.__setattr__(self, "model_contract", dict(self.model_contract))
        object.__setattr__(self, "strategies", strategies)

    @property
    def stage_ids(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(strategy.stage_id for strategy in self.strategies))

    def as_dict(self) -> dict[str, Any]:
        return {
            "problem_id": self.problem_id,
            "title": self.title,
            "statement_hash": self.statement_hash,
            "domain": self.domain,
            "source": self.source,
            "model_contract": dict(self.model_contract),
            "strategies": [strategy.as_dict() for strategy in self.strategies],
            "model_audit_status": self.model_audit_status,
            "priority": self.priority,
        }


@dataclass(frozen=True)
class BatchPlan:
    batch_id: str
    collection: str
    problems: Sequence[BatchProblemPlan]
    global_seed: int
    expected_problem_count: int | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "batch_id", _normalized_id(self.batch_id, label="batch_id")
        )
        object.__setattr__(
            self, "collection", _normalized_id(self.collection, label="collection")
        )
        problems = tuple(self.problems)
        if not problems:
            raise ValueError("batch must contain at least one problem")
        problem_ids = [problem.problem_id for problem in problems]
        if len(problem_ids) != len(set(problem_ids)):
            raise ValueError("problem_id values must be unique within a batch")
        if (
            self.expected_problem_count is not None
            and len(problems) != self.expected_problem_count
        ):
            raise ValueError(
                f"batch expects {self.expected_problem_count} problems, got {len(problems)}"
            )
        object.__setattr__(self, "problems", problems)
        global_seed = int(self.global_seed)
        if not -(1 << 63) <= global_seed < (1 << 63):
            raise ValueError("global_seed must fit a signed SQLite INTEGER")
        object.__setattr__(self, "global_seed", global_seed)

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": BATCH_CAMPAIGN_SCHEMA_VERSION,
            "batch_id": self.batch_id,
            "collection": self.collection,
            "global_seed": self.global_seed,
            "expected_problem_count": self.expected_problem_count,
            "problems": [problem.as_dict() for problem in self.problems],
        }

    @property
    def fingerprint(self) -> str:
        return _fingerprint(self.as_dict())


@dataclass(frozen=True)
class BatchClaim:
    leased_work: ClaimedWork
    batch_id: str
    parent_problem_id: str
    stage_id: str
    stage_index: int
    strategy_id: str
    executor_id: str
    executor_version: str
    launch_index: int
    deterministic_seed: int
    budget: dict[str, Any]
    config: dict[str, Any]
    config_fingerprint: str
    requires_independent_verification: bool
    checkpoint: dict[str, Any] | None

    @property
    def task_id(self) -> str:
        return self.leased_work.problem_id

    @property
    def attempt_id(self) -> int:
        return self.leased_work.attempt_id

    @property
    def worker_id(self) -> str:
        return self.leased_work.worker_id

    @property
    def fencing_token(self) -> int:
        return self.leased_work.fencing_token


class BatchCampaignCoordinator:
    """Durable orchestration for arbitrary batches of strategy runs.

    The core ``problems`` table is used as a lease queue for strategy run units.
    Batch-level mathematical state is kept in namespaced side tables in the same
    SQLite database. This module does not execute a mathematical strategy.
    """

    def __init__(
        self,
        database_path: str | Path,
        plan: BatchPlan,
        *,
        available_executors: Iterable[str] = (),
        busy_timeout_ms: int = 10_000,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self.database_path = Path(database_path).expanduser().resolve()
        self.plan = plan
        self.available_executors = {
            _normalized_id(value, label="executor_id")
            for value in available_executors
        }
        self.busy_timeout_ms = int(busy_timeout_ms)
        self._clock = clock
        self.store = CampaignStatusStore(
            self.database_path,
            busy_timeout_ms=self.busy_timeout_ms,
            clock=clock,
        )
        self._problem_plans = {
            problem.problem_id: problem for problem in self.plan.problems
        }
        self._migrate()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path,
            timeout=self.busy_timeout_ms / 1000,
            isolation_level=None,
        )
        connection.row_factory = sqlite3.Row
        connection.execute(f"PRAGMA busy_timeout = {self.busy_timeout_ms}")
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @contextmanager
    def _write_transaction(self) -> Iterator[sqlite3.Connection]:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _migrate(self) -> None:
        with self._write_transaction() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS batch_campaigns (
                    batch_id TEXT PRIMARY KEY,
                    collection_name TEXT NOT NULL UNIQUE,
                    schema_version TEXT NOT NULL,
                    plan_fingerprint TEXT NOT NULL,
                    global_seed INTEGER NOT NULL,
                    expected_problem_count INTEGER,
                    plan_json TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS batch_problem_state (
                    batch_id TEXT NOT NULL REFERENCES batch_campaigns(batch_id),
                    problem_id TEXT NOT NULL,
                    model_audit_status TEXT NOT NULL,
                    model_audit_detail_json TEXT NOT NULL DEFAULT '{}',
                    verification_status TEXT NOT NULL DEFAULT 'not_required',
                    candidate_fingerprint TEXT,
                    candidate_worker_id TEXT,
                    stop_reason TEXT NOT NULL DEFAULT '',
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    PRIMARY KEY (batch_id, problem_id)
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS batch_verifications (
                    verification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    batch_id TEXT NOT NULL,
                    problem_id TEXT NOT NULL,
                    candidate_fingerprint TEXT NOT NULL,
                    verifier_id TEXT NOT NULL,
                    verdict TEXT NOT NULL,
                    evidence_json TEXT NOT NULL DEFAULT '{}',
                    created_at REAL NOT NULL,
                    UNIQUE (
                        batch_id, problem_id, candidate_fingerprint, verifier_id
                    ),
                    FOREIGN KEY (batch_id, problem_id)
                        REFERENCES batch_problem_state(batch_id, problem_id)
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS batch_problem_audit_idx
                ON batch_problem_state(batch_id, model_audit_status)
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS batch_verification_idx
                ON batch_verifications(batch_id, problem_id, candidate_fingerprint)
                """
            )

    def initialize(self) -> dict[str, Any]:
        now = float(self._clock())
        plan_json = _canonical_json(self.plan.as_dict())
        with self._write_transaction() as connection:
            collection_owner = connection.execute(
                """
                SELECT batch_id FROM batch_campaigns
                WHERE collection_name = ? AND batch_id != ?
                """,
                (self.plan.collection, self.plan.batch_id),
            ).fetchone()
            if collection_owner is not None:
                raise BatchConfigurationError(
                    f"collection {self.plan.collection!r} already belongs to "
                    f"batch {collection_owner['batch_id']!r}"
                )
            existing = connection.execute(
                "SELECT plan_fingerprint FROM batch_campaigns WHERE batch_id = ?",
                (self.plan.batch_id,),
            ).fetchone()
            if (
                existing is not None
                and existing["plan_fingerprint"] != self.plan.fingerprint
            ):
                raise BatchConfigurationError(
                    f"batch {self.plan.batch_id!r} already exists with a different plan"
                )
            connection.execute(
                """
                INSERT INTO batch_campaigns (
                    batch_id, collection_name, schema_version, plan_fingerprint,
                    global_seed, expected_problem_count, plan_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(batch_id) DO UPDATE SET
                    updated_at = excluded.updated_at
                """,
                (
                    self.plan.batch_id,
                    self.plan.collection,
                    BATCH_CAMPAIGN_SCHEMA_VERSION,
                    self.plan.fingerprint,
                    self.plan.global_seed,
                    self.plan.expected_problem_count,
                    plan_json,
                    now,
                    now,
                ),
            )
            for problem in self.plan.problems:
                connection.execute(
                    """
                    INSERT INTO batch_problem_state (
                        batch_id, problem_id, model_audit_status,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(batch_id, problem_id) DO UPDATE SET
                        updated_at = excluded.updated_at
                    """,
                    (
                        self.plan.batch_id,
                        problem.problem_id,
                        problem.model_audit_status,
                        now,
                        now,
                    ),
                )

        inserted_tasks = 0
        for problem in self.plan.problems:
            stage_indexes = {
                stage_id: index for index, stage_id in enumerate(problem.stage_ids)
            }
            for strategy in problem.strategies:
                for launch_index in range(strategy.launches):
                    task = self._task_definition(
                        problem,
                        strategy,
                        stage_index=stage_indexes[strategy.stage_id],
                        launch_index=launch_index,
                    )
                    try:
                        previous = self.store.get_problem(task["task_id"])
                    except ProblemNotFoundError:
                        previous = None
                    if (
                        previous is not None
                        and previous["metadata"].get("implementation_status")
                        == "registered"
                        and task["implementation_status"] == "not_implemented"
                    ):
                        task["implementation_status"] = "registered"
                        task["planned_stop_reason"] = ""
                    runnable = (
                        problem.model_audit_status == "approved"
                        and task["stage_index"] == 0
                        and task["executor_id"] in self.available_executors
                    )
                    self.store.upsert_problem(
                        task["task_id"],
                        title=f"{problem.title} [{strategy.stage_id}/{strategy.strategy_id}"
                        f"#{launch_index}]",
                        source=problem.source,
                        domain=strategy.executor_id,
                        collection=self.plan.collection,
                        priority=float(problem.priority - task["stage_index"]),
                        stage=strategy.stage_id,
                        statement_hash=problem.statement_hash,
                        metadata=task,
                        status="queued" if runnable else "parked",
                    )
                    if previous is None:
                        inserted_tasks += 1
        self.reconcile()
        return {
            "schema_version": BATCH_CAMPAIGN_SCHEMA_VERSION,
            "batch_id": self.plan.batch_id,
            "collection": self.plan.collection,
            "plan_fingerprint": self.plan.fingerprint,
            "problem_count": len(self.plan.problems),
            "task_count": len(self.tasks()),
            "inserted_tasks": inserted_tasks,
            "summary": self.summary(),
        }

    def _task_definition(
        self,
        problem: BatchProblemPlan,
        strategy: StrategyPlan,
        *,
        stage_index: int,
        launch_index: int,
    ) -> dict[str, Any]:
        seed_payload = {
            "global_seed": self.plan.global_seed,
            "batch_id": self.plan.batch_id,
            "problem_id": problem.problem_id,
            "stage_id": strategy.stage_id,
            "strategy_id": strategy.strategy_id,
            "launch_index": launch_index,
        }
        deterministic_seed = int(_fingerprint(seed_payload)[:16], 16) & (
            (1 << 63) - 1
        )
        config_payload = {
            "schema_version": BATCH_CAMPAIGN_SCHEMA_VERSION,
            "batch_id": self.plan.batch_id,
            "problem_id": problem.problem_id,
            "statement_hash": problem.statement_hash,
            "model_contract": dict(problem.model_contract),
            "stage_id": strategy.stage_id,
            "stage_index": stage_index,
            "strategy_id": strategy.strategy_id,
            "executor_id": strategy.executor_id,
            "executor_version": strategy.executor_version,
            "launch_index": launch_index,
            "deterministic_seed": deterministic_seed,
            "budget": strategy.budget.as_dict(),
            "config": dict(strategy.config),
        }
        config_fingerprint = _fingerprint(config_payload)
        task_id = f"batch-task-{_fingerprint(config_payload)[:40]}"
        implementation_status = (
            "registered"
            if strategy.executor_id in self.available_executors
            else "not_implemented"
        )
        return {
            "kind": "batch_strategy_task",
            "schema_version": BATCH_CAMPAIGN_SCHEMA_VERSION,
            "task_id": task_id,
            "batch_id": self.plan.batch_id,
            "collection": self.plan.collection,
            "parent_problem_id": problem.problem_id,
            "problem_domain": problem.domain,
            "statement_hash": problem.statement_hash,
            "model_contract": dict(problem.model_contract),
            "stage_id": strategy.stage_id,
            "stage_index": stage_index,
            "strategy_id": strategy.strategy_id,
            "executor_id": strategy.executor_id,
            "executor_version": strategy.executor_version,
            "launch_index": launch_index,
            "deterministic_seed": deterministic_seed,
            "budget": strategy.budget.as_dict(),
            "config": dict(strategy.config),
            "config_fingerprint": config_fingerprint,
            "requires_independent_verification": (
                strategy.requires_independent_verification
            ),
            "implementation_status": implementation_status,
            "planned_stop_reason": (
                "" if implementation_status == "registered"
                else "executor_not_registered"
            ),
        }

    def tasks(self) -> list[dict[str, Any]]:
        return [
            row
            for row in self.store.list_problems(collection=self.plan.collection)
            if row["metadata"].get("batch_id") == self.plan.batch_id
        ]

    def problem_state(self, problem_id: str) -> dict[str, Any]:
        problem_id = _normalized_id(problem_id, label="problem_id")
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM batch_problem_state
                WHERE batch_id = ? AND problem_id = ?
                """,
                (self.plan.batch_id, problem_id),
            ).fetchone()
        if row is None:
            raise BatchStateError(f"problem {problem_id!r} is not in this batch")
        return self._decode_problem_state(row)

    def record_model_audit(
        self,
        problem_id: str,
        *,
        status: str,
        auditor_id: str,
        detail: Mapping[str, Any],
        stop_reason: str = "",
    ) -> dict[str, Any]:
        problem_id = _normalized_id(problem_id, label="problem_id")
        if status not in MODEL_AUDIT_STATUSES:
            raise ValueError(f"unsupported model audit status: {status}")
        auditor_id = _normalized_id(auditor_id, label="auditor_id")
        relevant = self._problem_tasks(problem_id)
        if any(row["status"] == "running" for row in relevant):
            raise BatchStateError("cannot change model audit while a strategy is running")
        if any(row["attempt_count"] > 0 for row in relevant):
            current = self.problem_state(problem_id)["model_audit_status"]
            if current != status:
                raise BatchStateError(
                    "cannot change model audit after strategy attempts have started"
                )
        now = float(self._clock())
        with self._write_transaction() as connection:
            cursor = connection.execute(
                """
                UPDATE batch_problem_state
                SET model_audit_status = ?, model_audit_detail_json = ?,
                    stop_reason = ?, updated_at = ?
                WHERE batch_id = ? AND problem_id = ?
                """,
                (
                    status,
                    _canonical_json(
                        {"auditor_id": auditor_id, "detail": dict(detail)}
                    ),
                    str(stop_reason),
                    now,
                    self.plan.batch_id,
                    problem_id,
                ),
            )
            if cursor.rowcount != 1:
                raise BatchStateError(f"problem {problem_id!r} is not in this batch")
        self.reconcile(problem_ids=[problem_id])
        return self.problem_state(problem_id)

    def activate_stage(self, problem_id: str, stage_id: str) -> list[str]:
        problem_id = _normalized_id(problem_id, label="problem_id")
        stage_id = _normalized_id(stage_id, label="stage_id")
        state = self.problem_state(problem_id)
        if state["model_audit_status"] != "approved":
            raise BatchStateError("model audit must be approved before stage activation")
        problem = self._problem_plans[problem_id]
        if stage_id not in problem.stage_ids:
            raise BatchStateError(
                f"unknown stage {stage_id!r} for problem {problem_id!r}"
            )
        target_index = problem.stage_ids.index(stage_id)
        earlier = [
            row
            for row in self._problem_tasks(problem_id)
            if int(row["metadata"]["stage_index"]) < target_index
        ]
        if any(row["status"] in {"queued", "retry", "running"} for row in earlier):
            raise BatchStateError("earlier stages are not terminal")
        activated: list[str] = []
        for row in self._problem_tasks(problem_id):
            metadata = row["metadata"]
            if metadata["stage_id"] != stage_id:
                continue
            if metadata["executor_id"] not in self.available_executors:
                continue
            if row["status"] == "parked" and row["attempt_count"] == 0:
                self.store.upsert_problem(
                    row["problem_id"],
                    title=row["title"],
                    source=row["source"],
                    domain=row["domain"],
                    collection=row["collection"],
                    priority=row["priority"],
                    stage=row["stage"],
                    statement_hash=row["statement_hash"],
                    metadata=metadata,
                    status="queued",
                    reset_status=True,
                    reset_reason=f"stage_activated:{stage_id}",
                )
                activated.append(row["problem_id"])
        return activated

    def reconcile(self, *, problem_ids: Iterable[str] | None = None) -> dict[str, Any]:
        selected = (
            set(self._problem_plans)
            if problem_ids is None
            else {
                _normalized_id(problem_id, label="problem_id")
                for problem_id in problem_ids
            }
        )
        activated: list[str] = []
        candidates_updated: list[str] = []
        for problem_id in selected:
            if problem_id not in self._problem_plans:
                raise BatchStateError(f"problem {problem_id!r} is not in this batch")
            state = self.problem_state(problem_id)
            problem = self._problem_plans[problem_id]
            if state["model_audit_status"] == "approved":
                activated.extend(self.activate_stage(problem_id, problem.stage_ids[0]))
            for task in self._problem_tasks(problem_id):
                result = task.get("last_result") or {}
                if (
                    task["status"] == "completed"
                    and result.get("outcome") == "candidate"
                    and result.get("candidate") is not None
                ):
                    self._register_candidate(
                        problem_id,
                        candidate=result["candidate"],
                        producer_worker_id=str(result.get("producer_worker_id") or ""),
                        requires_verification=bool(
                            result.get("requires_independent_verification", True)
                        ),
                    )
                    candidates_updated.append(problem_id)
        return {
            "activated_task_ids": sorted(set(activated)),
            "candidate_problem_ids": sorted(set(candidates_updated)),
        }

    def claim(self, worker_id: str, *, lease_seconds: float = 300) -> BatchClaim | None:
        if not self.available_executors:
            return None
        work = self.store.claim(
            worker_id,
            lease_seconds=lease_seconds,
            domains=sorted(self.available_executors),
            collections=[self.plan.collection],
            method="batch-strategy-run",
            config={
                "batch_id": self.plan.batch_id,
                "plan_fingerprint": self.plan.fingerprint,
            },
        )
        if work is None:
            return None
        metadata = work.problem["metadata"]
        if metadata.get("batch_id") != self.plan.batch_id:
            self.store.interrupt(
                work.problem_id,
                work.worker_id,
                work.fencing_token,
                reason="batch_collection_collision",
            )
            raise BatchConfigurationError(
                f"claimed task from a different batch: {metadata.get('batch_id')!r}"
            )
        checkpoint = work.latest_checkpoint
        if checkpoint is not None:
            state = checkpoint.get("state") or {}
            if state.get("config_fingerprint") != metadata["config_fingerprint"]:
                checkpoint = None
        return BatchClaim(
            leased_work=work,
            batch_id=self.plan.batch_id,
            parent_problem_id=metadata["parent_problem_id"],
            stage_id=metadata["stage_id"],
            stage_index=int(metadata["stage_index"]),
            strategy_id=metadata["strategy_id"],
            executor_id=metadata["executor_id"],
            executor_version=metadata["executor_version"],
            launch_index=int(metadata["launch_index"]),
            deterministic_seed=int(metadata["deterministic_seed"]),
            budget=dict(metadata["budget"]),
            config=dict(metadata["config"]),
            config_fingerprint=metadata["config_fingerprint"],
            requires_independent_verification=bool(
                metadata["requires_independent_verification"]
            ),
            checkpoint=checkpoint,
        )

    def heartbeat(self, claim: BatchClaim, *, extend_seconds: float = 300) -> str:
        return self.store.heartbeat(
            claim.task_id,
            claim.worker_id,
            claim.fencing_token,
            extend_seconds=extend_seconds,
        )

    def save_checkpoint(
        self,
        claim: BatchClaim,
        *,
        cursor: Mapping[str, Any],
        state: Mapping[str, Any] | None = None,
        metrics: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.store.save_checkpoint(
            claim.task_id,
            claim.worker_id,
            claim.fencing_token,
            cursor=dict(cursor),
            state={
                "schema_version": BATCH_CAMPAIGN_SCHEMA_VERSION,
                "batch_id": claim.batch_id,
                "parent_problem_id": claim.parent_problem_id,
                "stage_id": claim.stage_id,
                "strategy_id": claim.strategy_id,
                "launch_index": claim.launch_index,
                "deterministic_seed": claim.deterministic_seed,
                "config_fingerprint": claim.config_fingerprint,
                "executor_state": dict(state or {}),
            },
            metrics=dict(metrics or {}),
        )

    def complete(
        self,
        claim: BatchClaim,
        *,
        outcome: str,
        stop_reason: str,
        candidate: Mapping[str, Any] | None = None,
        metrics: Mapping[str, Any] | None = None,
        final_cursor: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        if outcome not in STRATEGY_OUTCOMES:
            raise ValueError(f"unsupported strategy outcome: {outcome}")
        stop_reason = str(stop_reason).strip()
        if not stop_reason:
            raise ValueError("stop_reason must not be empty")
        if outcome == "candidate" and candidate is None:
            raise ValueError("candidate outcome requires a candidate payload")
        if outcome != "candidate" and candidate is not None:
            raise ValueError("candidate payload is only valid for candidate outcomes")
        if final_cursor is not None:
            self.save_checkpoint(
                claim,
                cursor=final_cursor,
                metrics=metrics,
            )
        result = {
            "schema_version": BATCH_CAMPAIGN_SCHEMA_VERSION,
            "batch_id": claim.batch_id,
            "parent_problem_id": claim.parent_problem_id,
            "stage_id": claim.stage_id,
            "stage_index": claim.stage_index,
            "strategy_id": claim.strategy_id,
            "executor_id": claim.executor_id,
            "executor_version": claim.executor_version,
            "launch_index": claim.launch_index,
            "deterministic_seed": claim.deterministic_seed,
            "budget": claim.budget,
            "config_fingerprint": claim.config_fingerprint,
            "outcome": outcome,
            "stop_reason": stop_reason,
            "candidate": None if candidate is None else dict(candidate),
            "metrics": dict(metrics or {}),
            "producer_worker_id": claim.worker_id,
            "requires_independent_verification": (
                claim.requires_independent_verification
            ),
        }
        completed = self.store.complete(
            claim.task_id,
            claim.worker_id,
            claim.fencing_token,
            result=result,
            stage=claim.stage_id,
        )
        if candidate is not None:
            self._register_candidate(
                claim.parent_problem_id,
                candidate=candidate,
                producer_worker_id=claim.worker_id,
                requires_verification=claim.requires_independent_verification,
            )
        return completed

    def fail(
        self,
        claim: BatchClaim,
        *,
        stop_reason: str,
        retryable: bool,
        retry_after_seconds: float = 0,
    ) -> dict[str, Any]:
        reason = str(stop_reason).strip()
        if not reason:
            raise ValueError("stop_reason must not be empty")
        return self.store.fail(
            claim.task_id,
            claim.worker_id,
            claim.fencing_token,
            error=reason,
            retryable=retryable,
            retry_after_seconds=retry_after_seconds,
        )

    def interrupt(
        self,
        claim: BatchClaim,
        *,
        stop_reason: str = "worker_interrupted",
    ) -> dict[str, Any]:
        return self.store.interrupt(
            claim.task_id,
            claim.worker_id,
            claim.fencing_token,
            reason=stop_reason,
        )

    def record_independent_verification(
        self,
        problem_id: str,
        *,
        verifier_id: str,
        verdict: str,
        evidence: Mapping[str, Any],
    ) -> dict[str, Any]:
        problem_id = _normalized_id(problem_id, label="problem_id")
        if verdict not in VERIFICATION_VERDICTS:
            raise ValueError(f"unsupported verification verdict: {verdict}")
        verifier_id = _normalized_id(verifier_id, label="verifier_id")
        state = self.problem_state(problem_id)
        candidate_fingerprint = state.get("candidate_fingerprint")
        if not candidate_fingerprint:
            raise BatchStateError("problem has no candidate to verify")
        producer_ids = self._candidate_producer_ids(
            problem_id, str(candidate_fingerprint)
        )
        if verifier_id in producer_ids:
            raise BatchStateError("candidate producer cannot independently verify it")
        now = float(self._clock())
        with self._write_transaction() as connection:
            connection.execute(
                """
                INSERT INTO batch_verifications (
                    batch_id, problem_id, candidate_fingerprint,
                    verifier_id, verdict, evidence_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(
                    batch_id, problem_id, candidate_fingerprint, verifier_id
                ) DO UPDATE SET
                    verdict = excluded.verdict,
                    evidence_json = excluded.evidence_json,
                    created_at = excluded.created_at
                """,
                (
                    self.plan.batch_id,
                    problem_id,
                    candidate_fingerprint,
                    verifier_id,
                    verdict,
                    _canonical_json(dict(evidence)),
                    now,
                ),
            )
            verdict_rows = connection.execute(
                """
                SELECT DISTINCT verdict FROM batch_verifications
                WHERE batch_id = ? AND problem_id = ?
                    AND candidate_fingerprint = ?
                """,
                (self.plan.batch_id, problem_id, candidate_fingerprint),
            ).fetchall()
            verdicts = {str(row["verdict"]) for row in verdict_rows}
            if "verified" in verdicts and "rejected" in verdicts:
                aggregate = "contested"
            elif "rejected" in verdicts:
                aggregate = "rejected"
            elif "verified" in verdicts:
                aggregate = "verified"
            elif verdicts == {"inconclusive"}:
                aggregate = "inconclusive"
            else:
                aggregate = "pending"
            connection.execute(
                """
                UPDATE batch_problem_state
                SET verification_status = ?, updated_at = ?
                WHERE batch_id = ? AND problem_id = ?
                """,
                (aggregate, now, self.plan.batch_id, problem_id),
            )
        return self.problem_state(problem_id)

    def summary(self) -> dict[str, Any]:
        problem_states = [
            self.problem_state(problem.problem_id) for problem in self.plan.problems
        ]
        tasks = self.tasks()
        task_statuses: dict[str, int] = {}
        stop_reasons: dict[str, int] = {}
        for task in tasks:
            task_statuses[task["status"]] = task_statuses.get(task["status"], 0) + 1
            result = task.get("last_result") or {}
            reason = str(
                result.get("stop_reason")
                or task.get("last_error")
                or task["metadata"].get("planned_stop_reason")
                or ""
            )
            if reason:
                stop_reasons[reason] = stop_reasons.get(reason, 0) + 1
        return {
            "schema_version": BATCH_CAMPAIGN_SCHEMA_VERSION,
            "batch_id": self.plan.batch_id,
            "collection": self.plan.collection,
            "plan_fingerprint": self.plan.fingerprint,
            "problem_count": len(problem_states),
            "task_count": len(tasks),
            "task_status_counts": dict(sorted(task_statuses.items())),
            "model_audit_status_counts": self._count_values(
                state["model_audit_status"] for state in problem_states
            ),
            "verification_status_counts": self._count_values(
                state["verification_status"] for state in problem_states
            ),
            "stop_reason_counts": dict(sorted(stop_reasons.items())),
        }

    def _problem_tasks(self, problem_id: str) -> list[dict[str, Any]]:
        return [
            row
            for row in self.tasks()
            if row["metadata"].get("parent_problem_id") == problem_id
        ]

    def _register_candidate(
        self,
        problem_id: str,
        *,
        candidate: Mapping[str, Any],
        producer_worker_id: str,
        requires_verification: bool,
    ) -> None:
        candidate_fingerprint = _fingerprint(dict(candidate))
        now = float(self._clock())
        with self._write_transaction() as connection:
            row = connection.execute(
                """
                SELECT candidate_fingerprint FROM batch_problem_state
                WHERE batch_id = ? AND problem_id = ?
                """,
                (self.plan.batch_id, problem_id),
            ).fetchone()
            if row is None:
                raise BatchStateError(f"problem {problem_id!r} is not in this batch")
            previous = row["candidate_fingerprint"]
            verification_status = (
                "pending" if requires_verification else "not_required"
            )
            stored_producer = producer_worker_id
            if previous == candidate_fingerprint:
                current = connection.execute(
                    """
                    SELECT verification_status, candidate_worker_id
                    FROM batch_problem_state
                    WHERE batch_id = ? AND problem_id = ?
                    """,
                    (self.plan.batch_id, problem_id),
                ).fetchone()
                verification_status = str(current["verification_status"])
                stored_producer = str(
                    current["candidate_worker_id"] or producer_worker_id
                )
            connection.execute(
                """
                UPDATE batch_problem_state
                SET candidate_fingerprint = ?, candidate_worker_id = ?,
                    verification_status = ?, stop_reason = 'candidate_requires_review',
                    updated_at = ?
                WHERE batch_id = ? AND problem_id = ?
                """,
                (
                    candidate_fingerprint,
                    stored_producer,
                    verification_status,
                    now,
                    self.plan.batch_id,
                    problem_id,
                ),
            )

    def _candidate_producer_ids(
        self, problem_id: str, candidate_fingerprint: str
    ) -> set[str]:
        producer_ids: set[str] = set()
        for task in self._problem_tasks(problem_id):
            result = task.get("last_result") or {}
            candidate = result.get("candidate")
            if candidate is None or _fingerprint(candidate) != candidate_fingerprint:
                continue
            producer = str(result.get("producer_worker_id") or "")
            if producer:
                producer_ids.add(producer)
        state = self.problem_state(problem_id)
        stored = str(state.get("candidate_worker_id") or "")
        if stored:
            producer_ids.add(stored)
        return producer_ids

    @staticmethod
    def _decode_problem_state(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "batch_id": str(row["batch_id"]),
            "problem_id": str(row["problem_id"]),
            "model_audit_status": str(row["model_audit_status"]),
            "model_audit_detail": json.loads(row["model_audit_detail_json"]),
            "verification_status": str(row["verification_status"]),
            "candidate_fingerprint": row["candidate_fingerprint"],
            "candidate_worker_id": row["candidate_worker_id"],
            "stop_reason": str(row["stop_reason"]),
            "created_at": float(row["created_at"]),
            "updated_at": float(row["updated_at"]),
        }

    @staticmethod
    def _count_values(values: Iterable[str]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for value in values:
            counts[value] = counts.get(value, 0) + 1
        return dict(sorted(counts.items()))


__all__ = [
    "BATCH_CAMPAIGN_SCHEMA_VERSION",
    "SECOND_BATCH_EXPECTED_PROBLEMS",
    "MODEL_AUDIT_STATUSES",
    "VERIFICATION_STATUSES",
    "VERIFICATION_VERDICTS",
    "STRATEGY_OUTCOMES",
    "BatchCampaignError",
    "BatchConfigurationError",
    "BatchStateError",
    "StrategyBudget",
    "StrategyPlan",
    "BatchProblemPlan",
    "BatchPlan",
    "BatchClaim",
    "BatchCampaignCoordinator",
]
