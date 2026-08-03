# Independent audit: typed-chain scoped no-go

Verdict: **pass as a scoped no-go; reject exponent promotion**.

## Blind type reconstruction

Starting from the frozen simultaneous-switch normal form, rather than the
author's summary, gives

\[
F_j=GR_j,\qquad P_{A_0}=GB,\qquad B=R_jQ_j,\qquad
P_{A_j}=F_0Q_j.
\]

Here `F_j=P_(lambda_j X)` is a positive `0/1` set mask: the index `j`
changes the scalar applied to the one common set `X`.  By contrast, `Q_j` is
defined separately in each row by Laurent-domain division `B=R_jQ_j`.  It
may have negative coefficients.  The frozen data include no polynomial,
Laurent-polynomial, or set-valued family `Q(T)` satisfying
`Q(lambda_j)=Q_j`; nor do they define an operation that substitutes the set
`lambda_j X` into `Q_j`.

Thus `Q_j(lambda_j X)` is not merely unjustified notation: it has no type in
the frozen normal form.  Its coefficient Jacobian is likewise undefined.
The decisive lemma correctly kills only the proposed M01-to-M05 implication
in that formulation.  It does not rule out supplying a new family `Q(T)` and
proving its compatibility.

## Replacing `Q_j` by `F_j`

This replacement restores the scalar-copy type, but the inherited
heavy-factor theorem already begins with

\[
G\mid F_j=P_{\lambda_jX}.
\]

Newton-polytope additivity then puts every fixed nonzero direction `h` of
`G` in `lambda_j W`, where `W=span_Q(X-X)`.  Hence
`h=lambda_j w_j` for some nonzero `w_j in W`, and the common-tangent height
and cell become

\[
z_j={h\over2\rho w_j},\qquad
\rho^2+\tau_0+{h^2\over4\rho^2w_j^2}+{h\over w_j}X.
\]

Therefore replacing the quotient by the correctly typed source mask is
already absorbed **for the advertised common-X-to-reciprocal-chart output**.
This does not show that every future invariant built from `F_j` is redundant:
one producing information strictly beyond the existing chart would be a new
claim.

## Independent exponent ledger

The frozen endpoint supplies

\[
K=t^{5/9-o(1)},\quad S=t^{7/9+o(1)},\quad
U=t^{5/6+o(1)},\quad q=t^{13/18+o(1)}.
\]

The heavy-factor pigeonhole divides by at most `log_2 U`, and the same-sign
selection divides by two.  Both are `t^o(1)` losses, so the retained row
exponent is still `5/9-o(1)`.

The width formula on that same-sign class is

\[
\|q_{j,\tau_0}-q_{k,\tau_0}\|^2
=\frac{(b_j-b_k)^2}{4\rho^2D^2}.
\]

The `b_j` are distinct.  Fixing an extreme `b_j` makes the remaining
absolute differences distinct, so these are `K-1` genuine target--target
squared-distance labels, not merely formal parameters.  Their exponent is
only `5/9`, leaving

\[
3-\frac59=\frac{22}{9}
\]

before even asking for a fixed positive improvement above the cubic label
threshold.

Finally,

\[
\frac59+\frac79+\frac56+\frac{13}{18}=\frac{26}{9},
\qquad 3-\frac{26}{9}=\frac19.
\]

This arithmetic is correct.  Its interpretation must remain the author's
stated weak one: `26/9` is an optimistic formal product of all native counts.
Those counts are not proved independent, and this product is neither an
incidence bound nor an injective count of distance labels.

## Closure and scope

The decisive lemma is independently reconstructed at evidence level 2 as a
local, typed no-go.  It neither improves the public dimension-three `3/5`
exponent nor supplies the missing M1083R2-10 collision theorem.  Promotion
under the frozen `main_exponent_improved` contract must therefore be rejected.

The independent checker ran under 512 MiB virtual memory and a 120-second
timeout and completed successfully.  No Lean process was used.
