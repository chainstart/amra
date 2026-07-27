from __future__ import annotations

import fcntl
import hashlib
import json
import os
import sqlite3
import tempfile
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator

from amra.core.models import ProblemRecord
from amra.discovery.campaign_status import (
    CampaignStatusStore,
    LeaseLostError,
)
from amra.discovery.counterexample_campaign import run_builtin_counterexample_search
from amra.orchestration.workstreams import utc_now_iso
from amra.problem_banks.registry import load_problem_bank


STATUS_DATABASE_FILE = "status.sqlite3"
STATUS_CSV_FILE = "STATUS.csv"
STATUS_JSONL_FILE = "STATUS.jsonl"
STATUS_MARKDOWN_FILE = "STATUS.md"
STATUS_SUMMARY_FILE = "status_summary.json"
FIRST_BATCH_COLLECTION = "first-batch-20"
BACKLOG_COLLECTION = "backlog"
FIRST_BATCH_SCHEMA_VERSION = "amra.counterexample_first_batch.v2"
FIRST_BATCH_ENGINE_VERSION = "amra.counterexample_first_batch.engine.v2"
MAX_RETRY_ATTEMPTS = 3


BUILTIN_SEARCH_SPECS: tuple[dict[str, Any], ...] = (
    {
        "problem_id": "unsolvedmath-guy-a10",
        "source_id": "GUY-A10",
        "title": "Gilbreath's Conjecture",
        "default_bounds": {"max_sequence_terms": 5_000},
        "model_contract": "Repeated prime differences have first entry 1 in every generated row.",
    },
    {
        "problem_id": "unsolvedmath-nt-002",
        "source_id": "NT-002",
        "title": "Collatz Conjecture",
        "default_bounds": {"max_integer": 1_000_000, "max_steps": 20_000},
        "model_contract": "A finite refutation is a nontrivial exact cycle; a step timeout is unknown.",
    },
    {
        "problem_id": "unsolvedmath-nt-006",
        "source_id": "NT-006",
        "title": "Legendre's Conjecture",
        "default_bounds": {"max_square_base": 5_000},
        "model_contract": "Find n whose open interval (n^2,(n+1)^2) contains no prime.",
    },
    {
        "problem_id": "unsolvedmath-opg-2108",
        "source_id": "OPG-2108",
        "title": "Frankl's union-closed sets conjecture",
        "default_bounds": {"max_family_universe": 4},
        "model_contract": (
            "Find a nonempty union-closed finite family in which every element occurs "
            "in fewer than half of the members."
        ),
    },
    {
        "problem_id": "unsolvedmath-opg-37397",
        "source_id": "OPG-37397",
        "title": "Erdős-Straus conjecture",
        "default_bounds": {"max_erdos_straus_n": 5_000},
        "model_contract": "Find n>2 with no exact positive unit-fraction decomposition of 4/n.",
    },
    {
        "problem_id": "unsolvedmath-opg-439",
        "source_id": "OPG-439",
        "title": "Graceful Tree Conjecture",
        "default_bounds": {"max_tree_vertices": 8},
        "model_contract": "Find a finite tree for which every bijective vertex labeling misses an edge difference.",
    },
    {
        "problem_id": "unsolvedmath-opg-658",
        "source_id": "OPG-658",
        "title": "Reconstruction conjecture",
        "default_bounds": {"max_graph_vertices": 6},
        "model_contract": "Find two nonisomorphic finite graphs with identical vertex-deleted decks.",
    },
    {
        "problem_id": "unsolvedmath-opg-706",
        "source_id": "OPG-706",
        "title": "Goldbach conjecture",
        "default_bounds": {"max_integer": 1_000_000},
        "model_contract": "Find an even n>2 with no representation as a sum of two primes.",
    },
)


GRAPH_PROBLEM_IDS: tuple[str, ...] = (
    "unsolvedmath-opg-47343",
    "unsolvedmath-opg-37305",
    "unsolvedmath-opg-1808",
    "unsolvedmath-opg-34839",
    "unsolvedmath-opg-37271",
    "unsolvedmath-opg-46538",
    "unsolvedmath-opg-46824",
    "unsolvedmath-opg-46837",
    "unsolvedmath-opg-47294",
    "unsolvedmath-opg-646",
    "unsolvedmath-opg-700",
    "unsolvedmath-opg-145",
)

FIRST_BATCH_PROBLEM_IDS: tuple[str, ...] = tuple(
    spec["problem_id"] for spec in BUILTIN_SEARCH_SPECS
) + GRAPH_PROBLEM_IDS


def _atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _write_json(path: Path, payload: Any) -> None:
    _atomic_write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


@contextmanager
def _campaign_directory_lock(campaign_dir: Path) -> Iterator[None]:
    descriptor = os.open(campaign_dir, os.O_RDONLY)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _statement_hash(problem: ProblemRecord) -> str:
    return hashlib.sha256(problem.statement.encode("utf-8")).hexdigest()


def _search_config_fingerprint(problem: ProblemRecord, spec: dict[str, Any]) -> str:
    payload = json.dumps(
        {
            "schema_version": FIRST_BATCH_SCHEMA_VERSION,
            "engine_version": FIRST_BATCH_ENGINE_VERSION,
            "problem_id": problem.problem_id,
            "statement_hash": _statement_hash(problem),
            "bounds": spec.get("default_bounds", {}),
            "model": spec.get("model_contract") or spec.get("model"),
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _catalog_record_fingerprint(
    problem: ProblemRecord,
    *,
    selected: bool,
    batch_rank: int | None,
    search_config_fingerprint: str | None,
    baseline_result: dict[str, Any],
) -> str:
    metadata = problem.metadata or {}
    payload = json.dumps(
        {
            "problem_id": problem.problem_id,
            "title": problem.title,
            "source": problem.source,
            "domain": problem.domain,
            "statement_hash": _statement_hash(problem),
            "source_id": metadata.get("source_id"),
            "source_url": metadata.get("source_url"),
            "difficulty_level": metadata.get("difficulty_level"),
            "sets": metadata.get("sets", []),
            "selected": selected,
            "batch_rank": batch_rank,
            "search_config_fingerprint": search_config_fingerprint,
            "baseline_status": baseline_result.get("status", "not_screened"),
            "baseline_claim_kind": (
                baseline_result.get("classification") or {}
            ).get("claim_kind"),
            "baseline_outcome": (
                baseline_result.get("search_execution") or {}
            ).get("outcome"),
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _status_row_is_current(
    row: dict[str, Any],
    problem: ProblemRecord,
    *,
    selected: bool,
    catalog_record_fingerprint: str,
    search_config_fingerprint: str | None,
) -> bool:
    metadata = row["metadata"]
    expected_collection = (
        FIRST_BATCH_COLLECTION if selected else BACKLOG_COLLECTION
    )
    return bool(
        row["title"] == problem.title
        and row["source"] == problem.source
        and row["domain"] == problem.domain
        and row["statement_hash"] == _statement_hash(problem)
        and row["collection"] == expected_collection
        and metadata.get("catalog_record_fingerprint")
        == catalog_record_fingerprint
        and (
            not selected
            or (
                metadata.get("search_config_fingerprint")
                == search_config_fingerprint
                and metadata.get("search_generation")
            )
        )
    )


def _load_baseline_results(campaign_dir: Path) -> dict[str, dict[str, Any]]:
    path = campaign_dir / "results.jsonl"
    if not path.exists():
        return {}
    results: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        problem_id = str(row.get("problem_id", "")).strip()
        if problem_id:
            results[problem_id] = row
    return results


def _graph_specs() -> dict[str, dict[str, Any]]:
    from amra.discovery.first_batch_graphs import GRAPH_SEARCH_SPECS

    if isinstance(GRAPH_SEARCH_SPECS, dict):
        raw_specs: Iterable[dict[str, Any]] = GRAPH_SEARCH_SPECS.values()
    else:
        raw_specs = GRAPH_SEARCH_SPECS
    specs = {str(spec["problem_id"]): dict(spec) for spec in raw_specs}
    missing = [problem_id for problem_id in GRAPH_PROBLEM_IDS if problem_id not in specs]
    if missing:
        raise RuntimeError(f"Missing first-batch graph search specs: {', '.join(missing)}")
    return specs


def first_batch_specs() -> list[dict[str, Any]]:
    graph_specs = _graph_specs()
    return [
        *[dict(spec) for spec in BUILTIN_SEARCH_SPECS],
        *[graph_specs[problem_id] for problem_id in GRAPH_PROBLEM_IDS],
    ]


def initialize_status_table(
    *,
    bank_path: Path,
    campaign_dir: Path,
    reset_first_batch: bool = False,
) -> dict[str, Any]:
    bank_path = bank_path.expanduser().resolve()
    campaign_dir = campaign_dir.expanduser().resolve()
    campaign_dir.mkdir(parents=True, exist_ok=True)
    problems = load_problem_bank(bank_path)
    problem_ids = {problem.problem_id for problem in problems}
    missing = [problem_id for problem_id in FIRST_BATCH_PROBLEM_IDS if problem_id not in problem_ids]
    if missing:
        raise ValueError(f"First-batch problems missing from bank: {', '.join(missing)}")

    baseline = _load_baseline_results(campaign_dir)
    ranks = {problem_id: rank for rank, problem_id in enumerate(FIRST_BATCH_PROBLEM_IDS, start=1)}
    specs = {spec["problem_id"]: spec for spec in first_batch_specs()}
    catalog_fingerprints: dict[str, str] = {}
    config_fingerprints: dict[str, str | None] = {}
    for problem in problems:
        selected = problem.problem_id in ranks
        config_fingerprint = (
            _search_config_fingerprint(problem, specs[problem.problem_id])
            if selected
            else None
        )
        config_fingerprints[problem.problem_id] = config_fingerprint
        catalog_fingerprints[problem.problem_id] = _catalog_record_fingerprint(
            problem,
            selected=selected,
            batch_rank=ranks.get(problem.problem_id),
            search_config_fingerprint=config_fingerprint,
            baseline_result=baseline.get(problem.problem_id, {}),
        )

    with _campaign_directory_lock(campaign_dir):
        store = CampaignStatusStore(campaign_dir / STATUS_DATABASE_FILE)
        recovered = store.recover_expired_leases()
        existing_rows = {
            row["problem_id"]: row for row in store.list_problems()
        }
        refresh_skipped = bool(
            not reset_first_batch
            and set(existing_rows) == problem_ids
            and all(
                _status_row_is_current(
                    existing_rows[problem.problem_id],
                    problem,
                    selected=problem.problem_id in ranks,
                    catalog_record_fingerprint=catalog_fingerprints[
                        problem.problem_id
                    ],
                    search_config_fingerprint=config_fingerprints[
                        problem.problem_id
                    ],
                )
                for problem in problems
            )
        )
        inserted = 0
        refreshed = 0
        pruned: list[str] = []
        if not refresh_skipped:
            for index, problem in enumerate(problems, start=1):
                selected = problem.problem_id in ranks
                previous = existing_rows.get(problem.problem_id)
                result = baseline.get(problem.problem_id, {})
                metadata = problem.metadata or {}
                collection = (
                    FIRST_BATCH_COLLECTION if selected else BACKLOG_COLLECTION
                )
                status = "queued" if selected else "parked"
                reset_reasons: list[str] = []
                if reset_first_batch and selected:
                    reset_reasons.append("operator_requested_rerun")
                if (
                    selected
                    and previous is not None
                    and previous["collection"] != FIRST_BATCH_COLLECTION
                ):
                    reset_reasons.append("promoted_to_first_batch")
                config_fingerprint = config_fingerprints[problem.problem_id]
                if selected and previous is not None:
                    previous_config = previous["metadata"].get(
                        "search_config_fingerprint"
                    )
                    if previous["statement_hash"] != _statement_hash(problem):
                        reset_reasons.append("statement_changed")
                    if previous_config != config_fingerprint:
                        reset_reasons.append(
                            "search_config_changed_or_missing"
                        )
                    if not previous["metadata"].get("search_generation"):
                        reset_reasons.append("legacy_generation_missing")
                reset_status = bool(reset_reasons)
                previous_generation = max(
                    int(
                        ((previous or {}).get("metadata") or {}).get(
                            "search_generation"
                        )
                        or 0
                    ),
                    int((previous or {}).get("attempt_count") or 0),
                )
                search_generation = (
                    previous_generation + 1
                    if selected and reset_status
                    else max(1, previous_generation)
                    if selected
                    else None
                )
                store.upsert_problem(
                    problem.problem_id,
                    title=problem.title,
                    source=problem.source,
                    domain=problem.domain,
                    collection=collection,
                    priority=float(
                        10_000 - ranks[problem.problem_id]
                        if selected
                        else -index
                    ),
                    stage="G2" if selected else "G0",
                    status=status,
                    statement_hash=_statement_hash(problem),
                    reset_status=reset_status,
                    reset_reason=";".join(reset_reasons),
                    metadata={
                        "source_id": metadata.get("source_id"),
                        "source_url": metadata.get("source_url"),
                        "difficulty_level": metadata.get("difficulty_level"),
                        "sets": metadata.get("sets", []),
                        "batch": 1 if selected else None,
                        "batch_rank": ranks.get(problem.problem_id),
                        "selected": selected,
                        "search_config_fingerprint": config_fingerprint,
                        "search_generation": search_generation,
                        "search_engine_version": (
                            FIRST_BATCH_ENGINE_VERSION if selected else None
                        ),
                        "catalog_record_fingerprint": catalog_fingerprints[
                            problem.problem_id
                        ],
                        "baseline_status": result.get(
                            "status", "not_screened"
                        ),
                        "baseline_claim_kind": (
                            result.get("classification") or {}
                        ).get("claim_kind"),
                        "baseline_outcome": (
                            result.get("search_execution") or {}
                        ).get("outcome"),
                    },
                )
                if previous is None:
                    inserted += 1
                else:
                    refreshed += 1

            pruned = store.prune_problems_not_in(problem_ids)

    paths = export_status_tables(campaign_dir)
    return {
        "schema_version": FIRST_BATCH_SCHEMA_VERSION,
        "database": str(store.path),
        "bank": str(bank_path),
        "inserted": inserted,
        "refreshed": refreshed,
        "pruned": pruned,
        "recovered_expired_leases": recovered,
        "refresh_skipped": refresh_skipped,
        "first_batch_count": len(FIRST_BATCH_PROBLEM_IDS),
        "summary": store.summary(),
        "artifacts": paths,
    }


def _builtin_spec(problem_id: str) -> dict[str, Any] | None:
    return next(
        (dict(spec) for spec in BUILTIN_SEARCH_SPECS if spec["problem_id"] == problem_id),
        None,
    )


def _execute_search(
    problem: ProblemRecord,
    *,
    checkpoint: dict[str, Any] | None,
    search_config_fingerprint: str,
    search_generation: int,
    progress: Callable[[dict[str, Any], int], None] | None = None,
) -> dict[str, Any]:
    checkpoint_matches = _checkpoint_matches(
        checkpoint,
        problem=problem,
        search_config_fingerprint=search_config_fingerprint,
        search_generation=search_generation,
    )
    active_checkpoint = checkpoint if checkpoint_matches else None
    stored_cursor = dict((active_checkpoint or {}).get("cursor") or {})
    stored_state = dict((active_checkpoint or {}).get("state") or {})
    if stored_cursor.get("phase") == "search_completed":
        artifact_value = str(stored_state.get("attempt_artifact") or "")
        artifact = Path(artifact_value) if artifact_value else None
        if artifact is not None and artifact.exists():
            try:
                restored = json.loads(artifact.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                restored = {}
            if (
                restored.get("problem_id") == problem.problem_id
                and restored.get("statement_hash") == _statement_hash(problem)
                and restored.get("search_config_fingerprint")
                == search_config_fingerprint
                and restored.get("search_generation") == search_generation
            ):
                restored["resumed_from_completed_artifact"] = True
                return restored

    started = time.monotonic()
    builtin = _builtin_spec(problem.problem_id)
    if builtin is not None:
        execution = run_builtin_counterexample_search(
            problem,
            budget=dict(builtin["default_bounds"]),
        )
        model_contract = builtin["model_contract"]
    else:
        from amra.discovery.first_batch_graphs import GRAPH_SEARCH_SPECS, run_graph_search

        spec = dict(GRAPH_SEARCH_SPECS[problem.problem_id])
        bounds = dict(spec["default_bounds"])
        chunk_cases = 50_000
        bounds["max_cases"] = chunk_cases
        graph_checkpoint = (
            {"next_case": int(stored_cursor["next_case"])}
            if "next_case" in stored_cursor
            else None
        )
        total_checked = int(
            ((active_checkpoint or {}).get("metrics") or {}).get(
                "checked_cases_total", 0
            )
        )
        while True:
            execution = run_graph_search(
                problem.problem_id,
                bounds=bounds,
                checkpoint=graph_checkpoint,
            )
            total_checked += int(execution.get("checked_cases", 0) or 0)
            graph_checkpoint = dict(execution.get("checkpoint") or {})
            if progress is not None:
                progress(graph_checkpoint, total_checked)
            if execution.get("outcome") != "paused":
                break
        execution["checked_cases"] = total_checked
        execution["bounds"] = {
            **dict(execution.get("bounds") or {}),
            "max_cases": 0,
            "max_cases_per_checkpoint": chunk_cases,
        }
        model_contract = execution.get("model_contract")
    candidate = execution.get("candidate")
    return {
        "schema_version": FIRST_BATCH_SCHEMA_VERSION,
        "search_engine_version": FIRST_BATCH_ENGINE_VERSION,
        "search_config_fingerprint": search_config_fingerprint,
        "search_generation": search_generation,
        "problem_id": problem.problem_id,
        "source_id": str((problem.metadata or {}).get("source_id", "")),
        "title": problem.title,
        "statement_hash": _statement_hash(problem),
        "generated_at": utc_now_iso(),
        "duration_seconds": round(time.monotonic() - started, 6),
        "outcome": execution.get("outcome", "inconclusive"),
        "evidence_level": "exact_candidate" if candidate else "scoped_null_result",
        "candidate_counterexample": candidate,
        "independently_verified": False,
        "model_contract": model_contract,
        "verification_boundary": (
            "A candidate requires an independent verifier and a source-statement audit. "
            "No candidate within the recorded finite scope does not prove the conjecture."
        ),
        "execution": execution,
    }


def _write_attempt_artifact(
    campaign_dir: Path,
    *,
    problem_id: str,
    attempt_id: int,
    result: dict[str, Any],
) -> Path:
    path = campaign_dir / "attempts" / problem_id / f"attempt-{attempt_id:06d}.json"
    result["attempt_artifact"] = str(path)
    _write_json(path, result)
    return path


def _checkpoint_matches(
    checkpoint: dict[str, Any] | None,
    *,
    problem: ProblemRecord,
    search_config_fingerprint: str,
    search_generation: int,
) -> bool:
    state = dict((checkpoint or {}).get("state") or {})
    return bool(
        checkpoint
        and state.get("problem_id") == problem.problem_id
        and state.get("statement_hash") == _statement_hash(problem)
        and state.get("search_config_fingerprint") == search_config_fingerprint
        and state.get("search_generation") == search_generation
    )


def _checkpoint_state(
    problem: ProblemRecord,
    *,
    attempt_id: int,
    search_config_fingerprint: str,
    search_generation: int,
    attempt_artifact: str | None = None,
) -> dict[str, Any]:
    state = {
        "attempt_id": attempt_id,
        "problem_id": problem.problem_id,
        "statement_hash": _statement_hash(problem),
        "search_config_fingerprint": search_config_fingerprint,
        "search_generation": search_generation,
    }
    if attempt_artifact is not None:
        state["attempt_artifact"] = attempt_artifact
    return state


@contextmanager
def _lease_heartbeat(
    store: CampaignStatusStore,
    *,
    problem_id: str,
    worker_id: str,
    fencing_token: int,
    lease_seconds: float,
) -> Iterator[list[BaseException]]:
    stop = threading.Event()
    errors: list[BaseException] = []
    interval = max(0.01, min(30.0, lease_seconds / 3.0))

    def renew() -> None:
        while not stop.wait(interval):
            try:
                store.heartbeat(
                    problem_id,
                    worker_id,
                    fencing_token,
                    extend_seconds=lease_seconds,
                )
            except BaseException as exc:
                errors.append(exc)
                return

    thread = threading.Thread(
        target=renew,
        name=f"lease-heartbeat-{problem_id}",
        daemon=True,
    )
    thread.start()
    try:
        yield errors
    finally:
        stop.set()
        thread.join(timeout=max(1.0, interval + 1.0))


def run_first_batch(
    *,
    bank_path: Path,
    campaign_dir: Path,
    resume: bool = True,
    max_problems: int | None = None,
    worker_id: str = "first-batch-worker",
    lease_seconds: float = 3_600,
) -> dict[str, Any]:
    campaign_dir = campaign_dir.expanduser().resolve()
    initialization = initialize_status_table(
        bank_path=bank_path,
        campaign_dir=campaign_dir,
        reset_first_batch=not resume,
    )
    store = CampaignStatusStore(campaign_dir / STATUS_DATABASE_FILE)
    store.recover_expired_leases()
    problem_by_id = {
        problem.problem_id: problem
        for problem in load_problem_bank(bank_path.expanduser().resolve())
    }
    completed: list[str] = []
    failed: list[str] = []
    interrupted: list[str] = []
    candidates: list[str] = []
    limit = None if max_problems is None else max(0, int(max_problems))

    while limit is None or len(completed) + len(failed) + len(interrupted) < limit:
        claim = store.claim(
            worker_id,
            lease_seconds=lease_seconds,
            collections=[FIRST_BATCH_COLLECTION],
            method="deterministic-bounded-counterexample-search",
        )
        if claim is None:
            break
        problem = problem_by_id[claim.problem_id]
        try:
            config_fingerprint = str(
                claim.problem["metadata"]["search_config_fingerprint"]
            )
            search_generation = int(claim.problem["metadata"]["search_generation"])
            resumable_checkpoint = (
                claim.latest_checkpoint
                if resume
                and _checkpoint_matches(
                    claim.latest_checkpoint,
                    problem=problem,
                    search_config_fingerprint=config_fingerprint,
                    search_generation=search_generation,
                )
                else None
            )
            inherited_cursor = dict(
                (resumable_checkpoint or {}).get("cursor") or {}
            )
            inherited_metrics = dict(
                (resumable_checkpoint or {}).get("metrics") or {}
            )
            store.save_checkpoint(
                claim.problem_id,
                worker_id,
                claim.fencing_token,
                cursor={
                    "phase": "search_started",
                    **(
                        {"next_case": inherited_cursor["next_case"]}
                        if "next_case" in inherited_cursor
                        else {}
                    ),
                },
                state=_checkpoint_state(
                    problem,
                    attempt_id=claim.attempt_id,
                    search_config_fingerprint=config_fingerprint,
                    search_generation=search_generation,
                ),
                metrics={
                    "checked_cases_total": int(
                        inherited_metrics.get("checked_cases_total", 0) or 0
                    )
                },
            )

            def record_progress(cursor: dict[str, Any], checked: int) -> None:
                store.save_checkpoint(
                    claim.problem_id,
                    worker_id,
                    claim.fencing_token,
                    cursor={"phase": "graph_search", **cursor},
                    state=_checkpoint_state(
                        problem,
                        attempt_id=claim.attempt_id,
                        search_config_fingerprint=config_fingerprint,
                        search_generation=search_generation,
                    ),
                    metrics={"checked_cases_total": checked},
                )

            with _lease_heartbeat(
                store,
                problem_id=claim.problem_id,
                worker_id=worker_id,
                fencing_token=claim.fencing_token,
                lease_seconds=lease_seconds,
            ) as heartbeat_errors:
                result = _execute_search(
                    problem,
                    checkpoint=resumable_checkpoint,
                    search_config_fingerprint=config_fingerprint,
                    search_generation=search_generation,
                    progress=record_progress,
                )
            if heartbeat_errors:
                raise heartbeat_errors[0]
            artifact = _write_attempt_artifact(
                campaign_dir,
                problem_id=claim.problem_id,
                attempt_id=claim.attempt_id,
                result=result,
            )
            execution_checkpoint = dict(
                ((result.get("execution") or {}).get("checkpoint") or {})
            )
            store.save_checkpoint(
                claim.problem_id,
                worker_id,
                claim.fencing_token,
                cursor={"phase": "search_completed", **execution_checkpoint},
                state=_checkpoint_state(
                    problem,
                    attempt_id=claim.attempt_id,
                    search_config_fingerprint=config_fingerprint,
                    search_generation=search_generation,
                    attempt_artifact=str(artifact),
                ),
                metrics={
                    "checked_cases_total": int(
                        (result.get("execution") or {}).get("checked_cases", 0) or 0
                    )
                },
            )
            store.complete(
                claim.problem_id,
                worker_id,
                claim.fencing_token,
                result=result,
                stage="G2",
            )
            completed.append(claim.problem_id)
            if result.get("candidate_counterexample"):
                candidates.append(claim.problem_id)
        except LeaseLostError:
            interrupted.append(claim.problem_id)
        except KeyboardInterrupt:
            try:
                store.interrupt(
                    claim.problem_id,
                    worker_id,
                    claim.fencing_token,
                    reason="campaign interrupted by operator",
                )
            except LeaseLostError:
                pass
            interrupted.append(claim.problem_id)
            export_status_tables(campaign_dir)
            break
        except Exception as exc:
            retryable = bool(
                isinstance(
                    exc,
                    (OSError, TimeoutError, ConnectionError, sqlite3.OperationalError),
                )
                and int(claim.problem.get("attempt_count") or 0)
                < MAX_RETRY_ATTEMPTS
            )
            try:
                error = f"{type(exc).__name__}: {exc}"
                if retryable:
                    store.fail(
                        claim.problem_id,
                        worker_id,
                        claim.fencing_token,
                        error=error,
                        retryable=True,
                        retry_after_seconds=60,
                    )
                else:
                    store.park(
                        claim.problem_id,
                        worker_id,
                        claim.fencing_token,
                        reason=error,
                        result={
                            "error_class": type(exc).__name__,
                            "retry_limit": MAX_RETRY_ATTEMPTS,
                        },
                    )
            except LeaseLostError:
                pass
            failed.append(claim.problem_id)
        export_status_tables(campaign_dir)

    paths = export_status_tables(campaign_dir)
    return {
        "schema_version": FIRST_BATCH_SCHEMA_VERSION,
        "generated_at": utc_now_iso(),
        "resume": resume,
        "initialization": initialization,
        "processed_this_run": len(completed) + len(failed) + len(interrupted),
        "completed_this_run": completed,
        "failed_this_run": failed,
        "interrupted_this_run": interrupted,
        "candidate_counterexamples": candidates,
        "summary": store.summary(),
        "artifacts": paths,
    }


def export_status_tables(campaign_dir: Path) -> dict[str, str]:
    campaign_dir = campaign_dir.expanduser().resolve()
    campaign_dir.mkdir(parents=True, exist_ok=True)
    database_path = campaign_dir / STATUS_DATABASE_FILE
    with _campaign_directory_lock(campaign_dir):
        if not database_path.exists():
            CampaignStatusStore(database_path)
        return _export_status_tables_unlocked(campaign_dir)


def _export_status_tables_unlocked(campaign_dir: Path) -> dict[str, str]:
    store = CampaignStatusStore(campaign_dir / STATUS_DATABASE_FILE)
    csv_path = store.export_csv(campaign_dir / STATUS_CSV_FILE)
    jsonl_path = store.export_jsonl(campaign_dir / STATUS_JSONL_FILE)
    summary = store.summary()
    summary_path = campaign_dir / STATUS_SUMMARY_FILE
    _write_json(summary_path, summary)

    rows = store.list_problems(collection=FIRST_BATCH_COLLECTION)
    lines = [
        "# UnsolvedMath Counterexample Campaign Status",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "The SQLite database is authoritative. CSV, JSONL, and this report are derived views.",
        "",
        "## Totals",
        "",
        f"- Problems: {summary['total_problems']}",
        f"- Attempts: {summary['attempts']}",
        f"- Checkpoints: {summary['checkpoints']}",
        f"- Statuses: `{json.dumps(summary['status_counts'], sort_keys=True)}`",
        "",
        "## First Batch",
        "",
        "| Rank | Source ID | Problem | Status | Outcome | Checked | Bounds |",
        "| ---: | --- | --- | --- | --- | ---: | --- |",
    ]
    for row in sorted(rows, key=lambda item: item["metadata"].get("batch_rank") or 999):
        result = row.get("last_result") or {}
        execution = result.get("execution") or {}
        source_id = str(row["metadata"].get("source_id") or "")
        title = str(row["title"]).replace("|", "\\|")
        outcome = str(result.get("outcome") or row["metadata"].get("baseline_outcome") or "")
        checked = execution.get("checked_cases", "")
        bounds = json.dumps(execution.get("bounds", {}), ensure_ascii=False, sort_keys=True)
        lines.append(
            f"| {row['metadata'].get('batch_rank')} | `{source_id}` | {title} | "
            f"`{row['status']}` | `{outcome}` | {checked} | `{bounds}` |"
        )
    lines.extend(
        [
            "",
            "A scoped null result means only that no counterexample was found within the recorded bounds.",
            "",
        ]
    )
    markdown_path = campaign_dir / STATUS_MARKDOWN_FILE
    _atomic_write_text(markdown_path, "\n".join(lines))
    return {
        "database": str(store.path),
        "csv": str(csv_path),
        "jsonl": str(jsonl_path),
        "markdown": str(markdown_path),
        "summary": str(summary_path),
    }


def status_summary(campaign_dir: Path) -> dict[str, Any]:
    campaign_dir = campaign_dir.expanduser().resolve()
    database_path = campaign_dir / STATUS_DATABASE_FILE
    if not database_path.exists():
        raise FileNotFoundError(
            f"counterexample campaign status database not found: {database_path}"
        )
    paths = export_status_tables(campaign_dir)
    store = CampaignStatusStore(database_path)
    rows = store.list_problems(collection=FIRST_BATCH_COLLECTION)
    return {
        "schema_version": FIRST_BATCH_SCHEMA_VERSION,
        "summary": store.summary(),
        "first_batch": [
            {
                "problem_id": row["problem_id"],
                "source_id": row["metadata"].get("source_id"),
                "title": row["title"],
                "status": row["status"],
                "outcome": (row.get("last_result") or {}).get("outcome"),
                "attempt_count": row["attempt_count"],
            }
            for row in sorted(rows, key=lambda item: item["metadata"].get("batch_rank") or 999)
        ],
        "artifacts": paths,
    }


__all__ = [
    "BACKLOG_COLLECTION",
    "BUILTIN_SEARCH_SPECS",
    "FIRST_BATCH_COLLECTION",
    "FIRST_BATCH_ENGINE_VERSION",
    "FIRST_BATCH_PROBLEM_IDS",
    "FIRST_BATCH_SCHEMA_VERSION",
    "GRAPH_PROBLEM_IDS",
    "STATUS_CSV_FILE",
    "STATUS_DATABASE_FILE",
    "STATUS_JSONL_FILE",
    "STATUS_MARKDOWN_FILE",
    "MAX_RETRY_ATTEMPTS",
    "export_status_tables",
    "first_batch_specs",
    "initialize_status_table",
    "run_first_batch",
    "status_summary",
]
