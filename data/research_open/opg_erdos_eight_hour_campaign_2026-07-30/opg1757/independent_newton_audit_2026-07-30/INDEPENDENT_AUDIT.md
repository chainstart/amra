# Independent audit of the first/second active Newton theorem

Date: 2026-07-30

Audited source (read-only):
`../FIRST_ACTIVE_NEWTON_THEOREM.md` and its companion verifier.

## Verdict

**Theorem-level verdict: PASS.**  Formulas (1), (1a)--(1c), and the
claimed strict signs are correct under the stated forest-polynomial
definition and normalization.  I found no sign, orbit-factor,
normalization, or boundary-case error.

**Counting-lemma verdict: PASS.**  The exponent in (2), the Liu--Chow
specializations, the adjacent/disjoint edge-pair identity, the rows in
(3), and the determinant layers (8), (9), (13), and (14) all survive
independent derivation and complete small-instance enumeration.

**Hypothesis-level qualification.**  The polynomial-degree bound and
the connection of this normalized coefficient to the larger
complete-split/OPG reduction are inherited by the note and were not
reproved here.  They are not needed for the local counting identities.
The purportedly imported capacity cancellation (10) is independently
proved below, so the first-support assertion itself is not conditional
on an unchecked computational observation.

There is one minor exposition omission, not a mathematical error:
the use of (17) also needs \(R(n)=n^2+2n-27>0\), which is immediate for
\(n\ge7\).  Stating this explicitly would make the inequality direction
fully transparent.

## 1. Independent reconstruction of the exponent

An \(n\)-vertex forest with \(c\) components has \(n-c\) edges.  If it
contains a prescribed matching of size \(h\), deleting the \(h\) forced
edge factors leaves degree
\[
(n-c)-h=n-h-c.
\]
Thus
\[
\Phi_h(x)=\sum_c W_{h,c}(n)x^{n-h-c}
\]
has exactly the exponent in (2).

Both products in the determinant have the same exponent:
\[
\begin{aligned}
\Phi_1^2 &: (n-1-c_1)+(n-1-c_2),\\
\Phi_0\Phi_2 &: (n-c_1)+(n-2-c_2).
\end{aligned}
\]
Consequently the coefficient of \(x^k\) has
\[
c_1+c_2=2n-2-k.                                      \tag{A1}
\]
This confirms that total component counts \(3,4,5,6\), rather than a
shifted set of layers, are used at the relevant evaluations.

## 2. Liu--Chow and the one-edge row

Formula (4) can be recovered without taking the cited formula on faith.
Let \(T(z)\) be the exponential generating function of rooted labeled
trees, so \(T=ze^T\), and let
\[
U(z)=T(z)-\frac{T(z)^2}{2}
\]
be the EGF of unrooted labeled trees.  A forest with \(c\) unordered
components therefore has count
\[
W_{0,c}(n)=\frac{n!}{c!}[z^n]U(z)^c.
\]
Lagrange inversion applied to
\(u^c(1-u/2)^c\) gives
\[
W_{0,c}(n)
=\frac{(n-1)!}{(c-1)!}
[u^{n-c}](1-u/2)^{c-1}(1-u)e^{nu}.                 \tag{A2}
\]
Expand only \((1-u/2)^{c-1}\).  For its \(u^r\) term, the factor
\((1-u)e^{nu}\) contributes
\[
\frac{n^{n-c-r}}{(n-c-r)!}
-\frac{n^{n-c-r-1}}{(n-c-r-1)!}
=\frac{(c+r)n^{n-c-r-1}}{(n-c-r)!}.
\]
Substitution in (A2) is exactly (4), including the factor \(c+r\), the
power \(n^{n-c-r-1}\), and the upper factorial range.

Direct substitution of \(c=1,2,3\) into (4) gives
\[
\begin{aligned}
W_{0,1}&=n^{n-2},\\
W_{0,2}&=\frac{(n-1)(n+6)}2n^{n-4},\\
W_{0,3}&=\frac{(n-2)(n-1)(n^2+13n+60)}8n^{n-6}.
\end{aligned}
\]
No orbit factor is present in the Liu--Chow formula: these count all
unrooted spanning forests, not a forest with an ordered component.

Every such forest has \(n-c\) edges.  Double-counting pairs
\((T,e)\), with \(e\) an edge of \(T\), gives
\[
\binom n2 W_{1,c}=(n-c)W_{0,c}.
\]
This reproduces the full \(h=1\) row of (3).

## 3. Adjacent and disjoint edge pairs

The number of unordered adjacent edge pairs is
\[
n\binom{n-1}{2}=\frac{n(n-1)(n-2)}2.
\]
The number of unordered disjoint edge pairs is
\[
3\binom n4=\frac{n(n-1)(n-2)(n-3)}8.
\]
Contracting a prescribed adjacent pair creates one vertex of weight
\(3\).  Expanding its weighted complete-graph forest count gives (12);
at \(c=1,2,3\) it simplifies exactly to (6).

A \(c\)-component forest contains
\(\binom{n-c}{2}\) unordered pairs of its own edges.  Splitting them
into the two orbits therefore gives
\[
N_{\rm adj}A_c+N_{\rm dis}W_{2,c}
=\binom{n-c}{2}W_{0,c},                              \tag{A3}
\]
with no missing factor of \(2\).  Solving (A3) reproduces all three
\(h=2\) entries of (3).  In particular,
\[
W_{2,1}=4n^{n-4},
\]
which is also the weighted Cayley count after contracting two disjoint
edges.

## 4. First support and the cancellation below it

Write \(q_0=\lfloor(k-2)/2\rfloor\) and evaluate at \(n=4+q\).

If \(k=2m+3\), then for \(q<q_0=m\), (A1) gives
\[
c_1+c_2\le1,
\]
which is impossible because both component counts are positive.

If \(k=2m+2\), all evaluations with \(q<m-1\) are likewise empty.  At
the final evaluation below support, \(q=m-1\), the total component
count is \(2\), so only \((c_1,c_2)=(1,1)\) occurs.  Its determinant is
\[
\begin{aligned}
W_{1,1}^2-W_{0,1}W_{2,1}
&=(2n^{n-3})^2-(n^{n-2})(4n^{n-4})\\
&=0.                                                   \tag{A4}
\end{aligned}
\]
This proves (10) for all \(k\), including the only nonempty
below-support layer.

At \(n_0=4+q_0\), (A1) gives total component count \(3\) for odd \(k\)
and \(4\) for even \(k\).  Direct substitution of (3) gives
\[
\mathcal C_3(n)=4n^{2n-8},
\qquad
\mathcal C_4(n)=4(n^2+4n-24)n^{2n-10}.
\]
These are (8) and (9).  Multiplication by
\[
\frac{k!}{2k(k-1)}=\frac{(k-2)!}{2}
\]
then gives exactly (1), including the negative-power presentation at
\(k=2\), which simplifies to \(1\).

## 5. The next forward difference

For a base-four Newton expansion,
\[
a_{k,q}=\Delta^q c_k(4).
\]
At \(q=q_0+1\), all terms before the final two vanish by (10).  Their
binomial coefficients and signs are
\[
\binom{q_0+1}{q_0}(-1)^1=-(q_0+1),
\qquad
\binom{q_0+1}{q_0+1}=1.
\]
Therefore
\[
a_{k,q_0+1}
=\frac{(k-2)!}{2}
\left(C_k(n_0+1)-(q_0+1)C_k(n_0)\right),
\]
confirming both the coefficient and the minus sign in (15).

Independent symbolic substitution of (4), (5), (7), and (12) through
total component counts \(5\) and \(6\) gives
\[
\mathcal C_5(n)
=2(n-4)(n^3+12n^2+20n-225)n^{2n-12},
\]
\[
\mathcal C_6(n)
=\frac23(n-4)Q(n)n^{2n-14}.
\]
In the odd case, \(q_0+1=n-4\) and the previous evaluation is \(n-1\);
factoring the resulting expression gives (1b).  In the even case,
\[
(n-1)^2+4(n-1)-24=n^2+2n-27=R(n),
\]
which gives (1c).  Thus the powers of both \(n\) and \(n-1\) in
(1b)--(1c) are correct.

## 6. Sign audit for (16) and (17)

For odd \(k\), factor \(n^{2n-12}\) from the bracket in (1b).  The
remaining expression is
\[
P(n)-2(n-1)^2
\left(1-\frac1n\right)^{2n-12}.
\]
Since the ratio is at most \(1\),
\[
\text{bracket}\ge
P(n)-2(n-1)^2
=n^3+10n^2+24n-227>0
\]
for \(n\ge6\).  The excluded case \(n=5\), equivalently \(k=3\), is
the directly checked value \(10\).

For even \(k\), \(n\ge7\) implies
\[
R(n)=n^2+2n-27>0.
\]
After factoring \(n^{2n-14}/3\), the same ratio bound reduces positivity
to
\[
Q(n)-6(n-1)^2R(n)>0.
\]
With \(n=m+5\), this is exactly
\[
m^5+35m^4+502m^3+3123m^2+4556m+1107>0.
\]
This confirms (17) and its inequality direction.  The remaining case
\(n=6\), equivalently \(k=4\), is \(294\).

## 7. Independent exhaustive regression

`independent_verify_newton.py` enumerates every edge subset of \(K_n\)
for \(4\le n\le7\), rejects cycles with a disjoint-set structure, and
counts forests containing:

1. no prescribed edge;
2. one prescribed edge;
3. two prescribed disjoint edges; and
4. two prescribed adjacent edges.

It does not use contraction, weighted Cayley recursion, or the source
verifier.  The enumeration confirms:

- 36 entries against (3), (4), and (12);
- 12 adjacent/disjoint orbit identities;
- 16 determinant layers for total component counts \(3\) through \(6\);
- formulas (1), (1b), and (1c) for \(2\le k\le7\).

The exact boundary data are
\[
\begin{array}{c|c|c|c}
k&q_0&(c_k(4),c_k(5),c_k(6))&
(a_{k,q_0},a_{k,q_0+1})\\ \hline
2&0&(1,1)&(1,\text{not active})\\
3&0&(2,12)&(2,10)\\
4&1&(0,84,462)&(84,294).
\end{array}
\]

Reproduction:

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/opg1757/independent_newton_audit_2026-07-30
pytest -q test_independent_verify_newton.py
python3 independent_verify_newton.py
```
