# Erdős #809 — fourth attack: fixed-pair congestion

Date: 2026-07-31

Status:
`NONEMPTY_SHORE_CONGESTION_EXACTLY_ONE__ZERO_SHORE_ENERGY_IDENTIFIED__RESIDUAL_OPEN`

## 1. Outcome

This attack continues only the centered maximum-degree branch from
`THIRD_ATTACK.md`.  Put
\[
A=N[v],\qquad B=V\setminus A,
\]
and recall the exact target
\[
D_A\le M_B+S_m+o(n^2),                                      \tag{1}
\]
where \(M_B\) is the number of missing edges in \(G[B]\).

The cross-colour congestion problem has a sharp local classification.

1. For a fixed missing pair \(bb'\) in \(B\), every colour using edges
   \(bx,b'z\), with \(x,z\in A\), supplies a two-vertex cover
   \(\{x,z\}\) of the shore graph of three-edge \(b\)-to-\(b'\) paths.
2. If at least one such three-edge path exists, then at most **one**
   colour can use the missing pair:
   \[
   \lambda(b,b')\le1.                                       \tag{2}
   \]
   Inducedness fixes the coordinate roles on a shore path; simultaneous
   left- and right-rooted colours create an explicit non-rainbow
   \(C_7\).
3. If no three-edge path exists, the cover condition is vacuous and
   local congestion is unbounded.  Such a zero-shore pair nevertheless
   forces at least
   \[
   \binom{\min\{d_A(b),d_A(b')\}}2                           \tag{3}
   \]
   missing edges inside \(A\).
4. An explicit \(A\)-energy threshold therefore eliminates all
   zero-shore pairs and gives the coefficient-one aggregate estimate
   \[
   D_B\le M_B,                                               \tag{4}
   \]
   where \(D_B\) is the defect contributed by extra chosen outer
   endpoints in \(B\).

Thus the desired coefficient-one cross-colour charge is complete when
zero-shore pairs are excluded.  The remaining obstacles are the total
multiplicity on zero-shore pairs and the outer-\(A\) residual defect.
No graph/colouring satisfying the full Case-1 contract and violating
(1) was constructed.  Erdős #809 remains open.

## 2. Fixed-pair shore graph

Retain the maximum-degree setup and \(L_4(2)\).  Fix a missing edge
\[
bb'\notin E(G[B]).
\]
Define the **shore graph**
\[
\mathcal H(b,b')
\]
whose vertices lie in \(V(G)\setminus\{b,b'\}\), and whose edges are
the unordered pairs \(\{p,q\}\) for which
\[
b-p-q-b'                                                    \tag{5}
\]
is a simple three-edge path, in one of the two orientations.

Let \(\Gamma(b,b')\) be the set of colours \(\gamma\) for which there
are good edges
\[
bx_\gamma,\qquad b'z_\gamma
\]
of colour \(\gamma\), with
\[
x_\gamma,z_\gamma\in A.                                    \tag{6}
\]
Because a colour class is an induced matching,
\[
x_\gamma\ne z_\gamma.
\]
As \(\gamma\) varies, both coordinate maps are injective: the
\(x_\gamma\) are distinct because \(bx_\gamma\) has one colour, and the
\(z_\gamma\) are distinct for the same reason at \(b'\).

## 3. Exact fixed-pair theorem

### Lemma 3.1 (every colour gives a shore cover)

For every \(\gamma\in\Gamma(b,b')\),
\[
C_\gamma=\{x_\gamma,z_\gamma\}
\]
is a vertex cover of \(\mathcal H(b,b')\).

#### Proof

The same-colour edges in (6), together with the fixed center \(v\), give
the four-edge path
\[
b-x_\gamma-v-z_\gamma-b'.
\]
A shore path cannot contain \(v\), since \(b,b'\in B=V\setminus N[v]\).
By the center-collapse lemma in `THIRD_ATTACK.md`, any three-edge
\(b\)-to-\(b'\) path avoiding \(x_\gamma,z_\gamma\) would complete the
centered path to a non-rainbow \(C_7\).  Hence every shore edge meets
\(C_\gamma\). \(\square\)

### Theorem 3.2 (nonempty-shore congestion at most one)

If
\[
E(\mathcal H(b,b'))\ne\varnothing,
\]
then
\[
|\Gamma(b,b')|\le1.                                        \tag{7}
\]

#### Proof

Fix one shore path
\[
b-p-q-b'.                                                   \tag{8}
\]
Every cover \(C_\gamma\) contains \(p\) or \(q\).  The induced-matching
condition forces the roles:

- if \(p\in C_\gamma\), then \(p=x_\gamma\), since the edge \(bp\)
  rules out \(p=z_\gamma\);
- if \(q\in C_\gamma\), then \(q=z_\gamma\), since the edge \(qb'\)
  rules out \(q=x_\gamma\);
- a cover cannot contain both \(p\) and \(q\), since the shore edge
  \(pq\) would join the two same-colour edges.

Thus every colour is of exactly one of two types:
\[
(x_\gamma,z_\gamma)=(p,a)
\quad\hbox{or}\quad
(x_\eta,z_\eta)=(c,q).                                     \tag{9}
\]
There is at most one colour of the first type, because \(bp\) has one
colour, and at most one of the second type, because \(b'q\) has one
colour.

Suppose both types occur.  We have \(a\ne c\): otherwise the edge
\(bc\) from the second pair would be a cross edge between the two edges
\(bp,b'a\) of the first colour.  The matching and cover-role conditions,
together with the center-collapse lemma, make
\[
b,p,q,b',a,v,c
\]
seven distinct vertices.  They form the cycle
\[
b-p-q-b'-a-v-c-b.                                          \tag{10}
\]
This \(C_7\) contains both \(bp\) and \(b'a\), which have colour
\(\gamma\).  It is not rainbow, a contradiction.  Therefore the two
types cannot coexist, proving (7). \(\square\)

The constant one is locally sharp: a single colour may cover one shore
edge.  If there are three internally vertex-disjoint three-edge
\(b\)-to-\(b'\) paths, then no two-vertex set covers their three
disjoint internal pairs, so the stronger conclusion
\[
\Gamma(b,b')=\varnothing                                   \tag{11}
\]
holds.

## 4. Exceptional zero-shore pairs

Theorem 3.2 has one local exception:
\[
E(\mathcal H(b,b'))=\varnothing.                            \tag{12}
\]
Then every coordinate pair in (6) is vacuously a shore cover, so the
centered certificate alone allows arbitrary congestion.

### Lemma 4.1 (zero shore forces missing energy in \(A\))

If (12) holds, then
\[
M_A\ge
\binom{\min\{d_A(b),d_A(b')\}}2.                            \tag{13}
\]

#### Proof

There is no edge with distinct endpoints
\[
p\in N_A(b),\qquad q\in N_A(b'),
\]
because it would give the shore path \(b-p-q-b'\).

For two sets of sizes \(c,d\), the number of distinct unordered pairs
with one endpoint in each is minimized when the smaller set coincides
with a subset of the larger.  The minimum is
\[
\binom{\min\{c,d\}}2.
\]
Every such distinct pair is a missing edge of \(G[A]\), proving (13).
\(\square\)

Put
\[
\ell_A=\max\{0,\delta(G)-|B|+1\}.                            \tag{14}
\]
Every \(b\in B\) has at most \(|B|-1\) neighbours in \(B\), so
\[
d_A(b)\ge\ell_A.
\]

### Corollary 4.2 (uniform nonempty-shore threshold)

If
\[
M_A<\binom{\ell_A}{2},                                      \tag{15}
\]
then every missing pair in \(B\) has a nonempty shore graph and hence
congestion at most one.

When the maximum-degree witness exceeds its minimal asymptotic size by
\(\theta n\), one has \(\ell_A\gtrsim\theta n\).  Thus (15) is a
genuine quadratic missing-energy threshold.

The same reasoning inside \(B\) gives, for a zero-shore pair,
\[
M_B\ge
\binom{\min\{d_B(b),d_B(b')\}}2,                            \tag{16}
\]
recovering the rich-outer rectangle theorem from `THIRD_ATTACK.md`.

## 5. Aggregate accounting

Fix an orientation into \(A\) for every good edge.  For a colour
\(\gamma\), let \(t_\gamma\) be the number of its good edges whose
chosen outer endpoint lies in \(B\).  Define
\[
D_B=\sum_\gamma(t_\gamma-1)_+.                              \tag{17}
\]
Always \(D_B\le D_A\).

As proved in `THIRD_ATTACK.md`,
\[
\sum_\gamma\binom{t_\gamma}{2}
=
\sum_{\{b,b'\}\in\overline E(G[B])}\lambda(b,b'),            \tag{18}
\]
and
\[
(t_\gamma-1)_+\le\binom{t_\gamma}{2}.
\]

Let \(\mathcal Z_0\) be the set of zero-shore missing pairs in \(B\), and
put
\[
E_0
=
\sum_{\{b,b'\}\in\mathcal Z_0}
(\lambda(b,b')-1)_+.                                        \tag{19}
\]
Theorem 3.2 and (18) give the unconditional residual form
\[
D_B\le M_B+E_0.                                              \tag{20}
\]
Thus only the multiplicity *beyond the first colour* on zero-shore
pairs escapes the \(M_B\) budget.

### Theorem 5.1 (aggregate coefficient-one threshold)

Under (15),
\[
D_B\le M_B.                                                  \tag{21}
\]

Indeed, Corollary 4.2 gives \(\mathcal Z_0=\varnothing\), so
\(E_0=0\) in (20).  If every missing pair has three internally
vertex-disjoint shore paths, then \(D_B=0\).

## 6. Explicit conditional closure

Put
\[
R_A=D_A-D_B\ge0.                                             \tag{22}
\]
This is the residual defect from colour classes whose extra good edges
cannot all be charged after rooting their \(B\)-outer part.  It includes
the low-\(B\)-degree outer-\(A\) residue identified in
`THIRD_ATTACK.md`.

Recall the exact surplus
\[
|E_{\rm good}(A)|-\Phi(n,e)=M_B+S_m.
\]

### Corollary 6.1 (coefficient-one conditional closure)

Without any shore-energy threshold, the sufficient condition
\[
R_A+E_0\le S_m                                               \tag{23}
\]
implies
\[
D_A=R_A+D_B\le S_m+M_B,
\]
so the maximum-degree branch closes exactly.

In particular, under (15) one has \(E_0=0\), so it is enough that
\[
R_A\le S_m.                                                  \tag{24}
\]

In particular, if every non-singleton good colour class is
\(B\)-supported, meaning all its good edges can be oriented with their
outer endpoints in \(B\), then \(R_A=0\).  Under (15), every such
instance closes without any further slack requirement.

## 7. Sharp barriers

### 7.1 One is locally sharp

Take vertices
\[
\{v,b,b',p,q,a\}
\]
and edges
\[
vp,\ va,\ bp,\ pq,\ qb',\ b'a.
\]
Give \(bp,b'a\) one colour.  They form an induced matching, the shore
graph for \(bb'\) contains \(\{p,q\}\), and there is no \(C_7\) because
the graph has six vertices.  Hence \(\lambda(b,b')=1\).

### 7.2 Empty shore permits arbitrary local congestion

For any \(h\), take vertices
\[
v,b,b',x_1,z_1,\ldots,x_h,z_h
\]
and edges
\[
vx_i,\ vz_i,\ bx_i,\ b'z_i.
\]
Put \(A=N[v]\), and give \(bx_i,b'z_i\) the common colour
\(\gamma_i\).  The graph is bipartite, so it has no \(C_7\), and the
shore graph for \(bb'\) is empty.  Therefore
\[
\lambda(b,b')=h.                                             \tag{22}
\]

This graph fails the Case-1 density and \(L_4(2)\) hypotheses.  It is
not a counterexample under the original contract.  It proves that
global hypotheses are indispensable for controlling zero-shore
multiplicity.

### 7.3 What was not constructed

No family satisfying

- the Case-1 density and minimum degree;
- \(L_4(2)\);
- \(A=N[v]\) for a maximum-degree vertex; and
- a rainbow-\(C_7\) colouring

was found with aggregate defect exceeding \(M_B+S_m+o(n^2)\).
Therefore this attack does not refute the canonical-charge route.

## 8. Exact remaining gap

The maximum-degree branch is now split into three layers.

1. **Nonempty shores:** fixed-pair congestion has exactly the
   coefficient-one bound required by the missing-edge budget.
2. **Empty shores:** each exceptional pair forces the quadratic
   \(A\)-missing energy (13), but its colour multiplicity is not yet
   globally charged.  Its exact unabsorbed amount is \(E_0\).
3. **Outer-\(A\) residue:** it is measured exactly by \(R_A\).

To reach (1) without extra hypotheses, one must charge the total
multiplicity of zero-shore pairs to their forced \(A\)-missing energy
and simultaneously absorb \(R_A\) into \(S_m\).  This requires overlap
control between exceptional neighbourhood rectangles, the Case-1
edge-energy identity, or a stability decomposition.

This is a narrower gap than the centered-charge statement in
`THIRD_ATTACK.md`, but it is not closed.

## 9. Verification

`verify_809_fourth_attack.py` checks:

1. the sharp one-colour nonempty-shore example;
2. the explicit non-rainbow \(C_7\) forced by simultaneous left- and
   right-rooted colours;
3. coordinate-injective congestion 40 with an empty shore;
4. the exact double count (18) and rooted-extra inequality;
5. the zero-shore missing-energy bound on overlapping neighbourhood
   sets.

The command

```text
python3 -m unittest -v test_809_fourth_attack.py
```

returns

```text
Ran 5 tests
OK
```

These are finite local certificates.  Theorems 3.2 and 5.1 and the
conditional closure are proved independently above.

## 10. Claim boundary

- Fixed-pair cover formulation: **proved**.
- Nonempty-shore congestion \(\lambda\le1\): **proved and sharp**.
- Three disjoint shores force \(\lambda=0\): **proved**.
- Zero-shore \(A\)-missing-energy bound: **proved**.
- Aggregate coefficient-one theorem under (15): **proved, unbounded
  conditional theorem**.
- Unconditional residual estimate \(D_B\le M_B+E_0\): **proved**.
- Conditional closures (23)--(24): **proved**.
- Aggregate control of zero-shore multiplicity: **open**.
- Absorption of the outer-\(A\) residual \(R_A\): **open**.
- A full-contract counterexample to the canonical charge: **not found**.
- Maximum-degree Case 1 and Erdős #809: **open / not claimed**.
