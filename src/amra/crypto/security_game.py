from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from amra.modeling.model_spec import _dict_value, _list_value, _string_list, slug


SECURITY_GAME_SCHEMA_VERSION = "amra.crypto.security_game.v1"
SECURITY_ASSUMPTION_SCHEMA_VERSION = "amra.crypto.security_assumption.v1"


@dataclass(slots=True)
class SecurityAssumption:
    assumption_id: str
    statement: str
    family: str = ""
    hardness_parameters: dict[str, Any] = field(default_factory=dict)
    evidence_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any], *, index: int = 0) -> "SecurityAssumption":
        statement = str(payload.get("statement") or payload.get("description") or "")
        return cls(
            assumption_id=str(payload.get("assumption_id") or payload.get("id") or f"assumption-{index + 1}"),
            statement=statement,
            family=str(payload.get("family") or payload.get("type") or ""),
            hardness_parameters=_dict_value(payload.get("hardness_parameters") or payload.get("parameters")),
            evidence_ids=_string_list(payload.get("evidence_ids")),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SECURITY_ASSUMPTION_SCHEMA_VERSION,
            "assumption_id": self.assumption_id,
            "statement": self.statement,
            "family": self.family,
            "hardness_parameters": dict(self.hardness_parameters),
            "evidence_ids": list(self.evidence_ids),
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class SecurityGameSpec:
    game_id: str
    title: str
    scheme: str
    adversary_model: str
    oracle_access: list[str] = field(default_factory=list)
    winning_condition: str = ""
    advantage_threshold: float = 0.0
    threat_model_id: str = ""
    assumptions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any], *, threat_model_id: str = "") -> "SecurityGameSpec":
        title = str(payload.get("title") or payload.get("name") or "Security game")
        threshold = payload.get("advantage_threshold", payload.get("win_threshold", 0.0))
        return cls(
            game_id=str(payload.get("game_id") or payload.get("object_id") or payload.get("id") or f"game-{slug(title)}"),
            title=title,
            scheme=str(payload.get("scheme") or payload.get("scheme_id") or ""),
            adversary_model=str(payload.get("adversary_model") or payload.get("adversary") or ""),
            oracle_access=_string_list(payload.get("oracle_access") or payload.get("oracles")),
            winning_condition=str(payload.get("winning_condition") or ""),
            advantage_threshold=float(threshold or 0.0),
            threat_model_id=str(payload.get("threat_model_id") or threat_model_id),
            assumptions=_string_list(payload.get("assumptions") or payload.get("assumption_ids")),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SECURITY_GAME_SCHEMA_VERSION,
            "game_id": self.game_id,
            "object_id": self.game_id,
            "object_type": "security_game",
            "title": self.title,
            "scheme": self.scheme,
            "adversary_model": self.adversary_model,
            "oracle_access": list(self.oracle_access),
            "winning_condition": self.winning_condition,
            "advantage_threshold": self.advantage_threshold,
            "threat_model_id": self.threat_model_id,
            "assumptions": list(self.assumptions),
            "metadata": dict(self.metadata),
        }


def security_assumptions_from_payload(payload: dict[str, Any]) -> list[SecurityAssumption]:
    return [
        SecurityAssumption.from_dict(item, index=index)
        for index, item in enumerate(_list_value(payload.get("assumptions") or payload.get("security_assumptions")))
        if isinstance(item, dict)
    ]
