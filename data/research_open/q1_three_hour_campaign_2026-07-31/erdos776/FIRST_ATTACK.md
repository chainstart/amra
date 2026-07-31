# Erdős #776: first attack — a zero-slack rank-18 gate

Date: 2026-07-31

## 1. Outcome

The attack does not prove Erdős #776 and does not prove the previously
proposed quantitative gap

\[
G_2(V)\ge V+1.
\]

It does prove a substantially weaker sufficient condition for closing the
five-term colex route.

> **Zero-slack rank-18 gate.**  Let \(V\ge288\), and let
> \[
> D_{V-12}=0,\qquad
> D_{q-1}=V+\operatorname{KK}_q(D_q).
> \]
> Put
> \[
> P_q(V)=\binom{V-12}{q}+\binom{V-13}{q-1}.
> \]
> If
> \[
> \boxed{D_{18}\le P_{18}(V),} \tag{1.1}
> \]
> then
> \[
> \boxed{D_8<\binom{V-11}{8}.} \tag{1.2}
> \]

Exact arithmetic supplies (1.2) directly for \(40\le V\le287\).
Consequently the entire inherited route is now reduced to the qualitative
colex domination (1.1) for \(V\ge288\).

This is strictly weaker than the old reverse rank-18 barrier.  That barrier
required

\[
D_{18}\le P_{18}
-\left[
\binom{V-27}{3}-\binom{V-30}{3}+1
\right],
\]

so it demanded a positive slack of order \(V^2\).  The new gate only asks
that the slack

\[
X_{18}=P_{18}-D_{18}
\]

be nonnegative.

## 2. Two elementary shadow bounds

If

\[
x=\sum_i\binom{a_i}{i}
\]

is its \(r\)-canonical expansion, then

\[
\operatorname{KK}_r(x)
=\sum_i\binom{a_i}{i-1}
\le r\sum_i\binom{a_i}{i}
=rx. \tag{2.1}
\]

We also use monotonicity of the Kruskal--Katona shadow.  No asymptotic
estimate and no finite carry extrapolation enters the analytic proof.

## 3. Rank 18 to rank 16

Assume (1.1).  The two terms in \(P_{18}\) are canonically separated and

\[
\operatorname{KK}_{18}(P_{18})=P_{17}.
\]

Therefore

\[
D_{17}
=V+\operatorname{KK}_{18}(D_{18})
\le P_{17}+V. \tag{3.1}
\]

For \(V\ge288\),

\[
V<\binom{V-13}{15}.
\]

This holds by direct comparison at \(V=288\), and the ratio
\(\binom{V-13}{15}/V\) is strictly increasing by the same calculation used
in Section 4.

Hence the \(15\)-canonical expansion of the residual \(V\) lies strictly
below the two displayed terms of

\[
P_{17}
=\binom{V-12}{17}+\binom{V-13}{16}.
\]

There is no hidden carry, and

\[
\operatorname{KK}_{17}(P_{17}+V)
=P_{16}+\operatorname{KK}_{15}(V).
\]

Using (3.1), monotonicity, and (2.1) gives

\[
\begin{aligned}
D_{16}
&\le V+\operatorname{KK}_{17}(P_{17}+V)\\
&=P_{16}+V+\operatorname{KK}_{15}(V)\\
&\le P_{16}+16V. \tag{3.2}
\end{aligned}
\]

Thus qualitative domination at rank 18 produces a linear rank-16
residual.  The old attack required that residual to be smaller than \(V\);
the next section shows that any explicit \(16V\) bound is already enough.

## 4. Fixed-depth propagation

Define

\[
\begin{aligned}
c_{14}&=16,\\
c_{r-1}&=1+r c_r\qquad(r=14,\ldots,7).
\end{aligned}
\]

The exact coefficients are

\[
\begin{array}{c|rrrrrrrrr}
r&14&13&12&11&10&9&8&7&6\\
\hline
c_r&
16&225&2926&35113&386244&3862441&
34761970&278095761&1946670328.
\end{array} \tag{4.1}
\]

At \(V=288\), exact integer comparison gives

\[
c_rV<\binom{V-13}{r}\qquad(6\le r\le14). \tag{4.2}
\]

The smallest margin is at \(r=6\), where it equals

\[
7{,}970{,}088{,}636.
\]

For fixed \(r\), the ratio

\[
\frac{\binom{V-13}{r}}{V}
\]

is strictly increasing in \(V\).  Indeed, its step ratio is greater than
one precisely because

\[
V(V-12)-(V+1)(V-12-r)
=(r-1)V+r+12>0.
\]

Thus (4.2) holds for every \(V\ge288\).

Starting from (3.2), write

\[
D_{16}\le
\binom{V-12}{16}+\binom{V-13}{15}+w_{14},
\qquad w_{14}\le c_{14}V.
\]

By (4.2), \(w_{14}<\binom{V-13}{14}\), so the residual is separated.
Suppose at a later rank the majorizing orbit has the separated form

\[
\binom{V-12}{r+2}
+\binom{V-13}{r+1}+w_r,
\qquad w_r\le c_rV.
\]

One exact shadow step gives the next residual

\[
w_{r-1}=V+\operatorname{KK}_r(w_r)
\le(1+r c_r)V=c_{r-1}V. \tag{4.3}
\]

The next separation follows again from (4.2).  Iterating (4.3) to rank
eight yields

\[
D_8\le
\binom{V-12}{8}+\binom{V-13}{7}+w_6,
\qquad
w_6\le c_6V<\binom{V-13}{6}.
\]

Pascal's identity now gives

\[
D_8
<\binom{V-12}{8}
 +\binom{V-13}{7}
 +\binom{V-13}{6}
=\binom{V-11}{8},
\]

which proves the zero-slack gate.

## 5. Exact finite bridge

The compressed exact Macaulay engine verifies

\[
D_8<\binom{V-11}{8}
\qquad(40\le V\le287).
\]

The minimum margin on that finite interval is \(260272\).  This finite
bridge is a finite component of the conditional reduction; it is not
evidence that (1.1) holds for arbitrary \(V\).

Combining the bridge with the analytic theorem gives:

> To close the inherited five-term construction for every parameter, it is
> enough to prove \(D_{18}\le P_{18}\) for every \(V\ge288\).

## 6. A one-binomial complementary formulation

The zero-slack condition has a simpler reverse complement than the old
four-term barrier.  Set

\[
n=V-11,\qquad R=V-29.
\]

Because

\[
P_{18}
=\binom n{18}-\binom{n-2}{16},
\]

the complement of the reverse start \(P_{18}\) is just

\[
\boxed{C_R=\binom{V-13}{R}.} \tag{6.1}
\]

Define the independent complementary descent

\[
C_{r-1}=\operatorname{KK}_r(C_r+V)
\qquad(r=R,\ldots,3). \tag{6.2}
\]

At the penultimate reverse rank put

\[
T(V)=\binom{V-11}{2}-V. \tag{6.3}
\]

The tail-complement identity and the zero-basin theorem give the exact
equivalence

\[
\boxed{
D_{18}\le P_{18}
\iff C_2\le T(V).
} \tag{6.4}
\]

Thus the remaining target starts from one binomial term, rather than the
four nontrivial terms and one unit in the old reverse barrier.  Equation
(6.4) is still an equivalence, not a proof: a finite reverse run cannot
replace a uniform bound on (6.2).

## 7. Audit of the proposed \(G_2\) induction

For the old quantitative reverse barrier, let

\[
G_2(V)=S_2(A_2^{[V]})-A_3^{[V+1]}.
\]

If the exact endpoint at parameter \(V\) is

\[
A_2^{[V]}=T(V),
\]

then Galois adjunction gives

\[
A_2^{[V+1]}\le T(V+1)
\iff G_2(V)\ge V+1. \tag{7.1}
\]

There is no slack in (7.1).  More explicitly,

\[
\begin{aligned}
S_2(T(V))-(V+1)
={}&\binom{V-12}{3}
+\binom{V-26}{2}+V-52. \tag{7.2}
\end{aligned}
\]

Hence

\[
G_2(V)\ge V+1
\iff
A_3^{[V+1]}
\le
\binom{V-12}{3}+\binom{V-26}{2}+V-52. \tag{7.3}
\]

In the next parameter \(W=V+1\), the right side is

\[
\binom{W-13}{3}+\binom{W-27}{2}+W-53,
\]

which is exactly the rank-three Galois fibre ceiling for
\(A_2^{[W]}\le T(W)\).  Thus an argument that derives (7.1) only by
rewriting the next endpoint is circular.  A valid proof of \(G_2\ge V+1\)
must import an independent quantitative loss from rank \(3\) or higher.

No counterexample to (7.1) was found.  The first unclosed inference is not
the low-rank algebra; it is the absence of an all-carry lower bound on the
rank-four shadow loss in the exact gap recursion.

The zero-slack theorem bypasses this stronger target.  It does not require
the old \(G_2\) gap or the order-\(V^2\) rank-18 slack.

## 8. A triangular-slack lemma for the residual-jump route

There is a second rigorous conditional route on the separated rank-18/17
chart.  Write

\[
\begin{aligned}
z&=z_3(V),&
z'&=z_3(V+1),&
\Delta_+&=\max(0,z'-z),\\
y&=V+\operatorname{KK}_3(z),&
k&=\operatorname{KK}_2(y).
\end{aligned}
\]

### Lemma 8.1

If

\[
\boxed{1+3\Delta_+\le k,} \tag{8.1}
\]

then

\[
W(V+1)-W(V)\le1. \tag{8.2}
\]

### Proof

The one-set shadow increment bound gives

\[
\operatorname{KK}_3(z')-\operatorname{KK}_3(z)
\le3\Delta_+.
\]

Consequently

\[
y(V+1)\le y+1+3\Delta_+. \tag{8.3}
\]

Since \(k=\operatorname{KK}_2(y)\), Galois adjunction gives

\[
y\le U_1(k)=\binom{k}{2}.
\]

Equations (8.1)--(8.3) imply

\[
y(V+1)
\le\binom{k}{2}+k
=\binom{k+1}{2}
=U_1(k+1).
\]

A second use of adjunction yields

\[
\operatorname{KK}_2(y(V+1))\le k+1.
\]

On the separated chart \(W=27+\operatorname{KK}_2(y)\), proving
(8.2). \(\square\)

This lemma isolates a genuinely sufficient jump bound.  Moreover \(y\ge V\)
and \(y\le\binom{k}{2}\), so

\[
k\ge
\min\left\{m:\binom m2\ge V\right\}
=\left\lceil\frac{1+\sqrt{1+8V}}2\right\rceil. \tag{8.4}
\]

Thus any all-parameter estimate

\[
z_3(V+1)-z_3(V)=O(\log V)
\]

would make (8.1) automatic for sufficiently large \(V\), after which an
exact finite bridge would close the Lipschitz route.

This attack does not prove such a jump estimate.  Adjacent suspension gives
only a qualitative domination after the large rank-18 shadow loss is
discarded; extracting an \(O(\log V)\), or even \(o(\sqrt V)\), jump bound
again requires a carry-independent quantitative potential.  The observed
fact that a residual jump can exceed \(2\) also rules out the simplest
constant-two conjecture; no finite observation is used as a theorem.

## 9. Exact guard

Run:

```bash
cd data/research_open/q1_three_hour_campaign_2026-07-31/erdos776
python3 verify_zero_slack_gate.py
```

Result:

```text
status: PASS
analytic base: V = 288
finite bridge: 40 <= V <= 287
minimum finite rank-8 margin: 260272
rank-16 majorizer: V + KK_15(V) <= 16V
open premise: D18 <= P18 for every V >= 288
```

The guard checks the coefficient table and all base separations, the exact
finite bridge, the rank-18-to-rank-16 majorizer at strategic parameters,
and the final \(G_2\) endpoint identity.  Selected evaluations of
\(P_{18}-D_{18}\) are explicitly labelled falsifier evidence only.

## 10. First unclosed step and second-round recommendation

The strongest closed result is the zero-slack gate (1.1)--(1.2).  The first
unclosed statement is now

\[
\boxed{D_{18}\le P_{18}\quad(V\ge288),}
\]

or equivalently the one-binomial complement bound (6.4).

The recommended second attack is:

1. work with the one-binomial start \(C_R=\binom{V-13}{R}\);
2. seek a carry-independent supersolution for (6.2) proving
   \(C_2\le T(V)\);
3. use the first hypothetical violation of \(C_2\le T\), rather than
   following the complete canonical word;
4. retain \(G_2\) only as a secondary route unless an independent
   rank-four loss lower bound is found;
5. in parallel, try to prove the weaker jump estimate
   \(z_3(V+1)-z_3(V)=o(\sqrt V)\), which is already enough by Lemma 8.1.

Proving the zero-slack comparison would close the inherited
\(n_0(r)\le2r+5\) construction after the already verified finite bridge.
