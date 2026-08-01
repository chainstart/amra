# Red-team audit: primitive lines, tangent separation, and frozen exponents

Date: 2026-08-01

## 0. Verdict

The primitive-direction construction and the
tangent-transversality dichotomy pass an independent line-by-line
reconstruction.  All overlap quantities in the dichotomy are
**ordered** row-pair counts.  Replacing them by unordered counts
changes only a factor of two and none of the frozen exponents.

## 1. Maximal-line partition

Fix a positive direction \(v=(p,q)\) with \(p,q<L\).  A point
\((a,b)\in Q_L\) has no predecessor in the box exactly when

\[
 a<p\quad\text{or}\quad b<q.
\]

The number of starts is therefore

\[
 pL+qL-pq.
\]

Repeatedly adding \(v\) to a start stays in one finite string until
it exits the box.  Conversely, repeatedly subtracting \(v\) from any
box point terminates at one and only one start.  Hence these strings
are disjoint and cover \(Q_L\); no primitivity assumption is needed
for this partition fact.  Primitivity is used later only to choose
one representative of each rational direction.

Every line leaves at most \(S-1\) points, so

\[
 E_v<S\bigl((p+q)L-pq\bigr)<2MSL.
\]

Both \(L^2\) and the covered mass are divisible by \(S\), hence
\(S\mid E_v\).

The remote starts \((2L+j,2L)\) give disjoint blocks.  Equality
between points in two such blocks forces equal step indices from the
second coordinate because \(q>0\), and then equal \(j\)'s from the
first.  Their second coordinates are at least \(2L\), so they cannot
meet the core box.

It follows exactly that

\[
 |V_v|=|V|=L^2=SU,\qquad
 |V_v\cap V|=L^2-E_v,
\]

and

\[
 \frac{|V_v\mathbin\triangle V|}{SU}
 =\frac{2E_v}{L^2}<\frac{4MS}{L}.
\]

For \(v=(1,1)\) and \(S\mid L\), the exact remainder
\(E_v=L(S-1)\) proves that the \(S/L\) boundary scale is attained.

## 2. Primitive-direction count and transversality

If two one-dimensional spaces

\[
 \mathbb Q(p+q\sqrt2),\qquad
 \mathbb Q(p'+q'\sqrt2)
\]

intersect nontrivially, their generators have a rational ratio.
Comparison of the rational and \(\sqrt2\) coefficients makes
\((p,q)\) and \((p',q')\) rationally proportional.  Two primitive
positive integer vectors with this property are equal.

For the count, every non-coprime pair belongs to the set of pairs
whose two coordinates are divisible by some \(d\ge2\).  Thus

\[
\begin{aligned}
 |\mathcal D_M|
 &\ge M^2-\sum_{d=2}^M\lfloor M/d\rfloor^2\\
 &\ge\left(2-\frac{\pi^2}{6}\right)M^2.
\end{aligned}
\]

Multiple counting of non-coprime pairs only weakens this lower bound;
it does not invalidate it.

## 3. Pairwise disjoint tangent sets

A core start has both coefficients below \(L\).  A remote start has
second coefficient \(2L\) and first coefficient

\[
 2L+j<2L+E_v/S<2L+2ML\le4ML.
\]

Therefore the difference of any two starts has rational coefficient
of absolute value below \(4ML\) and \(\sqrt2\)-coefficient of
absolute value at most \(2L\).

For distinct directions \(v=(p,q)\), \(w=(p',q')\),

\[
 z_v^2-z_w^2
 =\frac{(S-1)^2}{4}
 \left[
 p^2+2q^2-p'^2-2q'^2
 +2(pq-p'q')\sqrt2
 \right].
\]

At least one bracket coefficient is a nonzero integer.  Hence at
least one coefficient of \(z_v^2-z_w^2\) has absolute value at least
\((S-1)^2/4\).  Under

\[
 (S-1)^2/4>4ML,
\]

this cannot equal a difference of block starts.  Since

\[
 \tau_v=\bigl(C+\iota(a_v)\bigr)-1-z_v^2,
\]

equality \(\tau_v=\tau_w\) would require precisely that impossible
coefficient equality.  Thus the tangent sets are pairwise disjoint.

The positivity constant also passes:

\[
 z_{p,q}^2<3S^2M^2,\qquad C=10S^2M^2+10,
\]

and all block-start embeddings are nonnegative.

## 4. Frozen exponent table

All exponents below are powers of \(t\).

| Quantity | Calculation | Exponent |
|---|---:|---:|
| \(S\) | frozen | \(7/9=14/18\) |
| \(U\) | frozen | \(5/6=15/18\) |
| \(B=SU\) | \(7/9+5/6\) | \(29/18\) |
| \(q\) | frozen block rows | \(13/18\) |
| \(R\) | tangent universe | \(1=18/18\) |
| \(L=\sqrt B\) | \(29/18\div2\) | \(29/36\) |
| \(L/S\) | \(29/36-28/36\) | \(1/36\) |
| optimized \(M\) | \((L/S)/\omega\) | \(1/36-o(1)\) |
| optimized \(k\) | \(M^2\) | \(1/18-o(1)\) |
| optimized \(|\bigcup T_v|\) | \(kU\) | \(8/9-o(1)\) |
| full row--tangent incidences \(qU\) | \(13/18+15/18\) | \(14/9\) |
| overlap main term \(q^2U^2/R\) | \((26+30-18)/18\) | \(19/9\) |
| diagonal subtraction \(qU\) | \(28/18\) | \(14/9\) |
| one-\(\tau\) transverse pair mass | \(19/9-1\) | \(10/9\) |
| rows supporting those pairs | \((10/9)/2\) | \(5/9\) |
| nontransverse star degree \(qU/R\) | \((13+15-18)/18\) | \(5/9\) |
| pairwise-transverse fixed-\(\tau\) union | \(5/9+7/9\) | \(4/3\) |
| remaining common-spectrum capacity gap | \(29/18-4/3\) | \(5/18\) |

The subtraction \(qU=t^{14/9}\) is lower order than
\(q^2U^2/R=t^{19/9}\), so it does not change \(P_0\)'s leading
exponent.

## 5. Ordered versus unordered conventions

Define

\[
 P_\perp
 =\sum_{\substack{i\ne j\\W_i\cap W_j=\{0\}}}|T_i\cap T_j|
\]

and \(P_\parallel\) analogously.  These sums are over **ordered**
pairs.  Then

\[
 P_\perp+P_\parallel
 =\sum_\tau r_\tau(r_\tau-1).
\]

In the nontransverse branch, dividing \(P_\parallel\) by \(U\)
gives a lower bound for the number of ordered nontransverse row
pairs.  Averaging ordered out-degrees over \(q\) rows gives

\[
 \frac12(qU/R-1).
\]

In the transverse branch, pigeonholing the ordered mass over \(R\)
tangent squares gives \(P_0/(2R)\) ordered transverse pairs on one
\(\tau\).  A support of \(n\) rows has at most \(n(n-1)\) such
ordered pairs, so \(n\ge\sqrt{P_0/(2R)}\) at exponent scale.

If all quantities are instead made unordered, every pair mass and
pair count is divided by exactly two.  The degree and support
conclusions change only by absolute constants.

## 6. Scope

The audit verifies:

- the optimized Følner obstruction;
- its exact tangent-set separation;
- every frozen exponent in the repaired dichotomy; and
- the ordered-pair normalization.

It does not prove that either repaired branch contradicts the global
few-distance hypothesis.
