from fractions import Fraction

from effective_gap_bound import certify


EXPECTED_S_GAP = int(
    "557318272747802613573322901489669353946699423886389776921726369126"
    "099873157883699268070504958536925059099817311331374"
)


def test_effective_gap_bound_certificate() -> None:
    result = certify()
    assert result["k_cutoff"] == 1000
    assert result["geometry_threshold"] == 58_564
    assert result["S_gap_effective"] == EXPECTED_S_GAP
    assert all(
        item["attained_at_k"] == 999
        for item in result["fixed"].values()
    )
    assert all(
        item["bound_at_k1000"] < Fraction(1, 2)
        for item in result["growing"].values()
    )
    assert result["dominant_nonnegative"]["odd_page_q"]["start"] == 50
    assert result["dominant_nonnegative"]["even_page_q"]["start"] == 100
