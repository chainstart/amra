# Independent audit of the \(2/9\) collinear-centre argument

Date: 2026-07-30

Audited manuscript:

`../route_b/COLLINEAR_CENTER_LINEARIZATION_THEOREM.md`

## Verdict

\[
\boxed{\text{PASS}}
\]

The argument rigorously excludes the Euclidean hub for every fixed
\(\kappa<2/9\), subject to the inherited matching-or-hub setup and
point--circle theorem already audited in Route B.

One branch requires particular care:

> The \(+RQ\) term in the fixed-\(A\) Szemerédi--Trotter sum is not
> excluded by the old scalar lower bound on \(m\) alone.  It is
> excluded only after retaining the full global point--circle
> inequality \(11a+2b\le18\).

The manuscript does retain this inequality as (15) and uses its
consequence (17), so the published proof passes.  If (15) were
deleted, the proposed \(2/9\) deduction would fail.

## 1. Geometry of the lift

For fixed \(A\), define
\[
\Phi_A(u,z)=\bigl(z,(u-A)^2+z^2\bigr).
\]
An image point fixes \(z\) and \((u-A)^2\), hence has at most two
preimages.  Moreover,
\[
(u-A)^2+(z-w)^2=\rho^2
\]
is equivalent to
\[
Y=2wZ+(\rho^2-w^2).
\]
For fixed \(A\), equality of two lifted lines first fixes \(w\) from
the slope and then \(\rho^2\) from the intercept.  Positive radii
therefore give distinct lines for distinct normalized circles.

Thus
\[
I(P_\alpha,\mathcal C_A)
\le
2I(\Phi_A(P_\alpha),\Lambda_A)
\ll
Q^{2/3}N_A^{2/3}+Q+N_A.
\tag{1}
\]
Summing over \(R\) active signed \(A\)'s and using Hölder gives
\[
I(P_\alpha,\mathcal C)
\ll
Q^{2/3}R^{1/3}N^{2/3}+RQ+N.
\tag{2}
\]
No common lift is asserted across different \(A\)'s; (1) is applied
separately, as required.

## 2. Dyadic quantifiers

Start with a mass-carrying \((s,u)\) layer.  Its circle weights are
comparable, so its mass is comparable to \(suN\).

For a signed fibre
\[
(A,b),\qquad b=\rho^2,
\]
let \(\nu(A,b)\) be its number of circles.  Dyadically selecting
\(\nu(A,b)\asymp H\) loses only \(O(\log N)=t^{o(1)}\) in circle
count and hence in mass.  If \(K\) signed fibres survive, then
\[
N\asymp KH,\qquad b_{\rm exp}=c+h.
\tag{3}
\]

No uniformity in the number \(N_A\) of circles per \(A\) is needed
for (2), because Hölder handles arbitrary \(N_A\).  If one wants the
endpoint variables \(J\) and \(j\), a second dyadic selection by the
number of represented fibres per \(A\) again costs only
\(t^{o(1)}\).

A signed fibre \((A,b)\) maps to the geometric tangent--label line
\[
d=b+A^2\tau.
\]
Only \(A\) and \(-A\) can map to the same geometric line, so signed
copies cost a factor at most two.

Every represented line is \(u/2\)-rich.  With
\[
|\mathcal T_\alpha\times\mathcal D_0|
\le t^{3-2\kappa+o(1)}
\]
the rich-line theorem gives two possible exponents
\[
6-4\kappa-3m,\qquad3-2\kappa-m.
\]
Because \(m\le1+o(1)\) and \(\kappa<2/9\), their difference is at
least
\[
1-2\kappa-o(1)>\frac59-o(1).
\]
Hence
\[
c\le6-4\kappa-3m+o(1).
\tag{4}
\]

## 3. Target capacity

Fix one represented fibre \((A,b)\).  Its \(H\) circles have distinct
centre heights \(w\).  Within one circle, distinct producing triples
give distinct target points: an off-axis point fixes its axial plane,
and then \(d=b+y^2\) fixes the label.  Across circles, the height
coordinate differs.

Thus one fibre uses at least \(Hu\) distinct target points in the
ordinary plane \(x=A\).  Select one fibre for every active signed
\(A\).  Distinct \(A\)'s give disjoint planes \(x=A\), while the
entire retained target union has at most \(MQ=t^{4+o(1)}\) points.
Therefore
\[
r+h+m\le4+o(1).
\tag{5}
\]
Equations (3)--(5) imply
\[
\boxed{
r\le10-4\kappa-b-4m+o(1).
}
\tag{6}
\]

Here \(R\) counts signed centre coordinates, not target planes.  It
may exceed \(M\); the proof never assumes \(r\le1\).

## 4. Full global point--circle input

The selected circles remain distinct merged circles in the source
plane.  The global point--circle theorem gives
\[
W
\ll
u\left(
Q^{2/3}N^{2/3}
+Q^{6/11}N^{9/11}t^{o(1)}
+Q+N
\right).
\tag{7}
\]

For \(\kappa<2/9\), the first term could carry only if
\[
m\ge3-5\kappa-o(1)>1,
\]
contrary to \(\mu(C)\le M=t^{1+o(1)}\).  The \(+Q\) term has exponent
at most \(4+o(1)\), while the layer mass is
\(t^{7-3\kappa-o(1)}\).  The \(+N\) term is bounded by the total
triple exponent \(6-2\kappa+o(1)\), which misses by
\(1-\kappa\).

Hence the \(6/11,9/11\) term must carry, giving
\[
\boxed{11a+2b\le18+o(1).}
\tag{8}
\]
Together with
\[
a+b+m\ge7-3\kappa-o(1),\qquad
b+m\le6-2\kappa+o(1),
\tag{9}
\]
this yields
\[
\begin{aligned}
a&\ge1-\kappa-o(1),\\
a&\le\frac{4+6\kappa+2m}{9}+o(1),\\
m&\ge\frac{5-15\kappa}{2}-o(1).
\end{aligned}
\tag{10}
\]

## 5. Audit of all three fixed-\(A\) ST branches

Multiplying (2) by the upper dyadic multiplicity gives
\[
W\ll
u\left(
Q^{2/3}R^{1/3}N^{2/3}+RQ+N
\right).
\tag{11}
\]

### The \(+N\) branch

If it carried, \(a\le o(1)\).  This contradicts
\(a\ge1-\kappa-o(1)\).

### The \(+RQ\) branch

If it carried, then
\[
a+b\le3+r+o(1).
\tag{12}
\]
Using (6), (9), and (12) gives
\[
a\ge1+2m-2\kappa-o(1).
\tag{13}
\]
Combining (13) with the upper bound for \(a\) in (10) yields
\[
m\le\frac{24\kappa-5}{16}+o(1).
\tag{14}
\]
The lower bound in (10) and (14) can coexist only if
\[
\frac{5-15\kappa}{2}
\le
\frac{24\kappa-5}{16}+o(1),
\]
which forces
\[
\kappa\ge\frac5{16}-o(1).
\tag{15}
\]
Thus the \(+RQ\) branch is impossible throughout the much larger
range \(\kappa<5/16\), in particular for \(\kappa<2/9\).

At \(\kappa=2/9\), the gap between the two sides of (14) is exactly
\[
\frac{13}{16}.
\]
This confirms that the branch is not marginal.

### The main branch

The first term of (11) must carry, so
\[
3a+b\le6+r+o(1).
\tag{16}
\]
Using (6) and then the mass inequality gives
\[
a+2m\le2+2\kappa+o(1).
\tag{17}
\]
Since \(a\ge1-\kappa-o(1)\),
\[
m\le\frac{1+3\kappa}{2}+o(1).
\tag{18}
\]
Combining (18) with the lower bound in (10) forces
\[
\frac{5-15\kappa}{2}
\le
\frac{1+3\kappa}{2}+o(1),
\]
or
\[
\boxed{\kappa\ge\frac29-o(1).}
\tag{19}
\]
Every fixed \(\kappa<2/9\) leaves the exact positive gap
\[
2-9\kappa.
\]

## 6. Endpoint and claim boundary

The manuscript's endpoint assignment
\[
(a,b,m,c,h,r)
=
\left(
\frac79,\frac{85}{18},\frac56,
\frac{47}{18},\frac{19}{9},\frac{19}{18}
\right)
\]
saturates (3)--(6), (8)--(10), (16)--(18).  The independent exact
certificate reproduces every equality.

The audit therefore accepts:

- the fixed-\(A\) linearization;
- the strict hub exclusion for every fixed \(\kappa<2/9\);
- the resulting structural matching exponent
  \(2/9-\varepsilon\).

It does not upgrade the result to:

- exclusion at the endpoint \(\kappa=2/9\);
- a Euclidean realization of the endpoint ledger;
- an improvement of the global \(3/5\) distinct-distance exponent;
- a standalone top-quartile paper without a further global
  extraction theorem.

## 7. Reproduction

```bash
cd data/research_open/erdos1083_two_hour_q1_attack_2026-07-30/route_d
python3 verify_two_ninths_audit.py
pytest -q test_verify_two_ninths_audit.py
```
