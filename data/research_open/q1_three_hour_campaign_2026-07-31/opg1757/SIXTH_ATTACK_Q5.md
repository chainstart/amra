# OPG-1757 sixth attack: complete closure of \(B_{2s-10}\)

Date: 2026-07-31

## 1. Exact theorem

Let \(s\ge5\) be an integer and put
\[
n=2s-10.
\]
Then
\[
\boxed{
B_{2s-10}(s,\beta)
=n!\,s^{2s-18}\beta^{4s-20}
\sum_{r=0}^{10}s^rP_r(s)\beta^r,
}
\tag{1}
\]
where
\[
\boxed{
\begin{aligned}
P_0
&=\frac{(s-5)(s-4)}{30}
(s^8+29s^7+321s^6+459s^5-23239s^4-161291s^3\\
&\hspace{38mm}+565356s^2+5972364s-18174240),\\
P_1
&=\frac{(s-5)(s-4)}9
(3s^8+68s^7+504s^6-1638s^5-45762s^4-122342s^3\\
&\hspace{38mm}+1328907s^2+3955734s-18174240),\\
P_2
&=\frac{(s-5)(s-4)}{18}
(30s^8+489s^7+1507s^6-27821s^5-221251s^4+486683s^3\\
&\hspace{38mm}+6647577s^2-10477962s-22921920),\\
P_3
&=\frac{4(s-5)(s-4)}{45}
(60s^8+600s^7-1660s^6-47888s^5-67659s^4+1513961s^3\\
&\hspace{38mm}+1517269s^2-20404086s+21846888),\\
P_4
&=\frac{(s-5)(s-4)}{45}
(540s^8+2040s^7-35935s^6-208854s^5+1192098s^4\\
&\hspace{38mm}+6034869s^3-29097509s^2-883302s+73389888),\\
P_5
&=\frac{2(s-5)(s-4)}{45}
(444s^8-1044s^7-29951s^6+35449s^5+1048166s^4\\
&\hspace{38mm}-2139865s^3-11917920s^2+40844052s-29418336),\\
P_6
&=\frac{(s-5)(s-4)(2s-11)}9
(108s^7-312s^6-5189s^5+13371s^4\\
&\hspace{38mm}+106278s^3-396539s^2+84492s+609444),\\
P_7
&=\frac{4(s-5)(s-4)(2s-11)(2s-9)}9
(12s^6-52s^5-365s^4+1758s^3+2151s^2-16288s+15300),\\
P_8
&=\frac{(s-5)(s-4)(2s-11)(2s-9)}{90}
(300s^6-3060s^5+4025s^4+50419s^3\\
&\hspace{38mm}-194938s^2+175488s+64656),\\
P_9
&=\frac{(s-5)(s-4)(2s-11)(2s-9)(2s-7)}{45}\\
&\qquad\times(s^2-s-8)(30s^3-345s^2+1255s-1398),\\
P_{10}
&=\frac{(s-5)(s-4)^2(s-3)(2s-11)(2s-9)(2s-7)}{90}\\
&\qquad\times(12s^3-136s^2+469s-446).
\end{aligned}
}
\tag{2}
\]
At \(s=5\), all eleven \(P_r\) vanish and
\[
\boxed{B_0(5,\beta)=0.}
\tag{3}
\]
For every integer \(s\ge6\),
\[
\boxed{
B_{2s-10}(s,\beta)>_{\mathrm{coeff}}0.
}
\tag{4}
\]

## 2. Exact \(q=5\) reduction and the count firewall

For \(0\le r\le10\), the master formula is
\[
\boxed{
\begin{aligned}
\frac{[\beta^{2n+r}]B_n}{n!}
={}&
\sum_{\ell=0}^{\lfloor r/2\rfloor}\frac1{\ell!}
\sum_{\substack{e+f+a=r-2\ell\\0\le a\le6-\ell}}
\binom{6-\ell}{a}s^a\\
&\quad\times[x^{n-\ell}]
\left(
\mathcal H_{1,e}^{(\ell)}\mathcal H_{1,f}^{(\ell)}
-
\mathcal H_{0,e}^{(\ell)}\mathcal H_{2,f}^{(\ell)}
\right),
\end{aligned}
}
\tag{5}
\]
with
\[
c+d+e+f=8-\ell.
\tag{6}
\]
Consequently the full endpoint set is
\[
\boxed{
\mathcal E_5
=
\{(h,e,c):h=0,1,2,\ 0\le e\le6,\ 1\le c\le7-e\}.
}
\tag{7}
\]
For each \(h\), it contains \(7+6+\cdots+1=28\) entries, hence
\[
\boxed{|\mathcal E_5|=84.}
\tag{8}
\]
The denominator-aware Abel count is
\[
\boxed{
\sum_{(h,e,c)\in\mathcal E_5}(2c+3e-1)=924.
}
\tag{9}
\]

There is a useful bookkeeping firewall:

- full endpoint proof: \(84\) entries and \(924\) values;
- if the top coefficient is supplied separately by the all-depth
  Stirling theorem: \(81\) entries and \(867\) values;
- \(81\) entries with \(924\) values is an inconsistent mixture and is
  not used.

`verify_sixth_q5.py` uses the complete \(84/924\) route over
\(10\le s\le28\).

## 3. Endpoint completeness

The \(63\) \(q=4\) formulas are inherited from `verify_fifth_q4.py`.
The \(21\) new boundary entries are
\[
(h,e,7-e),
\qquad h=0,1,2,\quad0\le e\le6,
\tag{10}
\]
and are displayed exactly in `_q5_endpoint_polynomials()` in the
verifier.  The generated certificate includes the factored formula for
every one of all \(84\) entries, not only the new boundary.

For each entry,
\[
H_{h,e,c}
=2^hs^{s-h-2c-e}Q_{h,e,c}(s),
\tag{11}
\]
and the Abel theorem gives before evaluation
\[
\deg(s^eQ_{h,e,c})\le2c+3e-2.
\tag{12}
\]
The \(924\) values therefore prove the complete table.  A posteriori,
every denominator cancels and
\[
Q_{h,e,c}\in\mathbb Q[s],
\qquad
\deg Q_{h,e,c}\le2c+2e-2.
\tag{13}
\]

The excess-six species are exhaustive because the exponential contraction
formula includes all eleven partitions of six:
\[
\begin{gathered}
6,\ 5+1,\ 4+2,\ 4+1+1,\ 3+3,\ 3+2+1,\\
3+1+1+1,\ 2+2+2,\ 2+2+1+1,\ 2+1+1+1+1,\ 1^6.
\end{gathered}
\tag{14}
\]
An excess part \(a\) represents a hyperedge of size \(a+2\).

## 4. Independent identity certificate

The boundary-factor theorem proves
\[
(s-4)(s-5)\mid R_{5,r}(s),
\tag{15}
\]
where
\[
\frac{[\beta^{2n+r}]B_n}
{n!\,s^{2s-18+r}}
=\frac{R_{5,r}(s)}{s^r},
\qquad
\deg R_{5,r}\le r+12.
\tag{16}
\]
After division by (15), the degree is at most \(r+10\).  Thus exactly
\[
r+11
\tag{17}
\]
non-boundary values prove offset \(r\).  The older primitive
page-transfer/Newton implementation independently compares
\(R_{5,r}\) with \(s^rP_r\) at these values.  The total is
\[
\sum_{r=0}^{10}(r+11)=176,
\tag{18}
\]
covering \(6\le s\le26\).  It also separately checks \(B_0(5,\beta)=0\).
This certificate does not import the sixth-attack verifier.

## 5. Strict sign proof

The \(s=u+5\) expansion is not coefficientwise positive, so it is not used
for the sign proof.  Instead put
\[
u=s-6.
\]
Exact expansion gives
\[
P_r(u+6)=\sum_{j=0}^{10}a_{r,j}u^j.
\tag{19}
\]
The coefficient rows \((a_{r,0},\ldots,a_{r,10})\) are:
\[
\begin{aligned}
r=0:\;&
\left(93312,\frac{2339928}{5},\frac{4665454}{5},
\frac{2783630}{3},\frac{2923055}{6},\frac{2048696}{15},
\frac{61703}{3},\frac{5383}{3},\frac{278}{3},\frac83,\frac1{30}\right),\\
r=1:\;&
\left(559872,2835012,\frac{16834940}{3},\frac{50069267}{9},
\frac{8908507}{3},\frac{7856716}{9},143208,\frac{123778}{9},
\frac{2342}{3},\frac{221}{9},\frac13\right),\\
r=2:\;&
\left(1461888,7483110,\frac{44620136}{3},\frac{269034097}{18},
\frac{74482007}{9},\frac{23481533}{9},\frac{4278947}{9},
\frac{459854}{9},\frac{29066}{9},\frac{673}{6},\frac53\right),\\
r=3:\;&
\left(2184192,\frac{170250544}{15},\frac{1032565712}{45},
\frac{1069905412}{45},\frac{125144240}{9},\frac{214806208}{45},
\frac{43846708}{45},\frac{5322928}{45},\frac{75664}{9},
\frac{976}{3},\frac{16}{3}\right),\\
r=4:\;&
\left(2066688,\frac{164699836}{15},\frac{1030167224}{45},
\frac{124305771}{5},\frac{140289608}{9},\frac{29426743}{5},
\frac{60835606}{45},\frac{934409}{5},\frac{135805}{9},
\frac{1972}{3},12\right),\\
r=5:\;&
\left(1294848,\frac{35500384}{5},\frac{46442296}{3},
\frac{804577664}{45},\frac{109446238}{9},\frac{228857234}{45},
\frac{59376722}{45},\frac{9400736}{45},\frac{174178}{9},
960,\frac{296}{15}\right),\\
r=6:\;&
\left(545024,\frac{9354176}{3},\frac{64832306}{9},
\frac{80624875}{9},\frac{60046291}{9},\frac{27975733}{9},
\frac{8225308}{9},\frac{1497775}{9},\frac{160778}{9},
\frac{3068}{3},24\right),\\
r=7:\;&
\left(152576,\frac{2762720}{3},\frac{20526200}{9},
\frac{27767212}{9},\frac{22819876}{9},1322820,
\frac{3980068}{9},\frac{278896}{3},\frac{104960}{9},
\frac{7040}{9},\frac{64}{3}\right),\\
r=8:\;&
\left(27264,\frac{877028}{5},\frac{7052854}{15},
\frac{31392877}{45},\frac{11462497}{18},\frac{16824073}{45},
\frac{12839171}{90},\frac{1564288}{45},\frac{46220}{9},
\frac{1232}{3},\frac{40}{3}\right),\\
r=9:\;&
\left(2816,\frac{97372}{5},\frac{2561324}{45},
\frac{4194349}{45},\frac{855185}{9},\frac{2838727}{45},
\frac{1242031}{45},\frac{352696}{45},\frac{12376}{9},
\frac{400}{3},\frac{16}{3}\right),\\
r=10:\;&
\left(128,\frac{4786}{5},\frac{137918}{45},
\frac{166871}{30},\frac{57221}{9},\frac{431347}{90},
\frac{108739}{45},\frac{36236}{45},\frac{1528}{9},
\frac{184}{9},\frac{16}{15}\right).
\end{aligned}
\tag{20}
\]
Every number in (20) is strictly positive.  This proves (4) for every
integer \(s\ge6\), with no numerical root cutoff.

## 6. Executable evidence and scope

The complete certificate schema is
`amra.opg1757.sixth_attack_q5.v1`; its digest is
```
b57014668227d7981c207f93a051d6c497ea59417414721874792a13ecfd955e
```
The independent coefficient certificate digest is
```
cb48205d645974aeebee2b371ea11db3b01ce7b19225dd6bb2c77dd9bfd4d754
```

This proves exactly the complete-split pooled layer \(B_{2s-10}\), hence
the six deepest nonzero layers \(q=0,\ldots,5\).

It does **not** prove positivity for arbitrary fixed \(q\), all \(B_n\),
the full disjoint-core \(\alpha^2\) layer, or arbitrary-host OPG-1757.
