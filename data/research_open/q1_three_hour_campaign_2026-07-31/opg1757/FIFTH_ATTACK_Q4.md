# OPG-1757 fifth attack: complete closure of \(B_{2s-9}\)

Date: 2026-07-31

## 1. Exact theorem

Let \(s\) be an integer with \(s\ge5\), and put
\[
n=2s-9.
\]
Then
\[
\boxed{
B_{2s-9}(s,\beta)
=n!\,s^{2s-16}\beta^{4s-18}
\sum_{r=0}^{8}s^rP_r(s)\beta^r,
}
\tag{1}
\]
where
\[
\boxed{
\begin{aligned}
P_0(s)
&=\frac{(s-5)(s-4)}6
(s^6+25s^5+229s^4+211s^3-10101s^2-36081s+183330),\\
P_1(s)
&=\frac{4(s-5)(s-4)}3
(s^6+19s^5+111s^4-321s^3-5409s^2-3867s+61110),\\
P_2(s)
&=\frac{2(s-5)(s-4)}9
(24s^6+312s^5+565s^4-11427s^3-42073s^2+165669s+98280),\\
P_3(s)
&=\frac{4(s-5)(s-4)}{15}
(50s^6+355s^5-1420s^4-16156s^3+21221s^2+186954s-305424),\\
P_4(s)
&=\frac{(s-5)(s-4)}3
(68s^6+88s^5-3185s^4-3446s^3+64500s^2-77429s-68112),\\
P_5(s)
&=\frac{4(s-5)(s-4)}9
(60s^6-264s^5-1967s^4+10074s^3+10232s^2-96345s+103680),\\
P_6(s)
&=\frac{8(s-5)(s-4)(2s-9)}3
(4s^5-22s^4-54s^3+489s^2-704s-18),\\
P_7(s)
&=\frac43(s-5)(s-4)(2s-9)(2s-7)
(s^2-s-8)(2s^2-13s+19),\\
P_8(s)
&=\frac1{90}(s-5)(s-4)(s-3)(2s-9)(2s-7)\\
&\qquad\times(60s^3-600s^2+1865s-1706).
\end{aligned}
}
\tag{2}
\]
The \(s=5\) specialization is the combined exact expression: all nine
\(P_r(5)\) vanish and
\[
\boxed{B_1(5,\beta)=0.}
\tag{3}
\]
For every integer \(s\ge6\),
\[
\boxed{
B_{2s-9}(s,\beta)>_{\mathrm{coeff}}0.
}
\tag{4}
\]
There is no claim for \(s=4\), because \(2s-9=-1\) is not a pooled depth.

## 2. The \(q=4\) finite reduction

For \(0\le r\le8\), the overlap/excess identity is
\[
\boxed{
\begin{aligned}
\frac{[\beta^{2n+r}]B_n}{n!}
={}&
\sum_{\ell=0}^{\lfloor r/2\rfloor}\frac1{\ell!}
\sum_{\substack{e+f+a=r-2\ell\\0\le a\le5-\ell}}
\binom{5-\ell}{a}s^a\\
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
The component orders obey
\[
c+d+e+f=7-\ell.
\tag{6}
\]
Thus the exact endpoint set is
\[
\boxed{
\mathcal E_4
=
\left\{
(h,e,c):
h\in\{0,1,2\},\
0\le e\le5,\
1\le c\le6-e
\right\}.
}
\tag{7}
\]
It has \(63\) entries.  Overlap orders \(0,\ldots,4\) all occur.

The seven excess-five partitions are all present:

- one \(7\)-edge;
- a \(6\)-edge and a \(3\)-edge;
- a \(5\)-edge and a \(4\)-edge;
- a \(5\)-edge and two \(3\)-edges;
- two \(4\)-edges and a \(3\)-edge;
- a \(4\)-edge and three \(3\)-edges;
- five \(3\)-edges.

This exhausts the new species rather than selecting only positive
contributions.

## 3. The 63 endpoint formulas

Use the normalization
\[
H_{h,e,c}
=2^h s^{s-h-2c-e}Q_{h,e,c}(s).
\tag{8}
\]
The 45 formulas in \(\mathcal E_3\) are inherited verbatim from
`verify_fourth_q3.py`.  The 18 new boundary formulas are:
\[
\begin{aligned}
Q_{0,0,6}
&=\frac{(s-5)(s-4)(s-3)(s-2)(s-1)}{3840}\\
&\quad\times(s^5+40s^4+835s^3+10960s^2+87636s+332640),\\
Q_{1,0,6}
&=\frac{(s-6)(s-5)(s-4)(s-3)(s-2)}{3840}\\
&\quad\times(s^5+40s^4+835s^3+10960s^2+87636s+332640),\\
Q_{2,0,6}
&=\frac{(s-7)(s-6)(s-5)(s-4)}{3840}\\
&\quad\times(s^6+37s^5+705s^4+8095s^3+48626s^2+12792s-1235520),
\end{aligned}
\tag{9}
\]
\[
\begin{aligned}
Q_{0,1,5}
&=\frac{(s-6)(s-5)(s-4)(s-3)(s-2)(s-1)}{2304}\\
&\quad\times(3s^4+98s^3+1557s^2+13766s+55440),\\
Q_{1,1,5}
&=\frac{(s-7)(s-6)(s-5)(s-4)(s-3)(s-2)}{2304}\\
&\quad\times(3s^4+98s^3+1557s^2+13766s+55440),\\
Q_{2,1,5}
&=\frac{(s-8)(s-7)(s-6)(s-5)(s-4)}{2304}\\
&\quad\times(3s^5+89s^4+1239s^3+8435s^2+6546s-201960),
\end{aligned}
\tag{10}
\]
\[
\begin{aligned}
Q_{0,2,4}
&=\frac{(s-6)(s-5)(s-4)(s-3)(s-2)(s-1)}{1152}\\
&\quad\times(3s^4+58s^3+383s^2-928s-20160),\\
Q_{1,2,4}
&=\frac{(s-7)(s-6)(s-5)(s-4)(s-3)(s-2)}{1152}\\
&\quad\times(3s^4+55s^3+308s^2-1734s-23760),\\
Q_{2,2,4}
&=\frac{(s-8)(s-7)(s-6)(s-5)(s-4)}{1152}\\
&\quad\times(3s^5+43s^4+59s^3-3437s^2-19132s+97020),
\end{aligned}
\tag{11}
\]
\[
\begin{aligned}
Q_{0,3,3}
&=\frac{(s-6)(s-5)(s-4)(s-3)(s-2)(s-1)}{5760}\\
&\quad\times(15s^4+90s^3-945s^2-7556s+40544),\\
Q_{1,3,3}
&=\frac{(s-7)(s-6)(s-5)(s-4)(s-3)(s-2)}{1920}\\
&\quad\times(5s^4+20s^3-425s^2-2432s+19008),\\
Q_{2,3,3}
&=\frac{(s-8)(s-7)(s-6)(s-5)(s-4)}{5760}\\
&\quad\times(15s^5-15s^4-1725s^3-1471s^2+101012s-260460),
\end{aligned}
\tag{12}
\]
\[
\begin{aligned}
Q_{0,4,2}
&=\frac{(s-6)(s-5)(s-4)(s-3)(s-2)(s-1)}{11520}\\
&\quad\times(15s^4-110s^3-795s^2+8546s-18368),\\
Q_{1,4,2}
&=\frac{(s-7)(s-6)(s-5)(s-4)(s-3)(s-2)}{11520}\\
&\quad\times(15s^4-155s^3-660s^2+11536s-31296),\\
Q_{2,4,2}
&=\frac{(s-8)(s-7)(s-6)(s-5)(s-4)}{11520}\\
&\quad\times(15s^5-245s^4+135s^3+16701s^2-98142s+158976),
\end{aligned}
\tag{13}
\]
and
\[
\begin{aligned}
Q_{0,5,1}
&=\frac{(s-6)^2(s-5)^2(s-4)(s-3)(s-2)(s-1)}{11520}
(3s^2-29s+64),\\
Q_{1,5,1}
&=\frac{(s-7)^2(s-6)^2(s-5)(s-4)(s-3)(s-2)}{11520}
(3s^2-35s+96),\\
Q_{2,5,1}
&=\frac{(s-8)^2(s-7)^2(s-6)(s-5)(s-4)(s-3)}{11520}
(3s^2-41s+134).
\end{aligned}
\tag{14}
\]

The Abel lemma proves a priori that
\[
s^eQ_{h,e,c}(s)
\quad\text{has degree at most}\quad
2c+3e-2.
\tag{15}
\]
Therefore the complete endpoint table requires
\[
\sum_{(h,e,c)\in\mathcal E_4}(2c+3e-1)
=588
\tag{16}
\]
exact values.  `verify_fifth_q4.py` checks exactly those \(588\) values
over \(9\le s\le24\).  All displayed \(Q_{h,e,c}\) turn out to be
polynomials of degree at most \(2c+2e-2\), but this stronger cancellation
is an output, not an interpolation assumption.

## 4. Nine exact coefficient formulas

Substitution of all 63 endpoints in (5) makes every term share
\[
s^{2s-16+r}.
\tag{17}
\]
The complete symbolic sum over
\[
(\ell,e,f,a,c,d)
\]
then simplifies to (2).  All possible endpoint denominators cancel.

There is also a non-circular identity certificate.  Put
\[
C_{4,r}(s)
=
\frac{[\beta^{2n+r}]B_n}
{n!\,s^{2s-16+r}}.
\tag{18}
\]
The fixed-deficit theorem proves
\[
C_{4,r}(s)=\frac{R_{4,r}(s)}{s^r},
\qquad
\deg R_{4,r}\le r+10.
\tag{19}
\]
The older primitive page-transfer/Newton engine independently evaluates
\(R_{4,r}\).  Comparing it with \(s^rP_r(s)\) at exactly \(r+11\)
values proves one identity.  Across \(r=0,\ldots,8\), this is
\[
\sum_{r=0}^{8}(r+11)=135
\tag{20}
\]
independent exact values, with the largest sample \(s=24\).  Hence the
nine formulas are not inferred from a short numerical pattern.

## 5. Full sign proof

Let \(u=s-5\).  In increasing powers of \(u\),
\[
\begin{aligned}
P_0(u+5)
={}&2275u+\frac{103759}{6}u^2+26358u^3
+\frac{40790}{3}u^4+\frac{7385}{3}u^5
+214u^6+\frac{28}{3}u^7+\frac16u^8,\\
P_1(u+5)
={}&14400u+\frac{249572}{3}u^2+\frac{364576}{3}u^3
+\frac{194800}{3}u^4+13480u^5
+\frac{4040}{3}u^6+\frac{200}{3}u^7+\frac43u^8,\\
P_2(u+5)
={}&\frac{99700}{3}u+\frac{1489928}{9}u^2
+\frac{721124}{3}u^3+\frac{1248290}{9}u^4
+\frac{103492}{3}u^5+\frac{36794}{9}u^6
+\frac{704}{3}u^7+\frac{16}{3}u^8,\\
P_3(u+5)
={}&\frac{191328}{5}u+\frac{534268}{3}u^2+267392u^3
+\frac{518060}{3}u^4+\frac{260532}{5}u^5
+\frac{22448}{3}u^6+508u^7+\frac{40}{3}u^8,\\
P_4(u+5)
={}&24456u+\frac{339989}{3}u^2+\frac{549181}{3}u^3
+\frac{407414}{3}u^4+\frac{149369}{3}u^5
+8881u^6+732u^7+\frac{68}{3}u^8,\\
P_5(u+5)
={}&\frac{26840}{3}u+\frac{392620}{9}u^2
+\frac{235756}{3}u^3+\frac{614104}{9}u^4
+\frac{91556}{3}u^5+\frac{61876}{9}u^6
+\frac{2128}{3}u^7+\frac{80}{3}u^8,\\
P_6(u+5)
={}&1832u+\frac{29576}{3}u^2+\frac{61288}{3}u^3
+\frac{63320}{3}u^4+\frac{34832}{3}u^5
+\frac{10000}{3}u^6+448u^7+\frac{64}{3}u^8,\\
P_7(u+5)
={}&192u+1184u^2+2892u^3+\frac{10832}{3}u^4
+\frac{7412}{3}u^5+\frac{2744}{3}u^6
+\frac{496}{3}u^7+\frac{32}{3}u^8,\\
P_8(u+5)
={}&\frac{119}{15}u+\frac{1033}{18}u^2+\frac{503}{3}u^3
+\frac{4603}{18}u^4+\frac{3296}{15}u^5
+\frac{956}{9}u^6+\frac{80}{3}u^7+\frac83u^8.
\end{aligned}
\tag{21}
\]
The constant term is zero in every row and every coefficient of
\(u,\ldots,u^8\) is strictly positive.  Thus (3)--(4) follow immediately.

## 6. Executable evidence and scope

The main certificate has schema
`amra.opg1757.fifth_attack_q4.v1` and digest
```
d7077e98219656bd21bdf5c4b322690a0cc91e40727ae44d376fca7be4eb159c
```
The independent coefficient certificate has digest
```
4522fb4b1e0a4180f38314fb4244ba5f35ff645d476d369d388a510475225815
```

This proves exactly the complete-split pooled layer \(B_{2s-9}\).  It
closes the five deepest nonzero layers \(q=0,1,2,3,4\).

It does **not** prove arbitrary fixed \(q\), all \(B_n\), the full
disjoint-core \(\alpha^2\) layer, or arbitrary-host OPG-1757.  No
arbitrary-\(q\) induction is claimed.
