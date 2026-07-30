# Resonant multistars: exact optimization and a logarithmic infinite family

## 1. Question and outcome

Round 27 produced a resonant star: one translated cross edge can have
linearly many partners.  That does not imply that the average partner
degree

\[
\overline d(A)=\frac{H_{X,Y}(A)}{|A|^2}
\]

grows.  This round separates the two phenomena.

There are three conclusions.

1. Exhaustive finite-universe optimization through subset size \(12\)
   finds no dense network in the natural SAT-star candidates.  Its largest
   average is \(95/81\).
2. Rational translations under the actual SAT parameters have average
   below \(2\), and the apparent algebraic complexity reduces to one
   two-layer hyperbola.
3. Average degree is nevertheless not universally bounded.  An explicit
   multistar additive box has

   \[
   \overline d(A)=1+\Theta(\log |A|).
   \]

   This growth is exact and unbounded, but it is only \(|A|^{o(1)}\).
   It does not repair any polynomial exponent deficit in the global
   construction.

## 2. Exhaustive optimization method

For a finite candidate universe \(U=\{x_1,\ldots,x_M\}\), every compatible
ordered quadruple \((s,\beta,\gamma,\delta)\in U^4\) is assigned to the bit
mask of its distinct vertices.  Let \(c(B)\) be the number assigned to mask
\(B\).  Then for every subset \(A\subseteq U\),

\[
H(A)=\sum_{B\subseteq A}c(B).
\]

A subset zeta transform evaluates this expression for all \(2^M\) subsets.
Thus the reported optimum at each cardinality is exact within the stated
universe; it is not a local-search result.

### Simplified rational model

For \(X=2,Y=1\) and integer differences, factorization gives only

\[
(u,v)=(0,0),(0,-2),(-4,0),(-4,-2).
\]

Writing \(a=r_A(2)\) and \(b=r_A(4)\),

\[
H=(n+a)(n+b).                                              \tag{1}
\]

The graph on an integer set with edges at gaps \(2\) and \(4\) is a union
of induced subgraphs of squared paths.  It has at most \(2n-3\) edges, so
\(a+b\le2n-3\).  Equation (1) is maximized by
\((a,b)=(n-1,n-2)\), attained by a step-two arithmetic progression.
Therefore, for \(n\ge2\),

\[
H\le(2n-1)(2n-2)<4n^2.                                   \tag{2}
\]

Exhausting every subset of
\(\{-11,-9,\ldots,9,11\}\) verifies equality for every \(2\le n\le12\).

### Actual SAT star universe

Use

\[
X=-\frac32,\qquad Y=\frac{\sqrt{12285}}2,\qquad R=-3069
\]

and generate the star endpoints from
\(t=\pm1,\pm2,\pm3,\pm4\).  After exact deduplication this is a
17-point universe in \(\mathbb Q(Y)\).  Exhausting all \(131072\) subsets
gives:

| \(n\) | maximum \(H\) | maximum average |
|---:|---:|---:|
| 1 | 1 | 1 |
| 2 | 4 | 1 |
| 3 | 10 | 1.1111 |
| 4 | 18 | 1.1250 |
| 5 | 29 | 1.1600 |
| 6 | 42 | 1.1667 |
| 7 | 57 | 1.1633 |
| 8 | 75 | 1.171875 |
| 9 | 95 | \(95/81=1.17284\ldots\) |
| 10 | 114 | 1.1400 |
| 11 | 136 | 1.12397 |
| 12 | 160 | 1.1111 |

The single-star candidate pool therefore shows no finite-size trend toward
polynomial average growth.

## 3. Rational translations at the actual SAT parameters

If \(A\subset\mathbb Q\), then both differences \(u,v\) are rational.
In

\[
u^2-v^2-3u-\sqrt{12285}\,v=0,
\]

comparison of rational and irrational parts forces \(v=0\), then
\(u\in\{0,3\}\).  Hence

\[
H(A)=n^2+n\,r_A(3)\le2n^2-n.                              \tag{3}
\]

The bound is sharp for a step-three rational progression.  Thus actual SAT
resonance cannot arise from rational translations alone.

## 4. Exact two-layer reduction

The star construction naturally has two layers

\[
A=P\ \cup\ (Q-Y),
\]

with \(P,Q\) in a coefficient field not containing \(Y\).  Write
\(u=a+bY\), \(v=c+dY\), where \(b,d\in\{-1,0,1\}\).  Comparing the two
coefficients in \(F(u,v)=0\) leaves only:

\[
\begin{array}{c|c}
(b,d)&(a,c)\\ \hline
(0,0)&(0,0),(3,0)\\
(0,1)&(-189/2,0),(195/2,0)\\
(0,-1)&(a-3/2)^2-c^2=-3069 .
\end{array}                                                \tag{4}
\]

All other layer pairs require \(\sqrt{2729}\) or \(\sqrt{8193}\) in the
coefficient field, or have no solution.  In particular, every scalable
multistar interaction lies on the single rational hyperbola

\[
(a-3/2-c)(a-3/2+c)=-3069.                                 \tag{5}
\]

If

\[
r_0(a)=r_P(a)+r_Q(a),\qquad r_{Q-P}(c)=|\{(q,p):q-p=c\}|,
\]

then, apart from the four explicit exceptions in (4), the total is exactly

\[
\sum_{(a-3/2)^2-c^2=-3069}r_0(a)r_{Q-P}(c).                \tag{6}
\]

This is the reusable multistar-overlap lemma: many high-degree stars raise
the average only when their same-layer and cross-layer endpoints overlap
on many common hyperbola differences.

## 5. Explicit logarithmic multistar family

Let \(T\) be transcendental; \(T=e\) is an explicit choice.  For
\(j=1,\ldots,k\), set

\[
\begin{aligned}
u_j&=\frac12(T^j+RT^{-j})-X,\\
c_j&=\frac12(T^j-RT^{-j}),\\
v_j^\pm&=\pm c_j-Y.
\end{aligned}
\]

Both \((u_j,v_j^+)\) and \((u_j,v_j^-)\) solve the actual SAT
compatibility equation.

Fix an integer \(L\ge2\) and form the proper additive box

\[
P=\left\{
\sum_{j=1}^k\alpha_j u_j+\sum_{j=1}^k\beta_j c_j:
0\le\alpha_j,\beta_j<L
\right\},
\qquad
A=P\cup(P-Y).                                              \tag{7}
\]

The \(2k\) generators are integer-linearly independent.  Indeed, in a
relation, the coefficients of \(T^j\) and \(T^{-j}\) give respectively
\(\alpha_j+\beta_j=0\) and \(\alpha_j-\beta_j=0\).
Consequently

\[
|P|=L^{2k},\qquad n=|A|=2L^{2k}.                          \tag{8}
\]

The exact popular-difference counts are

\[
r_A(u_j)=n\left(1-\frac1L\right),\qquad
r_A(v_j^\pm)=\frac n2\left(1-\frac1L\right).
\]

The \(2k\) hyperbola points and the baseline \((0,0)\) therefore give

\[
H(A)\ge
n^2\left[1+k\left(1-\frac1L\right)^2\right].              \tag{9}
\]

In fact equality holds.  In the Laurent polynomial ring, (5) says that
two factors multiply to the nonzero constant \(R\); both factors must be
Laurent monomial units.  Comparing their largest and smallest powers shows
that the only supported nonconstant solutions are precisely
\((u_j,\pm c_j)\).  The exceptional fixed differences in (4) are absent
from the proper box difference set.

For \(L=2\),

\[
n=2\cdot4^k,\qquad
\overline d(A)=1+\frac{k}{4}
=1+\frac14\log_4(n/2).                                   \tag{10}
\]

This proves genuine unbounded average degree while sharply separating it
from the linear maximum degree of a single resonant star.

## 6. Cell and service exponent audit

The difference palette of (7) is exact:

\[
|A-A|=3(2L-1)^{2k}
=3(n/2)^{\log_L(2L-1)}.                                  \tag{11}
\]

For \(L=2\), this is \(3\cdot9^k\), or
\(\Theta(n^{\log_2 3})\).  The compatibility mass in (9) is

\[
H=n^2\Theta(\log n)=n^{2+o(1)}.
\]

Thus the multistar merger buys a logarithm and increases the translation
difference palette, but changes no polynomial exponent.  On the one-layer
SAT scaling with \(m=\Theta(n)\), it remains at service exponent \(2\),
far below the campaign threshold \(33/10\).  The logarithm cannot cover
the missing \(13/10\).  Layering this construction likewise changes the
previous ledgers only by \(n^{o(1)}\).

The correct conclusion is therefore:

- universal constant average degree is false;
- the explicit growth found here is logarithmic;
- a successful counterexample still needs \(n^{\Omega(1)}\) average
  degree, equivalently polynomially many hyperbola points compressed into
  a low-dimensional additive structure.

## Reproducibility

```bash
python3 verify_resonant_multistar_optimization.py
pytest -q test_verify_resonant_multistar_optimization.py
```

The verifier performs both exhaustive subset optimizations, checks the
rational SAT bound and two-layer solution types, verifies the resonant
pairs as Laurent identities, and certifies (8)--(11).
