# Erdős #1083: a quadratic bound for the cyclotomic simultaneous-positive-multiple model

Date: 2026-08-02

Status: **PROVED — INDEPENDENT CROSS-AUDIT PASSED**

## 0. Outcome

Let \(S\) be prime and let \(M\) be a positive integer with
\(S\nmid M\). In independent Laurent directions \(x,y\), put

\[
 F_0=P_S(x),\qquad F_m=P_S(y^m)\quad(m\mid M),
 \qquad P_r(z)=1+z+\cdots+z^{r-1}.
\tag{0.1}
\]

Let \({\cal D}\subseteq\{m:m\mid M\}\), and let \(Q\) be an arbitrary
integral Laurent polynomial, possibly signed and involving additional
variables. For \(m\in{\cal D}\), define

\[
 R_m=\frac{F_M}{F_m}Q.
\tag{0.2}
\]

Assume only that every simultaneous positive multiple

\[
 B_m:=F_0R_m
\tag{0.3}
\]

is a \(0/1\) mask and that

\[
 1\le R_m(1)=C<S.
\tag{0.4}
\]

Neither \(Q\) nor \(R_m\) is assumed nonnegative.  The lower bound in
(0.4) excludes the vacuous zero mask; without it, \(Q=0\) would make an
arbitrary \({\cal D}\) a trivial counterexample.  Then

\[
 \boxed{
 |{\cal D}|\le
 1+2\sum_{r=2}^{C}\varphi(r)\le C^2.}
\tag{0.5}
\]

More precisely, for every \(m,n\in{\cal D}\), if

\[
 g=(m,n),\qquad a=m/g,\qquad b=n/g,
\tag{0.6}
\]

then

\[
 \boxed{a\le C,\qquad b\le C.}
\tag{0.7}
\]

At the frozen endpoint \(C=t^{1/18+o(1)}\), (0.5) is

\[
 |{\cal D}|\le t^{1/9+o(1)},
\tag{0.8}
\]

which rules out the required \(t^{5/9-o(1)}\) family by a polynomial
margin. Thus the same-line cyclotomic construction cannot realize the
power-large contaminated branch, even by hiding signed quotients behind
the common positive multiplier \(P_S(x)\).

The theorem is stronger than the earlier prime-valuation barrier. That
barrier treats one cyclotomic zero at a time. Here all zeros in the
reduced scale ratio \(m/(m,n)\) are combined, and positivity is recovered
from a cyclic shadow of \(P_S(x)R_m\), rather than incorrectly assumed for
\(R_m\) itself.

## 1. A sharp positive-multiple mass lemma

For integers \(a\ge1\) with \((a,S)=1\), define

\[
 H_{S,a}(z)=\frac{P_S(z^a)}{P_S(z)}\in\mathbb Z[z].
\tag{1.1}
\]

### Lemma 1.1

If a nonzero Laurent polynomial \(A\) has nonnegative integer
coefficients and \(H_{S,a}\mid A\), then

\[
 \boxed{A(1)\ge\min\{S,a\}.}
\tag{1.2}
\]

The same statement holds for \(H_{S,a}(y^g)\) in a multivariable
Laurent ring: collect the other monomials and the exponent of \(y\)
modulo \(g\), and apply (1.2) to any nonzero fibre.

#### Proof

Multiplying by a monomial if necessary, reduce the exponents of \(A\)
modulo \(N=Sa\). This gives a nonzero function

\[
 f:\mathbb Z/N\mathbb Z\longrightarrow\mathbb Z_{\ge0}
\tag{1.3}
\]

with total mass \(A(1)\). Reduction can merge coefficients but cannot
change their total mass.

The roots of \(H_{S,a}\) among the \(N\)-th roots of unity are all
roots of \(P_S(z^a)\) except the cancelled nontrivial \(S\)-th roots.
Consequently the Fourier support of \(f\) is contained in

\[
 \{\xi:\xi^a=1\}\ \cup\
 \{\xi:\xi^S=1,\ \xi\ne1\}.
\tag{1.4}
\]

Under the Chinese-remainder identification

\[
 \mathbb Z/(Sa)\mathbb Z
 \simeq \mathbb Z/a\mathbb Z\times\mathbb Z/S\mathbb Z,
\tag{1.5}
\]

the set (1.4) is the union of the two frequency axes. Fourier inversion
therefore gives the rectangular identity

\[
 f(i,j)+f(i',j')=f(i,j')+f(i',j)
 \qquad(i,i'\bmod a,\ j,j'\bmod S).
\tag{1.6}
\]

If every entry is positive, the mass is at least \(aS\). Otherwise
choose \(f(i_0,j_0)=0\). Equation (1.6) becomes

\[
 f(i,j)=f(i,j_0)+f(i_0,j).
\tag{1.7}
\]

If some entry in the distinguished column is positive, its contribution
is repeated across all \(S\) columns, giving mass at least \(S\). If
not, nonzeroness forces a positive entry in the distinguished row, which
is repeated across all \(a\) rows, giving mass at least \(a\). This
proves (1.2).

The bound is sharp in both regimes:

\[
 H_{S,a}(z)P_a(z)=P_a(z^S),\qquad
 H_{S,a}(z)P_S(z)=P_S(z^a).
\tag{1.8}
\]

The first right side has \(a\) terms and the second has \(S\). QED.

## 2. The cyclic shadow recovers positivity from a signed quotient

The main point is that Lemma 1.1 can be applied even when \(R_m\) is
signed.

### Lemma 2.1 (prime cyclic shadow)

Let \(R\) be an integral Laurent polynomial in \(x\) and any other
variables. Suppose

\[
 B=P_S(x)R
\tag{2.1}
\]

is a \(0/1\) mask with \(B(1)=SC\). Reduce the exponent of \(x\)
modulo \(S\). Then there is a nonnegative integral Laurent polynomial
\(K\), in the remaining variables, such that

\[
 \boxed{\overline B=P_S(x)K,\qquad K(1)=C.}
\tag{2.2}
\]

Moreover, if a polynomial \(H\) independent of \(x\) divides \(B\),
then \(H\mid K\).

#### Proof

Fix one monomial in all variables other than \(x\), and let
\(c_0,\ldots,c_{S-1}\) be the nonnegative counts in the \(S\) residue
classes of the \(x\)-exponent. At a primitive \(S\)-th root
\(\omega\), (2.1) gives

\[
 \sum_{r=0}^{S-1}c_r\omega^r=0.
\tag{2.3}
\]

Since \(S\) is prime, the minimal polynomial of \(\omega\) is
\(P_S\), of degree \(S-1\). Hence all \(c_r\) are equal. Doing this
for every remaining monomial gives (2.2), and augmentation gives
\(K(1)=C\).

If \(B=HT\) and \(H\) is independent of \(x\), collect the coefficients
of \(T\) in each \(x\)-residue class. Every corresponding coefficient
of \(\overline B\), in particular the common coefficient \(K\), remains
a multiple of \(H\). QED.

This step is exactly what preserves the clean/contaminated firewall:
it does not claim \(R\ge0\). It extracts a separate nonnegative shadow
from the positive product \(P_S(x)R\).

## 3. Pairwise scale rigidity

Take \(m,n\in{\cal D}\), and use (0.6). Since

\[
 F_mR_m=F_MQ=F_nR_n,
\tag{3.1}
\]

cancellation of \(F_g\) gives

\[
 H_{S,a}(y^g)R_m=H_{S,b}(y^g)R_n.
\tag{3.2}
\]

The two displayed \(H\)-factors are coprime. Indeed,

\[
 F_r=\prod_{d\mid r}\Phi_{Sd}(y)
 \qquad(S\nmid r),
\tag{3.3}
\]

and a common cyclotomic factor would be indexed by a divisor of both
\(m\) and \(n\) which does not divide \(g\), an impossibility. Euclid's
lemma applied to (3.2) therefore gives

\[
 H_{S,a}(y^g)\mid R_n,
 \qquad H_{S,b}(y^g)\mid R_m.
\tag{3.4}
\]

In particular the first factor divides the positive mask
\(B_n=P_S(x)R_n\). Apply Lemma 2.1 to obtain a nonnegative shadow
\(K_n\) of mass \(C\), still divisible by \(H_{S,a}(y^g)\). Lemma 1.1
now yields

\[
 C\ge\min\{S,a\}.
\tag{3.5}
\]

Because \(C<S\), this forces \(a\le C\). Interchanging \(m,n\) gives
\(b\le C\), proving (0.7).

Fix \(m_0\in{\cal D}\). Each \(m\in{\cal D}\) determines its reduced
fraction

\[
 \frac m{m_0}=\frac{a_m}{b_m},\qquad
 (a_m,b_m)=1,\qquad 1\le a_m,b_m\le C.
\tag{3.6}
\]

Distinct \(m\)'s give distinct fractions. The number of coprime
ordered pairs in the \(C\)-by-\(C\) square is

\[
 1+2\sum_{r=2}^{C}\varphi(r)\le C^2,
\tag{3.7}
\]

which proves (0.5).

## 4. A nonempty sharp-boundary family

The theorem rules out a power-large family, not every family. If
\(M<S\), take the positive \(M\)-term regularizer

\[
 Q=P_M(y).
\tag{4.1}
\]

Then for every \(m\mid M\), writing \(r=M/m\),

\[
 \boxed{
 F_MQ=P_{SM}(y),\qquad
 \frac{F_M}{F_m}Q=P_m(y)P_r(y^{Sm}).}
\tag{4.2}
\]

Both are direct \(0/1\) masks, so all \(\tau(M)\) divisors work with
\(C=M<S\). This realizes the small-prime mechanism exactly, but

\[
 \tau(M)=\exp\!\left(O\!\left(\frac{\log M}{\log\log M}\right)\right)
 =C^{o(1)},
\tag{4.3}
\]

far below the endpoint demand. Formula (4.2) also shows that the
positive-multiple mass bound \(a\) in Lemma 1.1 is the correct local
scale.

## 5. Exact boundary

This closes the same-line cyclotomic simultaneous-positive-multiple
model, including quotients \(R_m\) which are themselves signed but are
made positive by the common centre mask \(P_S(x)\). It does not prove
that an arbitrary complementary-divisor family \(R_j\mid B\) is
cyclotomic or one-dimensional, and it does not close the full
contaminated branch of POWER_LARGE_SIMULTANEOUS_SWITCH_CORE.md.

The next exact obstruction is therefore no longer “small primes” in this
model. It is a genuinely multidirectional signed-switch family in which
the common heavy divisor has no reduction to the ratios
\(P_S(y^m)/P_S(y^g)\). Any future construction must evade the cyclic
shadow bound, not merely use many powers of primes at most \(C\).

## 6. Reproduction

~~~bash
python3 verify_cyclotomic_simultaneous_positive_multiple_bound.py
python3 -m unittest -v test_cyclotomic_simultaneous_positive_multiple_bound.py
~~~

The verifier checks the sharp polynomial identities, finite CRT matrix
instances, the signed cyclic-shadow mechanism, the exact divisor-family
construction, pairwise coprimality/divisibility, and the endpoint exponent
gap. The all-parameter result is the proof above.
