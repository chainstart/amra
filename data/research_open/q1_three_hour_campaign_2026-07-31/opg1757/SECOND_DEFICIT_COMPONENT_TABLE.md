# Exact component table for the second depth deficit

Date: 2026-07-31

## 1. Definition

For
\[
\mathbf w_h=(\underbrace{2,\ldots,2}_{h},
\underbrace{1,\ldots,1}_{s-2h}),\qquad h=0,1,2,
\]
let \(\mathcal H_{h,e}(x)\) be the complete weighted hyperforest
polynomial in which \(x\) marks hyperedges and
\[
e=\sum_E(|E|-2)
\]
is the total excess above binary edges.  Let
\[
H_{h,e,c}
=[x^{s-h-c-e}]\mathcal H_{h,e}(x)
\]
be the weight of the terms with \(c\) connected components.  The exact
normalization is
\[
\boxed{
H_{h,e,c}
=2^h s^{s-h-2c-e}P_{h,e,c}(s).
}
\tag{1}
\]

Only
\[
(e,c)\in
\{(0,1),(0,2),(0,3),(0,4),
(1,1),(1,2),(1,3),(2,1),(2,2),(3,1)\}
\]
are needed for \(B_{2s-7}\).

## 2. Complete table

For \(e=0\),
\[
P_{0,0,1}=P_{1,0,1}=P_{2,0,1}=1,
\]
\[
\begin{aligned}
P_{0,0,2}&=\frac{(s-1)(s+6)}2,\\
P_{1,0,2}&=\frac{(s-2)(s+6)}2,\\
P_{2,0,2}&=\frac{s^2+3s-20}2,
\end{aligned}
\]
\[
\begin{aligned}
P_{0,0,3}
&=\frac{(s-2)(s-1)(s^2+13s+60)}8,\\
P_{1,0,3}
&=\frac{(s-3)(s-2)(s^2+13s+60)}8,\\
P_{2,0,3}
&=\frac{(s-4)(s^3+10s^2+17s-210)}8,
\end{aligned}
\]
\[
\begin{aligned}
P_{0,0,4}
&=\frac{(s-3)(s-2)(s-1)
(s^3+21s^2+202s+840)}{48},\\
P_{1,0,4}
&=\frac{(s-4)(s-3)(s-2)
(s^3+21s^2+202s+840)}{48},\\
P_{2,0,4}
&=\frac{(s-5)(s-4)
(s^4+18s^3+133s^2+138s-3024)}{48}.
\end{aligned}
\]

For \(e=1\),
\[
\begin{aligned}
P_{0,1,1}&=\frac{(s-2)(s-1)}2,\\
P_{1,1,1}&=\frac{(s-3)(s-2)}2,\\
P_{2,1,1}&=\frac{(s-4)(s-3)}2,
\end{aligned}
\]
\[
\begin{aligned}
P_{0,1,2}
&=\frac{(s-3)(s-2)(s-1)(3s+20)}{12},\\
P_{1,1,2}
&=\frac{(s-4)(s-3)(s-2)(3s+20)}{12},\\
P_{2,1,2}
&=\frac{(s-5)(s-4)(3s^2+11s-66)}{12},
\end{aligned}
\]
\[
\begin{aligned}
P_{0,1,3}
&=\frac{(s-4)(s-3)(s-2)(s-1)
(3s^2+43s+210)}{48},\\
P_{1,1,3}
&=\frac{(s-5)(s-4)(s-3)(s-2)
(3s^2+43s+210)}{48},\\
P_{2,1,3}
&=\frac{(s-6)(s-5)(s-4)
(3s^3+34s^2+69s-728)}{48}.
\end{aligned}
\]

For \(e=2\),
\[
\begin{aligned}
P_{0,2,1}
&=\frac{(s-3)(s-2)(s-1)(3s-8)}{24},\\
P_{1,2,1}
&=\frac{(s-4)(s-3)(s-2)(3s-11)}{24},\\
P_{2,2,1}
&=\frac{(s-5)(s-4)(s-3)(3s-14)}{24},
\end{aligned}
\]
\[
\begin{aligned}
P_{0,2,2}
&=\frac{(s-4)(s-3)(s-2)(s-1)
(3s^2+11s-80)}{48},\\
P_{1,2,2}
&=\frac{(s-5)(s-4)(s-3)(s-2)
(3s^2+8s-102)}{48},\\
P_{2,2,2}
&=\frac{(s-6)(s-5)(s-4)
(3s^3-4s^2-145s+406)}{48}.
\end{aligned}
\]

For \(e=3\),
\[
\begin{aligned}
P_{0,3,1}
&=\frac{(s-4)^2(s-3)^2(s-2)(s-1)}{48},\\
P_{1,3,1}
&=\frac{(s-5)^2(s-4)^2(s-3)(s-2)}{48},\\
P_{2,3,1}
&=\frac{(s-6)^2(s-5)^2(s-4)(s-3)}{48}.
\end{aligned}
\]

## 3. Why finite reconstruction is exact

The displayed expressions themselves satisfy
\[
\deg_s P_{h,e,c}\leq2c+2e-2.
\tag{2}
\]
This displayed degree is not used as a premise.

The denominator-aware Abel proof in
`ABEL_EXCEPTIONAL_PROFILE_LEMMA.md` first establishes
\[
\boxed{
\frac{H_{h,e,c}}{2^hs^{s-h-2c-e}}
=\frac{N_{h,e,c}(s)}{s^e},
\qquad
\deg N_{h,e,c}\le2c+3e-2.
}
\tag{3}
\]
Consequently, after multiplying a proposed table identity by \(s^e\),
both sides have degree at most \(2c+3e-2\).  Equality at
\[
2c+3e-1
\tag{4}
\]
distinct values proves the identity without assuming in advance that the
normalized endpoint is a polynomial.

The verifier checks precisely those values for all 30 entries: 180 exact
endpoint values in total, from \(s=7\) through the required maximum
\(s=16\).  An independent direct-position implementation checks the same
180 values.  Thus the table consists of exact all-\(s\) identities rather
than fitted small cases.

## 4. Executable source

`verify_second_deficit.py` contains:

- the primitive weighted component-partition sum;
- the aggregated \(r\)-block contraction operator;
- unordered hyperedge enumeration with the exact \(1/m!\) factor;
- all 30 normalized polynomials in (1);
- the denominator-aware 180-value identity certificate.
