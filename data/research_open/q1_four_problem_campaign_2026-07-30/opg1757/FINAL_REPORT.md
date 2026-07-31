# OPG-1757 parallel attack: final report

Date: 2026-07-30

## Outcome

The campaign did not solve OPG-1757 or the complete \(\alpha^2\) layer.
It did produce two new unbounded theorems.

First, the general fixed-page determinant kernel now has the uniform
positive window
\[
\boxed{
[\beta^r]K_k(s,\beta)>0
\quad(k,s\ge4,\ 0\le r\le8).
}
\]
The inherited result stopped at \(r=4\).  The four new ranks are exact
polynomial identities for arbitrary \(k,s\), not checks of four more
fixed page counts.  Their positive forms use
\((m,v)=(k-4,s-4)\), so they also cover the physically relevant region
\(s<k\).

Second, the leading long-recurrence layer has a quantitative spectral
law.  If \(\rho\) is the unique dominant zero of its Airy/\({}_2F_0\)
entire function, then
\[
\frac{1961}{1000}<\rho<\frac{1962}{1000}
\]
and
\[
G_{n-1}=3\rho^{-n}
\left(1+O_{\rm explicit}\!\left((327/350)^n\right)\right).
\]
This identifies the limiting ratio and exponential convergence rate,
rather than only the sign of \(G_q\).

## Proof and verification

The kernel proof consists of:

1. the primitive page-partition transfer;
2. exact deconvolution of the universal
   \((1+k\beta)^{2s-2k-2}\) factor;
3. the label-support bounds
   \(\deg_k n_d\le2d-6\), \(\deg_s n_d\le d\);
4. 746 exact grid values which uniquely force the four identities;
5. eight evaluations outside those grids;
6. explicit positive shifted polynomials containing 148 positive
   monomials in total; and
7. an independent connected-component recurrence based on the
   weighted bipartite Cayley formula.

The complete local regression is:

```text
4 passed
```

Run it with:

```bash
pytest -q data/research_open/q1_four_problem_campaign_2026-07-30/opg1757
```

## Publication assessment

This materially strengthens the existing OPG manuscript nucleus:

- it replaces four additional parameter scans by four all-parameter
  coefficient theorems;
- it doubles the general fixed-page positive window;
- it adds a clean dominant-singularity theorem to the all-rank
  long-recurrence theory.

It is still not, by itself, a secure Q1 main theorem.  The eight-layer
window is finite in the kernel coefficient rank, and the spectral law
concerns only the leading depth coefficient.  A Q1-level upgrade most
likely requires one of:

1. a uniform exchange-tail or total-positivity theorem proving every
   coefficient of \(K_k\);
2. removal of the alternating inversion and proof of every \(F_k\),
   which would close the full \(\alpha^2\) layer; or
3. an all-depth compatibility/real-rootedness theorem which converts
   the long recurrence into the missing middle Newton control.

Computing \(\beta^9,\beta^{10}\) of \(K_k\), or the ninth and tenth
ordinary-symbol ranks, is intentionally not recommended as the next
step.  The next work should seek the cross-layer injection or positive
kernel factorization suggested by the common positive
\((k-4,s-4)\)-shift.

## Literature boundary

The formulas use known forest-enumeration inputs of Liu--Chow and
Myrvold.  Tang--Zhang's 2026 result concerns fixed-component forests of
complete graphs for sufficiently large order and does not state these
fixed-page kernel identities.  Fang--Ma's current C-Gårding classes do
not cover general complete-split graphic matroids.  These comparisons
support non-overlap, but a MathSciNet/zbMATH/Scopus-level priority audit
is still mandatory before a novelty claim.

## Files

- `GENERAL_K_EIGHT_LAYER_POSITIVITY_THEOREM.md`: main new kernel theorem;
- `DOMINANT_ZERO_SPECTRAL_ASYMPTOTIC_THEOREM.md`: analytic theorem;
- `INDEPENDENT_AUDIT.md`: audit and claim boundary;
- `CLAIM_LEDGER.md`: proved/open separation;
- `verify_general_k_beta5_beta8.py`: exact all-parameter verifier;
- `independent_verify_general_k_beta5_beta8.py`: independent method;
- `verify_dominant_zero_spectral_asymptotic.py`: exact spectral audit.
