# Erdős #1083: exact-block transverse stars force quotient cliques

Date: 2026-08-02

## 0. Main result

The full common-spectrum partition supplies a structural conclusion
that was not used in the previous bounded-cycle route.

Let

\[
 V=A_i\oplus\lambda_iX,
 \qquad |X|=S\ge2,
 \qquad |V|=SU,
\tag{0.1}
\]

be an exact block, and assume

\[
 U<S^2.
\tag{0.2}
\]

Put

\[
 W_i=\operatorname{span}_{\mathbb Q}
       (\lambda_i(X-X)).
\tag{0.3}
\]

Then the graph joining \(i,j\) when \(W_i\cap W_j=\{0\}\) is
triangle-free.  Consequently the transverse neighbourhood of every
row is a pairwise **nontransverse** family.

There are two useful endpoint applications.  First, in the
transverse-heavy tangent-overlap branch, averaging over row--tangent
incidences gives one fixed row and one fixed tangent square shared
with

\[
 \boxed{t^{5/9+o(1)}}
\tag{0.4}
\]

transverse partner rows.  Second, retaining one fixed nonzero tangent
difference gives a \(t^{1/6+o(1)}\)-leaf star.  In both cases the
leaves pairwise have nonzero rational-space intersection.  Writing

\[
 W=\operatorname{span}_{\mathbb Q}(X-X),
\]

their heights satisfy the exact pairwise quotient constraint

\[
 \boxed{
 \frac{z_i}{z_j}
 \in\frac{W\setminus\{0\}}{W\setminus\{0\}}
 \quad(i\ne j).}
\tag{0.5}
\]

Thus the exact-block branch already produces a common-tangent
\(t^{5/9}\)-row quotient clique before any cycle or path extraction,
and a fixed-difference \(t^{1/6}\)-row version when the parabolic
edge equation must also be retained.  This is not yet a
distance contradiction: for high-dimensional \(W\), pairwise
intersection need not give one common rational direction.  It does,
however, replace the former unstructured final interface by a precise
inverse problem for a power-large quotient clique.

## 1. No transverse triangle in an exact endpoint block

We use the torsion-free direct-tiling rank theorem from the
2026-07-31 breakthrough campaign:

> If \(V=A_i\oplus\lambda_iX\) and a subfamily of the spaces
> \(W_i\) is pairwise transverse, then
> \(S^k\le|V|\), where \(k\) is the subfamily size.

For completeness, the input is exact unique representation.  In the
integral group ring of the finitely generated torsion-free group
containing all sets, it gives

\[
 P_V=P_{A_i}P_{\lambda_iX}.
\tag{1.1}
\]

Pairwise transverse Newton direction spaces make the factors
\(P_{\lambda_iX}\) pairwise coprime.  Their product divides \(P_V\),
and augmentation gives \(S^k\mid |V|\), in particular
\(S^k\le|V|\).

If three rows formed a transverse triangle, this theorem would give

\[
 S^3\le|V|=SU,
\]

or \(S^2\le U\), contradicting (0.2).  Hence:

### Lemma 1 (triangle firewall)

Under (0.1)--(0.2), the transverse graph is triangle-free.

In particular, if \(j,k\) are distinct transverse neighbours of
\(i\), then

\[
 W_j\cap W_k\ne\{0\}.
\tag{1.2}
\]

This conclusion genuinely uses the full exact tilings (0.1).  The
standalone Euclidean theta model in
`COHERENT_THETA_EUCLIDEAN_NO_GO.md` deliberately violates this
completion constraint: its internal rows can be mutually transverse,
so three of its selected cells cannot all be completed to one exact
endpoint spectrum.

## 2. Common-tangent windmill compression

In the transverse-heavy branch of the inherited
tangent-transversality dichotomy, put

\[
 P_\perp
 =\sum_{\substack{i\ne j\\W_i\cap W_j=\{0\}}}
 |T_i\cap T_j|.
\tag{2.1}
\]

For \(\tau\in T_i\), define the transverse row--tangent degree

\[
 d_\perp(i,\tau)
 =|\{j\ne i:\tau\in T_j,
                 \ W_i\cap W_j=\{0\}\}|.
\tag{2.2}
\]

Every ordered common-tangent incidence is counted exactly once, so

\[
 \sum_i\sum_{\tau\in T_i}d_\perp(i,\tau)=P_\perp.
\tag{2.3}
\]

There are \(qU\) row--tangent slots.  Hence some \((i_0,\tau_0)\)
has a leaf set \(L_{\tau_0}\) of size at least

\[
 \boxed{|L_{\tau_0}|\ge\frac{P_\perp}{qU}.}
\tag{2.4}
\]

Every leaf is transverse to \(i_0\), so Lemma 1 makes the leaf spaces
pairwise nontransverse.  All corresponding targets

\[
 q_{j,\tau_0}=(A,\sqrt{\tau_0},-z_j)
 \qquad(j\in L_{\tau_0})
\tag{2.5}
\]

are genuine collinear points on one tangent line.

At the frozen endpoint,

\[
 P_\perp\ge t^{19/9+o(1)},\qquad
 qU=t^{14/9+o(1)},
\]

and therefore

\[
 \boxed{|L_{\tau_0}|\ge t^{5/9+o(1)}.}
\tag{2.6}
\]

This is stronger in row count than the fixed-difference star below,
but it does not retain one \(\delta\).  Collinearity alone is not a
distance contradiction: \(n\) arbitrary points on a line can have
only \(n-1\) distinct distances.  The new content is simultaneous
common tangent and pairwise rational-space intersection.

## 3. Fixed-difference star compression

Use the setup and conclusion of the inherited
`TRANSVERSE_NONZERO_DIFFERENCE_THEOREM.md`.  A nonzero
\(\delta\in T_*-T_*\) supports \(M\) distinct ordered row pairs
\((i,j)\), each transverse, with a unique source pair satisfying

\[
 z_i^2-z_j^2+2\rho(z_ix_{ij}-z_jx'_{ij})=\delta.
\tag{3.1}
\]

Let \(q\) be the number of rows.  Averaging ordered outdegrees gives
a row \(i_0\) and a leaf set \(L\) with

\[
 |L|\ge\frac Mq.
\tag{3.2}
\]

Every \(j\in L\) is transverse to \(i_0\).  Lemma 1 therefore gives

\[
 W_j\cap W_k\ne\{0\}
 \qquad(j\ne k\in L).
\tag{3.3}
\]

This proves the all-parameter star-cluster theorem:

### Theorem 2 (transverse-star / nontransverse-leaf conversion)

In an exact block satisfying \(U<S^2\), any directed transverse graph
with \(M\) edges on \(q\) rows contains a transverse star with at
least \(M/q\) leaves, and the leaf spaces are pairwise
nontransverse.  If all graph edges also carry one fixed difference
\(\delta\), the star retains that same \(\delta\) and equation (3.1)
on every leaf.

At the frozen endpoint,

\[
 M=t^{8/9+o(1)},\qquad q=t^{13/18+o(1)},
\]

so

\[
 \frac Mq
 =t^{8/9-13/18+o(1)}
 =\boxed{t^{1/6+o(1)}}.
\tag{3.4}
\]

The hypothesis (0.2) has a large power margin:

\[
 \frac{S^2}{U}
 =t^{14/9-5/6+o(1)}
 =t^{13/18+o(1)}.
\tag{3.5}
\]

## 4. Exact quotient form and low-rank inverse theorem

In the reverse-circle block, \(\lambda_i=2\rho z_i\), and therefore

\[
 W_i=2\rho z_iW,
 \qquad W=\operatorname{span}_{\mathbb Q}(X-X).
\tag{4.1}
\]

For two leaves \(i,j\), choose a nonzero element of
\(W_i\cap W_j\).  Then there are nonzero \(u,v\in W\) such that

\[
 2\rho z_i u=2\rho z_jv.
\]

Cancelling \(2\rho\) proves (0.5).  Equivalently, relative to any
one leaf \(j_*\),

\[
 \{z_j:j\in L\}
 \subseteq
 z_{j_*}\frac{W\setminus\{0\}}{W\setminus\{0\}},
\tag{4.2}
\]

and, more strongly, every pairwise ratio lies in the same quotient
set.

### Rank-one corollary

If \(\dim_{\mathbb Q}W=1\), write \(W=\alpha\mathbb Q\).
Then all nonzero scalar dilates of \(W\) intersect exactly when their
scalar ratio is rational.  The common-tangent leaf family is therefore
a genuinely rationally commensurate height family of size

\[
 t^{5/9+o(1)}.
\tag{4.3}
\]

More explicitly, for any \(x_0\in X\) there is a finite
\(Y\subset\mathbb Q\) with

\[
 X=x_0+\alpha Y.
\tag{4.4}
\]

Choose one leaf height \(z_*\).  There are distinct
\(r_j\in\mathbb Q^*\) such that \(z_j=r_jz_*\), and the common-tangent
cells have the exact normal form

\[
\begin{aligned}
 C_{j,\tau_0}
 ={}&\rho^2+\tau_0+r_j^2z_*^2
     +2\rho r_jz_*x_0\\
 &\quad +(2\rho z_*\alpha)r_jY.
\end{aligned}
\tag{4.5}
\]

This is a one-parameter rationally commensurate parabolic affine-copy
chart.  The quantifier boundary matters: the rationals \(r_j\) and
the elements of \(Y\) have no inherited denominator or height bound.
Thus the polynomial-coordinate ruled escape theorem cannot yet be
invoked.

### Rank-two star/top corollary

If \(\dim_{\mathbb Q}W=2\), the leaf spaces are two-dimensional
\(\mathbb Q\)-subspaces.  Any finite pairwise-intersecting family of
two-dimensional subspaces satisfies one of:

1. all spaces contain one common nonzero line; or
2. all spaces lie in one three-dimensional \(\mathbb Q\)-subspace.

Indeed, choose distinct spaces \(A,B\), with common line
\(L=A\cap B\).  If every space contains \(L\), the first outcome
holds.  Otherwise choose \(C\) not containing \(L\).  The lines
\(C\cap A\) and \(C\cap B\) are distinct, so
\(C\subseteq A+B\), a three-dimensional space.  Any further member
not containing \(L\) is contained in \(A+B\) by the same argument;
a member containing \(L\) meets \(C\) in a second line and is also
contained in \(A+B\).  This proves the dichotomy.

The two outcomes have concrete height forms.  In the common-line
case choose \(0\ne h\in\bigcap_j z_jW\).  Then

\[
 z_j=\frac{h}{w_j}
 \qquad\text{for some }0\ne w_j\in W.
\tag{4.6}
\]

In the three-dimensional top case, let \(H\) contain every \(z_jW\)
and define

\[
 \mathcal M(W,H)=\{z\in\mathbb R:zW\subseteq H\}.
\tag{4.7}
\]

This is a \(\mathbb Q\)-vector space.  Multiplication by any fixed
\(0\ne w\in W\) injects \(\mathcal M(W,H)\) into \(H\), so

\[
 \dim_{\mathbb Q}\mathcal M(W,H)\le3.
\tag{4.8}
\]

All leaf heights lie in \(\mathcal M(W,H)\).  Thus the rank-two
alternative is either the reciprocal chart (4.6) or an additive
height chart of rational rank at most three.

The top alternative is not an artefact of allowing arbitrary
subspaces.  Let \(\alpha\) be the real root of

\[
 \alpha^3-\alpha^2-1=0
\]

and take \(W=\operatorname{span}_{\mathbb Q}\{1,\alpha\}\).  Then

\[
 W=\langle1,\alpha\rangle,
 \quad \alpha W=\langle\alpha,\alpha^2\rangle,
 \quad \alpha^2W=\langle\alpha^2,1\rangle.
\tag{4.9}
\]

These three scalar dilates intersect pairwise in three different
lines and have zero total intersection.  Thus “pairwise
nontransverse” cannot be replaced by “one common nonzero vector.”

Conversely, the common-line alternative need not have bounded total
ambient rank.  For a transcendental \(\theta\), put
\(W=\langle1,\theta\rangle\) and
\(z_c=(1+c\theta)^{-1}\) for distinct rational \(c\).  Every
\(z_cW\) contains \(1\), while the rational functions
\((1+c\theta)^{-1}\) are linearly independent as \(c\) varies.
This is the exact counterexample boundary behind the star/top split.

Rank at most two therefore converts (2.6) into a common-direction,
reciprocal, or bounded-ambient-rank chart on
\(t^{5/9+o(1)}\) rows.  The unresolved case is large
\(\mathbb Q\)-rank of \(X-X\).

## 5. Consequences for the old network route

Three immediate corrections/refinements follow.

1. The fixed-difference transverse graph has no triangles.  Hence the
   inherited bounded-cycle theorem may start at length four; an odd
   noncoherent cycle can first occur at length five.
2. A coherent theta is not an arbitrary collection of transverse
   arms after exact completion.  Its first neighbours of a common
   endpoint are automatically pairwise nontransverse.
3. Cycle/path amplification is not needed to obtain a power-large
   inverse object: common-tangent averaging gives exponent \(5/9\),
   while the original fixed-difference star retains \(\delta\) at
   exponent \(1/6\).

This does not invalidate the cycle and path theorems.  It changes the
best next target.  The first unproved interface is now:

> Convert a common-tangent \(t^{5/9+o(1)}\)-element pairwise quotient
> clique, or the fixed-\(\delta\) \(t^{1/6+o(1)}\) clique satisfying
> the parabolic star equations (3.1), into either a
> common low-rank direction, a bounded-height ruled chart, or more
> than \(t^{3+o(1)}\) global distances.

Pairwise nonzero intersections alone do not imply a common vector in
high dimension, so no stronger conclusion is claimed here.

### Exact interface back to the public problem

The conclusions above are conditional on being inside the literal
exact common-spectrum block (0.1) and, for (2.6), on the
transverse-heavy half of the tangent-overlap split.  The original
\(N\)-point problem supplies only a near-direct, near-block endpoint
before a still-unproved stability extraction.  Even after that
extraction, (4.5)--(4.8) do not exceed the \(t^3=N^{3/5}\) distance
budget without a denominator-free escape theorem.  Therefore no
improvement of \(f_3(N)\) is claimed.

## 6. Reproduction

Run:

```bash
python3 verify_exact_block_transverse_star_cluster.py
python3 -m unittest -v test_exact_block_transverse_star_cluster.py
```

The verifier independently checks the endpoint inequalities and
exponents, the graph-neighbourhood implication on exhaustive finite
graphs, the quotient algebra on exact rational subspaces, and both
rank-two alternatives on explicit examples.  The group-ring theorem
and the all-parameter deductions above remain manuscript proofs, not
finite-enumeration claims.
