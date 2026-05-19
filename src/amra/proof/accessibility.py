from __future__ import annotations

from pathlib import Path
from typing import Any

from amra.core.workspace import utc_now_iso


def _infer_module_name(path: Path) -> str:
    if "lean" in path.parts:
        index = path.parts.index("lean")
        return ".".join(Path(*path.parts[index + 1 :]).with_suffix("").parts)
    for index, part in enumerate(path.parts):
        if part and part[:1].isupper():
            return ".".join(Path(*path.parts[index:]).with_suffix("").parts)
    return path.stem


def _parse_imports(path: Path) -> list[str]:
    imports: list[str] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return imports
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("import "):
            continue
        imports.extend(item.strip() for item in stripped[len("import ") :].split() if item.strip())
    return imports


class AccessiblePremiseGraphPlanner:
    """Build a static accessibility report for locally available Lean premises."""

    def _module_access_reason(
        self,
        module_name: str,
        *,
        project_modules: set[str],
        imported_modules: set[str],
        ready_imports: set[str],
        compiled_modules: set[str],
        compiled_suffixes: dict[str, list[str]],
        staged_modules: dict[str, Any],
    ) -> tuple[bool, str, str]:
        if module_name in project_modules:
            return True, "project_module", module_name
        if module_name in imported_modules:
            return True, "project_import", module_name
        if module_name in ready_imports:
            return True, "ready_import_hint", module_name
        if module_name in compiled_modules:
            return True, "compiled_module", module_name
        if module_name in staged_modules:
            module_payload = staged_modules[module_name] or {}
            stage_kind = str(module_payload.get("kind", "copy")).strip() or "copy"
            return True, f"staged_{stage_kind}", module_name

        for imported in sorted(imported_modules.union(ready_imports)):
            if module_name.startswith(f"{imported}."):
                return True, "import_prefix", imported

        suffix_matches = compiled_suffixes.get(module_name, [])
        if len(suffix_matches) == 1:
            return True, "compiled_suffix_match", suffix_matches[0]
        if len(suffix_matches) > 1:
            return False, "ambiguous_compiled_suffix", ",".join(suffix_matches)
        return False, "not_accessible", ""

    def build_report(
        self,
        *,
        project_dir: Path,
        theorem_hints: list[dict[str, Any]],
        porting_candidates: list[dict[str, Any]],
        accessible_support: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        formal_dir = project_dir / "formal"
        project_files = sorted(formal_dir.rglob("*.lean")) if formal_dir.exists() else []
        modules: list[dict[str, Any]] = []
        discovered_imports: set[str] = set()
        for file_path in project_files:
            module_name = _infer_module_name(file_path)
            imports = _parse_imports(file_path)
            discovered_imports.update(imports)
            modules.append(
                {
                    "module": module_name,
                    "path": str(file_path),
                    "imports": imports,
                }
            )

        support = accessible_support or {}
        project_modules = {
            str(item).strip()
            for item in support.get("project_modules", [])
            if str(item).strip()
        } or {item["module"] for item in modules}
        imported_modules = {
            str(item).strip()
            for item in support.get("project_imports", [])
            if str(item).strip()
        } or discovered_imports
        compiled_modules = {
            str(item).strip()
            for item in support.get("compiled_modules", [])
            if str(item).strip()
        }
        compiled_suffixes = {
            str(key).strip(): [str(item).strip() for item in value if str(item).strip()]
            for key, value in (support.get("compiled_suffixes", {}) or {}).items()
            if str(key).strip()
        }
        stage_plan = support.get("stage_plan") or {}
        staged_modules = dict(stage_plan.get("modules", {}) or {})
        ready_imports = {
            str(item.get("import_hint", "")).strip()
            for item in porting_candidates
            if item.get("import_ready") and str(item.get("import_hint", "")).strip()
        }
        accessible_premises: list[dict[str, Any]] = []
        inaccessible_premises: list[dict[str, Any]] = []
        for item in theorem_hints:
            module_name = _infer_module_name(Path(str(item.get("path", ""))))
            accessible, access_reason, access_target = self._module_access_reason(
                module_name,
                project_modules=project_modules,
                imported_modules=imported_modules,
                ready_imports=ready_imports,
                compiled_modules=compiled_modules,
                compiled_suffixes=compiled_suffixes,
                staged_modules=staged_modules,
            )
            premise = {
                "name": item.get("name", ""),
                "statement": item.get("statement", ""),
                "path": item.get("path", ""),
                "line": item.get("line"),
                "module": module_name,
                "access_reason": access_reason,
                "access_target": access_target,
            }
            if str(item.get("path", "")).startswith(str(formal_dir)) or accessible:
                accessible_premises.append(premise)
            else:
                inaccessible_premises.append(premise)

        edges: list[dict[str, str]] = []
        for module in modules:
            for imported in module.get("imports", []):
                edges.append({"from": module["module"], "to": imported})

        import_candidates: list[dict[str, Any]] = []
        for item in porting_candidates:
            import_hint = str(item.get("import_hint", "")).strip()
            staged = import_hint in staged_modules if import_hint else False
            compiled_suffix_matches = compiled_suffixes.get(import_hint, []) if import_hint else []
            import_candidates.append(
                {
                    "name": item.get("name", ""),
                    "import_hint": import_hint,
                    "source_path": item.get("source_path", ""),
                    "import_ready": bool(item.get("import_ready")),
                    "already_imported": bool(import_hint and import_hint in imported_modules),
                    "compiled": bool(import_hint and import_hint in compiled_modules),
                    "staged": staged,
                    "compiled_suffix_matches": compiled_suffix_matches,
                }
            )

        return {
            "generated_at": utc_now_iso(),
            "project_module_count": len(modules),
            "imported_module_count": len(imported_modules),
            "project_modules": modules,
            "edges": edges,
            "accessible_premises": accessible_premises[:12],
            "inaccessible_premises": inaccessible_premises[:12],
            "import_candidates": import_candidates[:12],
            "support_summary": {
                "project_import_count": len(imported_modules),
                "compiled_module_count": len(compiled_modules),
                "staged_module_count": len(staged_modules),
                "stage_plan_status": str(stage_plan.get("status", "")).strip(),
                "unresolved_import_count": len(stage_plan.get("unresolved_imports", [])),
                "blocked_source_count": len(stage_plan.get("blocked_sources", [])),
            },
            "project_imports": sorted(imported_modules),
            "compiled_modules": sorted(compiled_modules)[:80],
            "staged_modules": sorted(staged_modules)[:80],
            "stage_plan_status": str(stage_plan.get("status", "")).strip(),
        }
