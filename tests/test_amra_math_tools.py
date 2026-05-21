from __future__ import annotations

import json
from pathlib import Path

from amra.math_tools import MATH_TOOL_REPORT_SCHEMA_VERSION, ensure_math_tools, selected_tool_specs


def test_selected_math_tool_profiles_expand_by_scope() -> None:
    essential = {spec.tool_id for spec in selected_tool_specs("essential")}
    extended = {spec.tool_id for spec in selected_tool_specs("extended")}
    full = {spec.tool_id for spec in selected_tool_specs("full")}

    assert {"python_math_stack", "z3", "lean4"} <= essential
    assert essential < extended
    assert extended < full
    assert "sagemath" in full


def test_ensure_math_tools_writes_durable_report_without_installing(tmp_path: Path) -> None:
    report = ensure_math_tools(
        output_dir=tmp_path,
        profile="essential",
        install_missing=False,
        run_smoke=False,
    )

    assert report["schema_version"] == MATH_TOOL_REPORT_SCHEMA_VERSION
    assert report["profile"] == "essential"
    assert report["install_missing"] is False
    assert (tmp_path / "math_tools_report.json").exists()
    assert (tmp_path / "math_tools_report.md").exists()
    payload = json.loads((tmp_path / "math_tools_report.json").read_text(encoding="utf-8"))
    assert payload["available_tool_ids"] == report["available_tool_ids"]
    assert "Agent Guidance" in (tmp_path / "math_tools_report.md").read_text(encoding="utf-8")
