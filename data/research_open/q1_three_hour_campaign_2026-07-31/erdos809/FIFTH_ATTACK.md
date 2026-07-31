# Erdős #809 — fifth attack: zero-shore structure

Date: 2026-07-31

Status:
`R003_ZERO_SHORE_INTERFACE_AND_QUADRATIC_COLOUR_RECTANGLE_PROVED__GLOBAL_BYPASS_OPEN`

## 1. Outcome

The fourth attack proves the exact coefficient-one charge for every
missing pair in \(B\) having a three-edge shore.  This attack studies
the only exceptional pairs:
\[
bb'\notin E(G[B]),\qquad
\text{no three-edge path from \(b\) to \(b'\)}.              \tag{1}
\]

Three rigorous additions result.

1. If \(h=\lambda(b,b')\) colours use a zero-shore pair, their
   \(A\)-coordinates span an \(h\)-by-\(h\) missing rectangle.  Hence
   \[
   M_A\ge h^2.                                                \tag{2}
   \]
   This improves the earlier \(\binom h2\) consequence.
2. The old R003 no-three-step dichotomy applies with deletion set
   \(S=\varnothing\), and the \(h\) colour pairs occupy the two exclusive
   sides of that decomposition.  In its common-neighbour branch this
   gives the additional bound
   \[
   h\le n-2\delta(G).                                        \tag{3}
   \]
3. Every exact four-edge \(b\)-to-\(b'\) path has the forced form
   \[
   b-p-\ell-q-b',
   \quad p\in N(b),\ q\in N(b'),\
   \ell\notin N(b)\cup N(b').                                \tag{4}
   \]
   The \(L_4(2)\) property says that the hypergraph of these connector
   triples has transversal number at least three.

These statements make the proposed structural bypass precise.  They do
not by themselves force an aligned dense core at fixed \(s>0\): the
R003 exceptional blocks may still have linear size \(2sn\) or \(4sn\).
The remaining theorem is to convert *many* zero-shore excess incidences
into either an aligned compatible core or slack \(S_m\).  Erdős #809
remains open.

## 2. Setup

Use the maximum-degree witness
\[
A=N[v],\qquad B=V\setminus A.
\]
Fix a zero-shore missing pair \(bb'\) as in (1).  Let
\(\Gamma(b,b')\) be the colours \(\gamma\) with same-colour edges
\[
bx_\gamma,\qquad b'y_\gamma,
\qquad x_\gamma,y_\gamma\in A,
\]
and write
\[
h=|\Gamma(b,b')|.
\]

Put
\[
X=\{x_\gamma:\gamma\in\Gamma(b,b')\},\qquad
Y=\{y_\gamma:\gamma\in\Gamma(b,b')\}.                         \tag{5}
\]
Both coordinate maps are injective, so \(|X|=|Y|=h\).

## 3. Quadratic colour rectangle

### Lemma 3.1

The sets \(X,Y\) are disjoint and anticomplete.  Consequently
\[
M_A\ge |X||Y|=h^2.                                           \tag{6}
\]

#### Proof

For each \(\gamma\), inducedness of the pair
\(bx_\gamma,b'y_\gamma\) gives
\[
b'x_\gamma,\ by_\gamma\notin E(G).                           \tag{7}
\]
If \(x_\gamma=y_\eta\) for any \(\gamma,\eta\), then this vertex is both
adjacent and nonadjacent to \(b'\), by its definitions as
\(y_\eta\) and \(x_\gamma\).  Thus \(X\cap Y=\varnothing\).

If some \(xy\) with \(x\in X,y\in Y\) were an edge, then
\[
b-x-y-b'
\]
would be a three-edge shore path, contradicting (1).  Hence all \(h^2\)
distinct pairs in \(X\times Y\) are missing edges of \(G[A]\). \(\square\)

In particular,
\[
\lambda(b,b')\le\lfloor\sqrt{M_A}\rfloor.                    \tag{8}
\]
This is an individual-pair bound.  It is not yet an aggregate bound,
because different zero-shore pairs may force heavily overlapping
missing rectangles in \(A\).

## 4. Exact R003 transplantation

Put
\[
P=N(b),\qquad Q=N(b'),\qquad R=P\cap Q,
\]
\[
W=(P\cup Q)\setminus R,\qquad
L=V(G)\setminus(P\cup Q).                                    \tag{9}
\]
Since (1) is exactly the R003 no-three-step hypothesis with
\(S=\varnothing\), any distinct \(p\in P,q\in Q\) are nonadjacent.

The two R003 branches become:

### Branch I: \(R\ne\varnothing\)

\[
R\ \text{is independent},\qquad E(R,W)=\varnothing,
\]
\[
|R|\ge3\delta-n,\qquad |W|\le2n-4\delta.                     \tag{10}
\]

By (7),
\[
X\subseteq P\setminus Q,\qquad
Y\subseteq Q\setminus P.
\]
Therefore \(X\cup Y\subseteq W\), and (5) gives
\[
2h\le |W|\le2n-4\delta,
\]
which proves (3).

### Branch II: \(R=\varnothing\)

\[
P\cap Q=\varnothing,\qquad E(P,Q)=\varnothing,
\]
\[
|P|,|Q|\ge\delta,\qquad |L|\le n-2\delta.                    \tag{11}
\]
For \(p\in P\) and \(q\in Q\),
\[
d_{G[P]}(p)\ge\delta-|L|,\qquad
d_{G[Q]}(q)\ge\delta-|L|.                                   \tag{12}
\]

Under the fixed-\(s\) Case-1 normalization
\[
\delta\ge(1/2-s-o(1))n,
\]
(10)--(12) give
\[
|W|\le(4s+o(1))n
\]
in Branch I, and
\[
|L|\le(2s+o(1))n
\]
in Branch II.  These errors are \(o(n)\) only in the near-Dirac regime
\(s=o(1)\).  This is why the previously proved R003 closure cannot
simply be cited as a fixed-\(s\) solution.

## 5. Robust connector theorem

### Lemma 5.1 (forced path pattern)

Every simple exact four-edge \(b\)-to-\(b'\) path has the form (4).

#### Proof

Write such a path as
\[
b-p-\ell-q-b'.
\]
Then \(p\in P\) and \(q\in Q\).  The path is simple, so \(p\ne q\).
If \(\ell\in P\), the edge \(\ell q\) would join distinct vertices of
\(P,Q\), forbidden by the zero-shore property.  Likewise
\(\ell\notin Q\).  Hence \(\ell\in L\). \(\square\)

Let \(\mathcal K(b,b')\) be the 3-uniform hypergraph whose edges are the
internal triples
\[
\{p,\ell,q\}
\]
of the paths in Lemma 5.1.

### Lemma 5.2 (robust connector transversal)

\[
\tau(\mathcal K(b,b'))\ge3.                                  \tag{13}
\]
In particular, at least three distinct vertices of \(L\) occur as
middle vertices of exact four-edge \(b\)-to-\(b'\) paths.

#### Proof

If a set \(T\) of at most two internal vertices met every connector
triple, then \(G-T\) would contain no exact four-edge
\(b\)-to-\(b'\) path, contrary to \(L_4(2)\).  This proves (13).

If at most two vertices of \(L\) occurred as middle vertices, deleting
them would hit every connector triple, again contradicting (13).
\(\square\)

This is the additional information supplied by the full Case-1
contract beyond the bare R003 dichotomy.  It rules out one- and
two-hub local models, but does not yet give a linear-size connector
family or a large compatible edge family.

## 6. Aggregate interface

Recall from `FOURTH_ATTACK.md`
\[
E_0
=
\sum_{\substack{bb'\notin E(B)\\bb'\ {\rm zero\ shore}}}
(\lambda(b,b')-1)_+
\]
and
\[
D_B\le M_B+E_0.                                              \tag{14}
\]

The present attack adds the per-pair constraints
\[
\lambda(b,b')^2\le M_A,                                     \tag{15}
\]
and, in R003 Branch I,
\[
\lambda(b,b')\le n-2\delta.                                 \tag{16}
\]
Neither can be summed directly: the missing rectangles \(X\times Y\)
may overlap for different \(bb'\).

The exact structural bypass still needed is:

> If \(E_0=\Omega(n^2)\), then either \(G\) has an aligned
> \((1/2+s-o(1))n\)-vertex core spanning all but \(o(n^2)\) clique
> edges, or \(G\) contains \(T(s)n^2-o(n^2)\) pairwise
> \(C_7\)-compatible edges.

Either conclusion would close the zero-shore branch using
`SECOND_ATTACK.md`.  R003 plus Lemmas 3.1 and 5.2 are the current exact
inputs to that theorem; the theorem itself is not proved here.

## 7. Verification

`verify_809_fifth_attack.py` checks:

1. the \(h^2\) missing rectangle for arbitrary \(h\);
2. the Branch-I inequality \(2h\le |W|\le2n-4\delta\);
3. three disjoint \(P\)-\(L\)-\(Q\) connectors, whose triple
   transversal number is exactly three and which survive deletion of
   any two internal vertices.

The command

```text
python3 -m unittest -v test_809_fifth_attack.py
```

returns

```text
Ran 3 tests
OK
```

The finite guards check only the exact local combinatorics.  They do not
extrapolate the open aggregate bypass theorem.

## 8. Claim boundary

- Zero-shore colour rectangle \(M_A\ge\lambda^2\): **proved**.
- Exact R003 \(S=\varnothing\) transplantation: **proved**.
- Branch-I bound \(\lambda\le n-2\delta\): **proved**.
- Forced \(P\)-\(L\)-\(Q\) path pattern: **proved**.
- Connector transversal number at least three: **proved**.
- Fixed-\(s\) aligned-core/compatible-family bypass: **open**.
- Maximum-degree Case 1 and Erdős #809: **open / not claimed**.
