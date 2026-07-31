# OPG-1757: every fixed deficit is eventually coefficientwise positive

Date: 2026-07-31

Status:
`PROVED__ALL_FIXED_DEFICITS__EXACT_POSITIVE_LEADING_SYMBOL`

This note concerns only the complete-split pooled, disjoint-core
\(\alpha^2\) layer.  It closes the arbitrary-fixed-deficit asymptotic
problem; it does not give a threshold uniform in the deficit and does not
prove arbitrary-host OPG-1757.

The later companion `LOGARITHMIC_GROWING_DEFICIT_WINDOW.md` records a
conditional route toward the uniform range
\(q\le c_0\log s/\log\log s\).  Its remaining uniform-height lemma is
not used here.  The leading-symbol proof below is unconditional.

## 1. The theorem

Fix \(q\geq0\), put
\[
n=2s-5-q,
\]
and, for \(0\leq r\leq2q\), retain the exact rational normalization
\[
C_{q,r}(s)
=\frac{[\beta^{2n+r}]B_n(s,\beta)}
       {n!s^{2s-8-2q+r}}
=\frac{R_{q,r}(s)}{s^r}.
\tag{1}
\]
The fixed-deficit reduction proves that \(R_{q,r}\in\mathbb Q[s]\), and
the endpoint top-two theorem proves
\(\deg R_{q,r}\leq2q+r\).
The companion `ENDPOINT_POLYNOMIALITY_THEOREM.md` now also proves
\(s^r\mid R_{q,r}\), so \(C_{q,r}\) is itself a polynomial.  The leading
symbol below was derived independently of that stronger cancellation.

The new exact leading-symbol identity is
\[
\boxed{
[s^{2q+r}]R_{q,r}(s)
=\frac4{q!}[z^r](1+2z+2z^2)^q.
}
\tag{2}
\]
Every coefficient on the right of (2) is strictly positive.  Therefore
\[
\boxed{\deg R_{q,r}=2q+r}
\tag{3}
\]
for every admissible \((q,r)\), and, as a formal Laurent expansion at
infinity,
\[
C_{q,r}(s)
=\frac4{q!}[z^r](1+2z+2z^2)^q\,s^{2q}
+O_{q,r}(s^{2q-1}).
\tag{4}
\]
Equivalently,
\[
[\beta^{2n+r}]B_n
=\frac{4n!}{q!}[z^r](1+2z+2z^2)^q
 s^{2s-8+r}\bigl(1+O_{q,r}(s^{-1})\bigr).
\tag{5}
\]
No analytic uniformity is hidden in (4)--(5): all functions are exact
rational functions and the statements are their formal Laurent leading
terms.

Since there are only \(2q+1\) offsets, (2) immediately gives the
cross-layer conclusion:
\[
\boxed{
\text{For every fixed }q\geq0\text{ there is }S_q\text{ such that }
\text{every coefficient in the natural support }
\beta^{2n},\ldots,\beta^{2n+2q}\text{ is positive}
\quad(s\geq S_q).
}
\tag{6}
\]
Coefficients below \(\beta^{2n}\) are structurally zero, so (6) is
supportwise strict positivity, not literal strict positivity in every
ambient polynomial degree.

## 2. A marked one-block expansion

The missing information beyond the endpoint top-two theorem is only one
second difference in the prescribed-edge parameter.  We first compute a
subleading term for one exceptional block.

Let \(H^{(a)}_{e,c}(s)\) be the complete weighted hyperforest endpoint
with one block of fixed weight \(a\geq1\), \(s-a\) unit blocks, excess
\(e\), and \(c\) components.  Set
\[
D=2c+2e-2,
\qquad
A_{e,c}=\frac1{2^{c+e-1}(c-1)!e!},
\tag{7}
\]
and let \(b_{0,e,c}\) be the unmarked subleading ratio
\[
b_{0,e,c}
=\frac{(15-4e)(c-1)-e(4e+5)}3.
\tag{8}
\]
Then
\[
\boxed{
\frac{H^{(a)}_{e,c}(s)}
     {a s^{s-a+1-2c-e}}
=A_{e,c}s^D
+\left[
b_{0,e,c}-2(a-1)
\left(e+\frac{c-1}{a}\right)
\right]A_{e,c}s^{D-1}
+O_{a,e,c}(s^{D-2}).
}
\tag{9}
\]

Here is a direct derivation.  Write
\[
\Phi(t,u)=\frac{e^{ut}-1}{u},
\qquad
T=z e^{\Phi(T,u)},
\]
and let \(V(T,u)\) be the unrooted hypertree series from the endpoint
top-two theorem.  With \(N=s-a\), the exceptional component is rooted at
the weight-\(a\) block, so
\[
H^{(a)}_{e,c}(s)
=N![z^Nu^e]
e^{a\Phi(T,u)}\frac{V(T,u)^{c-1}}{(c-1)!}.
\tag{10}
\]
Lagrange inversion turns (10) into
\[
\frac{(N-1)!}{(c-1)!}[t^{N-1}u^e]e^{s\Phi(t,u)}
\left[
a e^{ut}V^{c-1}
+(c-1)V^{c-2}(1-te^{ut})
\right].
\tag{11}
\]
For a polynomial \(P(t)=\sum p_dt^d\), the relevant coefficient
functional is
\[
\mathcal L_{s,a}P
=\sum_dp_d\frac{(s-a-1)_d}{s^d}
=\left[
1-\frac{D_t(D_t+2a+1)}{2s}+O(s^{-2})
\right]P\bigg|_{t=1},
\tag{12}
\]
where \(D_t=t\partial_t\).  Substitute \(u=v/s\),
\[
V=t-\frac{t^2}{2}-\frac{vt^3}{3s}+O(s^{-2}),
\]
and
\[
e^{s(\Phi-t)}
=e^{vt^2/2}\left(1+\frac{v^2t^3}{6s}+O(s^{-2})\right).
\]
After division by the leading factor \(2^{1-c}e^{v/2}\), the order
\(s^{-1}\) expression differs from its \(a=1\) value by exactly
\[
-\frac{a-1}{a}\{av+2(c-1)\}.
\tag{13}
\]
Finally,
\[
\frac{[v^e]v e^{v/2}}{[v^e]e^{v/2}}=2e,
\]
which proves (9).  The executable verifier recomputes (11)--(13)
symbolically rather than assuming them.

Two checks on (9) are important.  At \(a=2\), it reproduces the known
one-prescribed-edge shift \(-(c+2e-1)\).  At \(a=3\), which represents
two adjacent prescribed binary edges, it gives
\[
b_{\angle,e,c}
=b_{0,e,c}-\frac43(c+3e-1).
\tag{14}
\]

## 3. Endpoint curvature in the prescribed matching

Write the three disjoint-edge endpoints in relative form
\[
Q_{h,e,c}(s)
=A_{e,c}s^D
\left(
1+\frac{b_{0,e,c}-h\kappa_{e,c}}s
+\frac{g_{h,e,c}}{s^2}+O(s^{-3})
\right),
\qquad
\kappa_{e,c}=c+2e-1.
\tag{15}
\]
The new curvature identity is
\[
\boxed{
g_{2,e,c}-2g_{1,e,c}+g_{0,e,c}
=\delta_{e,c},
}
\tag{16}
\]
where
\[
\boxed{
\delta_{e,c}
=c^2+(4e-5)c+4e^2-6e+4
=\kappa_{e,c}^2-3(c-1)-2e.
}
\tag{17}
\]

For completeness, (16) needs no full formula for any \(g_h\).  Let
\(W=H_{0,e,c}\), let \(m(F)\) count the nonbinary edges of a hyperforest,
and put \(M_j=\sum_Fm(F)^jw(F)\).  The number of binary edges is
\[
b(F)=s-c-e-m(F).
\tag{18}
\]
The incidence-degree ledger used in the endpoint theorem says that the
stratum \(m=e-k\) loses at least \(k\) powers of \(s\).  Consequently
\[
M_1=eW+O(s^{s-2c-e+D-1}),
\]
and
\[
M_2-e^2W
=(2e-1)(M_1-eW)+O(s^{s-2c-e+D-2}).
\tag{19}
\]
The latter identity holds because at the only relevant next stratum
\(m=e-1\),
\(m^2-e^2=(2e-1)(m-e)\).

Binary-edge marking gives the exact identities
\[
\binom{s}{2}H_{1,e,c}=(s-c-e)W-M_1,
\tag{20}
\]
and
\[
\begin{aligned}
&\frac{s(s-1)(s-2)(s-3)}4H_{2,e,c}
+s(s-1)(s-2)H_{\angle,e,c}\\
&\quad=(s-c-e)(s-c-e-1)W
-\{2(s-c-e)-1\}M_1+M_2.
\end{aligned}
\tag{21}
\]
Insert (14), (15), and (19) into (20)--(21).  If \(C=c+e\), all unknown
next-stratum terms cancel, leaving
\[
g_2-2g_1+g_0
=C^2+2Ce-9C-3b_\angle+3b_0+e^2-9e+8.
\tag{22}
\]
Equations (8) and (14) reduce (22) to (17).  Thus the only second-order
endpoint information needed by the determinant is explicit for every
\((e,c)\).

## 4. Collapse of the complete leading symbol

Consider one ordered endpoint pair
\[
A=(e,c),\qquad B=(f,d),
\]
at overlap \(\ell\).  Put
\[
\rho=c-1,\qquad\sigma=d-1.
\]
The component equation becomes
\[
\rho+e+\sigma+f=q+1-\ell=:N.
\tag{23}
\]
After the apparent degrees \(2q+2\) and \(2q+1\) cancel as in the
endpoint top-two theorem, expand the two falling factorials one order
further and average the ordered pair with its transpose.  Equations
(16)--(17) give the remaining kernel
\[
\boxed{
G(A,B,\ell)
=\kappa_A\kappa_B+\ell
-\frac{\delta_A+\delta_B}{2}.
}
\tag{24}
\]
Including the determinant normalization, its contribution per ordered
profile is \(4A_{e,c}A_{f,d}G(A,B,\ell)\).  The antisymmetric terms vanish
under \(A\leftrightarrow B\); (24) also holds directly on the diagonal.

It remains to sum (24), and this is where the unexpectedly simple positive
symbol appears.  Let \(z\) mark the beta offset.  Summing the lambda
degree contributes
\[
\sum_{a=0}^N\binom Na z^a=(1+z)^N.
\]
Put \(x=(1+z)/2\) and introduce a profile-size marker \(y\).  On one side,
\[
F(y)
=\sum_{\rho,e\geq0}\frac{(xy)^\rho(xzy)^e}{\rho!e!}
=\exp\left(\frac{(1+z)^2y}{2}\right).
\tag{25}
\]
The \(\kappa=\rho+2e\) moment is
\[
m=y x(1+2z)F,
\]
while \(\delta=\kappa^2-3\rho-2e\) has moment
\[
\{y^2x^2(1+2z)^2+2yx(z-1)\}F.
\]
Therefore the sum of (24) over the two profiles is exactly
\[
\boxed{
\{\ell+y(1-z^2)\}e^{y(1+z)^2}.
}
\tag{26}
\]

The overlap itself contributes \(z^{2\ell}/\ell!\).  Hence the complete
leading polynomial \(L_q(z)\) is
\[
\begin{aligned}
\frac{L_q(z)}4
&=\sum_{\ell=0}^{q+1}\frac{z^{2\ell}}{\ell!}
[y^{q+1-\ell}]
\{\ell+y(1-z^2)\}e^{y(1+z)^2}\\
&=\frac{z^2}{q!}\{(1+z)^2+z^2\}^q
+\frac{1-z^2}{q!}\{(1+z)^2+z^2\}^q\\
&=\frac1{q!}(1+2z+2z^2)^q.
\end{aligned}
\tag{27}
\]
This is (2).

## 5. Reproducible audit

Run the ordinary certificate:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 verify_fixed_deficit_leading_symbol.py
```

It checks:

- the marked one-block Lagrange calculation symbolically;
- (16) on all 28 endpoint profiles through the complete \(q=5\) table;
- the finite pre-collapse profile sum against (27) for \(0\leq q\leq7\);
- all 36 coefficients in the already proved exact layers \(q=0,\ldots,5\).

The certificate digest is
`cca70600865309db23389e5f584cf91d47a35a82e8348227afe199cdc36afbe0`.

The slower extended regression

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 verify_fixed_deficit_leading_symbol.py --extended-q6
```

checks all 36 endpoint profiles and all 49 exact-layer coefficients
through \(q=6\).  Its digest is
`56fc206f63f3227d19dbcc358281d505241e914e9e03f75cda62298c6d5fd6e5`.
These finite checks audit the proof; the all-\(q\) quantifier comes from
the generating-function identity (27), not extrapolation.

## 6. Scope firewall

**Proved here:**

- the exact positive leading symbol (2) for every fixed \(q,r\);
- the exact degree (3), improving a degree upper bound to equality;
- eventual strict positivity on the natural support (6) for every fixed
  deficit (with the structurally forced lower coefficients equal to zero).
- together with the companion endpoint theorem,
  \(C_{q,r}\in\mathbb Q[s]\) has exact degree \(2q\).

**Not proved here:**

- an explicit or uniform bound for \(S_q\);
- positivity when \(q=q(s)\) grows with \(s\);
- every pooled layer simultaneously for a fixed \(s\);
- the full complete-split Rayleigh difference or arbitrary-host OPG-1757.
