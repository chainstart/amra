import itertools

from verify_geometric_radius_high_energy import (
    exhaustive_search,
    geometric_circles,
    has_sidon_differences,
    identical_height_energy_lower_bound,
    offsets_by_product,
    theorem_lower_bound,
    verify_thin_slab_instance,
)
from verify_affine_copy_barrier import parameter_line_count


def test_thin_slab_theorem_exhaustively_small() -> None:
    candidates = tuple(itertools.combinations(range(5), 2))
    for height_sets in itertools.product(candidates, repeat=3):
        line_count, lower_bound = verify_thin_slab_instance(
            height_sets,
            radial_scale=6,
        )
        assert lower_bound == theorem_lower_bound(height_sets)
        assert line_count >= lower_bound


def test_documented_small_searches() -> None:
    first = exhaustive_search(3, 3, 6)
    assert first.configurations_checked == 8000
    assert first.minimum_line_count == 18
    assert first.minimizer == ((0, 1, 2),) * 3

    second = exhaustive_search(3, 4, 6)
    assert second.configurations_checked == 3375
    assert second.minimum_line_count == 23
    assert second.minimizer == ((0, 1, 2, 3),) * 3


def test_sidon_offsets_and_identical_height_bound() -> None:
    for ratio in range(2, 7):
        for radius_count in range(1, 12):
            assert all(
                has_sidon_differences(values)
                for values in offsets_by_product(radius_count, ratio).values()
            )

    for radius_count in range(2, 8):
        for height_set in (
            (0, 1, 2),
            (0, 2, 9, 20),
            (0, 10, 11, 31, 80),
        ):
            height_sets = (height_set,) * radius_count
            line_count = parameter_line_count(geometric_circles(height_sets))
            lower_bound = identical_height_energy_lower_bound(
                radius_count,
                height_set,
            )
            assert line_count >= lower_bound
