from __future__ import annotations

import json
from pathlib import Path

import pytest

from amra.amra_library import AmraLibraryManager
from ara_math.ara_library import AraLibraryManager
from amra.portfolio_campaign import PortfolioCampaignRunner


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _verified_project(tmp_path: Path, *, unsafe_source: bool = False) -> tuple[Path, Path]:
    project = tmp_path / "projects" / "demo"
    source_file = project / "formal" / "MathProject" / "Reusable.lean"
    source_file.parent.mkdir(parents=True)
    body = [
        "import Mathlib",
        "",
        "namespace MathProject",
        "",
        "/-- Reusable helper. -/",
        "theorem reusable_helper : True := by",
        "  trivial",
        "",
    ]
    if unsafe_source:
        body.extend(
            [
                "opaque unsafe_placeholder_constant : True",
                "",
                "theorem unsafe_helper : True := by",
                "  sorry",
                "",
            ]
        )
    body.extend(["end MathProject", ""])
    source_file.write_text("\n".join(body), encoding="utf-8")
    _write_json(project / "artifacts" / "lean_build_report.json", {"status": "passed", "sorry_count": 0})
    _write_json(
        project / "verified_declarations.json",
        {
            "schema_version": "amra.verified_declarations.v1",
            "declarations": [
                {
                    "name": "reusable_helper",
                    "full_name": "MathProject.reusable_helper",
                    "lean_name": "reusable_helper",
                    "relative_path": "MathProject/Reusable.lean",
                    "status": "lean_verified",
                }
            ],
        },
    )
    return project, source_file


def test_amra_library_manager_creates_canonical_skeleton(tmp_path: Path) -> None:
    manager = AmraLibraryManager(repo_root=tmp_path)

    inventory = manager.ensure_library()

    assert inventory["library_root"] == str(tmp_path / "amra_library")
    assert inventory["module_prefix"] == "AmraLibrary"
    assert (tmp_path / "amra_library" / "formal" / "lakefile.lean").exists()
    assert (tmp_path / "amra_library" / "formal" / "lean-toolchain").exists()
    assert (tmp_path / "amra_library" / "formal" / "AmraLibrary.lean").exists()
    assert (tmp_path / "amra_library" / "registry.json").exists()


def test_legacy_ara_library_manager_remains_available(tmp_path: Path) -> None:
    manager = AraLibraryManager(repo_root=tmp_path)

    inventory = manager.ensure_library()

    assert inventory["library_root"] == str(tmp_path / "ara_library")
    assert inventory["module_prefix"] == "AraLibrary"
    assert (tmp_path / "ara_library" / "formal" / "AraLibrary.lean").exists()


def test_amra_library_add_module_updates_registry_and_root_import(tmp_path: Path) -> None:
    manager = AmraLibraryManager(repo_root=tmp_path)

    report = manager.add_module(
        module_name="AmraLibrary.NumberTheory.Carmichael",
        imports=["Mathlib", "Mathlib"],
        title="Carmichael helpers",
        domain="number_theory",
        status="candidate",
        tags=["carmichael"],
        description="Reusable lemmas for Korselt-style arguments.",
    )

    module_path = tmp_path / "amra_library" / "formal" / "AmraLibrary" / "NumberTheory" / "Carmichael.lean"
    root_text = (tmp_path / "amra_library" / "formal" / "AmraLibrary.lean").read_text(encoding="utf-8")
    inventory = manager.inventory()

    assert report["status"] == "module_ready"
    assert module_path.exists()
    assert module_path.read_text(encoding="utf-8").count("import Mathlib") == 1
    assert "import AmraLibrary.NumberTheory.Carmichael" in root_text
    assert inventory["module_count"] == 1
    assert inventory["modules"][0]["module_name"] == "AmraLibrary.NumberTheory.Carmichael"
    assert "import AmraLibrary.NumberTheory.Carmichael" in inventory["modules"][0]["import_hints"]


def test_amra_library_accepts_legacy_module_prefix_as_migration_shim(tmp_path: Path) -> None:
    manager = AmraLibraryManager(repo_root=tmp_path)

    report = manager.add_module(module_name="AraLibrary.NumberTheory.LegacyName")

    module = report["module"]
    assert module["module_name"] == "AmraLibrary.NumberTheory.LegacyName"
    assert module["legacy_module_name"] == "AraLibrary.NumberTheory.LegacyName"
    assert Path(report["path"]).relative_to(tmp_path / "amra_library" / "formal") == Path(
        "AmraLibrary/NumberTheory/LegacyName.lean"
    )


def test_amra_library_promotes_only_verified_clean_declarations(tmp_path: Path) -> None:
    project, source_file = _verified_project(tmp_path)
    manager = AmraLibraryManager(repo_root=tmp_path)

    report = manager.promote_declarations(
        source_file=source_file,
        source_project=project,
        module_name="AmraLibrary.NumberTheory.Reusable",
        declarations=["reusable_helper"],
        imports=["Mathlib"],
        title="Reusable helpers",
        domain="number_theory",
        status="candidate",
        tags=["reuse"],
    )

    module_path = Path(report["path"])
    text = module_path.read_text(encoding="utf-8")

    assert report["status"] == "promoted"
    assert report["promoted_declarations"] == ["reusable_helper"]
    assert "theorem reusable_helper : True := by" in text
    assert "end MathProject" not in text
    assert "Promotion provenance" in text
    assert report["module"]["provenance"]["source_verification"]["verified"] is True
    assert "import AmraLibrary.NumberTheory.Reusable" in report["module"]["import_hints"]


def test_amra_library_rejects_unverified_source_project(tmp_path: Path) -> None:
    project, source_file = _verified_project(tmp_path)
    (project / "artifacts" / "lean_build_report.json").unlink()
    manager = AmraLibraryManager(repo_root=tmp_path)

    with pytest.raises(ValueError, match="passing no-sorry Lean build report"):
        manager.promote_declarations(
            source_file=source_file,
            source_project=project,
            module_name="AmraLibrary.NumberTheory.Unverified",
            declarations=["reusable_helper"],
        )


def test_amra_library_rejects_missing_verified_declaration_index(tmp_path: Path) -> None:
    project, source_file = _verified_project(tmp_path)
    (project / "verified_declarations.json").unlink()
    manager = AmraLibraryManager(repo_root=tmp_path)

    with pytest.raises(ValueError, match="verified_declarations.json"):
        manager.promote_declarations(
            source_file=source_file,
            source_project=project,
            module_name="AmraLibrary.NumberTheory.Unindexed",
            declarations=["reusable_helper"],
        )


def test_amra_library_rejects_sorry_admit_axiom_opaque_and_placeholders(tmp_path: Path) -> None:
    project, source_file = _verified_project(tmp_path, unsafe_source=True)
    manager = AmraLibraryManager(repo_root=tmp_path)

    audit = manager.audit_source_file(source_file)

    assert audit["counts"]["sorry"] == 1
    assert audit["counts"]["opaque"] == 1
    assert audit["counts"]["placeholder"] == 1
    with pytest.raises(ValueError, match="forbidden placeholders"):
        manager.promote_declarations(
            source_file=source_file,
            source_project=project,
            module_name="AmraLibrary.NumberTheory.Unsafe",
            declarations=["reusable_helper"],
        )


def test_portfolio_harvest_candidates_filters_to_verified_clean_declarations(tmp_path: Path) -> None:
    project, _ = _verified_project(tmp_path)
    payload = json.loads((project / "verified_declarations.json").read_text(encoding="utf-8"))
    payload["declarations"].append(
        {
            "name": "draft_helper",
            "lean_name": "draft_helper",
            "relative_path": "MathProject/Reusable.lean",
            "status": "draft",
        }
    )
    _write_json(project / "verified_declarations.json", payload)

    report = PortfolioCampaignRunner(repo_root=tmp_path).harvest_library_candidates(
        project=project,
        module="AmraLibrary.NumberTheory.Reusable",
    )

    assert report["candidate_count"] == 1
    assert report["rejected_count"] == 1
    assert report["candidates"][0]["declaration"] == "reusable_helper"
    assert report["candidates"][0]["import_hints"] == [
        "import AmraLibrary.NumberTheory.Reusable",
        "open AmraLibrary -- enables `reusable_helper` after importing AmraLibrary.NumberTheory.Reusable",
    ]
    assert (project / "review" / "library_harvest_candidates.json").exists()
