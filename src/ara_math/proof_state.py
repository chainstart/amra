"""Deprecated compatibility shim for canonical AMRA proof state."""

from __future__ import annotations

from amra.proof.state import ProofArtifactTracker
from amra.portfolio_memory import (
    consolidate_memory,
    consolidate_project_memory,
    consolidate_portfolio_memory,
    failed_route_prompt_block,
    render_failed_route_prompt_block,
    render_failed_route_memory,
    retrieve_failed_route_memory,
    retrieve_failed_routes,
)

__all__ = [
    "ProofArtifactTracker",
    "consolidate_memory",
    "consolidate_project_memory",
    "consolidate_portfolio_memory",
    "retrieve_failed_routes",
    "retrieve_failed_route_memory",
    "render_failed_route_prompt_block",
    "render_failed_route_memory",
    "failed_route_prompt_block",
]
