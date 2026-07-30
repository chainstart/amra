from verify_all_rank_recurrence_leading_positivity import audit


def test_all_rank_recurrence_leading_positivity_certificate():
    report = audit()
    assert report["status"] == "PASS"
    assert report["finite_prefix"]["maximum_band"] == 98
    assert report["finite_prefix"]["nonpositive_bands"] == []
    assert report["jensen_tail"]["analytic_start_index"] == 100
    assert "G_q>0 for every q>=0" in report["conclusion"]
