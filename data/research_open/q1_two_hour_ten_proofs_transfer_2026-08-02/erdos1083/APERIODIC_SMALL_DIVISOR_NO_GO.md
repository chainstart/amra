# An aperiodic five-term mask with vanishing Fourier conditioning

Date: 2026-08-02  
Status: **AUTHOR-FROZEN / PROVED IN THIS NOTE / NOT BLIND-AUDITED / NOT IN FINAL CLAIM LEDGER**  
Public-problem status: **Erdős #1083 remains open.**

## 0. Result

Put

\[
 P(x)=1+x+x^3+x^5+x^6=P_{\{0,1,3,5,6\}}(x).
\tag{0.1}
\]

Then:

1. \(P\) has no root-of-unity zero, so this five-point source has no finite
   cyclic tiling shadow of the type used in the previous campaign;
2. \(P\) nevertheless has a zero \(z_0\) on the complex unit circle;
3. that zero is not a root of unity; and
4. if

   \[
   \sigma_n(P)=\min_{\zeta^n=1}|P(\zeta)|,
   \tag{0.2}
   \]

   then for every \(n\ge1\),

   \[
   \boxed{0<\sigma_n(P)\le\frac{15\pi}{n}.}
   \tag{0.3}
   \]

   Moreover, for infinitely many \(n\),

   \[
   \boxed{0<\sigma_n(P)\le\frac{30\pi}{n^2}.}
   \tag{0.4}
   \]

5. The same mask has an explicit signed positive quotient of augmentation two:

   \[
   \boxed{Q=1-x^5+x^8+x^{10}-x^{13}+x^{18},\qquad Q(1)=2<5,}
   \tag{0.5}
   \]

   and

   \[
   \boxed{PQ=1+x+x^3+x^9+x^{11}+x^{13}+x^{15}+x^{21}+x^{23}+x^{24}.}
   \tag{0.6}
   \]

Thus aperiodicity does **not** give a uniform Fourier inverse bound, even for a
fixed five-term \(0/1\) mask.  Any proof that estimates a signed quotient by
\(\|P^{-1}\|\) through the smallest torsion-character singular value necessarily
pays an unbounded condition number.  The exact reciprocal-frame/factorial-energy
identity in `SIGNED_RESIDUAL_FACTORIAL_ENERGY.md` avoids this loss because it
keeps the full weighted spectral sum instead of replacing all denominators by
their minimum.

## 1. Irreducibility

Reduce \(P\) modulo three.  For a monic degree-six polynomial over
\(\mathbf F_3\), Rabin's criterion requires

\[
 x^{3^6}-x\equiv0\pmod P
\tag{1.1}
\]

and coprimality with \(x^{3^{6/q}}-x\) for the prime divisors
\(q=2,3\) of six.  Repeated squaring gives

\[
\begin{aligned}
 x^{3^2}-x&\equiv x^4-x^3-1 &&\pmod P,\\
 x^{3^3}-x&\equiv -x^5-x^4-x^2-x-1 &&\pmod P,\\
 x^{3^6}-x&\equiv0 &&\pmod P,
\end{aligned}
\tag{1.2}
\]

and the first two displayed remainders have gcd one with \(P\) in
\(\mathbf F_3[x]\).  Hence \(P\) is irreducible modulo three and therefore
irreducible over \(\mathbf Q\).

## 2. Unit-circle and off-circle roots

The polynomial is reciprocal.  Dividing by \(x^3\) and writing
\(y=x+x^{-1}\) gives

\[
 x^{-3}P(x)=
 (x^3+x^{-3})+(x^2+x^{-2})+1
 =f(y),
\tag{2.1}
\]

where

\[
 f(y)=y^3+y^2-3y-1.
\tag{2.2}
\]

Now

\[
 f(-1/2)>0>f(0),\qquad f(1)<0<f(2).
\tag{2.3}
\]

Thus \(f\) has real roots in \((-1/2,0)\) and \((1,2)\).  For each
\(y\in(-2,2)\), the two solutions of \(x+x^{-1}=y\) are nonreal conjugates
on the unit circle.  Therefore \(P\) has unit-circle zeros.

On the other hand,

\[
 f(-3)<0<f(-2),
\tag{2.4}
\]

so another root has \(y<-2\), and the corresponding reciprocal real roots of
\(P\) lie off the unit circle.  Consequently \(P\) is not cyclotomic.

If any zero of the irreducible polynomial \(P\) were a root of unity, its
cyclotomic minimal polynomial would divide \(P\).  Irreducibility would make
\(P\) cyclotomic, contradicting the off-circle roots.  Hence no zero of \(P\)
is torsion, proving both claims 1 and 3.

For completeness, if the support of \(P\) tiled \(\mathbb Z/n\mathbb Z\) with
an indicator \(1_Y\), Fourier transform of the tiling identity at every
nontrivial character would give \(\widehat P\,\widehat{1_Y}=0\).  The first
factor never vanishes, so all nontrivial Fourier coefficients of \(1_Y\) would
vanish.  Fourier inversion would make \(1_Y\) the constant \(|Y|/n=1/5\),
impossible for an indicator.  Hence there is no finite cyclic tiling shadow.

## 3. Quantitative small divisors

Write one unit-circle zero as \(z_0=e^{i\theta}\).  For every \(n\), choose an
integer \(k\) nearest to \(n\theta/(2\pi)\) and put
\(\zeta_n=e^{2\pi i k/n}\).  Then

\[
 |\zeta_n-z_0|\le|2\pi k/n-\theta|\le\frac\pi n.
\tag{3.1}
\]

On the unit circle,

\[
 |P'(z)|=|1+3z^2+5z^4+6z^5|
 \le1+3+5+6=15.
\tag{3.2}
\]

Integrating \(P'\) along the shorter circular arc from \(z_0\) to
\(\zeta_n\) (whose length is at most \(\pi/n\)) yields

\[
 |P(\zeta_n)|=|P(\zeta_n)-P(z_0)|\le\frac{15\pi}{n}.
\tag{3.3}
\]

Since \(P\) has no torsion zero, \(P(\zeta)\ne0\) for every
\(\zeta^n=1\); hence \(\sigma_n(P)>0\).  This proves (0.3).

In particular, on prime shadows \(p>5\), the automatic invertibility lemma from
the factorial-energy manuscript applies, but

\[
 \|P^{-1}\|_{2\to2}=\sigma_p(P)^{-1}\ge\frac{p}{15\pi}
\tag{3.4}
\]

along every prime sequence.  Invertibility and uniform conditioning are therefore
strictly different interfaces.

There is also a quadratic small-divisor subsequence.  Since \(z_0\) is not a
root of unity, \(\alpha=\theta/(2\pi)\) is irrational.  Continued-fraction
approximation gives infinitely many \(k/n\) with

\[
 \left|\alpha-\frac kn\right|<\frac1{n^2}.
\tag{3.5}
\]

For the corresponding \(n\)-th root of unity, the shorter arc has length at
most \(2\pi/n^2\); (3.2) then gives (0.4).  Thus the inverse norm grows at
least quadratically on an infinite (not necessarily prime) sequence of cyclic
shadows.

## 4. A signed escape on the same ill-conditioned centre

Direct multiplication of (0.1) and (0.5) gives (0.6).  The right side is a
ten-term \(0/1\) mask, exactly the required mass \(SC=5\cdot2\).  The quotient
has four coefficients \(+1\) and two coefficients \(-1\), so

\[
 \|Q\|_2^2=6,\qquad
 \delta(Q)=\frac{\|Q\|_2^2-Q(1)}2=2.
\tag{4.1}
\]

The quotient factorization is also exact:

\[
 \boxed{
 Q=(1+x^8)(1-x+x^2)
 (x^8+x^7-x^5-x^4-x^3+x+1).}
\tag{4.2}
\]

The three factors have augmentations \(2,1,1\).  This records explicitly how
one heavy occurrence and two augmentation-unit occurrences coexist in the
escape; no irreducibility of the quotient is asserted.

Thus the poorly conditioned aperiodic centre really hides signed cancellation
inside a positive mask.  This connects the small-divisor obstruction to the
actual residual interface, but it remains a one-row construction.

There is an important compensation.  Let \(M=PQ\) be the mask in (0.6).  At
every torsion point \(\zeta\), \(P(\zeta)\ne0\), and hence

\[
 \frac{|M(\zeta)|^2}{|P(\zeta)|^2}=|Q(\zeta)|^2\le
 \left(\sum_g|Q(g)|\right)^2=36.
\tag{4.3}
\]

Thus the individual inverse norm diverges, but the numerator co-vanishes at the
same non-torsion unit roots and the actual reciprocal-frame ratio stays bounded.
On every sufficiently support-injective prime shadow, Parseval gives exactly

\[
 \frac1p\sum_{\zeta^p=1}
 \frac{|M(\zeta)|^2}{|P(\zeta)|^2}
 =\|Q\|_2^2=6.
\tag{4.4}
\]

The minimum-singular-value estimate loses precisely this numerator/denominator
alignment, while the factorial-energy identity preserves it.

## 5. Quantifier firewall

This note proves one fixed aperiodic mask has both arbitrarily poor finite-shadow
conditioning and one signed positive quotient.  It does not construct a second
scalar-copy row, a common-mask power-large family, or a Euclidean #1083
counterexample, and it does not refute Erdős #1083.  It refutes arguments that
replace the reciprocal-frame sum by a uniform lower bound on
\(|\widehat P|\) derived from aperiodicity alone, and shows that the bad
conditioning occurs on a centre relevant to signed cancellation.

## 6. Reproduction

```bash
python3 verify_aperiodic_small_divisor_nogo.py
python3 -m unittest -v test_aperiodic_small_divisor_nogo.py
```

The verifier checks the exact Rabin remainders and gcds, reciprocal substitution,
sign intervals, numerical root geometry, absence of torsion factors through order
256, the exact signed product and factorial debt, and the small-divisor estimate
on a sample of prime shadows.  The
all-\(n\) estimate is proved above.
