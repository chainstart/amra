from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path


def _load_script_module():
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "imo_proofbench_campaign.py"
    spec = importlib.util.spec_from_file_location("imo_proofbench_campaign_script", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_proofbench_csv(path: Path) -> None:
    rows = [
        {
            "Problem ID": "PB-Advanced-012",
            "Problem": "Prove n >= 5.",
            "Solution": "Reference route.",
            "Grading guidelines": "Guidelines.",
            "Category": "Number theory",
            "Level": "IMO-hard",
            "Short Answer": "",
            "Source": "Novel Problem",
        },
        {
            "Problem ID": "PB-Advanced-024",
            "Problem": "Find the maximum number of values.",
            "Solution": "Reference route.",
            "Grading guidelines": "Guidelines.",
            "Category": "Algebra",
            "Level": "IMO-hard",
            "Short Answer": "2",
            "Source": "(Modified) IMO 2024 P6",
        },
        {
            "Problem ID": "PB-Basic-001",
            "Problem": "Easy problem.",
            "Solution": "",
            "Grading guidelines": "",
            "Category": "Algebra",
            "Level": "IMO-easy",
            "Short Answer": "",
            "Source": "Fixture",
        },
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def test_selects_hard_problems_from_csv(tmp_path: Path) -> None:
    module = _load_script_module()
    csv_path = tmp_path / "proofbench.csv"
    _write_proofbench_csv(csv_path)

    records = module.load_proofbench(csv_path)
    selected = module.select_problems(
        records,
        problem_ids=[],
        level="IMO-hard",
        categories=[],
        limit=2,
        exclude_ids=set(),
    )

    assert [record.problem_id for record in selected] == ["PB-Advanced-012", "PB-Advanced-024"]


def test_prepare_curated_workspace_writes_target_contract(tmp_path: Path) -> None:
    module = _load_script_module()
    csv_path = tmp_path / "proofbench.csv"
    _write_proofbench_csv(csv_path)
    record = module.load_proofbench(csv_path)[0]

    prepared = module.prepare_problem(record=record, run_root=tmp_path / "run", include_reference=False)

    target_path = prepared.workspace / prepared.target_file
    assert target_path.exists()
    assert prepared.target_theorem == "pb_advanced_012_main"
    assert "theorem pb_advanced_012_main" in target_path.read_text(encoding="utf-8")
    assert "theorem pb_advanced_012_main" in prepared.expected_header_path.read_text(encoding="utf-8")
    assert prepared.context_paths == [prepared.expected_header_path]
    assert not prepared.reference_path.exists()
    problem_payload = module.json.loads((prepared.problem_dir / "input" / "problem.json").read_text(encoding="utf-8"))
    assert problem_payload["solution"] == ""
    assert problem_payload["grading_guidelines"] == ""
    assert problem_payload["short_answer"] == ""


def test_closed_book_campaign_rejects_web_search(tmp_path: Path) -> None:
    module = _load_script_module()
    csv_path = tmp_path / "proofbench.csv"
    _write_proofbench_csv(csv_path)

    args = module.build_parser().parse_args(
        [
            "--proofbench-csv",
            str(csv_path),
            "--output-root",
            str(tmp_path / "runs"),
            "--problem-id",
            "PB-Advanced-012",
            "--dry-run",
            "--backend",
            "none",
            "--search",
        ]
    )

    try:
        module.run_campaign(args)
    except ValueError as exc:
        assert "disabled for IMO-ProofBench benchmark campaigns" in str(exc)
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("closed-book benchmark accepted --search")


def test_dry_run_campaign_prepares_selected_problem_dirs(tmp_path: Path) -> None:
    module = _load_script_module()
    csv_path = tmp_path / "proofbench.csv"
    _write_proofbench_csv(csv_path)

    args = module.build_parser().parse_args(
        [
            "--proofbench-csv",
            str(csv_path),
            "--output-root",
            str(tmp_path / "runs"),
            "--problem-id",
            "PB-Advanced-012",
            "--problem-id",
            "PB-Advanced-024",
            "--dry-run",
            "--backend",
            "none",
        ]
    )
    state = module.run_campaign(args)

    assert state["status"] == "prepared"
    assert state["selected_problem_ids"] == ["PB-Advanced-012", "PB-Advanced-024"]
    assert state["supervisor_backend"] == "none"
    assert state["include_reference"] is False
    assert state["external_source_policy"] == "closed_book_no_web_no_reference_solution"
    assert len(state["problems"]) == 2
    for problem in state["problems"]:
        assert Path(problem["workspace"]).exists()
