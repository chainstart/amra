# G202 first kill test: exact spoke negative island

## Outcome

The full marked-spoke stabilizer polynomial has the exact rational point

\[
 (a,b,c,d)=(-8,1/8,8,7),\qquad P=294896>0,\qquad \xi=-16<0.
\]

This point does **not** kill G202: it lies outside the full distinguished
positivity component of `P`.  Its exclusion is exact and uses convexity of the
already established Gårding component, not a finite connectivity scan.
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

The spoke deletion is a series extension of `M(K4)` and its `C`-Gårding
status was already established from the Fang--Ma six-element base theorem
and series-extension closure.  A distinguished Gårding positivity component
is convex.  If `v` belonged to that component together with the positive
anchor `u`, their entire segment would lie in it and hence in `{P>0}`.  The
displayed negative segment value is a contradiction.  Therefore `v` is
outside the **full** distinguished component, not merely outside the natural
fibre component.

## Status and scope

The initial bounded scan served only to locate the rational candidate.  The
reported point values, forest reconstruction, fibre barrier, and global
component exclusion are exact.  The scan is not complete and supplies no
evidence that all negative points are excluded.

- G202: survives this exact first kill test; not proved.
- Full four-variable spoke domination: open.
- Rim orbit: not used.
- Campaign phase: remains `mechanism_falsification`.
- OPG-1757 and its global interface: unchanged.

Reproduction, without Lean:

- `evidence/verify_g202_spoke_exact_negative_island.py`, SHA-256
  `fdb8ed637cfe71e9f104402ea9b159aa3cc34ea45063678def084091390cd994`
- `evidence/G202_SPOKE_EXACT_NEGATIVE_ISLAND.json`, SHA-256
  `d39f2dc2d18b92084aae2c007b54b5bc947948497aa398ecc10f156bd83e5d28`

```sh
ulimit -v 2097152
timeout 120s python3 evidence/verify_g202_spoke_exact_negative_island.py
```
