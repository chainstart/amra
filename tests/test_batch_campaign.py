from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from amra.discovery.batch_campaign import (
    BatchCampaignCoordinator,
    BatchConfigurationError,
    BatchPlan,
    BatchProblemPlan,
    BatchStateError,
    StrategyBudget,
    StrategyPlan,
)


def _strategy(
    *,
    stage_id: str = "screen",
    strategy_id: str = "enumerate",
    executor_id: str = "test.enumerate",
    launches: int = 1,
    time_seconds: int = 60,
) -> StrategyPlan:
    return StrategyPlan(
        stage_id=stage_id,
        strategy_id=strategy_id,
        executor_id=executor_id,
        executor_version="v1",
        budget=StrategyBudget(
            time_seconds=time_seconds,
            max_cases=1_000,
            memory_mb=256,
            parameters={"bound": 10},
        ),
        launches=launches,
        config={"symmetry_breaking": True},
    )


def _problem(
    problem_id: str = "p1",
    *,
    strategies: tuple[StrategyPlan, ...] | None = None,
    audit: str = "pending",
) -> BatchProblemPlan:
    return BatchProblemPlan(
        problem_id=problem_id,
        title=f"Problem {problem_id}",
        statement_hash=f"sha256:{problem_id}",
        domain="graph_theory",
        source="fixture",
        model_contract={
            "objects": "finite graphs",
            "premise": "P(G)",
            "counterexample": "P(G) and not Q(G)",
        },
        strategies=strategies or (_strategy(),),
        model_audit_status=audit,
        priority=10,
    )


def _plan(
    *,
    problems: tuple[BatchProblemPlan, ...] | None = None,
    seed: int = 20260727,
) -> BatchPlan:
    return BatchPlan(
        batch_id="batch-2",
        collection="counterexample-batch-2",
        problems=problems or (_problem(),),
        global_seed=seed,
        expected_problem_count=len(problems or (_problem(),)),
    )


def _coordinator(
    tmp_path: Path,
    *,
    plan: BatchPlan | None = None,
    executors: tuple[str, ...] = ("test.enumerate",),
) -> BatchCampaignCoordinator:
    return BatchCampaignCoordinator(
        tmp_path / "batch.sqlite3",
        plan or _plan(),
        available_executors=executors,
    )


def test_expected_problem_count_is_enforced_for_second_batch() -> None:
    with pytest.raises(ValueError, match="expects 100 problems"):
        BatchPlan(
            batch_id="batch-2",
            collection="batch-2",
            problems=(_problem(),),
            global_seed=7,
            expected_problem_count=100,
        )


def test_one_hundred_problem_batch_initializes_without_first_batch_constants(
    tmp_path: Path,
) -> None:
    problems = tuple(_problem(f"p-{index:03d}") for index in range(100))
    plan = BatchPlan(
        batch_id="batch-2-100",
        collection="counterexample-batch-2-100",
        problems=problems,
        global_seed=7,
        expected_problem_count=100,
    )
    coordinator = _coordinator(tmp_path, plan=plan, executors=())

    initialized = coordinator.initialize()

    assert initialized["problem_count"] == 100
    assert initialized["task_count"] == 100
    assert initialized["summary"]["task_status_counts"] == {"parked": 100}
    assert initialized["summary"]["model_audit_status_counts"] == {"pending": 100}
    assert initialized["summary"]["stop_reason_counts"] == {
        "executor_not_registered": 100
    }
    assert coordinator.claim("worker-a") is None


def test_model_audit_gates_registered_tasks_and_unimplemented_tasks_stay_parked(
    tmp_path: Path,
) -> None:
    problem = _problem(
        strategies=(
            _strategy(launches=2),
            _strategy(
                stage_id="deep",
                strategy_id="sat",
                executor_id="missing.sat",
                time_seconds=600,
            ),
        )
    )
    coordinator = _coordinator(tmp_path, plan=_plan(problems=(problem,)))

    initialized = coordinator.initialize()
    assert initialized["problem_count"] == 1
    assert initialized["task_count"] == 3
    assert initialized["summary"]["task_status_counts"] == {"parked": 3}
    assert coordinator.claim("worker-a") is None

    audited = coordinator.record_model_audit(
        "p1",
        status="approved",
        auditor_id="model-auditor",
        detail={"premise_checked": True, "negation_checked": True},
    )
    assert audited["model_audit_status"] == "approved"

    tasks = coordinator.tasks()
    screen = [task for task in tasks if task["metadata"]["stage_id"] == "screen"]
    deep = [task for task in tasks if task["metadata"]["stage_id"] == "deep"]
    assert {task["status"] for task in screen} == {"queued"}
    assert {task["status"] for task in deep} == {"parked"}
    assert deep[0]["metadata"]["planned_stop_reason"] == "executor_not_registered"
    assert coordinator.summary()["stop_reason_counts"] == {
        "executor_not_registered": 1
    }


def test_multistart_seeds_are_distinct_and_stable_across_reopen(tmp_path: Path) -> None:
    problem = _problem(
        strategies=(_strategy(launches=3),),
        audit="approved",
    )
    plan = _plan(problems=(problem,), seed=91)
    first = _coordinator(tmp_path, plan=plan)
    first.initialize()
    first_seeds = {
        task["metadata"]["launch_index"]: task["metadata"]["deterministic_seed"]
        for task in first.tasks()
    }

    reopened = _coordinator(tmp_path, plan=plan)
    reopened.initialize()
    second_seeds = {
        task["metadata"]["launch_index"]: task["metadata"]["deterministic_seed"]
        for task in reopened.tasks()
    }

    assert first_seeds == second_seeds
    assert len(set(first_seeds.values())) == 3
    assert all(0 <= seed < 2**63 for seed in first_seeds.values())


def test_worker_claims_only_tasks_for_its_registered_executors(tmp_path: Path) -> None:
    problem = _problem(
        strategies=(
            _strategy(strategy_id="enum-a", executor_id="executor.a"),
            _strategy(strategy_id="enum-b", executor_id="executor.b"),
        ),
        audit="approved",
    )
    plan = _plan(problems=(problem,))
    initializer = _coordinator(
        tmp_path,
        plan=plan,
        executors=("executor.a", "executor.b"),
    )
    initializer.initialize()

    worker_a = _coordinator(
        tmp_path,
        plan=plan,
        executors=("executor.a",),
    )
    worker_a.initialize()
    claim = worker_a.claim("worker-a")
    assert claim is not None
    assert claim.executor_id == "executor.a"
    worker_a.complete(
        claim,
        outcome="no_candidate",
        stop_reason="finite_bound_exhausted",
    )
    assert worker_a.claim("worker-a") is None

    remaining = [
        task
        for task in initializer.tasks()
        if task["status"] == "queued"
    ]
    assert len(remaining) == 1
    assert remaining[0]["metadata"]["executor_id"] == "executor.b"
    assert remaining[0]["metadata"]["implementation_status"] == "registered"


def test_checkpoint_resume_preserves_strategy_identity_seed_and_cursor(
    tmp_path: Path,
) -> None:
    coordinator = _coordinator(
        tmp_path,
        plan=_plan(problems=(_problem(audit="approved"),)),
    )
    coordinator.initialize()
    first = coordinator.claim("worker-a", lease_seconds=60)
    assert first is not None
    checkpoint = coordinator.save_checkpoint(
        first,
        cursor={"next_case": 501},
        state={"rng_state": "deterministic-state"},
        metrics={"checked_cases": 500},
    )
    assert checkpoint["state"]["config_fingerprint"] == first.config_fingerprint
    coordinator.interrupt(first, stop_reason="planned_restart")

    second = coordinator.claim("worker-b", lease_seconds=60)
    assert second is not None
    assert second.task_id == first.task_id
    assert second.deterministic_seed == first.deterministic_seed
    assert second.config_fingerprint == first.config_fingerprint
    assert second.checkpoint is not None
    assert second.checkpoint["cursor"] == {"next_case": 501}
    assert second.checkpoint["state"]["executor_state"] == {
        "rng_state": "deterministic-state"
    }
    coordinator.complete(
        second,
        outcome="no_candidate",
        stop_reason="finite_bound_exhausted",
        metrics={"checked_cases": 1_000},
        final_cursor={"next_case": 1_001},
    )
    result = coordinator.store.get_problem(second.task_id)["last_result"]
    assert result["stop_reason"] == "finite_bound_exhausted"
    assert result["budget"]["time_seconds"] == 60


def test_later_stage_requires_terminal_earlier_stage(tmp_path: Path) -> None:
    problem = _problem(
        strategies=(
            _strategy(stage_id="screen", strategy_id="enum"),
            _strategy(
                stage_id="deep",
                strategy_id="random-restart",
                executor_id="test.random",
                time_seconds=900,
            ),
        ),
        audit="approved",
    )
    coordinator = _coordinator(
        tmp_path,
        plan=_plan(problems=(problem,)),
        executors=("test.enumerate", "test.random"),
    )
    coordinator.initialize()
    with pytest.raises(BatchStateError, match="earlier stages are not terminal"):
        coordinator.activate_stage("p1", "deep")

    claim = coordinator.claim("worker-a")
    assert claim is not None
    assert claim.stage_id == "screen"
    coordinator.complete(
        claim,
        outcome="no_candidate",
        stop_reason="screen_budget_exhausted",
    )
    activated = coordinator.activate_stage("p1", "deep")
    assert len(activated) == 1
    deep = coordinator.claim("worker-b")
    assert deep is not None
    assert deep.stage_id == "deep"
    assert deep.budget["time_seconds"] == 900


def test_candidate_requires_a_different_worker_for_independent_verification(
    tmp_path: Path,
) -> None:
    coordinator = _coordinator(
        tmp_path,
        plan=_plan(problems=(_problem(audit="approved"),)),
    )
    coordinator.initialize()
    claim = coordinator.claim("search-worker")
    assert claim is not None
    coordinator.complete(
        claim,
        outcome="candidate",
        stop_reason="candidate_found",
        candidate={"n": 17, "certificate": [1, 2, 3]},
    )
    state = coordinator.problem_state("p1")
    assert state["verification_status"] == "pending"
    assert state["stop_reason"] == "candidate_requires_review"

    with pytest.raises(BatchStateError, match="cannot independently verify"):
        coordinator.record_independent_verification(
            "p1",
            verifier_id="search-worker",
            verdict="verified",
            evidence={"replayed": True},
        )

    verified = coordinator.record_independent_verification(
        "p1",
        verifier_id="independent-worker",
        verdict="verified",
        evidence={"implementation": "second", "replayed": True},
    )
    assert verified["verification_status"] == "verified"

    contested = coordinator.record_independent_verification(
        "p1",
        verifier_id="third-worker",
        verdict="rejected",
        evidence={"premise_failed": True},
    )
    assert contested["verification_status"] == "contested"


def test_all_workers_that_produced_the_same_candidate_are_not_independent(
    tmp_path: Path,
) -> None:
    coordinator = _coordinator(
        tmp_path,
        plan=_plan(
            problems=(
                _problem(
                    strategies=(_strategy(launches=2),),
                    audit="approved",
                ),
            )
        ),
    )
    coordinator.initialize()
    candidate = {"graph6": "Dhc"}
    for worker_id in ("search-a", "search-b"):
        claim = coordinator.claim(worker_id)
        assert claim is not None
        coordinator.complete(
            claim,
            outcome="candidate",
            stop_reason="candidate_found",
            candidate=candidate,
        )

    for producer_id in ("search-a", "search-b"):
        with pytest.raises(BatchStateError, match="cannot independently verify"):
            coordinator.record_independent_verification(
                "p1",
                verifier_id=producer_id,
                verdict="verified",
                evidence={"replayed": True},
            )


def test_same_batch_is_idempotent_but_changed_plan_is_rejected(tmp_path: Path) -> None:
    coordinator = _coordinator(tmp_path)
    first = coordinator.initialize()
    second = coordinator.initialize()
    assert first["inserted_tasks"] == 1
    assert second["inserted_tasks"] == 0

    changed_problem = replace(
        _problem(),
        strategies=(_strategy(time_seconds=120),),
    )
    changed = _coordinator(
        tmp_path,
        plan=_plan(problems=(changed_problem,)),
    )
    with pytest.raises(BatchConfigurationError, match="different plan"):
        changed.initialize()


def test_invalid_result_shape_never_creates_a_candidate(tmp_path: Path) -> None:
    coordinator = _coordinator(
        tmp_path,
        plan=_plan(problems=(_problem(audit="approved"),)),
    )
    coordinator.initialize()
    claim = coordinator.claim("worker-a")
    assert claim is not None

    with pytest.raises(ValueError, match="requires a candidate payload"):
        coordinator.complete(
            claim,
            outcome="candidate",
            stop_reason="candidate_found",
        )
    assert coordinator.problem_state("p1")["verification_status"] == "not_required"
    coordinator.fail(
        claim,
        stop_reason="invalid_executor_result",
        retryable=False,
    )
    assert coordinator.summary()["stop_reason_counts"] == {
        "invalid_executor_result": 1
    }
