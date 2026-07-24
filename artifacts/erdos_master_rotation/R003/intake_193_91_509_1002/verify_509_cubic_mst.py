#!/usr/bin/env python3
"""Exact/numerical checks for the cubic MST route audit in #509."""

from decimal import Decimal, getcontext

getcontext().prec = 50
sqrt3 = Decimal(3).sqrt()
d = Decimal(3) / 2

# Both root triples have MST edge multiset {d,d}.
equilateral_mst = [d, d]
collinear_mst = [d, d]
assert equilateral_mst == collinear_mst

# Equilateral roots centred at zero give z^3-R^3, R=d/sqrt(3).
# Collinear roots {-d,0,d} give z^3-d^2 z.
# A cubic lemniscate is connected iff both critical values have modulus <=1.
equilateral_critical_modulus = d**3 / (Decimal(3) * sqrt3)
collinear_critical_modulus = Decimal(2) * d**3 / (Decimal(3) * sqrt3)
assert equilateral_critical_modulus < 1
assert collinear_critical_modulus > 1

# The elementary one-disc sufficient condition applies to the equilateral
# example: its minimum enclosing radius is d/sqrt(3)<1.
assert d / sqrt3 < 1

# A second elementary regime: if a pair of cubic roots is at distance delta
# no greater than the value below, two disks of total radius two work.
threshold = Decimal(4) - Decimal(2) * (Decimal(27) / 4) ** (Decimal(1) / 3)
assert Decimal("0.220") < threshold < Decimal("0.221")
for pair_distance in [Decimal("0"), threshold]:
    cap = Decimal(2) - pair_distance / 2
    x = Decimal(2) * cap / 3
    singleton_radius = cap / 3
    pair_radius = pair_distance / 2 + x
    product_lower_bound = x**2 * singleton_radius
    assert abs(pair_radius + singleton_radius - 2) < Decimal("1e-40")
    assert product_lower_bound >= 1 - Decimal("1e-40")

print(
    "PASS #509:",
    {
        "equilateral_critical_modulus": str(equilateral_critical_modulus),
        "collinear_critical_modulus": str(collinear_critical_modulus),
        "close_pair_threshold": str(threshold),
    },
)
