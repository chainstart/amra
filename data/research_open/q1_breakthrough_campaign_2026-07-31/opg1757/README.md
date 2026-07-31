# OPG-1757 breakthrough package

The central result is
`ALL_FIXED_DEFICIT_EVENTUAL_POSITIVITY_THEOREM.md`:
for every fixed deficit \(q\), every coefficient in the natural support
of \(B_{2s-5-q}\) is strictly positive for all sufficiently large \(s\).
The structurally forced lower coefficients remain zero.  The proof
identifies the exact leading symbol
\[
\frac4{q!}(1+2z+2z^2)^q.
\]

Files:

- `ALL_FIXED_DEFICIT_EVENTUAL_POSITIVITY_THEOREM.md` — proof;
- `CLAIM_LEDGER.md` — proved/open firewall;
- `verify_fixed_deficit_leading_symbol.py` — exact symbolic and regression
  certificate;
- `test_fixed_deficit_leading_symbol.py` — fast unit tests.
- `SECOND_SYMBOL_CONJECTURE.md` and
  `verify_second_symbol_conjecture.py` — the retained discovery record;
- `SECOND_SYMBOL_THEOREM.md` and `verify_second_symbol_theorem.py` — a
  certificate-backed all-\(q\), all-offset second Laurent formula;
- `LAURENT_DEGREE_LEMMA.md` — the filtered-ring proof closing the former
  endpoint Laurent total-degree condition.
- `TWO_MARKED_HYPERFOREST_EGF_LEMMA.md` and its verifier — an exact
  all-excess path-kernel formula replacing the \(h=2\) incidence list.
- `ENDPOINT_POLYNOMIALITY_THEOREM.md` and its verifier — uniform endpoint
  polynomiality and arbitrary-fixed-deficit denominator cancellation.
- `LOGARITHMIC_GROWING_DEFICIT_WINDOW.md` — conditional reduction of
  simultaneous positivity for \(q\le c_0\log s/\log\log s\) to a uniform
  coefficient-height lemma.

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 verify_fixed_deficit_leading_symbol.py
PYTHONDONTWRITEBYTECODE=1 \
python3 verify_fixed_deficit_leading_symbol.py --extended-q6
PYTHONDONTWRITEBYTECODE=1 \
python3 -m unittest -v test_fixed_deficit_leading_symbol.py
PYTHONDONTWRITEBYTECODE=1 \
python3 verify_two_marked_hyperforest_egf.py
PYTHONDONTWRITEBYTECODE=1 \
python3 verify_second_symbol_conjecture.py
PYTHONDONTWRITEBYTECODE=1 \
python3 verify_endpoint_polynomiality.py --extended-q6
PYTHONDONTWRITEBYTECODE=1 \
python3 verify_second_symbol_theorem.py --extended-endpoints
```

This package does not claim a polynomial/linear-width deficit window, the
full complete-split Rayleigh theorem, or arbitrary-host OPG-1757.
