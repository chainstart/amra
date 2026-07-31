# Erdős #776: a rank-16 linear gate for the five-term colex route

Date: 2026-07-30

## Outcome

The named problem is not closed.  The campaign proves a new all-parameter
fixed-depth implication which replaces the inherited rank-eight degree-six
residual test by a linear residual test eight ranks earlier:

> **Rank-16 linear-gate theorem.**  Let \(V\ge175\), and let
> \[
> D_{V-12}=0,\qquad D_{q-1}=V+\operatorname{KK}_q(D_q).
> \]
> If
> \[
> D_{16}\le
> \binom{V-12}{16}+\binom{V-13}{15}+V-1, \tag{1}
> \]
> then
> \[
> D_8<\binom{V-11}{8}. \tag{2}
> \]

Together with the inherited R004 descent, (2) implies the needed rank-two
reservoir condition.  Exact integer arithmetic separately verifies (2) for
\(40\le V\le174\).  Thus the entire remaining colex route is reduced to proving
the unbounded rank-16 premise (1) for \(V\ge175\).

The premise is true at the selected falsifier points
\[
V=175,379,1000,6329,10000,
\]
with residuals \(64,69,83,148,177\), respectively.  These observations are not
used to claim (1) for arbitrary \(V\).

## Proof of the rank-16 linear-gate theorem

Put \(A=V-12\).  The Kruskal--Katona shadow is monotone, so it suffices to start
rank 16 at the right side of (1):

\[
\widetilde D_{16}
=\binom A{16}+\binom{A-1}{15}+w_{14},
\qquad w_{14}=V-1.
\]

For every rank \(r\), if

\[
x=\sum_i\binom{a_i}{i}
\]

is its canonical expansion, then

\[
\operatorname{KK}_r(x)
=\sum_i\binom{a_i}{i-1}
\le \sum_i i\binom{a_i}{i}
\le r x. \tag{3}
\]

Define

\[
c_{14}=1,\qquad c_{r-1}=1+r c_r
\quad(r=14,\ldots,7).
\]

The exact values are

\[
\begin{array}{c|rrrrrrrrr}
r&14&13&12&11&10&9&8&7&6\\
\hline
c_r&1&15&196&2353&25884&258841&
2329570&18636561&130455928.
\end{array}
\]

At \(V=175\), direct integer comparison gives

\[
c_rV<\binom{V-13}{r}\qquad(6\le r\le14). \tag{4}
\]

For fixed \(r\), the ratio \(\binom{V-13}{r}/V\) is strictly increasing:

\[
\frac{\binom{V-12}{r}/(V+1)}
     {\binom{V-13}{r}/V}
=\frac{V(V-12)}{(V+1)(V-12-r)}>1.
\]

Hence (4) holds for every \(V\ge175\).

We now descend.  Suppose at rank \(q\) the separated canonical prefix is

\[
\widetilde D_q
=\binom A q+\binom{A-1}{q-1}+w_{q-2},
\qquad w_{q-2}<c_{q-2}V.
\]

By (4), the residual is below
\(\binom{A-1}{q-2}\), so no hidden carry crosses the two displayed terms.
Consequently

\[
\widetilde D_{q-1}
=\binom A{q-1}+\binom{A-1}{q-2}+w_{q-3},
\]

where

\[
w_{q-3}=V+\operatorname{KK}_{q-2}(w_{q-2})
       <(1+(q-2)c_{q-2})V=c_{q-3}V
\]

by (3).  Induction from \(q=16\) to \(q=8\) gives

\[
\widetilde D_8
=\binom{V-12}{8}+\binom{V-13}{7}+w_6,
\qquad
w_6<c_6V<\binom{V-13}{6}.
\]

Pascal's identity now yields

\[
\widetilde D_8
<
\binom{V-12}{8}+\binom{V-13}{7}+\binom{V-13}{6}
=\binom{V-11}{8}.
\]

Monotonicity transfers this strict inequality from the majorizing orbit
\(\widetilde D\) to the actual orbit \(D\), proving the theorem.

## Why this is a useful but incomplete milestone

R004 stopped at the actual rank-eight expansion

\[
D_8=\binom{V-12}{8}+\binom{V-13}{7}+W_6
\]

and required the degree-six reservoir inequality
\(W_6<\binom{V-13}{6}\).  The present theorem shows that it is enough to
establish a far sharper but structurally simpler statement at rank 16: after
the same two harmonic terms, the remaining residual is less than \(V\).
Once that happens, all later carries are absorbed by a fixed explicit
coefficient table.

The exact orbit has this form throughout the tested range, and its observed
rank-16 residual grows far more slowly than \(V\).  However, the first-carry
rank in the inherited Macaulay dynamics grows like
\(\log\log V+O(1)\) and is unbounded.  Therefore no finite list of carry blocks,
including the present tests, proves (1).  A valid completion still needs either

1. a carry-block invariant proving (1) uniformly across every first-carry
   interval; or
2. a parameter-suspension potential which forces the rank-16 residual below
   \(V\) without enumerating those intervals.

## Literature significance

He and Tang's arXiv:2602.09803v2 proves

\[
2r+2\le n_0(r)\le
2r+2\log_2r+O(\log_2\log_2r)
\]

and explicitly asks whether the error above \(2r\) is bounded.  Closing (1)
would complete the inherited \(n_0(r)\le2r+5\) construction and directly answer
that bounded-error question.  The conditional reduction by itself is not yet a
paper-level solution.

## Reproduction

Run:

```bash
python3 \
  data/research_open/q1_four_problem_campaign_2026-07-30/erdos776/\
verify_rank16_linear_gate.py
```

The script:

1. checks the coefficient separations at the analytic base \(V=175\);
2. verifies \(40\le V\le174\) with both the inherited compressed engine and an
   independent ordinary canonical engine;
3. records selected rank-16 falsifier values; and
4. explicitly labels the arbitrary-\(V\) rank-16 premise as open.

## Second-attack addendum

The second attack did not prove the rank-16 premise.  It produced three
sharper all-parameter interfaces.

1. Adjacent shortened orbits obey diagonal suspension.  On the separated
   rank-16 branch, the conjectured one-Lipschitz estimate for \(W(V)\) is
   exactly equivalent to a rank-17 shadow-loss inequality.  Actual jump
   points attain that inequality with equality, so qualitative gap
   positivity is insufficient.
2. A 14-term moving-block lemma gives
   \[
   W=27+\operatorname{KK}_2(y_2),\qquad
   y_2=V+\operatorname{KK}_3(z_3).
   \]
   An all-block \(O(\log\log V)\) bound for the final entry rank would close
   the gate.  The inherited \(O(\log\log V)\) first-carry theorem does not
   control the later chart changes required here.
3. The reverse zero-basin at rank \(q\) is exactly the integer interval
   \([D_q,E_q-1]\).  Therefore the observed reverse rank-18 trajectory to
   zero is equivalent to the candidate barrier \(D_{18}\le B_{18}\), not an
   independent proof of it.  Its useful output is a sharp forward invariant
   target whose threshold has three consecutive defect-two canonical digits
   and one additional unit.  It is enough to dominate that colex threshold;
   the actual orbit need not have the same literal prefix.

See `LIPSCHITZ_ATTACK.md` and `REVERSE_RANK18_BARRIER.md`.  All three
interfaces retain the same open all-\(V\) lower edge; none is a proof of
\(n_0(r)\le2r+5\).
