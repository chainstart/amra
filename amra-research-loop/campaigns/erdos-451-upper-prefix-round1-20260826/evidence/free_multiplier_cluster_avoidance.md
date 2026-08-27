# Free-multiplier absorber avoidance for bounded clusters

This note remains in `survivor_deepening` with `closes=[]`.  It proves that a
subexponential free multiplier can simultaneously move every bounded-
diameter cluster resonance of slowly growing bounded rank away from its
dangerous prefix-pole scale.  It controls only these explicitly known
characters, not the full Fourier sum or Erdos 451.

## 1. Family of cluster obstructions

Let

\[
 A=\lfloor k/\log^2k\rfloor,
 \qquad Q_0={k+A\choose A}.
\]

For every fixed `r>=2`, fix an arbitrary nonnegative integer diameter `B_r`
(a real diameter bound may first be replaced by its ceiling).  Let
`mathscr C_k(R)` be the family of sets

\[
 S=\{p_1<\cdots<p_r\}\subset(k+A,2k),
 \qquad 2\le r\le R,qquad p_r-p_1\le B_r.           \tag{1}
\]

Write

\[
 P_S=\prod_{p\in S}p,qquad
 L_S=\prod_{i<j}(p_j-p_i),qquad
 \ell_S=(-1)^{r+1}L_S.                              \tag{2}
\]

Choosing the smallest prime and then its fixed integer offsets shows

\[
 N_k(R):=|\mathscr C_k(R)|\le C_R k,                 \tag{3}
\]

where one may take

\[
 C_R=1+\sum_{r=2}^R {B_r\choose r-1}.               \tag{4}
\]

The estimate deliberately uses only `O(k)` possible bases, not a fictitious
`k^r` independent choice of primes.

For every fixed `R` and all sufficiently large `k`, each `L_S` is smaller
than every prime in `S`.  Thus

\[
 \gcd(Q_0L_S,P_S)=1,                                \tag{5}
\]

because all primes in (1) are beyond the primes absorbed by `Q_0`.

## 2. Exact bad-multiplier count

Fix constants `D>=2` and `C>=0`.  For `S` of rank `r`, set

\[
 K_S=k^D(\log k)^{Cr},\qquad
 R_S=\frac{P_S}{K_S}.                               \tag{6}
\]

For a positive integer `u`, the transported cluster frequency under

\[
 q=Q_0u,qquad s=qt-(k+1)
\]

is exactly

\[
 a_S(u)=\langle uQ_0\ell_S\rangle_{P_S}.             \tag{7}
\]

By (5), multiplication by `Q_0 ell_S` permutes `Z/P_SZ`.  Hence in
`1<=u<=U`,

> **Single-cluster multiplier count.**
> \[
> \#\{u\le U:|a_S(u)|\le R_S\}
> \le(2\lfloor R_S\rfloor+1)
>       \left(\frac U{P_S}+1\right).                \tag{8}
> \]

This includes the incomplete endpoint block of `u` and makes no random
or equidistribution assumption.

Summing (8) over (1), and using `P_S>k^r>=k^2`, gives

\[
 \frac1U\#\{u\le U:\text{some cluster is bad}\}
 \le \frac{2N_k(R)}{k^D}+\frac{N_k(R)}{k^2}
      +\frac1U\sum_{S\in\mathscr C_k(R)}
        (2\lfloor R_S\rfloor+1).                   \tag{9}
\]

The first two terms are the complete-period contribution; the final term is
the exact endpoint loss.  In particular, it is not enough merely to say that
`u` is uniform modulo every different `P_S`: `U` must also dominate the sum
of the radii.

## 3. Enforcing all remaining-prime inverses

The affine formula at a remaining prime needs `u` to be coprime to that
prime.  Let

\[
 \mathcal P_k=\{p:k+A<p<2k,\ p\text{ prime}\}.
\]

The number of `u<=U` divisible by at least one member of `mathcal P_k` is at
most

\[
 \sum_{p\in\mathcal P_k}\left\lfloor\frac Up\right\rfloor
 \le \frac U k|\mathcal P_k|
 =O(U/\log k).                                      \tag{10}
\]

Thus coprimality removes a vanishing proportion, not one independent choice
per prime.

For fixed `R`, take for example

\[
 U=C_R(2k)^{R+4}.                                   \tag{11}
\]

Since `P_S<=(2k)^r`, (3) and (6) show

\[
 \frac1U\sum_S(2\lfloor R_S\rfloor+1)=o_R(1).       \tag{12}
\]

Moreover, (3) makes the first two terms of (9) `o_R(1)` for every `D>=2`.
Together with (10), this proves:

> **Fixed-rank free-multiplier lemma.**  For every fixed `R,D,C` and all
> sufficiently large `k`, there is an integer `1<=u<=U` such that
> \[
> \gcd\left(u,\prod_{p\in\mathcal P_k}p\right)=1
> \quad\text{and}\quad
> |a_S(u)|>\frac{P_S}{k^D(\log k)^{C|S|}}
> \quad(S\in\mathscr C_k(R)).                       \tag{13}
> \]

No primality theorem beyond the standard upper bound
`|mathcal P_k|=O(k/log k)` is used in this selection.

## 4. A slowly growing rank cutoff

The constants in (3)--(5) can grow arbitrarily badly with `R`, so `R` cannot
be replaced by an unspecified growing function.  A diagonal choice is still
available.  Let

\[
 L_R^*=1+\max_{2\le r\le R}
       B_r^{r(r-1)/2}.
\]

Choose an integer function `R_0(k)` tending to infinity so slowly that

\[
 R_0(k)\log(2k)=o(k),\qquad
 C_{R_0(k)}\le k^{1/4},\qquad
 L_{R_0(k)}^*<k.                                    \tag{14}
\]

Such a function exists because every `C_R,L_R^*` is finite when `R` is
fixed.  With

\[
 U(k)=C_{R_0(k)}(2k)^{R_0(k)+4},                    \tag{15}
\]

one has `log U=o(k)`.  The estimates (9)--(12) remain uniform: their
complete-period part is

\[
 O(C_{R_0}k^{1-D}+C_{R_0}/k)=o(1),                 \tag{16}
\]

and (15) dominates the endpoint sum by four additional powers of `2k`.
Therefore (13) holds simultaneously for every cluster of rank at most
`R_0(k)`.

For each fixed `r`, eventually `r<=R_0(k)`.  Hence the selected multiplier
eliminates, at the quantitative scale (13), every fixed-rank bounded-
diameter Maynard obstruction, including any one fixed offset pattern that
occurs infinitely often.

## 5. Budget and exact affine formulas after changing the absorber

Put `q=Q_0u` with the multiplier supplied above.  Every prime
`k<p<=k+A` still divides `q`, so `n=qt` satisfies its 451 constraint
automatically.  At every remaining prime, (10) gives `gcd(q,p)=1`, and the
allowed set is exactly

\[
 t\bmod p\in\{0,-q^{-1},\ldots,-(p-k-1)q^{-1}\}.    \tag{17}
\]

The canonical congruence becomes

\[
 q\equiv u(-1)^A{p-k-1\choose A}\pmod p.            \tag{18}
\]

Thus the inverse-binomial/Vandermonde Fourier formulas remain valid after
replacing `Q_0` by `q`: the combined denominator `Q_0(P/p)` gains the factor
`u`, so its inverse local frequency gains `u^{-1}`.  The rational carry
identity from the preceding round rescales by the same common factor; no new
cancellation is inferred.  Consistently, a direct global frequency `ell`
moves to `q ell mod P` as in (7).

Finally,

\[
 \log q=\log Q_0+\log u=o(k),                        \tag{19}
\]

by the canonical binomial estimate and (14)--(15).  Multiplying the final
`t` by `q` therefore preserves every `exp(o(k))` target budget.

## 6. What the lemma actually controls

For the scaled cluster product, every global Fourier coefficient has
magnitude at most `P_S`.  The interval kernel at a nonzero centered frequency
`a` is at most `P_S/(2|a|)` up to an absolute endpoint convention.  Hence
(13) bounds the contribution of the **specific transported cluster
resonance and its conjugate** by

\[
 O\left(P_S k^D(\log k)^{C|S|}\right)
 =O\left(2^{|S|}k^{|S|+D}(\log k)^{C|S|}\right).     \tag{20}
\]

This is precisely the desired scale for those known characters.

It is not a dyadic block estimate.  The lemma does not control:

- other large Fourier characters of the same support;
- clusters whose diameter or rank exceeds the diagonal cutoff;
- the signed sum over all supports;
- arbitrary Vandermonde patterns with constants growing too rapidly; or
- the many-seed fixed-prefix transfer.

Accordingly, the free multiplier removes every fixed-rank bounded-cluster
counterexample to the *specific canonical-frequency placement*, but it does
not restore the refuted uniform termwise theorem and does not prove an upper
bound for Erdos 451.  Phase and `closes=[]` remain unchanged.
