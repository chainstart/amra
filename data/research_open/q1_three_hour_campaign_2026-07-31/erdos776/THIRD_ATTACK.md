# Erdős #776: third attack — the rank-44 gate and its late tail

Date: 2026-07-31

## 1. Outcome

This attack does **not** prove

\[
D_{44}<H_{44}\qquad(V\ge288),
\]

and therefore does not close Erdős #776.  It does reduce the target in
three exact ways and sharply audits two tempting proof routes.

1. The Galois complement of \(H_{44}-1\) has the explicit
   two-binomial-plus-one start
   \[
   \binom{V-13}{V-55}
   +\binom{V-27}{V-56}+1.
   \]
   Its endpoint comparison is again the same rank-two capacity
   \(\binom{V-11}{2}-V\).  This is a global equivalence with the usual
   early-stop convention, not a fixed-chart heuristic.
2. Complementing a second time gives a new fixed-rank formulation.  Put
   \(N=V-25\) and
   \[
   E_{N-1}=0,\qquad
   E_{q-1}=V+\operatorname{KK}_q(E_q).
   \]
   Then
   \[
   \boxed{
   D_{44}<H_{44}
   \iff
   E_{31}<
   \binom{N-1}{31}+\binom{N-2}{30}.
   } \tag{1.1}
   \]
   On the successful side the two strict slacks are equal.
3. There is an exact algebraic late-tail normalization
   \[
   H_{44}-D_{44}
   =\binom{V-55}{2}-R_2(V),
   \]
   where \(R_2=D_{44}-J_{44}\) and \(J_{44}\) is an explicit 42-term
   binomial block.  Thus the genuinely quantitative next target is
   \(R_2(V)\le7V\).  That bound would close the gate for every
   \(V\ge288\).  The nearest smaller integer-linear proposal
   \(R_2\le6V\) is false: at \(V=288\),
   \[
   R_2=1970>1728=6V.
   \]

The observed rank-44 canonical template is extremely stable, but proving
that it is a legal canonical prefix already forces
\(R_2<\binom{V-55}{2}\) and hence proves the desired gate.  It cannot be
used as an unproved premise before bounding \(R_2\).

Two remaining single-lemma targets are therefore

\[
\boxed{R_2(V)\le7V\quad(V\ge288)}
\tag{1.2}
\]

or the adjacent diagonal inequality

\[
\boxed{
D^{[V+1]}_{44}-D^{[V]}_{44}\le H_{43}(V)
\quad(V\ge288).
} \tag{1.3}
\]

Neither is proved here.

## 2. Frozen definitions and quantifiers

For every integer \(V\), the shortened orbit is

\[
D_{V-12}=0,\qquad
D_{q-1}=V+\operatorname{KK}_q(D_q).
\tag{2.1}
\]

At residual rank \(s=29\), the moving block from `SECOND_ATTACK.md` is

\[
\begin{aligned}
H_{44}
&=\binom{V-12}{44}
  +\sum_{j=1}^{14}\binom{V-28+j}{29+j}\\
&=\binom{V-12}{44}
  +\sum_{i=30}^{43}\binom{V-57+i}{i}.
\end{aligned}
\tag{2.2}
\]

The first-entry theorem proved in the second attack gives

\[
D_{44}<H_{44}
\iff
\text{no moving-block entry at any rank }q\ge44.
\tag{2.3}
\]

Thus (2.3), followed by the proved rank-28 subadditive gate, would imply
\(D_{18}<P_{18}\), the rank-eight entry condition, and the inherited
construction.  Because the target is strict and integer-valued, its exact
form for Galois inversion is

\[
D_{44}\le H_{44}-1.
\tag{2.4}
\]

## 3. The exact two-binomial complement

Put

\[
n=V-11,\qquad R=n-44=V-55,
\qquad T(V)=\binom n2-V.
\tag{3.1}
\]

Recall

\[
P_{44}
=\binom{V-12}{44}+\binom{V-13}{43},
\qquad
P_{44}-H_{44}=\binom{V-27}{29}.
\tag{3.2}
\]

Two Pascal cancellations give

\[
\binom n{44}-P_{44}
=\binom{V-13}{R}.
\tag{3.3}
\]

Since \(\binom{V-27}{29}=\binom{V-27}{R-1}\), equations
(3.2)--(3.3) yield the exact missing-size identity

\[
\boxed{
\binom n{44}-(H_{44}-1)
=\binom{V-13}{R}
+\binom{V-27}{R-1}+1.
} \tag{3.4}
\]

Start the independent descent

\[
\begin{aligned}
C_R&=\binom{V-13}{R}
 +\binom{V-27}{R-1}+1,\\
C_{r-1}&=\operatorname{KK}_r(C_r+V)
\qquad(r=R,\ldots,3).
\end{aligned}
\tag{3.5}
\]

### Proposition 3.1

For every parameter for which (2.1) is defined,

\[
\boxed{
D_{44}<H_{44}
\iff C_2\le T(V).
} \tag{3.6}
\]

### Proof

At rank \(q=n-r\), set

\[
A_r=\binom nq-D_q.
\]

At \(r=2\), equation (2.1) gives \(D_{n-2}=V\), and hence
\(A_2=T(V)\).  As long as the capacity is nonnegative, the tail-complement
identity is

\[
A_{r+1}=U_r(A_r)-V.
\tag{3.7}
\]

Galois adjunction gives

\[
\operatorname{KK}_r(x+V)\le y
\iff x\le U_{r-1}(y)-V.
\tag{3.8}
\]

If the right side first becomes negative, the forward defect has exceeded
\(\binom nq\).  Monotonicity prevents such a failure from recovering at
a later lower rank.  Thus a negative right-adjoint value is an exact
early-stop failure, rather than a quantity that may be propagated
formally.

Iterating (3.8) with this convention proves

\[
C_2\le A_2\iff C_R\le A_R.
\]

Using (3.4), the right inequality is precisely

\[
\binom n{44}-(H_{44}-1)
\le \binom n{44}-D_{44},
\]

which is (2.4). \(\square\)

The endpoint has no hidden spare unit.  At \(V=288\), exact arithmetic
gives

\[
C_2=T(288)=37938.
\tag{3.9}
\]

Consequently the tempting strengthening \(C_2\le T(V)-1\) is already
false at the analytic anchor, even though the desired rank-44 inequality
has margin \(25058\) there.  The Galois endpoint encodes a large
rank-44 slack in a single capacity-boundary event.

## 4. A second complement: the fixed rank 31 gate

The second complement from `SECOND_ATTACK.md` works at rank 44 as well as
at rank 18.  Its bookkeeping is included here to freeze every index.

Put

\[
m=V-13,\qquad N=V-25.
\tag{4.1}
\]

On the nonfailed branch write

\[
A_r=\binom mr+u_r.
\tag{4.2}
\]

At \(r=2\),

\[
u_2=V-25=N,
\]

and canonical separation gives

\[
u_{r+1}=U_{r-1}(u_r)-V.
\tag{4.3}
\]

Set \(c_k=u_{k+1}\), and complement inside \(\binom Nk\):

\[
E_{N-k}=\binom Nk-c_k.
\tag{4.4}
\]

The tail-complement identity turns (4.3) into the independent orbit

\[
\boxed{
E_{N-1}=0,\qquad
E_{q-1}=V+\operatorname{KK}_q(E_q).
} \tag{4.5}
\]

At rank 44 one has

\[
k=R-1=V-56=N-31.
\tag{4.6}
\]

By (3.4), the desired inequality is equivalent on the successful chart to

\[
c_k\ge\binom{N-2}{k}+1
=\binom{N-2}{29}+1.
\tag{4.7}
\]

Using (4.4), Pascal's identity twice gives

\[
\begin{aligned}
E_{31}
&\le \binom N{31}-\binom{N-2}{29}-1\\
&=\binom{N-1}{31}+\binom{N-2}{30}-1.
\end{aligned}
\tag{4.8}
\]

This proves (1.1) on the separated branch.  The equivalence is global:
if (4.2) first fails, its complement \(E_q\) exceeds
\(\binom Nq\); the added positive tax in (4.5) prevents recovery below
that capacity.  Since the right side of (4.8) is strictly below
\(\binom N{31}\), a failed branch cannot spuriously satisfy (4.8).
The same early-stop argument applies on the \(D\)-side because
\(H_{44}<P_{44}\).

Moreover, whenever the equivalent inequalities hold,

\[
\boxed{
H_{44}-D_{44}
=
\left[
\binom{N-1}{31}+\binom{N-2}{30}
\right]-E_{31}.
} \tag{4.9}
\]

Thus the rank-44 problem is exactly a zero-slack rank-31 capacity problem
for a zero-seed orbit with inflated tax \(V=N+25\).  This is not yet a
solution: no carry-independent potential for (4.5) at rank 31 is known.

## 5. The algebraic late tail

Define the explicit block

\[
\begin{aligned}
J_{44}(V)
={}&\binom{V-12}{44}
 +\sum_{i=31}^{43}\binom{V-57+i}{i}\\
&+\sum_{i=3}^{30}\binom{V-58+i}{i}.
\end{aligned}
\tag{5.1}
\]

The common terms in (2.2) and (5.1) cancel.  Hockey-stick summation gives

\[
\begin{aligned}
H_{44}-J_{44}
&=\binom{V-27}{30}
 -\sum_{i=3}^{30}\binom{V-58+i}{i}\\
&=\sum_{i=0}^{2}\binom{V-58+i}{i}\\
&=\boxed{\binom{V-55}{2}}.
\end{aligned}
\tag{5.2}
\]

Now define an **algebraic** tail, without assuming a canonical chart,

\[
R_2(V)=D_{44}-J_{44}(V).
\tag{5.3}
\]

Equations (5.2)--(5.3) prove the unconditional identity

\[
\boxed{
H_{44}-D_{44}
=\binom{V-55}{2}-R_2(V).
} \tag{5.4}
\]

Consequently

\[
\boxed{
D_{44}<H_{44}
\iff
R_2(V)<\binom{V-55}{2}.
} \tag{5.5}
\]

### Proposition 5.1 (linear late-tail gate)

If

\[
R_2(V)\le7V,
\tag{5.6}
\]

then \(D_{44}<H_{44}\) for every \(V\ge92\), in particular for every
\(V\ge288\).

Indeed,

\[
\binom{V-55}{2}-7V
=\frac{V^2-125V+3080}{2}>0
\qquad(V\ge92).
\tag{5.7}
\]

More generally, any all-parameter estimate \(R_2(V)=o(V^2)\) closes the
rank-44 gate for all sufficiently large \(V\), after which only an exact
finite bridge remains.  This is a genuine unbounded-parameter conditional
theorem, but (5.6) and the \(o(V^2)\) premise are open for the actual
orbit.

### Canonical-template loop warning

Selected exact expansions have the form

\[
\begin{aligned}
D_{44}
={}&\binom{V-12}{44}
 +\sum_{i=31}^{43}\binom{V-57+i}{i}\\
&+\sum_{i=3}^{30}\binom{V-58+i}{i}
 +\operatorname{Can}_2(R_2).
\end{aligned}
\tag{5.8}
\]

If (5.8) is asserted as a **legal canonical expansion**, its lowest fixed
term is \(\binom{V-55}{3}\), and legality already forces every residual
top index below \(V-55\).  Hence

\[
R_2<\binom{V-55}{2},
\]

which is exactly (5.5).  Therefore a proof of the stable template is a
proof of the target; it cannot be silently treated as a preliminary
normal form and followed by a separate easy tail estimate.

The useful noncircular formulation is instead (5.3): prove the numerical
upper barrier \(D_{44}\le J_{44}+7V\) directly, across every borrow chart.

## 6. The closest failed integer-linear barrier

At \(V=288\), independent exact arithmetic gives

\[
\begin{aligned}
R_2(288)
&=\binom{63}{2}+\binom{17}{1}\\
&=1970.
\end{aligned}
\tag{6.1}
\]

Therefore

\[
R_2(288)>6V=1728,
\tag{6.2}
\]

so the proposed uniform supersolution

\[
D_{44}\le J_{44}+6V
\tag{6.3}
\]

is rigorously false.

The reverse zero-basin test makes the failure structural.  Start at
\(b_{44}=J_{44}+6V\) and iterate

\[
b_{q+1}=U_q(b_q-V).
\tag{6.4}
\]

For \(V=288\), the orbit reaches

\[
b_{275}=287<V,
\tag{6.5}
\]

so the next subtraction is illegal.  This is an exact certificate that
\(J_{44}+6V\) lies below the zero basin, not merely a comparison of two
large decimal expansions.

At the same anchor,

\[
R_2(288)=1970\le2016=7V,
\]

and the reverse orbit from \(J_{44}+7V\) is legal and ends at
\(b_{276}=0\).  Thus coefficient \(7\) is the smallest integer coefficient
surviving the anchor.  Its success at one parameter is only a falsifier
check; (5.6) remains open for unbounded \(V\).

Selected exact rows are:

\[
\begin{array}{r|r|r|r}
V&R_2(V)&\binom{V-55}{2}-R_2&H_{44}-D_{44}\\
\hline
288&1970&25058&25058\\
379&2065&50261&50261\\
1000&2704&443336&443336\\
6329&8234&19670167&19670167\\
10000&12035&49434505&49434505
\end{array}
\tag{6.6}
\]

These rows explain why a linear late-tail theorem is plausible.  They do
not prove it.

## 7. An exact adjacent target

Let

\[
F(V)=H_{44}(V)-D^{[V]}_{44}.
\tag{7.1}
\]

Termwise Pascal identities in (2.2) give

\[
H_{44}(V+1)-H_{44}(V)=H_{43}(V).
\tag{7.2}
\]

Consequently

\[
\boxed{
F(V+1)-F(V)
=H_{43}(V)
-\left(D^{[V+1]}_{44}-D^{[V]}_{44}\right).
} \tag{7.3}
\]

Since \(F(288)=25058\), the diagonal inequality (1.3) would make
\(F\) nondecreasing and prove \(D_{44}<H_{44}\) for every \(V\ge288\).
It is logically independent of assuming the stable template.

Finite exact arithmetic finds (7.3) positive throughout
\(288\le V\le500\), with increments

\[
231,\ 323,\ 444
\]

at \(V=288,379,500\), respectively.  This is a finite falsifier window
only.

Even the observed almost-linear increment needs a sharp constant.  The
stronger proposal

\[
F(V+1)-F(V)\ge V-57
\tag{7.4}
\]

is false at the exact point \(V=1361\):

\[
F(1362)-F(1361)=1303=1361-58.
\tag{7.5}
\]

Thus a proof should target nonnegativity in (7.3), not extrapolate an
overly sharp affine margin from selected rows.

## 8. Why direct subadditivity still misses the target

There is a strict version of the subadditivity lemma used in the second
attack.

### Lemma 8.1

For \(q\ge2\) and positive integers \(x,y\),

\[
\boxed{
\operatorname{KK}_q(x+y)
\le
\operatorname{KK}_q(x)+\operatorname{KK}_q(y)-1.
} \tag{8.1}
\]

### Proof

Take shadow-minimizing \(q\)-uniform families of sizes \(x\) and \(y\).
Relabel their ground sets so that one selected set from each family shares
the same \(q-1\) vertices, while all remaining vertices of the two ground
sets are disjoint.  The two \(q\)-families remain disjoint, but their lower
shadows share at least that common \((q-1)\)-set.  Their union is therefore
a \(q\)-family of size \(x+y\) whose shadow has size at most the right side
of (8.1). \(\square\)

Let

\[
\delta_q=D^{[V+1]}_q-D^{[V]}_q.
\]

After aligning the two orbits,

\[
\delta_{V-12}=V+1,
\]

and at the next rank

\[
\delta_{V-13}
=1+\operatorname{KK}_{V-12}(V+1).
\tag{8.2}
\]

Below this rank both summands are positive, and (8.1) gives the direct
majorizer

\[
\delta_{q-1}\le\operatorname{KK}_q(\delta_q).
\tag{8.3}
\]

This is the strongest bound obtained by charging only the guaranteed
one-unit overlap at every step.  It is nevertheless enormously too weak.
At \(V=288\), iterating (8.3) to rank 44 gives

\[
3{,}475{,}140{,}719{,}231{,}442{,}109{,}223{,}817{,}014{,}
401{,}697{,}283{,}918{,}257{,}441{,}646{,}960,
\]

whereas \(H_{43}(288)\) is

\[
550{,}556{,}177{,}877{,}110{,}467{,}877{,}294{,}714{,}559{,}
268{,}138{,}527{,}272{,}984{,}643{,}600.
\]

The exact overshoot is

\[
2{,}924{,}584{,}541{,}354{,}331{,}641{,}346{,}522{,}299{,}
842{,}429{,}145{,}390{,}984{,}457{,}003{,}360.
\tag{8.4}
\]

Thus even strict subadditivity loses the overlap geometry carried by the
stable high prefix.  Any successful proof of (1.2) or (1.3) must use a
late-tail/capped invariant that survives borrow transitions; decomposing
all taxes or adjacent increments independently cannot be sharp enough.

## 9. Honest status and next action

The strongest proved statements from this attack are:

1. the global Galois equivalence (3.6);
2. the fixed-rank-31 equivalence (1.1) and slack identity (4.9);
3. the exact late-tail identity (5.4);
4. the all-\(V\) conditional linear gate, Proposition 5.1;
5. the exact adjacent reduction (7.3);
6. strict subadditivity (8.1), together with the quantitative no-go
   (8.4);
7. the explicit counterexamples to \(C_2\le T-1\),
   \(R_2\le6V\), and the affine increment bound (7.4).

The first unproved inference remains

\[
D_{44}<H_{44}\qquad(V\ge288).
\]

The next useful attack should build one of the following, with borrow
states included in the induction hypothesis:

1. a capped late-tail potential proving \(R_2\le7V\);
2. a diagonal overlap potential proving (1.3); or
3. a fixed-rank-31 capacity potential for the inflated-tax orbit (4.5).

Until one of these is proved for every parameter, Erdős #776 remains
**OPEN**.

## 10. Reproduction

Run

```bash
python3 \
  data/research_open/q1_three_hour_campaign_2026-07-31/erdos776/verify_rank44_third_attack.py
```

The script independently implements ordinary greedy Macaulay arithmetic,
crosses both truth values of the two global equivalences, verifies the
symbolic identities, checks the explicit failed supersolutions, and uses
the run-compressed engine only for clearly labelled finite falsifier rows.
It prints `"status": "PASS"`.
