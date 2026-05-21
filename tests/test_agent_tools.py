from __future__ import annotations

import importlib
import json
from pathlib import Path

from ara_math.agent_tools import (
    AMRA_AGENT_RUN_DIR_ENV,
    AMRA_AGENT_WORKSPACE_ENV,
    LEGACY_AGENT_RUN_DIR_ENV,
    LEGACY_AGENT_WORKSPACE_ENV,
    ToolRegistry,
    ToolSpec,
    agent_environment,
)


def test_legacy_agent_tools_aliases_canonical_module() -> None:
    legacy = importlib.import_module("ara_math.agent_tools")
    canonical = importlib.import_module("amra.agents.tools")

    assert legacy is canonical
    assert ToolRegistry is canonical.ToolRegistry
    assert ToolSpec is canonical.ToolSpec
    assert agent_environment is canonical.agent_environment


def test_tool_registry_uses_amra_environment_contract(tmp_path: Path) -> None:
    workspace = tmp_path / "formal"
    workspace.mkdir()
    (workspace / "lean-toolchain").write_text("leanprover/lean4:v4.12.0\n", encoding="utf-8")

    registry = ToolRegistry(build_command=["lake", "build", "MathProject"])
    payload = registry.to_dict()
    templates = "\n".join(
        template
        for tool in payload["tools"]
        for template in tool["command_templates"]
    )

    assert AMRA_AGENT_RUN_DIR_ENV in templates
    assert AMRA_AGENT_WORKSPACE_ENV in templates
    assert LEGACY_AGENT_RUN_DIR_ENV not in templates
    assert LEGACY_AGENT_WORKSPACE_ENV not in templates
    assert payload["environment_variables"] == {
        "run_dir": AMRA_AGENT_RUN_DIR_ENV,
        "workspace": AMRA_AGENT_WORKSPACE_ENV,
        "legacy_run_dir": LEGACY_AGENT_RUN_DIR_ENV,
        "legacy_workspace": LEGACY_AGENT_WORKSPACE_ENV,
    }

    snapshot = registry.write_artifacts(tmp_path / "run", workspace=workspace, install_missing_math_tools=False)
    artifact_payload = json.loads((tmp_path / "run" / "tool_registry.json").read_text(encoding="utf-8"))
    markdown = (tmp_path / "run" / "tool_registry.md").read_text(encoding="utf-8")

    assert artifact_payload["registry"]["environment_variables"] == payload["environment_variables"]
    assert artifact_payload["registry"]["math_tools_profile"] == "essential"
    assert "math_tools" in artifact_payload
    assert snapshot["environment_variables"] == payload["environment_variables"]
    assert snapshot["math_tools"]["profile"] == "essential"
    assert artifact_payload["environment"]["workspace"]["toolchain"] == "leanprover/lean4:v4.12.0"
    assert f"${AMRA_AGENT_RUN_DIR_ENV}" in markdown
    assert "legacy ARA aliases remain available" in markdown
