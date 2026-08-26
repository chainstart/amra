# Exact r=2 prime-predecessor hypergraph reduction

For an integer `m`, its representations `m=pa` with `p` prime and `a in A`
are in bijection with the distinct prime divisors `p|m` for which `m/p` lies
in `A`.  Thus the `r=2` condition is

    |A intersect {m/p : p is a prime divisor of m}| <= 2

for every positive integer `m`.

Every forbidden triple therefore has the exact form

    {m/p, m/q, m/s}

for distinct prime divisors `p,q,s` of `m`.  Writing `g=m/(pqs)` gives

    {g q s, g p s, g p q}.

Conversely every triple `g{pq,pr,qr}` with distinct primes `p,q,r` is the
three-predecessor triple of `m=gpqr`.  Hence admissible sets for `r=2` are
exactly the independent sets in the 3-uniform hypergraph

    H_N = { g{pq,pr,qr} : p,q,r distinct primes, g>=1,
            max(gpq,gpr,gqr)<=N }.

The public objective is its maximum vertex weight for `w(n)=1/n`.

This equivalence retains common-gcd scaling and prime powers in `g`; the
squarefree finite-prime cube is only the induced subhypergraph with `g=1`.

## Exact inherited double count

For primes `p<=N`,

    (sum_{a in A} 1/a)(sum_{p<=N} 1/p)
      = sum_{p<=N,a in A} 1/(pa)
      <= r sum_{m<=N^2} 1/m.

The inequality is correct because each `m` has at most `r` representations.
Its loss is also exact: it replaces the actual predecessor identity and the
overlap of the hyperedges by the cap `r` separately at every `m`.

## Admission target

The first computational phase searches the exact finite `H_N` and its
finite-prime exponent-lattice restrictions for counterexamples to candidate
weighted local inequalities.  Survival is not a proof; any retained inequality
must subsequently be shown stable under arbitrary `g`, exponents, and `N`.
