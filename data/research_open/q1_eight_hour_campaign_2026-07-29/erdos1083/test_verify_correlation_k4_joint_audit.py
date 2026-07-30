import itertools
from fractions import Fraction

from verify_correlation_k4_joint_audit import (
    c4_free_path_inequality,
    exponent_ledger,
    has_c4,
    parity_barrier,
)


def test_exponent_ledger() -> None:
    zero = exponent_ledger(Fraction(0, 1))
    assert zero.line_exponent_in_l == Fraction(8, 3)
    assert zero.correlation_exponent_in_l == Fraction(10, 3)
    assert zero.dyadic_overlap_boundary_in_l == Fraction(5, 6)
    assert zero.active_edge_exponent_at_boundary == Fraction(3, 2)
    assert zero.required_representation_multiplicity_in_l == Fraction(2, 3)
    assert zero.automatic_edge_density_at_boundary_in_l == Fraction(-7, 6)
    assert zero.maximum_edge_density_at_boundary_in_l == Fraction(-1, 6)

    eta = Fraction(1, 10)
    positive = exponent_ledger(eta)
    assert positive.dyadic_overlap_boundary_in_l == Fraction(5, 6) - eta
    assert positive.required_representation_multiplicity_in_l == (
        Fraction(2, 3) + eta
    )


def test_parity_barrier() -> None:
    for size in (2, 4, 8, 12, 20):
        barrier = parity_barrier(size)
        assert barrier.edge_densities == (Fraction(1, 2),) * 4
        assert barrier.transversal_cycle_count == 0


def test_c4_detection_and_path_inequality_exhaustive_small() -> None:
    for vertex_count in range(1, 6):
        possible_edges = tuple(
            itertools.combinations(range(vertex_count), 2)
        )
        for mask in range(1 << len(possible_edges)):
            edges = {
                edge
                for index, edge in enumerate(possible_edges)
                if mask & (1 << index)
            }
            assert c4_free_path_inequality(vertex_count, edges)

    cycle = {(0, 1), (1, 2), (2, 3), (0, 3)}
    assert has_c4(4, cycle)
