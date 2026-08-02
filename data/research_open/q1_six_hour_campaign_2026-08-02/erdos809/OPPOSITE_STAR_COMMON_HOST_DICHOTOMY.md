# Erdős #809 — opposite-star common-host intersection theorem

Date: 2026-08-02

Status: `PROVED__PENDING_INDEPENDENT_CROSS_AUDIT`

## 1. Setup

Let `G` be a finite simple graph on `n` vertices.  Fix a vertex `b` and
distinct leaves `L={c_1,...,c_l}`.  Put

\[
P=N(b),\qquad C=V(G)\setminus P,\qquad Q_c=N(c).
\tag{1}
\]

Assume that every `bc`, `c in L`, is an opposite-neighbourhood zero-shore
pair.  Explicitly,

\[
P\cap Q_c=\varnothing,
\qquad E(P,Q_c)=\varnothing.
\tag{2}
\]

Define the union host and common exceptional set

\[
U=\bigcup_{c\in L}Q_c,
\qquad R=C\setminus U,
\qquad r=|R|,
\qquad T=L\setminus U,\quad t=|T|.
\tag{3}
\]

For each leaf write

\[
\rho_c=|C\setminus Q_c|=n-d(b)-d(c).
\tag{4}
\]

## 2. Exact theorem

### Theorem 2.1 (intersection versus synchronization)

Under (1)--(4):

1. `U` is anticomplete to `P`, and every `P`--`C` edge ends in `R`:
   \[
   E(P,U)=\varnothing,
   \qquad e(P,C)=e(P,R)\le |P|r.
   \tag{5}
   \]
2. If
   \[
   \Psi_e(p)=\binom p2+\binom{n-p}{2}-e(G),
   \qquad p=|P|,
   \tag{6}
   \]
   then
   \[
   \boxed{
   M(P)+M(C)=\Psi_e(p)+e(P,C)
   \le\Psi_e(p)+pr.
   }
   \tag{7}
   \]
3. For every leaf,
   \[
   \boxed{|U\setminus Q_c|=\rho_c-r.}
   \tag{8}
   \]
   In particular, if `delta=delta(G)` and `kappa=n-2delta`, then
   \[
   \boxed{t+1\le r\le\kappa},
   \qquad |U\setminus Q_c|\le\kappa-r.
   \tag{9}
   \]
4. Every two leaf neighbourhoods obey
   \[
   \boxed{
   |Q_c\mathbin\triangle Q_d|
   \le(\rho_c-r)+(\rho_d-r)
   \le2(\kappa-r).
   }
   \tag{10}
   \]
5. Their common intersection satisfies
   \[
   \left|\bigcap_{c\in L}Q_c\right|
   \ge |U|-\sum_{c\in L}(\rho_c-r)
   \ge |U|-\ell(\kappa-r).
   \tag{11}
   \]

#### Proof

Equation (2) holds for every `c`, so taking the union gives
`E(P,U)=empty`.  Since `C=U disjoint-union R`, every edge from `P` to `C`
therefore ends in `R`, proving (5).

Partitioning the edges of `G` across `P,C` gives

\[
e(G)=\binom p2-M(P)+\binom{n-p}{2}-M(C)+e(P,C).
\]

Rearrangement and (5) prove (7).

Now `Q_c` is a subset of `U`, while `|Q_c|=d(c)` and
`|U|=|C|-r=n-p-r`.  Therefore

\[
|U\setminus Q_c|
=n-p-r-d(c)
=\rho_c-r,
\]

which proves (8).  Minimum degree gives `p>=delta`, `d(c)>=delta`, hence
`rho_c<=n-2delta=kappa`.  Also `U` contains every `Q_c`, so
`|U|>=delta`, and consequently

\[
r=|C|-|U|\le n-\delta-\delta=\kappa.
\]

Every active zero-shore pair \(bc\) is missing.  Hence \(L\subseteq C\),
the centre \(b\) belongs to \(C\), and \(b\notin N(c)\) for every leaf.
Therefore

\[
 \{b\}\mathbin{\dot\cup}(L\setminus U)
 \subseteq C\setminus U=R,
\]

so \(r\ge t+1\).  This proves (9).  Since both `Q_c,Q_d` lie inside `U`, their symmetric
difference is contained in the union of their two deficits from `U`.
This gives (10).  Finally, the complement in `U` of the common
intersection is the union of the deficits `U\\Q_c`; the union bound and
(9) prove (11).  \(\square\)

## 3. Two endpoint consequences

The theorem replaces the previous per-leaf residual by the smaller common
residual `r=|intersection_c(C\\Q_c)|`.

### Corollary 3.1 (small common residual)

In the fixed-`s` maximum-degree normalization of the inherited campaign,
write `alpha=p/n` and let `zeta` be the maximum-degree overshoot.  Then the
larger of `P,C` obeys

\[
M(\mathrm{larger}(P,C))
\le
\left(2s\zeta+\zeta^2+\alpha\frac rn+o(1)\right)n^2.
\tag{12}
\]

Thus `zeta=o(1)` and `r=o(n)` yield an aligned
`(1/2+s-o(1))n`-vertex block with `o(n^2)` missing edges.  This is the
inherited dense-core exit with `r`, rather than any selected `rho_c`.

### Corollary 3.2 (large common residual)

If `kappa-r=o(n)`, then every leaf has

\[
|N(c)\mathbin\triangle U|=o(n),
\]

and every two leaf neighbourhoods differ in `o(n)` vertices.  If in
addition `ell(kappa-r)=o(n)`, the leaves share a common neighbourhood of
size `|U|-o(n)`.

This is an exact synchronization conclusion even when every individual
residual `rho_c` is linear.

## 4. Scope firewall

The theorem does not yet exclude the intermediate regime in which both
`r` and `kappa-r` are linear.  Nor does neighbourhood synchronization by
itself construct the final pairwise `C_7`-compatible edge family.  The
outer-`A` residual is untouched.  Erdős #809 remains open.

The basepoint strengthening \(r\ge t+1\) was independently checked
during Red Team I against the inherited definition of an active
zero-shore missing pair.  The rest of the theorem retains its prior
audit status.
