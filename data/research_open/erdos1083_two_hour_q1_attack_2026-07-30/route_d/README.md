# Route D

This route tests whether the true Euclidean cross-centre distances can
exclude the Route B \(9/41\) endpoint.

Main file:

- `CROSS_HEIGHT_ENERGY_AND_EUCLIDEAN_BARRIER.md`
- `TWO_NINTHS_INDEPENDENT_AUDIT.md`
- `TWO_NINTHS_NEXT_TARGET.md`

Certificates:

- `verify_cross_height_energy.py`
- `test_verify_cross_height_energy.py`
- `verify_two_ninths_audit.py`
- `test_verify_two_ninths_audit.py`
- `RED_TEAM_AUDIT.md`

The outcome is a sharp localization rather than endpoint exclusion:
same-height collisions miss the required collision mass by
\(t^{26/41}\), so any endpoint example must have a very large
cross-height parabolic-affine energy.  A genuine Euclidean
cancellation model proves that the cross-distance formula alone has
no power saving; the remaining essential constraint is reuse of only
\(M\) global target planes.

The independent audit of the stronger collinear-centre route returns
**PASS**: after all three Szemerédi--Trotter branches are treated
separately, it rigorously improves the structural matching threshold
to \(2/9-\varepsilon\).
