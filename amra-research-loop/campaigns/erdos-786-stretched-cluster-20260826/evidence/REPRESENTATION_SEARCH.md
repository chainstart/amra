# Representation search

Ten representations were compared across valuation coding, incidence
geometry, analytic resource accounting, integer padding, and scale transfer.
The decisive combination is not a larger finite-plane computation.  It is the
joint representation

\[
 \text{projective plane}
 +\text{entropy-coded point partitions}
 +\text{prime/bit ledger}
 +\text{integer padding flow}
 +\text{dyadic transfer}.
\]

The point-partition representation stores \(q+1\) incidences with
\(O(\log q)\) private primes.  The analytic ledger then shows that selecting
all globally private primes below \(q^6\) costs only
\(O((\log q)^2)\) bits in any one integer.  The projective plane supplies the
exact blocking number, the padding flow makes the arithmetic identities live
in a fixed top band, and the dyadic representation supplies every large
integer cutoff.

Exponent codes, affine planes, smooth composite labels, multi-prime padding,
and unions of disjoint clusters remain useful adversarial comparators.  Each
has a first test that can refute a claimed improvement without weakening the
frozen target.
