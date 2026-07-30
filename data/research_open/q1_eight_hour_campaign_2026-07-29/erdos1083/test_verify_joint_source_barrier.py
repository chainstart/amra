from verify_joint_source_barrier import run


def test_odd_dihedral_product_has_quadratic_joint_moment() -> None:
    result = run(11, 7)
    assert result.points == 77
    assert result.mirror_count == 11
    assert result.min_fixed_points == 7
    assert result.max_fixed_points == 7
    assert result.rotation_success == 77
    assert result.joint_moment == 77 * 77
    assert result.joint_over_n_squared == 1.0


def test_even_dihedral_product_has_same_total_fixed_mass() -> None:
    result = run(12, 5)
    assert result.joint_moment == result.points * result.points
    assert result.min_fixed_points == 0
    assert result.max_fixed_points == 10
