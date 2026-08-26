# Cross-audit of the M05 special-zonotope low-support ledger

Date: 2026-08-27

Audit type: same-model cross-audit by an agent that did not author
`m05_special_zonotope_linear_gate.md`.  This is not a human referee report or
an independent-model audit.  The author file was read without modification.

Scope: Lemma 9.1 and equations (31)--(41), with special attention to reduced
support, local sinc mass, the zero reciprocal phase, the smoothing order,
small `b`, and the endpoint cases `r_epsilon=0,q`; followed by Lemma 11.1
and the weighted determinant/resultant audit in equations (45)--(57).

## Verdict

**Lemma 9.1, equations (34)--(35): PASS.  The asymptotic conclusion (41):
CONDITIONAL PASS with two mandatory scope corrections.**

The finite low-support bound is correct.  Equation (41) follows by the stated
argument provided:

1. `L>=2` is a fixed integer independent of `k` (as intended earlier in the
   note); and
2. `0<epsilon<1`, `h>=C^q`, and `h->infinity`.

The displayed hypothesis (38) should therefore either say, for example,
"fixed `B>0`, fixed `C>1`, fixed integer `L>=2`, and `0<epsilon<1`", or state
`h>=C^q` and `h->infinity` directly.  As written it says only
`epsilon>0` and does not specify the sign of `B`.  For `epsilon>1`, (39) can
be negative and cannot be passed to Lemma 9.1, whose parameter satisfies
`0<=r<=q`.  If `B=0`, fixed rank and density bounded away from zero can leave
`h` bounded, so the particular `h^{-epsilon L+o(1)}` deduction does not tend
to zero.  The latter edge can alternatively be handled directly from the
`b^{-L}` coordinate mass, but that extra case is not in the written proof.

These are scope/proof-completeness corrections, not a failure of the central
reduced-support mechanism.  No missing `sigma<=r_epsilon` class was found.
Lemma 11.1 and the two determinant branches also reconstruct in their target
regime, subject to the additional finite hypothesis `X>=1/2` and the stated
unbounded-rank/`h<<P` asymptotic scope below.

## 1. Local sinc masses

For

```text
psi_i(n)=|sinc(2 pi b n/(L p_i))|^L,
```

the standard bound `|sinc u|<=min(1,1/|u|)` gives

```text
sum_n psi_i(n) = O_L(p_i/b),
sum_{t != 0} psi_i(p_i t) = O_L(b^{-L}).
```

For the second estimate, when `b>=1` every nonzero term is
`O_L((b|t|)^{-L})`; when `1/2<=b<1`, the claimed `O_L(b^{-L})` absorbs the
finitely many unit-size terms.  Thus excluding the multiples of `p_i` in the
first sum gives (33).  There is no hidden small-`b` failure: definition (1)
always has `b>=1/2`, while the asymptotic regime in (38) has
`b asymp Delta->infinity`.

The dependence on `L` is not uniform.  Constants in the sinc comparison and
the later logarithmic ledger may grow with `L`; consequently `L` must remain
fixed.  The author note says this immediately after (33), but (38)--(41)
should retain it explicitly.

## 2. Reduced support and denominator

Fix `S={i:p_i does not divide z_i}`.  For `i in S`, (33) contributes at most
`C_L p_i/b<=C'_L k/b`; for `i not in S`, summing all `z_i=p_i t_i`, including
zero, contributes at most `1+D_Lb^{-L}`.  Hence the total coordinate mass for
this exact reduced support is

```text
(C_L k/b)^|S| (1+D_L b^{-L})^(q-|S|),
```

which is (36) after harmless adjustment of the `L`-dependent constant.

Inactive coordinates contribute integers to
`alpha(z)=sum_i z_i/p_i`.  The remaining fractional denominator divides
`product_{i in S}p_i`.  Therefore a nonzero `alpha` satisfies

```text
|alpha(z)| >= 1/product_{i in S}p_i >= (2k)^(-|S|).
```

This remains valid when the fractional part cancels to a nonzero integer,
and when `S` is empty it reads `|alpha|>=1`.  Applying the sinc decay to the
diagonal factor and summing over the `binomial(q,s)` choices of `S` proves
(34), including `s=0`.

## 3. Zero reciprocal phase

If `alpha(z)=0`, multiplication by `P=product_i p_i` and reduction modulo
`p_i` forces `p_i|z_i` for every `i`.  Writing `z_i=p_i t_i` then gives
`sum_i t_i=0`.  Choosing `t_1,...,t_{q-1}` freely, determining `t_q`, and
discarding its weight yields

```text
(1+D_L b^{-L})^(q-1)-1
 <= exp(D_L q/b^L)-1.
```

Thus (35) is correct.  Every zero-phase vector has reduced support zero, so
(35) covers it for every `r>=0`; it is not omitted from (41).  At `q=1` the
only zero-phase vector is the removed zero vector.  The degenerate `q=0`
block should simply be declared trivial rather than using the proof's
"last coordinate" language.

## 4. The transition and both endpoint cases

Assume now fixed `0<epsilon<1`.  For

```text
s<=r_epsilon<=floor((1-epsilon)log h/log(2k)),
```

one has `(2k)^s<=h^(1-epsilon)`, so the diagonal factor in (34) is
`O_L(h^{-epsilon L})`.  For `r=r_epsilon>=1`,

```text
log sum_{s<=r} binomial(q,s)(C_L k/b)^s
 <= r[log(eq/r)+log(C'_L k/b)]+O(q/b^L).
```

The floor causes no problem.  If `r<q`, `h>=C^q` gives
`q/r=O(log k)`; if `r=q`, this ratio is one; and if `r=0`, the sum has only
the `s=0` term.  Since `k/b=O((log k)^3)` and
`r<=log h/log(2k)`, the displayed logarithm is
`O(log h loglog k/log k)+o(1)=o(log h)`.  Also
`q/b^L=o(1)` follows from `q<=Delta`, `b asymp Delta`, `L>=2`, and
`Delta>k/(log k)^3`.

The endpoint cases are therefore sound under the corrected scope:

- If `r_epsilon=0`, (34) controls the nonzero integer phases with reduced
  support zero by `h^{-epsilon L+o(1)}`, while (35) controls all zero phases.
- If `r_epsilon=q`, the same estimate applies through `s=q`, so (34) covers
  every nonzero phase and (35) covers the remaining zero phase.  In this
  case the hypothesis itself implies
  `log h >= q log(2k)/(1-epsilon)+O(log k)`, which pays the full binomial
  entropy.

Thus, after adding the two scope conditions in the verdict, (34)--(35)
indeed imply

```text
sum_{z != 0, sigma(z)<=r_epsilon} |fhat_L(z)|=o(1).
```

## 5. Exact boundary of the result

The proof is absolute-value based and does not estimate any support with
`sigma(z)>r_epsilon`.  It therefore does not prove the covering criterion
(7), except in the exceptional parameter regime `r_epsilon=q`.  It also
does not use finite experiments as an asymptotic theorem.  Subject to the
scope corrections above, the author's final description—low reduced support
and the entire zero-phase class are removed, while high reduced support
remains—is accurate.

## 6. Singleton projection and its asymptotic scope

For each admitted endpoint `A`, (44) and `M<p_i/2` determine a unique
centered symbol `z_i(A) in [-M,M]`.  If distinct endpoints `A,B` have equal
symbols on coordinates `T`, subtracting (44) gives `p_i|(A-B)` for every
`i in T`; the distinct primes therefore give

```text
k^|T| < product_{i in T}p_i <= |A-B| <= 2X.                 (CA1)
```

With `J=floor(log(2X)/log k)`, agreement on any prescribed `J+1`
coordinates contradicts (CA1).  Projection to one fixed set of `J+1`
coordinates is consequently injective and has at most
`(2M+1)^(J+1)` values.  The quantifiers in the Singleton projection are
correct: it is not necessary to union over the choices of the projection.

The literal finite lemma should add `X>=1/2`, equivalently `J>=0`.  Under
only `0<X<P/2`, one may have `J<=-2`, when the right side of (46) is below
one although `A=0` is admitted.  This does not affect the intended target,
where `X=P/h->infinity`, but it is a mandatory statement correction (or the
case `X<1/2` must be separated as the trivial singleton case).

At `X=P/h`,

```text
log P=q log k+O(q)
```

and the floor contributes `O(1)`, so (48) follows.  The application also
needs `2<h<=2P` and `J<q`.  In the intended nontrivial application one first
separates `h>=P`, where the period bound is already stronger, and the target
density scale then gives `J<q`; these conditions are not consequences of an
arbitrary lower bound on `h` alone.
Finally, (50) is the relevant statement for the unbounded-rank regime
`q->infinity`.  There,

```text
log h=O(q loglog k+log k),   log(2M+1)=O(loglog k),
```

at the proposed scale `h=k^B C^q delta_B^(-1)`.  Hence the Singleton saving is only an
`O(loglog k/log k)+O(1/q)` fraction of the original word entropy.  Bounded
rank is already absorbable into a fixed polynomial loss and should not be
included in the `exp((1-o(1))q log(2M+1))` wording without qualification.

## 7. Weighted Vandermonde and the normalization audit

Subtracting (44) for `A_u,A_v` gives

```text
A_v-A_u == (-1)^(q-1)F'(d_i)(z_i(v)-z_i(u))  (mod p_i).
```

Multiplication over the `binomial(s,2)` pairs proves (52), including its
sign.  If `E_i` local pairs have equal symbols, then
`p_i^E_i|V_A`; because the endpoints are distinct, `V_A` is nonzero, and

```text
sum_i E_i log p_i <= log|V_A| <= binomial(s,2)log(2X).
```

The convexity bound
`E_i>=s^2/(2(2M+1))-s/2` is exact.  Substitution and division by `s/2`
reproduce LS2 verbatim.  Using joint coordinate agreements instead recovers
the Singleton projection above.  Thus the divisibility-only branch contains
no extra entropy.

On the nonzero branch, `|V_i|<=(2M)^binomial(s,2)` and

```text
|F'(d_i)|=product_{j!=i}|d_i-d_j| < Delta^(q-1).
```

The available integer representative of the right side of (52) therefore
pays the full inverse-derivative height.  No scalar normalization removes
it.  Since `F'(d_i)` is a unit modulo `p_i`, multiplying by its modular
inverse merely rewrites the same congruence as

```text
V_i == (+/-)F'(d_i)^(-C_s)V_A  (mod p_i);
```

there is no small archimedean representative for that inverse.  Dividing an
integer Vandermonde or the polynomial (56) by a power of `F'(d_i)` produces
rational coefficients; clearing denominators restores exactly the discarded
height.  Multiplication over `i` replaces the local factors by the
discriminant `product_i F'(d_i)` and increases rather than cancels the
height.  Because `gcd(F'(d_i),p_i)=1`, no `p_i`-adic common factor is
available for a primitive reduction.

The resultant branch is likewise correct: the admitted symbol supplies one
factor of (56) divisible by `p_i`, while the elementary evaluation bound is
`(|A|+M|F'(d_i)|)^(2M+1)`, far beyond `p_i` at unbounded rank.

Accordingly the author's two-branch no-go is valid for the explicitly
described unweighted integer Vandermonde/resultant method.  It is not a
no-go for controlling the centered residues of `F'(d_i) mod p_i`, for a
signed combination across coordinates, or for a different weighted code
estimate; the author preserves exactly those exceptions.
