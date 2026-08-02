# Root independent cross-audit — Erdős #776 transfer lane

Audit window: 2026-08-02 21:25--21:50 HKT  
Verdict: **PASS AFTER ONE ASSOCIATION REPAIR**  
Public problem: **OPEN / NEITHER PROVED NOR REFUTED**

The audit did not import or call the author's verifier.  The independent
program `root_independent_audit.py` uses a direct linear Macaulay
decomposition and rebuilds all decisive finite quantities.

## 1. Exact algebra and domains

Subtracting the two triangular coordinates gives

\[
b=cq+\binom c2+u-r+1.
\]

The identity `x+tau=z+1` is literal cancellation.  Expanding the rank-three
canonical words independently gives (2.2), and complementing either low
block gives (2.7) and (3.6) with the stated signs.  No reversal was found.

For the multi-cap lemma, telescope

\[
\Lambda_{j,A+g}(E)-\Lambda_{j,A}(E)\le gE
\]

and subtract it from the same-cap inequality
\(\Lambda_{j,A}(D)-\Lambda_{j,A}(E)\ge U_j(D-E)\).
The domain is legal because
\(E\le D\le\binom Aj\le\binom{A+i}j\).  The independent guard checked
252,730 small-domain tuples without a failure.

## 2. Census and shallow phase

The independent engine reproduced exactly:

```text
retained states                 85,278
promotion counts               2:36,288; 3:33,620; 4:14,921; 5:449
nonpositive gamma4             0
minimum gamma4                 69 at (16,2,0,3,37,256)
second-level bound positive    85,276
residual exact/lower values    (354,-3), (489,-51)
```

It also independently found the 20 admissible `q<90` rows of Theorem 5.1,
all positive, with minimum 186 at `(q,u,b,h)=(39,13,55,327)`.
Formula (5.8) follows by writing

\[
\binom{q-1}{2}-\delta
=\binom{q-2}{2}+(q-2-\delta),
\]

so the displayed loss and its direction are correct.  The large-`q`
comparison is strict at `q=90`; the finite and analytic pieces have no
integer gap.

## 3. Fixed-promotion compactness audit

For fixed `c`, the ranges of `r,u` give `a=q+O_c(1)` and
`t=q+O_c(1)`.  A bad sequence therefore has a subsequence on which the
integer gap `g=t-a` is fixed and the normalized tails converge.  The exact
displacement gives

\[
g+S-P=c+U^2-R^2\ge c-1.
\]

The independently reconstructed scaling

\[
N_q/q^2\to\theta/2
\quad\Longrightarrow\quad
U_2(N_q)/q^3\to\theta^{3/2}/6
\]

then yields the normalized numerator
`g-1+S^(3/2)-P^(3/2)`.  With
`f(x)=x-x^(3/2)` and `0<=f<=4/27`, it is at least
`c-2-4/27 >= 23/27` for every fixed `c>=3`.  The proof has the correct
quantifiers

\[
\forall c\ge3\;\exists Q_c\;\forall q\ge Q_c;
\]

it is not uniform when `c=c(q)` grows.

For `c=2`, the same phase check shows every subsequential limit is
nonnegative.  If it is zero, then
`2+U^2-R^2=1`, hence `(R,U)=(1,0)`.  Proposition 5.3 therefore passes.

## 4. Independent audit and sharpening of the boundary handoff

Put `k=q-r>=1`.  On the localized boundary `k=o(q), u=o(q)`, direct
substitution eventually gives

\[
a=q,\quad t=q+1,
\]

and the exact same-cap deficits

\[
D=\frac{(u+2k+1)(2q+u+2)}2,
\]

\[
E=\frac{2q(u+k)+k^2+2ku+5k+4u+4}{2},
\]

\[
F=D-E=\frac{-k^2+2kq-k+2q+u^2-u-2}{2}.
\]

Thus

\[
\gamma_4=\Lambda_{2,q}(D)-\Lambda_{2,q}(E)
-\binom{q-k}{2}-1
\ge U_2(F)-\binom{q-k}{2}-1.
\]

The independent guard reconstructed this identity on 10,033 boundary rows.
If `gamma4<=0`, the elementary lower growth
`U_2(F) >> F^(3/2)` gives

\[
k=O(q^{1/3}),\qquad u=O(q^{2/3}).
\]

For fixed `(k,u)`, the exact loss asymptotic

\[
\Lambda_{2,q}(dq+O(1))/q^2\to d/2
\]

gives `gamma4/q^2 -> k/2>0`; hence a bad sequence also needs
`k+u -> infinity`.

There is one further quantitative consequence.  Along a convergent
normalized subsequence put

\[
K=\lim k/q^{1/3},\qquad U=\lim u/q^{2/3}.
\]

Then

\[
F/q^{4/3}\to K+U^2/2,
\qquad
U_2(F)/q^2\to\frac{(2K+U^2)^{3/2}}6.
\]

The bad-sequence upper bound tends to `1/2`, so every limit point obeys

\[
\boxed{2K+U^2\le3^{2/3}.}
\]

Equivalently, for every such bad sequence,

\[
\limsup_n\left(
 2\frac{k_n}{q_n^{1/3}}+
 \left(\frac{u_n}{q_n^{2/3}}\right)^2
\right)\le3^{2/3}.
\]

This is the limsup of the single displayed scalar expression, not a sum of
two coordinatewise limsups.  It shrinks the unresolved boundary to a compact
parabolic cap, but does not empty it.  A separate red-team reconstruction
confirmed the `1/6` shadow-scaling constant and the limiting `1/2` upper
bound.

## 5. Repair and firewall

The frozen manuscript linked Theorem 5.1 to the Proposition 5.3 boundary.
That association is false: in Theorem 5.1,
`delta=binom(b,2)-2binom(q,2)=O(q)` forces

\[
u/q\to\sqrt2-1,
\]

not zero.  Theorem 5.1 and Proposition 5.3 are both correct; only the
sentence relating their phases was wrong.  The live manuscript has been
repaired to call them separate phases.  This is why the verdict is
`PASS_AFTER_REPAIR` rather than `PASS`.

The remaining critical parabolic cap, all growing-promotion regimes, and the
bridge-to-public-problem step remain open.  None of the audited results proves
or refutes Erdős #776.
