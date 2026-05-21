from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from amra.modeling.model_spec import _dict_value, _list_value, _string_list, slug


THREAT_MODEL_SCHEMA_VERSION = "amra.crypto.threat_model.v1"


@dataclass(slots=True)
class ThreatModel:
    threat_model_id: str
    title: str
    scheme: str
    assets: list[str] = field(default_factory=list)
    adversary_goals: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    exclusions: list[str] = field(default_factory=list)
    environment: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ThreatModel":
        title = str(payload.get("title") or payload.get("name") or "Threat model")
        return cls(
            threat_model_id=str(payload.get("threat_model_id") or payload.get("id") or f"threat-{slug(title)}"),
            title=title,
            scheme=str(payload.get("scheme") or payload.get("scheme_id") or ""),
            assets=_string_list(payload.get("assets")),
            adversary_goals=_string_list(payload.get("adversary_goals") or payload.get("goals")),
            capabilities=_string_list(payload.get("capabilities") or payload.get("adversary_capabilities")),
            exclusions=_string_list(payload.get("exclusions") or payload.get("out_of_scope")),
            environment=_dict_value(payload.get("environment")),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": THREAT_MODEL_SCHEMA_VERSION,
            "threat_model_id": self.threat_model_id,
            "title": self.title,
            "scheme": self.scheme,
            "assets": list(self.assets),
            "adversary_goals": list(self.adversary_goals),
            "capabilities": list(self.capabilities),
            "exclusions": list(self.exclusions),
            "environment": dict(self.environment),
            "metadata": dict(self.metadata),
        }


def threat_model_from_payload(payload: dict[str, Any]) -> ThreatModel:
    threat_model = payload.get("threat_model") or payload.get("threat") or {}
    if not isinstance(threat_model, dict):
        threat_model = {}
    if not threat_model:
        threat_model = {
            "title": "Threat model",
            "scheme": str(_dict_value(payload.get("security_game")).get("scheme") or ""),
            "assets": _list_value(payload.get("assets")),
            "adversary_goals": _list_value(payload.get("adversary_goals")),
            "capabilities": _list_value(payload.get("capabilities")),
        }
    return ThreatModel.from_dict(threat_model)
