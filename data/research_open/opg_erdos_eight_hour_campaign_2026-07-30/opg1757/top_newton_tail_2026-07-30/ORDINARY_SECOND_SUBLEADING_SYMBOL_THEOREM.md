# OPG-1757: the all-orders second subleading ordinary-power symbol

Date: 2026-07-30

## 0. Result

Write
\[
c_k(s)=\sum_{d\ge0}b_{k,d}s^{2k-4-d}.
\]
The leading and first subleading symbols are known for every fixed
depth.  The next symbol also has a closed form.

### Theorem 1

For every \(d\ge2\),
\[
\boxed{
\begin{aligned}
b_{k,d}
={}&k^d
-\frac{
22d^3+147d^2+161d-258
}{36}\,k^{d-1}\\
&+\frac{
286d^6+3546d^5+12721d^4-7812d^3
-86231d^2+40338d+209160
}{5184}\,k^{d-2}\\
&+O_d(k^{d-3}).
\end{aligned}
}                                                     \tag{1}
\]

Equivalently, if \(C_d=[k^{d-2}]b_{k,d}\), then
\[
\boxed{
\sum_{d\ge2}C_dz^d
=
\frac{
z^2(2389z^6-13818z^5+31221z^4-32952z^3
+14112z^2-1116z+3024)
}{72(1-z)^7}.
}                                                     \tag{2}
\]

The degree-six scale in (1) is the square of the cubic first
correction, as required by a prospective \(k\asymp d^3\) transition.
The theorem does not by itself control all lower symbols uniformly in
\(d\).

## 1. Fourth profile symbol

Use the exact profiles and normalization in
`ORDINARY_SUBLEADING_SYMBOL_THEOREM.md`.  Thus
\[
\Phi_h(s,x)
=\frac{2^jj!}{s^{2j}}U_{h,j}(s),\qquad j=xs.
\]
The parameterized Cauchy-saddle expansion one order further gives
\[
\boxed{
\Phi_h(s,x)
=A(x)+\frac{P_h(x)}s+\frac{Q_h(x)}{s^2}
+\frac{S_h(x)}{s^3}+\frac{T_h(x)}{s^4}
+O_{\rm formal}(s^{-5}).
}                                                     \tag{3}
\]
Put \(w=1-2x\).  The fourth symbols are
\[
T_h(x)=\frac{N_h(x)}{155520\,w^{23/2}},             \tag{4}
\]
where
\[
\begin{aligned}
N_0(x)=-x(&146176x^{11}-663552x^{10}+1220352x^9
-774144x^8\\
&-736992x^7+2750976x^6-8160912x^5
+13685760x^4\\
&+47385675x^3-112674240x^2+40091760x
+17729280),
\end{aligned}                                      \tag{5}
\]
\[
\begin{aligned}
N_1(x)=x(&690451712x^{11}-3711086592x^{10}
+8894124288x^9\\
&-12380967936x^8+10858590432x^7
-6111072000x^6\\
&+2540586384x^5-1519300800x^4
+1006618725x^3\\
&-199208160x^2-73347120x+4976640),
\end{aligned}                                      \tag{6}
\]
and
\[
\begin{aligned}
N_2(x)=-x(&38115777280x^{11}-189099147264x^{10}
+412563816192x^9\\
&-516716734464x^8+407929881888x^7
-212168180736x^6\\
&+75677948784x^5-19289301120x^4
+3340767915x^3\\
&-487969920x^2+184051440x-23950080).
\end{aligned}                                      \tag{7}
\]

### Lemma 2 (all-orders fourth-profile extraction)

Equations (3)--(7) hold as identities of formal power series in \(x\);
in particular, they determine the fourth subdegree at every loss, not
only at finitely many losses.

### Proof

The exact Cauchy integrals (11a)--(11b) of
`ORDINARY_SUBLEADING_SYMBOL_THEOREM.md` have phase
\[
\phi_x(y)
=y+(1-x)\log(1-y/2)-x\log y
\]
and contributing saddle \(y_0=2x\) for \(0<x<1/2\).
The proof there defines:

- the phase-exponential polynomials \(E_n\);
- the Gaussian moment functional \({\cal M}\);
- the saddle coefficients \(B_r(g)\);
- the Bernoulli--Gamma corrections \(\Gamma_r({\cal A})\); and
- their convolution \(C_r(g,{\cal A})\).

For rank four, the same finite recurrences require only
\[
E_0,\ldots,E_8,\qquad
\phi_x^{(2)}(2x),\ldots,\phi_x^{(10)}(2x),
\qquad
\Gamma_0,\ldots,\Gamma_4.                          \tag{8}
\]
No new limiting interchange is needed.  They give
\[
\Phi_a^{\rm main}(s,x)
=\sqrt{1-2x}\sum_{r=0}^{4}
C_r(g_a,{\cal A}_a)s^{-r}+O(s^{-5})               \tag{9}
\]
for \(a=0,2,4\), and
\[
\Phi^{\rm ex}(s,x)
=\frac{8x}{s\sqrt{1-2x}}
\sum_{r=0}^{3}C_r(g_*,{\cal A}_*)s^{-r}
+O(s^{-5}).                                       \tag{10}
\]
Combining
\[
\Phi_0=\Phi_0^{\rm main},\qquad
\Phi_1=\Phi_2^{\rm main},\qquad
\Phi_2=\Phi_4^{\rm main}+\Phi^{\rm ex}
\]
and simplifying the rank-four terms gives (4)--(7).

The companion
`verify_ordinary_second_subleading_all_orders.py` evaluates all
recurrences in (8) symbolically and proves the three rational-function
identities (4)--(7).  It performs no interpolation in the loss
variable.  As in the preceding theorem, the calculation first holds
for rational \(0<x<1/2\), and analytic continuation to a neighbourhood
of \(x=0\) identifies every Taylor coefficient. \(\square\)

## 2. The fourth determinant kernel

Introduce a loss marker \(t\), set \(u=tx\), \(v=t(1-x)\), and write
\[
\begin{aligned}
{\cal F}_h(x;t,k)
={}&A(tx)+\frac{t}{k}P_h(tx)
+\frac{t^2}{k^2}Q_h(tx)
+\frac{t^3}{k^3}S_h(tx)\\
&+\frac{t^4}{k^4}T_h(tx)+O_{\rm formal}(k^{-5}).
\end{aligned}                                      \tag{11}
\]
The coefficient of \(k^{-4}\) in
\({\cal F}_1(x){\cal F}_1(1-x)
-{\cal F}_0(x){\cal F}_2(1-x)\) is
\[
\begin{aligned}
G_4(x,t)=t^4\{&
(T_1(u)-T_0(u))A(v)
+A(u)(T_1(v)-T_2(v))\\
&+P_1(u)S_1(v)+S_1(u)P_1(v)+Q_1(u)Q_1(v)\\
&-P_0(u)S_2(v)-S_0(u)P_2(v)-Q_0(u)Q_2(v)
\}.
\end{aligned}                                      \tag{12}
\]

Let \(J\sim{\rm Bin}(k,\tfrac12)\) and
\(\delta=J/k-\tfrac12\).  The exact moments needed through order
\(k^{-4}\) are
\[
\mathbb E\delta^2=\frac1{4k},\qquad
\mathbb E\delta^3=0,\qquad
\mathbb E\delta^4=\frac3{16k^2}-\frac1{8k^3}.
\tag{13}
\]
The order-\(k^{-1}\) kernel remains exactly antisymmetric and has zero
binomial expectation.  Taylor expansion of the remaining kernels
therefore gives
\[
\boxed{
H_4(t)
=G_4(\tfrac12,t)
+\frac18\partial_x^2G_3(\tfrac12,t)
+\frac1{128}\partial_x^4G_2(\tfrac12,t).
}                                                     \tag{14}
\]
The factor \(1/128\) is
\((1/4!)\cdot(3/16)\).  Terms involving the sixth central moment start
at order \(k^{-5}\) after the leading \(k^{-2}G_2\) factor.

Substitution and exact simplification yield
\[
\boxed{
H_4(t)
=
\frac{t^5(
2389t^7-14334t^6+34245t^5-40008t^4
+22152t^3-5400t^2+3672t+144
)}
{36(1-t)^7}.
}                                                     \tag{15}
\]

## 3. Coefficient extraction

Let \(N_L(k)\) be the binomially averaged numerator before division by
\(2k(k-1)\).  Coefficientwise in the fixed loss \(L\),
\[
\begin{aligned}
N_L(k)
={}&k^{L-2}[t^L]H_2(t)
+k^{L-3}[t^L]H_3(t)\\
&+k^{L-4}[t^L]H_4(t)
+O_L(k^{L-5}).                                     \tag{16}
\end{aligned}
\]
Since
\[
\frac1{2k(k-1)}
=\frac1{2k^2}
\left(1+\frac1k+\frac1{k^2}+O(k^{-3})\right),
\]
putting \(L=d+4\) gives
\[
\boxed{
[k^{d-2}]b_{k,d}
=\frac12[t^{d+4}]\bigl(H_2+H_3+H_4\bigr).
}                                                     \tag{17}
\]
Using the earlier
\[
H_2(t)=\frac{2t^4}{1-t},
\qquad
H_3(t)=
-\frac{t^4(43t^4-129t^3+108t^2-6t+6)}
{3(1-t)^4},
\]
equations (15)--(17) simplify to
\[
\frac{H_2+H_3+H_4}{2t^4}
=
\frac{
t^2(2389t^6-13818t^5+31221t^4-32952t^3
+14112t^2-1116t+3024)
}{72(1-t)^7}.                                      \tag{18}
\]
This proves (2).

Finally, apply the Euler operator
\(\mathcal D=t\,d/dt\) to
\[
\sum_{d\ge2}t^d=\frac{t^2}{1-t}.
\]
The right side of (18) is exactly
\[
\frac1{5184}
\left(
286\mathcal D^6+3546\mathcal D^5
+12721\mathcal D^4-7812\mathcal D^3
-86231\mathcal D^2+40338\mathcal D+209160
\right)
\frac{t^2}{1-t}.
\]
Coefficient extraction proves the second correction in (1).
\(\square\)

## 4. Verification and scope

Run:

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/opg1757/top_newton_tail_2026-07-30
python3 verify_ordinary_second_subleading_all_orders.py
pytest -q test_verify_ordinary_second_subleading_all_orders.py \
  test_verify_ordinary_second_subleading_symbol.py
```

The all-orders verifier checks:

1. three rank-four profile identities in symbolic \(x\);
2. the exact identity (15);
3. the all-depth generating-function identity (18); and
4. the Euler-operator coefficient polynomial in (1).

The older finite certificate remains an independent regression:
it reconstructs exact profiles through loss \(34\) and exact ordinary
coefficients through depth \(22\).  It is no longer the logical basis
for Theorem 1.

The theorem supplies two complete lower symbols.  A uniform bound on
all remaining symbols is still required to prove positivity throughout
the conjectural top window \(d\ll k^{1/3}\).
