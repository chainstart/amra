# Independent audit — reverse rank-18 barrier

Date: 2026-07-30

## Verdict

**PASS as an exact reduction; OPEN as an all-\(V\) barrier.**

I independently reconstructed the zero basin, both comparisons with
\(P_{18}\), the forward-complement indexing, and the canonical expansion in
(5.7).  I found no reversed Galois inequality, off-by-one shadow rank, or
incorrect binomial identity.

The central boundary is:

\[
\boxed{
D_{18}\le B_{18}
\iff
\text{the reverse orbit is legal at every step and terminates at zero}.
}
\]

Thus the reverse computation does not prove the barrier until legality
\(b_q\ge V\) has been proved independently.  Using the observed terminal
zero to justify the intermediate subtractions would be circular.

All statements below are safely scoped to the advertised range \(V\ge70\).
Several algebraic statements hold from \(V\ge31\), and the canonical display
(5.7) is valid in its printed four-term form from \(V\ge34\).

## 1. Galois adjunction and the zero basin

For the \(q\)-canonical expansion, let \(U_q\) raise the lower index and
\(\operatorname{KK}_{q+1}\) take the lower shadow.  The adjunction is
\[
U_q(x)\ge y
\iff
x\ge\operatorname{KK}_{q+1}(y).
\tag{1}
\]
Negating (1) and using integrality gives
\[
U_q(x)\le y-1
\iff
x\le\operatorname{KK}_{q+1}(y)-1.
\tag{2}
\]
The direction and the two minus-one terms are correct.

Let
\[
D_{V-12}=0,\qquad E_{V-12}=1,
\]
with both orbits descended by
\[
Y_q=V+\operatorname{KK}_{q+1}(Y_{q+1}).
\]
At the top reverse rank, the zero basin is
\[
\{0\}=[D_{V-12},E_{V-12}-1].
\]
If the basin at \(q+1\) is
\([D_{q+1},E_{q+1}-1]\), then \(x\) is in the basin at \(q\) exactly when
\[
D_{q+1}\le U_q(x-V)\le E_{q+1}-1.
\]
Equations (1)--(2) convert this to
\[
V+\operatorname{KK}_{q+1}(D_{q+1})
\le x\le
V+\operatorname{KK}_{q+1}(E_{q+1})-1,
\]
namely
\[
\boxed{\mathcal I_q=[D_q,E_q-1]\cap\mathbb Z.}
\tag{3}
\]

There is no legality gap inside this induction.  For \(q\le V-13\),
\(D_q\ge V\), so every \(x\) in (3) can be subtracted by \(V\); its image
belongs to the next basin by construction.

**Classification:** (3) is an all-parameter theorem.  Applying it to the
specific symbolic number \(B_{18}\) still requires locating that number
inside the interval.

## 2. Independent comparison \(B_{18}<P_{18}<E_{18}\)

Write
\[
P_q=\binom{V-12}{q}+\binom{V-13}{q-1}.
\]
The sum in \(B_{18}\) satisfies
\[
\sum_{i=4}^{17}\binom{V-31+i}{i}
=
\binom{V-13}{17}
-1-(V-30)-\binom{V-29}{2}-\binom{V-28}{3}.
\]
Substitution and two Pascal differences give
\[
\boxed{
P_{18}-B_{18}
=V-28+2\binom{V-29}{2}+\binom{V-30}{2}.
}
\tag{4}
\]
This is positive for \(V\ge31\).

The seeded upper orbit starts one unit above the zero orbit.  At rank
\(V-13\),
\[
E_{V-13}
=V+\operatorname{KK}_{V-12}(1)
=2V-12,
\]
whereas
\[
P_{V-13}
=\binom{V-12}{V-13}+\binom{V-13}{V-14}
=2V-25.
\]
The displayed two terms of \(P_q\) are canonically separated and
\[
\operatorname{KK}_q(P_q)=P_{q-1}.
\]
Consequently, if \(E_q\ge P_q\), then
\[
E_{q-1}
=V+\operatorname{KK}_q(E_q)
\ge V+P_{q-1}>P_{q-1}.
\]
Descending to rank 18 proves
\[
\boxed{B_{18}<P_{18}<E_{18}.}
\tag{5}
\]

Because the quantities are integral, (5) supplies
\(B_{18}\le E_{18}-1\).  Hence (3) reduces the reverse test to its lower
edge:
\[
\boxed{
B_{18}\in\mathcal I_{18}
\iff D_{18}\le B_{18}.
}
\tag{6}
\]

**Classification:** (4)--(6), including the upper edge, are all-parameter
theorems.  The lower inequality \(D_{18}\le B_{18}\) is open.

## 3. Legality is equivalent to the open barrier

Start \(b_{18}=B_{18}\) and define
\[
b_{q+1}=U_q(b_q-V).
\]
The recurrence is defined only while \(b_q\ge V\).  Since (5) has already
placed the start below the upper basin edge, every legal step also stays
below the corresponding upper edge.

At rank \(V-13\), legality and the upper basin bound give
\[
V\le b_{V-13}\le E_{V-13}-1=2V-13.
\]
Thus
\[
0\le b_{V-13}-V\le V-13,
\]
whose \(U_{V-13}\)-image is zero.  Therefore
\[
\boxed{
b_q\ge V\ (18\le q\le V-13)
\iff D_{18}\le B_{18}.
}
\tag{7}
\]

The experimentally stronger identity \(b_{V-13}=V\) is unnecessary and
is not proved for every \(V\).  Finite arithmetic shows the proposed
barrier succeeds from the tested transition near \(V=69\), while it fails
for many smaller values.  This is falsifier information only.

**Circularity warning:** one may not symbolically run the recurrence to zero
and then infer that all prior subtractions were legal.  By (7), proving that
legality is exactly proving the desired lower barrier.

## 4. The two formulas for \(P_{18}-B_{18}\)

The shorter formula is
\[
\boxed{
P_{18}-B_{18}
=\binom{V-27}{3}-\binom{V-30}{3}+1.
}
\tag{8}
\]
Indeed, the right side of (8) is
\[
\binom{V-28}{2}+\binom{V-29}{2}
+\binom{V-30}{2}+1.
\]
Using
\[
\binom{V-28}{2}
=\binom{V-29}{2}+V-29
\]
recovers (4).  The two formulas are identical, not competing bounds.

Since \(X_{18}=P_{18}-D_{18}\), the barrier is equivalently
\[
\boxed{
X_{18}\ge
\binom{V-27}{3}-\binom{V-30}{3}+1.
}
\tag{9}
\]

**Classification:** the identity (8) and equivalence (9) are exact
all-parameter statements.  Inequality (9) for the actual orbit remains
open.

## 5. Forward-slack complement identity

Put
\[
n=V-11,\qquad R=n-q,\qquad X_q=P_q-D_q.
\]
Pascal gives
\[
P_q
=\binom nq-\binom{n-2}{q-2}.
\tag{10}
\]
Inside a canonical tail-complement chart, the complement identity has the
correct index
\[
\operatorname{KK}_q(P_q-X_q)
=P_{q-1}-U_{R-1}(X_q).
\tag{11}
\]
Subtracting the forward recurrence for \(D\) from \(P_{q-1}\) yields
\[
\boxed{X_{q-1}=U_{R-1}(X_q)-V.}
\tag{12}
\]

The index \(R-1=n-q-1\) is correct.  At \(q=V-13\), it equals one and
\[
X_{V-13}=P_{V-13}-V=V-25,
\]
which is consistent with (12).

Equation (12) is exact only while the complement chart is separated.
Continuing it across a re-canonicalization requires a carry-transition
lemma.  The document states this limitation correctly.  Treating (12) as a
single global scalar recurrence would reproduce the same legality
circularity as the reverse orbit.

**Classification:** (10)--(12) are all-parameter identities on every
specified separated chart.  The assertion that the actual orbit remains in
one adequate sequence of charts down to rank 18 is open.

## 6. Canonical expansion (5.7)

At rank 18,
\[
R-1=V-30.
\]
The threshold in (9) has the exact expansion
\[
\begin{aligned}
\binom{V-27}{3}-\binom{V-30}{3}+1
={}&
\binom{V-28}{V-30}
+\binom{V-29}{V-31}\\
&+\binom{V-30}{V-32}
+\binom{V-33}{V-33}.
\end{aligned}
\tag{13}
\]
The lower indices decrease by one, and the upper indices are strictly
decreasing:
\[
V-28>V-29>V-30>V-33.
\]
Moreover, the next possible first term
\(\binom{V-27}{V-30}=\binom{V-27}{3}\) is strictly larger than the
threshold.  Repeating this check after each subtraction confirms that
(13) is the greedy \((V-30)\)-canonical expansion, not merely a binomial
sum.

There is one wording qualification.  Equation (13) is the canonical
expansion of the **threshold**.  The open inequality \(X_{18}\ge\) threshold
does not force the canonical expansion of \(X_{18}\) to have these four
terms as an identical literal prefix: \(X_{18}\) may instead cross the
threshold with a larger earlier digit.  Thus “canonical-prefix target”
should mean domination of the canonical word in colex order, or a
sufficient invariant that enforces the displayed prefix, not a necessary
equality of prefixes.

**Classification:** (13) is an all-parameter theorem.  The claim that the
actual \(X_{18}\) dominates this canonical threshold is exactly the open
barrier.

## 7. Independent exact checks

Using an ordinary greedy combinadic implementation, independently of the
reverse-barrier prose, I checked:

- the adjunction (1) for ranks \(1,\ldots,8\), \(0\le x<300\), and
  \(0\le y<100\);
- equality of (4) and (8) at
  \(V=31,32,33,34,40,68,69,70,100,175,379\);
- \(B_{18}<P_{18}<E_{18}\) at the same parameters;
- the equivalence between basin membership and legal termination;
- the exact canonical expansion (13) from its legal four-term range;
- the forward complement index on actual finite orbit charts.

The checks reproduce the lower-cutoff phenomenon: \(V=40,\ldots,68\)
contains failures of the proposed lower barrier, while the tested values
from \(V=69\) onward pass.  No finite range is extrapolated.

## 8. Final claim ledger

| Statement | Status |
|---|---|
| Galois adjunction with the strict upper form | **ALL-PARAMETER THEOREM** |
| Zero-basin interval \(\mathcal I_q=[D_q,E_q-1]\) | **ALL-PARAMETER THEOREM** |
| \(B_{18}<P_{18}<E_{18}\) | **ALL-PARAMETER THEOREM** |
| Both formulas for \(P_{18}-B_{18}\) | **ALL-PARAMETER IDENTITY** |
| Forward-slack recurrence inside a separated complement chart | **ALL-PARAMETER CHART IDENTITY** |
| Canonical expansion (5.7) of the numerical threshold | **ALL-PARAMETER THEOREM** |
| Reverse orbit is legal and ends at zero iff \(D_{18}\le B_{18}\) | **ALL-PARAMETER EQUIVALENCE** |
| \(D_{18}\le B_{18}\) for every \(V\ge70\) | **OPEN** |
| \(b_q\ge V\) at every reverse rank for every \(V\ge70\) | **OPEN / EQUIVALENT BARRIER** |
| Actual \(X_{18}\) dominates the threshold in (5.7) for every \(V\ge70\) | **OPEN / EQUIVALENT BARRIER** |
| \(b_{V-13}=V\) for every \(V\ge70\) | **FINITE EVIDENCE ONLY** |

The reverse formulation is therefore mathematically sound and sharper than
a numerical pattern, but it has not shortened the universal proof obligation
below the lower-edge inequality itself.
