# Independent red-team audit: complementary endpoint localization

Date: 2026-07-30

## 0. Verdict

\[
\boxed{\text{PASS after two expository repairs}}
\]

`COMPLEMENTARY_ENDPOINT_LOCALIZATION_LEMMA.md` gives an all-rank
proof that
\[
\frac{F_{h,r}(x)}{\sqrt{1-2x}}
\]
is regular at \(x=1\).  It is sufficient to replace assumption (5g)
in `ALL_RANK_ORDINARY_SYMBOL_DEGREE_THEOREM.md`; the cubic-degree
theorem can therefore be stated unconditionally.

The two repairs made during this audit were:

1. coefficient matching is now stated first on the dense set of
   rational \(x\in(0,1/2)\), with \(s\) restricted to the appropriate
   multiples, and then promoted by rational-function identity; and
2. the \(\sqrt{2\pi s}\) Stirling prefactor and its cancellation
   against the contour Gaussian are displayed explicitly.

Neither repair changes an exact formula.  The finite verifier is a
normalization audit only and is not used as the all-rank proof.

## 1. Exact main coefficient identity

For
\[
\mathcal S_s(J,Q)
=\sum_i\frac{J_{\underline i}Q_{\underline i}}{i!}
\left(-\frac1{2s}\right)^i,
\]
direct coefficient extraction gives
\[
\frac{\mathcal S_s(J,Q)}{Q!}
=[u^Q]e^u(1-u/(2s))^J.
\]
Subtracting the \(J-1\) term with its exact \(J/s\) multiplier yields
\[
\frac1{Q!}\left(
\mathcal S_s(J,Q)-\frac Js\mathcal S_s(J-1,Q)
\right)
=\frac1s[u^Q]e^u(1-u/(2s))^{J-1}
(Q+a-u/2),
\]
because \(s-J=Q+a\).  No reversal of a length-\(J\) sum is hidden
here.

The falling factorial contributes
\[
(s-a)_{\underline J}
=\frac{\Gamma(s-a+1)}{\Gamma(Q+1)}.
\]
The \(\Gamma(Q+1)=Q!\) factor cancels exactly.  After \(u=sv\), all
powers of \(s\) combine to \(s^{a-s}\), and the remaining
\(v\)-power is \(v^{a-1}\).  This independently recovers
\[
\Gamma(s-a+1)2^{xs}s^{a-s}
\frac1{2\pi i}\oint
\frac{v^{a-1}(q-v/2)}{1-v/2}e^{s\psi_q(v)}\,dv.
\]
Thus the Gamma argument, the power of \(s\), and the amplitude in
(10)--(11) are correct.  In particular, \(a=0\) genuinely gives
\(v^{-1}\); it is regular in the local ring at \(v=1\).

## 2. Exact exceptional identity

With \(L=J-1\), \(P=qs-3\), one has \(L+P=s-4\) and
\[
(s-4)_{\underline L}
=\frac{\Gamma(s-3)}{\Gamma(P+1)}.
\]
The same coefficient identity cancels \(P!\).  The remaining factors
are
\[
\frac{4x}{s}\Gamma(s-3)2^{xs}s^{4-s},
\qquad
\widetilde g_*(v)=\frac{v^2}{1-v/2}.
\]
Hence (21), including the constant \(4x/s\), is correct.  Its leading
contribution is
\[
\frac{8x}{s\sqrt{1-2x}},
\]
which agrees with the exceptional rank shift in the original profile
recurrence.

## 3. Saddle geometry

The complementary stationary equation is exactly
\[
\psi_q'(v)
=-\frac{(v-1)(v-2q)}{2v(1-v/2)}.
\]
For \(0<x<1/2\), \(2q>1\), so the second saddle lies outside the unit
coefficient circle.  On \(v=e^{i\theta}\),
\[
\frac d{d\theta}\Re\psi_q(e^{i\theta})
=\sin\theta\left(-1+\frac{2x}{5-4\cos\theta}\right)<0
\quad(0<\theta<\pi).
\]
Thus \(v=1\) is the unique maximum on the circle.  The integrand is
analytic on a neighbourhood of the circle; the possible \(v=0\)
factor lies inside it and is the ordinary coefficient pole, not a
competing contour saddle.

For the original representation, the same modulus calculation on
\(|y|=2x\) gives a unique maximum at \(y=2x\), while the other
stationary point \(y=1\) is outside because \(2x<1\).  Therefore both
exact representations have one contributing nondegenerate saddle on
the overlap.

## 4. Poincare matching and endpoint continuation

Fix rational \(x\in(0,1/2)\) and take \(s\) through multiples of its
denominator.  Both exact integrals represent the same finite
quantity, and the complement of the unique saddle neighbourhood is
exponentially smaller.  Uniqueness of asymptotic power series gives
coefficient equality at that \(x\).  After extracting \(\sqrt W\),
the two saddle recurrences have rational coefficients in \(x\).
Equality on dense rational \(x\) therefore proves equality as
rational functions, not merely equality of finitely many ranks.

At \(v=1\),
\[
\psi_q''(1)=W=2q-1,\qquad
\widetilde g_a(1;q)=W.
\]
Moreover
\[
\Gamma(s-a+1)s^{a-s}e^s
=\sqrt{2\pi s}(1+O(s^{-1})),
\]
while the contour Gaussian contributes
\((2\pi sW)^{-1/2}\).  Their product with the amplitude starts with
\(\sqrt W\).  Every higher coefficient is built from:

- polynomial \(q\)-jets of the phase and amplitudes at \(v=1\);
- coefficients of Stirling's series depending only on \(a\); and
- inverse powers of \(W\).

At \(q=0\), \(W=-1\) is a unit.  Consequently every rational
Poincare coefficient is regular there.  This is coefficient-level
analytic continuation; it does not require the finite integer
parameter \(Q=qs-a\) to remain nonnegative at \(q=0\).

For the exceptional block, division by the full profile's
\(\sqrt W\) introduces \(W^{-1}\), again a unit at \(q=0\).
Therefore no \(q^{-1}=(1-x)^{-1}\) pole remains at any rank.

## 5. Scope of the verifier

`verify_complementary_endpoint_localization.py` independently checks:

- the finite hypergeometric coefficient identity;
- main and exceptional constants against the original finite sums;
- the stationary factorization and Hessian; and
- regular local amplitude jets at \(q=0,v=1\).

These checks are useful for detecting a missing \(2\), \(J\), Gamma
shift, or power of \(s\).  They do not establish arbitrary-rank
Poincare uniqueness or analytic continuation.  Those steps are the
proof in Sections 3--4 above.

## 6. Replacement of (5g)

The exact replacement is:
\[
\boxed{
\text{For every }h\in\{0,1,2\},\ r\ge0,\quad
C_{h,r}(x)=F_{h,r}(x)/\sqrt{1-2x}
\text{ is regular at }x=1.
}
\]
Together with the existing finite-source argument at \(x=0\), this
removes both endpoint poles from the rational saddle recurrence.
Only the discriminant pole \(1-2x=0\) remains, exactly as required by
the localized ring \(\mathcal R_{3r}\).
