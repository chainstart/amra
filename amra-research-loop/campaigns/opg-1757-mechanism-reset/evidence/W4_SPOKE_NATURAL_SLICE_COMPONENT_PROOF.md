# W4 spoke: strict domination on the natural two-variable component

Date: 2026-08-02
Status: **exact two-variable survivor proof; not full four-variable domination**

## 1. Artifacts and claim

- `evidence/w4_spoke_c_component_proof.py`
  SHA-256 `6046a420eb2db33841df5b5a5e339ea4d644b496fcb34ffbf86873307d9af046`
- `evidence/w4_spoke_c_component_proof.json`
  SHA-256 `562dee561634c8e44e9486059157429346aa61c2b0bee31067c8688bd49f648b`

For the marked spoke `01`, use the stabilizer variables from
`W4_GARDING_ORBIT_PROBE.md` and impose the natural slice

\[
 b=a,\qquad d=c.
\]

The exact conclusion is:

> On the connected component of the sliced set
> `C_{M\setminus e}>0` that contains the positive orthant, every point is in
> the full deletion distinguished component and satisfies `xi_e>0`.

Thus the narrow spoke-`c` boundary gap is not a numerical accident: no point
of this entire two-dimensional component can kill the marked-spoke orbit.
This does not prove domination on the original four-variable specialization.

## 2. Depressed-cubic form

Set `x=a+1`.  The exact polynomials from the forest enumeration become

\[
 C_{M\setminus e}=cP(x,c),\qquad \xi_e=2cQ(x,c),
\]

where

\[
\begin{aligned}
A(c)&=(c+2)(c^2+2c+2),\\
H(c)&=c^2+4c+6,\\
P(x,c)&=A(c)x^3-2H(c)x+2(c+4),\\
Q(x,c)&=H(c)x^2-3(c+4)x+6-c.
\end{aligned}
\]

This is identity (S) in a more useful coordinate.  Direct substitution also
recovers it exactly:

\[
 (a+1)P-(a^2c+2ac+3a+c+2)Q=a^2(4a^2-2a-c).
\]

## 3. Exact root geometry for every `c>0`

Elimination gives

\[
\begin{aligned}
\operatorname{disc}_x(P)
={}&4c^2(c+2)(c^2+2c+2)\\
 &\quad\cdot(8c^4+69c^3+204c^2+206c+36)>0,\\
\operatorname{disc}_x(Q)&=c^2(4c+1)>0,\\
\operatorname{Res}_x(P,Q)&=-c^7(c^2+2c+2)\ne0.
\end{aligned}
\]

Therefore, for every `c>0`, `P` has three distinct real roots

\[
 p_1(c)<p_2(c)<p_3(c),
\]

and `Q` has two distinct real roots `q_1(c)<q_2(c)`.  All five labelled roots
vary continuously with `c`, and no `q_i` can cross any `p_j` because the
resultant never vanishes.

It remains to determine the order once.  At `c=1`,

\[
 P=15x^3-22x+10,\qquad Q=11x^2-15x+5,
\]

and

\[
 q_2=\frac{15+\sqrt5}{22}>0,
 \qquad
 P(q_2)=\frac{95-56\sqrt5}{1331}<0.
\]

The final sign is exact because `56^2*5>95^2`.  Also `P(0)=10>0`, while
the positive-leading cubic is negative at negative infinity, so its first
root is negative.  Hence the positive point `q_2` at which `P<0` lies between
`p_2` and `p_3`.  In particular,

\[
 q_2(1)<p_3(1).
\]

Continuity plus the nonzero resultant now gives the global strict ordering

\[
 q_2(c)<p_3(c)\qquad(c>0).                              \tag{1}
\]

This is the symbolic replacement for the earlier `0.00264` single-channel
gap.

## 4. Distinguished-component membership

Because `C_delete=cP`, any path from the positive orthant inside
`{C_delete>0}` must retain `c>0`.  For fixed `c>0`, the rightmost positive
interval of the cubic is `x>p_3(c)`.  It contains the positive-activity
region.  Indeed,

\[
 P(1,c)=c^2(c+2)>0
\]

and, for `x>=1`,

\[
 \partial_xP=3A(c)x^2-2H(c)
 \ge 3A(c)-2H(c)=c(3c^2+10c+10)>0.
\]

Thus `p_3(c)<1` for every `c>0`.  The set

\[
 \mathcal S=\{(x,c):c>0,\ x>p_3(c)\}
\]

is exactly the sliced positivity component containing the positive orthant.
Membership in the **full** deletion component is witnessed without assuming
that a positive polynomial value suffices.  From any `(x,c)` in `S`:

1. move `x` to `1` at fixed `c`, staying to the right of `p_3(c)`;
2. move `c` to `1` at `x=1`, where
   `C_delete=cP(1,c)=c^3(c+2)>0`;
3. move `x` from `1` to `2` at `c=1`, ending at
   `a=b=c=d=1`.

This is an explicit continuous path in the original four-variable
`{C_delete>0}` set to a strictly positive activity vector.  Every point of
`S` is therefore in the deletion distinguished component.

## 5. Strict sign of `xi`

The quadratic `Q` has positive leading coefficient `H(c)`.  By (1), every
`x>p_3(c)` also satisfies `x>q_2(c)`, so

\[
 Q(x,c)>0.
\]

Since `c>0` on `S`, it follows strictly that

\[
 \xi_e=2cQ>0\qquad\text{on }\mathcal S.
\]

There is consequently no `Q<=0` point with the required explicitly proved
component membership anywhere on this natural two-variable component.

## 6. Reproduction and boundary

The symbolic checks were run with the campaign limits:

```bash
AMRA_MEMORY_KIB=5242880 AMRA_TIMEOUT_SECONDS=1800 \
  amra-research-loop/scripts/run_bounded.sh python \
  amra-research-loop/campaigns/opg-1757-mechanism-reset/evidence/w4_spoke_c_component_proof.py
```

They exited `0` in under one second.  No Lean process was started.

What is proved:

- exact root ordering and strict `xi>0` on the complete natural sliced
  component `S`;
- explicit membership paths from every point of `S` into the full deletion
  distinguished component.

What remains open:

- whether every point of the full deletion component satisfying `b=a,d=c`
  must lie in `S` (off-slice paths could in principle join another sliced
  positivity island);
- domination on the full stabilizer four-variable component;
- the moving-edge lemma for `W4` or arbitrary graphic matroids.

No OPG-1757 promotion follows.  The useful next target is to retain one of
the two splittings `b-a` or `d-c` and seek a resultant/SOS deformation of
the strict root separation above.
