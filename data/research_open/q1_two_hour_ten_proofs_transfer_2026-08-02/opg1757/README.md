# OPG-1757 ten-proofs transfer lane

This lane applies the normalization, complete-certificate, and endpoint
stability patterns extracted from `openai/ten-proofs@94bc0fe` to the remaining
OPG-1757 logarithmic boundary layer.

## Main result

`COMPLETE_LOG_LAYER_THEOREM.md` proves a single-threshold eventual theorem for

\[
 31\le d<241\log s.
\]

The proof restores the beta-shift cost omitted by the previous absolute-value
estimate.  It combines all bases at fixed index into a positive generating
certificate and, for growing index, shows that only two positive page terms
can meet at the scale transition.  Together with the old low columns,
`d>=241 log s` theorem, and top bands, this gives coefficientwise positivity
of both third-active transport candidates for every sufficiently large `s`.

The result is eventual, not universal in `s`; OPG-1757 remains open.

## Files

- `TEN_PROOFS_METHOD_TRANSFER.md`: source reading and method extraction.
- `COMPLETE_LOG_LAYER_THEOREM.md`: mathematical proof.
- `CLAIM_LEDGER.md`: exact quantifiers, dependency splice, and firewall.
- `EFFECTIVE_GAP_BOUND.md`: explicit 117-digit upper bound for the new gap
  threshold.
- `effective_gap_bound.py`: exact-integer/rational certificate for that
  bound.
- `verify_complete_log_layer.py`: exact finite algebraic certificate.
- `test_complete_log_layer.py`: regression test for the certificate.
- `stress_complete_log_layer.py`: larger exact scan, explicitly
  corroborative only.
- `STRESS_TEST_REPORT.md`: stress-test scope and output.
- `RESEARCH_LOG.md`: chronological work log.
- `AUDIT_HANDOFF.md`: independent author-swap checklist.

## Verification

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_complete_log_layer.py
PYTHONDONTWRITEBYTECODE=1 python3 effective_gap_bound.py
PYTHONDONTWRITEBYTECODE=1 pytest -q
```

The verifier pins the old common-base source by SHA-256.  It does not rewrite
or modify any old-campaign artifact.
