# OPG-1757 midpoint report

Date: 2026-08-01

## Unconditional result already closed

The former uniform-height gap is closed:

\[
\lVert C_{q,r}\rVert_1
\le7200(q+2)^6\,2^{2q+2}(2q+6)^{2q+2}
\le(32q)^{12q}.
\]

This includes all zero-, one-, and two-marked endpoints, all four
master shifts, the restricted lambda binomial, overlap factorial,
endpoint products, the exact cancellation of \(n!\), and the absence of
an \(s\)-dependent denominator.

It gives the explicit threshold
\[
s>E_q q!/4
\]
and proves, with explicit quantifiers, simultaneous supportwise
positivity for every fixed
\[
0<c<1/3,\qquad q\le c\frac{\log s}{\log\log s}.
\]

The number \(3\) in the logarithmic threshold is audited as
\[
\frac{\log E_q}{q\log q}\to2,\qquad
\frac{\log(q!)}{q\log q}\to1.
\]

## Highest-value candidate under audit

A loss-by-loss argument appears to bypass the raw height barrier and
prove
\[
s\ge2(4096q)^{67}
\quad\Longrightarrow\quad
C_{q,r}(s)>0\quad(0\le r\le2q),
\]
hence the power window
\[
q\le s^{1/67}/8192.
\]

The argument uses the all-\(k\) endpoint degree bound, triangular Newton
interpolation, an exact absolute-profile EGF, and a geometric root
majorant.  It is recorded in
POLYNOMIAL_GROWING_DEFICIT_WINDOW.md and deliberately remains
**PENDING INDEPENDENT CROSS-AUDIT**.

The diagonal quantifier has also been checked explicitly: every
inherited identity is exact for all \(q\) on the common stable range
\(s\ge6q+4\), and the candidate threshold absorbs that range.  No
\(O_q(\cdot)\) estimate is reused with \(q=q(s)\).

## Red-team status

- Exact \(q=0\) normalization: \(C_{0,0}=4\).
- Both beta boundaries \(r=0,2q\): included.
- Exact profile EGF: 99/99 coefficient identities through \(q=9\).
- Newton triangular reconstruction: 1,001/1,001.
- Constant chain: 7,440/7,440.
- Four-shift falling factors: 881,548/881,548.
- Frozen \(q=6\) endpoint losses: 1,008/1,008.
- Frozen \(q=6\) final-layer losses: 156/156.
- New unit tests: 9/9; new plus inherited focused tests: 25/25.

No finite check is used to supply an all-parameter quantifier.

## 01:30 bold-attack freeze

The higher-risk base-four Newton route did not yield a general sign
proof and remains explicitly conjectural.  It did yield one exact
all-deficit corollary: the inherited boundary factor forces every Newton
order below \(\lfloor q/2\rfloor\) to vanish, and the first active order
is strictly positive for every \(q,r\).  At that order the pooled depth
is exactly \(2\) for odd \(q\) and \(3\) for even \(q\), so the result
follows from the already proved exact \(B_2\) and \(B_3\) formulas.  For
odd \(q=2m+1\), its whole beta-offset generating polynomial is

\[
2(m+4+2z)^{2m+2}(1+z)^{2m}>_{\rm coeff}0.
\]

The full conjecture has 364 positive and 91 forced-zero exact Newton
coefficients through \(q=6\), with no negative value.  However,
profilewise, transposed-pair, and fixed-overlap approaches are all
refuted as sign-preserving routes.  At the smallest obstruction
\((q,r)=(1,2)\), the \(\ell=0\) row is \((-32,-36)\) and becomes positive
only after adding the \(\ell=1\) row \((40,64,16)\).  The exact global
profile EGF and this barrier are isolated in
`BASE4_NEWTON_GLOBAL_ATTACK.md`; no finite evidence is promoted to a
theorem.

## Remaining work

1. independent reconstruction of the all-\(k\) normalized endpoint
   interface;
2. independent derivation of the absolute profile EGF and
   \(S_{q,r}/L_{q,r}\le10q\);
3. independent audit of the apparent-loss shift \(K=k+2\) and the
   constants \(67,8192\);
4. status upgrade or precise downgrade before the 05:15 freeze.
