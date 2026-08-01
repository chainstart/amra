# Erdős #1083: sharp Følner tradeoff and a tangent-transversality repair

Date: 2026-08-01

## 0. Main conclusions

The simple \(m\)-direction construction can be optimized.  At the
frozen #1083 endpoint it supports

\[
 t^{1/18-o(1)}
\]

pairwise transverse dilation spaces, not merely \(t^{1/72}\), while
the common-spectrum error is still \(o(SU)\).  Its tangent-square
sets can moreover be proved pairwise disjoint, and their full union
has only

\[
 t^{8/9-o(1)}<t
\]

elements.  Thus the tangent-universe cap by itself does not repair
qualitative stability.

However, the full frozen block has \(q=t^{13/18+o(1)}\) rows.  Such a
block cannot be made entirely from the disjoint-tangent Følner
mechanism: its \(qU\) row--tangent incidences inside an \(R=t^{1+o(1)}\)
universe force tangent-pair mass \(t^{19/9+o(1)}\).

Splitting that mass according to whether the two dilation spaces are
transverse gives an exact repaired dichotomy:

1. one tangent square supports \(t^{10/9+o(1)}\) ordered transverse
   row pairs; or
2. one row has \(t^{5/9+o(1)}\) nontransverse partners.

This does not solve either branch, but it identifies the weakest
network statistic discarded by rowwise qualitative stability.

## 1. General primitive-direction construction

Let integers \(L>S\ge2\) satisfy \(S\mid L^2\), and put

\[
 U=\frac{L^2}{S}.
\tag{1.1}
\]

Fix \(1\le M<L\), and let

\[
 \mathcal D_M
 =\{(p,q):1\le p,q\le M,\ \gcd(p,q)=1\}.
\tag{1.2}
\]

For \(v=(p,q)\in\mathcal D_M\), partition the box

\[
 Q_L=\{0,\ldots,L-1\}^2
\]

into its maximal \(v\)-strings.  The initial points are exactly those
\((a,b)\) for which \(a<p\) or \(b<q\).  Hence their number is

\[
 N_v=(p+q)L-pq.
\tag{1.3}
\]

Cut every string into consecutive \(S\)-blocks and a terminal
remainder.  Let \(E_v\) be the total remainder.  Then

\[
 0\le E_v<SN_v<2MSL,\qquad S\mid E_v.
\tag{1.4}
\]

As in the main counterexample, add \(E_v/S\) remote \(S\)-blocks.
This produces \(U\) base points and an injective row spectrum \(V_v\)
of size \(SU=L^2\), while the one common box spectrum \(V\) satisfies

\[
 |V_v\mathbin\triangle V|=2E_v.
\tag{1.5}
\]

### Theorem 1 (constructive error--rank frontier)

There are \(|\mathcal D_M|\) exact direct rows with pairwise
transverse rational dilation spaces and

\[
 \boxed{
 \max_{v\in\mathcal D_M}
 \frac{|V_v\mathbin\triangle V|}{SU}
 <\frac{4MS}{L}.}
\tag{1.6}
\]

Moreover,

\[
 \boxed{
 |\mathcal D_M|
 \ge c_0M^2,\qquad
 c_0=2-\frac{\pi^2}{6}>0.}
\tag{1.7}
\]

#### Proof

Equation (1.6) follows immediately from (1.4)--(1.5) and
\(|V|=L^2\).

Embed \(\mathbb Z^2\) in \(\mathbb R\) by
\(\iota(a,b)=a+b\sqrt2\), take

\[
 X=\{j/(S-1):0\le j<S\},
\qquad
 \lambda_{p,q}=(S-1)(p+q\sqrt2),
\]

and use the block starts as the base sets.  Then the relevant
rational space is

\[
 W_{p,q}=\mathbb Q(p+q\sqrt2).
\]

Two such spaces intersect nontrivially only if their coefficient
vectors are rationally proportional.  Distinct primitive positive
vectors cannot be proportional, so the spaces are pairwise
transverse.

Every non-coprime pair in \(\{1,\ldots,M\}^2\) has a common divisor
\(d\ge2\).  The union bound gives

\[
\begin{aligned}
 M^2-|\mathcal D_M|
 &\le\sum_{d=2}^M\left\lfloor\frac Md\right\rfloor^2\\
 &\le M^2\sum_{d=2}^{\infty}\frac1{d^2}
 =M^2\left(\frac{\pi^2}{6}-1\right),
\end{aligned}
\]

which proves (1.7).  \(\square\)

### Corollary 2 (arbitrarily small error)

For any function \(\omega\to\infty\) with

\[
 \omega=o(L/S),
\]

choose

\[
 M=\left\lfloor\frac{L}{S\omega}\right\rfloor.
\tag{1.8}
\]

Then the uniform relative error is \(O(1/\omega)=o(1)\), while the
pairwise transverse rank is at least

\[
 c_0\left(\frac{L}{S\omega}-1\right)^2.
\tag{1.9}
\]

Thus the achieved block-segmentation tradeoff is

\[
 k\gg\left(\varepsilon\frac LS\right)^2
\]

at error scale \(O(\varepsilon)\), up to absolute constants and
integer rounding.  This is an achieved frontier for the
square-bounded primitive-direction family; no converse for arbitrary
near-tilings is claimed.

### Lemma 2A (the boundary scale is attained)

Assume additionally that \(S\mid L\).  For the diagonal direction
\(v=(1,1)\), every disjoint placement of \(S\)-blocks on the maximal
diagonals leaves exactly

\[
 \boxed{E_{1,1}=L(S-1)}
\tag{1.10}
\]

box points uncovered.  Consequently the completed direct row has

\[
 \boxed{
 \frac{|V_{1,1}\mathbin\triangle V|}{SU}
 =\frac{2(S-1)}{L}.}
\tag{1.11}
\]

#### Proof

The maximal diagonal lengths are

\[
 1,2,\ldots,L-1,L,L-1,\ldots,2,1.
\]

A line of length \(\ell\) contains at most
\(\lfloor\ell/S\rfloor\) disjoint \(S\)-blocks, leaving
\(\ell\bmod S\) points.  Write \(L=aS\).  The central diagonal leaves
zero, and

\[
 E_{1,1}
 =2\sum_{\ell=1}^{L-1}(\ell\bmod S)
 =2a\sum_{j=1}^{S-1}j
 =L(S-1).
\]

Remote completion replaces exactly the missing mass outside \(V\),
so the symmetric difference is twice this quantity.  \(\square\)

Thus the scale \(S/L=\sqrt{S/U}\) is not merely an artifact of the
upper-bound proof: it is exact, including its leading constant, for
the diagonal row in the box model.

## 2. Endpoint optimization

At the frozen endpoint,

\[
 S=t^{7/9},\qquad U=t^{5/6},\qquad
 L=\sqrt{SU}=t^{29/36},
\]

so

\[
 \frac LS=t^{1/36}.
\tag{2.1}
\]

Taking

\[
 M=\left\lfloor\frac{t^{1/36}}{\omega(t)}\right\rfloor
\]

with an arbitrarily slowly growing \(\omega\) gives

\[
 \boxed{
 k\ge t^{1/18-o(1)},\qquad
 \max_v\frac{|V_v\mathbin\triangle V|}{SU}=o(1).}
\tag{2.2}
\]

For example, \(\omega=\log t\) gives error \(O(1/\log t)\) and
\(k\gg t^{1/18}/(\log t)^2\).

The power \(1/18\) is the optimized output of this two-dimensional
primitive-direction template.  It is still much smaller than the
full block size \(q=t^{13/18}\), but it is more than enough to refute
any bounded-rank qualitative stability theorem.

## 3. The tangent sets are actually disjoint

Use the parabolic heights

\[
 z_{p,q}=\frac{S-1}{2}(p+q\sqrt2)
\tag{3.1}
\]

and

\[
 T_{p,q}=A_{p,q}-1-z_{p,q}^2.
\tag{3.2}
\]

Taking

\[
 C=10S^2M^2+10
\]

in the common translation makes every tangent square positive,
because \(z_{p,q}^2<3S^2M^2\) and all block-start coordinates have
positive real embedding.

Every core block start has both coordinates below \(L\).  Every
remote start has second coordinate \(2L\), while its first coordinate
is less than

\[
 2L+\frac{E_v}{S}<2L+2ML\le4ML.
\tag{3.3}
\]

For two distinct primitive directions \(v=(p,q)\) and
\(w=(p',q')\),

\[
\begin{aligned}
 z_v^2-z_w^2
 =\frac{(S-1)^2}{4}\bigl[
 &(p^2+2q^2-p'^2-2q'^2)\\
 &+2(pq-p'q')\sqrt2\bigr].
\end{aligned}
\tag{3.4}
\]

At least one of the two integer coefficients in brackets is nonzero:
otherwise the positive real numbers \(p+q\sqrt2\) and
\(p'+q'\sqrt2\) would have equal squares and hence be equal.

Consequently, if

\[
 \frac{(S-1)^2}{4}>4ML,
\tag{3.5}
\]

then no difference of two block starts can equal (3.4), coefficient
by coefficient in \(\mathbb Q(\sqrt2)\).  Therefore

\[
 \boxed{T_v\cap T_w=\varnothing\qquad(v\ne w).}
\tag{3.6}
\]

Condition (3.5) holds with an enormous margin at the endpoint:
\(S^2=t^{14/9}\), whereas \(ML\le t^{5/6+o(1)}\).

It follows that the optimized family has

\[
 \left|\bigcup_vT_v\right|=kU
 \le t^{1/18+5/6-o(1)}
 =\boxed{t^{8/9-o(1)}<t.}
\tag{3.7}
\]

Thus neither the mere cap \(|T_*|\le t\) nor positivity of all tangent
squares excludes the optimized Følner family.

## 4. Why the full \(q\)-row block is different

Now take an arbitrary family of \(q\) rows with

\[
 |T_i|=U,\qquad T_i\subseteq T_*,\qquad |T_*|=R.
\tag{4.1}
\]

Write

\[
 W_i=\operatorname{span}_{\mathbb Q}(\lambda_i(X-X)).
\]

Split the ordered tangent-overlap mass into

\[
 P_\perp
 =\sum_{\substack{i\ne j\\W_i\cap W_j=\{0\}}}
 |T_i\cap T_j|
\tag{4.2}
\]

and

\[
 P_\parallel
 =\sum_{\substack{i\ne j\\W_i\cap W_j\ne\{0\}}}
 |T_i\cap T_j|.
\tag{4.3}
\]

The symbol \(\parallel\) here means only rational-space
nontransversality; it is not assumed to be an equivalence relation.

### Theorem 3 (tangent-transversality dichotomy)

Put

\[
 P_0=\frac{q^2U^2}{R}-qU.
\tag{4.4}
\]

Then

\[
 P_\perp+P_\parallel\ge P_0.
\tag{4.5}
\]

Consequently at least one of the following holds:

1. **mixed-transverse tangent branch**

   \[
   P_\perp\ge\frac{P_0}{2};
   \tag{4.6}
   \]

2. **fixed-tangent nontransverse-star branch:** some row \(i\) and
   some tangent square \(\tau\in T_i\) have at least

   \[
   \boxed{\frac12\left(\frac{qU}{R}-1\right)}
   \tag{4.7}
   \]

   distinct partners \(j\) satisfying both

   \[
   \tau\in T_j
   \qquad\text{and}\qquad
   W_i\cap W_j\ne\{0\}.
   \]

In branch 1, some fixed tangent square \(\tau\in T_*\) supports at
least

\[
 \boxed{\frac{P_0}{2R}}
\tag{4.8}
\]

ordered pairs of transverse rows that both contain \(\tau\).

#### Proof

Let \(r_\tau=|\{i:\tau\in T_i\}|\).  Since
\(\sum_\tau r_\tau=qU\), Cauchy--Schwarz gives

\[
\begin{aligned}
 P_\perp+P_\parallel
 &=\sum_\tau r_\tau(r_\tau-1)\\
 &\ge\frac{(qU)^2}{R}-qU=P_0,
\end{aligned}
\]

proving (4.5).

If (4.6) fails, then \(P_\parallel\ge P_0/2\).  Some row \(i\) has
weighted nontransverse degree

\[
 \sum_{\substack{j\ne i\\W_i\cap W_j\ne\{0\}}}
 |T_i\cap T_j|
 \ge\frac{P_0}{2q}.
\]

Expand this sum over the \(U\) tangent squares in \(T_i\).  One
\(\tau\in T_i\) belongs to at least

\[
 \frac{P_0}{2qU}
 =\frac12\left(\frac{qU}{R}-1\right)
\]

nontransverse partner rows, proving the stronger fixed-tangent form
of (4.7).  In branch 1, pigeonhole the mass \(P_\perp\) over the
\(R\) tangent squares to get (4.8).  \(\square\)

### Endpoint substitution

Use

\[
 q=t^{13/18+o(1)},\quad U=t^{5/6+o(1)},\quad
 R=t^{1+o(1)}.
\tag{4.9}
\]

Then

\[
 P_0=t^{19/9+o(1)}
\tag{4.10}
\]

and Theorem 3 says:

- either one tangent square supports \(t^{10/9+o(1)}\) ordered
  transverse row pairs, hence at least \(t^{5/9+o(1)}\) distinct
  rows;
- or one row and one of its tangent squares are shared with
  \(t^{5/9+o(1)}\) nontransverse partners.

This is exactly the network information absent from the optimized
Følner family, whose tangent sets are disjoint.

## 5. Does the frozen block exclude the mechanism?

The answer has two levels.

### Yes: it excludes a full disjoint-tangent Følner block

If all \(q=t^{13/18}\) rows had pairwise disjoint \(U\)-element
tangent sets, their union would have size

\[
 qU=t^{14/9},
\]

contradicting \(R=t\).  More quantitatively, Theorem 3 forces the
mass in (4.10), while the explicit Følner family has zero tangent
overlap.

### No: it does not yet exclude a hybrid block

The forced overlap may concentrate among rows whose rational spaces
already intersect.  Such rows could form large commensurate
subfamilies, while a smaller number of transverse representatives
retain a Følner boundary.  The cap alone does not prevent this
hybrid, and pairwise intersection of general higher-dimensional
\(W_i\)'s is not transitive.

Therefore it would be incorrect to say that the frozen parameters
restore the exact rank theorem.  They instead force the two branches
of Theorem 3.

## 6. Repaired research target

The weakest additional input missing from qualitative stability is
not another rowwise \(o(SU)\) statement.  It is the interaction
between tangent reuse and rational transversality.

The revised target should be:

> Given the full \(q\)-row near-block, resolve the exact
> tangent-transversality dichotomy.  In the mixed branch, turn one
> common tangent square carrying \(t^{10/9}\) transverse row pairs
> into a nondegenerate labelled parabolic cycle.  In the
> fixed-tangent nontransverse-star branch, turn the
> \(t^{5/9}\)-row rational intersection star in one target plane into
> a bounded-denominator affine-height chart or a distance-expanding
> ruled subsystem.

A theorem based only on approximate mask-polynomial divisibility is
now ruled out.  A theorem using either branch above remains plausible
and uses information genuinely forced by the frozen #1083 block.

## 7. Reproduction

The general primitive-direction enumeration, tradeoff bound, and
tangent-transversality split are checked by:

    python3 verify_approximate_transverse_counterexample.py
    python3 -m unittest -v test_approximate_transverse_counterexample.py

The verifier checks general primitive directions \((p,q)\), not only
the simpler \((1,r)\) subfamily.
