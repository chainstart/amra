# Free-multiplier bilinear counting: exact formulas and a conductor-only no-go

This note remains in `survivor_deepening` and has `closes=[]`.  It asks
whether averaging the free multiplier in `q=Q_0u` turns the fixed-prefix
problem into a bilinear estimate.  The exact answer is that it produces a
positive divisor weight on the same prefix.  Complete-period and second-
moment formulas are available, but any estimate that separates the
bilinear kernel from the interval Fourier coefficients loses exponentially
at the full 451 conductor.  A coefficient--kernel signed coupling remains
open.

## 1. The combined count is a divisor-weighted prefix

Put

\[
 A=\lfloor k/\log ^2k\rfloor,
 \qquad Q_0={k+A\choose A},
\]

and let `mathcal P` be the primes `k+A<p<2k`.  For `p=k+b` define

\[
 \mathcal A_p=
 \{0,-Q_0^{-1},\ldots,-(b-1)Q_0^{-1}\}\pmod p,
\qquad
 F(s)=\prod_{p\in\mathcal P}{\bf1}_{\mathcal A_p}(s).
                                                               \tag{1}
\]

Thus `n=Q_0ut` satisfies every remaining 451 congruence exactly when
`F(ut)=1`; the primes at offset at most `A` are already absorbed by `Q_0`.
For positive integers `U,H`, let

\[
 d_{U,H}(s)=\#\{(u,t):1\le u\le U,\ 1\le t\le H,\ ut=s\}.
                                                               \tag{2}
\]

Then the following identity is literal regrouping, with no equidistribution
input:

> **Divisor-weight identity.**
> \[
> {1\over U}\sum_{u\le U}\sum_{t\le H}F(ut)
> ={1\over U}\sum_{s\le UH}d_{U,H}(s)F(s).          \tag{3}
> \]

In particular, positivity of either side gives a valid 451 candidate below
`Q_0UH`, but averaging has created no candidate outside the original prefix
`s<=UH`.  If that prefix contains no allowed `s`, both sides vanish.  The
weight is highly nonuniform and cannot be replaced by its mean without a
new theorem.

## 2. Exact Fourier and conductor decomposition

Let

\[
 P=\prod_{p\in\mathcal P}p,
 \qquad D=\prod_{p=k+b\in\mathcal P}{b\over p}.
\]

For a local interval write

\[
 \beta_p(h)={1\over b}\sum_{x\in\mathcal A_p}e_p(-hx),
 \qquad \beta_p(0)=1.                               \tag{4}
\]

CRT Fourier inversion gives the exact combined count

\[
 N(U,H):=\sum_{u\le U,t\le H}F(ut)
 =D\left(UH+
 \sum_{\emptyset\ne S\subseteq\mathcal P}
 \sum_{a\in(\mathbb Z/P_S\mathbb Z)^*}
       \beta_S(a)B_{P_S}(a;U,H)\right),             \tag{5}
\]

where `P_S=product_{p in S}p`, `beta_S` is the product of the nonzero
local coefficients selected by the CRT frequency `a`, and

\[
 B_M(a;U,H)=\sum_{u\le U}\sum_{t\le H}e_M(aut).
                                                               \tag{6}
\]

For a frequency `a mod q`, put `g=(a,q)`, `M=q/g`, and `a_0=a/g`.
Then

\[
 B_q(a;U,H)=B_M(a_0;U,H),\qquad (a_0,M)=1.          \tag{7}
\]

Thus the exact conductor of a support is `P_S`; zero local coordinates are
not silently charged to the full product.

The term `DUH` in (5) is only the zero Fourier character.  It is not the
expectation of a uniform product map.  Already for one prime, if `u,t` each
run through a complete residue system modulo `p`, then

\[
 {1\over p^2}\#\{(u,t):ut\in\mathcal A_p\}
 ={p+(p-1)b\over p^2}
 ={b\over p}+{p-b\over p^2}.                        \tag{8}
\]

The excess is the zero-product multiplicity.  If `u` is restricted to
units and `t` is complete, the probability is exactly `b/p`; however, the
interval `1<=u<=U` then acquires a sieve weight.  Removing multipliers
divisible by any remaining prime costs at most

\[
 \sum_{p\in\mathcal P}\lfloor U/p\rfloor=O(U/\log k),             \tag{9}
\]

but it does not restore a plain rectangular bilinear kernel.

## 3. Unconditional bilinear formulas

Assume `(a,M)=1`.  Orthogonality over one complete `u` period gives

\[
 \sum_{u=1}^{M}\sum_{t\le H}e_M(aut)
 =M\lfloor H/M\rfloor.                              \tag{10}
\]

Consequently, if `U=vM+r`, `0<=r<M`, then

\[
 B_M(a;U,H)
 =vM\lfloor H/M\rfloor+B_M(a;r,H).                 \tag{11}
\]

In particular, if both side lengths are multiples of `M`, then

\[
 B_M(a;U,H)=UH/M,                                   \tag{12}
\]

not zero.  Summing the geometric kernels in the incomplete block gives the
standard unconditional pointwise estimate

\[
 |B_M(a;U,H)|
 \le {UH\over M}+O(M(1+\log M)),                   \tag{13}
\]

together with the always available `|B_M|<=UH`.  Formula (13) is useful in
the long-period regime but says nothing when `M` is much larger than the
rectangle.

There is also an exact additive second moment.  Define

\[
 E_M(H)=\#\{t_1,t_2\le H:t_1\equiv t_2\pmod M\}.
\]

If `H=wM+h`, `0<=h<M`, then

\[
 E_M(H)=h(w+1)^2+(M-h)w^2
 \le H^2/M+H.                                       \tag{14}
\]

Parseval over a complete `u` period and Cauchy--Schwarz yield

\[
 |B_M(a;U,H)|^2
 \le U(\lfloor U/M\rfloor+1)M E_M(H),              \tag{15}
\]

and the symmetric bound obtained by interchanging `U,H`.  In particular,
for `U,H<=M`,

\[
 |B_M(a;U,H)|\le\min\{UH,\sqrt{UHM}\}.             \tag{16}
\]

The square-root expression improves the trivial bound only when `UH>M`.

Finally, the exact frequency second moment is

\[
 \sum_{a\bmod M}|B_M(a;U,H)|^2
 =M\,\mathcal E_M(U,H),                             \tag{17}
\]

where

\[
 \mathcal E_M(U,H)
 =\#\{u_1t_1\equiv u_2t_2\pmod M:
          u_i\le U,\ t_i\le H\}.                  \tag{18}
\]

This identity is exact for every `M`; restricting the left side to primitive
frequencies requires Ramanujan sums and is not the same identity.  The
diagonal gives `mathcal E_M(U,H)>=UH`.

## 4. A genuine high-conductor counterexample

The short-rectangle obstruction is pointwise, not merely a poor upper
bound.  If

\[
 M\ge12UH,
\]

then every phase in `B_M(1;U,H)` lies between `0` and `pi/6`.  Therefore

\[
 \Re B_M(1;U,H)\ge\cos(\pi/6)UH,
 \qquad |B_M(1;U,H)|\ge\cos(\pi/6)UH.              \tag{19}
\]

The same proof works after restricting `u` to any subset, including the
multipliers coprime to all remaining primes, with `UH` replaced by the
number of retained pairs.

This occurs in the actual 451 family.  By the prime number theorem,

\[
 \log P=\sum_{k+A<p<2k}\log p=(1+o(1))k.            \tag{20}
\]

Hence for every `U,H` with `log U+log H=o(k)`, the full support satisfies
`P>=12UH` for large `k`.  The CRT character `a=1 mod P` has a nonzero local
coordinate at every remaining prime, and every corresponding proper-
interval Fourier coefficient is nonzero.  Thus (19) is a real full-support
451 character on which multiplier averaging produces no cancellation.
It strictly refutes any proposed bound

\[
 |B_{P_S}(a;U,H)|=o(UH)
\]

that depends only on large conductor or large support.  It does not by
itself show that this character dominates the signed Fourier sum, because
its interval coefficient may be small.

## 5. Why separate absolute-value and second-moment ledgers still fail

The local interval coefficients obey the exact Parseval formula

\[
 \sum_{h\bmod p}|\beta_p(h)|^2={p\over b},
 \qquad
 \sum_{h\ne0}|\beta_p(h)|^2={k\over b}.             \tag{21}
\]

Nevertheless, applying Cauchy--Schwarz separately to the complete Fourier
coefficient vector and to (17) loses the required coupling.  Here
`widehat F(a)=sum_{x mod P}F(x)e_P(-ax)` is **unnormalized**; Fourier
inversion in (5) uses `widehat F(a)/P`.  Globally,

\[
 \sum_{a\bmod P}|\widehat F(a)|^2=P^2D,
 \qquad
 \sum_{a\bmod P}|B_P(a)|^2=P\mathcal E_P(U,H).      \tag{22}
\]

If `UH<P/2`, then after removing the zero frequency,

\[
 \sum_{a\ne0}|B_P(a)|^2
 =P\mathcal E_P(U,H)-(UH)^2\ge\tfrac12PUH.          \tag{23}
\]

Also the nonzero Fourier coefficient square mass is
`P^2D(1-D)`.  Thus the numerical right side

\[
 {1\over P}
 \left(\sum_{a\ne0}|\widehat F(a)|^2\right)^{1/2}
 \left(\sum_{a\ne0}|B_P(a)|^2\right)^{1/2}
\]

delivered by separate global Cauchy--Schwarz, relative to the
zero-character main term `DUH`, is

\[
 \sqrt{{(1-D)P\over2DUH}}.                          \tag{24}
\]

For the 451 parameters, `log P=Theta(k)`, `-log D=o(k)`, and
`log(UH)=o(k)`, so (24) is `exp(Theta(k))`.  This is a no-go for the
**method** of separating the two vectors; it is not a lower bound for the
actual signed error.

The elementary triangle ledger is also fatal, although its sharp scale is
subexponential rather than `exp(Omega(k))`.  For primes in any fixed bulk
subinterval of `(3k/2,2k)`, the discrete interval Dirichlet kernel satisfies

\[
 \sum_{h\ne0}|\beta_p(h)|\gg\log k.                \tag{25}
\]

One proof pairs consecutive `h`: since `b/p` stays in a compact subinterval
of `(0,1)`, at least one of two consecutive numerators
`|sin(pi b h/p)|` is bounded below, and harmonic summation for
`h<=p/4` gives (25).  There are `Theta(k/log k)` such primes.  Therefore the
triangle envelope that assigns the trivial `|B_{P_S}|<=UH` to the high
supports has relative size at least

\[
 \exp\!\left(\Omega\!\left(
       {k\log\log k\over\log k}\right)\right),      \tag{26}
\]

by taking supports containing a fixed positive fraction of those bulk
primes.  Their conductors are `exp(Theta(k))`, hence exceed `UH`.  The
ledger (26) is already far too large to prove positivity, despite being
`exp(o(k))`; it must not be misstated as an `exp(Omega(k))` lower bound.

## 6. Exact surviving interface

Equations (19), (24), and (26) kill three specific bridges:

1. large conductor alone makes every nonzero bilinear character small;
2. a global or conductor-wise second moment may be separated from the
   interval coefficient vector by absolute Cauchy--Schwarz; or
3. high supports may be summed after applying the trivial pointwise kernel
   bound character by character.

They do **not** refute a signed theorem coupling the exact inverse-binomial/
Vandermonde coefficient `beta_S(a)` to the same phase `a` in `B_{P_S}(a)`.
A sufficient remaining bridge is a bound of the form

\[
 \sum_{\emptyset\ne S\subseteq\mathcal P}
 \sum_{a\in(\mathbb Z/P_S\mathbb Z)^*}
       \beta_S(a)B_{P_S}(a;U,H)>-UH+o(UH),          \tag{27}
\]

or any stronger quantitative estimate making the bracket in (5) positive,
for some `log U+log H=o(k)`.  Such a theorem would close the combined
counting interface and produce `n=Q_0ut=exp(o(k))`.  It is presently open;
none of (10)--(18) controls its sign.

Accordingly the free-multiplier cluster lemma remains valid, but replacing
selection of one `u` by an unweighted bilinear average does not close a new
full-character interface.  The only surviving version must retain signed
coefficient--kernel coupling.  The campaign phase and `closes=[]` remain
unchanged.

## 7. Unit-group multiplicative characters: a distinct surviving interface

There is a more natural diagonalization of the product `ut`.  It is
genuinely different from the additive kernel (6), although it still does not
close the high-conductor range.

Restrict both variables to

\[
 \mathcal U_X=\{n\le X:(n,P)=1\}
\]

and put `mathcal A_p^times=mathcal A_p minus {0}`.  This loses no logical
generality for an existence proof.  The number of excluded integers is at
most

\[
 X\sum_{p\in\mathcal P}{1\over p}=O(X/\log k),       \tag{28}
\]

although this error must **not** be subtracted from the exponentially sparse
main term.  Instead the unit-restricted count is analyzed in its own right.
Its local and global densities are

\[
 \delta_p^\times={b-1\over p-1},\qquad
 \delta^\times=\prod_{p\in\mathcal P}\delta_p^\times.
                                                               \tag{29}
\]

Moreover

\[
 \log {\delta^\times\over D}
 =\sum_{p=k+b}\log\left(1-{k\over b(p-1)}\right)=o(1).          \tag{30}
\]

Indeed Brun--Titchmarsh applied to each dyadic offset block
`B<b<=2B`, `B>=A`, gives `O(B/log k)` primes (uniformly down to
`A=floor(k/log^2 k)`), so the absolute logarithmic loss in (30) is
`O(loglog k/log k)`.  Thus `delta^times=(1-o(1))D` and the zero-product bias
from (8) has disappeared.

Let `widehat G=(Z/PZ)^*` be the multiplicative character group.  For
`chi in widehat G` define

\[
 c_\chi={1\over\varphi(P)}
   \sum_{x\in(\mathbb Z/P\mathbb Z)^*}
   {\bf1}_{\mathcal A^\times}(x)\overline{\chi(x)},
 \qquad
 S_X^P(\chi)=\sum_{n\in\mathcal U_X}\chi(n).        \tag{31}
\]

Then multiplicative Fourier inversion gives the exact diagonal identity

> **Unit-group product identity.**
> \[
> \sum_{u\in\mathcal U_U,t\in\mathcal U_H}
>   {\bf1}_{\mathcal A^\times}(ut)
> =\sum_{\chi\in\widehat G}c_\chi
>       S_U^P(\chi)S_H^P(\chi).                    \tag{32}
> \]

The principal coefficient is `c_1=delta^times`, so its contribution is

\[
 \delta^\times|\mathcal U_U||\mathcal U_H|
 =(1+O(1/\log k))\delta^\times UH.                 \tag{33}
\]

The coefficients factor locally.  For a local character `psi mod p`,

\[
 c_{p,\psi}={1\over p-1}
 \sum_{j=1}^{b-1}\overline{\psi(-Q_0^{-1}j)},       \tag{34}
\]

so the canonical inverse-binomial absorber is retained as a multiplicative
phase, rather than being erased.

There are two precise limitations.

First, a character whose nonprincipal local components have primitive
conductor `f` is still a character modulo `P`: outside `f` it contains the
principal unit sieve.  Removing that sieve would allow complete `f`-periods
or the classical bound `O(sqrt(f)log f)`, but exact inclusion--exclusion is

\[
 S_X^P(\chi)=
 \sum_{\substack{d\mid P/f\\d\le X}}
   \mu(d)\chi^*(d)
   \sum_{m\le X/d}\chi^*(m),                       \tag{35}
\]

where `chi^*` is the inducing primitive character.  Thus “low conductor is
killed by complete periods” is exact only before the outer unit sieve;
afterward it needs a weighted sieve/character-sum estimate.  Low support is
still the plausible tractable range, but (35) is not a free cancellation.

Second, for the full conductor `f=P=exp(Theta(k))`, every affordable
`X=exp(o(k))` lies far below the unconditional Burgess threshold
`P^(1/4+epsilon)`.  Burgess therefore gives no nontrivial full-support bound.
The exact group large-sieve identity has the same obstruction.  Since
`UH<P`,

\[
 \sum_{\chi\in\widehat G}
 |S_U^P(\chi)S_H^P(\chi)|^2
 =\varphi(P)\,
 \#\{u_1t_1=u_2t_2:
          u_i\in\mathcal U_U,t_i\in\mathcal U_H\}. \tag{36}
\]

Also multiplicative Parseval gives

\[
 \sum_\chi|c_\chi|^2=\delta^\times,
 \qquad
 \sum_{\chi\ne1}|c_\chi|^2
 =\delta^\times(1-\delta^\times).                 \tag{37}
\]

After removing the principal character, the kernel square norm is

\[
 \varphi(P)\mathcal E_P^\times(U,H)
 -|\mathcal U_U|^2|\mathcal U_H|^2
 \ge\tfrac12\varphi(P)|\mathcal U_U||\mathcal U_H|,              \tag{38}
\]

because `UH=o(varphi(P))`.  Hence the numerical Cauchy--Schwarz ledger,
relative to (33), is at least

\[
 \sqrt{{(1-\delta^\times)\varphi(P)
              \over\delta^\times UH}}
 =\exp(\Theta(k)).                                  \tag{39}
\]

As before, (39) is a no-go for separated global `L^2`, not a lower bound on
the signed character error.

Therefore (32) is a legitimate surviving representation: it repairs the
zero-product bias and exactly diagonalizes `ut`.  Its precise open interface
is a weighted multiplicative-character theorem coupling the interval
coefficient (34) to the two sieved sums in (32), with enough aggregate
cancellation over conductors up to `P`.  Complete periods can address only
a low-conductor portion, and current unconditional Burgess/large-sieve
inputs do not reach the high-conductor portion.  This representation does
not alter `closes=[]`.
