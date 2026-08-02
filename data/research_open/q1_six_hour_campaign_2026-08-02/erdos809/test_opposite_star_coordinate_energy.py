from verify_opposite_star_coordinate_energy import run_exhaustive


def test_exhaustive_coordinate_energy_guards():
    result = run_exhaustive(max_n=5)
    assert result["status"] == "PASS"
    assert result["star_systems"] > 0
