# Cross-audit: M10 high-support Fejer bridge, round 3

Date: 2026-08-27

Audit type: same-model mathematical cross-audit of
`evidence/m10_high_support_fejer_bridge_round3.md` and its derivation in
`work/m10_round1/high_support_joint_correlation_round3.md`.  This is not an
independent human review.  The author files were not modified.

Verdict: **PASS.**  The Fejer majorant, all normalizations, the general-`L`
principal obstruction, and the exact raw-moment ledgers reconstruct.  The
initial audit required equation (37) to assume `r_epsilon<q`; the current
author derivation now states that hypothesis explicitly, so the mandatory
scope correction is resolved.

## 1. Carry majorant and subtraction

For nonnegative `u_i` and

```text
W(A)=sum_{A(z)=A} product_i u_i(z_i),
V(r)=product_i U_i(c_i r)=sum_m W(r+mP),
Omega(r)=sum_l Phi_h(r+lP),
```

expanding both periodizations gives

```text
S=sum_r Omega(r)V(r)
 =sum_r sum_(l,m) Phi_h(r+lP)W(r+mP) >= E.
```

The `z=0` term of `V(0)` has weight one and is paired in `S` with all of
`Omega(0)`.  Removing this exact cross term gives

```text
E-1 <= S-Omega(0).
```

For `L=2`, integer `h`, `Phi_h(lP)=sinc(pi h l)^2`, so `Omega(0)=1`.
Thus `E-1<=S-1`, and `S<2` really is sufficient for the complete
single-block Fourier criterion.  Zero-phase nonzero vectors remain on both
sides; no improper subtraction occurs.

With normalized DFT `fhat(j)=P^(-1)sum_r f(r)e_P(-jr)`, Poisson gives,
when `h<P/2`,

```text
Omegahat(j)=h^(-1)(1-|j|_P/h)_+.
```

The local triangular coefficient is

```text
beta_i(a)=b^(-1)(1-|a|/b)_+.
```

Parseval therefore contributes the required factor `P/h`, not `1/h` or
`P^2/h`, and yields exactly (14d).  The strict conditions are
`|H(a)|_P<h` and `|a_i|<b`; writing weak inequalities is harmless only
because the boundary weights vanish.

The exact cofactor cancellation also passes:

```text
P/p_i == epsilon F'(d_i) (mod p_i),
c_i == epsilon F'(d_i)^(-1),
H(a) == a_i (mod p_i).
```

It untwists local residue labels but does not control the centered lift;
`H/P == sum_i a_i c_i/p_i (mod 1)` retains the joint phase.

## 2. General smoothing order

If `eta_i` is uniform on an interval of length `2b/(Lp_i)`, the density at
zero of its `L`-fold convolution is

```text
(Lp_i/(2b)) times [density at zero of a sum of L U[-1/2,1/2]],
```

and the bracket is `asymp L^(-1/2)`.  Hence
`beta_i(0)>=c sqrt(L)/b`.  Also, on `|A|<=cP/h`, the sinc argument is
`O(1/L)` and its `L`-th power is bounded below, so the spectral zero term
has mass at least `cP/h`.  The displayed principal lower bound (22b)
follows.  For fixed per-prime `C`, `q/log k -> infinity`, and unbounded even
`L`, it exceeds two.  This is correctly scoped to the periodized
majorant, not the smaller exact fibre sum.

## 3. Exact moments

Equality of `s` exact numerators implies

```text
z_i^(nu)-z_i^(1)=p_i t_i^(nu),
sum_i t_i^(nu)=0,
```

which reconstructs (31).  Dropping these zero-sum constraints is allowed
because all terms are nonnegative.  The identities

```text
sum_t K_(i,s)(t)=sum_n u_i(n)U_i(n)^(s-1),
U_i(n)<=1+C/b^2,
sum_n u_i(n)<=Cp_i/b
```

give (35) with the stated scale.

For the lower diagonal, `1<=n<=floor(p_i/(4b))` gives
`u_i(n)>=8/pi^2` and at least `p_i/(8b)` choices.  Identical `s`-tuples
therefore give

```text
(c_0^s/8)^q P/b^q.
```

Every chosen vector has support exactly `q`, so this is a lower bound for
`M_s^>` **only under `r_epsilon<q`**.  If `r_epsilon=q`, then the condition
`sigma(z)>r_epsilon` is empty.  The intended macroscopic target has
`r_epsilon<q` eventually; the current equation (37) and evidence summary now
state that hypothesis.

With that now-explicit hypothesis, Holder gives the necessary threshold (39),
and substituting `d_i>=2b` gives (40).  Its logarithm is
`Omega(sq log k)` in the stated large-block regime, including `s=2`; the
claim is a no-go only for raw positive collision moments.

## 4. Finite LLL diagnostic

The separate LLL script uses the basis

```text
(2b,2h,...,2h),  -2hp_i e_i,
```

which spans exactly `(2bH,2ha_i)` with `a_i==H (mod p_i)`.  Its inside
test and the single-term logarithm match (14d), and `h` is computed by an
exact integer ceiling.  The reported 36-block scan is correctly only a
falsification diagnostic: LLL basis rows do not enumerate all short words.
The absence of a one-vector obstruction therefore neither proves `S<2`
nor changes the bridge's open status.

Final classification: the Fejer bridge is a valid, materially sharper
remaining interface.  The earlier missing `r_epsilon<q` hypothesis in the
full-support diagonal lower bound has been corrected in the frozen author
files.
