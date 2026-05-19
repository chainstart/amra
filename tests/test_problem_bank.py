from pathlib import Path

from amra.core.models import ProblemRecord
from amra.problem_banks.registry import (
    DEFAULT_BANK_PATH,
    import_erdos_open_problems,
    load_problem_bank,
    load_problem_bank_with_executor_metadata,
    refresh_erdos_problem_bank,
)


def test_import_erdos_open_problems_normalizes_entries(tmp_path: Path) -> None:
    source = tmp_path / "open_problems.yaml"
    source.write_text(
        "\n".join(
            [
                "- number: '1052'",
                "  tags:",
                "    - number theory",
                "    - divisors",
                "  formalized:",
                "    state: 'yes'",
                "  status:",
                "    state: open",
                "  comments: unitary perfect numbers",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "bank.yaml"

    import_erdos_open_problems(source, output)
    problems = load_problem_bank(output)

    assert len(problems) == 1
    assert problems[0].problem_id == "1052"
    assert problems[0].formalized == "yes"
    assert "number theory" in problems[0].tags
    assert "unitary perfect numbers" in problems[0].notes


def test_refresh_erdos_problem_bank_updates_open_flag(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "bank.yaml"
    problems = [
        ProblemRecord(
            problem_id="633",
            title="Erdős Problem #633",
            source="Erdős Problems",
            statement="placeholder",
            domain="geometry",
            references=["https://www.erdosproblems.com/633"],
            metadata={"source_catalog": "erdosproblems", "status_state": "open"},
        )
    ]
    from amra.problem_banks.registry import save_problem_bank

    save_problem_bank(problems, bank_path)

    def fake_refresh(problem: ProblemRecord) -> ProblemRecord:
        payload = problem.to_dict()
        payload["open_problem"] = False
        payload["metadata"] = {**problem.metadata, "status_state": "likely_solved_preprint"}
        return ProblemRecord.from_dict(payload)

    monkeypatch.setattr("amra.problem_banks.registry.refresh_erdos_problem_record", fake_refresh)

    report = refresh_erdos_problem_bank(bank_path)
    refreshed = load_problem_bank(bank_path)

    assert report["updated_problem_count"] == 1
    assert refreshed[0].open_problem is False
    assert refreshed[0].metadata["status_state"] == "likely_solved_preprint"


def test_curated_problem_bank_carries_domain_executor_metadata() -> None:
    problems = {problem.problem_id: problem for problem in load_problem_bank(DEFAULT_BANK_PATH)}

    expected = {
        "erdos-1052": "unitary_perfect.bounded_divisor_scan.v1",
        "amicable-odd-odd": "amicable.bounded_divisor_sum_scan.v1",
        "amicable-prime-exclusion": "amicable.bounded_divisor_sum_scan.v1",
        "korselt-criterion": "carmichael.korselt_scan.v1",
        "triangle-dissection-19": "triangle_dissection.certificate_stub.v1",
    }
    for problem_id, executor_id in expected.items():
        metadata = problems[problem_id].metadata["domain_search_executors"][0]
        assert metadata["executor_id"] == executor_id
        assert metadata["deterministic"] is True
        assert metadata["bounded"] is True


def test_problem_bank_can_be_loaded_with_full_executor_metadata(tmp_path: Path) -> None:
    bank_path = tmp_path / "bank.yaml"
    from amra.problem_banks.registry import save_problem_bank

    save_problem_bank(
        [
            ProblemRecord(
                problem_id="triangle-dissection-fixture",
                title="Triangle dissection fixture",
                source="unit",
                statement="Determine whether a triangle can be dissected into 19 congruent triangles.",
                domain="geometry",
                tags=["geometry", "finite_case"],
            )
        ],
        bank_path,
    )

    loaded = load_problem_bank_with_executor_metadata(bank_path)
    metadata = loaded[0].metadata["domain_search_executors"][0]

    assert metadata["executor_id"] == "triangle_dissection.certificate_stub.v1"
    assert metadata["description"]
    assert metadata["default_parameters"] == {"max_cases": 20}
