from __future__ import annotations

from collections import Counter

import pytest

from amra.discovery import opg_uniform_forest_extensions as extensions
from amra.discovery.opg_coloring_search import decode_graph6
from amra.discovery.opg_uniform_forest_extensions import (
    EXPECTED_LABELLED_EXTENSIONS,
    encode_simple_graph6,
    evaluate_inherited_pair,
    expected_labelled_extension_count,
    iter_labelled_vertex_extensions,
    search_labelled_vertex_extensions,
)
from amra.discovery.opg_uniform_forest_search import (
    ForestEvaluationBudgetExceeded,
    ForestStatistics,
)


def _path_nine_graph6() -> str:
    return encode_simple_graph6(
        9,
        tuple((vertex, vertex + 1) for vertex in range(8)),
    )


def _path_ten_graph6() -> str:
    return encode_simple_graph6(
        10,
        tuple((vertex, vertex + 1) for vertex in range(9)),
    )


def _path_eleven_graph6() -> str:
    return encode_simple_graph6(
        11,
        tuple((vertex, vertex + 1) for vertex in range(10)),
    )


def test_fixed_seed_enumeration_has_all_372_stable_labels() -> None:
    seed = _path_nine_graph6()
    labelled = list(iter_labelled_vertex_extensions(seed))

    assert len(labelled) == EXPECTED_LABELLED_EXTENSIONS == 372
    assert [item.label_index for item in labelled] == list(range(372))
    assert Counter(len(item.neighbours) for item in labelled) == {
        2: 36,
        3: 84,
        4: 126,
        5: 126,
    }
    assert labelled[0].neighbours == (0, 1)
    assert labelled[-1].neighbours == (4, 5, 6, 7, 8)
    assert len({item.graph.encoding for item in labelled}) == 372
    for item in labelled:
        replay = decode_graph6(item.graph.encoding)
        assert replay.vertex_count == 10
        assert set(replay.edges) == set(item.graph.edges)


def test_order_ten_seed_has_627_roundtrippable_extensions() -> None:
    seed = _path_ten_graph6()
    seed_edge_count = len(decode_graph6(seed).edges)
    labelled = list(iter_labelled_vertex_extensions(seed))

    assert expected_labelled_extension_count(10) == 627
    assert len(labelled) == 627
    assert [item.label_index for item in labelled] == list(range(627))
    assert Counter(len(item.neighbours) for item in labelled) == {
        2: 45,
        3: 120,
        4: 210,
        5: 252,
    }
    assert labelled[0].neighbours == (0, 1)
    assert labelled[-1].neighbours == (5, 6, 7, 8, 9)
    assert len({item.graph.encoding for item in labelled}) == 627
    for item in labelled:
        replay = decode_graph6(item.graph.encoding)
        assert replay.vertex_count == 11
        assert set(replay.edges) == set(item.graph.edges)
        assert all(
            right == 10
            for _, right in item.graph.edges[seed_edge_count:]
        )
    payload = search_labelled_vertex_extensions(
        seed,
        (0, 1),
        wall_seconds=0.0,
    ).as_dict()
    assert payload["seed_order"] == 10
    label_scope = payload["label_enumeration"]
    assert isinstance(label_scope, dict)
    assert label_scope["extension_vertex"] == 10
    assert label_scope["expected_labelled_extensions"] == 627
    assert label_scope["label_index_range"] == [0, 626]


def test_order_eleven_seed_has_1012_roundtrippable_extensions() -> None:
    seed = _path_eleven_graph6()
    seed_edge_count = len(decode_graph6(seed).edges)
    labelled = list(iter_labelled_vertex_extensions(seed))

    assert expected_labelled_extension_count(11) == 1012
    assert len(labelled) == 1012
    assert [item.label_index for item in labelled] == list(range(1012))
    assert Counter(len(item.neighbours) for item in labelled) == {
        2: 55,
        3: 165,
        4: 330,
        5: 462,
    }
    assert labelled[0].neighbours == (0, 1)
    assert labelled[-1].neighbours == (6, 7, 8, 9, 10)
    assert len({item.graph.encoding for item in labelled}) == 1012
    for item in labelled:
        replay = decode_graph6(item.graph.encoding)
        assert replay.vertex_count == 12
        assert set(replay.edges) == set(item.graph.edges)
        assert all(
            right == 11
            for _, right in item.graph.edges[seed_edge_count:]
        )
    payload = search_labelled_vertex_extensions(
        seed,
        (0, 1),
        wall_seconds=0.0,
    ).as_dict()
    assert payload["seed_order"] == 11
    label_scope = payload["label_enumeration"]
    assert isinstance(label_scope, dict)
    assert label_scope["extension_vertex"] == 11
    assert label_scope["expected_labelled_extensions"] == 1012
    assert label_scope["label_index_range"] == [0, 1011]


def test_inherited_pair_screen_matches_exact_cycle_ten_counts() -> None:
    extension = next(
        item
        for item in iter_labelled_vertex_extensions(_path_nine_graph6())
        if item.neighbours == (0, 8)
    )
    # This extension is C_10.  Every proper edge subset is a forest.
    evaluation = evaluate_inherited_pair(
        extension,
        (0, 1),
        timeout_seconds=5.0,
        max_states=100_000,
    )

    assert (
        evaluation.forest_count,
        evaluation.forest_count_e,
        evaluation.forest_count_f,
        evaluation.forest_count_ef,
    ) == (1023, 511, 511, 255)
    assert evaluation.margin == 256
    assert not evaluation.violates_negative_association


def test_search_ranks_exact_ratios_without_full_pair_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class ScreeningCounter:
        statistics_calls = 0
        state_budgets: list[int] = []

        def __init__(
            self,
            _vertex_count: int,
            edges,
            *,
            timeout_seconds: float,
            max_states: int,
        ) -> None:
            assert timeout_seconds > 0
            self.edges = tuple(edges)
            self.neighbours = tuple(
                left for left, right in self.edges if right == 9
            )
            self.states = 4
            self.elapsed_seconds = 0.0
            self.state_budgets.append(max_states)

        def count_after_contracting(self, indexes=()) -> int:
            indexes = tuple(indexes)
            if not indexes:
                return 10
            if len(indexes) == 1:
                return 10
            return 1 + sum(1 << vertex for vertex in self.neighbours) % 9

        def statistics(self) -> ForestStatistics:
            type(self).statistics_calls += 1
            raise AssertionError("nonviolating screens need no all-pair work")

    monkeypatch.setattr(
        extensions,
        "GraphicMatroidForestCounter",
        ScreeningCounter,
    )
    seed = _path_nine_graph6()
    result = search_labelled_vertex_extensions(
        seed,
        (0, 1),
        top_k=3,
        per_graph_seconds=1.0,
        wall_seconds=5.0,
        max_states=1234,
    )

    expected = []
    for item in iter_labelled_vertex_extensions(seed):
        value = 1 + sum(1 << vertex for vertex in item.neighbours) % 9
        expected.append((value, item.label_index))
    expected.sort(key=lambda value: (-value[0], value[1]))

    assert result.status == "complete"
    assert result.attempted == result.evaluated == 372
    assert [item.label_index for item in result.top_evaluations] == [
        label for _, label in expected[:3]
    ]
    assert ScreeningCounter.statistics_calls == 0
    assert set(ScreeningCounter.state_budgets) == {1234}
    payload = result.as_dict()
    assert payload["label_enumeration"] == {
        "kind": "fixed-seed-labelled-one-vertex-extension",
        "extension_vertex": 9,
        "neighbour_subset_size_range": [2, 5],
        "expected_labelled_extensions": 372,
        "label_index_range": [0, 371],
        "isomorphism_deduplicated": False,
        "possible_isomorphic_duplicate_label_range": [0, 371],
        "nonisomorphic_exhaustion_claimed": False,
    }
    assert payload["pair_screening"] == {
        "screened_before_trigger": "inherited edge pair only",
        "full_pair_trigger": "inherited left_product > right_product",
        "all_pairs_checked_for_nontriggering_extensions": False,
        "counterexample_exhaustion_claimed": False,
    }


def test_true_inherited_ratio_triggers_full_pair_pending_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class ViolatingCounter:
        statistics_calls = 0

        def __init__(
            self,
            _vertex_count: int,
            edges,
            *,
            timeout_seconds: float,
            max_states: int,
        ) -> None:
            assert timeout_seconds > 0
            assert max_states == 999
            self.edges = tuple(edges)
            self.states = 7
            self.elapsed_seconds = 0.0

        def count_after_contracting(self, indexes=()) -> int:
            indexes = tuple(indexes)
            if not indexes:
                return 10
            if len(indexes) == 1:
                return 4
            return 2

        def statistics(self) -> ForestStatistics:
            type(self).statistics_calls += 1
            edge_count = len(self.edges)
            pair_counts = [
                [0] * edge_count for _ in range(edge_count)
            ]
            for first in range(edge_count):
                for second in range(first + 1, edge_count):
                    pair_counts[first][second] = 1
                    pair_counts[second][first] = 1
            pair_counts[0][1] = pair_counts[1][0] = 2
            return ForestStatistics(
                10,
                (4,) * edge_count,
                tuple(tuple(row) for row in pair_counts),
                self.states,
                self.elapsed_seconds,
            )

    monkeypatch.setattr(
        extensions,
        "GraphicMatroidForestCounter",
        ViolatingCounter,
    )
    result = search_labelled_vertex_extensions(
        _path_nine_graph6(),
        (0, 1),
        top_k=2,
        per_graph_seconds=1.0,
        wall_seconds=5.0,
        max_states=999,
    )

    assert result.status == "candidate_pending_independent_verification"
    assert result.attempted == result.evaluated == 1
    assert result.candidate is not None
    assert (
        result.candidate["verification_status"]
        == "pending_independent_verification"
    )
    assert result.candidate["strongest_full_pair"]["edge_indexes"] == [0, 1]
    assert result.candidate["strongest_full_pair"]["margin"] == -4
    assert ViolatingCounter.statistics_calls == 1


def test_full_pair_timeout_is_not_promoted_to_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FullTimeoutCounter:
        def __init__(
            self,
            _vertex_count: int,
            edges,
            *,
            timeout_seconds: float,
            max_states: int,
        ) -> None:
            self.edges = tuple(edges)
            self.states = 1
            self.elapsed_seconds = 0.0

        def count_after_contracting(self, indexes=()) -> int:
            indexes = tuple(indexes)
            if not indexes:
                return 10
            if len(indexes) == 1:
                return 4
            return 2

        def statistics(self) -> ForestStatistics:
            raise ForestEvaluationBudgetExceeded("full replay timed out")

    monkeypatch.setattr(
        extensions,
        "GraphicMatroidForestCounter",
        FullTimeoutCounter,
    )
    result = search_labelled_vertex_extensions(
        _path_nine_graph6(),
        (0, 1),
        per_graph_seconds=1.0,
        wall_seconds=5.0,
        max_states=999,
    )

    assert result.status == (
        "inherited_violation_pending_full_pair_recheck"
    )
    assert result.candidate is None
    assert result.pending_inherited_violation is not None


def test_zero_wall_budget_starts_no_counter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class UnexpectedCounter:
        def __init__(self, *args, **kwargs) -> None:
            raise AssertionError("zero wall budget must start no counter")

    monkeypatch.setattr(
        extensions,
        "GraphicMatroidForestCounter",
        UnexpectedCounter,
    )
    result = search_labelled_vertex_extensions(
        _path_nine_graph6(),
        (0, 1),
        wall_seconds=0.0,
    )
    assert result.status == "paused_wall_budget"
    assert result.attempted == result.evaluated == 0
    assert result.next_label_index == 0


@pytest.mark.parametrize(
    ("pair", "kwargs", "message"),
    (
        ((0, 0), {}, "distinct"),
        ((0, 99), {}, "outside"),
        ((0, 1), {"top_k": -1}, "top_k"),
        ((0, 1), {"per_graph_seconds": 0.0}, "per_graph_seconds"),
        ((0, 1), {"wall_seconds": float("nan")}, "wall_seconds"),
        ((0, 1), {"max_states": 0}, "max_states"),
    ),
)
def test_search_validates_scope_and_budgets(
    pair: tuple[int, int],
    kwargs: dict[str, object],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        search_labelled_vertex_extensions(
            _path_nine_graph6(),
            pair,
            **kwargs,
        )
