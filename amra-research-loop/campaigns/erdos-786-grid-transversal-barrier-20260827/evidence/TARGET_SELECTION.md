# Target selection: from one circuit to a complete grid family

## Frozen target

Let `H_N` be the distinct-Finset bad-relation hypergraph on `{2,...,N}`.
The predecessor campaigns prove that one edge-prime `K_(s+1,s)` incidence
graph gives a support-minimal squarefree bad relation, but one relation costs
only one repair.  This campaign asks whether *all* such grids over shared
prime pools force a quantitatively large transversal even after an arbitrary
global alteration.

For `d>=3`, put `r=d-1`.  Freeze `r` disjoint prime pools of size `m` and
form every `r`-by-`d` grid whose entries in row `i` are distinct primes from
pool `P_i`.  The `r` row products and `d` column products form an
`r`-versus-`d` equal-product relation.  The finite target is

\[
 {d|D_{\rm col}|\over m^{d-1}}+
 {|D_{\rm row}|\over {m\choose d}}\ge 1                         \tag{T.1}
\]

for every transversal `D` of the complete grid family.  In the parameter
range used below this yields `|D|>=m^(d-1)/d`, while deleting all possible
column products gives the matching logarithmic-scale upper comparator
`m^(d-1)`.

Choose the cell primes from `(x/2,x]`, where `x=N^(1/d)`, partition the
available primes into `d-1` equal pools, and optimize
`d=floor(sqrt(log N/log log N))`.  The asymptotic target is

\[
 \log \tau(H_N)\ge \log N-(2+o(1))
       \sqrt{\log N\log\log N}.                                  \tag{T.2}
\]

Every constructed integer must remain at most `N` and above
`(x/2)^(d-1)=N^(1-1/d)/2^(d-1)`.

## What would count

The campaign succeeds only if it proves the complete-family inequality
(T.1), derives (T.2) for every sufficiently large `N`, verifies relation
minimality and integer distinctness, and makes the global-repair consequence
explicit.  This would close a new global lower-bound interface and improve
the known lower-bound exponent scale for the full finite hypergraph.

## What would not count

A single grid, a disjoint packing, a finite computation, or a local query
counterexample does not meet the target.  Neither (T.1) nor (T.2) proves an
`o(N)` transversal upper bound or an infinite density-one set.  No claim
about priority, journal tier, or resolution of Erdos 786 is part of the
frozen contract.
