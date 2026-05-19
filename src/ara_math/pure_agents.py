"""Deprecated compatibility shim for canonical AMRA proof-agent runners."""

from __future__ import annotations

from amra.agents.episode_loop import (
    CodexEpisodeConfig,
    CodexEpisodeLoopAgent,
    EpisodeObserver,
    _count_lean_pattern,
    _extract_lean_target_name,
    _extract_next,
    _extract_status,
    _iter_project_lean_files,
    _lean_target_exists,
    _new_run_dir,
    _resolve_loose,
    _run_command,
    _strip_lean_comments,
    _tail,
    read_text,
    slugify,
    utc_now_iso,
    write_json,
    write_text,
)
from amra.agents.env import (
    AMRA_AGENT_RUN_DIR_ENV,
    AMRA_AGENT_WORKSPACE_ENV,
    LEGACY_AGENT_RUN_DIR_ENV,
    LEGACY_AGENT_WORKSPACE_ENV,
    agent_environment,
)
from amra.agents.lean import LeanFromNaturalProofAgent
from amra.agents.proof import NaturalLanguageTheoremProverAgent, UnifiedProofAgentLoop
from amra.agents.tools import ToolRegistry, ToolSpec
from amra.proof.state import ProofArtifactTracker

__all__ = [
    "AMRA_AGENT_RUN_DIR_ENV",
    "AMRA_AGENT_WORKSPACE_ENV",
    "CodexEpisodeConfig",
    "CodexEpisodeLoopAgent",
    "EpisodeObserver",
    "LEGACY_AGENT_RUN_DIR_ENV",
    "LEGACY_AGENT_WORKSPACE_ENV",
    "NaturalLanguageTheoremProverAgent",
    "LeanFromNaturalProofAgent",
    "UnifiedProofAgentLoop",
    "ToolRegistry",
    "ToolSpec",
    "ProofArtifactTracker",
    "agent_environment",
    "utc_now_iso",
    "slugify",
    "read_text",
    "write_text",
    "write_json",
    "_resolve_loose",
    "_tail",
    "_new_run_dir",
    "_extract_status",
    "_extract_next",
    "_strip_lean_comments",
    "_iter_project_lean_files",
    "_extract_lean_target_name",
    "_lean_target_exists",
    "_count_lean_pattern",
    "_run_command",
]
