# Erdős #776 — first-stage freeze

Freeze time: 2026-08-01 01:30 HKT

## Closed

- The inherited universal rank-six gate is false.  The first exact
  failure is \((j,L,b)=(10,114688,57349)\), and \(b=L/2+5\) is an
  infinite counterfamily.
- No fixed post-carry rank can replace rank six.  On the counterfamily,
  the exact first seed has order \(\log_2\log(L/2)\).
- Among fixed central offsets \(b=h+k\), \(k=5\) is the unique slow wall:
  \(k=1,2,3\) seed at rank four, \(k=4\) at rank five, and the paired
  constants strictly improve for every fixed \(k\ge6\).
- Every moving synchronized cap is reduced exactly to a rank-two
  triangular carry.  On a fixed carry-count chamber the target is affine
  in the triangular remainder, so only endpoints remain.
- For \(5\le k\le h-2\), the complete rank-four cap atlas is controlled
  by \(f(k)=2k^2-8k+9\) and \(g(k)=f(k+1)\).  The single asymmetric
  rank-three cap integer is always positive.  The endpoints \(k=h-1\)
  and \(k=h\) seed at ranks four and five respectively.
- In the synchronized chart, \(h\) is eliminated.  If
  \(n=f(k)-3h\), then
  \[
  \gamma_4=U_2(n+4k-6)-U_2(n)-(2k^2-7k+7).
  \]
  A negative point has triangular leading index
  \(q<\lceil(4k-6)/3\rceil\).
- If this synchronized \(\gamma_4\) is negative and both next low blocks
  borrow, then \(\gamma_5>0\).  The proof checks all six symbolic
  deficit-row endpoint pairs \(1\le j\le i\le3\).

## Still open

The remaining moving-central bridge is

\[
\gamma_4<0\Longrightarrow\gamma_5\ge0
\]

in only two cap states:

1. \(S_2(n)-H+1<0\le S_2(n)+\gamma_4\) (asymmetric transition);
2. \(0\le S_2(n)-H+1<S_2(n)+\gamma_4\) (synchronized no borrow),

where \(H=2k^2-7k+7\).

Offsets \(k<0\) have not been included in this moving-center theorem.
Therefore neither a uniform seed over the whole strip nor Erdős #776 is
claimed.

## Verification

At freeze, the focused regression suite reported “4 passed in 12.33s”.
The exact scans are discovery and regression guards only; all universal
claims above have symbolic proofs in RANK6_CARRY_ATTACK.md.
