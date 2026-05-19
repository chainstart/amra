from pathlib import Path

from amra.core.models import ProblemRecord
from amra.problem_banks.registry import import_erdos_open_problems, load_problem_bank, refresh_erdos_problem_bank


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
