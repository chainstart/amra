# Representation search: five views of the grid atlas

## Incidence algebra

The coloured row-pool representation makes prime factorization a literal
incidence matrix.  It separates three obligations: product equality follows
because every cell prime occurs once on each shore; distinctness follows
from pool signatures and injectivity within rows; minimality follows from
connectivity of `K_(d-1,d)`.  The uncoloured and repeated-label variants are
retained as collision tests, not assumed equivalents.

## Probabilistic transversal

The complete atlas is too large to enumerate symbolically, but a uniformly
random injected grid has simple exact marginals.  This representation asks
only whether a deletion set can cover all grids.  A first-moment union bound
is sufficient; columns are explicitly dependent because row samples are
without replacement.  Deleting the complete column universe supplies the
upper comparator `m^(d-1)`.

## Asymptotic optimization

The exact lower bound is the minimum of a column scale and a row-binomial
scale.  The column scale produces loss `log N/d+d log log N`; the row scale
must be checked rather than silently discarded.  Fixed `d`, growing `d`,
and the false all-parameter binomial shortcut are separate representations.

## Prime geometry

The cell labels come from `(x/2,x]`, `x=N^(1/d)`.  This simultaneously
controls height, creates a lower tail threshold, and avoids all smaller
queried primes.  The prime number theorem supplies the population.  Bertrand
alone is a comparator because it does not count enough primes in the same
fixed interval.

## Alteration interface

A valuation-query classifier with a retain-labelled zero branch keeps every
integer made from the grid primes.  Unlike the predecessor path theorem, the
second stage must hit the complete atlas.  The resulting repair threshold is
large but still `o(N)`; the explicit budget comparison prevents an invalid
claim about all sublinear alterations or the original problem.
