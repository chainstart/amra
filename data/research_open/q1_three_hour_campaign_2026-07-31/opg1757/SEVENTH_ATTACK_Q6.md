# OPG-1757 seventh attack: complete closure of \(B_{2s-11}\)

Date: 2026-07-31

## 1. Exact theorem

Let \(s\ge6\) be an integer and put \(n=2s-11\).  Then
\[
\boxed{
B_{2s-11}(s,\beta)
=n!s^{2s-20}\beta^{4s-22}
\sum_{r=0}^{12}s^rP_r(s)\beta^r.
}
\tag{1}
\]
The thirteen factors are
\[
\begin{aligned}
P_0={}&\frac{F}{180}(s^9+39s^8+667s^7+5064s^6-10918s^5
-512106s^4\\
&\hspace{26mm}-2462113s^3+15195399s^2+108066951s-385491960),\\
P_1={}&\frac{F}{45}(3s^9+97s^8+1309s^7+5982s^6-57396s^5
-834688s^4\\
&\hspace{26mm}-1331401s^3+27140127s^2+71718471s-385491960),\\
P_2={}&\frac{F}{90}(36s^9+922s^8+8823s^7+2697s^6-647927s^5
-3900203s^4\\
&\hspace{26mm}+12372203s^3+136241377s^2-161376108s-762037920),\\
P_3={}&\frac{F}{405}(630s^9+11925s^8+62010s^7-515024s^6
-7196322s^5\\
&\hspace{26mm}-5179532s^4+236824458s^3+309695827s^2
-3320427270s+2613794400),\\
P_4={}&\frac{F}{180}(780s^9+9600s^8-2795s^7-743576s^6
-3024266s^5\\
&\hspace{26mm}+23040040s^4+113327830s^3-480942194s^2
-518446149s+2114358750),\\
P_5={}&\frac{2F}{315}(1428s^9+8232s^8-88109s^7-881706s^6
+2148874s^5\\
&\hspace{26mm}+34670526s^4-60290564s^3-504561798s^2
+1398747555s-575672202),\\
P_6={}&\frac{F}{135}(1968s^9-1368s^8-152196s^7-177962s^6
+6502782s^5\\
&\hspace{26mm}+4420408s^4-154686372s^3+244336501s^2
+508123992s-1041647256),\\
P_7={}&\frac{2F}{45}(408s^9-2884s^8-21246s^7+148389s^6
+709230s^5\\
&\hspace{26mm}-5314587s^4-3005613s^3+71300470s^2
-138576132s+62098560),
\end{aligned}
\tag{2}
\]
where \(F=(s-4)(s-5)(s-6)\), and
\[
\begin{aligned}
P_8={}&\frac{F(2s-11)}{180}(1560s^8-12260s^7-48130s^6
+519793s^5+526163s^4\\
&\hspace{34mm}-11229722s^3+21034223s^2+14038365s-45227700),\\
P_9={}&\frac{F(2s-11)(2s-9)}{135}(420s^7-4020s^6-2565s^5
+119107s^4\\
&\hspace{42mm}-214808s^3-906217s^2+3037523s-2155500),\\
P_{10}={}&\frac{F(2s-11)(2s-9)}{90}(144s^7-2264s^6+10144s^5
+11306s^4\\
&\hspace{42mm}-208341s^3+525041s^2-290924s-271056),\\
P_{11}={}&\frac{F(2s-11)(2s-9)^2(2s-7)(s^2-s-8)}{45}\\
&\hspace{34mm}\times(6s^3-77s^2+307s-358),\\
P_{12}={}&\frac{F(s-3)(2s-11)(2s-9)(2s-7)}{11340}\\
&\hspace{34mm}\times(504s^5-10836s^4+90342s^3-360955s^2
+677187s-457250).
\end{aligned}
\tag{3}
\]
At \(s=6\), every \(P_r\) vanishes and the exact boundary is
\[
\boxed{B_1(6,\beta)=0.}
\tag{4}
\]
For every integer \(s\ge7\),
\[
\boxed{B_{2s-11}(s,\beta)>_{\rm coeff}0.}
\tag{5}
\]

## 2. Complete endpoint reduction

At offset \(0\le r\le12\), overlap order \(\ell\) uses
\[
c+d+e+f=9-\ell.
\tag{6}
\]
Thus the exact endpoint set is
\[
\mathcal E_6=
\{(h,e,c):h=0,1,2,\ 0\le e\le7,\ 1\le c\le8-e\}.
\tag{7}
\]
It has
\[
|\mathcal E_6|=3(8+7+\cdots+1)=108
\tag{8}
\]
entries.  The denominator-aware Abel theorem assigns
\(2c+3e-1\) exact values to entry \((h,e,c)\), so the complete count is
\[
\boxed{
\sum_{(h,e,c)\in\mathcal E_6}(2c+3e-1)=1368.
}
\tag{9}
\]
The verifier checks all 108 entries and all 1,368 values over
\(11\le s\le32\).  The 84 old entries are inherited from \(q=5\); the
24 genuinely new entries are
\[
(h,e,8-e),\qquad h=0,1,2,\quad0\le e\le7.
\tag{10}
\]

## 3. Faster exact forest recurrence

The new boundary would be needlessly expensive with temporary component
labels.  The verifier instead anchors the component containing the first
exceptional block.  For a profile \((1^N,v_1,\ldots,v_p)\), choose a set
\(J\subseteq\{2,\ldots,p\}\) and \(k\) of the \(N\) unit vertices.  The
weighted Cayley contribution of that anchored component is
\[
\binom Nk
\left(v_1+\sum_{j\in J}v_j+k\right)^{|J|+k-1}
v_1\prod_{j\in J}v_j,
\tag{11}
\]
with the singleton value interpreted as one.  Recursing on the remaining
vertices partitions every forest exactly once.  If no exceptional block
remains, the same recurrence anchors the least labelled unit vertex and
uses \(m^{m-2}\) for a component of total size \(m\).

This is an exact re-indexing, not a numerical approximation.  As a code-path
firewall, 24 weighted-profile/component values are also compared with the
older temporary-label recurrence.  The hyperedge contraction recurrence is
unchanged and automatically includes all 15 partitions of excess seven.

## 4. Sharp independent identity certificate

Let \(R_{6,r}\) be the cleared numerator, so that
\[
\frac{[\beta^{2n+r}]B_n}{n!s^{2s-20+r}}
=\frac{R_{6,r}(s)}{s^r}.
\tag{12}
\]
The endpoint top-two theorem improves the former general estimate by two:
\[
\deg R_{6,r}\le 2q+r=12+r.
\tag{13}
\]
The boundary theorem gives
\[
F=(s-4)(s-5)(s-6)\mid R_{6,r}.
\tag{14}
\]
Consequently
\[
\deg(R_{6,r}/F)\le9+r,
\tag{15}
\]
and exactly \(10+r\) non-boundary values prove offset \(r\).  The total is
\[
\boxed{\sum_{r=0}^{12}(10+r)=208,}
\tag{16}
\]
covering \(7\le s\le28\).

`audit_seventh_q6_independent.py` uses the pre-existing primitive
page-transfer/Newton engine and does not import the seventh-attack verifier.
All 208 comparisons pass, as does the separate \(B_1(6,\beta)=0\) check.
Its SHA-256 digest is
`da7b0e5430ab29140cbf3847777a5790ce65fea1f3a161daecd35af706c45d25`.
The complete main certificate (endpoints, symbolic layers, recurrence
cross-checks, and independent point count) has SHA-256 digest
`73245de5eb600ffa7727ce130c362f76c71decc64236112aae496a4974d8c887`.

## 5. Strict sign proof

Put \(u=s-7\).  Exact expansion gives
\[
P_r(u+7)=\sum_{j=0}^{12}a_{r,j}u^j,
\qquad a_{r,j}>0
\quad(0\le r,j\le12).
\tag{17}
\]
The executable certificate records every rational \(a_{r,j}\), rather than
only testing values of \(s\).  Hence \(P_r(s)>0\) for every real \(s\ge7\),
which proves (5).  The common factor (14) proves the boundary (4).

## 6. Reproduction and scope

Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_seventh_q6.py
PYTHONDONTWRITEBYTECODE=1 python3 audit_seventh_q6_independent.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify_seventh_q6.py
```

This closes only the \(q=6\) complete-split pooled layer.  It does not prove
all fixed deficits, all \(B_n\), the complete \(\alpha^2\) layer, or
OPG-1757 for arbitrary host graphs.
