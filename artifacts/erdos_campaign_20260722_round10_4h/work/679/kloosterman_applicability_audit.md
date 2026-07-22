# #679: audit of available Kloosterman-fraction inputs

Date: 2026-07-22

The primitive formula in `primitive_phase_target.md` contains modular
inverses, so Kloosterman-fraction estimates are a natural comparison. This
note distinguishes an actual theorem application from a merely analogous
phase shape.

## 1. Primary results checked

### Bettin--Chandee

Bettin and Chandee bound trilinear forms with arbitrary coefficient
sequences of the schematic form

\[
 \sum_{a\sim A}\sum_{m\sim M}\sum_{n\sim N}
 \nu_a\alpha_m\beta_n,e(a\overline m/n),             \tag{1}
\]

in terms of the three \(\ell^2\)-norms, with a power saving in suitable
ranges. See [Bettin--Chandee, *Trilinear forms with Kloosterman
fractions*](https://arxiv.org/abs/1502.00769).

### Walker's sieve-weight consequence

Walker considers a one-variable truncated divisor sum

\[
 \lambda_Z^*(n)=\sum_{d\mid n}\rho_Z^*(d),\qquad
 \rho_Z^*(d)=0\ (d>Z),\quad |\rho_Z^*(d)|\le B.
\]

His general off-diagonal proposition gives

\[
 \sum_n\lambda_Z^*(n)\lambda_Z^*(n+k)
 =\text{explicit main term}
 +O_\epsilon\!\left(
 B^2\min\{Z^2,X^{47/74+\epsilon}Z^{53/74}\}\right). \tag{2}
\]

The latter error is nontrivial in the intended fixed-shift application for
\(Z\le X^{27/53-\epsilon}\). See [Walker, *Correlations of sieve weights
and distributions of zeros*](https://arxiv.org/abs/2101.04418), especially
the general correlation proposition in Section 2. The paper explicitly
derives (2) from Bettin--Chandee after Poisson summation.

### Later distribution results

Fouvry--Radziwiłł prove level-of-distribution results beyond \(1/2\) for
specific unbalanced multiplicative convolutions, including consequences for
sieve weights; the input requires a tiny Siegel--Walfisz factor and gives an
average over moduli. See [Fouvry--Radziwiłł, *Level of distribution of
unbalanced convolutions*](https://arxiv.org/abs/1811.08672).

Wright's 2026 preprint improves the Kloosterman estimate when the denominator
has a fixed factor and correspondingly improves those unbalanced-convolution
ranges. Its stated consequences still assume a divisor-bounded convolution,
a Siegel--Walfisz factor, and a modulus average. See [Wright, *Trilinear
Kloosterman fractions I: partially fixed moduli and unbalanced
convolutions*](https://arxiv.org/abs/2604.25177).

These are primary sources. No result above states a bound for the object in
(7) of `primitive_phase_target.md`.

## 2. Exact mismatch with the #679 tail

There are four independent mismatches.

1. **Prime endpoint is not divisor level.** Our prime endpoint
   \(z=X^{1/L_2}=X^{o(1)}\) is small, but expansion of the Euler product is
   supported on products of primes up to the full CRT modulus
   \(Q=\prod_{H<p\le z}p\). The crossing terms under attack have divisor
   conductor \(c(T)\asymp X^{1-o(1)}\), not support \(d\le z\). Substituting
   the prime endpoint for Walker's divisor level \(Z\) would be invalid.

2. **Growing shifted dimension.** Since \(p>H\), one may write
   \(X_p(n)=\sum_{j<H}1_{p\mid n-K-j}\), but an expanded term assigns
   different selected primes to as many as \(H=(\log X)^2\) shifted linear
   forms. It is not a divisor sum \(\sum_{d\mid n}\rho(d)\), nor the product
   of two such sums appearing in (2).

3. **The terminal suffix is coefficient-dependent.** In the exact frontier
   formula, \(V_{p_*}(n)\) changes with the smallest selected prime \(p_*\).
   It cannot be absorbed into an arbitrary coefficient sequence in (1): it
   is a function of the interval variable \(n\), and its complete divisor
   support extends far beyond every polynomial level.

4. **The needed conclusion is additive and subunit.** After the round-10
   reduction, the target is \(O(X^{-\delta})\) for the whole signed tail.
   Walker's error (2), before any problem-specific coefficient gains, is a
   positive power of \(X\). A direct citation of (2) therefore would not
   establish the needed estimate even if the structural hypotheses matched.

Thus none of the checked theorems can be inserted as a black box.

## 3. A legitimate conditional interface

The analogy can nevertheless be stated without overclaiming. Group the
approximately \(L_2\) prime factors of a frontier conductor into two or
three dyadic product variables. CRT reciprocity converts the local inverses
\(h_p(u)\) in (3) of `primitive_phase_target.md` into Kloosterman fractions
between those product variables. A usable theorem would have to bound the
resulting sum while retaining

* the primitive frequency \(u\),
* the coefficient/frontier-dependent suffix \(V_{p_*}\), and
* enough joint cancellation over all frontier factorizations to produce a
  fixed negative power after the interval sum.

**Conditional statement.** If such a phase-preserving multilinear estimate
gives (8) of `primitive_phase_target.md` for one fixed \(q,C\) with
\(qC>1\), then `fixed_power_additive_sufficiency.md` closes the relevant
dyadic interval and hence the candidate sequence.

This conditional is logically exact; the required multilinear theorem is
not presently supplied by any source checked here.

Strict status: **literature applicability audit / conditional route, not a
theorem application and not a proof of Erdős #679**.
