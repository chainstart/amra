from verify_outer_a_low_degree_residue import run_exhaustive


def test_colourwise_and_aggregate_residue_guards():
    result = run_exhaustive(max_edges_per_type=8, max_colours=3)
    assert result["status"] == "PASS"
    assert result["aggregate_profiles"] > 0
    assert result["internal_low_parameter_cases"] > 0
