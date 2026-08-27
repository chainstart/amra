# Exact finite-scan audit

The first guarded command

    /home/biostar/work/projects/openmath/bin/openmath-memory-guard -- \
      work/exact_carry_scan 250000000 evidence/exact_carry_scan_250m.json

completed without a safety event and initially reported

    max_{1<=n<=250000000} f(n) = f(3250)
      = 1.17924290579448...

within floating summation precision.  The accepted-prime list at 3250 was
reconstructed independently with exact Legendre valuations; its reciprocal
sum agrees with the scan value to `2e-11`.  The verifier also replayed the
Legendre, digit and one-level interval predicates for every `n<5000`.

## Why the scan covers every n in the finite range

For an odd prime `p`, put `h=(p-1)/2`.  Every integer `n>=p` has a unique
decomposition

    n=xp+d,  x>=1,  0<=d<p.

Its base-`p` digits are all at most `h` exactly when `x` is itself carry-free
and `0<=d<=h`.  Thus, for each recursively generated carry-free prefix `x`,
the complete set of accepted `n` with that prefix is the integer interval

    [xp, xp+h].

The scanner adds `1/p` to these intervals by a difference array.  The intervals
are disjoint for fixed `p`, every accepted `n>=p` occurs in one, and `p=2`
accepts no positive `n`.  After processing every sieved prime up to the cutoff,
one prefix sum therefore equals the exact `f(n)` at every finite `n` (apart from
ordinary floating addition error, which cannot affect the reported gap without
being many orders of magnitude larger than machine error).

## Extended scan and corrected finite record

The same exact algorithm was then run through `2,000,000,000` under the same
aggregate memory guard.  It found one later record:

    n = 1,293,081,501,
    f(n) = 1.18050255777032...  (difference-array accumulation).

This is larger than `f(3250)` by about `0.00125965`, so the natural conjecture
that 3250 is the absolute maximiser is false.  A separate direct implementation
sieved all primes through the new `n` and evaluated the Legendre valuation for
each prime, without using carry-free prefix intervals.  It found 39,480,473
accepted primes and Kahan sum `1.18050255776492`, agreeing within `5.5e-12`.
See `record_1293081501_independent_replay.json`.

The full accepted-prime list would occupy 387 MB.  The committed evidence keeps
its count, a SHA-256 digest of the canonical JSON list, the mass split by digit
depth, and the independent replay checksum instead of storing that redundant
list.

The result is a finite theorem only.  It gives no information for
`n>2000000000` and is not used as proof of a universal maximum or of boundedness.
