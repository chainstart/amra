# M05 round 2: direct audit of the special zonotope linear gate

Date: 2026-08-26

Status: **the generic gate and single-split gate are killed; a proved
low-support Fourier estimate leaves one high-support boundary-counting
interface.**  This note does not assert a new representation of Erdős 451.
It directly audits whether the
coordinate-plus-one-diagonal zonotope from M05 admits a linear, rather than
`q^(3/2)`, affine covering theorem.

## 1. The located zonotope

For one dyadic block, write `p_i=k+d_i`,
`Delta<=d_i<2Delta`, and

\[
 b=\left\lfloor{\Delta-1\over2}\right\rfloor+\tfrac12,
 \qquad v=(1/p_i)_{i=1}^q.                                  \tag{1}
\]

After centering the positive time interval, the relevant symmetric body is

\[
 K_h=\left\{tv+(u_i/p_i)_i:|t|\le h,\ |u_i|\le b\right\}.    \tag{2}
\]

Its support function on the dual integer lattice is exactly

\[
 h_{K_h}(z)=h\left|\sum_i{z_i\over p_i}\right|
                  +\sum_i b{|z_i|\over p_i}=R_h(z).          \tag{3}
\]

The actual gap starts give only the diagonal orbit `xv mod Z^q`, not every
torus translate.  Covering every translate of (2) is sufficient but
strictly stronger than the 451 maximum-gap statement.  This distinction is
kept below.

The unconditional John-ellipsoid/Euclidean-transference gate from
`m05_high_support_small_A_round2.md` requires

\[
                     \min_{z\ne0}R_h(z)>q^{3/2}/2.            \tag{4}
\]

The box-Dirichlet lemma in that note constructs `R_h(z)=O(Cq)` at
`h=k^B C^q delta_B^(-1)`.  Hence (4) is impossible for every fixed `C` and
large `q`.  The rest of this note asks whether the special generator matrix
in (2) admits a genuinely linear gate.

## 2. An exact positive Fourier closure criterion

There is a direct way to test the special body without invoking generic
flatness.  Split each of the `q+1` generating segments in (2) into `L>=2`
equal subsegments and convolve the uniform probability measures on those
subsegments.  The resulting continuous density `rho_L` is supported in
`K_h`.  Its periodization

\[
                  f_L(x)=\sum_{n\in\mathbb Z^q}\rho_L(n-x)   \tag{5}
\]

has mean one on the torus and Fourier coefficients

\[
 \widehat f_L(z)=
 \operatorname{sinc}\!\left({2\pi h\over L}
                    \sum_i{z_i\over p_i}\right)^L
 \prod_i\operatorname{sinc}\!\left({2\pi b z_i\over Lp_i}\right)^L,
                                                                    \tag{6}
\]

where `sinc(u)=sin(u)/u`.  For `L>=2` the series is absolutely convergent.
Consequently the following is an exact sufficient lemma:

> **Box-spline covering criterion.**  If
> \[
> \sum_{0\ne z\in\mathbb Z^q}
> \left|\operatorname{sinc}\!\left({2\pi h\over L}
>                   \sum_i{z_i\over p_i}\right)\right|^L
> \prod_i\left|\operatorname{sinc}\!\left(
>                   {2\pi b z_i\over Lp_i}\right)\right|^L<1,       \tag{7}
> \]
> then `f_L(x)>0` for every `x`, and every translate of `K_h` contains an
> integer point.

This criterion is stronger than needed because it covers the full torus,
but it is a genuine primal covering implication.  It does not separate a
Fourier coefficient from its reciprocal-sum phase.

Dropping the diagonal factor in (7) is fatal.  For each coordinate, all
integers `|z_i|<=c_L p_i/b` have the local sinc factor bounded below by a
positive constant depending only on `L`.  Therefore the separated
coordinate product has mass at least

\[
               c_L^q\prod_i{p_i\over b}
               =c_L^q\delta_B^{-1}\prod_i{d_i\over b}.       \tag{8}
\]

Thus the diagonal reciprocal-sum phase must cancel the full density entropy;
coordinate smoothing alone merely returns it.

## 3. The exact near-zero shell count

The counting problem underneath (7) can be stated without Fourier
terminology.  For positive integers `M_i` and `eta>0`, put

\[
 N(M,\eta)=\#\left\{z\in\mathbb Z^q:
 |z_i|\le M_i,\ \left|\sum_i{z_i\over p_i}\right|\le\eta
 \right\}.                                                     \tag{9}
\]

Fixing the first `q-1` coordinates leaves an interval of length
`2p_q eta` for the integer `z_q`.  Hence the strongest bound obtained from
one unrestricted slicing is the exact elementary inequality

\[
 N(M,\eta)
 \le \prod_{i<q}(2M_i+1)\,(2p_q\eta+1).                     \tag{10}
\]

At the natural coordinate scale `M_i asymp k/Delta` and the proposed time
scale

\[
                    h\asymp C^q\delta_B^{-1},                \tag{11}
\]

the volume part of (10), with `eta=1/h`, is

\[
 \prod_{i<q}M_i\,{p_q\over h}
              \ll {\Delta\over C^q}.                         \tag{12}
\]

This is excellent.  The discrete endpoint `+1`, however, contributes

\[
                    \prod_{i<q}(2M_i+1)
       =\exp\!\left(\Theta\left(q\log{k\over\Delta}\right)\right), \tag{13}
\]

which is precisely the entropy that (11) was meant to pay.  Averaging (10)
over the choice of the last coordinate does not remove (13); every slice has
the same possible single-integer endpoint.

Therefore a proof of (7) needs an arithmetic estimate saying that this
possible integer is absent on almost all slices.  In the exact notation of
the other round-2 note, that integer is governed by

\[
 F'(d_i)z_i\equiv(-1)^{q-1}A\pmod {p_i},
 \qquad A=P\sum_i{z_i\over p_i}.                              \tag{14}
\]

So the boundary term is not a generic lattice-point error.  It is exactly
the weighted centered inverse-derivative phase left in alternatives (27)--
(28) there.

## 4. Why the Dirichlet vectors are not primal gaps

Lemma 4.1 of the high-support note is a one-way method obstruction.  It
constructs a nonzero dual vector with small `R_h(z)`, so any sufficient
criterion demanding a larger minimum dual width fails.  It does **not**
choose a start `x`, does not show that `xv+K_h` is lattice-free, and does not
produce a long interval without an allowed residue.

This logical direction cannot be reversed: flatness/transference says that
a lattice-free translate has a short dual certificate; the existence of a
short dual vector alone supplies no translate or separation phase.  In (7)
the same point is visible analytically: one moderately large Fourier
coefficient does not force the nonnegative periodized density (5) to vanish
at any point.  Any use of Lemma 4.1 as a primal max-gap witness would therefore
be invalid.

## 5. A scoped no-go for uniform triangular slicing

The `+1` in (10) is not a cosmetic choice of a sharp cutoff.  Let

\[
 \Psi_L(y)=\left|\operatorname{sinc}(2\pi y/L)\right|^L.
\]

For `L>=2`, comparison with the decreasing tails gives the uniform sampling
bound

\[
             \sum_{n\in\mathbb Z}\Psi_L(Y(n+\theta))
                  \le 1+{C_L\over Y}\qquad(Y>0),             \tag{15}
\]

with an absolute `C_L` depending only on `L`.  The term one is necessary
when `theta` is an integer.  Apply (15) to the `z_q` sum in (7), after
discarding its coordinate sinc factor.  Applying the same estimate to each
remaining coordinate gives only

\[
 1+\sum_{z\ne0}|\widehat f_L(z)|
 \le\left(1+C_L{p_q\over h}\right)
       \prod_{i<q}\left(1+C_L{p_i\over b}\right).             \tag{16}
\]

The `p_q/h` part has the correct volume saving.  The product of the unit
endpoint terms is

\[
               \exp\!\left(\Theta\left(q\log{k\over\Delta}\right)\right), \tag{17}
\]

and is independent of `h`.  Therefore the precisely scoped method

```text
take absolute values in (7), sum one reciprocal coordinate at a time,
and use a uniform translated one-dimensional sampling inequality
```

cannot prove (7), regardless of how the subexponential time budget is
enlarged.  This no-go does not apply to a joint estimate that proves the
nearest integer is absent for most outer slices.

Exact `A`-shell counting does not repair the uniform argument.  When
`2M_i<p_i`, the map

\[
                  z\longmapsto A=P\sum_i{z_i\over p_i}        \tag{18}
\]

is injective on the coefficient box: equality for two vectors would give a
zero reciprocal sum, and reduction modulo each active prime forces equality
coordinate by coordinate.  Thus

\[
                    N(M,\eta)\le2P\eta+1.                    \tag{19}
\]

At `eta=1/h` and (11), this is of order
`product_i(d_i)/C^q`, while (10) gives the competing boundary
`(k/Delta)^(q-1)`.  Taking the better of these two size-only bounds still
does not say that the unique endpoint in a given slice is absent.  The
missing input remains the distribution of the residues in (14), not the
cardinality of their possible `A` values.

There is a genuinely joint, but still unsuccessful, standard estimate.
For `X<P/2`, define

\[
 \mathscr A(X,M)=\left\{A\in[-X,X]\cap\mathbb Z:
 \left|\left\langle(-1)^{q-1}A/F'(d_i)\right\rangle_{p_i}\right|
       \le M\quad\hbox{for every }i\right\}.                  \tag{LS1}
\]

Here the angle brackets mean the centered representative.  By (14), this is
exactly the set of `A`-phases whose centered coefficient vector lies in the
uniform box.  Modulo `p_i`, the set (LS1) occupies at most
`nu_i=2M+1` residue classes.

The elementary larger-sieve inequality says that a set of `N` integers in
an interval of length `Y` occupying at most `nu_i` classes modulo `p_i`
satisfies

\[
 N\left(\sum_i{\log p_i\over\nu_i}-\log Y\right)
       \le\sum_i\log p_i-\log Y,                              \tag{LS2}
\]

when the coefficient on the left is positive.  For completeness, sum
`log p_i` over ordered congruent pairs.  Cauchy gives at least
`N^2/nu_i-N` such pairs modulo `p_i`, while for each distinct pair the sum
of `log p_i` over primes dividing its difference is at most `log Y`.
Rearrangement is (LS2).

At the required `X=P/h`, one has

\[
 \begin{split}
 \sum_i{\log p_i\over2M+1}-\log(2P/h)
   &=\log h-\left(1-{1\over2M+1}\right)\log P+O(1)\\
   &=-\Theta(k)                                                \tag{LS3}
 \end{split}
\]

for every `M>=1`, because `log h=o(k)` and `log P=(1+o(1))k`.
Thus the joint pair-collision larger sieve has a negative denominator and
gives no bound at all.  This is stronger than saying that one-coordinate
slicing is wasteful, but it kills only the explicit pair-collision inequality
(LS2), not every conceivable second-moment argument.  A surviving `A`-shell
estimate must use information beyond the cardinalities `nu_i`, plausibly
higher-order correlations among the twisted classes in (LS1).

## 6. An actual gap is phase-certified by one short vector

The one-way warning in Section 4 does not mean short vectors are irrelevant.
An exact actual-prime example shows that the **additional start phase** can
turn one into a genuine gap certificate.

For `k=168`, take the dyadic block

\[
 (p_i)=(191,193,197,199),\qquad(d_i)=(23,25,29,31).           \tag{20}
\]

Exact CRT enumeration gives period `1445140189`, allowed cardinality
`516925`, and maximum cyclic gap

\[
                              G=4327275.                       \tag{21}
\]

The full-moment vector

\[
                  z=(-1,2,-2,1),\qquad A=-96                 \tag{22}
\]

is the primitive inverse-Vandermonde vector.  With `w=7`, `b=15/2`, and
the located time half-width `h=G/2-w=4327261/2`, its exact support is

\[
                         R_h(z)={541272603\over1445140189}.   \tag{23}
\]

For one center of the sign-reflected actual 451 gap, the distance of the
dual center phase to the nearest integer is

\[
                    {719009335\over1445140189}>R_h(z).        \tag{24}
\]

Hence the interval of dual values of the translated zonotope misses every
integer hyperplane, which by itself certifies that translate is lattice-free.
This proves a finite structural fact, not an asymptotic gap family.  It also
shows exactly what Lemma 4.1 lacks: the latter supplies `z` but no center
whose phase satisfies (24).

The guarded verifier is
`work/m10_round1/actual_gap_dual_certificate.py`.  Authoritative unit
`openmath-task-20260827-000337-344292.scope` exited zero in `0.34s`, with
maximum RSS `73876 KiB` and zero swap.

## 7. Single-split transference is false even at rank two

The rank-four example in Section 6 might suggest a stronger theorem: every
lattice-free translate of (2) is certified by one integral hyperplane,
namely some `z` with

\[
                 \|\langle z,xv\rangle\|_{\mathbb R/\mathbb Z}>R_h(z).
                                                                    \tag{25}
\]

This is false for an actual 451 block, and the counterexample is exhaustive
rather than a bounded search artifact.

Take

\[
                 k=15,\qquad(p_1,p_2)=(23,29),
 \qquad(d_1,d_2)=(8,14).                                    \tag{26}
\]

The exact maximum gap has length `62`, between positive-model residues `352`
and `414`.  Reflect to the actual 451 sign convention, put `w=3`, `b=7/2`,
and take the **closed** located body with `h=27`; the extra unit beyond
`G/2-w` is removed, so this body lies strictly inside the gap.  For
`z=(-1,1)`,

\[
 A=-6,\qquad R_h(z)={344\over667},\qquad
 \|\langle z,xv\rangle\|={297\over667}.                     \tag{27}
\]

This is the best possible margin among all dual vectors.  Indeed enumerate
`|z_i|<=5`.  Outside that box, one coordinate has absolute value at least
six, so its transverse contribution alone is greater than

\[
                        {b\cdot6\over2k}={7\over10}>{1\over2}, \tag{28}
\]

while every centered phase distance is at most `1/2`.  Inside the box, exact
enumeration of all `120` nonzero vectors finds (27) as the minimum support
and the largest phase-minus-support margin, namely `-47/667<0`.  Thus no
vector satisfies (25), although the translate is lattice-free.

The guarded scan checked `126` actual-prime blocks under similarly exhaustive
coefficient cutoffs and found `63` split failures.  The first counterexample
above is already decisive.  Script:
`work/m10_round1/special_zonotope_split_search.py`; authoritative guard unit
`openmath-task-20260827-002141-349572.scope`, exit zero, `15.24s`, maximum
RSS `48040 KiB`, zero swap.

This kills only **single-hyperplane** or split transference.  A linear
flatness theorem with a multi-facet certificate, or the box-spline aggregate
(7), remains possible.  Quantitatively, (27) also shows that any universal
criterion of the form `min R_h(z)>c q implies covering` must have

\[
                         c\ge {172\over667}=0.257871\ldots,    \tag{29}
\]

because this lattice-free rank-two body has `min R_h=344/667`.  This is a
lower bound on the possible linear constant, not a refutation of all fixed
constants.

Among the `63` failures, the largest observed value of `min R_h/q` was the
nearby rank-two block `k=39`, `(p_1,p_2)=(47,53)`, where

\[
                   \min R_h/q={646\over2491}
                   =0.2593336009\ldots .                    \tag{30}
\]

This slightly strengthens the finite necessary lower bound on a universal
linear constant, but it is still only finite evidence and is not promoted to
an asymptotic obstruction.

## 8. Result of the direct proof attempt

The following possibilities are now rigorously separated.

1. Generic John/Euclidean flatness is insufficient by the proven
   `O(Cq)` dual vectors.
2. Coordinate-separated smoothing is insufficient by the density lower
   ledger (8).
3. One-coordinate lattice slicing is insufficient by the endpoint term
   (13).
4. A special linear theorem can still survive if it proves either the
   coupled Fourier sum (7) or a weighted form of (9) in which the endpoint
   occupancy from (14) has `C^q` cancellation.
5. Even at rank two, lattice-free translates need not admit a single split
   certificate, by (26)--(28); any phase-aware theorem must aggregate more
   than one dual direction.

No actual-prime family was found for which the maximum gap disproves a
linear special-zonotope threshold.  Conversely, no theorem removing (13) is
proved.  The unique next inequality is a phase-aware boundary occupancy
bound, not another generic transference estimate.

## 9. A composable low-residue-support Fourier theorem

There is one unconditional gain inside (7).  It is important to measure the
support after reduction modulo the local prime:

\[
 \sigma(z)=\#\{i:p_i\nmid z_i\}.                             \tag{31}
\]

This differs from the ordinary support because a nonzero multiple of `p_i`
has zero local residue.  Put

\[
 \psi_i(n)=\left|\operatorname{sinc}
                \left({2\pi b n\over Lp_i}\right)\right|^L,
 \qquad L\ge2\ \hbox{a fixed integer}.                       \tag{32}
\]

Integral comparison with `min(1,C_L/|x|)^L` gives

\[
 \sum_{p_i\nmid n}\psi_i(n)\le C_L{p_i\over b},\qquad
 \sum_{0\ne t\in\mathbb Z}\psi_i(p_it)\le D_Lb^{-L}.       \tag{33}
\]

Here and below `C_L,D_L` depend only on the fixed smoothing order `L`.

> **Lemma 9.1 (absolute low-support ledger).**  Let
> `alpha(z)=sum_i z_i/p_i`.  For every integer `0<=r<=q`, the contribution
> to (7) from `alpha(z) ne 0` and `sigma(z)<=r` is at most
> \[
> e^{D_Lq/b^L}
> \sum_{s=0}^r {q\choose s}
>       \left(C_L{k\over b}\right)^s
>       \min\left\{1,
>       \left({C_L(2k)^s\over h}\right)^L\right\}.           \tag{34}
> \]
> The contribution from the nonzero vectors with `alpha(z)=0` is at most
> \[
>                  e^{D_Lq/b^L}-1.                            \tag{35}
> \]

Proof.  Fix the reduced support `S`.  The product of all coordinate weights
over vectors with this reduced support is, by (33), at most

\[
        (C_Lk/b)^{|S|}(1+D_Lb^{-L})^{q-|S|}.                 \tag{36}
\]

If `alpha(z) ne 0`, reduce its rational numerator modulo every prime in
`S`.  Its reduced denominator divides `product_(i in S)p_i`, so

\[
                         |\alpha(z)|\ge(2k)^{-|S|}.           \tag{37}
\]

The diagonal factor in (6) is therefore bounded by the last factor in
(34), and summing (36) over the choices of `S` proves (34).

If `alpha(z)=0`, reduction modulo each `p_i` shows that `z_i=p_it_i` for all
`i`, and then `sum_i t_i=0`.  Choose `t_1,...,t_(q-1)` freely and discard
the final coordinate weight.  Equation (33) bounds the resulting sum,
including the zero vector, by `(1+D_Lb^(-L))^(q-1)`.  Removing the zero
vector proves (35).

This aggregate estimate has the correct exponent.  Suppose `B>0` and
`C>1` are fixed, `h` tends to infinity, and

\[
 \Delta>{k\over(\log k)^3},\qquad
 h\ge k^B C^q\delta_B^{-1},                                  \tag{38}
\]

where `delta_B=product_i(d_i/p_i)`, and fix `0<epsilon<1`.  Let

\[
 r_\epsilon=\min\left\{q,\left\lfloor(1-\epsilon)
                 {\log h\over\log(2k)}\right\rfloor\right\}. \tag{39}
\]

For `s<=r_epsilon`, the diagonal factor in (34) is
`h^(-epsilon L+o(1))`.  Moreover `b asymp Delta`, while the factor preceding
it has logarithm at most

\[
 r_\epsilon\left[
   \log{eq\over\max(1,r_\epsilon)}+\log{C_Lk\over b}
                  \right]+O(q/b^L)
       =o(\log h).                                           \tag{40}
\]

For the last equality, `h>=C^q` gives
`q/max(1,r_epsilon)=O(log k)`, and
`k/b=O((log k)^3)`; hence the bracket is `O(log log k)`, whereas
`r_epsilon<=log h/log(2k)`.  Also `q<=Delta` and `L>=2` give
`q/b^L=o(1)`.  Consequently (34)--(35) yield

\[
 \sum_{\substack{z\ne0\\\sigma(z)\le r_\epsilon}}
                   |\widehat f_L(z)|=o(1).                   \tag{41}
\]

Thus sparse fixed-pattern resonances and all other reduced supports below
the transition (39) can be paid **in aggregate**, not one at a time.  This
is a genuine block lemma.  It neither covers the body nor controls the
remaining supports `sigma(z)>r_epsilon`.

## 10. Exact dyadic shell form of the remaining inequality

The high-support remainder can now be written without a hidden triangle
loss.  Put `P=product_i p_i` and

\[
                         A(z)=P\alpha(z)\in\mathbb Z.         \tag{42}
\]

Use coordinate shells `j_i>=0` at scale `p_i/b`: shell zero has
`|z_i|<=p_i/b`, while shell `j_i>=1` has
`2^(j_i-1)p_i/b<|z_i|<=2^j_i p_i/b`.  Use diagonal shells `t>=0` at scale
`P/h` in the same way.  Let `N_>(j,t)` count the vectors in these shells
with `sigma(z)>r_epsilon`.  Directly from (6), with `J=sum_i j_i`,

\[
 \sum_{\substack{z:\ \sigma(z)>r_\epsilon}}
       |\widehat f_L(z)|
 \le C_L^q\sum_{j_1,\ldots,j_q,t\ge0}
            2^{-L(J+t)}N_>(j,t).                             \tag{43}
\]

Equation (43), together with (41), is a sufficient quantitative interface:
it is enough to make its right side less than `1-o(1)`.  It retains both
the diagonal sinc and the exact coefficient shells.

The old endpoint loss survives precisely in `N_>`.  On every core shell
with `2^j p_i/b<p_i/2`, the map `z mapsto A(z)` is injective, and its image
obeys the simultaneous congruences

\[
             F'(d_i)z_i\equiv(-1)^{q-1}A\pmod {p_i}.         \tag{44}
\]

The volume prediction for `N_>(j,t)` has the saving `2^tP/h`, but slicing
one coordinate replaces that saving by the possible single endpoint on
each of `asymp 2^J product_(i<q)(p_i/b)` outer slices.  After multiplication
by `2^{-L(J+t)}` and summation, this is exactly the exponential product in
(16)--(17).  The larger-sieve denominator (LS3) is negative at the same
scale.  Therefore the combination

```text
dyadic coefficient boxes + exact A shells + either one-coordinate endpoint
counting or cardinality-only larger sieve
```

still cannot prove (43).  This is a scoped triangle/cardinality no-go, not a
no-go for a signed or higher-correlation estimate.  The remaining theorem is
now narrower than (7): prove weighted cancellation/repulsion for the
high-reduced-support solutions of the specific inverse-derivative system
(44).  Low support, zero diagonal phase, generic transference, and a
single-split certificate have all been removed rigorously.

## 11. A higher-order endpoint bound, and its exact deficit

The congruences (44) do give more than the pair-collision larger sieve.  The
following code bound uses simultaneous agreement of arbitrarily many local
coordinates.

> **Lemma 11.1 (CRT Singleton bound).**  Let `1/2<=X<P/2`, `M<p_i/2`, and let
> `mathscr A(X,M)` be the set in (LS1).  Put
> \[
>                  J=\left\lfloor{\log(2X)\over\log k}\right\rfloor.
>                                                                    \tag{45}
> \]
> If `J<q`, then
> \[
>                         |\mathscr A(X,M)|
>                              \le(2M+1)^{J+1}.               \tag{46}
> \]

Proof.  Associate to each `A` its unique centered word
`(z_1(A),...,z_q(A)) in [-M,M]^q` through (44).  If the words for distinct
`A,B` agree on a set `T`, then every `p_i`, `i in T`, divides `A-B`.
Therefore

\[
                         k^{|T|}<\prod_{i\in T}p_i
                              \le |A-B|\le2X.                 \tag{47}
\]

No two words can agree on any prescribed `J+1` coordinates.  Projection to
those coordinates is injective and has at most `(2M+1)^(J+1)` possible
values, proving (46).

For `0<X<1/2`, the interval `[-X,X]` contains only zero, so the corresponding
count is the trivial singleton and no logarithmic `J` is needed.

This is a genuine all-orders improvement over (LS2): it says that the local
words have Hamming distance at least `q-J`.  It is nevertheless too weak at
the target scale.  Take `X=P/h`, `M asymp k/Delta`, and (38), additionally
with `2<h<=2P`, `J<q`, and `q` tending to infinity.  These conditions hold
at the proposed scale in the intended unbounded-rank regime: there
`log h=O(log k+q log log k)=o(q log k)=o(log P)`.  Since
`log P=q log k+O(q)`,

\[
 q-J={\log h\over\log k}+O\left({q\over\log k}+1\right).     \tag{48}
\]

Hence (46) saves only about

\[
                  {\log h\over\log k}\log(2M+1)             \tag{49}
\]

from the original box entropy `q log(2M+1)`.  In the entire large-block
range `M=O((log k)^3)`, (49) is only an `O(log log k/log k)` fraction of
the required entropy.  In particular the upper bound in (46) remains

\[
                \exp((1-o(1))q\log(2M+1)),                  \tag{50}
\]

whereas the volume heuristic at `h=C^q delta_B^(-1)` is `C^{-q}`.

Thus even the higher-order method

```text
encode the endpoint by its local centered word; use only the fact that
too many coordinate agreements force product divisibility of A-B
```

does not bound the boundary term by `C^q`.  This does not kill a weighted
code estimate using the actual inverse-derivative symbols, or a signed
Fourier estimate.  It shows precisely that Hamming distance/divisibility
alone recovers only the already-paid low-support transition (39), not the
remaining density entropy.

## 12. Weighted Vandermonde determinant audit

One can try to use the actual multipliers `F'(d_i)`, rather than only word
agreements.  Take distinct endpoint phases `A_1,...,A_s` in
`mathscr A(X,M)` and write `z_i(u)=z_i(A_u)`.  With
`C_s=binom(s,2)`, set

\[
 V_A=\prod_{u<v}(A_v-A_u),\qquad
 V_i=\prod_{u<v}(z_i(v)-z_i(u)).                              \tag{51}
\]

Multiplying the pairwise versions of (44) gives the exact weighted
congruence

\[
        V_A\equiv(-1)^{(q-1)C_s}F'(d_i)^{C_s}V_i\pmod {p_i}. \tag{52}
\]

This is the natural determinant/resultant use of the inverse derivative.
It has two branches, and neither improves Lemma 11.1 without new phase
information.

First, use only divisibility.  If `E_i` is the number of pairs `u<v` with
`z_i(u)=z_i(v)`, then

\[
          \sum_iE_i\log p_i\le\log|V_A|le C_s\log(2X).      \tag{53}
\]

Since `z_i` has `nu=2M+1` possible values,

\[
                     E_i\ge{s^2\over2\nu}-{s\over2}.        \tag{54}
\]

Substitution of (54) into (53) is exactly the larger-sieve collision ledger
(LS2), with the same negative denominator (LS3).  If instead one uses the
fact that every projection to `J+1` coordinates is injective, one recovers
the Singleton bound (46).  Thus the determinant's divisibility branch gives
no entropy beyond Section 11.

Second, retain the nonzero local determinant in (52).  Although
`|V_i|<=(2M)^(C_s)`, the archimedean multiplier has the uniform bound only

\[
                       |F'(d_i)|^{C_s}le
                              \Delta^{(q-1)C_s}.              \tag{55}
\]

Already for `s=2`, (55) is much larger than `p_i` throughout an unbounded
rank block.  Consequently (52) does not force equality over the integers,
does not locate its centered residue, and gives no norm saving.  Replacing
`F'(d_i)` by its centered residue modulo `p_i` is precisely the phase input
that is currently missing; no uniform bound for those centered residues is
available.

The same obstruction appears in the one-point resultant polynomial

\[
             R_i(Y)=\prod_{m=-M}^{M}(Y-(-1)^{q-1}F'(d_i)m).  \tag{56}
\]

For every admitted `A`, `p_i` divides `R_i(A)`, but the elementary norm
bound

\[
          |R_i(A)|\le(|A|+M|F'(d_i)|)^{2M+1}                 \tag{57}
\]

is vastly larger than `p_i`; multiplying (57) over `i` is weaker still.

Therefore the first genuinely weighted determinant/resultant attempt has a
precise no-go: its divisibility part collapses to larger-sieve/Singleton
entropy, while its archimedean part pays the full inverse-derivative height
`Delta^(q-1)`.  This does **not** refute a theorem exploiting cancellation
among the centered residues `F'(d_i) mod p_i`.  It identifies that signed
centered-residue correlation, rather than an unweighted higher determinant,
as the sole surviving high-support input.
