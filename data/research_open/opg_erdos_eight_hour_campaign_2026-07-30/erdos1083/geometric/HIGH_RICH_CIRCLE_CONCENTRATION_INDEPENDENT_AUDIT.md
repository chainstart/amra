# Independent audit: critical high-rich reverse-circle concentration

Date: 2026-07-30

Audited file:

- `HIGH_RICH_CIRCLE_CONCENTRATION_COROLLARY.md`

## 0. Verdict

\[
\boxed{\mathrm{PASS}}
\]

The \(t^{9/4+\eta}\) threshold, the aligned-family reduction, the
merged-circle multiplicity cap, the \(MQ\) weighted bound, and both
comparisons with the hub mass are correct.  The result is a structural
concentration theorem and does not improve the \(3/5\) exponent.

## 1. Source-theorem boundary

Mathialagan--Sheffer, Theorem 1.4(b) in
[*Distinct distances on non-ruled surfaces and between
circles*](https://arxiv.org/abs/2011.08098), states that finite sets
of sizes \(m,n\) on two circles which are neither aligned nor
perpendicular determine
\[
\Omega\!\left(
\min\{m^{2/3}n^{2/3},m^2,n^2\}
\right)
\tag{A1}
\]
bipartite distances.  The source states an unqualified
\(\Omega\)-bound; the algebraic-incidence constants are controlled by
the fixed curve degrees, so the campaign does not insert an
unrecorded quantitative separation from the exceptional locus.

The axial-chart translation was checked separately.  A retained
circle has
\[
A=\cos(\alpha-\beta)v\ne0
\]
because the target is off-axis and the perpendicular target plane was
removed.  Hence the perpendicular-circle exception, which would
require \(A_1=A_2=0\), cannot occur.  Within one fixed source plane,
aligned circles have a common perpendicular axis and therefore a
common centre.

## 2. Richness threshold

If two distinct retained circles have
\[
s_1,s_2\ge t^{9/4+\eta},
\]
then the first term in (A1) is at least
\[
(s_1s_2)^{2/3}
\ge t^{3+4\eta/3}.
\tag{A2}
\]
The other two terms are even larger.  For fixed \(\eta>0\), (A2)
contradicts the critical global budget \(t^{3+o(1)}\).  Thus every
pair in the high-rich sector is aligned.  Since all these circles lie
in the same source plane, they are concentric.  Distinct normalized
positive-radius circles with a common centre have different radii and
are disjoint, so
\[
\sum_C |P_\alpha\cap C|\le |P_\alpha|\le Q.
\tag{A3}
\]
Removing the at most two intersection points before applying (A1)
does not affect any exponent.

## 3. Multiplicity and weighted mass

For one fixed retained target plane \(\Pi_\beta\), the already audited
reverse-circle lemma makes
\[
(q,d)\longmapsto\Gamma_{\beta,q,d}
\]
injective.  Therefore a fixed merged normalized circle receives at
most one triple from each \(\beta\), even if labels are reused across
different planes.  With at most \(M\) target planes,
\[
\mu(C)\le M.
\tag{A4}
\]
Combining (A3)--(A4) gives
\[
W_{\rm high}
=\sum_C\mu(C)|P_\alpha\cap C|
\le M\sum_C|P_\alpha\cap C|
\le MQ=t^{4+o(1)}.
\tag{A5}
\]

The hub mass is \(LH=t^{7-3\kappa-o(1)}\), so for fixed
\(\kappa<1\)
\[
\frac{W_{\rm high}}{LH}
\le t^{-3(1-\kappa)+o(1)}=o(1).
\tag{A6}
\]
A zero-radius triple has at most one source incidence, and there are
at most \(MQL=t^{6-2\kappa+o(1)}\) such triples.  Its exponent gap
from \(LH\) is \(1-\kappa>0\).  Empty circles contribute nothing and
the perpendicular target plane was removed upstream.  Hence the
remaining positive-radius mass is indeed supported principally on
circles with richness below \(t^{9/4+\eta}\).

## 4. Reproduction and scope

The exact exponent and finite weighted-partition checks are:

```bash
python3 verify_high_rich_circle_concentration.py
pytest -q test_verify_high_rich_circle_concentration.py
```

The verification code checks the rational exponent identities and
the finite form of (A3)--(A5).  The mathematical proof additionally
uses the cited two-circle theorem and the previously audited
reverse-circle injectivity lemma.

No conclusion is drawn about how the moderately rich mass is
distributed among nonaligned classes.  That aggregation problem is
the surviving step toward an exponent improvement.
