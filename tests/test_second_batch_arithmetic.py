from __future__ import annotations

import time

import pytest
from sympy import nextprime
from sympy.ntheory.primetest import is_strong_lucas_prp, mr

from amra.discovery.second_batch_arithmetic import (
    _BPSW_KNOWN_EXHAUSTIVE_LOWER_BOUND,
    _SearchTimeLimit,
    GAP_BINARY,
    GAP_ROOT,
    SECOND_BATCH_ARITHMETIC_SPECS,
    _cross_polytope_vertices,
    _cube_vertices,
    _divisibility_matching,
    _exact_cs_polytope_data,
    _factorial_mod,
    _has_distinct_adjacent_sum_cycle,
    _prime_field_bases,
    _prime_sieve,
    _parse_gap_result,
    _native_selfridge_strong_lucas_prp,
    _native_strong_miller_rabin_base_2,
    _partition_number,
    _passes_bpsw_part_one,
    _remote_bpsw_layers,
    _remote_semiprime_streams,
    _rota_row_permutations,
    _rota_transversal_decomposition,
    _run_gap,
    _runner_has_lonely_time,
    _verify_candidate,
    _zero_sum_free,
    run_second_batch_arithmetic_search,
)


SMOKE_BUDGET = {
    "max_cases": 10,
    "max_order": 6,
    "max_n": 20,
    "max_q": 20,
    "max_modulus": 8,
    "max_index": 1,
    "max_factor": 30,
    "max_exponent": 12,
    "max_prime": 30,
    "root_height": 2,
    "max_dimension": 1,
    "max_xy": 20,
    "max_runners": 3,
    "max_speed": 3,
    "max_subset": 3,
    "max_cosets": 2,
    "max_row": 5,
    "max_root": 20,
    "max_base": 4,
    "max_value": 8,
    "max_moduli": 2,
    "max_power": 3,
}


@pytest.mark.parametrize(
    "spec",
    SECOND_BATCH_ARITHMETIC_SPECS,
    ids=lambda spec: str(spec["source_id"]),
)
def test_each_registered_arithmetic_problem_has_an_executable_smoke(spec: dict) -> None:
    if spec["domain"] == "group_theory" and not (GAP_BINARY.exists() and GAP_ROOT.exists()):
        pytest.skip("isolated GAP/SmallGrp is not installed")

    result = run_second_batch_arithmetic_search(
        spec["problem_id"],
        strategy_id="exact-small",
        budget=SMOKE_BUDGET,
        seed=7,
    )

    assert result["outcome"] in {
        "candidate_counterexample",
        "no_counterexample_within_bound",
        "inconclusive",
    }
    assert result["checked_cases"] >= 0
    assert result["stop_reason"]
    assert result["checkpoint"]["problem_id"] == spec["problem_id"]
    assert result["model_contract"] == spec["model_contract"]
    assert result["tool_versions"]["python_sympy"]
    if result["candidate"] is not None:
        verification = result["candidate"]["internal_verification"]
        assert verification["status"] == "passed"
        assert verification["independence"].startswith("internal_only")


def test_second_batch_contains_34_real_executors() -> None:
    allowed_scopes = {
        "full_claim",
        "explicit_subclaim",
        "restricted_family",
        "witness_search",
    }

    assert len(SECOND_BATCH_ARITHMETIC_SPECS) == 34
    assert len({spec["problem_id"] for spec in SECOND_BATCH_ARITHMETIC_SPECS}) == 34
    for spec in SECOND_BATCH_ARITHMETIC_SPECS:
        assert spec["claim_scope"] in allowed_scopes
        assert spec["scope_limitation"].endswith(".")
        expected_launches = 3 if "multistart" in spec["strategies"] else 1
        assert spec["deep_launches"] == expected_launches
        assert spec["deep_search_role"]
        assert spec["frontier_provenance"]


def test_replaced_problem_specs_preserve_source_scope_and_count() -> None:
    by_id = {
        str(spec["problem_id"]): spec
        for spec in SECOND_BATCH_ARITHMETIC_SPECS
    }
    added = {
        "unsolvedmath-kou-21.87",
        "unsolvedmath-kou-21.88",
        "unsolvedmath-kou-21.89",
        "unsolvedmath-opg-511",
    }

    assert added <= by_id.keys()
    assert all(by_id[problem_id]["source_statement"] for problem_id in added)
    for problem_id in added:
        contract = by_id[problem_id]["model_contract"]
        assert contract["source_statement"] == by_id[problem_id]["source_statement"]
        assert contract["scope_limitation"] == by_id[problem_id]["scope_limitation"]
    assert by_id["unsolvedmath-kou-21.87"]["claim_scope"] == "restricted_family"
    assert by_id["unsolvedmath-kou-21.88"]["claim_scope"] == "witness_search"
    assert by_id["unsolvedmath-kou-21.89"]["claim_scope"] == "full_claim"
    assert by_id["unsolvedmath-opg-511"]["claim_scope"] == "witness_search"
    assert "Part (2) is excluded" in by_id["unsolvedmath-opg-511"]["scope_limitation"]


def test_resolved_and_duplicate_replacements_are_absent_with_audited_provenance() -> None:
    by_id = {
        str(spec["problem_id"]): spec
        for spec in SECOND_BATCH_ARITHMETIC_SPECS
    }
    forbidden = {
        "unsolvedmath-alg-012",
        "unsolvedmath-opg-16555",
        "unsolvedmath-green-039",
        "unsolvedmath-green-071",
        "unsolvedmath-opg-37402",
    }
    rota_id = (
        "unsolvedmath-alg-012-collision-rota-s-basis-conjecture-5ad44b45"
    )

    assert forbidden.isdisjoint(by_id)
    assert by_id[rota_id]["claim_scope"] == "restricted_family"
    assert (
        by_id[rota_id]["frontier_provenance"]["current_progress"]
        == "arXiv:2508.05601"
    )
    assert "pairwise-disjoint labelled bases" in by_id[rota_id][
        "source_statement"
    ]
    assert by_id["unsolvedmath-geo-025"]["claim_scope"] == "restricted_family"
    assert by_id["unsolvedmath-geo-025"]["frontier_provenance"]["sources"] == [
        "arXiv:2308.02909",
        "arXiv:0708.3661",
    ]
    assert "excluding the empty face" in by_id["unsolvedmath-geo-025"][
        "source_statement"
    ]
    assert by_id["unsolvedmath-guy-a12a"]["claim_scope"] == "witness_search"
    bpsw_provenance = by_id["unsolvedmath-opg-511"]["frontier_provenance"]
    assert bpsw_provenance["part_number"] == 1
    assert "GUY-A12B" in bpsw_provenance["nonoverlap"]


def test_rota_row_matching_enforces_permutations_and_solver_returns_only_them() -> None:
    # All columns have a choice, but columns 1 and 2 both require row element 2.
    allowed = ((1,), (2,), (2,))
    assert all(allowed)
    assert list(_rota_row_permutations(allowed)) == []

    rank = 3
    standard = tuple(
        tuple(1 if row == column else 0 for column in range(rank))
        for row in range(rank)
    )
    sample_base = _prime_field_bases(rank, 2)[7]
    solved, _, arrangement = _rota_transversal_decomposition(
        (standard, sample_base, sample_base),
        2,
        node_limit=None,
    )

    assert solved is True
    assert arrangement is not None
    assert all(
        sorted(permutation) == list(range(rank))
        for permutation in arrangement
    )


@pytest.mark.parametrize("dimension", range(1, 5))
def test_kalai_cube_and_cross_polytope_have_exactly_three_power_d_faces(
    dimension: int,
) -> None:
    cube = _exact_cs_polytope_data(
        _cube_vertices(dimension),
        dimension,
        subset_limit=None,
        cross_check=True,
    )
    cross = _exact_cs_polytope_data(
        _cross_polytope_vertices(dimension),
        dimension,
        subset_limit=None,
        cross_check=True,
    )

    assert cube is not None
    assert cross is not None
    assert sum(cube["face_vector"]) == 3**dimension
    assert sum(cross["face_vector"]) == 3**dimension
    assert cube["face_vector"][-1] == cross["face_vector"][-1] == 1
    assert cube["nonempty_face_count"] == cross["nonempty_face_count"]


def test_rota_and_kalai_deep_streams_resume_without_replaying_cases() -> None:
    rota_id = (
        "unsolvedmath-alg-012-collision-rota-s-basis-conjecture-5ad44b45"
    )
    rota_budget = {
        "minimum_rank": 5,
        "max_rank": 5,
        "max_field_prime": 2,
        "solver_node_limit": 100_000,
        "max_cases": 2,
    }
    rota = run_second_batch_arithmetic_search(
        rota_id,
        strategy_id="multistart",
        budget=rota_budget,
        seed=17,
    )
    rota_resumed = run_second_batch_arithmetic_search(
        rota_id,
        strategy_id="multistart",
        budget={**rota_budget, "max_cases": 4},
        seed=17,
        checkpoint=rota["checkpoint"],
    )
    kalai_budget = {
        "minimum_dimension": 5,
        "max_dimension": 5,
        "max_antipodal_pairs": 7,
        "max_facet_subsets": 200_000,
        "max_cases": 2,
    }
    kalai = run_second_batch_arithmetic_search(
        "unsolvedmath-geo-025",
        strategy_id="multistart",
        budget=kalai_budget,
        seed=19,
    )
    kalai_resumed = run_second_batch_arithmetic_search(
        "unsolvedmath-geo-025",
        strategy_id="multistart",
        budget={**kalai_budget, "max_cases": 4},
        seed=19,
        checkpoint=kalai["checkpoint"],
    )

    assert rota_resumed["checked_cases"] == 4
    assert rota_resumed["metrics"]["exact_solver_cases"] == 4
    assert rota_resumed["metrics"]["solver_cutoff_cases"] == 0
    assert rota_resumed["checkpoint"]["resume"]["intra_bound_cursor_restored"]
    assert kalai_resumed["checked_cases"] == 4
    assert kalai_resumed["metrics"]["exact_polytopes"] == 4
    assert kalai_resumed["metrics"]["minimum_search_dimension"] == 5
    assert kalai_resumed["metrics"]["non_simple_non_simplicial"] > 0
    assert kalai_resumed["checkpoint"]["resume"]["intra_bound_cursor_restored"]


def test_partition_recurrence_and_modular_factorial_are_exact() -> None:
    partitions = [1]
    for value in range(1, 11):
        partitions.append(_partition_number(partitions, value))

    assert partitions == [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42]
    assert _factorial_mod(5, 7) == 1
    assert _factorial_mod(7, 7) == 0


def test_bpsw_screen_requires_both_probable_prime_predicates_and_factor_certificate() -> None:
    assert not _passes_bpsw_part_one(2_047)
    assert not _verify_candidate(
        "unsolvedmath-opg-511",
        {
            "n": 2_047,
            "nontrivial_factor": 23,
            "cofactor": 89,
        },
    )


def test_native_bpsw_replay_is_a_distinct_implementation_matching_reference() -> None:
    for value in range(3, 20_000, 2):
        assert _native_strong_miller_rabin_base_2(value) == bool(mr(value, [2]))
        assert _native_selfridge_strong_lucas_prp(value) == bool(
            is_strong_lucas_prp(value)
        )


def test_element_order_matching_checks_the_correct_divisibility_direction() -> None:
    assert _divisibility_matching((1, 2), (1, 4)) is not None
    assert _divisibility_matching((1, 4), (1, 2)) is None


def test_zero_sum_and_cyclic_order_verifiers_are_exact() -> None:
    assert _zero_sum_free(((1,),), 3)
    assert not _zero_sum_free(((1,), (2,)), 3)
    assert _has_distinct_adjacent_sum_cycle(5, (0, 1, 3))


def test_lonely_runner_interval_checker_handles_a_small_exact_instance() -> None:
    speeds = (0, 1, 3)

    assert all(_runner_has_lonely_time(speeds, runner) for runner in range(len(speeds)))


def test_runner_rejects_unregistered_problem_and_strategy() -> None:
    with pytest.raises(KeyError):
        run_second_batch_arithmetic_search(
            "missing",
            strategy_id="exact-small",
            budget={},
            seed=0,
        )

    with pytest.raises(ValueError):
        run_second_batch_arithmetic_search(
            SECOND_BATCH_ARITHMETIC_SPECS[0]["problem_id"],
            strategy_id="not-a-strategy",
            budget={},
            seed=0,
        )


def test_same_module_candidate_replay_is_not_labeled_independent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "amra.discovery.second_batch_arithmetic._execute",
        lambda *args, **kwargs: ({"synthetic": True}, 1, True),
    )
    monkeypatch.setattr(
        "amra.discovery.second_batch_arithmetic._verify_candidate",
        lambda *args, **kwargs: True,
    )

    result = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-37396",
        strategy_id="exact-small",
        budget={"max_cases": 1},
        seed=0,
    )

    assert result["outcome"] == "candidate_counterexample"
    assert result["candidate"]["internal_verification"]["status"] == "passed"
    assert "independent_verification" not in result["candidate"]
    assert result["stop_reason"] == "candidate_passed_internal_verification"


def test_campaign_stage_strategy_aliases_and_checkpoint_semantics() -> None:
    events: list[tuple[dict, int]] = []
    screen = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-416",
        strategy_id="screen-exact",
        budget=SMOKE_BUDGET,
        seed=7,
        progress=lambda cursor, checked: events.append((dict(cursor), checked)),
    )
    deep = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-416",
        strategy_id="deep-diversified",
        budget=SMOKE_BUDGET,
        seed=11,
        checkpoint=screen["checkpoint"],
    )

    assert screen["effective_strategy_id"] == "exact-small"
    assert deep["effective_strategy_id"] == "multistart"
    assert deep["checkpoint"]["launch_seed"] == 11
    assert deep["checkpoint"]["resume"]["mode"] == "block_cursor"
    assert deep["checkpoint"]["resume"]["checkpoint_received"]
    assert not deep["checkpoint"]["resume"]["intra_bound_cursor_restored"]
    assert events[-1][0]["phase"] == "complete"
    assert events[-1][1] == screen["checked_cases"]


def test_seed_reproducibility_and_multistart_diversification() -> None:
    deterministic_arguments = {
        "problem_id": "unsolvedmath-opg-37396",
        "strategy_id": "segmented-primes",
        "budget": {"max_q": 30, "max_cases": 10},
    }
    first = run_second_batch_arithmetic_search(
        **deterministic_arguments,
        seed=1,
    )
    second = run_second_batch_arithmetic_search(
        **deterministic_arguments,
        seed=999,
    )
    assert first["checkpoint"] == second["checkpoint"]

    multistart_arguments = {
        "problem_id": "unsolvedmath-kou-21.130",
        "strategy_id": "multistart",
        "budget": {
            "max_order": 9,
            "max_subset": 6,
            "max_cases": 10,
        },
    }
    launch_a = run_second_batch_arithmetic_search(
        **multistart_arguments,
        seed=7,
    )
    launch_a_repeat = run_second_batch_arithmetic_search(
        **multistart_arguments,
        seed=7,
    )
    launch_b = run_second_batch_arithmetic_search(
        **multistart_arguments,
        seed=8,
    )
    assert launch_a == launch_a_repeat
    assert launch_a["checkpoint"] != launch_b["checkpoint"]


def test_kou_21_113_counts_the_identity_as_a_p_element() -> None:
    if not (GAP_BINARY.exists() and GAP_ROOT.exists()):
        pytest.skip("isolated GAP/SmallGrp is not installed")

    result = run_second_batch_arithmetic_search(
        "unsolvedmath-kou-21.113",
        strategy_id="exact-small",
        budget={"max_order": 2, "max_cases": 10},
        seed=0,
    )

    assert result["candidate"] is None
    assert result["outcome"] == "no_counterexample_within_bound"
    assert result["checked_cases"] > 0


def test_kou_21_35_skips_nonprime_factors_at_the_trivial_group() -> None:
    if not (GAP_BINARY.exists() and GAP_ROOT.exists()):
        pytest.skip("isolated GAP/SmallGrp is not installed")

    result = run_second_batch_arithmetic_search(
        "unsolvedmath-kou-21.35",
        strategy_id="exact-small",
        budget={"max_order": 2, "max_cases": 10},
        seed=0,
    )

    assert result["candidate"] is None
    assert result["checked_cases"] > 0


@pytest.mark.parametrize(
    ("problem_id", "budget"),
    [
        (
            "unsolvedmath-kou-21.87",
            {"max_order": 16, "max_d": 3, "max_cases": 200},
        ),
        (
            "unsolvedmath-kou-21.88",
            {"max_order": 63, "max_cases": 1_000},
        ),
    ],
)
def test_new_smallgroups_searches_have_executable_smokes(
    problem_id: str,
    budget: dict,
) -> None:
    if not (GAP_BINARY.exists() and GAP_ROOT.exists()):
        pytest.skip("isolated GAP/SmallGrp is not installed")

    result = run_second_batch_arithmetic_search(
        problem_id,
        strategy_id="exact-small",
        budget=budget,
        seed=0,
    )

    assert result["candidate"] is None
    assert result["outcome"] == "no_counterexample_within_bound"
    assert result["checked_cases"] > 0


def test_kou_21_89_and_opg_511_have_executable_smokes() -> None:
    partition_result = run_second_batch_arithmetic_search(
        "unsolvedmath-kou-21.89",
        strategy_id="exact-small",
        budget={"max_n": 50, "max_cases": 11},
        seed=0,
    )
    bpsw_result = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-511",
        strategy_id="exact-small",
        budget={
            "start_n": 3,
            "max_n": 300,
            "segment_size": 100,
            "max_cases": 200,
        },
        seed=0,
    )

    assert partition_result["candidate"] is None
    assert partition_result["checked_cases"] == 11
    assert partition_result["outcome"] == "no_counterexample_within_bound"
    assert bpsw_result["candidate"] is None
    assert bpsw_result["checked_cases"] > 0
    assert bpsw_result["outcome"] == "no_counterexample_within_bound"


def test_gap_break_loop_is_never_reported_as_an_exhausted_search() -> None:
    if not (GAP_BINARY.exists() and GAP_ROOT.exists()):
        pytest.skip("isolated GAP/SmallGrp is not installed")

    with pytest.raises(RuntimeError, match="GAP exited"):
        _run_gap('Error("intentional protocol failure");')

    with pytest.raises(RuntimeError, match="DONE marker"):
        _parse_gap_result("CAND|2|1|2\n")


def test_gap_engine_errors_are_conservative_inconclusive(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_gap(script: str, *, timeout: int = 120) -> str:
        del script, timeout
        raise RuntimeError("synthetic GAP failure")

    monkeypatch.setattr(
        "amra.discovery.second_batch_arithmetic._run_gap",
        fail_gap,
    )
    result = run_second_batch_arithmetic_search(
        "unsolvedmath-kou-21.88",
        strategy_id="exact-small",
        budget={"max_order": 3, "max_cases": 3},
        seed=0,
    )

    assert result["outcome"] == "inconclusive"
    assert result["stop_reason"] == "search_engine_error"
    assert result["checkpoint"]["phase"] == "search_engine_error"
    assert not result["checkpoint"]["bounded_scope_exhausted"]


def test_kou_21_25_scans_a5_without_transitive_group_data() -> None:
    if not (GAP_BINARY.exists() and GAP_ROOT.exists()):
        pytest.skip("isolated GAP/SmallGrp is not installed")

    result = run_second_batch_arithmetic_search(
        "unsolvedmath-kou-21.25",
        strategy_id="simple-groups",
        budget={"max_order": 64, "max_cases": 1_000, "time_seconds": 10},
        seed=20_260_727,
    )

    assert result["candidate"] is None
    assert result["outcome"] == "no_counterexample_within_bound"
    assert result["checked_cases"] >= 613


def test_bpsw_deep_strategies_start_beyond_2_to_64_and_cover_distinct_families() -> None:
    by_id = {
        str(spec["problem_id"]): spec for spec in SECOND_BATCH_ARITHMETIC_SPECS
    }
    spec = by_id["unsolvedmath-opg-511"]
    assert spec["strategies"] == [
        "exact-small",
        "chernick-korselt",
        "remote-factor-layers",
    ]
    assert spec["deep_bounds"]["discovery_min_n"] > 2**64
    assert "Method A/Selfridge" in spec["model_contract"]["counterexample_condition"]

    structured = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-511",
        strategy_id="chernick-korselt",
        budget={
            "max_n": 10**23,
            "max_cases": 12,
            "structure_block_size": 4,
        },
        seed=0,
    )
    layered = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-511",
        strategy_id="remote-factor-layers",
        budget={
            "max_n": 10**23,
            "max_cases": 12,
            "remote_layers": 6,
            "remote_block_size": 4,
        },
        seed=0,
    )

    for result in (structured, layered):
        metrics = result["metrics"]
        assert result["checked_cases"] == 12
        assert metrics["known_exhaustive_lower_bound"] == 2**64
        assert metrics["min_tested_n"] > 2**64
        assert metrics["max_tested_n"] >= metrics["min_tested_n"]
        assert sum(metrics["family_sample_counts"].values()) == 12
    assert set(structured["metrics"]["family_sample_counts"]) == {
        "chernick_korselt_form"
    }
    assert structured["metrics"]["min_structure_parameter"] <= structured["metrics"][
        "max_structure_parameter"
    ]
    assert all(
        family.startswith("remote_semiprime_")
        for family in layered["metrics"]["family_sample_counts"]
    )
    assert sum(layered["metrics"]["layer_sample_counts"].values()) == 12


def test_bpsw_block_cursor_resumes_after_an_interrupted_progress_update() -> None:
    saved: dict = {}

    def interrupt_after_first_block(cursor: dict, checked: int) -> None:
        saved.clear()
        saved.update(cursor)
        if checked >= 4 and cursor.get("phase") == "searching":
            raise _SearchTimeLimit("synthetic interruption after durable save")

    interrupted = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-511",
        strategy_id="chernick-korselt",
        budget={
            "max_n": 10**23,
            "max_cases": 12,
            "structure_block_size": 4,
        },
        seed=0,
        progress=interrupt_after_first_block,
    )
    assert interrupted["stop_reason"] == "time_budget_exhausted"
    assert interrupted["checked_cases"] == 4
    first_next = interrupted["checkpoint"]["next_structure_parameter"]

    resumed = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-511",
        strategy_id="chernick-korselt",
        budget={
            "max_n": 10**23,
            "max_cases": 12,
            "structure_block_size": 4,
        },
        seed=0,
        checkpoint=saved,
    )
    assert resumed["checked_cases"] == 12
    assert resumed["checkpoint"]["resume"]["intra_bound_cursor_restored"]
    assert resumed["checkpoint"]["next_structure_parameter"] > first_next
    assert resumed["metrics"]["family_sample_counts"]["chernick_korselt_form"] == 12


def test_bpsw_remote_streams_generate_unique_candidates_and_resume() -> None:
    layers = _remote_bpsw_layers(2**64 + 1, 10**27, 24)
    streams = _remote_semiprime_streams(layers)
    assert len({int(stream["first"]) for stream in streams}) == len(streams)
    seconds = [int(stream["initial_second"]) for stream in streams]
    values: set[int] = set()
    for sample_index in range(100_000):
        stream_index = sample_index % len(streams)
        value = int(streams[stream_index]["first"]) * seconds[stream_index]
        assert value not in values
        values.add(value)
        seconds[stream_index] = int(nextprime(seconds[stream_index]))

    snapshots: list[tuple[dict, int]] = []
    first = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-511",
        strategy_id="remote-factor-layers",
        budget={
            "max_n": 10**23,
            "max_cases": 12,
            "remote_layers": 6,
            "remote_block_size": 4,
        },
        seed=0,
        progress=lambda cursor, checked: snapshots.append((cursor, checked)),
    )
    resumed = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-511",
        strategy_id="remote-factor-layers",
        budget={
            "max_n": 10**23,
            "max_cases": 24,
            "remote_layers": 6,
            "remote_block_size": 4,
        },
        seed=0,
        checkpoint=first["checkpoint"],
    )

    assert first["checked_cases"] == 12
    assert [
        (sum(cursor["stream_positions"]), checked)
        for cursor, checked in snapshots
        if cursor.get("phase") == "searching"
    ] == [(4, 4), (8, 8), (12, 12)]
    assert resumed["checked_cases"] == 24
    assert sum(resumed["checkpoint"]["stream_positions"]) == 24
    assert resumed["metrics"]["unique_candidate_generation"] is True
    assert resumed["metrics"]["duplicate_candidates_generated"] == 0
    assert resumed["checkpoint"]["resume"]["intra_bound_cursor_restored"]


@pytest.mark.parametrize(
    ("problem_id", "strategy_id", "budget", "metric_key"),
    [
        (
            "unsolvedmath-opg-563",
            "multistart",
            {
                "max_n": 15,
                "max_dimension": 4,
                "max_cases": 12,
                "memory_mb": 64,
            },
            "parameter_strata",
        ),
        (
            "unsolvedmath-opg-156",
            "multistart",
            {"max_n": 5, "max_cases": 20},
            "parameter_strata",
        ),
        (
            "unsolvedmath-opg-416",
            "multistart",
            {
                "minimum_runners": 14,
                "max_runners": 16,
                "max_speed": 30,
                "max_cases": 10,
            },
            "runner_counts",
        ),
        (
            "unsolvedmath-kou-21.115",
            "multistart",
            {"max_order": 20, "max_cosets": 6, "max_cases": 32},
            "moduli",
        ),
    ],
)
def test_multistart_searches_cross_parameter_strata_without_materializing_space(
    problem_id: str,
    strategy_id: str,
    budget: dict,
    metric_key: str,
) -> None:
    result = run_second_batch_arithmetic_search(
        problem_id,
        strategy_id=strategy_id,
        budget=budget,
        seed=20260727,
    )

    assert result["checked_cases"] == budget["max_cases"]
    assert len(result["metrics"][metric_key]) > 1
    if "next_case" in result["checkpoint"]:
        assert result["checkpoint"]["next_case"] == result["checked_cases"]
    else:
        assert sum(result["checkpoint"]["tuple_ranks"].values()) == result[
            "checked_cases"
        ]
    assert result["checkpoint"]["resume"]["mode"] == "block_cursor"


def test_large_bound_searches_are_streamed_post_frontier_and_resumable() -> None:
    wall = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-822",
        strategy_id="post-frontier-prime-stream",
        budget={
            "start_prime": 200_000_000_000_000_003,
            "max_prime": 100_000_000_000_000_000_000,
            "known_computational_lower_bound": 146_000_000_000_000_000,
            "checkpoint_block_size": 2,
            "max_cases": 4,
        },
        seed=0,
    )
    lehmer = run_second_batch_arithmetic_search(
        "unsolvedmath-nt-035",
        strategy_id="structural-post-frontier",
        budget={
            "minimum_n": 10**30 + 1,
            "minimum_prime_factors": 15,
            "max_cases": 8,
        },
        seed=0,
    )
    hardy_littlewood = run_second_batch_arithmetic_search(
        "unsolvedmath-hl-b",
        strategy_id="gap-targeted",
        budget={"max_xy": 1_000_000, "max_cases": 8},
        seed=0,
    )

    assert wall["checked_cases"] == 4
    assert wall["metrics"]["min_tested_prime"] > 146_000_000_000_000_000
    assert wall["metrics"]["coverage_kind"] == "post_frontier_streamed_primes"
    assert lehmer["checked_cases"] == 8
    assert lehmer["metrics"]["subsets_enumerated"] == 8
    assert lehmer["metrics"]["korselt_filter_exact"]
    assert min(lehmer["metrics"]["factor_counts"]) >= 15
    assert hardy_littlewood["checked_cases"] == 8
    assert hardy_littlewood["metrics"]["max_x_plus_y"] > 1_000


def test_lehmer_stream_reaches_a_known_korselt_compatible_post_frontier_case() -> None:
    case_index = 175_871 * 6
    checkpoint = {
        "problem_id": "unsolvedmath-nt-035",
        "effective_strategy_id": "structural-post-frontier",
        "checked_cases": case_index,
        "metrics": {},
        "next_case": case_index,
    }

    result = run_second_batch_arithmetic_search(
        "unsolvedmath-nt-035",
        strategy_id="structural-post-frontier",
        budget={
            "minimum_n": 10**30 + 1,
            "minimum_prime_factors": 15,
            "subset_block_size": 1,
            "max_cases": case_index + 1,
        },
        seed=0,
        checkpoint=checkpoint,
    )

    assert result["checked_cases"] == case_index + 1
    assert result["metrics"]["korselt_candidates"] == 1
    assert result["metrics"]["post_frontier_candidates"] == 1
    assert result["metrics"]["quotient_feasible_candidates"] == 1
    assert result["metrics"]["lehmer_tested"] == 1
    assert result["metrics"]["min_tested_n"] > 10**30
    assert result["candidate"] is None


def test_prime_sieve_uses_compact_storage_and_semiprime_searches_checkpoint() -> None:
    flags, primes = _prime_sieve(1_000_000)
    compact_bytes = len(flags) + len(primes) * primes.itemsize

    assert isinstance(flags, bytearray)
    assert primes.typecode == "I"
    assert compact_bytes < 2_000_000

    for problem_id in ("unsolvedmath-nt-059", "unsolvedmath-opg-37404"):
        first = run_second_batch_arithmetic_search(
            problem_id,
            strategy_id="segmented-primes",
            budget={
                "max_n": 10_000,
                "n_block_size": 4,
                "max_cases": 8,
            },
            seed=0,
        )
        resumed = run_second_batch_arithmetic_search(
            problem_id,
            strategy_id="segmented-primes",
            budget={
                "max_n": 10_000,
                "n_block_size": 4,
                "max_cases": 12,
            },
            seed=0,
            checkpoint=first["checkpoint"],
        )

        assert first["checkpoint"]["next_n"] < resumed["checkpoint"]["next_n"]
        assert resumed["checked_cases"] == 12
        assert resumed["metrics"]["blocks_completed"] == 3
        assert resumed["checkpoint"]["resume"]["intra_bound_cursor_restored"]
        assert (
            resumed["metrics"]["prime_flag_bytes"]
            + resumed["metrics"]["semiprime_flag_bytes"]
            + resumed["metrics"]["prime_storage_bytes"]
            < 1_000_000_000
        )


def test_segmented_and_stratified_arithmetic_searches_resume_with_exact_metadata() -> None:
    primitive = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-37396",
        strategy_id="segmented-primes",
        budget={
            "max_q": 100_000,
            "segment_size": 1_024,
            "prime_block_size": 4,
            "max_cases": 8,
        },
        seed=0,
    )
    primitive_resumed = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-37396",
        strategy_id="segmented-primes",
        budget={
            "max_q": 100_000,
            "segment_size": 1_024,
            "prime_block_size": 4,
            "max_cases": 12,
        },
        seed=0,
        checkpoint=primitive["checkpoint"],
    )
    quartic = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-791",
        strategy_id="integer-root-targeted",
        budget={"root_height": 100, "max_cases": 10},
        seed=0,
    )
    hardy_littlewood = run_second_batch_arithmetic_search(
        "unsolvedmath-hl-b",
        strategy_id="gap-targeted",
        budget={
            "max_xy": 1_000_000,
            "minimum_x_y_ratio": 128,
            "max_cases": 10,
        },
        seed=0,
    )

    assert primitive_resumed["checked_cases"] == 12
    assert primitive_resumed["checkpoint"]["next_q"] > primitive["checkpoint"]["next_q"]
    assert primitive_resumed["metrics"]["coverage_kind"] == "segmented_prime_q_stream"
    assert primitive_resumed["checkpoint"]["resume"]["intra_bound_cursor_restored"]
    assert quartic["metrics"]["duplicate_canonical_shapes"] == 0
    assert quartic["metrics"]["canonical_shapes_checked"] == 10
    assert quartic["metrics"]["affine_normalization"] == (
        "subtract_min_then_divide_gcd"
    )
    assert hardy_littlewood["metrics"]["minimum_x_to_y_seen"] >= 128
    assert hardy_littlewood["metrics"]["duplicate_pairs"] == 0
    assert hardy_littlewood["metrics"]["prime_count_method"] == "exact_sympy_primepi"


def test_targeted_davenport_runner_and_covering_searches_report_honest_scope() -> None:
    davenport = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-563",
        strategy_id="multistart",
        budget={
            "max_n": 15,
            "max_dimension": 4,
            "memory_mb": 64,
            "max_cases": 12,
        },
        seed=5,
    )
    runners = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-416",
        strategy_id="multistart",
        budget={
            "minimum_runners": 14,
            "max_runners": 16,
            "max_speed": 30,
            "max_cases": 3,
        },
        seed=5,
    )
    covering = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-491",
        strategy_id="cover-targeted",
        budget={
            "max_modulus": 999,
            "max_moduli": 10,
            "max_period": 100_000,
            "max_cases": 2,
        },
        seed=5,
    )

    assert davenport["metrics"]["target_moduli"] == [6, 10, 12, 14, 15]
    assert all(
        modulus in {6, 10, 12, 14, 15} and dimension >= 3
        for modulus, dimension in davenport["metrics"]["parameter_strata"]
    )
    assert davenport["metrics"]["iid_sequence_generation"] is False
    assert runners["metrics"]["runner_counts"] == [14, 15, 16]
    assert runners["metrics"]["runner_predicates_checked"] == 45
    assert runners["metrics"]["duplicate_canonical_tuples"] == 0
    assert covering["checked_cases"] == 2
    assert covering["metrics"]["duplicate_modulus_sets"] == 0
    assert covering["metrics"]["candidate_check"] == (
        "exact_complete_lcm_period_bitset"
    )
    assert covering["metrics"]["search_completeness"] == (
        "multistart_coordinate_descent_not_exhaustive"
    )


def test_power_completion_searches_use_large_bounds_without_large_tables() -> None:
    sextic = run_second_batch_arithmetic_search(
        "unsolvedmath-opg-508",
        strategy_id="meet-in-the-middle",
        budget={"max_base": 100_000, "max_cases": 16},
        seed=0,
    )
    equal_sums = run_second_batch_arithmetic_search(
        "unsolvedmath-nt-058",
        strategy_id="meet-in-the-middle",
        budget={"max_power": 8, "max_base": 100_000, "max_cases": 32},
        seed=0,
    )

    assert sextic["checked_cases"] == 16
    assert sextic["metrics"]["max_target_base"] > 8
    assert sextic["checkpoint"]["next_case"] == 16
    assert equal_sums["checked_cases"] == 32
    assert max(equal_sums["metrics"]["powers"]) > 5
    assert equal_sums["checkpoint"]["next_case"] == 32


def test_partition_block_cursor_rebuilds_state_and_resumes_at_next_n() -> None:
    first = run_second_batch_arithmetic_search(
        "unsolvedmath-kou-21.89",
        strategy_id="partition-recurrence",
        budget={"max_n": 80, "max_cases": 8, "n_block_size": 4},
        seed=0,
    )
    assert first["checked_cases"] == 8
    assert first["checkpoint"]["next_n"] == 48

    resumed = run_second_batch_arithmetic_search(
        "unsolvedmath-kou-21.89",
        strategy_id="partition-recurrence",
        budget={"max_n": 80, "max_cases": 16, "n_block_size": 4},
        seed=0,
        checkpoint=first["checkpoint"],
    )
    assert resumed["checked_cases"] == 16
    assert resumed["checkpoint"]["next_n"] == 56
    assert resumed["metrics"]["min_tested_n"] == 40
    assert resumed["metrics"]["max_tested_n"] == 55
    assert resumed["metrics"]["replayed_partition_terms"] == 39 + 47
    assert resumed["checkpoint"]["resume"]["intra_bound_cursor_restored"]


def test_targeted_group_searches_filter_catalog_before_expensive_predicates() -> None:
    if not (GAP_BINARY.exists() and GAP_ROOT.exists()):
        pytest.skip("isolated GAP/SmallGrp is not installed")

    nonsolvable = run_second_batch_arithmetic_search(
        "unsolvedmath-kou-21.87",
        strategy_id="smallgroups-targeted",
        budget={
            "max_order": 120,
            "max_d": 8,
            "max_cases": 1,
            "group_chunk_size": 1,
        },
        seed=0,
    )
    commuting = run_second_batch_arithmetic_search(
        "unsolvedmath-kou-21.88",
        strategy_id="odd-smallgroups",
        budget={
            "max_order": 2_000,
            "max_cases": 100,
            "group_chunk_size": 8,
        },
        seed=0,
    )

    assert nonsolvable["checked_cases"] == 1
    assert nonsolvable["metrics"]["first_target_group_id"] == [60, 5]
    assert nonsolvable["metrics"]["a5_reached"]
    assert nonsolvable["metrics"]["solvable_groups_constructed"] == 0
    assert nonsolvable["checkpoint"]["next_order"] == 120
    resumed_group = run_second_batch_arithmetic_search(
        "unsolvedmath-kou-21.87",
        strategy_id="smallgroups-targeted",
        budget={
            "max_order": 120,
            "max_d": 8,
            "max_cases": 2,
            "group_chunk_size": 1,
        },
        seed=0,
        checkpoint=nonsolvable["checkpoint"],
    )
    assert resumed_group["checked_cases"] == 2
    assert resumed_group["metrics"]["last_group_id"] == [120, 5]
    assert resumed_group["checkpoint"]["resume"]["intra_bound_cursor_restored"]
    assert commuting["checked_cases"] == 72
    assert commuting["metrics"]["nonabelian_groups_checked"] == 10
    assert commuting["metrics"]["unavailable_orders"] == [
        1071,
        1275,
        1377,
        1683,
        1785,
        1989,
    ]


@pytest.mark.parametrize(
    ("problem_id", "strategy_id", "budget", "time_seconds"),
    [
        (
            "unsolvedmath-kou-21.87",
            "smallgroups-targeted",
            {
                "max_order": 512,
                "max_d": 8,
                "max_cases": 1_000_000_000,
                "group_chunk_size": 1,
            },
            2,
        ),
        (
            "unsolvedmath-kou-21.88",
            "odd-smallgroups",
            {
                "max_order": 2_000,
                "max_cases": 1_000_000_000,
                "group_chunk_size": 1,
            },
            2,
        ),
        (
            "unsolvedmath-kou-21.89",
            "partition-recurrence",
            {
                "max_n": 1_000_000,
                "max_cases": 1_000_000_000,
                "n_block_size": 4,
            },
            0.05,
        ),
        (
            "unsolvedmath-opg-511",
            "chernick-korselt",
            {
                "max_n": 10**27,
                "structure_block_size": 32,
                "max_cases": 1_000_000_000,
            },
            0.05,
        ),
    ],
)
def test_time_budget_interrupts_python_and_gap_searches(
    problem_id: str,
    strategy_id: str,
    budget: dict,
    time_seconds: float,
) -> None:
    if problem_id in {
        "unsolvedmath-kou-21.87",
        "unsolvedmath-kou-21.88",
    } and not (GAP_BINARY.exists() and GAP_ROOT.exists()):
        pytest.skip("isolated GAP/SmallGrp is not installed")
    started = time.monotonic()

    result = run_second_batch_arithmetic_search(
        problem_id,
        strategy_id=strategy_id,
        budget={**budget, "time_seconds": time_seconds},
        seed=0,
    )

    assert time.monotonic() - started < time_seconds + 3
    assert result["outcome"] == "inconclusive"
    assert result["stop_reason"] == "time_budget_exhausted"
    assert result["checkpoint"]["phase"] == "time_budget_exhausted"
    assert not result["checkpoint"]["bounded_scope_exhausted"]
    assert result["checked_cases"] > 0
    assert result["checkpoint"]["resume"]["mode"] == "block_cursor"
