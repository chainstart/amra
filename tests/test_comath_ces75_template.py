import json
from pathlib import Path

from ara_math.cli import main
from ara_math.coordinator import (
    CES75_DENSE_BLOCKER_ID,
    bootstrap_ces75_erdos866_workstreams,
    comath_paths,
    select_next_workstreams,
)
from ara_math.workspace import write_text


def _write_minimal_ces75_project(project_dir: Path) -> Path:
    lean_file = project_dir / "formal" / "MathProject" / "MainClaim.lean"
    write_text(
        lean_file,
        "\n".join(
            [
                "namespace MathProject",
                "theorem erdos866_g6_sqrt_order_of_CES75_theorem4_integer_source : True := by",
                "  trivial",
                "end MathProject",
                "",
            ]
        ),
    )
    write_text(project_dir / "idea" / "exact_statement.md", "Placeholder statement.\n")
    return lean_file


def test_bootstrap_ces75_template_creates_four_workstreams_without_touching_lean(tmp_path: Path) -> None:
    project_dir = tmp_path / "erdos-866-ai-continuation-20260505"
    lean_file = _write_minimal_ces75_project(project_dir)
    before = lean_file.read_text(encoding="utf-8")

    payload = bootstrap_ces75_erdos866_workstreams(project_dir, repo_root=Path.cwd())
    paths = comath_paths(project_dir)
    state = json.loads(paths.project_state.read_text(encoding="utf-8"))
    dashboard = paths.dashboard.read_text(encoding="utf-8")
    graph = json.loads(paths.artifact_graph.read_text(encoding="utf-8"))
    ledger = json.loads(paths.uncertainty_ledger.read_text(encoding="utf-8"))
    selected = select_next_workstreams(project_dir, limit=1)

    assert lean_file.read_text(encoding="utf-8") == before
    assert payload["top_blocker_id"] == CES75_DENSE_BLOCKER_ID
    assert state["top_blocker_id"] == CES75_DENSE_BLOCKER_ID
    assert [item["workstream_id"] for item in state["workstreams"]] == [
        "source-dense-central-block",
        "lean-current-final-window",
        "source-audit-ces75-theorem4",
        "global-review",
    ]
    assert state["workstreams"][3]["dependencies"] == [
        "source-dense-central-block",
        "lean-current-final-window",
        "source-audit-ces75-theorem4",
    ]
    assert "Dense central block theorem is the current source-level blocker" in dashboard
    assert selected[0].workstream_id == "source-dense-central-block"
    assert any(node["node_id"] == "lean-final-window-mainclaim" for node in graph["nodes"])
    assert any(item["item_id"] == CES75_DENSE_BLOCKER_ID for item in ledger["items"])
    assert (paths.workstream_dir("source-dense-central-block") / "report.md").exists()


def test_bootstrap_ces75_template_cli_uses_local_project_path(tmp_path: Path, capsys) -> None:
    project_dir = tmp_path / "ces75-cli"
    lean_file = _write_minimal_ces75_project(project_dir)
    before = lean_file.read_text(encoding="utf-8")

    exit_code = main(["--json", "bootstrap-ces75-comath", "--project", str(project_dir)])
    payload = json.loads(capsys.readouterr().out)
    state = json.loads((project_dir / "comath" / "project_state.json").read_text(encoding="utf-8"))

    assert exit_code == 0
    assert payload["top_blocker_id"] == CES75_DENSE_BLOCKER_ID
    assert len(payload["workstreams"]) == 4
    assert state["workstreams"][0]["workstream_id"] == "source-dense-central-block"
    assert lean_file.read_text(encoding="utf-8") == before
