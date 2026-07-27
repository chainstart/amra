from __future__ import annotations

import copy
from pathlib import Path
import time

import pytest
import yaml

from amra.discovery import second_batch_finite as finite
from amra.discovery.first_batch_campaign import FIRST_BATCH_PROBLEM_IDS
from amra.discovery.second_batch_arithmetic import SECOND_BATCH_ARITHMETIC_SPECS
from amra.discovery.second_batch_campaign import (
    SECOND_BATCH_EXPECTED_TOTAL,
    SecondBatchConfigurationError,
    SecondBatchExecutorFamily,
    SecondBatchRegistry,
    load_default_second_batch_registry,
    validate_second_batch_registry,
)
from amra.discovery.second_batch_finite import (
    EXECUTOR_ID,
    SECOND_BATCH_FINITE_SPECS,
    run_second_batch_finite_search,
    verify_second_batch_finite_candidate,
)
from amra.discovery.second_batch_graphs import SECOND_BATCH_GRAPH_SPECS


BANK_PATH = Path("data/banks/unsolvedmath_open_non_erdos.yaml")
SOURCE_BANK = {
    row["problem_id"]: row
    for row in yaml.safe_load(BANK_PATH.read_text(encoding="utf-8"))
}
ALLOWED_SCOPES = {
    "full_claim",
    "explicit_subclaim",
    "restricted_family",
    "witness_search",
}
CATALOGUE_SHARDED_IDS = {
    "unsolvedmath-kou-21.26",
    "unsolvedmath-kou-21.99",
    "unsolvedmath-opg-48264",
}
CATALOGUE_STRATEGIES = [
    "deep-catalogue-0",
    "deep-catalogue-1",
    "deep-catalogue-2",
]


def test_finite_registry_has_exactly_34_new_problem_ids() -> None:
    finite_ids = [str(spec["problem_id"]) for spec in SECOND_BATCH_FINITE_SPECS]
    excluded = (
        set(FIRST_BATCH_PROBLEM_IDS)
        | {str(spec["problem_id"]) for spec in SECOND_BATCH_GRAPH_SPECS}
        | {str(spec["problem_id"]) for spec in SECOND_BATCH_ARITHMETIC_SPECS}
    )

    assert len(finite_ids) == 34
    assert len(set(finite_ids)) == 34
    assert not set(finite_ids) & excluded
    assert "unsolvedmath-opg-432" not in finite_ids
    assert (
        "unsolvedmath-comb-003-collision-the-union-closed-sets-conjecture-3866e1eb"
        not in finite_ids
    )
    assert not {
        "unsolvedmath-nt-008",
        "unsolvedmath-opg-655",
        "unsolvedmath-opg-2359",
        "unsolvedmath-opg-46432",
        "unsolvedmath-opg-37196",
        "unsolvedmath-alg-010",
    } & set(finite_ids)
    assert {
        "unsolvedmath-comb-003",
        "unsolvedmath-opg-369",
        "unsolvedmath-opg-600",
        "unsolvedmath-kou-21.26",
        "unsolvedmath-opg-382",
    } <= set(finite_ids)


def test_default_registry_is_exactly_100_across_three_real_families() -> None:
    registry = load_default_second_batch_registry()
    validation = validate_second_batch_registry(registry)

    assert validation["family_counts"] == {
        "graph": 32,
        "arithmetic": 34,
        "finite": 34,
    }
    assert validation["total_count"] == SECOND_BATCH_EXPECTED_TOTAL == 100
    assert registry.runner_for(EXECUTOR_ID) is run_second_batch_finite_search


def test_registry_rejects_known_cross_batch_concept_duplicates() -> None:
    registry = load_default_second_batch_registry()
    finite_specs = list(registry.extra_families[0].specs)
    duplicate = dict(finite_specs[0])
    duplicate["problem_id"] = "unsolvedmath-opg-432"
    finite_specs[0] = duplicate
    invalid = SecondBatchRegistry(
        graph_specs=registry.graph_specs,
        arithmetic_specs=registry.arithmetic_specs,
        graph_runner=registry.graph_runner,
        arithmetic_runner=registry.arithmetic_runner,
        extra_families=(
            SecondBatchExecutorFamily(
                family="finite",
                specs=finite_specs,
                runner=run_second_batch_finite_search,
            ),
        ),
    )

    with pytest.raises(
        SecondBatchConfigurationError, match="conceptually duplicates"
    ):
        validate_second_batch_registry(invalid)


@pytest.mark.parametrize(
    "spec",
    SECOND_BATCH_FINITE_SPECS,
    ids=lambda spec: str(spec["source_id"]),
)
def test_each_finite_spec_preserves_the_source_statement_and_scope(spec: dict) -> None:
    source = SOURCE_BANK[spec["problem_id"]]
    contract = spec["model_contract"]

    assert spec["source_id"] == source["metadata"]["source_id"]
    assert spec["title"] == source["title"]
    assert spec["domain"] == source["domain"]
    assert contract["source_statement"] == source["statement"]
    assert spec["claim_scope"] in ALLOWED_SCOPES
    assert contract["claim_scope"] == spec["claim_scope"]
    assert contract["scope_limitation"] == spec["scope_limitation"]
    expected_quantifiers = (
        spec["claim_scope"] != "restricted_family"
        and spec["problem_id"] != "unsolvedmath-comb-003"
    )
    assert bool(contract["source_quantifiers_preserved"]) is expected_quantifiers
    assert contract["objects"]
    assert contract["premise"]
    assert contract["counterexample_or_witness"]
    assert "bounded" in contract["bounded_result_semantics"].lower()
    if spec["problem_id"] in CATALOGUE_SHARDED_IDS:
        assert spec["strategies"] == ["screen-exact", *CATALOGUE_STRATEGIES]
        assert spec["deep_strategies"] == CATALOGUE_STRATEGIES
        assert spec["deep_launches"] == 1
    else:
        assert spec["strategies"] == ["screen-exact", "deep-diversified"]
        assert spec["deep_strategies"] == ["deep-diversified"]
    assert spec["screen_bounds"]["max_cases"] > 0
    assert spec["deep_bounds"]["max_cases"] > 0
    assert spec["deep_launches"] in {1, 3}
    assert spec["deep_search_role"] in {
        "disjoint_canonical_catalogue_shards",
        "seeded_stratified_frontier_search",
        "monotone_exact_case_enumeration",
    }
    assert spec["frontier_provenance"]["case_generator_contract"]
    assert spec["frontier_provenance"]["resume_indexing"]


@pytest.mark.parametrize(
    "spec",
    SECOND_BATCH_FINITE_SPECS,
    ids=lambda spec: str(spec["source_id"]),
)
def test_each_finite_problem_has_a_one_case_executable_smoke(spec: dict) -> None:
    result = run_second_batch_finite_search(
        spec["problem_id"],
        strategy_id="screen-exact",
        budget={"max_cases": 1, "time_seconds": 10, "max_flips": 500},
        seed=7,
    )

    assert result["executor_id"] == EXECUTOR_ID
    assert result["strategy_id"] == "screen-exact"
    assert result["checked_cases"] == 1
    assert result["outcome"] in {"candidate", "inconclusive"}
    assert result["stop_reason"] in {
        "candidate_found",
        "case_budget_exhausted",
    }
    assert result["checkpoint"]["next_case"] == 1
    assert result["checkpoint"]["atomic_boundary"] == "one complete finite case"
    assert result["model_contract"] == spec["model_contract"]
    assert result["metrics"]["atomic_cases"] == 1
    if result["candidate"] is not None:
        assert verify_second_batch_finite_candidate(
            spec["problem_id"], result["candidate"]
        )


def test_checkpoint_resume_and_seed_strata_are_deterministic() -> None:
    problem_id = "unsolvedmath-nt-027"
    first = run_second_batch_finite_search(
        problem_id,
        strategy_id="deep-diversified",
        budget={"max_cases": 1},
        seed=101,
    )
    repeated = run_second_batch_finite_search(
        problem_id,
        strategy_id="deep-diversified",
        budget={"max_cases": 1},
        seed=101,
    )
    other_seed = run_second_batch_finite_search(
        problem_id,
        strategy_id="deep-diversified",
        budget={"max_cases": 1},
        seed=202,
    )
    resumed = run_second_batch_finite_search(
        problem_id,
        strategy_id="deep-diversified",
        budget={"max_cases": 1},
        seed=101,
        checkpoint=first["checkpoint"],
    )

    assert first["checkpoint"] == repeated["checkpoint"]
    assert first["checkpoint"]["stratum"] != other_seed["checkpoint"]["stratum"]
    assert resumed["checkpoint"]["next_case"] == 2
    assert resumed["checkpoint"]["seed"] == 101
    with pytest.raises(ValueError, match="seed"):
        run_second_batch_finite_search(
            problem_id,
            strategy_id="deep-diversified",
            budget={"max_cases": 1},
            seed=999,
            checkpoint=first["checkpoint"],
        )


@pytest.mark.parametrize(
    ("problem_id", "strategy_id"),
    [
        ("unsolvedmath-kou-21.26", "deep-diversified"),
        ("unsolvedmath-kou-21.99", "deep-diversified"),
        ("unsolvedmath-opg-48264", "deep-diversified"),
        ("unsolvedmath-nt-027", "deep-catalogue-0"),
    ],
)
def test_runner_rejects_strategies_not_declared_by_the_problem(
    problem_id: str, strategy_id: str
) -> None:
    with pytest.raises(ValueError, match="unsupported strategy"):
        run_second_batch_finite_search(
            problem_id,
            strategy_id=strategy_id,
            budget={"max_cases": 1},
            seed=101,
        )


def test_independent_verifier_rejects_unbound_or_tampered_certificates() -> None:
    assert not verify_second_batch_finite_candidate(
        "unsolvedmath-nt-027", {"witness": {"n": 1}}
    )
    assert not verify_second_batch_finite_candidate(
        "unsolvedmath-nt-027",
        {
            "search_case": {"n": 1},
            "witness": {"n": 1, "fabricated": True},
        },
    )


@pytest.mark.parametrize(
    "problem_id",
    [
        "unsolvedmath-comb-003",
        "unsolvedmath-opg-404",
        "unsolvedmath-opg-600",
        "unsolvedmath-nt-039",
    ],
)
def test_expensive_searches_honor_an_internal_wall_clock_deadline(
    problem_id: str,
) -> None:
    started = time.monotonic()
    result = run_second_batch_finite_search(
        problem_id,
        strategy_id="screen-exact",
        budget={"max_cases": 10, "time_seconds": 0.1},
        seed=5,
    )
    elapsed = time.monotonic() - started

    assert elapsed < 1.0
    assert result["outcome"] in {"candidate", "inconclusive"}
    if result["outcome"] == "inconclusive":
        assert result["stop_reason"] in {
            "time_budget_exhausted",
            "case_budget_exhausted",
        }
    assert result["checkpoint"]["next_case"] == result["checked_cases"]


def test_progress_is_throttled_and_final_atomic_checkpoint_is_forced() -> None:
    updates: list[tuple[dict, int]] = []

    result = run_second_batch_finite_search(
        "unsolvedmath-nt-026",
        strategy_id="screen-exact",
        budget={"max_cases": 250},
        seed=11,
        progress=lambda checkpoint, checked: updates.append(
            (dict(checkpoint), int(checked))
        ),
    )

    assert [checked for _, checked in updates] == [100, 200, 250]
    assert result["checkpoint"]["next_case"] == 250
    assert updates[-1][0] == result["checkpoint"]


def test_mid_case_timeout_does_not_advance_the_atomic_cursor() -> None:
    updates: list[tuple[dict, int]] = []
    result = run_second_batch_finite_search(
        "unsolvedmath-comb-003",
        strategy_id="screen-exact",
        budget={"max_cases": 10, "time_seconds": 0.01},
        seed=17,
        progress=lambda checkpoint, checked: updates.append(
            (dict(checkpoint), int(checked))
        ),
    )

    assert result["outcome"] == "inconclusive"
    assert result["stop_reason"] == "time_budget_exhausted"
    assert result["metrics"]["timed_out_mid_case"] is True
    assert result["checkpoint"]["next_case"] == result["checked_cases"]
    assert updates[-1][0] == result["checkpoint"]


@pytest.mark.parametrize(
    "problem_id",
    [
        "unsolvedmath-comb-003",
        "unsolvedmath-opg-369",
        "unsolvedmath-opg-600",
        "unsolvedmath-opg-382",
    ],
)
def test_replacement_problem_checkpoint_resumes_at_the_next_atomic_case(
    problem_id: str,
) -> None:
    first = run_second_batch_finite_search(
        problem_id,
        strategy_id="screen-exact",
        budget={"max_cases": 1, "time_seconds": 10, "max_flips": 500},
        seed=23,
    )
    assert first["checked_cases"] == 1
    resumed = run_second_batch_finite_search(
        problem_id,
        strategy_id="screen-exact",
        budget={"max_cases": 1, "time_seconds": 10, "max_flips": 500},
        seed=23,
        checkpoint=first["checkpoint"],
    )

    assert resumed["checked_cases"] == 1
    assert resumed["checkpoint"]["next_case"] == 2


def test_replacement_scopes_and_deep_launches_are_explicit() -> None:
    specs = {
        spec["problem_id"]: spec for spec in SECOND_BATCH_FINITE_SPECS
    }

    assert specs["unsolvedmath-comb-003"]["claim_scope"] == "witness_search"
    assert specs["unsolvedmath-opg-369"]["claim_scope"] == "restricted_family"
    assert specs["unsolvedmath-opg-600"]["claim_scope"] == "full_claim"
    assert specs["unsolvedmath-kou-21.26"]["claim_scope"] == "restricted_family"
    assert specs["unsolvedmath-opg-382"]["claim_scope"] == "restricted_family"
    assert specs["unsolvedmath-comb-003"]["deep_launches"] == 3
    assert specs["unsolvedmath-opg-369"]["deep_launches"] == 3
    assert specs["unsolvedmath-opg-600"]["deep_launches"] == 3
    assert specs["unsolvedmath-kou-21.26"]["deep_launches"] == 1
    assert specs["unsolvedmath-kou-21.99"]["deep_launches"] == 1
    assert specs["unsolvedmath-opg-48264"]["deep_launches"] == 1
    assert specs["unsolvedmath-opg-382"]["deep_launches"] == 3


def test_replacement_verifiers_reject_known_or_incomplete_certificates() -> None:
    assert not verify_second_batch_finite_candidate(
        "unsolvedmath-comb-003",
        {
            "search_case": {"order": 42, "attempt": 0},
            "witness": {"order": 42, "edges": [], "colors": []},
        },
    )
    assert not verify_second_batch_finite_candidate(
        "unsolvedmath-opg-600",
        {
            "search_case": {
                "dimension": 3,
                "matching": [[0, 1], [1, 3]],
            },
            "witness": {
                "dimension": 3,
                "matching": [[0, 1], [1, 3]],
                "solver_results": [],
            },
        },
    )


@pytest.mark.parametrize(
    "matroids",
    [
        [
            {"blocks": [[0]], "capacities": [1]},
            {"blocks": [[0], [0, 1]], "capacities": [1, 1]},
        ],
        [
            {"blocks": [[0, 1]], "capacities": [3]},
            {"blocks": [[0, 1]], "capacities": [0]},
        ],
        [
            {"blocks": [[0], [1]], "capacities": [1]},
            {"blocks": [[0], [1]], "capacities": [1, 1]},
        ],
    ],
)
def test_aharoni_berger_verifier_rejects_malformed_partition_matroids(
    matroids: list[dict],
) -> None:
    assert not verify_second_batch_finite_candidate(
        "unsolvedmath-opg-382",
        {
            "search_case": {
                "ground_size": 2,
                "k": 2,
                "ell": 1,
                "matroid_codes": [0, 0],
            },
            "witness": {
                "ground_size": 2,
                "k": 2,
                "ell": 1,
                "matroids": matroids,
            },
        },
    )


def test_expanded_group_and_regular_graph_cases_are_not_single_trivial_families() -> None:
    sylow_cases = [
        finite._case("unsolvedmath-kou-21.26", index) for index in range(6)
    ]
    kou_cases = [
        finite._case("unsolvedmath-kou-21.99", index) for index in range(6)
    ]
    signing_cases = [
        finite._case("unsolvedmath-opg-48264", index) for index in range(6)
    ]

    assert {case["catalogue_label"] for case in sylow_cases} == {
        "S3",
        "A4",
        "D12",
        "S4",
        "A5",
        "D20",
    }
    assert {case["family"] for case in kou_cases} == {
        "symmetric",
        "dihedral",
        "alternating",
    }
    assert {case["family"] for case in signing_cases} == {
        "prism",
        "mobius_ladder",
        "petersen",
        "circulant4",
        "bipartite_quartic",
        "quartic_circulant",
    }
    graph_degrees = set()
    for case in signing_cases:
        order, edges = finite._group_edges(case["family"], case["level"])
        degrees = [
            sum(vertex in edge for edge in edges) for vertex in range(order)
        ]
        assert len(set(degrees)) == 1
        graph_degrees.add(degrees[0])
    assert graph_degrees == {3, 4}


def test_kourovka_fixed_point_search_uses_nonregular_coset_actions() -> None:
    for index in range(6):
        case = finite._case("unsolvedmath-kou-21.99", index)
        source_group = finite._permutation_group(
            case["family"], case["parameter"]
        )
        subgroup = finite._catalogue_subgroup(
            source_group, case["subgroup_kind"]
        )
        action, cosets = finite._coset_action(source_group, subgroup, None)

        assert 1 < len(subgroup) < len(source_group)
        assert len(cosets) < len(source_group)
        assert {permutation[0] for permutation in action} == set(
            range(len(cosets))
        )


def test_kourovka_sylow_deep_catalogue_cycles_factor_families() -> None:
    if not finite.GAP_BINARY.exists() or not finite.GAP_ROOT.exists():
        pytest.skip("isolated GAP SmallGroups installation is unavailable")

    catalogue = finite._kou_21_26_smallgroup_catalogue()
    cases = [
        finite._case(
            "unsolvedmath-kou-21.26",
            finite._seeded_index(
                "unsolvedmath-kou-21.26",
                cursor,
                "deep-catalogue-0",
                101,
            ),
        )
        for cursor in range(6)
    ]

    assert len(catalogue) > 6_000
    assert len({order for order, _ in catalogue}) > 100
    assert len({case["catalogue_family"] for case in cases}) == 6
    assert len({tuple(case["smallgroup_id"]) for case in cases}) == 6
    assert all(case["group_order"] > 60 for case in cases)


def test_kourovka_deep_group_and_action_coverage_survives_resume() -> None:
    if not finite.GAP_BINARY.exists() or not finite.GAP_ROOT.exists():
        pytest.skip("isolated GAP SmallGroups installation is unavailable")

    sylow_first = run_second_batch_finite_search(
        "unsolvedmath-kou-21.26",
        strategy_id="deep-catalogue-0",
        budget={"max_cases": 3, "time_seconds": 10},
        seed=101,
    )
    sylow_resumed = run_second_batch_finite_search(
        "unsolvedmath-kou-21.26",
        strategy_id="deep-catalogue-0",
        budget={"max_cases": 3, "time_seconds": 10},
        seed=101,
        checkpoint=sylow_first["checkpoint"],
    )
    action_first = run_second_batch_finite_search(
        "unsolvedmath-kou-21.99",
        strategy_id="deep-catalogue-0",
        budget={"max_cases": 3, "time_seconds": 10},
        seed=101,
    )
    action_resumed = run_second_batch_finite_search(
        "unsolvedmath-kou-21.99",
        strategy_id="deep-catalogue-0",
        budget={"max_cases": 3, "time_seconds": 10},
        seed=101,
        checkpoint=action_first["checkpoint"],
    )

    assert sylow_resumed["checkpoint"]["next_case"] == 6
    assert len(sylow_resumed["metrics"]["smallgroup_ids_tested"]) == 6
    assert len(sylow_resumed["metrics"]["group_families_tested"]) == 6
    assert sylow_resumed["metrics"]["catalogue_shard_position"] == 5
    assert sylow_resumed["metrics"]["catalogue_shard_size"] == 2_103
    assert (
        sylow_resumed["metrics"]["group_search_role"]
        == "nonabelian_smallgroups_orders_61_through_255"
    )
    assert action_resumed["checkpoint"]["next_case"] == 6
    assert len(action_resumed["metrics"]["action_labels_tested"]) == 6
    assert len(action_resumed["metrics"]["action_hashes_tested"]) == 6
    assert len(action_resumed["metrics"]["action_degrees_tested"]) >= 4


def test_kourovka_sylow_deep_shards_are_a_unique_global_partition() -> None:
    if not finite.GAP_BINARY.exists() or not finite.GAP_ROOT.exists():
        pytest.skip("isolated GAP SmallGroups installation is unavailable")

    catalogue = finite._kou_21_26_smallgroup_catalogue()
    shards = finite._kou_21_26_catalogue_shards()
    global_ids = [
        (order, group_index)
        for shard in shards
        for _family, _position, order, group_index in shard
    ]

    assert len(catalogue) == 6_308
    assert [len(shard) for shard in shards] == [2_103, 2_102, 2_103]
    assert len(global_ids) == len(set(global_ids)) == len(catalogue)
    assert set(global_ids) == set(catalogue)

    first_thousand_ids = []
    for shard, strategy_id in enumerate(CATALOGUE_STRATEGIES):
        cases = [
            finite._case(
                "unsolvedmath-kou-21.26",
                finite._seeded_index(
                    "unsolvedmath-kou-21.26",
                    cursor,
                    strategy_id,
                    101,
                ),
            )
            for cursor in range(min(1_000, len(shards[shard])))
        ]
        ids = {tuple(case["smallgroup_id"]) for case in cases}
        assert len(ids) == len(cases)
        assert {case["catalogue_shard"] for case in cases} == {shard}
        assert [case["catalogue_shard_position"] for case in cases] == list(
            range(len(cases))
        )
        first_thousand_ids.append(ids)

    assert all(
        first_thousand_ids[left].isdisjoint(first_thousand_ids[right])
        for left, right in ((0, 1), (0, 2), (1, 2))
    )


def test_kourovka_deep_coset_catalogue_is_faithful_unique_and_diverse() -> None:
    labels = set()
    action_hashes = set()
    degrees = set()
    source_orders = set()
    subgroup_orders = set()
    positions = set()
    shards = finite._kou_21_99_action_shards()
    for shard, strategy_id in enumerate(CATALOGUE_STRATEGIES):
        for shard_position in range(len(shards[shard])):
            case = finite._case(
                "unsolvedmath-kou-21.99",
                finite._seeded_index(
                    "unsolvedmath-kou-21.99",
                    shard_position,
                    strategy_id,
                    101,
                ),
            )
            source_group = finite._permutation_group(
                case["family"], case["parameter"]
            )
            subgroup = finite._catalogue_subgroup(
                source_group, case["subgroup_kind"]
            )
            action, cosets = finite._coset_action(
                source_group, subgroup, None
            )
            action_hash = finite.hashlib.sha256(
                finite.json.dumps(
                    [list(permutation) for permutation in action],
                    separators=(",", ":"),
                ).encode()
            ).hexdigest()

            labels.add(case["catalogue_label"])
            action_hashes.add(action_hash)
            degrees.add(len(cosets))
            source_orders.add(len(source_group))
            subgroup_orders.add(len(subgroup))
            positions.add(case["catalogue_position"])
            assert case["catalogue_shard"] == shard
            assert case["catalogue_shard_position"] == shard_position
            assert 1 < len(subgroup) < len(source_group)
            assert len(action) == len(source_group)
            assert len(action) > len(cosets)
            assert action_hash == case["action_sha256"]
            assert {permutation[0] for permutation in action} == set(
                range(len(cosets))
            )

    assert len(labels) == len(action_hashes) == 17
    assert positions == set(range(17))
    assert len(degrees) >= 10
    assert len(source_orders) >= 6
    assert len(subgroup_orders) >= 7


def test_kourovka_action_shards_stop_at_their_finite_bound() -> None:
    shards = finite._kou_21_99_action_shards()
    observed_positions = set()

    for shard, strategy_id in enumerate(CATALOGUE_STRATEGIES):
        result = run_second_batch_finite_search(
            "unsolvedmath-kou-21.99",
            strategy_id=strategy_id,
            budget={"max_cases": 100, "time_seconds": 10},
            seed=101,
        )

        assert result["checked_cases"] == len(shards[shard])
        assert result["checkpoint"]["next_case"] == len(shards[shard])
        assert result["stop_reason"] == "finite_catalogue_exhausted"
        assert result["metrics"]["finite_catalogue_exhausted"] is True
        assert result["metrics"]["action_catalogue_shards_tested"] == [shard]
        observed_positions.update(
            result["metrics"]["action_catalogue_positions_tested"]
        )

        repeated = run_second_batch_finite_search(
            "unsolvedmath-kou-21.99",
            strategy_id=strategy_id,
            budget={"max_cases": 1, "time_seconds": 10},
            seed=101,
            checkpoint=result["checkpoint"],
        )
        assert repeated["checked_cases"] == 0
        assert repeated["checkpoint"] == result["checkpoint"]
        assert repeated["stop_reason"] == "finite_catalogue_exhausted"

    assert observed_positions == set(range(17))


@pytest.mark.parametrize(
    ("problem_id", "max_cases"),
    [
        ("unsolvedmath-kou-21.26", 6),
        ("unsolvedmath-kou-21.99", 6),
        ("unsolvedmath-opg-48264", 6),
    ],
)
def test_expanded_families_execute_multiple_informative_cases(
    problem_id: str, max_cases: int
) -> None:
    result = run_second_batch_finite_search(
        problem_id,
        strategy_id="screen-exact",
        budget={"max_cases": max_cases, "time_seconds": 10},
        seed=31,
    )

    assert result["checked_cases"] == max_cases
    assert result["checkpoint"]["next_case"] == max_cases
    if problem_id == "unsolvedmath-kou-21.99":
        assert len(result["metrics"]["action_families_tested"]) == 3
        assert len(result["metrics"]["source_group_orders_tested"]) >= 3
        assert len(result["metrics"]["subgroup_orders_tested"]) >= 3
    if problem_id == "unsolvedmath-opg-48264":
        assert set(result["metrics"]["signing_graph_families_tested"]) == {
            "prism",
            "mobius_ladder",
            "petersen",
            "circulant4",
            "bipartite_quartic",
            "quartic_circulant",
        }
        assert len(result["metrics"]["signing_graph_hashes_tested"]) == 6
        assert result["metrics"]["normalized_signings_checked_total"] >= 6


def test_aharoni_berger_deep_strata_prioritize_k_at_least_four() -> None:
    logical_indices = {
        finite._seeded_index(
            "unsolvedmath-opg-382", 0, "deep-diversified", seed
        )
        for seed in (101, 202, 303)
    }
    cases = [
        finite._case("unsolvedmath-opg-382", index)
        for index in logical_indices
    ]

    assert len(logical_indices) >= 2
    assert all(case["k"] >= 4 for case in cases)


def test_many_weights_cases_use_only_composite_cyclic_groups() -> None:
    cases = [finite._case("unsolvedmath-opg-369", index) for index in range(24)]
    assert {case["modulus"] for case in cases} == {4, 6, 8, 9, 10, 12}
    assert all(not finite.sympy.isprime(case["modulus"]) for case in cases)


def test_many_weights_deep_strata_reach_larger_graphs_and_weight_strata() -> None:
    cases = [
        finite._case(
            "unsolvedmath-opg-369",
            finite._seeded_index(
                "unsolvedmath-opg-369", 0, "deep-diversified", seed
            ),
        )
        for seed in (101, 202, 303)
    ]

    assert all(case["vertices"] >= 5 for case in cases)
    assert len({tuple(case["weights"]) for case in cases}) == 3
    assert all(not finite.sympy.isprime(case["modulus"]) for case in cases)


def test_hypercube_screen_and_deep_cases_target_distinct_known_ranges() -> None:
    screen = [
        finite._case("unsolvedmath-opg-600", index) for index in range(16)
    ]
    deep = [
        finite._case(
            "unsolvedmath-opg-600",
            finite._seeded_index(
                "unsolvedmath-opg-600", 0, "deep-diversified", seed
            ),
        )
        for seed in (101, 202, 303)
    ]

    assert all(2 <= case["dimension"] <= 5 for case in screen)
    assert all(case["search_role"] == "replication_d_le_5" for case in screen)
    assert all(case["dimension"] == 6 for case in deep)
    assert all(
        case["search_role"] == "frontier_q6_uncovered_matching"
        for case in deep
    )
    assert all(case["perfect_matching_extendable"] is False for case in deep)
    assert all(len(case["matching"]) >= 16 > 2 * case["dimension"] - 1 for case in deep)
    assert all(
        {
            (left ^ right).bit_length() - 1
            for left, right in case["matching"]
        }
        == set(range(6))
        for case in deep
    )
    assert len(
        {
            tuple(tuple(edge) for edge in case["matching"])
            for case in deep
        }
    ) == 3


def test_hypercube_unsat_encodings_are_independently_generated() -> None:
    case = finite._case("unsolvedmath-opg-600", 0)
    matching = finite._validated_hypercube_matching(
        case["dimension"], case["matching"]
    )
    assert matching is not None
    successor = finite._hamiltonian_successor_smt(
        case["dimension"], matching, None
    )
    flow = finite._hamiltonian_flow_smt(
        case["dimension"], matching, None
    )

    assert successor != flow
    assert "(declare-fun p_" in successor
    assert "(declare-fun f_" in flow


def test_hypercube_deep_solver_timeout_is_atomic() -> None:
    started = time.monotonic()
    result = run_second_batch_finite_search(
        "unsolvedmath-opg-600",
        strategy_id="deep-diversified",
        budget={"max_cases": 1, "time_seconds": 0.1},
        seed=101,
    )

    assert time.monotonic() - started < 1.0
    assert result["checked_cases"] == 0
    assert result["checkpoint"]["next_case"] == 0
    assert result["stop_reason"] == "time_budget_exhausted"
    assert result["metrics"]["timed_out_mid_case"] is True
    assert result["metrics"]["direction_count"] == 6
    assert result["metrics"]["matching_size"] >= 16
    assert result["metrics"]["frontier_exceeded"] is True
    assert len(result["metrics"]["matching_hashes_tested"]) == 1


def test_hypercube_frontier_rejects_perfect_extendable_partial_matching() -> None:
    perfect = {
        (vertex, vertex ^ 1)
        for vertex in range(64)
        if vertex & 1 == 0
    }
    for direction in range(1, 6):
        for base in range(64):
            if base & 1:
                continue
            first = tuple(sorted((base, base ^ 1)))
            second = tuple(
                sorted((base ^ (1 << direction), base ^ (1 << direction) ^ 1))
            )
            if first not in perfect or second not in perfect:
                continue
            perfect.remove(first)
            perfect.remove(second)
            perfect.add(tuple(sorted((base, base ^ (1 << direction)))))
            perfect.add(
                tuple(
                    sorted(
                        (
                            base ^ 1,
                            base ^ 1 ^ (1 << direction),
                        )
                    )
                )
            )
            break
        else:
            raise AssertionError("failed to diversify a Q6 perfect matching")

    diversified = sorted(
        edge for edge in perfect if (edge[0] ^ edge[1]) != 1
    )
    direction_zero = sorted(
        edge for edge in perfect if (edge[0] ^ edge[1]) == 1
    )
    partial = diversified + direction_zero[: 16 - len(diversified)]
    metrics: dict = {}

    assert len(partial) == 16
    assert len({(left ^ right).bit_length() - 1 for left, right in partial}) == 6
    assert finite._matching_extends_to_perfect(6, partial)
    with pytest.raises(RuntimeError, match="extendable_to_perfect_matching"):
        finite._search_hypercube_matching(
            {
                "dimension": 6,
                "matching": partial,
                "search_role": "frontier_q6_uncovered_matching",
            },
            None,
            metrics,
        )
    assert metrics["frontier_exceeded"] is False
    assert metrics["known_family_reasons"] == [
        "extendable_to_perfect_matching"
    ]


def test_graph_signing_index_700_timeout_kills_worker_and_is_atomic() -> None:
    checkpoint = {
        "next_case": 700,
        "strategy_id": "screen-exact",
        "seed": 7,
    }
    started = time.monotonic()
    result = run_second_batch_finite_search(
        "unsolvedmath-opg-48264",
        strategy_id="screen-exact",
        budget={"max_cases": 1, "time_seconds": 0.1},
        seed=7,
        checkpoint=checkpoint,
    )

    assert time.monotonic() - started < 1.0
    assert result["checked_cases"] == 0
    assert result["checkpoint"]["next_case"] == 700
    assert result["stop_reason"] == "time_budget_exhausted"
    assert result["metrics"]["timed_out_mid_case"] is True


def test_graph_signing_deep_catalogue_is_large_unique_and_sharded() -> None:
    catalogue = finite._opg_48264_deep_catalogue()
    position_shards = [
        set(range(shard, len(catalogue), 3)) for shard in range(3)
    ]

    assert len(catalogue) == len(set(catalogue)) == 41_301
    assert [len(shard) for shard in position_shards] == [13_767] * 3
    assert set().union(*position_shards) == set(range(len(catalogue)))
    assert all(
        position_shards[left].isdisjoint(position_shards[right])
        for left, right in ((0, 1), (0, 2), (1, 2))
    )
    first_thousand_positions = []
    first_thousand_graphs = []
    for shard, strategy_id in enumerate(CATALOGUE_STRATEGIES):
        cases = [
            finite._case(
                "unsolvedmath-opg-48264",
                finite._seeded_index(
                    "unsolvedmath-opg-48264",
                    cursor,
                    strategy_id,
                    101,
                ),
            )
            for cursor in range(1_000)
        ]
        positions = {case["catalogue_position"] for case in cases}
        graphs = {
            finite._group_edges(case["family"], case["level"])[1]
            for case in cases
        }

        assert len(positions) == len(graphs) == len(cases)
        assert {case["catalogue_shard"] for case in cases} == {shard}
        assert [case["catalogue_shard_position"] for case in cases] == list(
            range(1_000)
        )
        assert {case["family"] for case in cases} == {"nauty_cubic_18"}
        assert {
            finite._group_edges(case["family"], case["level"])[0]
            for case in cases
        } == {18}
        first_thousand_positions.append(positions)
        first_thousand_graphs.append(graphs)

    assert all(
        first_thousand_positions[left].isdisjoint(
            first_thousand_positions[right]
        )
        and first_thousand_graphs[left].isdisjoint(
            first_thousand_graphs[right]
        )
        for left, right in ((0, 1), (0, 2), (1, 2))
    )

    screen_cases = [
        finite._case("unsolvedmath-opg-48264", cursor)
        for cursor in range(6)
    ]
    assert all("catalogue_position" not in case for case in screen_cases)
    assert {case["family"] for case in screen_cases}.isdisjoint(
        {"nauty_cubic_18"}
    )


def test_graph_signing_deep_case_executes_exact_normalized_signings() -> None:
    result = run_second_batch_finite_search(
        "unsolvedmath-opg-48264",
        strategy_id="deep-catalogue-0",
        budget={"max_cases": 1, "time_seconds": 30},
        seed=101,
    )

    assert result["checked_cases"] == 1
    assert result["checkpoint"]["next_case"] == 1
    assert result["metrics"]["graph_order"] == 18
    assert result["metrics"]["graph_degree"] == 3
    assert result["metrics"]["cycle_rank"] == 10
    assert 1 <= result["metrics"]["normalized_signings_checked"] <= 1 << 10
    assert result["metrics"]["signing_catalogue_positions_tested"] == [0]
    assert result["metrics"]["signing_catalogue_shards_tested"] == [0]
    assert result["metrics"]["signing_catalogue_shard_position"] == 0
    assert (
        result["metrics"]["signing_certificate_method"]
        == "exact_rational_schur_negative_direction"
    )


@pytest.mark.parametrize(
    ("matrix", "positive_semidefinite"),
    [
        ([[2, -1], [-1, 2]], True),
        ([[0, 0], [0, 0]], True),
        ([[-1, 0], [0, 3]], False),
        ([[0, 2], [2, 0]], False),
        ([[2, 3], [3, 2]], False),
        (
            [
                [4, 2, 0],
                [2, 1, 3],
                [0, 3, 1],
            ],
            False,
        ),
    ],
)
def test_graph_signing_negative_directions_are_exact_integer_certificates(
    matrix: list[list[int]],
    positive_semidefinite: bool,
) -> None:
    vector = finite._negative_quadratic_witness(matrix)

    if positive_semidefinite:
        assert vector is None
    else:
        assert vector is not None
        assert all(isinstance(value, int) for value in vector)
        assert finite._integer_quadratic_value(matrix, vector) < 0


def test_graph_signing_verifier_rejects_nonnegative_or_incomplete_certificates() -> None:
    search_case = {"family": "prism", "level": 0}
    order, edges = finite._group_edges(
        search_case["family"], search_case["level"]
    )
    tree_edges = finite._spanning_tree_edge_indices(order, edges)
    free_count = len(edges) - len(tree_edges)
    degree = 3
    certificates = [
        {
            "signing_bits": signing_bits,
            "vector": [1, *([0] * (order - 1))],
            "quadratic_value": 5,
        }
        for signing_bits in range(1 << free_count)
    ]
    forged = {
        "search_case": search_case,
        "witness": {
            "order": order,
            "family": search_case["family"],
            "degree": degree,
            "edges": [list(edge) for edge in edges],
            "spanning_tree_edge_indices": list(tree_edges),
            "cycle_rank": free_count,
            "threshold_squared": 4 * (degree - 1),
            "signing_witnesses": certificates,
        },
    }

    assert not verify_second_batch_finite_candidate(
        "unsolvedmath-opg-48264", forged
    )
    forged["witness"]["signing_witnesses"] = certificates[:-1]
    assert not verify_second_batch_finite_candidate(
        "unsolvedmath-opg-48264", forged
    )


def test_ramsey_search_extends_a_verified_k42_and_reports_seeded_trajectories() -> None:
    for vertices in finite.itertools.combinations(range(42), 5):
        colors = {
            finite._RAMSEY_55_K42_ROWS[left][right]
            for left, right in finite.itertools.combinations(vertices, 2)
        }
        assert len(colors) > 1

    results = [
        run_second_batch_finite_search(
            "unsolvedmath-comb-003",
            strategy_id="deep-diversified",
            budget={
                "max_cases": 1,
                "time_seconds": 5,
                "max_flips": 200,
            },
            seed=seed,
        )
        for seed in (101, 202, 303)
    ]

    assert all(result["checked_cases"] == 1 for result in results)
    assert all(result["metrics"]["flips"] == 200 for result in results)
    assert all("best_conflicts" in result["metrics"] for result in results)
    assert len(
        {
            result["metrics"]["trajectory_hashes"][0]
            for result in results
        }
    ) == 3


def test_ramsey_deep_search_uses_full_and_perturbed_edge_basins() -> None:
    expected_basins = {
        "known_k42_extension",
        "full_k43_restart",
        "perturbed_k42_extension",
    }
    cases = [
        finite._case(
            "unsolvedmath-comb-003",
            finite._RAMSEY_DEEP_OFFSET + index,
        )
        for index in range(3)
    ]
    assert {case["search_basin"] for case in cases} == expected_basins

    perturbation_metrics: dict = {}
    perturbed = finite._perturbed_k42_edge_colors(
        finite._RAMSEY_DEEP_OFFSET + 2,
        None,
        perturbation_metrics,
    )
    known = finite._known_k42_edge_colors()
    edges, five_set_edges, _, k42_mask = finite._ramsey_k43_search_arrays()
    edge_lookup = {edge: index for index, edge in enumerate(edges)}
    colors = finite.numpy.zeros(len(edges), dtype=finite.numpy.uint8)
    for edge, color in perturbed.items():
        colors[edge_lookup[edge]] = color

    assert perturbed != known
    assert perturbation_metrics["base_changed_edges"] > 0
    assert not finite.numpy.any(
        finite._monochromatic_rows(
            colors,
            five_set_edges[k42_mask],
        )
    )

    full_metrics: dict = {}
    finite._search_ramsey_55(
        finite._RAMSEY_DEEP_OFFSET + 1,
        200,
        None,
        full_metrics,
        "full_k43_restart",
    )
    assert full_metrics["edge_space_size"] == 903
    assert full_metrics["active_edge_count"] > 42
    assert full_metrics["initialization"] == "full_random_K43"


def test_ramsey_basin_coverage_survives_checkpoint_resume() -> None:
    first = run_second_batch_finite_search(
        "unsolvedmath-comb-003",
        strategy_id="deep-diversified",
        budget={
            "max_cases": 2,
            "time_seconds": 10,
            "max_flips": 100,
        },
        seed=101,
    )
    frozen_first_checkpoint = copy.deepcopy(first["checkpoint"])
    resumed = run_second_batch_finite_search(
        "unsolvedmath-comb-003",
        strategy_id="deep-diversified",
        budget={
            "max_cases": 1,
            "time_seconds": 10,
            "max_flips": 100,
        },
        seed=101,
        checkpoint=first["checkpoint"],
    )

    assert resumed["checkpoint"]["next_case"] == 3
    assert set(resumed["metrics"]["search_basins_tested"]) == {
        "known_k42_extension",
        "full_k43_restart",
        "perturbed_k42_extension",
    }
    assert resumed["metrics"]["edge_space_size"] == 903
    assert resumed["metrics"]["max_active_edge_count"] > 42
    assert len(resumed["metrics"]["trajectory_hashes"]) == 3
    assert len(resumed["metrics"]["base_coloring_hashes"]) >= 2
    assert first["checkpoint"] == frozen_first_checkpoint


def test_ramsey_default_deep_case_is_a_bounded_chunk(monkeypatch) -> None:
    observed: dict[str, int | str] = {}

    def fake_search(
        attempt,
        max_flips,
        deadline,
        metrics,
        search_basin,
    ):
        observed.update(
            {
                "attempt": int(attempt),
                "max_flips": int(max_flips),
                "search_basin": str(search_basin),
            }
        )
        metrics.update(
            {
                "flips": 0,
                "best_conflicts": 1,
                "trajectory_hash": "0" * 64,
                "search_basin": str(search_basin),
                "active_edge_count": 0,
                "edge_space_size": 903,
                "max_flips_configured": int(max_flips),
            }
        )
        return None

    monkeypatch.setattr(finite, "_search_ramsey_55", fake_search)
    result = run_second_batch_finite_search(
        "unsolvedmath-comb-003",
        strategy_id="deep-diversified",
        budget={"max_cases": 1, "time_seconds": 10},
        seed=101,
    )

    assert observed["max_flips"] == finite._RAMSEY_DEEP_CHUNK_FLIPS == 10_000
    assert result["checked_cases"] == 1
    assert result["metrics"]["max_flips_configured"] == 10_000


def test_ramsey_timeout_resume_restarts_atomically_and_matches_direct_run() -> None:
    seed = 6_827_464_245_645_958_021
    budget = {
        "max_cases": 1,
        "time_seconds": 15,
        "max_flips": 1_000,
    }
    timed = run_second_batch_finite_search(
        "unsolvedmath-comb-003",
        strategy_id="deep-diversified",
        budget={**budget, "time_seconds": 0.01},
        seed=seed,
    )

    assert timed["checked_cases"] == 0
    assert timed["checkpoint"]["next_case"] == 0
    assert timed["checkpoint"]["coverage"] == {}
    assert timed["stop_reason"] == "time_budget_exhausted"

    resumed = run_second_batch_finite_search(
        "unsolvedmath-comb-003",
        strategy_id="deep-diversified",
        budget=budget,
        seed=seed,
        checkpoint=timed["checkpoint"],
    )
    direct = run_second_batch_finite_search(
        "unsolvedmath-comb-003",
        strategy_id="deep-diversified",
        budget=budget,
        seed=seed,
    )

    assert resumed["checked_cases"] == direct["checked_cases"] == 1
    assert resumed["checkpoint"]["next_case"] == 1
    assert resumed["checkpoint"]["coverage"] == direct["checkpoint"]["coverage"]
    assert resumed["metrics"]["trajectory_hashes"] == direct["metrics"][
        "trajectory_hashes"
    ]
    assert resumed["metrics"]["flips"] == direct["metrics"]["flips"] == 1_000


def test_grimm_matching_regression_finishes_the_previously_stalled_case() -> None:
    checkpoint = {
        "next_case": 1_608,
        "strategy_id": "deep-diversified",
        "seed": 20_260_727,
    }
    started = time.monotonic()
    result = run_second_batch_finite_search(
        "unsolvedmath-nt-033",
        strategy_id="deep-diversified",
        budget={"max_cases": 1, "time_seconds": 0.2},
        seed=20_260_727,
        checkpoint=checkpoint,
    )

    assert time.monotonic() - started < 1.0
    assert result["checked_cases"] == 1
    assert result["checkpoint"]["next_case"] == 1_609


def test_mixed_van_der_waerden_search_crosses_the_old_exact_cap() -> None:
    checkpoint = {
        "next_case": 5,
        "strategy_id": "deep-diversified",
        "seed": 20_260_727,
    }
    result = run_second_batch_finite_search(
        "unsolvedmath-opg-404",
        strategy_id="deep-diversified",
        budget={"max_cases": 1, "time_seconds": 5},
        seed=20_260_727,
        checkpoint=checkpoint,
    )

    assert result["checked_cases"] == 1
    assert result["checkpoint"]["next_case"] == 6
