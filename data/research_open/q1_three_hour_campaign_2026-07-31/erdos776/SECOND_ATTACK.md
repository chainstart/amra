# Erdős #776: second attack — global complement audit and a weak entry gate

Date: 2026-07-31

## 1. Outcome

This attack does **not** prove

\[
D_{18}\le P_{18}
\qquad(V\ge288),
\]

and it finds no counterexample in the exact falsifier runs.  It does make
three rigorous advances.

1. The one-binomial complementary formulation from `FIRST_ATTACK.md` is
   globally valid.  Its proof can be written entirely with Galois
   adjunctions and an early-stop convention; it does not assume that one
   fixed canonical chart survives all re-normalizations.
2. A second tail complement turns the open rank-18 comparison into an
   exact fixed-rank-five capacity comparison.  Put \(N=V-25\), and define
   \[
   E_{N-1}=0,\qquad E_{q-1}=V+\operatorname{KK}_q(E_q).
   \]
   Then
   \[
   \boxed{D_{18}\le P_{18}
   \iff E_5\le\binom N5.} \tag{1.1}
   \]
   On the successful side, the two slacks are equal.
3. A carry-independent subadditive majorizer proves that it is enough to
   show that the **first** entry into the old 14-term moving block occurs
   at residual rank at most \(28\).  More generally, a purely analytic
   version only needs the much weaker factorial scale
   \[
   s\lesssim 2\frac{\log V}{\log\log V}.
   \]
   A precise, non-asymptotic version is proved below.  This is
   substantially weaker than the old \(s=O(\log\log V)\) hypothesis that
   was used to control the rank-16 residual.

The first unclosed inference is now one of the following equivalent
all-parameter statements:

\[
D_{18}\le P_{18},\qquad
C_2\le T(V),\qquad
E_5\le\binom{V-25}{5}.
\]

The strongest remaining target exposed here is therefore

\[
\boxed{\text{first moving-block entry }s(V)\le28}
\]

(with the no-entry-through-rank-18 case already harmless).  No all-\(V\)
proof of this entry bound is currently known.

## 2. Global audit of the one-binomial complement

Put

\[
n=V-11,\qquad m=n-2=V-13,\qquad R=V-29,
\]

and

\[
P_q=\binom{V-12}{q}+\binom{V-13}{q-1}.
\]

Pascal cancellation gives

\[
\binom n{18}-P_{18}
=\binom mR. \tag{2.1}
\]

Start the independent complementary descent at

\[
C_R=\binom mR,\qquad
C_{r-1}=\operatorname{KK}_r(C_r+V)
\quad(r=R,\ldots,3), \tag{2.2}
\]

and put

\[
T(V)=\binom n2-V. \tag{2.3}
\]

### Proposition 2.1

For every parameter for which the shortened orbit is defined,

\[
\boxed{D_{18}\le P_{18}\iff C_2\le T(V).} \tag{2.4}
\]

This equivalence is global; no separated moving-block chart is an
assumption.

### Proof

For a nonnegative threshold \(y\), Galois adjunction gives

\[
\operatorname{KK}_r(x+V)\le y
\iff
x\le U_{r-1}(y)-V. \tag{2.5}
\]

If the expression on the right is negative, the left inequality is
impossible for \(x\ge0\).  Thus (2.5) remains exact if a negative
right-adjoint value is treated as an immediate failed capacity, rather
than being formally propagated.

At rank \(q=n-r\), let

\[
A_r=\binom nq-D_q.
\]

At \(q=n-2=V-13\), one has \(D_q=V\), and hence

\[
A_2=T(V).
\]

As long as \(A_r\ge0\), the standard tail-complement identity is

\[
A_{r+1}=U_r(A_r)-V. \tag{2.6}
\]

If an \(A_r\) first becomes negative, then \(D_q>\binom nq\).
Monotonicity shows that this failure cannot recover at a lower rank:
the next defect is at least
\[
V+\operatorname{KK}_q\!\left(\binom nq+1\right)
>\binom n{q-1}.
\]
In particular it cannot later lie below \(P_{18}<\binom n{18}\).

Iterating (2.5), with this early-stop convention, gives

\[
C_2\le A_2\iff C_R\le A_R. \tag{2.7}
\]

At rank 18, equations (2.1) and (2.7) say

\[
\binom n{18}-P_{18}
\le
\binom n{18}-D_{18},
\]

which is exactly \(D_{18}\le P_{18}\). \(\square\)

This proof explains why the recurrence in (2.2) must be
\(\operatorname{KK}_r(C_r+V)\).  Replacing it by
\(V+\operatorname{KK}_r(C_r)\) would describe a different orbit.

## 3. A second complement and a fixed-rank-five target

The first complement also admits a useful second normalization, but it
must be stopped at the first failed capacity rather than continued
formally through a negative residual.

While \(D_q\le P_q\), write

\[
A_r=\binom mr+u_r.
\]

At \(r=2\),

\[
u_2=V-25.
\]

The upper separation is automatic up to the first failure, and (2.6)
gives

\[
u_{r+1}=U_{r-1}(u_r)-V. \tag{3.1}
\]

Set

\[
N=V-25,\qquad c_k=u_{k+1}.
\]

Then \(c_1=N\) and

\[
c_{k+1}=U_k(c_k)-V. \tag{3.2}
\]

There is no hidden upper carry in this normalization.  At \(k=1\),
\(c_1=\binom N1\).  If
\[
0\le c_k\le\binom Nk,
\]
then \(N<m\) makes \(c_k<\binom mk\), which is exactly the separation
needed above the \(\binom mr\) baseline.  Moreover
\[
U_k(c_k)\le\binom N{k+1},
\]
so either the next \(c_{k+1}\) is negative, which is the explicit
early-stop event, or it again lies strictly below its next capacity.

Complement once more inside \(\binom Nk\):

\[
E_{N-k}=\binom Nk-c_k.
\]

The exact tail-complement identity converts (3.2) into

\[
E_{N-1}=0,\qquad
E_{q-1}=V+\operatorname{KK}_q(E_q). \tag{3.3}
\]

At the final aligned rank, \(k=N-5\), symmetry gives
\(\binom Nk=\binom N5\).  If either comparison first fails, monotonicity
keeps it failed at every subsequent rank.  Therefore the early-stop
argument used in Proposition 2.1 proves the global sign equivalence

\[
D_{18}\le P_{18}
\iff
E_5\le\binom N5, \tag{3.4}
\]

which is (1.1).  Moreover, on this successful chart,

\[
\boxed{
P_{18}-D_{18}
=\binom N5-E_5.
} \tag{3.5}
\]

Equation (3.4) is a genuine fixed-rank reduction, but not yet a proof:
the new orbit has additive tax \(V=N+25\), and no carry-independent
rank-five capacity barrier is currently known.

## 4. The moving-block identity

For \(s\ge3\), put \(q=s+15\) and recall

\[
H_{s+15}
=\binom{V-12}{s+15}
+ \sum_{j=1}^{14}\binom{V-28+j}{s+j}. \tag{4.1}
\]

The hockey-stick identity gives

\[
\sum_{j=1}^{14}\binom{V-28+j}{s+j}
=\binom{V-13}{s+14}-\binom{V-27}{s}.
\]

Consequently

\[
\boxed{
P_{s+15}-H_{s+15}=\binom{V-27}{s}.
} \tag{4.2}
\]

In particular, at rank 18,

\[
P_{18}-H_{18}=\binom{V-27}{3}. \tag{4.3}
\]

Suppose \(q=s+15\) is the first rank in the downward orbit at which

\[
D_q\ge H_q,
\]

and write \(D_q=H_q+Z_s\).  Since
\(\operatorname{KK}_{q+1}(H_{q+1})=H_q\), first entry gives

\[
\boxed{0\le Z_s\le V.} \tag{4.4}
\]

This uses only monotonicity at the first crossing; it does not identify
this event with the earlier Round12 first carry.

## 5. A factorial-scale first-entry theorem

Define

\[
B_s=1,\qquad B_{r-1}=1+rB_r
\quad(r=s,\ldots,4). \tag{5.1}
\]

### Theorem 5.1

Let \(V\ge288\), and suppose either:

1. the orbit has not entered the block (4.1) by rank 18; or
2. its first entry has residual rank \(s\) satisfying
   \[
   s\le\frac{V-27}{2} \tag{5.2}
   \]
   and
   \[
   \boxed{
   \frac{V(s+1)!}{24}
   <\binom{V-27}{3}.
   } \tag{5.3}
   \]

Then

\[
\boxed{D_{18}<P_{18}.} \tag{5.4}
\]

### Proof

In the no-entry case, \(D_{18}<H_{18}<P_{18}\).

In the entry case, (4.4) gives \(Z_s\le B_sV\).  Before a first putative
collision with the bottom of the moving block,

\[
Z_{r-1}=V+\operatorname{KK}_r(Z_r)
\le V+rZ_r. \tag{5.5}
\]

It follows inductively that

\[
Z_r\le B_rV. \tag{5.6}
\]

The coefficients in (5.1) satisfy

\[
B_r\le\frac{(s+1)!}{(r+1)!}. \tag{5.7}
\]

Indeed, equality holds at \(r=s\), and
\[
1+r\frac{(s+1)!}{(r+1)!}
\le\frac{(s+1)!}{r!}
\]
because \((s+1)!/(r+1)!\ge1\).

The sequence \(B_r\) decreases as \(r\) increases, while
\(\binom{V-27}{r}\) is nondecreasing for
\(3\le r\le s\) under (5.2).  Hence (5.3), (5.6), and (5.7) imply

\[
Z_r
\le B_rV
\le B_3V
<\binom{V-27}{3}
\le\binom{V-27}{r}
\qquad(3\le r\le s). \tag{5.8}
\]

Thus the putative first collision cannot occur.  The separated recurrence
(5.5) is valid all the way to \(r=3\), and

\[
D_{18}=H_{18}+Z_3
<H_{18}+\binom{V-27}{3}
=P_{18}.
\]
\(\square\)

### Corollary 5.2

For every fixed \(\varepsilon>0\), the estimate

\[
s(V)\le
(2-\varepsilon)\frac{\log V}{\log\log V}
\tag{5.9}
\]

for all sufficiently large \(V\) implies the open zero-slack premise for
all sufficiently large \(V\).  An exact finite bridge would then finish
the inherited construction.

This follows from Stirling's formula:
\(\log((s+1)!)\le(2-\varepsilon/2)\log V\) eventually, whereas the
right side of (5.3), after division by \(V\), has logarithm
\((2+o(1))\log V\).

The constant \(2\) in this asymptotic statement is a threshold scale, not
an achieved all-\(V\) entry estimate.  In particular, the inherited
first-carry \(O(\log\log V)\) theorem cannot simply be substituted for
\(s(V)\): these are different events, as already audited in
`LIPSCHITZ_ATTACK.md`.

## 6. A carry-independent rank-28 entry gate

The factorial estimate deliberately uses the crude bound
\(\operatorname{KK}_r(x)\le rx\).  Subadditivity gives a much stronger
finite-depth majorizer.

### Lemma 6.1

For \(r\ge2\) and nonnegative integers \(x,y\),

\[
\operatorname{KK}_r(x+y)
\le\operatorname{KK}_r(x)+\operatorname{KK}_r(y). \tag{6.1}
\]

Indeed, take shadow-minimizing \(r\)-uniform families of sizes \(x\) and
\(y\) on disjoint ground sets.  Their union has size \(x+y\), and its
two lower shadows are disjoint.

Set \(V_0=288\), and define rational constants downwards by

\[
K_{28}=1,\qquad
M_r=\left\lceil V_0K_r\right\rceil,\qquad
K_{r-1}=1+\frac{2\operatorname{KK}_r(M_r)}{V_0}.
\tag{6.2}
\]

All quantities in (6.2) are exact integers or rationals.  Some landmarks
in the resulting certificate are

\[
\begin{array}{c|rrrrrr}
r&28&27&20&10&4&3\\
\hline
K_r&
1&
3469/144&
22992256/3&
4481446639/72&
729341/48&
58691/48.
\end{array} \tag{6.3}
\]

The exact 26-row certificate verifies

\[
\left\lceil288K_r\right\rceil
<\binom{261}{r}
\qquad(3\le r\le28). \tag{6.4}
\]

The smallest margin in (6.4) is at \(r=3\):

\[
\binom{261}{3}-288K_3
=2{,}577{,}144. \tag{6.5}
\]

### Theorem 6.2

Let \(V\ge288\).  If there is no moving-block entry by rank 18, or if its
first entry has residual rank

\[
\boxed{s\le28,} \tag{6.6}
\]

then

\[
\boxed{D_{18}<P_{18}.} \tag{6.7}
\]

### Proof

Only the entry case needs consideration.  Since every \(K_r\ge1\),
(4.4) gives \(Z_s\le K_sV\).

Suppose inductively, before a first putative collision, that
\(Z_r\le K_rV\).  Put

\[
\mu=\left\lceil\frac{V}{V_0}\right\rceil.
\]

The definition of \(M_r\) gives \(Z_r\le\mu M_r\).  Monotonicity,
subadditivity, and \(V\ge V_0\) give

\[
\begin{aligned}
\operatorname{KK}_r(Z_r)
&\le \mu\operatorname{KK}_r(M_r)\\
&\le \frac{2V}{V_0}\operatorname{KK}_r(M_r).
\end{aligned}
\]

Thus

\[
Z_{r-1}
\le
\left(
1+\frac{2\operatorname{KK}_r(M_r)}{V_0}
\right)V
=K_{r-1}V. \tag{6.8}
\]

For fixed \(r\), the ratio

\[
\frac{\binom{V-27}{r}}{V}
\]

is strictly increasing in \(V\), since the cross-multiplied step
difference is

\[
(r-1)V+r+26>0.
\]

Equations (6.4) and (6.8) therefore imply

\[
Z_r\le K_rV<\binom{V-27}{r}
\qquad(3\le r\le s). \tag{6.9}
\]

This simultaneously validates every separated step and rules out the
putative collision.  At rank three, (4.3) and (6.9) give (6.7).
\(\square\)

Theorem 6.2 is stronger than the factorial gate in the range most relevant
to the observed orbit.  It uses finite exact arithmetic only to freeze
the 26 constants in a proved, parameter-uniform induction; it does not
scan the unbounded parameter \(V\).

### Corollary 6.3 (one fixed-rank target)

The remaining entry assertion has the exact fixed-rank form

\[
\boxed{
\text{first entry }s\le28\text{, or no entry through rank 18}
\iff
D_{44}<H_{44}.
} \tag{6.10}
\]

Indeed, once \(D_q\ge H_q\), the comparison cannot recover:

\[
D_{q-1}
=V+\operatorname{KK}_q(D_q)
\ge V+\operatorname{KK}_q(H_q)
=H_{q-1}+V.
\]

Thus \(D_{44}<H_{44}\) says exactly that no entry occurred at any
rank \(q\ge44\); every later possible entry has
\(s=q-15\le28\).

Combining Corollary 6.3 with Theorem 6.2 gives the particularly narrow
closing target

\[
\boxed{D_{44}<H_{44}\quad(V\ge288).} \tag{6.11}
\]

This is not proved here.  Exact values such as
\[
H_{44}-D_{44}
=25{,}058,\ 50{,}261,\ 443{,}336
\]
at \(V=288,379,1000\), respectively, are falsifier evidence only.

## 7. A sharp obstruction to a stronger endpoint supersolution

The one-binomial endpoint has essentially no spare integer room.
Independent exact arithmetic gives

\[
C_2=T(V)-1
\]

at each of

\[
V=70,100,175,288,379,1000.
\]

For example, at \(V=288\),

\[
T(288)=37938,\qquad C_2=37937.
\]

Therefore the tempting uniform strengthening

\[
C_2\le T(V)-2
\]

is **false**, already at an explicit parameter inside the analytic range.
This is not a finite extrapolation: one exact parameter is a counterexample
to that stronger universal claim.

At the same parameter, the high-rank slack is

\[
P_{18}-D_{18}=2{,}924{,}809.
\]

Thus the complementary descent compresses a large rank-18 slack to a
one-unit endpoint slack.  Any carry-independent supersolution must be
sharp enough to allow this terminal plateau; a proof demanding two units
of endpoint room cannot succeed.

## 8. Exact guard and remaining target

Run:

```bash
cd data/research_open/q1_three_hour_campaign_2026-07-31/erdos776
python3 verify_zero_slack_gate.py
```

The extended guard checks:

- the global one-binomial endpoint at selected falsifier parameters;
- the identity \(P_{s+15}-H_{s+15}=\binom{V-27}{s}\);
- first-entry excesses and their \(0\le Z_s\le V\) bound;
- the coefficient recursion and synthetic instances of Theorem 5.1;
- all 26 rational constants and base separations in Theorem 6.2;
- the fixed-rank-five sign equivalence, including failed small parameters;
- the exact counterexample to \(C_2\le T-2\).

All finite rows are labelled either exact certificate components or
regression/falsifier evidence.  The proved unbounded content is
Theorems 5.1 and 6.2 together with the two adjunction equivalences.

The next legitimate attack is narrowly defined:

1. prove the first moving-block entry bound \(s(V)\le28\), without
   identifying it with the Round12 first carry — equivalently, prove the
   fixed-rank inequality \(D_{44}<H_{44}\); or
2. prove the equivalent fixed-rank-five capacity
   \(E_5\le\binom{V-25}{5}\) using a potential that survives every carry.

Neither statement is established here, so Erdős #776 remains open.
