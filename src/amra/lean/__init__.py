"""Canonical AMRA Lean interfaces."""

from __future__ import annotations

from typing import Any

from amra.lean.audit import audit_lean_source_file, audit_lean_source_text, strip_lean_comments
from amra.lean.contract import (
    compare_lean_declaration_headers,
    extract_lean_declaration_header,
    normalize_lean_declaration_header,
    render_lean_header_with_sorry,
    trim_lean_proof_from_header,
)

__all__ = [
    "FormalizationPreparer",
    "LeanExecutor",
    "LeanFormalizerRunner",
    "audit_lean_source_file",
    "audit_lean_source_text",
    "compare_lean_declaration_headers",
    "collect_proof_lab_context_paths",
    "extract_lean_declaration_header",
    "normalize_lean_declaration_header",
    "render_lean_header_with_sorry",
    "strip_lean_comments",
    "trim_lean_proof_from_header",
]


def __getattr__(name: str) -> Any:
    if name == "LeanExecutor":
        from amra.lean.executor import LeanExecutor

        return LeanExecutor
    if name == "FormalizationPreparer":
        from amra.lean.formalization import FormalizationPreparer

        return FormalizationPreparer
    if name in {"LeanFormalizerRunner", "collect_proof_lab_context_paths"}:
        from amra.lean.formalizer import LeanFormalizerRunner, collect_proof_lab_context_paths

        return {
            "LeanFormalizerRunner": LeanFormalizerRunner,
            "collect_proof_lab_context_paths": collect_proof_lab_context_paths,
        }[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
