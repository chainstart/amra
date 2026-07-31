# Erdős #776: independent audit of the reverse rank-18 barrier

Date: 2026-07-30

## 1. Proposed barrier and verdict

For the shortened orbit

\[
D_{V-12}=0,\qquad D_q=V+\operatorname{KK}_{q+1}(D_{q+1}),
\]

consider

\[
\begin{aligned}
B_{18}(V)
={}&\binom{V-12}{18}
+  \sum_{i=4}^{17}\binom{V-31+i}{i}
+  \binom{V-30}{3}-1. \tag{1.1}
\end{aligned}
\]

Starting with \(b_{18}=B_{18}(V)\), the proposed reverse test is

\[
b_{q+1}=U_q(b_q-V),\qquad 18\le q\le V-13. \tag{1.2}
\]

Exact experiments give \(b_{V-13}=V\) and \(b_{V-12}=0\) for all tested
\(V\ge70\).

The audit verdict is:

> **The experiment is an exact reformulation, not yet a proof.**  For every
> \(V\) for which the displayed quantities are defined, (1.2) is legal at
> every rank and ends at zero if and only if
> \[
> D_{18}\le B_{18}(V).
> \]
> Thus an all-parameter proof that every intermediate \(b_q\ge V\) would
> prove the desired rank-18 barrier, but that positivity assertion is
> precisely the unresolved lower-edge inequality.  Checking the terminal
> value after a finite computation cannot supply its missing universal
> quantifier.

No counterexample was found for \(V\ge70\), but this note does **not** prove
the barrier.

## 2. Macaulay adjunction

For the \(q\)-canonical expansion

\[
x=\sum_i\binom{a_i}{i},
\]

write

\[
U_q(x)=\sum_i\binom{a_i}{i+1}.
\]

The only order-theoretic input needed below is

\[
U_q(x)\ge y
\quad\Longleftrightarrow\quad
x\ge\operatorname{KK}_{q+1}(y). \tag{2.1}
\]

Since all quantities are integers, (2.1) also gives

\[
U_q(x)\le y-1
\quad\Longleftrightarrow\quad
x\le\operatorname{KK}_{q+1}(y)-1. \tag{2.2}
\]

## 3. The exact zero-basin interval

Define the adjacent seeded orbit

\[
E_{V-12}=1,\qquad
E_q=V+\operatorname{KK}_{q+1}(E_{q+1}). \tag{3.1}
\]

For \(18\le q\le V-12\), let \(\mathcal I_q\) be the set of integers \(x\)
such that the reverse process

\[
x_q=x,\qquad x_{p+1}=U_p(x_p-V)
\]

is legal from rank \(q\) to rank \(V-12\) and has
\(x_{V-12}=0\).

### Theorem 3.1 (zero-basin theorem)

\[
\boxed{\mathcal I_q=[D_q,E_q-1]\cap\mathbb Z.} \tag{3.2}
\]

### Proof

At the top rank,

\[
\mathcal I_{V-12}=\{0\}
=[D_{V-12},E_{V-12}-1].
\]

Suppose (3.2) holds at rank \(q+1\).  An integer \(x\) belongs to
\(\mathcal I_q\) exactly when

\[
D_{q+1}\le U_q(x-V)\le E_{q+1}-1.
\]

By (2.1)--(2.2), this is equivalent to

\[
\operatorname{KK}_{q+1}(D_{q+1})
\le x-V
\le\operatorname{KK}_{q+1}(E_{q+1})-1.
\]

The two endpoint recurrences turn this into

\[
D_q\le x\le E_q-1.
\]

Moreover \(D_q\ge V\) below the top rank, so membership in this interval
automatically makes every subtraction in the reverse process legal.  This
completes the induction. \(\square\)

Consequently,

\[
\boxed{
\text{the reverse orbit from }B_{18}\text{ is legal and ends at }0
\iff D_{18}\le B_{18}\le E_{18}-1.
} \tag{3.3}
\]

This theorem pinpoints the quantifier issue: terminal zero is a valid
certificate for any *specified* \(V\), but proving it for every \(V\) is
exactly proving that the symbolic starting point lies in the interval
(3.2).

## 4. The upper edge is unconditional and easy

Put

\[
P_q(V)=\binom{V-12}{q}+\binom{V-13}{q-1}. \tag{4.1}
\]

The candidate has a useful closed comparison with \(P_{18}\).  The
hockey-stick identity gives

\[
\sum_{i=4}^{17}\binom{V-31+i}{i}
=\binom{V-13}{17}
-1-(V-30)-\binom{V-29}{2}-\binom{V-28}{3}.
\]

Therefore

\[
\boxed{
P_{18}(V)-B_{18}(V)
=V-28+2\binom{V-29}{2}+\binom{V-30}{2}.
} \tag{4.2}
\]

In particular \(B_{18}<P_{18}\) for \(V\ge31\).

There is also a short all-parameter lower bound on the upper basin edge.
At rank \(V-13\),

\[
\begin{aligned}
E_{V-13}
&=V+\operatorname{KK}_{V-12}(1)
=2V-12,\\
P_{V-13}
&=(V-12)+(V-13)
=2V-25.
\end{aligned}
\]

Thus \(E_{V-13}>P_{V-13}\).  Whenever \(q\le V-13\), the two displayed
terms in \(P_q\) are canonically separated, so

\[
\operatorname{KK}_q(P_q)=P_{q-1}.
\]

Monotonicity now yields

\[
E_{q-1}
=V+\operatorname{KK}_q(E_q)
\ge V+\operatorname{KK}_q(P_q)
>P_{q-1}.
\]

Descending to rank \(18\) proves

\[
\boxed{B_{18}<P_{18}<E_{18}.} \tag{4.3}
\]

Hence the right-hand inequality in (3.3) is already proved for every
\(V\ge31\).  The reverse barrier has only one remaining side:

\[
\boxed{D_{18}\le B_{18}.} \tag{4.4}
\]

Equivalently, since (4.3) rules out escape through the upper edge, it
suffices and is necessary to prove

\[
b_q\ge V\quad(18\le q\le V-13). \tag{4.5}
\]

At the last rank, (4.5) and (4.3) give

\[
V\le b_{V-13}\le2V-13.
\]

Every integer in this interval maps to zero, because
\(0\le b_{V-13}-V\le V-13\) has zero \(U_{V-13}\)-image.  The experimentally
observed equality \(b_{V-13}=V\) is a stronger feature of this particular
candidate; it is not forced by the basin argument and is not needed for
\(D_{18}\le B_{18}\).

## 5. Connection with the forward slack chart

The same missing inequality can be seen from the forward orbit.  Set

\[
n=V-11,\qquad X_q=P_q-D_q,\qquad R=n-q.
\]

Pascal's identity gives the useful complement form

\[
P_q
=\binom{n}{q}-\binom{n-2}{q-2}. \tag{5.1}
\]

In any rank interval in which the tail complement is canonically
separated, the standard complement identity gives

\[
\operatorname{KK}_q(P_q-X_q)
=P_{q-1}-U_{R-1}(X_q).
\]

Consequently the forward slack obeys the exact scalar recurrence

\[
\boxed{X_{q-1}=U_{R-1}(X_q)-V.} \tag{5.2}
\]

At rank \(q=V-13\), one has \(R=2\), \(D_q=V\), and hence

\[
X_{V-13}=P_{V-13}-D_{V-13}=V-25. \tag{5.3}
\]

The moving-block comparison

\[
H_q=P_q-\binom{V-27}{s},\qquad s=q-15,
\]

is the same complement cap, since

\[
\binom{V-27}{s}
=\binom{V-27}{R-1}. \tag{5.4}
\]

At rank \(18\), equation (4.2) has the shorter equivalent form

\[
\boxed{
P_{18}-B_{18}
=\binom{V-27}{3}-\binom{V-30}{3}+1.
} \tag{5.5}
\]

Thus the rank-18 barrier is equivalently the forward-slack lower bound

\[
X_{18}
\ge\binom{V-27}{3}-\binom{V-30}{3}+1. \tag{5.6}
\]

This threshold itself has a particularly simple canonical prefix.  At
slack rank \(R-1=V-30\),

\[
\begin{aligned}
\binom{V-27}{3}-\binom{V-30}{3}+1
={}&\binom{V-28}{V-30}
+\binom{V-29}{V-31}\\
&+\binom{V-30}{V-32}
+\binom{V-33}{V-33}. \tag{5.7}
\end{aligned}
\]

Thus one sufficient form of a successful forward invariant is to guarantee
the three consecutive defect-two leading digits

\[
(V-28,V-30),\quad(V-29,V-31),\quad(V-30,V-32)
\]

and one further unit in the \((V-30)\)-canonical expansion.  More generally,
it is enough that \(X_{18}\) dominate the colex threshold (5.7); a larger
earlier canonical digit need not reproduce the displayed prefix literally.
This is the sharp explicit domination target exposed by the reverse barrier.
The finite orbits do exhibit a much longer prefix, but that persistence is
not yet an all-\(V\) theorem.

This explains why the proposed reverse process numerically mirrors the
successive-block slack process: they are the two Galois-adjoint views of
the same inequality.  Formula (5.2) is exact inside a separated complement
chart, but continuing it across every later chart change without a
carry-transition lemma would again assume the point at issue.

## 6. Canonical form at rank 18

The low tail in (1.1) can be expanded without ambiguity:

\[
\binom{V-30}{3}-1
=\binom{V-31}{3}
+\binom{V-32}{2}
+\binom{V-33}{1}. \tag{6.1}
\]

Thus \(B_{18}\) has the canonical expansion

\[
\binom{V-12}{18}
+\sum_{i=4}^{17}\binom{V-31+i}{i}
+\binom{V-31}{3}
+\binom{V-32}{2}
+\binom{V-33}{1}. \tag{6.2}
\]

This is a clean initial chart, but it does not remain a single fixed chart
under (1.2): before each suspension one subtracts \(V\), and that
subtraction can borrow across the lowest surviving canonical term.
Successive borrow positions depend on \(V\).  Merely shifting every lower
index in (6.2), or continuing the first borrow chart after its first
collision, silently assumes (4.5).

In partition language, if a canonical digit is written
\(\binom{i+\lambda_i}{i}\), then \(U_q\) decreases every surviving
\(\lambda_i\) by one and discards zero parts.  The difficult operation is
the intervening subtraction of \(V\), which re-canonicalizes the tail and
can cross a block boundary.  A successful canonical invariant must control
all such re-canonicalizations, not only the first one.

## 7. Falsifier information and the sharp warning

Finite exact arithmetic is useful only as a falsifier here.  With the
ordinary greedy combinadic expansion:

- the proposed reverse process reaches \(b_{V-13}=V\) and then zero for
  every checked \(V\ge69\);
- for \(40\le V\le68\), it instead drops below \(V\) at rank \(V-13\)
  (for example, \(V=40\) gives \(b_{27}=37\), and \(V=68\) gives
  \(b_{55}=67\)).

These observations explain why a proof needs an explicit lower cutoff and
why the advertised \(V\ge70\) is plausible.  They do not establish the
infinite range.

The most dangerous invalid argument is:

1. prove \(B_{18}<E_{18}\);
2. propagate the reverse recurrence formally;
3. infer that the terminal value is \(0\).

Step 2 is legal only after proving every \(b_q\ge V\).  By Theorem 3.1 that
legality is equivalent to \(B_{18}\ge D_{18}\), the desired result itself.
Thus this argument is circular.

## 8. Exact next target

The reverse formulation is still useful because it isolates a concrete
invariant problem:

> Find an all-\(V\) canonical potential \(\Phi_q\), valid across every
> borrow chart, such that
> \[
> \Phi_{18}(B_{18})\ge0,\qquad
> \Phi_q(b_q)\ge0\Longrightarrow b_q\ge V
> \text{ and }\Phi_{q+1}(U_q(b_q-V))\ge0.
> \]

Two acceptable ways to close it would be:

1. a block-by-block induction whose transition statement explicitly
   includes the collision/carry case; or
2. a set-family construction showing that after reserving \(V\) \(q\)-sets
   at every stage, the colex clique operator still contains the next
   reserved family.

Until such a lower invariant is supplied, the rank-18 reverse barrier
remains an exact, well-focused conjectural certificate rather than an
all-parameter theorem.

## 9. Independent finite guard

The independent exact guard is
`verify_reverse_rank18_barrier.py`.  It contains both an ordinary greedy
combinadic implementation and a separately run-compressed implementation;
it imports neither the inherited #776 engine nor any campaign module.

Run:

```bash
cd data/research_open/q1_four_problem_campaign_2026-07-30/erdos776
python3 verify_reverse_rank18_barrier.py
```

Result on 2026-07-30:

```text
status: PASS
scope: FINITE FALSIFIER/REGRESSION EVIDENCE ONLY
formula and canonical checks: 40 <= V <= 1000
expected failures: 40 <= V <= 68
contiguous successes: 69 <= V <= 500
strategic successes: V = 632, 750, 1000
ordinary/compressed agreement: 2411 reverse steps, 40 <= V <= 100
zero-basin endpoint checks: V = 40, 50, 69, 70, 100
```

The failure guard includes \(b_{27}=37<40\) at \(V=40\) and
\(b_{55}=67<68\) at \(V=68\).  Every successful row in the stated finite
sets has \(b_{V-13}=V\) and \(b_{V-12}=0\).  The zero-basin guard checks,
at every relevant rank for its five parameters, both endpoint recurrences,
the inside images of \(D_q\) and \(E_q-1\), and the outside images of
\(D_q-1\) and \(E_q\) whenever defined.

This execution is deliberately labelled finite evidence.  It does not
alter the open all-\(V\) status of (4.4)--(4.5).
