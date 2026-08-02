"""Regression test for the frozen multi-promotion no-borrow atlas."""

from verify_multi_promotion_no_borrow import finite_atlas, shallow_two_cap_base


def test_frozen_atlas() -> None:
    result = finite_atlas()
    assert result["checked_states"] == 85_278
    assert result["states_by_promotions"] == {
        2: 36_288,
        3: 33_620,
        4: 14_921,
        5: 449,
    }
    assert result["gamma4_nonpositive_states"] == 0
    assert result["minimum_gamma4"] == 69
    assert result["minimum_state"] == {
        "q": 16,
        "promotions": 2,
        "r": 0,
        "u": 3,
        "b": 37,
        "h": 256,
        "gamma3": -408,
        "x0": 14,
        "y0": 272,
    }
    assert result["rank3_cap_gap"] == [1, 34]
    assert result["conditional_lower_bounds"]["uncovered_states"] == 31_935
    assert result["uncovered_templates"] == {
        "forward_boundary: beta>=alpha and D>=E": {
            "count": 120,
            "by_promotions": {2: 120},
            "cap_gap_range_by_promotions": {2: [1, 1]},
        },
        "reverse_remainders: beta<alpha and D<E": {
            "count": 31_815,
            "by_promotions": {2: 15_463, 3: 12_418, 4: 3_881, 5: 53},
            "cap_gap_range_by_promotions": {
                2: [2, 14],
                3: [3, 22],
                4: [5, 28],
                5: [12, 28],
            },
        },
    }


def test_shallow_two_cap_finite_base() -> None:
    result = shallow_two_cap_base()
    assert result["checked_states"] == 20
    assert result["minimum"] == {
        "q": 39,
        "u": 13,
        "b": 55,
        "h": 327,
        "gamma3": -590,
        "delta": 3,
        "beta": 151,
        "gamma4": 186,
    }
