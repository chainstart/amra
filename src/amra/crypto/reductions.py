from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from amra.modeling.model_spec import _dict_value, _list_value, _string_list, slug


SECURITY_REDUCTION_SCHEMA_VERSION = "amra.crypto.security_reduction.v1"


@dataclass(slots=True)
class SecurityReduction:
    reduction_id: str
    game_id: str
    assumption_id: str
    statement: str
    loss_bound: str = ""
    proof_sketch: str = ""
    dependencies: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any], *, game_id: str = "", index: int = 0) -> "SecurityReduction":
        assumption_id = str(payload.get("assumption_id") or payload.get("target_assumption_id") or "")
        return cls(
            reduction_id=str(payload.get("reduction_id") or payload.get("id") or f"reduction-{index + 1}-{slug(assumption_id)}"),
            game_id=str(payload.get("game_id") or game_id),
            assumption_id=assumption_id,
            statement=str(payload.get("statement") or payload.get("description") or ""),
            loss_bound=str(payload.get("loss_bound") or payload.get("advantage_loss") or ""),
            proof_sketch=str(payload.get("proof_sketch") or payload.get("sketch") or ""),
            dependencies=_string_list(payload.get("dependencies")),
            limitations=_string_list(payload.get("limitations")),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SECURITY_REDUCTION_SCHEMA_VERSION,
            "reduction_id": self.reduction_id,
            "game_id": self.game_id,
            "assumption_id": self.assumption_id,
            "statement": self.statement,
            "loss_bound": self.loss_bound,
            "proof_sketch": self.proof_sketch,
            "dependencies": list(self.dependencies),
            "limitations": list(self.limitations),
            "metadata": dict(self.metadata),
        }


def reductions_from_payload(payload: dict[str, Any], *, game_id: str) -> list[SecurityReduction]:
    return [
        SecurityReduction.from_dict(item, game_id=game_id, index=index)
        for index, item in enumerate(_list_value(payload.get("reductions")))
        if isinstance(item, dict)
    ]
