# Survivor deepening: a near-linear grid-transversal barrier

Throughout, `H_N` is the hypergraph on `{2,...,N}` whose edges are supports
of disjoint finite sets with equal products and unequal cardinalities.  All
logarithms are natural.

## Theorem G.1 (finite complete-grid transversal theorem)

Let `d>=3`, put `r=d-1`, and let `P_1,...,P_r` be pairwise disjoint sets of
`m>=d` primes.  For each row `i`, choose an ordered injection

\[
 (p_{i,1},\ldots,p_{i,d})\in(P_i)_d.
\]

Associate the row and column integers

\[
 R_i=\prod_{j=1}^d p_{i,j},\qquad
 C_j=\prod_{i=1}^{r}p_{i,j}.                         \tag{G.1}
\]

Let `G_(d,m)` be the hypergraph consisting of the supports
`{R_1,...,R_r,C_1,...,C_d}` over all such grids.  Then:

1. every support is a support-minimal squarefree `r`-versus-`d`
   equal-product relation on `2d-1` distinct integers;
2. if a transversal `D` contains `a` possible row products and `c`
   possible column products, then

   \[
   {a\over {m\choose d}}+{dc\over m^r}\ge1;          \tag{G.2}
   \]

   in particular

   \[
   \tau(G_{d,m})\ge
   \min\left\{{m^r\over d},{m\choose d}\right\};    \tag{G.3}
   \]

3. for every `0<delta<1` satisfying

   \[
   \delta m\ge2dr,qquad
   m>2^d d!\,\delta^{-d},                             \tag{G.4}
   \]

   one has the stronger bounds

   \[
   (1-\delta)m^r\le\tau(G_{d,m})\le m^r.             \tag{G.5}
   \]

### Proof of algebra and minimality

Every cell prime in (G.1) occurs once among the rows and once among the
columns, so the two shore products agree.  The shore sizes `r=d-1` and `d`
differ.

Rows from distinct pools have different prime signatures.  Two columns are
different because the row injections use different primes in their two
positions.  A row product has `d` primes from one pool, while a column has
one prime from each of `r>=2` pools, so row and column values cannot agree.

For support minimality, give every displayed integer an arbitrary signed
coefficient in `{-1,0,1}` and suppose their signed product is one.  Write
`u_i` for the coefficient of `R_i` and `v_j` for that of `C_j`.  The
valuation at the private prime `p_(i,j)` gives

\[
 u_i+v_j=0                                           \tag{G.6}
\]

for every edge of `K_(r,d)`.  Connectivity forces all `u_i` to one common
value and every `v_j` to its negative.  The common value is zero, one, or
minus one.  Hence the only signed relations are the empty relation and the
two orientations of the full support.

### Proof of the exact marginal bound

Choose each row independently and uniformly from its ordered injections.
For a fixed column `j`, the tuple `(p_(1,j),...,p_(r,j))` is uniform on
`P_1 times ... times P_r`.  Therefore its product is uniform on the
`m^r` possible column products.  The unordered prime set in row `i` is
uniform among the `binom(m,d)` subsets of `P_i`.

The row-product universes for different `i` and the column-product universe
are pairwise disjoint.  If `D` hits every grid, a random grid meets `D` with
probability one.  Applying the union bound to its `d` columns and `r` rows
gives

\[
 1\le {dc\over m^r}+
 \sum_{i=1}^r {|D\cap V_{\rm row,i}|\over {m\choose d}}
 ={dc\over m^r}+{a\over {m\choose d}},
\]

which is (G.2).  Bounding the sum `a+c` by the reciprocal of the larger
coefficient gives (G.3).  No independence between different columns is
used.

### Proof of the dense-atlas strengthening

Deleting every possible column product gives the upper bound in (G.5).
For the lower bound, suppose for contradiction that a transversal `D` has
fewer than `(1-delta)m^r` vertices.  Regard a column product as its unique
tuple in

\[
 U=P_1\mathbin{\times}\cdots\mathbin{\times}P_r,
 \qquad |U|=m^r,
\]

and let `E` be the tuples whose products are not in `D`.  Since the number
of deleted column products is at most `|D|`,

\[
 |E|>\delta m^r.                                     \tag{G.7}
\]

An ordered `d`-matching in `E` is a sequence of `d` tuples that are
coordinatewise distinct.  After `k<d` tuples have been selected, at most
`krm^(r-1)` tuples share a used coordinate.  The first condition in (G.4)
and (G.7) therefore give at least

\[
 \prod_{k=0}^{d-1}(|E|-krm^{r-1})
 \ge (\delta m^r/2)^d                                \tag{G.8}
\]

ordered `d`-matchings in `E`.

A fixed deleted row product in pool `P_i` specifies one unordered
`d`-subset of that pool.  There are at most

\[
 d!(m)_d^{r-1}\le d!m^{d(r-1)}                       \tag{G.9}
\]

ordered coordinatewise matchings having exactly that row set.  There are
fewer than `m^r` deleted row products because `|D|<m^r`.  Thus the total
number of matchings blocked by a deleted row product is less than

\[
 d!m^{r+d(r-1)}=d!m^{rd-1},                          \tag{G.10}
\]

where the final equality uses `r=d-1`.  By the second condition in (G.4),

\[
 d!m^{rd-1}<(\delta m^r/2)^d.                        \tag{G.11}
\]

Some ordered matching from (G.8) is therefore blocked by neither a column
nor a row deletion.  Its `d` tuples are the columns of an injected grid, so
the corresponding edge of `G_(d,m)` avoids `D`, a contradiction.  This
proves (G.5).

## Theorem G.2 (optimized arithmetic embedding)

For every sufficiently large integer `N`, the hypergraph `H_N` contains a
squarefree subhypergraph `G_N` such that

\[
 \log\tau(G_N)=
 \log N-(2+o(1))\sqrt{\log N\log\log N}.             \tag{G.12}
\]

Consequently

\[
 \tau(H_N)\ge
 N\exp\left(-(2+o(1))
       \sqrt{\log N\log\log N}\right).              \tag{G.13}
\]

Every vertex of `G_N` lies in the explicit interval

\[
 \left({N^{1-1/d}\over2^{d-1}},N\right],
 \qquad
 d=\left\lfloor\sqrt{\log N\over\log\log N}\right\rfloor,
                                                               \tag{G.14}
\]

and hence in

\[
 \left(N\exp(-(1+o(1))
       \sqrt{\log N\log\log N}),N\right].            \tag{G.15}
\]

### Proof

Put `L=log N`, `ell=log L`, take the displayed `d` (which is at least three
for large `N`), and set `x=N^(1/d)`.  The prime number theorem gives

\[
 Q:=\pi(x)-\pi(x/2)=(1+o(1)){x\over2\log x}.         \tag{G.16}
\]

Here `x=exp(L/d)` tends to infinity.  Partition these `Q` primes into
`r=d-1` pools of equal size

\[
 m=\left\lfloor{Q\over d-1}\right\rfloor
  =(1+o(1)){x\over2L},                               \tag{G.17}
\]

using `d log x=L` and `(d-1)/d=1+o(1)`.  Since `x/L` tends to infinity, the
integer floor is negligible.

Every row product has `d` primes at most `x`, and every column has `d-1`,
so all values are at most `x^d=N`.  As every cell prime exceeds `x/2`, the
smallest possible column product is greater than `(x/2)^(d-1)`; row
products are larger still for `x>2`.  This proves (G.14).

Choose `delta=L^(-1/4)`.  From (G.17),

\[
 \log m=(1+o(1))\sqrt{L\ell},\qquad
 \log(d!)=(1/2+o(1))\sqrt{L\ell},\qquad
 d\log(1/\delta)=(1/4+o(1))\sqrt{L\ell}.             \tag{G.18}
\]

The logarithm of `2^d d! delta^(-d)` is therefore
`(3/4+o(1))sqrt(L ell)`, strictly below `log m`; also
`delta m/(2d(d-1))` tends to infinity.  Both conditions in (G.4) hold.
Theorem G.1 yields

\[
 \tau(G_N)=(1+o(1))m^{d-1}.                          \tag{G.19}
\]

Finally, (G.17) gives

\[
\begin{aligned}
 \log\tau(G_N)
 &=(d-1)\left({L\over d}-\log(2L)+o(1)\right)+o(1)\\
 &=L-{L\over d}-(d-1)\log(2L)+o(d)\\
 &=L-(2+o(1))\sqrt{L\ell},
\end{aligned}
\]

which proves (G.12)--(G.13).  The logarithm of the lower endpoint in
(G.14) is `L-L/d-(d-1)log 2`, giving (G.15).

## Corollary G.3 (arbitrary alteration and randomized outputs)

Let

\[
 T_{d,m,\delta}=(1-\delta)m^{d-1}
\]

under (G.4).  Every deletion set whose complement is admissible for `H_N`
has at least `T_(d,m,delta)` elements.  In particular:

1. if any first-stage classifier retains every vertex of `G_(d,m)`, every
   arbitrary second-stage repair producing a transversal has size at least
   `T_(d,m,delta)`;
2. if the cell primes lie above `x/2`, the preceding statement applies to a
   retain-labelled all-zero transcript of any uniform valuation-query tree
   querying only primes below `x/2` on that branch;
3. for any random deletion set `D`, with no independence or algorithmic
   restriction,

   \[
   \Pr(D\text{ is a transversal of }H_N)
   \le {\mathbb E|D|\over T_{d,m,\delta}}.            \tag{G.20}
   \]

Indeed, the first two assertions are direct restrictions to `G_(d,m)`.  For
the third, the indicator of successful transversality is pointwise at most
`|D|/T_(d,m,delta)`.

## Scope and interpretation

Theorem G.2 changes the verified global lower-bound exponent scale in the
present campaign record: it replaces a single repairable circuit and the
earlier stretched-exponential cluster by an explicit squarefree subhypergraph
with transversal number `N^(1-o(1))`.
It also closes the previously open global-alteration interface for the
frozen local-query obstruction.

It does **not** solve Erdos 786.  The lower bound in (G.13) is still `o(N)`;
for example `N/log N` is asymptotically much larger.  The missing result is
an `o(N)` *upper* bound for `tau(H_N)`, followed by an independent coherence
argument for the infinite density statement.  No priority or journal-tier
claim follows without independent reconstruction and literature review.
