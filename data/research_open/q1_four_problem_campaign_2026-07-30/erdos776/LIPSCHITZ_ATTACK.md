# Erdős #776: attack on the rank-16 residual Lipschitz conjecture

Date: 2026-07-30

## 1. Status

For the shortened orbit

\[
D^{[V]}_{V-12}=0,\qquad
D^{[V]}_{q-1}=V+\operatorname{KK}_q(D^{[V]}_q),
\]

put

\[
P_q(V)=\binom{V-12}{q}+\binom{V-13}{q-1},
\qquad
W(V)=D^{[V]}_{16}-P_{16}(V).
\]

The proposed closing lemma is

\[
\boxed{W(V+1)-W(V)\le1\qquad(V\ge175).} \tag{L}
\]

Together with \(W(175)=64\), (L) would give
\(W(V)\le V-111<V\), and hence close the rank-16 gate.

This attack does **not** prove (L), and it finds no counterexample to (L).
It does prove an all-parameter diagonal-suspension theorem and reduces (L)
to a sharp, explicit rank-17 shadow-loss inequality.  It also isolates the
precise missing quantifier in a proposed moving-block asymptotic proof.
Finite evaluations below are falsifier diagnostics only.

## 2. Macaulay notation

If

\[
x=\sum_i\binom{a_i}{i}
\]

is the \(p\)-canonical expansion, write

\[
U_p(x)=\sum_i\binom{a_i}{i+1},
\qquad
S_p(x)=\sum_i\binom{a_i+1}{i+1}=x+U_p(x).
\]

The identities used below are

\[
\operatorname{KK}_{p+1}(S_p(x))
=x+\operatorname{KK}_p(x), \tag{2.1}
\]

and the Galois adjunction

\[
U_p(x)\ge y
\quad\Longleftrightarrow\quad
x\ge\operatorname{KK}_{p+1}(y). \tag{2.2}
\]

The one-set shadow bound gives, for every \(r\ge1\),

\[
\operatorname{KK}_r(x+1)-\operatorname{KK}_r(x)\le r. \tag{2.3}
\]

Indeed, the next \(r\)-set in colex order has at most \(r\) new
\((r-1)\)-subsets.

## 3. An unconditional diagonal-suspension theorem

### Theorem 3.1

For every \(V\ge40\) and every common rank in the aligned descent,

\[
\boxed{
D^{[V+1]}_q
\le S_{q-1}\!\left(D^{[V]}_{q-1}\right)
}
\qquad(16\le q\le V-12). \tag{3.1}
\]

### Proof

At the first aligned rank \(q=V-12\),

\[
D^{[V+1]}_{V-12}=V+1,\qquad
D^{[V]}_{V-13}=V.
\]

The \((V-13)\)-canonical expansion is

\[
V=\binom{V-12}{V-13}
  +\sum_{i=V-25}^{V-14}\binom{i}{i},
\]

so simultaneous suspension gives

\[
S_{V-13}(V)=V+1.
\]

Thus (3.1) starts with equality.

Suppose (3.1) holds at rank \(q\), and put

\[
x=D^{[V]}_{q-1},\qquad
y=D^{[V]}_{q-2}=V+\operatorname{KK}_{q-1}(x).
\]

By monotonicity and (2.1),

\[
\begin{aligned}
D^{[V+1]}_{q-1}
&\le V+1+\operatorname{KK}_q(S_{q-1}(x))\\
&=V+1+x+\operatorname{KK}_{q-1}(x)
=y+x+1. \tag{3.2}
\end{aligned}
\]

On the other hand, (2.3) and \(V\ge q-1\) give

\[
y\ge\operatorname{KK}_{q-1}(x+1).
\]

The adjunction (2.2) therefore yields \(U_{q-2}(y)\ge x+1\), and hence

\[
S_{q-2}(y)=y+U_{q-2}(y)\ge y+x+1.
\]

Combining this with (3.2) proves the next aligned rank. \(\square\)

This theorem is genuinely all-parameter.  It is nevertheless too weak by
itself: the nonnegative diagonal gap must produce a quantitatively large
shadow loss at rank 17.

## 4. Exact gap recursion and the sharp closing inequality

Define

\[
G_q(V)=
S_{q-1}\!\left(D^{[V]}_{q-1}\right)-D^{[V+1]}_q\ge0. \tag{4.1}
\]

With \(x,y\) as in the proof of Theorem 3.1, define

\[
\begin{aligned}
L_q(V)
&=\operatorname{KK}_q(S_{q-1}(x))
 -\operatorname{KK}_q(S_{q-1}(x)-G_q(V)),\\
E_{q-1}(V)
&=U_{q-2}(y)-x-1.
\end{aligned}
\]

The proof above shows \(E_{q-1}(V)\ge0\), and direct substitution gives the
exact gap recursion

\[
\boxed{G_{q-1}(V)=E_{q-1}(V)+L_q(V).} \tag{4.2}
\]

Thus the qualitative suspension theorem only records \(E,L\ge0\); the
desired conclusion needs a lower bound on one of these losses.

Assume \(0\le W(V)<V\).  This is the positive separated branch relevant to
the proposed induction; for \(V\ge175\) it ensures the canonical expansion

\[
D^{[V]}_{16}=P_{16}(V)+W(V)
\]

and consequently

\[
\operatorname{KK}_{16}(D^{[V]}_{16})
=P_{15}(V)+\operatorname{KK}_{14}(W(V)). \tag{4.3}
\]

Let

\[
N=S_{16}(D^{[V]}_{16}),\qquad
L_{17}=\operatorname{KK}_{17}(N)
       -\operatorname{KK}_{17}(N-G_{17}(V)).
\]

Since \(P_{16}(V+1)-P_{16}(V)=P_{15}(V)\), equations (2.1) and (4.3)
give the exact identity

\[
\boxed{
W(V+1)-W(V)
=V+1+\operatorname{KK}_{14}(W(V))-L_{17}.
} \tag{4.4}
\]

Therefore the proposed Lipschitz lemma is exactly equivalent, on this
positive separated branch, to

\[
\boxed{
L_{17}\ge V+\operatorname{KK}_{14}(W(V)).
} \tag{4.5}
\]

There is no asymptotic or finite extrapolation in (4.4)--(4.5).

The Galois adjunction turns (4.5) into a minimum-gap threshold.  If

\[
\ell=V+\operatorname{KK}_{14}(W(V)),
\]

then (4.5) is equivalent to

\[
\boxed{
G_{17}(V)\ge
N-U_{16}\!\left(\operatorname{KK}_{17}(N)-\ell\right).
} \tag{4.6}
\]

Equation (4.6), rather than \(G_{17}\ge0\), is the precise remaining
diagonal-suspension target.

Exact diagnostics illustrate that (4.5) is sharp:

| \(V\) | \(W(V)\) | \(W(V+1)\) | \(L_{17}\) | required in (4.5) | surplus |
|---:|---:|---:|---:|---:|---:|
| 175 | 64 | 64 | 571 | 570 | 1 |
| 205 | 64 | 65 | 600 | 600 | 0 |
| 240 | 65 | 66 | 635 | 635 | 0 |
| 379 | 69 | 69 | 805 | 804 | 1 |
| 381 | 69 | 70 | 806 | 806 | 0 |
| 1000 | 83 | 83 | 1477 | 1476 | 1 |
| 6329 | 148 | 148 | 7070 | 7069 | 1 |

These rows are checks, not a proof.  In particular, a coarse positive-gap
argument cannot close (L): actual jump points attain (4.5) with equality.

## 5. The 14-term moving block

For \(s\ge2\), define the canonical moving block

\[
H_{s+15}(V)
=\binom{V-12}{s+15}
 +\sum_{j=1}^{14}\binom{V-28+j}{s+j}. \tag{5.1}
\]

The displayed upper indices are \(V-12,V-14,\ldots,V-27\).
If

\[
D^{[V]}_{s+15}=H_{s+15}(V)+Z_s,\qquad
0\le Z_s<\binom{V-27}{s}, \tag{5.2}
\]

then the residual is canonically separated from the lowest moving-block
term.  One exact descent gives

\[
D^{[V]}_{s+14}=H_{s+14}(V)+Z_{s-1},
\qquad
Z_{s-1}=V+\operatorname{KK}_s(Z_s), \tag{5.3}
\]

provided the next residual remains separated.  Iterating (5.3) down to
rank 18 and rank 17 gives

\[
\begin{aligned}
D^{[V]}_{18}
&=\binom{V-12}{18}
 +\sum_{i=4}^{17}\binom{V-31+i}{i}+z_3,\\
D^{[V]}_{17}
&=\binom{V-12}{17}
 +\sum_{i=3}^{16}\binom{V-30+i}{i}+y_2,\\
y_2&=V+\operatorname{KK}_3(z_3). \tag{5.4}
\end{aligned}
\]

Finally, the hockey-stick identity gives

\[
V+\sum_{i=2}^{15}\binom{V-29+i}{i}
=\binom{V-13}{15}+27,
\]

and therefore

\[
\boxed{W(V)=27+\operatorname{KK}_2(y_2).} \tag{5.5}
\]

Equations (5.1)--(5.5) are a rigorous **conditional block lemma**.  What is
not yet proved is that the actual orbit remains in this separated block
through every intervening carry for arbitrary \(V\).

There is one useful unconditional fact about entry.  At the top rank,
\(D_{V-12}=0<H_{V-12}=1\), and at rank \(V-13\),

\[
D_{V-13}=V<H_{V-13}=V+2.
\]

If \(q=s+15\ge17\) is the first rank on the downward orbit with
\(D_q\ge H_q\), then monotonicity gives

\[
\begin{aligned}
0\le Z_s
&=D_q-H_q\\
&=V-\left(
\operatorname{KK}_{q+1}(H_{q+1})
-\operatorname{KK}_{q+1}(D_{q+1})\right)
\le V. \tag{5.6}
\end{aligned}
\]

Moreover \(q\le V-14\), so \(2\le s\le V-29\), and
\(V<\binom{V-27}{s}\).  Thus the first entry itself is separated.
The unresolved issue is preventing a later residual from colliding with
the bottom of the moving block.

If no entry has occurred by rank 17, then

\[
D_{16}=V+\operatorname{KK}_{17}(D_{17})
\le V+\operatorname{KK}_{17}(H_{17})
=P_{16}(V)+27,
\]

which already proves the rank-16 gate.  Hence only the entered-block branch
needs further control.

## 6. A conditional asymptotic closure theorem

Suppose that the first moving-block entry occurs at residual rank \(s=s(V)\)
and that

\[
s(V)=O(\log\log V). \tag{6.1}
\]

Starting from the separated entry (5.6), follow (5.3) up to the first
putative later collision and use the elementary bound
\(\operatorname{KK}_r(x)\le r x\).  If

\[
B_s=1,\qquad B_{r-1}=1+rB_r,
\]

then

\[
Z_r\le B_rV,\qquad
B_r\le\frac{(s+1)!}{(r+1)!}. \tag{6.2}
\]

Condition (6.1) implies

\[
(s+1)!=
\exp(O(\log\log V\log\log\log V))=V^{o(1)}.
\]

Thus (6.2) gives \(Z_r\le V^{1+o(1)}\) before that putative collision.  Since
\(2\le r\le s=o(V)\),

\[
\binom{V-27}{r}\ge\binom{V-27}{2}
\]

for all sufficiently large \(V\).  Hence (6.2) contradicts the first
putative collision and bootstraps (5.3) all the way to rank 2.  No separate
no-collision assumption is needed once (6.1) and the first-entry bound are
available for large \(V\).

At the last two ranks, the standard fixed-rank shadow estimates give

\[
z_3\le V^{1+o(1)},\qquad
\operatorname{KK}_3(z_3)=V^{2/3+o(1)},
\]

so

\[
y_2=V+V^{2/3+o(1)},\qquad
W(V)=V^{1/2+o(1)}<V. \tag{6.3}
\]

Consequently:

> **Conditional closure.**  A uniform proof that the actual first
> moving-block entry rank satisfies \(s(V)=O(\log\log V)\) closes the
> rank-16 gate for all sufficiently large \(V\); an exact finite bridge
> would then finish the route.

This conclusion is stronger than Lipschitz, but its hypothesis is not
currently available.

## 7. Why the Round12 first-carry partition does not prove (6.1)

Round12 rigorously partitions all parameters according to the **first**
canonical carry of its forward slack orbit and proves that this first-carry
rank is \(\log_2\log V+O(1)\).  It also explicitly stops after giving the
post-first-carry normal form: the second and later blocks have no uniform
potential.

The moving-block entry used in (5.6) is a later sign/cap event after all
intervening re-canonicalizations.  Identifying its residual rank \(s(V)\)
with the Round12 first-carry rank would silently assume that every
successive block preserves the same cap.  That is exactly the missing
statement, not a consequence of the first-carry partition.

Equivalently, before the first low-tail collision one may rewrite the
block deficit by a forward recurrence of the form

\[
g_{p+1}=U_p(g_p)-V.
\]

At its first collision the subtraction is no longer confined to the same
lowest canonical term; the tail-complement formula changes chart.  Continuing
the old scalar recurrence beyond that collision is invalid.  The Round12
partition certifies the location and normal form of this first chart change,
but not the final moving-block entry after successive chart changes.

Therefore the inference

\[
\text{“first carry has rank }O(\log\log V)\text{”}
\quad\Longrightarrow\quad
\text{“the entry rank in (5.6) is }O(\log\log V)\text{”}
\]

is presently a quantifier gap.  Finite persistence of the 14-term block
cannot repair it.

## 8. A lower-rank equivalent target

When the rank-17/18 forms (5.4) hold for both adjacent parameters, (5.5)
turns (L) into a two-step Galois condition.  Write

\[
k=\operatorname{KK}_2(y_2(V)).
\]

Then

\[
\begin{aligned}
W(V+1)-W(V)\le1
&\iff \operatorname{KK}_2(y_2(V+1))\le k+1\\
&\iff y_2(V+1)\le U_1(k+1)
=\binom{k+1}{2}. \tag{8.1}
\end{aligned}
\]

Since \(y_2(V+1)=V+1+\operatorname{KK}_3(z_3(V+1))\), whenever the
right side below is nonnegative this is further equivalent to

\[
\boxed{
z_3(V+1)\le
U_2\!\left(\binom{k+1}{2}-(V+1)\right).
} \tag{8.2}
\]

Thus there are now two exact, nonredundant closing targets:

1. the rank-17 diagonal shadow-loss inequality (4.5), which does not assume
   a moving-block history; or
2. the rank-3 Galois threshold (8.2), after proving uniform separated entry
   into the 14-term moving block.

The next useful theorem must supply one of these quantitative statements.
Qualitative diagonal domination, first-carry classification, or a larger
finite cutoff alone is insufficient.
