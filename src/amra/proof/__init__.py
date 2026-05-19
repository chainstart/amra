"""Canonical AMRA proof state and proof-run support."""

from __future__ import annotations

from amra.proof.loops import (
    ProofLoopRegistry,
    ProofRunRequest,
    ProofRunResult,
    ProofRunnerContract,
    default_proof_loop_registry,
    normalize_proof_status,
    run_proof_loop,
    select_proof_loop_route,
)
from amra.proof.state import ProofArtifactTracker

__all__ = [
    "ProofArtifactTracker",
    "ProofLoopRegistry",
    "ProofRunRequest",
    "ProofRunResult",
    "ProofRunnerContract",
    "default_proof_loop_registry",
    "normalize_proof_status",
    "run_proof_loop",
    "select_proof_loop_route",
]
