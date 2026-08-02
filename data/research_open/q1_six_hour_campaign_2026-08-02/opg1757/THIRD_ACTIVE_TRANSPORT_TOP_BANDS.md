# OPG-1757: universal top bands of the third-active transports

Date: 2026-08-02

Status: **PROVED TOP BANDS; FULL TRANSPORTS OPEN**.

## 1. Statement

Retain the exact reduced polynomials from
`THIRD_ACTIVE_EXACT_REDUCTION.md`, and put

\[
 R_s^{\rm o}(z)=H_{s+1}^{\rm o}(z)-(s+6z)^2H_s^{\rm o}(z),
 \qquad s\ge8,
\tag{1}
\]

\[
 R_s^{\rm e}(z)=H_{s+1}^{\rm e}(z)-(s+7z)^2H_s^{\rm e}(z),
 \qquad s\ge9.
\tag{2}
\]

Then the complete reverse boundary bands of the two proposed
transports are strictly positive:

\[
 \boxed{
 [z^{2s-4-t}]R_s^{\rm o}(z)>0
 \quad(0\le t\le7, s\ge8),
 }
\tag{3}
\]

\[
 \boxed{
 [z^{2s-4-t}]R_s^{\rm e}(z)>0
 \quad(0\le t\le9, s\ge9).
 }
\tag{4}
\]

These are all-parameter statements.  They do not follow from the old
finite scan through `m=100`.

The band widths are the natural ones.  Homogenizing the top `B6` term
in (1) leaves a nonnegative scaling exponent through degree
`2s-12`, so its escaping reverse band has eight degrees.  The analogous
`B7` cutoff is `2s-14`, leaving ten degrees.  Thus (3)--(4) remove the
entire top-boundary obstruction from any future bulk proof of the two
transports.

## 2. Exact reverse extraction

For a fixed page base `a`, exponent `E(s)`, kernel

\[
 K(s,\beta)=\sum_i k_i(s)\beta^i,
\]

and reverse-fixed target degree `D(s)`, define

\[
 \mathcal T_{a,E,K,D}(s)
 =\sum_{i:\ c_i\in\mathbb Z_{\ge0}}
 k_i(s)\binom{E(s)}{c_i}
 a^{E(s)-c_i-2s},
 \qquad c_i=E(s)-D(s)+i.
\tag{5}
\]

Then

\[
 [\beta^{D(s)}](1+a\beta)^{E(s)}K(s,\beta)
 =a^{2s}\mathcal T_{a,E,K,D}(s).
\tag{6}
\]

Apply (5) directly to the five exponentials in `F_s^(6)` and the
three in `F_{s-1}^(4)`, including the two `(1+z)` convolution layers
and the elementary bottom term in the odd formula.  The even formula
uses the six exponentials in `F_s^(7)`, the four in `F_{s-1}^(5)`, and
the two in `J_{s-2}^(3)`, including its four `(1+z)` layers.

If

\[
 [z^{2s-6-t}]H_s=\sum_a a^{2s}D_{t,a}(s),
\tag{7}
\]

then taking the coefficient of degree `2s-4-t` in (1) or (2) gives
the exact transport identity

\[
 [z^{2s-4-t}]R_s
 =\sum_a a^{2s}\Bigl(
 a^2D_{t,a}(s+1)-p^2D_{t,a}(s)
 -2spD_{t-1,a}(s)-s^2D_{t-2,a}(s)
 \Bigr),
\tag{8}
\]

where `p=6` in the odd branch and `p=7` in the even branch; terms with
negative subscripts are zero.  This also checks all three coefficient
shifts contributed by `(s+pz)^2`.

Putting `n=s-8` in the odd branch and `n=s-9` in the even branch,
(8) simplifies exactly to

\[
 [z^{2s-4-t}]R_s=\sum_{a=2}^{p}a^{2n}P_{t,a}(n),
\tag{9}
\]

with fixed rational polynomials `P_{t,a}`.  No exponent depending on
`n` remains inside a polynomial coefficient.

## 3. Dominant-exponential certificate

For each row of the following table, let `A` be the displayed dominant
base.  Let `P=P_{t,A}` and let `Q` be the sum of the absolute values of
all negative monomials in the lower-base polynomials.  Positive
lower-base monomials are discarded.  Since every lower base is at most
`A-1`, (9) gives

\[
 [z^{2s-4-t}]R_s
 \ge A^{2n}P(n)-(A-1)^{2n}Q(n).
\tag{10}
\]

The exact certificates are:

| branch | `t` | dominant `A` | `deg P` | `deg Q` | shift `n_0` |
|---|---:|---:|---:|---:|---:|
| odd | 0 | 5 | 0 | 2 | 0 |
| odd | 1 | 6 | 1 | 4 | 2 |
| odd | 2 | 6 | 3 | 6 | 1 |
| odd | 3 | 6 | 5 | 8 | 1 |
| odd | 4 | 6 | 7 | 10 | 0 |
| odd | 5 | 6 | 9 | 12 | 0 |
| odd | 6 | 6 | 11 | 14 | 0 |
| odd | 7 | 6 | 13 | 16 | 1 |
| even | 0 | 6 | 0 | 2 | 0 |
| even | 1 | 7 | 1 | 4 | 4 |
| even | 2 | 7 | 3 | 6 | 3 |
| even | 3 | 7 | 5 | 8 | 2 |
| even | 4 | 7 | 7 | 10 | 1 |
| even | 5 | 7 | 9 | 12 | 1 |
| even | 6 | 7 | 11 | 14 | 1 |
| even | 7 | 7 | 13 | 16 | 2 |
| even | 8 | 7 | 15 | 18 | 2 |
| even | 9 | 7 | 17 | 20 | 3 |

For every table row, the following three exact facts hold:

1. `P(x+n_0)` has strictly positive monomial coefficients;
2. after clearing positive denominators,
   \[
   A^2P(n+1)Q(n)-(A-1)^2Q(n+1)P(n)
   \tag{11}
   \]
   has nonnegative monomial coefficients after `n=x+n_0`;
3. the gap in (10) at `n=n_0` is strictly positive.

Consequently the ratio

\[
 \frac{A^{2n}P(n)}{(A-1)^{2n}Q(n)}
\tag{12}
\]

is nondecreasing from `n_0`, and its initial value is greater than one.
This proves (10) for every `n>=n_0`.  The 24 values with `n<n_0` are
evaluated exactly and are all strictly positive.

There is a real cancellation at `t=0`: the nominal top base `6` in the
odd transport, respectively `7` in the even transport, vanishes
identically.  The proof therefore uses dominant bases `5` and `6` in
those two rows.  Treating the uncancelled page base as dominant would be
an invalid shortcut.

## 4. Verification and boundary

Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 third_active_transport_top_attack.py
```

The verifier derives (5)--(9) from the frozen `K3,...,K7` kernels.  It
checks 330 shifted ratio-polynomial monomials, all 24 exceptional exact
values, and 72 direct comparisons with the full transport convolution.
The direct comparisons guard transcription only; the unbounded proof is
the fixed-polynomial ratio argument (10)--(12).

Equations (3)--(4) do **not** prove either complete transport.  The bulk
degrees remain open, so the full third-active row and the original
OPG-1757 proposition remain open.
