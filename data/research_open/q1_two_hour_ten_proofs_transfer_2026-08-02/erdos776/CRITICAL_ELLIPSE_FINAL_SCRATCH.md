# Critical-ellipse final scratch: exact cap-depth closure

Date: 2026-08-02

Status: **POST-FREEZE NEW SCRATCH; PROPOSED FIXED-`c=2` EVENTUAL POSITIVITY
THEOREM, NOT YET ADMITTED TO THE FROZEN CLAIM SET**.

This note continues `BOUNDARY_SCRATCH_HANDOFF.md` and the independently
audited localization

\[
k=O(q^{1/3}),\qquad u=O(q^{2/3}),\qquad k+u\longrightarrow\infty.
\tag{0.1}
\]

It uses the exact canonical cap indices rather than only the transported
lower bound `U_2(F)`.  The resulting analysis appears to eliminate the
whole critical region for fixed promotion count `c=2`.

## 1. Exact cap-depth coordinates

Recall

\[
D=\frac{(u+2k+1)(2q+u+2)}2,
\]

\[
E=\frac{2q(u+k)+k^2+2ku+5k+4u+4}{2},
\]

and, eventually on the localized boundary,

\[
\gamma_4=\Lambda_{2,q}(D)-\Lambda_{2,q}(E)
-\binom{q-k}{2}-1.
\tag{1.1}
\]

For an integer depth `s`, put

\[
A_q(s)=\binom q2-\binom{q-s}{2}
=sq-\binom{s+1}{2}.
\tag{1.2}
\]

Let `s_D` and `s_E` be the least depths for which

\[
D\le A_q(s_D),\qquad E\le A_q(s_E).
\]

Because `D,E=o(q^2)`, both depths are `o(q)`.  Their canonical remainders

\[
\rho_D=A_q(s_D)-D,qquad \rho_E=A_q(s_E)-E
\]

satisfy

\[
0\le\rho_D<q-s_D,qquad0\le\rho_E<q-s_E,
\tag{1.3}
\]

by minimality and
`A_q(s)-A_q(s-1)=q-s`.  Consequently

\[
\binom q2-D=\binom{q-s_D}{2}+\rho_D,
\qquad
\binom q2-E=\binom{q-s_E}{2}+\rho_E
\tag{1.4}
\]

are the exact rank-two canonical words.

The useful baseline depths are not guessed.  Direct substitution gives

\[
A_q(u+2k+1)-D
=-(2k^2+3ku+5k+u^2+3u+2)<0,
\]

\[
A_q(u+k)-E
=-\left(k^2+2ku+3k+\frac{u^2+5u+4}{2}\right)<0.
\]

Thus there are positive integers `h_D,h_E` such that

\[
s_D=u+2k+1+h_D,qquad s_E=u+k+h_E.
\tag{1.5}
\]

For a common trial correction `h`, define

\[
R_D(h)=A_q(u+2k+1+h)-D,
\]

\[
R_E(h)=A_q(u+k+h)-E.
\]

Their exact doubled forms are

\[
\begin{aligned}
2R_D(h)={}&2hq-h^2-4hk-2hu-3h\\
&-4k^2-6ku-10k-2u^2-6u-4,
\end{aligned}
\tag{1.6}
\]

\[
\begin{aligned}
2R_E(h)={}&2hq-h^2-2hk-2hu-h\\
&-2k^2-4ku-6k-u^2-5u-4.
\end{aligned}
\tag{1.7}
\]

Most importantly,

\[
R_E(h)-R_D(h)
=\frac{2hk+2h+2k^2+2ku+4k+u^2+u}{2}>0.
\tag{1.8}
\]

Since `h_D,h_E` are the first corrections at which the corresponding
`R` becomes nonnegative, (1.8) implies

\[
h_E\le h_D.
\tag{1.9}
\]

## 2. Three cap steps force positivity

Put

\[
v_D=q-s_D,qquad v_E=q-s_E,qquad m=v_E-v_D=s_D-s_E.
\]

Equations (1.5) and (1.9) give the exact integer lower bound

\[
\boxed{m=k+1+h_D-h_E\ge k+1\ge2.}
\tag{2.1}
\]

Using (1.4) in the definition of the Macaulay raise gives

\[
\Lambda_{2,q}(D)-\Lambda_{2,q}(E)
=\binom{v_E}{3}-\binom{v_D}{3}
+\binom{\rho_E}{2}-\binom{\rho_D}{2}.
\tag{2.2}
\]

If `m>=3`, then (1.3), monotonicity, and `v_D/q->1` give

\[
\begin{aligned}
\Lambda_{2,q}(D)-\Lambda_{2,q}(E)
&\ge \binom{v_D+3}{3}-\binom{v_D}{3}
     -\binom{v_D-1}{2}\\
&=v_D(v_D+3).
\end{aligned}
\tag{2.3}
\]

Therefore

\[
\liminf\frac{\gamma_4}{q^2}
\ge1-\frac12=\frac12>0.
\tag{2.4}
\]

Every putative bad sequence must consequently have `m=2` eventually.
Equation (2.1) then forces the rigid discrete phase

\[
\boxed{k=1,qquad h_D=h_E=:h.}
\tag{2.5}
\]

This already rules out every sequence on which `k` diverges, and every
sequence whose two cap depths acquire unequal next-order corrections.

## 3. Only two equal-correction phases exist

Specialize (1.6)--(1.7) to `k=1`.  Equal minimal correction `h` requires

\[
R_D(h)\ge0,qquad R_E(h-1)<0.
\tag{3.1}
\]

The exact expressions are

\[
2R_D(h)=2hq-h^2-2hu-7h-2u^2-12u-18,
\tag{3.2}
\]

\[
2R_E(h-1)=2hq-h^2-2hu-h-2q-u^2-7u-10.
\tag{3.3}
\]

For the interval in (3.1) to be nonempty, (3.2)--(3.3) necessarily give

\[
(2h-4)q<h^2+2hu-5h+2u+2.
\tag{3.4}
\]

Here `h<=s_D=o(q)` and `u=o(q)`.  If `h>=3`, divide (3.4) by `hq`:
the left side is at least `2/3`, while the right side tends uniformly to
zero.  Hence every bad sequence in (2.5) has, eventually,

\[
\boxed{h\in\{1,2\}.}
\tag{3.5}
\]

## 4. Exact sign in the last two phases

Substituting the canonical words (1.4) into (1.1) gives an exact polynomial
in each remaining phase.

### Phase `h=1`

The cap condition `R_D(1)>=0` is

\[
u^2+7u+13\le q.
\tag{4.1}
\]

The exact surplus is

\[
\boxed{
\gamma_4=
\frac{4q^2+4qu^2-4qu-12q
-3u^4-34u^3-141u^2-318u-328}{8}.}
\tag{4.2}
\]

Along any sequence in this phase, pass to a subsequence on which
`x=u^2/q` converges.  Equation (4.1) gives `0<=x<=1`, and (4.2) yields

\[
\frac{\gamma_4}{q^2}
\longrightarrow
\frac12+\frac x2-\frac{3x^2}{8}.
\tag{4.3}
\]

The right side is at least `1/2` on `[0,1]`.  Thus this phase is eventually
strictly positive.

### Phase `h=2`

Now `R_D(2)>=0` and `R_E(1)<0` are exactly

\[
u^2+8u+18\le2q<u^2+11u+16.
\tag{4.4}
\]

In particular `u^2/q->2`.  The exact surplus is

\[
\boxed{
\gamma_4=
\frac{4q^2+8qu^2+8qu+44q
-3u^4-38u^3-181u^2-506u-656}{8}.}
\tag{4.5}
\]

Dividing by `q^2` and using (4.4) gives

\[
\frac{\gamma_4}{q^2}\longrightarrow
\frac12+2-\frac{3\cdot4}{8}=1>0.
\tag{4.6}
\]

This eliminates the final equal-correction phase.

## 5. Proposed consequence and firewall

Assume an unbounded nonpositive sequence exists on the fixed slice `c=2`.
Proposition 5.3 and the audited boundary handoff give (0.1).  Sections 1--2
force (2.5); Section 3 forces (3.5); and Section 4 makes both remaining
phases strictly positive.  This is a contradiction.  Therefore the exact
cap-depth argument proposes the strengthened conclusion

\[
\boxed{
\exists Q_2\ \forall q\ge Q_2:\quad
\text{every admissible fixed-}c=2\text{ no-borrow point has }\gamma_4>0.}
\tag{5.1}
\]

Combined with the already audited fixed-`c>=3` theorem, this would give
eventual positivity for every **fixed** promotion count `c>=2`, with a
threshold allowed to depend on `c`.

The limitations are unchanged in the directions that matter for Erdős
#776:

- (5.1) is a post-freeze scratch theorem and needs an author-swapped audit
  before promotion;
- it is not uniform in `c` and gives no control when `c=c(q)` grows;
- it concerns the complementary relaxed no-borrow bridge only;
- it neither proves the adaptive bridge nor proves or refutes Erdős #776.

