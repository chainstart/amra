# Multi-promotion no-borrow atlas and a multi-cap transport inequality

Frozen finite census: 2026-08-02 20:35 HKT.

This note attacks the part of the relaxed no-borrow lattice not covered by
the earlier one-promotion chart.  It deliberately separates exact identities
and proved inequalities from finite evidence.  In particular, the census
below is **not** an unbounded proof.

## 1. Exact promotion coordinates

Write the two rank-two canonical inputs as

\[
 n=\binom q2+r,\qquad
 n+b-1=\binom{q+c}{2}+u,
 \qquad 0\le r<q,\quad 0\le u<q+c.
\tag{1.1}
\]

Here \(c\ge0\) is the exact number of leading-index promotions.  Subtracting
the two equations gives the exact lattice parametrization

\[
 \boxed{b=cq+\binom c2+u-r+1.}
\tag{1.2}
\]

Conversely, every integral tuple satisfying (1.1)--(1.2),

\[
 2h=\binom{b-1}{2}+2-n,
\tag{1.3}
\]

and the parity and range conditions is a point of the relaxed lattice.  The
two shadows have independent closed forms

\[
 z=U_2(n)=\binom q3+\binom r2,
 \qquad
 w=U_2(n+b-1)=\binom{q+c}{3}+\binom u2.
\tag{1.4}
\]

Thus (c) is a finite type label in precisely the sense used in the
`CompactnessAndDegeneracy` witness compression: no geometric information is
discarded, but the first branching variable has been isolated.

Put

\[
 H=\binom b2+1,\quad \tau=H-n,\quad
 \gamma_3=w-z-H,\quad
 x=n+z-H+1,\quad y=n+z+\gamma_3.
\tag{1.5}
\]

At a no-borrow point \(x\ge0\), the next comparison is

\[
 \gamma_4=U_3(y)-U_3(x)-x-\tau.
\tag{1.6}
\]

The cancellation

\[
 \boxed{x+\tau=z+1}
\tag{1.7}
\]

turns this into the tax-free comparator

\[
 \boxed{\gamma_4=U_3(y)-U_3(x)-z-1.}
\tag{1.8}
\]

Equations (1.2), (1.4), and (1.8) are exact and unbounded.

## 2. Exact rank-three remainder comparator

Normalize the two positive low blocks as

\[
 x=\binom a3+\alpha,\qquad
 y=\binom t3+\beta,\qquad
 0\le\alpha<\binom a2,\qquad
 0\le\beta<\binom t2.
\tag{2.1}
\]

Canonical concatenation and (1.8) give the exact formula

\[
 \boxed{
 \gamma_4=
 \binom t4-\binom a4
 +U_2(\beta)-U_2(\alpha)-z-1.}
\tag{2.2}
\]

For example, when \(\beta\ge\alpha\), superadditivity gives the rigorous
conditional lower bound

\[
 \gamma_4\ge
 \binom t4-\binom a4+U_2(\beta-\alpha)-z-1.
\tag{2.3}
\]

This is the comparator analogue of retaining the whole positive Gram
remainder in `MetricCodes`: the leading blocks alone are not a valid sign
certificate.

### 2.1 A second-level positive-remainder bound

Expand both remainders one canonical level further:

\[
 \alpha=\binom s2+\rho,\qquad
 \beta=\binom v2+\sigma,\qquad
 0\le\rho<s,\quad 0\le\sigma<v.
\tag{2.4}
\]

Substitution into (2.2) gives another exact, unbounded comparator:

\[
 \boxed{
 \gamma_4=
 \binom t4-\binom a4
 +\binom v3-\binom s3
 +\binom\sigma2-\binom\rho2-z-1.}
\tag{2.5}
\]

Since \(\rho<s\), retaining the positive \(\binom\sigma2\) term gives

\[
 \boxed{
 \gamma_4\ge
 \binom t4-\binom a4
 +\binom v3-\binom s3
 +\binom\sigma2-\binom{s-1}{2}-z-1.}
\tag{2.6}
\]

This elementary inequality is much sharper than applying superadditivity
only to \(\beta-\alpha\).  It is valid without a finite-range assumption.

There is also a dual exact form.  Put
\(\delta=\binom a2-\alpha\).  Definition (3.1) at rank two gives

\[
 \boxed{
 \gamma_4=
 \left(\binom t4-\binom a4-\binom a3\right)
 +U_2(\beta)+\Lambda_{2,a}(\delta)-z-1.}
\tag{2.7}
\]

The established bound \(\Lambda_{2,a}(\delta)\ge U_2(\delta)\) therefore
yields

\[
 \boxed{
 \gamma_4\ge
 \left(\binom t4-\binom a4-\binom a3\right)
 +U_2(\beta)+U_2(\delta)-z-1.}
\tag{2.8}
\]

Equations (2.5), (2.7), and inequalities (2.6), (2.8) are unbounded;
the counts reported below are only finite applications of them.

## 3. A proved multi-cap deficit transport lemma

For \(0\le d\le\binom Aj\), recall the full-block loss

\[
 \Lambda_{j,A}(d)
 =\binom A{j+1}-U_j\!\left(\binom Aj-d\right).
\tag{3.1}
\]

The proved one-cap inequalities are Lemma 2.1, equations (2.2)--(2.3), of
`data/research_open/q1_six_hour_campaign_2026-08-02/erdos776/LEADING_BLOCK_DEFICIT_THEOREM.md`:

\[
 \Lambda_{j,A}(D)-\Lambda_{j,A}(E)\ge U_j(D-E)
 \quad(D\ge E),
\tag{3.2}
\]

and

\[
 \Lambda_{j,A+1}(E)-\Lambda_{j,A}(E)\le E.
\tag{3.3}
\]

Iterating (3.3) before applying (3.2) gives the following new form.

**Lemma 3.1 (multi-cap transport).**  If
\(0\le E\le D\le\binom Aj\) and \(g\ge0\), then

\[
 \boxed{
 \Lambda_{j,A}(D)-\Lambda_{j,A+g}(E)
 \ge U_j(D-E)-gE.}
\tag{3.4}
\]

**Proof.**  Telescope the vertical displacement and use (3.3) at each
step.  Its domain condition is legal throughout, because
\(E\le D\le\binom Aj\le\binom{A+i}j\) for every
\(0\le i<g\):

\[
 \Lambda_{j,A+g}(E)-\Lambda_{j,A}(E)
 =\sum_{i=0}^{g-1}
   \bigl(\Lambda_{j,A+i+1}(E)-\Lambda_{j,A+i}(E)\bigr)
 \le gE.
\]

Subtract this from (3.2).  This proves (3.4).  \(\square\)

For (2.1), set

\[
 A=a+1,\quad B=t+1=A+g,\quad
 D=\binom A3-x,\quad E=\binom B3-y.
\tag{3.5}
\]

Then (1.6) has the second exact normal form

\[
 \boxed{
 \gamma_4=
 \left(\binom{A+g}{4}-\binom A4-\binom A3\right)
 +D+\Lambda_{3,A}(D)-\Lambda_{3,A+g}(E)-\tau.}
\tag{3.6}
\]

When \(g\ge1\), its displayed leading term is

\[
 \sum_{i=1}^{g-1}\binom{A+i}{3}.
\tag{3.7}
\]

Consequently, whenever \(D\ge E\), Lemma 3.1 yields

\[
 \boxed{
 \gamma_4\ge
 \left(\binom{A+g}{4}-\binom A4-\binom A3\right)
 +D+U_3(D-E)-gE-\tau.}
\tag{3.8}
\]

No finite search is used in Lemma 3.1 or identities (1.2), (1.8), (2.2),
and (3.6).

## 4. Frozen exact census

The verifier exhausts

\[
 2\le q\le60,\qquad 2\le c\le14,\qquad
 0\le r<q,\qquad 0\le u<q+c,
\tag{4.1}
\]

then retains exactly the points satisfying

\[
 b\ge31,\quad h\ge224,\quad b<h,\quad
 \gamma_3<0,\quad x\ge0.
\tag{4.2}
\]

The result is:

```text
checked_states                 85278
states_by_promotions           {2: 36288, 3: 33620, 4: 14921, 5: 449}
gamma4_nonpositive_states      0
minimum_gamma4                 69
rank3_cap_gap                  [1, 34]
beta_at_least_alpha            53463
forward_bound_positive         53343
D_at_least_E                   33278
deficit_bound_positive         32542
positive_by_either_bound       53343
uncovered_states               31935
dual_deficit_bound_positive    84743
second_level_bound_positive    85276
second_level_residual_count    2
```

Thus the frozen box gives an exact finite classification: every one of its
85,278 multi-promotion no-borrow states seeds at rank four.  A minimizing
state is

\[
 (q,c,r,u,b,h)=(16,2,0,3,37,256),
\tag{4.3}
\]

for which

\[
 n=120, H=667, z=560, w=819, \tau=547,
\quad \gamma_3=-408,\quad x=14,\quad y=272.
\]

Its canonical words are

\[
 14=\binom53+\binom32+\binom11,\qquad
 272=\binom{12}3+\binom{10}2+\binom71.
\]

Hence \(U_3(14)=6\), \(U_3(272)=636\), and

\[
 \gamma_4=636-6-14-547=69.
\tag{4.4}
\]

The independent rank-two closed forms (1.4) are checked against a greedy
binary-search Macaulay engine at every point.  The same engine verifies
(1.7), (2.2), (2.5), (2.7), (3.6), and all displayed conditional lower
bounds pointwise.

Reproduction:

```bash
python3 data/research_open/q1_two_hour_ten_proofs_transfer_2026-08-02/erdos776/verify_multi_promotion_no_borrow.py
pytest -q data/research_open/q1_two_hour_ten_proofs_transfer_2026-08-02/erdos776/test_verify_multi_promotion_no_borrow.py
```

The test result at freeze time was `1 passed`.

The loops really do include \(6\le c\le14\).  Their absence from
`states_by_promotions` means only that no tuple in this **particular finite
box** survives all of (4.2).  It is a filter output, not a proof that
\(c\ge6\) is globally impossible.

## 5. What remains genuinely open

The finite result strongly suggests the classification target

\[
 c\ge2,\quad\gamma_3<0,\quad x\ge0
 \quad\Longrightarrow\quad \gamma_4>0,
\tag{5.1}
\]

but (5.1) is **not proved**.  In particular, (2.3) and (3.8) certify only
53,343 of the 85,278 frozen points in union.  The remaining 31,935 points
show exactly where a proof must retain more of the canonical remainder:
The type compression is sharper than those two separate counts suggest.
There are exactly two joint orientation templates in the uncovered set:

| frozen template | count | promotions | cap-gap ranges |
|---|---:|---|---|
| reverse remainders: \(\beta<\alpha, D<E\) | 31,815 | \(c=2,3,4,5\), with counts 15,463, 12,418, 3,881, 53 | respectively \(2\!:\!14, 3\!:\!22, 5\!:\!28, 12\!:\!28\) |
| adjacent forward boundary: \(\beta\ge\alpha, D\ge E\) | 120 | only \(c=2\) | only \(g=1\) |

There are no uncovered mixed-orientation points in the frozen box.  These
two rows are finite templates, not unbounded chamber theorems.  The second
row is particularly rigid: all 120 misses of the forward bound occur at two
rank-two promotions and one rank-three cap step.  The first row is the true
bulk obstruction and reverses both monotone orientations simultaneously.

Applying the new second-level bound (2.6), rather than only (2.3) and
(3.8), collapses these two coarse templates almost completely: it proves a
strictly positive lower bound at 85,276 of all 85,278 points.  Its only two
finite residual rows are

| \((q,c,r,u,b,h)\) | \((a,t;s,\rho;v,\sigma)\) | lower bound (2.6) | exact \(\gamma_4\) |
|---|---|---:|---:|
| \((36,2,35,12,51,281)\) | \((35,37;34,19;16,1)\) | -3 | 354 |
| \((38,2,37,13,54,320)\) | \((37,39;36,11;16,7)\) | -51 | 489 |

Thus the only phase not certified by the coarse bound (2.6) has narrowed to
the two-promotion, two-cap-step phase.  The two rows themselves are not
counterexamples; their exact comparators are strongly positive.  They only
show that the uniform coarse replacement
\(\binom\rho2\mapsto\binom{s-1}{2}\) can still lose too much.

Their complete relevant canonical words make that loss explicit.  At the
first row,

\[
 \begin{aligned}
 z&=\binom{36}{3}+\binom{35}{2},\\
 x&=\binom{35}{3}+\binom{34}{2}+\binom{19}{1},\\
 y&=\binom{37}{3}+\binom{16}{2}+\binom11.
 \end{aligned}
\tag{5.2}
\]

Formula (2.5) is therefore

\[
 66045-52360+560-5984+0-171-7140-595-1=354.
\tag{5.3}
\]

Bound (2.6) replaces \(\binom{19}{2}=171\) by
\(\binom{33}{2}=528\), losing exactly 357 and returning \(354-357=-3\).
At the second row,

\[
 \begin{aligned}
 z&=\binom{38}{3}+\binom{37}{2},\\
 x&=\binom{37}{3}+\binom{36}{2}+\binom{11}{1},\\
 y&=\binom{39}{3}+\binom{16}{2}+\binom71,
 \end{aligned}
\tag{5.4}
\]

and (2.5) is

\[
 82251-66045+560-7140+21-55-8436-666-1=489.
\tag{5.5}
\]

Here replacing \(\binom{11}{2}=55\) by
\(\binom{35}{2}=595\) loses 540 and returns \(489-540=-51\).

### 5.1 Closing the shallow two-cap template

The two finite residuals belong to one unbounded phase that can be closed
by the exact adjacent loss rather than by (2.6).

For Theorems 5.1--5.2 and Proposition 5.3, an *admissible no-borrow point*
means a tuple satisfying (1.1)--(1.6), integral \(h\),

\[
 b\ge31,\qquad h\ge224,\qquad b<h,\qquad
 \gamma_3<0,\qquad x\ge0,
\tag{5.6a}
\]

with every displayed canonical remainder in its stated range.

**Theorem 5.1 (shallow two-cap closure).**  Suppose a relaxed-lattice point
is admissible in this sense and has

\[
 c=2,\qquad r=q-1,\qquad (a,t)=(q-1,q+1),
\tag{5.6}
\]

and put \(\delta=\binom{q-1}{2}-\alpha\).  If
\(1\le\delta\le q-2\), then \(\gamma_4>0\).

**Proof.**  The promotion identity gives \(b=q+u+3\).  Direct substitution
into the two remainder coordinates gives

\[
 \delta=\binom b2-2\binom q2,
 \qquad
 \beta=\binom u2+2q-2-\delta.
\tag{5.7}
\]

Because \(1\le\delta\le q-2\), the complement of \(\alpha\) crosses
exactly one rank-two wall:

\[
 \binom{q-1}{2}-\delta
 =\binom{q-2}{2}+(q-2-\delta).
\]

Consequently its full-block loss is exact:

\[
 \Lambda_{2,q-1}(\delta)
 =\delta(q-2)-\binom{\delta+1}{2}.
\tag{5.8}
\]

The two leading rank-three caps in (2.7) cancel the leading part of
\(z=\binom q3+\binom{q-1}{2}\), leaving

\[
 \boxed{
 \gamma_4=U_2(\beta)
 +\delta(q-2)-\binom{\delta+1}{2}
 -\binom{q-1}{2}-1.}
\tag{5.9}
\]

The middle loss in (5.9) is nonnegative.  Equation (5.7) and
\(\delta\le q-2\) also give

\[
 \beta\ge\binom u2+q,
 \qquad U_2(\beta)\ge\binom u3.
\tag{5.10}
\]

For \(q\ge40\), the inequality \(\delta>0\) forces \(u>q/3\).  Indeed,
if \(u\le q/3\), then

\[
 \binom{q+u+3}{2}
 \le\binom{4q/3+3}{2}<2\binom q2,
\]

where the last strict inequality is equivalent to
\(2q^2-78q-54>0\), contradicting (5.7).  For \(q\ge90\), put
\(Q=q/3\).  Then

\[
 Q(Q-1)(Q-2)>3q(q-1)
\]

because it reduces to \(Q^2-30Q+11>0\).  Hence

\[
 U_2(\beta)\ge\binom u3>\binom q2
 >\binom{q-1}{2}+1,
\]

and (5.9) is positive.  The exact verifier exhausts the remaining
\(q<90\) phase: there are 20 admissible points, all positive, with minimum
\(\gamma_4=186\) at \((q,u,b,h,\delta,\beta)=(39,13,55,327,3,151)\).
This completes the template.  \(\square\)

### 5.2 Eventual positivity for every fixed \(c\ge3\)

The finite disappearance of \(c\ge6\) must not be extrapolated, but a
compact normalized-tail argument settles the large-\(q\) part of every
fixed slice except \(c=2\).

**Theorem 5.2 (fixed-promotion tail).**  For every fixed integer
\(c\ge3\), there is a threshold \(Q_c\) such that every admissible
no-borrow point with promotion count \(c\) and \(q\ge Q_c\) satisfies
\(\gamma_4>0\), uniformly over \(0\le r<q\) and \(0\le u<q+c\).

**Proof.**  Suppose otherwise for one fixed \(c\ge3\), and take a sequence
with \(q\to\infty\) and \(\gamma_4\le0\).  Formula (1.2) and the ranges of
\(r,u\) give \(b=O_c(q)\).  Equations (1.4)--(1.5), uniformly on those
ranges, give

\[
 z=\binom q3+O(q^2),\qquad
 x=\binom q3+O_c(q^2),\qquad
 y=\binom q3+O_c(q^2).
\tag{5.11}
\]

Thus the leading indices in (2.1) satisfy

\[
 a=q+O_c(1),\qquad t=q+O_c(1).
\tag{5.12}
\]

After taking a subsequence, the integer shifts \(a-q,t-q\), and hence
\(g=t-a\), are constant.  Compactness also lets us assume

\[
 \frac rq\to R,\quad \frac uq\to U,\quad
 \frac{2\alpha}{q^2}\to P,\quad
 \frac{2\beta}{q^2}\to S,
 \qquad R,U,P,S\in[0,1].
\tag{5.13}
\]

The displacement has both exact descriptions

\[
 y-x=\binom{q+c}{3}-\binom q3
      +\binom u2-\binom r2-1
\]

and

\[
 y-x=\binom t3-\binom a3+\beta-\alpha.
\]

Dividing by \(q^2/2\) and passing to the limit yields

\[
 \boxed{g+S-P=c+U^2-R^2\ge c-1.}
\tag{5.14}
\]

We also use the elementary rank-two scaling rule

\[
 \frac{N_q}{q^2}\to\frac\theta2
 \quad\Longrightarrow\quad
 \frac{U_2(N_q)}{q^3}\to\frac{\theta^{3/2}}6.
\tag{5.15}
\]

Indeed, the leading index of the rank-two word is
\(\sqrt\theta\,q+o(q)\), while its rank-one remainder contributes only
\(O(q^2)\) after raising.  Apply (5.15) to \(\alpha,\beta\) in the exact
comparator (2.2).  Since \(z/q^3\to1/6\),

\[
 \frac{\gamma_4}{q^3}\to
 \frac{g-1+S^{3/2}-P^{3/2}}6.
\tag{5.16}
\]

For \(f(x)=x-x^{3/2}\) on \([0,1]\), one has
\(0\le f(x)\le4/27\).  Using (5.14), the numerator in (5.16) is at least

\[
 c-2+f(P)-f(S)\ge c-2-\frac4{27}\ge\frac{23}{27}>0.
\tag{5.17}
\]

This contradicts \(\gamma_4\le0\) along the sequence.  Hence the claimed
threshold exists.  The compactness argument is uniform in \(r,u\), while
the threshold is allowed to depend on \(c\).  \(\square\)

**Proposition 5.3 (two-promotion boundary localization).**  Along every
admissible sequence on the fixed slice \(c=2\), one has

\[
 \liminf_{q\to\infty}\frac{\gamma_4}{q^3}\ge0.
\]

Moreover, if an unbounded sequence on that slice has \(\gamma_4\le0\),
then necessarily

\[
 \frac rq\to1,\qquad \frac uq\to0.
\tag{5.18}
\]

**Proof.**  Use the same subsequence and notation as in Theorem 5.2.  Put
\(D=2+U^2-R^2\in[1,3]\).  The limiting numerator in (5.16) can be written

\[
 g-1+S^{3/2}-P^{3/2}
 =D-1+f(P)-f(S).
\tag{5.19}
\]

If \(D\ge2\), this is at least \(1-4/27>0\).  If \(1<D<2\), the identity
\(g+S-P=D\) has two possible integer phases.  For \(g=1\), one has
\(S>P\), so the original form in (5.19) is positive.  For \(g=2\), one has
\(P>S\), and

\[
 1+S^{3/2}-P^{3/2}>0.
\]

The endpoint phases can have zero limit only when \(D=1\).  Since
\(D=2+U^2-R^2\), this forces \((R,U)=(1,0)\), proving (5.18).
\(\square\)

The two residual rows of (2.6) are therefore closed as an unbounded
conditional template, not merely checked individually.  What remains is to
prove that every multi-promotion point outside the already certified
inequalities necessarily enters one of the symbolically closed phases; the
finite atlas alone does not establish that global exhaustiveness.  Theorem
5.2 also removes the eventual tail of every fixed \(c\ge3\), leaving
\(c=2\) as the main unbounded classification target.  Proposition 5.3
further confines any possible bad \(c=2\) sequence to the thin boundary
\(r/q\to1,u/q\to0\).  Theorem 5.1 instead closes a separate shallow phase
containing the two finite residual rows; it is not a phase on this boundary.

## 6. Scope firewall

- The census is finite evidence and a falsifier, not a proof of (5.1).
- Theorem 5.1 is conditional on the exact shallow phase (5.6); it does not
  say that every \(c=2\) state enters that phase.
- The quantifiers in Theorem 5.2 are
  \(\forall c\ge3\;\exists Q_c\;\forall q\ge Q_c\).  It supplies neither
  a threshold uniform in \(c\) nor control when \(c=c(q)\) grows, and it
  deliberately leaves the other \(c=2\) phases open.
- Proposition 5.3 is a localization, not a positivity theorem at its
  boundary; lower-order analysis is still required when (5.18) holds.
- The earlier fixed rank-five bridge is already refuted by a genuine dyadic
  family; the family recovers at rank six.
- A bridge counterexample is not a counterexample to Erdős #776.
- Nothing in this note proves or disproves the original Erdős problem.
