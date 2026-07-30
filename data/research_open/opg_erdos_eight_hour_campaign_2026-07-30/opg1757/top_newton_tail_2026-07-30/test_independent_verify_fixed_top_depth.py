from independent_verify_fixed_top_depth import (
    audit,
    cycle_union_stress,
    elementary_leading_and_triangular_audit,
    exact_exceptional_audit,
    mixed_binomial_moment_audit,
    profile_degree_audit,
    refined_bidegree_audit,
    refined_cancellation_audit,
    symbolic_exceptional_audit,
)


def test_independent_marked_profiles_and_cycle_unions():
    assert len(profile_degree_audit(3, 5)) == 12
    assert len(refined_bidegree_audit(3)) == 10
    assert cycle_union_stress(1000) == 1000


def test_mixed_moments_exceptions_and_triangular_signs():
    assert mixed_binomial_moment_audit(6) > 300
    assert set(exact_exceptional_audit(5)) == {2, 3, 4, 5}
    assert set(symbolic_exceptional_audit()) == {1, 2}
    assert [row[0] for row in refined_cancellation_audit()] == [4, 5, 6]
    constants = elementary_leading_and_triangular_audit(8)
    assert str(constants[-1]) == "2/315"


def test_full_independent_fixed_top_depth_audit():
    result = audit()
    assert result["verdict"] == "PASS"
    assert result["refined_b_k_d_bound"] == "O_d(k^d)"
    assert result["previous_repairs_verified"] is True
    assert result["main_text_modified"] is False
