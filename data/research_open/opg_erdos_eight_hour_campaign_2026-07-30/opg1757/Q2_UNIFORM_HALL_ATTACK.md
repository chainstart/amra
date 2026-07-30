# OPG-1757: a uniform Hall attack for the \(q=2\) reserve graph

Date: 2026-07-30

## 0. Status

- **HUMAN PROOF:** the candidate Hall condition admits the exact
  fibre-excess reformulation below.
- **HUMAN PROOF:** protected basis exchanges are graphic-matroid exchanges;
  without the active-set deletion, each fixed-cardinality forest exchange
  graph is connected.
- **FINITE EVIDENCE:** the reserve-expanded graphs have full matchings at
  \(k=5,6,7,8\); the older direct/single certificates cover \(k\le4\).
  Hence every possible nonempty \(q=2\) layer is computationally certified
  in the current model.
- **OPEN GAP:** the fibre-excess inequality has not been proved uniformly.
  Symmetric exchange alone does not supply the required vertex expansion.

No symbolic all-\(k\) injection theorem is claimed in this note.

## 1. The \(q=2\) range is finite but structure still matters

The \(q=2\) reduced model lives on the six vertices
\[
\{0,1,2,3,4,5\}.
\]
Each colour is a forest and therefore contains at most five edges.  Since a
layer-\(k\) pair has \(k+2\) coloured edge copies,
\[
k+2\le10,\qquad k\le8.                              \tag{1}
\]
The active condition makes the layers below \(k=1\) empty.  Thus a literal
“all \(k\)” theorem for \(q=2\) has only eight nonempty cases.

The current certificates cover \(k=1,\ldots,8\), so finite checking has
settled the fixed \(q=2\) model.  The purpose here is stronger: isolate an
inequality that might survive when the number of active vertices grows.

## 2. Graphic-matroid formulation

Let \(M=M(K_6)\) be the graphic matroid on the edge set \(\mathcal E\).
Write \(\mathcal N_k\) and \(\mathcal P_k\) for the negative and positive
forest pairs, respectively.  The marked conditions are
\[
\begin{aligned}
(R,B)\in\mathcal N_k &: E\notin R,\ E,F\in B,\\
(R,B)\in\mathcal P_k &: E\in R,\ E\notin B,\ F\in B.
\end{aligned}
\]

For a source \(s\in\mathcal N_k\), define:

- \(\psi(s)\in\mathcal P_k\): its deterministic global cycle-opening
  target;
- \(D(s)\subseteq\mathcal P_k\): every valid direct or single
  \(E\leftrightarrow x\) target.

Define \(H_k\) on \(\mathcal P_k\).  Two positive objects are adjacent when
one is obtained from the other by one protected exchange
\[
C\longmapsto C-a+b
\]
in one colour, with the active set preserved.  Include a loop at every
vertex by using the closed neighbourhood \(N_H[y]\).

The candidate neighbourhood of a source is exactly
\[
\Gamma(s)=D(s)\cup N_H[\psi(s)].                    \tag{2}
\]

The graph \(H_k\) is contained in a Cartesian product of two
fixed-cardinality independent-set exchange graphs of \(M\).  Protection of
\(E,F\) is deletion/contraction to a matroid minor.  The active-set
condition then deletes some product vertices and exchange edges.

## 3. What symmetric exchange proves—and what it does not

For a matroid, two independent sets \(I,J\) of equal size can be connected
by exchanges that successively increase \(|I\cap J|\).  Applied in one
colour at a time, this proves connectivity of the unrestricted
fixed-size product exchange graph.

This observation supplies:

1. existence of legal local moves;
2. reversibility of an exchange edge;
3. paths between objects inside an unrestricted size component.

It does not supply:

1. vertex expansion of every subset;
2. preservation of the active union along the connecting path;
3. enough distinct neighbours to absorb several sources with the same
   deterministic target;
4. bridges between different red/blue size splits.

The direct targets \(D(s)\) are essential for item 4.  At \(k=5\), using
only the deterministic target and its reserve neighbourhood leaves a
finite deficit, whereas adding all direct/single targets gives a full
matching.

Consequently, a bare citation of symmetric basis exchange cannot prove the
desired injection.

## 4. Exact fibre reduction

For \(y\in\mathcal P_k\), let
\[
\mathcal F_y=\psi^{-1}(y)
\]
be the deterministic-opening fibre.  The tagged inverse theorem gives
\[
|\mathcal F_y|\le 1+|B_y\setminus R_y|,              \tag{3}
\]
but this congestion bound alone cannot pay unit source weights.

Given a nonempty source set \(S\subseteq\mathcal N_k\), put
\[
A=\psi(S)
\]
and, for every \(y\in A\),
\[
T_y=S\cap\mathcal F_y.
\]
All sources in one fibre have the same reserve neighbourhood.  Therefore
(2) gives the exact identity
\[
\Gamma(S)=
N_H[A]\ \cup\
\bigcup_{y\in A}\ \bigcup_{s\in T_y}D(s).           \tag{4}
\]

Since \(A\subseteq N_H[A]\),
\[
|S|=|A|+\sum_{y\in A}(|T_y|-1).                     \tag{5}
\]
Equations (4)--(5) prove the following equivalence.

### Proposition 1: fibre-excess Hall criterion — HUMAN PROOF

The reserve-expanded graph has a matching covering \(\mathcal N_k\) if and
only if, for every \(A\subseteq\mathcal P_k\) and every choice of nonempty
sets \(T_y\subseteq\mathcal F_y\),
\[
\boxed{
\left|
\left(
N_H[A]\cup
\bigcup_{y\in A}\bigcup_{s\in T_y}D(s)
\right)\setminus A
\right|
\ge
\sum_{y\in A}(|T_y|-1).
}
\tag{FE}
\]

Proof.  Every nonempty \(S\) determines \(A,T_y\) as above, and every such
choice determines \(S=\bigcup_yT_y\).  The left side of (FE) counts the
available targets beyond the \(|A|\) fibre centres already present in
\(N_H[A]\).  Combining (4) and (5), (FE) is exactly
\(|\Gamma(S)|\ge|S|\).  Hall's theorem completes the equivalence.
\(\square\)

This is a quotient of Hall by deterministic collision fibres.  It removes
all singleton-fibre demand: only the collision excess
\[
\operatorname{exc}(T)=\sum_y(|T_y|-1)               \tag{6}
\]
must be paid by new exchange/direct targets.

## 5. The minimum pending lemma

The smallest structural statement that closes the present approach is:

> **Fibre-excess expansion lemma (OPEN).**
> For every nonempty \(q=2\) layer and all \(A,T_y\) in Proposition 1, the
> protected forest-exchange boundary together with direct/single targets
> satisfies (FE).

No termination argument or additional inverse construction would then be
needed: Proposition 1 would give the injection immediately.

For extension beyond fixed \(q=2\), the same statement can be made on the
corresponding larger active vertex set.  A useful proof would need a lower
bound of the form
\[
\left|\partial_H A\cup
\left(\bigcup D(T_y)\setminus A\right)\right|
\ge \operatorname{exc}(T),                          \tag{7}
\]
where \(\partial_HA=N_H[A]\setminus A\), that depends on collision
multiplicity rather than the total size of \(A\).

## 6. A proved private-target sufficient condition

The exact criterion (FE) yields a constructive special case.

Choose one representative \(r_y\in\mathcal F_y\) for every nonempty
opening fibre and put
\[
Y=\psi(\mathcal N_k),\qquad
X=\mathcal N_k\setminus\{r_y:y\in Y\}.
\]
Partition the excess sources as \(X=X_D\sqcup X_H\).

### Proposition 2: private-target allocation — HUMAN PROOF

Suppose:

1. there is an injection
   \[
   p:X_D\longrightarrow\mathcal P_k\setminus Y,
   \qquad p(s)\in D(s);
   \]
2. for every \(y\in Y\), there is a set
   \[
   Q_y\subseteq
   N_H[y]\setminus\bigl(Y\cup p(X_D)\bigr)
   \]
   of size \(|X_H\cap\mathcal F_y|\);
3. the sets \(Q_y\) are pairwise disjoint.

Then the reserve-expanded graph has an injection.

Proof.  Send each representative \(r_y\) to \(y\), each source in \(X_D\)
to its private direct target \(p(s)\), and biject
\(X_H\cap\mathcal F_y\) with \(Q_y\).  Every assigned pair is a candidate
edge.  The three target classes are disjoint by construction, and the
\(Q_y\)'s are mutually disjoint. \(\square\)

A reserve-only special case takes \(X_D=\varnothing\).  It is enough to
find disjoint boundary blocks
\[
Q_y\subseteq N_H[y]\setminus Y,\qquad
|Q_y|=|\mathcal F_y|-1.                              \tag{8}
\]
This is stronger than (FE), but it is local and directly verifiable.
It separates two possible proof mechanisms: genuinely private direct
targets and common reserve capacity.

The \(k=5\) fixed-union core shows why the direct-only version is
insufficient: some colliding sources have no distinct direct target outside
their opening centre.  Proposition 2 allows those sources to be assigned
through \(Q_y\).

## 7. Uncrossing a hypothetical obstruction

For \(S\subseteq\mathcal N_k\), define its Hall deficiency
\[
d(S)=|S|-|\Gamma(S)|.
\]
The neighbourhood-size function is submodular, so \(d\) is supermodular:
\[
d(S)+d(T)\le d(S\cup T)+d(S\cap T).                 \tag{9}
\]

### Proposition 3: canonical maximum-deficiency core — HUMAN PROOF

If Hall fails, the family of sets attaining
\[
d_{\max}=\max_Sd(S)>0
\]
is closed under union and intersection.  Consequently it has unique
inclusion-minimal and inclusion-maximal members.  In the minimal member
\(C\),
\[
\Gamma(C)=\Gamma(C\setminus\{s\})
\quad\text{for every }s\in C.                       \tag{10}
\]
In particular, \(C\) contains an opening collision; \(\psi\) cannot be
injective on \(C\).

Proof.  For two maximizers, (9) has left side \(2d_{\max}\), while each term
on the right is at most \(d_{\max}\).  Equality follows, and the
intersection is nonempty because \(d(\varnothing)=0<d_{\max}\).  Finite
repeated union/intersection gives the two canonical members.

For \(s\in C\), let
\[
L=|\Gamma(C)\setminus\Gamma(C\setminus\{s\})|.
\]
Then
\[
d(C\setminus\{s\})=d(C)+L-1.
\]
Inclusion minimality among maximizers forces \(L=0\), proving (10).  If
\(\psi\) were injective on \(C\), its distinct centres would already give
\(|\Gamma(C)|\ge|C|\), contradicting \(d(C)>0\). \(\square\)

This is a genuine reduction: any counterexample to (FE) can be uncrossed to
a collision core in which no source owns even one private target.
However, it does not justify replacing a partial fibre
\(T_y\subsetneq\mathcal F_y\) by the full fibre.  Adding the missing sources
also adds their direct targets, so deficiency is not monotone under fibre
saturation.  The quantifier over arbitrary nonempty \(T_y\) in (FE) cannot
yet be removed.

## 8. Why elementary degree counting is insufficient

At \(q=2,k=7\), the expanded graph has:

\[
38\le\deg_{\rm left}\le60,\qquad
6\le\deg_{\rm right}\le142.
\]
Thus the standard crude sufficient bound
\[
\min\deg_{\rm left}\ge\max\deg_{\rm right}
\]
fails strongly.  Connectivity also does not imply (7): a connected
exchange graph may have a narrow vertex boundary.

The finite matchings show that the combined boundary is large in the
actual deficient regions, but they do not yet yield a symbolic lower bound.

## 9. Alternating-channel formulation

There is a second, equivalent computational view.  Fix a maximum matching
\(M_0\) of the direct/single graph.  Contract each matched source-target
pair into a channel.  A reserve augmenting path alternates through these
channels from an unmatched source to a free target.

The observed completions are:

| layer | base defect | maximum observed path length |
|---:|---:|---:|
| 5 | 6 | 2 |
| 6 | 856 | 2 |
| 7 | 5312 | 3 |
| 8 | 9092 | 6 |

A stronger sufficient lemma would assert a vertex-disjoint packing of
bounded-length reserve channels covering all base defects.  This is more
constructive than (FE), but it depends on choosing \(M_0\) and the observed
length bound is not uniform.  Therefore (FE), not bounded path length, is
the minimal theorem target.

## 10. Current conclusion

The progress is structural but incomplete:

```text
graphic-matroid exchange
        -> legal and reversible reserve edges
        -> exact deterministic-fibre quotient
        -> fibre-excess inequality (FE)
        -> Hall injection
```

The first two arrows and the equivalence of the last two are human proofs.
Propositions 2--3 give a constructive sufficient case and a canonical form
for any obstruction.  The inequality (FE) is still the open middle step.
Finite success for every possible \(q=2\) layer verifies eight explicit
graphs but does not prove (FE) symbolically.
