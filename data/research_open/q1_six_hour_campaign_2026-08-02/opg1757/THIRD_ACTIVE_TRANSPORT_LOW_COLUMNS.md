# OPG-1757: 31 universal low columns of the third-active transports

Date: 2026-08-02

Status: **PROVED LOW BANDS; FULL TRANSPORTS OPEN**.

## 1. Result

Use the strict transport candidates

\[
 R_s^{\rm o}=H_{s+1}^{\rm o}-(s+6z)^2H_s^{\rm o},
 \qquad
 R_s^{\rm e}=H_{s+1}^{\rm e}-(s+7z)^2H_s^{\rm e}.
\tag{1}
\]

The first 31 columns are universally positive throughout the part of
the support where the top homogenization exponent is nonnegative:

\[
 \boxed{
 [z^d]R_s^{\rm o}>0
 \quad\left(s\ge8, 0\le d\le\min\{30,2s-12\}\right),
 }
\tag{2}
\]

\[
 \boxed{
 [z^d]R_s^{\rm e}>0
 \quad\left(s\ge9, 0\le d\le\min\{30,2s-14\}\right).
 }
\tag{3}
\]

Together with `THIRD_ACTIVE_TRANSPORT_TOP_BANDS.md`, this proves the
complete odd transports for `8<=s<=21` and the complete even transports
for `9<=s<=22`.  That finite consequence is not used to extrapolate in
`s`; the content of (2)--(3) is the two unbounded fixed-column bands.

## 2. Odd sufficient kernel

Write

\[
 u_j=1+j\beta,\qquad \lambda_a=1+a\beta,
\]

\[
 P_{6,s}=F_s^{(6)}/\beta^8,\qquad
 P_{4,s}=F_s^{(4)}/\beta^4,
\]

and define

\[
 D_{6,s}=P_{6,s+1}-u_6^2P_{6,s},\qquad
 B_{6,s}=u_6^2P_{6,s}.
\tag{4}
\]

Fix a degree `d` and put

\[
 N=2s-12-d.
\tag{5}
\]

The top `B6` part of the odd transport has coefficient

\[
 \frac1{12}\left(
 (s+1)^N[\beta^d](D_{6,s}+B_{6,s})
 -s^N[\beta^d]B_{6,s}
 \right).
\tag{6}
\]

On the columns certified below, `[beta^d]D_(6,s)>=0`.  The proved `B6`
theorem gives `B_(6,s)>=_coeff 0`.  For `N>=0`, Bernoulli's inequality
therefore gives the lower bound

\[
 (6)\ge
 \frac{s^N}{12}[\beta^d]\left(
 D_{6,s}+\frac{2s-12-\beta\partial_\beta}{s}B_{6,s}
 \right).
\tag{7}
\]

In the remaining two parts of the transport, discard the positive
transported-middle term and the positive next-bottom term.  The negative
next-middle term is exact.  For the negative transported-bottom term,
coefficientwise replace every nonnegative power of `s-2` by the same
power of `s`.  This is legal precisely when `d<=2s-12`.  It gives the
sufficient coefficient kernel

\[
\begin{aligned}
 L_{s,d}^{\rm o}={}&\frac1{12}[\beta^d]\left(
 D_{6,s}+\frac{2s-12-\beta\partial_\beta}{s}B_{6,s}
 \right)\\
 &-(s-3)s^2[\beta^d]\lambda_s^2P_{4,s}\\
 &-(s-4)(s-5)s^4[\beta^d]
 u_6^2\lambda_s^4u_2^{2s-10}.
\end{aligned}
\tag{8}
\]

Thus

\[
 [z^d]R_s^{\rm o}\ge s^N L_{s,d}^{\rm o}.
\tag{9}
\]

The final term in (8) deliberately overpays the negative bottom
transport.  Omitting the Bernoulli gain in (7), on the other hand, is
not valid as a proof route: the resulting coarse kernel develops a
negative constant coefficient from `s=16` onward.

## 3. Even sufficient kernel

Define analogously

\[
 P_{7,s}=F_s^{(7)}/\beta^{10},\quad
 P_{5,s}=F_s^{(5)}/\beta^6,\quad
 P_{3,s}=J_s^{(3)}/\beta^2,
\]

\[
 D_{7,s}=P_{7,s+1}-u_7^2P_{7,s},\qquad
 B_{7,s}=u_7^2P_{7,s},
\tag{10}
\]

and now let `N=2s-14-d`.  The same argument gives

\[
\begin{aligned}
 L_{s,d}^{\rm e}={}&\frac1{60}[\beta^d]\left(
 D_{7,s}+\frac{2s-14-\beta\partial_\beta}{s}B_{7,s}
 \right)\\
 &-\frac{(s-3)s^2}{3}[\beta^d]\lambda_s^2P_{5,s}\\
 &-(s-4)(s-5)s^4[\beta^d]
 u_7^2\lambda_{s-2}^4P_{3,s-2}.
\end{aligned}
\tag{11}
\]

For `d<=2s-14`, every scale exponent used in replacing `s-2` by `s`
is nonnegative, and

\[
 [z^d]R_s^{\rm e}\ge s^N L_{s,d}^{\rm e}.
\tag{12}
\]

## 4. Fixed-column certificates

For each `0<=d<=30`, set

\[
 s_d^{\rm o}=\max\left\{8,\left\lceil\frac{d+12}{2}\right\rceil\right\},
 \qquad
 s_d^{\rm e}=\max\left\{9,\left\lceil\frac{d+14}{2}\right\rceil\right\}.
\tag{13}
\]

Direct fixed-degree extraction from the frozen `K3,...,K7` kernels
proves the following exact polynomial facts:

- every coefficient of
  `12(s_d^o+x)L_(s_d^o+x,d)^o` is strictly positive;
- every coefficient of
  `60(s_d^e+x)L_(s_d^e+x,d)^e` is strictly positive;
- the shifted fixed-column polynomials
  `[beta^d]D_(6,s_d^o+x)` and
  `[beta^d]D_(7,s_d^e+x)` have no negative coefficient.

Across the 31 columns, the two strict sufficient-kernel certificates
contain respectively 775 and 837 positive monomials.  The two discrete
page-recurrence certificates contain respectively 713 and 775 positive
monomials; zero monomials are ignored.  Since `x>=0`, (8)--(13) prove
(2)--(3) without a finite upper bound on `s`.

## 5. Verification and firewall

Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 third_active_transport_bulk_attack.py
```

The verifier reconstructs every fixed coefficient from the alternating
fixed-page formulas.  It also compares the sufficient lower bounds with
90 coefficients of the full exact transports at independent small
parameters; those comparisons guard transcription only.

The arbitrary cutoff `d=30` is not asserted to be maximal.  Equations
(2)--(3) and the reverse bands leave an unbounded middle interval for
large `s`.  Hence neither complete transport, the universal third-active
row, nor the original OPG-1757 statement is proved here.
