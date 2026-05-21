from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from amra.orchestration.workstreams import utc_now_iso
from amra.portfolio_memory import write_json
from amra.research.objects import (
    ConjectureRecord,
    ConstructionRecord,
    CounterexampleRecord,
    NegativeResultRecord,
    ResearchConfidence,
    ResearchObjectStatus,
)


CONJECTURE_MINING_SCHEMA_VERSION = "amra.conjecture_mining_fixture.v1"
CONJECTURE_MINING_RUN_SCHEMA_VERSION = "amra.conjecture_mining_run.v1"

CONJECTURE_MINING_RUN_FILE = "conjecture_mining_run.json"
CONJECTURE_MINING_CONJECTURES_FILE = "conjectures.json"
CONJECTURE_MINING_COUNTEREXAMPLES_FILE = "counterexamples.json"
CONJECTURE_MINING_CONSTRUCTIONS_FILE = "constructions.json"
CONJECTURE_MINING_NEGATIVE_RESULTS_FILE = "negative_results.json"
CONJECTURE_MINING_NOVELTY_HANDOFF_FILE = "novelty_gate_handoff.json"


def _dict_value(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _list_value(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _string_list(value: Any) -> list[str]:
    return [str(item) for item in _list_value(value)]


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _slug(value: str) -> str:
    normalized = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    parts = [part for part in normalized.split("-") if part]
    return "-".join(parts) or "candidate"


def _field(row: dict[str, Any], name: str) -> Any:
    current: Any = row
    for part in name.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _number(value: Any) -> int | float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    try:
        text = str(value).strip()
        if "." in text:
            return float(text)
        return int(text)
    except ValueError:
        return None


def _evaluate_predicate(predicate: dict[str, Any], row: dict[str, Any]) -> bool:
    op = str(predicate.get("op") or "").strip().lower()
    field_name = str(predicate.get("field") or "value")
    value = _field(row, field_name)

    if op == "mod_eq":
        number = _number(value)
        modulus = _number(predicate.get("mod"))
        expected = _number(predicate.get("equals", 0))
        return number is not None and modulus not in {None, 0} and expected is not None and number % modulus == expected
    if op == "equals":
        return value == predicate.get("value")
    if op == "not_equals":
        return value != predicate.get("value")
    if op in {"gte", "lte", "gt", "lt"}:
        number = _number(value)
        expected = _number(predicate.get("value"))
        if number is None or expected is None:
            return False
        return {
            "gte": number >= expected,
            "lte": number <= expected,
            "gt": number > expected,
            "lt": number < expected,
        }[op]
    if op == "divides":
        divisor = _number(value)
        dividend = _number(_field(row, str(predicate.get("dividend_field") or "value")))
        return divisor not in {None, 0} and dividend is not None and dividend % divisor == 0
    if op == "is_even":
        number = _number(value)
        return number is not None and number % 2 == 0
    if op == "is_odd":
        number = _number(value)
        return number is not None and number % 2 == 1
    if op == "always_true":
        return True
    raise ValueError(f"unsupported conjecture predicate op: {op!r}")


def _assignment(row: dict[str, Any], variables: list[str]) -> dict[str, Any]:
    if not variables:
        return dict(row)
    return {name: _field(row, name) for name in variables}


@dataclass(slots=True)
class _Candidate:
    spec: dict[str, Any]
    object_id: str
    title: str
    statement: str
    predicate: dict[str, Any]


class ConjectureMiningRunner:
    def run_fixture(self, *, fixture: Path, output_dir: Path) -> dict[str, Any]:
        fixture_path = fixture.expanduser().resolve()
        output_dir = output_dir.expanduser().resolve()
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("conjecture mining fixture must be a JSON object")

        observations = [_dict_value(item) for item in _list_value(payload.get("observations"))]
        search_rows = [_dict_value(item) for item in _list_value(payload.get("search_space") or observations)]
        candidates = [self._candidate(item) for item in _list_value(payload.get("candidates")) if isinstance(item, dict)]
        if not candidates:
            raise ValueError("conjecture mining fixture requires at least one candidate")

        fixture_hash = _sha256_file(fixture_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        conjectures: list[ConjectureRecord] = []
        counterexamples: list[CounterexampleRecord] = []
        constructions: list[ConstructionRecord] = []
        negative_results: list[NegativeResultRecord] = []
        novelty_items: list[dict[str, Any]] = []

        for candidate in candidates:
            support_rows = [row for row in observations if _evaluate_predicate(candidate.predicate, row)]
            if len(support_rows) != len(observations):
                continue

            search = self._bounded_search(candidate=candidate, rows=search_rows, payload=payload)
            novelty = self._novelty_report(candidate=candidate, payload=payload)
            status = (
                ResearchObjectStatus.COUNTEREXAMPLE_FOUND
                if search["counterexample"]
                else ResearchObjectStatus.EMPIRICALLY_SUPPORTED
            )
            conjecture = ConjectureRecord(
                object_id=candidate.object_id,
                title=candidate.title,
                status=status,
                statement=candidate.statement,
                informal_statement=candidate.statement,
                formal_statement=candidate.spec.get("formal_statement"),
                domain=str(payload.get("domain") or candidate.spec.get("domain") or ""),
                tags=sorted(set(["conjecture_mining", *(_string_list(candidate.spec.get("tags")))])),
                confidence=ResearchConfidence.LOW,
                scope=str(candidate.spec.get("scope") or payload.get("scope") or ""),
                known_cases=[f"{len(observations)} fixture observations"],
                excluded_cases=_string_list(candidate.spec.get("excluded_cases")),
                counterexample_search=[search["search_id"]],
                novelty_report=novelty,
                promotion_target="proof_task" if not search["counterexample"] else "negative_result",
                metadata={
                    "candidate_id": str(candidate.spec.get("id") or candidate.object_id),
                    "predicate": dict(candidate.predicate),
                    "support_count": len(support_rows),
                    "fixture_sha256": fixture_hash,
                },
            )
            conjectures.append(conjecture)
            constructions.extend(self._construction_records(candidate=candidate, conjecture=conjecture, rows=support_rows))
            if search["counterexample"]:
                counterexample = self._counterexample_record(
                    candidate=candidate,
                    conjecture=conjecture,
                    row=search["counterexample"],
                    search=search,
                )
                counterexamples.append(counterexample)
                negative_results.append(
                    NegativeResultRecord(
                        object_id=f"negative-{conjecture.object_id}",
                        title=f"Counterexample refutes {conjecture.title}",
                        status=ResearchObjectStatus.COUNTEREXAMPLE_FOUND,
                        statement=f"{counterexample.violation_summary} Therefore the mined conjecture is refuted within the fixture bound.",
                        domain=conjecture.domain,
                        tags=["counterexample_search", "negative_result"],
                        confidence=ResearchConfidence.MEDIUM,
                        target_object_id=conjecture.object_id,
                        refuted_by=[counterexample.object_id],
                        search_bound=search["bound"],
                        result_summary=counterexample.violation_summary,
                    )
                )
            novelty_items.append(self._novelty_handoff_item(conjecture=conjecture, novelty=novelty, search=search))

        handoff = {
            "schema_version": "amra.novelty_gate_handoff.v1",
            "generated_at": utc_now_iso(),
            "fixture": {"path": str(fixture_path), "sha256": fixture_hash},
            "items": novelty_items,
            "summary": {
                "ready_for_review": sum(1 for item in novelty_items if item["recommended_action"] == "review_for_proof_promotion"),
                "blocked_by_counterexample": sum(1 for item in novelty_items if item["recommended_action"] == "record_negative_result"),
                "known_or_likely_known": sum(1 for item in novelty_items if item["novelty_status"] in {"known", "likely_known"}),
            },
        }
        run = {
            "schema_version": CONJECTURE_MINING_RUN_SCHEMA_VERSION,
            "status": "succeeded",
            "generated_at": utc_now_iso(),
            "deterministic": True,
            "fixture": {"path": str(fixture_path), "sha256": fixture_hash},
            "output_dir": str(output_dir),
            "counts": {
                "conjectures": len(conjectures),
                "counterexamples": len(counterexamples),
                "constructions": len(constructions),
                "negative_results": len(negative_results),
            },
            "conjectures": [record.to_dict() for record in conjectures],
            "counterexamples": [record.to_dict() for record in counterexamples],
            "constructions": [record.to_dict() for record in constructions],
            "negative_results": [record.to_dict() for record in negative_results],
            "novelty_gate_handoff": handoff,
            "record_files": {
                "run": str(output_dir / CONJECTURE_MINING_RUN_FILE),
                "conjectures": str(output_dir / CONJECTURE_MINING_CONJECTURES_FILE),
                "counterexamples": str(output_dir / CONJECTURE_MINING_COUNTEREXAMPLES_FILE),
                "constructions": str(output_dir / CONJECTURE_MINING_CONSTRUCTIONS_FILE),
                "negative_results": str(output_dir / CONJECTURE_MINING_NEGATIVE_RESULTS_FILE),
                "novelty_gate_handoff": str(output_dir / CONJECTURE_MINING_NOVELTY_HANDOFF_FILE),
            },
        }
        write_json(output_dir / CONJECTURE_MINING_CONJECTURES_FILE, [record.to_dict() for record in conjectures])
        write_json(output_dir / CONJECTURE_MINING_COUNTEREXAMPLES_FILE, [record.to_dict() for record in counterexamples])
        write_json(output_dir / CONJECTURE_MINING_CONSTRUCTIONS_FILE, [record.to_dict() for record in constructions])
        write_json(output_dir / CONJECTURE_MINING_NEGATIVE_RESULTS_FILE, [record.to_dict() for record in negative_results])
        write_json(output_dir / CONJECTURE_MINING_NOVELTY_HANDOFF_FILE, handoff)
        write_json(output_dir / CONJECTURE_MINING_RUN_FILE, run)
        return run

    def _candidate(self, payload: dict[str, Any]) -> _Candidate:
        candidate_id = str(payload.get("id") or payload.get("object_id") or payload.get("title") or "candidate")
        object_id = str(payload.get("object_id") or f"conjecture-{_slug(candidate_id)}")
        title = str(payload.get("title") or candidate_id)
        statement = str(payload.get("statement") or title)
        predicate = _dict_value(payload.get("predicate"))
        if not predicate:
            raise ValueError(f"candidate {candidate_id!r} is missing predicate")
        return _Candidate(spec=payload, object_id=object_id, title=title, statement=statement, predicate=predicate)

    def _bounded_search(self, *, candidate: _Candidate, rows: list[dict[str, Any]], payload: dict[str, Any]) -> dict[str, Any]:
        max_cases = int(_dict_value(payload.get("bounds")).get("max_cases") or len(rows))
        variables = _string_list(candidate.spec.get("variables") or payload.get("variables"))
        checked_rows = rows[:max(0, max_cases)]
        counterexample = next((row for row in checked_rows if not _evaluate_predicate(candidate.predicate, row)), None)
        return {
            "search_id": f"counterexample-search-{_slug(candidate.object_id)}",
            "checked": len(checked_rows),
            "variables": variables,
            "counterexample": counterexample,
            "bound": {
                "max_cases": max_cases,
                "checked_cases": len(checked_rows),
                "variables": variables,
            },
        }

    def _novelty_report(self, *, candidate: _Candidate, payload: dict[str, Any]) -> dict[str, Any]:
        text = " ".join(
            [
                candidate.object_id,
                candidate.title,
                candidate.statement,
                " ".join(_string_list(candidate.spec.get("tags"))),
            ]
        ).lower()
        sources = [_dict_value(item) for item in _list_value(payload.get("known_results"))]
        for source in sources:
            terms = [term.lower() for term in _string_list(source.get("match_terms"))]
            if terms and all(term in text for term in terms):
                return {
                    "status": str(source.get("status") or "likely_known"),
                    "matched_source_id": str(source.get("source_id") or source.get("id") or ""),
                    "rationale": str(source.get("rationale") or "Fixture source terms matched the mined statement."),
                }
        if not sources:
            return {
                "status": "insufficient_source",
                "matched_source_id": "",
                "rationale": "No fixture novelty sources were provided.",
            }
        return {
            "status": "novel_candidate",
            "matched_source_id": "",
            "rationale": "No fixture source matched the candidate statement.",
        }

    def _construction_records(
        self,
        *,
        candidate: _Candidate,
        conjecture: ConjectureRecord,
        rows: list[dict[str, Any]],
    ) -> list[ConstructionRecord]:
        records: list[ConstructionRecord] = []
        for index, row in enumerate(rows[:3], start=1):
            records.append(
                ConstructionRecord(
                    object_id=f"construction-{_slug(conjecture.object_id)}-{index}",
                    title=f"Witness {index} for {conjecture.title}",
                    status=ResearchObjectStatus.EMPIRICALLY_SUPPORTED,
                    statement=f"Fixture witness {index} satisfies {conjecture.object_id}.",
                    domain=conjecture.domain,
                    tags=["construction_search", "fixture_witness"],
                    confidence=ResearchConfidence.LOW,
                    target_conjecture_id=conjecture.object_id,
                    parameters=_assignment(row, _string_list(candidate.spec.get("variables"))),
                    witness=dict(row),
                    verifies=True,
                )
            )
        return records

    def _counterexample_record(
        self,
        *,
        candidate: _Candidate,
        conjecture: ConjectureRecord,
        row: dict[str, Any],
        search: dict[str, Any],
    ) -> CounterexampleRecord:
        variables = _string_list(candidate.spec.get("variables")) or _string_list(search.get("variables"))
        assignment = _assignment(row, variables)
        summary = f"{assignment or row} violates {conjecture.object_id}."
        return CounterexampleRecord(
            object_id=f"counterexample-{_slug(conjecture.object_id)}",
            title=f"Counterexample to {conjecture.title}",
            status=ResearchObjectStatus.COUNTEREXAMPLE_FOUND,
            statement=summary,
            domain=conjecture.domain,
            tags=["counterexample_search"],
            confidence=ResearchConfidence.MEDIUM,
            target_conjecture_id=conjecture.object_id,
            assignment=assignment,
            observed_value=dict(row),
            violation_summary=summary,
            search_space=search["bound"],
            predicate=dict(candidate.predicate),
        )

    def _novelty_handoff_item(
        self,
        *,
        conjecture: ConjectureRecord,
        novelty: dict[str, Any],
        search: dict[str, Any],
    ) -> dict[str, Any]:
        if search["counterexample"]:
            action = "record_negative_result"
        elif novelty["status"] in {"known", "likely_known"}:
            action = "suppress_or_cite_known_result"
        else:
            action = "review_for_proof_promotion"
        return {
            "conjecture_id": conjecture.object_id,
            "statement": conjecture.statement,
            "novelty_status": novelty["status"],
            "matched_source_id": novelty.get("matched_source_id", ""),
            "counterexample_search_id": search["search_id"],
            "counterexample_found": bool(search["counterexample"]),
            "promotion_target": conjecture.promotion_target,
            "recommended_action": action,
        }


def run_conjecture_mining_fixture(*, fixture: Path, output_dir: Path) -> dict[str, Any]:
    return ConjectureMiningRunner().run_fixture(fixture=fixture, output_dir=output_dir)
