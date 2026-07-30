from verify_dim11_sharp_noncommuting_cubes import build_audit


def test_dimension_eleven_sharp_witness() -> None:
    audit = build_audit()
    assert audit["filtration_profile"] == [2, 2, 2, 2, 2, 1]
    assert audit["raw_cube_count"] == 171
    assert audit["zero_A3_cube_count"] == 9
    assert audit["leading_A3_image_size"] == 7
    assert audit["leading_A3_fibre_sizes"] == [
        9,
        27,
        27,
        27,
        27,
        27,
        27,
    ]
    assert audit["raw_cube_set_closed"] is False
    assert audit["wilson_counterexample"] is False
