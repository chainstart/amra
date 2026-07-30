from verify_cycle_lifting_parity_barrier import (
    barrier_certificate,
    k23_cycle_parities,
    representation_edges,
    selected_values,
    transversal_cycle_count,
)


def test_parity_representation_graphs_exact() -> None:
    for height_count in range(4, 30, 2):
        same = representation_edges(height_count, True)
        opposite = representation_edges(height_count, False)
        assert len(same) == height_count * height_count // 2
        assert len(opposite) == height_count * height_count // 2
        assert all((left - right) % 2 == 0 for left, right in same)
        assert all((left - right) % 2 != 0 for left, right in opposite)
        assert len(selected_values(height_count, True)) == (
            height_count // 2
        )
        assert len(selected_values(height_count, False)) == (
            height_count // 2
        )
        assert transversal_cycle_count(height_count) == 0


def test_full_shifted_correlation_certificate() -> None:
    for height_count in (4, 6, 10, 20, 40):
        certificate = barrier_certificate(height_count)
        assert certificate.all_external_indices_distinct
        assert certificate.external_indices_disjoint_from_cycle
        assert certificate.transversal_point_cycle_count == 0
        for edge in certificate.edge_certificates:
            assert sum(edge.cycle_pair) == sum(edge.external_pair)
            assert edge.offset_difference > 0
            assert edge.selected_value_count == height_count // 2
            assert edge.representation_count == (
                height_count * height_count // 2
            )
            assert edge.average_representation_multiplicity == height_count
            assert edge.target_values_verified


def test_k23_always_has_consistent_parity_cycle() -> None:
    for mask in range(1 << 6):
        labels = tuple((mask >> index) & 1 for index in range(6))
        parities = k23_cycle_parities(labels)
        assert parities[0] ^ parities[1] ^ parities[2] == 0
        assert 0 in parities
