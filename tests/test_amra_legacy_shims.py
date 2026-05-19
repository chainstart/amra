from __future__ import annotations

import ast
import importlib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "amra_legacy_module_disposition.zh.md"

MODULE_ALIAS_SHIMS = {
    "ara_math.models": "amra.core.models",
    "ara_math.workspace": "amra.core.workspace",
    "ara_math.runtime": "amra.infra.runtime",
    "ara_math.context": "amra.core.context",
    "ara_math.problem_bank": "amra.problem_banks.registry",
    "ara_math.artifact_graph": "amra.core.artifact_graph",
    "ara_math.lean_audit": "amra.lean.audit",
    "ara_math.lean_contract": "amra.lean.contract",
    "ara_math.agent_tools": "amra.agents.tools",
}

MIGRATED_SHIM_FILES = {
    Path("src/ara_math/models.py"): "amra.core.models",
    Path("src/ara_math/workspace.py"): "amra.core.workspace",
    Path("src/ara_math/runtime.py"): "amra.infra.runtime",
    Path("src/ara_math/context.py"): "amra.core.context",
    Path("src/ara_math/problem_bank.py"): "amra.problem_banks.registry",
    Path("src/ara_math/artifact_graph.py"): "amra.core.artifact_graph",
    Path("src/ara_math/lean_audit.py"): "amra.lean.audit",
    Path("src/ara_math/lean_contract.py"): "amra.lean.contract",
    Path("src/ara_math/agent_tools.py"): "amra.agents.tools",
    Path("src/ara_math/ara_library.py"): "amra.amra_library",
    Path("src/ara_math/proof_state.py"): "amra.proof.state",
    Path("src/ara_math/pure_agents.py"): "amra.agents",
}

TEMPORARY_AMRA_LEGACY_IMPORTS = {
    Path("src/amra/cli.py"): {"ara_math.cli"},
    Path("src/amra/core/artifact_graph.py"): {"ara_math.workstreams"},
    Path("src/amra/core/workspace.py"): {"ara_math.coordinator"},
    Path("src/amra/lean/executor.py"): {"ara_math.lean"},
    Path("src/amra/math_scout.py"): {"ara_math.math_scout"},
    Path("src/amra/portfolio_campaign.py"): {"ara_math.math_scout"},
    Path("src/amra/problem_banks/registry.py"): {"ara_math.erdos_status"},
    Path("src/amra/proof/focused_attack.py"): {"ara_math.focused_attack"},
}


def _absolute_import_targets(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    targets: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            targets.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            targets.add(node.module)
            targets.update(
                f"{node.module}.{alias.name}"
                for alias in node.names
                if alias.name != "*"
            )
    return targets


def _legacy_import_targets(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    targets: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            targets.update(
                alias.name
                for alias in node.names
                if alias.name == "ara_math" or alias.name.startswith("ara_math.")
            )
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            if node.module == "ara_math":
                targets.update(
                    "ara_math.*" if alias.name == "*" else f"ara_math.{alias.name}"
                    for alias in node.names
                )
            elif node.module.startswith("ara_math."):
                targets.add(node.module)
    return targets


def test_migrated_legacy_shim_sources_are_deprecated_canonical_imports() -> None:
    for relative_path, canonical_module in MIGRATED_SHIM_FILES.items():
        path = REPO_ROOT / relative_path
        source = path.read_text(encoding="utf-8")
        imports = _absolute_import_targets(path)

        assert "Deprecated" in source or "deprecated" in source
        assert not _legacy_import_targets(path), f"{relative_path} still imports ara_math"
        assert any(
            imported == canonical_module or imported.startswith(f"{canonical_module}.")
            for imported in imports
        ), f"{relative_path} does not import {canonical_module}"


def test_module_alias_shims_share_canonical_module_identity() -> None:
    for legacy_name, canonical_name in MODULE_ALIAS_SHIMS.items():
        assert importlib.import_module(legacy_name) is importlib.import_module(canonical_name)


def test_reexport_shim_symbols_are_canonical() -> None:
    legacy_library = importlib.import_module("ara_math.ara_library")
    canonical_library = importlib.import_module("amra.amra_library")
    assert legacy_library.AmraLibraryManager is canonical_library.AmraLibraryManager
    assert legacy_library.LegacyAraLibraryManager is canonical_library.LegacyAraLibraryManager
    assert issubclass(legacy_library.AraLibraryManager, canonical_library.LegacyAraLibraryManager)

    legacy_state = importlib.import_module("ara_math.proof_state")
    canonical_state = importlib.import_module("amra.proof.state")
    canonical_memory = importlib.import_module("amra.portfolio_memory")
    assert legacy_state.ProofArtifactTracker is canonical_state.ProofArtifactTracker
    assert legacy_state.retrieve_failed_routes is canonical_memory.retrieve_failed_routes
    assert legacy_state.consolidate_memory is canonical_memory.consolidate_memory

    legacy_agents = importlib.import_module("ara_math.pure_agents")
    canonical_episode_loop = importlib.import_module("amra.agents.episode_loop")
    canonical_lean = importlib.import_module("amra.agents.lean")
    canonical_proof = importlib.import_module("amra.agents.proof")
    canonical_tools = importlib.import_module("amra.agents.tools")
    assert legacy_agents.CodexEpisodeLoopAgent is canonical_episode_loop.CodexEpisodeLoopAgent
    assert legacy_agents.LeanFromNaturalProofAgent is canonical_lean.LeanFromNaturalProofAgent
    assert legacy_agents.NaturalLanguageTheoremProverAgent is canonical_proof.NaturalLanguageTheoremProverAgent
    assert legacy_agents.UnifiedProofAgentLoop is canonical_proof.UnifiedProofAgentLoop
    assert legacy_agents.ToolRegistry is canonical_tools.ToolRegistry


def test_src_amra_legacy_imports_are_documented_temporary_exceptions() -> None:
    observed = {
        path.relative_to(REPO_ROOT): legacy_imports
        for path in sorted((REPO_ROOT / "src" / "amra").rglob("*.py"))
        if (legacy_imports := _legacy_import_targets(path))
    }

    assert observed == TEMPORARY_AMRA_LEGACY_IMPORTS

    disposition_doc = DOC_PATH.read_text(encoding="utf-8")
    missing_docs = [
        f"{relative_path}:{legacy_import}"
        for relative_path, legacy_imports in TEMPORARY_AMRA_LEGACY_IMPORTS.items()
        for legacy_import in sorted(legacy_imports)
        if f"`{relative_path.as_posix()}`" not in disposition_doc
        or f"`{legacy_import}`" not in disposition_doc
    ]
    assert not missing_docs
