from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from ara_math.workstreams import utc_now_iso


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


class UncertaintyKind(_StringEnum):
    FAILED_ROUTE = "failed_route"
    UNRESOLVED_ASSUMPTION = "unresolved_assumption"
    SOURCE_DEBT = "source_debt"
    THEOREM_DEBT = "theorem_debt"
    STATEMENT_DRIFT = "statement_drift"
    COMPUTATION_DEBT = "computation_debt"
    STALLED_WORKSTREAM = "stalled_workstream"


class UncertaintyStatus(_StringEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    FROZEN = "frozen"


class SourceDebtStatus(_StringEnum):
    SOURCE_VERIFIED = "source_verified"
    SOURCE_FORMALIZATION_NEEDED = "source_formalization_needed"
    EXTERNAL_THEOREM_NEEDED = "external_theorem_needed"
    RESEARCH_GAP = "research_gap"


def normalize_route_text(text: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    return re.sub(r"\s+", " ", normalized)


def route_fingerprint(text: str) -> str:
    normalized = normalize_route_text(text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def _string_list(values: list[Any] | None) -> list[str]:
    return [str(value) for value in values or []]


def _dict_value(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


@dataclass(slots=True)
class UncertaintyItem:
    item_id: str
    kind: UncertaintyKind
    title: str
    description: str = ""
    owner_workstream_id: str = ""
    claim_id: str = ""
    status: UncertaintyStatus = UncertaintyStatus.OPEN
    source_debt_status: SourceDebtStatus | None = None
    confidence: float = 0.0
    severity: str = "medium"
    related_artifact_ids: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.kind = UncertaintyKind.coerce(self.kind)
        self.status = UncertaintyStatus.coerce(self.status)
        if self.source_debt_status:
            self.source_debt_status = SourceDebtStatus.coerce(self.source_debt_status)
        self.related_artifact_ids = _string_list(self.related_artifact_ids)
        self.metadata = _dict_value(self.metadata)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "UncertaintyItem":
        raw_source_debt_status = payload.get("source_debt_status")
        return cls(
            item_id=str(payload["item_id"]),
            kind=UncertaintyKind.coerce(payload.get("kind", UncertaintyKind.UNRESOLVED_ASSUMPTION)),
            title=str(payload.get("title", "")),
            description=str(payload.get("description", "")),
            owner_workstream_id=str(payload.get("owner_workstream_id", "")),
            claim_id=str(payload.get("claim_id", "")),
            status=UncertaintyStatus.coerce(payload.get("status", UncertaintyStatus.OPEN)),
            source_debt_status=SourceDebtStatus.coerce(raw_source_debt_status) if raw_source_debt_status else None,
            confidence=float(payload.get("confidence", 0.0) or 0.0),
            severity=str(payload.get("severity", "medium")),
            related_artifact_ids=_string_list(payload.get("related_artifact_ids")),
            created_at=str(payload.get("created_at") or utc_now_iso()),
            updated_at=str(payload.get("updated_at") or utc_now_iso()),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "kind": self.kind.value,
            "title": self.title,
            "description": self.description,
            "owner_workstream_id": self.owner_workstream_id,
            "claim_id": self.claim_id,
            "status": self.status.value,
            "source_debt_status": self.source_debt_status.value if self.source_debt_status else "",
            "confidence": self.confidence,
            "severity": self.severity,
            "related_artifact_ids": list(self.related_artifact_ids),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": dict(self.metadata),
        }

    def resolve(self) -> None:
        self.status = UncertaintyStatus.RESOLVED
        self.updated_at = utc_now_iso()


@dataclass(slots=True)
class FailedRouteRecord:
    route_id: str
    summary: str
    failure_reason: str
    owner_workstream_id: str = ""
    claim_id: str = ""
    fingerprint: str = ""
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.fingerprint:
            self.fingerprint = route_fingerprint(self.summary)
        self.metadata = _dict_value(self.metadata)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "FailedRouteRecord":
        summary = str(payload.get("summary", ""))
        return cls(
            route_id=str(payload["route_id"]),
            summary=summary,
            failure_reason=str(payload.get("failure_reason", "")),
            owner_workstream_id=str(payload.get("owner_workstream_id", "")),
            claim_id=str(payload.get("claim_id", "")),
            fingerprint=str(payload.get("fingerprint") or route_fingerprint(summary)),
            created_at=str(payload.get("created_at") or utc_now_iso()),
            metadata=_dict_value(payload.get("metadata")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "route_id": self.route_id,
            "summary": self.summary,
            "failure_reason": self.failure_reason,
            "owner_workstream_id": self.owner_workstream_id,
            "claim_id": self.claim_id,
            "fingerprint": self.fingerprint or route_fingerprint(self.summary),
            "created_at": self.created_at,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class UncertaintyLedger:
    ledger_id: str
    items: list[UncertaintyItem] = field(default_factory=list)
    failed_routes: list[FailedRouteRecord] = field(default_factory=list)
    generated_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.items = [UncertaintyItem.from_dict(item) if isinstance(item, dict) else item for item in self.items]
        self.failed_routes = [
            FailedRouteRecord.from_dict(item) if isinstance(item, dict) else item for item in self.failed_routes
        ]
        self.metadata = _dict_value(self.metadata)

    @classmethod
    def from_dict(cls, payload: dict[str, Any] | None) -> "UncertaintyLedger":
        payload = payload or {}
        return cls(
            ledger_id=str(payload.get("ledger_id", "uncertainty-ledger")),
            items=[UncertaintyItem.from_dict(item) for item in payload.get("items", [])],
            failed_routes=[FailedRouteRecord.from_dict(item) for item in payload.get("failed_routes", [])],
            generated_at=str(payload.get("generated_at") or utc_now_iso()),
            metadata=_dict_value(payload.get("metadata")),
        )

    @classmethod
    def load(cls, path: Path) -> "UncertaintyLedger":
        if not path.exists():
            return cls(ledger_id="uncertainty-ledger")
        return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def to_dict(self) -> dict[str, Any]:
        return {
            "ledger_id": self.ledger_id,
            "generated_at": self.generated_at,
            "items": [item.to_dict() for item in self.items],
            "failed_routes": [route.to_dict() for route in self.failed_routes],
            "metadata": dict(self.metadata),
        }

    def get_item(self, item_id: str) -> UncertaintyItem | None:
        return next((item for item in self.items if item.item_id == item_id), None)

    def add_item(self, item: UncertaintyItem | dict[str, Any] | None = None, **kwargs: Any) -> UncertaintyItem:
        if item is None:
            item = UncertaintyItem(**kwargs)
        elif isinstance(item, dict):
            item = UncertaintyItem.from_dict(item)
        existing = self.get_item(item.item_id)
        if existing:
            return existing
        self.items.append(item)
        self.generated_at = utc_now_iso()
        return item

    def upsert_item(self, item: UncertaintyItem | dict[str, Any]) -> UncertaintyItem:
        if isinstance(item, dict):
            item = UncertaintyItem.from_dict(item)
        for index, existing in enumerate(self.items):
            if existing.item_id == item.item_id:
                if not item.created_at:
                    item.created_at = existing.created_at
                self.items[index] = item
                self.generated_at = utc_now_iso()
                return item
        return self.add_item(item)

    def add_source_debt(
        self,
        *,
        item_id: str,
        title: str,
        source_debt_status: SourceDebtStatus | str,
        description: str = "",
        owner_workstream_id: str = "",
        claim_id: str = "",
        confidence: float = 0.0,
        severity: str = "high",
    ) -> UncertaintyItem:
        return self.upsert_item(
            UncertaintyItem(
                item_id=item_id,
                kind=UncertaintyKind.SOURCE_DEBT,
                title=title,
                description=description,
                owner_workstream_id=owner_workstream_id,
                claim_id=claim_id,
                source_debt_status=SourceDebtStatus.coerce(source_debt_status),
                confidence=confidence,
                severity=severity,
            )
        )

    def add_failed_route(
        self,
        *,
        route_id: str,
        summary: str,
        failure_reason: str,
        owner_workstream_id: str = "",
        claim_id: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> FailedRouteRecord:
        record = FailedRouteRecord(
            route_id=route_id,
            summary=summary,
            failure_reason=failure_reason,
            owner_workstream_id=owner_workstream_id,
            claim_id=claim_id,
            fingerprint=route_fingerprint(summary),
            metadata=metadata or {},
        )
        if any(existing.fingerprint == record.fingerprint for existing in self.failed_routes):
            return next(existing for existing in self.failed_routes if existing.fingerprint == record.fingerprint)
        self.failed_routes.append(record)
        self.upsert_item(
            UncertaintyItem(
                item_id=f"failed-route:{route_id}",
                kind=UncertaintyKind.FAILED_ROUTE,
                title=summary,
                description=failure_reason,
                owner_workstream_id=owner_workstream_id,
                claim_id=claim_id,
                severity="medium",
                metadata={"route_id": route_id, "fingerprint": record.fingerprint},
            )
        )
        self.generated_at = utc_now_iso()
        return record

    def open_items(self) -> list[UncertaintyItem]:
        return [item for item in self.items if item.status in {UncertaintyStatus.OPEN, UncertaintyStatus.IN_PROGRESS}]

    def items_by_kind(self, kind: UncertaintyKind | str) -> list[UncertaintyItem]:
        expected = UncertaintyKind.coerce(kind)
        return [item for item in self.items if item.kind == expected]

    def source_debt_items(self) -> list[UncertaintyItem]:
        return self.items_by_kind(UncertaintyKind.SOURCE_DEBT)

    def blocking_items(self) -> list[UncertaintyItem]:
        blocking_source_statuses = {
            SourceDebtStatus.EXTERNAL_THEOREM_NEEDED,
            SourceDebtStatus.RESEARCH_GAP,
            SourceDebtStatus.SOURCE_FORMALIZATION_NEEDED,
        }
        blockers: list[UncertaintyItem] = []
        for item in self.open_items():
            if item.kind in {
                UncertaintyKind.UNRESOLVED_ASSUMPTION,
                UncertaintyKind.THEOREM_DEBT,
                UncertaintyKind.STATEMENT_DRIFT,
                UncertaintyKind.COMPUTATION_DEBT,
                UncertaintyKind.STALLED_WORKSTREAM,
            }:
                blockers.append(item)
            elif item.source_debt_status in blocking_source_statuses:
                blockers.append(item)
        return blockers

    def find_failed_route(self, summary: str) -> FailedRouteRecord | None:
        fingerprint = route_fingerprint(summary)
        return next((route for route in self.failed_routes if route.fingerprint == fingerprint), None)

    def should_suppress_route(self, summary: str, *, changed_note: str = "") -> bool:
        if changed_note.strip():
            return False
        return self.find_failed_route(summary) is not None

    def counts_by_kind(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in self.items:
            counts[item.kind.value] = counts.get(item.kind.value, 0) + 1
        return counts


def load_uncertainty_ledger(path: Path) -> UncertaintyLedger:
    return UncertaintyLedger.load(path)


def save_uncertainty_ledger(path: Path, ledger: UncertaintyLedger) -> None:
    ledger.save(path)


def load_failed_routes_jsonl(path: Path) -> list[FailedRouteRecord]:
    if not path.exists():
        return []
    records: list[FailedRouteRecord] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(FailedRouteRecord.from_dict(json.loads(line)))
    return records


def append_failed_route_jsonl(path: Path, route: FailedRouteRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(route.to_dict(), ensure_ascii=False) + "\n")
