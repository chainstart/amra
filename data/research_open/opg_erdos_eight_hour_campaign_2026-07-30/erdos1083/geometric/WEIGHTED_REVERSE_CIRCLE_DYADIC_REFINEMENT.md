# Erdős #1083: weighted reverse-circle dyadic refinement

Date: 2026-07-30

## 0. Result

Fix the source plane and the retained positive-radius,
incidence-active reverse-circle triples from
`EUCLIDEAN_HUB_INCIDENCE_EXPANSION_THEOREM.md`.  Merge equal normalized
circle equations.  Let
\[
w_C=\#\{(\beta,q,d):\Gamma_{\beta,q,d}=C\},
\qquad
\mu=\max_Cw_C,
\tag{1}
\]
and let
\[
\mathsf T=\sum_Cw_C\le MQL
\tag{2}
\]
be the total triple weight.  If the source point set has size at most
\(Q\), then the weighted incidence count satisfies
\[
\boxed{
\begin{aligned}
W:=\sum_Cw_C|P_\alpha\cap C|
\ll{}&
Q^{2/3}\mathsf T^{2/3}\mu^{1/3}\\
&+
Q^{6/11}\mathsf T^{9/11}\mu^{2/11}t^{o(1)}\\
&+Q\mu+\mathsf Tt^{o(1)}.
\end{aligned}}
\tag{3}
\]

At the critical hub parameters
\[
M=t^{1+o(1)},\qquad
Q=t^{3+o(1)},\qquad
L=t^{2-2\kappa-o(1)},\qquad
\mathsf T\le t^{6-2\kappa+o(1)},
\tag{4}
\]
the hub mass \(W\ge t^{7-3\kappa-o(1)}\) forces
\[
\boxed{
\mu\ge t^{(5-15\kappa)/2-o(1)}
\qquad(\kappa<1/3).
}
\tag{5}
\]

For \(\kappa<1/5\), the exponent in (5) is larger than \(1\).
Fixed-plane injectivity gives \(\mu\le M=t^{1+o(1)}\), recovering the
impossibility of the hub in that range.  For
\(1/5\le\kappa<1/3\), equation (5) is a strict improvement over the
previous coarse exponent \((5-15\kappa)/11\).

This strengthens the structural repeated-circle conclusion but does
not by itself improve the \(3/5\) distinct-distance exponent.

## 1. Dyadic weighted incidence bound

For dyadic \(u=2^j\le\mu\), put
\[
\mathcal C_u=\{C:u\le w_C<2u\},\qquad n_u=|\mathcal C_u|.
\tag{6}
\]
Since the total weight is \(\mathsf T\),
\[
n_u\le\frac{\mathsf T}{u}.
\tag{7}
\]
The circles in \(\mathcal C_u\) are distinct because equal normalized
equations were merged before forming the classes.

The planar point--circle theorem gives
\[
I(P_\alpha,\mathcal C_u)
\ll
Q^{2/3}n_u^{2/3}
+Q^{6/11}n_u^{9/11}t^{o(1)}
+Q+n_u.
\tag{8}
\]
Multiplying by the upper weight \(2u\) in this layer and using (7)
gives
\[
\begin{aligned}
\sum_{C\in\mathcal C_u}w_C|P_\alpha\cap C|
\ll{}&
Q^{2/3}\mathsf T^{2/3}u^{1/3}\\
&+Q^{6/11}\mathsf T^{9/11}u^{2/11}t^{o(1)}\\
&+Qu+\mathsf T.
\end{aligned}
\tag{9}
\]

The first three terms are geometric sums in \(u\), dominated by the
largest layer \(u\le\mu\).  The last term is repeated only
\(O(\log\mathsf T)=t^{o(1)}\) times.  Summing (9) proves (3).

No injectivity is needed for this dyadic step.  Injectivity is used
only for the separate upper bound \(\mu\le M\): on one fixed target
plane \(\beta\), the map \((q,d)\mapsto\Gamma_{\beta,q,d}\) is
injective, so one merged circle class receives at most one triple
from that plane.

## 2. Empty and zero-radius equations

Empty circle equations contribute no incidence and are deleted.
A zero-radius equation contributes at most one source incidence.
There are at most \(MQL=\mathsf T_{\max}\) triples, so all zero-radius
terms contribute at most
\[
t^{6-2\kappa+o(1)}.
\tag{10}
\]
For fixed \(\kappa<1\), this is negligible compared with
\[
LH=t^{7-3\kappa-o(1)}
\tag{11}
\]
because the exponent gap is \(1-\kappa>0\).  Hence the retained
positive-radius weighted incidence count still has the lower bound
used in (5).

The perpendicular target plane was removed before the
matching-or-hub extraction and is not charged to (3).

## 3. Exact exponent audit

Write
\[
\mu=t^{m+o(1)}.
\]
The four terms in (3) have exponents
\[
\begin{array}{c|c}
\text{term}&t\text{-exponent}\\ \hline
Q^{2/3}\mathsf T^{2/3}\mu^{1/3}
&6-\frac{4\kappa}{3}+\frac m3\\[1mm]
Q^{6/11}\mathsf T^{9/11}\mu^{2/11}
&\frac{72}{11}-\frac{18\kappa}{11}+\frac{2m}{11}\\[1mm]
Q\mu&3+m\\
\mathsf T&6-2\kappa.
\end{array}
\tag{12}
\]
To reach the hub exponent \(7-3\kappa\), the first three terms would
respectively require
\[
m\ge3-5\kappa,\qquad
m\ge\frac{5-15\kappa}{2},\qquad
m\ge4-3\kappa.
\tag{13}
\]
For every \(\kappa>0\),
\[
\frac{5-15\kappa}{2}
<
3-5\kappa
<
4-3\kappa.
\tag{14}
\]
The fourth term misses the hub exponent by \(1-\kappa>0\).
Therefore, if
\[
m<\frac{5-15\kappa}{2}-o(1),
\]
all four terms in (3) are too small, a contradiction.  This proves
(5).  The lower bound is nontrivial exactly for \(\kappa<1/3\).

## 4. Scope

The refinement is unconditional inside the existing fixed-plane hub
branch.  It does not assert that the lower bound (5) is attainable,
nor that one repeated circle expands distances.  The aligned
circle--axis barriers remain compatible with large multiplicity.
