# OPG-1757: uniform height and a growing positive deficit window

Date: 2026-08-01

Status: `PROVED__UNIFORM_HEIGHT__EVERY_CONSTANT_BELOW_ONE_THIRD_WINDOW`

## 1. Statement

This note concerns the complete-split pooled, disjoint-core
\(\alpha^2\) layer.  Put

\[
 n=2s-5-q,
 \qquad
 C_{q,r}(s)=
 \frac{[\beta^{2n+r}]B_n(s,\beta)}
 {n!s^{2s-8-2q+r}}
 \qquad(0\le r\le2q).
 \tag{1}
\]

The preceding endpoint-polynomiality theorem proves
\(C_{q,r}\in\mathbb Q[s]\), and the leading-symbol theorem proves

\[
 \deg C_{q,r}=2q,
 \qquad
 [s^{2q}]C_{q,r}
 =\frac4{q!}[z^r](1+2z+2z^2)^q
 \ge \frac4{q!}.
 \tag{2}
\]

For \(P(s)=\sum_jp_js^j\), write
\(\lVert P\rVert _1=\sum_j|p_j|\).  The missing uniform estimate is now
proved with the following explicit envelope: for every \(q\ge1\) and
every \(0\le r\le2q\),

\[
\boxed{
 \lVert C_{q,r}\rVert _1
 \le E_q
 :=7200(q+2)^6\,2^{2q+2}(2q+6)^{2q+2}.
}
\tag{3}
\]

In particular,

\[
 E_q\le(32q)^{12q}\le(32q)^{32q}.
 \tag{4}
\]

Thus the formerly conditional height lemma holds, for example with
\(K=32\).  More importantly, retaining (3), rather than discarding it
into (4), gives

\[
 \log(E_q q!/4)=(3+o(1))q\log q.
 \tag{5}
\]

Consequently, for **every fixed** \(0<c<1/3\), there is an effective
\(s_0(c)\) such that, simultaneously for every integer \(s\ge s_0(c)\),

\[
 0\le q\le c\frac{\log s}{\log\log s},\quad 0\le r\le2q
 \quad\Longrightarrow\quad
 [\beta^{2n+r}]B_n(s,\beta)>0.
 \tag{6}
\]

This improves the earlier claim of an unspecified sufficiently small
constant to every constant strictly below \(1/3\).  The number \(1/3\)
is the output of the present coefficient-height argument, not an
optimality claim.

## 2. One exact endpoint representation

Write \(\rho=c-1\), \(m=e+\rho\), \(D=2m\), \(\epsilon=s^{-1}\), and
\(u=\epsilon v\).  Set

\[
\begin{aligned}
 \Phi_\epsilon(t,v)&=\frac{e^{\epsilon vt}-1}{\epsilon v},\\
 V_\epsilon(t,v)&=t-\frac{t^2}{2}
 -\sum_{j\ge1}\frac{(j+1)\epsilon^jv^jt^{j+2}}{(j+2)!},\\
 J_\epsilon(t,v)&=1-te^{\epsilon vt}.
\end{aligned}
\tag{7}
\]

For \(P(t)=\sum_dp_dt^d\), define

\[
 \mathcal L_{\alpha,\epsilon}P
 =\sum_dp_dt^d\prod_{i=0}^{d-1}
       \{1-\epsilon(\alpha+i)\}\bigg|_{t=1}.
\tag{8}
\]

Equivalently, the contribution of \(p_dt^d\) in (8) is
\(p_d(s-\alpha)_d/s^d\).  The zero-, one-, and two-marked Lagrange
formulas, including cancellation of the two-marked path pole against the
Lagrange Jacobian, give the single exact identity

\[
\boxed{
 Q_{h,e,\rho+1}(s)
 =\frac{s^{D}}{\rho!}[v^e]\,
 \mathcal L_{h+2,\epsilon}
 \left[
 e^{(\Phi_\epsilon-t)/\epsilon}
 \left{
 e^{\epsilon vt}V_\epsilon^\rho
 +2^{-h}\rho J_\epsilon V_\epsilon^{\rho-1}
 \right}
 \right]
}
\tag{9}
\]

for \(h=0,1,2\); the second summand is absent when \(\rho=0\).
Formula (9) is the all-excess identity proved in
`LAURENT_DEGREE_LEMMA.md`.  We use it here without truncating the Laurent
order.

## 3. The atom budget and absence of an \(s\)-denominator

Expand the integrand in (9) as

\[
 \sum_{j,d,k}f_{j,d,k}\epsilon^jt^dv^k.
\tag{10}
\]

Every monomial contributing to \([v^e]\) satisfies

\[
\boxed{j+d\le 2(e+\rho)=D.}
\tag{11}
\]

Here is a complete class-by-class ledger.  An atom with \(v\)-degree
\(a\) has the indicated \(\epsilon\)-order plus \(t\)-degree.

| source | atom | order plus degree | available budget |
|---|---:|---:|---:|
| \(e^{(\Phi_\epsilon-t)/\epsilon}\) | \(\epsilon^{a-1}v^at^{a+1}/(a+1)!\), \(a\ge1\) | \(2a\) | \(2a\) |
| \(e^{\epsilon vt}\) | \((\epsilon vt)^a/a!\) | \(2a\) | \(2a\) |
| one \(V_\epsilon\) factor | \(t\) or \(-t^2/2\) | \(1\) or \(2\) | \(2\) |
| one \(V_\epsilon\) factor | \(- (a+1)\epsilon^av^at^{a+2}/(a+2)!\) | \(2a+2\) | \(2(a+1)\) |
| \(J_\epsilon\) | \(1\), \(-t\), or \(-\epsilon^av^at^{a+1}/a!\) | \(0,1,2a+1\) | \(2(a+1)\) |

The first summand in braces in (9) has \(\rho\) copies of \(V\); the
second has \(\rho-1\) copies and one \(J\).  Summing the last column at
total \(v\)-degree \(e\) proves (11) in both cases.

Now a monomial in (10) contributes exactly

\[
 \frac{f_{j,d,e}}{\rho!}
 s^{D-j-d}(s-h-2)_d
 \tag{12}
\]

to the endpoint.  Equation (11) makes the first exponent nonnegative.
This simultaneously handles every changing falling-factorial shift and
shows, term by term, that no \(s\)-dependent denominator remains.
Factorials in the scalar \(f_{j,d,e}/\rho!\) are constants in \(s\).

## 4. Explicit endpoint height

For an absolutely convergent formal series, let \(|F|(1,1,1)\) mean the
sum of the absolute values of all coefficients.  The four input series
in (9) have the uniform majorants

\[
\begin{aligned}
 \left|e^{(\Phi_\epsilon-t)/\epsilon}\right|(1,1,1)
 &=\exp\!\left(\sum_{a\ge1}\frac1{(a+1)!}\right)<3,\\
 |e^{\epsilon vt}|(1,1,1)&=e<3,\\
 |V_\epsilon|(1,1,1)
 &=1+\frac12+\sum_{a\ge1}\frac{a+1}{(a+2)!}=2,\\
 |J_\epsilon|(1,1,1)&=1+e<4.
\end{aligned}
\tag{13}
\]

It follows that the sum of the absolute scalar coefficients in the
whole integrand of (9), and hence also in its \([v^e]\)-slice, is at
most

\[
 3\{3\,2^\rho+4\rho\,2^{\rho-1}\}
 =(6\rho+9)2^\rho
 \le15(\rho+1)2^\rho.
\tag{14}
\]

For \(0\le d\le D\) and \(h+2\le4\), submultiplicativity of coefficient
norm gives

\[
 \lVert(s-h-2)_d\rVert _1
 \le\prod_{i=0}^{d-1}(1+h+2+i)
 \le(D+4)^d\le(D+4)^D.
\tag{15}
\]

The factor \(s^{D-j-d}\) does not change coefficient norm, and
\(1/\rho!\le1\).  Equations (12)--(15) prove the endpoint lemma

\[
\boxed{
 \lVert Q_{h,e,c}\rVert _1
 \le H_m:=15(m+1)2^m(2m+4)^{2m},
 \qquad m=e+c-1.
}
\tag{16}
\]

This estimate includes all zero-, one-, and two-marked endpoint classes;
there is no suppressed profile-dependent constant.

## 5. Exact master formula and its height

Let \((x)_\ell=x(x-1)\cdots(x-\ell+1)\).  Put

\[
 a=r-2\ell-e-f,
 \qquad c+d=q+3-\ell-e-f.
\tag{17}
\]

The normalized overlap/excess formula is exactly

\[
\begin{aligned}
 C_{q,r}(s)=4
 \sum_{\substack{0\le\ell\le\lfloor r/2\rfloor\\
                  e,f\ge0,\ 0\le a\le q+1-\ell\\
                  c,d\ge1,\ c+d=q+3-\ell-e-f}}
 \frac{\binom{q+1-\ell}{a}}{\ell!}
 \big[&
 (s-1-c-e)_\ell(s-1-d-f)_\ell
 Q_{1,e,c}Q_{1,f,d}\\
 &-(s-c-e)_\ell(s-2-d-f)_\ell
 Q_{0,e,c}Q_{2,f,d}\big].
\end{aligned}
\tag{18}
\]

This is already the coefficient after division by \(n!\) in (1).  The
factorial cancellation is rederived below, before any estimate.
Therefore no \(s\)-dependent \(n!\) is being estimated as a polynomial
coefficient.  The combinatorial derivation applies throughout the
inherited stable range \(s\ge6q+4\); since both sides of (18) are
polynomials after endpoint polynomiality, equality on those infinitely
many integers is the exact polynomial identity used for the norm bound.

### 5.1 Normalization and shift audit

Here is an independent ledger from the pre-normalized master formula.
An endpoint of type \((h,e,c)\) has order

\[
 j_{h,e,c}=s-h-c-e.
\tag{18a}
\]

Taking its \(\ell\)-th active-page generating-function derivative
contributes
\((j_{h,e,c})_\ell\).  Thus the two positive profiles
\((h,h')=(1,1)\) have shifts

\[
 s-(1+c+e),\qquad s-(1+d+f),
\]

and the negative profiles \((h,h')=(0,2)\) have shifts

\[
 s-(c+e),\qquad s-(2+d+f),
\]

exactly as displayed in (18).  In either determinant product
\(h+h'=2\), so substituting

\[
 H_{h,e,c}=2^h s^{s-h-2c-e}Q_{h,e,c}
\]

contributes the common marked weight \(2^{h+h'}=4\).  Before the
\(\lambda\)-coefficient is included, its power of \(s\) is

\[
 2s-2-2(c+d)-(e+f).
\]

The selected term of
\(\lambda^{q+1-\ell}=(1+s\beta)^{q+1-\ell}\) contributes
\(\binom{q+1-\ell}{a}s^a\).  Using

\[
 c+d=q+3-\ell-e-f,\qquad
 r=2\ell+e+f+a,
\]

the total power is exactly

\[
\begin{aligned}
 2s-2-2(c+d)-(e+f)+a
 &=2s-8-2q+2\ell+e+f+a\\
 &=2s-8-2q+r.
\end{aligned}
\tag{18b}
\]

It is therefore cancelled exactly by the power in (1); no missing
positive or negative power of \(s\) remains in (18).

The factorial ledger can also be read before differentiation.  The
ordered-chain identity supplies \(j!\) and \(k!\) for endpoint orders
\(j,k\), while pooled overlap supplies
\[
\frac{n!}{\ell!(j-\ell)!(k-\ell)!}.
\]
Their product is
\[
\frac{n!}{\ell!}(j)_\ell(k)_\ell.
\]
After the \(n!\) in (1) is divided out, this leaves exactly
\(1/\ell!\) and the two falling factors in (18).  These are the only
master-level factorial denominators outside the endpoint polynomials
(the displayed binomial coefficient is an integer).

At \(q=0,r=0\), only
\(\ell=e=f=a=0\) and \((c,d)=(1,2),(2,1)\) occur.  Formula (9) gives

\[
\begin{aligned}
 Q_{h,0,1}&=1,\\
 Q_{0,0,2}&=(s-1)(s+6)/2,\\
 Q_{1,0,2}&=(s-2)(s+6)/2,\\
 Q_{2,0,2}&=(s^2+3s-20)/2.
\end{aligned}
\]

Hence \(2Q_{1,0,2}-Q_{0,0,2}-Q_{2,0,2}=1\), and (18) gives
\(C_{0,0}=4\), agreeing with (2).  At the other range boundaries,
\(r=0\) forces \(\ell=e=f=a=0\), while \(r=2q\) still has
\(0\le\ell\le q\) and is filtered only by the displayed condition
\(0\le a\le q+1-\ell\).  Thus neither endpoint requires a negative
overlap factorial, an out-of-range binomial coefficient, or a
negative-order falling factorial.

Set

\[
 m_1=e+c-1,\qquad m_2=f+d-1.
\]

The key conservation law, which avoids losing an unnecessary factor
\(q^{2q}\), is

\[
\boxed{m_1+m_2+\ell=q+1.}
\tag{19}
\]

All four shifts in (18) are at most \(q+4\), and \(\ell\le q\), so each
falling factorial has norm at most \((2q+4)^\ell\).  Combining it with
(16), and using (19), gives for either endpoint product in (18)

\[
\begin{aligned}
 &\lVert (s-A)_\ell(s-B)_\ell
       Q_{h,e,c}Q_{h',f,d}\rVert _1\\
 &\qquad\le
 225(q+2)^2 2^{q+1}(2q+6)^{2(q+1-\ell)}
 (2q+4)^{2\ell}\\
 &\qquad\le
 225(q+2)^2 2^{q+1}(2q+6)^{2q+2}.
\end{aligned}
\tag{20}
\]

The remaining finite ledger is explicit:

- at most \((q+1)(2q+1)^2(q+2)\le4(q+2)^4\) tuples
  \((\ell,e,f,c)\);
- \(\binom{q+1-\ell}{a}\le2^{q+1}\);
- \(1/\ell!\le1\);
- the outer factor is \(4\), and the determinant difference costs a
  further factor \(2\).

Multiplying these quantities by (20) proves (3).  Notice that restricted
binomial extraction, both endpoint products, every changing shift, and
all scalar factorial normalizations have been counted explicitly.

For completeness, when \(q\ge2\), the elementary inequalities

\[
 7200<32^3,\quad q+2\le2q,\quad 2q+6\le5q
\]

bound the right side of (3) by \((32q)^{4q+13}\), which is at most
\((32q)^{12q}\).  The case \(q=1\) is a direct numerical inequality.
This proves (4).

## 6. Positivity threshold and the \(1/3\) window

Write \(C_{q,r}(s)=L_{q,r}s^{2q}+P_{q,r}(s)\), with
\(\deg P_{q,r}\le2q-1\).  For \(s\ge1\), (2)--(3) imply

\[
 |P_{q,r}(s)|\le E_qs^{2q-1},
 \qquad L_{q,r}\ge4/q!.
\tag{21}
\]

Hence every natural-support coefficient is strictly positive whenever

\[
\boxed{s>T_q:=E_q q!/4.}
\tag{22}
\]

This threshold also exceeds the inherited stable-range requirement
\(s\ge6q+4\) for \(q\ge1\).  The case \(q=0\) is immediate from (2):
\(C_{0,0}=4\).  From (3),

\[
\begin{aligned}
\log T_q={}&\log1800+6\log(q+2)+(2q+2)\log2\\
&+(2q+2)\log(2q+6)+\log(q!).
\end{aligned}
\tag{23}
\]

This identity makes the logarithmic constant auditable.  Indeed,

\[
\lim_{q\to\infty}\frac{\log E_q}{q\log q}=2,
\qquad
\lim_{q\to\infty}\frac{\log(q!)}{q\log q}=1,
\qquad
\lim_{q\to\infty}\frac{\log T_q}{q\log q}=3.
\tag{24}
\]

The first limit follows term by term from (3).  The second follows, for
example, from
\(q\log q-q+1\le\log(q!)\le q\log q\).  Thus the three units in the
last limit consist of two from the combined endpoint/overlap polynomial
height and one from the smallest leading coefficient \(4/q!\).

For a proof of the quantifiers in (6) that does not use \(o(1)\), fix
\(0<c<1/3\) and put

\[
 \eta=\frac{1/c-3}{2}>0,\qquad
 C_*=\log1800+6\log(4/3).
\tag{25}
\]

For \(q\ge6\), equation (23), \(q+2\le4q/3\),
\(2q+6\le3q\), and \(\log(q!)\le q\log q\) give

\[
 \log T_q
 \le3q\log q+
 \{8\log q+C_*+(2q+2)\log6\}.
\tag{26}
\]

Define the effective integer

\[
 q_0(\eta)=\left\lceil
 \max\left\{
 6,\,
 \exp(6\log6/\eta),\,
 \frac{2(8+C_*)}{\eta}
 \right\}
 \right\rceil.
\tag{27}
\]

For \(q\ge q_0(\eta)\), the last brace in (26) is at most
\(\eta q\log q\): the term \(3q\log6\) uses the exponential condition
in (27), while \(8\log q+C_*\) uses its final condition.  Therefore

\[
 \log T_q\le(3+\eta)q\log q
 \qquad(q\ge q_0(\eta)).
\tag{28}
\]

Choose \(s_0(c)\) larger than

\[
 \exp(\exp(\max\{1,c\}))
 \quad\hbox{and}\quad
 1+\max_{1\le q<q_0(\eta)}T_q.
\tag{29}
\]

For \(s\ge s_0(c)\), put \(L=\log s\).  If
\(q\le cL/\log L\), then \(q\le L\) and
\(\log q\le\log L\).  When \(q\ge q_0(\eta)\), equations (28) and (25)
give

\[
 \log T_q
 \le(3+\eta)cL
 =\frac{1+3c}{2}L<L.
\tag{30}
\]

When \(q<q_0(\eta)\), equation (29) gives \(s>T_q\) directly.  Together
with (22), this proves the exact quantifier
\[
 \text{for every fixed }0<c<1/3\text{ there exists }s_0(c)
 \text{ such that (6) holds for every }s\ge s_0(c).
\]

One entirely explicit but deliberately coarse corollary is

\[
 q\le\frac{\log s}{28\log\log s},\qquad s\ge e^{32},
\tag{31}
\]

because (4) and \(q!\le q^q\) give
\(T_q<(32q)^{13q}\), while
\(\log(32q)\le2\log\log s\) under (31).

## 7. Scope firewall

Proved here:

- the uniform endpoint height (16), with no unlisted endpoint class;
- the uniform master height (3), including all shifts and
  normalizations;
- an effective positivity threshold (22);
- simultaneous positivity throughout every window with constant
  \(c<1/3\).

Not proved by the raw monomial-height comparison in this note:

- positivity when \(q\) is a positive power of \(s\), or even when
  \(q\asymp\log s\);
- optimality of the constant \(1/3\);
- positivity of other pooled layers or arbitrary-host OPG-1757.

The companion POLYNOMIAL_GROWING_DEFICIT_WINDOW.md uses the stronger
loss-by-loss Laurent filtration, rather than the raw norm comparison,
and is undergoing independent audit.
