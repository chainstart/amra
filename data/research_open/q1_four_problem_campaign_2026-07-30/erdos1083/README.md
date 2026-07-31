# Erdős #1083: four-problem Q1 campaign

Date: 2026-07-30

## Outcome

This round did not improve the arbitrary-set bound
\[
f_3(N)\gg N^{3/5}.
\]

It did close one previously vague part of the \(2/9\) endpoint.  A
surviving hub cannot merely consist of isolated or concentric
repeated circles.  It forces one fixed-\((A,\rho)\) bundle containing
\[
t^{19/9-o(1)}
\]
pairwise nonaligned congruent reverse circles, each with at least
\[
t^{7/9-o(1)}
\]
source incidences and
\[
t^{5/6-o(1)}
\]
producing triples.

A new distinct-dilate energy budget shows that the distance map in
almost every height row is near-injective in aggregate.  Since the
global distance budget is only \(t^{3+o(1)}\), two different-height
rows must share
\[
t^{2/9-o(1)}
\]
distinct anchor-to-axis squared-distance labels.

More globally, the endpoint contains a genuine spectral incidence
graph: at least
\[
t^{35/18-o(1)}
\]
distance labels each occur in at least
\[
t^{13/18-o(1)}
\]
different nonaligned circle rows.

For every fixed \(\varepsilon>0\), the package further forces
\[
t^{17/6-o(1)}
\]
nonaligned row pairs, each sharing
\[
t^{2/9-\varepsilon-o(1)}
\]
labels.  The obstruction is therefore a dense synchronized network,
not one accidental pair.

Thus the exact endpoint conclusion is now:

> either \(t^{1-o(1)}\) labels support rich plane-pair matchings of
> size \(t^{2/9-o(1)}\), or a pair of incidence-rich,
> multiplicity-rich, nonaligned reverse-circle charts has a
> \(t^{2/9-o(1)}\)-sized synchronized distance spectrum, inside the
> larger \(t^{35/18}\)-by-\(t^{13/18}\) spectral graph.

The remaining local problem is an upper bound or exceptional-family
classification for that synchronized spectrum.

## Files

- `MULTIDILATE_ENERGY_AND_NONALIGNED_SYNCHRONIZATION_THEOREM.md` —
  human proof, Euclidean translation, and endpoint theorem.
- `INDEPENDENT_AUDIT.md` — independent reconstruction and red-team
  boundary.
- `QUANTIFIER_AND_GEOMETRIC_GAP_AUDIT.md` — adverse-direction
  \(o(1)\)/\(\varepsilon\) audit, exact \(35/18,13/18,17/6\)
  derivations, Mathialagan--Sheffer comparison, and the required
  de-reuse lemma.
- `verify_multidilate_nonaligned_bundle.py` — exact finite and
  exponent verifier.
- `test_verify_multidilate_nonaligned_bundle.py` — regression tests.
- `CLAIM_LEDGER.md` — proved/conditional/open separation.
- `FINAL_REPORT.md` — campaign assessment and next target.

## Reproduction

```bash
cd data/research_open/q1_four_problem_campaign_2026-07-30/erdos1083
python3 verify_multidilate_nonaligned_bundle.py
pytest -q
```

The verifier does not replace the all-parameter proof.
