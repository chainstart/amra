# Erdős #776: rank-eight entry attack

## Frozen inherited statement

Let

\[
D_{V-12}=0,\qquad
D_{q-1}=V+\operatorname{KK}_q(D_q)
\quad(q=V-12,\ldots,3).
\]

The inherited R004 proof establishes that, for every \(V\ge40\),

\[
D_8<\binom{V-11}{8}
\quad\Longrightarrow\quad
D_2\le\binom{V-9}{2}.
\]

At rank eight the exact canonical prefix is

\[
D_8=\binom{V-12}{8}+\binom{V-13}{7}+W_6,
\]

so the only unproved entry condition is

\[
W_6<\binom{V-13}{6}. \tag{E8}
\]

## Route A: delayed two-harmonic normal form

Once a rank \(q\) has the separated form

\[
D_q=\binom{V-12}{q}+\binom{V-13}{q-1}+W_{q-2},
\qquad W_{q-2}<\binom{V-13}{q-2},
\]

the next residual obeys the exact recurrence

\[
W_{q-3}=V+\operatorname{KK}_{q-2}(W_{q-2}),
\]

provided the residual remains below the second prefix top index.  Thus the
research task is to prove a uniform entry rank and a reservoir bound strong
enough to propagate to rank six.  Computed examples suggest that the residual
top indices remain tiny compared with \(V\), but that observation is not used
as a theorem.

## Route B: supersolution barrier

Seek a rank-dependent colex barrier \(B_q\) satisfying

\[
B_{V-12}\ge0,\qquad
V+\operatorname{KK}_q(B_q)\le B_{q-1},\qquad
B_8<\binom{V-11}{8}.
\]

A single binomial \(B_q=\binom{t_q}{q}-1\) cannot start near rank \(V-12\);
therefore the barrier must encode at least one pre-carry block and then switch
to the two-harmonic normal form.  This records a necessary design constraint,
not a proof.

## Route C: analytic large-\(V\) plus exact finite closure

It is acceptable to prove (E8) analytically for \(V\ge V_0\), with a fully
specified finite exact verification for \(40\le V<V_0\).  The analytic part
must bound the actual carry residual, not merely sample it.  The preferred
target is a polynomial or iterated-log bound on \(W_6\), since the available
reservoir is of order \(V^6\).
