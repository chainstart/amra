# Iterated partner-coordinate reuse networks

Date: 2026-07-30

## Purpose

`REAL_MULTI_HUB_REUSE.md` constructs one real coordinate with
\(\Theta(U^2)\) hub-pair services.  The only remaining local-to-global
question is whether the partner coordinates can themselves be centres of
many such stars.

This note gives an exact answer for the anchor-coherent subnetwork, in which
all hub witnesses use one common height \(A\).  After translating \(A\) to
zero, the quadratic service equation becomes an additive Cayley graph for
the difference set of the exponential moment curve
\[
 H=\{(u,B^u):u\in{\cal U}\},\qquad B=q^2\geq4.
\]
The pointwise \(U^2\)-star remains possible, but its dense iteration is not:
the graph satisfies
\[
\begin{aligned}
 \sum_{n\in N}d(n)^2
   &\ll U\sum_{n\in N}d(n)+|N|^2,\\
 \sum_{n\in N}d(n)
   &\ll |N|U+|N|^{3/2}. \tag{1}
\end{aligned}
\]
For \(|N|\leq Lm\) and \(m\asymp L\), this is
\[
 \sum_n d(n)\ll L^2U+L^3. \tag{2}
\]
At \(U=L^\alpha\), \(\alpha\geq5/6+2\eta\), (2) has the required form
\[
 U^{2-c}L^{2+o(1)}
\]
for every
\[
 c\leq 2-\frac1\alpha.
\]
At \(\eta=0\) this permits \(c=4/5\), stronger than the required \(2/5\).
More generally,
\[
 2-\frac1{5/6+2\eta}
 =\frac{4+24\eta}{5+12\eta}
 >\frac{2+30\eta}{5+12\eta}
\]
whenever \(\eta<1/3\).  In the nonvacuous range
\(5/6+2\eta\leq1\), namely \(\eta\leq1/12\), this exponent is also at
most one, as required to absorb the \(L^2U\) term.

This is a genuine positive result, but it is not yet an unconditional
improvement for the original four-height energy.  With varying hub anchors,
the additive state decomposes and the common-neighbour lemma below no longer
applies.  The exact missing step is an anchor-coherence extraction or a
replacement codegree theorem for the full four-part hypergraph.

No unconditional exponent improvement is claimed.

## 1. The labelled service hypergraph

Let
\[
 \rho_j=Tq^j,\qquad C_{ij}=(\rho_i-\rho_j)^2.
\]
A service is a labelled four-tuple
\[
 ((u,a),(v,z),(x,c),(y,d))
\]
with
\[
 u+v=x+y,\qquad
 C_{uv}+(a-z)^2=C_{xy}+(c-d)^2. \tag{3}
\]
The coordinate vertices are the pairs \((j,t)\), \(t\in Z_j\).  Projecting
a service onto \((v,z)\)--\((y,d)\) gives a labelled multigraph edge; its
label retains the two hub-coordinate vertices \((u,a),(x,c)\).

Equivalently, define the pair-state map
\[
 {\cal K}((u,a),(v,z))
 =
 \left(
 u+v,\,
 \rho_u^2+\rho_v^2+(a-z)^2
 \right). \tag{4}
\]
Because \(\rho_u\rho_v=T^2q^{u+v}\), equation (3) is exactly equality of the
two pair states in (4).  Thus the full network is a four-part collision
hypergraph for \({\cal K}\).

The term \(-2az\) in \((a-z)^2\) prevents (4) from splitting into a hub
state plus a nonhub state when \(a\) varies.  This is the obstruction that
remains at the end of this note.

## 2. Additive linearization under a common anchor

Suppose every selected hub coordinate is the same real height \(A\).
Translate all heights by \(A\), and put
\[
 w(v,z)=(z-A)^2+\rho_v^2,\qquad
 n(v,z)=(v,w(v,z)),
\]
and
\[
 h_u=(u,\rho_u^2).
\]
Then (3) is equivalent to
\[
 n(v,z)+h_u=n(y,d)+h_x. \tag{5}
\]
Indeed the two radial products cancel because \(u+v=x+y\).

Let
\[
 H=\{h_u:u\in{\cal U}\},\qquad
 D=(H-H)\setminus\{0\}. \tag{6}
\]
For a finite coordinate-state set \(N\), form the simple graph \(G_D[N]\)
by joining \(n,n'\) when \(n'-n\in D\).  Equation (5) identifies every
oriented edge with one service.  The label \((u,x)\) is unique: the first
coordinate gives \(u-x\), and strict convexity of \(B^j\), or the
\(B_2\) property below, determines the ordered pair.

Thus
\[
 d(n)=|(n+D)\cap N| \tag{7}
\]
is exactly the number of anchor-coherent services using \(n\).

The map \(z\mapsto(z-A)^2\) is at most two-to-one.  If a height set contains
both \(A+t\) and \(A-t\), retain the state multiplicity.  This replaces the
simple graph by a blow-up of multiplicity at most two at each vertex and
changes all estimates below by absolute constants only.  Equivalently, split
each state into its two signs before applying the count.

This formulation explicitly retains reuse of the same coordinate across
different product fibres.  The single-star construction is simply
\[
 \{n_0\}\cup(n_0+D),
\]
for which \(d(n_0)=U(U-1)\).

## 3. The exponential \(B_4\) lemma

### Lemma 1

For an integer \(B\geq4\), the set
\[
 H_U=\{(j,B^j):0\leq j<U\}
\]
is a \(B_4\) set: equality between two sums of at most four elements, with
the same number of summands, forces equality of the two multisets.

### Proof

For \(B\geq5\), every base-\(B\) digit multiplicity lies between zero and
four, so uniqueness of base-\(B\) expansion proves the assertion from the
second coordinate alone.

For \(B=4\), let \(j\) be the least exponent whose multiplicities differ.
Modulo \(4^{j+1}\), their difference at \(j\) must be \(0\) or \(\pm4\).
The zero case contradicts the choice of \(j\).  The value \(\pm4\) consumes
all four available summands on one side at exponent \(j\); any already
matched lower term would make this impossible.  The other side would have
to replace those four terms by one term at \(j+1\), but it must still have
the same number of positive summands.  The remaining three terms make its
sum strictly larger.  Hence carrying is impossible. \(\square\)

The same conclusion holds for an arbitrary subset of exponent indices.

## 4. Exact common-neighbour classification

### Lemma 2

Let \(D=(H_U-H_U)\setminus\{0\}\).  For every nonzero translation \(t\),
\[
 |D\cap(D+t)|
 \leq
 \begin{cases}
 2U-4,&t\in D,\\
 4,&t\notin D.
 \end{cases} \tag{8}
\]
For \(t\in D\), equality holds.

### Proof

Write \(t=h_a-h_b\).  The \(2U-4\) solutions are
\[
\begin{aligned}
 (h_a-h_r)-(h_b-h_r)&=t,\\
 (h_r-h_b)-(h_r-h_a)&=t,
\end{aligned}
\qquad r\notin\{a,b\}. \tag{9}
\]
The \(B_3\) consequence of Lemma 1 shows that these are all the solutions.

Now suppose \(t\notin D\cup\{0\}\), and write
\[
 t=(h_i-h_j)-(h_k-h_l).
\]
The positive two-multiset \(\{i,l\}\) and negative two-multiset
\(\{j,k\}\) are disjoint; otherwise cancellation would put \(t\) in
\(D\cup\{0\}\).  Comparing two representations and applying Lemma 1 to
the resulting equality of four-term sums fixes these positive and negative
multisets.  There are at most two orders within each, hence at most four
representations. \(\square\)

Lemma 2 is the first constraint that excludes dense iteration of the
single-star example.  It also explains why looking only for an unlabelled
4-cycle was too coarse: adjacent star centres may have \(\Theta(U)\) common
partners, but all other centre pairs have only \(O(1)\).

## 5. The global second moment

### Theorem 3

For every finite \(N\subset\mathbb R^2\), with \(n=|N|\), the graph
\(G_D[N]\) satisfies (1).

### Proof

Let \(e\) be its number of unoriented edges.  Count a length-two path by its
middle vertex and then by its endpoint pair.  Lemma 2 gives
\[
\begin{aligned}
 \sum_{v\in N}\binom{d(v)}2
 &=
 \sum_{\{p,q\}\subset N}|(p+D)\cap(q+D)\cap N|\\
 &\leq
 (2U-4)e+4\left(\binom n2-e\right)\\
 &\ll Ue+n^2. \tag{10}
\end{aligned}
\]
Since \(\sum_vd(v)=2e\),
\[
 \sum_vd(v)^2\ll U\sum_vd(v)+n^2. \tag{11}
\]
Cauchy--Schwarz now gives
\[
 \left(\sum_vd(v)\right)^2
 \leq n\sum_vd(v)^2
 \ll nU\sum_vd(v)+n^3.
\]
Solving the quadratic inequality yields
\[
 \sum_vd(v)\ll nU+n^{3/2}. \tag{12}
\]
Substitution into (11) also gives the explicit second-moment form
\[
 \sum_vd(v)^2
 \ll nU^2+Un^{3/2}+n^2. \tag{13}
\]
\(\square\)

For the coordinate universe,
\[
 n\leq\sum_v|Z_v|\leq Lm.
\]
Equations (2) and the claimed exponent comparison follow from
\(m\asymp L\).  The explicit second moment (13) also satisfies
\[
 \sum_vd(v)^2
 \lesssim U^{4-2c}L^{2+o(1)}
\]
at \(U\geq L^\alpha\) for every \(c\leq2-1/\alpha\).

## 6. Why 4-, 6- and 8-cycles do not individually obstruct reuse

The state sum in (5) decomposes the graph into collision cliques.  Fix a
product index \(P\), a sufficiently large \(W\), and for every hub \(u\)
put a coordinate in radius class \(v=P-u\) with
\[
 (z_u-A)^2=W-\rho_u^2-\rho_{P-u}^2. \tag{14}
\]
Then
\[
 n(P-u,z_u)+h_u=(P,W) \tag{15}
\]
for every \(u\).  Hence these \(U\) coordinate nodes form a complete
service clique.  It contains simple cycles of every length from three to
\(U\), including 4, 6 and 8.  Taking \(m\) different large values of \(W\)
gives \(m\) disjoint parallel cliques while using exactly \(m\) coordinates
in each receiving height set.

All their squared distances are equal:
\[
 C_{u,P-u}+(z_u-A)^2=W-2T^2q^P. \tag{16}
\]
Thus every minimum cycle constraint is exactly saturated over the reals.
The saving in Theorem 3 comes from the global intersection pattern of star
neighbourhoods, not from forbidding a particular short cycle.

There are also purely label-balanced cycles.  Along a closed walk, (5)
requires
\[
 \sum_i(u_i-x_i)=0,\qquad
 \sum_i(\rho_{u_i}^2-\rho_{x_i}^2)=0. \tag{17}
\]
If the source- and target-hub label multisets agree, both equations telescope
identically.  Permutation cycles of lengths 6 and 8 therefore carry no new
real-order information.

## 7. The exact remaining gap: varying anchors

For general services, (4) is still an exact collision representation, but
it is not additive:
\[
 \rho_u^2+\rho_v^2+(a-z)^2
 =
 \rho_u^2+a^2+\rho_v^2+z^2-2az. \tag{18}
\]
The bilinear term depends simultaneously on the hub coordinate and the
nonhub coordinate.  Consequently:

1. a projected node difference no longer determines its hub-pair label;
2. two star neighbourhoods are not translates of one fixed \(B_4\)
   difference set;
3. the codegree dichotomy (8) is no longer available after mixing anchor
   pairs; and
4. splitting by the two hub anchors costs up to \(m^2\), far beyond the
   available saving.

Theorem 3 applies verbatim to any selected subnetwork whose two hub
witnesses share one common height \(A\).  It does not show that a large
general network contains such a subnetwork with sufficient mass.

The precise next lemma would be one of:

> **Anchor-coherence extraction.** A service network above the required
> mass contains, after losing only \(U^{o(1)}L^{o(1)}\), a common-anchor or
> bounded-anchor-rank subnetwork.

or

> **Full hypergraph codegree.** The collision hypergraph of (4) obeys an
> analogue of (11), with an error that is absorbed by the joint triangle
> moment.

Neither statement is proved here.  The complete-clique construction shows
that 4/6/8-cycle existence alone cannot replace them.

## 8. Status

The iterated-reuse problem is solved with a power saving in the
anchor-coherent model.  Its \(c=4/5\) benchmark at \(\eta=0\) is more than
the \(c=2/5\) needed by the hub dichotomy.  The remaining obstruction is now
strictly localized to mixing different hub heights in the same projected
coordinate network.

No unrestricted real second-moment theorem, no improvement of the
\(3/5\) distance exponent, and no publication claim is made.

## 9. Verification

`verify_iterated_partner_reuse.py` checks the \(B_4\) property, the exact
codegree classification, the two-path identity, the moment bound, the
single-star degree and the parallel complete-clique realization of
4/6/8-cycles.
