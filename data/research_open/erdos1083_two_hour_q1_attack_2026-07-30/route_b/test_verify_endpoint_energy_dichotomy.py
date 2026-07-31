from fractions import Fraction

from verify_endpoint_energy_dichotomy import endpoint_energy_ledger


def test_endpoint_energy_ledger():
    cert = endpoint_energy_ledger()
    assert cert["energy_product"] == Fraction(274, 41)
    assert cert["additive_min_feasible"] == Fraction(151, 41)
    assert cert["eta_max"] == 41


def test_energy_tradeoff_endpoints():
    cert = endpoint_energy_ledger()
    additive_max = cert["additive_max"]
    additive_min = cert["additive_min_feasible"]
    product = cert["energy_product"]
    assert product - additive_max == cert["multiplicative_min"]
    assert product - additive_min == cert["multiplicative_max"]
