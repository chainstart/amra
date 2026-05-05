from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ara_math.lean import LeanExecutor
from ara_math.workspace import read_json, utc_now_iso, write_json, write_text


DECLARATION_PATTERN = re.compile(
    r"^\s*(?:@[^\n]+\s*)*(?:noncomputable\s+)?"
    r"(theorem|lemma|def|abbrev|instance|class|structure|inductive)\s+([A-Za-z0-9_'.]+)\b"
)


def _module_to_path(module_name: str) -> Path:
    parts = module_name.split(".")
    if len(parts) < 2 or parts[0] != "AraLibrary":
        raise ValueError("ARA library modules must be named like `AraLibrary.NumberTheory.Carmichael`.")
    return Path(*parts).with_suffix(".lean")


def _normalise_imports(imports: list[str] | None) -> list[str]:
    cleaned: list[str] = []
    seen: set[str] = set()
    for item in imports or ["Mathlib"]:
        value = str(item).strip()
        if not value or value in seen:
            continue
        seen.add(value)
        cleaned.append(value)
    return cleaned or ["Mathlib"]


class AraLibraryManager:
    """Manage reusable Lean modules that fill gaps outside upstream mathlib."""

    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.library_root = repo_root / "ara_library"
        self.formal_dir = self.library_root / "formal"
        self.registry_path = self.library_root / "registry.json"
        self.readme_path = self.library_root / "README.md"

    def _registry(self) -> dict[str, Any]:
        payload = read_json(self.registry_path, default={})
        if not isinstance(payload, dict):
            payload = {}
        return {
            "generated_at": str(payload.get("generated_at", "")).strip() or utc_now_iso(),
            "library_root": str(payload.get("library_root", self.library_root)),
            "modules": list(payload.get("modules", [])),
        }

    def _write_registry(self, payload: dict[str, Any]) -> None:
        payload["generated_at"] = utc_now_iso()
        payload["library_root"] = str(self.library_root)
        write_json(self.registry_path, payload)

    def ensure_library(self) -> dict[str, Any]:
        self.formal_dir.mkdir(parents=True, exist_ok=True)
        (self.formal_dir / "AraLibrary").mkdir(parents=True, exist_ok=True)
        lakefile = self.formal_dir / "lakefile.lean"
        if not lakefile.exists():
            write_text(
                lakefile,
                "\n".join(
                    [
                        "import Lake",
                        "open Lake DSL",
                        "",
                        "package AraLibrary where",
                        "  leanOptions := #[",
                        "    \u27e8`autoImplicit, false\u27e9",
                        "  ]",
                        "",
                        "require mathlib from git",
                        "  \"https://github.com/leanprover-community/mathlib4\" @ \"v4.26.0\"",
                        "",
                        "@[default_target]",
                        "lean_lib AraLibrary",
                        "",
                    ]
                ),
            )
        toolchain = self.formal_dir / "lean-toolchain"
        if not toolchain.exists():
            write_text(toolchain, "leanprover/lean4:v4.26.0\n")
        root_module = self.formal_dir / "AraLibrary.lean"
        if not root_module.exists():
            write_text(
                root_module,
                "\n".join(
                    [
                        "/-!",
                        "Reusable ARA Math library modules.",
                        "",
                        "This package contains Lean code for useful theorems and APIs that are",
                        "not yet available in upstream mathlib or are being prepared for a future",
                        "mathlib contribution.",
                        "-/",
                        "",
                    ]
                ),
            )
        if not self.readme_path.exists():
            write_text(
                self.readme_path,
                "\n".join(
                    [
                        "# ARA Local Math Library",
                        "",
                        "This directory stores reusable Lean modules for mathematics that is not",
                        "yet available in upstream mathlib, or that needs to be staged before a",
                        "mathlib PR. ARA projects automatically add this library to their Lean",
                        "search path during guarded verification.",
                        "",
                        "Code promoted here should be reusable, source-attributed, and free of",
                        "`sorry`, `axiom`, `constant`, `opaque`, `admit`, and placeholder markers",
                        "before it is treated as a trusted premise.",
                        "",
                    ]
                ),
            )
        if not self.registry_path.exists():
            self._write_registry({"modules": []})
        return self.inventory()

    def _sync_root_imports(self, modules: list[dict[str, Any]]) -> None:
        imports = sorted({str(module.get("module_name", "")).strip() for module in modules if module.get("module_name")})
        lines = [
            "/-!",
            "Reusable ARA Math library modules.",
            "",
            "This file imports every registered reusable module.",
            "-/",
            "",
        ]
        lines.extend(f"import {module_name}" for module_name in imports)
        lines.append("")
        write_text(self.formal_dir / "AraLibrary.lean", "\n".join(lines))

    def _upsert_module(self, entry: dict[str, Any]) -> dict[str, Any]:
        registry = self._registry()
        modules = [
            module
            for module in registry.get("modules", [])
            if str(module.get("module_name", "")).strip() != entry["module_name"]
        ]
        existing = next(
            (module for module in registry.get("modules", []) if str(module.get("module_name", "")).strip() == entry["module_name"]),
            {},
        )
        merged = {
            **existing,
            **entry,
            "created_at": str(existing.get("created_at", "")).strip() or utc_now_iso(),
            "updated_at": utc_now_iso(),
        }
        modules.append(merged)
        modules.sort(key=lambda item: str(item.get("module_name", "")))
        registry["modules"] = modules
        self._write_registry(registry)
        self._sync_root_imports(modules)
        return merged

    def add_module(
        self,
        *,
        module_name: str,
        imports: list[str] | None = None,
        title: str = "",
        domain: str = "",
        status: str = "candidate",
        tags: list[str] | None = None,
        description: str = "",
    ) -> dict[str, Any]:
        self.ensure_library()
        module_path = self.formal_dir / _module_to_path(module_name)
        module_path.parent.mkdir(parents=True, exist_ok=True)
        if not module_path.exists():
            import_lines = [f"import {item}" for item in _normalise_imports(imports)]
            write_text(
                module_path,
                "\n".join(
                    [
                        "/-!",
                        title or module_name,
                        "",
                        description or "Reusable ARA Math library module.",
                        "-/",
                        "",
                        *import_lines,
                        "",
                        "namespace AraLibrary",
                        "",
                        "",
                        "end AraLibrary",
                        "",
                    ]
                ),
            )
        entry = self._upsert_module(
            {
                "module_name": module_name,
                "path": str(module_path.relative_to(self.library_root)),
                "title": title,
                "domain": domain,
                "status": status,
                "tags": [str(tag) for tag in tags or []],
                "description": description,
                "declarations": self._scan_module_declarations(module_path),
            }
        )
        return {"status": "module_ready", "module": entry, "path": str(module_path)}

    def _declaration_blocks(self, source_file: Path, names: list[str]) -> list[dict[str, Any]]:
        lines = source_file.read_text(encoding="utf-8", errors="ignore").splitlines()
        matches: list[dict[str, Any]] = []
        declaration_starts: list[tuple[int, str, str]] = []
        for index, line in enumerate(lines):
            match = DECLARATION_PATTERN.match(line)
            if match:
                declaration_starts.append((index, match.group(1), match.group(2)))
        start_by_name = {name: (index, kind) for index, kind, name in declaration_starts}
        all_starts = [index for index, _, _ in declaration_starts]
        for name in names:
            if name not in start_by_name:
                matches.append({"name": name, "found": False, "block": ""})
                continue
            start, kind = start_by_name[name]
            doc_start = start
            cursor = start - 1
            while cursor >= 0:
                stripped = lines[cursor].strip()
                if stripped == "":
                    break
                if stripped.startswith("/--") or stripped.startswith("--") or stripped.startswith("-/") or stripped.startswith("*"):
                    doc_start = cursor
                    cursor -= 1
                    continue
                break
            later_starts = [item for item in all_starts if item > start]
            end = later_starts[0] if later_starts else len(lines)
            matches.append(
                {
                    "name": name,
                    "kind": kind,
                    "found": True,
                    "source_line": start + 1,
                    "block": "\n".join(lines[doc_start:end]).rstrip(),
                }
            )
        return matches

    def promote_declarations(
        self,
        *,
        source_file: Path,
        module_name: str,
        declarations: list[str],
        imports: list[str] | None = None,
        title: str = "",
        domain: str = "",
        status: str = "candidate",
        tags: list[str] | None = None,
        description: str = "",
        source_project: Path | None = None,
    ) -> dict[str, Any]:
        if not declarations:
            raise ValueError("At least one declaration name is required.")
        if not source_file.exists():
            raise FileNotFoundError(f"Source Lean file does not exist: {source_file}")
        self.ensure_library()
        module_report = self.add_module(
            module_name=module_name,
            imports=imports,
            title=title or module_name,
            domain=domain,
            status=status,
            tags=tags,
            description=description or f"Declarations promoted from {source_file}.",
        )
        module_path = Path(module_report["path"])
        blocks = self._declaration_blocks(source_file, declarations)
        missing = [item["name"] for item in blocks if not item.get("found")]
        found_blocks = [item for item in blocks if item.get("found")]
        if found_blocks:
            text = module_path.read_text(encoding="utf-8")
            insertion = "\n\n".join(item["block"] for item in found_blocks).strip()
            provenance = "\n".join(
                [
                    "",
                    "/-!",
                    "## Promotion provenance",
                    f"- Source file: `{source_file}`",
                    f"- Source project: `{source_project or ''}`",
                    f"- Promoted at: `{utc_now_iso()}`",
                    "-/",
                    "",
                    insertion,
                    "",
                ]
            )
            if "\nend AraLibrary" in text:
                text = text.replace("\nend AraLibrary", provenance + "\nend AraLibrary", 1)
            else:
                text = text.rstrip() + "\n" + provenance
            write_text(module_path, text)
        entry = self._upsert_module(
            {
                **module_report["module"],
                "source_file": str(source_file),
                "source_project": str(source_project or ""),
                "promoted_declarations": declarations,
                "missing_declarations": missing,
                "declarations": self._scan_module_declarations(module_path),
                "status": status,
            }
        )
        return {
            "status": "promoted" if not missing else "partial",
            "module": entry,
            "path": str(module_path),
            "promoted_declarations": [item["name"] for item in found_blocks],
            "missing_declarations": missing,
        }

    def _scan_module_declarations(self, module_path: Path) -> list[dict[str, Any]]:
        if not module_path.exists():
            return []
        declarations: list[dict[str, Any]] = []
        for line_number, line in enumerate(module_path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
            match = DECLARATION_PATTERN.match(line)
            if not match:
                continue
            declarations.append({"kind": match.group(1), "name": match.group(2), "line": line_number})
        return declarations

    def inventory(self) -> dict[str, Any]:
        self.library_root.mkdir(parents=True, exist_ok=True)
        registry = self._registry()
        modules = []
        for module in registry.get("modules", []):
            path = self.library_root / str(module.get("path", ""))
            modules.append(
                {
                    **module,
                    "exists": path.exists(),
                    "absolute_path": str(path),
                    "declarations": self._scan_module_declarations(path),
                }
            )
        return {
            "generated_at": utc_now_iso(),
            "library_root": str(self.library_root),
            "formal_dir": str(self.formal_dir),
            "registry_path": str(self.registry_path),
            "module_count": len(modules),
            "modules": modules,
        }

    def build(self, *, timeout_sec: int | None = None, allow_cold_cache: bool = False) -> dict[str, Any]:
        self.ensure_library()
        executor = LeanExecutor(allow_cold_cache=allow_cold_cache)
        report = executor.build(self.library_root, timeout_sec=timeout_sec)
        write_json(self.library_root / "build_report.json", report.to_dict())
        return report.to_dict()
