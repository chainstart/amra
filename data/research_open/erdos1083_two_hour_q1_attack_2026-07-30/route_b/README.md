# Route B: moderate-rich Euclidean hub

The route produced a new tangent--label rich-line encoding and an
unconditional improvement of the hub-elimination threshold:
\[
\kappa<1/5
\quad\longrightarrow\quad
\kappa<9/41
\quad\longrightarrow\quad
\kappa<2/9.
\]

Main result:

- `TANGENT_LABEL_RICH_LINE_HUB_THEOREM.md`
- `NINE_FORTY_ONE_NEXT_ATTACK.md` (signed-slope aggregation and the
  sharp \(9/41\) method ledger)
- `COLLINEAR_CENTER_LINEARIZATION_THEOREM.md` (fixed-signed-centre
  parabolic lift and the improved \(2/9\) hub threshold)
- `ENDPOINT_ENERGY_DICHOTOMY.md` (conditional arithmetic structure at
  the former \(9/41\) ledger)

Verification:

- `verify_tangent_label_rich_line_hub.py`
- `test_verify_tangent_label_rich_line_hub.py`
- `verify_nine_forty_one_next_attack.py`
- `test_verify_nine_forty_one_next_attack.py`
- `verify_collinear_center_linearization.py`
- `test_verify_collinear_center_linearization.py`
- `verify_endpoint_energy_dichotomy.py`
- `test_verify_endpoint_energy_dichotomy.py`
- `INDEPENDENT_AUDIT.md`
- `SECOND_INDEPENDENT_AUDIT.md`
- `COLLINEAR_CENTER_LINEARIZATION_INDEPENDENT_AUDIT.md`

The strongest current consequence is a
\(t^{2/9-\varepsilon-o(1)}\) rich matching for
\(t^{1-o(1)}\) labels.  This is a structural exponent improvement,
not yet an improvement of the global \(3/5\) distinct-distance
exponent.
