# Erdős #809 red-team addendum: a zero-star's colour mass is paid by \(D_B\)

Date: 2026-08-02

Status: PROVED__INDEPENDENTLY_AUDITED

## 0. Result

Let \(b\in B\) be the centre of any active zero-shore star with leaf
set \(L\). For each leaf \(c\), let

\[
 h_c=|\{\gamma:b,c\in Y_\gamma\}|,
\qquad
 H=\sum_{c\in L}h_c.
\]

Then the exact outer-\(B\) colour defect satisfies

\[
\boxed{H\le D_B.}
\tag{1}
\]

This holds for same- and opposite-neighbourhood stars, with no reserve
assumption and no requirement that different leaves have disjoint
colour supports.

For a star selected by an inclusion-maximal repeated-zero matching,
write \(\ell=|L|\), \(W=H-\ell\), and \(f=|F|\). The inherited
concentration inequality \(E_0/(4f)\le W\) then gives

\[
\boxed{
 E_0\le4f(D_B-\ell).
}
\tag{2}
\]

A selected repeated-zero leaf has \(h_c\ge2\). Consequently

\[
\boxed{
 2\ell\le H\le D_B,\qquad \ell\le\lfloor D_B/2\rfloor.
}
\tag{3}
\]

A negative right side means that the selected star branch is
impossible. Equations (1)--(3) are additional explicit necessary
constraints in both B-same and B-opposite.

## 1. Proof

For each colour \(\gamma\), put

\[
 k_\gamma=
 |\{c\in L:b,c\in Y_\gamma\}|.
\]

If \(k_\gamma>0\), then \(Y_\gamma\) contains the centre \(b\) and
those \(k_\gamma\) distinct leaves. Hence

\[
 t_\gamma=|Y_\gamma|\ge k_\gamma+1,
\]

and therefore

\[
 (t_\gamma-1)_+\ge k_\gamma.
\]

For \(k_\gamma=0\) the same inequality is trivial. Summing over all
colours gives

\[
 D_B=\sum_\gamma(t_\gamma-1)_+
 \ge\sum_\gamma k_\gamma.
\]

Double-counting leaf--colour incidences gives

\[
 \sum_\gamma k_\gamma
 =\sum_{c\in L}|\{\gamma:b,c\in Y_\gamma\}|
 =H,
\]

which proves (1). The selected-star concentration and
\(W=H-\ell\) prove (2).

The unused defect has an exact nonnegative decomposition:

\[
 D_B-H
 =\sum_{\gamma:k_\gamma>0}
   (t_\gamma-1-k_\gamma)
  +\sum_{\gamma:k_\gamma=0}(t_\gamma-1)_+.
\tag{4}
\]

For \(k_\gamma>0\), the summand is precisely the number of outer
endpoints of that colour other than the centre and its selected
supported leaves. Thus equality in (1) has a literal support
description, rather than being only a numerical possibility.

## 2. Scope

The bound is exact: if every relevant colour has outer endpoint set
consisting of \(b\) and its supported leaves, and no other colours
contribute to \(D_B\), then \(D_B=H\).

Equation (2) does not alone eliminate a branch when \(fD_B\) is large.
Its value is that the star colour mass used by \(x_0,y_0\) is not a
free parameter; it is linearly capped by the same global defect
already present in the canonical system.

## 3. Reproduction

\[
\texttt{python3 verify\_erdos809\_zero\_star\_defect\_mass.py}
\]

The verifier exhausts finite families of colour supports and optional
extra outer endpoints. The all-parameter result is the proof above.
