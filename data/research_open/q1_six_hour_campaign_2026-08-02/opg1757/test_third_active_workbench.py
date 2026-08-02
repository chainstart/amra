from third_active_workbench import (
    first_nonpositive,
    one_plus_z_multiplicity,
    reduced_third_row,
    stable_even_reduced_formula,
    stable_odd_reduced_formula,
    third_active_row,
    transport_remainder,
    verify_symbolic_maximal_factor_certificates,
)


def test_stable_reductions_are_exact() -> None:
    for m in range(2, 13):
        assert reduced_third_row("odd", m) == stable_odd_reduced_formula(m + 6)
    for m in range(3, 13):
        assert reduced_third_row("even", m) == stable_even_reduced_formula(m + 6)


def test_exact_finite_rows_have_no_nonpositive_coefficient() -> None:
    for m in range(21):
        assert first_nonpositive(third_active_row("odd", m)) is None
    for m in range(1, 21):
        assert first_nonpositive(third_active_row("even", m)) is None


def test_maximal_common_one_plus_z_factors() -> None:
    for m in range(21):
        expected = max(0, 2 * m - 4)
        assert one_plus_z_multiplicity(third_active_row("odd", m)) == expected
    for m in range(1, 21):
        expected = max(0, 2 * m - 6)
        assert one_plus_z_multiplicity(third_active_row("even", m)) == expected


def test_candidate_transports_survive_finite_falsification() -> None:
    for s in range(8, 25):
        assert first_nonpositive(
            transport_remainder("odd", s), strict=True
        ) is None
    for s in range(9, 25):
        assert first_nonpositive(
            transport_remainder("even", s), strict=True
        ) is None


def test_symbolic_maximal_factor_certificates() -> None:
    k6_value, k7_value = verify_symbolic_maximal_factor_certificates()
    assert k6_value != 0
    assert k7_value != 0


def test_exact_positive_bases() -> None:
    assert third_active_row("odd", 0) == [8, 16, 16]
    assert third_active_row("odd", 1) == [
        24044, 94336, 170092, 175968, 109396, 38752, 6196
    ]
    assert reduced_third_row("odd", 2)[-1] == 530304
    assert third_active_row("even", 1) == [360, 1184, 1872, 1392, 464]
    assert third_active_row("even", 2)[-1] == 143076
    assert reduced_third_row("even", 3)[-1] == 16350372
