"""Bounded deterministic domain search executors for AMRA."""

from __future__ import annotations

from amra.domain_executors.base import (
    EXECUTOR_INTERFACE_SCHEMA_VERSION,
    RESULT_SCHEMA_VERSION,
    DomainSearchRequest,
    DomainSearchResult,
    ExecutorMetadata,
    SearchBudget,
)
from amra.domain_executors.geometry import TriangleDissectionCertificateExecutor
from amra.domain_executors.number_theory import (
    BoundedAmicableExecutor,
    BoundedCarmichaelExecutor,
    BoundedUnitaryPerfectExecutor,
)
from amra.domain_executors.registry import (
    DOMAIN_EXECUTOR_METADATA_KEY,
    attach_executor_metadata,
    attach_executor_metadata_to_bank,
    available_executor_metadata,
    available_executors,
    compact_executor_signal,
    executor_metadata_for_problem,
    get_executor,
    infer_executor_ids_for_problem,
    run_domain_executor,
    select_executors_for_problem,
)


__all__ = [
    "DOMAIN_EXECUTOR_METADATA_KEY",
    "EXECUTOR_INTERFACE_SCHEMA_VERSION",
    "RESULT_SCHEMA_VERSION",
    "BoundedAmicableExecutor",
    "BoundedCarmichaelExecutor",
    "BoundedUnitaryPerfectExecutor",
    "DomainSearchRequest",
    "DomainSearchResult",
    "ExecutorMetadata",
    "SearchBudget",
    "TriangleDissectionCertificateExecutor",
    "attach_executor_metadata",
    "attach_executor_metadata_to_bank",
    "available_executor_metadata",
    "available_executors",
    "compact_executor_signal",
    "executor_metadata_for_problem",
    "get_executor",
    "infer_executor_ids_for_problem",
    "run_domain_executor",
    "select_executors_for_problem",
]
