from independent_verify_two_circle_axis_chart_barrier import (
    audit,
    general_formula_residuals,
    k_chart_ledger,
    two_chart_ledger,
)


def test_general_cross_formulas_against_direct_coordinates():
    residuals = general_formula_residuals(
        alpha1=0.23,
        alpha2=1.17,
        A1=3.4,
        A2=-0.8,
        w1=0.7,
        w2=-1.1,
        r1=0.6,
        r2=1.9,
        phi=-0.4,
        psi=0.91,
        y=1.3,
        z=-0.2,
    )
    assert max(residuals) < 1e-10


def test_complete_two_chart_category_ledger():
    record = two_chart_ledger(9, 4)
    assert record["within_circle_1"] == 4
    assert record["within_circle_2"] == 4
    assert record["between_circles"] == 5
    assert record["axis_axis"] == 7
    assert record["circle_1_axis"] == 4
    assert record["circle_2_axis"] == 4
    assert record["representations"] == 4 * 9 * 4
    assert record["multiplicity_per_chart"] == 8
    assert record["distinct_distances"] <= record["upper_bound"]


def test_fixed_k_explicit_extension():
    for chart_count in range(1, 7):
        record = k_chart_ledger(8, 3, chart_count)
        assert record["representations"] == 2 * chart_count * 3 * 8
        assert record["within_source_blocks"] == 4 * chart_count
        assert record["between_source_blocks"] == 5 * (
            chart_count * (chart_count - 1) // 2
        )
        assert record["axis_axis"] == 5
        assert record["circle_axis_blocks"] == 3 * chart_count
        assert record["distinct_distances"] <= record["explicit_upper_bound"]


def test_full_independent_audit():
    result = audit()
    assert result["status"] == "PASS"
    assert result["general_formula_cases"] == 3
    assert result["two_chart_cases"] == 60
    assert result["k_chart_cases"] == 40
