from verify_809_a_oriented_taxonomy import random_guard, sharp_local_guard


def test_sharp_local_guard() -> None:
    result = sharp_local_guard()
    assert result["bound_attained"]
    assert result["outer_codegree"] == 2


def test_random_guard() -> None:
    result = random_guard()
    assert result["random_graphs"] == 400
    assert result["distance_two_orientations"] > 0
    assert result["distance_three_clean_orientations"] > 0
    assert result["distance_three_transversal_orientations"] > 0
