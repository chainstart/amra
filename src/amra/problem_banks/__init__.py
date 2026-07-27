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
    load_problem_bank_with_executor_metadata,
    normalize_erdos_problem_entry,
    refresh_erdos_problem_bank,
    resolve_bank_path,
    save_bank_registry,
    save_problem_bank,
)
from amra.problem_banks.unsolvedmath import (
    UnsolvedMathImporter,
    import_unsolvedmath_snapshot,
    parse_unsolvedmath_detail_page,
    parse_unsolvedmath_index_page,
    parse_unsolvedmath_sets_page,
)

__all__ = [
    "DEFAULT_BANK_PATH",
    "DEFAULT_BANK_REGISTRY_PATH",
    "get_problem",
    "import_erdos_open_problems",
    "import_erdos_problem_catalog",
    "load_bank_registry",
    "load_problem_bank",
    "load_problem_bank_with_executor_metadata",
    "normalize_erdos_problem_entry",
    "refresh_erdos_problem_bank",
    "resolve_bank_path",
    "save_bank_registry",
    "save_problem_bank",
    "UnsolvedMathImporter",
    "import_unsolvedmath_snapshot",
    "parse_unsolvedmath_detail_page",
    "parse_unsolvedmath_index_page",
    "parse_unsolvedmath_sets_page",
]
