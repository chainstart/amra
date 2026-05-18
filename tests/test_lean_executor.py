from pathlib import Path
from subprocess import CompletedProcess

from ara_math.lean import LeanExecutor


def test_prepare_package_cache_links_best_matching_candidate(tmp_path: Path) -> None:
    target_formal = tmp_path / "target" / "formal"
    target_formal.mkdir(parents=True)
    (target_formal / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")

    mismatch = tmp_path / "mismatch-project"
    mismatch.mkdir()
    (mismatch / "lean-toolchain").write_text("leanprover/lean4:v4.15.0\n", encoding="utf-8")
    (mismatch / ".lake" / "packages" / "mathlib" / "lean-toolchain").parent.mkdir(parents=True)
    (mismatch / ".lake" / "packages" / "mathlib" / "lean-toolchain").write_text(
        "leanprover/lean4:v4.15.0\n",
        encoding="utf-8",
    )

    candidate = tmp_path / "cache-project"
    candidate.mkdir()
    (candidate / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")
    (candidate / ".lake" / "packages" / "mathlib" / "lean-toolchain").parent.mkdir(parents=True)
    (candidate / ".lake" / "packages" / "mathlib" / "lean-toolchain").write_text(
        "leanprover/lean4:v4.26.0\n",
        encoding="utf-8",
    )
    (candidate / ".lake" / "packages" / "mathlib" / ".lake" / "build" / "lib" / "lean" / "Mathlib").mkdir(parents=True)

    executor = LeanExecutor(cache_search_roots=[tmp_path])
    report = executor.prepare_package_cache(target_formal)

    assert report["status"] == "linked"
    assert Path(report["selected_source"]) == candidate / ".lake" / "packages"
    assert (target_formal / ".lake" / "packages").is_symlink()


def test_prepare_package_cache_keeps_existing_target_packages(tmp_path: Path) -> None:
    target_formal = tmp_path / "target" / "formal"
    existing = target_formal / ".lake" / "packages"
    existing.mkdir(parents=True)
    (existing / "mathlib").mkdir()
    (target_formal / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")

    executor = LeanExecutor(cache_search_roots=[tmp_path])
    report = executor.prepare_package_cache(target_formal)

    assert report["status"] == "existing_cold"
    assert Path(report["selected_source"]) == existing


def test_prepare_package_cache_relinks_existing_cold_target_packages(tmp_path: Path) -> None:
    target_formal = tmp_path / "target" / "formal"
    existing = target_formal / ".lake" / "packages"
    existing.mkdir(parents=True)
    (existing / "mathlib").mkdir()
    (target_formal / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")

    candidate = tmp_path / "cache-project"
    candidate.mkdir()
    (candidate / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")
    (candidate / ".lake" / "packages" / "mathlib" / "lean-toolchain").parent.mkdir(parents=True)
    (candidate / ".lake" / "packages" / "mathlib" / "lean-toolchain").write_text(
        "leanprover/lean4:v4.26.0\n",
        encoding="utf-8",
    )
    (candidate / ".lake" / "packages" / "mathlib" / ".lake" / "build" / "lib" / "lean" / "Mathlib").mkdir(parents=True)

    executor = LeanExecutor(cache_search_roots=[tmp_path])
    report = executor.prepare_package_cache(target_formal)

    assert report["status"] == "linked"
    assert Path(report["selected_source"]) == candidate / ".lake" / "packages"


def test_prepare_manifest_copies_compatible_ready_manifest(tmp_path: Path) -> None:
    target_formal = tmp_path / "target" / "formal"
    target_formal.mkdir(parents=True)
    lakefile = (
        "import Lake\nopen Lake DSL\n\npackage MathProject where\n\nrequire mathlib from git\n"
        '  "https://github.com/leanprover-community/mathlib4" @ "v4.26.0"\n'
    )
    (target_formal / "lakefile.lean").write_text(lakefile, encoding="utf-8")
    (target_formal / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")

    source_formal = tmp_path / "source" / "formal"
    (source_formal / ".lake" / "packages" / "mathlib" / ".lake" / "build" / "lib" / "lean" / "Mathlib").mkdir(parents=True)
    (source_formal / "lakefile.lean").write_text(lakefile, encoding="utf-8")
    (source_formal / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")
    (source_formal / "lake-manifest.json").write_text('{"name":"MathProject"}\n', encoding="utf-8")

    executor = LeanExecutor(cache_search_roots=[tmp_path])
    report = executor.prepare_manifest(target_formal)

    assert report["status"] == "copied"
    assert (target_formal / "lake-manifest.json").exists()


def test_build_reports_missing_lake(tmp_path: Path, monkeypatch) -> None:
    project_dir = tmp_path / "project"
    (project_dir / "formal" / "MathProject").mkdir(parents=True)
    (project_dir / "formal" / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")
    (project_dir / "formal" / "MathProject" / "Basic.lean").write_text(
        "theorem test : True := by trivial\n",
        encoding="utf-8",
    )
    executor = LeanExecutor(cache_search_roots=[tmp_path])
    monkeypatch.setattr(executor, "resolve_binary", lambda name: None)

    report = executor.build(project_dir)

    assert report.status == "blocked"
    assert "lake" in report.summary


def test_lean_executor_default_process_cap_allows_worker_threads(monkeypatch) -> None:
    monkeypatch.delenv("ARA_MATH_LEAN_MAX_PROCESSES", raising=False)

    executor = LeanExecutor()

    assert executor.max_processes >= 4096


def test_build_blocks_when_manifest_cannot_be_reused(tmp_path: Path, monkeypatch) -> None:
    project_dir = tmp_path / "project"
    formal_dir = project_dir / "formal" / "MathProject"
    formal_dir.mkdir(parents=True)
    (project_dir / "formal" / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")
    (project_dir / "formal" / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject where\n", encoding="utf-8")
    (formal_dir / "Basic.lean").write_text("theorem test : True := by trivial\n", encoding="utf-8")
    executor = LeanExecutor(cache_search_roots=[tmp_path], allow_cold_cache=True)
    monkeypatch.setattr(executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        "ara_math.lean.check_system_headroom",
        lambda **kwargs: {"status": "ready", "snapshot": {}, "blockers": [], "thresholds": kwargs},
    )

    report = executor.build(project_dir)

    assert report.status == "blocked"
    assert "manifest is missing" in report.summary


def test_build_blocks_cold_cache_when_guarded(tmp_path: Path, monkeypatch) -> None:
    project_dir = tmp_path / "project"
    formal_dir = project_dir / "formal" / "MathProject"
    formal_dir.mkdir(parents=True)
    (project_dir / "formal" / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")
    (project_dir / "formal" / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject where\n", encoding="utf-8")
    (project_dir / "formal" / "lake-manifest.json").write_text('{"name":"MathProject"}\n', encoding="utf-8")
    (formal_dir / "Basic.lean").write_text("theorem test : True := by trivial\n", encoding="utf-8")
    executor = LeanExecutor(cache_search_roots=[tmp_path], allow_cold_cache=False)
    monkeypatch.setattr(executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(executor, "prepare_package_cache", lambda _: {"status": "not_found", "selected_source": ""})

    report = executor.build(project_dir)

    assert report.status == "blocked"
    assert "Cold-cache Lean builds are disabled" in report.summary
    assert report.resource_policy["allow_cold_cache"] is False


def test_build_blocks_when_system_guard_is_unhealthy(tmp_path: Path, monkeypatch) -> None:
    project_dir = tmp_path / "project"
    formal_dir = project_dir / "formal" / "MathProject"
    formal_dir.mkdir(parents=True)
    (project_dir / "formal" / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")
    (project_dir / "formal" / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject where\n", encoding="utf-8")
    (project_dir / "formal" / "lake-manifest.json").write_text('{"name":"MathProject"}\n', encoding="utf-8")
    (formal_dir / "Basic.lean").write_text("theorem test : True := by trivial\n", encoding="utf-8")
    executor = LeanExecutor(cache_search_roots=[tmp_path], allow_cold_cache=True)
    monkeypatch.setattr(executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        "ara_math.lean.check_system_headroom",
        lambda **kwargs: {
            "status": "blocked",
            "snapshot": {"mem_available_mb": 256.0, "load_per_cpu": 2.4},
            "blockers": ["System too busy for a guarded Lean build."],
            "thresholds": kwargs,
        },
    )

    report = executor.build(project_dir)

    assert report.status == "blocked"
    assert report.summary == "System load guard blocked the Lean build before launch."
    assert report.system_guard["status"] == "blocked"


def test_build_flags_sorry_even_after_success(tmp_path: Path, monkeypatch) -> None:
    project_dir = tmp_path / "project"
    formal_dir = project_dir / "formal" / "MathProject"
    formal_dir.mkdir(parents=True)
    (project_dir / "formal" / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")
    (project_dir / "formal" / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject where\n", encoding="utf-8")
    (project_dir / "formal" / "lake-manifest.json").write_text('{"name":"MathProject"}\n', encoding="utf-8")
    (formal_dir / "Basic.lean").write_text(
        "theorem test : True := by\n  sorry\n",
        encoding="utf-8",
    )
    executor = LeanExecutor(cache_search_roots=[tmp_path])
    monkeypatch.setattr(executor, "resolve_binary", lambda name: "/usr/bin/lake")
    monkeypatch.setattr(
        executor,
        "prepare_package_cache",
        lambda _: {"status": "linked", "selected_source": str(tmp_path / "cache"), "build_ready": True},
    )
    monkeypatch.setattr(executor, "package_cache_state", lambda _: "ready")
    monkeypatch.setattr(
        executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 0, stdout="build ok\n", stderr=""),
    )

    report = executor.build(project_dir)

    assert report.status == "needs_attention"
    assert report.sorry_count == 1
    assert report.resource_policy["memory_mb"] > 0


def test_count_sorries_ignores_lake_staging(tmp_path: Path) -> None:
    formal_root = tmp_path / "formal"
    (formal_root / "MathProject").mkdir(parents=True)
    (formal_root / "MathProject" / "MainClaim.lean").write_text(
        "/- replace placeholder propositions and `sorry` proofs later -/\n"
        "theorem clean_claim : True := by\n  trivial\n",
        encoding="utf-8",
    )
    (formal_root / ".lake" / "ara_math_staging" / "src" / "Companion").mkdir(parents=True)
    (formal_root / ".lake" / "ara_math_staging" / "src" / "Companion" / "Basic.lean").write_text(
        "theorem staged_claim : True := by\n  sorry\n",
        encoding="utf-8",
    )

    executor = LeanExecutor(cache_search_roots=[tmp_path])

    assert executor.count_sorries(formal_root) == 0


def test_build_auto_enables_direct_verify_for_local_companion_assets(tmp_path: Path, monkeypatch) -> None:
    project_dir = tmp_path / "project"
    formal_dir = project_dir / "formal" / "MathProject"
    formal_dir.mkdir(parents=True)
    (project_dir / "idea").mkdir(parents=True)
    (project_dir / "formal" / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")
    (project_dir / "formal" / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject where\n", encoding="utf-8")
    (project_dir / "formal" / "lake-manifest.json").write_text('{"name":"MathProject"}\n', encoding="utf-8")
    (formal_dir / "Basic.lean").write_text("import UnitaryPerfect.UnitaryPerfect\n", encoding="utf-8")
    (formal_dir / "GeneratedClaims.lean").write_text("import MathProject.Basic\n", encoding="utf-8")
    (formal_dir / "MainClaim.lean").write_text("import MathProject.GeneratedClaims\n", encoding="utf-8")
    asset_root = tmp_path / "companion"
    (asset_root / ".lake" / "build" / "lib" / "lean" / "UnitaryPerfect").mkdir(parents=True)
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        '{"local_assets": [{"kind": "local_project_dir", "path": "' + str(asset_root) + '"}]}',
        encoding="utf-8",
    )

    executor = LeanExecutor(cache_search_roots=[tmp_path], allow_cold_cache=True)
    monkeypatch.setattr(executor, "resolve_binary", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(executor, "prepare_package_cache", lambda _: {"status": "linked", "selected_source": str(tmp_path / "cache")})
    monkeypatch.setattr(executor, "package_cache_state", lambda _: "ready")
    monkeypatch.setattr(executor, "count_sorries", lambda _: 0)
    monkeypatch.setattr(
        executor,
        "run_direct_lean_verification",
        lambda **kwargs: (["lean MathProject/Basic.lean"], CompletedProcess(["lean"], 0, stdout="ok\n", stderr="")),
    )

    report = executor.build(project_dir)

    assert report.status == "passed"
    assert report.resource_policy["direct_lean_verify"] is True
    assert str(asset_root / ".lake" / "build" / "lib" / "lean") in report.resource_policy["local_asset_search_entries"]


def test_build_falls_back_to_direct_verify_after_lake_import_failure(tmp_path: Path, monkeypatch) -> None:
    project_dir = tmp_path / "project"
    formal_dir = project_dir / "formal" / "MathProject"
    formal_dir.mkdir(parents=True)
    (project_dir / "idea").mkdir(parents=True)
    (project_dir / "formal" / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")
    (project_dir / "formal" / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage MathProject where\n", encoding="utf-8")
    (project_dir / "formal" / "lake-manifest.json").write_text('{"name":"MathProject"}\n', encoding="utf-8")
    (formal_dir / "Basic.lean").write_text("import Mathlib\n", encoding="utf-8")
    (formal_dir / "GeneratedClaims.lean").write_text("import MathProject.Basic\n", encoding="utf-8")
    (formal_dir / "MainClaim.lean").write_text("import MathProject.GeneratedClaims\n", encoding="utf-8")

    executor = LeanExecutor(cache_search_roots=[tmp_path], allow_cold_cache=True)
    monkeypatch.setattr(executor, "resolve_binary", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(executor, "prepare_package_cache", lambda _: {"status": "linked", "selected_source": str(tmp_path / "cache")})
    monkeypatch.setattr(executor, "package_cache_state", lambda _: "ready")
    monkeypatch.setattr(executor, "count_sorries", lambda _: 0)
    monkeypatch.setattr(
        executor,
        "run_command",
        lambda command, cwd, timeout: CompletedProcess(command, 1, stdout="error: bad import 'Mathlib'\n", stderr="error: no such file or directory\n"),
    )
    monkeypatch.setattr(
        executor,
        "run_direct_lean_verification",
        lambda **kwargs: (["lean MathProject/Basic.lean"], CompletedProcess(["lean"], 0, stdout="ok\n", stderr="")),
    )

    report = executor.build(project_dir)

    assert report.status == "passed"
    assert report.command[0] == "lake-build-fallback"
    assert "Used direct Lean verification after `lake build` hit import/cache issues." in report.summary


def test_stage_local_asset_modules_builds_shims_for_source_only_companions(tmp_path: Path, monkeypatch) -> None:
    project_dir = tmp_path / "project"
    formal_dir = project_dir / "formal" / "MathProject"
    formal_dir.mkdir(parents=True)
    (project_dir / "idea").mkdir(parents=True)
    (project_dir / "proof").mkdir(parents=True)
    (project_dir / "formal" / "lean-toolchain").write_text("leanprover/lean4:v4.26.0\n", encoding="utf-8")

    asset_root = tmp_path / "companion"
    (asset_root / "lean").mkdir(parents=True)
    (asset_root / ".lake" / "build" / "lib" / "lean" / "UnitaryPerfect").mkdir(parents=True)
    (asset_root / ".lake" / "build" / "lib" / "lean" / "UnitaryPerfect" / "UnitaryDivisor.olean").write_text("", encoding="utf-8")
    (asset_root / ".lake" / "build" / "lib" / "lean" / "UnitaryPerfect" / "UnitaryPerfect.olean").write_text("", encoding="utf-8")
    (asset_root / ".lake" / "build" / "lib" / "lean" / "UnitaryPerfect" / "OptimalSequence.olean").write_text("", encoding="utf-8")
    (asset_root / "lean" / "ProductInequalities.lean").write_text("import OptimalSequence\n\nnamespace Goto\nend Goto\n", encoding="utf-8")
    (asset_root / "lean" / "GotoBound.lean").write_text(
        "import UnitaryDivisor\nimport UnitaryPerfect\nimport ProductInequalities\n\nnamespace Goto\nend Goto\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        '{"local_assets": [{"kind": "local_project_dir", "path": "' + str(asset_root) + '"}]}',
        encoding="utf-8",
    )
    (project_dir / "proof" / "porting_candidates.json").write_text(
        '{"candidates": [{"name": "upn_finite_goto", "source_path": "' + str(asset_root / "lean" / "GotoBound.lean") + '", "import_ready": false}]}',
        encoding="utf-8",
    )

    commands: list[list[str]] = []

    def _fake_run_guarded(command, cwd, timeout, env, memory_mb, cpu_seconds, max_processes, niceness):
        commands.append(command)
        return CompletedProcess(command, 0, stdout="ok\n", stderr="")

    monkeypatch.setattr("ara_math.lean.run_guarded_command", _fake_run_guarded)

    executor = LeanExecutor(cache_search_roots=[tmp_path], allow_cold_cache=True)
    report = executor.stage_local_asset_modules(project_dir, project_dir / "formal", "/usr/bin/lean", timeout=15)

    shim_path = Path(report["stage_source_root"]) / "UnitaryDivisor.lean"
    copied_path = Path(report["stage_source_root"]) / "ProductInequalities.lean"

    assert report["status"] == "ready"
    assert report["compiled_module_count"] == 5
    assert report["compiled_modules"] == [
        "UnitaryDivisor",
        "UnitaryPerfect",
        "OptimalSequence",
        "ProductInequalities",
        "GotoBound",
    ]
    assert "import UnitaryPerfect.UnitaryDivisor" in shim_path.read_text(encoding="utf-8")
    assert "import OptimalSequence" in copied_path.read_text(encoding="utf-8")
    assert any("GotoBound.lean" in " ".join(command) for command in commands)


def test_stage_plan_prefers_compiled_shim_for_available_submodule(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    (project_dir / "idea").mkdir(parents=True)
    (project_dir / "proof").mkdir(parents=True)
    asset_root = tmp_path / "companion"
    (asset_root / "lean").mkdir(parents=True)
    (asset_root / ".lake" / "build" / "lib" / "lean" / "UnitaryPerfect").mkdir(parents=True)
    (asset_root / ".lake" / "build" / "lib" / "lean" / "UnitaryPerfect" / "UnitaryPerfect.olean").write_text("", encoding="utf-8")
    (asset_root / ".lake" / "build" / "lib" / "lean" / "UnitaryPerfect" / "OptimalSequence.olean").write_text("", encoding="utf-8")
    (asset_root / "lean" / "ProductInequalities.lean").write_text("import OptimalSequence\n", encoding="utf-8")
    (asset_root / "lean" / "OptimalSequence.lean").write_text("namespace Goto\nend Goto\n", encoding="utf-8")
    (asset_root / "lean" / "GotoBound.lean").write_text("import UnitaryPerfect\nimport ProductInequalities\n", encoding="utf-8")
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        '{"local_assets": [{"kind": "local_project_dir", "path": "' + str(asset_root) + '"}]}',
        encoding="utf-8",
    )
    (project_dir / "proof" / "porting_candidates.json").write_text(
        '{"candidates": [{"name": "upn_finite_goto", "source_path": "' + str(asset_root / "lean" / "GotoBound.lean") + '", "import_ready": false}]}',
        encoding="utf-8",
    )

    executor = LeanExecutor(cache_search_roots=[tmp_path], allow_cold_cache=True)
    plan = executor._discover_source_stage_plan(project_dir)

    assert plan["modules"]["UnitaryPerfect"]["kind"] == "shim"
    assert plan["modules"]["OptimalSequence"]["kind"] == "shim"


def test_stage_plan_discovers_fallback_companion_source_modules(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    (project_dir / "idea").mkdir(parents=True)
    (project_dir / "proof").mkdir(parents=True)
    asset_root = tmp_path / "companion"
    (asset_root / "lean").mkdir(parents=True)
    (asset_root / "UnitaryPerfect").mkdir(parents=True)
    (asset_root / ".lake" / "build" / "lib" / "lean" / "UnitaryPerfect").mkdir(parents=True)
    (asset_root / ".lake" / "build" / "lib" / "lean" / "UnitaryPerfect" / "UnitaryPerfect.olean").write_text("", encoding="utf-8")
    (asset_root / "UnitaryPerfect" / "UnitaryDivisor.lean").write_text("namespace Nat\nend Nat\n", encoding="utf-8")
    (asset_root / "lean" / "GotoBound.lean").write_text("import UnitaryDivisor\nimport UnitaryPerfect\n", encoding="utf-8")
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        '{"local_assets": [{"kind": "local_project_dir", "path": "' + str(asset_root) + '"}]}',
        encoding="utf-8",
    )
    (project_dir / "proof" / "porting_candidates.json").write_text(
        '{"candidates": [{"name": "upn_finite_goto", "source_path": "' + str(asset_root / "lean" / "GotoBound.lean") + '", "import_ready": false}]}',
        encoding="utf-8",
    )

    executor = LeanExecutor(cache_search_roots=[tmp_path], allow_cold_cache=True)
    plan = executor._discover_source_stage_plan(project_dir)

    assert plan["modules"]["UnitaryDivisor"]["kind"] == "copy"
    assert plan["modules"]["UnitaryDivisor"]["source_path"].endswith("UnitaryPerfect/UnitaryDivisor.lean")


def test_stage_plan_blocks_unsafe_source_only_companion_modules(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    (project_dir / "idea").mkdir(parents=True)
    (project_dir / "proof").mkdir(parents=True)
    asset_root = tmp_path / "companion"
    (asset_root / "lean").mkdir(parents=True)
    (asset_root / "lean" / "GotoBound.lean").write_text(
        "import Mathlib\n\naxiom unsafe_bridge : True\n\ntheorem upn_finite_goto : True := by\n  sorry\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        '{"local_assets": [{"kind": "local_project_dir", "path": "' + str(asset_root) + '"}]}',
        encoding="utf-8",
    )
    (project_dir / "proof" / "porting_candidates.json").write_text(
        '{"candidates": [{"name": "upn_finite_goto", "source_path": "' + str(asset_root / "lean" / "GotoBound.lean") + '", "import_ready": false}]}',
        encoding="utf-8",
    )

    executor = LeanExecutor(cache_search_roots=[tmp_path], allow_cold_cache=True)
    plan = executor._discover_source_stage_plan(project_dir)

    assert plan["status"] == "blocked"
    assert plan["compile_order"] == []
    assert plan["blocked_sources"][0]["module"] == "GotoBound"
    assert plan["blocked_sources"][0]["source_audit"]["counts"]["axiom"] == 1
    assert plan["blocked_sources"][0]["source_audit"]["counts"]["sorry"] == 1


def test_stage_plan_skips_unaligned_unsafe_companion_modules(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    (project_dir / "idea").mkdir(parents=True)
    (project_dir / "proof").mkdir(parents=True)
    asset_root = tmp_path / "companion"
    (asset_root / "lean").mkdir(parents=True)
    (asset_root / "lean" / "GotoBound.lean").write_text(
        "import Mathlib\n\naxiom unsafe_bridge : True\n\ntheorem upn_finite_goto : True := by\n  sorry\n",
        encoding="utf-8",
    )
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        '{"local_assets": [{"kind": "local_project_dir", "path": "' + str(asset_root) + '"}]}',
        encoding="utf-8",
    )
    (project_dir / "proof" / "porting_candidates.json").write_text(
        '{"candidates": [{"name": "upn_finite_goto", "source_path": "'
        + str(asset_root / "lean" / "GotoBound.lean")
        + '", "import_ready": false, "aligned_with_target": false}]}',
        encoding="utf-8",
    )

    executor = LeanExecutor(cache_search_roots=[tmp_path], allow_cold_cache=True)
    plan = executor._discover_source_stage_plan(project_dir)

    assert plan["status"] == "not_needed"
    assert plan["compile_order"] == []
    assert plan["blocked_sources"] == []


def test_discover_local_asset_search_entries_includes_source_roots(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    (project_dir / "idea").mkdir(parents=True)
    asset_root = tmp_path / "companion"
    (asset_root / "lean").mkdir(parents=True)
    (asset_root / "UnitaryPerfect").mkdir(parents=True)
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        '{"local_assets": [{"kind": "local_project_dir", "path": "' + str(asset_root) + '"}]}',
        encoding="utf-8",
    )

    executor = LeanExecutor(cache_search_roots=[tmp_path])
    entries = executor.discover_local_asset_search_entries(project_dir)

    assert str(asset_root / "lean") in entries
    assert str(asset_root) in entries


def test_discover_local_asset_search_entries_includes_seeded_asset_paths(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    (project_dir / "idea").mkdir(parents=True)
    (project_dir / "artifacts").mkdir(parents=True)
    primary_asset = tmp_path / "formal-math" / "erdos-1052-unitary-perfect"
    secondary_asset = tmp_path / "formal-math" / "unitary-perfect-lean4" / "mathlib-contrib"
    (primary_asset / "lean").mkdir(parents=True)
    (secondary_asset / ".lake" / "build" / "lib" / "lean" / "Mathlib" / "NumberTheory" / "UnitaryPerfect").mkdir(
        parents=True
    )
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        '{"local_assets": [{"kind": "local_project_dir", "path": "' + str(primary_asset) + '"}]}',
        encoding="utf-8",
    )
    (project_dir / "artifacts" / "formal_preparation.json").write_text(
        '{"seed_asset_paths": ["' + str(primary_asset) + '", "' + str(secondary_asset) + '"]}',
        encoding="utf-8",
    )

    executor = LeanExecutor(cache_search_roots=[tmp_path])
    entries = executor.discover_local_asset_search_entries(project_dir)

    assert str(primary_asset / "lean") in entries
    assert str(secondary_asset / ".lake" / "build" / "lib" / "lean") in entries


def test_discover_accessible_premise_support_collects_compiled_and_staged_modules(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    formal_dir = project_dir / "formal" / "MathProject"
    formal_dir.mkdir(parents=True)
    (project_dir / "idea").mkdir(parents=True)
    (project_dir / "proof").mkdir(parents=True)
    (formal_dir / "Basic.lean").write_text("theorem local_basic : True := by\n  trivial\n", encoding="utf-8")
    (formal_dir / "MainClaim.lean").write_text(
        "\n".join(
            [
                "import MathProject.Basic",
                "import Companion.Helper",
                "",
                "theorem local_main : True := by",
                "  trivial",
                "",
            ]
        ),
        encoding="utf-8",
    )

    asset_root = tmp_path / "companion"
    (asset_root / ".lake" / "build" / "lib" / "lean" / "Companion").mkdir(parents=True)
    (asset_root / ".lake" / "build" / "lib" / "lean" / "Companion" / "Helper.olean").write_text("", encoding="utf-8")
    source_path = asset_root / "lean" / "UnitaryPerfect" / "GotoBound.lean"
    source_path.parent.mkdir(parents=True)
    source_path.write_text("theorem gotoBound : True := by\n  trivial\n", encoding="utf-8")
    (project_dir / "idea" / "proof_path_assessment.json").write_text(
        '{"local_assets": [{"kind": "local_project_dir", "path": "' + str(asset_root) + '"}]}',
        encoding="utf-8",
    )
    (project_dir / "proof" / "porting_candidates.json").write_text(
        '{"candidates": [{"name": "gotoBound", "source_path": "'
        + str(source_path)
        + '", "import_ready": false, "import_hint": "UnitaryPerfect.GotoBound"}]}',
        encoding="utf-8",
    )

    executor = LeanExecutor(cache_search_roots=[tmp_path])
    support = executor.discover_accessible_premise_support(project_dir)

    assert "Companion.Helper" in support["project_imports"]
    assert "Companion.Helper" in support["compiled_modules"]
    assert support["stage_plan"]["status"] == "ready"
    assert "UnitaryPerfect.GotoBound" in support["stage_plan"]["modules"]


def test_lean_executor_discovers_amra_library_search_entries(tmp_path: Path, monkeypatch) -> None:
    project_dir = tmp_path / "projects" / "demo"
    (project_dir / "idea").mkdir(parents=True)
    (project_dir / "artifacts").mkdir(parents=True)
    (project_dir / "formal" / "MathProject").mkdir(parents=True)
    (project_dir / "formal" / "MathProject" / "MainClaim.lean").write_text(
        "import AmraLibrary\n\n",
        encoding="utf-8",
    )
    formal_dir = tmp_path / "amra_library" / "formal"
    build_dir = formal_dir / ".lake" / "build" / "lib" / "lean"
    build_dir.mkdir(parents=True)
    (formal_dir / "AmraLibrary").mkdir(parents=True)
    monkeypatch.setenv("AMRA_REPO_ROOT", str(tmp_path))

    entries = LeanExecutor().discover_local_asset_search_entries(project_dir)

    assert str(build_dir) in entries
    assert str(formal_dir) in entries


def test_lean_executor_keeps_legacy_ara_library_search_entries(tmp_path: Path, monkeypatch) -> None:
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
