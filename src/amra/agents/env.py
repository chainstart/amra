from __future__ import annotations

from pathlib import Path


AMRA_AGENT_RUN_DIR_ENV = "AMRA_AGENT_RUN_DIR"
AMRA_AGENT_WORKSPACE_ENV = "AMRA_AGENT_WORKSPACE"
LEGACY_AGENT_RUN_DIR_ENV = "ARA_PURE_AGENT_RUN_DIR"
LEGACY_AGENT_WORKSPACE_ENV = "ARA_PURE_AGENT_WORKSPACE"


def agent_environment(*, run_dir: Path, workspace: Path) -> dict[str, str]:
    run_dir_value = str(run_dir)
    workspace_value = str(workspace)
    return {
        AMRA_AGENT_RUN_DIR_ENV: run_dir_value,
        AMRA_AGENT_WORKSPACE_ENV: workspace_value,
        LEGACY_AGENT_RUN_DIR_ENV: run_dir_value,
        LEGACY_AGENT_WORKSPACE_ENV: workspace_value,
    }


__all__ = [
    "AMRA_AGENT_RUN_DIR_ENV",
    "AMRA_AGENT_WORKSPACE_ENV",
    "LEGACY_AGENT_RUN_DIR_ENV",
    "LEGACY_AGENT_WORKSPACE_ENV",
    "agent_environment",
]
