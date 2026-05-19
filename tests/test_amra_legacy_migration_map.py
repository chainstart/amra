from __future__ import annotations

import json
import re
from pathlib import Path

from amra.legacy_migration import (
    LEGACY_MODULE_INVENTORY,
    TEMPORARY_AMRA_LEGACY_IMPORTS,
    collect_amra_legacy_imports,
    module_alias_shims,
    undeclared_amra_legacy_imports,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "amra_legacy_module_disposition.zh.md"

IMPLEMENTATION_STATUSES = {"shim"}
CLEANUP_STATUSES = {"retain_compatibility"}
DISPOSITIONS = {
    "keep-core",
    "move",
    "split",
    "merge",
    "deprecate",
    "shim",
    "delete-later",
}


def _doc_disposition_rows() -> dict[str, tuple[str, ...]]:
    rows: dict[str, tuple[str, ...]] = {}
    for line in DOC_PATH.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        match = re.fullmatch(r"`([^`]+\.py)`", cells[0])
        if not match:
            continue
        rows[match.group(1)] = tuple(label for label in cells[3].strip("`").split("+") if label)
    return rows


def test_legacy_migration_inventory_covers_every_ara_math_module() -> None:
    live_files = {path.name for path in (REPO_ROOT / "src" / "ara_math").glob("*.py")}

    assert set(LEGACY_MODULE_INVENTORY) == live_files
    assert len(LEGACY_MODULE_INVENTORY) == 51


def test_legacy_migration_inventory_is_machine_readable_and_classified() -> None:
    json.dumps(LEGACY_MODULE_INVENTORY, sort_keys=True)

    statuses = {entry["implementation_status"] for entry in LEGACY_MODULE_INVENTORY.values()}
    cleanup_statuses = {entry["cleanup_status"] for entry in LEGACY_MODULE_INVENTORY.values()}

    assert statuses == IMPLEMENTATION_STATUSES
    assert cleanup_statuses == CLEANUP_STATUSES

    for filename, entry in LEGACY_MODULE_INVENTORY.items():
        assert entry["module"].startswith("ara_math")
        assert entry["canonical_target"].startswith("amra")
        assert entry["implementation_status"] in IMPLEMENTATION_STATUSES
        assert entry["cleanup_status"] in CLEANUP_STATUSES
        assert set(entry["disposition"]) <= DISPOSITIONS
        assert entry["cleanup_status"] == "retain_compatibility", filename
        assert entry["migration_blocked_by"] == (), filename


def test_legacy_migration_inventory_matches_disposition_doc_table() -> None:
    doc_rows = _doc_disposition_rows()

    assert set(doc_rows) == set(LEGACY_MODULE_INVENTORY)
    assert {
        filename: tuple(entry["disposition"])
        for filename, entry in LEGACY_MODULE_INVENTORY.items()
    } == doc_rows


def test_canonical_import_audit_blocks_undeclared_ara_math_dependencies() -> None:
    assert collect_amra_legacy_imports(REPO_ROOT) == TEMPORARY_AMRA_LEGACY_IMPORTS
    assert undeclared_amra_legacy_imports(REPO_ROOT) == {}


def test_module_alias_shim_inventory_matches_importable_compatibility_set() -> None:
    aliases = module_alias_shims()

    assert aliases["ara_math.cli"] == "amra.cli"
    assert aliases["ara_math.models"] == "amra.core.models"
    assert aliases["ara_math.lean"] == "amra.lean.executor"
    assert aliases["ara_math.lean_formalizer"] == "amra.lean.formalizer"
    assert "ara_math.ara_library" not in aliases
