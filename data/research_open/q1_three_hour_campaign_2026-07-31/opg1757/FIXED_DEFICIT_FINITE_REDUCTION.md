# Fixed-deficit finite rational reduction

Date: 2026-07-31

This note extracts the uniform statement justified by the two OPG attacks.
It is a finite-reduction theorem, not an arbitrary-depth positivity theorem.

## 1. Quantifiers and notation

Fix an integer
\[
q\ge0
\]
independently of \(s\), and put
\[
n=2s-5-q.
\tag{1}
\]
For a completely stable incidence interpretation it is enough to assume
\[
s\ge6q+4.
\tag{2}
\]
Indeed, excess at most \(2q\) uses at most \(3(2q)=6q\) previously
untouched unit blocks, and the two doubled core blocks leave \(s-4\) unit
blocks.  The resulting rational identities extend algebraically wherever
the original profiles exist: unavailable incidence types carry a zero
falling factorial.  The explicit bound (2) is therefore a convenient safe
quantifier, not an optimized threshold and not a restriction on finite
certificate values.

The support bounds give
\[
2n=4s-10-2q
\le\deg_\beta B_n\le4s-10.
\tag{3}
\]
Thus there are \(2q+1\) possible coefficients, indexed by
\[
0\le r\le2q.
\]

## 2. Uniform overlap/excess formula

Let \(\mathcal H_{h,e}(x)\) be the complete hyperforest EGF of excess
\(e\) from the core profile with \(h\) doubled blocks.  The ordered-chain
identity and binomial-basis overlap formula give
\[
\boxed{
\begin{aligned}
\frac{[\beta^{2n+r}]B_n}{n!}
={}&
\sum_{\ell=0}^{\lfloor r/2\rfloor}\frac1{\ell!}
\sum_{\substack{e+f+a=r-2\ell\\0\le a\le q+1-\ell}}
\binom{q+1-\ell}{a}s^a\\
&\quad\times[x^{n-\ell}]
\left(
\mathcal H_{1,e}^{(\ell)}
\mathcal H_{1,f}^{(\ell)}
-
\mathcal H_{0,e}^{(\ell)}
\mathcal H_{2,f}^{(\ell)}
\right).
\end{aligned}
}
\tag{4}
\]
Here
\[
2s-4-j-k=q+1-\ell
\]
is the exponent of \(\lambda=1+s\beta\), and
\[
r=2\ell+e+f+a.
\tag{5}
\]
All sums in (4) are finite once \(q\) is fixed.

If the left and right hyperforests have \(c,d\) components, their orders
force
\[
c+d+e+f=3+q-\ell.
\tag{6}
\]
Therefore only the endpoint set
\[
\boxed{
\mathcal E_q
=\left\{
(h,e,c):
h\in\{0,1,2\},\
0\le e\le \min(2q,q+1),\
1\le c\le q+2-e
\right\}
}
\tag{7}
\]
can occur.  Its cardinality is
\[
|\mathcal E_q|
=
\begin{cases}
6,&q=0,\\[1mm]
\dfrac{3(q+2)(q+3)}2,&q\ge1.
\end{cases}
\tag{8}
\]
For \(q=2\), this is exactly the 30-entry second-attack table.

## 3. Endpoint certificate size

The denominator-aware Abel lemma proves
\[
\frac{H_{h,e,c}}
{2^h s^{s-h-2c-e}}
=\frac{N_{h,e,c}(s)}{s^e},
\qquad
\deg N_{h,e,c}\le2c+3e-2.
\tag{9}
\]
Consequently one endpoint requires
\[
2c+3e-1
\tag{10}
\]
stable exact values.  Summing (10) over (7) gives the closed count
\[
\boxed{
M(q)
=
\begin{cases}
12,&q=0,\\[1mm]
\dfrac{(q+2)(q+3)(5q+8)}2,&q\ge1.
\end{cases}
}
\tag{11}
\]
For \(q=2\), \(M(2)=180\).

This establishes a finite algorithm for every fixed \(q\):

1. enumerate the finitely many excess partitions \(e\le q+1\);
2. enumerate their finite contraction incidence types;
3. evaluate the endpoints in (7) at the counts (10);
4. reconstruct the cleared numerators using (9);
5. substitute them into (4).

The algorithm is exact and terminates for each fixed \(q\).

## 4. Final coefficient degree bound

Define
\[
C_{q,r}(s)
=
\frac{[\beta^{2n+r}]B_n}
{n!\,s^{2s-8-2q+r}}.
\tag{12}
\]
The common power in (12) follows from (5)--(6).  For a term of (4), put
\(E=e+f\).  Its two endpoint denominators divide \(s^E\), hence the
whole coefficient denominator divides \(s^r\).

After taking the common denominator \(s^r\), the numerator degree is at
most
\[
\begin{aligned}
&\bigl(2c+3e-2\bigr)
+\bigl(2d+3f-2\bigr)
+2\ell+(r-E)\\
&\qquad
=2(c+d)+2E+2\ell+r-4\\
&\qquad
=2q+r+2,
\end{aligned}
\tag{13}
\]
where \(2\ell\) is the degree of the two falling factorials created by
the derivatives and the last equality uses (6).

Thus:
\[
\boxed{
C_{q,r}(s)=\frac{R_{q,r}(s)}{s^r},
\qquad
\deg R_{q,r}\le2q+r+2.
}
\tag{14}
\]
A proposed closed formula for one coefficient is therefore determined by
\[
\boxed{2q+r+3}
\tag{15}
\]
stable exact values.  Alternatively, taking the common denominator
\(s^{2q}\) for all \(r\) gives the uniform numerator bound \(4q+2\), so
\(4q+3\) values per coefficient suffice.

The subsequently proved endpoint top-two theorem
(`../OPG_ENDPOINT_TOP_TWO_THEOREM.md`) cancels the two apparent leading
degrees in (13) and sharpens (14) to
\[
\deg R_{q,r}\le2q+r.
\tag{16}
\]
Thus only \(2q+r+1\) values are needed before using any forced boundary
factor.  The older bound above remains a valid self-contained consequence
of the denominator-aware endpoint lemma.

## 5. What the theorem does and does not prove

Equations (7), (11), and (14) prove a finite rational reduction for every
fixed depth deficit \(q\).  They explain why the \(q=2\) layer can be
closed by a finite exact certificate.  The \(q=3\) route has now been
executed in `FOURTH_ATTACK_Q3.md`: 45 endpoint identities, 345 exact
endpoint values, and all seven beta-offset formulas prove \(B_{2s-8}\).
The same reduction is executed at \(q=4\) in `FIFTH_ATTACK_Q4.md`, with
63 endpoints, 588 endpoint values, and nine beta-offset formulas.
At \(q=5\), `SIXTH_ATTACK_Q5.md` uses the full, count-consistent
84-endpoint/924-value table and closes all eleven beta offsets.
At \(q=6\), `SEVENTH_ATTACK_Q6.md` uses all 108 endpoints and 1,368
endpoint values, closes all thirteen offsets, and combines the sharper
bound (16) with three forced boundary roots for a 208-value independent
certificate.

They do **not** show that \(R_{q,r}\) is nonnegative, that the denominator
cancels for every \(q\), or that all pooled depths are positive.  Any
positivity claim still requires the reconstructed numerator signs to be
proved.
