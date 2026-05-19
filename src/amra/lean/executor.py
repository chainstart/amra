from __future__ import annotations

import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from amra.lean.audit import audit_lean_source_file
from amra.core.models import LeanBuildReport
from amra.infra.runtime import build_resource_policy, check_system_headroom, env_bool, env_float, env_int, run_guarded_command
from amra.core.workspace import read_json, utc_now_iso


__all__ = ["LeanExecutor"]


class LeanExecutor:
    AXIOM_PATTERN = re.compile(r"^\s*axiom\b", re.MULTILINE)
    ADMIT_PATTERN = re.compile(r"\badmit\b")
    PLACEHOLDER_PATTERN = re.compile(r"ARA_MATH_PLACEHOLDER")
    BLOCK_COMMENT_PATTERN = re.compile(r"/-.*?-/", re.DOTALL)
    LINE_COMMENT_PATTERN = re.compile(r"--.*?$", re.MULTILINE)

    def __init__(
        self,
        timeout_sec: int = 600,
        cache_search_roots: list[Path] | None = None,
        *,
        max_memory_mb: int | None = None,
        max_cpu_seconds: int | None = None,
        max_processes: int | None = None,
        niceness: int | None = None,
        allow_cold_cache: bool | None = None,
    ) -> None:
        self.timeout_sec = timeout_sec
        self.cache_search_roots = [Path(root) for root in cache_search_roots] if cache_search_roots else None
        self.max_memory_mb = max_memory_mb if max_memory_mb is not None else env_int("ARA_MATH_LEAN_MAX_MEMORY_MB", 12288)
        self.max_cpu_seconds = (
            max_cpu_seconds if max_cpu_seconds is not None else env_int("ARA_MATH_LEAN_MAX_CPU_SECONDS", max(timeout_sec + 30, 900))
        )
        # Lean/lake can create many worker threads, and RLIMIT_NPROC is counted
        # against the whole Unix user. A low cap can fail before Lean starts on
        # otherwise idle WSL machines that already have background services.
        self.max_processes = max_processes if max_processes is not None else env_int("ARA_MATH_LEAN_MAX_PROCESSES", 4096)
        self.niceness = niceness if niceness is not None else env_int("ARA_MATH_LEAN_NICENESS", 10)
        self.allow_cold_cache = allow_cold_cache if allow_cold_cache is not None else env_bool("ARA_MATH_ALLOW_COLD_CACHE", False)
        self.min_available_memory_mb = env_int("ARA_MATH_MIN_AVAILABLE_MEMORY_MB", max(4096, self.max_memory_mb // 2))
        self.max_load_per_cpu = env_float("ARA_MATH_MAX_LOAD_PER_CPU", 1.5)
        self.olean_only = env_bool("ARA_MATH_LEAN_OLEAN_ONLY", True)
        self.direct_lean_verify = env_bool("ARA_MATH_DIRECT_LEAN_VERIFY", False)

    def resolve_binary(self, name: str) -> str | None:
        candidate = shutil.which(name)
        if candidate:
            return candidate
        fallback = Path.home() / ".elan" / "bin" / name
        if fallback.exists():
            return str(fallback)
        return None

    def run_command(self, command: list[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
        return run_guarded_command(
            command,
            cwd=cwd,
            timeout=timeout,
            memory_mb=self.max_memory_mb,
            cpu_seconds=min(self.max_cpu_seconds, max(timeout + 10, timeout)),
            max_processes=self.max_processes,
            niceness=self.niceness,
        )

    def count_sorries(self, root: Path) -> int:
        total = 0
        pattern = re.compile(r"\bsorry\b")
        for lean_file in self.iter_project_lean_files(root):
            text = self.strip_lean_comments(lean_file.read_text(encoding="utf-8"))
            total += len(pattern.findall(text))
        return total

    def count_pattern(self, root: Path, pattern: re.Pattern[str], *, strip_comments: bool = False) -> int:
        total = 0
        for lean_file in self.iter_project_lean_files(root):
            text = lean_file.read_text(encoding="utf-8")
            if strip_comments:
                text = self.strip_lean_comments(text)
            total += len(pattern.findall(text))
        return total

    def iter_project_lean_files(self, root: Path):
        for lean_file in root.rglob("*.lean"):
            if any(part in {".lake", "__pycache__"} for part in lean_file.parts):
                continue
            yield lean_file

    def strip_lean_comments(self, text: str) -> str:
        without_blocks = self.BLOCK_COMMENT_PATTERN.sub("", text)
        return self.LINE_COMMENT_PATTERN.sub("", without_blocks)

    def extract_diagnostics(self, stdout: str, stderr: str) -> list[str]:
        diagnostics: list[str] = []
        for line in (stdout + "\n" + stderr).splitlines():
            lowered = line.lower()
            if "error:" in lowered or "warning:" in lowered or "sorry" in lowered:
                diagnostics.append(line.strip())
        return diagnostics[-40:]

    def should_retry_with_direct_verify(self, stdout: str, stderr: str) -> bool:
        text = f"{stdout}\n{stderr}".lower()
        retry_markers = (
            "bad import",
            "object file",
            "no such file or directory",
            "module",
        )
        return any(marker in text for marker in retry_markers)

    def coerce_text(self, value: str | bytes | None) -> str:
        if value is None:
            return ""
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        return value

    def read_toolchain(self, root: Path) -> str:
        toolchain_path = root / "lean-toolchain"
        if not toolchain_path.exists():
            return ""
        return toolchain_path.read_text(encoding="utf-8").strip()

    def default_search_roots(self, formal_dir: Path) -> list[Path]:
        roots: list[Path] = []
        env_value = os.environ.get("ARA_MATH_LEAN_CACHE_ROOTS", "").strip()
        if env_value:
            for item in env_value.split(os.pathsep):
                item = item.strip()
                if item:
                    roots.append(Path(item))

        project_dir = formal_dir.parent
        if project_dir.parent.name == "projects":
            repo_root = project_dir.parent.parent
            roots.append(repo_root)
            roots.append(repo_root.parent)
        else:
            roots.append(project_dir.parent)

        home_work = Path.home() / "work"
        roots.append(home_work)
        roots.append(Path.home())

        unique_roots: list[Path] = []
        seen: set[Path] = set()
        for root in roots:
            resolved = root.expanduser()
            if not resolved.exists():
                continue
            if resolved in seen:
                continue
            seen.add(resolved)
            unique_roots.append(resolved)
        return unique_roots

    def package_build_ready(self, packages_dir: Path) -> bool:
        return (packages_dir / "mathlib" / ".lake" / "build" / "lib" / "lean" / "Mathlib").exists()

    def manifest_signature(self, formal_dir: Path) -> dict[str, str]:
        return {
            "toolchain": self.read_toolchain(formal_dir),
            "lakefile": (formal_dir / "lakefile.lean").read_text(encoding="utf-8") if (formal_dir / "lakefile.lean").exists() else "",
        }

    def discover_package_cache_candidates(self, formal_dir: Path) -> list[dict[str, Any]]:
        target_toolchain = self.read_toolchain(formal_dir)
        search_roots = self.cache_search_roots or self.default_search_roots(formal_dir)
        target_packages = formal_dir / ".lake" / "packages"
        candidates: list[dict[str, Any]] = []

        for root in search_roots:
            for packages_dir in root.rglob("packages"):
                if packages_dir.name != "packages":
                    continue
                if packages_dir.parent.name != ".lake":
                    continue
                if not (packages_dir / "mathlib").exists():
                    continue
                try:
                    if target_packages.exists() and packages_dir.resolve() == target_packages.resolve():
                        continue
                except OSError:
                    pass
                project_root = packages_dir.parent.parent
                project_toolchain = self.read_toolchain(project_root)
                mathlib_toolchain = self.read_toolchain(packages_dir / "mathlib")
                score = 0
                if target_toolchain and project_toolchain == target_toolchain:
                    score += 100
                if target_toolchain and mathlib_toolchain == target_toolchain:
                    score += 75
                if self.package_build_ready(packages_dir):
                    score += 25
                if score <= 0:
                    continue
                candidates.append(
                    {
                        "packages_dir": packages_dir,
                        "project_root": project_root,
                        "project_toolchain": project_toolchain,
                        "mathlib_toolchain": mathlib_toolchain,
                        "score": score,
                        "build_ready": self.package_build_ready(packages_dir),
                    }
                )

        candidates.sort(
            key=lambda item: (
                item["score"],
                len(str(item["project_root"])),
            ),
            reverse=True,
        )
        return candidates

    def prepare_package_cache(self, formal_dir: Path) -> dict[str, Any]:
        target_packages = formal_dir / ".lake" / "packages"
        report: dict[str, Any] = {
            "target_packages_dir": str(target_packages),
            "target_toolchain": self.read_toolchain(formal_dir),
            "status": "not_needed",
            "selected_source": "",
            "candidate_count": 0,
        }

        if target_packages.exists():
            try:
                has_entries = target_packages.is_symlink() or any(target_packages.iterdir())
            except OSError:
                has_entries = True
            if has_entries:
                report["status"] = "existing"
                report["selected_source"] = str(target_packages)
                report["build_ready"] = self.package_build_ready(target_packages)
                if report["build_ready"]:
                    return report
                report["status"] = "existing_cold"

        candidates = self.discover_package_cache_candidates(formal_dir)
        report["candidate_count"] = len(candidates)
        if not candidates:
            if report["status"] == "existing_cold":
                report["status"] = "existing_cold"
            else:
                report["status"] = "not_found"
            return report

        selected = candidates[0]
        target_packages.parent.mkdir(parents=True, exist_ok=True)
        if target_packages.is_symlink() or target_packages.exists():
            if target_packages.is_symlink() or target_packages.is_file():
                target_packages.unlink()
            else:
                shutil.rmtree(target_packages)
        target_packages.symlink_to(selected["packages_dir"], target_is_directory=True)
        report.update(
            {
                "status": "linked",
                "selected_source": str(selected["packages_dir"]),
                "selected_project_root": str(selected["project_root"]),
                "selected_project_toolchain": selected["project_toolchain"],
                "selected_mathlib_toolchain": selected["mathlib_toolchain"],
                "selected_score": selected["score"],
                "build_ready": selected["build_ready"],
            }
        )
        return report

    def package_cache_state(self, formal_dir: Path) -> str:
        target_packages = formal_dir / ".lake" / "packages"
        if not target_packages.exists():
            return "missing"
        if not (target_packages / "mathlib").exists():
            return "missing"
        return "ready" if self.package_build_ready(target_packages) else "cold"

    def _module_path(self, module_name: str) -> Path:
        return Path(*module_name.split("."))

    def _parse_imports(self, source_path: Path) -> list[str]:
        imports: list[str] = []
        for line in source_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            stripped = line.strip()
            if not stripped.startswith("import "):
                continue
            raw_imports = stripped[len("import ") :].split()
            imports.extend(item.strip() for item in raw_imports if item.strip())
        return imports

    def _is_external_module(self, module_name: str) -> bool:
        return module_name.startswith(("Mathlib", "Init", "Lean", "Lake", "Std", "Batteries", "Aesop"))

    def _infer_source_root_and_module(self, source_path: Path) -> tuple[Path, str]:
        if "lean" in source_path.parts:
            index = source_path.parts.index("lean")
            source_root = Path(*source_path.parts[: index + 1])
            module = ".".join(source_path.relative_to(source_root).with_suffix("").parts)
            return source_root, module
        if source_path.parent.name and source_path.parent.name[0].isupper():
            source_root = source_path.parent.parent
            module = ".".join(source_path.relative_to(source_root).with_suffix("").parts)
            return source_root, module
        return source_path.parent, source_path.stem

    def _compiled_module_index(self, search_entries: list[str]) -> tuple[set[str], dict[str, list[str]]]:
        exact: set[str] = set()
        suffix_map: dict[str, set[str]] = {}
        for raw_entry in search_entries:
            entry = Path(raw_entry)
            if not entry.exists() or ".lake" not in entry.parts:
                continue
            for olean_path in entry.rglob("*.olean"):
                relative = olean_path.relative_to(entry).with_suffix("")
                module_name = ".".join(relative.parts)
                exact.add(module_name)
                suffix = relative.name
                suffix_map.setdefault(suffix, set()).add(module_name)
        return exact, {key: sorted(value) for key, value in suffix_map.items()}

    def _project_imports_library(self, project_dir: Path, module_prefixes: tuple[str, ...]) -> bool:
        formal_dir = project_dir / "formal"
        if not formal_dir.exists():
            return False
        for lean_file in formal_dir.rglob("*.lean"):
            if ".lake" in lean_file.parts or lean_file.name == "lakefile.lean":
                continue
            for imported in self._parse_imports(lean_file):
                if any(imported == prefix or imported.startswith(f"{prefix}.") for prefix in module_prefixes):
                    return True
        return False

    def _repo_root_for_local_library(self) -> Path:
        repo_root_override = os.environ.get("AMRA_REPO_ROOT", "").strip() or os.environ.get("ARA_MATH_REPO_ROOT", "").strip()
        if repo_root_override:
            return Path(repo_root_override).expanduser()
        for parent in Path(__file__).resolve().parents:
            if (parent / "pyproject.toml").exists() or (parent / "research_lab.yaml").exists():
                return parent
        return Path(__file__).resolve().parents[3]

    def _library_search_entries(
        self,
        *,
        library_root_name: str,
        module_prefixes: tuple[str, ...],
        project_dir: Path | None = None,
    ) -> list[str]:
        repo_root = self._repo_root_for_local_library()
        formal_dir = repo_root / library_root_name / "formal"
        if not formal_dir.exists():
            return []
        if project_dir is not None and not self._project_imports_library(project_dir, module_prefixes):
            return []
        candidates = [formal_dir / ".lake" / "build" / "lib" / "lean"]
        if project_dir is not None:
            candidates.append(formal_dir)
        return [str(candidate) for candidate in candidates if candidate.exists()]

    def amra_library_search_entries(self, project_dir: Path | None = None) -> list[str]:
        return self._library_search_entries(
            library_root_name="amra_library",
            module_prefixes=("AmraLibrary",),
            project_dir=project_dir,
        )

    def legacy_ara_library_search_entries(self, project_dir: Path | None = None) -> list[str]:
        return self._library_search_entries(
            library_root_name="ara_library",
            module_prefixes=("AraLibrary",),
            project_dir=project_dir,
        )

    def ara_library_search_entries(self, project_dir: Path | None = None) -> list[str]:
        """Return canonical AMRA and deprecated ARA library search entries.

        The method name is retained for migration compatibility with older
        callers, but the canonical local library is `amra_library` with Lean
        module prefix `AmraLibrary`.
        """
        entries: list[str] = []
        seen: set[str] = set()
        for raw_entry in [
            *self.amra_library_search_entries(project_dir),
            *self.legacy_ara_library_search_entries(project_dir),
        ]:
            if raw_entry in seen:
                continue
            seen.add(raw_entry)
            entries.append(raw_entry)
        return entries

    def _discover_source_stage_plan(self, project_dir: Path) -> dict[str, Any]:
        candidates_payload = read_json(project_dir / "proof" / "porting_candidates.json", default={})
        porting_candidates = candidates_payload.get("candidates", [])
        target_sources = []
        for candidate in porting_candidates:
            source_path = Path(str(candidate.get("source_path", "")).strip())
            if candidate.get("import_ready") or not source_path.exists():
                continue
            aligned_with_target = candidate.get("aligned_with_target")
            if aligned_with_target is None:
                aligned_with_target = candidate.get("usable_for_main_claim")
            if aligned_with_target is None:
                aligned_with_target = True
            if not aligned_with_target:
                continue
            target_sources.append(source_path)

        if not target_sources:
            return {
                "status": "not_needed",
                "target_module_count": 0,
                "staged_module_count": 0,
                "compile_order": [],
                "modules": {},
                "unresolved_imports": [],
                "blocked_sources": [],
            }

        source_module_map: dict[str, Path] = {}
        target_modules: list[str] = []
        for source_path in target_sources:
            source_root, module_name = self._infer_source_root_and_module(source_path)
            target_modules.append(module_name)
            for lean_file in source_root.rglob("*.lean"):
                if ".lake" in lean_file.parts:
                    continue
                try:
                    root_hint, discovered = self._infer_source_root_and_module(lean_file)
                except ValueError:
                    continue
                if root_hint != source_root:
                    continue
                source_module_map.setdefault(discovered, lean_file)
            if source_root.name == "lean":
                fallback_candidates: dict[str, list[Path]] = {}
                for lean_file in source_root.parent.glob("*/*.lean"):
                    if ".lake" in lean_file.parts or lean_file.parent == source_root:
                        continue
                    fallback_candidates.setdefault(lean_file.stem, []).append(lean_file)
                for stem, paths in fallback_candidates.items():
                    best_path = sorted(
                        paths,
                        key=lambda path: (0 if "UnitaryPerfect" in path.parts else 1, len(path.parts), str(path)),
                    )[0]
                    source_module_map.setdefault(stem, best_path)

        local_asset_entries = self.discover_local_asset_search_entries(project_dir)
        compiled_modules, compiled_suffixes = self._compiled_module_index(local_asset_entries)
        staged_modules: dict[str, dict[str, Any]] = {}
        compile_order: list[str] = []
        unresolved_imports: list[dict[str, str]] = []
        blocked_sources: list[dict[str, Any]] = []
        resolving: set[str] = set()

        def unique_suffix_target(module_name: str) -> str | None:
            matches = compiled_suffixes.get(module_name, [])
            if len(matches) == 1:
                return matches[0]
            return None

        def ensure_module(module_name: str, requested_by: str) -> bool:
            if self._is_external_module(module_name):
                return True
            if module_name in compiled_modules or module_name in staged_modules:
                return True
            if module_name in resolving:
                return True
            source_path = source_module_map.get(module_name)
            shim_target = unique_suffix_target(module_name)
            if (
                shim_target
                and source_path is not None
                and "lean" not in source_path.parts
                and shim_target.endswith(f".{module_name}")
            ):
                shim_target = None
            if shim_target and shim_target != module_name:
                staged_modules[module_name] = {
                    "kind": "shim",
                    "target_import": shim_target,
                }
                compile_order.append(module_name)
                return True
            if source_path is None:
                unresolved_imports.append({"module": module_name, "requested_by": requested_by})
                return False
            source_audit = audit_lean_source_file(source_path)
            if source_audit["trust_level"] != "trusted":
                blocked_sources.append(
                    {
                        "module": module_name,
                        "requested_by": requested_by,
                        "source_path": str(source_path),
                        "source_audit": source_audit,
                    }
                )
                return False
            resolving.add(module_name)
            blocking_imports: list[str] = []
            imports = self._parse_imports(source_path)
            for import_name in imports:
                if not ensure_module(import_name, requested_by=module_name):
                    blocking_imports.append(import_name)
            resolving.remove(module_name)
            staged_modules[module_name] = {
                "kind": "copy",
                "source_path": str(source_path),
                "source_audit": source_audit,
                "imports": imports,
                "blocking_imports": blocking_imports,
            }
            compile_order.append(module_name)
            return True

        for module_name in target_modules:
            ensure_module(module_name, requested_by="project")

        if blocked_sources and not staged_modules:
            status = "blocked"
        elif blocked_sources or unresolved_imports:
            status = "partial"
        else:
            status = "ready"
        return {
            "status": status,
            "target_module_count": len(target_modules),
            "staged_module_count": len(staged_modules),
            "compile_order": compile_order,
            "modules": staged_modules,
            "unresolved_imports": unresolved_imports,
            "blocked_sources": blocked_sources,
        }

    def _stage_search_entries(self, formal_dir: Path, *, project_dir: Path) -> tuple[Path, Path]:
        staging_root = formal_dir / ".lake" / "ara_math_staging"
        return staging_root / "src", staging_root / "build" / "lib" / "lean"

    def stage_local_asset_modules(self, project_dir: Path, formal_dir: Path, lean_bin: str, timeout: int) -> dict[str, Any]:
        stage_plan = self._discover_source_stage_plan(project_dir)
        if stage_plan["status"] == "not_needed":
            return {
                **stage_plan,
                "compiled_module_count": 0,
                "compiled_modules": [],
                "diagnostics": [],
                "stage_source_root": "",
                "stage_build_root": "",
            }

        stage_source_root, stage_build_root = self._stage_search_entries(formal_dir, project_dir=project_dir)
        if stage_source_root.exists():
            shutil.rmtree(stage_source_root)
        stage_build_root.mkdir(parents=True, exist_ok=True)
        stage_source_root.mkdir(parents=True, exist_ok=True)

        staged_files: list[str] = []
        for module_name in stage_plan["compile_order"]:
            module_payload = stage_plan["modules"][module_name]
            target_path = stage_source_root / self._module_path(module_name).with_suffix(".lean")
            if module_payload["kind"] == "shim":
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(f"import {module_payload['target_import']}\n", encoding="utf-8")
            else:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(module_payload["source_path"], target_path)
            staged_files.append(str(target_path))

        lean_path_entries = self.lean_search_path_entries(formal_dir, project_dir=project_dir, staged_entries=[str(stage_build_root)])
        env = os.environ.copy()
        env["LEAN_PATH"] = ":".join(lean_path_entries)
        compiled_modules: list[str] = []
        diagnostics: list[str] = []
        commands: list[str] = []

        for module_name in stage_plan["compile_order"]:
            source_path = stage_source_root / self._module_path(module_name).with_suffix(".lean")
            output_base = stage_build_root / self._module_path(module_name)
            output_base.parent.mkdir(parents=True, exist_ok=True)
            command = [
                lean_bin,
                str(source_path),
                "-o",
                str(output_base.with_suffix(".olean")),
                "-i",
                str(output_base.with_suffix(".ilean")),
            ]
            commands.append(" ".join(command))
            completed = run_guarded_command(
                command,
                cwd=formal_dir,
                timeout=timeout,
                env=env,
                memory_mb=self.max_memory_mb,
                cpu_seconds=min(self.max_cpu_seconds, max(timeout + 10, timeout)),
                max_processes=self.max_processes,
                niceness=self.niceness,
            )
            if completed.returncode != 0:
                diagnostics.extend(self.extract_diagnostics(completed.stdout, completed.stderr))
                return {
                    **stage_plan,
                    "status": "failed",
                    "compiled_module_count": len(compiled_modules),
                    "compiled_modules": compiled_modules,
                    "diagnostics": diagnostics,
                    "command": commands,
                    "stage_source_root": str(stage_source_root),
                    "stage_build_root": str(stage_build_root),
                    "staged_files": staged_files,
                }
            compiled_modules.append(module_name)

        return {
            **stage_plan,
            "compiled_module_count": len(compiled_modules),
            "compiled_modules": compiled_modules,
            "diagnostics": diagnostics,
            "command": commands,
            "stage_source_root": str(stage_source_root),
            "stage_build_root": str(stage_build_root),
            "staged_files": staged_files,
        }

    def discover_local_asset_search_entries(self, project_dir: Path) -> list[str]:
        proof_path = read_json(project_dir / "idea" / "proof_path_assessment.json", default={})
        formal_preparation = read_json(project_dir / "artifacts" / "formal_preparation.json", default={})
        entries: list[str] = []
        seen: set[str] = set()
        for raw_entry in self.ara_library_search_entries(project_dir):
            if raw_entry not in seen:
                seen.add(raw_entry)
                entries.append(raw_entry)
        raw_candidates: list[str] = []
        for asset in proof_path.get("local_assets", []):
            raw_path = str(asset.get("path", "")).strip()
            if not raw_path:
                continue
            raw_candidates.append(raw_path)
        for raw_path in formal_preparation.get("seed_asset_paths", []):
            raw_path = str(raw_path).strip()
            if not raw_path:
                continue
            raw_candidates.append(raw_path)
        for raw_path in raw_candidates:
            path = Path(raw_path)
            if not path.exists():
                continue
            current = path if path.is_dir() else path.parent
            for candidate_root in (current, *current.parents):
                build_dir = candidate_root / ".lake" / "build" / "lib" / "lean"
                if build_dir.exists():
                    key = str(build_dir)
                    if key not in seen:
                        seen.add(key)
                        entries.append(key)
                source_root = candidate_root / "lean"
                if source_root.exists():
                    key = str(source_root)
                    if key not in seen:
                        seen.add(key)
                        entries.append(key)
                if any((candidate_root / name).is_dir() for name in ("UnitaryPerfect", "WeirdNumbers")):
                    key = str(candidate_root)
                    if key not in seen:
                        seen.add(key)
                        entries.append(key)
                    break
        return entries

    def discover_project_modules(self, formal_dir: Path) -> list[str]:
        modules: list[str] = []
        for lean_file in sorted(formal_dir.rglob("*.lean")):
            if ".lake" in lean_file.parts:
                continue
            if lean_file.name == "lakefile.lean":
                continue
            relative = lean_file.relative_to(formal_dir).with_suffix("")
            modules.append(".".join(relative.parts))
        return modules

    def discover_accessible_premise_support(self, project_dir: Path) -> dict[str, Any]:
        formal_dir = project_dir / "formal"
        project_modules = self.discover_project_modules(formal_dir) if formal_dir.exists() else []
        project_imports: set[str] = set()
        if formal_dir.exists():
            for lean_file in sorted(formal_dir.rglob("*.lean")):
                if ".lake" in lean_file.parts or lean_file.name == "lakefile.lean":
                    continue
                project_imports.update(self._parse_imports(lean_file))
        local_asset_entries = self.discover_local_asset_search_entries(project_dir)
        compiled_modules, compiled_suffixes = self._compiled_module_index(local_asset_entries)
        stage_plan = self._discover_source_stage_plan(project_dir)
        return {
            "generated_at": utc_now_iso(),
            "project_modules": project_modules,
            "project_imports": sorted(project_imports),
            "local_asset_search_entries": local_asset_entries,
            "compiled_modules": sorted(compiled_modules),
            "compiled_suffixes": compiled_suffixes,
            "stage_plan": stage_plan,
        }

    def lean_search_path_entries(
        self,
        formal_dir: Path,
        *,
        project_dir: Path | None = None,
        staged_entries: list[str] | None = None,
    ) -> list[str]:
        packages_dir = formal_dir / ".lake" / "packages"
        entries: list[str] = []
        if project_dir is not None:
            entries.extend(self.discover_local_asset_search_entries(project_dir))
        if packages_dir.exists():
            for package_dir in sorted(packages_dir.iterdir()):
                build_dir = package_dir / ".lake" / "build" / "lib" / "lean"
                if build_dir.exists():
                    entries.append(str(build_dir))
        if staged_entries:
            entries.extend(staged_entries)
        project_build_dir = formal_dir / ".lake" / "build" / "lib" / "lean"
        project_build_dir.mkdir(parents=True, exist_ok=True)
        entries.append(str(project_build_dir))
        deduped: list[str] = []
        seen: set[str] = set()
        for entry in entries:
            if entry in seen:
                continue
            seen.add(entry)
            deduped.append(entry)
        return deduped

    def run_direct_lean_verification(
        self,
        *,
        project_dir: Path,
        formal_dir: Path,
        lean_bin: str,
        timeout: int,
        staged_entries: list[str] | None = None,
    ) -> tuple[list[str], subprocess.CompletedProcess[str]]:
        modules = self.discover_project_modules(formal_dir)
        commands: list[str] = []
        completed: subprocess.CompletedProcess[str] | None = None
        lean_path = ":".join(self.lean_search_path_entries(formal_dir, project_dir=project_dir, staged_entries=staged_entries))
        env = os.environ.copy()
        env["LEAN_PATH"] = lean_path
        for module in modules:
            source = formal_dir / Path(*module.split(".")).with_suffix(".lean")
            output_base = formal_dir / ".lake" / "build" / "lib" / "lean" / Path(*module.split("."))
            output_base.parent.mkdir(parents=True, exist_ok=True)
            command = [
                lean_bin,
                str(source),
                "-o",
                str(output_base.with_suffix(".olean")),
                "-i",
                str(output_base.with_suffix(".ilean")),
            ]
            commands.append(" ".join(command))
            completed = run_guarded_command(
                command,
                cwd=formal_dir,
                timeout=timeout,
                env=env,
                memory_mb=self.max_memory_mb,
                cpu_seconds=min(self.max_cpu_seconds, max(timeout + 10, timeout)),
                max_processes=self.max_processes,
                niceness=self.niceness,
            )
            if completed.returncode != 0:
                return commands, completed
        return commands, completed or subprocess.CompletedProcess([lean_bin], 0, "", "")

    def discover_manifest_candidates(self, formal_dir: Path) -> list[dict[str, Any]]:
        signature = self.manifest_signature(formal_dir)
        search_roots = self.cache_search_roots or self.default_search_roots(formal_dir)
        target_manifest = formal_dir / "lake-manifest.json"
        candidates: list[dict[str, Any]] = []
        for root in search_roots:
            for manifest_path in root.rglob("lake-manifest.json"):
                if manifest_path == target_manifest:
                    continue
                candidate_formal = manifest_path.parent
                if self.manifest_signature(candidate_formal) != signature:
                    continue
                packages_state = self.package_cache_state(candidate_formal)
                if packages_state != "ready":
                    continue
                candidates.append(
                    {
                        "manifest_path": manifest_path,
                        "formal_dir": candidate_formal,
                        "packages_state": packages_state,
                    }
                )
        candidates.sort(key=lambda item: len(str(item["formal_dir"])))
        return candidates

    def prepare_manifest(self, formal_dir: Path) -> dict[str, Any]:
        manifest_path = formal_dir / "lake-manifest.json"
        report: dict[str, Any] = {
            "target_manifest_path": str(manifest_path),
            "status": "not_needed",
            "selected_source": "",
            "candidate_count": 0,
        }
        if manifest_path.exists():
            report["status"] = "existing"
            report["selected_source"] = str(manifest_path)
            return report
        candidates = self.discover_manifest_candidates(formal_dir)
        report["candidate_count"] = len(candidates)
        if not candidates:
            report["status"] = "not_found"
            return report
        selected = candidates[0]
        shutil.copy2(selected["manifest_path"], manifest_path)
        report.update(
            {
                "status": "copied",
                "selected_source": str(selected["manifest_path"]),
                "selected_formal_dir": str(selected["formal_dir"]),
            }
        )
        return report

    def build(self, project_dir: Path, timeout_sec: int | None = None) -> LeanBuildReport:
        formal_dir = project_dir / "formal"
        timeout = timeout_sec or self.timeout_sec
        lake_bin = self.resolve_binary("lake")
        lean_bin = self.resolve_binary("lean")
        toolchain = {"lake": lake_bin, "lean": lean_bin}
        reuse_report = self.prepare_package_cache(formal_dir) if formal_dir.exists() else {}
        manifest_report = self.prepare_manifest(formal_dir) if formal_dir.exists() else {}
        local_asset_entries = self.discover_local_asset_search_entries(project_dir) if formal_dir.exists() else []
        reuse_payload = {**reuse_report, "manifest": manifest_report, "local_asset_search_entries": local_asset_entries}
        direct_verify_mode = self.direct_lean_verify or bool(local_asset_entries)
        resource_policy = build_resource_policy(
            memory_mb=self.max_memory_mb,
            cpu_seconds=min(self.max_cpu_seconds, max(timeout + 10, timeout)),
            max_processes=self.max_processes,
            niceness=self.niceness,
            allow_cold_cache=self.allow_cold_cache,
        )
        resource_policy["olean_only"] = self.olean_only
        resource_policy["direct_lean_verify"] = direct_verify_mode
        resource_policy["local_asset_search_entries"] = local_asset_entries
        system_guard = check_system_headroom(
            min_available_memory_mb=self.min_available_memory_mb,
            max_load_per_cpu=self.max_load_per_cpu,
        )

        if not formal_dir.exists():
            return LeanBuildReport(
                status="blocked",
                command=[],
                workdir=str(formal_dir),
                generated_at=utc_now_iso(),
                build_seconds=0.0,
                returncode=None,
                sorry_count=0,
                toolchain=toolchain,
                reuse_report=reuse_payload,
                resource_policy=resource_policy,
                system_guard=system_guard,
                summary="The project has no formal/ workspace.",
                diagnostics=["Missing formal/ directory."],
            )

        if not lake_bin and not (direct_verify_mode and lean_bin):
            return LeanBuildReport(
                status="blocked",
                command=[],
                workdir=str(formal_dir),
                generated_at=utc_now_iso(),
                build_seconds=0.0,
                returncode=None,
                sorry_count=self.count_sorries(formal_dir),
                toolchain=toolchain,
                reuse_report=reuse_payload,
                resource_policy=resource_policy,
                system_guard=system_guard,
                summary="`lake` was not found. Install Lean 4 tooling before build verification.",
                diagnostics=["Lean toolchain missing: `lake` executable not found."],
            )

        if direct_verify_mode and not lean_bin:
            return LeanBuildReport(
                status="blocked",
                command=[],
                workdir=str(formal_dir),
                generated_at=utc_now_iso(),
                build_seconds=0.0,
                returncode=None,
                sorry_count=self.count_sorries(formal_dir),
                toolchain=toolchain,
                reuse_report=reuse_payload,
                resource_policy=resource_policy,
                system_guard=system_guard,
                summary="Direct Lean verification was selected, but the `lean` executable is unavailable.",
                diagnostics=["Lean toolchain missing: `lean` executable not found."],
            )

        if system_guard["status"] != "ready":
            return LeanBuildReport(
                status="blocked",
                command=[],
                workdir=str(formal_dir),
                generated_at=utc_now_iso(),
                build_seconds=0.0,
                returncode=None,
                sorry_count=self.count_sorries(formal_dir),
                toolchain=toolchain,
                reuse_report=reuse_payload,
                resource_policy=resource_policy,
                system_guard=system_guard,
                summary="System load guard blocked the Lean build before launch.",
                diagnostics=system_guard["blockers"],
            )

        if manifest_report.get("status") == "not_found" and not direct_verify_mode:
            diagnostics = [
                "No reusable `lake-manifest.json` was found for this project.",
                "Guarded mode refuses a first-time dependency resolution because it may trigger network fetches and heavy local rebuilds.",
            ]
            return LeanBuildReport(
                status="blocked",
                command=[],
                workdir=str(formal_dir),
                generated_at=utc_now_iso(),
                build_seconds=0.0,
                returncode=None,
                sorry_count=self.count_sorries(formal_dir),
                toolchain=toolchain,
                reuse_report=reuse_payload,
                resource_policy=resource_policy,
                system_guard=system_guard,
                summary="Lean manifest is missing and guarded mode will not create one from scratch.",
                diagnostics=diagnostics,
            )

        cache_state = self.package_cache_state(formal_dir)
        if not self.allow_cold_cache and cache_state != "ready":
            diagnostics = [
                "Lean dependency cache is not build-ready.",
                "Refusing a cold-cache build in guarded mode to avoid large local compiles and accidental workstation stalls.",
            ]
            if cache_state == "missing":
                diagnostics.append("No reusable `.lake/packages` cache was linked for this project.")
            else:
                diagnostics.append("The linked `.lake/packages` exists but does not contain a ready mathlib build cache.")
            return LeanBuildReport(
                status="blocked",
                command=[],
                workdir=str(formal_dir),
                generated_at=utc_now_iso(),
                build_seconds=0.0,
                returncode=None,
                sorry_count=self.count_sorries(formal_dir),
                toolchain=toolchain,
                reuse_report=reuse_payload,
                resource_policy=resource_policy,
                system_guard=system_guard,
                summary="Cold-cache Lean builds are disabled by default in AMRA guarded mode.",
                diagnostics=diagnostics,
            )

        started = time.monotonic()
        fallback_triggered = False
        staged_entries: list[str] = []
        staging_report: dict[str, Any] = {}
        if direct_verify_mode and lean_bin:
            staging_report = self.stage_local_asset_modules(project_dir, formal_dir, lean_bin, timeout)
            reuse_payload["staging"] = staging_report
            if staging_report.get("status") in {"ready", "partial"} and staging_report.get("compiled_module_count", 0) > 0:
                staged_entries.append(staging_report["stage_build_root"])
        try:
            if direct_verify_mode and lean_bin:
                commands, completed = self.run_direct_lean_verification(
                    project_dir=project_dir,
                    formal_dir=formal_dir,
                    lean_bin=lean_bin,
                    timeout=timeout,
                    staged_entries=staged_entries,
                )
                command = ["direct-lean-verify", *commands]
            else:
                if self.olean_only:
                    module_targets = [f"+{module}:olean" for module in self.discover_project_modules(formal_dir)]
                    command = [lake_bin, "build", *module_targets]
                else:
                    command = [lake_bin, "build"]
                completed = self.run_command(command, cwd=formal_dir, timeout=timeout)
                if completed.returncode != 0 and lean_bin and self.should_retry_with_direct_verify(completed.stdout, completed.stderr):
                    fallback_triggered = True
                    commands, completed = self.run_direct_lean_verification(
                        project_dir=project_dir,
                        formal_dir=formal_dir,
                        lean_bin=lean_bin,
                        timeout=timeout,
                        staged_entries=staged_entries,
                    )
                    command = ["lake-build-fallback", *commands]
        except subprocess.TimeoutExpired as exc:
            return LeanBuildReport(
                status="timeout",
                command=command,
                workdir=str(formal_dir),
                generated_at=utc_now_iso(),
                build_seconds=round(time.monotonic() - started, 3),
                returncode=None,
                sorry_count=self.count_sorries(formal_dir),
                toolchain=toolchain,
                reuse_report=reuse_payload,
                resource_policy=resource_policy,
                system_guard=system_guard,
                stdout_tail=self.coerce_text(exc.stdout)[-6000:],
                stderr_tail=self.coerce_text(exc.stderr)[-6000:],
                diagnostics=["Lean build timed out."],
                summary=f"Lean build exceeded the timeout of {timeout} seconds.",
            )

        build_seconds = round(time.monotonic() - started, 3)
        sorry_count = self.count_sorries(formal_dir)
        diagnostics = self.extract_diagnostics(completed.stdout, completed.stderr)
        blocked_sources = (staging_report or {}).get("blocked_sources", [])
        if blocked_sources:
            diagnostics.extend(
                [
                    f"Blocked unsafe companion module `{item['module']}` from {item['source_path']} "
                    f"(sorry={item['source_audit']['counts']['sorry']}, "
                    f"axiom={item['source_audit']['counts']['axiom']}, "
                    f"admit={item['source_audit']['counts']['admit']}, "
                    f"placeholder={item['source_audit']['counts']['placeholder']})."
                    for item in blocked_sources[:10]
                ]
            )

        if completed.returncode != 0:
            status = "failed"
            if "failed to create thread" in completed.stderr.lower():
                status = "blocked"
                diagnostics = [*diagnostics, "Lean hit the guarded process/thread ceiling during build."]
                summary = "Lean build was blocked by the guarded process/thread ceiling."
            else:
                summary = "Lean build failed."
        elif blocked_sources and sorry_count == 0:
            status = "needs_attention"
            summary = "Lean build passed, but companion source modules were blocked because they still contain unfinished or axiomatic content."
        elif sorry_count > 0:
            status = "needs_attention"
            summary = "Lean build passed, but unresolved `sorry` placeholders remain."
        else:
            status = "passed"
            summary = "Lean build passed with no detected `sorry` placeholders."
        if staging_report.get("compiled_module_count", 0) > 0 and status in {"passed", "needs_attention"}:
            summary = f"{summary} Staged {staging_report['compiled_module_count']} local companion modules for direct verification."
        if fallback_triggered and status in {"passed", "needs_attention"}:
            summary = f"{summary} Used direct Lean verification after `lake build` hit import/cache issues."

        return LeanBuildReport(
            status=status,
            command=command,
            workdir=str(formal_dir),
            generated_at=utc_now_iso(),
            build_seconds=build_seconds,
            returncode=completed.returncode,
            sorry_count=sorry_count,
            diagnostics=diagnostics,
            stdout_tail=completed.stdout[-6000:],
            stderr_tail=completed.stderr[-6000:],
            toolchain=toolchain,
            reuse_report=reuse_payload,
            resource_policy=resource_policy,
            system_guard=system_guard,
            summary=summary,
        )
