# Blind reconstruction: distinct-factor log-defect transversal

## Protocol

This reconstruction was written before opening any author file under
`evidence/` or any author verifier.  I read only `campaign_state.json`, the
frozen statement and variant lock in `closure_contract.json`, and the
statement/dependency list in `decisive_lemma.json`.  The reconstruction treats
all products as Finset products: no integer may occur twice on one shore.

## 1. Reduction to disjoint positive supports

Let finite sets `S,T` of natural numbers have equal products and unequal
cardinalities.  If `S` and `T` overlap and all entries are positive, cancel
`S intersect T`.  With

\[
S'=S\setminus T,\qquad T'=T\setminus S,
\]

the new shores are disjoint,

\[
\prod S'=\prod T',\qquad |S'|-|T'|=|S|-|T|\ne0. \tag{1}
\]

Thus it is sufficient to forbid disjoint bad relations.  Each surviving
integer occurs exactly once in their support `S' union T'`; there is no
multiplicity hidden in the hyperedge.

The integer `1` must be absent, since `{1}` and the empty Finset have equal
product and different cardinality.  If the convention for the naturals
includes `0`, then `0` must also be absent: `{0}` and `{0,2}` already violate
the property, and cancellation by division is unavailable at zero.  Deleting
`0,1` has no effect on either density assertion.  On the vertex set
`{2,...,N}`, an unequal relation cannot have an empty shore, because a
nonempty product of integers at least two is greater than one.

## 2. The fractional vertex-cover inequality

Fix `N>=2`.  Let a hyperedge be the union of disjoint shores `S,T` contained
in `{2,...,N}` with equal product `P` and unequal sizes.  Interchange the
shores so that

\[
k=|S|>|T|=l.
\]

Define

\[
w_N(n)=\frac{\log(N/n)}{\log N}.
\]

These weights are nonnegative, including `w_N(N)=0`.  Because every member
of the smaller shore is at most `N`,

\[
P=\prod_{t\in T}t\le N^l.                              \tag{2}
\]

Both shore products equal `P`, and the support is disjoint, so every support
vertex is counted once and

\[
\begin{aligned}
\sum_{n\in S\cup T}w_N(n)
 &=\frac{(k+l)\log N-\log\prod S-\log\prod T}{\log N}\\
 &=\frac{(k+l)\log N-2\log P}{\log N}\\
 &\ge k-l\ge1.                                        \tag{3}
\end{aligned}
\]

Thus `w_N` is a fractional vertex cover of every bad-support edge, with no
bound on the length, prime support, or exponent sizes of the relation.

## 3. Exact total mass and Stirling asymptotic

Summing over the actual vertex set, not over the deleted vertex `1`, gives

\[
\begin{aligned}
\sum_{n=2}^N w_N(n)
 &=\frac{(N-1)\log N-\sum_{n=2}^N\log n}{\log N}\\
 &=\frac{N\log N-\log(N!)}{\log N}-1.                 \tag{4}
\end{aligned}
\]

Stirling's formula yields

\[
\log(N!)=N\log N-N+\tfrac12\log(2\pi N)+O(1/N),
\]

and hence

\[
\sum_{n=2}^Nw_N(n)
=\frac N{\log N}-\frac{\log(2\pi N)}{2\log N}-1
 +O\!\left(\frac1{N\log N}\right)
=(1+o(1))\frac N{\log N}.                             \tag{5}
\]

In particular the fractional optimum is at most this `o(N)` value.  This is
an upper bound on the optimum; equality with the optimum is neither claimed
nor needed.

## 4. Exact bounded-length high-tail theorem

Let `L=L(N)>=1` be an integer with `L=o(log N)` and retain only

\[
A_{N,L}=\{n\le N:n>N^{1-1/L}\}.
\]

The deletion count is at most `N^(1-1/L)`, whose ratio to `N` is

\[
N^{-1/L}=\exp(-\log N/L)=o(1).                         \tag{6}
\]

Suppose a bad disjoint relation in `A_(N,L)` has larger shore size `k<=L`
and smaller size `l<=k-1`.  The retained lower endpoint is strict, so

\[
\prod S>N^{k(1-1/L)}\ge N^{k-1}\ge N^l\ge\prod T,
\]

a contradiction.  Therefore deleting the low tail removes every bad
relation whose larger shore has at most `L` elements.  It does not address
relations whose length grows faster than the selected `L`.

## 5. Minimal squarefree relations of every odd support size

Fix `s>=1`.  Give every edge of the connected bipartite graph
`K_(s+1,s)` its own distinct prime.  For each graph vertex `x`, let `a_x` be
the product of the primes on edges incident to `x`.  Every `a_x` is
squarefree, and different graph vertices have different incident-prime sets.
The product over the `s+1` vertices on the left and the product over the `s`
vertices on the right both equal the product of all edge primes.  This is an
`(s+1)`-versus-`s` bad relation on `2s+1` distinct integers.

It is support-minimal.  In any signed multiplicative subrelation supported on
these integers, let `c_x in {-1,0,1}` be the coefficient of vertex `x`.
For an edge prime `p_(xy)`, equality of its exponents says

\[
c_x+c_y=0.                                             \tag{7}
\]

Connectivity forces all coefficients on the left to be one common value and
all coefficients on the right to its negative.  The only possibilities are
the zero relation and the full displayed relation (up to reversing shores).
Thus no proper subset of its support is bad.  Its total size `2s+1` is also
the smallest possible for prescribed shore sizes `s+1` and `s`, tautologically.
The construction works already at `s=1`; a statement beginning at `s=2` is
valid but not sharp in range.

## 6. Fixed-`N` hypergraph and ILP completeness

For fixed `N` there are finitely many disjoint pairs of Finsets in
`{2,...,N}`.  Form the finite hypergraph `H_N` of their bad supports.  A set
`A subseteq {2,...,N}` has the product-cardinality property exactly when it
contains no edge of `H_N`, i.e. when it is independent.  Equivalently its
deleted complement is a transversal.

It is enough to keep inclusion-minimal bad supports: every bad edge contains
an inclusion-minimal bad edge because the family of bad subsets below it is
finite and nonempty.  Therefore the binary ILP

\[
\min\sum_{n=2}^Nx_n,
\qquad \sum_{n\in E}x_n\ge1\quad(E\text{ minimal bad}),
\qquad x_n\in\{0,1\},                                 \tag{8}
\]

computes the exact deletion optimum at that fixed `N`.  Exhaustion or ILP
through any bounded `N` remains finite evidence; it supplies no uniform
integrality-gap theorem.

## 7. Scope and unresolved density statements

Equations (3)--(5) prove an all-`N` fractional theorem.  They do not produce
an integral transversal of size `o(N)`.  Since the fractional mass is of
order `N/log N`, an integrality loss of general order `log N` gives only
`O(N)`, not the required `o(N)` deletion.  A structured loss `o(log N)` (or a
different integral mechanism) is still required for the finite assertion.

Even a finite integral construction `A_N` for every cutoff would not by
itself give one infinite set of natural density greater than `1-epsilon`:
the finite optima need not be nested, and product relations may cross block
or cylinder boundaries.  A coherent stabilization/profinite/periodic
construction with an actual natural-density limit remains separate.

Accordingly the finite density-one assertion and the infinite natural-density
assertion are both unresolved by the reconstructed theorem.  The public
finite/infinite Erdős #786 problem is not solved.  Subject to replay of the
author evidence, the all-circuit fractional cover is nevertheless an exact
standalone global interface and is a plausible
`standalone_decisive_lemma`; promotion would have to state this scope and
must not be labeled `original_problem_closed` or finite-density closure.
