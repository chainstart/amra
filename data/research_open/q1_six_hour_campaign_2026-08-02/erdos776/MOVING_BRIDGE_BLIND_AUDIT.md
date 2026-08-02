# Independent blind audit of the inherited moving-\(k\) bridge

Source frozen: 2026-08-01 01:56 HKT
Audit opened: 2026-08-02 HKT

## Scope

The audited statement is the synchronized rank-four/rank-five implication

\[
 \gamma_4<0\quad\Longrightarrow\quad\gamma_5>0
\]

on the relaxed integral lattice

\[
\begin{gathered}
k\ge5,\qquad n\ge0,\qquad
n\equiv2k^2-8k+9\pmod3,\\
h=(2k^2-8k+9-n)/3\ge224,\qquad k\le h-2.
\end{gathered}
\]

This audit does not infer anything about the separate pre-cap branch or
about \(k<0\).

## Independent reconstruction

Put

\[
H=2k^2-7k+7,\quad m=4k-6,\quad
z=U_2(n),\quad \Delta=U_2(n+m)-z,\quad S=n+z.
\]

Then \(\gamma_4=\Delta-H\), \(\tau=H-n\), and the two algebraic
rank-five low blocks are

\[
x_0=S-H+1,\qquad y_0=S+\gamma_4=x_0+(\Delta-1).
\]

At a negative point, the one-third chunk bound gives
\(q<\lceil m/3\rceil\), and in particular \(\Delta-1>0\).  Hence the
reachable sign states are exactly

1. \(x_0<y_0<0\) (double borrow);
2. \(x_0<0\le y_0\) (asymmetric transition);
3. \(0\le x_0<y_0\) (no borrow).

The missing orientation \(y_0<0\le x_0\) is algebraically impossible.
Equality belongs to the non-borrowing side, matching the manuscript's strict
and weak inequalities.

## Checks still being completed

- independent reproduction of the 36 promotion endpoints and 738 bounded
  ((K,q)) endpoints with a separately coded Macaulay expansion;
- a boundary matrix at the first synchronized value \(k=21\), at
  \(n=0\), \(k=h-2\), and every equality convention;
- line-by-line verification of the two real-root estimates in the no-borrow
  tail and the finite-row cutoff in the asymmetric state;
- comparison of the exact verifier domain with the prose lattice.

## Provisional verdict

No counterexample or omitted borrow state has been found.  The verdict remains
**PENDING** until the independent endpoint and boundary checks are frozen.
