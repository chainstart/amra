# Negative no-borrow gate freeze

Frozen: 2026-08-02 12:20 HKT

Final validation: 2026-08-02 12:28 HKT; 13 focused tests passed.

Superseded on 2026-08-02: the frozen gate (NB) is now **REFUTED** by the
actual dyadic family in `FINAL_CHAMBER_COUNTERFAMILY.md`.  The family
recovers at rank six, so this update does not refute Erdős #776.

## Proved boundary

The negative-offset initial chambers now have the following status.

1. The double-borrow chamber \(b\ge5\), \(b^2-b+4<4h\), has a uniform
   seed by \(p_5(h)=\log_2\log h+O(1)\) for sufficiently large \(h\).
2. The initial \(x\)-only borrow chamber seeds by rank four.  The only
   exceptional algebraic depth \(q=1\) is covered by the exact positive
   formula (1.6) of NEGATIVE_INITIAL_CHAMBERS.md.
3. In the initial no-borrow chamber, the local orbit has the exact
   dimensionless parameters

   \[
   H=\binom b2+1,\quad m=b-1,\quad
   \tau=H-n,\quad
   \gamma_3=U_2(n+m)-U_2(n)-H.
   \]

   If \(\gamma_3<0\), the next low blocks are

   \[
   x_0=n+U_2(n)-H+1,\qquad
   y_0=x_0+\bigl(U_2(n+m)-U_2(n)-1\bigr).
   \]

   The three possible signs are double borrow, \(x\)-only borrow, and no
   borrow; the reverse asymmetric state is impossible.
4. On the rank-four no-borrow antecedent

   \[
   \gamma_3<0,\qquad x_0\ge0,\qquad\gamma_4<0,
   \]

   Lemma 2.1 proves uniformly for sufficiently large \(h\) that the
   following rank-five low blocks satisfy \(X_1,Y_1>0\):

   \[
   X_1=U_3(x_0)-\tau+1,\qquad
   Y_1=U_3(y_0)-\tau.
   \]

   Thus there is no unaccounted high-rank borrow in the remaining
   asymptotic target.
5. The two tax terms cancel exactly:

   \[
   \gamma_4=U_3(x_0+d)-U_3(x_0)-U_2(n)-1,
   \]

   \[
   \gamma_5=U_4(X_1+e)-U_4(X_1)-U_3(x_0)-1,
   \]

   where \(d=y_0-x_0\) and \(e=Y_1-X_1\).  In particular the former
   gate is a pure iterated-promotion inequality, independent of the
   original tax once the low blocks have been formed.

## Former first unproved lemma: now refuted

The assertion frozen here was

\[
\boxed{
\gamma_3<0,\quad x_0\ge0,\quad\gamma_4<0
\quad\Longrightarrow\quad
U_4(Y_1)-U_4(X_1)-X_1-\tau>0.}
\tag{NB}
\]

It is false even on the actual dyadic sublattice.  Take

\[
K=6,\quad r=10,\quad
h=224\,2^s,\quad
q=(448\,2^s-2)/5,
\quad s\equiv2\pmod4,
\]

and put \(b=q+6,n=\binom q2+10\).  For every \(s\ge14\) in this
residue class, all of the antecedent and cap-legality conditions hold, but

\[
\gamma_5=4\,302\,695-6q<0.
\]

The two rank-four borrowing sign states are still not frozen symbolically.
They are separate from this explicit no-borrow counterfamily.

## Earlier exact evidence and updated reduction

The pre-refutation independent verifier recorded:

- 61,918 asymmetric states with \(q\ge2\), all positive at rank three;
- 235 exact \(q=1\) states, all positive at rank four;
- 219 relaxed no-borrow antecedent points through \(b=250\), with
  \(\min X_1=40405\) and \(\min Y_1=46310\);
- 167 dyadic points through \(j=10\) with
  \(\gamma_3,\gamma_4<0\), all having \(\gamma_5>0\), with minimum
  \(\gamma_5=39710\) at \((j,b)=(2,154)\).

The earlier finite scans did not reach the first counterexample.  The
counterfamily has triangular coordinates

\[
n=\binom q2+r,\qquad
n+b-1=\binom{q+1}{2}+u;
\]

that is, exactly one rank-two promotion occurs.  Writing \(K=b-q\)
then gives \(u=r+K-1\) and the exact first surplus

\[
\gamma_3=(K-1)r-K(q+1)<0.
\]

The assertion that the antecedent of (NB) always forces this one-promotion
state remains experimental and must not be used as a theorem.  It is no
longer a route to a rank-five proof, but may still classify the
complementary lattice.  The two signs are

\[
R=\binom{r+1}{2}-Kq-\binom K2,\qquad
S=R+\binom{r+K-1}{2}-\binom r2-1.
\]

These coordinates reproduce every observed endpoint without referring to
the dyadic strip scan.

For the counterfamily itself, the two canonical levels are proved directly,
so neither global one-promotion exhaustiveness nor global wall
exhaustiveness is being assumed.  Its exact adaptive repair is rank six:
\(\gamma_6>0\) for the whole family.
