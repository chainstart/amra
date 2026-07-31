# Erdős #1083 Route D: what would actually move the \(2/9\) endpoint?

Date: 2026-07-30

## 0. Stage conclusion

\[
\boxed{\text{No unconditional power saving at }\kappa=2/9
\text{ was obtained in Route D.}}
\]

The strongest proved information is:

1. the collinear-centre proof itself passes and gives the strict
   structural threshold \(2/9\);
2. at its endpoint, same-height distance collisions miss the required
   collision mass by \(t^{5/9-o(1)}\);
3. exact row-minimal sumsets are impossible by \(t^{1/9-o(1)}\);
4. nevertheless, a genuine Euclidean rich reverse-circle fibre has
   only \(O(UH)\) cross distances if it is allowed \(UH\) fresh target
   planes and labels.

Thus the remaining issue is neither the cross-distance polynomial
alone nor same-height sum-product.  It is the simultaneous reuse of
only \(M\) global target planes and \(L\) global labels across many
centre heights and signed centres.

## 1. Live endpoint data

The scalar endpoint of
`../route_b/COLLINEAR_CENTER_LINEARIZATION_THEOREM.md` is
\[
\begin{aligned}
S&=t^{7/9+o(1)},&
U&=t^{5/6+o(1)},\\
H&=t^{19/9+o(1)},&
R_A&=t^{19/18+o(1)},\\
M&=t^{1+o(1)},&
D&=t^{3+o(1)}.
\end{aligned}
\tag{1}
\]
Here \(S\) is source-circle richness, \(U\) is circle multiplicity,
\(H\) is the number of circles over one signed parameter line,
\(R_A\) is the number of active signed centre coordinates, and
\(M\) bounds the global tangent-square set at one fixed \(A\).

For one fibre, the exact cross-distance relation is
\[
v=\rho^2+\tau+z^2+2\rho zx,
\qquad
\tau\in T_z\subset T_\ast,\quad |T_\ast|\le M.
\tag{2}
\]

## 2. The collision target and its \(1/18\) slack

One fibre supplies
\[
SUH=t^{67/18+o(1)}
\tag{3}
\]
source--target tuples.  If their values lie in the global
\(D=t^{3+o(1)}\) distance set, Cauchy--Schwarz requires collision
energy
\[
\mathcal E\ge t^{40/9-o(1)}.
\tag{4}
\]
The multi-dilate energy theorem bounds the same-height part by
\[
\mathcal E_{\rm same}\ll
t^{1+7/9+19/9+o(1)}
=t^{35/9+o(1)}.
\tag{5}
\]
Therefore cross-height collisions must contribute
\[
\boxed{\mathcal E_{\rm cross}\ge t^{40/9-o(1)}.}
\tag{6}
\]

A natural coarse benchmark is
\[
S^2UH=t^{9/2+o(1)}.
\tag{7}
\]
The difference between (7) and the required exponent (6) is
\[
\boxed{\frac92-\frac{40}{9}=\frac1{18}.}
\tag{8}
\]
Consequently, a proposed estimate
\[
\mathcal E_{\rm cross}
\ll t^{-\delta}S^2UH
\tag{9}
\]
contradicts the endpoint only when
\[
\boxed{\delta>\frac1{18}.}
\tag{10}
\]
An arbitrary positive \(\delta\) is not enough.  This is because the
one-line target fibre has size
\[
UH=t^{53/18+o(1)},
\]
leaving \(t^{1/18+o(1)}\) slack below the global distance budget.

Aggregating all \(R_A\) signed centres does not remove this numerical
floor by itself.  The full tuple count is \(t^{43/9+o(1)}\), so the
global collision lower exponent is \(59/9\), while the corresponding
coarse benchmark
\[
R_A^2S^2UH
\]
has exponent \(119/18\), again larger by exactly \(1/18\).

## 3. Exact row-minimality is already excluded

Let \(T_z\subset T_\ast\) be a row of \(U\) tangent squares.  If every
row attained
\[
|T_z+2\rho zX|=U+S-1,
\tag{11}
\]
then the equality case of the real sumset inequality forces \(X\)
and every \(T_z\) to be arithmetic progressions with compatible
gaps.  Endpoint pairs in the \(M\)-element global set \(T_\ast\)
then give
\[
H\le M(M-1).
\tag{12}
\]
At (1),
\[
H=t^{19/9+o(1)}
\quad\text{and}\quad
M^2=t^{2+o(1)},
\]
so literal equality fails by \(t^{1/9-o(1)}\).

This does not control rows of size \(O(U)\): since
\(U/S=t^{1/18+o(1)}\), constant-factor small sumsets are far from the
exact equality regime.

## 4. Saving-to-threshold conversions

The location of a saving matters.  The following conversions have
been checked algebraically.  They are local conversions for
\(\delta\) small enough that the inherited point--circle,
rich-line, and \(+RQ\)-branch ranges remain unchanged.

### 4.1 Saving in the fixed-\(A\) incidence main term

Suppose the main term of the summed fixed-\(A\) incidence estimate
improves by \(t^{-\delta}\):
\[
I(P_\alpha,\mathcal C)
\ll
t^{-\delta}Q^{2/3}R_A^{1/3}N^{2/3}
+R_AQ+N.
\tag{13}
\]
When the main term carries,
\[
3a+b\le6+r-3\delta.
\]
Repeating the scalar proof gives
\[
m\le\frac{1+3\kappa-3\delta}{2},
\]
and comparison with
\[
m\ge\frac{5-15\kappa}{2}
\]
forces
\[
\boxed{
\kappa\ge\frac29+\frac{\delta}{6}.
}
\tag{14}
\]

### 4.2 Saving in rich-line count or target capacity

If instead a factor \(t^{-\delta}\) improves either
\[
c\le6-4\kappa-3m-\delta
\]
or
\[
r+h+m\le4-\delta,
\]
the final upper bound on \(m\) gains only \(\delta/2\), and the
threshold becomes
\[
\boxed{
\kappa\ge\frac29+\frac{\delta}{18}.
}
\tag{15}
\]

Equations (14)--(15) must not be interchanged: a saving before the
one-third exponent in the fixed-\(A\) incidence term is multiplied by
three after clearing denominators.

### 4.3 A cross-energy saving

The estimate (9) is not yet a scalar incidence saving.  Even after
\(\delta>1/18\) excludes the exact endpoint, no interval
\[
\kappa<\frac29+c(\delta)
\]
follows until (9) is proved uniformly for every nearby dyadic ledger
and translated into one of the inequalities used in the scalar
linear program.  Claiming either (14) or (15) directly from (9) would
be unjustified.

## 5. Strongest precise next lemma

A sufficient next theorem is:

> **Global-reuse cross-height theorem.**  In every regular
> fixed-\((A,\rho)\) fibre satisfying (1)--(2),
> \[
> \mathcal E_{\rm cross}
> \ll t^{-1/18-\epsilon}S^2UH
> \]
> for some absolute \(\epsilon>0\), unless the target-plane/label
> incidence graph has an explicitly classified exceptional form.

The exceptional form cannot merely say that individual \(T_z\)'s are
arithmetic progressions: the Euclidean cancellation model shows that
fresh rows can cancel the cross term perfectly.  It must use
\[
T_z\subset T_\ast,\qquad |T_\ast|\le M,
\]
and, for a global result, the common selected-label set of size \(L\).

No such theorem is proved here.  The exact target, exponent floor,
and threshold conversions are now explicit.

## 6. Reproduction

```bash
cd data/research_open/erdos1083_two_hour_q1_attack_2026-07-30/route_d
python3 verify_two_ninths_audit.py
pytest -q test_verify_two_ninths_audit.py
```
