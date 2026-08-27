# M10 round 3: full-system Fejer spectral ledger and method no-goes

Date: 2026-08-27

Status: **proved exact spectral identity, a genuine exceptional-prime
counterexample to the direct majorant, and scoped no-goes for standard
entropy/L2/larger-sieve/conditioning estimates.**  No 451 upper bound is
claimed.

## 1. Probability normalization

Retain the reconstruction-safe widths

\[
 b_i=d_i/2,qquad
 \beta_i(a)=b_i^{-1}(1-|a|/b_i)_+,qquad
 Z_i=\sum_{a\in\mathbb Z}\beta_i(a).                       \tag{1}
\]

Thus `Z_i=1` for even `d_i`, while
`Z_i=1+d_i^(-2)` for odd `d_i`.  Put `Z=product_i Z_i` and let
`mu_i(a)=beta_i(a)/Z_i`.  The CRT map from the box `|a_i|<b_i` to
`Z/PZ` is injective; push the product probability `product_i mu_i` forward
and call it `mu(H)`.  The exact full-system bridge is

\[
 {S\over Z}={P\over h}
       \sum_{|H|_P<h}\left(1-{|H|_P\over h}\right)\mu(H).   \tag{2}
\]

When offset one is absent, distinctness of the remaining odd offsets gives

\[
                  1\le Z<\exp(\pi^2/8-1)<1.264.            \tag{3}
\]

## 2. Exact positive spectral identity

Let

\[
 \varphi_i(r)=\sum_a\mu_i(a)e_{p_i}(ar)
              ={U_i(r)\over U_i(0)}.                        \tag{4}
\]

The last expression is a periodization of sinc squares, so
`0<=varphi_i(r)<=1`.  For
`c_i=(P/p_i)^(-1) (mod p_i)`, the global characteristic function is

\[
             \widehat\mu(ell)=\prod_i\varphi_i(c_iell)\ge0. \tag{5}
\]

The triangular interval weight in (2) is the autocorrelation of an
`h`-term interval.  Finite Fourier inversion therefore proves exactly

\[
 {S\over Z}=1+sum_{0\ne\ell\bmod P}K_h(\ell)
                         \prod_i\varphi_i(c_i\ell),          \tag{6}
\]

where

\[
 K_h(\ell)={1\over h^2}
       \left|\sum_{t=0}^{h-1}e_P(\ell t)\right|^2\ge0.      \tag{7}
\]

This has two consequences.

First, if `d_i=1` occurs then `Z_i=2`, whence (6) gives

\[
                              S\ge Z\ge2.                   \tag{8}
\]

Thus the direct reconstruction-safe carry-forgetting bridge `S<2` is
rigorously impossible for every `k` with `k+1` prime.  Enlarging the width
to `(d_i+1)/2` is not a repair: its integer-endpoint located intervals can
intersect in `(N,N+1)` without an integer common time.  A uniform proof must
retain the exact carry of this prime or build a new discrete/dilate-aware
bridge after imposing `s=0 (mod k+1)`.

Second, when offset one is absent, there is no signed Fourier cancellation
available inside this majorant.  The precise remaining theorem is the
positive phase-dispersion estimate

\[
 \sum_{\ell\ne0}K_h(\ell)\prod_i\varphi_i(c_i\ell)
                              <{2\over Z}-1.                 \tag{9}
\]

The right side is a fixed positive constant by (3).  Equation (9) retains
the full joint inverse-cofactor phases; no marginal estimate can replace
their product automatically.

## 3. Renyi/entropy-only ledger

Let `r>1` and `B_*=product_i b_i`.  Since `beta_i<=1/b_i`, has at most
`2b_i+1<=3b_i` nonzero integer values when `d_i>=2`, and `Z_i>=1`,

\[
 \sum_H\mu(H)^r=\prod_i\sum_a\mu_i(a)^r
                       \le3^mB_*^{1-r}.                    \tag{10}
\]

Holder applied to (2) gives the available bound

\[
 S\le Z\,2^{1-1/r}3^{m/r}{P\over B_*}
                                  \left({B_*\over h}\right)^{1/r}. \tag{11}
\]

At `h=k^BC^mP/D`, one has

\[
 \log(B_*/h)=\log P-o(k)=\Theta(k),qquad
 {P\over B_*}=2^m{P\over D}\ge2^m.                         \tag{12}
\]

Therefore (11) exceeds two for every choice of `r`; for each fixed `r` it
is `exp(Theta(k/r))`, and its `r` tending to infinity limit still retains
the location-blind min-entropy factor `P/B_*>=2^m`.  This rigorously kills
the method

```text
forget CRT locations, retain only product support/Renyi data, and apply
Holder to the short interval.
```

It is not a lower bound for the actual small-interval probability.

The case `r=2` is the usual separated L2/large-sieve ledger.  It leaves

\[
                        \exp((1/2+o(1))\log P)=\exp(Theta(k)) \tag{13}
\]

at the density-scale `h`; no `exp(o(k))` multiplier can repay this square
root of the full conductor.

## 4. Support-only larger sieve is below level

The support of the `i`-th local factor occupies at most `d_i` residue
classes modulo `p_i`.  Gallagher's larger-sieve denominator would contain

\[
              \sum_i{\log p_i\over d_i}-\log(2h).           \tag{14}
\]

Distinct offsets give the unconditional upper bound

\[
 \sum_i{\log p_i\over d_i}
       \le\log(2k)\sum_{d\le k}{1\over d}=O((\log k)^2).    \tag{15}
\]

For fixed `C>1`, the target has
`log h>=m log C` and `m=(1+o(1))k/log k`, so (14) is negative for large
`k`.  The standard support-only larger sieve therefore supplies no bound at
the required level.  Weighted local shapes or joint phases would be new
information, not a refinement of that denominator.

## 5. Sequential complete-period conditioning

Let `J` be a subset of coordinates, `P_J=product_(i in J)p_i`, and let
`B_(J^c)=product_(i notin J)b_i`.  Complete-period summation of the selected
local factors and supremum disposal of the rest give exactly

\[
 S\le Z_J\left\{{2P\over P_JB_{J^c}}
                         +{P\over hB_{J^c}}\right\}.        \tag{16}
\]

If `J` omits a coordinate, the first term contains
`p_i/b_i=2p_i/d_i>2`; if `J` contains every coordinate, the second term is
`P/h=exp(Theta(k))`.  Hence no subset choice makes this positive endpoint
ledger less than two.  Carry-sensitive cancellation in the one incomplete
period is indispensable.

## 6. Relation to M05 Theorem 4.1

The `6^q/delta_B` result in M05 Theorem 4.1 is an anchored homogeneous
difference/successor statement for one dyadic block.  It neither covers an
arbitrary torus translate nor bounds the positive spectral sum (9).
Consequently the existence of the full-system Fejer bridge does not upgrade
that theorem to a maximum-gap estimate.  Applying Theorem 4.1 separately
to blocks still leaves the already-open block-shift merge, and replacing it
by (9) requires genuinely new joint phase dispersion.  No `6^m` closure of
the full 451 problem follows.

## 7. Frozen survivor

For systems without offset one, the sole surviving majorant interface is
(9), preferably split dyadically using

\[
 K_h(\ell)\ll\min\{1,(P/(h|\ell|_P))^2\}.                  \tag{17}
\]

It demands a conductor-wide average theorem for the correlated phases
`c_i=(-1)^(m-1)F'(d_i)^(-1)`, not another entropy norm.  For systems with
offset one, even that majorant is killed by (8); the next action must first
preserve that coordinate's exact carry or replace continuous common-time
reconstruction by a proved discrete dilated analogue.
