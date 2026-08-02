# Independent audit of the OPG-1757 polynomial deficit window

Date: 2026-08-02

Verdict: **PASSED; THE PREVIOUS `1/67` WINDOW IS PROVED**.

This audit reconstructs the proof from the exact endpoint and master
identities.  It does not treat the previous finite certificate as a
proof.  The conclusion remains restricted to the complete-split pooled,
disjoint-core, alpha-squared layer.

## 1. Exact object and normalization

For integers (q\ge1), (0\le r\le2q), put

\[
 n=2s-5-q,
 \qquad
 C_{q,r}(s)=
 \frac{[\beta^{2n+r}]B_n(s,\beta)}
 {n!s^{2s-8-2q+r}}.
 \tag{1}
\]

The exact master identity is

\[
\begin{aligned}
C_{q,r}(s)=4\sum
\frac{1}{\ell!}\binom{q+1-\ell}{a}
\big[&
(s-1-c-e)_\ell(s-1-d-f)_\ell Q_{1,e,c}Q_{1,f,d}\\
&-(s-c-e)_\ell(s-2-d-f)_\ell Q_{0,e,c}Q_{2,f,d}\big],
\end{aligned}
\tag{2}
\]

where

\[
a=r-2\ell-e-f,
\quad 0\le a\le q+1-\ell,
\quad c,d\ge1,
\quad c+d=q+3-\ell-e-f.
\tag{3}
\]

The normalization in (2) checks independently as follows.  Endpoint
orders (j,k) contribute (j!k!), while a pooled overlap contributes

\[
\frac{n!}{\ell!(j-\ell)!(k-\ell)!}.
\]

After division by the (n!) in (1), this is exactly
((j)_\ell(k)_\ell/\ell!), giving the four falling factors in (2).
Writing (c=\rho+1,d=\sigma+1), the power selected from
((1+s\beta)^{q+1-\ell}) is (s^a), and

\[
-2-2(c+d)-(e+f)+a=-8-2q+r.
\]

It cancels precisely the remaining power in (1).  No factorial or power
of (s) is omitted from (2).

## 2. Endpoint loss coefficients

Let (m=e+\rho).  The endpoint normalization is

\[
Q_{h,e,\rho+1}(s)=
\frac{s^{2m}}{2^m\rho!e!}
\left(1+\sum_{k\ge1}q_{h,k}(e,\rho)s^{-k}\right).
\tag{4}
\]

The inherited filtered identity uses exactly this (Q), including the
functional shift (h+2):

\[
Q_{h,e,\rho+1}
=\frac{s^{2m}}{\rho!}[v^e]\mathcal L_{h+2,s^{-1}}
\left[e^{(\Phi-t)s}
\{e^{s^{-1}vt}V^\rho+2^{-h}\rho JV^{\rho-1}\}\right].
\tag{5}
\]

Here the second term is absent at (\rho=0).  Expanding by Laurent
order gives the following independent degree ledger.

- An order-(j) term of the exponential correction has (v)-degree at
  most (2j).
- In (V^\rho), choosing (p) corrected factors costs degree (p) in
  (\rho), while (p\le j); the combined parameter degree is at most
  (2j).
- The positive-order part of (J-J_0) starts at order one, which pays
  for the extra explicit (\rho).
- The order-(i) part of the falling-factor functional is a polynomial
  in (t\partial_t) of order at most (2i).  In the (J_0=1-t)
  term, one derivative is forced to hit (1-t), cancelling its one
  extra parameter degree.

Thus, at total Laurent loss (k=i+j), coefficient extraction against
(e^{v/2}) turns each (v^u) into (2^u(e)_u), without increasing
total degree.  Therefore

\[
q_{h,k}\in\mathbb Q[e,\rho],
\qquad \deg q_{h,k}\le2k
\tag{6}
\]

for every (k\ge1) and (h=0,1,2).  This is the same normalized
endpoint interface needed in (2), not a differently shifted endpoint.

The uniform endpoint norm gives, on the triangular grid
(e+\rho\le2k),

\[
|q_{h,k}(e,\rho)|
\le15(2k+1)2^{4k}(2k)!(4k+4)^{4k}.
\tag{7}
\]

The total-degree Newton identity

\[
p(e,\rho)=\sum_{i+j\le2k}
\Delta_e^i\Delta_\rho^jp(0,0)
\binom ei\binom\rho j
\tag{8}
\]

uses only points (a+b\le i+j\le2k).  Hence the triangular grid is
unisolvent and controls the actual profile values, not merely formal
monomial coefficients.  The previous bound

\[
|q_{h,k}(e,\rho)|
\le[128(k+1)]^{16k}q^{2k}
\tag{9}
\]

for (0\le e,\rho\le q+1) follows.  A stronger quantitative version is
proved separately in `POWER_EIGHTH_WINDOW_THEOREM.md`.

## 3. Four-factor loss and its domain

In (2), conservation is

\[
(e+\rho)+(f+\sigma)+\ell=q+1.
\tag{10}
\]

Thus all endpoint parameters are at most (q+1).  The four falling
shifts are

\[
e+\rho+2,\quad f+\sigma+2,\quad
e+\rho+1,\quad f+\sigma+3,
\]

and natural support implies (\ell\le q).  Consequently every
loss-(i) falling coefficient is bounded by the same envelope (9).
Convolving the two endpoints and two falling factors gives, at total
apparent loss (K\),

\[
U_K(q)=[256(K+1)]^{20K}q^{2K}.
\tag{11}
\]

There is no missing fifth loss factor: the binomial coefficient and
(1/\ell!) are scalar profile weights already accounted for below.

## 4. Independent profile EGF

Starting from (2), use five nonnegative coordinates
((\ell,\rho,e,\sigma,f)) with sum (q+1).  For one determinant side,
the absolute leading profile weight is

\[
\frac1{\ell!2^{\rho+e+\sigma+f}
\rho!e!\sigma!f!}
\binom{q+1-\ell}{a},
\quad r=2\ell+e+f+a.
\tag{12}
\]

Summing (a) first yields ((1+z)^{\rho+e+\sigma+f}).  If (y)
marks the coordinate sum, the five independent EGFs are

\[
e^{yz^2},\quad
e^{y(1+z)/2},\quad e^{yz(1+z)/2},\quad
e^{y(1+z)/2},\quad e^{yz(1+z)/2}.
\]

Their product is

\[
\exp\{y(1+2z+2z^2)\}.
\tag{13}
\]

There are two determinant sides and the outer marked factor is four.
Therefore the exact absolute baseline mass is

\[
S_{q,r}=\frac8{(q+1)!}
[z^r](1+2z+2z^2)^{q+1}.
\tag{14}
\]

Let (a_{q,r}=[z^r](1+2z+2z^2)^q).  Incrementing the leftmost digit
below two in a weighted word gives

\[
a_{q,r-1}\le q a_{q,r},\qquad
a_{q,r-2}\le q^2a_{q,r}.
\tag{15}
\]

This remains valid at (r=0) by the zero convention and at (r=2q)
because every source word still has an incrementable digit.  Since

\[
L_{q,r}=\frac4{q!}a_{q,r},
\]

(14)--(15) give

\[
\frac{S_{q,r}}{L_{q,r}}
=\frac{2(a_{q,r}+2a_{q,r-1}+2a_{q,r-2})}
{(q+1)a_{q,r}}
\le10q.
\tag{16}
\]

No exponential-in-(q) profile-count factor is present.

## 5. Apparent loss and root bound

Every profile in (2) has apparent degree

\[
2(e+\rho)+2(f+\sigma)+2\ell=2q+2.
\]

The exact polynomial (C_{q,r}) has degree (2q) with leading
coefficient (L_{q,r}>0).  Hence apparent losses zero and one cancel,
and the coefficient of (s^{2q-k}) is at apparent loss (K=k+2).
Equations (11) and (16) imply the previous estimate

\[
\frac{|[s^{2q-k}]C_{q,r}|}{L_{q,r}}
\le10q[256(k+3)]^{20(k+2)}q^{2(k+2)}.
\tag{17}
\]

For (1\le k\le2q), the displayed elementary inequalities in the
previous proof give

\[
\frac{|[s^{2q-k}]C_{q,r}|}{L_{q,r}}
\le\{(4096q)^{67}\}^k.
\tag{18}
\]

If (s\ge2(4096q)^{67}), division by (L_{q,r}s^{2q}>0) leaves the
strict lower bound

\[
1-\sum_{k=1}^{2q}2^{-k}=2^{-2q}>0.
\]

The threshold exceeds (6q+4), so the stable combinatorial range is
automatic.  Finally,

\[
q\le s^{1/67}/8192
\quad\Longrightarrow\quad
2(4096q)^{67}\le2^{-66}s<s.
\]

The (q=0) case is the exact identity (C_{0,0}=4).  This closes every
normalization, endpoint, profile, loss-index, boundary, and quantifier
gate.  The former pending claims are therefore promoted to `PROVED`.

## 6. Scope firewall

This audit proves the polynomial window only for the named
complete-split pooled disjoint-core alpha-squared layer.  It neither
proves the full base-four Newton conjecture nor arbitrary-host OPG-1757.
