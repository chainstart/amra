from __future__ import annotations

import ast
import importlib
from pathlib import Path

from amra.legacy_migration import collect_amra_legacy_imports


REPO_ROOT = Path(__file__).resolve().parents[1]


def _absolute_import_targets(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    targets: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            targets.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            targets.add(node.module)
    return targets


def test_canonical_amra_cli_imports_only_canonical_modules() -> None:
    imports = _absolute_import_targets(REPO_ROOT / "src" / "amra" / "cli.py")

    assert not {target for target in imports if target == "ara_math" or target.startswith("ara_math.")}
    assert "amra.orchestrator" in imports
    assert "amra.proof.lab" in imports
    assert "amra.proof.campaign_loop" in imports
    assert "amra.lean.formalizer" in imports
    assert "amra.result_bundle" in imports


def test_canonical_amra_tree_has_no_temporary_legacy_imports() -> None:
    assert collect_amra_legacy_imports(REPO_ROOT) == {}


def test_legacy_cli_and_orchestrator_forward_to_canonical_modules() -> None:
    assert importlib.import_module("ara_math.cli") is importlib.import_module("amra.cli")
    assert importlib.import_module("ara_math.orchestrator") is importlib.import_module("amra.orchestrator")
