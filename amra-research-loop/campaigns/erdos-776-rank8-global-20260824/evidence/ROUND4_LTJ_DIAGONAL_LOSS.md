# Round 4: LTJ diagonal loss on the actual zero-seed orbit

## Status and scope

This note studies only the surviving M776G-01 route.  It does **not** prove
the LTJ bound and does **not** close the rank-8 entry or the public problem.
It proves an all-parameter diagonal domination and its exact loss recurrence,
then gives an all-parameter obstruction to obtaining the missing estimate from
the magnitude of the diagonal gap alone.

The conclusions are:

1. The exact recurrence is
   \[
   L_{q-1}=T_q+P_q,
   \]
   where the first term is tax capacity and the second is propagated shadow
   loss.  Both terms are nonnegative on the actual aligned zero-seed orbits.
2. Hence the actual orbits satisfy the all-parameter diagonal domination
   \[
   E_{q+1}^{(V+1)}\le S_q(E_q^{(V)}).
   \]
3. No positive lower bound for \(P_q\) can depend only on \(q\) and the
   positive gap \(L_q\): arbitrarily long canonical cells have \(P_q=0\).
4. The remaining LTJ inequality is displayed exactly in (R4.12).  Proving it
   requires actual-orbit information about canonical plateau position (or an
   equivalent effective suffix separator), not merely accumulated gap size.

Thus the gap-only propagated-loss subroute is refuted.  M776G-01 itself
remains open.

## 1. Actual orbit and the correct residual variables

Write \(\partial_q=\operatorname{KK}_q\) for the lower-shadow numerical
operator.  For each parameter \(V\), the shortened zero-seed orbit is

\[
 E_{V-26}^{(V)}=0,\qquad
 E_{q-1}^{(V)}=V+\partial_q(E_q^{(V)}).
 \tag{R4.1}
\]

Put \(N=V-25\).  The residual variables used by LTJ are

\[
 Z_3(V)=E_5^{(V)}-\binom{N-1}{5}-\binom{N-2}{4},
 \tag{R4.2}
\]
\[
 B_2(V)=E_4^{(V)}-\binom{N-1}{4}-\binom{N-2}{3}
       =V+\partial_3(Z_3(V)).
 \tag{R4.3}
\]

In particular, \(B_2\) here is the rank-2 **residual**, not the full value
\(E_4^{(V)}\).  Write its 2-canonical expansion as

\[
 B_2(V)=\binom a2+b,\qquad 0\le b<a.
 \tag{R4.4}
\]

The target LTJ statement is

\[
 \bigl(B_2(V+1)-B_2(V)\bigr)_+\le a(B_2(V))
 \quad(V\ge125).
 \tag{LTJ}
\]

## 2. Upper adjoint and suspension

If the \(r\)-canonical expansion is
\(x=\sum_i\binom{a_i}{i}\), define

\[
 U_r(x)=\sum_i\binom{a_i}{i+1},
 \qquad
 S_r(x)=x+U_r(x)=\sum_i\binom{a_i+1}{i+1}.
 \tag{R4.5}
\]

The standard numerical Kruskal--Katona adjunction and Pascal's identity give

\[
 U_r(x)=\max\{t:\partial_{r+1}(t)\le x\},
 \qquad
 \partial_{r+1}(S_r(x))=x+\partial_r(x).
 \tag{R4.6}
\]

## 3. Exact diagonal-loss recurrence

Fix \(V\), align the two actual orbits by putting

\[
 x_q=E_q^{(V)},\qquad y_{q+1}=E_{q+1}^{(V+1)},
 \qquad L_q=S_q(x_q)-y_{q+1}.
 \tag{R4.7}
\]

At the aligned top rank \(q=V-26\), both seeds are zero and \(L_q=0\).
For \(5\le q\le V-26\), let

\[
 m=x_{q-1}=V+\partial_q(x_q),
\]
\[
 T_q=U_{q-1}(m)-x_q-1,
 \qquad
 P_q=\partial_{q+1}(S_q(x_q))-\partial_{q+1}(y_{q+1}).
 \tag{R4.8}
\]

Then, identically,

\[
 \boxed{L_{q-1}=T_q+P_q.}
 \tag{R4.9}
\]

Indeed, (R4.1) and (R4.6) give

\[
\begin{aligned}
L_{q-1}
 &=S_{q-1}(m)-\bigl(V+1+\partial_{q+1}(y_{q+1})\bigr)\\
 &=U_{q-1}(m)-x_q-1
   +\partial_{q+1}(S_q(x_q))-\partial_{q+1}(y_{q+1}).
\end{aligned}
\]

This recurrence has a noncircular one-sided consequence.  Numerical shadows
are subadditive, so for \(h=\lfloor V/q\rfloor\),

\[
 \partial_q(x_q+h)-\partial_q(x_q)
 \le \partial_q(h)\le qh\le V.
\]

By the adjunction in (R4.6),

\[
 U_{q-1}(m)\ge x_q+h,
 \qquad T_q\ge\lfloor V/q\rfloor-1\ge0.
 \tag{R4.10}
\]

If \(L_q\ge0\), monotonicity of \(\partial_{q+1}\) gives \(P_q\ge0\).
Starting at the zero top loss and descending in \(q\), (R4.9)--(R4.10)
therefore prove, for every admissible \(V,q\),

\[
 \boxed{E_{q+1}^{(V+1)}\le S_q(E_q^{(V)})}.
 \tag{R4.11}
\]

This is an all-parameter actual-orbit theorem, not a finite extrapolation.
It is nevertheless too weak for LTJ because it records only nonnegativity of
the two summands in (R4.9).

## 4. Rank-4 specialization and the exact remaining inequality

The separated rank-4 and rank-5 expansions cancel their two large prefix
terms under suspension.  Consequently

\[
 L_4=S_2(B_2(V))-Z_3(V+1).
\]

At the last recurrence step \(q=5\), (R4.9) becomes

\[
 T_5=U_2(B_2(V))-Z_3(V)-1,
\]
\[
 P_5=B_2(V)+Z_3(V)+1-Z_3(V+1),
 \qquad L_4=T_5+P_5.
\]

Let \(B=B_2(V)=\binom a2+b\) and \(k=B-V=\partial_3(Z_3(V))\).
Since

\[
B_2(V+1)=V+1+\partial_3(Z_3(V+1)),
\]

LTJ is equivalent, by the adjunction (R4.6), to the following exact loss
threshold:

\[
 \boxed{
 L_4\ge S_2(B)-U_2(k+a-1).
 }
 \tag{R4.12}
\]

This is the remaining inequality, not a claimed theorem.  The recurrence
proves \(L_4\ge0\), but (R4.12) can demand strictly more.

## 5. All-parameter obstruction to a gap-only propagated-loss bound

The second term in (R4.9) can vanish throughout arbitrarily long canonical
cells.

**Plateau lemma.**  For every \(q\ge1\), \(A\ge q+2\), and
\(1\le L\le A-q-1\), set

\[
 x=\binom{A-1}{q},\qquad S_q(x)=\binom A{q+1},
 \qquad y=S_q(x)-L.
\]

Then \(L=S_q(x)-y>0\), but

\[
 \partial_{q+1}(S_q(x))-\partial_{q+1}(y)=0.
 \tag{R4.13}
\]

To prove this, first use the canonical expansion

\[
 \binom Aq-1
 =\binom{A-1}q+\binom{A-2}{q-1}+\cdots+\binom{A-q}{1}.
\]

Its upper adjoint is

\[
 U_q\!\left(\binom Aq-1\right)
 =\binom A{q+1}-(A-q).
 \tag{R4.14}
\]

By adjunction, every integer
\(y>\binom A{q+1}-(A-q)\) has
\(\partial_{q+1}(y)\ge\binom Aq\).  On the other hand
\(y<\binom A{q+1}\), so monotonicity gives
\(\partial_{q+1}(y)\le\binom Aq\).  Equality follows, proving (R4.13).

Since the permitted plateau length \(A-q-1\) is unbounded, (R4.13) refutes
every proposed uniform estimate

\[
 P_q\ge f(q,L_q)>0\quad\text{for all }L_q>0
\]

that uses no canonical-position information.  In particular, proportional
propagation of accumulated loss is impossible.  This obstruction is a theorem
about the proposed mechanism; it is **not** a counterexample to actual-orbit
LTJ.

## 6. Finite guards and fail-closed conclusion

A standalone exact-integer falsifier found no actual LTJ counterexample on
\(125\le V\le2000\).  This range is recorded only as a kill test and is not
used anywhere in the proof above.  No larger cutoff is claimed.  The retained
lightweight verifier checks selected actual rows, two complete aligned-orbit
recurrence instances, and 2,114 plateau instances guarding the symbolic
formula:

```text
python3 evidence/verify_round4_ltj_diagonal_loss.py
```

It returns `status: PASS`.  The verifier is not a proof of LTJ.

The exact surviving gap is (R4.12).  A valid next mechanism must prove an
actual-orbit plateau-escape statement (for example, a quantitative lower bound
on distance to the left edge of the current canonical cell), or retain enough
suffix data to force tax plus propagated loss above (R4.12).  The all-parameter
plateau lemma freezes any route depending only on \(L_q\).  Until such extra
structure is proved, the result is fail-closed.
