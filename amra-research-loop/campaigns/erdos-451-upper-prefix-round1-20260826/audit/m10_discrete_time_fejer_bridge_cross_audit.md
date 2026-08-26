# Cross-audit: exact discrete-time Fejer bridge

Date: 2026-08-27

Audited read-only:
`work/m10_round1/discrete_time_fejer_bridge_round3.md`.

Verdict: **PASS.**  The bridge is an exact integer-time sufficient lemma;
its joint spectral inequality (10) remains open.  This audit is independent
of the derivation in that note but belongs to the same model family.

## Reconstruction

For `r_i+s_i=d_i+1`, the cyclic convolution of the two uniform
probabilities on `0,...,r_i-1` and `0,...,s_i-1` has no wraparound and is
positive exactly on `0,...,d_i-1`.  In particular `d_i=1` gives a point
mass, with total mass and zero Fourier coefficient exactly one.

With the unnormalized local transform, inversion contributes `1/p_i` per
coordinate.  Multiplication of the local characters gives the global
frequency

\[
                     A(a)=\sum_i a_iP/p_i\pmod P,
\]

and this map is bijective by CRT.  Summing the integer triangular window
then gives exactly

\[
 N(c)={1\over P}\sum_a W_h(A(a)/P)e_P(A(a)c)\prod_iT_i(a_i).
\]

The zero word is `h/P`.  Since `W_h>=0`, the strict absolute inequality
`sum_(a ne 0) W_h product_i|T_i|<h` leaves `N(c)>0` for every integer
center.  No continuous common-time variable or endpoint rounding enters.
Taking `c=k+h` therefore yields an allowed integer `s` with
`k<s<k+2h` and the claimed `2k<n<2k+2h+1`.

The normalization and quantifiers pass.  The lemma is deliberately
stronger than needed because it removes the center phase by absolute value;
the note does not claim that this estimate has been proved.

## Expanded-width counterexample

The proposed continuous repair `b_i=(d_i+1)/2` is invalid.  Its positive
located intervals have integer endpoints and can be written, up to the
common translation convention, as

\[
                         I_i=(p_i a_i-d_i,p_i a_i+1).
\]

For two distinct coordinates, CRT supplies an integer `N` with
`N=0 (mod p_i)` and `N=-d_j (mod p_j)`.  Choose integers `a_i,a_j` with
`p_i a_i=N` and `p_j a_j=N+d_j`.  Then

\[
 I_i\cap I_j=(N,N+1),
\]

which is nonempty and supports a positive continuous summand but contains
no integer common time.  Thus endpoint vanishing coordinate by coordinate
does not prove the required integer intersection.  The reconstruction-safe
continuous width remains `d_i/2`; the discrete bridge avoids the issue
altogether.

No correction to the discrete lemma is required.

## Width-one fibre elimination

Verdict on Section 5: **PASS.**  Write `p=p_0` and `h=pH`.  Splitting
`0<=u<pH` uniquely as `u=v+pw` proves

\[
 D_{pH}(x)=D_p(x)D_H(px).
\]

For fixed real `alpha`, the numbers
`D_p(alpha+a/p)` are the length-`p` discrete Fourier transform of the
unit-modulus vector `(e(alpha v))_(0<=v<p)`.  Parseval therefore gives

\[
 \sum_{a\bmod p}|D_p(\alpha+a/p)|^2=p^2,
\]

and hence

\[
 \sum_{a\bmod p}W_{pH}(\alpha+a/p)=pW_H(p\alpha).
\]

If all remaining local frequencies vanish, `alpha=0`; all summands with
`a ne 0` vanish because `D_p(a/p)=0`, while the `a=0` summand is
`W_(pH)(0)=pH=h`.  Thus deleting the global zero word really deletes the
entire zero remaining fibre.  For every nonzero remaining word, CRT gives
`A' ne 0 (mod P')`, and the fibre identity reduces the left side of (10)
to `p` times the left side of (17).  The right side is `pH`, so division by
`p` is exact.  Since `(p,P')=1`, the resulting multiplication by `p` is an
invertible joint dilation.  No frequency is discarded, and the only
physical-window cost is the polynomial factor `p=O(k)`.

## Arc-dispersion closure audit

Verdict on Section 6: **PASS.**  The current author note incorporates the
required dilation-quantifier clarification.  The local
estimate is exactly

\[
 \sum_{a\bmod p}|T(a)|
 \le \left({p\over r}{p\over s}\right)^{1/2}
 ={p\over\sqrt{rs}}\le {2p\over d},
\]

because the balanced choice with `r+s=d+1` has
`sqrt(rs)>=d/2`.  CRT then factors the global `L1` mass and proves
`L<=2^mP/D`.

Suppose (21) holds at every centered scale `P/h<=X<=P/2`.  On the first
arc `|A|_P<=P/h`, the normalized Fejer weight is at most one.  On the
`j`-th doubling shell it is `O(4^(-j))`, while (21) bounds the cumulative
mass by `O(K^m 2^jL/h)`.  The resulting geometric series is

\[
 {1\over h}\sum_{A\ne0}W_h(A/P)w(A)
       \ll {K^mL\over h}.
\]

At `h=k^B C^mP/D`, this is
`k^(-B) O(2K/C)^m`; one fixed sufficiently large `C` closes (10), and
`log h=o(k)`.  Excluding `A=0` in the definition of `M(X)` is essential,
because that atom is the separately removed principal term.

The clarification is that centered-arc dispersion is **not automatically
invariant under arbitrary unit dilation**.  There is an exact obstruction,
not merely a logical warning.  Let `A_0` be the global frequency whose
local word is `a_i=1` for every `i`.  It is a unit modulo `P`, and the
elementary sine bound used in the norm ledger gives

\[
                         w(A_0)\ge(4/\pi^2)^m.
\]

The unit `gamma=A_0^(-1)` maps it to residue one.  At `X=P/h`, (21) would
bound this atom by
`K^mL/h<=k^(-B)(2K/C)^m`.  Once the closing constant is chosen with
`C>(pi^2/2)K`, this is strictly smaller than `w(A_0)` for large `k`.
Thus the version uniform over every unit is false.  The sufficient theorem only needs two
explicit cases: the undilated system, and, when `d=1` occurs, the one
specific dilation `gamma=p_0 (mod P')` produced by (17).  Dispersion for
that second measure is an additional hypothesis, not a formal consequence
of the first.
