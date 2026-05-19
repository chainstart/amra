"""Canonical AMRA problem bank interfaces."""

from __future__ import annotations

from amra.problem_banks.registry import (
    DEFAULT_BANK_PATH,
    DEFAULT_BANK_REGISTRY_PATH,
    get_problem,
    import_erdos_open_problems,
    import_erdos_problem_catalog,
    load_bank_registry,
    load_problem_bank,
    normalize_erdos_problem_entry,
    refresh_erdos_problem_bank,
    resolve_bank_path,
    save_bank_registry,
    save_problem_bank,
)

__all__ = [
    "DEFAULT_BANK_PATH",
    "DEFAULT_BANK_REGISTRY_PATH",
    "get_problem",
    "import_erdos_open_problems",
    "import_erdos_problem_catalog",
    "load_bank_registry",
    "load_problem_bank",
    "normalize_erdos_problem_entry",
    "refresh_erdos_problem_bank",
    "resolve_bank_path",
    "save_bank_registry",
    "save_problem_bank",
]
