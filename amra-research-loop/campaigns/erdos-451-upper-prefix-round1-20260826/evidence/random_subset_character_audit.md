# Random old-prime subsets: multiplicative characters and the missing transfer

This is a theoretical audit inside `survivor_deepening`.  No unproved
character-sum statement is used as an input to the campaign, and no phase gate
is advanced.

## 1. Exact Fourier transform of a random subset product

Fix an external prime `p` and a finite candidate set `C` of primes different
from `p`.  Reduce every `q in C` in `F_p^*`.  For independent Bernoulli bits
`epsilon_q`, define

\[
 Q_C=\prod_{q\in C}q^{\epsilon_q}\pmod p.
\]

If `mu` is its probability distribution and `chi` is a multiplicative
character modulo `p`, then

> **Bernoulli subset-product Fourier identity.**
> \[
> \widehat\mu(\chi):=\mathbb E\chi(Q_C)
>   =\prod_{q\in C}\frac{1+\chi(q)}2.                  \tag{1}
> \]

**Proof.**  Independence gives

\[
 \mathbb E\prod_q\chi(q)^{\epsilon_q}
 =\prod_q\mathbb E\chi(q)^{\epsilon_q}
 =\prod_q(1+\chi(q))/2.\quad\square
\]

This identity immediately exposes a support obstruction.  If a nontrivial
`chi` is one on every candidate prime, then the corresponding coefficient is
exactly one and the distribution cannot be close to uniform.  Equivalently,
one must at least prove that the candidate residues are not trapped in a
proper multiplicative subgroup of `F_p^*`.

There is also an exact sufficient criterion.  Put `M=|C|`.  If, for every
nonprincipal character,

\[
 \operatorname {Re}\sum_{q\in C}\chi(q)\le(1-\eta)M,  \tag{2}
\]

then

\[
 |\widehat\mu(\chi)|^2
 =\prod_q\frac{1+\operatorname {Re}\chi(q)}2
 \le \exp(-\eta M/2).                                 \tag{3}
\]

Indeed `log x<=x-1` applied to each factor proves (3).  Fourier inversion,
Parseval, and Cauchy's inequality therefore give

\[
 \|\mu-u_{\mathbb F_p^*}\|_{TV}
 \le\frac12\sqrt{p-2}\,\exp(-\eta M/4).               \tag{4}
\]

Thus a constant one-sided character gap would make a Bernoulli subset product
exponentially close to uniform; the factor `p` is harmless because
`M asymptotic k/log k`.

## 2. Fixed-size predecessor subsets in a random order

A random merge order does not give independent Bernoulli predecessors.
Conditioned on `p` having exactly `r` predecessors among `C`, that predecessor
set is a uniform `r`-subset.  Its exact Fourier coefficient is

\[
 \widehat\mu_r(\chi)
 =\frac{e_r((\chi(q))_{q\in C})}{{M\choose r}},         \tag{5}
\]

where `e_r` is the elementary symmetric polynomial.  Without conditioning,
the rank `r` is uniform on `{0,...,M}` and

\[
 \widehat\mu_{order}(\chi)
 =\frac1{M+1}\sum_{r=0}^{M}
   \frac{e_r((\chi(q))_{q\in C})}{{M\choose r}}.       \tag{6}
\]

Formula (6) also shows an unavoidable edge effect: with probability
`1/(M+1)`, `p` is first and the predecessor product is exactly one.  One can
only seek strong mixing for ranks bounded away from `0` and `M`, while paying
for the few edge ranks separately.

For completeness, a strong character gap would also control every middle
rank.  Assume the stronger uniform estimate

\[
 \left|\sum_{q\in C}\chi(q)\right|\le(1-\eta)M.        \tag{7}
\]

For `r=theta M`, `tau<=theta<=1-tau`, Cauchy's coefficient
formula on `|z|=rho=theta/(1-theta)` and concavity of `log` give

\[
 |e_r((\chi(q)))|
 \le \rho^{-r}(1+\rho)^M
      \exp(-\eta\theta(1-\theta)M).                   \tag{8}
\]

Stirling's formula gives, uniformly in this middle range,

\[
 {M\choose r}\gg_\tau
 M^{-1/2}\rho^{-r}(1+\rho)^M.
\]

Consequently

\[
 |\widehat\mu_r(\chi)|
 \ll_\tau \sqrt M\,
   \exp(-\eta\theta(1-\theta)M).                      \tag{9}
\]

Here the absolute value in (7) is needed because the Cauchy contour rotates
all `chi(q)` by a common phase.

## 3. What character-sum input would be needed

For the 451 system the relevant sum is

\[
 S_{p,k}(\chi)=
 \sum_{\substack{k<q<2k\\q\text{ prime},\ q\ne p}}
 \chi(q),\qquad p\in(k,2k).                            \tag{10}
\]

One needs (2), or for the fixed-rank argument (7), uniformly for every
external prime `p` and every nonprincipal character modulo `p`.  The modulus,
the interval length, and the main scale are all comparable:
`p asymptotic k`, while the number of summands is only `M=Theta(k/log k)`.

The standard inputs available without an additional theorem do not certify
this uniform statement:

- Pólya--Vinogradov and the elementary Burgess bound concern character sums
  over all integers.  Removing the composite terms and obtaining the needed
  bound for primes requires a von Mangoldt/prime character-sum theorem.
- Siegel--Walfisz is uniform only for moduli far smaller than `k`, whereas
  here `p asymptotic k`.
- Bombieri--Vinogradov averages over moduli and does not give the required
  assertion for every moving external prime and every character.
- A real exceptional character can obstruct a uniform *absolute* estimate
  such as (7).  Its negative bias may help the one-sided Bernoulli estimate
  (2), but that requires a separate signed argument and does not establish
  the fixed-size formula (9).

Under GRH for the Dirichlet `L`-functions modulo these primes, the standard
explicit-formula estimate would give, safely,

\[
 S_{p,k}(\chi)=O(\sqrt{k}\log^2 k)=o(k/\log k),         \tag{11}
\]

uniformly in `p` and `chi`.  Then (3)--(4), and away from edge ranks
(8)--(9), would give exponential multiplicative mixing.  This is a useful
conditional diagnostic, but GRH is not part of the closure contract.  No
uniform unconditional prime-character theorem with the exact quantifiers
needed for (10) has been proved or imported in this campaign, so (2) and (7)
remain dependency gaps rather than lemmas.

## 4. An unconditional bad-phase counting lemma

There is a fully elementary finite-support statement.  It shows exactly how
far divisor counting alone can go.

> **Small rational phase counting lemma.**  Let
> \[
> Q=\prod_{i=1}^j q_i,\qquad j\ge1,\qquad k<q_i<2k,
> \]
> and let `R` be a set of primes in `(k,2k)` not dividing `Q`.  Suppose
> `1<=H<k` and `1<=A<k`.  The number of `p in R` for which
> \[
> hQ\equiv a\pmod p                                    \tag{12}
> \]
> for some `1<=h<=H` and some nonzero integer `a` with `|a|<=A` is at most
> \[
> 2HA\,
> \frac{j\log(2k)+\log(2H)}{\log k}.                  \tag{13}
> \]

**Proof.**  For a fixed pair `(h,a)`, every counted prime divides the nonzero
integer `hQ-a`.  It is nonzero because `hQ>=Q>k>A`.  A nonzero integer `N`
has at most `log|N|/log k` distinct prime divisors larger than `k`.  Moreover

\[
 |hQ-a|<2hQ\le2H(2k)^j.
\]

There are `2HA` signed pairs `(h,a)`.  The union bound proves (13). `square`

Hence a next prime avoiding every approximation (12) is guaranteed only when

\[
 |R|>2HA\,
 \frac{j\log(2k)+\log(2H)}{\log k}.                   \tag{14}

This is too weak for a full ordering.  With `M=Theta(k/log k)` total primes,
the right side is of order `HA*j`.  Taking `H=A=L` can control at most the
first `j=O(M/L^2)` merge stages.  When `j` is a positive proportion of `M`,
even `H=A=1` is not guaranteed.  An Erdos--Turan bound using only
`1<=h<=H` and centered residues larger than `A` is in any event of scale
roughly

\[
 p/H+(p/A)\log H,                                      \tag{15}
\]

so polylogarithmic `H,A` leave a near-linear discrepancy and apply to only an
`o(M)` initial segment.  Divisor counting therefore cannot deliver the
middle-rank mixing required by (9).

## 5. Why even uniform phase does not close the short-prefix merge

Suppose, conditionally, that a random predecessor product `Q mod p` were
perfectly uniform and that its rational-rotation discrepancy were
polylogarithmic.  This controls the single orbit

\[
 b,\ b+Q,\ b+2Q,\ldots                                  \tag{16}
\]

of one old seed.  In the integers, consecutive terms of (16) are still
separated by the old period `Q`.  If the target prefix length `H` is smaller
than `Q`, it contains at most one point of this orbit.  Good distribution
modulo `p` has not created a second short-prefix seed.

More intrinsically, randomizing the merge order changes the proof parameter
`Q` but not the final CRT box or the distinguished initial interval.  The
needed distribution is that of

\[
 \{n\bmod p:n\in B_S\cap J\},                           \tag{17}
\]

where `B_S` is the old solution set and `J` is the fixed short prefix.  The
character product (1) contains no information about the locations of these
distinct old representatives.  The exact aligned P1--P3 counterexamples in
`density_sensitive_block_merge.md` already show that a well-defined block
phase can coexist with coherent short-window multiplicities.

Thus the random-subset route has two independent conditional bridges:

1. a uniform prime-character mixing theorem with the quantifiers in (10), or
   another unconditional proof of a comparable random-order bound; and
2. a many-seed transfer theorem from product-phase mixing to the fixed set
   (17), without first enumerating a full old period.

Even GRH would address only the first bridge.  The second is the original
position-sensitive block-merge difficulty in a sharper form.  The route
therefore remains conditional and does not change `closes=[]`.
