from __future__ import annotations

import csv
import fcntl
import hashlib
import inspect
import json
import os
import tempfile
import threading
import time
import traceback
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

from amra.discovery.batch_campaign import (
    BatchCampaignCoordinator,
    BatchClaim,
    BatchPlan,
    BatchProblemPlan,
    BatchStateError,
    StrategyBudget,
    StrategyPlan,
)
from amra.discovery.campaign_status import (
    CampaignStatusError,
    CampaignStatusStore,
    LeaseLostError,
    ProblemNotFoundError,
)
from amra.discovery.first_batch_campaign import FIRST_BATCH_PROBLEM_IDS
from amra.problem_banks.registry import load_problem_bank


SECOND_BATCH_SCHEMA_VERSION = "amra.second_batch_campaign.v1"
SECOND_BATCH_ID = "counterexample-batch-2"
SECOND_BATCH_COLLECTION = "counterexample-batch-2-100"
SECOND_BATCH_EXPECTED_TOTAL = 100
SECOND_BATCH_CLAIM_SCOPES = frozenset(
    {"full_claim", "explicit_subclaim", "restricted_family", "witness_search"}
)
SECOND_BATCH_FORBIDDEN_CONCEPT_DUPLICATES = {
    "unsolvedmath-opg-432": "duplicates first-batch Collatz problem NT-002",
    (
        "unsolvedmath-comb-003-collision-the-union-closed-sets-conjecture-3866e1eb"
    ): "duplicates first-batch union-closed problem OPG-2108",
}
SECOND_BATCH_FORBIDDEN_RESOLVED = {
    "unsolvedmath-nt-008": "Fibonacci perfect powers were determined in 2006",
    "unsolvedmath-opg-130": (
        "Jaeger's modular orientation conjecture was disproved in 2018"
    ),
    "unsolvedmath-opg-655": "Snevily's conjecture was proved in 2011",
    "unsolvedmath-opg-732": "the Frobenius conjecture was proved in 1991",
    "unsolvedmath-opg-2242": "the Goldberg-Seymour conjecture has been proved",
    "unsolvedmath-opg-2226": (
        "Seymour's r-graph conjecture follows from the Goldberg-Seymour theorem"
    ),
    "unsolvedmath-opg-824": "the strongly regular graph core conjecture was proved",
    "unsolvedmath-opg-2359": (
        "a complete proof preprint appeared in July 2026; excluded conservatively"
    ),
    "unsolvedmath-opg-16555": "nonexistence of Diophantine quintuples was proved",
    "unsolvedmath-opg-37402": "the Lucas residue classification was completed",
    "unsolvedmath-opg-46432": "Adam's conjecture was disproved",
}

SECOND_BATCH_DATABASE_FILE = "batch-2-status.sqlite3"
SECOND_BATCH_PLAN_FILE = "batch-2-plan.json"
SECOND_BATCH_MODEL_AUDIT_FILE = "batch-2-model-audit.jsonl"
SECOND_BATCH_STATUS_CSV_FILE = "BATCH2_STATUS.csv"
SECOND_BATCH_STATUS_JSONL_FILE = "BATCH2_STATUS.jsonl"
SECOND_BATCH_STATUS_MARKDOWN_FILE = "BATCH2_STATUS.md"
SECOND_BATCH_SUMMARY_FILE = "batch-2-summary.json"
SECOND_BATCH_EXPORT_LOCK_FILE = ".batch-2-export.lock"
SECOND_BATCH_MAIN_SYNC_LOCK_FILE = ".batch-2-main-sync.lock"
MAIN_STATUS_DATABASE_FILE = "status.sqlite3"

DEFAULT_SCREEN_TIME_SECONDS = 900
DEFAULT_DEEP_TIME_SECONDS = 7_200
DEFAULT_MEMORY_MB = 1_024
DEFAULT_DEEP_LAUNCHES = 3
DEFAULT_GLOBAL_SEED = 20_260_727

Runner = Callable[..., Mapping[str, Any]]


class SecondBatchConfigurationError(RuntimeError):
    pass


class SecondBatchExecutionError(RuntimeError):
    pass


@dataclass(frozen=True)
class SecondBatchExecutorFamily:
    family: str
    specs: Sequence[Mapping[str, Any]]
    runner: Runner

    def __post_init__(self) -> None:
        family = str(self.family).strip()
        if not family:
            raise ValueError("executor family name must not be empty")
        if not callable(self.runner):
            raise TypeError(f"{family}_runner must be callable")
        object.__setattr__(self, "family", family)
        object.__setattr__(
            self, "specs", tuple(dict(spec) for spec in self.specs)
        )


@dataclass(frozen=True)
class SecondBatchRegistry:
    graph_specs: Sequence[Mapping[str, Any]]
    arithmetic_specs: Sequence[Mapping[str, Any]]
    graph_runner: Runner
    arithmetic_runner: Runner
    extra_families: Sequence[SecondBatchExecutorFamily] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "graph_specs", tuple(dict(spec) for spec in self.graph_specs)
        )
        object.__setattr__(
            self,
            "arithmetic_specs",
            tuple(dict(spec) for spec in self.arithmetic_specs),
        )
        if not callable(self.graph_runner):
            raise TypeError("graph_runner must be callable")
        if not callable(self.arithmetic_runner):
            raise TypeError("arithmetic_runner must be callable")
        normalized_extras = tuple(
            family
            if isinstance(family, SecondBatchExecutorFamily)
            else SecondBatchExecutorFamily(**dict(family))
            for family in self.extra_families
        )
        reserved = {"graph", "arithmetic"}
        extra_names = [family.family for family in normalized_extras]
        duplicate_names = sorted(
            family
            for family in set(extra_names)
            if extra_names.count(family) > 1
        )
        collisions = sorted(set(extra_names) & reserved)
        if collisions or duplicate_names:
            names = collisions + duplicate_names
            raise ValueError(
                "executor family names must be unique: " + ", ".join(names)
            )
        object.__setattr__(self, "extra_families", normalized_extras)

    @property
    def families(
        self,
    ) -> tuple[SecondBatchExecutorFamily, ...]:
        return (
            SecondBatchExecutorFamily(
                family="graph",
                specs=self.graph_specs,
                runner=self.graph_runner,
            ),
            SecondBatchExecutorFamily(
                family="arithmetic",
                specs=self.arithmetic_specs,
                runner=self.arithmetic_runner,
            ),
            *self.extra_families,
        )

    @property
    def executor_ids(self) -> frozenset[str]:
        return frozenset(
            _executor_id(spec, family=family.family)
            for family in self.families
            for spec in family.specs
        )

    def runner_for(self, executor_id: str) -> Runner:
        for family in self.families:
            if any(
                _executor_id(spec, family=family.family) == executor_id
                for spec in family.specs
            ):
                return family.runner
        raise SecondBatchConfigurationError(
            f"no runner registered for executor {executor_id!r}"
        )


def load_default_second_batch_registry() -> SecondBatchRegistry:
    """Load real second-batch executors without making them import prerequisites."""

    try:
        from amra.discovery.second_batch_arithmetic import (
            SECOND_BATCH_ARITHMETIC_SPECS,
            run_second_batch_arithmetic_search,
        )
        from amra.discovery.second_batch_graphs import (
            SECOND_BATCH_GRAPH_SPECS,
            run_second_batch_graph_search,
        )
        from amra.discovery.second_batch_finite import (
            SECOND_BATCH_FINITE_SPECS,
            run_second_batch_finite_search,
        )
    except ImportError as exc:
        raise SecondBatchConfigurationError(
            "second-batch executor modules are not installed; initialization is blocked"
        ) from exc
    return SecondBatchRegistry(
        graph_specs=SECOND_BATCH_GRAPH_SPECS,
        arithmetic_specs=SECOND_BATCH_ARITHMETIC_SPECS,
        graph_runner=run_second_batch_graph_search,
        arithmetic_runner=run_second_batch_arithmetic_search,
        extra_families=(
            SecondBatchExecutorFamily(
                family="finite",
                specs=SECOND_BATCH_FINITE_SPECS,
                runner=run_second_batch_finite_search,
            ),
        ),
    )


def _atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _write_json(path: Path, payload: Any) -> None:
    _atomic_write_text(
        path,
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _canonical_fingerprint(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return _sha256(encoded)


def _runner_fingerprint(runner: Runner) -> str:
    module = inspect.getmodule(runner)
    source_path = inspect.getsourcefile(runner)
    source_sha256 = ""
    if source_path is not None:
        path = Path(source_path)
        if path.is_file():
            source_sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
    if not source_sha256:
        try:
            source_sha256 = _sha256(inspect.getsource(runner))
        except (OSError, TypeError):
            source_sha256 = _sha256(repr(runner))
    return _canonical_fingerprint(
        {
            "module": "" if module is None else module.__name__,
            "qualname": getattr(runner, "__qualname__", repr(runner)),
            "source_sha256": source_sha256,
        }
    )


def _spec_problem_id(spec: Mapping[str, Any]) -> str:
    problem_id = str(spec.get("problem_id") or "").strip()
    if not problem_id:
        raise SecondBatchConfigurationError("executor spec is missing problem_id")
    return problem_id


def _executor_id(spec: Mapping[str, Any], *, family: str) -> str:
    return str(
        spec.get("executor_id")
        or f"second_batch.{family}.exact_search"
    ).strip()


def _executor_version(spec: Mapping[str, Any]) -> str:
    return str(
        spec.get("version")
        or spec.get("executor_version")
        or "v1"
    ).strip()


def _normalize_model_contract(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        contract = dict(value)
    elif str(value).strip():
        contract = {"counterexample_condition": str(value).strip()}
    else:
        raise SecondBatchConfigurationError(
            "every second-batch spec must define a model_contract"
        )
    if not contract:
        raise SecondBatchConfigurationError("model_contract must not be empty")
    return contract


def _normalize_bounds(value: Any, *, label: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise SecondBatchConfigurationError(f"{label} must be a mapping")
    return dict(value)


def _positive_optional(value: int | None, *, label: str) -> int | None:
    if value is None:
        return None
    normalized = int(value)
    if normalized <= 0:
        raise ValueError(f"{label} must be positive")
    return normalized


def _spec_max_cases(value: Any, *, label: str) -> int | None:
    if value is None:
        return None
    normalized = int(value)
    if normalized < 0:
        raise ValueError(f"{label} must be non-negative")
    return normalized or None


def _supports_deep(spec: Mapping[str, Any]) -> bool:
    if "supports_deep" in spec:
        return bool(spec["supports_deep"])
    strategies = {
        str(value).strip().lower().replace("_", "-")
        for value in spec.get("strategies", ())
    }
    return bool({"deep", "deep-diversified"} & strategies)


def validate_second_batch_registry(registry: SecondBatchRegistry) -> dict[str, Any]:
    family_ids = {
        family.family: [
            _spec_problem_id(spec) for spec in family.specs
        ]
        for family in registry.families
    }
    all_ids = [
        problem_id
        for family in registry.families
        for problem_id in family_ids[family.family]
    ]
    duplicates = sorted(
        problem_id
        for problem_id in set(all_ids)
        if all_ids.count(problem_id) > 1
    )
    if duplicates:
        raise SecondBatchConfigurationError(
            "second-batch executor registries overlap: " + ", ".join(duplicates)
        )
    first_batch_overlap = sorted(set(all_ids) & set(FIRST_BATCH_PROBLEM_IDS))
    if first_batch_overlap:
        raise SecondBatchConfigurationError(
            "second batch overlaps the first batch: "
            + ", ".join(first_batch_overlap)
        )
    conceptual_overlap = sorted(
        set(all_ids) & set(SECOND_BATCH_FORBIDDEN_CONCEPT_DUPLICATES)
    )
    if conceptual_overlap:
        details = [
            f"{problem_id} ({SECOND_BATCH_FORBIDDEN_CONCEPT_DUPLICATES[problem_id]})"
            for problem_id in conceptual_overlap
        ]
        raise SecondBatchConfigurationError(
            "second batch conceptually duplicates the first batch: "
            + ", ".join(details)
        )
    resolved_overlap = sorted(
        set(all_ids) & set(SECOND_BATCH_FORBIDDEN_RESOLVED)
    )
    if resolved_overlap:
        details = [
            f"{problem_id} ({SECOND_BATCH_FORBIDDEN_RESOLVED[problem_id]})"
            for problem_id in resolved_overlap
        ]
        raise SecondBatchConfigurationError(
            "second batch contains resolved or conservatively excluded problems: "
            + ", ".join(details)
        )
    if len(all_ids) != SECOND_BATCH_EXPECTED_TOTAL:
        raise SecondBatchConfigurationError(
            f"second batch must contain exactly "
            f"{SECOND_BATCH_EXPECTED_TOTAL} unique problems, got {len(all_ids)}"
        )
    executor_families: dict[str, tuple[str, Runner]] = {}
    for family in registry.families:
        for spec in family.specs:
            executor_id = _executor_id(spec, family=family.family)
            if not executor_id:
                raise SecondBatchConfigurationError(
                    f"{_spec_problem_id(spec)} has an empty executor_id"
                )
            prior = executor_families.get(executor_id)
            if (
                prior is not None
                and prior[0] != family.family
                and prior[1] is not family.runner
            ):
                raise SecondBatchConfigurationError(
                    f"executor {executor_id!r} is assigned to multiple runners"
                )
            executor_families[executor_id] = (family.family, family.runner)
    family_counts = {
        family: len(problem_ids)
        for family, problem_ids in family_ids.items()
    }
    return {
        "graph_count": family_counts["graph"],
        "arithmetic_count": family_counts["arithmetic"],
        "family_counts": family_counts,
        "total_count": len(all_ids),
        "problem_ids": all_ids,
    }


def _validate_plan_registry_compatibility(
    plan: BatchPlan,
    registry: SecondBatchRegistry,
) -> None:
    current_specs = {
        _spec_problem_id(spec): (family.family, family.runner, spec)
        for family in registry.families
        for spec in family.specs
    }
    runner_fingerprints = {
        id(family.runner): _runner_fingerprint(family.runner)
        for family in registry.families
    }
    mismatches: list[str] = []
    for problem in plan.problems:
        current = current_specs.get(problem.problem_id)
        if current is None:
            mismatches.append(f"{problem.problem_id}:missing_spec")
            continue
        family, runner, spec = current
        expected_executor = _executor_id(spec, family=family)
        expected_version = _executor_version(spec)
        expected_spec_fingerprint = _canonical_fingerprint(dict(spec))
        expected_runner_fingerprint = runner_fingerprints[id(runner)]
        contract = _normalize_model_contract(spec.get("model_contract"))
        contract["claim_scope"] = str(
            spec.get("claim_scope") or contract.get("claim_scope") or ""
        ).strip()
        contract["scope_limitation"] = str(
            spec.get("scope_limitation")
            or contract.get("scope_limitation")
            or ""
        ).strip()
        if contract != dict(problem.model_contract):
            mismatches.append(f"{problem.problem_id}:model_contract")
        for strategy in problem.strategies:
            if strategy.executor_id != expected_executor:
                mismatches.append(
                    f"{problem.problem_id}:{strategy.stage_id}:executor_id"
                )
            if strategy.executor_version != expected_version:
                mismatches.append(
                    f"{problem.problem_id}:{strategy.stage_id}:executor_version"
                )
            if strategy.config.get("family") != family:
                mismatches.append(
                    f"{problem.problem_id}:{strategy.stage_id}:family"
                )
            if (
                strategy.config.get("spec_fingerprint")
                != expected_spec_fingerprint
            ):
                mismatches.append(
                    f"{problem.problem_id}:{strategy.stage_id}:spec_fingerprint"
                )
            if (
                strategy.config.get("runner_fingerprint")
                != expected_runner_fingerprint
            ):
                mismatches.append(
                    f"{problem.problem_id}:{strategy.stage_id}:runner_fingerprint"
                )
    if mismatches:
        raise SecondBatchConfigurationError(
            "stored plan is incompatible with the current executor registry: "
            + ", ".join(sorted(set(mismatches)))
        )


def build_second_batch_plan(
    *,
    bank_path: Path,
    registry: SecondBatchRegistry,
    screen_time_seconds: int = DEFAULT_SCREEN_TIME_SECONDS,
    deep_time_seconds: int = DEFAULT_DEEP_TIME_SECONDS,
    screen_max_cases: int | None = None,
    deep_max_cases: int | None = None,
    memory_mb: int = DEFAULT_MEMORY_MB,
    deep_launches: int = DEFAULT_DEEP_LAUNCHES,
    global_seed: int = DEFAULT_GLOBAL_SEED,
) -> BatchPlan:
    validation = validate_second_batch_registry(registry)
    screen_time_seconds = int(screen_time_seconds)
    deep_time_seconds = int(deep_time_seconds)
    memory_mb = int(memory_mb)
    deep_launches = int(deep_launches)
    if min(
        screen_time_seconds,
        deep_time_seconds,
        memory_mb,
        deep_launches,
    ) <= 0:
        raise ValueError("time, memory, and launch budgets must be positive")
    screen_max_cases = _positive_optional(
        screen_max_cases, label="screen_max_cases"
    )
    deep_max_cases = _positive_optional(
        deep_max_cases, label="deep_max_cases"
    )
    bank = {
        problem.problem_id: problem
        for problem in load_problem_bank(bank_path.expanduser().resolve())
    }
    missing = sorted(set(validation["problem_ids"]) - set(bank))
    if missing:
        raise SecondBatchConfigurationError(
            "second-batch problems missing from bank: " + ", ".join(missing)
        )

    problem_plans: list[BatchProblemPlan] = []
    ordered_specs = [
        (family.family, spec)
        for family in registry.families
        for spec in family.specs
    ]
    runner_fingerprints = {
        family.family: _runner_fingerprint(family.runner)
        for family in registry.families
    }
    for rank, (family, spec) in enumerate(ordered_specs, start=1):
        problem = bank[_spec_problem_id(spec)]
        executor_id = _executor_id(spec, family=family)
        version = _executor_version(spec)
        contract = _normalize_model_contract(spec.get("model_contract"))
        claim_scope = str(
            spec.get("claim_scope") or contract.get("claim_scope") or ""
        ).strip()
        if claim_scope not in SECOND_BATCH_CLAIM_SCOPES:
            raise SecondBatchConfigurationError(
                f"{problem.problem_id}.claim_scope must be one of "
                + ", ".join(sorted(SECOND_BATCH_CLAIM_SCOPES))
            )
        scope_limitation = str(
            spec.get("scope_limitation")
            or contract.get("scope_limitation")
            or ""
        ).strip()
        if not scope_limitation:
            raise SecondBatchConfigurationError(
                f"{problem.problem_id}.scope_limitation must not be empty"
            )
        contract["claim_scope"] = claim_scope
        contract["scope_limitation"] = scope_limitation
        screen_bounds = _normalize_bounds(
            spec.get("screen_bounds", spec.get("default_bounds")),
            label="screen_bounds",
        )
        spec_screen_max = screen_bounds.pop("max_cases", None)
        effective_screen_max = (
            screen_max_cases
            if screen_max_cases is not None
            else _spec_max_cases(
                spec_screen_max,
                label=f"{problem.problem_id}.screen_bounds.max_cases",
            )
        )
        common_config = {
            "family": family,
            "source_id": spec.get("source_id"),
            "spec_fingerprint": _canonical_fingerprint(dict(spec)),
            "runner_fingerprint": runner_fingerprints[family],
        }
        declared_strategies = [
            str(value).strip()
            for value in spec.get("strategies", ())
            if str(value).strip()
        ]
        if not declared_strategies:
            raise SecondBatchConfigurationError(
                f"{problem.problem_id} does not declare an executable strategy"
            )
        screen_strategy_id = str(
            spec.get("screen_strategy") or declared_strategies[0]
        )
        strategies = [
            StrategyPlan(
                stage_id="screen",
                strategy_id=screen_strategy_id,
                executor_id=executor_id,
                executor_version=version,
                budget=StrategyBudget(
                    time_seconds=screen_time_seconds,
                    max_cases=effective_screen_max,
                    memory_mb=memory_mb,
                    parameters=screen_bounds,
                ),
                launches=1,
                requires_independent_verification=True,
                config={
                    **common_config,
                    "mode": "screen",
                    "search_role": str(
                        spec.get("screen_search_role") or "bounded_screen"
                    ),
                    "frontier_provenance": {},
                },
            )
        ]
        if _supports_deep(spec):
            deep_bounds = _normalize_bounds(
                spec.get("deep_bounds", spec.get("default_bounds")),
                label="deep_bounds",
            )
            spec_deep_max = deep_bounds.pop("max_cases", None)
            effective_deep_max = (
                deep_max_cases
                if deep_max_cases is not None
                else _spec_max_cases(
                    spec_deep_max,
                    label=f"{problem.problem_id}.deep_bounds.max_cases",
                )
            )
            launches = int(spec.get("deep_launches", deep_launches))
            if launches <= 0:
                raise SecondBatchConfigurationError(
                    f"{problem.problem_id}.deep_launches must be positive"
                )
            deep_strategy_ids = [
                str(value).strip()
                for value in spec.get("deep_strategies", declared_strategies[1:])
                if str(value).strip()
            ] or [screen_strategy_id]
            for deep_strategy_id in deep_strategy_ids:
                strategies.append(
                    StrategyPlan(
                        stage_id="deep",
                        strategy_id=deep_strategy_id,
                        executor_id=executor_id,
                        executor_version=version,
                        budget=StrategyBudget(
                            time_seconds=deep_time_seconds,
                            max_cases=effective_deep_max,
                            memory_mb=memory_mb,
                            parameters=deep_bounds,
                        ),
                        launches=launches,
                        requires_independent_verification=True,
                        config={
                            **common_config,
                            "mode": "deep",
                            "search_role": str(
                                spec.get("deep_search_role")
                                or "bounded_deep_search"
                            ),
                            "frontier_provenance": dict(
                                spec.get("frontier_provenance") or {}
                            ),
                        },
                    )
                )
        audit_status = str(spec.get("model_audit_status") or "approved")
        problem_plans.append(
            BatchProblemPlan(
                problem_id=problem.problem_id,
                title=problem.title,
                statement_hash=_sha256(problem.statement),
                domain=problem.domain,
                source=problem.source,
                model_contract=contract,
                strategies=tuple(strategies),
                model_audit_status=audit_status,
                priority=float(
                    spec.get("priority")
                    if spec.get("priority") is not None
                    else SECOND_BATCH_EXPECTED_TOTAL - rank
                ),
            )
        )
    return BatchPlan(
        batch_id=SECOND_BATCH_ID,
        collection=SECOND_BATCH_COLLECTION,
        problems=tuple(problem_plans),
        global_seed=int(global_seed),
        expected_problem_count=SECOND_BATCH_EXPECTED_TOTAL,
    )


def _plan_to_json(plan: BatchPlan) -> dict[str, Any]:
    return plan.as_dict()


def _budget_from_json(payload: Mapping[str, Any]) -> StrategyBudget:
    return StrategyBudget(
        time_seconds=int(payload["time_seconds"]),
        max_cases=payload.get("max_cases"),
        memory_mb=payload.get("memory_mb"),
        parameters=dict(payload.get("parameters") or {}),
    )


def _plan_from_json(payload: Mapping[str, Any]) -> BatchPlan:
    problems = []
    for problem in payload["problems"]:
        strategies = [
            StrategyPlan(
                stage_id=strategy["stage_id"],
                strategy_id=strategy["strategy_id"],
                executor_id=strategy["executor_id"],
                executor_version=strategy["executor_version"],
                budget=_budget_from_json(strategy["budget"]),
                launches=int(strategy["launches"]),
                requires_independent_verification=bool(
                    strategy["requires_independent_verification"]
                ),
                config=dict(strategy.get("config") or {}),
            )
            for strategy in problem["strategies"]
        ]
        problems.append(
            BatchProblemPlan(
                problem_id=problem["problem_id"],
                title=problem["title"],
                statement_hash=problem["statement_hash"],
                domain=problem["domain"],
                source=problem["source"],
                model_contract=dict(problem["model_contract"]),
                strategies=tuple(strategies),
                model_audit_status=problem["model_audit_status"],
                priority=float(problem["priority"]),
            )
        )
    return BatchPlan(
        batch_id=payload["batch_id"],
        collection=payload["collection"],
        problems=tuple(problems),
        global_seed=int(payload["global_seed"]),
        expected_problem_count=payload.get("expected_problem_count"),
    )


def _campaign_paths(campaign_dir: Path) -> dict[str, Path]:
    root = campaign_dir.expanduser().resolve()
    return {
        "root": root,
        "database": root / SECOND_BATCH_DATABASE_FILE,
        "plan": root / SECOND_BATCH_PLAN_FILE,
        "model_audit": root / SECOND_BATCH_MODEL_AUDIT_FILE,
        "csv": root / SECOND_BATCH_STATUS_CSV_FILE,
        "jsonl": root / SECOND_BATCH_STATUS_JSONL_FILE,
        "markdown": root / SECOND_BATCH_STATUS_MARKDOWN_FILE,
        "summary": root / SECOND_BATCH_SUMMARY_FILE,
        "main_database": root / MAIN_STATUS_DATABASE_FILE,
    }


def _coordinator(
    campaign_dir: Path,
    plan: BatchPlan,
    registry: SecondBatchRegistry,
    *,
    executor_ids: Iterable[str] | None = None,
) -> BatchCampaignCoordinator:
    paths = _campaign_paths(campaign_dir)
    available = (
        registry.executor_ids
        if executor_ids is None
        else frozenset(str(value) for value in executor_ids)
    )
    unknown = set(available) - set(registry.executor_ids)
    if unknown:
        raise SecondBatchConfigurationError(
            "unknown second-batch executors: " + ", ".join(sorted(unknown))
        )
    return BatchCampaignCoordinator(
        paths["database"],
        plan,
        available_executors=available,
    )


def initialize_second_batch(
    *,
    bank_path: Path,
    campaign_dir: Path,
    registry: SecondBatchRegistry | None = None,
    screen_time_seconds: int = DEFAULT_SCREEN_TIME_SECONDS,
    deep_time_seconds: int = DEFAULT_DEEP_TIME_SECONDS,
    screen_max_cases: int | None = None,
    deep_max_cases: int | None = None,
    memory_mb: int = DEFAULT_MEMORY_MB,
    deep_launches: int = DEFAULT_DEEP_LAUNCHES,
    global_seed: int = DEFAULT_GLOBAL_SEED,
) -> dict[str, Any]:
    registry = registry or load_default_second_batch_registry()
    plan = build_second_batch_plan(
        bank_path=bank_path,
        registry=registry,
        screen_time_seconds=screen_time_seconds,
        deep_time_seconds=deep_time_seconds,
        screen_max_cases=screen_max_cases,
        deep_max_cases=deep_max_cases,
        memory_mb=memory_mb,
        deep_launches=deep_launches,
        global_seed=global_seed,
    )
    paths = _campaign_paths(campaign_dir)
    paths["root"].mkdir(parents=True, exist_ok=True)
    coordinator = _coordinator(campaign_dir, plan, registry)
    initialized = coordinator.initialize()
    _write_json(paths["plan"], _plan_to_json(plan))
    model_audits = _record_plan_model_audits(
        coordinator=coordinator,
        audit_path=paths["model_audit"],
    )
    artifacts = export_second_batch_status(
        campaign_dir=campaign_dir,
        coordinator=coordinator,
    )
    return {
        "schema_version": SECOND_BATCH_SCHEMA_VERSION,
        "batch_id": SECOND_BATCH_ID,
        "bank": str(bank_path.expanduser().resolve()),
        "initialization": initialized,
        "model_audits": model_audits,
        "artifacts": artifacts,
    }


def _record_plan_model_audits(
    *,
    coordinator: BatchCampaignCoordinator,
    audit_path: Path,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for problem in coordinator.plan.problems:
        contract_fingerprint = _canonical_fingerprint(problem.model_contract)
        detail = {
            "audit_kind": "registered_executor_contract_audit",
            "auditor_id": "second-batch-spec-contract-auditor-v1",
            "problem_id": problem.problem_id,
            "statement_hash": problem.statement_hash,
            "model_contract_fingerprint": contract_fingerprint,
            "claim_scope": problem.model_contract["claim_scope"],
            "scope_limitation": problem.model_contract["scope_limitation"],
            "checks": {
                "bank_problem_resolved": True,
                "statement_hash_frozen": True,
                "model_contract_nonempty": bool(problem.model_contract),
                "claim_scope_valid": (
                    problem.model_contract.get("claim_scope")
                    in SECOND_BATCH_CLAIM_SCOPES
                ),
                "executor_and_version_fingerprinted": all(
                    strategy.executor_id and strategy.executor_version
                    for strategy in problem.strategies
                ),
                "bounded_search_not_treated_as_proof": True,
                "candidate_requires_independent_verification": all(
                    strategy.requires_independent_verification
                    for strategy in problem.strategies
                ),
            },
            "scope": (
                "This mechanical audit validates the frozen executable contract "
                "and provenance fields; it is not an independent proof of semantic "
                "equivalence to the source conjecture."
            ),
            "status": problem.model_audit_status,
        }
        state = coordinator.record_model_audit(
            problem.problem_id,
            status=problem.model_audit_status,
            auditor_id="second-batch-spec-contract-auditor-v1",
            detail=detail,
            stop_reason=(
                ""
                if problem.model_audit_status == "approved"
                else f"model_audit_{problem.model_audit_status}"
            ),
        )
        rows.append(
            {
                **detail,
                "recorded_status": state["model_audit_status"],
            }
        )
    _atomic_write_text(
        audit_path,
        "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
            for row in rows
        ),
    )
    return {
        "auditor_id": "second-batch-spec-contract-auditor-v1",
        "audit_count": len(rows),
        "artifact": str(audit_path),
        "status_counts": _count_values(
            row["recorded_status"] for row in rows
        ),
    }


def _load_initialized_plan(campaign_dir: Path) -> BatchPlan:
    path = _campaign_paths(campaign_dir)["plan"]
    if not path.exists():
        raise SecondBatchConfigurationError(
            f"second batch is not initialized: missing {path}"
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    plan = _plan_from_json(payload)
    if (
        plan.batch_id != SECOND_BATCH_ID
        or len(plan.problems) != SECOND_BATCH_EXPECTED_TOTAL
    ):
        raise SecondBatchConfigurationError("stored second-batch plan is invalid")
    return plan


def _runner_budget(claim: BatchClaim) -> dict[str, Any]:
    budget = dict(claim.budget.get("parameters") or {})
    budget["time_seconds"] = int(claim.budget["time_seconds"])
    if claim.budget.get("max_cases") is not None:
        budget["max_cases"] = int(claim.budget["max_cases"])
    if claim.budget.get("memory_mb") is not None:
        budget["memory_mb"] = int(claim.budget["memory_mb"])
    return budget


def _normalize_runner_result(value: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise SecondBatchExecutionError("executor result must be a mapping")
    result = dict(value)
    outcome_aliases = {
        "candidate": "candidate",
        "candidate_counterexample": "candidate",
        "bounded_search_candidate": "candidate",
        "no_candidate": "no_candidate",
        "no_counterexample_within_bound": "no_candidate",
        "no_candidate_in_bounded_range": "no_candidate",
        "bounded_search_no_counterexample": "no_candidate",
        "inconclusive": "inconclusive",
        "paused": "inconclusive",
        "time_budget_exhausted": "inconclusive",
        "case_budget_exhausted": "inconclusive",
    }
    raw_outcome = str(result.get("outcome") or "").strip()
    outcome = outcome_aliases.get(raw_outcome)
    if outcome is None:
        raise SecondBatchExecutionError(
            f"executor returned unsupported outcome {raw_outcome!r}"
        )
    candidate = result.get("candidate")
    if outcome == "candidate" and not isinstance(candidate, Mapping):
        raise SecondBatchExecutionError(
            "candidate outcome requires a mapping candidate"
        )
    if outcome != "candidate" and candidate is not None:
        raise SecondBatchExecutionError(
            "non-candidate outcome must not include a candidate"
        )
    stop_reason = str(result.get("stop_reason") or "").strip()
    if not stop_reason:
        raise SecondBatchExecutionError("executor result is missing stop_reason")
    checkpoint = result.get("checkpoint") or {}
    if not isinstance(checkpoint, Mapping):
        raise SecondBatchExecutionError("executor checkpoint must be a mapping")
    result["outcome"] = outcome
    result["candidate"] = None if candidate is None else dict(candidate)
    result["stop_reason"] = stop_reason
    result["checkpoint"] = dict(checkpoint)
    result["checked_cases"] = int(result.get("checked_cases") or 0)
    executor_metrics = result.get("metrics") or {}
    if not isinstance(executor_metrics, Mapping):
        raise SecondBatchExecutionError("executor metrics must be a mapping")
    result["metrics"] = dict(executor_metrics)
    return result


def _validate_runner_result_identity(
    result: Mapping[str, Any],
    *,
    claim: BatchClaim,
    coordinator: BatchCampaignCoordinator,
) -> None:
    reported_executor = str(result.get("executor_id") or "").strip()
    reported_version = str(
        result.get("executor_version") or result.get("version") or ""
    ).strip()
    reported_strategy = str(result.get("strategy_id") or "").strip()
    mismatches: list[str] = []
    if reported_executor != claim.executor_id:
        mismatches.append(
            f"executor_id {reported_executor!r} != {claim.executor_id!r}"
        )
    if reported_version != claim.executor_version:
        mismatches.append(
            f"executor_version {reported_version!r} != "
            f"{claim.executor_version!r}"
        )
    if reported_strategy != claim.strategy_id:
        mismatches.append(
            f"strategy_id {reported_strategy!r} != {claim.strategy_id!r}"
        )
    problem = next(
        value
        for value in coordinator.plan.problems
        if value.problem_id == claim.parent_problem_id
    )
    reported_contract = result.get("model_contract")
    try:
        normalized_contract = _normalize_model_contract(reported_contract)
    except SecondBatchConfigurationError:
        mismatches.append("model_contract is missing or invalid")
    else:
        normalized_contract.setdefault(
            "claim_scope", problem.model_contract["claim_scope"]
        )
        normalized_contract.setdefault(
            "scope_limitation", problem.model_contract["scope_limitation"]
        )
        if normalized_contract != dict(problem.model_contract):
            mismatches.append("model_contract differs from the frozen plan")
    if mismatches:
        raise SecondBatchExecutionError(
            "executor result identity mismatch for "
            f"{claim.task_id}: " + "; ".join(mismatches)
        )


def _memory_safe_addition_chain_length(
    target: int,
    deadline: float | None,
    *,
    check_deadline: Callable[[float | None], None],
) -> int:
    """Compute an exact shortest addition-chain length without a BFS frontier."""

    target = int(target)
    if target <= 1:
        return 0

    # Repeated doubling gives the lower bound.  The usual binary method gives
    # a concrete chain and therefore a safe inclusive upper bound.
    lower_bound = (target - 1).bit_length()
    upper_bound = target.bit_length() - 1 + target.bit_count() - 1
    chain = [1]

    def reaches_target(remaining: int) -> bool:
        check_deadline(deadline)
        largest = chain[-1]
        if largest == target:
            return True
        if remaining <= 0 or largest << remaining < target:
            return False

        additions: set[int] = set()
        for left in range(len(chain) - 1, -1, -1):
            check_deadline(deadline)
            for right in range(left, -1, -1):
                value = chain[left] + chain[right]
                if (
                    largest < value <= target
                    and value << (remaining - 1) >= target
                ):
                    additions.add(value)

        for value in sorted(additions, reverse=True):
            chain.append(value)
            try:
                if reaches_target(remaining - 1):
                    return True
            finally:
                chain.pop()
        return False

    for depth in range(lower_bound, upper_bound + 1):
        if reaches_target(depth):
            return depth
    raise RuntimeError(f"addition-chain search failed for {target}")


@contextmanager
def _runner_compatibility_shims(
    claim: BatchClaim,
    runner: Runner,
) -> Iterator[list[str]]:
    shims: list[str] = []
    restore: Callable[[], None] | None = None
    if (
        claim.parent_problem_id == "unsolvedmath-kou-21.2"
        and claim.executor_id == "second_batch.arithmetic.kou_21_2.v1"
    ):
        from amra.discovery import second_batch_arithmetic

        if runner is second_batch_arithmetic.run_second_batch_arithmetic_search:
            original_run_gap = second_batch_arithmetic._run_gap

            def wide_gap_protocol(
                script: str,
                *,
                timeout: int = 120,
            ) -> str:
                return original_run_gap(
                    "SizeScreen([1000000,1000000]);;\n" + script,
                    timeout=timeout,
                )

            second_batch_arithmetic._run_gap = wide_gap_protocol
            shims.append("kou-21.2-gap-screen-width-v1")

            def restore() -> None:
                second_batch_arithmetic._run_gap = original_run_gap

    elif (
        claim.parent_problem_id == "unsolvedmath-nt-039"
        and claim.executor_id == "second_batch.finite.exact_search.v1"
    ):
        from amra.discovery import second_batch_finite

        if runner is second_batch_finite.run_second_batch_finite_search:
            original_addition_chain_length = (
                second_batch_finite._addition_chain_length
            )

            def memory_safe_addition_chain_length(
                target: int,
                deadline: float | None = None,
            ) -> int:
                return _memory_safe_addition_chain_length(
                    target,
                    deadline,
                    check_deadline=second_batch_finite._check_deadline,
                )

            second_batch_finite._addition_chain_length = (
                memory_safe_addition_chain_length
            )
            shims.append("nt-039-addition-chain-iddfs-v1")

            def restore() -> None:
                second_batch_finite._addition_chain_length = (
                    original_addition_chain_length
                )

    try:
        yield shims
    finally:
        if restore is not None:
            restore()


@contextmanager
def _lease_heartbeat(
    coordinator: BatchCampaignCoordinator,
    claim: BatchClaim,
    *,
    lease_seconds: float,
) -> Iterator[list[BaseException]]:
    stop = threading.Event()
    errors: list[BaseException] = []
    interval = max(0.1, min(30.0, lease_seconds / 3))

    def renew() -> None:
        while not stop.wait(interval):
            try:
                coordinator.heartbeat(claim, extend_seconds=lease_seconds)
            except BaseException as exc:
                errors.append(exc)
                return

    thread = threading.Thread(
        target=renew,
        name=f"batch2-heartbeat-{claim.task_id}",
        daemon=True,
    )
    thread.start()
    try:
        yield errors
    finally:
        stop.set()
        thread.join(timeout=max(1.0, interval + 1.0))


def _attempt_artifact_path(campaign_dir: Path, claim: BatchClaim) -> Path:
    return (
        campaign_dir.expanduser().resolve()
        / "batch-2-attempts"
        / claim.parent_problem_id
        / claim.stage_id
        / claim.strategy_id
        / f"launch-{claim.launch_index:03d}-attempt-{claim.attempt_id:06d}.json"
    )


def _execute_claim(
    *,
    campaign_dir: Path,
    coordinator: BatchCampaignCoordinator,
    registry: SecondBatchRegistry,
    claim: BatchClaim,
    lease_seconds: float,
) -> dict[str, Any]:
    runner = registry.runner_for(claim.executor_id)
    latest = claim.checkpoint or {}
    checkpoint = dict(latest.get("cursor") or {})
    progress_count = 0

    def progress(cursor: Mapping[str, Any], checked_cases: int = 0) -> None:
        nonlocal progress_count
        if not isinstance(cursor, Mapping):
            raise SecondBatchExecutionError("progress cursor must be a mapping")
        progress_count += 1
        coordinator.save_checkpoint(
            claim,
            cursor=dict(cursor),
            metrics={
                "checked_cases": int(checked_cases),
                "progress_updates": progress_count,
            },
        )

    started = time.monotonic()
    with _runner_compatibility_shims(claim, runner) as compatibility_shims:
        with _lease_heartbeat(
            coordinator,
            claim,
            lease_seconds=lease_seconds,
        ) as heartbeat_errors:
            raw_result = runner(
                claim.parent_problem_id,
                strategy_id=claim.strategy_id,
                budget=_runner_budget(claim),
                seed=claim.deterministic_seed,
                checkpoint=checkpoint or None,
                progress=progress,
            )
    if heartbeat_errors:
        raise heartbeat_errors[0]
    result = _normalize_runner_result(raw_result)
    _validate_runner_result_identity(
        result,
        claim=claim,
        coordinator=coordinator,
    )
    artifact_payload = {
        "schema_version": SECOND_BATCH_SCHEMA_VERSION,
        "task_id": claim.task_id,
        "attempt_id": claim.attempt_id,
        "worker_id": claim.worker_id,
        "parent_problem_id": claim.parent_problem_id,
        "stage_id": claim.stage_id,
        "strategy_id": claim.strategy_id,
        "launch_index": claim.launch_index,
        "deterministic_seed": claim.deterministic_seed,
        "config_fingerprint": claim.config_fingerprint,
        "budget": claim.budget,
        "compatibility_shims": compatibility_shims,
        "duration_seconds": round(time.monotonic() - started, 6),
        "executor_result": result,
    }
    artifact = _attempt_artifact_path(campaign_dir, claim)
    _write_json(artifact, artifact_payload)
    metrics = {
        "checked_cases": result["checked_cases"],
        "attempt_artifact": str(artifact),
        "tool_versions": result.get("tool_versions") or {},
        "progress_updates": progress_count,
        "executor_metrics": result["metrics"],
    }
    if compatibility_shims:
        metrics["compatibility_shims"] = compatibility_shims
    coordinator.complete(
        claim,
        outcome=result["outcome"],
        stop_reason=result["stop_reason"],
        candidate=result["candidate"],
        metrics=metrics,
        final_cursor=result["checkpoint"],
    )
    _auto_advance(coordinator, claim.parent_problem_id)
    return {
        "task_id": claim.task_id,
        "problem_id": claim.parent_problem_id,
        "stage_id": claim.stage_id,
        "strategy_id": claim.strategy_id,
        "launch_index": claim.launch_index,
        "outcome": result["outcome"],
        "stop_reason": result["stop_reason"],
        "candidate": result["candidate"],
        "attempt_artifact": str(artifact),
    }


def _auto_advance(
    coordinator: BatchCampaignCoordinator,
    problem_id: str,
) -> list[str]:
    problem = next(
        problem
        for problem in coordinator.plan.problems
        if problem.problem_id == problem_id
    )
    if "deep" not in problem.stage_ids:
        return []
    state = coordinator.problem_state(problem_id)
    if state["verification_status"] in {
        "pending",
        "verified",
        "contested",
    }:
        return []
    screen = [
        task
        for task in coordinator.tasks()
        if task["metadata"].get("parent_problem_id") == problem_id
        and task["metadata"].get("stage_id") == "screen"
        and task["metadata"].get("implementation_status") == "registered"
    ]
    if not screen or any(task["status"] != "completed" for task in screen):
        return []
    try:
        return coordinator.activate_stage(problem_id, "deep")
    except BatchStateError as exc:
        if "earlier stages are not terminal" in str(exc):
            return []
        raise


def _reconcile_second_batch_stages(
    coordinator: BatchCampaignCoordinator,
) -> list[str]:
    activated: list[str] = []
    for problem in coordinator.plan.problems:
        activated.extend(_auto_advance(coordinator, problem.problem_id))
    return sorted(set(activated))


def run_second_batch(
    *,
    campaign_dir: Path,
    registry: SecondBatchRegistry | None = None,
    worker_id: str = "batch2-worker",
    lease_seconds: float = 300,
    max_tasks: int | None = None,
    max_attempts: int = 3,
    executor_ids: Iterable[str] | None = None,
) -> dict[str, Any]:
    registry = registry or load_default_second_batch_registry()
    validate_second_batch_registry(registry)
    plan = _load_initialized_plan(campaign_dir)
    _validate_plan_registry_compatibility(plan, registry)
    coordinator = _coordinator(
        campaign_dir,
        plan,
        registry,
        executor_ids=executor_ids,
    )
    coordinator.initialize()
    coordinator.store.recover_expired_leases()
    _reconcile_second_batch_stages(coordinator)
    max_attempts = int(max_attempts)
    if max_attempts <= 0:
        raise ValueError("max_attempts must be positive")
    limit = None if max_tasks is None else max(0, int(max_tasks))
    completed: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    interrupted: list[str] = []

    while limit is None or len(completed) + len(failed) < limit:
        claim = coordinator.claim(worker_id, lease_seconds=lease_seconds)
        if claim is None:
            break
        try:
            result = _execute_claim(
                campaign_dir=campaign_dir,
                coordinator=coordinator,
                registry=registry,
                claim=claim,
                lease_seconds=lease_seconds,
            )
            completed.append(result)
        except KeyboardInterrupt:
            try:
                coordinator.interrupt(
                    claim,
                    stop_reason="campaign_interrupted_by_operator",
                )
            except LeaseLostError:
                pass
            interrupted.append(claim.task_id)
            break
        except Exception as exc:
            stop_reason = f"{type(exc).__name__}: {exc}"
            retryable = claim.leased_work.problem["attempt_count"] < max_attempts
            try:
                coordinator.fail(
                    claim,
                    stop_reason=stop_reason,
                    retryable=retryable,
                    retry_after_seconds=60 if retryable else 0,
                )
            except LeaseLostError:
                pass
            failure_artifact = _attempt_artifact_path(campaign_dir, claim).with_name(
                f"failure-{claim.attempt_id:06d}.json"
            )
            _write_json(
                failure_artifact,
                {
                    "schema_version": SECOND_BATCH_SCHEMA_VERSION,
                    "task_id": claim.task_id,
                    "problem_id": claim.parent_problem_id,
                    "attempt_id": claim.attempt_id,
                    "stop_reason": stop_reason,
                    "retryable": retryable,
                    "traceback": traceback.format_exc(),
                },
            )
            failed.append(
                {
                    "task_id": claim.task_id,
                    "problem_id": claim.parent_problem_id,
                    "stop_reason": stop_reason,
                    "retryable": retryable,
                    "failure_artifact": str(failure_artifact),
                }
            )
        export_second_batch_status(
            campaign_dir=campaign_dir,
            coordinator=coordinator,
        )

    sync = sync_second_batch_to_main(
        campaign_dir=campaign_dir,
        coordinator=coordinator,
    )
    artifacts = export_second_batch_status(
        campaign_dir=campaign_dir,
        coordinator=coordinator,
        main_sync=sync,
    )
    return {
        "schema_version": SECOND_BATCH_SCHEMA_VERSION,
        "batch_id": SECOND_BATCH_ID,
        "worker_id": worker_id,
        "processed_this_run": len(completed) + len(failed),
        "completed_this_run": completed,
        "failed_this_run": failed,
        "interrupted_this_run": interrupted,
        "summary": coordinator.summary(),
        "main_sync": sync,
        "artifacts": artifacts,
    }


def record_second_batch_verification(
    *,
    campaign_dir: Path,
    problem_id: str,
    verifier_id: str,
    verdict: str,
    evidence: Mapping[str, Any],
    registry: SecondBatchRegistry | None = None,
) -> dict[str, Any]:
    registry = registry or load_default_second_batch_registry()
    validate_second_batch_registry(registry)
    plan = _load_initialized_plan(campaign_dir)
    _validate_plan_registry_compatibility(plan, registry)
    coordinator = _coordinator(campaign_dir, plan, registry)
    coordinator.initialize()
    state = coordinator.record_independent_verification(
        problem_id,
        verifier_id=verifier_id,
        verdict=verdict,
        evidence=evidence,
    )
    activated = _auto_advance(coordinator, problem_id)
    sync = sync_second_batch_to_main(
        campaign_dir=campaign_dir,
        coordinator=coordinator,
    )
    artifacts = export_second_batch_status(
        campaign_dir=campaign_dir,
        coordinator=coordinator,
        main_sync=sync,
    )
    return {
        "schema_version": SECOND_BATCH_SCHEMA_VERSION,
        "problem_state": state,
        "activated_task_ids": activated,
        "main_sync": sync,
        "artifacts": artifacts,
    }


def _parent_status_rows(
    coordinator: BatchCampaignCoordinator,
) -> list[dict[str, Any]]:
    tasks = coordinator.tasks()
    latest_checkpoints = coordinator.store.latest_checkpoints(
        task["problem_id"] for task in tasks
    )
    rows: list[dict[str, Any]] = []
    for problem in coordinator.plan.problems:
        problem_tasks = [
            task
            for task in tasks
            if task["metadata"].get("parent_problem_id") == problem.problem_id
        ]
        state = coordinator.problem_state(problem.problem_id)
        task_status_counts: dict[str, int] = {}
        stage_status: dict[str, dict[str, int]] = {}
        outcomes: dict[str, int] = {}
        stop_reasons: list[str] = []
        task_progress: list[dict[str, Any]] = []
        search_roles: set[str] = set()
        frontier_provenance: list[dict[str, Any]] = []
        checked_cases = 0
        attempt_count = 0
        completed_task_count = 0
        task_updated_at: list[str] = []
        for task in problem_tasks:
            status = str(task["status"])
            task_status_counts[status] = task_status_counts.get(status, 0) + 1
            completed_task_count += int(status == "completed")
            attempts = int(task.get("attempt_count") or 0)
            attempt_count += attempts
            if task.get("updated_at"):
                task_updated_at.append(str(task["updated_at"]))
            stage = str(task["metadata"]["stage_id"])
            stage_counts = stage_status.setdefault(stage, {})
            stage_counts[status] = stage_counts.get(status, 0) + 1
            result = task.get("last_result") or {}
            outcome = str(result.get("outcome") or "")
            if outcome:
                outcomes[outcome] = outcomes.get(outcome, 0) + 1
            reason = str(
                result.get("stop_reason")
                or task.get("last_error")
                or task["metadata"].get("planned_stop_reason")
                or ""
            )
            if reason and reason not in stop_reasons:
                stop_reasons.append(reason)
            latest_checkpoint = latest_checkpoints.get(str(task["problem_id"]))
            result_metrics = result.get("metrics") or {}
            checkpoint_metrics = (
                (latest_checkpoint or {}).get("metrics") or {}
            )
            latest_attempt_checked = int(
                result_metrics.get(
                    "checked_cases",
                    checkpoint_metrics.get("checked_cases", 0),
                )
                or 0
            )
            cursor = (
                {}
                if latest_checkpoint is None
                else latest_checkpoint.get("cursor") or {}
            )
            cursor_checked = (
                int(cursor.get("checked_cases") or 0)
                if isinstance(cursor, Mapping)
                else 0
            )
            next_case = (
                int(cursor.get("next_case") or 0)
                if isinstance(cursor, Mapping)
                else 0
            )
            task_checked = max(
                latest_attempt_checked,
                int(checkpoint_metrics.get("checked_cases") or 0),
                cursor_checked,
                next_case,
            )
            checked_cases += task_checked
            search_role = str(
                task["metadata"]["config"].get("search_role")
                or "unspecified"
            )
            search_roles.add(search_role)
            task_frontier = dict(
                task["metadata"]["config"].get("frontier_provenance")
                or {}
            )
            if task_frontier and task_frontier not in frontier_provenance:
                frontier_provenance.append(task_frontier)
            task_progress.append(
                {
                    "task_id": task["problem_id"],
                    "stage": stage,
                    "strategy_id": task["metadata"]["strategy_id"],
                    "launch_index": int(task["metadata"]["launch_index"]),
                    "search_role": search_role,
                    "frontier_provenance": task_frontier,
                    "status": status,
                    "attempt_count": attempts,
                    "checked_cases": task_checked,
                    "latest_attempt_checked_cases": latest_attempt_checked,
                    "checkpoint_id": (
                        None
                        if latest_checkpoint is None
                        else int(latest_checkpoint["checkpoint_id"])
                    ),
                    "checkpoint_sequence": (
                        None
                        if latest_checkpoint is None
                        else int(latest_checkpoint["sequence"])
                    ),
                    "checkpoint_created_at": (
                        None
                        if latest_checkpoint is None
                        else latest_checkpoint["created_at"]
                    ),
                    "outcome": outcome,
                    "stop_reason": reason,
                    "cursor": None if latest_checkpoint is None else cursor,
                    "budget": task["metadata"]["budget"],
                    "updated_at": task.get("updated_at"),
                }
            )
        aggregate, final = _aggregate_parent_status(
            problem_tasks=problem_tasks,
            problem_state=state,
        )
        rows.append(
            {
                "problem_id": problem.problem_id,
                "title": problem.title,
                "domain": problem.domain,
                "source": problem.source,
                "statement_hash": problem.statement_hash,
                "aggregate_status": aggregate,
                "final": final,
                "model_audit_status": state["model_audit_status"],
                "claim_scope": problem.model_contract["claim_scope"],
                "scope_limitation": problem.model_contract["scope_limitation"],
                "verification_status": state["verification_status"],
                "candidate_fingerprint": state["candidate_fingerprint"],
                "updated_at": max(task_updated_at, default=None),
                "task_count": len(problem_tasks),
                "completed_task_count": completed_task_count,
                "attempt_count": attempt_count,
                "checked_cases": checked_cases,
                "search_roles": sorted(search_roles),
                "frontier_provenance": frontier_provenance,
                "task_status_counts": task_status_counts,
                "stage_status": stage_status,
                "outcome_counts": outcomes,
                "stop_reasons": stop_reasons,
                "task_progress": task_progress,
            }
        )
    return rows


def _aggregate_parent_status(
    *,
    problem_tasks: Sequence[Mapping[str, Any]],
    problem_state: Mapping[str, Any],
) -> tuple[str, bool]:
    verification = str(problem_state["verification_status"])
    if verification == "verified":
        return "candidate_verified", True
    if verification == "pending":
        return "candidate_pending_verification", False
    if verification == "contested":
        return "candidate_contested", False
    if verification == "inconclusive":
        return "candidate_verification_inconclusive", False
    if verification == "rejected":
        return "candidate_rejected", False
    if problem_state["model_audit_status"] != "approved":
        return f"model_audit_{problem_state['model_audit_status']}", False
    statuses = {str(task["status"]) for task in problem_tasks}
    if "running" in statuses:
        return "running", False
    if statuses & {"queued", "retry"}:
        return "queued", False
    registered = [
        task
        for task in problem_tasks
        if task["metadata"].get("implementation_status") == "registered"
    ]
    if registered and all(task["status"] == "completed" for task in registered):
        return "bounded_search_completed", True
    if "failed" in statuses:
        return "failed", False
    return "parked", False


def sync_second_batch_to_main(
    *,
    campaign_dir: Path,
    coordinator: BatchCampaignCoordinator,
) -> dict[str, Any]:
    paths = _campaign_paths(campaign_dir)
    paths["root"].mkdir(parents=True, exist_ok=True)
    lock_path = paths["root"] / SECOND_BATCH_MAIN_SYNC_LOCK_FILE
    with lock_path.open("a+", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            return _sync_second_batch_to_main_locked(
                campaign_dir=campaign_dir,
                coordinator=coordinator,
            )
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def _sync_second_batch_to_main_locked(
    *,
    campaign_dir: Path,
    coordinator: BatchCampaignCoordinator,
) -> dict[str, Any]:
    paths = _campaign_paths(campaign_dir)
    if not paths["main_database"].exists():
        return {
            "status": "skipped",
            "reason": "main_status_database_missing",
            "synced_problem_ids": [],
            "total_before": None,
            "total_after": None,
        }
    main = CampaignStatusStore(paths["main_database"])
    total_before = main.summary()["total_problems"]
    parent_rows = _parent_status_rows(coordinator)
    current: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    statement_mismatches: list[str] = []
    for row in parent_rows:
        try:
            current[row["problem_id"]] = main.get_problem(row["problem_id"])
        except ProblemNotFoundError:
            missing.append(row["problem_id"])
            continue
        if current[row["problem_id"]]["statement_hash"] != row["statement_hash"]:
            statement_mismatches.append(row["problem_id"])
    if missing:
        raise SecondBatchConfigurationError(
            "main status database is missing second-batch parents: "
            + ", ".join(sorted(missing))
        )
    if statement_mismatches:
        raise SecondBatchConfigurationError(
            "main status statement hashes differ from the batch-2 plan: "
            + ", ".join(sorted(statement_mismatches))
        )

    sync_collection = SECOND_BATCH_COLLECTION
    queued_results: dict[str, dict[str, Any]] = {}
    skipped_active: list[str] = []
    skipped_existing: list[str] = []
    for row in parent_rows:
        existing = current[row["problem_id"]]
        metadata = dict(existing["metadata"])
        metadata["batch_2"] = {
            "schema_version": SECOND_BATCH_SCHEMA_VERSION,
            "aggregate_status": row["aggregate_status"],
            "final": row["final"],
            "model_audit_status": row["model_audit_status"],
            "claim_scope": row["claim_scope"],
            "scope_limitation": row["scope_limitation"],
            "verification_status": row["verification_status"],
            "candidate_fingerprint": row["candidate_fingerprint"],
            "task_status_counts": row["task_status_counts"],
            "stage_status": row["stage_status"],
            "outcome_counts": row["outcome_counts"],
            "stop_reasons": row["stop_reasons"],
            "completed_task_count": row["completed_task_count"],
            "task_count": row["task_count"],
            "attempt_count": row["attempt_count"],
            "checked_cases": row["checked_cases"],
            "search_roles": row["search_roles"],
            "frontier_provenance": row["frontier_provenance"],
            "task_database": str(paths["database"]),
        }
        should_finalize = bool(row["final"])
        existing_result = existing.get("last_result") or {}
        existing_batch_result = (
            existing_result.get("schema_version") == SECOND_BATCH_SCHEMA_VERSION
            and existing_result.get("batch_id") == SECOND_BATCH_ID
        )
        current_result_matches = (
            existing_batch_result
            and existing_result.get("outcome") == row["aggregate_status"]
            and existing_result.get("verification_status")
            == row["verification_status"]
            and existing_result.get("candidate_fingerprint")
            == row["candidate_fingerprint"]
        )
        reset = False
        status = existing["status"]
        collection = existing["collection"]
        stage = existing["stage"]
        if should_finalize and not current_result_matches:
            if existing["status"] == "running":
                skipped_active.append(row["problem_id"])
            elif existing["status"] == "completed" and not existing_batch_result:
                skipped_existing.append(row["problem_id"])
            else:
                reset = True
                status = "queued"
                collection = sync_collection
                stage = "batch2-final"
                queued_results[row["problem_id"]] = {
                    "schema_version": SECOND_BATCH_SCHEMA_VERSION,
                    "batch_id": SECOND_BATCH_ID,
                    "problem_id": row["problem_id"],
                    "outcome": row["aggregate_status"],
                    "verification_status": row["verification_status"],
                    "candidate_fingerprint": row["candidate_fingerprint"],
                    "task_status_counts": row["task_status_counts"],
                    "stage_status": row["stage_status"],
                    "stop_reasons": row["stop_reasons"],
                    "completed_task_count": row["completed_task_count"],
                    "task_count": row["task_count"],
                    "attempt_count": row["attempt_count"],
                    "checked_cases": row["checked_cases"],
                    "search_roles": row["search_roles"],
                    "frontier_provenance": row["frontier_provenance"],
                    "finite_search_notice": (
                        "No candidate in a bounded search is not a proof of the "
                        "original unbounded statement."
                    ),
                    "batch_database": str(paths["database"]),
                }
        elif not should_finalize and existing_batch_result:
            if existing["status"] == "running":
                skipped_active.append(row["problem_id"])
            else:
                reset = True
                status = "parked"
                collection = sync_collection
                stage = "batch2-review"
        main.upsert_problem(
            row["problem_id"],
            title=existing["title"],
            source=existing["source"],
            domain=existing["domain"],
            collection=collection,
            priority=existing["priority"],
            stage=stage,
            statement_hash=existing["statement_hash"],
            metadata=metadata,
            status=status,
            reset_status=reset,
            reset_reason=(
                "second_batch_parent_finalized"
                if reset and should_finalize
                else "second_batch_parent_reopened"
                if reset
                else ""
            ),
        )

    synced: list[str] = []
    while queued_results:
        claim = main.claim(
            "batch2-parent-sync",
            lease_seconds=300,
            collections=[sync_collection],
            method="second-batch-parent-sync",
            config={"batch_id": SECOND_BATCH_ID},
        )
        if claim is None:
            break
        result = queued_results.pop(claim.problem_id, None)
        if result is None:
            main.park(
                claim.problem_id,
                claim.worker_id,
                claim.fencing_token,
                reason="no_second_batch_parent_result",
            )
            continue
        main.complete(
            claim.problem_id,
            claim.worker_id,
            claim.fencing_token,
            result=result,
            stage="batch2-final",
        )
        synced.append(claim.problem_id)
    total_after = main.summary()["total_problems"]
    if total_after != total_before:
        raise CampaignStatusError(
            f"main problem count changed during batch-2 sync: "
            f"{total_before} -> {total_after}"
        )
    return {
        "status": "completed",
        "synced_problem_ids": sorted(synced),
        "skipped_active_problem_ids": sorted(skipped_active),
        "skipped_existing_completed_problem_ids": sorted(skipped_existing),
        "total_before": total_before,
        "total_after": total_after,
    }


def export_second_batch_status(
    *,
    campaign_dir: Path,
    coordinator: BatchCampaignCoordinator,
    main_sync: Mapping[str, Any] | None = None,
) -> dict[str, str]:
    paths = _campaign_paths(campaign_dir)
    paths["root"].mkdir(parents=True, exist_ok=True)
    lock_path = paths["root"] / SECOND_BATCH_EXPORT_LOCK_FILE
    with lock_path.open("a+", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            rows = _parent_status_rows(coordinator)
            summary = {
                "schema_version": SECOND_BATCH_SCHEMA_VERSION,
                "batch": coordinator.summary(),
                "parent_status_counts": _count_values(
                    row["aggregate_status"] for row in rows
                ),
                "final_parent_count": sum(bool(row["final"]) for row in rows),
                "main_sync": dict(main_sync or {}),
            }
            _write_json(paths["summary"], summary)
            _atomic_write_text(
                paths["jsonl"],
                "".join(
                    json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
                    for row in rows
                ),
            )
            _write_parent_csv(paths["csv"], rows)
            _write_parent_markdown(paths["markdown"], rows, summary)
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    return {
        "database": str(paths["database"]),
        "plan": str(paths["plan"]),
        "model_audit": str(paths["model_audit"]),
        "csv": str(paths["csv"]),
        "jsonl": str(paths["jsonl"]),
        "markdown": str(paths["markdown"]),
        "summary": str(paths["summary"]),
    }


def _write_parent_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    columns = [
        "problem_id",
        "title",
        "domain",
        "aggregate_status",
        "final",
        "model_audit_status",
        "claim_scope",
        "scope_limitation",
        "verification_status",
        "candidate_fingerprint",
        "updated_at",
        "task_count",
        "completed_task_count",
        "attempt_count",
        "checked_cases",
        "search_roles",
        "frontier_provenance",
        "task_status_counts",
        "stage_status",
        "outcome_counts",
        "stop_reasons",
        "task_progress",
    ]
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            for item in rows:
                row = dict(item)
                for key in (
                    "task_status_counts",
                    "stage_status",
                    "outcome_counts",
                    "stop_reasons",
                    "task_progress",
                    "search_roles",
                    "frontier_provenance",
                ):
                    row[key] = json.dumps(
                        row[key], ensure_ascii=False, sort_keys=True
                    )
                writer.writerow({column: row.get(column) for column in columns})
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _write_parent_markdown(
    path: Path,
    rows: Sequence[Mapping[str, Any]],
    summary: Mapping[str, Any],
) -> None:
    lines = [
        "# Counterexample Campaign Batch 2",
        "",
        "The task SQLite database is authoritative. This report aggregates 100 "
        "parent problems; it does not claim that a bounded null result proves an "
        "unbounded conjecture.",
        "",
        f"- Parent problems: {len(rows)}",
        f"- Final parents: {summary['final_parent_count']}",
        f"- Statuses: `{json.dumps(summary['parent_status_counts'], sort_keys=True)}`",
        "",
        "| Problem | Domain | Scope | Status | Verification | Progress | Checked | Attempts |",
        "| --- | --- | --- | --- | --- | ---: | ---: | ---: |",
    ]
    for row in rows:
        title = str(row["title"]).replace("|", "\\|")
        lines.append(
            f"| `{row['problem_id']}` {title} | {row['domain']} | "
            f"`{row['claim_scope']}` | "
            f"`{row['aggregate_status']}` | `{row['verification_status']}` | "
            f"{row['completed_task_count']}/{row['task_count']} | "
            f"{row['checked_cases']} | {row['attempt_count']} |"
        )
    lines.append("")
    _atomic_write_text(path, "\n".join(lines))


def second_batch_status(
    *,
    campaign_dir: Path,
    registry: SecondBatchRegistry | None = None,
) -> dict[str, Any]:
    registry = registry or load_default_second_batch_registry()
    validate_second_batch_registry(registry)
    plan = _load_initialized_plan(campaign_dir)
    _validate_plan_registry_compatibility(plan, registry)
    coordinator = _coordinator(campaign_dir, plan, registry)
    coordinator.initialize()
    _reconcile_second_batch_stages(coordinator)
    sync = sync_second_batch_to_main(
        campaign_dir=campaign_dir,
        coordinator=coordinator,
    )
    artifacts = export_second_batch_status(
        campaign_dir=campaign_dir,
        coordinator=coordinator,
        main_sync=sync,
    )
    return {
        "schema_version": SECOND_BATCH_SCHEMA_VERSION,
        "summary": coordinator.summary(),
        "parent_rows": _parent_status_rows(coordinator),
        "main_sync": sync,
        "artifacts": artifacts,
    }


def _count_values(values: Iterable[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


__all__ = [
    "SECOND_BATCH_SCHEMA_VERSION",
    "SECOND_BATCH_ID",
    "SECOND_BATCH_COLLECTION",
    "SECOND_BATCH_EXPECTED_TOTAL",
    "SECOND_BATCH_DATABASE_FILE",
    "SECOND_BATCH_PLAN_FILE",
    "SECOND_BATCH_MODEL_AUDIT_FILE",
    "SECOND_BATCH_STATUS_CSV_FILE",
    "SECOND_BATCH_STATUS_JSONL_FILE",
    "SECOND_BATCH_STATUS_MARKDOWN_FILE",
    "SECOND_BATCH_SUMMARY_FILE",
    "SecondBatchConfigurationError",
    "SecondBatchExecutionError",
    "SecondBatchExecutorFamily",
    "SecondBatchRegistry",
    "load_default_second_batch_registry",
    "validate_second_batch_registry",
    "build_second_batch_plan",
    "initialize_second_batch",
    "run_second_batch",
    "record_second_batch_verification",
    "sync_second_batch_to_main",
    "export_second_batch_status",
    "second_batch_status",
]
