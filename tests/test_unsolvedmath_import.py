from __future__ import annotations

import json
from pathlib import Path

import yaml

import amra.problem_banks.unsolvedmath as unsolvedmath
from amra.problem_banks.unsolvedmath import (
    UnsolvedMathImporter,
    parse_unsolvedmath_detail_page,
    parse_unsolvedmath_index_page,
    parse_unsolvedmath_sets_page,
)


def _flight_page(problem: dict) -> str:
    flight = '6:{"problem":' + json.dumps(problem) + "}"
    encoded = json.dumps(flight)
    return f"<html><script>self.__next_f.push([1,{encoded}])</script></html>"


def _card(source_id: str, title: str, statement: str, *, status: str = "Open") -> str:
    return (
        f'<a href="/problems/{source_id}"><div>'
        f"<span>{source_id}</span><span>{status}</span>"
        f"<h3>{title}</h3><p>{statement}</p>"
        "<span>L<!-- -->2</span><span>Number Theory</span>"
        "</div></a>"
    )


def test_parse_detail_index_and_sets_payloads() -> None:
    problem = {
        "id": 7,
        "problem_number": "NT-007",
        "title": "A universal claim",
        "statement": "Every admissible integer has property P.",
        "status": "open",
        "published": True,
    }
    detail = parse_unsolvedmath_detail_page(_flight_page(problem), expected_source_id="NT-007")
    index = parse_unsolvedmath_index_page(
        _card("NT-007", "A universal claim", "Every admissible integer has property P..."),
        page=3,
    )
    sets = parse_unsolvedmath_sets_page(
        '<a href="/problems?set=8"><h3>Erdos Problems<svg></svg></h3>'
        "<p>Problems posed by Erdos.</p><span>632<!-- --> problems</span></a>"
    )

    assert detail["statement"] == "Every admissible integer has property P."
    assert index == [
        {
            "source_id": "NT-007",
            "source_page": 3,
            "title": "A universal claim",
            "statement": "Every admissible integer has property P",
            "category": "Number Theory",
            "difficulty_level": 2,
            "status": "open",
        }
    ]
    assert sets[0]["set_id"] == 8
    assert sets[0]["reported_problem_count"] == 632


def test_importer_builds_open_non_erdos_canonical_bank(
    tmp_path: Path,
    monkeypatch,
) -> None:
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "bank_registry.yaml").write_text("[]\n", encoding="utf-8")
    index_page = (
        _card("NT-001", "Index title", "Every integer has property P...")
        + _card("NT-002", "Detail title", "Every integer has property P...")
        + _card("EP-001", "Erdos item", "Every graph has property Q...")
        + "<p>Page 1 of 1</p>"
    )
    erdos_page = _card("EP-001", "Erdos item", "Every graph has property Q...") + "<p>Page 1 of 1</p>"
    sets_page = (
        '<a href="/problems?set=8"><h3>Erdos Problems<svg></svg></h3>'
        "<p>Problems posed by Erdos.</p><span>1 problems</span></a>"
    )
    details = {
        "NT-001": {
            "id": 1,
            "problem_number": "NT-001",
            "title": "Detail title",
            "statement": "Every integer has property P.",
            "status": "open",
            "published": True,
            "category": {"display_name": "Number Theory"},
            "difficulty": {"level": 2, "name": "L2"},
        },
        "NT-002": {
            "id": 2,
            "problem_number": "NT-002",
            "title": "Detail title",
            "statement": "Every integer has property P.",
            "status": "open",
            "published": True,
            "category": {"display_name": "Number Theory"},
            "difficulty": {"level": 2, "name": "L2"},
        },
        "EP-001": {
            "id": 3,
            "problem_number": "EP-001",
            "title": "Erdos item",
            "statement": "Every graph has property Q.",
            "status": "open",
            "published": True,
            "category": {"display_name": "Graph Theory"},
            "difficulty": {"level": 3, "name": "L3"},
        },
    }

    def fake_fetch(url: str, **_: object) -> str:
        if url.endswith("/problems?page=1"):
            return index_page
        if url.endswith("/sets"):
            return sets_page
        if "set=8" in url:
            return erdos_page
        source_id = url.rsplit("/", 1)[-1]
        return _flight_page(details[source_id])

    monkeypatch.setattr(unsolvedmath, "fetch_text", fake_fetch)
    payload = UnsolvedMathImporter(
        repo_root=tmp_path,
        workers=2,
        request_delay=0,
    ).run(refresh=True)

    assert payload["counts"]["all_records"] == 3
    assert payload["counts"]["index_card_rows"] == 3
    assert payload["counts"]["index_unique_source_ids"] == 3
    assert payload["counts"]["index_duplicate_card_occurrences"] == 0
    assert payload["counts"]["open_records"] == 3
    assert payload["counts"]["erdos_open_records"] == 1
    assert payload["counts"]["open_non_erdos_records"] == 2
    assert payload["counts"]["open_non_erdos_canonical"] == 1
    bank = yaml.safe_load(
        (tmp_path / "data" / "banks" / "unsolvedmath_open_non_erdos.yaml").read_text(encoding="utf-8")
    )
    assert [record["problem_id"] for record in bank] == ["unsolvedmath-nt-002"]
    assert bank[0]["metadata"]["source_consistency_flags"] == []


def test_importer_preserves_cross_page_source_id_collisions(
    tmp_path: Path,
    monkeypatch,
) -> None:
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "bank_registry.yaml").write_text("[]\n", encoding="utf-8")
    first_page = _card("C-001", "First Claim", "Every integer has property A.") + "<p>Page 1 of 2</p>"
    second_page = _card("C-001", "Second Claim", "Every graph has property B.") + "<p>Page 2 of 2</p>"
    detail = {
        "id": 1,
        "problem_number": "C-001",
        "title": "First Claim",
        "statement": "Every integer has property A.",
        "status": "open",
        "published": True,
        "category": {"display_name": "Number Theory"},
        "difficulty": {"level": 2, "name": "L2"},
    }

    def fake_fetch(url: str, **_: object) -> str:
        if url.endswith("/problems?page=1"):
            return first_page
        if url.endswith("/problems?page=2"):
            return second_page
        if url.endswith("/sets"):
            return ""
        return _flight_page(detail)

    monkeypatch.setattr(unsolvedmath, "fetch_text", fake_fetch)
    payload = UnsolvedMathImporter(
        repo_root=tmp_path,
        workers=1,
        request_delay=0,
    ).run(refresh=True)
    all_records = yaml.safe_load(
        (tmp_path / "data" / "banks" / "unsolvedmath_all.yaml").read_text(encoding="utf-8")
    )
    collisions = yaml.safe_load(
        (tmp_path / "data" / "banks" / "unsolvedmath_source_id_collisions.yaml").read_text(
            encoding="utf-8"
        )
    )

    assert payload["counts"]["index_card_rows"] == 2
    assert payload["counts"]["index_unique_source_ids"] == 1
    assert payload["counts"]["source_ids_with_title_collisions"] == 1
    assert payload["counts"]["source_id_collision_records"] == 1
    assert payload["counts"]["all_records"] == 2
    assert all_records[0]["metadata"]["statement_quality"] == "detail_page"
    assert all_records[1]["metadata"]["statement_quality"] == "index_collision_snippet"
    assert all_records[1]["metadata"]["canonical_source_record_id"] == "unsolvedmath-c-001"
    assert len(collisions) == 1
