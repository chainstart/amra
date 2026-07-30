# OPG-1757: ordinary second-subleading symbol certificate

Date: 2026-07-30

> **Status update.**  This note is the original finite discovery
> certificate.  The missing all-loss resummation has now been proved
> in `ORDINARY_SECOND_SUBLEADING_SYMBOL_THEOREM.md` by a symbolic
> rank-four Cauchy-saddle calculation.  The computations below remain
> useful as an independent regression, but are no longer the logical
> basis for the theorem.

## 0. Status and main formula

Write
\[
c_k(s)=\sum_{d\ge0}b_{k,d}s^{2k-4-d}.
\]
The leading and first-subleading symbols are already proved:
\[
b_{k,d}
=k^d-A_dk^{d-1}+O_d(k^{d-2}),\qquad
A_d=\frac{22d^3+147d^2+161d-258}{36}.
\]

The exact calculations in this note originally suggested the
following formula, now proved in the all-orders theorem:
\[
\boxed{
[k^{d-2}]b_{k,d}=Q_d
=\frac{
286d^6+3546d^5+12721d^4-7812d^3
-86231d^2+40338d+209160
}{5184}
}\tag{1}
\]
for every \(d\ge2\).  Equivalently,
\[
\boxed{
\sum_{d\ge2}Q_dz^d
=\frac{z^2}{72(1-z)^7}
\left(
2389z^6-13818z^5+31221z^4-32952z^3
+14112z^2-1116z+3024
\right).
}\tag{2}
\]

The original finite audit was deliberately split as follows:

1. Formula (1) is an **exact finite certificate**, verified from the
   original finite profiles for every \(2\le d\le22\), with two
   interpolation-external checks at every depth.  Depths
   \(19,\ldots,22\) are holdouts beyond the range used to discover the
   degree-six formula.
2. The new rank-four profile generating functions are verified for all
   losses \(4\le\ell\le34\).  Losses \(31,\ldots,34\) are holdout
   coefficients beyond the range used to discover their numerators.
3. At that stage, the all-\(d\) assertion was conditional on an all-loss
   rank-four resummation.
4. That condition is now discharged by
   `ORDINARY_SECOND_SUBLEADING_SYMBOL_THEOREM.md` and its symbolic
   saddle certificate.  Formula (1) is therefore proved for every
   \(d\ge2\); this file remains named a certificate to preserve the
   provenance of the independent finite computation.

The machine-readable audit is
`SECOND_SUBLEADING_FINITE_CERTIFICATE.json`; it is reproduced by
`verify_ordinary_second_subleading_symbol.py`.

## 1. Rank-four profile symbols

Use the notation of `ORDINARY_SUBLEADING_SYMBOL_THEOREM.md`:
\[
\begin{aligned}
R_{\ell,h}(j)
={}&A_\ell j^\ell+P_{h,\ell}j^{\ell-1}
+Q_{h,\ell}j^{\ell-2}+S_{h,\ell}j^{\ell-3}\\
&+V_{h,\ell}j^{\ell-4}+O_\ell(j^{\ell-5}),
\end{aligned}\tag{3}
\]
and define
\[
V_h(z)=\sum_{\ell\ge4}V_{h,\ell}z^{\ell-4}.
\tag{4}
\]
Put \(w=1-2z\).  The rank-four resummation, originally discovered from
the finite data and now proved in the all-orders theorem, is
\[
V_0(z)=-\frac{z}{155520w^{23/2}}
\left(
\begin{aligned}
&146176z^{11}-663552z^{10}+1220352z^9-774144z^8\\
&-736992z^7+2750976z^6-8160912z^5+13685760z^4\\
&+47385675z^3-112674240z^2+40091760z+17729280
\end{aligned}
\right),\tag{5}
\]
\[
V_1(z)=\frac{z}{155520w^{23/2}}
\left(
\begin{aligned}
&690451712z^{11}-3711086592z^{10}+8894124288z^9\\
&-12380967936z^8+10858590432z^7-6111072000z^6\\
&+2540586384z^5-1519300800z^4+1006618725z^3\\
&-199208160z^2-73347120z+4976640
\end{aligned}
\right),\tag{6}
\]
and
\[
V_2(z)=-\frac{z}{155520w^{23/2}}
\left(
\begin{aligned}
&38115777280z^{11}-189099147264z^{10}
+412563816192z^9\\
&-516716734464z^8+407929881888z^7
-212168180736z^6\\
&+75677948784z^5-19289301120z^4+3340767915z^3\\
&-487969920z^2+184051440z-23950080
\end{aligned}
\right).\tag{7}
\]

### Rank-four resummation lemma still to be closed

Equations (5)--(7) hold as formal power series for all losses
\(\ell\ge4\).

A direct proof has the following finite route.  Start from the exact
profiles
\[
\begin{aligned}
U_{0,j}(s)&=(s)_{\underline j}D(s,s-j,j),\\
U_{1,j}(s)&=(s-2)_{\underline j}D(s,s-2-j,j),\\
U_{2,j}(s)&=(s-4)_{\underline j}D(s,s-4-j,j)
+4(s-4)_{\underline{j-1}}E(s,s-3-j,j-1).
\end{aligned}\tag{8}
\]
Normalize by \(2^jj!/s^{2j}\), retain the coefficient of
\(j^{\ell-4}s^{-\ell}\), and convert each power of the internal summation
index into falling powers.  The finite sum is then eliminated by
\[
\sum_{r=0}^{j}\binom jr2^{j-r}(-1)^r
(r)_{\underline v}=(-1)^v(j)_{\underline v}.
\tag{9}
\]
Summing the remaining coefficient in \(\ell\) must yield (5)--(7).
This is precisely the all-loss algebra that remains to be recorded.
The finite verifier reconstructs the left-hand side of (3) directly and
checks 93 exact coefficients, but it does not replace the last
all-\(\ell\) derivation.

## 2. Determinant reduction through order four

Let \(J\sim\operatorname{Bin}(k,\tfrac12)\), \(x=J/k\), \(u=tx\), and
\(v=t(1-x)\).  Let \(A,P_h,Q_h,S_h\) be the proved profile symbols in the
first-subleading theorem.  Define
\[
\begin{aligned}
G_4(x,t)=t^4\{&
(V_1(u)-V_0(u))A(v)+A(u)(V_1(v)-V_2(v))\\
&+P_1(u)S_1(v)+S_1(u)P_1(v)+Q_1(u)Q_1(v)\\
&-P_0(u)S_2(v)-S_0(u)P_2(v)-Q_0(u)Q_2(v)\}.
\end{aligned}\tag{10}
\]
The lower functions \(G_2,G_3\) are those already defined in the
first-subleading proof.  Symmetry kills the odd determinant term
exactly.  Using
\[
\mathbb E(x-\tfrac12)^2=\frac1{4k},\qquad
\mathbb E(x-\tfrac12)^4=\frac3{16k^2}+O(k^{-3}),
\tag{11}
\]
the next central-binomial symbol is
\[
H_4(t)=G_4(\tfrac12,t)
+\frac18\partial_x^2G_3(\tfrac12,t)
+\frac1{128}\partial_x^4G_2(\tfrac12,t).
\tag{12}
\]
Exact symbolic simplification gives
\[
\boxed{
H_4(t)=\frac{t^5}{36(1-t)^7}
\left(
\begin{aligned}
&2389t^7-14334t^6+34245t^5-40008t^4\\
&+22152t^3-5400t^2+3672t+144
\end{aligned}
\right).
}\tag{13}
\]
In particular, for \(d\ge2\),
\[
[t^{d+4}]H_4(t)
=\frac1{2592}
\left(
\begin{aligned}
&286d^6+3546d^5+12721d^4-4644d^3\\
&-65063d^2+63522d+172008
\end{aligned}
\right).
\tag{14}
\]

Let \(N_L(k)\) be the binomially averaged numerator before division by
\(2k(k-1)\).  Conditional on (5)--(7),
\[
\begin{aligned}
N_L(k)
={}&k^{L-2}[t^L]H_2(t)
+k^{L-3}[t^L]H_3(t)\\
&+k^{L-4}[t^L]H_4(t)+O_L(k^{L-5}).
\end{aligned}\tag{15}
\]
Since
\[
\frac1{2k(k-1)}
=\frac1{2k^2}\left(1+\frac1k+\frac1{k^2}
+O(k^{-3})\right),\tag{16}
\]
putting \(L=d+4\) gives
\[
Q_d
=1+\frac12[t^{d+4}]H_3(t)
+\frac12[t^{d+4}]H_4(t).\tag{17}
\]
Substitution of the already proved \(H_3\) and (14) reduces (17) to
(1), and applying the Euler operator \(z\,d/dz\) to
\(z^2/(1-z)\) proves the rational identity (2).

Thus the only all-\(d\) dependency not already proved or checked as a
rational identity is the rank-four resummation lemma.

## 3. Quantitative root-window information

The first three symbols give the quadratic truncation
\[
b_{k,d}^{(2)}
=k^{d-2}\left(k^2-A_dk+Q_d\right).\tag{18}
\]
Its discriminant is
\[
A_d^2-4Q_d
=\frac{
33d^6+487d^5+2662d^4+7299d^3+6050d^2
-20569d-23766
}{216}.\tag{19}
\]
It is positive for every \(d\ge2\): after writing \(d=y+2\), its
numerator becomes
\[
33y^6+883y^5+9512y^4+53355y^3
+160612y^2+221699y+77976.\tag{20}
\]
Hence the outer zero of the truncation is
\[
R_2(d)=\frac{A_d+\sqrt{A_d^2-4Q_d}}2.\tag{21}
\]
The asymptotic constants are
\[
\frac{R_2(d)}{d^3}
\longrightarrow
\frac{11}{36}+\frac{\sqrt{22}}{24}
=0.5009895455\ldots,\tag{22}
\]
whereas the first-subleading truncation has outer zero
\[
\frac{A_d}{d^3}\longrightarrow\frac{11}{18}
=0.6111111111\ldots.\tag{23}
\]
Equivalently,
\[
\frac{R_2(d)}{A_d}
\longrightarrow
\frac12+\frac{3\sqrt{22}}{44}
=0.8198010745\ldots.\tag{24}
\]
Thus the second symbol improves the predicted outer \(d^3\)-window
constant by \(18.02\%\).

This is currently a statement about the three-term truncation, not a
rigorous zero bound for the full \(b_{k,d}\).  At scale \(k=Cd^3\), its
limiting normalized safety margin is
\[
1-\frac{11}{18C}+\frac{143}{2592C^2}.\tag{25}
\]
For example, at \(C=0.55\) the margin is approximately \(0.07127\).
Therefore a publishable root-window theorem can be closed by proving
that the normalized sum of symbols of order three and lower is
uniformly smaller than this margin for \(k\ge0.55d^3\).  Without such a
tail bound, replacing the existing root window by \(0.55d^3\) would be
an unsupported extrapolation.

## 4. Reproducible verification

Run
```bash
python3 verify_ordinary_second_subleading_symbol.py \
  --maximum-loss 34 --maximum-depth 22
pytest -q test_verify_ordinary_second_subleading_symbol.py
```

The first command verifies:

- 93 exact rank-four profile coefficients;
- the rational identity (13);
- the rational generating-function identity (2);
- 21 exact ordinary-polynomial second symbols, each with two unused
  interpolation points;
- positivity of the shifted discriminant (20).

The focused test suite contains three tests and uses only exact integer,
rational, and symbolic arithmetic.
