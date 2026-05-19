"""Canonical inventory and import audit for the ``ara_math`` migration."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any


InventoryEntry = dict[str, Any]


LEGACY_MODULE_INVENTORY: dict[str, InventoryEntry] = {
    "__init__.py": {
        "module": "ara_math",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("shim",),
        "canonical_target": "amra",
        "migration_blocked_by": (),
        "shim_kind": "package_metadata",
    },
    "__main__.py": {
        "module": "ara_math.__main__",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("shim",),
        "canonical_target": "amra.cli",
        "migration_blocked_by": (),
        "shim_kind": "entrypoint_forwarder",
    },
    "accessibility.py": {
        "module": "ara_math.accessibility",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("move",),
        "canonical_target": "amra.proof.accessibility",
        "migration_blocked_by": ("AMRA-PROOF-RUNNERS-MIGRATION-001",),
    },
    "agent_tools.py": {
        "module": "ara_math.agent_tools",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("move",),
        "canonical_target": "amra.agents.tools",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "ara_library.py": {
        "module": "ara_math.ara_library",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("move", "shim"),
        "canonical_target": "amra.amra_library",
        "migration_blocked_by": (),
        "shim_kind": "symbol_reexport",
    },
    "artifact_graph.py": {
        "module": "ara_math.artifact_graph",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("keep-core",),
        "canonical_target": "amra.core.artifact_graph",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "banking.py": {
        "module": "ara_math.banking",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("move",),
        "canonical_target": "amra.problem_banks.sync",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "campaign_loop.py": {
        "module": "ara_math.campaign_loop",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("move",),
        "canonical_target": "amra.proof.campaign_loop",
        "migration_blocked_by": ("AMRA-PROOF-RUNNERS-MIGRATION-001",),
    },
    "cli.py": {
        "module": "ara_math.cli",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("split", "shim"),
        "canonical_target": "amra.cli",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "closure.py": {
        "module": "ara_math.closure",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("move",),
        "canonical_target": "amra.proof.closure",
        "migration_blocked_by": ("AMRA-PROOF-RUNNERS-MIGRATION-001",),
    },
    "comath_benchmarks.py": {
        "module": "ara_math.comath_benchmarks",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("merge",),
        "canonical_target": "amra.evaluation.benchmarks",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "comath_capabilities.py": {
        "module": "ara_math.comath_capabilities",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("split", "merge"),
        "canonical_target": "amra.evaluation.capabilities",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "comath_runners.py": {
        "module": "ara_math.comath_runners",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("split", "merge"),
        "canonical_target": "amra.scheduler.executors",
        "migration_blocked_by": ("AMRA-ORCHESTRATION-MIGRATION-001",),
    },
    "comath_source_audit.py": {
        "module": "ara_math.comath_source_audit",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("move",),
        "canonical_target": "amra.sources.source_audit",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "comath_specialists.py": {
        "module": "ara_math.comath_specialists",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("move", "split"),
        "canonical_target": "amra.evaluation.specialists",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "context.py": {
        "module": "ara_math.context",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("keep-core",),
        "canonical_target": "amra.core.context",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "convergence.py": {
        "module": "ara_math.convergence",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("merge",),
        "canonical_target": "amra.evaluation.convergence",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "coordinator.py": {
        "module": "ara_math.coordinator",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("split", "merge"),
        "canonical_target": "amra.orchestration",
        "migration_blocked_by": ("AMRA-ORCHESTRATION-MIGRATION-001",),
    },
    "deliverables.py": {
        "module": "ara_math.deliverables",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("deprecate", "merge"),
        "canonical_target": "amra.result_bundle",
        "migration_blocked_by": ("AMRA-SOURCES-EVALUATION-MIGRATION-001",),
    },
    "erdos_status.py": {
        "module": "ara_math.erdos_status",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("move",),
        "canonical_target": "amra.problem_banks.erdos",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "evaluator.py": {
        "module": "ara_math.evaluator",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("merge",),
        "canonical_target": "amra.evaluation.evaluator",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "focused_attack.py": {
        "module": "ara_math.focused_attack",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("move",),
        "canonical_target": "amra.proof.focused_attack",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "formalization.py": {
        "module": "ara_math.formalization",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("merge",),
        "canonical_target": "amra.lean.formalization",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "goal_campaign.py": {
        "module": "ara_math.goal_campaign",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("merge",),
        "canonical_target": "amra.proof.goal_campaign",
        "migration_blocked_by": ("AMRA-PROOF-RUNNERS-MIGRATION-001",),
    },
    "lean.py": {
        "module": "ara_math.lean",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("keep-core", "split"),
        "canonical_target": "amra.lean.executor",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "lean_audit.py": {
        "module": "ara_math.lean_audit",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("keep-core",),
        "canonical_target": "amra.lean.audit",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "lean_contract.py": {
        "module": "ara_math.lean_contract",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("keep-core",),
        "canonical_target": "amra.lean.contract",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "lean_formalizer.py": {
        "module": "ara_math.lean_formalizer",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("move",),
        "canonical_target": "amra.lean.formalizer",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "literature.py": {
        "module": "ara_math.literature",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("split",),
        "canonical_target": "amra.sources.literature",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "math_attack.py": {
        "module": "ara_math.math_attack",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("merge",),
        "canonical_target": "amra.proof.attack",
        "migration_blocked_by": ("AMRA-PROOF-RUNNERS-MIGRATION-001",),
    },
    "math_scout.py": {
        "module": "ara_math.math_scout",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("move",),
        "canonical_target": "amra.math_scout",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "models.py": {
        "module": "ara_math.models",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("keep-core",),
        "canonical_target": "amra.core.models",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "obligation_refiner.py": {
        "module": "ara_math.obligation_refiner",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("merge",),
        "canonical_target": "amra.scheduler.obligations",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "orchestrator.py": {
        "module": "ara_math.orchestrator",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("split", "deprecate"),
        "canonical_target": "amra.orchestration",
        "migration_blocked_by": (
            "AMRA-ORCHESTRATION-MIGRATION-001",
            "AMRA-CANONICAL-CLI-ORCHESTRATOR-001",
        ),
    },
    "planning.py": {
        "module": "ara_math.planning",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("merge",),
        "canonical_target": "amra.proof.routes",
        "migration_blocked_by": ("AMRA-PROOF-RUNNERS-MIGRATION-001",),
    },
    "problem_bank.py": {
        "module": "ara_math.problem_bank",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("keep-core",),
        "canonical_target": "amra.problem_banks.registry",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "proof_lab.py": {
        "module": "ara_math.proof_lab",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("move",),
        "canonical_target": "amra.proof.lab",
        "migration_blocked_by": ("AMRA-PROOF-RUNNERS-MIGRATION-001",),
    },
    "proof_search.py": {
        "module": "ara_math.proof_search",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("split", "move"),
        "canonical_target": "amra.proof.search",
        "migration_blocked_by": ("AMRA-PROOF-RUNNERS-MIGRATION-001",),
    },
    "proof_state.py": {
        "module": "ara_math.proof_state",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("keep-core",),
        "canonical_target": "amra.proof.state",
        "migration_blocked_by": (),
        "shim_kind": "symbol_reexport",
    },
    "proof_system.py": {
        "module": "ara_math.proof_system",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("merge",),
        "canonical_target": "amra.proof.agenda",
        "migration_blocked_by": ("AMRA-PROOF-RUNNERS-MIGRATION-001",),
    },
    "pure_agents.py": {
        "module": "ara_math.pure_agents",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("split", "move"),
        "canonical_target": "amra.agents",
        "migration_blocked_by": (),
        "shim_kind": "symbol_reexport",
    },
    "retrieval.py": {
        "module": "ara_math.retrieval",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("move",),
        "canonical_target": "amra.retrieval",
        "migration_blocked_by": ("AMRA-PROOF-RUNNERS-MIGRATION-001",),
    },
    "review.py": {
        "module": "ara_math.review",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("merge",),
        "canonical_target": "amra.review.project_review",
        "migration_blocked_by": ("AMRA-ORCHESTRATION-MIGRATION-001",),
    },
    "review_gate.py": {
        "module": "ara_math.review_gate",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("keep-core", "move"),
        "canonical_target": "amra.review.gates",
        "migration_blocked_by": ("AMRA-ORCHESTRATION-MIGRATION-001",),
    },
    "runtime.py": {
        "module": "ara_math.runtime",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("keep-core",),
        "canonical_target": "amra.infra.runtime",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "scouting.py": {
        "module": "ara_math.scouting",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("merge",),
        "canonical_target": "amra.evaluation.scouting",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "strategy.py": {
        "module": "ara_math.strategy",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("merge",),
        "canonical_target": "amra.evaluation.strategy",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "uncertainty.py": {
        "module": "ara_math.uncertainty",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("merge",),
        "canonical_target": "amra.portfolio_memory",
        "migration_blocked_by": ("AMRA-ORCHESTRATION-MIGRATION-001",),
    },
    "workspace.py": {
        "module": "ara_math.workspace",
        "implementation_status": "shim",
        "cleanup_status": "retain_compatibility",
        "disposition": ("keep-core", "split"),
        "canonical_target": "amra.core.workspace",
        "migration_blocked_by": (),
        "shim_kind": "module_alias",
    },
    "workstreams.py": {
        "module": "ara_math.workstreams",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("merge",),
        "canonical_target": "amra.orchestration.workstreams",
        "migration_blocked_by": ("AMRA-ORCHESTRATION-MIGRATION-001",),
    },
    "writing.py": {
        "module": "ara_math.writing",
        "implementation_status": "active_implementation",
        "cleanup_status": "delete_later",
        "disposition": ("deprecate", "merge"),
        "canonical_target": "amra.result_bundle.writing_brief",
        "migration_blocked_by": ("AMRA-SOURCES-EVALUATION-MIGRATION-001",),
    },
}


TEMPORARY_AMRA_LEGACY_IMPORTS: dict[str, tuple[str, ...]] = {
    "src/amra/cli.py": (
        "ara_math.banking",
        "ara_math.campaign_loop",
        "ara_math.comath_benchmarks",
        "ara_math.comath_capabilities",
        "ara_math.comath_source_audit",
        "ara_math.comath_specialists",
        "ara_math.coordinator",
        "ara_math.goal_campaign",
        "ara_math.orchestrator",
        "ara_math.proof_lab",
        "ara_math.scouting",
        "ara_math.workstreams",
    ),
    "src/amra/core/artifact_graph.py": ("ara_math.workstreams",),
    "src/amra/core/workspace.py": ("ara_math.coordinator",),
}


def module_alias_shims() -> dict[str, str]:
    """Return legacy module aliases that should share canonical module identity."""

    return {
        entry["module"]: entry["canonical_target"]
        for entry in LEGACY_MODULE_INVENTORY.values()
        if entry.get("shim_kind") == "module_alias"
    }


def migrated_shim_files() -> dict[str, str]:
    """Return shim file paths with their canonical target modules."""

    return {
        f"src/ara_math/{filename}": entry["canonical_target"]
        for filename, entry in LEGACY_MODULE_INVENTORY.items()
        if entry["implementation_status"] == "shim"
        and entry.get("shim_kind") in {"module_alias", "symbol_reexport"}
    }


def collect_legacy_import_targets(path: Path) -> set[str]:
    """Collect absolute ``ara_math`` import targets from a Python source file."""

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


def collect_amra_legacy_imports(repo_root: Path) -> dict[str, tuple[str, ...]]:
    """Collect all canonical ``src/amra`` imports that target ``ara_math``."""

    observed: dict[str, tuple[str, ...]] = {}
    for path in sorted((repo_root / "src" / "amra").rglob("*.py")):
        imports = collect_legacy_import_targets(path)
        if imports:
            observed[path.relative_to(repo_root).as_posix()] = tuple(sorted(imports))
    return observed


def undeclared_amra_legacy_imports(repo_root: Path) -> dict[str, tuple[str, ...]]:
    """Return ``src/amra`` legacy imports not declared as temporary exceptions."""

    undeclared: dict[str, tuple[str, ...]] = {}
    observed = collect_amra_legacy_imports(repo_root)
    for relative_path, imports in observed.items():
        allowed = TEMPORARY_AMRA_LEGACY_IMPORTS.get(relative_path, ())
        missing = [
            target
            for target in imports
            if not any(
                target == allowed_target or target.startswith(f"{allowed_target}.")
                for allowed_target in allowed
            )
        ]
        if missing:
            undeclared[relative_path] = tuple(missing)
    return undeclared
