from __future__ import annotations

from pathlib import Path

from ara_math.ara_library import AraLibraryManager
from ara_math.lean import LeanExecutor
from ara_math.proof_search import ProofSearchRunner


def test_ara_library_manager_creates_skeleton(tmp_path: Path) -> None:
    manager = AraLibraryManager(repo_root=tmp_path)

    inventory = manager.ensure_library()

    assert inventory["library_root"] == str(tmp_path / "ara_library")
    assert (tmp_path / "ara_library" / "formal" / "lakefile.lean").exists()
    assert (tmp_path / "ara_library" / "formal" / "lean-toolchain").exists()
    assert (tmp_path / "ara_library" / "formal" / "AraLibrary.lean").exists()
    assert (tmp_path / "ara_library" / "registry.json").exists()


def test_ara_library_add_module_updates_registry_and_root_import(tmp_path: Path) -> None:
    manager = AraLibraryManager(repo_root=tmp_path)

    report = manager.add_module(
        module_name="AraLibrary.NumberTheory.Carmichael",
        imports=["Mathlib", "Mathlib"],
        title="Carmichael helpers",
        domain="number_theory",
        status="candidate",
        tags=["carmichael"],
        description="Reusable lemmas for Korselt-style arguments.",
    )

    module_path = tmp_path / "ara_library" / "formal" / "AraLibrary" / "NumberTheory" / "Carmichael.lean"
    root_text = (tmp_path / "ara_library" / "formal" / "AraLibrary.lean").read_text(encoding="utf-8")
    inventory = manager.inventory()

    assert report["status"] == "module_ready"
    assert module_path.exists()
    assert module_path.read_text(encoding="utf-8").count("import Mathlib") == 1
    assert "import AraLibrary.NumberTheory.Carmichael" in root_text
    assert inventory["module_count"] == 1
    assert inventory["modules"][0]["module_name"] == "AraLibrary.NumberTheory.Carmichael"


def test_ara_library_promotes_selected_declarations(tmp_path: Path) -> None:
    source_file = tmp_path / "project" / "formal" / "MathProject" / "GeneratedClaims.lean"
    source_file.parent.mkdir(parents=True)
    source_file.write_text(
        "\n".join(
            [
                "import Mathlib",
                "",
                "namespace MathProject",
                "",
                "/-- Reusable helper. -/",
                "theorem reusable_helper : True := by",
                "  trivial",
                "",
                "theorem unrelated_helper : True := by",
                "  trivial",
                "",
                "end MathProject",
                "",
            ]
        ),
        encoding="utf-8",
    )
    manager = AraLibraryManager(repo_root=tmp_path)

    report = manager.promote_declarations(
        source_file=source_file,
        source_project=tmp_path / "project",
        module_name="AraLibrary.NumberTheory.Reusable",
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
    assert report["missing_declarations"] == []
    assert "theorem reusable_helper : True := by" in text
    assert "theorem unrelated_helper" not in text
    assert "Promotion provenance" in text
    assert report["module"]["declarations"][0]["name"] == "reusable_helper"


def test_lean_executor_discovers_ara_library_search_entries(tmp_path: Path, monkeypatch) -> None:
    project_dir = tmp_path / "projects" / "demo"
    (project_dir / "idea").mkdir(parents=True)
    (project_dir / "artifacts").mkdir(parents=True)
    (project_dir / "formal" / "MathProject").mkdir(parents=True)
    (project_dir / "formal" / "MathProject" / "MainClaim.lean").write_text(
        "import AraLibrary\n\n",
        encoding="utf-8",
    )
    formal_dir = tmp_path / "ara_library" / "formal"
    build_dir = formal_dir / ".lake" / "build" / "lib" / "lean"
    build_dir.mkdir(parents=True)
    (formal_dir / "AraLibrary").mkdir(parents=True)
    monkeypatch.setenv("ARA_MATH_REPO_ROOT", str(tmp_path))

    entries = LeanExecutor().discover_local_asset_search_entries(project_dir)

    assert str(build_dir) in entries
    assert str(formal_dir) in entries


def test_lean_executor_does_not_force_source_library_without_import(tmp_path: Path, monkeypatch) -> None:
    project_dir = tmp_path / "projects" / "demo"
    (project_dir / "idea").mkdir(parents=True)
    (project_dir / "artifacts").mkdir(parents=True)
    formal_dir = tmp_path / "ara_library" / "formal"
    build_dir = formal_dir / ".lake" / "build" / "lib" / "lean"
    build_dir.mkdir(parents=True)
    monkeypatch.setenv("ARA_MATH_REPO_ROOT", str(tmp_path))

    entries = LeanExecutor().discover_local_asset_search_entries(project_dir)

    assert str(build_dir) not in entries
    assert str(formal_dir) not in entries


def test_proof_search_runner_includes_ara_library_as_local_asset(tmp_path: Path) -> None:
    project_dir = tmp_path / "projects" / "demo"
    (project_dir / "idea").mkdir(parents=True)
    (project_dir / "idea" / "proof_path_assessment.json").write_text('{"local_assets": []}', encoding="utf-8")
    formal_dir = tmp_path / "ara_library" / "formal"
    formal_dir.mkdir(parents=True)
    runner = ProofSearchRunner(repo_root=tmp_path)

    paths = runner._find_local_asset_paths(project_dir)

    assert formal_dir in paths
