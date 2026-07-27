from __future__ import annotations

import csv
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from amra.discovery.campaign_status import (
    CampaignStatusError,
    CampaignStatusStore,
    LeaseLostError,
    ProblemNotFoundError,
)


class ManualClock:
    def __init__(self, value: float = 1_800_000_000) -> None:
        self.value = value

    def __call__(self) -> float:
        return self.value

    def advance(self, seconds: float) -> None:
        self.value += seconds


def _add_problem(
    store: CampaignStatusStore,
    problem_id: str,
    *,
    priority: float = 0,
    domain: str = "number_theory",
) -> None:
    store.upsert_problem(
        problem_id,
        title=f"Problem {problem_id}",
        source="UnsolvedMath",
        domain=domain,
        collection="first-20",
        priority=priority,
        statement_hash=f"sha256:{problem_id}",
        metadata={"source_id": problem_id.upper()},
    )


def test_store_uses_wal_and_exports_total_status_table(tmp_path: Path) -> None:
    store = CampaignStatusStore(tmp_path / "campaign.sqlite3")
    _add_problem(store, "p-low", priority=1)
    _add_problem(store, "p-high", priority=10, domain="graph_theory")

    assert store.schema_version == 1
    assert store.journal_mode == "wal"
    assert [row["problem_id"] for row in store.list_problems()] == ["p-high", "p-low"]

    summary = store.summary()
    assert summary["total_problems"] == 2
    assert summary["status_counts"] == {"queued": 2}
    assert summary["domain_counts"] == {"graph_theory": 1, "number_theory": 1}

    jsonl_path = store.export_jsonl(tmp_path / "exports" / "status.jsonl")
    csv_path = store.export_csv(tmp_path / "exports" / "status.csv")
    json_rows = [
        json.loads(line) for line in jsonl_path.read_text(encoding="utf-8").splitlines()
    ]
    with csv_path.open(encoding="utf-8", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))

    assert [row["problem_id"] for row in json_rows] == ["p-high", "p-low"]
    assert [row["problem_id"] for row in csv_rows] == ["p-high", "p-low"]
    assert json.loads(csv_rows[0]["metadata"]) == {"source_id": "P-HIGH"}


def test_claim_checkpoint_heartbeat_complete_and_reopen(tmp_path: Path) -> None:
    clock = ManualClock()
    path = tmp_path / "campaign.sqlite3"
    store = CampaignStatusStore(path, clock=clock)
    _add_problem(store, "p1")

    claim = store.claim(
        "worker-a",
        lease_seconds=60,
        method="bounded-enumeration",
        config={"bound": 100},
    )
    assert claim is not None
    assert claim.problem_id == "p1"
    assert claim.fencing_token == 1
    assert claim.latest_checkpoint is None

    checkpoint = store.save_checkpoint(
        "p1",
        "worker-a",
        claim.fencing_token,
        cursor={"next": 51},
        state={"rng": "fixed"},
        metrics={"objects_checked": 50},
    )
    assert checkpoint["sequence"] == 1
    assert checkpoint["cursor"] == {"next": 51}

    clock.advance(30)
    renewed_until = store.heartbeat(
        "p1", "worker-a", claim.fencing_token, extend_seconds=120
    )
    assert renewed_until.endswith("Z")
    completed = store.complete(
        "p1",
        "worker-a",
        claim.fencing_token,
        result={"counterexample_found": False, "bound": 100},
        stage="G2",
    )
    assert completed["status"] == "completed"
    assert completed["stage"] == "G2"
    assert completed["last_result"]["bound"] == 100
    assert store.claim("worker-b") is None

    reopened = CampaignStatusStore(path, clock=clock)
    assert reopened.get_problem("p1")["status"] == "completed"
    assert reopened.latest_checkpoint("p1")["metrics"]["objects_checked"] == 50
    assert reopened.latest_checkpoints()["p1"]["cursor"] == {"next": 51}
    assert reopened.latest_checkpoints(["p1"])["p1"]["metrics"] == {
        "objects_checked": 50
    }
    assert reopened.latest_checkpoints([]) == {}
    assert reopened.attempts("p1")[0]["config"] == {"bound": 100}


def test_expired_lease_is_resumed_and_stale_worker_is_fenced(tmp_path: Path) -> None:
    clock = ManualClock()
    store = CampaignStatusStore(tmp_path / "campaign.sqlite3", clock=clock)
    _add_problem(store, "p1")

    first = store.claim("worker-a", lease_seconds=10)
    assert first is not None
    store.save_checkpoint(
        "p1",
        "worker-a",
        first.fencing_token,
        cursor={"next": 500},
    )
    clock.advance(11)

    with pytest.raises(LeaseLostError):
        store.save_checkpoint(
            "p1",
            "worker-a",
            first.fencing_token,
            cursor={"next": 999},
        )

    second = store.claim("worker-b", lease_seconds=20)
    assert second is not None
    assert second.attempt_id != first.attempt_id
    assert second.fencing_token > first.fencing_token
    assert second.latest_checkpoint["cursor"] == {"next": 500}

    with pytest.raises(LeaseLostError):
        store.complete("p1", "worker-a", first.fencing_token, result={})

    store.complete("p1", "worker-b", second.fencing_token, result={"checked": 1000})
    assert [attempt["status"] for attempt in store.attempts("p1")] == [
        "expired",
        "completed",
    ]


def test_explicit_recovery_requeues_expired_work_and_fences_owner(tmp_path: Path) -> None:
    clock = ManualClock()
    store = CampaignStatusStore(tmp_path / "campaign.sqlite3", clock=clock)
    _add_problem(store, "p1")
    claim = store.claim("worker-a", lease_seconds=10)
    assert claim is not None

    clock.advance(11)
    assert store.recover_expired_leases() == ["p1"]
    recovered = store.get_problem("p1")
    assert recovered["status"] == "queued"
    assert recovered["lease_owner"] is None
    assert recovered["lease_token"] > claim.fencing_token
    assert store.attempts("p1")[0]["status"] == "expired"


def test_fail_retry_interrupt_and_park_are_atomic_transitions(tmp_path: Path) -> None:
    clock = ManualClock()
    store = CampaignStatusStore(tmp_path / "campaign.sqlite3", clock=clock)
    _add_problem(store, "p1")

    first = store.claim("worker-a")
    assert first is not None
    failed = store.fail(
        "p1",
        "worker-a",
        first.fencing_token,
        error="solver timeout",
        retryable=True,
        retry_after_seconds=30,
    )
    assert failed["status"] == "retry"
    assert store.claim("worker-b") is None

    clock.advance(30)
    second = store.claim("worker-b")
    assert second is not None
    interrupted = store.interrupt(
        "p1", "worker-b", second.fencing_token, reason="planned shutdown"
    )
    assert interrupted["status"] == "queued"

    third = store.claim("worker-c")
    assert third is not None
    parked = store.park(
        "p1",
        "worker-c",
        third.fencing_token,
        reason="statement recovery required",
        result={"missing_source": True},
    )
    assert parked["status"] == "parked"
    assert store.claim("worker-d") is None
    assert [attempt["status"] for attempt in store.attempts("p1")] == [
        "failed",
        "interrupted",
        "parked",
    ]


def test_concurrent_claims_never_return_the_same_problem(tmp_path: Path) -> None:
    path = tmp_path / "campaign.sqlite3"
    store = CampaignStatusStore(path)
    for index in range(8):
        _add_problem(store, f"p-{index}", priority=index)

    def claim(worker: str) -> str:
        independent_store = CampaignStatusStore(path)
        work = independent_store.claim(worker, lease_seconds=60)
        assert work is not None
        return work.problem_id

    with ThreadPoolExecutor(max_workers=8) as executor:
        problem_ids = list(executor.map(claim, [f"worker-{i}" for i in range(8)]))

    assert len(set(problem_ids)) == 8
    assert store.summary()["status_counts"] == {"running": 8}


def test_problem_lookup_and_status_reset_guards(tmp_path: Path) -> None:
    store = CampaignStatusStore(tmp_path / "campaign.sqlite3")
    with pytest.raises(ProblemNotFoundError):
        store.get_problem("missing")

    _add_problem(store, "p1")
    claim = store.claim("worker-a")
    assert claim is not None
    with pytest.raises(Exception, match="active lease"):
        store.upsert_problem(
            "p1",
            title="Changed",
            status="queued",
            reset_status=True,
        )


def test_reset_clears_current_result_and_records_audit_event(tmp_path: Path) -> None:
    store = CampaignStatusStore(tmp_path / "campaign.sqlite3")
    _add_problem(store, "p1")
    claim = store.claim("worker-a")
    assert claim is not None
    store.complete("p1", "worker-a", claim.fencing_token, result={"bound": 100})

    reset = store.upsert_problem(
        "p1",
        title="Problem p1",
        status="queued",
        reset_status=True,
        reset_reason="search_config_changed",
    )

    assert reset["status"] == "queued"
    assert reset["last_result"] is None
    assert reset["last_error"] is None
    assert store.events("p1")[-1]["event_type"] == "reset"
    assert store.events("p1")[-1]["detail"]["reason"] == "search_config_changed"


def test_prune_removes_stale_problem_state_but_not_active_records(
    tmp_path: Path,
) -> None:
    store = CampaignStatusStore(tmp_path / "campaign.sqlite3")
    _add_problem(store, "keep")
    _add_problem(store, "remove", priority=10)
    claim = store.claim("worker-a")
    assert claim is not None
    claimed_id = claim.problem_id
    assert claimed_id == "remove"
    store.save_checkpoint(
        claimed_id,
        "worker-a",
        claim.fencing_token,
        cursor={"next": 2},
    )
    store.complete(claimed_id, "worker-a", claim.fencing_token, result={})

    removed = store.prune_problems_not_in({"keep"})

    assert removed == ["remove"]
    assert [row["problem_id"] for row in store.list_problems()] == ["keep"]
    with pytest.raises(ProblemNotFoundError):
        store.get_problem("remove")


def test_newer_database_schema_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "future.sqlite3"
    with sqlite3.connect(path) as connection:
        connection.execute("PRAGMA user_version = 999")

    with pytest.raises(CampaignStatusError, match="newer than supported"):
        CampaignStatusStore(path)
