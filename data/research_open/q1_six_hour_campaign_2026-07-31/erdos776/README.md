# Erdős #776: six-hour rank-six carry attack

Date: 2026-07-31--2026-08-01 (HKT)

This directory attacks the single unresolved gate left by the preceding
breakthrough campaign.  With

\[
L=224\,2^{j-1},\quad 1\le b\le L,\quad c=b+L/2-2,
\quad T=L+b-3,
\]

define the exact low-tail orbit

\[
x_3=\binom c3+\binom{b-1}{2}+2-L,
\qquad x_{p+1}=U_p(x_p)-T\quad(p=3,4,5).
\]

The initial target was the all-strip inequality

\[
\gamma _5:=x_6(b+1)-S_5(x_5(b))\ge0,
\]

equivalently the signed-lift threshold \(\delta _5\ge T+1\).  Dense or
longer scans are used only to discover and falsify candidate lemmas; they
are not evidence for an all-parameter theorem.

It is false.  The first exact failure is

\[
(j,L,b)=(10,114688,57349),\qquad \gamma_5=-46063,
\]

and the infinite family \(b=L/2+5\) has
\(\gamma_5=125969-3L/2<0\) for every \(j\ge10\).  More strongly, no
fixed post-carry rank works uniformly; the necessary and sufficient delay
on this family is asymptotically \(\log_2\log(L/2)\).

The moving-center analysis now has an exact cap atlas.  Every
synchronized cap overflow reduces to a rank-two triangular carry whose
value is affine in the within-row remainder, so each carry-count chamber
has only endpoint minima.  At rank four, all \(5\le k\le h-2\) reduce to

\[
\gamma_4=
U_2(n+4k-6)-U_2(n)-(2k^2-7k+7),
\qquad n=2k^2-8k+9-3h.
\]

The unique asymmetric rank-three cap point is always positive, and the
right endpoints \(k=h-1,h\) are closed explicitly.  If the synchronized
rank-four value is negative, its triangular leading index satisfies
\(q<\lceil(4k-6)/3\rceil\).  The entire double-borrow rank-five chamber
is proved positive by six symbolic endpoint inequalities; the asymmetric
borrow/no-borrow transition is positive as well.  The final no-borrow
state reduces exactly to a rank-three promotion inequality.  A
large-head/small-head dichotomy, nine symbolic promotion rows, and 738
finite \((K,q)\) endpoints prove it positive.  Consequently the full
synchronized rank-four/rank-five bridge is closed.  The distinct pre-cap
adaptive-rank problem remains open, and no statement in this directory
extrapolates the central result to offsets \(k<0\).

The proof and strict scope firewall are in `RANK6_CARRY_ATTACK.md`.
`SYNCHRONIZED_BRIDGE_FREEZE.md` records the closed bridge and its exact
remaining scope.
`rank6_counterexample_certificate.json` freezes the first integer
certificate, and `verify_rank6_carry.py` checks it with two independent
Macaulay implementations, a closed-form canonical certificate, and the
uncompressed global orbit.  None of these results is a counterexample to
Erdős #776 itself.
