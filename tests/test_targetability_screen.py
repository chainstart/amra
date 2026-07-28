from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import pytest

from amra.core.models import ProblemRecord
from amra.discovery.targetability_screen import (
    score_problem_targetability,
    screen_problem_banks_targetability,
)
from amra.problem_banks.registry import save_problem_bank


def _problem(
    problem_id: str,
    statement: str,
    *,
    title: str | None = None,
    domain: str = "graph_theory",
    formalized: str = "no",
    metadata: dict[str, object] | None = None,
) -> ProblemRecord:
    return ProblemRecord(
        problem_id=problem_id,
        title=title or problem_id,
        source="unit-test",
        statement=statement,
        domain=domain,
        formalized=formalized,
        references=["https://example.test/source"],
        metadata={
            "statement_quality": "detail_page",
            "current_status_verified": True,
            **(metadata or {}),
        },
    )


def _formal_problem(
    problem_id: str,
    declaration: str,
    *,
    source_file: str | None = None,
) -> ProblemRecord:
    metadata: dict[str, object] = {
        "statement_quality": "formal_lean4",
        "current_status_verified": True,
        "source_revision": "test-revision",
    }
    if source_file is not None:
        metadata["source_file"] = source_file
    return _problem(
        problem_id,
        f"```lean\n{declaration}\n```",
        domain="research_mathematics",
        formalized="lean4_statement",
        metadata=metadata,
    )


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _problem_fingerprint(problem: ProblemRecord) -> str:
    payload = json.dumps(
        {
            "problem_id": problem.problem_id,
            "title": problem.title,
            "statement": problem.statement,
            "metadata": problem.metadata,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def test_finite_universal_target_outranks_pure_existence() -> None:
    universal = _problem(
        "finite-universal",
        (
            "For every finite graph G with n vertices, every vertex of G has "
            "degree at most n - 1."
        ),
    )
    existence = _problem(
        "pure-existence",
        "Does there exist a finite graph with exactly seven vertices and eleven edges?",
    )

    universal_score = score_problem_targetability(universal)
    existence_score = score_problem_targetability(existence)

    assert universal_score["route"] == "counterexample"
    assert (
        universal_score["logical_profile"]["finite_witness_sufficient"] is True
    )
    assert universal_score["eligibility_status"] != "not_counterexample_target"
    assert existence_score["route"] == "witness_discovery"
    assert (
        existence_score["logical_profile"]["finite_witness_sufficient"] is False
    )
    assert existence_score["eligibility_status"] == "not_counterexample_target"
    assert (
        universal_score["score"]["targetability_score"]
        > existence_score["score"]["targetability_score"]
    )
    assert universal_score["priority_score"] > existence_score["priority_score"]


def test_direct_question_shape_overrides_stale_campaign_classification() -> None:
    existence = _problem(
        "stale-existence",
        "Is there a finite non-abelian group G with k(G) / |G| = 1/17?",
    )
    exact_value = _problem(
        "exact-value",
        "What is the exact value of the Ramsey number R(5,5)?",
    )
    stale_classification = {
        "classification": {"claim_kind": "equivalence_claim"}
    }

    existence_result = score_problem_targetability(
        existence,
        campaign_result=stale_classification,
    )
    exact_value_result = score_problem_targetability(
        exact_value,
        campaign_result={
            "classification": {"claim_kind": "universal_claim"}
        },
    )

    assert existence_result["route"] == "witness_discovery"
    assert existence_result["eligibility_status"] == "not_counterexample_target"
    assert exact_value_result["route"] == "subclaim_decomposition"
    assert exact_value_result["eligibility_status"] == "not_counterexample_target"


def test_multipart_record_requires_atomic_split() -> None:
    problem = _problem(
        "two-questions",
        (
            "For a finite group G define its type. "
            "a) Must a group of the same type have trivial radical? "
            "b) Must it be isomorphic to G?"
        ),
    )

    result = score_problem_targetability(problem)

    assert result["logical_profile"]["atomicity"] == "bundled"
    assert result["eligibility_status"] == "needs_atomic_split"


def test_natural_forall_exists_and_nested_existential_route_away() -> None:
    forall_exists = _problem(
        "forall-exists",
        (
            "Conjecture For all k there is an integer f(k) such that every "
            "digraph of minimum outdegree f(k) contains a target."
        ),
    )
    nested = _problem(
        "nested-existence",
        (
            "Definition Every graph has a cycle space. Problem Does there exist "
            "an infinite set of graphs such that there is no map between them?"
        ),
    )

    forall_result = score_problem_targetability(forall_exists)
    nested_result = score_problem_targetability(nested)

    assert forall_result["route"] == "subclaim_decomposition"
    assert forall_result["logical_profile"]["quantifier_structure"] == "mixed"
    assert nested_result["route"] == "witness_discovery"


@pytest.mark.parametrize(
    "statement",
    [
        "Must every infinite S-walk contain three collinear points?",
        "Do all but finitely many integers have property P?",
        "Does f(n) have asymptotic form f(n) \\sim n^(1/3)?",
        "Does every permutation of positive integers contain this pattern?",
        "Does the logarithmic density of A exist?",
    ],
)
def test_nonlocal_natural_claim_is_not_a_finite_counterexample_target(
    statement: str,
) -> None:
    result = score_problem_targetability(_problem("nonlocal", statement))

    assert result["logical_profile"]["finite_witness_sufficient"] is None
    assert result["eligibility_status"] == "modeling_candidate"


@pytest.mark.parametrize(
    "statement",
    [
        "Let f(n,k) be the minimum size. Determine f(n,k).",
        "For a finite game, find optimal strategies for both players.",
        "Under what conditions does this integer matrix have an integer inverse?",
        "Determine the best possible constant t.",
    ],
)
def test_embedded_answer_or_optimization_question_is_not_counterexample(
    statement: str,
) -> None:
    result = score_problem_targetability(_problem("answer-query", statement))

    assert result["route"] == "subclaim_decomposition"
    assert result["eligibility_status"] == "not_counterexample_target"


@pytest.mark.parametrize(
    (
        "declaration",
        "expected_route",
        "expected_claim_kind",
        "expected_structure",
        "finite_witness",
    ),
    [
        (
            "theorem no_bad : ¬ ∃ n : Fin 10, n.val = 9 := by sorry",
            "counterexample",
            "universal_claim",
            "negative_existence",
            True,
        ),
        (
            "theorem bounded : ∀ n : Fin 10, n.val < 10 := by sorry",
            "counterexample",
            "universal_claim",
            "universal",
            True,
        ),
        (
            "theorem some_good : ∃ n : Fin 10, n.val = 9 := by sorry",
            "witness_discovery",
            "existence_claim",
            "existential",
            False,
        ),
        (
            "theorem unknown_answer : answer(sorry) := by sorry",
            "answer_discovery",
            "answer_query",
            "answer_placeholder",
            False,
        ),
        (
            "theorem eventually_good : ∀ᶠ n in atTop, P n := by sorry",
            "formal_modeling",
            "global_or_asymptotic_claim",
            "global_semantics",
            False,
        ),
        (
            "theorem infinitely_many : Infinite {n : ℕ | Nat.Prime n}",
            "formal_modeling",
            "global_or_asymptotic_claim",
            "global_semantics",
            False,
        ),
        (
            "theorem realizable : Nonempty (Model α)",
            "witness_discovery",
            "existence_claim",
            "hidden_existential_predicate",
            False,
        ),
        (
            "def successor (n : ℕ) : ℕ := n + 1",
            "not_counterexample",
            "formal_definition",
            "non_prop_definition",
            False,
        ),
    ],
)
def test_lean_route_is_conservative_about_finite_refutation(
    declaration: str,
    expected_route: str,
    expected_claim_kind: str,
    expected_structure: str,
    finite_witness: bool,
) -> None:
    result = score_problem_targetability(
        _formal_problem("formal-route", declaration)
    )
    profile = result["logical_profile"]

    assert result["route"] == expected_route
    assert result["claim_kind"] == expected_claim_kind
    assert profile["quantifier_structure"] == expected_structure
    assert profile["finite_witness_sufficient"] is finite_witness


def test_lean_let_is_not_mistaken_for_declaration_proof_and_function_is_risky() -> None:
    let_result = score_problem_targetability(
        _formal_problem(
            "let-relation",
            "theorem let_relation (n : ℕ) : let x := n; x ≤ n",
        )
    )
    function_result = score_problem_targetability(
        _formal_problem(
            "function-relation",
            "theorem function_relation (a : ℕ → ℕ) : a 0 ≤ a 1",
        )
    )

    assert let_result["route"] == "counterexample"
    assert let_result["logical_profile"]["finite_witness_sufficient"] is True
    assert function_result["route"] == "counterexample"
    assert (
        function_result["logical_profile"]["finite_witness_sufficient"] is None
    )
    assert function_result["eligibility_status"] == "modeling_candidate"


def test_multi_bank_inventory_blocks_unusable_and_duplicate_records(
    tmp_path: Path,
) -> None:
    first_bank = tmp_path / "first.yaml"
    second_bank = tmp_path / "second.yaml"
    campaign_dir = tmp_path / "campaign"
    output_dir = tmp_path / "screen"
    campaign_dir.mkdir()
    save_problem_bank(
        [
            _problem(
                "clean",
                "For every finite graph G, every edge of G has two endpoints.",
            ),
            _problem(
                "dirty",
                "For every graph G, a disputed conclusion holds.",
                metadata={"source_consistency_flags": ["statement_conflict"]},
            ),
            _problem(
                "placeholder",
                "Detailed statement must be recovered from the source.",
                metadata={"statement_quality": "placeholder"},
            ),
            _problem(
                "duplicate-metadata",
                "For every graph G, another conclusion holds.",
                metadata={"duplicate_of": "clean"},
            ),
            _problem(
                "repeated-id",
                "For every finite graph G, G has at least zero vertices.",
            ),
        ],
        first_bank,
    )
    save_problem_bank(
        [
            _problem(
                "repeated-id",
                "For every finite graph G, G has at least zero vertices.",
            )
        ],
        second_bank,
    )

    summary = screen_problem_banks_targetability(
        bank_paths=[first_bank, second_bank],
        campaign_dir=campaign_dir,
        output_dir=output_dir,
        shortlist_size=5,
    )
    inventory = _read_jsonl(output_dir / "targetability-inventory.jsonl")
    by_id: dict[str, list[dict[str, object]]] = {}
    for row in inventory:
        by_id.setdefault(str(row["problem_id"]), []).append(row)

    assert by_id["dirty"][0]["admission_status"] == "needs_statement_recovery"
    assert by_id["placeholder"][0]["admission_status"] == (
        "needs_statement_recovery"
    )
    assert by_id["duplicate-metadata"][0]["admission_status"] == (
        "excluded_duplicate"
    )
    assert [row["admission_status"] for row in by_id["repeated-id"]] == [
        "included",
        "excluded_duplicate_record_id",
    ]
    assert summary["input_record_count"] == 6
    assert summary["ranked_target_count"] == 2
    assert {
        row["problem_id"]
        for row in _read_jsonl(output_dir / "targetability-ranking.jsonl")
    } == {"clean", "repeated-id"}


def test_known_disproof_is_excluded_before_ranking(tmp_path: Path) -> None:
    bank_path = tmp_path / "bank.yaml"
    campaign_dir = tmp_path / "campaign"
    output_dir = tmp_path / "screen"
    campaign_dir.mkdir()
    save_problem_bank(
        [
            _problem(
                "unsolvedmath-opg-59994",
                (
                    "Every (2t+1)-regular class 1 graph has circular flow "
                    "number at most 2 + 2/t."
                ),
            )
        ],
        bank_path,
    )

    summary = screen_problem_banks_targetability(
        bank_paths=[bank_path],
        campaign_dir=campaign_dir,
        output_dir=output_dir,
    )
    inventory = _read_jsonl(output_dir / "targetability-inventory.jsonl")

    assert inventory[0]["admission_status"] == "excluded_closed_or_solved"
    assert "Mattiolo-Steffen" in inventory[0]["reasons"][0]
    assert summary["ranked_target_count"] == 0
    assert _read_jsonl(output_dir / "targetability-ranking.jsonl") == []


def test_known_jackson_counterexample_is_excluded_before_ranking(
    tmp_path: Path,
) -> None:
    bank_path = tmp_path / "bank.yaml"
    campaign_dir = tmp_path / "campaign"
    output_dir = tmp_path / "screen"
    campaign_dir.mkdir()
    save_problem_bank(
        [
            _problem(
                "unsolvedmath-opg-47028",
                (
                    "Every oriented graph with minimum indegree and "
                    "outdegree d has a Hamilton cycle."
                ),
            )
        ],
        bank_path,
    )

    summary = screen_problem_banks_targetability(
        bank_paths=[bank_path],
        campaign_dir=campaign_dir,
        output_dir=output_dir,
    )
    inventory = _read_jsonl(output_dir / "targetability-inventory.jsonl")

    assert inventory[0]["admission_status"] == "excluded_closed_or_solved"
    assert "Guninski" in inventory[0]["reasons"][0]
    assert summary["ranked_target_count"] == 0


def test_known_source_scope_mismatch_requires_statement_recovery(
    tmp_path: Path,
) -> None:
    bank_path = tmp_path / "bank.yaml"
    campaign_dir = tmp_path / "campaign"
    output_dir = tmp_path / "screen"
    campaign_dir.mkdir()
    save_problem_bank(
        [
            _problem(
                "erdos-825-weird",
                "Determine whether every weird number has abundance index C=3.",
                domain="number_theory",
            )
        ],
        bank_path,
    )

    summary = screen_problem_banks_targetability(
        bank_paths=[bank_path],
        campaign_dir=campaign_dir,
        output_dir=output_dir,
    )
    inventory = _read_jsonl(output_dir / "targetability-inventory.jsonl")

    assert inventory[0]["admission_status"] == "needs_statement_recovery"
    assert "absolute-constant question is proved" in inventory[0]["reasons"][0]
    assert summary["ranked_target_count"] == 0


def test_prior_null_saturation_requires_matching_statement_hash() -> None:
    problem = _problem(
        "searched",
        "For every finite graph G, the maximum degree of G is at most 100.",
    )
    statement_hash = hashlib.sha256(problem.statement.encode("utf-8")).hexdigest()
    matching_history = {
        "problem_id": problem.problem_id,
        "statement_hash": statement_hash,
        "checked_cases": 10**12,
        "attempt_count": 10,
        "model_audit_status": "approved",
        "claim_scope": "full_claim",
    }
    stale_history = {
        **matching_history,
        "statement_hash": hashlib.sha256(b"an older statement").hexdigest(),
    }

    baseline = score_problem_targetability(problem)
    saturated = score_problem_targetability(
        problem,
        batch_result=matching_history,
    )
    stale = score_problem_targetability(problem, batch_result=stale_history)

    assert baseline["score"]["penalties"]["prior_null_saturation"] == 0
    assert saturated["score"]["penalties"]["prior_null_saturation"] == 15
    assert stale["score"]["penalties"]["prior_null_saturation"] == 0
    assert saturated["eligibility_status"] == "new_strategy_only"
    assert (
        saturated["score"]["targetability_score"]
        < saturated["score"]["gross"]
    )


def test_campaign_execution_must_map_to_the_current_problem_negation() -> None:
    problem = _problem(
        "campaign-mapping",
        "For every finite graph G, the maximum degree is at most 100.",
    )
    fingerprint = _problem_fingerprint(problem)
    unrelated_scan = {
        "problem_fingerprint": fingerprint,
        "search_execution": {
            "outcome": "domain_scan_not_logically_mapped_to_negation",
            "executions": [{"executor_id": "unrelated"}],
        },
    }
    mapped_scan = {
        "problem_fingerprint": fingerprint,
        "search_execution": {
            "outcome": "no_counterexample_within_bound",
            "deterministic": True,
            "replayable": True,
            "executor_id": "exact.graph.v1",
            "checked_cases": 100_000,
            "candidate": None,
        },
    }

    baseline = score_problem_targetability(problem)
    unrelated = score_problem_targetability(
        problem, campaign_result=unrelated_scan
    )
    mapped = score_problem_targetability(problem, campaign_result=mapped_scan)

    assert unrelated["component_scores"] == baseline["component_scores"]
    assert unrelated["score"]["penalties"] == baseline["score"]["penalties"]
    assert mapped["score"]["penalties"]["prior_null_saturation"] > 0
    assert mapped["eligibility_status"] == "new_strategy_only"


def test_screen_writes_complete_outputs_and_limits_each_cluster(
    tmp_path: Path,
) -> None:
    first_bank = tmp_path / "formal.yaml"
    second_bank = tmp_path / "natural.yaml"
    campaign_dir = tmp_path / "campaign"
    output_dir = tmp_path / "screen"
    campaign_dir.mkdir()
    save_problem_bank(
        [
            _formal_problem(
                "formal-erdos-123-a",
                "theorem erdos_variant : ∀ n : Fin 10, n.val < 10 := by sorry",
                source_file="FormalConjectures/ErdosProblems/123.lean",
            )
        ],
        first_bank,
    )
    save_problem_bank(
        [
            _problem(
                "unsolvedmath-ep-123-variant",
                "For every finite graph G, every vertex has finite degree.",
            ),
            _problem(
                "independent-cluster",
                "For every finite tree T, the number of edges is at most its number of vertices.",
            ),
        ],
        second_bank,
    )

    summary = screen_problem_banks_targetability(
        bank_paths=[first_bank, second_bank],
        campaign_dir=campaign_dir,
        output_dir=output_dir,
        shortlist_size=3,
        max_per_cluster=1,
    )

    expected_files = {
        "targetability-inventory.jsonl",
        "targetability-ranking.jsonl",
        "targetability-ranking.csv",
        "targetability-shortlist.json",
        "targetability-summary.json",
        "targetability-manifest.json",
        "TARGETABILITY_REPORT.md",
    }
    assert {path.name for path in output_dir.iterdir()} == expected_files

    inventory = _read_jsonl(output_dir / "targetability-inventory.jsonl")
    ranking = _read_jsonl(output_dir / "targetability-ranking.jsonl")
    shortlist_payload = json.loads(
        (output_dir / "targetability-shortlist.json").read_text(encoding="utf-8")
    )
    written_summary = json.loads(
        (output_dir / "targetability-summary.json").read_text(encoding="utf-8")
    )
    manifest = json.loads(
        (output_dir / "targetability-manifest.json").read_text(encoding="utf-8")
    )
    report = (output_dir / "TARGETABILITY_REPORT.md").read_text(encoding="utf-8")
    with (output_dir / "targetability-ranking.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        csv_rows = list(csv.DictReader(handle))

    shortlist = shortlist_payload["shortlist"]
    cluster_counts = Counter(row["canonical_group_id"] for row in shortlist)
    assert len(inventory) == 3
    assert len(ranking) == 3
    assert len(csv_rows) == 3
    assert summary == written_summary
    assert summary["canonical_group_count"] == 2
    assert summary["shortlist_size"] == 2
    assert cluster_counts["erdos:123"] == 1
    assert max(cluster_counts.values()) == 1
    assert manifest["rules"]["max_per_cluster"] == 1
    assert all(
        entry["sha256"]
        for entry in manifest["input_files"]
        if entry["path"] in {str(first_bank.resolve()), str(second_bank.resolve())}
    )
    assert "# 全题库反例可攻关性筛选" in report
