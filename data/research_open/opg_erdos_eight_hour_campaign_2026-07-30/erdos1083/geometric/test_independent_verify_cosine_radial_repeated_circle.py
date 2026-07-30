from independent_verify_cosine_radial_repeated_circle import (
    audit,
    direct_coordinate_check,
    normal_form_certificate,
    saturation_ledger,
)


def test_normal_form_and_sharp_symmetric_labels():
    transverse = (-7, -5, -3, -1, 1, 3, 5, 7)
    result = normal_form_certificate(transverse)
    assert result["multiplicity"] == 8
    assert result["distinct_plane_slopes"] == 8
    assert result["ordinary_radii"] == 4
    assert result["distance_labels"] == 4
    assert result["target_distances"] == 7
    assert result["common_circle_radius_squared"] == 16


def test_exact_three_part_distance_ledger():
    result = saturation_ledger(9, 4)
    assert result["source_source_distances"] == 4
    assert result["target_target_distances"] == 7
    assert result["cross_distances"] == 4
    assert result["distance_union_upper_bound"] == 15
    assert result["cross_representations"] == 72
    assert result["target_rays"] == 8
    assert result["full_configuration_rays"] == 9


def test_direct_full_coordinate_bound():
    actual = direct_coordinate_check(11, 5)
    assert actual <= 11 // 2 + 3 * 5 - 1


def test_full_independent_audit():
    result = audit()
    assert result["status"] == "PASS"
    assert result["normal_form_checks"] == 11
    assert result["full_coordinate_checks"] == 78
