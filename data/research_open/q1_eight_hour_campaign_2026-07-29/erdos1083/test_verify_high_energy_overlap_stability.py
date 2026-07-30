from fractions import Fraction

from verify_high_energy_overlap_stability import (
    adversarial_search,
    divisor_count,
    energy_certificate,
    verify_divisor_bound,
)


def test_second_moment_identity_and_bounds() -> None:
    examples = (
        ((0, 1, 2),) * 4,
        ((0, 1, 4), (0, 3), (2, 7, 9, 12), (0, 10, 20)),
        ((0, 100), (1, 30, 80), (0, 7, 90), (4, 11)),
    )
    for height_sets in examples:
        certificate = energy_certificate(height_sets)
        assert certificate.second_moment == (
            certificate.incidence_mass
            + certificate.ordered_cross_correlation
        )
        assert certificate.line_count >= certificate.cauchy_lower_bound
        assert certificate.incidence_mass >= (
            certificate.elementary_incidence_lower_bound
        )
        assert verify_divisor_bound(height_sets)


def test_divisor_count() -> None:
    expected = {
        1: 1,
        2: 2,
        4: 3,
        6: 4,
        12: 6,
        36: 9,
        60: 12,
    }
    for number, count in expected.items():
        assert divisor_count(number) == count
        assert divisor_count(-number) == count


def test_adversarial_search_is_deterministic() -> None:
    first = adversarial_search(
        4,
        4,
        universe_size=20,
        iterations=300,
        seed=17,
    )
    second = adversarial_search(
        4,
        4,
        universe_size=20,
        iterations=300,
        seed=17,
    )
    assert first == second
    assert first.best_line_count <= first.initial_line_count
    assert first.ratio_over_f_three_halves > 0
