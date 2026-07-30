# Network inverse audit for the high-correlation branch

Date: 2026-07-29

## Purpose

`HIGH_ENERGY_OVERLAP_STABILITY.md` proves that a small parameter-line count
forces large total correlation between shifted blocks
\[
 S_e=C_e+(Z_u-Z_v)^2
\]
having the same radius product.  This note asks whether graph extraction or
an immediate BSG step can convert that correlation into common
translate/reflection structure among the height sets.

Two rigorous conclusions emerge.

1. Weighted correlation does yield a high-minimum-degree graph, and under an
   explicit threshold it yields many consistency cycles.
2. Those graph facts alone are insufficient.  A finite Hadamard-design
   construction has complete, high-correlation block graphs and very small
   unions while no two blocks are close.  The construction uses arbitrary
   nonnegative block sets, not squared-difference sets.  It identifies
   squared-difference realizability as the indispensable next input.

No unconditional inverse theorem for the actual height sets is proved.

## 1. Dyadic network extraction

Fix one product exponent \(p\).  Let \({\cal B}_p\) be its \(t\) blocks and
write
\[
 w(e,f)=|S_e\cap S_f|,\qquad e\ne f.
\]
Assume \(w(e,f)\leq k\), and let
\[
 W=\sum_{\{e,f\}}w(e,f)
\]
be the unordered correlation mass.

### Theorem 1 (elementary weighted extraction)

There is a dyadic threshold \(r\in\{1,2,4,\ldots\}\), \(r\leq k\), such that
the graph
\[
 G_r=\{\{e,f\}:w(e,f)\geq r\}
\]
satisfies
\[
 r|E(G_r)|\geq
 \frac{W}{1+\lceil\log_2 k\rceil}. \tag{1}
\]
It contains a nonempty subgraph of minimum degree at least
\[
 \frac{|E(G_r)|}{t}. \tag{2}
\]
If the right side of (2) is larger than \(\sqrt t+1\), that subgraph
contains a \(4\)-cycle.

### Proof

For each positive integer weight \(w\leq k\),
\[
 w\leq\sum_{\substack{j\geq0\\2^j\leq w}}2^j.
\]
Summing over edges and pigeonholing the dyadic scales proves (1).  A graph of
average degree \(2|E|/t\) has a nonempty subgraph of minimum degree at least
half its average degree, proving (2).

Finally, if a graph on at most \(t\) vertices has minimum degree \(d\) and
\[
 t\binom d2>\binom t2,
\]
then two vertices have at least two common neighbours, which gives a
\(4\)-cycle.  The displayed sufficient condition on \(d\) implies this
inequality. \(\square\)

This supplies the requested high-average-degree network.  It does not yet
give height-set consistency: the vertices of \(G_r\) are radius pairs, and
for fixed \(p\) those radius pairs form a matching on the original radius
indices.  Thus even a triangle or \(4\)-cycle in \(G_r\) does not share an
original height set along adjacent graph edges.

### Corollary 1.1 (from the global stability failure)

Use the notation of `HIGH_ENERGY_OVERLAP_STABILITY.md`, and suppose
\[
 M\leq I/K,\qquad K>1.
\]
Then some product exponent \(p\) satisfies
\[
 \frac{W_p}{I_p}\geq\frac{K-1}{2}, \tag{3}
\]
where \(I_p=\sum_{e:p(e)=p}|S_e|\) and
\(W_p=\sum_{\{e,f\}}|S_e\cap S_f|\).  At a dyadic threshold in that fibre,
\[
 r|E(G_r)|
 \geq
 \frac{(K-1)I_p}
 {2(1+\lceil\log_2 k\rceil)}. \tag{4}
\]

Indeed, global stability gives ordered correlation at least \((K-1)I\), so
\(\sum_pW_p\geq(K-1)I/2\).  Pigeonholing with weights \(I_p\), followed by
Theorem 1, proves the claim.

This corollary extracts one quantitatively rich product fibre.  It does not
guarantee that the fibre carries a positive proportion of the total mass;
that stronger conclusion needs an additional non-concentration hypothesis.

## 2. Why a direct BSG invocation does not close

The correlation mass is
\[
 |Y_e\cap(Y_f+C_f-C_e)|,
 \qquad Y_e=(Z_u-Z_v)^2.
\]
It is cross-energy among many different sets at prescribed shifts.  It is
not the additive energy of one common set.  Standard BSG can be applied only
after producing a single ambient set or a coherent family with controlled
doubling.  Theorem 1 by itself produces neither.

Quantitatively, if \(t\asymp k\asymp L\) and a product fibre has union size
\[
 U_p=\varepsilon tk,
\]
then Cauchy forces unordered correlation of order \(tk/\varepsilon\).
The dyadic graph has average degree at some scale, but when
\(\varepsilon=o(1)\) that scale can still have only \(o(k)\) overlap per
edge.  Such diffuse correlation does not imply that two blocks differ in
only \(o(k)\) elements.

## 3. An abstract network-level barrier

The next proposition shows that no graph/energy argument treating the
\(Y_e\)'s as arbitrary finite sets can prove the desired inverse statement.

### Proposition 2 (Hadamard block design)

Let \(r\geq2\), \(U=2^r\), and \(k=U/2\).  There are \(t=U-1\) subsets
\[
 H_a\subseteq\{0,\ldots,U-1\},\qquad 1\leq a<U,
\]
such that
\[
 |H_a|=k,\qquad
 |H_a\cap H_b|=k/2,\qquad
 |H_a\mathbin\triangle H_b|=k
 \quad(a\ne b), \tag{5}
\]
and
\[
 \left|\bigcup_aH_a\right|=U=2k. \tag{6}
\]

For any prescribed distinct nonnegative offsets \(C_a\), after adding one
large common constant \(R\), the nonnegative sets
\[
 Y_a=R+H_a-C_a
\]
satisfy
\[
 C_a+Y_a=R+H_a.
\]
Thus their shifted blocks have complete correlation graph with edge weight
\(k/2\), union only \(2k\), and pairwise symmetric difference \(k\).

### Proof

Identify the universe with \(\mathbb F_2^r\).  For every nonzero
\(a\in\mathbb F_2^r\), let
\[
 H_a=\{x:a\cdot x=0\}.
\]
Each is a codimension-one subspace and has \(U/2=k\) elements.  Distinct
nonzero vectors over \(\mathbb F_2\) are linearly independent, so two
hyperplanes intersect in a codimension-two subspace of size \(U/4=k/2\).
This proves (5).  Every \(x\) lies in some such hyperplane when \(r\geq2\),
which proves (6).  Taking \(R\geq\max_aC_a\) proves the shifted-set
statement. \(\square\)

The labels \(x\in\mathbb F_2^r\) may be embedded in the reals as
\(\phi(x)=3^{\operatorname{index}(x)}\).  This preserves every intersection
statement.  Moreover,
\[
 \phi(x_1)+\phi(x_2)=\phi(x_3)+\phi(x_4)
\]
forces equality of the two unordered index pairs by uniqueness of base-three
digits.  Hence the ambient union has only the diagonal additive energy
\(2U^2-U\), the minimum order \(U^2\).  The barrier therefore cannot be
repaired by applying BSG to the ambient union: high block correlation can
coexist with low ordinary additive energy.

The ratio between total block mass and union size in this construction is
of order \(t\), the maximum possible collapse.  Nevertheless, the blocks
are not even approximately equal: every pair differs on \(k\) elements.
The complete graph contains all triangles and \(4\)-cycles, so cycle
extraction does not repair the problem.

### Scope of the barrier

The sets \(Y_a\) in Proposition 2 are arbitrary nonnegative sets.  They are
not asserted to have the special form
\[
 (Z_u-Z_v)^2.
\]
Therefore the proposition is not a counterexample to the geometric-radius
conjecture.  It proves a narrower and useful no-go:

> correlation graphs, second moments, dyadic extraction, and BSG applied
> without squared-difference realizability cannot close the branch.

## 4. Minimum viable inverse lemma

The remaining lemma must use the representation of every block by two
vertex-labelled height sets.

A quantitatively sufficient statement is the following conditional target.

### Conditional target NI

Let \(Z_0,\ldots,Z_{L-1}\) be \(m\)-point real sets, \(m\asymp L\).
For a positive proportion of the central sums \(p\), suppose the shifted
blocks
\[
 T^2(q^u-q^{p-u})^2+(Z_u-Z_{p-u})^2
\]
have union \(o(Lm)\).  Then either

1. the total parameter-line count from all products is
   \(\gg L^3/F^{o(1)}\) by an independent expansion; or
2. there is a subset \(U\subseteq\{0,\ldots,L-1\}\) of size
   \(L/F^{o(1)}\) and one common core \(Z^\circ\), of size
   \(m/F^{o(1)}\), contained in every \(Z_u\), \(u\in U\), after one common
   global translation or reflection.

If alternative 2 holds, the
identical-height/Sidon-offset argument from
`GEOMETRIC_RADIUS_HIGH_ENERGY.md` can be rerun on the common cores, losing
only subpolynomial factors.  Thus NI would close the synchronized
geometric-radius branch.

A formally weaker conclusion in which each \(Z_u\) has its own translation
or reflection does **not** yet suffice: the vertex-dependent translations
enter \(Z_u-Z_v\) as a nontrivial cocycle.  Such an inverse theorem would
need an additional consistency step that makes those translations constant
on a large subfamily.

NI is not proved.  Proposition 2 shows that its proof must use consistency
of the labelled representations \(Y_{uv}=(Z_u-Z_v)^2\), not only the
abstract block network.

## 5. Computational audit

`verify_network_inverse_barrier.py` verifies the Hadamard construction,
the dyadic extraction inequality, and the existence of \(4\)-cycles in the
resulting complete correlation graph.
