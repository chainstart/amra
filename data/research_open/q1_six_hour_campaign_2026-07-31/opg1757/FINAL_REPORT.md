# OPG-1757 six-hour campaign report

Date: 2026-08-01

Status at draft time: **primary theorem proved; power-window candidate
awaiting independent cross-audit**

## Primary theorem

The conditional gap left by the preceding campaign is closed.  Uniformly
for every \(q\ge1\) and \(0\le r\le2q\),

\[
\lVert C_{q,r}\rVert_1
\le
7200(q+2)^6\,2^{2q+2}(2q+6)^{2q+2}
\le(32q)^{12q}.
\]

Together with the exact leading symbol
\[
[s^{2q}]C_{q,r}
=\frac4{q!}[z^r](1+2z+2z^2)^q\ge4/q!,
\]
this gives positivity for \(s>E_q q!/4\).  In particular, for every
fixed \(0<c<1/3\), there is an effective \(s_0(c)\) such that all
natural-support coefficients are positive simultaneously when
\[
s\ge s_0(c),\qquad
q\le c\frac{\log s}{\log\log s}.
\]

The proof is not a longer fixed-deficit computation.  It is an
all-profile atom majorant followed by the exact normalized master
formula.  The factorial and shift ledger was independently rederived
from the ordered-chain and pooled-overlap identities.

## Bold continuation

The all-order endpoint filtration led to a much stronger candidate:
\[
s\ge2(4096q)^{67}
\quad\Longrightarrow\quad
C_{q,r}(s)>0\quad(0\le r\le2q),
\]
and hence
\[
q\le s^{1/67}/8192.
\]

The mechanism is loss-by-loss rather than raw-height:

1. the \(k\)-th relative endpoint coefficient is a polynomial of
   parameter degree at most \(2k\);
2. triangular Newton interpolation plus the endpoint height bounds its
   actual profile value by \(q^{2k}\) times a \(k\)-dependent constant;
3. the absolute profile mass collapses exactly to
   \(8[z^r](1+2z+2z^2)^{q+1}/(q+1)!\);
4. its ratio to the positive leading symbol is at most \(10q\);
5. the remaining tail is dominated by a finite geometric series.

This candidate is intentionally not promoted in this draft report until
an independent proof audit has checked the all-order normalization,
Newton interface, profile EGF, loss shift, and constants.

## Verification

- uniform endpoint atoms: 694;
- normalized master profiles: 80,806;
- exact \(q=0\) values: 37;
- exact profile-mass coefficients: 99, each via two coordinate systems;
- Newton reconstructions: 1,001;
- constant-chain values: 7,440;
- changing-shift falling coefficients: 881,548;
- exact frozen \(q=6\) endpoint losses: 1,008;
- exact frozen \(q=6\) final-layer losses: 156;
- new tests: 9/9;
- new and inherited focused tests: 25/25.

## Scope

Neither result settles arbitrary-host OPG-1757.  Both concern only the
complete-split pooled disjoint-core \(\alpha^2\) layer.  The power
exponent \(1/67\), if the cross-audit passes, is not claimed optimal.
