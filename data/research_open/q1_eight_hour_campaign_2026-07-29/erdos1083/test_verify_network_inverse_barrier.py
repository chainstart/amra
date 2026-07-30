import math
import random

from verify_network_inverse_barrier import (
    dyadic_extraction,
    four_cycle_count_complete_graph,
    hadamard_certificate,
)


def test_hadamard_design_exactly() -> None:
    for dimension in range(2, 8):
        certificate = hadamard_certificate(dimension)
        universe = 1 << dimension
        block_size = universe // 2
        assert certificate.block_count == universe - 1
        assert certificate.block_size == block_size
        assert certificate.union_size == universe
        assert certificate.minimum_intersection == block_size // 2
        assert certificate.maximum_intersection == block_size // 2
        assert certificate.minimum_symmetric_difference == block_size
        assert certificate.maximum_symmetric_difference == block_size
        assert certificate.correlation_edge_count == math.comb(
            universe - 1,
            2,
        )
        assert certificate.four_cycle_count == (
            four_cycle_count_complete_graph(universe - 1)
        )
        assert certificate.lacunary_union_additive_energy == (
            certificate.minimum_possible_energy_formula
        )
        assert certificate.minimum_possible_energy_formula == (
            2 * universe * universe - universe
        )


def test_dyadic_extraction_inequality() -> None:
    rng = random.Random(20260729)
    for length in range(1, 80):
        weights = [rng.randrange(0, 1000) for _ in range(length)]
        threshold, count, product = dyadic_extraction(weights)
        maximum = max(weights)
        if maximum == 0:
            assert product == 0
        else:
            scales = 1 + math.ceil(math.log2(maximum))
            assert count == sum(weight >= threshold for weight in weights)
            assert product * scales >= sum(weights)
