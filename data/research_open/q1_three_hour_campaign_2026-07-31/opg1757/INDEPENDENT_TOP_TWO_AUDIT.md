# Independent audit of the endpoint top-two theorem

Date: 2026-07-31

Audited source:
`../OPG_ENDPOINT_TOP_TWO_THEOREM.md`

Verdict:
`PASS_WITHOUT_RESERVATION_AFTER_TWO_LOCAL_REPAIRS`

No counterexample or incorrect constant was found.  The first audit requested
two explicit transitions; both are now present in the theorem source.  The
discussion below retains the original concerns and records their repair.

## 1. Rooted and unrooted hypertree series

For a rooted hypertree, a root-incident hyperedge with \(k\) other rooted
branches has excess \(k-1\).  The incident-edge EGF is therefore
\[
\sum_{k\ge1}\frac{u^{k-1}T^k}{k!}
=\frac{e^{uT}-1}{u},
\]
which proves
\[
T=z\exp\left(\frac{e^{uT}-1}{u}\right).
\]
The edge-rooted and incidence-rooted series are respectively
\[
\frac{e^{uT}-1-uT}{u^2},
\qquad
\frac{T(e^{uT}-1)}u.
\]
Thus the dissymmetry formula for \(V\) is correct.

Differentiating it gives
\[
\partial_TV=1-Te^{uT},
\]
and ordinary Lagrange inversion gives the factorial
\((s-1)!/(c-1)!\) and coefficient \(t^{s-1}\) appearing in the theorem.
No normalization discrepancy was found.

An independent symbolic operator calculation, retaining symbolic \(c\)
and \(v\), gives exactly
\[
L_1(v)=2^{1-c}e^{v/2}
\]
and
\[
L_2(v)
=2^{1-c}e^{v/2}
\left(
-\frac{4cv-30c+2v^2+5v+30}{6}
\right).
\]
This independently verifies the two Laurent coefficients used for
\(h=0\).

## 2. One prescribed and two prescribed binary edges

The identity
\[
\binom{s}{2}H_{1,e,c}=\sum_F b(F)
\]
is correct: contracting a fixed binary edge gives precisely the weighted
profile with one doubled block.

For ordered pairs of distinct binary edges, the disjoint and adjacent
counts are
\[
\frac{s(s-1)(s-2)(s-3)}4,
\qquad
s(s-1)(s-2).
\]
Two adjacent prescribed edges contract to one block of weight three, so
the factor \(3\) in the adjacent endpoint is also correct.  Expanding the
disjoint term contributes \(b_{2,e,c}-6\) at relative order \(s^{-1}\);
the adjacent term contributes \(+3\).  Comparison with the binary-edge
second factorial moment gives
\[
b_{2,e,c}=b_{0,e,c}-2(c+2e-1).
\]

The first draft needed to justify one error estimate.  The revised theorem
now supplies equations (17a) and (22a).  If a
stratum has \(m=e-k\) nonbinary edges, the endpoint theorem loses at least
\(k\) powers of \(s\), while replacing its binary-edge count by the
\(m=e\) value changes \(b(b-1)\) by only \(O(ks)\).  Hence the omitted
correction is at most relative order \(s^{-2}\), which is why it cannot
alter the two displayed coefficients.  This is exactly the estimate now
written in the source, so the first concern is closed.

## 3. Marked-Abel leading term

The first draft stated a stronger arbitrary-profile top-symbol lemma too
briefly.

Only the single exceptional block of weight three is needed in the
\(h=2\) argument.  The revised theorem now inserts the exact \(p=1\)
fallback below.  For one
exceptional block of weight \(a\), \(N=s-a\), the exact marked-Abel formula
reduces to
\[
\mathcal F_c(1^N,a)
=
\Lambda_{s,a}
\left(
\frac{(1-t)U(t)^{c-1}}{(c-1)!}
\right).
\]
Writing \(P=(1-t)U^{c-1}/(c-1)!\), one has
\[
P(1)=0,\qquad
(t\partial_t)P(1)=-\frac1{2^{c-1}(c-1)!},
\qquad
U'(1)=0.
\]
The first falling-factor correction therefore gives
\[
\mathcal F_c(1^N,a)
=
\frac{a\,s^{N-1}}{2^{c-1}(c-1)!}
+O(s^{N-2}),
\]
which is exactly the normalized leading term required for the adjacent
pair.  Replacing the stronger arbitrary-profile paragraph by this direct
case is exactly what equations (15a)--(15b) of the revised theorem now do,
so the second concern is closed without relying on a stronger
arbitrary-profile assertion.

## 4. Master transpose

For an ordered endpoint pair \(A=(e,c)\), \(B=(f,d)\), the lambda and
overlap prefactor depends on \(e+f\), not on their order.  The two falling
factor products have the same first shift because
\[
(1+c+e)+(1+d+f)=(c+e)+(2+d+f).
\]
The endpoint contribution left after leading cancellation is
\[
A_{e,c}A_{f,d}(\kappa_{f,d}-\kappa_{e,c}),
\qquad
\kappa_{e,c}=c+2e-1.
\]
The transposed pair is present with the same prefactor and contributes its
negative.  The degree-\((2q+1)\) cancellation is therefore valid.

## 5. Additional falsification

The supplied executable audit passes:

- 84 exact endpoint top-two rows;
- 119 rooted/unrooted EGF comparisons;
- 496 transpose checks through \(q=30\).

An additional out-of-table check was made at
\[
e=7,\qquad c=1,\qquad h=0,1,2.
\]
For each \(h\), 22 exact values reconstructed the cleared numerator under
the proved denominator degree bound.  The predicted leading and
subleading coefficients agreed in all three cases.

These checks do not replace the all-parameter proof, but they found no
hidden normalization or adjacency constant error.

After the two source repairs, every step needed for the endpoint top-two
formula and the resulting degree drop is now present in a self-contained
proof.  The final verdict is therefore an unreserved `PASS`.
