# Erdős #686: high Cartier layers and the monomial-basis obstruction

Date: 2026-07-22 (Asia/Hong_Kong)

Status: exact fixed-parameter certificates and a route audit; no uniform new
Cartier theorem and no solution of #686.

## Exact finite extension

The committed round-10 exact Mahler-certificate generator was rerun at

\[
 m=16,24,32,40,48,56,64.
\]

For each listed `m`, let

\[
 T(m)=m-2\operatorname{oddpart}(m)
      -v_2(\operatorname{oddpart}(m)!)
\]

and let `C_m(z)` be the transferred coefficient polynomial used in rounds
9--10.  The full finite-difference vector proves, for **every integer** `z`,

\[
 v_2(C_m(z))=T(m).
\]

This is stronger than sampling values of `z`, but it is still only seven
fixed values of `m`.  The exact normalized Mahler coefficients, parity vector,
and coefficient hashes are in `higher_cartier_fixed_scan.json`.

## Why coefficientwise monomial divisibility cannot prove the pattern

For every one of the seven parameters, divide `C_m(z)` by the predicted
power `2^{T(m)}` and inspect its ordinary monomial coefficients.  Apart from
the constant coefficient, many have negative 2-adic valuation; in fact the
minimum normalized monomial valuation is

\[
\begin{array}{c|rrrrrrr}
m&16&24&32&40&48&56&64\\ \hline
\min v_2&-14&-17&-30&-27&-41&-38&-62.
\end{array}
\]

Thus `2^{-T(m)}C_m(z)` is generally not in `Z_2[z]`, even though it is an
odd-valued integer-valued polynomial on every integer.  The proof mechanism
must exploit cancellations in the Mahler basis `binom(z,r)` (or an equivalent
divided-power/Cartier basis).  A coefficient-by-coefficient argument in the
ordinary monomial basis loses as many as `T(m)` powers of two and cannot be
repaired by a constant refinement.

The script `verify_basis_gap.py` reproduces these valuations from the exact
rational coefficients and cross-checks the all-integer Mahler certificates.

## Exact divided-power reduction added in this round

`MAHLER_COEFFICIENT_REDUCTION.md` proves the all-parameter identity

\[
 \Delta^r C_m(0)=r!\,[v^{m-r}]
 \frac{H_m(v)}{\prod_{j=1}^r(1-jv)}.
\]

It turns the desired all-integer valuation into explicit divisibility of the
Mahler coefficients, and proves uniformly that the last four coefficients
`r=m-3,m-2,m-1,m` already have the required extra factor of two throughout the
first unresolved family `m=4s`, `s` odd.  Hence only the constant valuation
and the middle band `1<=r<=m-4` remain.  This is a strict route reduction, not the
missing middle-band estimate.

## Remaining uniform target

The usable next theorem is still a uniform statement for a whole Cartier
layer, for example

\[
 v_2(C_{8s}(z))=T(8s)
 \quad(s\text{ odd},\ z\in\mathbb Z),
\]

or the previously identified general doubling congruence.  The finite data
support it but do not prove it.  Since #686 allows the auxiliary parameter to
vary, any fixed list of lengths is below the SCI-Q2 stopping threshold and
does not close the original problem.
