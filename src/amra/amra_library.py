from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from amra.core.workspace import read_json, utc_now_iso, write_json, write_text
from amra.lean import LeanExecutor


AMRA_LIBRARY_ROOT = "amra_library"
AMRA_MODULE_PREFIX = "AmraLibrary"
LEGACY_LIBRARY_ROOT = "ara_library"
LEGACY_MODULE_PREFIX = "AraLibrary"

DECLARATION_PATTERN = re.compile(
    r"^\s*(?:@[^\n]+\s*)*(?:(?:private|protected|noncomputable|unsafe|partial)\s+)*"
    r"(theorem|lemma|def|abbrev|instance|class|structure|inductive)\s+([A-Za-z_][A-Za-z0-9_'.!?]*)\b"
)
FORBIDDEN_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("sorry", re.compile(r"\bsorry\b")),
    ("admit", re.compile(r"\badmit\b")),
    ("axiom", re.compile(r"^\s*axiom\b", re.MULTILINE)),
    ("constant", re.compile(r"^\s*constant\b", re.MULTILINE)),
    ("opaque", re.compile(r"^\s*opaque\b", re.MULTILINE)),
    ("placeholder", re.compile(r"(?:ARA_MATH_PLACEHOLDER|AMRA_PLACEHOLDER|\w*placeholder\w*)", re.IGNORECASE)),
)
VERIFIED_STATUSES = {"lean_verified", "verified", "passed", "trusted"}


def _module_to_path(module_name: str, *, module_prefix: str) -> Path:
    parts = module_name.split(".")
    if len(parts) < 2 or parts[0] != module_prefix:
        raise ValueError(f"AMRA library modules must be named like `{module_prefix}.NumberTheory.Carmichael`.")
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


def _strip_lean_comments(text: str) -> str:
    without_blocks = LeanExecutor.BLOCK_COMMENT_PATTERN.sub("", text)
    return LeanExecutor.LINE_COMMENT_PATTERN.sub("", without_blocks)


class AmraLibraryManager:
    """Manage reusable Lean modules harvested into the canonical AMRA library."""

    def __init__(
        self,
        *,
        repo_root: Path,
        library_root_name: str = AMRA_LIBRARY_ROOT,
        module_prefix: str = AMRA_MODULE_PREFIX,
        legacy_module_prefix: str = LEGACY_MODULE_PREFIX,
        display_name: str = "AMRA",
        require_source_verification: bool = True,
    ) -> None:
        self.repo_root = repo_root
        self.library_root_name = library_root_name
        self.module_prefix = module_prefix
        self.legacy_module_prefix = legacy_module_prefix
        self.display_name = display_name
        self.require_source_verification = require_source_verification
        self.library_root = repo_root / library_root_name
        self.formal_dir = self.library_root / "formal"
        self.registry_path = self.library_root / "registry.json"
        self.readme_path = self.library_root / "README.md"

    def normalise_module_name(self, module_name: str) -> str:
        value = str(module_name).strip()
        if not value:
            raise ValueError("Library module name must not be empty.")
        if value == self.module_prefix or value.startswith(f"{self.module_prefix}."):
            return value
        if value == self.legacy_module_prefix or value.startswith(f"{self.legacy_module_prefix}."):
            return self.module_prefix + value[len(self.legacy_module_prefix) :]
        raise ValueError(f"AMRA library modules must be named like `{self.module_prefix}.NumberTheory.Carmichael`.")

    def audit_source_text(self, text: str) -> dict[str, Any]:
        stripped = _strip_lean_comments(text)
        counts = {name: len(pattern.findall(stripped)) for name, pattern in FORBIDDEN_PATTERNS}
        issue_count = sum(counts.values())
        return {
            "trust_level": "trusted" if issue_count == 0 else "unsafe",
            "issue_count": issue_count,
            "counts": counts,
        }

    def audit_source_file(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            return {
                "trust_level": "missing",
                "issue_count": 0,
                "counts": {name: 0 for name, _ in FORBIDDEN_PATTERNS},
                "path": str(path),
            }
        return {
            **self.audit_source_text(path.read_text(encoding="utf-8", errors="ignore")),
            "path": str(path),
        }

    def _registry(self) -> dict[str, Any]:
        payload = read_json(self.registry_path, default={})
        if not isinstance(payload, dict):
            payload = {}
        return {
            "schema_version": "amra.library_registry.v1",
            "generated_at": str(payload.get("generated_at", "")).strip() or utc_now_iso(),
            "library_root": str(payload.get("library_root", self.library_root)),
            "module_prefix": str(payload.get("module_prefix", self.module_prefix)),
            "modules": list(payload.get("modules", [])),
        }

    def _write_registry(self, payload: dict[str, Any]) -> None:
        payload["schema_version"] = "amra.library_registry.v1"
        payload["generated_at"] = utc_now_iso()
        payload["library_root"] = str(self.library_root)
        payload["module_prefix"] = self.module_prefix
        write_json(self.registry_path, payload)

    def ensure_library(self) -> dict[str, Any]:
        self.formal_dir.mkdir(parents=True, exist_ok=True)
        (self.formal_dir / self.module_prefix).mkdir(parents=True, exist_ok=True)
        lakefile = self.formal_dir / "lakefile.lean"
        if not lakefile.exists():
            write_text(
                lakefile,
                "\n".join(
                    [
                        "import Lake",
                        "open Lake DSL",
                        "",
                        f"package {self.module_prefix} where",
                        "",
                        "require mathlib from git",
                        '  "https://github.com/leanprover-community/mathlib4" @ "v4.26.0"',
                        "",
                        "@[default_target]",
                        f"lean_lib {self.module_prefix}",
                        "",
                    ]
                ),
            )
        toolchain = self.formal_dir / "lean-toolchain"
        if not toolchain.exists():
            write_text(toolchain, "leanprover/lean4:v4.26.0\n")
        manifest = self.formal_dir / "lake-manifest.json"
        legacy_manifest = self.repo_root / LEGACY_LIBRARY_ROOT / "formal" / "lake-manifest.json"
        if not manifest.exists() and legacy_manifest.exists():
            payload = read_json(legacy_manifest, default={})
            if isinstance(payload, dict) and payload:
                payload["name"] = self.module_prefix
                write_json(manifest, payload)
        root_module = self.formal_dir / f"{self.module_prefix}.lean"
        if not root_module.exists():
            write_text(
                root_module,
                "\n".join(
                    [
                        "/-!",
                        f"Reusable {self.display_name} Math library modules.",
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
                        f"# {self.display_name} Local Math Library",
                        "",
                        "This directory stores reusable Lean modules for mathematics that is not",
                        "yet available in upstream mathlib, or that needs to be staged before a",
                        f"mathlib PR. {self.display_name} projects add this library to their Lean",
                        "search path during guarded verification when they import it.",
                        "",
                        "Code promoted here must be reusable, source-attributed, Lean-verified,",
                        "and free of `sorry`, `axiom`, `constant`, `opaque`, `admit`, and",
                        "placeholder markers before it is treated as a trusted premise.",
                        "",
                    ]
                ),
            )
        if not self.registry_path.exists():
            self._write_registry({"modules": []})
        return self.inventory()

    def _import_hints(self, module_name: str, declarations: list[str] | None = None) -> list[str]:
        hints = [f"import {module_name}"]
        for declaration in declarations or []:
            hints.append(f"open {self.module_prefix} -- enables `{declaration}` after importing {module_name}")
        return hints

    def _sync_root_imports(self, modules: list[dict[str, Any]]) -> None:
        imports = sorted({str(module.get("module_name", "")).strip() for module in modules if module.get("module_name")})
        lines = [f"import {module_name}" for module_name in imports]
        lines.extend(
            [
                "",
                "/-!",
                f"Reusable {self.display_name} Math library modules.",
                "",
                "This file imports every registered reusable module.",
                "-/",
                "",
            ]
        )
        write_text(self.formal_dir / f"{self.module_prefix}.lean", "\n".join(lines))

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
        normalized_module_name = self.normalise_module_name(module_name)
        module_path = self.formal_dir / _module_to_path(normalized_module_name, module_prefix=self.module_prefix)
        module_path.parent.mkdir(parents=True, exist_ok=True)
        if not module_path.exists():
            import_lines = [f"import {item}" for item in _normalise_imports(imports)]
            write_text(
                module_path,
                "\n".join(
                    [
                        "/-!",
                        title or normalized_module_name,
                        "",
                        description or f"Reusable {self.display_name} Math library module.",
                        "-/",
                        "",
                        *import_lines,
                        "",
                        f"namespace {self.module_prefix}",
                        "",
                        "",
                        f"end {self.module_prefix}",
                        "",
                    ]
                ),
            )
        declarations = self._scan_module_declarations(module_path)
        entry = self._upsert_module(
            {
                "module_name": normalized_module_name,
                "legacy_module_name": module_name if module_name != normalized_module_name else "",
                "path": str(module_path.relative_to(self.library_root)),
                "title": title,
                "domain": domain,
                "status": status,
                "tags": [str(tag) for tag in tags or []],
                "description": description,
                "declarations": declarations,
                "import_hints": self._import_hints(normalized_module_name, [item["name"] for item in declarations]),
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

        def leading_indent(line: str) -> int:
            return len(line) - len(line.lstrip())

        def starts_new_top_level_item(line: str, declaration_indent: int) -> bool:
            stripped = line.strip()
            if not stripped or leading_indent(line) > declaration_indent:
                return False
            return (
                stripped == "end"
                or stripped.startswith("end ")
                or stripped.startswith("namespace ")
                or stripped.startswith("section ")
                or stripped.startswith("open ")
                or stripped.startswith("variable ")
                or stripped.startswith("import ")
                or stripped.startswith("/-!")
            )

        for name in names:
            short_name = name.split(".")[-1]
            lookup_name = name if name in start_by_name else short_name
            if lookup_name not in start_by_name:
                matches.append({"name": name, "found": False, "block": ""})
                continue
            start, kind = start_by_name[lookup_name]
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
            declaration_indent = leading_indent(lines[start])
            for cursor in range(start + 1, end):
                if starts_new_top_level_item(lines[cursor], declaration_indent):
                    end = cursor
                    break
            while end > doc_start and lines[end - 1].strip() == "":
                end -= 1
            block = "\n".join(lines[doc_start:end]).rstrip()
            matches.append(
                {
                    "name": lookup_name,
                    "requested_name": name,
                    "kind": kind,
                    "found": True,
                    "source_line": start + 1,
                    "block": block,
                    "source_audit": self.audit_source_text(block),
                }
            )
        return matches

    def _infer_source_project(self, source_file: Path) -> Path | None:
        if "formal" in source_file.parts:
            index = source_file.parts.index("formal")
            if index > 0:
                return Path(*source_file.parts[:index])
        return None

    def _build_report_paths(self, source_project: Path) -> list[Path]:
        return [
            source_project / "artifacts" / "lean_build_report.json",
            source_project / "build_report.json",
            source_project / "formal" / "build_report.json",
        ]

    def _load_source_build_report(self, source_project: Path | None) -> dict[str, Any]:
        if source_project is None:
            return {}
        for path in self._build_report_paths(source_project):
            payload = read_json(path, default={})
            if isinstance(payload, dict) and payload:
                return {**payload, "path": str(path)}
        return {}

    def _verified_declaration_names(self, source_project: Path | None) -> set[str]:
        if source_project is None:
            return set()
        payload = read_json(source_project / "verified_declarations.json", default={})
        declarations = payload.get("declarations", []) if isinstance(payload, dict) else []
        names: set[str] = set()
        for item in declarations:
            if not isinstance(item, dict):
                continue
            status = str(item.get("status") or "lean_verified").strip().lower()
            if status and status not in VERIFIED_STATUSES:
                continue
            for key in ("name", "full_name", "lean_name"):
                value = str(item.get(key, "")).strip()
                if value:
                    names.add(value)
                    names.add(value.split(".")[-1])
        return names

    def _source_verification_report(
        self,
        *,
        source_file: Path,
        source_project: Path | None,
        declarations: list[str],
    ) -> dict[str, Any]:
        inferred_project = source_project or self._infer_source_project(source_file)
        build_report = self._load_source_build_report(inferred_project)
        verified_names = self._verified_declaration_names(inferred_project)
        build_status = str(build_report.get("status", "")).strip().lower()
        sorry_count = int(build_report.get("sorry_count", 0) or 0) if build_report else 0
        build_passed = build_status in {"passed", "verified"} and sorry_count == 0
        declaration_matches = {
            name: (name in verified_names or name.split(".")[-1] in verified_names)
            for name in declarations
        }
        declarations_verified = bool(verified_names) and all(declaration_matches.values())
        verified = (not self.require_source_verification) or (build_passed and declarations_verified)
        blockers: list[str] = []
        if self.require_source_verification and not build_passed:
            blockers.append("Source project does not have a passing no-sorry Lean build report.")
        if self.require_source_verification and not verified_names:
            blockers.append("Source project does not list Lean-verified declarations in verified_declarations.json.")
        elif self.require_source_verification and not declarations_verified:
            missing = [name for name, matched in declaration_matches.items() if not matched]
            blockers.append(f"Declarations are absent from verified_declarations.json: {', '.join(missing)}")
        return {
            "verified": verified,
            "source_project": str(inferred_project or ""),
            "build_report": build_report,
            "verified_declaration_names": sorted(verified_names),
            "declaration_matches": declaration_matches,
            "blockers": blockers,
        }

    def _assert_harvest_safe(
        self,
        *,
        source_file: Path,
        source_project: Path | None,
        declarations: list[str],
        blocks: list[dict[str, Any]],
    ) -> dict[str, Any]:
        source_audit = self.audit_source_file(source_file)
        block_audits = {item["requested_name"]: item.get("source_audit", {}) for item in blocks if item.get("found")}
        blockers: list[str] = []
        if source_audit.get("trust_level") != "trusted":
            blockers.append("Source Lean file contains forbidden placeholders or trusted declarations.")
        for name, audit in block_audits.items():
            if audit.get("trust_level") != "trusted":
                blockers.append(f"Declaration `{name}` contains forbidden placeholders or trusted declarations.")
        verification = self._source_verification_report(
            source_file=source_file,
            source_project=source_project,
            declarations=declarations,
        )
        blockers.extend(verification["blockers"])
        report = {
            "source_audit": source_audit,
            "block_audits": block_audits,
            "source_verification": verification,
            "blockers": blockers,
        }
        if blockers:
            raise ValueError("AMRA library harvest rejected: " + "; ".join(blockers))
        return report

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
        source_file = source_file.expanduser().resolve()
        source_project = source_project.expanduser().resolve() if source_project is not None else None
        if not source_file.exists():
            raise FileNotFoundError(f"Source Lean file does not exist: {source_file}")
        normalized_module_name = self.normalise_module_name(module_name)
        self.ensure_library()
        module_report = self.add_module(
            module_name=normalized_module_name,
            imports=imports,
            title=title or normalized_module_name,
            domain=domain,
            status=status,
            tags=tags,
            description=description or f"Declarations promoted from {source_file}.",
        )
        module_path = Path(module_report["path"])
        blocks = self._declaration_blocks(source_file, declarations)
        missing = [item["requested_name"] for item in blocks if not item.get("found")]
        found_blocks = [item for item in blocks if item.get("found")]
        if missing:
            entry = self._upsert_module(
                {
                    **module_report["module"],
                    "source_file": str(source_file),
                    "source_project": str(source_project or ""),
                    "promoted_declarations": [],
                    "missing_declarations": missing,
                    "declarations": self._scan_module_declarations(module_path),
                    "status": status,
                }
            )
            return {
                "status": "partial",
                "module": entry,
                "path": str(module_path),
                "promoted_declarations": [],
                "missing_declarations": missing,
            }
        safety_report = self._assert_harvest_safe(
            source_file=source_file,
            source_project=source_project,
            declarations=[item["name"] for item in found_blocks],
            blocks=found_blocks,
        )
        promoted_names = [item["name"] for item in found_blocks]
        text = module_path.read_text(encoding="utf-8")
        insertion = "\n\n".join(item["block"] for item in found_blocks).strip()
        promoted_at = utc_now_iso()
        provenance = "\n".join(
            [
                "",
                "/-!",
                "## Promotion provenance",
                f"- Source file: `{source_file}`",
                f"- Source project: `{source_project or safety_report['source_verification'].get('source_project', '')}`",
                f"- Promoted at: `{promoted_at}`",
                f"- Source build report: `{safety_report['source_verification'].get('build_report', {}).get('path', '')}`",
                "-/",
                "",
                insertion,
                "",
            ]
        )
        end_marker = f"\nend {self.module_prefix}"
        if end_marker in text:
            text = text.replace(end_marker, provenance + end_marker, 1)
        else:
            text = text.rstrip() + "\n" + provenance
        write_text(module_path, text)
        module_declarations = self._scan_module_declarations(module_path)
        provenance_payload = {
            "source_file": str(source_file),
            "source_project": str(source_project or safety_report["source_verification"].get("source_project", "")),
            "promoted_at": promoted_at,
            "declarations": promoted_names,
            "source_verification": safety_report["source_verification"],
            "source_audit": safety_report["source_audit"],
        }
        entry = self._upsert_module(
            {
                **module_report["module"],
                "source_file": str(source_file),
                "source_project": provenance_payload["source_project"],
                "promoted_declarations": promoted_names,
                "missing_declarations": missing,
                "declarations": module_declarations,
                "status": status,
                "provenance": provenance_payload,
                "import_hints": self._import_hints(normalized_module_name, promoted_names),
            }
        )
        return {
            "status": "promoted",
            "module": entry,
            "path": str(module_path),
            "promoted_declarations": promoted_names,
            "missing_declarations": missing,
            "provenance": provenance_payload,
        }

    def promote_verified_file(
        self,
        *,
        source_file: Path,
        module_name: str,
        source_project: Path | None = None,
        title: str = "",
        domain: str = "",
        status: str = "verified",
        tags: list[str] | None = None,
        description: str = "",
        verification_basis: dict[str, Any] | None = None,
        build_timeout_sec: int | None = 600,
    ) -> dict[str, Any]:
        """Archive a complete verified Lean source file as a reusable AMRA module.

        This is used by Lean proof loops after the final target has passed the
        host verifier.  The whole file is preserved rather than extracting only
        the target declaration, because completed proofs often depend on local
        helper lemmas from the same file.
        """

        source_file = source_file.expanduser().resolve()
        source_project = source_project.expanduser().resolve() if source_project is not None else None
        if not source_file.exists():
            raise FileNotFoundError(f"Source Lean file does not exist: {source_file}")
        source_audit = self.audit_source_file(source_file)
        if source_audit.get("trust_level") != "trusted":
            raise ValueError("AMRA library file promotion rejected: source file contains forbidden placeholders.")

        normalized_module_name = self.normalise_module_name(module_name)
        self.ensure_library()
        module_path = self.formal_dir / _module_to_path(normalized_module_name, module_prefix=self.module_prefix)
        module_path.parent.mkdir(parents=True, exist_ok=True)
        root_module_path = self.formal_dir / f"{self.module_prefix}.lean"

        previous_module_text = module_path.read_text(encoding="utf-8") if module_path.exists() else None
        previous_root_text = root_module_path.read_text(encoding="utf-8") if root_module_path.exists() else None
        previous_registry = read_json(self.registry_path, default={})

        promoted_at = utc_now_iso()
        provenance_comment = "\n".join(
            [
                "/-",
                "## AMRA library promotion provenance",
                f"- Source file: `{source_file}`",
                f"- Source project: `{source_project or ''}`",
                f"- Promoted at: `{promoted_at}`",
                f"- Verification basis: `{(verification_basis or {}).get('basis', 'host_verified_final_target')}`",
                "-/",
                "",
            ]
        )
        source_text = source_file.read_text(encoding="utf-8", errors="ignore").lstrip()
        write_text(module_path, provenance_comment + source_text)
        declarations = self._scan_module_declarations(module_path)
        entry = self._upsert_module(
            {
                "module_name": normalized_module_name,
                "path": str(module_path.relative_to(self.library_root)),
                "title": title or normalized_module_name,
                "domain": domain,
                "status": status,
                "tags": [str(tag) for tag in tags or []],
                "description": description or f"Verified Lean file promoted from {source_file}.",
                "source_file": str(source_file),
                "source_project": str(source_project or ""),
                "declarations": declarations,
                "provenance": {
                    "source_file": str(source_file),
                    "source_project": str(source_project or ""),
                    "promoted_at": promoted_at,
                    "verification_basis": verification_basis or {"basis": "host_verified_final_target"},
                    "source_audit": source_audit,
                },
                "import_hints": self._import_hints(normalized_module_name, [item["name"] for item in declarations]),
            }
        )
        build_report = self.build(timeout_sec=build_timeout_sec, allow_cold_cache=True)
        if str(build_report.get("status") or "") not in {"passed", "verified"}:
            if previous_module_text is None:
                module_path.unlink(missing_ok=True)
            else:
                write_text(module_path, previous_module_text)
            if previous_root_text is not None:
                write_text(root_module_path, previous_root_text)
            if previous_registry:
                write_json(self.registry_path, previous_registry)
            else:
                self.registry_path.unlink(missing_ok=True)
            return {
                "status": "failed",
                "module": entry,
                "path": str(module_path),
                "source_file": str(source_file),
                "build_report": build_report,
                "rolled_back": True,
            }
        return {
            "status": "promoted",
            "module": entry,
            "path": str(module_path),
            "source_file": str(source_file),
            "declarations": declarations,
            "build_report": build_report,
            "rolled_back": False,
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

    def _resolve_declaration_source(self, project: Path, declaration: dict[str, Any]) -> Path | None:
        raw_candidates = [
            declaration.get("source_file"),
            declaration.get("file"),
            declaration.get("path"),
            declaration.get("absolute_path"),
            declaration.get("relative_path"),
        ]
        for raw in raw_candidates:
            value = str(raw or "").strip()
            if not value:
                continue
            path = Path(value)
            candidates = [path] if path.is_absolute() else [project / value, project / "formal" / value]
            for candidate in candidates:
                if candidate.exists():
                    return candidate
        name = str(declaration.get("lean_name") or declaration.get("name") or declaration.get("full_name") or "").split(".")[-1]
        if not name:
            return None
        formal_dir = project / "formal"
        for lean_file in sorted(formal_dir.rglob("*.lean")) if formal_dir.exists() else []:
            if ".lake" in lean_file.parts or lean_file.name == "lakefile.lean":
                continue
            if any(item.get("found") for item in self._declaration_blocks(lean_file, [name])):
                return lean_file
        return None

    def detect_harvest_candidates(self, *, project: Path, module: str) -> dict[str, Any]:
        project = project.expanduser().resolve()
        declarations_path = project / "verified_declarations.json"
        payload = read_json(declarations_path, {"declarations": []})
        declarations = payload.get("declarations", []) if isinstance(payload, dict) else []
        module_name = self.normalise_module_name(module)
        candidates: list[dict[str, Any]] = []
        rejected: list[dict[str, Any]] = []
        for item in declarations:
            if not isinstance(item, dict):
                continue
            status = str(item.get("status") or "lean_verified").strip().lower()
            name = str(item.get("name") or item.get("lean_name") or item.get("full_name") or "").strip()
            if not name:
                continue
            source_file = self._resolve_declaration_source(project, item)
            candidate = {
                "module": module_name,
                "declaration": name,
                "full_name": str(item.get("full_name") or name),
                "source": str(declarations_path),
                "source_file": str(source_file or ""),
                "status": "candidate",
                "import_hints": self._import_hints(module_name, [name.split(".")[-1]]),
            }
            if status and status not in VERIFIED_STATUSES:
                rejected.append({**candidate, "status": "rejected", "reason": f"declaration status is `{status}`"})
                continue
            if source_file is None:
                rejected.append({**candidate, "status": "rejected", "reason": "source Lean file could not be resolved"})
                continue
            blocks = self._declaration_blocks(source_file, [name])
            if not any(block.get("found") for block in blocks):
                rejected.append({**candidate, "status": "rejected", "reason": "declaration was not found in source Lean file"})
                continue
            try:
                safety = self._assert_harvest_safe(
                    source_file=source_file,
                    source_project=project,
                    declarations=[name.split(".")[-1]],
                    blocks=[block for block in blocks if block.get("found")],
                )
            except ValueError as exc:
                rejected.append({**candidate, "status": "rejected", "reason": str(exc)})
                continue
            candidates.append({**candidate, "safety": safety})
        return {
            "schema_version": "amra.library_harvest_candidates.v1",
            "generated_at": utc_now_iso(),
            "project": str(project),
            "module": module_name,
            "candidate_count": len(candidates),
            "rejected_count": len(rejected),
            "candidates": candidates,
            "rejected": rejected,
        }

    def harvest_verified_declarations(
        self,
        *,
        project: Path,
        module: str,
        imports: list[str] | None = None,
        title: str = "",
        domain: str = "",
        status: str = "candidate",
        tags: list[str] | None = None,
        description: str = "",
    ) -> dict[str, Any]:
        candidate_report = self.detect_harvest_candidates(project=project, module=module)
        promoted: list[dict[str, Any]] = []
        failed: list[dict[str, Any]] = []
        by_source: dict[str, list[str]] = {}
        for candidate in candidate_report["candidates"]:
            by_source.setdefault(candidate["source_file"], []).append(candidate["declaration"].split(".")[-1])
        for source_file, declarations in by_source.items():
            try:
                promoted.append(
                    self.promote_declarations(
                        source_file=Path(source_file),
                        source_project=project,
                        module_name=module,
                        declarations=declarations,
                        imports=imports,
                        title=title,
                        domain=domain,
                        status=status,
                        tags=tags,
                        description=description,
                    )
                )
            except Exception as exc:
                failed.append({"source_file": source_file, "declarations": declarations, "error": str(exc)})
        return {
            "schema_version": "amra.library_harvest_result.v1",
            "generated_at": utc_now_iso(),
            "project": str(project),
            "module": self.normalise_module_name(module),
            "candidate_report": candidate_report,
            "promoted": promoted,
            "failed": failed,
        }

    def inventory(self) -> dict[str, Any]:
        self.library_root.mkdir(parents=True, exist_ok=True)
        registry = self._registry()
        modules = []
        for module in registry.get("modules", []):
            path = self.library_root / str(module.get("path", ""))
            declarations = self._scan_module_declarations(path)
            modules.append(
                {
                    **module,
                    "exists": path.exists(),
                    "absolute_path": str(path),
                    "declarations": declarations,
                    "import_hints": module.get("import_hints") or self._import_hints(
                        str(module.get("module_name", "")),
                        [str(item.get("name", "")) for item in declarations if item.get("name")],
                    ),
                }
            )
        legacy_root = self.repo_root / LEGACY_LIBRARY_ROOT
        return {
            "schema_version": "amra.library_inventory.v1",
            "generated_at": utc_now_iso(),
            "library_root": str(self.library_root),
            "formal_dir": str(self.formal_dir),
            "registry_path": str(self.registry_path),
            "module_prefix": self.module_prefix,
            "module_count": len(modules),
            "modules": modules,
            "migration": {
                "canonical_root": AMRA_LIBRARY_ROOT,
                "canonical_module_prefix": AMRA_MODULE_PREFIX,
                "legacy_root": LEGACY_LIBRARY_ROOT,
                "legacy_module_prefix": LEGACY_MODULE_PREFIX,
                "legacy_root_exists": legacy_root.exists(),
            },
        }

    def build(self, *, timeout_sec: int | None = None, allow_cold_cache: bool = False) -> dict[str, Any]:
        self.ensure_library()
        executor = LeanExecutor(allow_cold_cache=allow_cold_cache)
        report = executor.build(self.library_root, timeout_sec=timeout_sec)
        payload = report.to_dict()
        write_json(self.library_root / "build_report.json", payload)
        return payload


class LegacyAraLibraryManager(AmraLibraryManager):
    """Compatibility manager for the deprecated ara_library/AraLibrary path."""

    def __init__(self, *, repo_root: Path, require_source_verification: bool = False) -> None:
        super().__init__(
            repo_root=repo_root,
            library_root_name=LEGACY_LIBRARY_ROOT,
            module_prefix=LEGACY_MODULE_PREFIX,
            legacy_module_prefix=AMRA_MODULE_PREFIX,
            display_name="ARA",
            require_source_verification=require_source_verification,
        )


__all__ = [
    "AMRA_LIBRARY_ROOT",
    "AMRA_MODULE_PREFIX",
    "LEGACY_LIBRARY_ROOT",
    "LEGACY_MODULE_PREFIX",
    "AmraLibraryManager",
    "LegacyAraLibraryManager",
]
