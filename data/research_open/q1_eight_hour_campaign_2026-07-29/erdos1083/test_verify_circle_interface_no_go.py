from verify_circle_interface_no_go import active_angles, run


def test_exact_critical_scale_counts() -> None:
    t = 7
    result = run(t)
    assert result.points == t**5
    assert result.fibre_count == t**3
    assert result.fibre_size == t**2
    assert result.active_angle_count == t
    assert result.critical_distance_parameter == t**3
    assert result.min_source_count == t**3
    assert result.min_rotation_success == t**3 * (t**2 - 2 * t)
    assert result.source_incidence_sum == t**4
    assert result.per_fibre_chord_labels == t**2 - 1
    assert result.generic_cylinder_distance_count == t**5 - 1


def test_joint_moment_closed_form() -> None:
    t = 9
    result = run(t)
    # F^2 sum_{j=1}^t (S-2j)
    expected = t**6 * (t * t**2 - t * (t + 1))
    assert result.active_joint_moment == expected
    assert result.joint_over_nD == t - 1 - 1 / t


def test_all_rotations_have_near_full_success() -> None:
    t = 25
    angles = active_angles(t)
    n = t**5
    assert len(angles) == t
    assert min(item.rotation_success for item in angles) / n == 1 - 2 / t
    assert all(item.index >= 1 for item in angles)
