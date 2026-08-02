# Signed residual factorial energy and the common-\(X\) reciprocal frame

Date: 2026-08-02  
Status: **AUTHOR-FROZEN / PROVED IN THIS NOTE / NOT BLIND-AUDITED / NOT IN FINAL CLAIM LEDGER**  
Public-problem status: **Erdős #1083 remains open; no distance exponent improvement is claimed.**

## 0. Outcome

The signed residual gate has an exact nonnegative integer potential.  It neither assumes
that the centre tiles a finite quotient nor assumes a cyclotomic or tensor normal form.

Let \(\Gamma\) be a finitely generated torsion-free abelian group.  For a finite
set \(A\subset\Gamma\), write \(P_A=\sum_{a\in A}[a]\).  Suppose

\[
 1\le S=|A_0|=|A_j|,\qquad q_j\in\mathbb Z[\Gamma],\qquad q_j(1)=C>0,
\tag{0.1}
\]

and there are masks \(M,N_j\) such that

\[
 \boxed{P_{A_j}q_j=P_M,\qquad P_{A_0}q_j=P_{N_j}},
 \qquad |M|=|N_j|=SC.
\tag{0.2}
\]

The exact-block application is pinned to equations (0.3)--(0.4) of
`data/research_open/q1_six_hour_campaign_2026-08-02/erdos1083/POWER_LARGE_SIMULTANEOUS_SWITCH_CORE.md`.
There \(F_j=GR_j=P_{\lambda_jX}\), \(P_{A_0^{\rm comp}}=GB\),
\(B=R_jQ_j\), and \(P_{A_j^{\rm comp}}=F_0Q_j\).  Hence cancellation gives the
literal two-product interface

\[
 F_jQ_j=GB=P_{A_0^{\rm comp}},\qquad
 F_0Q_j=P_{A_j^{\rm comp}}.
\tag{0.3a}
\]

Thus the notation in this note is exactly

\[
 A_j=\lambda_jX,\qquad A_0=\lambda_0X,\qquad
 M=A_0^{\mathrm{comp}},\qquad N_j=A_j^{\mathrm{comp}},\qquad q_j=Q_j,
\tag{0.3}
\]

using \(F_jQ_j=P_{A_0^{\mathrm{comp}}}\) and
\(F_0Q_j=P_{A_j^{\mathrm{comp}}}\) from the simultaneous-switch normal form.

Define the **factorial energy**

\[
 \boxed{\delta(q):=\frac12\sum_{g\in\Gamma}q(g)(q(g)-1).}
\tag{0.4}
\]

Then:

1. \(\delta(q)\in\mathbb Z_{\ge0}\), and under (0.2),
   \(\delta(q)=0\) exactly when \(q\) is a \(C\)-term mask.  Every signed
   residual pays \(\delta(q)\ge1\).
2. If \(q\) is signed, every mask multiplier of size \(S\) pays the exact
   negative autocorrelation debt

   \[
   \sum_{\substack{a,b\in A\\a\ne b}}
       \mathrm{Corr}_q(b-a)=-2S\delta(q)\le-2S.
   \tag{0.5}
   \]

   Hence the two homothetic copies in (0.2) carry exactly the same debt.
3. On a sufficiently large elementary prime quotient, every \(S\)-term mask is
   Fourier-invertible.  Parseval gives an exact reciprocal-frame formula for each debt
   and for their sum over all rows.
4. There is a \(C\)-term mask \(R\) with

   \[
   \boxed{\|q-P_R\|_1\le2\delta(q).}
   \tag{0.6}
   \]

   Thus the same integer is also a stability/edit-distance potential.

This converts the signed gate into a quantitative target: prove that the common-\(X\)
reciprocal-frame excess is \(o(K)\), and all but \(o(K)\) rows become direct
mask quotients.  The present note proves the conversion, not that final spectral bound.

## 1. The factorial-energy lemma

For an integral finite-support function \(q\), let

\[
 N_-(q)=\sum_{q(g)<0}|q(g)|,\qquad
 E_+(q)=\sum_{q(g)>0}(q(g)-1).
\tag{1.1}
\]

### Lemma 1.1

If \(q(1)=C>0\), then

\[
 \delta(q)=\sum_{q(g)>0}\binom{q(g)}2
 +\sum_{q(g)<0}\binom{|q(g)|+1}2
 \ge E_+(q)+N_-(q).
\tag{1.2}
\]

In particular \(\delta(q)\) is a nonnegative integer.  It vanishes exactly when
every coefficient is zero or one.  If \(q\) is signed, then
\(\delta(q)\ge N_-(q)\ge1\).

#### Proof

For a positive integer \(n\), \(n(n-1)/2=\binom n2\); for a negative
coefficient \(-m\), \((-m)(-m-1)/2=\binom{m+1}2\).  Moreover
\(\binom n2\ge n-1\) and \(\binom{m+1}2\ge m\).  Summing proves all
claims. QED.

If a nonnegative integral \(q\) satisfies \(P_Aq\) is a mask and
\(A\ne\varnothing\), then \(q\) must itself be a mask: a coefficient at least
two would survive in any translate by an element of \(A\), and two positive
representations would make a product coefficient at least two.  Consequently, under
(0.2),

\[
 q\text{ signed}\quad\longleftrightarrow\quad
 q\text{ is not a mask}\quad\longleftrightarrow\quad\delta(q)\ge1.
\tag{1.3}
\]

### Lemma 1.2 (edit stability)

Assume that \(\Gamma\) is infinite.  There is a \(C\)-term mask \(P_R\)
satisfying (0.6).  In the application, \(S\ge2\) and an \(S\)-element subset of a
torsion-free group forces \(\Gamma\) to be nontrivial and hence infinite.  If
\(\Gamma\) is trivial under the full hypotheses (0.1)--(0.2), necessarily
\(S=C=1\) and \(q=1\), so the conclusion is immediate without adding points.

#### Proof

Put \(P=C+N_-\) for the total positive mass and let \(r\) be the number of
positive support points.  Then \(E_+=P-r\), so
\(r=C+N_--E_+\).  If \(r\ge C\), retain any \(C\) positive support
points in \(R\); the \(\ell^1\) distance is \(2N_-\).  If \(r<C\),
retain all positive support points and add \(C-r\) new points; the distance is
\(2E_+\).  In either case it is
\(2\max\{N_-,E_+\}\le2\delta(q)\) by (1.2). QED.

## 2. Exact autocorrelation debt

Use

\[
 \mathrm{Corr}_q(d)=\sum_{g\in\Gamma}q(g)q(g-d).
\tag{2.1}
\]

### Theorem 2.1

If \(|A|=S\), \(q(1)=C\), and \(P_Aq\) is a mask, then

\[
 \boxed{
 \sum_{\substack{a,b\in A\\a\ne b}}
 \mathrm{Corr}_q(b-a)=-2S\delta(q).}
\tag{2.2}
\]

#### Proof

The product is a mask of augmentation \(SC\), hence its squared coefficient norm
is also \(SC\).  Expanding that norm gives

\[
\begin{aligned}
 SC=\|P_Aq\|_2^2
 &=\sum_g\left(\sum_{a\in A}q(g-a)\right)^2\\
 &=S\|q\|_2^2+\sum_{a\ne b}\mathrm{Corr}_q(b-a).
\end{aligned}
\tag{2.3}
\]

But

\[
 \|q\|_2^2-C=\sum_gq(g)(q(g)-1)=2\delta(q).
\tag{2.4}
\]

Substitution proves (2.2). QED.

Applying Theorem 2.1 to both products in (0.2) gives

\[
 \sum_{a\ne b\in A_j}\mathrm{Corr}_{q_j}(b-a)
 =\sum_{a\ne b\in A_0}\mathrm{Corr}_{q_j}(b-a)
 =-2S\delta(q_j).
\tag{2.5}
\]

For \(A_j=\lambda_jX\), this is an exact equality between the correlation
charges on \(\lambda_j(X-X)\) and \(\lambda_0(X-X)\).  It is the promised
explicit local object on which a coarea/averaging argument could act.

### Theorem 2.2 (cancellation forces a popular source difference)

Let \(A\) be finite with \(S=|A|\ge2\).  Define its largest nonzero ordered-difference
multiplicity by

\[
 \mu(A)=\max_{d\ne0}|\{(a,b)\in A^2:b-a=d\}|.
\tag{2.6}
\]

Suppose \(q\) is signed, put \(N=N_-(q)\), and assume only that \(P_Aq\)
is coefficientwise nonnegative; collisions are allowed.
Then some difference between a positive and a negative coefficient of \(q\),
say \(d=r-v\ne0\), satisfies

\[
 \boxed{|A\cap(A-d)|\ge\frac{S}{C+N}.}
\tag{2.7}
\]

Consequently

\[
 \boxed{
 \delta(q)\ge N\ge
 \max\left\{1,\left\lceil\frac{S}{\mu(A)}\right\rceil-C\right\}.}
\tag{2.8}
\]

#### Proof

Write \(q=q^+-q^-\), with disjoint nonnegative integral parts, and put

\[
 U=P_Aq^+,\qquad V=P_Aq^-.
\tag{2.9}
\]

Because \(U-V=P_Aq\) is coefficientwise nonnegative, \(U\ge V\).  Since \(U,V\)
are integral,

\[
 \langle U,V\rangle\ge\sum_zV(z)^2\ge\sum_zV(z)=SN.
\tag{2.10}
\]

On the other hand, expanding by a positive coefficient at \(r\) and a
negative coefficient of magnitude \(q^-(v)\) at \(v\) gives

\[
 \langle U,V\rangle
 =\sum_{r,v}q^+(r)q^-(v)
   |\{(a,b)\in A^2:b-a=r-v\}|.
\tag{2.11}
\]

The supports of \(q^+\) and \(q^-\) are disjoint, so every \(r-v\) here is
nonzero.  The total weight in (2.11) is

\[
 \left(\sum_rq^+(r)\right)\left(\sum_vq^-(v)\right)
 =(C+N)N.
\tag{2.12}
\]

The weighted average of the displayed difference multiplicities is therefore
at least \(SN/((C+N)N)=S/(C+N)\), proving (2.7).  Bounding every term by
\(\mu(A)\) gives \(S\le\mu(A)(C+N)\).  Now use integrality and
\(\delta(q)\ge N\ge1\) from Lemma 1.1. QED.

For the common-\(X\) interface, nonzero scalar multiplication preserves all
ordered-difference multiplicities, so

\[
 \mu(A_j)=\mu(\lambda_jX)=\mu(X).
\tag{2.13}
\]

Thus every signed row in (0.2) pays at least

\[
 L_X:=\max\left\{1,\left\lceil\frac{S}{\mu(X)}\right\rceil-C\right\},
\tag{2.14}
\]

and (3.4) below implies the strengthened count

\[
 \#\{j:q_j\text{ signed}\}
 \le \frac{\text{reciprocal-frame excess}}{2L_X}.
\tag{2.15}
\]

Equivalently, a signed row either spends large factorial energy or certifies a
popular nonzero difference of \(X\).  For a Sidon difference set
\(\mu(X)=1\), the cost is \(\delta(q)\ge S-C\).  At the endpoint
\(S=t^{7/9+o(1)}\), \(C=t^{1/18+o(1)}\), even the minimum-debt case
\(\delta=1\) forces a difference with at least
\(S/(C+1)=t^{13/18+o(1)}\) ordered representations.

In the signed minimum-debt case there is a sharper normal form.  If \(q\)
is signed, equality \(\delta(q)=1\) in Lemma 1.1 forces

\[
 q=P_R-[v],\qquad v\notin R,\qquad |R|=C+1.
\tag{2.16}
\]

Indeed there is exactly one coefficient \(-1\), and every positive coefficient
equals one.  Coefficientwise nonnegativity of
\(P_Aq=P_AP_R-P_{A+v}\) then gives the literal cover

\[
 \boxed{A+v\subseteq A+R,
 \qquad A\subseteq\bigcup_{r\in R}(A+r-v).}
\tag{2.17}
\]

For the two-product interface (0.2), the **same** \(C+1\) shifts \(R-v\) cover
both \(A_0\) and \(A_j\).  Thus the endpoint minimum-debt branch is not merely a
popular-difference statement: it has an explicit common finite cancellation
alphabet for the centre and leaf scalar copies.

This alphabet is common only to the centre/leaf pair belonging to one residual
\(q_j\); it may vary with \(j\).  Neither cross-row synchronization nor new
distinct distance labels follow from the cover alone.  Those are precisely the
remaining power-large steps.

### Theorem 2.3 (stable collision ledger)

The exact-mask hypothesis is not needed for the underlying conservation law.
For any integral \(q\) with \(q(1)=C\), any \(S\)-term mask \(P_A\), and
\(H=P_Aq\),

\[
 \boxed{
 \sum_{a\ne b\in A}\operatorname{Corr}_q(b-a)
 =2\delta(H)-2S\delta(q).}
\tag{2.18}
\]

Consequently, if \(A,B\) are two \(S\)-term masks, then

\[
 \boxed{
 \operatorname{Off}_A(q)-\operatorname{Off}_B(q)
 =2\bigl(\delta(P_Aq)-\delta(P_Bq)\bigr),}
\tag{2.19}
\]

where \(\operatorname{Off}_A\) denotes the ordered off-diagonal correlation
sum.  In particular, if both output defects are at most \(\varepsilon\), their
debts differ by at most \(2\varepsilon\); and if \(q\) is signed while
\(\delta(P_Aq)\le\varepsilon\), then

\[
 \operatorname{Off}_A(q)\le 2\varepsilon-2S.
\tag{2.20}
\]

#### Proof

The norm expansion (2.3) is valid without positivity.  Since
\(H(1)=SC\),

\[
 2\delta(H)=\|H\|_2^2-SC
 =S(\|q\|_2^2-C)+\operatorname{Off}_A(q)
 =2S\delta(q)+\operatorname{Off}_A(q).
\tag{2.21}
\]

Rearrange, subtract the identities for \(A,B\), and use
\(\delta(q)\ge1\) in the signed case. QED.

This supplies a precise outer-stability target.  If the near-extremal cleaning
step produces integral row products with total factorial defect \(o(SK)\), the
exact correlation debts survive with the same quantitative error.  What is
still missing is the geometric extraction theorem that bounds this algebraic
defect from the original number of exceptional distance cells.

## 3. Prime-shadow reciprocal-frame identity

Choose a prime \(p>S\) so large that reduction
\(\pi_p:\Gamma\to H:=\Gamma/p\Gamma\) is injective, separately, on every one of
the finite supports

\[
 A_0,\ A_1,\ldots,A_K,\ \operatorname{supp}q_1,\ldots,
 \operatorname{supp}q_K,\ M,\ N_1,\ldots,N_K.
\tag{3.0}
\]

Such primes exist after identifying \(\Gamma\cong\mathbb Z^r\): exclude the
finitely many prime divisors which make a nonzero coordinate-difference vector
from one of these supports vanish modulo \(p\), and also require \(p>S\).
Support injectivity preserves every coefficient and hence the augmentation and
the \(\ell^2\) norm of each listed object.  Reduction is a group-ring
homomorphism, so it sends the two convolution identities (0.2) to convolution
identities on \(H\); injectivity on \(M,N_j\) makes their images masks, while
injectivity on \(q_j\) gives
\(\|\pi_p(q_j)\|_2=\|q_j\|_2\).  These are precisely the preservation facts used
below; no finite-tiling property is assumed.
Use the unnormalized Fourier transform

\[
 \hat f(\chi)=\sum_{h\in H}f(h)\overline{\chi(h)}.
\tag{3.1}
\]

### Lemma 3.1 (automatic invertibility)

Every mask \(P_A\) with \(0<|A|=S<p\) has
\(\hat P_A(\chi)\ne0\) for every \(\chi\in\hat H\).

#### Proof

For a nontrivial character, all values are powers of a primitive \(p\)-th root
\(\zeta\).  If their \(S\)-term sum vanished, a polynomial
\(\sum_{k=0}^{p-1}n_kz^k\) with nonnegative integral coefficients and total
mass \(S<p\) would vanish at \(\zeta\).  It would be a multiple of
\(\Phi_p=1+z+\cdots+z^{p-1}\), forcing its mass to be a positive multiple of
\(p\), a contradiction.  The trivial transform equals \(S\). QED.

### Theorem 3.2 (rowwise and aggregate identities)

For every row in (0.2),

\[
 \boxed{
 2\delta(q_j)=\frac1{|H|}\sum_{\chi\in\hat H}
 \frac{|\hat P_M(\chi)|^2}{|\hat P_{A_j}(\chi)|^2}-C.}
\tag{3.2}
\]

The second positive multiplier gives

\[
 \boxed{
 2S\delta(q_j)=\frac1{|H|}\sum_{\chi\in\hat H}
 (S-|\hat P_{A_0}(\chi)|^2)
 \frac{|\hat P_M(\chi)|^2}{|\hat P_{A_j}(\chi)|^2}.}
\tag{3.3}
\]

Consequently

\[
 \boxed{
 2\sum_{j=1}^K\delta(q_j)
 =\frac1{|H|}\sum_{\chi}|\hat P_M(\chi)|^2
 \sum_{j=1}^K\frac1{|\hat P_{A_j}(\chi)|^2}-KC.}
\tag{3.4}
\]

In particular the number of signed rows is at most one half of the right-hand
reciprocal-frame excess in (3.4), and Theorem 2.2 improves the denominator from
\(2\) to \(2L_X\).

#### Proof

Fourier inversion of \(P_{A_j}q_j=P_M\), using Lemma 3.1, gives
\(\hat q_j=\hat P_M/\hat P_{A_j}\).  Parseval and (2.4) give (3.2).
Also

\[
 \frac1{|H|}\sum_\chi
 |\hat P_{A_0}|^2\frac{|\hat P_M|^2}{|\hat P_{A_j}|^2}
 =\|P_{A_0}q_j\|_2^2=SC.
\tag{3.5}
\]

Subtract (3.5) from \(S\) times (3.2), and sum over \(j\), to obtain
(3.3)--(3.4).  Finally each signed row has \(\delta(q_j)\ge1\). QED.

The summand in (3.3) is not pointwise nonnegative.  Its **total** is the nonnegative
even integer \(2S\delta(q_j)\).  Replacing this exact cancellation by a pointwise
positivity assertion would repeat the signed-residual error that this potential avoids.

## 4. Sharp transversality and common-\(X\) scope counterexamples

### 4.1 The existing full-transverse Euclidean no-go has minimum debt

The all-parameter construction in
`data/research_open/q1_six_hour_campaign_2026-08-02/erdos1083/SIMULTANEOUS_POSITIVE_COMPLEMENT_NO_GO.md`
already shows that one transverse row cannot force \(\delta=0\).  For every
\(S\ge4\), in independent Laurent variables put

\[
 P_S(z)=1+z+\cdots+z^{S-1},\qquad
 Q_S(x,y)=x+y-xy+xy^S+x^Sy.
\tag{4.1}
\]

Both \(P_S(x)Q_S\) and \(P_S(y)Q_S\) are \(3S\)-term masks, while

\[
 Q_S(1,1)=3<S,\qquad \|Q_S\|_2^2=5,
 \qquad\boxed{\delta(Q_S)=1.}
\tag{4.2}
\]

After the irrational exponent embedding in that manuscript,
\(P_S(x)=P_{\lambda_0X}\) and \(P_S(y)=P_{\lambda_1X}\) are scalar copies of
one \(S\)-point set, their rational Newton spaces are transverse, the two full
complements are masks, and the model has a genuine Euclidean realization and a
literal common tangent.  Theorem 2.1 adds the exact new ledger

\[
 \sum_{a\ne b\in\lambda_0X}\operatorname{Corr}_{Q_S}(b-a)
 =\sum_{a\ne b\in\lambda_1X}\operatorname{Corr}_{Q_S}(b-a)
 =-2S.
\tag{4.3}
\]

Thus even **full geometric transversality** permits the smallest possible signed
debt.  Any successful use of (3.4) must be genuinely power-large: it must compare
many rows through their one common mask/divisor lattice, not prove a positive
rowwise spectral gap.

### 4.2 A tiny common-mask reciprocal-frame equality case

Put

\[
 X=\{0,1,2\},\quad F_0=1+x+x^2,\quad
 F_1=1+x^2+x^4,\quad M=F_1.
\tag{4.4}
\]

Then

\[
 q_0=1-x+x^2,\qquad q_1=1
\tag{4.5}
\]

have augmentation \(C=1<S=3\) and

\[
 F_0q_0=F_1=M,\qquad F_1q_1=M,\qquad
 F_0q_1=F_0.
\tag{4.6}
\]

Thus one common mask has complementary quotients by two genuine scalar copies
\(P_X\) and \(P_{2X}\), and both quotients also become masks after multiplication
by the fixed \(F_0\).  Nevertheless \(q_0\) is signed and
\(\delta(q_0)=1\), the smallest possible debt.

This refutes any inference from “common mask + common-\(X\) scalar copies + both
positive products” to quotient positivity.  It does **not** refute the exact-block target:

\[
 F_1=F_0(1-x+x^2),\qquad \gcd(F_0,F_1)=F_0,
\tag{4.7}
\]

so this tiny equality case fails transversality/coprimality maximally and has only two
rows.  Section 4.1 supplies the stronger full-transverse rowwise firewall.  Together they
pin the remaining algebraic task down to the **simultaneous power-large** interface: use
the common divisor family to upper-bound (3.4), or force the negative debts (2.5) to
create new distance labels.

## 5. Quantifier firewall

Proved here:

- the all-parameter factorial-energy, autocorrelation, edit-stability, and prime-shadow
  identities under (0.1)--(0.2);
- the popular-difference amplifier (2.7)--(2.15), including the Sidon cost and
  the endpoint \(t^{13/18+o(1)}\) overlap in the minimum-debt branch;
- the minimum-debt common cancellation alphabet (2.16)--(2.17);
- the stable collision ledger (2.18)--(2.21), which identifies the exact
  algebraic error quantity needed by an outer near-extremal cleaning theorem;
- automatic Fourier invertibility on a sufficiently large elementary prime quotient;
- the new observation that the existing full-transverse Euclidean signed switch has
  exactly the minimum factorial debt \(\delta=1\), together with a two-row common-mask
  reciprocal-frame equality case.

Not proved here:

- an \(o(K)\) upper bound for the reciprocal-frame excess (3.4);
- any consequence of centre--leaf transversality for that excess;
- extraction of the literal exact block from a near-extremal point configuration;
- Erdős #1083 or any improvement of \(N^{3/5-o(1)}\) in dimension three.

## 6. Reproduction

```bash
python3 verify_signed_residual_factorial_energy.py
python3 -m unittest -v test_signed_residual_factorial_energy.py
```

The verifier checks exact random finite-support instances of the combinatorial identities,
the edit bound, the prime-shadow nonvanishing and both Fourier formulas, the aggregate
charge, and the sharp common-\(X\) scope counterexample.
