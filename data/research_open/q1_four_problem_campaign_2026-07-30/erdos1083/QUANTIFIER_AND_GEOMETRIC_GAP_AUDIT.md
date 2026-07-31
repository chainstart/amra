# Hard audit: endpoint quantifiers, exponents, and the geometric de-reuse gap

Date: 2026-07-30

## 1. Verdict

| Audit item | Verdict |
|---|---|
| \(H,s,\mu,R\) to \(S,U\) transfer | **PASS** |
| \(35/18\) label-count exponent | **PASS** |
| \(13/18\) row-degree exponent | **PASS** |
| \(17/6\) synchronized-pair exponent | **PASS** |
| Order of \(o(1)\) and fixed-\(\varepsilon\) quantifiers | **PASS after explicit convention below** |
| Mathialagan--Sheffer comparison | **The extracted circles are in their expanding, nonexceptional class, but their one-pair bound is too small** |
| Synchronized network implies \(>3/5\) | **NO; an aggregate geometric de-reuse lemma is missing** |

No global \(3/5+\delta\) claim is authorized by this audit.

## 2. Quantifier convention

Fix
\[
\kappa=\frac29.
\]
Suppose there is an unbounded sequence \(t\to\infty\) on which the
critical hub alternative survives.  For each \(t\), perform the
finite dyadic decompositions used in the inherited proof.  Their
number is polylogarithmic, so every loss is \(t^{o(1)}\).

After passing to a subsequence if necessary, write the selected
scales as
\[
s=t^{a+o(1)},\quad
u=t^{m+o(1)},\quad
N=t^{b+o(1)},\quad
K=t^{c+o(1)},\quad
H=t^{h+o(1)}.
\tag{2.1}
\]
Passing to a subsequence only stabilizes bounded logarithmic
exponents; it does not add a hypothesis.

Let \(\omega(t)\to0\) dominate:

- every inherited \(o(1)\);
- all dyadic pigeonhole losses;
- all factors two from sine and square fibres; and
- the loss from replacing \(H\) by \(H-1\) after choosing an anchor.

Every displayed endpoint exponent below means a lower or upper bound
with \(C\omega(t)\) in the adverse direction for one absolute
constant \(C\).

For the abundance assertion, the order is:

1. fix an arbitrary constant \(\varepsilon>0\);
2. take \(t\ge t_0(\varepsilon)\) so that
   \(C\omega(t)<\varepsilon/4\);
3. then perform the threshold comparison.

The dyadic layer and point configuration are not allowed to depend on
a quantity tending to zero after \(t\).  This is the standard meaning
of “for every fixed \(\varepsilon>0\)” in the final abundance result.

## 3. Scalar endpoint audit

With all errors charged adversely to \(\omega\), the inherited
inequalities are
\[
\begin{aligned}
a+b+m&\ge19/3-\omega,\\
b+m&\le50/9+\omega,\\
11a+2b&\le18+\omega,\\
m&\ge5/6-\omega,\qquad m\le1+\omega,\\
c&\le46/9-3m+\omega,\qquad b=c+h.
\end{aligned}
\tag{3.1}
\]

### 3.1 Source richness

Subtracting the second inequality from the first gives
\[
\boxed{a\ge7/9-2\omega.}
\tag{3.2}
\]
The mass bound also gives
\[
b\ge19/3-a-m-\omega.
\tag{3.3}
\]
Insert (3.3) into the point--circle inequality:
\[
11a+2(19/3-a-m-\omega)\le18+\omega.
\]
Hence
\[
9a-2m\le16/3+3\omega
\]
and
\[
\boxed{
a\le16/27+2m/9+\omega/3.
}
\tag{3.4}
\]

### 3.2 Number of circles on one signed parameter line

Equations (3.1) and (3.3) give
\[
\begin{aligned}
h=b-c
&\ge
(19/3-a-m-\omega)-(46/9-3m+\omega)\\
&=
11/9-a+2m-2\omega.
\end{aligned}
\tag{3.5}
\]
Use (3.4):
\[
h
\ge17/27+16m/9-C\omega.
\tag{3.6}
\]
Since \(m\ge5/6-\omega\),
\[
\boxed{h\ge19/9-C\omega.}
\tag{3.7}
\]

No equality in the old endpoint ledger has been assumed.  Only
one-sided inequalities were used.

## 4. Transfer from \(H,s,\mu,R\) to \(H,S,U,R,D\)

Choose one signed parameter line \((A,\rho^2)\).  Its merged circles
have distinct centre heights.  Choose one as anchor and retain the
other \(H-1\).

| Bundle quantity | Finite definition | Exponent bound |
|---|---|---|
| \(H'\) | nonanchor circle rows | \(H-1=t^{h+o(1)}\) |
| \(s\) | source incidences per circle in the dyadic layer | \(t^{a+o(1)}\) |
| \(\mu\) | producing triples per circle | \(u=t^{m+o(1)}\) |
| \(R\) | common tangent-square universe | \(R\le M=t^{1+\omega}\) |
| \(S\) | distinct sine values on the anchor circle | \(s/2\le S\le s\) |
| \(U\) | distinct target squares in one row | \(u/2\le U\le2u\) |
| \(D\) | global squared-distance budget | \(D\le t^{3+\omega}\) |

The lower bound for \(U\) uses the at-most-two-to-one map
\(y\mapsto y^2\).  Its upper bound uses that the row has fewer than
\(2u\) producing triples.  The lower bound for \(S\) uses the
at-most-two-to-one sine map on one circle.

Thus \(S,U,H'\) have exponents \(a,m,h\), while only the upper
exponents of \(R,D\) are used.

## 5. Reuse and aggregate-support exponents

From (3.5),
\[
\begin{aligned}
h+m-2-a
&\ge-7/9-2a+3m-C\omega\\
&\ge-53/27+23m/9-C\omega\\
&\ge\boxed{1/6-C\omega}.
\end{aligned}
\tag{5.1}
\]
Therefore
\[
\boxed{
\frac{H'U}{R^2S}\ge t^{1/6-C\omega}.
}
\tag{5.2}
\]
This verifies the direction of every estimate: \(H',U\) were given
lower bounds, and \(R,S\) upper bounds.

The total row-spectrum support satisfies
\[
\begin{aligned}
h+a+m
&\ge(11/9-a+2m)+a+m-C\omega\\
&=11/9+3m-C\omega\\
&\ge\boxed{67/18-C\omega}.
\end{aligned}
\tag{5.3}
\]
Since \(67/18-3=13/18>0\), the subtraction term in the pair-overlap
identity is lower order.

## 6. The \(35/18\) and \(13/18\) audit

The exact many-label theorem gives at least
\[
\frac{H'U}{8R}
\]
spectrally rich labels.  Its exponent is bounded below by
\[
h+m-1
\ge
19/9+5/6-1-C\omega
=
\boxed{35/18-C\omega}.
\tag{6.1}
\]

Every such label belongs to at least
\[
\frac{H'SU}{4D}
\]
different row spectra.  The exponent is
\[
h+a+m-3
\ge
67/18-3-C\omega
=
\boxed{13/18-C\omega}.
\tag{6.2}
\]

The quadratic cap used to count labels is exact: for fixed
\((d,x,\tau)\), a supporting height satisfies
\[
z^2+2\rho xz+(\rho^2+\tau-d)=0,
\tag{6.3}
\]
so there are at most two real heights.  Hence one label has row degree
at most \(2SR\).  No \(o(1)\) enters this finite cap.

## 7. The \(17/6\) audit and the \(\varepsilon\) order

Let
\[
\mathcal S=\sum_z|\mathcal V_z|.
\]
The reuse margin (5.2) and the exact aggregate-support theorem give
\[
\mathcal S\ge t^{h+a+m-C\omega}.
\tag{7.1}
\]
Since the union has at most \(D\) labels,
\[
\begin{aligned}
\mathcal J
&:=
\sum_{z\ne z'}|\mathcal V_z\cap\mathcal V_{z'}|\\
&\ge
\mathcal S^2/D-\mathcal S\\
&\ge
t^{2(h+a+m)-3-C\omega}.
\end{aligned}
\tag{7.2}
\]

Fix \(\varepsilon>0\) before taking \(t\) large and set
\[
\theta
=
t^{-\varepsilon/2}\frac{S^2U^2}{D}.
\tag{7.3}
\]
The total contribution of row pairs with intersection below
\(\theta\) is at most
\[
H'^2\theta
\le
t^{-\varepsilon/2+C\omega}\mathcal J
=o(\mathcal J).
\tag{7.4}
\]
Each remaining pair has intersection at most
\[
|\mathcal V_z|\le |X||T_z|\le2SU.
\tag{7.5}
\]
The number of remaining ordered pairs is therefore at least
\[
t^{2h+a+m-3-C\omega}.
\tag{7.6}
\]
Using (3.2), (3.7), and \(m\ge5/6-C\omega\),
\[
\begin{aligned}
2h+a+m-3
&\ge
2(19/9)+7/9+5/6-3-C\omega\\
&=
\boxed{17/6-C\omega}.
\end{aligned}
\tag{7.7}
\]
Passing from ordered to unordered pairs costs a factor two.

Finally, the exponent of (7.3) is
\[
2a+2m-3-\varepsilon/2-C\omega
\ge
2/9-\varepsilon
\tag{7.8}
\]
for \(t\ge t_0(\varepsilon)\).  This proves the correctly quantified
statement:

> For every fixed \(\varepsilon>0\), all sufficiently large members
> of a surviving endpoint sequence contain
> \(t^{17/6-o_\varepsilon(1)}\) unordered nonaligned row pairs, each
> sharing at least \(t^{2/9-\varepsilon}\) distinct labels.

There is no exchange of the limits \(t\to\infty\) and
\(\varepsilon\downarrow0\).

## 8. Nearest known two-circle theorem

The nearest classification result is Mathialagan--Sheffer,
[*Distinct distances on non-ruled surfaces and between circles*,
Theorem 1.4](https://arxiv.org/abs/2011.08098).  For point sets of
sizes \(s_1,s_2\) on two circles in \(\mathbb R^3\), it says:

- aligned or perpendicular circle pairs admit examples with
  \(\Theta(s_1+s_2)\) bipartite distances;
- every other pair determines
  \[
  \Omega\!\left(
  \min\{s_1^{2/3}s_2^{2/3},s_1^2,s_2^2\}
  \right)
  \tag{8.1}
  \]
  bipartite distances.

The circles extracted here lie in one source plane, have the same
radius, and have distinct centres \((A,w_i)\).  Their axes are
parallel distinct lines.  Hence they are not aligned.  The
perpendicular exception is impossible, both because their containing
planes agree and because retained reverse circles have \(A\ne0\).
Thus (8.1) applies.

At the smallest forced source richness,
\[
s_1,s_2\ge t^{7/9-o(1)},
\]
the known theorem gives only
\[
\Omega(t^{28/27-o(1)})
\tag{8.2}
\]
source--source distances for one pair.  This is far below the
\(t^{3+o(1)}\) global budget.

Even applying (8.1) to \(t^{17/6-o(1)}\) circle pairs does not permit
the lower bounds to be summed: the theorem contains no bound on how
often one numerical distance can be reused across different circle
pairs.  Moreover:

- Mathialagan--Sheffer concerns \(P_i\times P_j\) on two circles;
- the new spectra concern one anchor-circle set crossed with target
  points on the perpendicular axes \(L_i,L_j\);
- their theorem uses neither the common tangent-square universe
  \(T_\ast\), the target multiplicity \(U\), nor the selected-label
  service relation.

Therefore the missing result is not another classification of one
circle pair.  The aligned/perpendicular classification is already
complete for the present purpose.

## 9. Exact geometric de-reuse lemma still missing

For the hub network, the sufficient missing theorem is the following.

### Required bundle de-reuse lemma

There exist fixed \(\eta,\delta_0>0\) and an explicit finite list of
affine-quadratic exceptional families such that, uniformly for the
endpoint and all dyadic ledgers in a sufficiently small
\(O(\delta_0)\) exponent neighbourhood arising from
\(D\le t^{3+\delta_0}\), every regular reverse-circle bundle satisfies
either
\[
\boxed{
\sum_{z\ne z'}
|\mathcal V_z\cap\mathcal V_{z'}|
\ll
t^{-\eta}
\frac{\left(\sum_z|\mathcal V_z|\right)^2}{D},
}
\tag{9.1}
\]
or it belongs to one of the exceptional families; and every
exceptional family, when combined with the actual source incidences
and selected-label service graph, determines \(t^{3+\eta'}\)
distances for some fixed \(\eta'>0\).

The exact Cauchy--Schwarz lower bound is the same expression as the
right side of (9.1), up to the lower-order subtraction
\(\sum_z|\mathcal V_z|\), but without \(t^{-\eta}\).  Thus (9.1),
including discharge of its exceptions, contradicts the compressed
hub.  Uniformity in the stated exponent neighbourhood is essential
for converting endpoint exclusion into a fixed numerical
\(3/5+\delta\) gain; an estimate only at one formal equality ledger
would not suffice.

The lemma must use all of:

1. the quadratic translations \(z^2\);
2. the distinct nonaligned centre heights;
3. \(T_z\subseteq T_\ast\), \(|T_\ast|\le t^{1+o(1)}\);
4. the fact that every row also produces an \(s\)-rich source circle;
5. the common selected service labels
   \(\rho^2+T_z\subseteq\mathcal D_0\); and
6. compatibility across \(t^{17/6-o(1)}\) synchronized row pairs.

A pairwise bound using only \(|X|,|T_z|,|T_{z'}|\) cannot suffice:
the previous Euclidean cancellation model shows that fresh target
directions can compress one or several rows.  The saving must come
from global direction/label reuse across the entire nonaligned
network.

## 10. What would and would not give \(>3/5\)

In the normalization \(N=t^5\), a bound
\[
|\Delta^2(P)|\ge t^{3+\eta'}
\]
is exactly
\[
|\Delta(P)|\ge N^{3/5+\eta'/5}.
\]
Thus the required *uniform* bundle de-reuse lemma would convert the
**synchronized hub network** into a strict \(3/5\) improvement on
that branch.  The word uniform cannot be dropped: exclusion of only
the exact \(D=t^{3+o(1)}\) ledger does not automatically provide a
fixed positive exponent.

It would not by itself finish the full Erdős #1083 proof.  The exact
matching-or-hub theorem still has a matching alternative.  A global
proof additionally needs a matching-branch theorem of the form:

> Polynomially many coefficient-separated, pairwise plane-disjoint
> rich cells for many labels force \(t^{3+\eta''}\) total distances.

The existing four-plane signature-\((3,3)\) audit shows that this does
not follow from matching cardinalities alone.  Therefore:

- (9.1) is the unique remaining **local hub gap**;
- matching-to-distance expansion is a separate **global branch gap**;
- neither gap is claimed closed here.

## 11. Priority boundary

The Mathialagan--Sheffer comparison above was checked against the
primary arXiv v2 theorem statement.  No source found or cited here
provides the aggregate axis-spectrum de-reuse lemma (9.1).

This is a nearest-neighbour comparison, not an exhaustive priority
search.  The elementary multidilate inequality and its AMRA
application must not be advertised as globally novel until a broader
literature audit is completed.
