#!/usr/bin/env python3
"""Tests for the ruled-stability tensor no-go audit."""

from __future__ import annotations

from fractions import Fraction

from verify_ruled_stability_extraction import (
    audit,
    common_neighbour_exponent,
    dyadic_ledger,
    endpoint_common_target_exponent,
    random_balanced_endpoint_cell,
    random_support_model,
    split_rotation_ledger,
    symmetric_plane_pair_support_model,
)


def test_dyadic_exponents_at_all_critical_scales():
    for numerator in range(12, 17):
        omega = Fraction(numerator, 4)
        ledger = dyadic_ledger(omega)
        assert ledger["support_edges"]+omega == 8
        assert ledger["average_left_degree"]+2 == (
            ledger["support_edges"]
        )
        assert ledger["average_right_degree"]+3 == (
            ledger["support_edges"]
        )
        assert ledger["uniform_aggregate_energy"] == 13
        assert ledger["diagonal_energy"] == 8+omega


def test_worst_scale_drc_common_neighbour_losses():
    assert common_neighbour_exponent(4, 1) == 2
    assert common_neighbour_exponent(4, 2) == 1
    assert common_neighbour_exponent(4, 3) == 0
    assert common_neighbour_exponent(4, 4) == -1
    assert endpoint_common_target_exponent(1) == 1
    assert endpoint_common_target_exponent(2) == -1


def test_random_support_has_critical_mass_and_energy():
    for q in (3, 4, 5):
        model = random_support_model(q)
        assert model["left_vertices"] == q**2
        assert model["right_vertices"] == q**3
        assert model["left_degree"] == q**2
        assert model["cell_weight"] == q**4
        assert model["row_mass"] == q**6
        assert model["total_mass"] == q**8
        assert model["diagonal_energy"] == q**12
        assert model["aggregate_energy"] >= q**13
        assert model["cross_energy"] > 0


def test_random_balanced_endpoint_partition():
    for q in (3, 4, 5):
        cell = random_balanced_endpoint_cell(q)
        assert cell["endpoint_side_Q"] == q**3
        assert cell["labels_in_plane_pair"] == q**2
        assert cell["pairs_per_label"] == q**4
        assert cell["maximum_one_source_degree"] >= 1
        assert cell["maximum_two_source_codegree"] >= 0


def test_symmetric_plane_pair_tensor_keeps_energy_exponents():
    for q in (4, 5, 6, 7):
        model = symmetric_plane_pair_support_model(q)
        assert model["unordered_plane_pairs"] == q*(q-1)//2
        assert model["oriented_rows"] == q*(q-1)
        assert model["row_degree"] == q**2
        assert model["row_mass"] == q**6
        assert model["aggregate_energy"] >= (
            model["aggregate_cs_lower"]
        )
        assert model["cross_energy"] > 0


def test_split_rotation_reservoir_exact_mass():
    for q in range(3, 12):
        ledger = split_rotation_ledger(q)
        assert ledger["N"] == q**5
        assert ledger["source_mass"] == q**4
        assert ledger["reservoir_mass"] == q**5-q**4
        assert ledger["total_mass"] == q**5
        assert ledger["source_per_angle"] == q**3
        assert ledger["minimum_rotation_count"] > 0


def test_full_nogo_audit_boundary():
    result = audit()
    assert result["status"] == "TENSOR_LEVEL_NO_GO"
    assert result["euclidean_counterexample"] is False
    assert result["aggregate_energy_t_power"] == "13"
    assert result["diagonal_energy_t_power"] == "12"
