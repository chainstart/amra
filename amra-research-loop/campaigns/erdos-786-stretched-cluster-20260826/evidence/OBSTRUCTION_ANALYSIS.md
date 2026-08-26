# Obstruction analysis

The predecessor construction contains more quantitative room than its
recorded choice \(K<q<2K\) uses.  For a projective plane of order \(q\), a
point needs only

\[
 r=\lceil\log_2(q+2)\rceil+1
\]

private primes to provide distinct nontrivial bipartitions to its \(q+1\)
incident lines.  There are \(q^2+q+1\) points.  Choosing all point-private
primes below \(q^6\) is possible for large \(q\), since the prime number
theorem gives

\[
 \pi(q^6)\gg q^6/\log q\gg(q^2+q+1)r.
\]

The odd part belonging to one point is then at most \(q^{6r}\), so its
base-two logarithm is at most \(6r\log_2q=O((\log q)^2)\).  A private path
vertex uses factors from at most two point blocks and has twice this bit
cost.  Thus the actual constraint is

\[
  (\log q)^2=o(K),
\]

not \(q=O(K)\).  Taking a prime

\[
  2^{\lfloor\sqrt K/100\rfloor}<q<
  2^{\lfloor\sqrt K/100\rfloor+1}
\]

by Bertrand's postulate leaves a wide padding margin and changes the
projective-plane blocking number from logarithmic in \(N=2^K\) to
stretched exponential in \(\log N\).

Three checks are not automatic.  First, the point-private prime supply must
grow with \(q\); the old cutoff \(K^6\) cannot be retained.  Second, the
line-specific factor pairs must remain disjoint nontrivial subsets of a
fixed point block, because that is what gives a private valuation on every
path edge and hence support minimality.  Third, the result must be transferred
from powers of two to all large \(N\), with the band widened from a factor
32 to a factor 64.
