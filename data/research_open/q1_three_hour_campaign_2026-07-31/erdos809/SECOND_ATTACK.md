# Erdős #809 — second attack: quantifier-safe budgeted defect

Date: 2026-07-31

Status:
`UNIVERSAL_BD_REFUTED__BCM_CANONICAL_WITNESS_SURVIVES__ALIGNED_CORE_CLOSURE_PROVED`

## 1. Outcome

The budgeted-defect inequality from `FIRST_ATTACK.md` is the correct
algebraic target only **after its quantifier over the BCM witness \(A\) is
specified**.

This attack gives three conclusions.

1. **Universal budgeted defect is false.**  Even in the four-bridge
   two-clique extremal family, there are admissible sets \(A\) of the
   minimum BCM size for which
   \[
   D_A>|E_{\rm good}(A)|-\Phi(n,e)+\Omega(n^2),                \tag{1}
   \]
   where
   \[
   \Phi(n,e)=\frac e2+\frac n2\sqrt{e-\frac{n^2}{4}}.
   \]
   Thus changing raw defect to budgeted defect does not make an
   all-\(A\) assertion true.
2. **The BCM proof-generated witness behaves differently on the same
   family.**  The maximum-degree branch of BCM Lemma 3.1 selects the
   closed neighbourhood of a bridge endpoint in the larger clique.  For
   the extremal colouring, that exact witness has
   \[
   D_A=0.                                                     \tag{2}
   \]
   Hence the no-go result does not refute an existential or canonical
   witness-selection route.
3. **A closable conditional stability theorem is proved.**  Whenever
   \(G\) has an asymptotically complete larger core \(P\) of the extremal
   size, the required colour lower bound follows.  If in addition \(A\)
   contains all but \(o(n)\) vertices of \(P\), then the budgeted-defect
   inequality holds for that \(A\).  A defect exceeding its surplus then
   forces two same-colour edges in a pairwise \(C_7\)-compatible core and
   hence a non-rainbow \(C_7\).

The remaining problem is consequently quantifier-sensitive:

> either produce a BCM-admissible witness aligned with a dense larger
> core, or prove the colour bound in the genuinely non-two-clique branch.

No such global dichotomy is proved here, and Erdős #809 remains open.

## 2. Exact defect notation

Let \(G=(V,E)\) have an edge-colouring \(\chi\), and let
\(A\subseteq V\).  Define
\[
E_{\rm good}(A)
=\{uv\in E:u\in A\text{ or }v\in A\}.
\]
For each colour \(\gamma\), put
\[
M_\gamma(A)
=E_{\rm good}(A)\cap\chi^{-1}(\gamma)
\]
and
\[
D_A
=\sum_\gamma (|M_\gamma(A)|-1)_+.
\]
If
\[
c_A
=|\{\gamma:M_\gamma(A)\ne\varnothing\}|
\]
is the number of colours represented on good edges, then the exact
identity is
\[
c_A=|E_{\rm good}(A)|-D_A.                                   \tag{3}
\]

Thus the finite target associated with the BCM potential is
\[
D_A\le |E_{\rm good}(A)|-\Phi(n,e)+o(n^2),                    \tag{BD}
\]
or equivalently
\[
c_A\ge\Phi(n,e)-o(n^2).                                      \tag{4}
\]

When
\[
e=\left(\frac14+s^2+o(1)\right)n^2,
\qquad 0<s<\frac12,
\]
write
\[
a=\frac12+s,\qquad b=\frac12-s.
\]
Then
\[
\Phi(n,e)
=\left(T(s)+o(1)\right)n^2,
\qquad
T(s)=\frac{a^2}{2}
=\frac18+\frac s2+\frac{s^2}{2}.                             \tag{5}
\]

Equation (3) proves the algebra.  It says nothing about whether (BD)
holds for every, some, or a specially selected admissible \(A\).

### 2.1 Exact compatibility-graph reformulation

Define the **\(C_7\)-compatibility graph** \(\mathcal K_7(G)\) as follows.
Its vertices are the edges of \(G\), and two vertices of
\(\mathcal K_7(G)\) are adjacent precisely when the corresponding two
edges of \(G\) lie on a common \(C_7\).

An edge-colouring of \(G\) makes every \(C_7\) rainbow if and only if it
is a proper vertex-colouring of \(\mathcal K_7(G)\).  Consequently,
\[
\min_{\substack{\chi:\ {\rm every}\ C_7\\{\rm is\ rainbow}}}
|\chi(E(G))|
=\chi(\mathcal K_7(G)),                                      \tag{6a}
\]
and the number of colours represented on the good edges of any such
colouring is at least
\[
\chi\!\left(\mathcal K_7(G)[E_{\rm good}(A)]\right).          \tag{6b}
\]

This gives two possible closure mechanisms.

1. Find a clique of size \(\Phi(n,e)-o(n^2)\) in the good-edge
   compatibility graph, i.e. a pairwise \(C_7\)-compatible edge family.
2. Prove the same lower bound on its chromatic number without requiring
   a clique of that size.

Theorem 5.1 below uses the first, stronger mechanism.  The mixed-witness
construction in Section 3 supplies an actual proper colouring with
fewer than \(\Phi(n,e)-\Omega(n^2)\) colours on the induced good-edge
compatibility graph.  Hence the universal-\(A\) failure occurs already
at the exact compatibility-graph level.

## 3. Universal (BD) is false

### 3.1 The graph and colouring

Let \(p+q=n\), \(p\ge q\), \(p/n\to a\), and \(q/n\to b\).  Take disjoint
cliques \(P,Q\) of sizes \(p,q\), and add four independent bridges
\[
p_iq_i,\qquad 1\le i\le4.
\]
As in `FIRST_ATTACK.md`, write
\[
P^\circ=P\setminus\{p_1,\ldots,p_4\},\qquad
Q^\circ=Q\setminus\{q_1,\ldots,q_4\}.
\]

Inject \(E(Q^\circ)\) into \(E(P^\circ)\), give an edge and its image the
same colour, and give all remaining edges fresh colours.  Every \(C_7\)
is rainbow for **every** such injection.  Indeed, a cycle meeting both
cliques uses an even positive number of independent bridges.

- Four bridges require at least four nonempty within-clique segments, so
  the cycle length is at least eight.
- With two bridges, a within-clique segment containing an edge whose
  endpoints avoid all bridge endpoints has length at least three.  If a
  cycle contained one paired generic edge on each side, its length would
  therefore be at least \(2+3+3=8\).

The number of colours is
\[
\binom p2+4q-6
=\left(\frac{a^2}{2}+o(1)\right)n^2
=\left(T(s)+o(1)\right)n^2.                                  \tag{6}
\]
Thus the construction saturates #809; it is not a counterexample to the
original problem.

### 3.2 A mixed minimum-size witness

Let
\[
r=\left\lfloor\frac{q-1}{2}\right\rfloor,\qquad
t=q-1-r.
\]
Choose
\[
B_P\subseteq P^\circ,\quad |B_P|=r,
\qquad
B_Q\subseteq Q^\circ,\quad |B_Q|=t,
\]
and set
\[
B=B_P\cup B_Q,\qquad A=V\setminus B.
\]
Then
\[
|A|=p+1.                                                      \tag{7}
\]
All eight bridge endpoints lie in \(A\), and the entire graph has
diameter at most three.  Hence every two vertices of \(A\) have distance
at most three.

The exact BCM Lemma 3.1 threshold on this graph is
\[
\begin{aligned}
C_1
&=\frac n2+
\sqrt{e-\frac{n^2}{4}+\frac n2}\\
&=\frac n2+\sqrt{\frac{(p-q)^2}{4}+4}.
\end{aligned}                                                 \tag{8}
\]
If \(p-q\ge4\), then \(C_1<p+1\), so (7) is a fully admissible witness,
not merely an asymptotic one.

Arrange the injection so that every edge of \(G[B_P]\) is paired with a
different edge of \(G[B_Q]\).  This is possible because
\[
\binom r2\le\binom t2
\quad\text{and}\quad
\binom{p-4}{2}\ge\binom{q-4}{2}.
\]
Put
\[
h=\binom r2.
\]
Exactly these \(h\) colour classes have all their edges in \(B\).
There are no additional absent fresh colours: all \(Q^\circ\)-edges are
paired, and every edge of \(G[B_P]\) was used as an image.  Consequently
\[
\begin{aligned}
c_A
&=\binom p2+4q-6-h\\
&=\left(\frac{a^2}{2}-\frac{b^2}{8}+o(1)\right)n^2.           \tag{9}
\end{aligned}
\]
This is quadratically below (5).

The corresponding edge and defect counts are
\[
|E_{\rm good}(A)|
=e-\binom r2-\binom t2
=\left(\frac{a^2}{2}+\frac{b^2}{4}+o(1)\right)n^2,            \tag{10}
\]
\[
D_A
=|E_{\rm good}(A)|-c_A
=\left(\frac{3b^2}{8}+o(1)\right)n^2.                         \tag{11}
\]
The available surplus is only
\[
|E_{\rm good}(A)|-\Phi(n,e)
=\left(\frac{b^2}{4}+o(1)\right)n^2.                          \tag{12}
\]
Subtracting (12) from (11) leaves
\[
\left(\frac{b^2}{8}+o(1)\right)n^2.                           \tag{13}
\]
This proves the claimed asymptotic failure of universal (BD).

The no-go has three useful strengths:

- \(A\) has the minimum BCM size up to an additive constant;
- every bridge endpoint lies in \(A\), so the failure is not caused by a
  disconnected or badly linked witness;
- the graph, colouring, \(L_4(2)\) property, minimum degree, and density
  remain exactly those of the extremal saturating family.

### 3.3 Concrete finite guard

For \(p=120,q=80,n=200\), the verifier obtains
\[
C_1=120.099751\ldots,\qquad |A|=121,
\]
and
\[
\begin{array}{rcl}
|E_{\rm good}(A)|&=&8783,\\
D_A&=&2070,\\
c_A&=&6713,\\
\Phi(n,e)&=&6895.559577\ldots,\\
|E_{\rm good}(A)|-\Phi(n,e)&=&1887.440422\ldots.
\end{array}
\]
Thus \(D_A\) exceeds the finite surplus by more than \(182\), while the
colouring still has every \(C_7\) rainbow.

## 4. What BCM Lemma 3.1 actually quantifies

The statement of BCM Lemma 3.1 is existential:

> \(G\) contains a vertex set \(A\) of the stated size whose vertices
> have pairwise distance at most three.

Its proof supplies three selection branches, in this order.

1. If the maximum degree \(\Delta\ge C_1-1\), choose
   \[
   A=N[v_0]
   \]
   for a maximum-degree vertex \(v_0\).
2. If the first branch fails but the whole graph has diameter at most
   three, one may choose \(A=V\).
3. Otherwise define the threshold \(X\) from pairs at distance more than
   three and choose
   \[
   A=\{v:d(v)>X\}.
   \]

Therefore the BCM argument never establishes an all-\(A\) conclusion.
It is legitimate in a future proof to retain a witness generated by one
of these branches.  It is not legitimate to freeze an arbitrary
admissible \(A\) and then silently promote a claim about that \(A\) to an
existential conclusion.

### 4.1 The canonical witness on the four-bridge family

Take a bridge endpoint \(p_1\) in the larger clique.  It has
\[
d(p_1)=p=\Delta,
\]
and, by (8), \(\Delta\ge C_1-1\) whenever \(p-q\ge4\).  The first branch
therefore gives
\[
A_*=N[p_1]=P\cup\{q_1\}.                                     \tag{14}
\]
This is an exact \(p+1\)-vertex witness.

Under the paired colouring:

- all \(P\)-edges are good;
- all \(Q^\circ\)-edges are bad;
- all \(Q\)-edges incident with \(q_1\) are fresh because \(q_1\notin
  Q^\circ\);
- all four bridges are fresh.

It follows that every good edge has a distinct colour:
\[
D_{A_*}=0,\qquad
c_{A_*}=|E_{\rm good}(A_*)|
=\binom p2+q+3.                                               \tag{15}
\]

This corrects an exact-size subtlety in the informal proposal
“take \(A=P\)”: because of the four extra bridge edges, \(P\) alone is
slightly smaller than the finite threshold \(C_1\).  The closed
neighbourhood \(P\cup\{q_1\}\) is the exact favorable witness.

### 4.2 What this does and does not prove

The comparison between (13) and (15) proves that witness selection is
mathematically substantive, not a cosmetic normalization.

It does **not** prove either of the following global assertions:

\[
\exists A\text{ supplied by BCM Lemma 3.1 such that (BD) holds},         \tag{16}
\]
or the stronger
\[
\exists A\text{ supplied by BCM Lemma 3.1 such that }D_A=o(n^2).         \tag{17}
\]

Both remain open.  In particular, when the diameter-three branch chooses
\(A=V\), (BD) becomes the desired total colour lower bound itself:
\[
D_V=e(G)-|\chi(E(G))|
\le e(G)-\Phi(n,e)+o(n^2).
\]
Thus “choose a favorable witness” is not a free purely graph-theoretic
shortcut; it still needs a colour-sensitive proof or a structural core
that supplies many compatible edges.

## 5. A proved aligned-core closure theorem

The four-bridge family suggests the right stability endpoint: quadratic
defect is harmless when it comes from colour reuse between two cliques,
because the larger clique alone already contributes the target number of
different colours.

### Theorem 5.1 (dense larger-core closure)

Fix \(0<s<1/2\), and put \(a=1/2+s\).  Let \(G_n\) be an \(n\)-vertex
graph with a vertex set \(P_n\) satisfying
\[
|P_n|=(a+o(1))n                                               \tag{18}
\]
and
\[
\binom{|P_n|}{2}-e(G_n[P_n])=o(n^2).                          \tag{19}
\]
If every \(C_7\) in an edge-colouring of \(G_n\) is rainbow, then the
colouring uses at least
\[
\left(\frac{a^2}{2}-o(1)\right)n^2
=\left(T(s)-o(1)\right)n^2                                   \tag{20}
\]
colours.

Suppose additionally that \(A_n\) is any vertex set with
\[
|P_n\setminus A_n|=o(n).                                     \tag{21}
\]
Then the colours represented on \(E_{\rm good}(A_n)\) already satisfy
(20), and hence
\[
D_{A_n}
\le |E_{\rm good}(A_n)|-T(s)n^2+o(n^2).                       \tag{22}
\]

This theorem does not require the edges between \(P_n\) and its
complement, or the graph induced by the complement, to be close to any
particular model.

### Lemma 5.2 (dense graphs give pairwise compatible edges)

If an \(m\)-vertex graph \(H\) satisfies
\[
2\delta(H)-m\ge5
\quad\left(\text{equivalently }\delta(H)\ge\frac{m+5}{2}\right),          \tag{23}
\]
then every two distinct edges of \(H\) lie on a common \(C_7\).

#### Proof

First consider adjacent edges \(uv,vw\).  Choose successively distinct
vertices \(a,b,c\), avoiding the already used vertices, with
\[
wa,ab,bc\in E(H).
\]
Then choose
\[
d\in N(c)\cap N(u)
\]
outside the bounded used set.  This is possible because
\[
|N(c)\cap N(u)|\ge2\delta(H)-m\ge5,
\]
while at most four already used vertices can lie in this intersection.
Now
\[
u-v-w-a-b-c-d-u
\]
is a \(C_7\) containing both specified edges.

For disjoint edges \(uv,wz\), first choose
\[
c\in N(z)\cap N(u)
\]
outside their four endpoints.  Choose a fresh \(a\in N(v)\), and then
\[
b\in N(a)\cap N(w)
\]
outside the used set.  The same intersection bound applies, and
\[
u-v-a-b-w-z-c-u
\]
is the required \(C_7\). \(\square\)

### Proof of Theorem 5.1

Let
\[
\mu_n n^2
=\binom{|P_n|}{2}-e(G_n[P_n]),
\qquad \mu_n\to0.
\]
Delete from \(P_n\) every vertex incident with more than
\(\sqrt{\mu_n}n\) missing edges inside \(P_n\).  The missing-degree sum is
\(2\mu_n n^2\), so only \(O(\sqrt{\mu_n}n)=o(n)\) vertices are deleted.
Call the remaining set \(P_n^0\).

Every vertex of \(G_n[P_n^0]\) has all but \(o(n)\) of the other
vertices as neighbours.  Therefore, for all sufficiently large \(n\),
\[
2\delta(G_n[P_n^0])-|P_n^0|\ge5.
\]
Lemma 5.2 makes all edges of \(G_n[P_n^0]\) pairwise
\(C_7\)-compatible.  They must therefore all have different colours.
Moreover,
\[
\begin{aligned}
e(G_n[P_n^0])
&=\binom{|P_n|}{2}-o(n^2)\\
&=\left(\frac{a^2}{2}-o(1)\right)n^2.
\end{aligned}
\]
This proves (20).

Under (21), apply the same cleaning argument to
\(P_n\cap A_n\).  The resulting compatible core still has
\((a-o(1))n\) vertices and \((a^2/2-o(1))n^2\) edges.  Every one of those
edges is good.  Hence
\[
c_{A_n}\ge\left(T(s)-o(1)\right)n^2.
\]
Equation (3) now gives (22). \(\square\)

### 5.3 Exact “surplus violation gives a bad \(C_7\)” interface

The preceding proof has a useful deterministic form.  Let
\(H\subseteq E_{\rm good}(A)\) be a family of \(h\) edges such that every
two distinct edges of \(H\) lie on a common \(C_7\).  If
\[
D_A>|E_{\rm good}(A)|-h,                                     \tag{24}
\]
then (3) gives \(c_A<h\).  Two edges of \(H\) have the same colour by the
pigeonhole principle, and their common \(C_7\) is not rainbow.

Thus Theorem 5.1 is a genuine conditional closure of the requested form:
in the aligned two-clique stability regime, any defect exceeding the
good-edge surplus produces a forbidden \(C_7\), not merely a weak colour
count.

## 6. Correct next stability target

The all-\(A\) statement is dead.  A quantifier-safe global attack can use
one of the following two forms.

### Form A: canonical-witness dichotomy

For the \(A\) selected by the actual branches of BCM Lemma 3.1, prove
that either

1. \(A\) is aligned, in the sense of (21), with a set \(P\) satisfying
   (18)--(19); or
2. \(E_{\rm good}(A)\) contains
   \((T(s)-o(1))n^2\) pairwise \(C_7\)-compatible edges by another
   structural mechanism.

Theorem 5.1 closes branch 1.  Branch 2 is open.

### Form B: colouring-sensitive existential defect

Prove that for every Case-1 graph and rainbow-\(C_7\) colouring there
exists at least one BCM-admissible witness \(A\) for which
\[
D_A\le |E_{\rm good}(A)|-T(s)n^2+o(n^2).
\]
The mixed witness construction shows that the existential quantifier is
essential.  This form is still essentially the unresolved Case-1 colour
theorem, especially in diameter-three graphs.

The highest-value local problem is now narrower than the first attack's
proposal:

> derive the unbalanced dense-core alternative from a quadratic family
> of zero-codegree / three-path-cover certificates **while retaining the
> canonical BCM witness**.

Without that witness retention, the mixed-\(A\) construction supplies a
quadratic false positive.

## 7. Verification

`verify_809_second_attack.py` checks:

1. the \(p=120,q=80\) mixed witness, its exact BCM size, good-edge count,
   defect, colour count, and finite surplus violation;
2. the maximum-degree closed-neighbourhood witness on the same graph and
   the exact identity \(D_A=0\);
3. all five order-nine isomorphism types satisfying
   \(2\delta-m\ge5\) (their complements are matchings of sizes zero
   through four), as a finite boundary guard for the dense-core
   compatibility lemma.

The regression command

```text
python3 -m unittest -v test_809_second_attack.py
```

returns

```text
Ran 3 tests
OK
```

These computations verify finite constructions and formulas only.  The
proof of Theorem 5.1 is independent of them.

## 8. Claim boundary

- Exact definitions (3) and finite budget target: **proved algebra**.
- Universal (BD), quantified over every admissible \(A\): **false by an
  explicit asymptotic family**.
- Failure even for a minimum-size admissible \(A\): **proved**.
- BCM Lemma 3.1 has an existential, branch-generated witness:
  **verified from the primary source**.
- BCM maximum-degree witness on the four-bridge extremal family has
  \(D_A=0\): **proved exactly**.
- Dense larger-core closure, with aligned-witness (BD) as a corollary:
  **proved, unbounded conditional theorem**.
- Existence of a favorable BCM witness in every fixed-\(s\) Case-1 graph:
  **open**.
- Canonical-witness stability dichotomy: **open**.
- Fixed-\(s\) BCM Case 1 and Erdős #809: **open / not claimed**.
