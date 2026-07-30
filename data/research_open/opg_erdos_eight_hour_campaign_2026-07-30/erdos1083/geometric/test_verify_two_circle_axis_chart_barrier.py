from verify_two_circle_axis_chart_barrier import (
    audit,
    concentric_two_chart_model,
)


def test_regular_polygon_ap_two_chart_barrier():
    for order in (3, 4, 6, 8):
        result = concentric_two_chart_model(order, 5)
        assert result["chart_count"] == 2
        assert result["distinct_circle_radii"] == 2
        assert result["multiplicity_per_chart"] == 10
        assert result["cross_labels_per_chart"] == 5
        assert (
            result["distinct_squared_distances"]
            <= result["proved_linear_upper_bound"]
        )


def test_full_two_chart_audit():
    result = audit()
    assert result["status"] == "PASS"
    assert len(result["cases"]) == 16
