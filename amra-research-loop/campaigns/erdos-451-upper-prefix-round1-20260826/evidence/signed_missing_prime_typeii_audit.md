# Signed missing primes: exact Type-II expansion and the full-rank remainder barrier

This note continues only the signed missing-prime interface of
`coupled_conductor_heat_and_triangular_divisors.md`.  It derives an exact
weighted divisor/Mobius transform and then an exact bilinear character
formula in which the canonical absorber phase is still present.  It also
audits the strongest natural truncated Type-II bridge.  Even if divisor
distribution were perfect through the optimistic product level `X^2`, the
visible support rank would be only `O(k/log^2 k)`, whereas the actual 451
failure probabilities make every proper odd Bonferroni principal ledger
nonpositive.  Thus this bridge misses a factor `log k` in support rank.

The no-go is deliberately narrow.  It kills Type-II divisor distribution
followed by a sign-dropped Bonferroni remainder, not a genuinely coupled
signed estimate of that remainder.  No Erdos-451 upper bound is proved;
phase remains `survivor_deepening` and `closes=[]`.

## 1. Local weights and the exact divisor/Mobius transform

Keep the notation

\[
 A=\lfloor k/\log^2 k\rfloor,
 \quad Q_0={k+A\choose A},
 \quad \mathcal P=\{p:k+A<p<2k\},
 \quad P=\prod_{p\in\mathcal P}p.
\]

For `p=k+b`, put

\[
 d_p=b-1,\qquad w_p={d_p\over k},\qquad
 \delta_p={d_p\over p-1}={w_p\over1+w_p},\qquad
 q_p=1-\delta_p={k\over p-1}={1\over1+w_p}.       \tag{1}
\]

For a unit product `x=ut`, let

\[
 I_p(x)={\bf1}_{p\mid D(Q_0x)}.
\]

Thus `I_p=1` is exactly the allowed event at `p`, and a violation has
indicator `J_p=1-I_p`.  For `T subseteq S`, abbreviate

\[
 P_T=\prod_{p\in T}p,\quad
 I_T(x)=\prod_{p\in T}I_p(x)
       ={\mathbf 1}_{P_T\mid D(Q_0x)},
\]

and use analogous product notation for `w_T`, `delta_T`, and `q_T`.

The missing-prime weight from the preceding note has the following exact
local form:

> **Weighted divisor expansion.**  For every support `S`,
> \[
> \begin{split}
> \lambda_{k,S}(E_S(Q_0x))
> &=\prod_{p\in S}\bigl(I_p-w_p(1-I_p)\bigr)\\
> &=\prod_{p\in S}\bigl((1+w_p)I_p-w_p\bigr)       \tag{2}\\
> &=\sum_{T\subseteq S}(-1)^{|S|-|T|}
>       w_{S\setminus T}(1+w)_T I_T(x).           \tag{3}
> \end{split}
> \]

**Proof.**  If `I_p=1`, the local factor in (2) is one; if `I_p=0`, it is
`-w_p`.  Their product is exactly
`(-1)^omega(E_S) product_{p|E_S}w_p`.  Expanding the second product gives
(3). `square`

Since `D(Q0*x)` and `P_S` are squarefree, (3) is equivalently the weighted
Mobius divisor sum

\[
 \lambda_{k,S}(E_S(Q_0x))
 =(-1)^{|S|}w_S
   \sum_{d\mid\gcd(P_S,D(Q_0x))}
      \mu(d)\prod_{p\mid d}{p-1\over d_p}.        \tag{4}
\]

Multiplication by
`kappa_S=product_{p in S} k/(p-1)=product q_p` gives the particularly clean
centered form

\[
 \kappa_S\lambda_{k,S}(E_S(Q_0x))
 =\prod_{p\in S}(I_p-\delta_p)                    \tag{5}
\]

and hence

\[
 \prod_{p\in S}(I_p-\delta_p)
 =(-1)^{|S|}\delta_S
   \sum_{d\mid\gcd(P_S,D(Q_0x))}{\mu(d)\over\delta_d}.       \tag{6}
\]

Formula (6) is the useful exact divisor transform: it retains the sign of
the missing set, rather than replacing it by the size of `D`.

## 2. The phase-preserving Type-II formula

Let

\[
 \mathcal W_X=\{ut:1\le u,t\le X,\ (ut,P)=1\}
\]

as a multiset, and put

\[
 M_X=\#\{n\le X:(n,P)=1\},\qquad N=M_X^2.
\]

For `d|P`, define the allowed divisor count

\[
 N_d(X)=\sum_{\substack{u,t\le X\\(ut,P)=1}}
      {\mathbf 1}_{d\mid D(Q_0ut)}.                 \tag{7}
\]

If `d=P_T`, let

\[
 \mathcal J_d=\prod_{p\mid d}\{1,\ldots,d_p\}.
\]

For `j=(j_p) in mathcal J_d`, let `r_d(j)` be the unique unit residue modulo
`d` satisfying

\[
 r_d(j)\equiv-Q_0^{-1}j_p\pmod p\qquad(p\mid d). \tag{8}
\]

At a fixed `p`, at most one of `Q0*ut+1,...,Q0*ut+d_p` is divisible by
`p`.  Consequently the following is an equality of zero-one indicators,
not an overcount:

\[
 {\mathbf 1}_{d\mid D(Q_0ut)}
 =\sum_{j\in\mathcal J_d}{\mathbf 1}_{ut\equiv r_d(j)\pmod d}. \tag{9}
\]

For a character `chi mod d`, set

\[
 \widehat{\mathcal J}_{Q_0,d}(\chi)
 =\sum_{j\in\mathcal J_d}\overline{\chi(r_d(j))}
 =\chi(-Q_0)\prod_{p\mid d}
      \sum_{j=1}^{d_p}\overline{\chi_p(j)},       \tag{10}
\]

and

\[
 S_X^P(\chi)=\sum_{\substack{n\le X\\(n,P)=1}}\chi(n).
\]

Multiplicative orthogonality in (9) proves the exact bilinear identity

> \[
> N_d(X)={1\over\varphi(d)}
>   \sum_{\chi\bmod d}
>    \widehat{\mathcal J}_{Q_0,d}(\chi)
>       \bigl(S_X^P(\chi)\bigr)^2.                \tag{11}
> \]

The square in (11) is a signed complex square, not an absolute square.
The factor `chi(-Q0)` in (10) is therefore retained.  If `chi` is extended
as a Dirichlet character modulo `d`, the outer unit sieve also has the exact
Mobius expansion

\[
 S_X^P(\chi)=
 \sum_{\substack{e\mid P/d\\e\le X}}
   \mu(e)\chi(e)\sum_{v\le X/e}\chi(v).           \tag{12}
\]

The principal character in (11) contributes

\[
 {\prod_{p\mid d}d_p\over\varphi(d)}M_X^2
 =\delta_d N.
\]

Writing

\[
 N_d(X)=\delta_dN+\mathcal E_d(X),                \tag{13}
\]

and summing (6) over the actual product multiset gives

\[
 C_S(\mathcal W_X)
 =(-1)^{|S|}\delta_S
   \sum_{d\mid P_S}{\mu(d)\over\delta_d}N_d(X).  \tag{14}
\]

For every nonempty `S`, all principal terms cancel because
`sum_{d|P_S}mu(d)=0`; therefore

> \[
> C_S(\mathcal W_X)
> =(-1)^{|S|}\delta_S
>   \sum_{d\mid P_S}{\mu(d)\over\delta_d}
>      \mathcal E_d(X).                           \tag{15}
> \]

Equations (10), (11), and (15) are the desired non-separated Type-II
interface.  The existing low-conductor theorem controls the aggregate whose
primitive character conductor is at most `X^(4/3-eta)`.  Extending generic
bilinear distribution optimistically to divisor moduli of order `X^2`
would still not reach the ranks needed below.

## 3. The true support rank visible at the `X^2` level

Take

\[
 X=\exp(\gamma k/\log k)
\]

for a fixed `gamma>0`.  Every divisor `d|P` supported on `r` remaining
primes satisfies

\[
 d>(k+A)^r.                                       \tag{16}
\]

Multiplication by `Q0` changes the residue in (8), not its conductor.
Even if one generously calls `Q0*X^2` rather than `X^2` the available
product level, one has

\[
 r\le {\log Q_0+2\log X\over\log(k+A)}.          \tag{17}
\]

The standard binomial bound gives

\[
 \log Q_0\le A\log{e(k+A)\over A}
 =O\left({k\log\log k\over\log^2k}\right)
 =o(k/\log k).                                    \tag{18}
\]

Thus the most optimistic Type-II rank at that level is

\[
 R_{II}\le(2\gamma+o(1)){k\over\log^2k}.         \tag{19}
\]

On the other hand the prime number theorem gives

\[
 m=|\mathcal P|=(1+o(1)){k\over\log k}.          \tag{20}
\]

Consequently

\[
 {R_{II}\over m}\le{2\gamma+o(1)\over\log k}=o(1).          \tag{21}
\]

This is the precise missing factor: the natural Type-II product level sees
only `O(m/log k)` simultaneous prime conditions.  The full divisor `P` has
`log P=(1+o(1))k`, while `log(Q0*X^2)=O(k/log k)`.

## 4. Exact audit of truncated Bonferroni

For an actual product occurrence `x`, let

\[
 V(x)=\sum_{p\in\mathcal P}J_p(x)
\]

be its number of violations.  For `T subseteq mathcal P`, set

\[
 B_T(X)=\sum_{x\in\mathcal W_X}\prod_{p\in T}J_p(x).
\]

Every `B_T` of rank at most `R` is an alternating linear combination of
the `N_{P_U}` with `U subseteq T`.  Hence a perfect divisor-distribution
theorem through rank `R` would give

\[
 B_T(X)=q_TN\qquad(|T|\le R).                     \tag{22}
\]

The natural proposed closure is then the odd Bonferroni lower bound

\[
 N_0(X)\ge
 \sum_{j=0}^R(-1)^j\sum_{|T|=j}B_T(X),           \tag{23}
\]

where `N0` is the all-allowed count and `R` is odd.  The following shows
that this remains useless even under the ideal equality (22).

> **Full-rank Bonferroni barrier.**  Let `q_1,...,q_m` lie in `[1/2,1]`,
> and write `e_j(q)` for their elementary symmetric polynomials.  For every
> odd `R<m`,
> \[
> L_R(q):=\sum_{j=0}^R(-1)^je_j(q)\le0.           \tag{24}
> \]

**Proof.**  Let independent Bernoulli variables have failure probabilities
`q_i`, and let `V` be their sum.  For every integer `v` and odd `R`,

\[
 \sum_{j=0}^R(-1)^j{v\choose j}
 ={\mathbf 1}_{v=0}-{v-1\choose R}{\mathbf 1}_{v>R}. \tag{25}
\]

Taking expectations yields

\[
 L_R(q)=\prod_i(1-q_i)
 -\mathbb E\left[{V-1\choose R}{\bf1}_{V>R}\right].          \tag{26}
\]

The all-failure event alone contributes
`binom(m-1,R) product_i q_i` to the expectation.  Since
`binom(m-1,R)>=1` and `q_i>=1-q_i` coordinatewise, (26) is nonpositive.
`square`

In the 451 system, (1) gives `q_p>1/2` for every remaining prime because
`p<2k`.  Therefore (24) applies with the **actual unequal local
probabilities**, not merely with a half-density toy model.  Even perfect
Type-II distribution for every modulus through any proper odd support rank
produces no positive lower bound in (23).  Since (21) has `R_II=o(m)`, an
`X^2` Type-II theorem misses the needed full rank by a factor asymptotic to
`log k`.

This kills the quantitative candidate

> optimal divisor distribution through `Q0*X^2`, followed by truncated
> inclusion-exclusion with the high-rank remainder discarded by sign.

It does not kill cancellation that keeps that remainder coupled to (15).

## 5. The exact remainder and the precision obstruction

Summing (25) over the actual product multiset gives, for every odd `R<m`,

\[
 \begin{split}
 N_0(X)
 &=\sum_{j=0}^R(-1)^j\sum_{|T|=j}B_T(X)
   +\mathcal T_R(X),                              \tag{27}\\
 \mathcal T_R(X)
 &=\sum_{x\in\mathcal W_X}
    {V(x)-1\choose R}{\bf1}_{V(x)>R}.             \tag{28}
 \end{split}
\]

Thus the missing object is one explicit positive, but globally coupled,
violation-tail statistic.  Its independent comparator is

\[
 \mathcal T_R^{\rm ind}
 =N\,\mathbb E_q\left[{V-1\choose R}{\bf1}_{V>R}\right].     \tag{29}
\]

Controlling (28) by an ordinary relative asymptotic is not enough.  Put

\[
 q_*=\prod_pq_p=\kappa_{\mathcal P},\qquad
 \delta=\prod_p\delta_p,\qquad
 \rho=\prod_p{d_p\over k},
\]

so that `delta=q_* rho`.  The all-failure event gives

\[
 \mathcal T_R^{\rm ind}
 \ge N{m-1\choose R}q_*\ge Nq_*                 \tag{30}
\]

and hence

\[
 {\delta N\over\mathcal T_R^{\rm ind}}
 \le {\delta\over q_*}=\rho.                    \tag{31}
\]

Prime-number-theorem partial summation over `p=k+b` gives

\[
 -\log\rho
 =\sum_{p\in\mathcal P}\log{k\over p-k-1}
 =(1+o(1)){k\over\log k}.                        \tag{32}
\]

Indeed the corresponding integral is
`log(k)^(-1) integral_A^k log(k/b) db=(1+o(1))k/log k`;
the removed initial interval and the shift by one are lower order.
Therefore a separate estimate

\[
 \mathcal T_R(X)=(1+\varepsilon_k)\mathcal T_R^{\rm ind}
\]

can recover the survivor main term only if

\[
 |\varepsilon_k|=o(\rho)
 =\exp(-(1+o(1))k/\log k),                        \tag{33}
\]

not merely with a power or logarithmic saving.  Thus (33) is a necessary
precision threshold; if the independent tail is larger than the lower bound
in (30), the necessary precision is stronger still.  In the independent
comparator, the low-rank principal ledger and the tail are individually
exponentially larger than `delta*N` and cancel to the survivor scale.
Estimating them separately recreates the same information loss as separated
coefficient/kernel norms.

## 6. The sole surviving Type-II formulation

Equations (15) and (27) leave one precise possibility.  A successful theorem
must estimate, at absolute error `o(delta*N)`, the **combined signed
difference** between

1. the phase-preserving Type-II divisor ledger in (15), through the ranks
   genuinely accessible to bilinear distribution; and
2. the actual full-order remainder `T_R` in (28),

without taking absolute values or separate relative asymptotics.  Equivalently
it may prove a direct `delta*N`-scale law for the violation generating
polynomial of `D(Q0*ut)` at its endpoint.  Such a theorem would be a genuine
near-survivor result because it distinguishes the actual `V=0` fibre at a
scale smaller than the independent tail comparator by
`exp((1+o(1))k/log k)`.

No such coupled remainder theorem is proved here.  What is proved is the
exact phase-preserving divisor/character interface, the `X^2` support-rank
ceiling, and the full-rank Bonferroni/precision no-go.  The original problem,
main exponent, and main term are unchanged.
