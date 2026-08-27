# M10 round 3: the high-support weighted joint correlation

Date: 2026-08-27

Status: work in progress.  Exact identities and proved partial estimates are
labelled as such.  No maximum-gap theorem and no improvement to Erdős 451 is
claimed.

## 1. The exact fibre and a carry-forgetting surrogate

Keep the notation of `audit/m05_special_zonotope_linear_gate.md`.  Choose a
fixed even integer `L>=2` and put

\[
 u_i(n)=\operatorname{sinc}\left({2\pi b n\over Lp_i}\right)^L,
 \qquad
 U_i(r)=\sum_{m\in\mathbb Z}u_i(r+mp_i).                     \tag{1}
\]

The evenness makes `u_i,U_i` nonnegative.  Let

\[
 \epsilon=(-1)^{q-1},\qquad
 c_i\equiv\epsilon F'(d_i)^{-1}\pmod {p_i}.                  \tag{2}
\]

Put `P=product_i p_i` and, for `z in Z^q`, put

\[
 A(z)=\sum_i z_i{P\over p_i},\qquad
 w(z)=\prod_i u_i(z_i),\qquad
 W(A)=\sum_{A(z)=A}w(z).                                    \tag{3}
\]

Let `W_>(A)` denote the same fibre restricted to
`sigma(z)>r_epsilon`.  In the notation of the round-2 audit, the exact
unresolved high-support residual is

\[
 \mathcal H_>=\sum_A\Phi_h(A)W_>(A),\qquad
 \Phi_h(A)=\left|\operatorname{sinc}
              \left({2\pi hA\over LP}\right)\right|^L.     \tag{4}
\]

Thus the weakest precise sufficient statement is
`mathcal H_><1-o(1)`, with the strict margin left after Lemma 9.1.  This is
the target (43), not a new lemma, and is not assumed below.

The local periodizations forget one integer carry.  Indeed the congruence
in (2), together with the cofactor identity, gives the exact identity

\[
 \prod_iU_i(c_ix)=\sum_{\ell\in\mathbb Z}W(x+\ell P)          \tag{5}
\]

for every integer `x`.  To see this, expanding the left side sums over all
`z_i congruent c_i x (mod p_i)`; these congruences are equivalent to
`A(z) congruent x (mod P)`.  For a fixed numerator `A`, if `r_i` is the
centered representative of `c_iA (mod p_i)` and
`z_i=r_i+p_it_i`, the omitted exact carry is

\[
 \sum_i t_i={A-\sum_i r_iP/p_i\over P}.                     \tag{6}
\]

Consequently independent local carry summation is not equivalent to (4):
it merges every numerator `A+ell P`, while `Phi_h(A)` is not periodic.
Moreover each `U_i` is a periodization with small positive tails, so
positivity of its product does not certify that the original compact local
offset lies in the box.

There is nevertheless one valid **one-sided** use of the carry-forgetting
product.  Specialize from now through (7e) to `L=2`, take an integer
`1<=h<P/2`, and define on `Z/PZ`

\[
 \Omega(r)=\sum_{\ell\in\mathbb Z}\Phi_h(r+\ell P),\qquad
 V(r)=\prod_iU_i(c_ir),\qquad
 S=\sum_{r\bmod P}\Omega(r)V(r).                            \tag{7a}
\]

All summands are nonnegative, and (5) gives the rigorous comparison

\[
 E:=\sum_A\Phi_h(A)W(A)\le S.                              \tag{7b}
\]

The zero vector contributes one to `E` and contributes `Omega(0)` to `S`.
After removing exactly that one cross term, positivity still gives

\[
                    E-1\le S-\Omega(0).                    \tag{7c}
\]

Since `Phi_h(A)=sinc(pi hA/P)^2` and `h` is integral,

\[
             \Omega(0)=\sum_{\ell\in\mathbb Z}
                         \operatorname{sinc}(\pi h\ell)^2=1. \tag{7d}
\]

Therefore `S<2` is a genuine sufficient condition for the box-spline
criterion.  It is stronger than the exact fibre target, not equivalent to
it.

The normalized Fourier transform of `Omega` is obtained by Poisson
summation.  For the centered representative `|j|_P<P/2`,

\[
 \widehat\Omega(j)={1\over P}\sum_{r\bmod P}\Omega(r)e_P(-jr)
   ={1\over h}\left(1-{|j|_P\over h}\right)_+.             \tag{7e}
\]

There is only one Poisson alias because `h<P/2`.  Combining (7e) with the
local expansion below will give the exact, phase-preserving formula (14a).

For later method auditing only, define for a nonnegative finitely supported
integer weight `omega`

\[
 \mathcal C_y(\omega)=\sum_{t\in\mathbb Z}\omega(t)
                         \prod_iU_i(c_i(y+t)).                \tag{7}
\]

This is a carry-forgetting surrogate correlation.  Its exact Fourier
algebra can expose method losses.  An arbitrary choice of `omega` is not a
closure theorem; the special periodized Fejer weight in (7a)--(7e) is the
proved sufficient upper bridge.

## 2. Exact compact local Fourier transform

Use the continuous Fourier convention

\[
 \widehat f(\xi)=\int_{\mathbb R}f(x)e^{-2\pi i x\xi}\,dx.
\]

Let `eta_i` be the uniform probability density on
`[-b/(Lp_i),b/(Lp_i)]`.  Then `widehat eta_i(n)` is the sinc in (1), and

\[
             \widehat u_i=\eta_i^{*L}=:B_i,
 \qquad \operatorname {supp}B_i\subseteq[-b/p_i,b/p_i].     \tag{8}
\]

Poisson summation gives the normalized discrete transform

\[
 \begin{split}
 \widehat U_i(a)
   &:={1\over p_i}\sum_{r\bmod p_i}U_i(r)e_{p_i}(-ar)\\
   &={1\over p_i}\sum_{n\in\mathbb Z}u_i(n)e_{p_i}(-an)
     ={1\over p_i}\sum_{m\in\mathbb Z}B_i(m+a/p_i).         \tag{9}
 \end{split}
\]

Because `b<p_i/2`, at most one term occurs in the last sum.  Therefore the
following exact facts hold:

\[
 \widehat U_i(a)=
 \begin{cases}
   \beta_i(a):=p_i^{-1}B_i(a/p_i)\ge0,
      &|\langle a\rangle_{p_i}|\le b,\\
   0,&|\langle a\rangle_{p_i}|>b.
 \end{cases}                                                \tag{10}
\]

In particular

\[
              U_i(r)=\sum_{|a|\le b}\beta_i(a)e_{p_i}(ar).  \tag{11}
\]

The coefficient at zero satisfies

\[
          {c_L\over b}\le\beta_i(0)\le{C_L\over b},
 \qquad U_i(0)=1+O_L(b^{-L}),                               \tag{12}
\]

by scaling the fixed integral of `sinc(2 pi x/L)^L`.

## 3. Exact local untwisting inside the surrogate

Insert (11) into (7).  A local frequency `a_i in [-b,b]` creates the character
`a_i c_i mod p_i`.  Let `H(a) mod P` be the corresponding global CRT
frequency.  Reduction modulo `p_i`, followed by (1) of the round-2 phase
note, gives

\[
 \begin{split}
 H(a)&\equiv (a_ic_i){P\over p_i}\pmod {p_i}\\
     &\equiv a_i\,{\epsilon\over F'(d_i)}
                 \epsilon F'(d_i)\equiv a_i\pmod {p_i}.     \tag{13}
 \end{split}
\]

Thus `H(a)` is exactly the canonical CRT lift of the **small residues
`a_i` themselves**.  The inverse-derivative factors cancel from the local
residue labels and coefficient weights, but not from the centered size of
the global CRT lift.  The exact expansion is

\[
 \mathcal C_y(\omega)=
 \sum_{|a_i|\le b}\left(\prod_i\beta_i(a_i)\right)
 e_P(yH(a))\widehat\omega(-H(a)/P).                          \tag{14}
\]

Equation (14) is a proof-level reparameterization of the surrogate.  It
untwists the local coefficient weights and makes the residues of `H(a)`
equal to the small integers `a_i`.  It does **not** remove the joint phase:

\[
 {H(a)\over P}\equiv\sum_i{a_ic_i\over p_i}\pmod1,
 \qquad c_i=\left({P\over p_i}\right)^{-1}
             =\epsilon F'(d_i)^{-1}\pmod {p_i}.             \tag{14b}
\]

Thus marginal information about one inverse derivative does not control
the centered small-lift event, while the joint inverse-derivative
correlation remains exactly the core of that event.

For the special `L=2` Fejer bridge (7a), Parseval, (7e), and the injectivity
of the small-residue CRT box give the exact nonnegative formula

\[
 S={P\over h}
   \sum_{\substack{|a_i|\le b\\ |H(a)|_P<h}}
      \left(1-{|H(a)|_P\over h}\right)
      \prod_i\beta_i(a_i).                                  \tag{14a}
\]

Thus (14a) `<2` is a proved sufficient closure condition by (7c)--(7d).
The normalization is important: (7e) contributes `1/h`, while summing over
`P` residues contributes `P`.

For `L=2` the coefficient is completely explicit.  The convolution of two
uniform densities is triangular, and (9)--(10) give

\[
 \beta_i(a)={1\over b}\left(1-{|a|\over b}\right)_+
              \qquad (a\in\mathbb Z).                       \tag{14c}
\]

Consequently the sufficient bridge is the exact density-scale inequality

\[
 {P\over hb^q}
 \sum_{\substack{|a_i|<b\\ |H(a)|_P<h}}
       \left(1-{|H(a)|_P\over h}\right)
       \prod_i\left(1-{|a_i|\over b}\right)<2.             \tag{14d}
\]

The zero global Fourier frequency in (14d) contributes `P/(hb^q)`.  (It is
not the zero coefficient vector in the real-fibre decomposition; that
vector contributed `Omega(0)=1` in (7c).)  Thus, after choosing `h` so that
the spectral principal term is below one by a fixed margin, (14d) asks for
a weighted nonprincipal small-lift count of the remaining fixed margin.
This is the weakest concrete lemma isolated in this round that actually
closes the single-block box-spline criterion; it remains open.

Formula (14) for arbitrary `omega` does not itself identify (4), because
the missing carry (6), the nonperiodic weight `Phi_h`, and the high-support
restriction have disappeared.  Formula (14a) is different: positivity and
the exact periodized Fejer weight make it a valid **upper** bridge.  It is
still stronger than (4); its remaining object is precisely the weighted
joint small-lift count (14a), equivalently the correlated phase (14b).

## 4. A proved coefficient-aware subset moment

There is an exact partial averaging theorem for the carry-forgetting
surrogate, but it loses the unobserved coordinates.  Normalize

\[
                  \phi_i(x)={U_i(c_ix)\over U_i(0)}.          \tag{15}
\]

By (10)--(11), `0<=phi_i<=1`, and its mean on `Z/p_i` is

\[
              \mu_i={\beta_i(0)\over U_i(0)}\asymp_L b^{-1}.
                                                                    \tag{16}
\]

> **Lemma 4.1 (weighted subset-period bound).**  For every subset `S` of
> size `s`, every integer interval `J` of length `T`, and
> `P_S=product_(i in S)p_i`,
> \[
> {1\over T}\sum_{x\in J}\prod_{i\in S}\phi_i(x)
>       \le \left({C_L\over b}\right)^s+{P_S\over T}
>       \le \left({C_L\over b}\right)^s+{(2k)^s\over T}.    \tag{17}
> \]

Proof.  Multiplication by each `c_i` is a permutation modulo `p_i`.  CRT
therefore makes the mean over one full period `P_S` exactly
`product_(i in S)mu_i`.  The product in (17) lies in `[0,1]`; discard at
most one incomplete period and use (16).

Since the omitted factors are also at most one, (17) upper-bounds the full
product.  Optimizing the two terms gives only

\[
 s\simeq {\log T\over\log(2kb/C_L)},qquad
 {1\over T}\sum_{x\in J}\prod_{i=1}^q\phi_i(x)
       \ll \exp\left(-{\log b\over\log(2kb/C_L)}\log T\right).
                                                                    \tag{18}
\]

If one applies this surrogate bound on a numerator shell of length
`T=P/h`, with `log h=o(log P)` and `log b asymp log k`, it uses only about
half the coordinates and produces `b^{-(1/2+o(1))q}`.  Here `P/h` is the
scale of an `A`-shell in (4); it is **not** the support length of the
original time parameter `h` and is not a substitution into (7).  The
desired coefficient scale is `b^{-q}` up to an `exp(O(q))` factor.  Thus
the explicit surrogate method

```text
retain the exact coefficient weights on a subset, average that subset over
complete periods, and discard all complementary weights using positivity
```

repays `exp((1/2+o(1))q log b)`, which is `exp(Theta(k))` in a macroscopic
block.  This is only a no-go for carrying (17) into the exact residual via
positivity after independent carry summation.  It is not an obstruction to
the exact signed/full-fibre correlation (4).

### 4.2 The actual Fejer bridge has interval length `h`

For (14a), put

\[
        g_i(x)=\beta_i(\langle x\rangle_{p_i}).              \tag{18a}
\]

Then `0<=g_i<=C_L/b`, and its sum over a full `p_i`-period is
`U_i(0)=1+O_L(b^{-L})`.  CRT therefore gives, for every subset `S`, every
interval `J` of length `T`, and `P_S=product_(i in S)p_i`,

\[
 \sum_{x\in J}\prod_{i\in S}g_i(x)
       \le \exp(D_L|S|/b^L)
                    \left({T\over P_S}+1\right).            \tag{18b}
\]

This is stronger than bounding the incomplete period by its length: all
terms are nonnegative, so an incomplete period has at most the mass of one
complete period.  Discarding the complementary coefficient weights by
their suprema and using the centered interval `|x|<h` in (14a), whose
length is `T<2h`, proves

\[
 S\le 2e^{D_Lq/b^L}C_L^{q-|S|}\left\{
       {P\over P_Sb^{q-|S|}}+{P\over hb^{q-|S|}}\right\}.   \tag{18c}
\]

Thus the interval on the coefficient side of the actual sufficient bridge
has length `h`.  In a macroscopic block `b asymp k`,
`P_S=k^{s+o(s)}`.  The first term of (18c) can be bounded by an absolute
constant only when `q-s=O_L(1)`; with such `s`, the second term requires

\[
                    h\ge P/b^{O_L(1)}=exp(\Theta(k)).       \tag{18d}
\]

This is outside the `exp(o(k))` budget.  Conversely an affordable
`log h=O(q)` permits only `s=O(q/log k)`, leaving the first term on the
`exp(Theta(q))` scale.  Hence complete-period averaging on a coordinate
subset plus supremum disposal of its complement cannot prove `S<2` on the
top macroscopic block.  This is a rigorous no-go for that positive
subset-period ledger, not for signed estimates of (14a).

There is no contradiction with the `P/h` scale in (18).  The latter is the
dual real-space concentration scale of the periodized Fejer weight.  In
fact the partial-fraction identity for the cosecant gives, exactly,

\[
 \Omega(r)=
 \begin{cases}
  1,&r=0,\\[2mm]
  \displaystyle{\sin^2(\pi hr/P)\over
                    h^2\sin^2(\pi r/P)},&r\ne0,
 \end{cases}                                                 \tag{18e}
\]

and hence, for centered `|r|_P<=P/2`,

\[
             \Omega(r)\le
       C\min\left\{1,{P^2\over h^2(1+|r|_P)^2}\right\}.    \tag{18f}
\]

Split the residues into the central interval of length `O(P/h)` and the
dyadic shells
`2^{j-1}P/h<|r|_P<=2^jP/h`.  On the `j`-th shell, (18f) is `O(4^{-j})`
and the shell length is `O(2^jP/h)`.  Applying Lemma 4.1 on each of the at
most two component intervals and summing the geometric series yields the
rigorous transfer

\[
 {S\over\prod_iU_i(0)}
   =\sum_{r\bmod P}\Omega(r)\prod_i\phi_i(r)
   \le C_L\left\{ {P\over h}\left({C_L\over b}\right)^s
                         +P_S\right\}.                      \tag{18g}
\]

At the density-scale choice `h=C_0^qP/b^q` (harmless fixed-factor changes
from `d_i/b` being absorbed in `C_0`), the right side of (18g) is

\[
       C_L\left\{C_0^{-q}C_L^sb^{q-s}+k^{s+o(s)}\right\}.   \tag{18h}
\]

Balancing the displayed terms uses `s=(1/2+o(1))q` in a macroscopic block
and leaves `exp((1/2+o(1))q log k)=exp(Theta(k))`.  This supplies the
previously missing Fejer-tail transfer: the half-coordinate loss in (18)
really is a no-go for applying Lemma 4.1 to the sufficient majorant `S`.
It does not say that the exact fibre sum `E` is comparably large.

## 5. Fixed-order smooth endpoint still loses a linear exponent

The single incomplete period in (14) can be smoothed.  Let the time law be
the `L`-fold convolution of uniform integer intervals of length `T/L`, so
its total support is `O(T)`.  Its distribution modulo a period `P_S` has
nonprincipal Fourier mass at most

\[
                    C_L\left({LP_S\over T}\right)^L          \tag{19}
\]

when `LP_S<T`; this follows by summing the `L`-th powers of the geometric
sum bound `min(1,LP_S/(T|a|))`.  Total variation and (16) then give

\[
 \mathbb E\prod_{i=1}^q\phi_i(x)
 \le\left({C_L\over b}\right)^s
       +C_L\left({L(2k)^s\over T}\right)^L.                 \tag{20}
\]

Balancing the two exponents yields

\[
        s={L\log T+O_L(1)\over \log b+L\log(2k)}.            \tag{21}
\]

For a macroscopic block this is `(L/(L+1)+o(1))q`.  The missing fraction
`1/(L+1)` costs

\[
                   \exp\left((1+o(1)){q\log b\over L+1}\right).
                                                                    \tag{22}
\]

For every fixed `L`, (22) is `exp(Theta(k))`.  Letting `L` grow is not
covered by Lemma 9.1 or by the fixed-`L` constants in (10), (12), and (19).
Therefore fixed-order smooth completion plus positivity does not close
(4).  Since the Fejer construction gives a sufficient majorant, there is
no need to restore the exact carry if one can prove `S<2`; the point is that
fixed-order smoothing and subset disposal do not prove that bound.  The
exact fibre sum can of course be much smaller than this majorant.

Growing `L` also fails inside the same periodized bridge for a simpler
reason.  Let `L>=2` be even.  If `X_1,...,X_L` are uniform on
`[-1/2,1/2]`, Fourier inversion gives their sum-density at zero as
`integral sinc(pi xi)^L dxi`.  On `|xi|<=c/sqrt(L)` the integrand is at
least an absolute positive constant, so scaling the local uniforms in
(8) proves

\[
                         \beta_i(0)\ge {c\sqrt L\over b}.    \tag{22a}
\]

For general `L`, write
`Q_L(0)=sum_A Phi_(h,L)(A)`.  On `|A|<=cP/h` the sinc argument is
`O(1/L)` and its `L`-th power is bounded below by an absolute constant.
Hence `Q_L(0)>=cP/h` whenever `h<P/2`.  The principal `a=0` term of the
periodized bridge is therefore

\[
 S_0=Q_L(0)\prod_i\beta_i(0)
   \ge {cP\over h}\prod_i\beta_i(0)
   \ge k^{-B}\left({c\sqrt L\over C}\right)^q
                       \prod_i{d_i\over b},                 \tag{22b}
\]

at `h=k^BC^qP/product_i d_i`.  In the dyadic block `d_i/b` is bounded
below by an absolute constant larger than one.  For fixed `C`, macroscopic
`q` with `q/log k` tending to infinity, and even `L` tending to infinity,
the right side of (22b) eventually exceeds two.  Hence unbounded smoothing
order cannot rescue this majorant with a fixed per-prime constant: its
principal term already violates the sufficient target.  This says nothing
negative about the smaller exact fibre sum.

## 6. Centered-moment expansion: exact carry obstruction

There is a second tempting use of the dyadic structure.  Put

\[
                  K=2k+3\Delta,\qquad y_i=2d_i-3\Delta.
\]

Then `2p_i=K+y_i`, `|y_i|<=Delta`, and

\[
              \rho={\Delta\over K}\le {1\over5}.             \tag{23}
\]

For `M_t=sum_i z_i y_i^t` and `Z=||z||_1`, the reciprocal phase has the
absolutely convergent exact expansion

\[
 \alpha(z)=\sum_i{z_i\over p_i}
    ={2\over K}\sum_{t\ge0}{(-1)^tM_t\over K^t}.             \tag{24}
\]

The tail after `T` moments satisfies

\[
 |R_T|\le {2Z\over K}{\rho^T\over1-\rho}.                    \tag{25}
\]

This rapid analytic decay does **not** force exact moment cancellation.
Indeed the truncated numerator

\[
             Q_T=\sum_{t=0}^{T-1}(-1)^tM_tK^{T-1-t}
                   \in\mathbb Z                              \tag{26}
\]

obeys, whenever `|alpha(z)|<=eta`, only

\[
 |Q_T|\le {\eta K^T\over2}
              +{Z\Delta^T\over K(1-\rho)}.                  \tag{27}
\]

The second term in (27) grows with `T` once `Delta>=2`.  Choosing `T` large
enough that the analytic tail (25) is below `eta` therefore makes the
integer uncertainty in (27) larger, not smaller.  The reason is exact:
clearing the denominator multiplies the geometric tail by `K^T`, changing
`rho^T` back into `Delta^T`.

There is also no free base-`K` digit argument.  Although `M_0` can be below
`K`, already

\[
                         |M_1|\le Z\Delta.                    \tag{28}
\]

is much larger than `K` at the natural high-support coefficient budget.
Carries between adjacent moments are therefore unavoidable.  Equations
(23)--(28) rigorously kill only the proposed implication

```text
small reciprocal phase + geometric centered expansion, with no further
coefficient arithmetic, forces many exact zero moments.
```

They do not rule out a new carry-sensitive height theorem.  Such a theorem
would have to use the simultaneous integer-node structure of all `M_t`, not
the ratio `rho<=1/5` alone.  The guarded coefficient searches from round 2,
whose minimizing vectors have first nonzero moment one, are consistent with
this obstruction but are not used in its proof.

## 7. Exact fibre moments and the diagonal obstruction

Higher Holder moments can be written without losing the carry.  For an
integer `s>=2`, put

\[
 M_s^>=\sum_AW_>(A)^s,\qquad M_s=\sum_AW(A)^s.              \tag{29}
\]

For `t=(t_2,...,t_s) in Z^(s-1)`, define the local `s`-fold correlation

\[
 K_{i,s}(t)=\sum_{n\in\mathbb Z}u_i(n)
                  \prod_{\nu=2}^su_i(n+p_it_\nu).           \tag{30}
\]

> **Lemma 7.1 (exact carry moment).**  One has
> \[
> M_s=\sum_{\substack{t^{(2)},\ldots,t^{(s)}\in\mathbb Z^q\\
>                     \sum_i t_i^{(\nu)}=0\ (2\le\nu\le s)}}
>                   \prod_{i=1}^qK_{i,s}
>                   (t_i^{(2)},\ldots,t_i^{(s)}).            \tag{31}
> \]

Proof.  Expand `W(A)^s` and sum over `A`.  Equality of the `s` numerators
imposes

\[
 \sum_i(z_i^{(\nu)}-z_i^{(1)}){P\over p_i}=0
                       \qquad(2\le\nu\le s).                \tag{32}
\]

Reducing the `nu`-th equation modulo `p_i` shows
`p_i divides z_i^(nu)-z_i^(1)`.  Write the difference as
`p_it_i^(nu)` and divide (32) by `P`.  This gives precisely the zero-sum
carry conditions in (31), and the remaining base-coordinate sums are
(30).

The local correlations have an exact unconstrained total:

\[
 \sum_{t\in\mathbb Z^{s-1}}K_{i,s}(t)
   =\sum_{n\in\mathbb Z}u_i(n)U_i(n)^{s-1}.                 \tag{33}
\]

For `L=2`, the sinc-square tail gives uniformly in the residue `n mod p_i`

\[
 U_i(n)\le1+{C\over b^2},\qquad
 \sum_nu_i(n)\le {Cp_i\over b}.                            \tag{34}
\]

Dropping the zero-sum conditions in (31), which is legitimate because all
terms are nonnegative, therefore proves

\[
              M_s\le {C^qP\over b^q}
                         \exp\left({Csq\over b^2}\right).   \tag{35}
\]

Combining (35) with Holder already quantifies the fixed-order ledger:

\[
 \mathcal H_>\le C_s^q
       \left({P\over h}\right)^{1-1/s}
       \left({P\over b^q}\right)^{1/s}
       \exp\left({Cq\over b^2}\right).                     \tag{35a}
\]

In a macroscopic block `b=k^{1+o(1)}` and at the density-scale choice
`h=P b^{-q}exp(O(q))`, this is

\[
             \mathcal H_>\le P^{1-1/s}\exp(O_s(q)).        \tag{35b}
\]

For each fixed `s>=2`, the best exponent in this family is `s=2`, which
still leaves `P^(1/2)exp(O(q))=exp(Theta(k))`.  Thus no fixed moment order
improves the exponent class of this separated positive ledger.

This upper bound is close to the unavoidable diagonal scale, not to an
independent-density `s`-th moment.  Indeed let
`I_i={1,...,floor(p_i/(4b))}`.  Since `p_i/b>=4`,
`|I_i|>=p_i/(8b)`; and for `n in I_i`,

\[
 u_i(n)=\operatorname{sinc}(\pi bn/p_i)^2
                  \ge c_0:={8\over\pi^2}.                   \tag{36}
\]

Assume `r_epsilon<q`.  Take all `s` vectors in the expansion of (29) equal
and restrict their coordinates to `I_i`.  Every such vector has reduced
support `q`, so

\[
 M_s^>\ge \left({c_0^s\over8}\right)^q{P\over b^q}.         \tag{37}
\]

This lower bound rigorously kills the raw positive-moment closure.  If
`p=s/(s-1)`, integral comparison for the sinc-square diagonal factor gives

\[
 \sum_A\Phi_h(A)^p\le C{P\over h},
 \qquad
 \mathcal H_>\le
       \left(C{P\over h}\right)^{1-1/s}(M_s^>)^{1/s}.       \tag{38}
\]

For the right side of (38) to be less than one it is necessary that

\[
                         M_s^><c_s\left({h\over P}\right)^{s-1}.
                                                                    \tag{39}
\]

At the proposed density scale
`h=k^BC^qP/product_i d_i`, with `d_i>=2b`, the ratio of (37) to the
right side of (39) is at least

\[
 {k^q b^{q(s-2)}\over k^{B(s-1)}}
 \left({2^{s-1}c_0^s\over8C^{s-1}}\right)^q.               \tag{40}
\]

For the large dyadic blocks `b>=k/(3(log k)^3)`, fixed `B,C`, and
macroscopic `q` tending to infinity, (40) is
`exp(Omega(sq log k))` for every `s>=2` once `k` is large (the case `s=2`
already has exponent `(q-B)log k-O(q)`).  In particular choosing `s` to
grow slowly so that `P^(1/s)=exp(o(k))` does not help: the identical-tuple
fibre is exponentially larger than the moment threshold.

The no-go is precisely scoped.  It kills

```text
positive Holder on the raw exact fibres W_>(A), followed by an ordinary
s-th collision moment, even with growing s.
```

It does not kill a centered/factorial moment in which all coincidence
partitions are subtracted with their signs.  The unique surviving
higher-moment interface is therefore an exact carry-preserving cumulant (or
an equivalent signed off-diagonal expansion) whose local factors still
retain the joint phase (14b).  Such an estimate is strictly narrower than
“use higher moments”: it must cancel the diagonal family (37), not merely
bound it.
