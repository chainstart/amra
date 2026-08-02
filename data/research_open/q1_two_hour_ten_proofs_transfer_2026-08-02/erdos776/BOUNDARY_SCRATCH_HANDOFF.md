# Two-promotion boundary scratch handoff

Written after the 21:10 author freeze; this file is **not** part of the
frozen author claim set. It is a handoff for independent audit.

## 1. Exact boundary coordinates

Fix promotion count $c=2$, put $k=q-r\ge1$, and consider an admissible
sequence with

$$
q\to\infty,\qquad k=o(q),\qquad u=o(q).
\tag{1.1}
$$

This is the boundary localized by Proposition 5.3. The promotion identity
and the two rank-two shadows give

$$
b=q+u+k+2,\qquad n=\binom q2+q-k,
$$

$$
z=\binom q3+\binom{q-k}{2},\qquad
w=\binom{q+2}{3}+\binom u2.
\tag{1.2}
$$

Direct substitution in the low blocks gives

$$
x=\binom{q+1}{3}-D,
\qquad
D=\binom{q+u+k+2}{2}-\binom{q-k+1}{2},
\tag{1.3}
$$

and

$$
y=\binom{q+1}{3}+\binom q2-E.
\tag{1.4}
$$

The three exact integer quantities are

$$
\boxed{D=\frac{(u+2k+1)(2q+u+2)}2,}
\tag{1.5}
$$

$$
\boxed{E=\frac{2q(u+k)+k^2+2ku+5k+4u+4}{2},}
\tag{1.6}
$$

and

$$
\boxed{
F=D-E=\frac{-k^2+2kq-k+2q+u^2-u-2}{2}.}
\tag{1.7}
$$

Under (1.1), $D,E=o(q^2)$. Both are positive, and eventually

$$
0<E<D<\binom q2.
\tag{1.8}
$$

Indeed, eventually $k\le q-1$, whence
$2kq-k^2-k\ge kq$; also $u^2-u\ge0$. Thus
$2F\ge kq+2q-2>0$. Equations (1.3)--(1.8) now show exactly when the next
cap indices stabilize:

$$
\boxed{
a=q,\quad \alpha=\binom q2-D,\qquad
t=q+1,\quad \beta=\binom q2-E.}
\tag{1.9}
$$

This cap statement is eventual and conditional on (1.1), not a claim about
every finite $c=2$ point.

## 2. Exact loss comparator and the critical window

Set

$$
\Lambda_{2,q}(d)=\binom q3-U_2\!\left(\binom q2-d\right).
$$

The frozen exact comparator and (1.9) give

$$
\boxed{
\gamma_4=\Lambda_{2,q}(D)-\Lambda_{2,q}(E)
-\binom{q-k}{2}-1.}
\tag{2.1}
$$

Since $D\ge E$, deficit transport yields

$$
\boxed{
\gamma_4\ge U_2(F)-\binom{q-k}{2}-1.}
\tag{2.2}
$$

Suppose every member of an unbounded sequence has $\gamma_4\le0$. Then,
for large $q$,

$$
U_2(F)\le\binom{q-k}{2}+1\le q^2.
\tag{2.3}
$$

Here is an explicit converse growth constant. If $v$ is maximal with
$\binom v2\le N$, then $U_2(N)\ge\binom v3$. For all sufficiently large
$N$, one has $v\ge\sqrt{N/2}$ and $\binom v3\ge v^3/24$. Hence

$$
U_2(N)\ge\frac{N^{3/2}}{48\sqrt2}.
\tag{2.4}
$$

Combining (2.3)--(2.4),

$$
F\le(48\sqrt2)^{2/3}q^{4/3}
\tag{2.5}
$$

once $F$ exceeds the fixed threshold in (2.4); bounded $F$ is absorbed in
the same big-O conclusion. The exact expression (1.7) also gives

$$
2F\ge kq+2q-2+(u^2-u).
$$

Therefore

$$
\boxed{k=O(q^{1/3}),\qquad u=O(q^{2/3}).}
\tag{2.6}
$$

For the second estimate, use $u^2-u\ge u^2/2$ for $u\ge2$; $u=0,1$ is
harmless.

## 3. Fixed-pair positivity

The critical sequence cannot keep both $k$ and $u$ bounded. The required
rank-two loss scaling is elementary.

**Lemma 3.1.** For a fixed nonnegative integer $d$ and any
$N_q=dq+O(1)$,

$$
\frac{\Lambda_{2,q}(N_q)}{q^2}\longrightarrow\frac d2.
\tag{3.1}
$$

**Proof.** The leading index of $\binom q2-N_q$ is either $q-d$ or
$q-d-1$ for all large $q$. In the first case the rank-one remainder is
$O(1)$, and

$$
\binom q3-\binom{q-d}{3}=\frac d2q^2+O_d(q).
$$

In the second case the rank-one remainder is $q+O_d(1)$. Its raised
contribution is $q^2/2+O_d(q)$, while

$$
\binom q3-\binom{q-d-1}{3}
=\frac{d+1}{2}q^2+O_d(q).
$$

Subtracting the raised remainder again leaves
$dq^2/2+O_d(q)$. $\square$

For fixed $k,u$, equations (1.5)--(1.6) have

$$
D=(u+2k+1)q+O_{k,u}(1),\qquad
E=(u+k)q+O_{k,u}(1).
$$

Apply Lemma 3.1 in (2.1). Since
$\binom{q-k}{2}/q^2\to1/2$,

$$
\boxed{
\frac{\gamma_4}{q^2}\longrightarrow
\frac{u+2k+1}{2}-\frac{u+k}{2}-\frac12
=\frac k2>0.}
\tag{3.2}
$$

Consequently a nonpositive unbounded boundary sequence must also satisfy

$$
\boxed{k+u\to\infty.}
\tag{3.3}
$$

Otherwise integer compactness supplies a subsequence with fixed $(k,u)$,
contradicting (3.2).

## 4. Remaining target and firewall

The remaining candidate window is

$$
k=q-r=O(q^{1/3}),\qquad
u=O(q^{2/3}),\qquad
k+u\to\infty.
\tag{4.1}
$$

- This scratch note does **not** prove positivity in (4.1).
- It does not amend the frozen theorem note or claim ledger.
- Theorem 5.1's shallow two-cap phase has asymptotically
  $u/q\to\sqrt2-1$, not $u/q\to0$. It contains the two finite residual
  points of bound (2.6), but it is not a phase on the Proposition 5.3
  boundary.
- All statements concern the complementary relaxed no-borrow bridge. A
  bridge counterexample would not be a counterexample to Erdős #776.
