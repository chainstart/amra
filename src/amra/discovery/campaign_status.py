from __future__ import annotations

import csv
import json
import os
import sqlite3
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence


SCHEMA_VERSION = 1
RUNNABLE_STATUSES = ("queued", "retry")
TERMINAL_STATUSES = ("completed", "failed", "parked")


class CampaignStatusError(RuntimeError):
    """Base class for durable campaign-state errors."""


class ProblemNotFoundError(CampaignStatusError):
    pass


class LeaseLostError(CampaignStatusError):
    """Raised when a worker no longer owns the current problem lease."""


@dataclass(frozen=True)
class ClaimedWork:
    problem_id: str
    attempt_id: int
    worker_id: str
    fencing_token: int
    lease_expires_at: float
    problem: dict[str, Any]
    latest_checkpoint: dict[str, Any] | None

    def as_dict(self) -> dict[str, Any]:
        return {
            "problem_id": self.problem_id,
            "attempt_id": self.attempt_id,
            "worker_id": self.worker_id,
            "fencing_token": self.fencing_token,
            "lease_expires_at": _iso_timestamp(self.lease_expires_at),
            "problem": self.problem,
            "latest_checkpoint": self.latest_checkpoint,
        }


def _json_dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _json_load(value: str | None, default: Any) -> Any:
    if value is None or value == "":
        return default
    return json.loads(value)


def _iso_timestamp(value: float | int | None) -> str | None:
    if value is None:
        return None
    return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat().replace("+00:00", "Z")


class CampaignStatusStore:
    """SQLite-backed state table for a resumable, multi-worker campaign.

    A store instance does not retain a connection. Each public operation opens a
    short-lived connection, which makes the object safe to use from CLI processes
    and threads. Mutating operations use ``BEGIN IMMEDIATE`` where ownership or
    ordering matters.
    """

    def __init__(
        self,
        path: str | Path,
        *,
        busy_timeout_ms: int = 10_000,
        clock: Callable[[], float] = time.time,
    ) -> None:
        if busy_timeout_ms <= 0:
            raise ValueError("busy_timeout_ms must be positive")
        self.path = Path(path).expanduser().resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.busy_timeout_ms = int(busy_timeout_ms)
        self._clock = clock
        with self._connect() as connection:
            journal_mode = str(
                connection.execute("PRAGMA journal_mode").fetchone()[0]
            ).lower()
            if journal_mode != "wal":
                connection.execute("PRAGMA journal_mode = WAL")
            self._migrate(connection)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.path,
            timeout=self.busy_timeout_ms / 1000,
            isolation_level=None,
        )
        connection.row_factory = sqlite3.Row
        connection.execute(f"PRAGMA busy_timeout = {self.busy_timeout_ms}")
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA synchronous = FULL")
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

    def _migrate(self, connection: sqlite3.Connection) -> None:
        current = int(connection.execute("PRAGMA user_version").fetchone()[0])
        if current > SCHEMA_VERSION:
            raise CampaignStatusError(
                f"database schema version {current} is newer than supported version {SCHEMA_VERSION}"
            )
        if current < 1:
            connection.execute("BEGIN IMMEDIATE")
            try:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS problems (
                        problem_id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        source TEXT NOT NULL DEFAULT '',
                        domain TEXT NOT NULL DEFAULT '',
                        collection_name TEXT NOT NULL DEFAULT '',
                        priority REAL NOT NULL DEFAULT 0,
                        stage TEXT NOT NULL DEFAULT 'G0',
                        status TEXT NOT NULL DEFAULT 'queued',
                        statement_hash TEXT NOT NULL DEFAULT '',
                        metadata_json TEXT NOT NULL DEFAULT '{}',
                        created_at REAL NOT NULL,
                        updated_at REAL NOT NULL,
                        available_at REAL NOT NULL,
                        attempt_count INTEGER NOT NULL DEFAULT 0,
                        last_attempt_id INTEGER,
                        lease_owner TEXT,
                        lease_token INTEGER NOT NULL DEFAULT 0,
                        lease_expires_at REAL,
                        heartbeat_at REAL,
                        last_error TEXT,
                        last_result_json TEXT
                    )
                    """
                )
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS attempts (
                        attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        problem_id TEXT NOT NULL REFERENCES problems(problem_id),
                        worker_id TEXT NOT NULL,
                        fencing_token INTEGER NOT NULL,
                        status TEXT NOT NULL,
                        method TEXT NOT NULL DEFAULT '',
                        config_json TEXT NOT NULL DEFAULT '{}',
                        result_json TEXT,
                        error TEXT,
                        started_at REAL NOT NULL,
                        updated_at REAL NOT NULL,
                        finished_at REAL
                    )
                    """
                )
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS checkpoints (
                        checkpoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        attempt_id INTEGER NOT NULL REFERENCES attempts(attempt_id),
                        problem_id TEXT NOT NULL REFERENCES problems(problem_id),
                        sequence INTEGER NOT NULL,
                        fencing_token INTEGER NOT NULL,
                        cursor_json TEXT NOT NULL DEFAULT '{}',
                        state_json TEXT NOT NULL DEFAULT '{}',
                        metrics_json TEXT NOT NULL DEFAULT '{}',
                        created_at REAL NOT NULL,
                        UNIQUE(attempt_id, sequence)
                    )
                    """
                )
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS state_events (
                        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        problem_id TEXT NOT NULL REFERENCES problems(problem_id),
                        attempt_id INTEGER,
                        event_type TEXT NOT NULL,
                        worker_id TEXT,
                        fencing_token INTEGER,
                        detail_json TEXT NOT NULL DEFAULT '{}',
                        created_at REAL NOT NULL
                    )
                    """
                )
                connection.execute(
                    """
                    CREATE INDEX IF NOT EXISTS problems_queue_idx
                    ON problems(status, available_at, priority DESC, created_at, problem_id)
                    """
                )
                connection.execute(
                    """
                    CREATE INDEX IF NOT EXISTS problems_lease_idx
                    ON problems(status, lease_expires_at)
                    """
                )
                connection.execute(
                    """
                    CREATE INDEX IF NOT EXISTS attempts_problem_idx
                    ON attempts(problem_id, attempt_id DESC)
                    """
                )
                connection.execute(
                    """
                    CREATE INDEX IF NOT EXISTS checkpoints_problem_idx
                    ON checkpoints(problem_id, checkpoint_id DESC)
                    """
                )
                connection.execute(
                    """
                    CREATE INDEX IF NOT EXISTS events_problem_idx
                    ON state_events(problem_id, event_id)
                    """
                )
                connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
                connection.commit()
            except BaseException:
                connection.rollback()
                raise

    @property
    def schema_version(self) -> int:
        with self._connect() as connection:
            return int(connection.execute("PRAGMA user_version").fetchone()[0])

    @property
    def journal_mode(self) -> str:
        with self._connect() as connection:
            return str(connection.execute("PRAGMA journal_mode").fetchone()[0]).lower()

    def upsert_problem(
        self,
        problem_id: str,
        *,
        title: str,
        source: str = "",
        domain: str = "",
        collection: str = "",
        priority: float = 0,
        stage: str = "G0",
        statement_hash: str = "",
        metadata: Mapping[str, Any] | None = None,
        status: str = "queued",
        available_at: float | None = None,
        reset_status: bool = False,
        reset_reason: str = "",
    ) -> dict[str, Any]:
        """Insert a problem or refresh its descriptive fields.

        Existing execution state is preserved unless ``reset_status`` is true.
        Running work can never be reset through this method.
        """

        problem_id = str(problem_id).strip()
        title = str(title).strip()
        if not problem_id:
            raise ValueError("problem_id must not be empty")
        if not title:
            raise ValueError("title must not be empty")
        if status == "running":
            raise ValueError("problems must become running through claim()")
        now = float(self._clock())
        available = now if available_at is None else float(available_at)
        with self._write_transaction() as connection:
            existing = connection.execute(
                "SELECT status FROM problems WHERE problem_id = ?", (problem_id,)
            ).fetchone()
            if existing is None:
                connection.execute(
                    """
                    INSERT INTO problems (
                        problem_id, title, source, domain, collection_name,
                        priority, stage, status, statement_hash, metadata_json,
                        created_at, updated_at, available_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        problem_id,
                        title,
                        source,
                        domain,
                        collection,
                        float(priority),
                        stage,
                        status,
                        statement_hash,
                        _json_dump(dict(metadata or {})),
                        now,
                        now,
                        available,
                    ),
                )
                self._record_event(
                    connection, problem_id, "registered", now, detail={"status": status}
                )
            else:
                current_status = str(existing["status"])
                next_status = current_status
                next_available = None
                if reset_status:
                    if current_status == "running":
                        raise CampaignStatusError("cannot reset a problem with an active lease")
                    next_status = status
                    next_available = available
                connection.execute(
                    """
                    UPDATE problems
                    SET title = ?, source = ?, domain = ?, collection_name = ?,
                        priority = ?, stage = ?, statement_hash = ?,
                        metadata_json = ?, updated_at = ?,
                        status = ?,
                        available_at = COALESCE(?, available_at),
                        last_error = CASE WHEN ? THEN NULL ELSE last_error END,
                        last_result_json = CASE WHEN ? THEN NULL ELSE last_result_json END
                    WHERE problem_id = ?
                    """,
                    (
                        title,
                        source,
                        domain,
                        collection,
                        float(priority),
                        stage,
                        statement_hash,
                        _json_dump(dict(metadata or {})),
                        now,
                        next_status,
                        next_available,
                        int(reset_status),
                        int(reset_status),
                        problem_id,
                    ),
                )
                if reset_status:
                    self._record_event(
                        connection,
                        problem_id,
                        "reset",
                        now,
                        detail={
                            "from_status": current_status,
                            "to_status": next_status,
                            "reason": str(reset_reason),
                        },
                    )
            row = self._problem_row(connection, problem_id)
        return self._decode_problem(row)

    def upsert_problems(self, problems: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
        return [
            self.upsert_problem(
                str(problem["problem_id"]),
                title=str(problem["title"]),
                source=str(problem.get("source", "")),
                domain=str(problem.get("domain", "")),
                collection=str(problem.get("collection", problem.get("collection_name", ""))),
                priority=float(problem.get("priority", 0)),
                stage=str(problem.get("stage", "G0")),
                statement_hash=str(problem.get("statement_hash", "")),
                metadata=problem.get("metadata") or {},
                status=str(problem.get("status", "queued")),
                available_at=problem.get("available_at"),
                reset_status=bool(problem.get("reset_status", False)),
                reset_reason=str(problem.get("reset_reason", "")),
            )
            for problem in problems
        ]

    def prune_problems_not_in(self, active_problem_ids: Iterable[str]) -> list[str]:
        """Remove records no longer present in the authoritative problem bank.

        Running records are never pruned. Attempts and checkpoints for removed
        records are deleted transactionally; per-attempt JSON artifacts remain
        available outside the database for forensic use.
        """

        active = {str(problem_id) for problem_id in active_problem_ids}
        with self._write_transaction() as connection:
            rows = connection.execute(
                "SELECT problem_id, status FROM problems ORDER BY problem_id"
            ).fetchall()
            stale = [
                str(row["problem_id"])
                for row in rows
                if str(row["problem_id"]) not in active
            ]
            running = [
                str(row["problem_id"])
                for row in rows
                if str(row["problem_id"]) in stale and row["status"] == "running"
            ]
            if running:
                raise CampaignStatusError(
                    "cannot prune running problems: " + ", ".join(running)
                )
            for problem_id in stale:
                connection.execute(
                    "DELETE FROM checkpoints WHERE problem_id = ?", (problem_id,)
                )
                connection.execute(
                    "DELETE FROM attempts WHERE problem_id = ?", (problem_id,)
                )
                connection.execute(
                    "DELETE FROM state_events WHERE problem_id = ?", (problem_id,)
                )
                connection.execute(
                    "DELETE FROM problems WHERE problem_id = ?", (problem_id,)
                )
        return stale

    def get_problem(self, problem_id: str) -> dict[str, Any]:
        with self._connect() as connection:
            row = self._problem_row(connection, problem_id)
        return self._decode_problem(row)

    def list_problems(
        self,
        *,
        statuses: Sequence[str] | None = None,
        domain: str | None = None,
        collection: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        where: list[str] = []
        parameters: list[Any] = []
        if statuses:
            where.append(f"status IN ({','.join('?' for _ in statuses)})")
            parameters.extend(statuses)
        if domain is not None:
            where.append("domain = ?")
            parameters.append(domain)
        if collection is not None:
            where.append("collection_name = ?")
            parameters.append(collection)
        query = "SELECT * FROM problems"
        if where:
            query += " WHERE " + " AND ".join(where)
        query += " ORDER BY priority DESC, created_at, problem_id"
        if limit is not None:
            if limit < 0:
                raise ValueError("limit must be non-negative")
            query += " LIMIT ?"
            parameters.append(limit)
        with self._connect() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return [self._decode_problem(row) for row in rows]

    def claim(
        self,
        worker_id: str,
        *,
        lease_seconds: float = 180,
        statuses: Sequence[str] = RUNNABLE_STATUSES,
        domains: Sequence[str] | None = None,
        collections: Sequence[str] | None = None,
        method: str = "",
        config: Mapping[str, Any] | None = None,
    ) -> ClaimedWork | None:
        worker_id = str(worker_id).strip()
        if not worker_id:
            raise ValueError("worker_id must not be empty")
        if lease_seconds <= 0:
            raise ValueError("lease_seconds must be positive")
        if not statuses:
            return None
        now = float(self._clock())
        with self._write_transaction() as connection:
            self._recover_expired(connection, now)
            where = [
                f"status IN ({','.join('?' for _ in statuses)})",
                "available_at <= ?",
                "lease_owner IS NULL",
            ]
            parameters: list[Any] = [*statuses, now]
            if domains:
                where.append(f"domain IN ({','.join('?' for _ in domains)})")
                parameters.extend(domains)
            if collections:
                where.append(
                    f"collection_name IN ({','.join('?' for _ in collections)})"
                )
                parameters.extend(collections)
            row = connection.execute(
                f"""
                SELECT * FROM problems
                WHERE {' AND '.join(where)}
                ORDER BY priority DESC, available_at, created_at, problem_id
                LIMIT 1
                """,
                parameters,
            ).fetchone()
            if row is None:
                return None
            problem_id = str(row["problem_id"])
            latest_checkpoint = self._latest_checkpoint(connection, problem_id)
            token = int(row["lease_token"]) + 1
            expires_at = now + float(lease_seconds)
            cursor = connection.execute(
                """
                INSERT INTO attempts (
                    problem_id, worker_id, fencing_token, status, method,
                    config_json, started_at, updated_at
                ) VALUES (?, ?, ?, 'running', ?, ?, ?, ?)
                """,
                (
                    problem_id,
                    worker_id,
                    token,
                    method,
                    _json_dump(dict(config or {})),
                    now,
                    now,
                ),
            )
            attempt_id = int(cursor.lastrowid)
            connection.execute(
                """
                UPDATE problems
                SET status = 'running', updated_at = ?, attempt_count = attempt_count + 1,
                    last_attempt_id = ?, lease_owner = ?, lease_token = ?,
                    lease_expires_at = ?, heartbeat_at = ?, last_error = NULL
                WHERE problem_id = ?
                """,
                (now, attempt_id, worker_id, token, expires_at, now, problem_id),
            )
            self._record_event(
                connection,
                problem_id,
                "claimed",
                now,
                attempt_id=attempt_id,
                worker_id=worker_id,
                token=token,
                detail={"lease_expires_at": expires_at},
            )
            claimed_row = self._problem_row(connection, problem_id)
        return ClaimedWork(
            problem_id=problem_id,
            attempt_id=attempt_id,
            worker_id=worker_id,
            fencing_token=token,
            lease_expires_at=expires_at,
            problem=self._decode_problem(claimed_row),
            latest_checkpoint=(
                self._decode_checkpoint(latest_checkpoint) if latest_checkpoint is not None else None
            ),
        )

    def heartbeat(
        self,
        problem_id: str,
        worker_id: str,
        fencing_token: int,
        *,
        extend_seconds: float = 180,
    ) -> str:
        if extend_seconds <= 0:
            raise ValueError("extend_seconds must be positive")
        now = float(self._clock())
        with self._write_transaction() as connection:
            row = self._require_lease(
                connection, problem_id, worker_id, fencing_token, now
            )
            expires_at = now + float(extend_seconds)
            connection.execute(
                """
                UPDATE problems SET heartbeat_at = ?, lease_expires_at = ?, updated_at = ?
                WHERE problem_id = ?
                """,
                (now, expires_at, now, problem_id),
            )
            connection.execute(
                "UPDATE attempts SET updated_at = ? WHERE attempt_id = ?",
                (now, row["last_attempt_id"]),
            )
        return str(_iso_timestamp(expires_at))

    def save_checkpoint(
        self,
        problem_id: str,
        worker_id: str,
        fencing_token: int,
        *,
        cursor: Any,
        state: Any = None,
        metrics: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        now = float(self._clock())
        with self._write_transaction() as connection:
            row = self._require_lease(
                connection, problem_id, worker_id, fencing_token, now
            )
            attempt_id = int(row["last_attempt_id"])
            sequence = int(
                connection.execute(
                    """
                    SELECT COALESCE(MAX(sequence), 0) + 1
                    FROM checkpoints WHERE attempt_id = ?
                    """,
                    (attempt_id,),
                ).fetchone()[0]
            )
            insert = connection.execute(
                """
                INSERT INTO checkpoints (
                    attempt_id, problem_id, sequence, fencing_token,
                    cursor_json, state_json, metrics_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    attempt_id,
                    problem_id,
                    sequence,
                    fencing_token,
                    _json_dump(cursor),
                    _json_dump({} if state is None else state),
                    _json_dump(dict(metrics or {})),
                    now,
                ),
            )
            connection.execute(
                "UPDATE attempts SET updated_at = ? WHERE attempt_id = ?",
                (now, attempt_id),
            )
            self._record_event(
                connection,
                problem_id,
                "checkpoint",
                now,
                attempt_id=attempt_id,
                worker_id=worker_id,
                token=fencing_token,
                detail={"checkpoint_id": insert.lastrowid, "sequence": sequence},
            )
            checkpoint = connection.execute(
                "SELECT * FROM checkpoints WHERE checkpoint_id = ?",
                (insert.lastrowid,),
            ).fetchone()
        return self._decode_checkpoint(checkpoint)

    def latest_checkpoint(self, problem_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            self._problem_row(connection, problem_id)
            row = self._latest_checkpoint(connection, problem_id)
        return self._decode_checkpoint(row) if row is not None else None

    def latest_checkpoints(
        self,
        problem_ids: Iterable[str] | None = None,
    ) -> dict[str, dict[str, Any]]:
        selected = (
            None
            if problem_ids is None
            else tuple(dict.fromkeys(str(value) for value in problem_ids))
        )
        if selected == ():
            return {}
        where = ""
        parameters: tuple[Any, ...] = ()
        if selected is not None:
            placeholders = ", ".join("?" for _ in selected)
            where = f"WHERE problem_id IN ({placeholders})"
            parameters = selected
        with self._connect() as connection:
            rows = connection.execute(
                f"""
                SELECT checkpoint.*
                FROM checkpoints AS checkpoint
                JOIN (
                    SELECT problem_id, MAX(checkpoint_id) AS checkpoint_id
                    FROM checkpoints
                    {where}
                    GROUP BY problem_id
                ) AS latest
                ON checkpoint.checkpoint_id = latest.checkpoint_id
                """,
                parameters,
            ).fetchall()
        return {
            str(row["problem_id"]): self._decode_checkpoint(row)
            for row in rows
        }

    def complete(
        self,
        problem_id: str,
        worker_id: str,
        fencing_token: int,
        *,
        result: Any,
        stage: str | None = None,
    ) -> dict[str, Any]:
        return self._finish(
            problem_id,
            worker_id,
            fencing_token,
            problem_status="completed",
            attempt_status="completed",
            result=result,
            stage=stage,
        )

    def fail(
        self,
        problem_id: str,
        worker_id: str,
        fencing_token: int,
        *,
        error: str,
        retryable: bool = False,
        retry_after_seconds: float = 0,
    ) -> dict[str, Any]:
        if retry_after_seconds < 0:
            raise ValueError("retry_after_seconds must be non-negative")
        return self._finish(
            problem_id,
            worker_id,
            fencing_token,
            problem_status="retry" if retryable else "failed",
            attempt_status="failed",
            error=str(error),
            available_at=float(self._clock()) + retry_after_seconds,
            detail={"retryable": retryable, "retry_after_seconds": retry_after_seconds},
        )

    def park(
        self,
        problem_id: str,
        worker_id: str,
        fencing_token: int,
        *,
        reason: str,
        result: Any = None,
    ) -> dict[str, Any]:
        return self._finish(
            problem_id,
            worker_id,
            fencing_token,
            problem_status="parked",
            attempt_status="parked",
            error=str(reason),
            result=result,
        )

    def interrupt(
        self,
        problem_id: str,
        worker_id: str,
        fencing_token: int,
        *,
        reason: str = "worker interrupted",
        retry_after_seconds: float = 0,
    ) -> dict[str, Any]:
        """Release owned work back to the queue while retaining its checkpoint."""

        if retry_after_seconds < 0:
            raise ValueError("retry_after_seconds must be non-negative")
        return self._finish(
            problem_id,
            worker_id,
            fencing_token,
            problem_status="queued",
            attempt_status="interrupted",
            error=str(reason),
            available_at=float(self._clock()) + retry_after_seconds,
        )

    def _finish(
        self,
        problem_id: str,
        worker_id: str,
        fencing_token: int,
        *,
        problem_status: str,
        attempt_status: str,
        result: Any = None,
        error: str | None = None,
        stage: str | None = None,
        available_at: float | None = None,
        detail: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        now = float(self._clock())
        with self._write_transaction() as connection:
            row = self._require_lease(
                connection, problem_id, worker_id, fencing_token, now
            )
            attempt_id = int(row["last_attempt_id"])
            connection.execute(
                """
                UPDATE attempts
                SET status = ?, result_json = ?, error = ?,
                    updated_at = ?, finished_at = ?
                WHERE attempt_id = ?
                """,
                (
                    attempt_status,
                    None if result is None else _json_dump(result),
                    error,
                    now,
                    now,
                    attempt_id,
                ),
            )
            connection.execute(
                """
                UPDATE problems
                SET status = ?, stage = COALESCE(?, stage), updated_at = ?,
                    available_at = COALESCE(?, available_at),
                    lease_owner = NULL, lease_expires_at = NULL, heartbeat_at = NULL,
                    last_error = ?, last_result_json = ?
                WHERE problem_id = ?
                """,
                (
                    problem_status,
                    stage,
                    now,
                    available_at,
                    error,
                    None if result is None else _json_dump(result),
                    problem_id,
                ),
            )
            self._record_event(
                connection,
                problem_id,
                attempt_status,
                now,
                attempt_id=attempt_id,
                worker_id=worker_id,
                token=fencing_token,
                detail=dict(detail or {}),
            )
            finished = self._problem_row(connection, problem_id)
        return self._decode_problem(finished)

    def recover_expired_leases(self) -> list[str]:
        now = float(self._clock())
        with self._write_transaction() as connection:
            return self._recover_expired(connection, now)

    def _recover_expired(
        self, connection: sqlite3.Connection, now: float
    ) -> list[str]:
        rows = connection.execute(
            """
            SELECT problem_id, last_attempt_id, lease_owner, lease_token
            FROM problems
            WHERE status = 'running' AND lease_expires_at <= ?
            ORDER BY problem_id
            """,
            (now,),
        ).fetchall()
        recovered: list[str] = []
        for row in rows:
            problem_id = str(row["problem_id"])
            attempt_id = int(row["last_attempt_id"])
            old_token = int(row["lease_token"])
            connection.execute(
                """
                UPDATE attempts
                SET status = 'expired', error = 'lease expired',
                    updated_at = ?, finished_at = ?
                WHERE attempt_id = ? AND status = 'running'
                """,
                (now, now, attempt_id),
            )
            connection.execute(
                """
                UPDATE problems
                SET status = 'queued', updated_at = ?, available_at = ?,
                    lease_owner = NULL, lease_token = lease_token + 1,
                    lease_expires_at = NULL, heartbeat_at = NULL,
                    last_error = 'lease expired'
                WHERE problem_id = ? AND status = 'running' AND lease_token = ?
                """,
                (now, now, problem_id, old_token),
            )
            self._record_event(
                connection,
                problem_id,
                "lease_expired",
                now,
                attempt_id=attempt_id,
                worker_id=row["lease_owner"],
                token=old_token,
            )
            recovered.append(problem_id)
        return recovered

    def attempts(self, problem_id: str) -> list[dict[str, Any]]:
        with self._connect() as connection:
            self._problem_row(connection, problem_id)
            rows = connection.execute(
                "SELECT * FROM attempts WHERE problem_id = ? ORDER BY attempt_id",
                (problem_id,),
            ).fetchall()
        return [self._decode_attempt(row) for row in rows]

    def events(self, problem_id: str) -> list[dict[str, Any]]:
        with self._connect() as connection:
            self._problem_row(connection, problem_id)
            rows = connection.execute(
                "SELECT * FROM state_events WHERE problem_id = ? ORDER BY event_id",
                (problem_id,),
            ).fetchall()
        return [self._decode_event(row) for row in rows]

    def summary(self) -> dict[str, Any]:
        now = float(self._clock())
        with self._connect() as connection:
            total = int(connection.execute("SELECT COUNT(*) FROM problems").fetchone()[0])
            status_counts = self._group_counts(connection, "status")
            domain_counts = self._group_counts(connection, "domain")
            collection_counts = self._group_counts(connection, "collection_name")
            stage_counts = self._group_counts(connection, "stage")
            attempts = int(connection.execute("SELECT COUNT(*) FROM attempts").fetchone()[0])
            checkpoints = int(
                connection.execute("SELECT COUNT(*) FROM checkpoints").fetchone()[0]
            )
            expired_active = int(
                connection.execute(
                    """
                    SELECT COUNT(*) FROM problems
                    WHERE status = 'running' AND lease_expires_at <= ?
                    """,
                    (now,),
                ).fetchone()[0]
            )
        return {
            "schema_version": SCHEMA_VERSION,
            "database": str(self.path),
            "generated_at": _iso_timestamp(now),
            "total_problems": total,
            "status_counts": status_counts,
            "domain_counts": domain_counts,
            "collection_counts": collection_counts,
            "stage_counts": stage_counts,
            "attempts": attempts,
            "checkpoints": checkpoints,
            "expired_active_leases": expired_active,
        }

    def export_jsonl(self, path: str | Path) -> Path:
        destination = Path(path).expanduser().resolve()
        body = "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
            for row in self.list_problems()
        )
        self._atomic_write(destination, body)
        return destination

    def export_csv(self, path: str | Path) -> Path:
        destination = Path(path).expanduser().resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{destination.name}.",
            suffix=".tmp",
            dir=destination.parent,
        )
        os.fchmod(descriptor, 0o644)
        os.close(descriptor)
        temporary = Path(temporary_name)
        columns = [
            "problem_id",
            "title",
            "source",
            "domain",
            "collection",
            "priority",
            "stage",
            "status",
            "statement_hash",
            "metadata",
            "created_at",
            "updated_at",
            "available_at",
            "attempt_count",
            "last_attempt_id",
            "lease_owner",
            "lease_token",
            "lease_expires_at",
            "heartbeat_at",
            "last_error",
            "last_result",
        ]
        try:
            with temporary.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=columns)
                writer.writeheader()
                for item in self.list_problems():
                    row = dict(item)
                    row["metadata"] = _json_dump(row["metadata"])
                    row["last_result"] = (
                        "" if row["last_result"] is None else _json_dump(row["last_result"])
                    )
                    writer.writerow({key: row.get(key) for key in columns})
                handle.flush()
                os.fsync(handle.fileno())
            temporary.replace(destination)
        finally:
            if temporary.exists():
                temporary.unlink()
        return destination

    def _atomic_write(self, destination: Path, body: str) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{destination.name}.",
            suffix=".tmp",
            dir=destination.parent,
        )
        os.fchmod(descriptor, 0o644)
        os.close(descriptor)
        temporary = Path(temporary_name)
        try:
            with temporary.open("w", encoding="utf-8") as handle:
                handle.write(body)
                handle.flush()
                os.fsync(handle.fileno())
            temporary.replace(destination)
        finally:
            if temporary.exists():
                temporary.unlink()

    def _require_lease(
        self,
        connection: sqlite3.Connection,
        problem_id: str,
        worker_id: str,
        fencing_token: int,
        now: float,
    ) -> sqlite3.Row:
        row = self._problem_row(connection, problem_id)
        if (
            row["status"] != "running"
            or row["lease_owner"] != worker_id
            or int(row["lease_token"]) != int(fencing_token)
            or row["lease_expires_at"] is None
            or float(row["lease_expires_at"]) <= now
        ):
            raise LeaseLostError(
                f"lease lost for {problem_id!r}: worker={worker_id!r}, "
                f"fencing_token={fencing_token}"
            )
        return row

    @staticmethod
    def _problem_row(connection: sqlite3.Connection, problem_id: str) -> sqlite3.Row:
        row = connection.execute(
            "SELECT * FROM problems WHERE problem_id = ?", (problem_id,)
        ).fetchone()
        if row is None:
            raise ProblemNotFoundError(f"unknown problem_id: {problem_id}")
        return row

    @staticmethod
    def _latest_checkpoint(
        connection: sqlite3.Connection, problem_id: str
    ) -> sqlite3.Row | None:
        return connection.execute(
            """
            SELECT * FROM checkpoints
            WHERE problem_id = ?
            ORDER BY checkpoint_id DESC
            LIMIT 1
            """,
            (problem_id,),
        ).fetchone()

    @staticmethod
    def _record_event(
        connection: sqlite3.Connection,
        problem_id: str,
        event_type: str,
        now: float,
        *,
        attempt_id: int | None = None,
        worker_id: str | None = None,
        token: int | None = None,
        detail: Mapping[str, Any] | None = None,
    ) -> None:
        connection.execute(
            """
            INSERT INTO state_events (
                problem_id, attempt_id, event_type, worker_id,
                fencing_token, detail_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                problem_id,
                attempt_id,
                event_type,
                worker_id,
                token,
                _json_dump(dict(detail or {})),
                now,
            ),
        )

    @staticmethod
    def _group_counts(
        connection: sqlite3.Connection, column: str
    ) -> dict[str, int]:
        allowed = {"status", "domain", "collection_name", "stage"}
        if column not in allowed:
            raise ValueError(f"unsupported group column: {column}")
        rows = connection.execute(
            f"SELECT {column}, COUNT(*) AS count FROM problems GROUP BY {column}"
        ).fetchall()
        return {str(row[0]): int(row[1]) for row in rows}

    @staticmethod
    def _decode_problem(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "problem_id": str(row["problem_id"]),
            "title": str(row["title"]),
            "source": str(row["source"]),
            "domain": str(row["domain"]),
            "collection": str(row["collection_name"]),
            "priority": float(row["priority"]),
            "stage": str(row["stage"]),
            "status": str(row["status"]),
            "statement_hash": str(row["statement_hash"]),
            "metadata": _json_load(row["metadata_json"], {}),
            "created_at": _iso_timestamp(row["created_at"]),
            "updated_at": _iso_timestamp(row["updated_at"]),
            "available_at": _iso_timestamp(row["available_at"]),
            "attempt_count": int(row["attempt_count"]),
            "last_attempt_id": row["last_attempt_id"],
            "lease_owner": row["lease_owner"],
            "lease_token": int(row["lease_token"]),
            "lease_expires_at": _iso_timestamp(row["lease_expires_at"]),
            "heartbeat_at": _iso_timestamp(row["heartbeat_at"]),
            "last_error": row["last_error"],
            "last_result": _json_load(row["last_result_json"], None),
        }

    @staticmethod
    def _decode_attempt(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "attempt_id": int(row["attempt_id"]),
            "problem_id": str(row["problem_id"]),
            "worker_id": str(row["worker_id"]),
            "fencing_token": int(row["fencing_token"]),
            "status": str(row["status"]),
            "method": str(row["method"]),
            "config": _json_load(row["config_json"], {}),
            "result": _json_load(row["result_json"], None),
            "error": row["error"],
            "started_at": _iso_timestamp(row["started_at"]),
            "updated_at": _iso_timestamp(row["updated_at"]),
            "finished_at": _iso_timestamp(row["finished_at"]),
        }

    @staticmethod
    def _decode_checkpoint(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "checkpoint_id": int(row["checkpoint_id"]),
            "attempt_id": int(row["attempt_id"]),
            "problem_id": str(row["problem_id"]),
            "sequence": int(row["sequence"]),
            "fencing_token": int(row["fencing_token"]),
            "cursor": _json_load(row["cursor_json"], {}),
            "state": _json_load(row["state_json"], {}),
            "metrics": _json_load(row["metrics_json"], {}),
            "created_at": _iso_timestamp(row["created_at"]),
        }

    @staticmethod
    def _decode_event(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "event_id": int(row["event_id"]),
            "problem_id": str(row["problem_id"]),
            "attempt_id": row["attempt_id"],
            "event_type": str(row["event_type"]),
            "worker_id": row["worker_id"],
            "fencing_token": row["fencing_token"],
            "detail": _json_load(row["detail_json"], {}),
            "created_at": _iso_timestamp(row["created_at"]),
        }


__all__ = [
    "SCHEMA_VERSION",
    "RUNNABLE_STATUSES",
    "TERMINAL_STATUSES",
    "CampaignStatusError",
    "ProblemNotFoundError",
    "LeaseLostError",
    "ClaimedWork",
    "CampaignStatusStore",
]
