# High-energy radius branch: an elementary overlap dichotomy

Date: 2026-07-29

## Scope

This note treats the remaining case from
`GEOMETRIC_RADIUS_HIGH_ENERGY.md`: geometric-progression radii with height
sets that may vary independently and need not lie in a thin slab.

It proves an exact second-order energy dichotomy.  An anomalously small
parameter-line count forces a quantitatively large sum of cross-correlations
between squared height-difference sets.  It also closes a discrete subcase
in which these correlations have a uniform divisor bound.

It does not prove that high correlation forces common translates or
reflections of the height sets.  That inverse step remains open.

## Setup

Let
\[
 \rho_u=Tq^u,\qquad 0\leq u<L,
\]
and let \(Z_u\subset\mathbb R\) be arbitrary nonempty finite height sets.
For a radius pair \(e=(u,v)\), \(u\leq v\), put
\[
 p(e)=u+v,\quad
 C_e=T^2(q^u-q^v)^2,\quad
 Y_e=(Z_u-Z_v)^2,\quad
 S_e=C_e+Y_e.
\]
Pairs with different \(p\) have different product parameter \(B\).  Hence
the total parameter-line count is
\[
 M=\sum_p\left|\bigcup_{e:p(e)=p}S_e\right|. \tag{1}
\]
Define
\[
 I=\sum_e|Y_e|
\]
and the ordered cross-correlation mass
\[
 {\cal K}
 =\sum_p\ \sum_{\substack{e\ne f\\p(e)=p}}
 |S_e\cap S_f|. \tag{2}
\]
Equivalently, each summand in (2) is
\[
 |Y_e\cap(Y_f+C_f-C_e)|. \tag{3}
\]

## Theorem 1 (exact second-order stability)

The quantities above satisfy
\[
 M\geq \frac{I^2}{I+{\cal K}}. \tag{4}
\]
Moreover,
\[
 I\geq\frac{L+1}{4}F,\qquad
 F=\sum_u|Z_u|. \tag{5}
\]
Consequently, for every \(K>1\),
\[
 M\leq\frac{I}{K}
 \quad\Longrightarrow\quad
 {\cal K}\geq(K-1)I. \tag{6}
\]

Thus a factor-\(K\) failure of the natural \(M\asymp I\) line count forces
at least a factor-\(K\) excess of shifted squared-difference correlations.

### Proof

For each \(p\), let \(r_p(x)\) be the number of blocks \(S_e\), \(p(e)=p\),
that contain \(x\).  Then
\[
 \sum_{p,x}r_p(x)=I
\]
and
\[
 \sum_{p,x}r_p(x)^2
 =I+{\cal K}. \tag{7}
\]
Cauchy--Schwarz, first within the disjoint \(p\)-labelled union and then
globally, gives
\[
 I^2
 \leq
 \left(\sum_p|\{x:r_p(x)>0\}|\right)
 \left(\sum_{p,x}r_p(x)^2\right)
 =M(I+{\cal K}),
\]
which proves (4).

For arbitrary finite \(U,V\subset\mathbb R\),
\[
 |(U-V)^2|\geq\frac12\max\{|U|,|V|\}.
\]
Therefore
\[
\begin{aligned}
 I
 &\geq\frac12\sum_{u\leq v}\max\{|Z_u|,|Z_v|\}\\
 &\geq\frac14\sum_{u\leq v}(|Z_u|+|Z_v|)
 =\frac{L+1}{4}F,
\end{aligned}
\]
proving (5).  Rearranging (4) under the hypothesis in (6) proves the final
claim. \(\square\)

## Corollary 2 (bounded-correlation criterion)

Let
\[
 R=\max_{\substack{e\ne f\\p(e)=p(f)}}|S_e\cap S_f|
\]
and
\[
 H_L=\sum_p t_p(t_p-1),\qquad
 t_p=|\{e:p(e)=p\}|.
\]
Then
\[
 M\geq\frac{I^2}{I+RH_L}. \tag{8}
\]
For geometric-progression indices, \(H_L=\Theta(L^3)\).  In the balanced
case \(F\asymp L^2\), if \(R\leq F^{o(1)}\), equations (5) and (8) give
\[
 M\geq F^{3/2-o(1)}. \tag{9}
\]

This is an elementary, explicit substitute for an unavailable full inverse
theorem: it states exactly how much pairwise height-difference correlation
must be ruled out.

## Corollary 3 (integer-height divisor bound)

Assume \(q,T\) and every height are integers.  For distinct \(e,f\) with the
same product exponent, put
\[
 \delta_{ef}=C_f-C_e\ne0.
\]
Then
\[
 |S_e\cap S_f|\leq\tau(|\delta_{ef}|), \tag{10}
\]
where \(\tau\) is the positive-divisor function.  Consequently (8) holds
with
\[
 R=\max_{e\ne f,\ p(e)=p(f)}\tau(|\delta_{ef}|). \tag{11}
\]

### Proof

An element of \(S_e\cap S_f\) gives squared integer differences \(a^2\in
Y_e\), \(b^2\in Y_f\) satisfying
\[
 a^2-b^2=\delta_{ef}.
\]
Thus
\[
 (a-b)(a+b)=\delta_{ef}.
\]
Each factor pair determines at most one pair of nonnegative values
\((|a|,|b|)\), so the number of distinct squared-value pairs is at most
\(\tau(|\delta_{ef}|)\).  Each common value in the intersection determines
one such pair, proving (10). \(\square\)

This corollary is deliberately stated with the exact quantity \(R\).  The
generic bound \(\tau(n)=n^{o(1)}\) does not automatically imply
\(R=F^{o(1)}\) when the coordinates themselves can be exponentially large
in \(F\).  Polynomial coordinate height, or a direct divisor estimate for
the particular radial offsets, is an additional condition.

## What high correlation does and does not imply

By (3), a large summand supplies many distinct solutions of
\[
 y-y'=C_f-C_e,\qquad
 y\in(Z_u-Z_v)^2,\quad y'\in(Z_{u'}-Z_{v'})^2. \tag{12}
\]
Equivalently, after choosing signs,
\[
 (z-w-z'+w')(z-w+z'-w')=C_f-C_e. \tag{13}
\]
This is the exact algebraic input for a future inverse theorem.

However, large set-level correlation in (12) alone does not yet prove that
the four height sets are approximate translates or reflections.  Such a
conclusion must also control representation multiplicities inside the
difference sets.  The current rigorous endpoint is therefore:

1. either \(M\) has the desired near-\(FL\) size;
2. or the explicit correlation mass \({\cal K}\) is large as in (6);
3. and an additional inverse argument must convert that mass into common
   height structure or a separate distance expansion.

No BSG-type conclusion is asserted here.

### Proposition 4 (one-pair inverse no-go)

Arbitrarily large correlation for one pair of blocks does not force even
exact translate/reflection structure.  For \(h\geq3\), set
\[
 A=\{\cosh j:1\leq j\leq h\},\qquad
 B=\{\sinh j:1\leq j\leq h\}.
\]
The squared difference sets generated by the height-set pairs
\((A,\{0\})\) and \((B,\{0\})\) have at least \(h\) correlated values because
\[
 \cosh^2j-\sinh^2j=1.
\]
Both sets are strictly increasing.  A translation would have to match their
ordered elements, but
\(\cosh j-\sinh j=e^{-j}\) is nonconstant.  A reflected translation would
reverse the order; its sums at the two endpoints differ because
\[
 (\cosh1+\sinh h)-(\cosh h+\sinh1)=e^{-1}-e^{-h}>0.
\]
Thus neither exact relation is possible.

This example does not contradict a network-level inverse theorem using many
overlapping radius pairs.  It shows why Theorem 1 records total correlation
without promoting a single large summand to common height structure.

## Computational falsification

`verify_high_energy_overlap_stability.py` checks identities (1), (2), and
(7), the Cauchy bound (4), the divisor bound (10), and deterministic
adversarial searches with independently mutable integer height sets.

The tested balanced configurations did not show a decreasing
\(M/F^{3/2}\) trend.  Common arithmetic progressions remained the best
configurations found by the local search.  This is experimental evidence
only and is not used in any theorem above.
