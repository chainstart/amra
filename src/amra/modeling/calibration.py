from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from amra.modeling.model_spec import _dict_value, _list_value, _string_list


MODEL_CALIBRATION_SCHEMA_VERSION = "amra.model_calibration.v1"


@dataclass(slots=True)
class ModelDatasetRef:
    dataset_id: str
    role: str
    description: str = ""
    source: str = ""
    rows: int = 0
    checksum: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any], *, role: str) -> "ModelDatasetRef":
        return cls(
            dataset_id=str(payload.get("dataset_id") or payload.get("id") or payload.get("name") or role),
            role=str(payload.get("role") or role),
            description=str(payload.get("description") or ""),
            source=str(payload.get("source") or ""),
            rows=int(payload.get("rows") or payload.get("row_count") or 0),
            checksum=str(payload.get("checksum") or payload.get("sha256") or ""),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "role": self.role,
            "description": self.description,
            "source": self.source,
            "rows": self.rows,
            "checksum": self.checksum,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class CalibrationReport:
    calibration_id: str
    model_id: str
    method: str
    datasets: list[ModelDatasetRef] = field(default_factory=list)
    parameter_estimates: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, Any] = field(default_factory=dict)
    held_out_for_validation: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @classmethod
    def from_payload(cls, payload: dict[str, Any], *, model_id: str) -> "CalibrationReport":
        calibration = _dict_value(payload.get("calibration"))
        return cls(
            calibration_id=str(calibration.get("calibration_id") or calibration.get("id") or f"calibration-{model_id}"),
            model_id=model_id,
            method=str(calibration.get("method") or "fixture_calibration"),
            datasets=[
                ModelDatasetRef.from_dict(item, role="calibration")
                for item in _list_value(calibration.get("datasets") or calibration.get("data"))
                if isinstance(item, dict)
            ],
            parameter_estimates=_dict_value(calibration.get("parameter_estimates") or calibration.get("parameters")),
            metrics=_dict_value(calibration.get("metrics")),
            held_out_for_validation=_string_list(calibration.get("held_out_for_validation")),
            notes=_string_list(calibration.get("notes")),
        )

    @property
    def dataset_ids(self) -> list[str]:
        return [item.dataset_id for item in self.datasets]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": MODEL_CALIBRATION_SCHEMA_VERSION,
            "calibration_id": self.calibration_id,
            "model_id": self.model_id,
            "method": self.method,
            "datasets": [item.to_dict() for item in self.datasets],
            "parameter_estimates": dict(self.parameter_estimates),
            "metrics": dict(self.metrics),
            "held_out_for_validation": list(self.held_out_for_validation),
            "notes": list(self.notes),
        }
