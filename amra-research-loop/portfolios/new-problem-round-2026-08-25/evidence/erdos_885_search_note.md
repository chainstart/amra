# Erdős #885 — exact bounded search and resource note

For \(d\ge0\),

\[
d\in D(N)\quad\Longleftrightarrow\quad
\exists y>d:\ y\equiv d\pmod2,\ y^2-d^2=4N.
\]

The forward direction takes \(N=ab\), \(d=|b-a|\), \(y=a+b\); the reverse
direction takes \(a=(y-d)/2\), \(b=(y+d)/2\). Every certificate emitted by the
search is independently replayed through this equivalence.

The script work/search_885_k5.py enumerates every factor pair for every
\(N\le L\). If five such integers share five differences, they share each
four-subset of those differences. The script indexes four-subsets, then looks
for a fifth residual difference occurring for at least five members of the
bucket. Thus a run with no truncated bucket is a complete finite exclusion
through \(L\), not a random search.

The first in-memory implementation at \(L=200,000\) reached approximately
32 GB while constructing the four-subset map. The OpenMath guard contained the
process; it was terminated without a WSL crash. The replacement processes
deterministic hash buckets sequentially. At \(L=50,000\) it examined
33,055,143 exact memberships with no truncation, peaked at 288,047,104 bytes,
and proved that no five integers \(N_i\le50,000\) have five common factor
differences. A second complete run used 64 buckets, checked 105,720,376 exact
memberships, and extended the exclusion to \(N_i\le100,000\), again without
truncation.

The April 2026 forum example gives the five differences

\[
330,870,2445,4155,10482
\]

and three common integers. For two fixed differences \(d_0<d_1\), every
common \(N\) arises from

\[
(y_1-y_0)(y_1+y_0)=d_1^2-d_0^2,
\]

so all possibilities are obtained by finitely many factor pairs. The exact
script work/extend_885_fixed_differences.py checked all 50 admissible
factorisations of \(870^2-330^2=648000\). Exactly three integers survive all
five differences:

\[
189000,\quad3992800,\quad11282544.
\]

Thus that particular five-difference construction is provably saturated at
three common integers and cannot be extended to the required five.

The bounded \(N\)-search is finite evidence only, while saturation of the fixed
five-difference set is an exact theorem about that set. Neither refutes the
\(k=5\) case nor replaces the elliptic-curve mechanism in Bremner's \(k=4\)
construction.
