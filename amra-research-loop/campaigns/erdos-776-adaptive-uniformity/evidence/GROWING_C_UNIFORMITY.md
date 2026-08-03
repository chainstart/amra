# Growing-promotion uniformity in the relaxed no-borrow comparator

Date: 2026-08-02

Status: **author proof; independent reconstruction required**.

Scope: this note concerns the exact relaxed no-borrow coordinates of
`MULTI_PROMOTION_NO_BORROW_ATLAS.md`.  It does not prove the bridge from a
relaxed seed to an antichain satisfying the actual rank-capacity constraints,
and therefore does not solve Erdős #776.

## 1. Exact setting

Let an admissible no-borrow state have

\[
n=\binom q2+r,\qquad n+b-1=\binom{q+c}2+u,
\quad 0\le r<q,\quad0\le u<q+c,\quad c\ge2,
\]

so

\[
b=cq+\binom c2+u-r+1.
\tag{1.1}
\]

Put

\[
z=\binom q3+\binom r2,\qquad
w=\binom{q+c}3+\binom u2,
\]

\[
H=\binom b2+1,\qquad
x=n+z-H+1,\qquad y=n+w-H.
\]

The no-borrow condition includes `x>=0`, and the exact tax cancellation is

\[
\gamma _4=U_3(y)-U_3(x)-z-1.
\tag{1.2}
\]

Also

\[
\Delta:=y-x=w-z-1.
\tag{1.3}
\]

## 2. A uniform shadow asymptotic

For integers `N>=0`,

\[
U_3(N)=\frac{6^{4/3}}{24}N^{4/3}+O(N),
\tag{2.1}
\]

with an absolute error constant.  Indeed, if
`N=binom(a,3)+R`, `0<=R<binom(a,2)`, then

\[
U_3(N)=\binom a4+U_2(R).
\]

Here `a=(6N)^(1/3)+O(1)`, while `U_2(R)=O(a^3)=O(N)`.
This proves (2.1).  We also use the established superadditivity

\[
U_3(A+B)\ge U_3(A)+U_3(B).
\tag{2.2}
\]

## 3. Admissibility bounds the promotion scale

Since `x>=0`,

\[
H\le n+z+1=O(q^3).
\]

On the other hand, (1.1) gives `b>=(c-1)q`.  Hence

\[
c=O(\sqrt q).
\tag{3.1}
\]

If `c=c(q)->infinity`, then (3.1), (1.1), and the remainder ranges give

\[
b=cq(1+o(1))
\tag{3.2}
\]

and direct expansion of (1.3) gives

\[
\Delta
=\binom{q+c}3-\binom q3+\binom u2-\binom r2-1
=\frac{cq^2}{2}(1+o(1)).
\tag{3.3}
\]

In particular, `Delta>0` eventually.

## 4. Decisive growing-c lemma

**Lemma 4.1.**  Along every sequence of admissible no-borrow states with
`q->infinity` and `c=c(q)->infinity`, one has `gamma4>0` eventually.

**Proof.**  By (3.1), pass to a subsequence on which `c/sqrt(q)` converges.

If its limit is positive, then `c>=epsilon*sqrt(q)` on the subsequence.
By (2.2), (1.2), and (3.3),

\[
\gamma _4\ge U_3(\Delta)-z-1.
\]

Equations (2.1) and (3.3) give

\[
\frac{U_3(\Delta)}{q^3}
\asymp \frac{c^{4/3}}{q^{1/3}}\longrightarrow\infty,
\]

whereas `z/q^3->1/6`.  Thus `gamma4>0`.

It remains to consider `c/sqrt(q)->0`.  From (3.2),
`H=o(q^3)`, and therefore

\[
x=\frac{q^3}{6}(1+o(1)).
\tag{4.1}
\]

Moreover `Delta/x->0`.  Apply (2.1) at `x+Delta` and `x`.  The error after
subtraction is `O(q^3)`, while the main-term difference is

\[
\frac{6^{4/3}}{24}
\bigl((x+\Delta)^{4/3}-x^{4/3}\bigr)
=\frac q3\Delta(1+o(1))
=\frac{cq^3}{6}(1+o(1)).
\]

Because `c->infinity`, the `O(q^3)` error is negligible.  Subtracting
`z+1=q^3/6+O(q^2)` in (1.2) again leaves a positive quantity.  Every
subsequence has a further subsequence covered by one of these alternatives,
so an infinite nonpositive sequence cannot exist.  This proves the lemma.
\(\square\)

## 5. Uniform relaxed no-borrow corollary

The independently audited inherited results say:

- for fixed `c=2`, all sufficiently large admissible states have
  `gamma4>0`;
- for every fixed `c>=3`, all sufficiently large admissible states have
  `gamma4>0`, with a threshold allowed to depend on `c`.

Together with Lemma 4.1 they imply a genuinely uniform statement.

**Corollary 5.1.**  There is `Q` such that, for every `q>=Q` and every
admissible promotion count `c>=2`, the relaxed no-borrow comparator has
`gamma4>0`.

If not, choose bad states with `q->infinity`.  A bounded promotion sequence
has a constant subsequence, contradicting the corresponding fixed-`c`
theorem.  An unbounded promotion sequence has a subsequence with
`c->infinity`, contradicting Lemma 4.1.

This compactness conclusion is non-effective.  It closes the missing
growing-promotion quantifier in the relaxed comparator but supplies neither
an explicit global threshold nor the actual seed/rank-capacity bridge.

## 6. Evidence classification and remaining gap

- `statement_match`: exact for the relaxed no-borrow comparator; not the
  public problem.
- `mathematical_status`: proved by author natural proof, pending independent
  reconstruction.
- `machine_reproduced`: the companion finite probe is exact negative-route
  evidence only; it is not used to infer Lemma 4.1.
- `publication_state`: private research artifact.
- remaining decisive gap: prove a borrow-aware Hall/capacity bridge from the
  relaxed adaptive seed theorem to the actual Boolean-lattice construction.
