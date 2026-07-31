# OPG-1757: an eight-layer positive window for the general fixed-page kernel

Date: 2026-07-30

## 1. Statement

Let \(H_h^{(k)}(s,\beta)\), \(h=0,1,2\), be the weighted bipartite
forest polynomials for the three contracted core profiles
\[
(1^s),\qquad (2,1^{s-2}),\qquad (2,2,1^{s-4}),
\]
with \(k\) labelled page vertices.  The inherited fixed-page theorem
defines \(K_k\) by
\[
\boxed{
(H_1^{(k)})^2-H_0^{(k)}H_2^{(k)}
=2k(k-1)\beta^4(1+k\beta)^{2s-2k-2}K_k(s,\beta).
}
\tag{1}
\]

The coefficients through rank four were proved previously.  The new
result is:

> **Theorem.**  For every pair of integers \(k\ge4\), \(s\ge4\),
> \[
> \boxed{
> [\beta^r]K_k(s,\beta)>0\qquad(0\le r\le8).
> }
> \tag{2}
> \]
> In particular, the new ranks \(r=5,6,7,8\) are positive on the full
> rectangular parameter domain, including \(s<k\).

For \(k=2\), \(K_2=1\).  For \(k=3\), \(\deg_\beta K_3=4\), so the four
new coefficients vanish.  Thus (2) is the strict stable statement,
with the expected low-\(k\) boundary.

This is an all-\(k\), all-\(s\) theorem.  It is not a computation of
the ninth or tenth ordinary-symbol rank.

## 2. Positive forms

Put
\[
m=k-4,\qquad v=s-4.
\tag{3}
\]
For \(r=5,6,7,8\), exact reduction gives
\[
\boxed{
[\beta^r]K_k(s,\beta)
=\frac{(m+1)(m+2)}{c_r}Q_r(m,v),
}
\tag{4}
\]
where
\[
(c_5,c_6,c_7,c_8)=(15,90,315,2520).
\tag{5}
\]
Every monomial coefficient of every \(Q_r\) is a strictly positive
integer.  For auditability, write \(Q_r=\sum_bv^bQ_{r,b}(m)\).  The
complete coefficient table is:

\[
\begin{aligned}
Q_{5,0}={}&4m^8+148m^7+2383m^6+21475m^5+115920m^4\\
&+372752m^3+675904m^2+633344m+238080,\\
Q_{5,1}={}&20m^6+610m^5+7595m^4+47684m^3\\
&+148463m^2+188958m+88560,\\
Q_{5,2}={}&15m^4+350m^3+3000m^2+10225m+7260;
\end{aligned}
\tag{6}
\]

\[
\begin{aligned}
Q_{6,0}={}&8m^{10}+348m^9+6802m^8+77753m^7+566619m^6\\
&+2694844m^5+8263904m^4+15763776m^3\\
&+17830144m^2+10824192m+2672640,\\
Q_{6,1}={}&60m^8+2260m^7+36675m^6+327248m^5\\
&+1690598m^4+4864167m^3+6999538m^2\\
&+5134704m+1451520,\\
Q_{6,2}={}&90m^6+2805m^5+35525m^4+223320m^3\\
&+658510m^2+625110m+224640,\\
Q_{6,3}={}&15m^4+360m^3+3210m^2+11415m+7200;
\end{aligned}
\tag{7}
\]

\[
\begin{aligned}
Q_{7,0}={}&8m^{12}+396m^{11}+9002m^{10}+123101m^9
+1113941m^8\\
&+6916784m^7+29636600m^6+86367296m^5
+166604288m^4\\
&+206024448m^3+154480640m^2+62631936m+10321920,\\
Q_{7,1}={}&84m^{10}+3724m^9+73521m^8+836962m^7
+5930603m^6\\
&+26297104m^5+69926588m^4+104653374m^3\\
&+93814622m^2+42539808m+7741440,\\
Q_{7,2}={}&210m^8+8085m^7+133385m^6+1195404m^5\\
&+6018299m^4+15546426m^3+15806189m^2
+9531102m+1935360,\\
Q_{7,3}={}&105m^6+3360m^5+43785m^4+281925m^3\\
&+819840m^2+560805m+161280;
\end{aligned}
\tag{8}
\]

\[
\begin{aligned}
Q_{8,0}={}&16m^{14}+880m^{13}+22584m^{12}+355640m^{11}
+3799777m^{10}\\
&+28761787m^9+156527812m^8+610454896m^7\\
&+1678963648m^6+3180677376m^5+4042908672m^4\\
&+3306735616m^3+1616863232m^2+414941184m+41287680,\\
Q_{8,1}={}&224m^{12}+11312m^{11}+260176m^{10}+3556532m^9\\
&+31568390m^8+186445800m^7+722516464m^6\\
&+1762356850m^5+2618937242m^4+2587578982m^3\\
&+1342448476m^2+404527872m+41287680,\\
Q_{8,2}={}&840m^{10}+38080m^9+764470m^8+8759324m^7\\
&+61168667m^6+255064061m^5+569933651m^4\\
&+557677645m^3+471886954m^2+113993628m+15482880,\\
Q_{8,3}={}&840m^8+33180m^7+561050m^6+5124210m^5\\
&+25722200m^4+60828810m^3+33443690m^2
+22703940m+2580480,\\
Q_{8,4}={}&105m^6+3465m^5+46935m^4+316155m^3\\
&+951825m^2+517335m+161280.
\end{aligned}
\tag{9}
\]

Equations (3)--(9) prove positivity immediately.

## 3. Why the finite reconstruction proves an unbounded identity

Let
\[
D_k=\sum_{d\ge4}d_d(k,s)\beta^d,\qquad
2k(k-1)\beta^4K_k=\sum_{d\ge4}n_d(k,s)\beta^d.
\]
Coefficient extraction from (1) gives the exact deconvolution
\[
\boxed{
n_d=d_d-\sum_{p=1}^{d-4}
\binom{2s-2k-2}{p}k^p n_{d-p}.
}
\tag{10}
\]

A pair of forests with \(d\) total edges mentions at most \(d\)
page labels and at most \(d\) core labels.  Sorting the objects by the
sets of labels they use proves that \(d_d(k,s)\) has binomial-basis
degree at most \(d\) in each population variable.  The already proved
low numerators and induction in (10) then give
\[
\boxed{
\deg_k n_d\le2d-6,\qquad \deg_s n_d\le d
\quad(9\le d\le12).
}
\tag{11}
\]
Indeed the \(p\)-th deconvolution term has \(k\)-degree at most
\[
2p+\bigl(2(d-p)-6\bigr)=2d-6
\]
and \(s\)-degree at most \(p+(d-p)=d\).

Consequently the exact rectangle
\[
0\le k\le2d-6,\qquad 4\le s\le d+4
\tag{12}
\]
uniquely determines \(n_d\).  The verifier evaluates the primitive
page-partition transfer with integer arithmetic on all of (12), performs
(10), and obtains (4)--(9).  It additionally evaluates two parameter
pairs outside each rectangle.  Thus the calculation is a bounded
certificate for polynomial identities valid at every \(k,s\), not a
finite parameter scan.

## 4. Independent reconstruction

`independent_verify_general_k_beta5_beta8.py` does not use the
page-partition transfer.  It writes every bipartite forest as a set of
connected components.  If a nontrivial component uses core set \(I\),
page set \(J\), and core weights \(w_i\), its weighted Cayley factor is
\[
\boxed{
|J|^{|I|-1}
\left(\sum_{i\in I}w_i\right)^{|J|-1}
\prod_{i\in I}w_i.
}
\tag{13}
\]
A recurrence on the component containing the least unused core vertex
therefore reconstructs \(H_0,H_1,H_2\) independently and checks all four
new coefficients at five parameter pairs, including \(s<k\).

## 5. Scope

The theorem doubles the previously proved general kernel window from
\(\beta^0,\ldots,\beta^4\) to \(\beta^0,\ldots,\beta^8\).  It does not
prove coefficientwise positivity of every \(K_k\), and it does not
remove the alternating binomial inversion that defines the pooled
layers \(F_k\) and \(B_k\).  Hence the complete \(\alpha^2\) layer and
OPG-1757 remain open.

Reproduction:

```bash
pytest -q data/research_open/q1_four_problem_campaign_2026-07-30/opg1757
```
