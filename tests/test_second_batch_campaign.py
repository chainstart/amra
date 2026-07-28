from __future__ import annotations

import csv
import json
import time
from pathlib import Path

import pytest
import yaml

from amra.discovery.batch_campaign import (
    BatchCampaignCoordinator,
    BatchStateError,
)
from amra.discovery.campaign_status import CampaignStatusStore
from amra.discovery.first_batch_campaign import FIRST_BATCH_PROBLEM_IDS
from amra.discovery.second_batch_campaign import (
    SECOND_BATCH_DATABASE_FILE,
    SECOND_BATCH_MODEL_AUDIT_FILE,
    SECOND_BATCH_STATUS_CSV_FILE,
    SECOND_BATCH_STATUS_JSONL_FILE,
    SECOND_BATCH_STATUS_MARKDOWN_FILE,
    SecondBatchConfigurationError,
    SecondBatchExecutorFamily,
    SecondBatchRegistry,
    _memory_safe_addition_chain_length,
    _runner_compatibility_shims,
    build_second_batch_plan,
    initialize_second_batch,
    record_second_batch_verification,
    run_second_batch,
    second_batch_status,
    validate_second_batch_registry,
)
from amra.discovery import second_batch_arithmetic, second_batch_finite
from amra.cli import build_parser


FAKE_GRAPH_COUNT = 23
FAKE_ARITHMETIC_COUNT = 21
FAKE_ADDITIONAL_COUNT = 56


def _problem(problem_id: str, domain: str) -> dict:
    return {
        "problem_id": problem_id,
        "title": f"Problem {problem_id}",
        "source": "fixture",
        "statement": f"Every {problem_id} object has property Q.",
        "domain": domain,
        "tags": [],
        "open_problem": True,
        "formalized": "no",
        "metadata": {"source_id": problem_id.upper()},
    }


def _spec(
    problem_id: str,
    family: str,
    *,
    supports_deep: bool = False,
) -> dict:
    return {
        "problem_id": problem_id,
        "source_id": problem_id.upper(),
        "title": f"Problem {problem_id}",
        "domain": "graph_theory" if family == "graph" else "number_theory",
        "model_contract": {
            "objects": "finite fixture objects",
            "premise": "P(x)",
            "counterexample": "P(x) and not Q(x)",
        },
        "claim_scope": "full_claim",
        "scope_limitation": "The finite fixture preserves the full predicate.",
        "executor_id": f"fake.{family}",
        "executor_version": "v3",
        "strategies": (
            ["screen-exact", "deep-diversified"]
            if supports_deep
            else ["screen-exact"]
        ),
        "default_bounds": {"size": 5, "max_cases": 50},
        "screen_bounds": {"size": 5, "max_cases": 50},
        "supports_deep": supports_deep,
        "deep_bounds": {"size": 8, "max_cases": 500},
        "deep_launches": 2,
    }


def _registry(
    *,
    candidate_problem_id: str | None = None,
    malformed: bool = False,
) -> SecondBatchRegistry:
    graph_specs = tuple(
        _spec(
            f"p-g-{index:03d}",
            "graph",
            supports_deep=index == 1,
        )
        for index in range(FAKE_GRAPH_COUNT)
    )
    arithmetic_specs = tuple(
        _spec(f"p-a-{index:03d}", "arithmetic")
        for index in range(FAKE_ARITHMETIC_COUNT)
    )
    additional_specs = tuple(
        _spec(f"p-x-{index:03d}", "additional")
        for index in range(FAKE_ADDITIONAL_COUNT)
    )

    def runner(
        problem_id: str,
        *,
        strategy_id: str,
        budget: dict,
        seed: int,
        checkpoint: dict | None = None,
        progress=None,
    ) -> dict:
        if malformed:
            return {"outcome": "made-up-success"}
        start = int((checkpoint or {}).get("next_case", 0))
        if progress is not None:
            progress({"next_case": start + 5}, 5)
        candidate = (
            {"problem_id": problem_id, "witness": [seed % 17]}
            if problem_id == candidate_problem_id
            else None
        )
        family = (
            "graph"
            if problem_id.startswith("p-g")
            else "arithmetic"
            if problem_id.startswith("p-a")
            else "additional"
        )
        return {
            "executor_id": f"fake.{family}",
            "executor_version": "v3",
            "strategy_id": strategy_id,
            "outcome": "candidate" if candidate else "no_candidate",
            "candidate": candidate,
            "checked_cases": 5,
            "stop_reason": (
                "candidate_found" if candidate else "finite_bound_exhausted"
            ),
            "checkpoint": {"next_case": start + 5},
            "model_contract": {
                "objects": "finite fixture objects",
                "premise": "P(x)",
                "counterexample": "P(x) and not Q(x)",
                "claim_scope": "full_claim",
                "scope_limitation": (
                    "The finite fixture preserves the full predicate."
                ),
            },
            "tool_versions": {"fake": "1"},
            "metrics": {"fixture_metric": 7},
            "observed_budget": budget,
        }

    return SecondBatchRegistry(
        graph_specs=graph_specs,
        arithmetic_specs=arithmetic_specs,
        graph_runner=runner,
        arithmetic_runner=runner,
        extra_families=(
            SecondBatchExecutorFamily(
                family="additional",
                specs=additional_specs,
                runner=runner,
            ),
        ),
    )


def _write_bank(tmp_path: Path, registry: SecondBatchRegistry) -> Path:
    bank = tmp_path / "bank.yaml"
    rows = [
        _problem(
            spec["problem_id"],
            "graph_theory" if spec["problem_id"].startswith("p-g") else "number_theory",
        )
        for family in registry.families
        for spec in family.specs
    ]
    bank.write_text(
        yaml.safe_dump(rows, sort_keys=False),
        encoding="utf-8",
    )
    return bank


def _initialize_main_status(
    campaign: Path,
    bank: Path,
) -> CampaignStatusStore:
    rows = yaml.safe_load(bank.read_text(encoding="utf-8"))
    store = CampaignStatusStore(campaign / "status.sqlite3")
    for row in rows:
        statement_hash = __import__("hashlib").sha256(
            row["statement"].encode("utf-8")
        ).hexdigest()
        store.upsert_problem(
            row["problem_id"],
            title=row["title"],
            source=row["source"],
            domain=row["domain"],
            collection="backlog",
            stage="G0",
            statement_hash=statement_hash,
            metadata=row["metadata"],
            status="parked",
        )
    return store


def test_registry_requires_exact_100_across_extensible_families() -> None:
    registry = _registry()
    validated = validate_second_batch_registry(registry)
    assert validated["graph_count"] == FAKE_GRAPH_COUNT
    assert validated["arithmetic_count"] == FAKE_ARITHMETIC_COUNT
    assert validated["family_counts"] == {
        "graph": FAKE_GRAPH_COUNT,
        "arithmetic": FAKE_ARITHMETIC_COUNT,
        "additional": FAKE_ADDITIONAL_COUNT,
    }
    assert validated["total_count"] == 100
    assert registry.runner_for("fake.additional") is (
        registry.extra_families[0].runner
    )

    short = SecondBatchRegistry(
        graph_specs=registry.graph_specs,
        arithmetic_specs=registry.arithmetic_specs,
        graph_runner=registry.graph_runner,
        arithmetic_runner=registry.arithmetic_runner,
        extra_families=(
            SecondBatchExecutorFamily(
                family="additional",
                specs=registry.extra_families[0].specs[:-1],
                runner=registry.extra_families[0].runner,
            ),
        ),
    )
    with pytest.raises(SecondBatchConfigurationError, match="exactly 100"):
        validate_second_batch_registry(short)

    overlap_spec = dict(registry.graph_specs[0])
    overlap_spec["problem_id"] = FIRST_BATCH_PROBLEM_IDS[0]
    overlap = SecondBatchRegistry(
        graph_specs=(overlap_spec, *registry.graph_specs[1:]),
        arithmetic_specs=registry.arithmetic_specs,
        graph_runner=registry.graph_runner,
        arithmetic_runner=registry.arithmetic_runner,
        extra_families=registry.extra_families,
    )
    with pytest.raises(SecondBatchConfigurationError, match="overlaps"):
        validate_second_batch_registry(overlap)

    resolved_spec = dict(registry.graph_specs[0])
    resolved_spec["problem_id"] = "unsolvedmath-opg-824"
    resolved = SecondBatchRegistry(
        graph_specs=(resolved_spec, *registry.graph_specs[1:]),
        arithmetic_specs=registry.arithmetic_specs,
        graph_runner=registry.graph_runner,
        arithmetic_runner=registry.arithmetic_runner,
        extra_families=registry.extra_families,
    )
    with pytest.raises(
        SecondBatchConfigurationError,
        match="resolved or conservatively excluded",
    ):
        validate_second_batch_registry(resolved)


def test_cli_exposes_second_batch_init_run_and_status_commands() -> None:
    parser = build_parser()
    initialized = parser.parse_args(
        [
            "discovery",
            "batch2-init",
            "--bank",
            "bank.yaml",
            "--out",
            "campaign",
            "--screen-seconds",
            "120",
            "--deep-max-cases",
            "5000",
        ]
    )
    assert initialized.discovery_command == "batch2-init"
    assert initialized.screen_seconds == 120
    assert initialized.deep_max_cases == 5_000

    run = parser.parse_args(
        [
            "discovery",
            "batch2-run",
            "--out",
            "campaign",
            "--max-tasks",
            "4",
            "--executor",
            "fake.graph",
        ]
    )
    assert run.discovery_command == "batch2-run"
    assert run.max_tasks == 4
    assert run.executors == ["fake.graph"]

    status = parser.parse_args(
        ["discovery", "batch2-status", "--out", "campaign"]
    )
    assert status.discovery_command == "batch2-status"


def test_plan_contains_screen_and_only_declared_deep_multistarts(
    tmp_path: Path,
) -> None:
    registry = _registry()
    bank = _write_bank(tmp_path, registry)
    plan = build_second_batch_plan(
        bank_path=bank,
        registry=registry,
        screen_time_seconds=120,
        deep_time_seconds=900,
        screen_max_cases=75,
        deep_max_cases=750,
        memory_mb=512,
        deep_launches=4,
        global_seed=19,
    )

    assert len(plan.problems) == 100
    first = plan.problems[0]
    second = plan.problems[1]
    assert [strategy.stage_id for strategy in first.strategies] == ["screen"]
    assert [strategy.stage_id for strategy in second.strategies] == [
        "screen",
        "deep",
    ]
    assert second.strategies[1].launches == 2
    assert second.strategies[0].budget.max_cases == 75
    assert second.strategies[1].budget.max_cases == 750
    assert second.strategies[1].budget.time_seconds == 900
    assert len(second.strategies[0].config["runner_fingerprint"]) == 64
    assert (
        second.strategies[0].config["runner_fingerprint"]
        == second.strategies[1].config["runner_fingerprint"]
    )
    assert second.strategies[0].config["search_role"] == "bounded_screen"
    assert second.strategies[1].config["search_role"] == "bounded_deep_search"


def test_separate_task_database_and_parent_exports_do_not_pollute_main_count(
    tmp_path: Path,
) -> None:
    registry = _registry()
    bank = _write_bank(tmp_path, registry)
    campaign = tmp_path / "campaign"
    main = _initialize_main_status(campaign, bank)
    assert main.summary()["total_problems"] == 100

    initialized = initialize_second_batch(
        bank_path=bank,
        campaign_dir=campaign,
        registry=registry,
    )

    assert initialized["initialization"]["problem_count"] == 100
    assert initialized["initialization"]["task_count"] == 102
    assert (campaign / SECOND_BATCH_DATABASE_FILE).exists()
    task_store = CampaignStatusStore(campaign / SECOND_BATCH_DATABASE_FILE)
    assert task_store.summary()["total_problems"] == 102
    assert main.summary()["total_problems"] == 100
    assert (campaign / SECOND_BATCH_STATUS_CSV_FILE).exists()
    assert (campaign / SECOND_BATCH_STATUS_JSONL_FILE).exists()
    assert (campaign / SECOND_BATCH_STATUS_MARKDOWN_FILE).exists()
    audit_path = campaign / SECOND_BATCH_MODEL_AUDIT_FILE
    assert audit_path.exists()
    audit_rows = audit_path.read_text(encoding="utf-8").splitlines()
    assert len(audit_rows) == 100
    first_audit = json.loads(audit_rows[0])
    assert first_audit["claim_scope"] == "full_claim"
    assert first_audit["scope_limitation"]
    assert initialized["model_audits"]["auditor_id"] == (
        "second-batch-spec-contract-auditor-v1"
    )
    with (campaign / SECOND_BATCH_STATUS_CSV_FILE).open(
        encoding="utf-8", newline=""
    ) as handle:
        status_rows = list(csv.DictReader(handle))
        assert len(status_rows) == 100
        assert status_rows[0]["claim_scope"] == "full_claim"
        assert status_rows[0]["scope_limitation"]


def test_worker_runs_real_injected_executor_checkpoints_and_syncs_one_parent(
    tmp_path: Path,
) -> None:
    registry = _registry()
    bank = _write_bank(tmp_path, registry)
    campaign = tmp_path / "campaign"
    main = _initialize_main_status(campaign, bank)
    initialize_second_batch(
        bank_path=bank,
        campaign_dir=campaign,
        registry=registry,
    )

    result = run_second_batch(
        campaign_dir=campaign,
        registry=registry,
        worker_id="worker-a",
        lease_seconds=1,
        max_tasks=1,
    )

    assert result["processed_this_run"] == 1
    assert result["failed_this_run"] == []
    completed = result["completed_this_run"][0]
    assert completed["problem_id"] == "p-g-000"
    assert completed["outcome"] == "no_candidate"
    assert Path(completed["attempt_artifact"]).exists()
    task = CampaignStatusStore(
        campaign / SECOND_BATCH_DATABASE_FILE
    ).get_problem(completed["task_id"])
    assert task["last_result"]["metrics"]["executor_metrics"] == {
        "fixture_metric": 7
    }
    assert main.summary()["total_problems"] == 100
    parent = main.get_problem("p-g-000")
    assert parent["status"] == "completed"
    assert parent["last_result"]["outcome"] == "bounded_search_completed"
    assert parent["metadata"]["batch_2"]["final"] is True
    status_rows = [
        json.loads(line)
        for line in (
            campaign / SECOND_BATCH_STATUS_JSONL_FILE
        ).read_text(encoding="utf-8").splitlines()
    ]
    progress_row = next(
        row for row in status_rows if row["problem_id"] == "p-g-000"
    )
    assert progress_row["completed_task_count"] == 1
    assert progress_row["attempt_count"] == 1
    assert progress_row["checked_cases"] == 5
    assert progress_row["search_roles"] == ["bounded_screen"]
    assert progress_row["updated_at"]
    assert progress_row["task_progress"][0]["cursor"]["next_case"] == 5
    assert progress_row["task_progress"][0]["search_role"] == "bounded_screen"
    assert progress_row["task_progress"][0]["budget"]["time_seconds"] == 900
    assert progress_row["task_progress"][0]["checkpoint_id"] > 0
    assert progress_row["task_progress"][0]["checkpoint_sequence"] > 0
    assert progress_row["task_progress"][0]["checkpoint_created_at"]
    assert progress_row["task_progress"][0]["updated_at"]
    markdown = (
        campaign / SECOND_BATCH_STATUS_MARKDOWN_FILE
    ).read_text(encoding="utf-8")
    assert "| Verification | Progress | Checked | Attempts |" in markdown


def test_status_keeps_cumulative_checked_cases_across_interrupted_resume(
    tmp_path: Path,
) -> None:
    base_registry = _registry()
    calls = 0

    def resumable_runner(
        problem_id: str,
        *,
        strategy_id: str,
        budget: dict,
        seed: int,
        checkpoint: dict | None = None,
        progress=None,
    ) -> dict:
        nonlocal calls
        calls += 1
        start = int((checkpoint or {}).get("next_case", 0))
        if calls == 1:
            assert start == 0
            progress({"next_case": 7}, 7)
            raise KeyboardInterrupt
        assert start == 7
        progress({"next_case": 14}, 7)
        return {
            "executor_id": "fake.graph",
            "executor_version": "v3",
            "strategy_id": strategy_id,
            "outcome": "no_candidate",
            "candidate": None,
            "checked_cases": 7,
            "stop_reason": "finite_bound_exhausted",
            "checkpoint": {"next_case": 14},
            "model_contract": {
                "objects": "finite fixture objects",
                "premise": "P(x)",
                "counterexample": "P(x) and not Q(x)",
                "claim_scope": "full_claim",
                "scope_limitation": (
                    "The finite fixture preserves the full predicate."
                ),
            },
            "metrics": {"fixture_metric": 14},
        }

    registry = SecondBatchRegistry(
        graph_specs=base_registry.graph_specs,
        arithmetic_specs=base_registry.arithmetic_specs,
        graph_runner=resumable_runner,
        arithmetic_runner=base_registry.arithmetic_runner,
        extra_families=base_registry.extra_families,
    )
    bank = _write_bank(tmp_path, registry)
    campaign = tmp_path / "campaign"
    _initialize_main_status(campaign, bank)
    initialize_second_batch(
        bank_path=bank,
        campaign_dir=campaign,
        registry=registry,
    )

    interrupted = run_second_batch(
        campaign_dir=campaign,
        registry=registry,
        worker_id="resume-worker-1",
        max_tasks=1,
    )
    assert interrupted["processed_this_run"] == 0
    assert len(interrupted["interrupted_this_run"]) == 1

    resumed = run_second_batch(
        campaign_dir=campaign,
        registry=registry,
        worker_id="resume-worker-2",
        max_tasks=1,
    )
    assert resumed["processed_this_run"] == 1
    status_row = next(
        json.loads(line)
        for line in (
            campaign / SECOND_BATCH_STATUS_JSONL_FILE
        ).read_text(encoding="utf-8").splitlines()
        if '"problem_id": "p-g-000"' in line
    )
    assert status_row["attempt_count"] == 2
    assert status_row["checked_cases"] == 14
    progress_row = status_row["task_progress"][0]
    assert progress_row["checked_cases"] == 14
    assert progress_row["latest_attempt_checked_cases"] == 7
    assert progress_row["cursor"]["next_case"] == 14
    assert progress_row["checkpoint_id"] > 0
    assert progress_row["checkpoint_sequence"] > 0
    assert progress_row["checkpoint_created_at"]


def test_status_reconciles_deep_stage_after_post_complete_crash(
    tmp_path: Path,
) -> None:
    registry = _registry()
    bank = _write_bank(tmp_path, registry)
    campaign = tmp_path / "campaign"
    _initialize_main_status(campaign, bank)
    initialize_second_batch(
        bank_path=bank,
        campaign_dir=campaign,
        registry=registry,
    )
    plan = build_second_batch_plan(bank_path=bank, registry=registry)
    coordinator = BatchCampaignCoordinator(
        campaign / SECOND_BATCH_DATABASE_FILE,
        plan,
        available_executors=registry.executor_ids,
    )

    first = coordinator.claim("crash-window-worker")
    assert first is not None
    assert first.parent_problem_id == "p-g-000"
    coordinator.complete(
        first,
        outcome="no_candidate",
        stop_reason="finite_bound_exhausted",
    )
    screen = coordinator.claim("crash-window-worker")
    assert screen is not None
    assert screen.parent_problem_id == "p-g-001"
    assert screen.stage_id == "screen"
    coordinator.complete(
        screen,
        outcome="no_candidate",
        stop_reason="finite_bound_exhausted",
    )
    deep_before = next(
        task
        for task in coordinator.tasks()
        if task["metadata"]["parent_problem_id"] == "p-g-001"
        and task["metadata"]["stage_id"] == "deep"
    )
    assert deep_before["status"] == "parked"

    second_batch_status(campaign_dir=campaign, registry=registry)

    deep_after = CampaignStatusStore(
        campaign / SECOND_BATCH_DATABASE_FILE
    ).get_problem(deep_before["problem_id"])
    assert deep_after["status"] == "queued"


def test_candidate_stays_nonfinal_until_independent_verification(
    tmp_path: Path,
) -> None:
    registry = _registry(candidate_problem_id="p-g-000")
    bank = _write_bank(tmp_path, registry)
    campaign = tmp_path / "campaign"
    main = _initialize_main_status(campaign, bank)
    initialize_second_batch(
        bank_path=bank,
        campaign_dir=campaign,
        registry=registry,
    )
    run = run_second_batch(
        campaign_dir=campaign,
        registry=registry,
        worker_id="search-worker",
        max_tasks=1,
    )
    assert run["completed_this_run"][0]["outcome"] == "candidate"
    assert main.get_problem("p-g-000")["status"] == "parked"

    with pytest.raises(BatchStateError, match="cannot independently verify"):
        record_second_batch_verification(
            campaign_dir=campaign,
            problem_id="p-g-000",
            verifier_id="search-worker",
            verdict="verified",
            evidence={"replayed": True},
            registry=registry,
        )

    inconclusive = record_second_batch_verification(
        campaign_dir=campaign,
        problem_id="p-g-000",
        verifier_id="preliminary-verifier",
        verdict="inconclusive",
        evidence={"replayed": False, "reason": "second engine timed out"},
        registry=registry,
    )
    assert inconclusive["problem_state"]["verification_status"] == "inconclusive"
    assert main.get_problem("p-g-000")["status"] == "parked"
    status_row = next(
        json.loads(line)
        for line in (
            campaign / SECOND_BATCH_STATUS_JSONL_FILE
        ).read_text(encoding="utf-8").splitlines()
        if '"problem_id": "p-g-000"' in line
    )
    assert status_row["aggregate_status"] == (
        "candidate_verification_inconclusive"
    )
    assert status_row["final"] is False

    verified = record_second_batch_verification(
        campaign_dir=campaign,
        problem_id="p-g-000",
        verifier_id="verification-worker",
        verdict="verified",
        evidence={"independent_implementation": "fake-v2", "replayed": True},
        registry=registry,
    )
    assert verified["problem_state"]["verification_status"] == "verified"
    assert main.summary()["total_problems"] == 100
    parent = main.get_problem("p-g-000")
    assert parent["status"] == "completed"
    assert parent["last_result"]["outcome"] == "candidate_verified"

    contested = record_second_batch_verification(
        campaign_dir=campaign,
        problem_id="p-g-000",
        verifier_id="review-worker",
        verdict="rejected",
        evidence={"independent_implementation": "fake-v3", "replayed": False},
        registry=registry,
    )
    assert contested["problem_state"]["verification_status"] == "contested"
    reopened = main.get_problem("p-g-000")
    assert reopened["status"] == "parked"
    assert reopened["last_result"] is None
    assert reopened["metadata"]["batch_2"]["aggregate_status"] == (
        "candidate_contested"
    )


def test_malformed_executor_result_is_failed_not_fabricated(
    tmp_path: Path,
) -> None:
    registry = _registry(malformed=True)
    bank = _write_bank(tmp_path, registry)
    campaign = tmp_path / "campaign"
    _initialize_main_status(campaign, bank)
    initialize_second_batch(
        bank_path=bank,
        campaign_dir=campaign,
        registry=registry,
    )

    result = run_second_batch(
        campaign_dir=campaign,
        registry=registry,
        max_tasks=1,
        max_attempts=1,
    )

    assert result["completed_this_run"] == []
    assert len(result["failed_this_run"]) == 1
    assert "unsupported outcome" in result["failed_this_run"][0]["stop_reason"]
    assert Path(result["failed_this_run"][0]["failure_artifact"]).exists()


def test_string_executor_contract_is_normalized_against_frozen_plan(
    tmp_path: Path,
) -> None:
    base = _registry()
    condition = "P(x) and not Q(x)"
    graph_spec = dict(base.graph_specs[0])
    graph_spec["model_contract"] = condition

    def string_contract_runner(
        problem_id: str,
        *,
        strategy_id: str,
        budget: dict,
        seed: int,
        checkpoint: dict | None = None,
        progress=None,
    ) -> dict:
        result = base.graph_runner(
            problem_id,
            strategy_id=strategy_id,
            budget=budget,
            seed=seed,
            checkpoint=checkpoint,
            progress=progress,
        )
        if problem_id == graph_spec["problem_id"]:
            result["model_contract"] = condition
        return result

    registry = SecondBatchRegistry(
        graph_specs=(graph_spec, *base.graph_specs[1:]),
        arithmetic_specs=base.arithmetic_specs,
        graph_runner=string_contract_runner,
        arithmetic_runner=base.arithmetic_runner,
        extra_families=base.extra_families,
    )
    bank = _write_bank(tmp_path, registry)
    campaign = tmp_path / "campaign"
    _initialize_main_status(campaign, bank)
    initialize_second_batch(
        bank_path=bank,
        campaign_dir=campaign,
        registry=registry,
    )

    result = run_second_batch(
        campaign_dir=campaign,
        registry=registry,
        max_tasks=1,
        max_attempts=1,
    )

    assert len(result["completed_this_run"]) == 1
    assert result["failed_this_run"] == []


def test_kou_21_2_gap_protocol_shim_is_scoped_and_restored(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, int]] = []

    def fake_run_gap(script: str, *, timeout: int = 120) -> str:
        calls.append((script, timeout))
        return "DONE|0\n"

    monkeypatch.setattr(second_batch_arithmetic, "_run_gap", fake_run_gap)
    claim = type(
        "Claim",
        (),
        {
            "parent_problem_id": "unsolvedmath-kou-21.2",
            "executor_id": "second_batch.arithmetic.kou_21_2.v1",
        },
    )()

    with _runner_compatibility_shims(
        claim,
        second_batch_arithmetic.run_second_batch_arithmetic_search,
    ) as shims:
        assert shims == ["kou-21.2-gap-screen-width-v1"]
        second_batch_arithmetic._run_gap("Print(1);", timeout=17)

    assert calls == [
        ("SizeScreen([1000000,1000000]);;\nPrint(1);", 17)
    ]
    assert second_batch_arithmetic._run_gap is fake_run_gap


def test_memory_safe_addition_chain_matches_small_reference_bfs() -> None:
    def reference_length(target: int) -> int:
        if target <= 1:
            return 0
        frontier = {(1,)}
        for depth in range(1, target):
            next_frontier: set[tuple[int, ...]] = set()
            for chain in frontier:
                additions = {
                    chain[left] + chain[right]
                    for left in range(len(chain))
                    for right in range(left, len(chain))
                    if chain[-1] < chain[left] + chain[right] <= target
                }
                if target in additions:
                    return depth
                next_frontier.update((*chain, value) for value in additions)
            frontier = next_frontier
        raise RuntimeError(f"reference search failed for {target}")

    for target in range(1, 65):
        assert _memory_safe_addition_chain_length(
            target,
            None,
            check_deadline=lambda _deadline: None,
        ) == reference_length(target)


def test_nt_039_addition_chain_shim_is_exact_scoped_and_restored() -> None:
    original = second_batch_finite._addition_chain_length
    claim = type(
        "Claim",
        (),
        {
            "parent_problem_id": "unsolvedmath-nt-039",
            "executor_id": "second_batch.finite.exact_search.v1",
        },
    )()

    with _runner_compatibility_shims(
        claim,
        second_batch_finite.run_second_batch_finite_search,
    ) as shims:
        patched = second_batch_finite._addition_chain_length
        assert shims == ["nt-039-addition-chain-iddfs-v1"]
        assert patched is not original
        assert patched(127) == 10
        assert patched(255) == 10
        assert patched(511) == 12
        assert patched(1_023) == 13
        with pytest.raises(second_batch_finite._DeadlineExceeded):
            patched(2_047, time.monotonic() - 1)

    assert second_batch_finite._addition_chain_length is original


def test_nt_039_shim_advances_the_previously_ooming_atomic_case() -> None:
    claim = type(
        "Claim",
        (),
        {
            "parent_problem_id": "unsolvedmath-nt-039",
            "executor_id": "second_batch.finite.exact_search.v1",
        },
    )()
    checkpoint = {
        "next_case": 7,
        "strategy_id": "screen-exact",
        "seed": 5,
    }

    with _runner_compatibility_shims(
        claim,
        second_batch_finite.run_second_batch_finite_search,
    ):
        result = second_batch_finite.run_second_batch_finite_search(
            "unsolvedmath-nt-039",
            strategy_id="screen-exact",
            budget={"max_cases": 1, "time_seconds": 5},
            seed=5,
            checkpoint=checkpoint,
        )

    assert result["checked_cases"] == 1
    assert result["checkpoint"]["next_case"] == 8
    assert result["stop_reason"] == "case_budget_exhausted"


def test_runner_identity_mismatch_is_failed_against_frozen_claim(
    tmp_path: Path,
) -> None:
    registry = _registry()

    def wrong_runner(
        problem_id: str,
        *,
        strategy_id: str,
        budget: dict,
        seed: int,
        checkpoint: dict | None = None,
        progress=None,
    ) -> dict:
        return {
            "executor_id": "wrong.executor",
            "executor_version": "v999",
            "strategy_id": "wrong-strategy",
            "outcome": "no_candidate",
            "candidate": None,
            "checked_cases": 1,
            "stop_reason": "fabricated",
            "checkpoint": {"next_case": 1},
            "model_contract": {
                "objects": "wrong",
                "premise": "wrong",
                "counterexample": "wrong",
            },
        }

    wrong = SecondBatchRegistry(
        graph_specs=registry.graph_specs,
        arithmetic_specs=registry.arithmetic_specs,
        graph_runner=wrong_runner,
        arithmetic_runner=registry.arithmetic_runner,
        extra_families=registry.extra_families,
    )
    bank = _write_bank(tmp_path, wrong)
    campaign = tmp_path / "campaign"
    _initialize_main_status(campaign, bank)
    initialize_second_batch(
        bank_path=bank,
        campaign_dir=campaign,
        registry=wrong,
    )

    result = run_second_batch(
        campaign_dir=campaign,
        registry=wrong,
        max_tasks=1,
        max_attempts=1,
    )

    assert result["completed_this_run"] == []
    assert "executor result identity mismatch" in (
        result["failed_this_run"][0]["stop_reason"]
    )


def test_registry_and_plan_file_drift_are_rejected(
    tmp_path: Path,
) -> None:
    registry = _registry()
    bank = _write_bank(tmp_path, registry)
    campaign = tmp_path / "campaign"
    _initialize_main_status(campaign, bank)
    initialize_second_batch(
        bank_path=bank,
        campaign_dir=campaign,
        registry=registry,
    )

    changed_spec = dict(registry.graph_specs[0])
    changed_spec["version"] = "v999"
    changed = SecondBatchRegistry(
        graph_specs=(changed_spec, *registry.graph_specs[1:]),
        arithmetic_specs=registry.arithmetic_specs,
        graph_runner=registry.graph_runner,
        arithmetic_runner=registry.arithmetic_runner,
        extra_families=registry.extra_families,
    )
    with pytest.raises(
        SecondBatchConfigurationError,
        match="incompatible with the current executor registry",
    ):
        run_second_batch(campaign_dir=campaign, registry=changed, max_tasks=1)

    plan_path = campaign / "batch-2-plan.json"
    payload = json.loads(plan_path.read_text(encoding="utf-8"))
    payload["problems"][0]["strategies"][0]["budget"]["time_seconds"] += 1
    plan_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(Exception, match="different plan"):
        second_batch_status(campaign_dir=campaign, registry=registry)


def test_status_reopens_stored_plan_without_rebuilding_budgets(
    tmp_path: Path,
) -> None:
    registry = _registry()
    bank = _write_bank(tmp_path, registry)
    campaign = tmp_path / "campaign"
    _initialize_main_status(campaign, bank)
    initialize_second_batch(
        bank_path=bank,
        campaign_dir=campaign,
        registry=registry,
        screen_time_seconds=123,
    )

    status = second_batch_status(
        campaign_dir=campaign,
        registry=registry,
    )

    assert status["summary"]["problem_count"] == 100
    assert len(status["parent_rows"]) == 100
    assert status["main_sync"]["total_before"] == 100
    assert status["main_sync"]["total_after"] == 100
