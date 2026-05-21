from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, ClassVar

from amra.orchestration.workstreams import utc_now_iso


class _StringEnum(str, Enum):
    @classmethod
    def coerce(cls, value: Any) -> Any:
        if isinstance(value, cls):
            return value
        normalized = str(value).strip().lower()
        for item in cls:
            if normalized in {item.value, item.name.lower()}:
                return item
        raise ValueError(f"Invalid {cls.__name__}: {value}")


class ResearchObjectType(_StringEnum):
    CONJECTURE = "conjecture"
    HYPOTHESIS = "hypothesis"
    EXPERIMENT = "experiment"
    DATASET = "dataset"
    ALGORITHM = "algorithm"
    MODEL = "model"
    BENCHMARK = "benchmark"
    COUNTEREXAMPLE = "counterexample"
    CONSTRUCTION = "construction"
    SECURITY_GAME = "security_game"
    SECURITY_ASSUMPTION = "security_assumption"
    ML_THEORY_CLAIM = "ml_theory_claim"
    NEGATIVE_RESULT = "negative_result"
    THEORY_NODE = "theory_node"


class ResearchObjectStatus(_StringEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    TESTING = "testing"
    EMPIRICALLY_SUPPORTED = "empirically_supported"
    MODEL_CALIBRATED = "model_calibrated"
    MODEL_VALIDATED = "model_validated"
    COUNTEREXAMPLE_FOUND = "counterexample_found"
    PROOF_CANDIDATE = "proof_candidate"
    LEAN_CANDIDATE = "lean_candidate"
    VERIFIED = "verified"
    REJECTED = "rejected"
    PARKED = "parked"
    FROZEN = "frozen"
    ARCHIVED = "archived"


class ResearchConfidence(_StringEnum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    THEOREM_GRADE = "theorem_grade"


def _string_list(values: list[Any] | None) -> list[str]:
    return [str(value) for value in values or []]


def _dict_value(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _optional_dict(value: Any) -> dict[str, Any] | None:
    return dict(value) if isinstance(value, dict) else None


@dataclass(slots=True)
class ResearchObjectRecord:
    object_id: str
    title: str
    object_type: ResearchObjectType = ResearchObjectType.HYPOTHESIS
    status: ResearchObjectStatus = ResearchObjectStatus.DRAFT
    statement: str = ""
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    domain: str = ""
    tags: list[str] = field(default_factory=list)
    confidence: ResearchConfidence = ResearchConfidence.UNKNOWN
    evidence_ids: list[str] = field(default_factory=list)
    source_ids: list[str] = field(default_factory=list)
    artifact_ids: list[str] = field(default_factory=list)
    blocked_by: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    _typed_records: ClassVar[dict[ResearchObjectType, type["ResearchObjectRecord"]]] = {}

    def __post_init__(self) -> None:
        self.object_type = ResearchObjectType.coerce(self.object_type)
        self.status = ResearchObjectStatus.coerce(self.status)
        self.confidence = ResearchConfidence.coerce(self.confidence)
        self.tags = _string_list(self.tags)
        self.evidence_ids = _string_list(self.evidence_ids)
        self.source_ids = _string_list(self.source_ids)
        self.artifact_ids = _string_list(self.artifact_ids)
        self.blocked_by = _string_list(self.blocked_by)
        self.metadata = _dict_value(self.metadata)
        if self.status == ResearchObjectStatus.VERIFIED and self.confidence != ResearchConfidence.THEOREM_GRADE:
            raise ValueError("verified research objects require theorem_grade confidence")

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ResearchObjectRecord":
        object_type = ResearchObjectType.coerce(payload.get("object_type", ResearchObjectType.HYPOTHESIS))
        target_cls = cls._typed_records.get(object_type, cls)
        if target_cls is not cls:
            return target_cls.from_dict(payload)
        return cls(**_base_kwargs(payload, object_type=object_type))

    def to_dict(self) -> dict[str, Any]:
        return _base_dict(self)


def _base_kwargs(payload: dict[str, Any], *, object_type: ResearchObjectType) -> dict[str, Any]:
    return {
        "object_id": str(payload["object_id"]),
        "title": str(payload.get("title", "")),
        "object_type": object_type,
        "status": ResearchObjectStatus.coerce(payload.get("status", ResearchObjectStatus.DRAFT)),
        "statement": str(payload.get("statement", "")),
        "created_at": str(payload.get("created_at") or utc_now_iso()),
        "updated_at": str(payload.get("updated_at") or utc_now_iso()),
        "domain": str(payload.get("domain", "")),
        "tags": _string_list(payload.get("tags")),
        "confidence": ResearchConfidence.coerce(payload.get("confidence", ResearchConfidence.UNKNOWN)),
        "evidence_ids": _string_list(payload.get("evidence_ids")),
        "source_ids": _string_list(payload.get("source_ids")),
        "artifact_ids": _string_list(payload.get("artifact_ids")),
        "blocked_by": _string_list(payload.get("blocked_by")),
        "metadata": _dict_value(payload.get("metadata")),
    }


def _base_dict(record: ResearchObjectRecord) -> dict[str, Any]:
    return {
        "object_id": record.object_id,
        "object_type": record.object_type.value,
        "title": record.title,
        "status": record.status.value,
        "created_at": record.created_at,
        "updated_at": record.updated_at,
        "domain": record.domain,
        "tags": list(record.tags),
        "statement": record.statement,
        "confidence": record.confidence.value,
        "evidence_ids": list(record.evidence_ids),
        "source_ids": list(record.source_ids),
        "artifact_ids": list(record.artifact_ids),
        "blocked_by": list(record.blocked_by),
        "metadata": dict(record.metadata),
    }


@dataclass(slots=True)
class ConjectureRecord(ResearchObjectRecord):
    object_type: ResearchObjectType = ResearchObjectType.CONJECTURE
    formal_statement: str | None = None
    informal_statement: str = ""
    scope: str = ""
    known_cases: list[str] = field(default_factory=list)
    excluded_cases: list[str] = field(default_factory=list)
    counterexample_search: list[str] = field(default_factory=list)
    novelty_report: dict[str, Any] | None = None
    promotion_target: str = "proof_task"

    def __post_init__(self) -> None:
        self.object_type = ResearchObjectType.CONJECTURE
        ResearchObjectRecord.__post_init__(self)
        self.known_cases = _string_list(self.known_cases)
        self.excluded_cases = _string_list(self.excluded_cases)
        self.counterexample_search = _string_list(self.counterexample_search)
        self.novelty_report = _optional_dict(self.novelty_report)
        if not self.informal_statement and self.statement:
            self.informal_statement = self.statement

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ConjectureRecord":
        return cls(
            **_base_kwargs(payload, object_type=ResearchObjectType.CONJECTURE),
            formal_statement=payload.get("formal_statement"),
            informal_statement=str(payload.get("informal_statement", "")),
            scope=str(payload.get("scope", "")),
            known_cases=_string_list(payload.get("known_cases")),
            excluded_cases=_string_list(payload.get("excluded_cases")),
            counterexample_search=_string_list(payload.get("counterexample_search")),
            novelty_report=_optional_dict(payload.get("novelty_report")),
            promotion_target=str(payload.get("promotion_target", "proof_task")),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = _base_dict(self)
        payload.update(
            {
                "formal_statement": self.formal_statement,
                "informal_statement": self.informal_statement,
                "scope": self.scope,
                "known_cases": list(self.known_cases),
                "excluded_cases": list(self.excluded_cases),
                "counterexample_search": list(self.counterexample_search),
                "novelty_report": self.novelty_report,
                "promotion_target": self.promotion_target,
            }
        )
        return payload


@dataclass(slots=True)
class ExperimentRecord(ResearchObjectRecord):
    object_type: ResearchObjectType = ResearchObjectType.EXPERIMENT
    question: str = ""
    method: str = ""
    inputs: list[str] = field(default_factory=list)
    parameters: dict[str, Any] = field(default_factory=dict)
    seed: int | str | None = None
    budget: dict[str, Any] = field(default_factory=dict)
    environment: dict[str, Any] = field(default_factory=dict)
    command: str = ""
    outputs: list[str] = field(default_factory=list)
    result_summary: str = ""
    rerun_status: str = "not_rerun"
    reproducibility_report: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        self.object_type = ResearchObjectType.EXPERIMENT
        ResearchObjectRecord.__post_init__(self)
        self.inputs = _string_list(self.inputs)
        self.parameters = _dict_value(self.parameters)
        self.budget = _dict_value(self.budget)
        self.environment = _dict_value(self.environment)
        self.outputs = _string_list(self.outputs)
        self.reproducibility_report = _optional_dict(self.reproducibility_report)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ExperimentRecord":
        return cls(
            **_base_kwargs(payload, object_type=ResearchObjectType.EXPERIMENT),
            question=str(payload.get("question", "")),
            method=str(payload.get("method", "")),
            inputs=_string_list(payload.get("inputs")),
            parameters=_dict_value(payload.get("parameters")),
            seed=payload.get("seed"),
            budget=_dict_value(payload.get("budget")),
            environment=_dict_value(payload.get("environment")),
            command=str(payload.get("command", "")),
            outputs=_string_list(payload.get("outputs")),
            result_summary=str(payload.get("result_summary", "")),
            rerun_status=str(payload.get("rerun_status", "not_rerun")),
            reproducibility_report=_optional_dict(payload.get("reproducibility_report")),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = _base_dict(self)
        payload.update(
            {
                "question": self.question,
                "method": self.method,
                "inputs": list(self.inputs),
                "parameters": dict(self.parameters),
                "seed": self.seed,
                "budget": dict(self.budget),
                "environment": dict(self.environment),
                "command": self.command,
                "outputs": list(self.outputs),
                "result_summary": self.result_summary,
                "rerun_status": self.rerun_status,
                "reproducibility_report": self.reproducibility_report,
            }
        )
        return payload


@dataclass(slots=True)
class CounterexampleRecord(ResearchObjectRecord):
    object_type: ResearchObjectType = ResearchObjectType.COUNTEREXAMPLE
    target_conjecture_id: str = ""
    assignment: dict[str, Any] = field(default_factory=dict)
    observed_value: dict[str, Any] = field(default_factory=dict)
    violation_summary: str = ""
    search_space: dict[str, Any] = field(default_factory=dict)
    predicate: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.object_type = ResearchObjectType.COUNTEREXAMPLE
        ResearchObjectRecord.__post_init__(self)
        self.assignment = _dict_value(self.assignment)
        self.observed_value = _dict_value(self.observed_value)
        self.search_space = _dict_value(self.search_space)
        self.predicate = _dict_value(self.predicate)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "CounterexampleRecord":
        return cls(
            **_base_kwargs(payload, object_type=ResearchObjectType.COUNTEREXAMPLE),
            target_conjecture_id=str(payload.get("target_conjecture_id", "")),
            assignment=_dict_value(payload.get("assignment")),
            observed_value=_dict_value(payload.get("observed_value")),
            violation_summary=str(payload.get("violation_summary", "")),
            search_space=_dict_value(payload.get("search_space")),
            predicate=_dict_value(payload.get("predicate")),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = _base_dict(self)
        payload.update(
            {
                "target_conjecture_id": self.target_conjecture_id,
                "assignment": dict(self.assignment),
                "observed_value": dict(self.observed_value),
                "violation_summary": self.violation_summary,
                "search_space": dict(self.search_space),
                "predicate": dict(self.predicate),
            }
        )
        return payload


@dataclass(slots=True)
class ConstructionRecord(ResearchObjectRecord):
    object_type: ResearchObjectType = ResearchObjectType.CONSTRUCTION
    target_conjecture_id: str = ""
    method: str = "fixture_witness"
    parameters: dict[str, Any] = field(default_factory=dict)
    witness: dict[str, Any] = field(default_factory=dict)
    verifies: bool = False

    def __post_init__(self) -> None:
        self.object_type = ResearchObjectType.CONSTRUCTION
        ResearchObjectRecord.__post_init__(self)
        self.parameters = _dict_value(self.parameters)
        self.witness = _dict_value(self.witness)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ConstructionRecord":
        return cls(
            **_base_kwargs(payload, object_type=ResearchObjectType.CONSTRUCTION),
            target_conjecture_id=str(payload.get("target_conjecture_id", "")),
            method=str(payload.get("method", "fixture_witness")),
            parameters=_dict_value(payload.get("parameters")),
            witness=_dict_value(payload.get("witness")),
            verifies=bool(payload.get("verifies")),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = _base_dict(self)
        payload.update(
            {
                "target_conjecture_id": self.target_conjecture_id,
                "method": self.method,
                "parameters": dict(self.parameters),
                "witness": dict(self.witness),
                "verifies": self.verifies,
            }
        )
        return payload


@dataclass(slots=True)
class NegativeResultRecord(ResearchObjectRecord):
    object_type: ResearchObjectType = ResearchObjectType.NEGATIVE_RESULT
    target_object_id: str = ""
    refuted_by: list[str] = field(default_factory=list)
    failure_mode: str = "counterexample"
    search_bound: dict[str, Any] = field(default_factory=dict)
    result_summary: str = ""

    def __post_init__(self) -> None:
        self.object_type = ResearchObjectType.NEGATIVE_RESULT
        ResearchObjectRecord.__post_init__(self)
        self.refuted_by = _string_list(self.refuted_by)
        self.search_bound = _dict_value(self.search_bound)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "NegativeResultRecord":
        return cls(
            **_base_kwargs(payload, object_type=ResearchObjectType.NEGATIVE_RESULT),
            target_object_id=str(payload.get("target_object_id", "")),
            refuted_by=_string_list(payload.get("refuted_by")),
            failure_mode=str(payload.get("failure_mode", "counterexample")),
            search_bound=_dict_value(payload.get("search_bound")),
            result_summary=str(payload.get("result_summary", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = _base_dict(self)
        payload.update(
            {
                "target_object_id": self.target_object_id,
                "refuted_by": list(self.refuted_by),
                "failure_mode": self.failure_mode,
                "search_bound": dict(self.search_bound),
                "result_summary": self.result_summary,
            }
        )
        return payload


@dataclass(slots=True)
class AlgorithmRecord(ResearchObjectRecord):
    object_type: ResearchObjectType = ResearchObjectType.ALGORITHM
    problem_spec: str = ""
    baseline_ids: list[str] = field(default_factory=list)
    candidate_ids: list[str] = field(default_factory=list)
    complexity_claims: list[str] = field(default_factory=list)
    benchmark_ids: list[str] = field(default_factory=list)
    profiling_reports: list[str] = field(default_factory=list)
    ablation_reports: list[str] = field(default_factory=list)
    regression_risks: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.object_type = ResearchObjectType.ALGORITHM
        ResearchObjectRecord.__post_init__(self)
        self.baseline_ids = _string_list(self.baseline_ids)
        self.candidate_ids = _string_list(self.candidate_ids)
        self.complexity_claims = _string_list(self.complexity_claims)
        self.benchmark_ids = _string_list(self.benchmark_ids)
        self.profiling_reports = _string_list(self.profiling_reports)
        self.ablation_reports = _string_list(self.ablation_reports)
        self.regression_risks = _string_list(self.regression_risks)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AlgorithmRecord":
        return cls(
            **_base_kwargs(payload, object_type=ResearchObjectType.ALGORITHM),
            problem_spec=str(payload.get("problem_spec", "")),
            baseline_ids=_string_list(payload.get("baseline_ids")),
            candidate_ids=_string_list(payload.get("candidate_ids")),
            complexity_claims=_string_list(payload.get("complexity_claims")),
            benchmark_ids=_string_list(payload.get("benchmark_ids")),
            profiling_reports=_string_list(payload.get("profiling_reports")),
            ablation_reports=_string_list(payload.get("ablation_reports")),
            regression_risks=_string_list(payload.get("regression_risks")),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = _base_dict(self)
        payload.update(
            {
                "problem_spec": self.problem_spec,
                "baseline_ids": list(self.baseline_ids),
                "candidate_ids": list(self.candidate_ids),
                "complexity_claims": list(self.complexity_claims),
                "benchmark_ids": list(self.benchmark_ids),
                "profiling_reports": list(self.profiling_reports),
                "ablation_reports": list(self.ablation_reports),
                "regression_risks": list(self.regression_risks),
            }
        )
        return payload


@dataclass(slots=True)
class ModelRecord(ResearchObjectRecord):
    object_type: ResearchObjectType = ResearchObjectType.MODEL
    application_domain: str = ""
    variables: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    units: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    calibration_data: list[str] = field(default_factory=list)
    validation_data: list[str] = field(default_factory=list)
    sensitivity_reports: list[str] = field(default_factory=list)
    validity_range: str = ""
    validity_ranges: list[dict[str, Any]] = field(default_factory=list)
    known_failure_modes: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.object_type = ResearchObjectType.MODEL
        ResearchObjectRecord.__post_init__(self)
        self.variables = _string_list(self.variables)
        self.assumptions = _string_list(self.assumptions)
        self.units = _dict_value(self.units)
        self.parameters = _dict_value(self.parameters)
        self.calibration_data = _string_list(self.calibration_data)
        self.validation_data = _string_list(self.validation_data)
        self.sensitivity_reports = _string_list(self.sensitivity_reports)
        self.validity_ranges = [dict(item) for item in self.validity_ranges if isinstance(item, dict)]
        self.known_failure_modes = _string_list(self.known_failure_modes)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ModelRecord":
        return cls(
            **_base_kwargs(payload, object_type=ResearchObjectType.MODEL),
            application_domain=str(payload.get("application_domain", "")),
            variables=_string_list(payload.get("variables")),
            assumptions=_string_list(payload.get("assumptions")),
            units=_dict_value(payload.get("units")),
            parameters=_dict_value(payload.get("parameters")),
            calibration_data=_string_list(payload.get("calibration_data")),
            validation_data=_string_list(payload.get("validation_data")),
            sensitivity_reports=_string_list(payload.get("sensitivity_reports")),
            validity_range=str(payload.get("validity_range", "")),
            validity_ranges=[
                dict(item)
                for item in payload.get("validity_ranges", [])
                if isinstance(item, dict)
            ],
            known_failure_modes=_string_list(payload.get("known_failure_modes")),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = _base_dict(self)
        payload.update(
            {
                "application_domain": self.application_domain,
                "variables": list(self.variables),
                "assumptions": list(self.assumptions),
                "units": dict(self.units),
                "parameters": dict(self.parameters),
                "calibration_data": list(self.calibration_data),
                "validation_data": list(self.validation_data),
                "sensitivity_reports": list(self.sensitivity_reports),
                "validity_range": self.validity_range,
                "validity_ranges": [dict(item) for item in self.validity_ranges],
                "known_failure_modes": list(self.known_failure_modes),
            }
        )
        return payload


@dataclass(slots=True)
class SecurityGameRecord(ResearchObjectRecord):
    object_type: ResearchObjectType = ResearchObjectType.SECURITY_GAME
    scheme: str = ""
    adversary_model: str = ""
    oracle_access: list[str] = field(default_factory=list)
    winning_condition: str = ""
    assumptions: list[str] = field(default_factory=list)
    reductions: list[str] = field(default_factory=list)
    attack_attempts: list[str] = field(default_factory=list)
    security_status: str = "unstated"

    def __post_init__(self) -> None:
        self.object_type = ResearchObjectType.SECURITY_GAME
        ResearchObjectRecord.__post_init__(self)
        self.oracle_access = _string_list(self.oracle_access)
        self.assumptions = _string_list(self.assumptions)
        self.reductions = _string_list(self.reductions)
        self.attack_attempts = _string_list(self.attack_attempts)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SecurityGameRecord":
        return cls(
            **_base_kwargs(payload, object_type=ResearchObjectType.SECURITY_GAME),
            scheme=str(payload.get("scheme", "")),
            adversary_model=str(payload.get("adversary_model", "")),
            oracle_access=_string_list(payload.get("oracle_access")),
            winning_condition=str(payload.get("winning_condition", "")),
            assumptions=_string_list(payload.get("assumptions")),
            reductions=_string_list(payload.get("reductions")),
            attack_attempts=_string_list(payload.get("attack_attempts")),
            security_status=str(payload.get("security_status", "unstated")),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = _base_dict(self)
        payload.update(
            {
                "scheme": self.scheme,
                "adversary_model": self.adversary_model,
                "oracle_access": list(self.oracle_access),
                "winning_condition": self.winning_condition,
                "assumptions": list(self.assumptions),
                "reductions": list(self.reductions),
                "attack_attempts": list(self.attack_attempts),
                "security_status": self.security_status,
            }
        )
        return payload


@dataclass(slots=True)
class SecurityAssumptionRecord(ResearchObjectRecord):
    object_type: ResearchObjectType = ResearchObjectType.SECURITY_ASSUMPTION
    assumption_family: str = ""
    hardness_parameters: dict[str, Any] = field(default_factory=dict)
    related_game_ids: list[str] = field(default_factory=list)
    reduction_ids: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.object_type = ResearchObjectType.SECURITY_ASSUMPTION
        ResearchObjectRecord.__post_init__(self)
        self.hardness_parameters = _dict_value(self.hardness_parameters)
        self.related_game_ids = _string_list(self.related_game_ids)
        self.reduction_ids = _string_list(self.reduction_ids)
        self.limitation_notes = _string_list(self.limitation_notes)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SecurityAssumptionRecord":
        return cls(
            **_base_kwargs(payload, object_type=ResearchObjectType.SECURITY_ASSUMPTION),
            assumption_family=str(payload.get("assumption_family") or payload.get("family") or ""),
            hardness_parameters=_dict_value(payload.get("hardness_parameters")),
            related_game_ids=_string_list(payload.get("related_game_ids")),
            reduction_ids=_string_list(payload.get("reduction_ids")),
            limitation_notes=_string_list(payload.get("limitation_notes")),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = _base_dict(self)
        payload.update(
            {
                "assumption_family": self.assumption_family,
                "hardness_parameters": dict(self.hardness_parameters),
                "related_game_ids": list(self.related_game_ids),
                "reduction_ids": list(self.reduction_ids),
                "limitation_notes": list(self.limitation_notes),
            }
        )
        return payload


@dataclass(slots=True)
class MLTheoryClaimRecord(ResearchObjectRecord):
    object_type: ResearchObjectType = ResearchObjectType.ML_THEORY_CLAIM
    claim_kind: str = "empirical_observation"
    training_setup: dict[str, Any] = field(default_factory=dict)
    dataset_ids: list[str] = field(default_factory=list)
    metric_ids: list[str] = field(default_factory=list)
    theoretical_statement: str = ""
    empirical_support: list[str] = field(default_factory=list)
    known_gaps: list[str] = field(default_factory=list)
    promotion_target: str = "conjecture"

    def __post_init__(self) -> None:
        self.object_type = ResearchObjectType.ML_THEORY_CLAIM
        ResearchObjectRecord.__post_init__(self)
        self.training_setup = _dict_value(self.training_setup)
        self.dataset_ids = _string_list(self.dataset_ids)
        self.metric_ids = _string_list(self.metric_ids)
        self.empirical_support = _string_list(self.empirical_support)
        self.known_gaps = _string_list(self.known_gaps)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MLTheoryClaimRecord":
        return cls(
            **_base_kwargs(payload, object_type=ResearchObjectType.ML_THEORY_CLAIM),
            claim_kind=str(payload.get("claim_kind", "empirical_observation")),
            training_setup=_dict_value(payload.get("training_setup")),
            dataset_ids=_string_list(payload.get("dataset_ids")),
            metric_ids=_string_list(payload.get("metric_ids")),
            theoretical_statement=str(payload.get("theoretical_statement", "")),
            empirical_support=_string_list(payload.get("empirical_support")),
            known_gaps=_string_list(payload.get("known_gaps")),
            promotion_target=str(payload.get("promotion_target", "conjecture")),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = _base_dict(self)
        payload.update(
            {
                "claim_kind": self.claim_kind,
                "training_setup": dict(self.training_setup),
                "dataset_ids": list(self.dataset_ids),
                "metric_ids": list(self.metric_ids),
                "theoretical_statement": self.theoretical_statement,
                "empirical_support": list(self.empirical_support),
                "known_gaps": list(self.known_gaps),
                "promotion_target": self.promotion_target,
            }
        )
        return payload


ResearchObjectRecord._typed_records = {
    ResearchObjectType.CONJECTURE: ConjectureRecord,
    ResearchObjectType.COUNTEREXAMPLE: CounterexampleRecord,
    ResearchObjectType.CONSTRUCTION: ConstructionRecord,
    ResearchObjectType.EXPERIMENT: ExperimentRecord,
    ResearchObjectType.ALGORITHM: AlgorithmRecord,
    ResearchObjectType.MODEL: ModelRecord,
    ResearchObjectType.SECURITY_GAME: SecurityGameRecord,
    ResearchObjectType.SECURITY_ASSUMPTION: SecurityAssumptionRecord,
    ResearchObjectType.ML_THEORY_CLAIM: MLTheoryClaimRecord,
    ResearchObjectType.NEGATIVE_RESULT: NegativeResultRecord,
}
