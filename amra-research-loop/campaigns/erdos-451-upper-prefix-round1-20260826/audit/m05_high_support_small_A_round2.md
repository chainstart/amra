# M05 round 2: the high-support, small-phase dual obstruction

Date: 2026-08-26

Status: **a rigorous narrowing, not a maximum-gap theorem and not a solution
of Erdős 451.**  This note continues the independent M10 audit of the M05
single-block extension.  It proves the exact inverse-Vandermonde formula for
the deepest moment cancellation, a root-of-unity height lemma, and an
unconditional Dirichlet construction of critical-support small-phase dual
vectors for every actual 451 block.  The last result shows why a generic
support-sensitive transference argument is quantitatively tight up to
constants.  The remaining statement is an arithmetic, coefficient-sensitive
covering theorem, stated exactly in Section 6.

No M05 author file is modified here.

## 1. The dual problem and the parameter split

Let `p_i=k+d_i` be all primes of one dyadic block

\[
                 \Delta\le d_i<2\Delta,\qquad 1\le i\le q,
                                                                    \tag{1}
\]

and put `P=product_i p_i`.  With

\[
 w=\left\lfloor{\Delta-1\over2}\right\rfloor,
 \qquad b=w+\tfrac12,
\]

the exact support function of the symmetric affine-covering body is

\[
 R_h(z)=h\left|\sum_i{z_i\over p_i}\right|
            +\sum_i b{|z_i|\over p_i}.                         \tag{2}
\]

For `Delta>=2`, `b>=Delta/4`, and hence

\[
 R_h(z)\ge h{|A|\over P}+{\Delta\over8k}\|z\|_1,
 \qquad A=P\sum_i{z_i\over p_i}\in\mathbb Z.                 \tag{3}
\]

If the support has cardinality `r`, the previously proved divisibility
argument gives

\[
 R_h(z)>{h\over(2k)^r}+{r\Delta\over8k}.                       \tag{4}
\]

There is a useful rigorous scale split.  For
`Delta<=k/(log k)^3`, distinctness alone gives `q<=Delta`, so any one-block
loss `q^(O(q))` has

\[
 \log q^{O(q)}=O(\Delta\log\Delta)
              =O\left({k\over(\log k)^2}\right)=o(k).          \tag{5}
\]

The sum of (5) over the dyadic blocks below this cutoff has the same order.
Thus generic dimension loss is exponent-compatible there.  Above the cutoff,
however, the transverse term in (4) is only

\[
                  {r\Delta\over8k}\ge {r\over8(\log k)^3}.    \tag{6}
\]

Even a hypothetical support-sensitive transference theorem with a linear
`Theta(r)` threshold therefore loses a factor up to `(log k)^3`.  Standard
ambient-dimensional transference asks for control on the `q` scale, which is
still stronger when `r=o(q)`.  Equations (5)--(6) do not close the large
blocks; they identify the exact range in which coefficient quality is needed.

## 2. Exact offset-polynomial and Vandermonde identities

Let

\[
              F(X)=\prod_{i=1}^q(X-d_i).
\]

Reduction modulo `p_i=k+d_i` gives the exact phase formula

\[
 {P\over p_i}\equiv\prod_{j\ne i}(d_j-d_i)
             =(-1)^{q-1}F'(d_i)\pmod {p_i}.                   \tag{7}
\]

Consequently every dual vector obeys

\[
                 F'(d_i)z_i\equiv(-1)^{q-1}A\pmod {p_i}.      \tag{8}
\]

This is the precise weighted-centered-CRT problem; replacing the residues in
(8) by arbitrary units discards the common offset polynomial.

There is also an exact description of the deepest ordinary-moment
cancellation.  Suppose

\[
                 \sum_i z_i d_i^t=0\quad(0\le t\le q-2).      \tag{9}
\]

Put

\[
                 C_D=\mathop{\rm lcm}_i |F'(d_i)|.
\]

The nullspace of the `(q-1) by q` Vandermonde matrix is one-dimensional, so
the primitive integral solutions of (9) are, up to a common sign,

\[
                         z_i={C_D\over F'(d_i)}.               \tag{10}
\]

Indeed these entries are integral, and their gcd is one: if a prime divided
every `C_D/F'(d_i)`, then `C_D` divided by that prime would still be a common
multiple of all `|F'(d_i)|`.

Partial fractions give more than a congruence.  Since

\[
 {1\over F(x)}=\sum_i{1\over F'(d_i)(x-d_i)},
\]

evaluation at `x=-k` yields

\[
 \sum_i{C_D\over F'(d_i)p_i}
       ={(-1)^{q+1}C_D\over P},
 \qquad A=(-1)^{q+1}C_D.                                    \tag{11}
\]

Thus the full moment resonance is not merely a formal analogy: it is an
exact small-phase dual vector, with its phase and coefficient cost coupled by
the same integer `C_D`.

## 3. A standalone sparse-polynomial height lemma

The following unconditional lemma measures one part of that coupling.

> **Lemma 3.1 (root-of-unity height).**  Let
> `Z(X)` be a nonzero integer polynomial of degree at most `D`, let its exact
> multiplicity at `X=1` be `rho`, and let `L` be the sum of the absolute
> values of its coefficients.  For all sufficiently large `D`,
> \[
>                 \log L\gg \rho\sqrt{{\log D\over D}}.       \tag{12}
> \]
> The implied constant is absolute.

Proof.  Write `Z=(X-1)^rho Q` with `Q(1)\ne0`.  Choose

\[
                         M=C\sqrt{D\log D}
\]

with a sufficiently large absolute `C`.  By the prime number theorem there
are `gg M/log M` primes `ell` in `[M,2M]`.  The distinct cyclotomic factors
`Phi_ell` have degree `ell-1>=M-1`, so at most `D/(M-1)` of them divide `Q`.
The choice of `C` leaves a prime `ell` for which `Phi_ell` does not divide
`Q`.

For a primitive `ell`-th root `zeta`, the resultant is a nonzero integer and

\[
 \prod_{a=1}^{\ell-1}|Z(\zeta^a)|
   =\ell^\rho |\operatorname {Res}(Q,\Phi_\ell)|
   \ge\ell^\rho.                                             \tag{13}
\]

Every factor on the left is at most `L`.  Hence

\[
             L^{\ell-1}\ge\ell^\rho,
 \qquad \log L\ge {\rho\log\ell\over\ell-1},                \tag{14}
\]

and (12) follows from `ell` being comparable to `sqrt(D log D)`.  This proof uses no
distribution information about the nodes.

For `Z(X)=sum_i z_i X^(d_i-d_1)`, (9) is equivalent to a zero at one with
multiplicity at least `q-1`.  Lemma 3.1 therefore gives

\[
        \log\|z\|_1\gg q\sqrt{{\log\Delta\over\Delta}}.      \tag{15}
\]

For a macroscopic block this is `Omega(sqrt(k/log k))`, much larger than
`log k`, so the exact full-moment vector has coefficient cost exceeding every
fixed power of `k`.  This is genuine progress over the bare support bound.

It does **not** settle (2).  A phase as small as `exp(-Theta(q))` need not
come from exact vanishing of the first `q-1` moments.  Turning approximate
cancellation of `sum z_i/(k+d_i)` into exact high multiplicity would require
a new arithmetic stability theorem; the rational granularity `1/P` is only
`exp(-Theta(q log k))`, too fine for such a conclusion by rounding.

## 4. Critical-support small phases exist for every actual block

The next result prevents an overstrong reading of (15).

> **Lemma 4.1 (box Dirichlet with a support certificate).**  Let
> `p_1,...,p_q` be distinct primes in `(k,2k)` and let `1<=M<k` be an
> integer.  There is a nonzero `z in [-M,M]^q intersect Z^q` such that
> \[
> \left|\sum_i{z_i\over p_i}\right|
>   \le {Mq\over k((M+1)^q-1)}.                               \tag{16}
> \]
> If `r` is its support size, then
> \[
> r\ge {\log\bigl(k((M+1)^q-1)/(Mq)\bigr)\over\log(2k)}.     \tag{17}
> \]

Proof.  The `(M+1)^q` numbers

\[
                 \sum_i{a_i\over p_i},\qquad 0\le a_i\le M,
\]

lie in an interval of length at most `Mq/k`.  Two consecutive ordered values
have separation at most (16); their coefficient-vector difference is the
required `z`.  This difference is nonzero.  Moreover the rational sum cannot
vanish: after restricting to its support and multiplying by the product of
the active primes, reduction modulo `p_i` would give `p_i|z_i`, impossible
because `|z_i|<p_i`.  Its absolute value is therefore at least the reciprocal
of that active product, which is greater than `(2k)^(-r)`.  Comparison with
(16) proves (17).

Substitution into (2) gives the exact upper ledger

\[
 \min_{z\ne0}R_h(z)
 \le {hMq\over k((M+1)^q-1)}+{bMq\over k}.                   \tag{18}
\]

Taking `M` on the scale `(h/b)^(1/q)` makes the right side

\[
                  O\left({q\over k}h^{1/q}b^{1-1/q}
                           +{bq\over k}\right).              \tag{19}
\]

At the proposed density scale

\[
 h=k^B C^q\delta_B^{-1},\qquad
 \delta_B=\prod_i{d_i\over p_i},                             \tag{20}
\]

the right side is `O(C' q k^(B/q))`, where `C'` absorbs the harmless
within-block factor between the `d_i`.  For `q/log k -> infinity`, this is
`O(C' q)`.  Meanwhile (17) places the support at least on the critical scale

\[
         r\ge(1-o(1)){q\log M\over\log k}.                   \tag{21}
\]

Lemma 4.1 applies to the actual prime moduli of every 451 block.  It is an
exact method boundary: the best possible universal lower bound for (2) is at
most linear in ambient rank at the density scale, and small-phase vectors
already occur at the same critical support suggested by (4).  It does not
produce a long primal gap; a short dual vector is not a converse to a
covering theorem.

## 5. What the parameter split does and does not buy

For `Delta<=k/(log k)^3`, (5) makes even a `q^(O(q))` single-block theorem
affordable.  For `Delta>k/(log k)^3`, put

\[
       r_*(h)=\left\lfloor{\log h\over\log(2k)}\right\rfloor.
                                                                    \tag{22}
\]

The time term in (4) controls supports below this transition only at a
constant-width scale; above it, (6) is the available unconditional growth.
For example, when `Delta=k/(log k)^3` and (20) holds,

\[
             r_*(h)=B+O\left({q\log\log k\over\log k}\right)=o(q). \tag{23}
\]

Thus a statement whose flatness cost is linear in the **ambient** dimension
still asks for `Theta(q)` dual width throughout most of the interval
`r_*<r<=q`, whereas (4) supplies only `r/(log k)^3`.  Merely replacing the
ambient dimension by the active support would ask for `Theta(r)` and still
miss by the same `(log k)^3` factor.  This is the exact constant/dimension
obstruction requested in the parameter-split audit.

Lemma 3.1 removes the endpoint of exact full-moment cancellation when the
coefficient budget is small, but Lemma 4.1 shows that approximate phases at
the critical rank are unavoidable.  Neither generic flatness nor the bare
support count distinguishes these two facts.

## 6. A concrete affine-covering gate, and why it fails

The transference requirement can be made unconditional and concrete.  Let
`K_h` be the closed centered zonotope whose support function is (2).  The
located target for a forward increment is a translate of such a body with
time half-width `h=(H-w)/2`; a lattice point in every translate gives an
actual forward increment at most `H+w` after the common offset correction.

> **Lemma 6.1 (John--Euclidean flatness gate).**  Every translate of `K_h`
> contains a point of `Z^q` if
> \[
>                 \min_{0\ne z\in\mathbb Z^q}R_h(z)
>                         >{q^{3/2}\over2}.                   \tag{24}
> \]

Proof.  By the symmetric form of John's theorem there is an ellipsoid `E`
with

\[
                         E\subseteq K_h\subseteq\sqrt q E.   \tag{25}
\]

If some translate of `K_h` were lattice-free, the same translate of `E`
would be lattice-free, so its lattice covering radius would exceed one.  The
Euclidean covering/dual-short-vector transference theorem
`mu(E,Z^q) lambda_1(E polar,Z^q)<=q/2` then supplies a nonzero integral `z`
with `h_E(z)<q/2`.  From (25),

\[
                    R_h(z)=h_{K_h}(z)le\sqrt q h_E(z)
                              <{q^{3/2}\over2},               \tag{26}
\]

contrary to (24).  This also pins down why a support count cannot simply be
inserted into the standard theorem: John's factor and the Euclidean
transference dimension are the ambient `q`, not the support of the selected
dual vector.

Lemma 4.1 rigorously kills this particular gate at the desired scale.  For
fixed exponential base `C`, (19) constructs, in every sufficiently large-rank
actual block, a nonzero dual vector with `R_h(z)=O(Cq)`.  This is eventually
smaller than `q^(3/2)/2`, so (24) cannot be verified by any lower bound: the
criterion itself is too expensive.  This is a no-go only for the
John-ellipsoid/Euclidean-flatness handoff.  It is not a primal long-gap
construction and does not refute a special zonotope covering theorem with a
linear threshold.

## 7. The unique remaining one-block interface

A sufficient arithmetic input must retain (8).  Two honest versions are:

1. **Ambient-rank coefficient-phase alternative.**  For the `h` in (20),
   every nonzero `z` satisfies either
   \[
       h{|A|\over P}\ge \tau q
       \quad\hbox{or}\quad
       \|z\|_1\ge 8\tau{k\over\Delta}q,                      \tag{27}
   \]
   with `tau` large enough for a stated affine covering theorem.

2. **Support-sensitive alternative.**  Prove a covering theorem whose loss
   for a witness supported on `r` coordinates is `tau r`, and prove
   \[
       h{|A|\over P}\ge \tau r
       \quad\hbox{or}\quad
       \|z\|_1\ge 8\tau{k\over\Delta}r.                      \tag{28}
   \]

Equation (27) is stronger.  Equation (28) is not sufficient without the new
support-sensitive covering statement; standard transference keeps ambient
dimension.  Lemma 4.1 says that the order `q` in (24) cannot be raised, and
that constants and the exact phase-coefficient coupling matter.

Proving (27), or the paired statements behind (28), would give the missing
single-block max-gap theorem with a `C^q`-compatible loss.  The current round
does not prove either.  The remaining inequality is strictly narrower than
"control the gap": it is a weighted centered-representative theorem for the
specific inverse derivatives `F'(d_i)^(-1) mod p_i`, stable under approximate
rather than exact moment cancellation.

## 8. Guarded finite falsification

The exact script

```text
work/m10_round1/high_support_vandermonde_search.py
```

enumerates primitive full-moment vectors for all node sets of size at most
ten in a bounded interval and records actual-prime dyadic blocks.  It is only
a kill test for naive coefficient lower bounds.  Among all node sets in
`[0,20]`, the minimum observed `L1` norms for ranks two through ten were

```text
2, 4, 6, 16, 12, 64, 42, 256, 252.
```

The rank-six set `(0,1,4,6,9,10)` has primitive vector
`(-1,2,-3,3,-2,1)` and `L1=12`; hence the tempting bound `L1>=2^(q-1)` is
false.  Actual 451 blocks also realize the rank-four pattern: for `k=168`,
the block offsets `(23,25,29,31)` have primitive `L1=6`.

Authoritative replay:

```text
/home/biostar/work/projects/openmath/bin/openmath-memory-guard -- \
  python3 work/m10_round1/high_support_vandermonde_search.py \
  --max-q 10 --width 20 --max-k 1000
```

Guard unit `openmath-task-20260826-234557-339851.scope`, exit status zero,
wall time `2.00s`, maximum RSS `15520 KiB`, and zero swap.  The finite data
neither prove nor refute (27)--(28).

An independent exact coefficient-budget search is recorded in
`evidence/m10_round2_actual_dual_budget_summary.json`.  Its meet-in-the-middle
algorithm was checked against brute force on the complete rank-four
frontier.  The two largest accepted searches were:

- `k=58`, rank six, every `|z_i|<=45` (conceptually `91^6-1` vectors):
  the minimum found for (2), at `h=k^2 6^q delta_B^(-1)`, has
  `z=(-8,10,4,0,-7,1)`, support five, first nonzero moment one, and
  `R_h(z)/q=1.8373188133`;
- `k=116`, rank seven, every `|z_i|<=20` (conceptually `41^7-1` vectors):
  the minimum has `z=(-8,13,-5,8,-7,-11,10)`, full support, first nonzero
  moment one, and `R_h(z)/q=6.3695873022`.

The first run used guard unit `openmath-task-20260826-235131-341628.scope`
(exit zero, `48.09s`, maximum RSS `268640 KiB`, zero swap); the second used
`openmath-task-20260826-235302-342002.scope` (exit zero, `9.19s`, maximum RSS
`557072 KiB`, zero swap).  The observed minimizers are approximate
cancellations of moment order only one, so Lemma 3.1 does not control them.
No finite row is promoted to an all-parameter lower bound.
