from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


MODEL_SPEC_SCHEMA_VERSION = "amra.model_spec.v1"


def _dict_value(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _list_value(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    items = value if isinstance(value, list) else [value]
    return [str(item) for item in items]


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def slug(value: str, *, fallback: str = "model") -> str:
    normalized = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    parts = [part for part in normalized.split("-") if part]
    return "-".join(parts) or fallback


@dataclass(slots=True)
class ModelVariable:
    name: str
    unit: str
    role: str = "input"
    description: str = ""
    symbol: str = ""
    valid_range: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ModelVariable":
        return cls(
            name=str(payload["name"]),
            unit=str(payload.get("unit") or payload.get("units") or ""),
            role=str(payload.get("role") or "input"),
            description=str(payload.get("description") or ""),
            symbol=str(payload.get("symbol") or ""),
            valid_range=_dict_value(payload.get("valid_range") or payload.get("range")),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "unit": self.unit,
            "role": self.role,
            "description": self.description,
            "symbol": self.symbol,
            "valid_range": dict(self.valid_range),
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ModelAssumption:
    assumption_id: str
    statement: str
    scope: str = "model"
    required: bool = True
    testable: bool = False
    evidence_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any], *, index: int = 0) -> "ModelAssumption":
        statement = str(payload.get("statement") or payload.get("description") or "")
        return cls(
            assumption_id=str(payload.get("assumption_id") or payload.get("id") or f"assumption-{index + 1}"),
            statement=statement,
            scope=str(payload.get("scope") or "model"),
            required=bool(payload.get("required", True)),
            testable=bool(payload.get("testable", False)),
            evidence_ids=_string_list(payload.get("evidence_ids")),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "assumption_id": self.assumption_id,
            "statement": self.statement,
            "scope": self.scope,
            "required": self.required,
            "testable": self.testable,
            "evidence_ids": list(self.evidence_ids),
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ModelParameter:
    name: str
    value: Any = None
    unit: str = ""
    source: str = ""
    calibration_method: str = ""
    uncertainty: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ModelParameter":
        return cls(
            name=str(payload["name"]),
            value=payload.get("value"),
            unit=str(payload.get("unit") or payload.get("units") or ""),
            source=str(payload.get("source") or ""),
            calibration_method=str(payload.get("calibration_method") or payload.get("method") or ""),
            uncertainty=_dict_value(payload.get("uncertainty")),
            metadata=_dict_value(payload.get("metadata")),
        )

    @property
    def traceable(self) -> bool:
        return bool(self.source or self.calibration_method)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "source": self.source,
            "calibration_method": self.calibration_method,
            "uncertainty": dict(self.uncertainty),
            "metadata": dict(self.metadata),
            "traceable": self.traceable,
        }


@dataclass(slots=True)
class ValidityRange:
    variable: str
    min_value: float | None = None
    max_value: float | None = None
    unit: str = ""
    notes: str = ""

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ValidityRange":
        return cls(
            variable=str(payload.get("variable") or payload.get("name") or ""),
            min_value=_number(payload.get("min", payload.get("min_value"))),
            max_value=_number(payload.get("max", payload.get("max_value"))),
            unit=str(payload.get("unit") or payload.get("units") or ""),
            notes=str(payload.get("notes") or ""),
        )

    def contains(self, value: Any) -> bool:
        number = _number(value)
        if number is None:
            return True
        if self.min_value is not None and number < self.min_value:
            return False
        if self.max_value is not None and number > self.max_value:
            return False
        return True

    def to_dict(self) -> dict[str, Any]:
        return {
            "variable": self.variable,
            "min": self.min_value,
            "max": self.max_value,
            "unit": self.unit,
            "notes": self.notes,
        }


@dataclass(slots=True)
class AppliedModelSpec:
    object_id: str
    title: str
    statement: str = ""
    application_domain: str = ""
    domain: str = ""
    tags: list[str] = field(default_factory=list)
    variables: list[ModelVariable] = field(default_factory=list)
    assumptions: list[ModelAssumption] = field(default_factory=list)
    parameters: list[ModelParameter] = field(default_factory=list)
    validity_ranges: list[ValidityRange] = field(default_factory=list)
    equations: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AppliedModelSpec":
        object_id = str(payload.get("object_id") or payload.get("id") or slug(str(payload.get("title") or "model")))
        variables = [ModelVariable.from_dict(item) for item in _list_value(payload.get("variables")) if isinstance(item, dict)]
        validity_payload = payload.get("validity_ranges") or payload.get("validity_range")
        validity_ranges = [
            ValidityRange.from_dict(item)
            for item in _list_value(validity_payload)
            if isinstance(item, dict)
        ]
        if not validity_ranges:
            validity_ranges = [
                ValidityRange.from_dict({"variable": item.name, **item.valid_range})
                for item in variables
                if item.valid_range
            ]
        return cls(
            object_id=object_id,
            title=str(payload.get("title") or object_id),
            statement=str(payload.get("statement") or payload.get("model_statement") or ""),
            application_domain=str(payload.get("application_domain") or payload.get("domain") or ""),
            domain=str(payload.get("domain") or payload.get("application_domain") or ""),
            tags=_string_list(payload.get("tags")),
            variables=variables,
            assumptions=[
                ModelAssumption.from_dict(item, index=index)
                for index, item in enumerate(_list_value(payload.get("assumptions")))
                if isinstance(item, dict)
            ],
            parameters=[
                ModelParameter.from_dict(item)
                for item in _list_value(payload.get("parameters"))
                if isinstance(item, dict)
            ],
            validity_ranges=validity_ranges,
            equations=_string_list(payload.get("equations")),
            outputs=_string_list(payload.get("outputs")),
            metadata=_dict_value(payload.get("metadata")),
        )

    @property
    def units(self) -> dict[str, str]:
        return {item.name: item.unit for item in self.variables}

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": MODEL_SPEC_SCHEMA_VERSION,
            "object_id": self.object_id,
            "object_type": "model",
            "title": self.title,
            "statement": self.statement,
            "application_domain": self.application_domain,
            "domain": self.domain,
            "tags": list(self.tags),
            "variables": [item.to_dict() for item in self.variables],
            "units": dict(self.units),
            "assumptions": [item.to_dict() for item in self.assumptions],
            "parameters": [item.to_dict() for item in self.parameters],
            "validity_ranges": [item.to_dict() for item in self.validity_ranges],
            "equations": list(self.equations),
            "outputs": list(self.outputs),
            "metadata": dict(self.metadata),
        }
