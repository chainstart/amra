# First mechanism falsification ledger

All finite statements below use the exact Kummer/Legendre predicate.  They are
route-level tests, not a proof or disproof of the public conjecture.

## M377-01 — killed exactly

For `n=11`, `p=3`, the largest power of `p` at most `2n` is `9`.  We have
`11 mod 9=2<9/2`, but `11 mod 3=2>=3/2`.  Thus the top-power test passes while
the lower-power test detects a carry.  One power cannot replace all powers.

## M377-02 — killed in its summable-annulus form

For every `K>=1`, take `n=3^K`.  Its base-3 expansion is a one followed by
zeros, so `3` is carry-free.  The power of 3 nearest `sqrt(n)` has exponent
growing like `K/2`, yet contributes the fixed mass `1/3`.  Therefore no
summable majorant depending only on the annulus/exponent index can bound this
assignment.  A future charge may isolate each small prime globally, but that
is a different mechanism.

## M377-03 — survives and is proved as a partial lemma

See `large_prime_tail_lemma.md`.  Chebyshev plus partial summation bounds all
primes above `sqrt(2n)` by an absolute reciprocal mass.  This leaves the full
small-prime problem.

## M377-04 — killed in its common-contraction form

At the finite record `n=3250`, all of

    3,5,7,13,19,23,47,53

are carry-free and at most `sqrt(n)`.  No `m<=sqrt(3250)` accepts this same
set: necessarily `53<=m<=57`, and exact replay gives respectively

    m=53: 13,23,47,53
    m=54: 13,23,47,53
    m=55: 5,13,23,47,53
    m=56: 5,7,13,23,47,53
    m=57: 5,7,13,19,23,47,53.

Moreover the natural upper blocks `floor(n/p)` depend on `p`.  Hence there is
no injective transfer to one common smaller argument supporting the claimed
`max_{m<=sqrt(n)} f(m)` recurrence.  An averaged multi-child recursion remains
a different, unproved route.

## M377-05 — killed as an every-prefix product bound

For depths `(3^3,5^2,7^2)`, CRT gives exact independence over the full modulus
`33075`: the joint accepted density is the product density.  But among prefixes
of length at least 100, the exact joint count is 1.270395... times the product
prediction at endpoint 113.  Full-period independence does not imply the
claimed pointwise/every-prefix domination.

## M377-06 — killed exactly

At `n=3250`, several primes are fully carry-free even though the product of
the first prime powers exceeding the search bound is more than `10^39` times
that bound for the accepted primes through 47.  Coprime digit moduli can have a
product vastly larger than `n`; CRT does not yield the claimed `O(n)` product
constraint.

This failure is also structurally necessary: the 1975 EGRS two-base theorem
constructs infinitely many common carry-free integers for every two fixed odd
primes.  No pairwise modulus-product obstruction can prove the public bound.

## M377-07 — surviving admission mechanism

A pointwise genuinely many-base Fourier/large-sieve inequality was not refuted.  The
full-period CRT computation shows that it must include cutoff discrepancy and
cannot be an independence or pairwise-incompatibility argument; the EGRS
theorem rules out the latter.  No all-parameter inequality is yet proved.

## M377-08 — killed in its fixed-decay form

Again `n=3^K` keeps the reciprocal mass `1/3` unresolved and accepted through
arbitrarily many base-3 digit levels.  There is no universal fixed fractional
loss at every digit stopping level.  Any valid stopping time must charge a
prime once and then remove it from later levels.

## M377-09 — killed for the proposed natural cylinders

Lower-half cylinders for different bases overlap rather than form a prefix
code; the CRT test above gives exact product overlap over a full common period
and positive prefix discrepancy.  Thus a Kraft inequality does not follow
from the digit cylinders themselves.  A new explicit disjointification would
be a new mechanism.

## M377-10 — killed as a local nonnegative jump certificate

For a contributing prime every Legendre jump equals zero.  Consequently a
nonnegative linear combination of its jumps is also zero and cannot majorize
the indicator of zero total valuation.  Adding a unit constant separately for
each prime restores the trivial `sum_{p<=n}1/p` loss.  A genuinely interacting
cross-prime sieve is represented by M377-07, not by this local ledger.

## M377-11 — killed in its common-contraction form

The first surviving digit blocks at `n=3250` are `floor(3250/p)` and differ for
every accepted prime.  The explicit `m=53,...,57` replay under M377-04 shows
that no common contracted integer preserves even the accepted primes below
`sqrt(n)`.  The claimed single recursive subproblem therefore does not exist.

## M377-12 — killed as a closure mechanism in this round

Its only proved component is M377-03, which removes `p>sqrt(2n)`.  The proposed
middle Fourier component is precisely the still-unproved survivor M377-07,
and the recursive small-prime component M377-11 is false.  The loss ledger
therefore leaves the entire `p<=sqrt(2n)` reciprocal mass unpaid.  Calling the
three labels a hybrid does not supply an interface theorem; a future hybrid
must state a new quantitative middle-to-small bridge.
