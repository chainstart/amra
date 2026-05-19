"""Canonical AMRA proof-loop routing contracts."""

from __future__ import annotations

import importlib
import re
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping


SCHEMA_VERSION = "amra.proof_loop.result.v1"


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def _has_value(parameters: Mapping[str, Any], key: str) -> bool:
    value = parameters.get(key)
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


@dataclass(frozen=True, slots=True)
class ProofRunnerContract:
    """Stable route metadata for a proof-loop runner."""

    route: str
    runner_module: str
    runner_class: str
    method_name: str
    required_parameters: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    description: str = ""

    @property
    def adapter_id(self) -> str:
        return f"{self.runner_module}:{self.runner_class}.{self.method_name}"

    def accepts(self, parameters: Mapping[str, Any]) -> bool:
        return all(_has_value(parameters, key) for key in self.required_parameters)


@dataclass(frozen=True, slots=True)
class ProofRunRequest:
    """Canonical request envelope for proof-loop adapters."""

    repo_root: Path
    route: str | None = None
    parameters: Mapping[str, Any] = field(default_factory=dict)
    request_id: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_kwargs(
        cls,
        *,
        repo_root: Path,
        route: str | None = None,
        request_id: str = "",
        metadata: Mapping[str, Any] | None = None,
        **parameters: Any,
    ) -> "ProofRunRequest":
        return cls(
            repo_root=repo_root,
            route=route,
            request_id=request_id,
            metadata=dict(metadata or {}),
            parameters=dict(parameters),
        )


@dataclass(frozen=True, slots=True)
class ProofRunResult:
    """Canonical result envelope returned by proof-loop adapters."""

    route: str
    canonical_status: str
    raw_status: str
    report: Mapping[str, Any]
    metadata: Mapping[str, Any]
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "route": self.route,
            "canonical_status": self.canonical_status,
            "raw_status": self.raw_status,
            "report": dict(self.report),
            "metadata": dict(self.metadata),
        }


RunnerFactory = Callable[[ProofRunnerContract, Path], Any]


def _default_runner_factory(contract: ProofRunnerContract, repo_root: Path) -> Any:
    module = importlib.import_module(contract.runner_module)
    runner_class = getattr(module, contract.runner_class)
    return runner_class(repo_root=repo_root)


def _status_token(value: Any) -> str:
    return _normalize_key(str(value or ""))


def _extract_raw_status(report: Mapping[str, Any]) -> str:
    for key in ("status", "outcome", "stop_reason", "last_backend_status", "backend_status"):
        if _status_token(report.get(key)):
            return _status_token(report.get(key))

    final_observation = report.get("final_observation")
    if isinstance(final_observation, Mapping):
        for key in ("status", "stop_reason", "backend_status"):
            if _status_token(final_observation.get(key)):
                return _status_token(final_observation.get(key))

    best_audit = report.get("best_audit")
    if isinstance(best_audit, Mapping) and best_audit.get("verified") is True:
        return "verified"

    return "unknown"


def normalize_proof_status(status: Any = "", report: Mapping[str, Any] | None = None) -> str:
    """Collapse legacy proof-loop statuses into canonical AMRA buckets."""

    token = _status_token(status)
    if not token and report is not None:
        token = _extract_raw_status(report)

    verified = {
        "verified",
        "converged",
        "passed",
        "success",
        "succeeded",
        "closed",
        "closed_candidate",
        "final_target_verified",
        "root_goal_verified",
    }
    completed = {"completed", "complete", "done"}
    partial = {
        "partial",
        "proof_candidate",
        "rigorous",
        "heuristic",
        "exhausted",
        "rounds_exhausted",
        "time_budget_exhausted",
        "stalled",
    }
    blocked = {
        "blocked",
        "deferred",
        "needs_target",
        "missing_project",
        "no_ready_goals",
        "not_started",
        "not_run",
        "system_guard_blocked",
        "source_grounding_failed",
        "unavailable",
        "unsupported",
    }
    failed = {"failed", "failure", "error", "timeout", "cancelled", "canceled", "aborted"}
    skipped = {"skipped", "dry_run"}
    running = {"running", "in_progress"}

    if token in verified:
        return "verified"
    if token in completed:
        return "completed"
    if token in partial:
        return "partial"
    if token in blocked:
        return "blocked"
    if token in failed:
        return "failed"
    if token in skipped:
        return "skipped"
    if token in running:
        return "running"
    return "unknown"


DEFAULT_PROOF_RUNNER_CONTRACTS: tuple[ProofRunnerContract, ...] = (
    ProofRunnerContract(
        route="proof_lab",
        runner_module="ara_math.proof_lab",
        runner_class="AIProofLabRunner",
        method_name="run",
        required_parameters=("statement",),
        aliases=("proof-lab", "ai_proof_lab", "ai-proof-lab", "run-ai-proof-lab"),
        description="Clean-room natural-language proof route discovery.",
    ),
    ProofRunnerContract(
        route="proof_search",
        runner_module="ara_math.proof_search",
        runner_class="ProofSearchRunner",
        method_name="run_project",
        required_parameters=("project_dir", "orchestrator"),
        aliases=("proof-search", "search", "run-proof-search"),
        description="Project proof-search loop over generated proof plans and Lean assets.",
    ),
    ProofRunnerContract(
        route="math_attack",
        runner_module="ara_math.math_attack",
        runner_class="MathAttackRunner",
        method_name="run",
        required_parameters=("project_dir",),
        aliases=("math-attack", "attack", "run-math-attack"),
        description="Math-only iterative attack loop for a selected target.",
    ),
    ProofRunnerContract(
        route="campaign_loop",
        runner_module="ara_math.campaign_loop",
        runner_class="CampaignLoopRunner",
        method_name="run",
        required_parameters=("statement",),
        aliases=("campaign-loop", "run-campaign-loop"),
        description="Outer proof-lab and Lean formalizer campaign loop.",
    ),
    ProofRunnerContract(
        route="goal_campaign",
        runner_module="ara_math.goal_campaign",
        runner_class="GoalDrivenCampaignRunner",
        method_name="run",
        required_parameters=("manifest_path",),
        aliases=("goal-campaign", "goal_campaigns", "run-goal-campaign"),
        description="Root-goal driven campaign loop over dependent obligations.",
    ),
    ProofRunnerContract(
        route="closure",
        runner_module="ara_math.closure",
        runner_class="ClosureProverRunner",
        method_name="run",
        required_parameters=("project_dir", "orchestrator"),
        aliases=("closure-prover", "closure_prover", "run-closure-prover"),
        description="Strict Lean-first closure loop for an explicit theorem target.",
    ),
    ProofRunnerContract(
        route="focused_attack",
        runner_module="ara_math.focused_attack",
        runner_class="FocusedLeanAttackAgent",
        method_name="run",
        required_parameters=("workspace", "attack_targets"),
        aliases=("focused-attack", "focused_lean_attack", "focused-lean-attack", "run-focused-lean-attack"),
        description="Host-enforced focused Lean attack loop for exact declarations.",
    ),
)


class ProofLoopRegistry:
    """Route AMRA proof-loop requests to canonical adapter contracts."""

    def __init__(
        self,
        contracts: tuple[ProofRunnerContract, ...] = DEFAULT_PROOF_RUNNER_CONTRACTS,
        *,
        runner_factory: RunnerFactory | None = None,
    ) -> None:
        self._contracts = {contract.route: contract for contract in contracts}
        self._aliases: dict[str, str] = {}
        for contract in contracts:
            for name in (contract.route, *contract.aliases):
                self._aliases[_normalize_key(name)] = contract.route
        self._runner_factory = runner_factory or _default_runner_factory

    def contracts(self) -> tuple[ProofRunnerContract, ...]:
        return tuple(self._contracts.values())

    def resolve_route(self, route: str) -> ProofRunnerContract:
        key = _normalize_key(route)
        canonical = self._aliases.get(key)
        if canonical is None:
            known = ", ".join(sorted(self._contracts))
            raise KeyError(f"Unknown proof-loop route `{route}`. Known routes: {known}")
        return self._contracts[canonical]

    def select_route(self, parameters: Mapping[str, Any], route: str | None = None) -> ProofRunnerContract:
        if route:
            contract = self.resolve_route(route)
            missing = [key for key in contract.required_parameters if not _has_value(parameters, key)]
            if missing:
                missing_text = ", ".join(missing)
                raise ValueError(f"Route `{contract.route}` is missing required parameter(s): {missing_text}")
            return contract

        if _has_value(parameters, "manifest_path"):
            return self._contracts["goal_campaign"]
        if _has_value(parameters, "attack_targets") and _has_value(parameters, "workspace"):
            return self._contracts["focused_attack"]
        if (
            _has_value(parameters, "target_theorem")
            and _has_value(parameters, "project_dir")
            and _has_value(parameters, "orchestrator")
        ):
            return self._contracts["closure"]
        if _has_value(parameters, "orchestrator") and _has_value(parameters, "project_dir"):
            return self._contracts["proof_search"]
        if _has_value(parameters, "target") and _has_value(parameters, "project_dir"):
            return self._contracts["math_attack"]
        if _has_value(parameters, "workspace") or _has_value(parameters, "final_target_theorem"):
            if _has_value(parameters, "statement"):
                return self._contracts["campaign_loop"]
        if _has_value(parameters, "statement"):
            return self._contracts["proof_lab"]

        raise ValueError("Could not select a proof-loop route from the supplied parameters.")

    def run(self, request: ProofRunRequest) -> ProofRunResult:
        parameters = dict(request.parameters)
        contract = self.select_route(parameters, request.route)
        if contract.route == "math_attack":
            parameters.setdefault("target", "")
        elif contract.route == "closure":
            parameters.setdefault("target_theorem", None)
        runner = self._runner_factory(contract, request.repo_root)
        method = getattr(runner, contract.method_name)
        raw_report = method(**parameters)
        report = dict(raw_report or {})
        raw_status = _extract_raw_status(report)
        canonical_status = normalize_proof_status(raw_status, report)
        metadata = {
            "schema_version": SCHEMA_VERSION,
            "generated_at": _utc_now_iso(),
            "request_id": request.request_id,
            "route": contract.route,
            "adapter_id": contract.adapter_id,
            "runner_module": contract.runner_module,
            "runner_class": contract.runner_class,
            "method_name": contract.method_name,
            "repo_root": str(request.repo_root),
            "raw_status": raw_status,
            "canonical_status": canonical_status,
            **dict(request.metadata),
        }
        return ProofRunResult(
            route=contract.route,
            canonical_status=canonical_status,
            raw_status=raw_status,
            report=report,
            metadata=metadata,
        )


def default_proof_loop_registry() -> ProofLoopRegistry:
    return ProofLoopRegistry()


def select_proof_loop_route(
    *,
    route: str | None = None,
    registry: ProofLoopRegistry | None = None,
    **parameters: Any,
) -> ProofRunnerContract:
    return (registry or default_proof_loop_registry()).select_route(parameters, route)


def run_proof_loop(
    route: str | None = None,
    *,
    repo_root: Path,
    registry: ProofLoopRegistry | None = None,
    request_id: str = "",
    metadata: Mapping[str, Any] | None = None,
    **parameters: Any,
) -> ProofRunResult:
    request = ProofRunRequest.from_kwargs(
        repo_root=repo_root,
        route=route,
        request_id=request_id,
        metadata=metadata,
        **parameters,
    )
    return (registry or default_proof_loop_registry()).run(request)


__all__ = [
    "DEFAULT_PROOF_RUNNER_CONTRACTS",
    "ProofLoopRegistry",
    "ProofRunRequest",
    "ProofRunResult",
    "ProofRunnerContract",
    "default_proof_loop_registry",
    "normalize_proof_status",
    "run_proof_loop",
    "select_proof_loop_route",
]
