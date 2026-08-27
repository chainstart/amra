# Coupled conductor heat flow and the triangular shifted-divisor interface

This note attacks only the signed high-conductor interface left by
`weighted_multiplicative_character_deepening.md`.  It keeps the interval
coefficient and the product kernel coupled.  The first result is an exact
conductor-marked heat flow with a positive physical interpretation.  Its
endpoint resolution can then be audited sharply: noise strong enough to
damp high conductors creates false near-survivors, while noise fine enough
to certify an actual survivor damps no conductor by a nontrivial amount.
The second result rewrites every centered support correlation as a signed
weighted divisor statistic of the actual integers `Q0*u*t`.  This is the
remaining special-arithmetic interface.  No Erdos-451 upper bound is proved;
phase remains `survivor_deepening` and `closes=[]`.

## 1. Exact conductor heat transform

Retain

\[
 A=\lfloor k/\log ^2k\rfloor,\qquad
 Q_0={k+A\choose A},\qquad
 \mathcal P=\{p:k+A<p<2k\},\qquad P=\prod_{p\in\mathcal P}p.
\]

For `p=k+b`, put

\[
 d_p=b-1,\qquad
 \mathcal A_p^\times=-Q_0^{-1}\{1,\ldots,d_p\}\pmod p,
 \qquad \delta_p={d_p\over p-1},
 \qquad \delta=\prod_p\delta_p.                    \tag{1}
\]

Let `W` be the multiset

\[
 \mathcal W=\{ut:1\le u,t\le X,\ (ut,P)=1\},
 \qquad N=|\mathcal W|=(1+o(1))X^2,                \tag{2}
\]

where `X=exp(gamma*k/log k)`.  Write

\[
 z_p(x)={\bf1}_{\mathcal A_p^\times}(x)-\delta_p.
\]

For a multiplicative character `chi mod P`, let `f_chi` be its primitive
support conductor, `c_chi` the exact interval coefficient, and
`K_chi(W)=S_X^P(chi)^2`.  For real `sigma>=0`, define

\[
 \mathcal H_{\mathcal W}(\sigma)
 =\sum_{\chi\bmod P}f_\chi^{-\sigma}c_\chi
       K_\chi(\mathcal W).                         \tag{3}
\]

> **Coupled conductor-heat identity.**  One has exactly
> \[
> \mathcal H_{\mathcal W}(\sigma)
> =\sum_{x\in\mathcal W}\prod_{p\in\mathcal P}
>   \left(\delta_p+p^{-\sigma}z_p(x)\right).       \tag{4}
> \]

**Proof.**  Locally, the principal character has coefficient `delta_p`,
while the sum of all nonprincipal local Fourier terms is `z_p(x)`.
Because

\[
 f_\chi^{-\sigma}
 =\prod_{p:\chi_p\ne1}p^{-\sigma},
\]

expanding the product on the right of (4) selects exactly the character
terms in (3), with their signs and the `chi(-Q0)` phases intact. `square`

In particular,

\[
 \mathcal H_{\mathcal W}(0)
 =\#\{x\in\mathcal W:x\in\mathcal A_p^\times
                         \text{ for every }p\},   \tag{5}
\]

counted with product multiplicity.  Thus (4) is evaluated on the actual
fixed product multiset and not on a translated or complete-period average.

There is also an exact noise interpretation.  Independently at coordinate
`p`, keep the membership state of `x` with probability `p^{-sigma}` and
resample a uniform unit state with the complementary probability.  The
probability that the resulting coordinate is allowed is precisely the
local factor in (4).  Therefore `H_W(sigma)/N` is the probability that this
coordinate noise sends a uniformly chosen product occurrence to the
all-allowed vertex.  The `Q0` phase remains in the starting membership
pattern.

## 2. Exact near-survivor enumerator

For `x in W`, let

\[
 V(x)=\{p\in\mathcal P:x\notin\mathcal A_p^\times\}
\]

be its violation set.  Put

\[
 a_p(\sigma)=\delta_p+p^{-\sigma}(1-\delta_p),
 \quad \mathfrak A(\sigma)=\prod_pa_p(\sigma),
 \quad
 r_p(\sigma)={\delta_p(1-p^{-\sigma})\over a_p(\sigma)}.        \tag{6}
\]

All these quantities are nonnegative.  Splitting the local factor in (4)
according to membership gives the exact positive formula

> **Near-survivor identity.**
> \[
> {\mathcal H_{\mathcal W}(\sigma)\over\mathfrak A(\sigma)}
> =\sum_{x\in\mathcal W}\prod_{p\in V(x)}r_p(\sigma).           \tag{7}
> \]

For every remaining prime,

\[
 0\le r_p(\sigma)
 \le1-p^{-\sigma}
 \le\sigma\log p
 \le\sigma\log(2k).                              \tag{8}
\]

The first inequality in (8) follows because the denominator in (6) is at
least `delta_p`; the sharper displayed bound follows after canceling
`1-p^{-sigma}` and using `delta_p<=a_p(sigma)`.

Consequently, if (5) is zero, every `V(x)` is nonempty and

\[
 0\le\mathcal H_{\mathcal W}(\sigma)
 \le \mathfrak A(\sigma)N\min\{1,\sigma\log(2k)\}
 \le N\sigma\log(2k).                             \tag{9}
\]

This is not an absolute-value separation of the coefficient and kernel:
it is a pointwise consequence of their already-coupled positive inverse
transform (7).

## 3. Endpoint-resolution no-go for conductor damping

The principal term in (3) is exactly `delta*N`.  Suppose one tries to prove
a lower bound

\[
 \mathcal H_{\mathcal W}(\sigma)\ge c\delta N       \tag{10}
\]

with a fixed `c>0`, and then infer from it that (5) is nonzero.  Bound (9)
can contradict the no-survivor case only at the resolution

\[
 \sigma\log(2k)<c\delta.                           \tag{11}
\]

But the prime number theorem and the usual density estimate give

\[
 \log P=(1+o(1))k,
 \qquad \delta=\exp(-\Theta(k/\log k)).            \tag{12}
\]

At every `sigma` satisfying (11), uniformly for **all** conductors `f|P`,

\[
 0\le1-f^{-\sigma}
 \le\sigma\log f
 \le\sigma\log P
 =O\left({\delta k\over\log k}\right)=o(1).       \tag{13}
\]

Thus the only noise resolution at which principal-scale positivity can
certify an actual product survivor assigns weight `1-o(1)` even to the full
conductor.  Conversely, to damp conductors at the existing threshold

\[
 Y=X^{4/3-\eta}=\exp(\Theta(k/\log k))
\]

by a fixed factor requires `sigma=Omega(log k/k)`.  Then the no-survivor
right-hand side available in (9) is on the polynomial scale
`N*log^2(k)/k`, exponentially larger than `delta*N`.  Noise at that scale
can create the positive smoothed count entirely from near-survivors.

This rigorously kills one precise coupled bridge: apply conductor heat to
damp the high-support characters, prove principal dominance at positive
time, and use positivity alone to pass to the exact endpoint.  It does not
kill a signed Tauberian theorem that also controls the distribution of
near-survivors.

## 4. Derivatives identify the missing information

The endpoint derivatives of (4) make the required Tauberian input exact.
Writing `ell_p=log p`, direct differentiation at `sigma=0` gives

\[
 \mathcal H_{\mathcal W}'(0)
 =-\sum_{x:V(x)=\emptyset}\sum_p(1-\delta_p)\ell_p
  +\sum_p\#\{x:V(x)=\{p\}\}\,\delta_p\ell_p.      \tag{14}
\]

Indeed an all-allowed point has derivative
`-sum_p(1-delta_p)ell_p`; a point with the single violation `p` has
derivative `delta_p*ell_p`; and a point with two or more violations has a
zero of order at least two.  More generally, if `|V(x)|=v`, its summand in
(4) has the expansion

\[
 \prod_p(\delta_p+p^{-\sigma}z_p(x))
 =\sigma^v\prod_{p\in V(x)}\delta_p\ell_p
  +O_k(\sigma^{v+1}).                              \tag{15}
\]

Hence successive endpoint derivatives form a triangular ledger of exact
`v`-violation product counts.  A Tauberian continuation from a genuinely
damped time to `sigma=0` must control these near-survivor counts (or prove
cancellation equivalent to them); positivity and the low-conductor theorem
alone contain no such information.

## 5. The special 451 triangular shifted-divisor identity

There is a second exact form which retains the common start and the
canonical absorber arithmetically.  For a unit product `x`, put `y=Q0*x`
as an ordinary positive integer and define

\[
 P_j=\prod_{\substack{p\in\mathcal P\\p>k+j}}p,
 \qquad
 D(y)=\prod_{j=1}^{k-1}\gcd(y+j,P_j).              \tag{16}
\]

Because every `p in P` exceeds `k`, it can divide at most one of the
integers `y+1,...,y+k-1`.  Thus `D(y)` is a squarefree divisor of `P`.

> **Triangular divisor/carry lemma.**  For `p=k+b in P`, the following are
> equivalent:
> \[
> \begin{split}
> x&\in\mathcal A_p^\times,\\
> p&\mid D(Q_0x),\\
> p&\mid {Q_0x+d_p\choose d_p}.
> \end{split}                                      \tag{17}
> \]

**Proof.**  Membership means `Q0*x congruent -j mod p` for a unique
`1<=j<=d_p=b-1`; this is exactly the condition that `p` occur in the
`j`-th factor of (16), since `j<p-k` is equivalent to `p>k+j`.
Also `d_p<p`, so `d_p!` is a unit modulo `p`, and

\[
 {Q_0x+d_p\choose d_p}
 ={(Q_0x+1)\cdots(Q_0x+d_p)\over d_p!}
\]

is divisible by `p` exactly when one of those numerator factors is.
This proves (17). `square`

The last condition is equivalently the base-`p` carry condition for adding
`d_p` to `Q0*x mod p`.  It makes the special `start=width` structure
explicit rather than replacing the local allowed set by an arbitrary set
of size `d_p`.

For a support `S`, put

\[
 P_S=\prod_{p\in S}p,\quad
 E_S(y)={P_S\over\gcd(P_S,D(y))},\quad
 \kappa_S=\prod_{p\in S}{k\over p-1},             \tag{18}
\]

and for squarefree `E|P_S` define

\[
 \lambda_{k,S}(E)=(-1)^{\omega(E)}
       \prod_{\substack{p=k+b\\p\mid E}}{b-1\over k}.         \tag{19}
\]

Since an allowed coordinate contributes
`1-delta_p=k/(p-1)` and a violated coordinate contributes
`-delta_p=-(k/(p-1))*(d_p/k)`, (17) yields the exact coupled identity

> \[
> C_S(\mathcal W):=\sum_{x\in\mathcal W}\prod_{p\in S}z_p(x)
> =\kappa_S\sum_{x\in\mathcal W}
>       \lambda_{k,S}(E_S(Q_0x)).                  \tag{20}
> \]

For full support, if

\[
 \rho=\prod_{p\in\mathcal P}{d_p\over k},
 \qquad \delta=\kappa_{\mathcal P}\rho,
\]

then a sufficient full-slice estimate would be

\[
 \sum_{x\in\mathcal W}
 \lambda_{k,\mathcal P}(E_{\mathcal P}(Q_0x))
 =o(\rho N).                                       \tag{21}
\]

Equation (20), unlike a separated character norm, retains simultaneously
the `Q0` phase, the product multiset, every varying width `d_p`, and the
sign of the missing-prime set.  Estimate (21) is open and addresses only
the full-support slice; the total high-conductor aggregate needs its
support-weighted analogue with the outside density factors.

## 6. Why divisor size alone gives no estimate

Formula (16) implies the true divisibility

\[
 D(y)\mid\prod_{j=1}^{k-1}(y+j).                  \tag{22}
\]

For the actual rectangle,

\[
 y\le Q_0X^2=\exp(O(k/\log k)).                   \tag{23}
\]

Consequently the elementary size ledger gives only

\[
 \log D(y)
 \le k\log(y+k)=O(k^2/\log k),
 \qquad
 \omega(D(y))=O(k^2/\log^2k).                    \tag{24}
\]

But

\[
 \log P=\Theta(k),
 \qquad |\mathcal P|=\Theta(k/\log k).            \tag{25}
\]

The right side of the prime-count bound in (24) is larger than the entire
remaining-prime set by a factor of order `k/log k`; even the full product
`P` fits easily inside the crude capacity in (22).  Therefore product-size,
divisor-counting, or the fact that each large prime divides only one shift
cannot force a single violation and cannot yield cancellation in (21).
This is a quantitative no-go for a size-only use of the triangular
identity, not a counterexample to a signed shifted-divisor theorem.

## 7. Exact remaining interface

The conductor heat identity is a genuine signed coefficient--kernel
coupling, but its positivity interpolates between the exact survivor count
and a noise-created near-survivor count.  The resolution necessary to tell
those apart gives no conductor damping.  The next minimal interface is now
precise:

1. prove a weighted bound for the number of actual products with exactly
   `v` violations strong enough to control the derivative ledger (14)--(15);
   or
2. prove signed cancellation in the triangular missing-prime statistic
   (20), aggregated over the still-uncontrolled high conductors.

Either route must use more than the size of the shifted product and must
retain the parity and weights of `E_S(Q0*u*t)`.  No such bound is proved in
this round, so the main term, main exponent, and public Erdos-451 statement
are unchanged.

The exact finite replay in `coupled_heat_triangular_audit.json` checks (7),
(17), and (20) for 3,913 unit pairs in four small 451 systems.  It is only
an algebraic regression test; all asymptotic statements above are proved
symbolically and do not rely on the finite data.
