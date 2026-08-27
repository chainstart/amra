# Literature boundary for the surviving mechanism

The primary source is P. Erdős, R. L. Graham, I. Z. Ruzsa and E. G. Straus,
*On the Prime Factors of the Central Binomial Coefficient*, Mathematics of
Computation 29 (1975), 83–92:

<https://renyi.hu/~p_erdos/1975-27.pdf>

Its Theorem 1 proves that if digit cutoffs `A,B` obey

    A/(p-1) + B/(q-1) > 1,

then infinitely many integers have all base-`p` digits below `A` and all
base-`q` digits below `B`.  Taking the lower-half digit alphabets for two odd
primes satisfies this inequality.  Hence any two fixed odd primes can both
fail to divide `binomial(2n,n)` for infinitely many `n`.

The same paper proves first and second mean results for the reciprocal sum and
states that it cannot decide whether the function is unbounded.  Thus neither
average concentration nor pairwise digit incompatibility is a plausible new
closure mechanism.

A 2010 arXiv preprint by Robert J. Betts, arXiv:1010.3070, claims an extension
to any three fixed odd primes.  This campaign records it as an unaudited claim,
not as an accepted dependency.  If correct, it pushes the necessary rigidity
boundary from two to at least four/growing prime bases; either way, the public
problem needs a quantitative theorem for a growing weighted family.
