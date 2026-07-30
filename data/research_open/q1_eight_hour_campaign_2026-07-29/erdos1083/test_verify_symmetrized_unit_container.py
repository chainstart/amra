from verify_symmetrized_unit_container import (
    consecutive_family_scaling_audit,
    consecutive_unit_certificate,
    determinant_container_lemma_ledger,
    explicit_minor_closed_form,
    explicit_minor_row_indices,
    rigorous_degree_five_log_determinant,
)


def test_degree_five_is_a_rigorous_raw_additive_rank_counterexample():
    result = consecutive_unit_certificate(5)
    log_minor = rigorous_degree_five_log_determinant()
    assert result["irreducible"]
    assert result["mod_two_irreducible"]
    assert result["real_root_count"] == 5
    assert result["raw_additive_rank"] == 2
    assert all(norm == 1 for norm in result["unit_norms"])
    assert log_minor["excludes_zero"]
    assert log_minor["lower"] > 6
    assert log_minor["all_shift_intervals_exclude_zero"]
    assert "entirely in mp.iv" in log_minor["endpoint_construction"]


def test_log_minor_interval_is_stable_and_strictly_separated_from_zero():
    coarse = rigorous_degree_five_log_determinant(30)
    fine = rigorous_degree_five_log_determinant(45)
    for certificate in (coarse, fine):
        assert certificate["interval_decimal_digits"] >= 50
        assert certificate["all_shift_intervals_exclude_zero"]
        assert certificate["excludes_zero"]
        assert 6.3 < certificate["lower"] <= certificate["upper"] < 6.4
        assert 0 < certificate["width"] < 1e-12
        assert certificate["lower_interval_text"].startswith("[6.310")
        assert certificate["upper_interval_text"].startswith("[6.310")
    assert abs(coarse["lower"] - fine["lower"]) < 1e-12
    assert abs(coarse["upper"] - fine["upper"]) < 1e-12


def test_inverse_symmetrization_restores_full_rank_in_exact_family():
    for degree in range(5, 13):
        result = consecutive_unit_certificate(degree)
        assert result["irreducible"]
        assert result["real_root_count"] == degree
        assert result["product_remainder"].as_expr() == 1
        assert result["symmetrized_rank"] == degree
        assert result["independent_minor_determinant"] > 0
        assert result["explicit_minor_identity_holds"]
        assert (
            result["explicit_minor_determinant"]
            == explicit_minor_closed_form(degree)
        )
        assert result["explicit_minor_rows"] == explicit_minor_row_indices(
            degree
        )
        assert (
            result["side_lengths"]
            == result["side_lengths_closed_form"]
        )
        assert (
            result["box_size"]
            >= result["determinant_volume_lower_bound"]
        )


def test_closed_form_extends_exact_digit_sequence_and_audits_target_failure():
    audit = consecutive_family_scaling_audit(5, 30)
    records = audit["records"]
    assert len(records) == 26
    assert [record["minor_digits"] for record in records[:8]] == [
        12,
        16,
        21,
        27,
        33,
        40,
        48,
        57,
    ]
    assert [record["box_digits"] for record in records[:8]] == [
        27,
        36,
        46,
        57,
        71,
        85,
        102,
        120,
    ]
    assert all(record["irreducible"] for record in records)
    assert all(
        record["real_root_count"] == record["degree"]
        for record in records
    )
    for left, right in zip(records, records[1:]):
        assert (
            right["minor"]
            == 3069
            * __import__("math").factorial(left["degree"] - 2)
            * left["minor"]
        )
    assert "far below" in audit["target_failure"]
    assert "2^-d" in audit["overlap_density"]


def test_credible_replacement_is_explicitly_only_a_conjecture():
    ledger = determinant_container_lemma_ledger()
    assert ledger["raw_unit_claim"].startswith("false")
    assert ledger["status"].startswith("CONJECTURE")
    assert "5/2+eta" in ledger["threshold_condition"]
