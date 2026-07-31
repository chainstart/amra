# OPG endpoint top-two theorem and the improved fixed-deficit degree bound

Date: 2026-07-31

Status:
`ALL_EXCESS_TOP_TWO_ASYMPTOTICS_PROVED__ALL_FIXED_Q_DEGREE_BOUND_IMPROVED`

This theorem concerns the complete-split pooled model only. It does not
prove positivity at arbitrary deficit or arbitrary-host OPG-1757.

## 1. Endpoint statement

Let \(H_{h,e,c}(s)\) be the complete weighted hyperforest endpoint used in
the fixed-deficit reduction, where \(h\in\{0,1,2\}\) is the number of
prescribed disjoint binary core edges already contracted, \(e\ge0\) is
the total nonbinary excess, and \(c\ge1\) is the number of components.

The denominator-aware Abel theorem makes
\[
Q_{h,e,c}(s)
:=
\frac{H_{h,e,c}(s)}
{2^h s^{s-h-2c-e}}
\tag{1}
\]
an exact rational function of \(s\). Put
\[
D_{e,c}=2c+2e-2,
\qquad
A_{e,c}
=\frac1{2^{c+e-1}(c-1)!\,e!},
\tag{2}
\]
and
\[
b_{h,e,c}
=
\frac{(15-4e)(c-1)-e(4e+5)}3
-h(c+2e-1).
\tag{3}
\]
Then, as an identity of formal Laurent expansions at \(s=\infty\),
\[
\boxed{
Q_{h,e,c}(s)
=
A_{e,c}s^{D_{e,c}}
+A_{e,c}b_{h,e,c}s^{D_{e,c}-1}
+O_{e,c}(s^{D_{e,c}-2}).
}
\tag{4}
\]
When \(D_{e,c}=0\), (4) means only the leading constant statement. No
analytic limit or unproved uniform error estimate is used.

The 84 exact endpoint polynomials needed for \(q\le5\) agree with (4).
That finite agreement is a regression audit, not the proof of the
all-\(e,c\) quantifier.

## 2. Rooted-hypertree derivation for \(h=0\)

Let \(u\) mark nonbinary excess. The EGF \(T=T(z,u)\) of rooted complete
hypertrees obeys
\[
T
=z\exp\!\left(\frac{e^{uT}-1}{u}\right).
\tag{5}
\]
Indeed, after removing the root, its incident hyperedges form a set, and
an edge with \(k\) other rooted branches has excess \(k-1\).

The dissymmetry theorem gives the unrooted hypertree series
\[
V(t,u)
=t+\frac{e^{ut}-1-ut}{u^2}
-\frac{t(e^{ut}-1)}u.
\tag{6}
\]
For \(u=0\), this is \(t-t^2/2\), the ordinary unrooted-tree series.
A forest of \(c\) components has EGF \(V(T,u)^c/c!\), so
\[
H_{0,e,c}(s)
=s![z^su^e]\frac{V(T,u)^c}{c!}.
\tag{7}
\]

Write
\[
\Phi(t,u)=\frac{e^{ut}-1}{u}.
\]
The derivative of (6) is \(\partial_tV=1-te^{ut}\). Lagrange inversion
turns (7) into the exact formula
\[
H_{0,e,c}(s)
=\frac{(s-1)!}{(c-1)!}
[t^{s-1}u^e]\,
V(t,u)^{c-1}(1-te^{ut})e^{s\Phi(t,u)}.
\tag{8}
\]

Separate \(e^{st}\) and put \(u=v/s\). For a polynomial
\(P(t)=\sum_dp_dt^d\), coefficient extraction against \(e^{st}\) uses
\[
\mathcal L_sP
:=
\sum_dp_d\frac{(s-1)_d}{s^d}.
\tag{9}
\]
With \(D=t\partial_t\),
\[
\begin{aligned}
\mathcal L_sP
=\bigg[
1-\frac{D(D+1)}{2s}
&+\frac1{2s^2}
\left\{
\left(\frac{D(D+1)}2\right)^2
-\frac{D(D+1)(2D+1)}6
\right\}\\
&+O(s^{-3})
\bigg]P\Big|_{t=1}.
\end{aligned}
\tag{10}
\]

The required input expansions are
\[
\begin{aligned}
V(t,v/s)
&=t-\frac{t^2}2-\frac{vt^3}{3s}
-\frac{v^2t^4}{8s^2}+O(s^{-3}),\\
1-te^{vt/s}
&=1-t-\frac{vt^2}s-\frac{v^2t^3}{2s^2}
+O(s^{-3}),\\
e^{s(\Phi(t,v/s)-t)}
&=e^{vt^2/2}
\left[
1+\frac{v^2t^3}{6s}
+\frac1{s^2}
\left(\frac{v^3t^4}{24}+\frac{v^4t^6}{72}\right)
+O(s^{-3})
\right].
\end{aligned}
\tag{11}
\]
Substitution into (10) is finite algebra. The first two surviving
coefficient-generating functions, after the leading zero at \(t=1\), are
\[
L_1(v)=2^{1-c}e^{v/2},
\tag{12}
\]
\[
L_2(v)
=
2^{1-c}e^{v/2}
\left(
-\frac{4cv-30c+2v^2+5v+30}{6}
\right).
\tag{13}
\]
Because replacing \(u\) by \(v/s\) contributes \(s^e\), equations
(8)--(13) give
\[
Q_{0,e,c}(s)
=
\frac{s^{D_{e,c}}}{(c-1)!}
\left(
[v^e]L_1(v)
+\frac{[v^e]L_2(v)}s
+O(s^{-2})
\right).
\tag{14}
\]
Now
\[
\frac{[v^e]L_1(v)}{(c-1)!}=A_{e,c},
\]
and direct extraction from (13) gives
\[
\frac{[v^e]L_2(v)}{[v^e]L_1(v)}
=
\frac{(15-4e)(c-1)-e(4e+5)}3.
\tag{15}
\]
This proves (4) for \(h=0\).

## 3. Prescribed binary edges

We use once the following one-mark leading term.  For one exceptional
block of weight \(a\), put \(N=s-a\).  The exact \(p=1\) marked-Abel
formula is
\[
\mathcal F_c(1^N,a)
=
\Lambda_{s,a}
\left(
\frac{(1-t)U(t)^{c-1}}{(c-1)!}
\right).
\tag{15a}
\]
For
\[
P(t)=\frac{(1-t)U(t)^{c-1}}{(c-1)!}
\]
one has
\[
P(1)=0,\qquad
(t\partial_t)P(1)
=-\frac1{2^{c-1}(c-1)!},
\qquad
t^2P''(1)=0,
\]
where the last equality uses \(U'(1)=0\).  If
\(P(t)=\sum_dp_dt^d\), then
\[
\Lambda_{s,a}(P)
=s^N\sum_dp_d\frac{(N)_d}{s^d},
\qquad
\frac{(N)_d}{s^d}
=1-\frac{ad+d(d-1)/2}{s}+O(s^{-2}).
\]
Thus \(P(1)=0\), the displayed first derivative, and
\(\sum_dd(d-1)p_d=t^2P''(1)=0\) give
\[
\boxed{
\mathcal F_c(1^N,a)
=
\frac{a\,s^{N-1}}{2^{c-1}(c-1)!}
+O_{a,c}(s^{N-2}).
}
\tag{15b}
\]
This is exactly the exceptional-profile input needed below.  In the
leading excess-\(e\) stratum, the \(e\) ternary-edge contribution is still
the \(e\)-th coefficient of \(e^{v/2}\) from (12); (15b) shows that the
single initial exceptional block changes only its removed weight factor,
not \(A_{e,c}\).

For a hyperforest \(F\) in (7), let \(m(F)\) be its number of nonbinary
edges. Its number of binary edges is exactly
\[
b(F)=s-c-e-m(F).
\tag{16}
\]
The leading term in (12) comes from \(e\) ternary hyperedges, so
\[
m(F)=e
\tag{17}
\]
through the leading \(s^{D_{e,c}}\) stratum. Every record with fewer
nonbinary edges loses at least one degree in \(s\).  More precisely, if
\(W_m\) is the contribution with \(m\) nonbinary edges, the incidence
degree ledger gives
\[
W_{e-k}/s^{s-2c-e}=O(s^{D_{e,c}-k})
\qquad(k\ge1).
\tag{17a}
\]

Let \(W(a)\) mark every binary edge by \(a\), and write \(W=W(1)\). By
symmetry,
\[
\binom s2 H_{1,e,c}=W'(1)=\sum_F b(F).
\tag{18}
\]
After inserting (16)--(17) and the normalization (1), equation (18)
gives
\[
Q_{1,e,c}(s)
=A_{e,c}s^{D_{e,c}}
+A_{e,c}\{b_{0,e,c}-(c+2e-1)\}s^{D_{e,c}-1}
+O(s^{D_{e,c}-2}).
\tag{19}
\]

For two prescribed binary edges, differentiate twice. Ordered pairs of
disjoint binary edges number
\[
\frac{s(s-1)(s-2)(s-3)}4,
\]
while ordered adjacent pairs number \(s(s-1)(s-2)\). Let
\(H_{\angle,e,c}\) denote the endpoint with two prescribed adjacent
binary edges. Contracting those edges creates one exceptional block of
weight three. The marked Abel leading term is independent of the fixed
exceptional profile after its product of block weights is removed, hence
\[
H_{\angle,e,c}
=3s^{s-2c-e-2}
\left(A_{e,c}s^{D_{e,c}}+O(s^{D_{e,c}-1})\right).
\tag{20}
\]
Therefore
\[
W''(1)
=
\frac{s(s-1)(s-2)(s-3)}4H_{2,e,c}
+s(s-1)(s-2)H_{\angle,e,c}.
\tag{21}
\]
On the other hand, (16)--(17) give
\[
\frac{W''(1)}{s^{s-2c-e}}
=A_{e,c}s^{D_{e,c}+2}
\left[
1+\frac{b_{0,e,c}-2c-4e-1}{s}
+O(s^{-2})
\right].
\tag{22}
\]
For completeness, the error order in (22) is not inferred by simply
replacing every \(m(F)\) with \(e\).  The exact identity is
\[
\sum_F b(F)(b(F)-1)
=s^2W-s\{(2c+2e+1)W+2M\}+O(W),
\qquad
M=\sum_Fm(F).
\tag{22a}
\]
Equation (17a) gives
\[
M-eW=O\!\left(s^{s-2c-e+D_{e,c}-1}\right).
\]
After the extra factor \(s\) in (22a), this discrepancy is two orders
below the leading \(s^{s-2c-e+D_{e,c}+2}\) term.  Thus only
\(M=eW\) at leading order is needed for the coefficient of \(s^{-1}\)
in (22).
Substituting (20) into (21), and using
\[
\frac{s}{(s-1)(s-2)}
=\frac1s\left(1+\frac3s+O(s^{-2})\right),
\]
yields
\[
b_{2,e,c}=b_{0,e,c}-2(c+2e-1).
\tag{23}
\]
Equations (19) and (23) finish (4).

## 4. Consequence for every fixed deficit

Fix \(q\ge0\), \(0\le r\le2q\), and use
\[
C_{q,r}(s)=\frac{R_{q,r}(s)}{s^r}
\tag{24}
\]
from the fixed-deficit theorem. In a master-formula summand, put
\[
A=(e,c),\qquad B=(f,d).
\]
The component-order equation is
\[
c+d+e+f=q+3-\ell.
\tag{25}
\]
Including the two \(\ell\)-fold falling factorials, the apparent maximum
degree is
\[
D_{e,c}+D_{f,d}+2\ell=2q+2.
\tag{26}
\]

The degree \(2q+2\) cancels term by term because the leading endpoint
coefficient \(A_{e,c}\) is independent of \(h\). For the next degree put
\[
\kappa_{e,c}=c+2e-1.
\]
The falling-factor shifts agree on the positive and negative sides:
\[
(1+c+e)+(1+d+f)
=(c+e)+(2+d+f).
\tag{27}
\]
After the leading cancellation, the ordered endpoint pair contributes a
multiple of
\[
A_{e,c}A_{f,d}
(\kappa_{f,d}-\kappa_{e,c}).
\tag{28}
\]
The master sum contains the transposed pair \((B,A)\) with the same
prefactor; its contribution is the negative of (28). Thus degree
\(2q+1\) also cancels.

The denominator-aware theorem already proves that \(R_{q,r}\) is a
polynomial. Equations (26)--(28) improve its degree bound by two:
\[
\boxed{\deg R_{q,r}\le2q+r.}
\tag{29}
\]

Combining (29) with the boundary factor
\[
F_q(s)=\prod_{j=4}^{\lfloor(q+6)/2\rfloor}(s-j),
\qquad m_q=\deg F_q,
\]
a proposed offset formula needs only
\[
\boxed{2q+r+1-m_q}
\tag{30}
\]
nonboundary exact values. For \(q=5\), this is \(r+9\), or 154 values
over all eleven offsets. The already completed 176-value independent
certificate remains valid; (30) is a sharper theorem discovered
afterward.

## 5. Scope firewall

Proved:

- the all-\(e,c\), \(h=0,1,2\) top-two endpoint expansion (4);
- the all-fixed-\(q\) degree bound (29);
- the reduced certificate count (30).

Not proved:

- that every \(Q_{h,e,c}\) is a polynomial rather than a rational
  function;
- that every \(C_{q,r}\) has its denominator cancelled;
- positivity for arbitrary fixed \(q\);
- all pooled depths or arbitrary-host OPG-1757.
