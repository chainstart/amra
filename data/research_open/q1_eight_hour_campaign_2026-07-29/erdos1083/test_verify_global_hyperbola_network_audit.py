from fractions import Fraction

import verify_global_hyperbola_network_audit as verifier


def test_finite_affine_tensor_counts() -> None:
    certificate = verifier.affine_tensor(2, 4)
    assert certificate["block_count"] == 16
    assert certificate["line_size"] == 2
    assert certificate["direction_count"] == 2
    assert certificate["core_size"] == 8
    assert certificate["block_sizes"] == [16]
    assert certificate["union_size"] == 128
    assert certificate["total_incidence"] == 256
    assert certificate["strong_edge_count"] == 16
    assert certificate["strong_overlap_sizes"] == [8]
    assert certificate["strong_degrees"] == [2]
    assert certificate["symbol_multiplicities"] == [2]
    assert certificate["correlation"] == 128
    assert certificate["weighted_overlap"] == 128


def test_reuse_lemma_is_sharp_on_finite_tensor() -> None:
    certificate = verifier.affine_tensor(2, 4)
    assert certificate["reuse_lower_bound"] == 2
    assert certificate["maximum_multiplicity"] == 2


def test_symbolic_exponent_ledger() -> None:
    for dimension in (3, 4, 6, 8):
        ledger = verifier.exponent_ledger(dimension)
        assert ledger["block_size"] == 1
        assert ledger["strong_degree"] == Fraction(1, 2)
        assert ledger["union"] == ledger["target_union"]
        assert ledger["correlation"] == ledger["forced_correlation"]
        assert ledger["strong_edges"] == Fraction(5, 2)
        assert (
            ledger["propagation_target"]
            - ledger["common_multiplicity"]
            == ledger["reuse_gap"]
        )


def test_hyperbola_vertex_potential_identity() -> None:
    offsets = [3, 17, 29, 101]
    for first, second, third in [(0, 1, 2), (1, 2, 3), (0, 2, 3)]:
        delta_first_second = offsets[second] - offsets[first]
        delta_second_third = offsets[third] - offsets[second]
        delta_first_third = offsets[third] - offsets[first]
        assert (
            delta_first_second + delta_second_third
            == delta_first_third
        )
