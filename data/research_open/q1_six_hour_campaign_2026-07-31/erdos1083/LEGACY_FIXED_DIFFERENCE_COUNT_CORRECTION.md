# Correction and repair: fixed-difference projection multiplicity

Date: 2026-08-01

Audited source: Theorem 8(4), equations (5.21)--(5.23), in the
2026-07-31 breakthrough campaign.

## 0. Final verdict

Two logically different assertions must be separated.

1. **Refuted as stated:** after pigeonholing coincidence records by
   \(\delta=\tau'-\tau\), those records do not automatically project
   injectively to tuples \((z,z',x,x')\).  A dimension-three exact
   block gives two records with the same projection.
2. **Reproved:** the final existence conclusion and its
   \(t^{19/18}\) endpoint exponent are nevertheless correct.  A
   global difference-multiplicity budget repairs the proof without
   losing any power.

The repaired theorem is:

### Theorem A (unweighted fixed-difference count)

In an exact \(q\)-row block, some fixed
\(\delta\in T_*-T_*\) supports at least

\[
 \boxed{
 \frac{q(q-1)SU}{\Sigma_\mu}
 \ge
 \frac{q(q-1)SU}{R^2}}
\tag{0.1}
\]

distinct tuples \((z,z',x,x')\) satisfying

\[
 z^2-z'^2+2\rho(zx-z'x')=\delta,
\tag{0.2}
\]

where

\[
 \mu(\delta)
 =\max_{z\ne z'}
 |\{\tau\in T_z:\tau+\delta\in T_{z'}\}|
\tag{0.3}
\]

and

\[
 \Sigma_\mu=\sum_{\delta\in T_*-T_*}\mu(\delta).
\tag{0.4}
\]

At the frozen endpoint, (0.1) has exponent \(19/18\).

Thus the previous numerical theorem survives, but its original
projection-injectivity justification must be replaced by the proof
below.

## 1. The failed projection step

For a common value \(v\in V\) and ordered row pair \((z,z')\), exact
directness gives unique representations

\[
 v=\rho^2+z^2+\tau+2\rho zx
  =\rho^2+z'^2+\tau'+2\rho z'x'.
\tag{1.1}
\]

Put \(\delta=\tau'-\tau\).  Then

\[
 z^2-z'^2+2\rho(zx-z'x')=\delta.
\tag{1.2}
\]

The cell identity supplies exactly

\[
 q(q-1)SU
\tag{1.3}
\]

records

\[
 (v,z,z',\tau,\tau',x,x').
\tag{1.4}
\]

The old proof grouped (1.4) by \(\delta\) and treated the resulting
records as distinct projected tuples

\[
 (z,z',x,x').
\tag{1.5}
\]

That projection is not injective.  For fixed
\((z,z',x,x',\delta)\), every
\(\tau\in T_z\) with \(\tau+\delta\in T_{z'}\) gives another record,
with another common value \(v\).  The exact projection multiplicity
is

\[
 r_{T_z,T_{z'}}(\delta)
 =|\{\tau\in T_z:\tau+\delta\in T_{z'}\}|.
\tag{1.6}
\]

## 2. Minimal explicit collision certificate

Use the exact dimension-three hypercube block with

\[
 X=\{0,1\},\qquad a_i=3^i.
\]

Take

\[
 z=\frac12,\qquad z'=\frac32,\qquad\delta=-2.
\]

The following two distinct records occur:

| \(v\) | \(\tau\) | \(\tau'\) | \(x\) | \(x'\) |
|---:|---:|---:|---:|---:|
| \(83\) | \(327/4\) | \(319/4\) | \(0\) | \(0\) |
| \(92\) | \(363/4\) | \(355/4\) | \(0\) | \(0\) |

Both project to

\[
 (z,z',x,x')=(1/2,3/2,0,0)
\]

and both have \(\tau'-\tau=-2\).  The projection multiplicity is
two.  In the checked dimension-six hypercube, the maximum projection
multiplicity is \(16\).

The verifier reconstructs every row representation and both
groupings from scratch.  This strictly refutes projection
injectivity, although it does not refute the final lower bound.

## 3. Difference-multiplicity repair

Let \(C_\delta\) be the number of full records (1.4) carrying
\(\delta\), and let \(N_\delta\) be the number of distinct projected
solutions (1.5).  Equation (1.6) gives the exact weighted identity

\[
 C_\delta
 =\sum_{\substack{(z,z',x,x')\\\text{solving (1.2)}}}
 r_{T_z,T_{z'}}(\delta).
\tag{3.1}
\]

Therefore

\[
 C_\delta\le\mu(\delta)N_\delta.
\tag{3.2}
\]

Summing and using (1.3),

\[
\begin{aligned}
 q(q-1)SU
 &=\sum_\delta C_\delta\\
 &\le\sum_\delta\mu(\delta)N_\delta\\
 &\le\left(\max_\delta N_\delta\right)\Sigma_\mu.
\end{aligned}
\tag{3.3}
\]

It remains to control \(\Sigma_\mu\).  Let

\[
 r_{T_*}(\delta)
 =|\{(\tau,\tau')\in T_*^2:\tau'-\tau=\delta\}|.
\tag{3.4}
\]

Since every \(T_z,T_{z'}\) is a subset of \(T_*\),

\[
 \mu(\delta)\le r_{T_*}(\delta).
\tag{3.5}
\]

But every ordered pair in \(T_*^2\) has exactly one difference, so

\[
 \sum_\delta r_{T_*}(\delta)=R^2.
\tag{3.6}
\]

Consequently

\[
 \boxed{\Sigma_\mu\le R^2.}
\tag{3.7}
\]

Combining (3.3) and (3.7) proves Theorem A.

This argument also shows why dividing one naively selected
\(\delta\)-fibre by \(U\) is unnecessarily wasteful.  Large
projection multiplicity can occur, but the total of the worst
difference multiplicities over all \(\delta\)'s has the exact global
budget \(R^2\).

### Ordered-pair and zero-difference conventions

All counts above are ordered and signed.

- The row pairs are ordered pairs \((z,z')\) with \(z\ne z'\).
  Hence their number is \(q(q-1)\).
- The tangent-difference representation function is

  \[
  r_{T_*}(\delta)
  =|\{(\tau,\tau')\in T_*^2:\tau'-\tau=\delta\}|,
  \]

  again with ordered pairs.  Swapping the tangent pair changes
  \(\delta\) to \(-\delta\).
- The value \(\delta=0\) is included.  Since \(T_*\) is a set,

  \[
  r_{T_*}(0)=R.
  \]

  Meanwhile

  \[
  \mu(0)
  =\max_{z\ne z'}|T_z\cap T_{z'}|
  \le R=r_{T_*}(0).
  \]

- Excluding \(z=z'\) in \(\mu(\delta)\) only decreases the maximum
  relative to the global universe bound.  It does not alter
  \(\mu(\delta)\le r_{T_*}(\delta)\).

With these conventions, every ordered pair
\((\tau,\tau')\in T_*^2\), including the \(R\) diagonal pairs,
contributes to exactly one signed difference.  This proves (3.6)
with equality and no missing factor of two.

If one instead uses unordered tangent pairs and absolute
differences, the nonzero fibres combine \(\delta\) and \(-\delta\);
all displayed constants must then be adjusted.  The present proof
uses the ordered convention throughout.

## 4. Endpoint exponent

The repaired unweighted count has exponent

\[
 2\left(\frac{13}{18}\right)
 +\frac{29}{18}-2
 =\boxed{\frac{19}{18}}.
\tag{4.1}
\]

No \(U=t^{5/6}\) loss is needed.  The parameterized denominator
\(\Sigma_\mu\) can only improve the conclusion when the tangent
universe has a sparse difference profile across the row family.

## 5. Correct claim boundary

The following statements are now certified.

- The direct projection of pigeonholed records is not injective.
- The \(t^{19/18}\) weighted coincidence count is valid.
- The \(t^{19/18}\) distinct projected-tuple existence bound is also
  valid, by Theorem A rather than by direct projection.
- The sharper all-parameter denominator is \(\Sigma_\mu\), with
  \(\Sigma_\mu\le R^2\).

The phrase “the pigeonholed records are already distinct
\((z,z',x,x')\) tuples” is refuted as stated.  The theorem
“some \(\delta\) has at least \(q(q-1)SU/R^2\) distinct projected
tuples” is reproved.

## 6. Independence of the new tangent-overlap dichotomy

The tangent-transversality dichotomy in the present campaign does
not use (5.21), fixed differences, common values, or projection
injectivity.  Its proof consists only of

\[
 \sum_\tau r_\tau=qU,
\]

\[
 \sum_\tau r_\tau(r_\tau-1)
 \ge\frac{q^2U^2}{R}-qU,
\]

and the exact split of the final sum according to whether
\(W_i\cap W_j\) is zero.

The fixed-tangent rigidity theorem is also independent: it subtracts
two explicit cell equations.  Thus neither new result is weakened by
the correction above.

## 7. Reproduction

The verifier checks, in exact rational arithmetic for hypercube
dimensions three through six:

- the full-record total \(q(q-1)SU\);
- the weighted identity (3.1);
- \(C_\delta\le\mu(\delta)N_\delta\) for every signed difference,
  including zero;
- \(\mu(\delta)\le r_{T_*}(\delta)\);
- \(\sum_\delta r_{T_*}(\delta)=R^2\);
- \(\Sigma_\mu\le R^2\); and
- the final unweighted lower bound (0.1).
