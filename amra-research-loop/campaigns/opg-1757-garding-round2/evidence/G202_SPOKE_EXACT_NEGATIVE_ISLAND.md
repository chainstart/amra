# G202 first kill test: exact spoke negative island

> **Erratum (2026-08-03).**  The original segment argument below incorrectly
> used `C`-Gårding status alone to infer convexity.  Fang--Ma,
> arXiv:2604.27755v2, Example 11.7 explicitly shows that an ordinary Gårding
> component need not be convex.  The point exclusion is nevertheless valid
> by the later, independently audited exact component theorem
> `FULL_SPOKE_DOMINATION_THEOREM.md`: after shifting `x=a+1`, the full
> distinguished component has `x>0`, whereas this point has `x=-7`.  The
> point values and fixed-fibre barrier in this note remain exact; the segment
> alone is not a component certificate.

## Outcome

The full marked-spoke stabilizer polynomial has the exact rational point

\[
 (a,b,c,d)=(-8,1/8,8,7),\qquad P=294896>0,\qquad \xi=-16<0.
\]

This point does **not** kill G202: it lies outside the full distinguished
positivity component of `P`.  Its exclusion is now supplied by the later
exact full-component characterization, not by convexity and not by a finite
connectivity scan.
G202 therefore survives this first broken-symmetry kill test but remains open.

## Full spoke reconstruction

For the marked spoke `01`, the stabilizer classes are

\[
 a:\{02,04\},\quad b:\{03\},\quad
 c:\{12,14\},\quad d:\{23,34\}.
\]

The verifier reconstructs `P=C_(M\\01)` by enumerating every forest of
`W4-01`; `xi` is the sub-sum whose forests already connect `0` to `1`.
There are respectively 86 and 38 such forests, reproducing
`P(1,1,1,1)=86` and `xi(1,1,1,1)=38` without importing the inherited
polynomial.

Writing the complete four-variable expressions as quadratics in `a` gives a
compact exact definition:

\[
 P=A_2a^2+A_1a+A_0,
\]

\[
\begin{aligned}
A_2={}&(b+1)(cd+c+d)(cd+c+d+2),\\
A_1={}&2(bc^2d^2+2bc^2d+bc^2+2bcd^2+4bcd+2bc\\
&\qquad +bd^2+2bd+c^2d^2+c^2d+2cd^2+2cd+d^2),\\
A_0={}&cd(c+2)(bd+2b+d),
\end{aligned}
\]

and

\[
 \xi=B_2a^2+B_1a+B_0,
\]

\[
\begin{aligned}
B_2={}&2(cd+c+d),\\
B_1={}&2(bcd^2+2bcd+2bc+bd^2+2bd+cd^2+2cd+d^2),\\
B_0={}&2cd(bd+2b+d).
\end{aligned}
\]

These are the full spoke stabilizer-variable polynomials; neither equality
`b=a` nor `d=c` is imposed.

## Exact island certificate

On the broken-symmetry fibre `(b,c,d)=(1/8,8,7)`,

\[
 P(a)=\frac{46647a^2+82830a+36400}{8},\qquad
 \xi(a)=\frac{568a^2+5007a+3640}{4}.
\]

Thus `a=-8` gives the negative point above, while

\[
 P(-4/5)=-31/25<0.
\]

This already proves that the negative point and `a=1` lie in different
positive intervals of this one-dimensional fibre.  Fibre separation alone
would not exclude an off-fibre path, so it is not used as the final component
argument.

Let `u=(1,1,1,1)` and `v=(-8,1/8,8,7)`.  At parameter `t=1/5`, their segment
contains

\[
 (1-t)u+tv=(-4/5,33/40,12/5,11/5)
\]

and exact substitution gives

\[
 P((1-t)u+tv)=-1009646/78125<0.
\]

The displayed negative segment value is exact, but it does **not** by itself
exclude `v` from an ordinary Gårding component: such components need not be
convex.  The valid global exclusion comes instead from the later theorem
`FULL_SPOKE_DOMINATION_THEOREM.md`, which proves that the full component is
the domain (3) there.  In its shifted coordinates `x=a+1`; every component
point has `x>0`, while `v` has `x=-7`.  Thus `v` is outside the **full**
distinguished component, with no convexity premise.

## Status and scope

The initial bounded scan served only to locate the rational candidate.  The
reported point values, forest reconstruction, and fibre barrier are exact;
the global exclusion is exact through the later full-component theorem.  The
scan itself is not complete and supplies no such completeness evidence.

- G202: survived this first test and was subsequently proved by
  `FULL_SPOKE_DOMINATION_THEOREM.md`.
- Full four-variable spoke domination: proved and independently audited in
  the later artifacts; not proved by this first-test note alone.
- Rim orbit: not used.
- Campaign phase at the time of this test: `mechanism_falsification`; the
  campaign is now frozen after its later audited results.
- OPG-1757 and its global interface: unchanged.

Reproduction, without Lean:

- `evidence/verify_g202_spoke_exact_negative_island.py`, SHA-256
  `5ae250c9b3a858f4e15dce6327ec4daefafc2a0c3a5b5856c29f46cc9e64109d`
- `evidence/G202_SPOKE_EXACT_NEGATIVE_ISLAND.json`, SHA-256
  `45630bc9db949b7b1a67ff39f891646cba49df15113a2896d07724b4fa285f05`

```sh
ulimit -v 2097152
timeout 120s python3 evidence/verify_g202_spoke_exact_negative_island.py
```
