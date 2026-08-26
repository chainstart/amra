# Audit: extending the L=2 Fejer majorant to all 451 primes

Date: 2026-08-27

Verdict: **PASS when `d=1` is absent; CONDITIONAL on an extra exact-carry or
discrete reconstruction when it is present.**  No dyadic block merge
remains, but common-time integrality forbids enlarging the widths merely by
using open B-spline support.  The weighted small-lift inequality itself is
open.

## Parity-safe full widths

Use the exact coordinate `s=n-(k+1)`.  For `p_i=k+d_i`, the 451 condition is

\[
                         s\bmod p_i\in\{0,1,\ldots,d_i-1\}. \tag{1}
\]

Put

\[
             \theta_i={d_i-1\over2},\qquad b_i={d_i\over2}. \tag{2}
\]

The located interval for the common real diagonal parameter then has
half-integer endpoints.  Any nonempty intersection of such open intervals
has half-integer endpoints a positive integral distance apart, and hence
contains an integer.  For that integer, the coordinate residue lies in
`0,...,d_i-1`.  This is the common-time reconstruction used in M05 Lemma
2.2.

The tempting enlargement `b_i=(d_i+1)/2` is invalid despite the B-spline
density vanishing at each individual endpoint.  Its located intervals have
integer endpoints and can have a nonempty common intersection `(N,N+1)`
with no integer.  Explicitly, for two coordinates choose by CRT an integer
`N` with `N=0 (mod p_i)` and `N=-d_j (mod p_j)`.  The corresponding located
intervals `I_i=(p_i a_i-d_i,p_i a_i+1)` and
`I_j=(p_j a_j-d_j,p_j a_j+1)` can be placed so that their intersection is
exactly `(N,N+1)`.  A continuous summand is positive there, but it produces
no integer common time.  Thus positivity coordinate by coordinate does not
repair the reconstruction.  The varying centers `theta_i/p_i` are harmless
only with the half-integer endpoint choice (2).

## Exact full-system majorant

Let the index set contain every prime `k<p_i<2k`, let `m` be its size, and
put

\[
 P=\prod_i p_i,qquad D=\prod_i d_i,qquad
 c_i\equiv(P/p_i)^{-1}\pmod {p_i}.                          \tag{3}
\]

For an integer word `a=(a_i)` with `|a_i|<b_i`, let `H(a)` be the centered
CRT lift characterized by `H(a)=a_i (mod p_i)`.  Equivalently,

\[
 {H(a)\over P}\equiv\sum_i{a_ic_i\over p_i}\pmod1.         \tag{4}
\]

The same carry-majorization and L=2 Poisson calculation as in the round-3
proof note, now coordinate by coordinate, gives

\[
 S={P\over h\prod_i b_i}
 \sum_{\substack{a_i\in\mathbb Z, |a_i|<b_i\\
                  |H(a)|_P<h}}
 \left(1-{|H(a)|_P\over h}\right)
 \prod_i\left(1-{|a_i|\over b_i}\right).                  \tag{5}
\]

This is valid for integer `1<=h<P/2`.  If

\[
                              S<2,                           \tag{6}
\]

then the full inhomogeneous box spline covers every torus translate.  In
particular, center the diagonal interval at `s=k+h`; the resulting allowed
integer has

\[
                     k\le s\le k+2h,qquad
                     2k<n=s+k+1\le2k+2h+1.                 \tag{7}
\]

Thus (5)--(6) for the full prime set directly proves the desired successor
bound.  There is no residual block-shift, common-endpoint orientation, or
merge loss: full-torus covering is stronger than the one distinguished
start needed in (7).

The local coefficient mass is uniformly controlled.  From

\[
 \beta_i(a)={1\over b_i}\left(1-{|a|\over b_i}\right)_+,
\]

one computes exactly

\[
 Z_i:=\sum_{a\in\mathbb Z}\beta_i(a)=
 \begin{cases}
  1,&d_i\text{ even }(b_i\text{ integral}),\\
  1+d_i^{-2},&d_i\text{ odd }(b_i\text{ half-integral}).
 \end{cases}                                                \tag{7a}
\]

If `d_i=1` occurs, its factor is two and removes the automatic strict mean
margin for the carry-forgetting majorant.  In fact the normalized local
characteristic functions and the time Fejer kernel are nonnegative, so the
spectral identity in the companion theory note gives `S>=product_i Z_i`.
Consequently `d_i=1` forces `S>=2`: the strict bridge (6) is impossible for
every `k` with `k+1` prime.  One may impose its exact
condition `s=0 (mod k+1)` and write `s=(k+1)y`, at only polynomial cost in
the final interval length.  But the remaining residue sets are then
multiplicative dilates in `y`, and positivity for a common **real** diagonal
parameter does not by itself produce an integer `y`.  Therefore this
absorption requires a new discrete/dilate-aware reconstruction; it is not
proved by the present continuous all-translate box spline.

After removing that possible coordinate, the remaining odd offsets are
distinct and at least three, so

\[
 \prod_iZ_i
 <\exp\left(\sum_{\substack{n\ge3\\n\text{ odd}}}{1\over n^2}\right)
 =\exp(\pi^2/8-1)<1.264.                                   \tag{7b}
\]

Hence local periodization does not consume the strict margin below two when
`d_i=1` is absent.  When it is present, retaining its exact carry or proving
the discrete dilated bridge is an additional exceptional-prime interface;
widening the continuous segment is not a valid repair.

## Exponent ledger

Take

\[
        h=\left\lceil k^B C^m{P\over D}\right\rceil.        \tag{8}
\]

Since `product_i b_i=D/2^m`, the zero global-frequency contribution to (5)
is

\[
                    {P\over h\prod_i b_i}\le
                    k^{-B}(2/C)^m.                          \tag{9}
\]

It therefore has a fixed margin below one for any fixed `C>2` and large
`k`.  Moreover

\[
 \log(P/D)=\sum_{k<p<2k}\log{p\over p-k}=o(k).              \tag{10}
\]

For completeness, split offsets at `k/(log k)^2`.  The smaller offsets are
at most `k/(log k)^2` integers and contribute `O(k/log k)`; for the larger
offsets each logarithm is `O(log log k)`, while the standard bound
`pi(2k)=O(k/log k)` makes their total `O(k log log k/log k)=o(k)`.
Together with `m=O(k/log k)`, (8) gives `log h=o(k)`.
The standard Chebyshev/PNT estimate also gives `log P=Theta(k)`, so the
required alias condition `h<P/2` holds for all sufficiently large `k`.

Consequently, proving (6) at (8), with any fixed `B` and sufficiently large
fixed `C>2`, would yield

\[
                          n_k\le2k+2h+1=\exp(o(k)),          \tag{11}
\]

and hence the requested `n_k<exp(epsilon k)` for every fixed positive
`epsilon` and all sufficiently large `k`.

If `d_i=1` is absent, the only unresolved step is the genuinely joint
weighted small-lift estimate (5)--(6) for all primes at once.  If it is
present, the same implication remains true if (6) can be proved directly,
but the local mass-two alias removes the automatic margin; exact handling
of that coordinate leaves the additional discrete/dilate-aware
reconstruction described after (7a).  In either case the statement is a
sufficient strengthening, not a reformulation known to follow from the
original distinguished-start problem, and no claim that it holds is made.
