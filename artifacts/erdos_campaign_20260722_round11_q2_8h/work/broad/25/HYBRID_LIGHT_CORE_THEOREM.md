# Erdős #25: a hybrid light-tail / low-clique-core theorem

Date: 2026-07-22 (Asia/Hong_Kong)

Status: rigorous sufficient condition for **natural density**.  It does not
settle Erdős #25 in full.

## 1. Set-up

Let

\[
 n_1<n_2<\cdots,
 \qquad R_i=\{m\geq 1:m\equiv a_i\pmod {n_i}\},
 \qquad C_i=R_i\cap[n_i,\infty),
\]

and put

\[
 A=\mathbb N\setminus\bigcup_i C_i.
\]

For a finite index set `J`, let

\[
 d(J)=d\!\left(\mathbb N\setminus\bigcup_{i\in J}R_i\right).
\]

This density exists because the set is periodic.  Write

\[
 d_*:=\lim_{h\to\infty}d(\{1,\ldots,h\});
\]

the limit exists by monotonicity.

Before forming the graph below, delete from `J` every class `R_j` contained
in another class `R_i` in `J`.  This does not change either the full union or
the activated union: if `R_j subset R_i`, then necessarily `n_i<=n_j`, so
`C_j subset C_i`.  On the remaining indices form the compatibility graph
`G(J)`: two vertices are adjacent precisely when their congruences are CRT
compatible.  Let `kappa(J)` be the number of cliques of `G(J)`, including the
empty clique.

## 2. The theorem

For `x>=1`, put `I_x={i:n_i<=x}`.  Suppose that for every sufficiently large
`x` one can choose `J_x subset I_x` and an integer `h(x)` such that

\[
 \{1,\ldots,h(x)\}\subseteq J_x,\qquad h(x)\longrightarrow\infty,
                                                               \tag{1}
\]

and

\[
 \frac{\kappa(J_x)}x\longrightarrow0,
 \qquad
 \sum_{i\in I_x\setminus J_x}\frac1{n_i}\longrightarrow0.    \tag{2}
\]

Then `A` has natural density, and

\[
 \boxed{d(A)=d_*.}                                           \tag{3}
\]

The sets `J_x` need not be nested.  Thus a different structured core may be
chosen at every observation scale.

## 3. Proof

Let

\[
 A_{J_x}^{\rm act}=
 \mathbb N\setminus\bigcup_{i\in J_x}C_i.
\]

Every omitted active class has at most `x/n_i` members in `[1,x]`.  Indeed,
its first allowed representative is at least `n_i` and subsequent
representatives are spaced by `n_i`.  Consequently

\[
 0\leq |A_{J_x}^{\rm act}\cap[1,x]|-|A\cap[1,x]|
 \leq x\sum_{i\in I_x\setminus J_x}\frac1{n_i}.              \tag{4}
\]

There are no indices outside `I_x` active below `x`.

Apply inclusion--exclusion to the active slices belonging to `J_x`.  A
nonempty intersection occurs exactly for a clique of `G(J_x)`: pairwise CRT
compatibility is equivalent to joint compatibility for congruences.  For a
compatible clique `Q`, put

\[
 L_Q=\mathop{\rm lcm}_{i\in Q}n_i,
 \qquad M_Q=\max_{i\in Q}n_i.
\]

Its active intersection in `[1,x]` is one residue class modulo `L_Q`, cut
off below `M_Q`.  Since `M_Q<=L_Q`, its cardinality differs from `x/L_Q` by
less than `2`.  The empty clique contributes the ambient interval and obeys
the same harmless bound.  Hence

\[
 \left|
 \frac{|A_{J_x}^{\rm act}\cap[1,x]|}{x}-d(J_x)
 \right|
 \leq \frac{2\kappa(J_x)}x.                                \tag{5}
\]

Finally, (1) and `J_x subset I_x` give the squeeze

\[
 d_*\leq d(J_x)\leq d(\{1,\ldots,h(x)\}),                  \tag{6}
\]

so `d(J_x)->d_*`.  Combining (4)--(6) with (2) proves (3).

## 4. Concrete corollaries

1. **Light tails.**  If `sum_i 1/n_i<infinity`, choose `J_x` to contain a
   sufficiently slowly growing initial segment.  For each fixed segment its
   clique count is fixed, while the omitted reciprocal tail tends to zero.
   This recovers the known summable case.
2. **Low clique complexity.**  If the globally reduced compatibility graph
   on all of `I_x` has `kappa(I_x)=o(x)`, take `J_x=I_x`.  This recovers the
   compatibility-clique theorem.
3. **Mixed systems.**  The theorem also covers systems in which neither the
   whole reciprocal sum converges nor the full compatibility graph has
   `o(x)` cliques: a divergent but highly incompatible part can be retained
   in the core, while a compatible sparse fringe can be paid for by its
   reciprocal mass.
4. If the reduced graph induced by `J_x` has `R_x` vertices and degeneracy
   `Delta_x`, then

   \[
   \kappa(J_x)\leq 1+R_x2^{\Delta_x}.
   \]

   Thus `R_x2^{Delta_x}=o(x)` is an easily checked replacement for the first
   condition in (2).

## 5. Logarithmically averaged hybrid form

There is a formally weaker averaged version aimed directly at the official
question.  No claim is made here that an explicit congruence system strictly
separating the two hypotheses has been constructed.
Keep (1), but replace (2) by

\[
 \frac1{\log X}\sum_{2\leq x\leq X}\frac{e_x}{x}
 \longrightarrow0,                                      \tag{7}
\]

where

\[
 e_x=\min\!\left\{1,
       \sum_{i\in I_x\setminus J_x}\frac1{n_i}
       +\frac{2\kappa(J_x)}x\right\}.                    \tag{8}
\]

Then `A` has logarithmic density `d_*`.

Indeed, (4)--(5) give

\[
 \left|\frac{|A\cap[1,x]|}{x}-d(J_x)\right|\leq e_x.     \tag{9}
\]

By (6), `d(J_x)->d_*`.  Discrete Abel summation says

\[
 \sum_{m\leq X}\frac{1_A(m)}m
 =\frac{|A\cap[1,X]|}{X}
  +\sum_{x<X}\frac{|A\cap[1,x]|}{x(x+1)}.                \tag{10}
\]

After division by `log X`, the endpoint vanishes, the logarithmic Cesàro
mean of `d(J_x)` tends to `d_*`, and (7) kills the error in (9).  Notice that
(7) permits arbitrarily bad individual cutoffs provided that they have zero
logarithmic mass.  Taking `J_x=I_x` recovers the pure logarithmically averaged
clique-entropy theorem; taking pointwise (2) recovers the natural-density
statement above.

## 6. Exact evidence boundary

This result is a flexible sufficient criterion, not a proof that suitable
cores `J_x` exist for every sequence of moduli and residues.  In particular,
no universal optimization argument balancing clique count against reciprocal
tail mass has been proved.  Therefore the original logarithmic-density
problem remains open.
