# M05 round 3: high-support weighted A-shell audit

Date: 2026-08-27

Verdict: **CONDITIONAL on a new weighted exact-carry estimate.**  The exact
`A`-fibre identity and the finite carry lemma below pass.  Separated
Cauchy is exponentially too weak.  No finite counterexample to the desired
weighted average was found.  An arbitrary periodized `C_y(omega)` does not
identify it, while the special Fejer periodization below gives a valid
stronger one-sided bridge whose `S<2` estimate remains open.

Audit type: same-model adversarial audit of the residual high-reduced-support
interface in equations (43)--(44) of
`m05_special_zonotope_linear_gate.md`.  The author note is not modified.
Finite searches below are falsification diagnostics only.

## 1. Exact weakest positive A-average

Fix the smoothing order `L>=2`.  Write

```text
A(z)=sum_i z_i(P/p_i),
Phi_h(A)=|sinc(2 pi h A/(L P))|^L,
psi_i(n)=|sinc(2 pi b n/(L p_i))|^L,
w(z)=product_i psi_i(z_i).
```

For an integer `A`, define the exact high-support fibre mass

```text
W_>(A)=sum_{z: A(z)=A, sigma(z)>r_epsilon} w(z).             (R3.1)
```

Then the residual absolute Fourier mass is not merely bounded by, but equals

```text
H_>=sum_A Phi_h(A)W_>(A).                                   (R3.2)
```

Since the low-support contribution is `o(1)`, the weakest positive
A-averaged statement sufficient for the box-spline criterion is

```text
limsup H_> < 1.                                              (WA)
```

A fixed bound `H_><=1-eta` is a convenient robust version.  This is weaker
than separately bounding every A-shell and weaker than replacing the exact
diagonal sinc by the supremum on a dyadic shell.

On the centered core, put

```text
z_i(A)=centered[(-1)^(q-1) A/F'(d_i)] modulo p_i.            (R3.3)
```

Every actual vector in the core with numerator `A` has exactly these local
coordinates.  Thus a usable sufficient overcount is the weighted correlation
of `Phi_h(A)` with `product_i psi_i(z_i(A))`, retaining the actual simultaneous
inverse-derivative phases.  Counting only the number of admitted A values
discards precisely this weight.

## 2. Exact fibre-energy identity

There is a rigorous second-moment identity for (R3.1).  First omit the
support restriction and put

```text
W(A)=sum_{z:A(z)=A}w(z),
C_i(t)=sum_n psi_i(n)psi_i(n+p_i t).                         (R3.4)
```

Two coefficient vectors have the same exact numerator iff their difference
is `(p_i t_i)_i` with `sum_i t_i=0`.  Consequently

```text
sum_A W(A)^2
 = sum_{t_1+...+t_q=0} product_i C_i(t_i).                  (R3.5)
```

The same right side is an upper bound for `sum_A W_>(A)^2`.  This identity
uses exact equality of A, not congruence or a cardinality-only sieve.

For fixed `L`, polynomial-tail convolution gives

```text
C_i(t) <= C_L(p_i/b)(1+b|t|)^(-L).                          (R3.6)
```

Choosing `t_1,...,t_(q-1)` freely and discarding the last decay factor yields

```text
sum_A W_>(A)^2
 <= C_L^q product_i(p_i/b) exp(D_L q/b^L).                  (R3.7)
```

Meanwhile the one-dimensional sampling bound gives

```text
sum_A Phi_h(A)^2 <= 1+C_L P/h.                              (R3.8)
```

Cauchy applied to the exact weighted average therefore proves only

```text
H_> <= [(1+C_LP/h) C_L^q product_i(p_i/b)
                         exp(D_Lq/b^L)]^(1/2).               (R3.9)
```

At the nontrivial target scale
`h=k^B C^q P/product_i d_i` with `P/h>>1` and `b asymp d_i`, the logarithm
of (R3.9) is

```text
(1/2)log P+O(q+log k).                                      (R3.10)
```

For a block of rank `q=Theta(k/log k)`, this is `Theta(k)`.  Thus the exact
unweighted fibre second moment pays `exp(Theta(k))` and cannot prove (WA).
This is a scoped no-go for separated Cauchy after A-grouping, not for a
coefficient-weighted or signed correlation estimate.

## 3. Finite falsification questions

The guarded diagnostics test the following, without promoting samples to an
asymptotic law:

1. for actual 451 dyadic prime blocks, whether small nonzero A have
   anomalously many small centered values (R3.3), or joint sinc weight far
   above its full-period product mean;
2. the same question for explicitly labelled structured offset families;
3. whether the centered geometric expansion at `c=3 Delta/2` admits exact
   carry cancellation before many centered moments vanish.

The exact results and their scope are recorded below after guarded replay.

## 4. Guarded finite results (falsifiers, not asymptotics)

The replay used fixed `L=2`, `B=2`, `C=6`, `epsilon=1/4`, scanned

```text
k=300,437,...,3000,
24 selected actual 451 dyadic prime blocks of ranks 8 through 128,
1<=A<=min(30000,floor(P/h)),
```

and three explicitly labelled pairwise-coprime, not-asserted-prime
structured offset systems.  It retained the exact inverse-`F'(d_i)` phases
and verified the bigint numerator for each reported extremizer.

No scanned positive-`A` partial high-support mass approached one.  The
largest was the actual block `k=711, Delta=64, q=8`, with

```text
log(sum of scanned Phi_h(A) w(z(A))) = -26.3206852739.
```

This is only a positive-`A`, finite-prefix partial sum: it omits negative
`A`, `A=0`, and the unscanned tail, so it is not an upper bound for (WA).
It is recorded only because no finite resonance falsified (WA).

The largest individual joint local weight relative to the product of the
**centered-core residue means** was also in that block:

```text
A=7471,
z=(5,257,-150,-87,12,-10,4,-36),
log(w(z)/product_i mean_core(psi_i))=2.5116418954.
```

Thus one actual word was larger than this diagnostic product mean by about
`12.3`, but not by a `q^(cq)` or `exp(cq)` factor in the scanned systems.
The comparison is not to the full periodized local mass: multiples of
`p_i` are intentionally absent from the centered-core mean.

Across the actual systems the initial-zero centered-moment histogram among
the `143260` scanned high-support zero-carry words was

```text
zero moments 0: 142353
zero moments 1:    904
zero moments 2:      3.
```

The last line supplies an exact actual-451 counterexample to any claim that
a small geometric ratio alone forces many exact moments.  In the block

```text
k=711, Delta=64,
p=(787,797,809,811,821,823,827,829),
P=190636239282683486702929,
z=(135,-367,122,289,131,-367,-207,264),
A(z)=1032,
E=2d-3Delta=(-40,-20,4,8,28,32,40,44),
K=1614,
```

direct integer arithmetic gives

```text
(M_0,M_1,M_2,M_3)=(0,0,-3552,-5457792),
max_i |E_i|/K=44/1614<0.028,
alpha(z)=1032/P != 0.
```

So exact vanishing stops after two moments even at ratio below `0.028`;
the remaining geometric series carries the nonzero rational phase.

### 4.1 Deeper fixed-parameter scans

A second guarded scan used `k=500,831,...,10000`, 36 selected actual
blocks of ranks 11 through 427, and `A<=100000`.  The same systems were
replayed for fixed `(L,C)=(2,6),(4,6),(6,6),(2,3)`.  The maxima were:

```text
(L,C)  max log(word/core-residue-product-mean)  max log(scanned total)
(2,6)                  0.7872103140                    -37.2281029554
(4,6)                -14.8424704494                    -49.4743775787
(6,6)                -11.7805029541                    -44.2218324005
(2,3)                  0.7872103140                    -37.2280883692
```

Again, column two is an individual centered-core diagnostic and column
three is the positive-`A` diagonal-weighted partial mass.  They must not be
identified.  No tested fixed order produced a finite resonance, but these
prefixes provide no tail bound.

The longer scan found five words with exactly two initial zero moments.
For example, the actual block `k=6458, Delta=128, q=14` has a reported
word with `M_0=M_1=0`, `M_2=-314976`, and geometric ratio below `0.009`.
This independently reinforces the finite carry obstruction.

### 4.2 Exhaustive feasible small-rank Fejer tests

After (R3.15)--(R3.16) was identified, a separate exact-`h` scan exhausted
every actual-prime subblock on the explicit grid

```text
k=50,60,...,100,  q in {3,4,5},
(2 floor(b)+1)^q <= 1000000,
C=1.05,1.10,...,6.00,
h=floor(k^2 C^q P/product_i d_i),  1<=h<P/2.
```

Here each decimal `C=c/100` was evaluated with the integer formula

```text
h=floor(k^2 c^q P/(100^q product_i d_i)),
```

so there is no floating-point floor ambiguity.  Exactly 238 feasible
subblocks were scanned (`166` of rank 3, `71` of rank 4, and `1` of rank
5); 157 larger frequency boxes were excluded by the declared word cap and
9 subblocks had no valid `h` on the grid.

All 238 feasible subblocks attained `S<2` by `C<=1.15`.  The worst first
grid crossing was

```text
k=60, Delta=32, p=(101,103,107,109), d=(41,43,47,49):
C=1.10 gives S=2.0002185824,
C=1.15 gives S=1.9612850627.
```

This is encouraging evidence that the Fejer bridge is not already false
at modest rank.  It is neither monotonicity evidence nor an asymptotic
bound: the grid, rank, word cap, and `k` range are part of the result.

### 4.3 Complete-block exact-interval diagnostics

The later direct integer-`H` scanner avoids frequency-box enumeration.  For
the complete actual dyadic block it checks every `1<=H<h` against the unique
centered residues and evaluates (R3.16).  Its membership, rational ceiling,
origin, sign factor, and triangular weights independently pass the detailed
cross-audit in
`audit/m10_periodized_bridge_exact_interval_cross_audit_by_m05.md`.

It gives strict finite counterexamples to the choice `C=1`:

```text
(k,Delta,q)   S(C=1)
(57,32,7)      2.928087268
(100,64,8)     3.989495594
(118,64,9)     7.742589110
(117,64,10)   15.477197745.
```

Thus the strong positive Fejer bridge cannot close with unit exponential
factor.  This is not a counterexample to the exact-carry Fourier sum.

Independent guarded `C=2` replays give respectively `1.010813016`,
`1.002870796`, `1.022549451`, and `1.006700721` in ranks seven through ten.
The strongest additional budgeted complete-block scan used `30<=k<=1000`,
`h<=10^9`, and total `h` budget `10^10`; it tested 79 cases, including all
12 eligible rank-seven blocks in that declared box, with no `C=2` failure.
The current arbitrary-precision GMP source also passed a rational rank-eight
replay and reproduced rank nine.  These are encouraging finite falsifiers,
not a uniform `C=2` estimate and not evidence of monotonicity in block rank.

## 5. The finite carry lemma that actually follows

Let `p_i=(K+E_i)/2`, `|E_i|<=R<K`, `rho=R/K`,
`Z=sum_i|z_i|`, and `M_j=sum_i z_i E_i^j`.  If
`M_0=...=M_(s-1)=0`, the exact series implies

```text
|M_s|
 <= K^(s+1)|alpha(z)|/2 + Z R^s rho/(1-rho).                (R3.11)
```

Indeed, after isolating the `s`-th term, the remaining series is at most
`Z rho^(s+1)/(1-rho)` before multiplying by `K^s`.  Since `M_s` is an
integer, (R3.11) proves the recursive implication

```text
K^(s+1)|alpha(z)|/2 + Z R^s rho/(1-rho) < 1
    ==> M_s=0.                                               (R3.12)
```

This is a valid finite carry lemma.  At natural high support, however,
`Z` is large and already the second term in (R3.12) exceeds one.  The
actual example above shows this is a real loss, not just loose notation.
A successful root-of-unity height argument must therefore exploit the
simultaneous integer-node structure of the moments, or a weighted average
over `A`; geometric decay alone cannot supply high exact multiplicity.

## 6. Cross-audit of the periodized joint correlation and its repair

The first version of the separate proof-line note
`work/m10_round1/high_support_joint_correlation_round3.md` contained one
correct algebraic cancellation but an invalid direct closure implication.
The current author version has removed that implication and labels the
arbitrary `C_y(omega)` only as a surrogate.

The cancellation passes.  With `epsilon=(-1)^(q-1)`,

```text
P/p_i == epsilon F'(d_i) (mod p_i),
c_i == epsilon/F'(d_i) (mod p_i),
```

so the global CRT frequency created by `a_i c_i` has residue `a_i` modulo
`p_i`.  Equations (5)--(10), the subset full-period estimate (14), and the
centered-moment algebra (20)--(25) are valid in their stated local scopes.

The reason the original direct implication failed is exact carry.  Directly
expanding the definition gives

```text
product_i U_i(c_i x)
 = sum_{z: A(z) == x (mod P)} product_i u_i(z_i)
 = sum_{ell in Z} W(x+ell P).                               (R3.13)
```

In contrast, the needed quantity is

```text
H_>=sum_A Phi_h(A) W_>(A),                                  (R3.14)
```

and `Phi_h(A)` is not periodic under `A -> A+P`.  Multiplying two separate
periodizations introduces cross-carry terms; an arbitrary `C_y(omega)`
therefore does not identify (43) or (WA).

There is also no located-point implication from positivity of the proposed
`C_y`.  The function `U_i` is the periodization of the noncompact
`sinc^L` sequence.  For every residue `r mod p_i`, its `m=0` term is
nonzero when `r!=0` because `p_i>2b`, while the zero residue has its unit
term.  Hence `U_i(r)>0` for every residue.  Positivity of `C_y` therefore
does not certify `|z_i|<=b` (nor an allowed positive orthant point).  Using
the compact physical B-spline instead restores location, but its discrete
Fourier coefficients are the noncompact `U_i`; this is precisely the
uncertainty tradeoff hidden by the proposed swap.

Likewise, a subset average applied directly to `C_y` uses its physical
integer time length, not `P/h`.  If time is made continuous, the exact
identity is

```text
sum_i a_i c_i/p_i = H(a)/P + kappa(a),  kappa(a) in Z,
```

and the Fourier transform must retain `kappa(a)`; only integer time makes
it disappear, which is exactly the carry-periodization loss in (R3.13).

The author has resolved those points.  More importantly, there is a valid
one-sided repair that deliberately overcounts cross-carries.  For `L=2`,
integer `1<=h<P/2`, set

```text
Omega(r)=sum_ell Phi_h(r+ell P),
V(r)=sum_m W(r+mP)=product_i U_i(c_i r),
S=sum_(r mod P) Omega(r)V(r).
```

Positivity gives `E<=S`, where `E=sum_A Phi_h(A)W(A)`.  The zero vector is
paired with all of `Omega(0)`, and `Omega(0)=1`, so

```text
H_nonzero=E-1 <= S-1.                                      (R3.15)
```

Normalized Poisson/Parseval gives the exact finite bridge

```text
S=(P/h) sum_{|a_i|<b, |H(a)|_P<h}
       (1-|H(a)|_P/h) product_i [b^(-1)(1-|a_i|/b)].        (R3.16)
```

Thus `S<2` is sufficient for the complete Fourier criterion.  This does
not recover exact carry; it is a stronger positive majorant.  It also does
not permit the already-proved low-support contribution to be subtracted
inside the factored `V`.  The remaining theorem is the weighted joint
small-CRT concentration bound (R3.16).

## 7. Final scope

What survives rigorously is:

1. (WA) is the exact weakest positive high-support target after the proved
   low-support `o(1)` estimate;
2. (R3.5) is an exact weighted `A`-fibre energy identity;
3. separated Cauchy still costs `exp(Theta(k))` at macroscopic rank;
4. the finite carry lemma (R3.11)--(R3.12) is sharp enough to expose why
   ratio `<=1/5` alone is insufficient;
5. the cofactor/`F'` cancellation in the arbitrary periodized surrogate is
   correct but loses exact carry;
6. the special Fejer periodization converts that loss into the valid
   one-sided majorant (R3.15)--(R3.16), whose `S<2` estimate remains open.
   Finite exact scans disprove `C=1` for that majorant but have not found a
   `C=2` failure through the tested rank-ten cases.

No general no-go, maximum-gap theorem, or result on Erdős 451 is claimed.
