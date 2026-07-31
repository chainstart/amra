# OPG-1757 fourth attack: complete closure of \(B_{2s-8}\)

Date: 2026-07-31

## 1. The theorem and its exact quantifiers

Let \(s\) be an integer with \(s\ge4\), and put
\[
n=2s-8.
\]
Then
\[
\boxed{
B_{2s-8}(s,\beta)
=n!\,s^{2s-14}\beta^{4s-16}
\sum_{r=0}^{6}s^rP_r(s)\beta^r,
}
\tag{1}
\]
where
\[
\boxed{
\begin{aligned}
P_0(s)
&=\frac23(s-4)
\left(
s^5+16s^4+52s^3-587s^2-3063s+12240
\right),\\
P_1(s)
&=\frac43(s-4)
\left(
3s^5+31s^4-16s^3-1217s^2-1038s+12240
\right),\\
P_2(s)
&=\frac23(s-4)
\left(
18s^5+85s^4-678s^3-3138s^2+13195s-2475
\right),\\
P_3(s)
&=\frac83(s-4)
\left(
8s^5-6s^4-314s^3+432s^2+2847s-5265
\right),\\
P_4(s)
&=\frac23(s-4)(2s-9)
\left(
18s^4-29s^3-391s^2+1054s-312
\right),\\
P_5(s)
&=\frac43(s-4)(2s-9)(2s-7)(3s-7)
(s^2-s-8),\\
P_6(s)
&=\frac23(s-4)(s-3)(2s-9)(2s-7)
(2s^2-11s+13).
\end{aligned}
}
\tag{2}
\]
At \(s=4\), (1) is interpreted as the combined exact expression.  Every
\(P_r(4)\) is zero and the structural boundary is
\[
\boxed{B_0(4,\beta)=0.}
\tag{3}
\]
For every integer \(s\ge5\), all seven displayed coefficients are strictly
positive:
\[
\boxed{
B_{2s-8}(s,\beta)>_{\mathrm{coeff}}0
\qquad(s\ge5).
}
\tag{4}
\]
Thus the theorem is not merely a stable-range assertion.  Its precise range
is: zero at the only boundary \(s=4\), and coefficientwise strictly positive
for every integer \(s\ge5\).

## 2. Exact overlap/excess reduction

For \(0\le r\le6\), the fixed-deficit master formula with \(q=3\) is
\[
\boxed{
\begin{aligned}
\frac{[\beta^{2n+r}]B_n}{n!}
={}&
\sum_{\ell=0}^{\lfloor r/2\rfloor}\frac1{\ell!}
\sum_{\substack{e+f+a=r-2\ell\\0\le a\le4-\ell}}
\binom{4-\ell}{a}s^a\\
&\quad\times[x^{n-\ell}]
\left(
\mathcal H_{1,e}^{(\ell)}\mathcal H_{1,f}^{(\ell)}
-
\mathcal H_{0,e}^{(\ell)}\mathcal H_{2,f}^{(\ell)}
\right).
\end{aligned}
}
\tag{5}
\]
Here \(0\le\ell\le3\).  If the two endpoints have \(c,d\) components,
their orders give
\[
c+d+e+f=6-\ell.
\tag{6}
\]
Since \(c,d\ge1\), no individual excess above four can occur.  The exact
endpoint set is therefore
\[
\boxed{
\mathcal E_3
=
\left\{
(h,e,c):
h\in\{0,1,2\},\
0\le e\le4,\
1\le c\le5-e
\right\},
}
\tag{7}
\]
which has \(45\) entries.

The excess-four exponential contains every partition of four:

- one \(6\)-edge;
- one \(5\)-edge and one \(3\)-edge;
- two \(4\)-edges;
- one \(4\)-edge and two \(3\)-edges;
- four \(3\)-edges.

Thus neither the endpoint set nor (5) suppresses an unfavourable
hyperedge species.

## 3. The 45 endpoint formulas and 345-point proof

Write
\[
H_{h,e,c}
=2^h s^{s-h-2c-e}Q_{h,e,c}(s).
\tag{8}
\]
The \(30\) entries with
\[
(e,c)\in
\{(0,1\!:\!4),(1,1\!:\!3),(2,1\!:\!2),(3,1)\}
\]
are exactly the formulas already displayed in
`SECOND_DEFICIT_COMPONENT_TABLE.md`.  The fifteen new boundary entries
needed for \(q=3\) are as follows:
\[
\begin{aligned}
Q_{0,0,5}
&=\frac{(s-4)(s-3)(s-2)(s-1)}{384}
(s^4+30s^3+451s^2+3846s+15120),\\
Q_{1,0,5}
&=\frac{(s-5)(s-4)(s-3)(s-2)}{384}
(s^4+30s^3+451s^2+3846s+15120),\\
Q_{2,0,5}
&=\frac{(s-6)(s-5)(s-4)}{384}
(s^5+27s^4+353s^3+2289s^2+1354s-55440),
\end{aligned}
\tag{9}
\]
\[
\begin{aligned}
Q_{0,1,4}
&=\frac{(s-5)(s-4)(s-3)(s-2)(s-1)}{96}
(s^3+23s^2+234s+1008),\\
Q_{1,1,4}
&=\frac{(s-6)(s-5)(s-4)(s-3)(s-2)}{96}
(s^3+23s^2+234s+1008),\\
Q_{2,1,4}
&=\frac{(s-7)(s-6)(s-5)(s-4)}{96}
(s^4+20s^3+159s^2+202s-3600),
\end{aligned}
\tag{10}
\]
\[
\begin{aligned}
Q_{0,2,3}
&=\frac{(s-5)(s-4)(s-3)(s-2)(s-1)}{576}
(9s^3+99s^2+74s-3360),\\
Q_{1,2,3}
&=\frac{(s-6)(s-5)(s-4)(s-3)(s-2)}{576}
(9s^3+90s^2-67s-4088),\\
Q_{2,2,3}
&=\frac{(s-7)(s-6)(s-5)(s-4)}{576}
(9s^4+54s^3-487s^2-4270s+16560),
\end{aligned}
\tag{11}
\]
\[
\begin{aligned}
Q_{0,3,2}
&=\frac{(s-5)(s-4)(s-3)(s-2)(s-1)}{1440}
(15s^3-15s^2-770s+2352),\\
Q_{1,3,2}
&=\frac{(s-6)(s-5)(s-4)(s-3)(s-2)}{1440}
(15s^3-45s^2-860s+3542),\\
Q_{2,3,2}
&=\frac{(s-7)(s-6)(s-5)(s-4)}{1440}
(15s^4-120s^3-725s^2+8122s-16176),
\end{aligned}
\tag{12}
\]
and
\[
\begin{aligned}
Q_{0,4,1}
&=\frac{(s-5)(s-4)(s-3)(s-2)(s-1)}{5760}
(15s^3-195s^2+830s-1152),\\
Q_{1,4,1}
&=\frac{(s-6)(s-5)(s-4)(s-3)(s-2)}{5760}
(15s^3-240s^2+1265s-2192),\\
Q_{2,4,1}
&=\frac{(s-7)(s-6)(s-5)(s-4)(s-3)}{5760}
(15s^3-285s^2+1790s-3712).
\end{aligned}
\tag{13}
\]

The denominator-aware Abel lemma proves before interpolation that
\[
s^eQ_{h,e,c}(s)
\quad\text{has degree at most}\quad
2c+3e-2.
\tag{14}
\]
Consequently one entry needs exactly
\[
2c+3e-1
\tag{15}
\]
distinct exact values.  Summing (15) over (7) gives
\[
\sum_{(h,e,c)\in\mathcal E_3}(2c+3e-1)=345.
\tag{16}
\]
`verify_fourth_q3.py` checks all \(345\) values, using \(8\le s\le20\).
This is an identity certificate under the already proved degree bound, not
an empirical fit.

The formulas in fact show the stronger a posteriori cancellation
\[
Q_{h,e,c}(s)\in\mathbb Q[s],
\qquad
\deg Q_{h,e,c}\le2c+2e-2,
\tag{17}
\]
but (17) is not assumed in the certificate.

## 4. Symbolic assembly of the seven coefficients

Substituting (8) into (5), including both falling factorials from the
\(\ell\)-fold derivatives, gives a common power
\[
s^{2s-14+r}.
\tag{18}
\]
The executable symbolic sum iterates every
\[
(\ell,e,f,a,c,d)
\]
satisfying (5)--(6).  Exact simplification yields precisely (2).  In
particular, the possible denominator \(s^r\) allowed by the general
fixed-deficit theorem cancels in every one of the seven \(q=3\)
coefficients.

This calculation also checks the general degree prediction
\[
\deg\!\left(s^rC_{3,r}(s)\right)\le r+8.
\tag{19}
\]
The actual normalized polynomials in (2) all have degree six.

## 5. All-parameter sign proof

Put \(u=s-5\).  In increasing powers of \(u\), exact expansion gives
\[
\begin{aligned}
P_0(u+5)
={}&1250+\frac{15934}{3}u+\frac{19870}{3}u^2
+\frac{8930}{3}u^3+442u^4+28u^5+\frac23u^6,\\
P_1(u+5)
={}&4500+18456u+\frac{69640}{3}u^2
+\frac{33188}{3}u^3+\frac{5840}{3}u^4
+\frac{436}{3}u^5+4u^6,\\
P_2(u+5)
={}&6450+26260u+34438u^2+\frac{54928}{3}u^3
+4038u^4+\frac{1106}{3}u^5+12u^6,\\
P_3(u+5)
={}&4720+\frac{59096}{3}u+\frac{83512}{3}u^2
+\frac{51104}{3}u^3+\frac{14080}{3}u^4
+\frac{1616}{3}u^5+\frac{64}{3}u^6,\\
P_4(u+5)
={}&1872+8262u+\frac{38794}{3}u^2
+\frac{27782}{3}u^3+\frac{9518}{3}u^4
+\frac{1432}{3}u^5+24u^6,\\
P_5(u+5)
={}&384+1840u+3260u^2+\frac{8296}{3}u^3
+1180u^4+\frac{704}{3}u^5+16u^6,\\
P_6(u+5)
={}&32+\frac{508}{3}u+\frac{1034}{3}u^2+350u^3
+188u^4+\frac{152}{3}u^5+\frac{16}{3}u^6.
\end{aligned}
\tag{20}
\]
Every coefficient in (20) is strictly positive.  Hence \(P_r(s)>0\)
for every \(s\ge5\) and every \(0\le r\le6\), proving (4) without root
estimates or a finite cutoff argument.

## 6. Non-circular independent audit

`audit_fourth_q3_independent.py` does not import the fourth-attack verifier.
It checks the result by two routes:

1. all \(345\) endpoint values are recomputed by enumerating subsets of
   current profile positions and evaluating the remaining forest through
   labelled component allocation, rather than the main equal-weight
   aggregation;
2. all seven final coefficients are recomputed from the primitive
   page-transfer and Newton-pooling engine for \(s=4,\ldots,16\).

The second route checks \(84\) positive coefficient rows, together with the
empty \(s=4\) boundary row.  The independent audit digest is
```
ee808d89398c3f05cd373e84b1d086a6039667d1221e4897554584fbfeccfdda
```
and the complete symbolic certificate digest is
```
b3a61e4490fe6c298a7ecb5d775942dcfc5586a6c9217efeae71e303ad0d552c
```

## 7. Scope firewall

The proved statement is exactly the complete-split pooled layer
\(B_{2s-8}\).  It closes \(q=3\), and therefore the four deepest nonzero
layers \(q=0,1,2,3\).

It does **not** prove positivity for arbitrary fixed \(q\), for all
\(B_n\), or for arbitrary host graphs in OPG-1757.  No induction in \(q\)
is asserted here.
