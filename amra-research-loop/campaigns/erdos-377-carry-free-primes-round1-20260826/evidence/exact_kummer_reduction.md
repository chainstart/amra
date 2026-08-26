# Exact Kummer/Legendre reduction for Erdős 377

For every prime `p`, Legendre's formula gives

    v_p(binomial(2n,n))
      = sum_{j>=1} (floor(2n/p^j) - 2 floor(n/p^j)).

Each summand is either zero or one, and it equals one precisely when

    fractional_part(n/p^j) >= 1/2,

equivalently when `n mod p^j >= p^j/2`.  Consequently

    p does not divide binomial(2n,n)

if and only if

    n mod p^j < p^j/2 for every j>=1.

Only powers `p^j<=2n` need checking.  The same condition is Kummer's statement
that adding `n+n` in base `p` has no carry.  If

    n = sum_j d_j p^j,

it is equivalent to `2 d_j < p` for every digit.  In particular `p=2` never
contributes for positive `n`.

This is an exact all-parameter equivalence, not a probabilistic model.  The
campaign objective is therefore

    f(n) = sum_{p<=n, all base-p digits of n <= (p-1)/2} 1/p.

## First scale boundary

If `p^2>2n`, only the `j=1` Legendre term can be nonzero.  Writing
`q=floor(n/p)`, the carry-free condition is

    n-q p < p/2,

or

    n/(q+1/2) < p <= n/q.

This explicit interval model is exact for the large-prime range.  Summing over
all primes above `sqrt(2n)` is already O(1) by Mertens; the missing theorem is
a summable mechanism through every lower prime-power scale.
