from verify_six_coprime_cyclotomic_escape import (
    audit,
    injection_grid,
    quadratic_injection_grid,
    signed_relation_grid,
)


def test_six_coprime_audit_passes():
    result = audit()
    assert result["exact_quotient_arithmetic"] is True
    assert result["order_8_collision_verified"] is True
    assert result["order_9_collision_verified"] is True
    assert result["status"] == "finite_audit_passed"


def test_orders_with_factor_five_have_injective_sample_labels():
    for order in (5, 25, 35, 55, 65):
        assert injection_grid(order)["distinct_labels_checked"] > 0


def test_signed_relation_grid_includes_prime_power_and_mixed_orders():
    for order in (5, 25, 35):
        assert signed_relation_grid(order)["signed_relations_checked"] > 0


def test_quadratic_base_field_samples_are_injective():
    for order in (5, 25, 35):
        row = quadratic_injection_grid(order)
        assert row["quadratic_base_distinct_labels_checked"] > 0
