# Erdős #1083: transverse nonzero-difference compression

Date: 2026-08-01

## 0. Result

In the transverse-heavy branch of the tangent-overlap dichotomy, one
can force a **nonzero** tangent difference \(\delta\) that is carried
by many distinct transverse row pairs.

At the frozen endpoint, the resulting directed graph has

\[
 t^{8/9+o(1)}
\]

ordered transverse edges, all satisfying the same quadratic
difference equation.  Consequently one row has
\(t^{1/6+o(1)}\) partners on that same nonzero difference.

This is weaker in raw exponent than the all-pair fixed-difference
count, but it removes two degeneracies simultaneously:

- every selected row pair is rationally transverse; and
- the selected tangent difference is nonzero.

The theorem uses the global difference-multiplicity repair rather
than the invalid direct-projection step audited elsewhere.

## 1. Setup

Let \(I\) be an exact identical-spectrum block of \(q\) rows:

\[
 V=(\rho^2+z_i^2+T_i)\oplus(2\rho z_iX),
\qquad i\in I,
\tag{1.1}
\]

where

\[
 |X|=S,\qquad |T_i|=U,\qquad
 T_i\subseteq T_*,\qquad |T_*|=R,
\]

and hence

\[
 |V|=B=SU.
\]

Assume \(S\ge2\).  The nonzero-difference statement below is made
under

\[
 R\ge2,\qquad N_\perp>0.
\tag{1.2a}
\]

These are not hidden endpoint assumptions.  If \(R=1\), every row
has the same singleton tangent set, so two exact common cells would
both equal the \(S\)-element set \(V\).  Fixed-tangent transverse
rigidity then forbids a transverse row pair when \(S\ge2\).  Thus
\(N_\perp=0\), and the transverse theorem is vacuous.  If
\(N_\perp=0\) directly, there is likewise no transverse branch to
compress.

Put

\[
 W_i=\operatorname{span}_{\mathbb Q}
 \bigl(2\rho z_i(X-X)\bigr).
\]

Let

\[
 \mathcal E_\perp
 =\{(i,j):i\ne j,\ W_i\cap W_j=\{0\}\}
\tag{1.2}
\]

be the ordered transverse row-pair set, and let
\(N_\perp=|\mathcal E_\perp|\).

## 2. Per-pair nonzero mass

Fix \((i,j)\in\mathcal E_\perp\).  Every \(v\in V\) gives a unique
coincidence record

\[
 v=\rho^2+z_i^2+\tau+2\rho z_ix
  =\rho^2+z_j^2+\tau'+2\rho z_jx'.
\tag{2.1}
\]

There are exactly \(B=SU\) such records.

If \(\delta=\tau'-\tau=0\), then \(\tau=\tau'\).  For each common
tangent square, fixed-tangent transverse rigidity says that the two
cells share at most one value.  Therefore the total number of
zero-difference records for \((i,j)\) is at most

\[
 |T_i\cap T_j|\le U.
\tag{2.2}
\]

Thus every ordered transverse row pair supplies at least

\[
 B-U=U(S-1)
\tag{2.3}
\]

records with nonzero tangent difference.

## 3. Global nonzero-difference theorem

### Theorem 1

Some nonzero \(\delta\in T_*-T_*\) supports at least

\[
 \boxed{
 \frac{N_\perp U(S-1)}{R^2-R}}
\tag{3.1}
\]

distinct projected tuples \((i,j,x,x')\) satisfying

\[
 z_i^2-z_j^2+2\rho(z_ix-z_jx')=\delta,
\tag{3.2}
\]

where every \((i,j)\) is transverse.

Moreover, for a fixed transverse ordered pair and fixed \(\delta\),
there is at most one source pair \((x,x')\).  Hence (3.1) is also a
lower bound for the number of distinct ordered transverse row pairs
carrying this one nonzero \(\delta\).

#### Proof

By (2.3), the total number of nonzero-difference records across
\(\mathcal E_\perp\) is at least

\[
 N_\perp U(S-1).
\tag{3.3}
\]

For \(\delta\ne0\), define

\[
 \mu_\perp(\delta)
 =\max_{(i,j)\in\mathcal E_\perp}
 |\{\tau\in T_i:\tau+\delta\in T_j\}|.
\tag{3.4}
\]

Exactly as in the repaired global difference theorem, if
\(C_\delta^\perp\) is the number of full records and
\(M_\delta^\perp\) the number of distinct projected tuples, then

\[
 C_\delta^\perp
 \le\mu_\perp(\delta)M_\delta^\perp.
\tag{3.5}
\]

The common tangent universe gives

\[
 \mu_\perp(\delta)\le r_{T_*}(\delta).
\]

Since the zero-difference fibre consists of the \(R\) diagonal
ordered tangent pairs,

\[
 \sum_{\delta\ne0}r_{T_*}(\delta)=R^2-R.
\tag{3.6}
\]

Therefore

\[
 \sum_{\delta\ne0}\mu_\perp(\delta)\le R^2-R.
\tag{3.7}
\]

Combine (3.3), (3.5), and (3.7) to obtain (3.1).

Finally, suppose the same transverse ordered pair \((i,j)\) and the
same \(\delta\) admitted two distinct source pairs
\((x_1,x'_1)\ne(x_2,x'_2)\).  Subtracting their two copies of (3.2)
gives

\[
 2\rho z_i(x_1-x_2)
 =2\rho z_j(x'_1-x'_2).
\]

The common value is nonzero: if either difference vanished, the
other would vanish because the heights are nonzero, contradicting
distinctness of the source pairs.  It therefore belongs to both
\(W_i\) and \(W_j\), contrary to transversality.  Hence each
projected tuple at fixed \(\delta\) has a different ordered row pair,
which justifies identifying the tuple count in (3.1) with a row-pair
count.
\(\square\)

## 4. Input from the tangent-transversality branch

Recall

\[
 P_\perp
 =\sum_{(i,j)\in\mathcal E_\perp}|T_i\cap T_j|.
\tag{4.1}
\]

Since each intersection has size at most \(U\),

\[
 N_\perp\ge \frac{P_\perp}{U}.
\tag{4.2}
\]

In the transverse-heavy branch,

\[
 P_\perp\ge\frac12
 \left(\frac{q^2U^2}{R}-qU\right)
 =\frac{P_0}{2}.
\tag{4.3}
\]

Combining (3.1)--(4.3) gives:

### Corollary 2

Some nonzero difference supports at least

\[
 \boxed{
 \frac{P_0(S-1)}{2(R^2-R)}}
\tag{4.4}
\]

distinct ordered transverse row pairs.

## 5. Frozen exponents

At

\[
 q=t^{13/18+o(1)},\quad
 U=t^{5/6+o(1)},\quad
 S=t^{7/9+o(1)},\quad
 R=t^{1+o(1)},
\]

we have

\[
 P_0=t^{19/9+o(1)}.
\]

Equation (4.4) has exponent

\[
 \frac{19}{9}+\frac79-2
 =\boxed{\frac89}.
\tag{5.1}
\]

Thus one nonzero \(\delta\) carries

\[
 t^{8/9+o(1)}
\]

ordered transverse row pairs.  Since there are
\(q=t^{13/18+o(1)}\) possible first rows, one row has at least

\[
 t^{8/9-13/18+o(1)}
 =\boxed{t^{1/6+o(1)}}
\tag{5.2}
\]

distinct partners on the same \(\delta\).

The source set has size \(S=t^{7/9}\), so (5.2) still does not force
a repeated source value by pigeonhole.  The theorem creates a
nonzero, transverse, fixed-difference graph; converting it to an
affine-height chart remains open.

## 6. Claim boundary

The theorem proves a genuine algebraic compression of the
transverse-heavy branch.  It does not show that the selected graph
contains a large clique, that its source labels repeat, or that its
heights have bounded rational complexity.  It therefore does not
close #1083.
