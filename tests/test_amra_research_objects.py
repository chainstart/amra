from __future__ import annotations

import pytest

from amra.research import (
    ConjectureRecord,
    EvidenceConfidence,
    EvidenceKind,
    EvidenceRecord,
    ExperimentRecord,
    MLTheoryClaimRecord,
    ResearchConfidence,
    ResearchObjectRecord,
    ResearchObjectStatus,
    ResearchObjectType,
)


def test_research_object_records_round_trip_typed_payloads() -> None:
    conjecture = ConjectureRecord(
        object_id="conjecture-001",
        title="Bounded search suggests an invariant",
        status=ResearchObjectStatus.EMPIRICALLY_SUPPORTED,
        statement="For all tested n <= 1000, f(n) is even.",
        domain="number_theory",
        tags=["conjecture_mining", 7],
        confidence=ResearchConfidence.LOW,
        known_cases=["n <= 1000"],
        counterexample_search=["search-001"],
        novelty_report={"status": "unknown"},
    )

    payload = conjecture.to_dict()
    restored = ResearchObjectRecord.from_dict(payload)

    assert isinstance(restored, ConjectureRecord)
    assert restored.object_type == ResearchObjectType.CONJECTURE
    assert restored.to_dict() == payload
    assert restored.tags == ["conjecture_mining", "7"]


def test_experiment_and_ml_theory_records_keep_reproducibility_boundaries() -> None:
    experiment = ExperimentRecord(
        object_id="experiment-001",
        title="Search for small counterexamples",
        status="testing",
        question="Does the candidate invariant survive small exhaustive search?",
        method="bounded exhaustive search",
        inputs=["fixture.json"],
        parameters={"limit": 1000},
        seed=13,
        budget={"seconds": 2},
        environment={"python": "3.12"},
        command="python search.py --limit 1000",
        outputs=["counterexamples.json"],
        result_summary="No counterexample found within budget.",
    )
    ml_claim = MLTheoryClaimRecord(
        object_id="ml-claim-001",
        title="Toy optimizer observation",
        theoretical_statement="",
        empirical_support=[experiment.object_id],
        known_gaps=["No theorem-grade proof."],
    )

    assert ExperimentRecord.from_dict(experiment.to_dict()).to_dict() == experiment.to_dict()
    assert MLTheoryClaimRecord.from_dict(ml_claim.to_dict()).promotion_target == "conjecture"
    assert ml_claim.to_dict()["object_type"] == "ml_theory_claim"


def test_non_proof_evidence_cannot_claim_theorem_grade_confidence() -> None:
    with pytest.raises(ValueError, match="cannot be marked theorem_grade"):
        EvidenceRecord(
            evidence_id="empirical-001",
            kind=EvidenceKind.EMPIRICAL_EVIDENCE,
            target_object_id="conjecture-001",
            confidence=EvidenceConfidence.THEOREM_GRADE,
        )

    lean_evidence = EvidenceRecord(
        evidence_id="lean-001",
        kind=EvidenceKind.LEAN_VERIFIED,
        target_object_id="claim-001",
        confidence=EvidenceConfidence.THEOREM_GRADE,
    )

    assert lean_evidence.theorem_grade is True
    assert EvidenceRecord.from_dict(lean_evidence.to_dict()).theorem_grade is True
