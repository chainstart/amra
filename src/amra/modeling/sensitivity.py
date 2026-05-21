from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from amra.modeling.model_spec import _dict_value, _list_value, _number, _string_list, slug


MODEL_SENSITIVITY_REPORT_SCHEMA_VERSION = "amra.model_sensitivity_report.v1"


@dataclass(slots=True)
class SensitivityScenario:
    scenario_id: str
    parameter: str
    perturbation_pct: float
    output_metric: str
    response_pct: float
    notes: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, Any], *, index: int = 0) -> "SensitivityScenario":
        parameter = str(payload.get("parameter") or payload.get("variable") or f"parameter-{index + 1}")
        return cls(
            scenario_id=str(payload.get("scenario_id") or payload.get("id") or f"sensitivity-{slug(parameter)}-{index + 1}"),
            parameter=parameter,
            perturbation_pct=float(_number(payload.get("perturbation_pct")) or 0.0),
            output_metric=str(payload.get("output_metric") or payload.get("metric") or ""),
            response_pct=float(_number(payload.get("response_pct")) or _number(payload.get("response")) or 0.0),
            notes=_string_list(payload.get("notes")),
        )

    @property
    def elasticity(self) -> float:
        if self.perturbation_pct == 0:
            return 0.0
        return self.response_pct / self.perturbation_pct

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "parameter": self.parameter,
            "perturbation_pct": self.perturbation_pct,
            "output_metric": self.output_metric,
            "response_pct": self.response_pct,
            "elasticity": round(self.elasticity, 6),
            "notes": list(self.notes),
        }


@dataclass(slots=True)
class SensitivityReport:
    report_id: str
    model_id: str
    scenarios: list[SensitivityScenario] = field(default_factory=list)
    uncertainty_propagation: dict[str, Any] = field(default_factory=dict)
    dominant_parameters: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @classmethod
    def from_payload(cls, payload: dict[str, Any], *, model_id: str) -> "SensitivityReport":
        sensitivity = _dict_value(payload.get("sensitivity"))
        scenarios = [
            SensitivityScenario.from_dict(item, index=index)
            for index, item in enumerate(_list_value(sensitivity.get("scenarios")))
            if isinstance(item, dict)
        ]
        dominant = _string_list(sensitivity.get("dominant_parameters"))
        if not dominant:
            dominant = [
                item.parameter
                for item in sorted(scenarios, key=lambda scenario: abs(scenario.elasticity), reverse=True)[:3]
                if item.parameter
            ]
        return cls(
            report_id=str(sensitivity.get("report_id") or sensitivity.get("id") or f"sensitivity-{model_id}"),
            model_id=model_id,
            scenarios=scenarios,
            uncertainty_propagation=_dict_value(sensitivity.get("uncertainty_propagation")),
            dominant_parameters=dominant,
            notes=_string_list(sensitivity.get("notes")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": MODEL_SENSITIVITY_REPORT_SCHEMA_VERSION,
            "report_id": self.report_id,
            "model_id": self.model_id,
            "scenarios": [item.to_dict() for item in self.scenarios],
            "uncertainty_propagation": dict(self.uncertainty_propagation),
            "dominant_parameters": list(self.dominant_parameters),
            "notes": list(self.notes),
        }
