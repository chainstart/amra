"""Canonical AMRA proof runners, state, and proof-run support."""

from __future__ import annotations

from amra.proof.attack import MathAttackRunner
from amra.proof.campaign_loop import (
    CampaignLoopRunner,
    extract_first_theorem_name,
    extract_formalization_target_from_run,
)
from amra.proof.closure import ClosureProverRunner
from amra.proof.goal_campaign import (
    GoalDrivenCampaignRunner,
    normalize_goal_manifest,
    write_goal_manifest_template,
)
from amra.proof.lab import (
    AIProofLabRunner,
    cluster_route_attempts,
    parse_labeled_fields,
    route_signature,
)
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
from amra.proof.planning import MathPlanner
from amra.proof.proof_system import ProofSearchAgendaPlanner, ProofSystemPlanner
from amra.proof.retrieval import PremiseRetriever
from amra.proof.search import ProofSearchRunner
from amra.proof.state import ProofArtifactTracker
from amra.proof.stability import (
    FAILURE_TAXONOMY,
    PROOF_STABILITY_CASE_SCHEMA_VERSION,
    PROOF_STABILITY_REPORT_SCHEMA_VERSION,
    PROOF_STABILITY_RESUME_SCHEMA_VERSION,
    PROOF_STABILITY_SUITE_SCHEMA_VERSION,
    load_proof_stability_suite,
    run_proof_stability_benchmark,
)

__all__ = [
    "AIProofLabRunner",
    "CampaignLoopRunner",
    "ClosureProverRunner",
    "GoalDrivenCampaignRunner",
    "MathAttackRunner",
    "MathPlanner",
    "PremiseRetriever",
    "ProofSearchAgendaPlanner",
    "ProofSearchRunner",
    "ProofSystemPlanner",
    "ProofArtifactTracker",
    "FAILURE_TAXONOMY",
    "PROOF_STABILITY_CASE_SCHEMA_VERSION",
    "PROOF_STABILITY_REPORT_SCHEMA_VERSION",
    "PROOF_STABILITY_RESUME_SCHEMA_VERSION",
    "PROOF_STABILITY_SUITE_SCHEMA_VERSION",
    "ProofLoopRegistry",
    "ProofRunRequest",
    "ProofRunResult",
    "ProofRunnerContract",
    "default_proof_loop_registry",
    "normalize_proof_status",
    "cluster_route_attempts",
    "extract_first_theorem_name",
    "extract_formalization_target_from_run",
    "normalize_goal_manifest",
    "parse_labeled_fields",
    "route_signature",
    "load_proof_stability_suite",
    "run_proof_loop",
    "run_proof_stability_benchmark",
    "select_proof_loop_route",
    "write_goal_manifest_template",
]
