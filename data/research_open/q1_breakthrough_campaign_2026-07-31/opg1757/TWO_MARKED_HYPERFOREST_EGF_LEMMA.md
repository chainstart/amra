# OPG-1757: a closed two-marked hyperforest EGF

Date: 2026-07-31

Status: `PROVED__ALL_EXCESS__ALL_COMPONENT_COUNTS`

The fixed-deficit computation previously generated the \(h=2\) endpoint
by enumerating nonbinary contraction-incidence types.  The following
closed species formula replaces that growing list by one two-marked path
kernel.

## 1. Statement

Put
\[
\Phi(t,u)=\frac{e^{ut}-1}{u},
\qquad
T=z e^{\Phi(T,u)},
\tag{1}
\]
and let
\[
V(t,u)
=t+\frac{e^{ut}-1-ut}{u^2}
-\frac{t(e^{ut}-1)}u
\tag{2}
\]
be the unrooted hypertree series.  For a distinguished block of weight
\(a\), define
\[
R_a(T,u)=e^{a\Phi(T,u)}.
\tag{3}
\]
For two labelled distinguished blocks of weights \(a,b\), define the
same-component series
\[
\boxed{
R_{a,b}(T,u)
=ab\,e^{(a+b)\Phi(T,u)}
\frac{e^{uT}}{1-Te^{uT}}.
}
\tag{4}
\]

Let \(H^{(a,b)}_{e,c}(s)\) be the weighted complete-hyperforest endpoint
on the profile
\[
(a,b,1^{s-a-b}),
\]
with total nonbinary excess \(e\) and \(c\) components.  Then, with
\(N=s-a-b\),
\[
\boxed{
\begin{aligned}
H^{(a,b)}_{e,c}(s)
=N![z^Nu^e]\bigg{&
R_{a,b}(T,u)\frac{V(T,u)^{c-1}}{(c-1)!}\\
&+\mathbf1_{c\ge2}R_a(T,u)R_b(T,u)
\frac{V(T,u)^{c-2}}{(c-2)!}
\bigg\}.
\end{aligned}
}
\tag{5}
\]
In particular, the disjoint prescribed-edge endpoint in the pooled
Rayleigh determinant is
\[
H_{2,e,c}(s)=H^{(2,2)}_{e,c}(s).
\tag{6}
\]
Equations (3) and (5), together with the unmarked formula
\[
H_{0,e,c}=s![z^su^e]\frac{V(T,u)^c}{c!},
\]
give one closed all-excess EGF description of all three endpoint profiles
\(h=0,1,2\).

## 2. Proof of the path kernel

A hyperedge incident to one distinguished root block and to \(k\) rooted
branches has weight marker
\[
a\,u^{k-1}\frac{T^k}{k!}.
\]
Taking a set of such incident edges gives (3).

Now place the two distinguished blocks in the same hypertree.  There is a
unique alternating path of vertices and hyperedges between them.  A path
hyperedge contains its two path vertices and any set of \(k\) off-path
rooted branches.  Its excess is \(k\), so its branch series is
\[
\sum_{k\ge0}\frac{(uT)^k}{k!}=e^{uT}.
\]
Every internal path vertex, together with all of its off-path incident
hyperedges, contributes one rooted hypertree \(T\).  Therefore a path of
one or more hyperedges contributes
\[
e^{uT}\sum_{j\ge0}(Te^{uT})^j
=\frac{e^{uT}}{1-Te^{uT}}.
\]
The two end blocks contribute their incidence weights \(ab\), and their
off-path incident hyperedges contribute
\(e^{a\Phi}e^{b\Phi}\).  This proves (4).

For a \(c\)-component forest, either the two marked blocks lie in the
same component, giving the first term of (5), or they lie in two distinct
labelled components, giving the second.  The remaining unmarked
components form an unordered set, hence the displayed factorials.  These
two cases are disjoint and exhaustive, proving (5).

## 3. Why this matters and what remains

Formula (5) removes the partition-of-excess incidence explosion from the
\(h=2\) endpoint: arbitrary excess is now encoded by the single geometric
path kernel \((1-Te^{uT})^{-1}\).  It is a plausible route to both:

- higher Laurent symbols beyond the newly proved leading symbol.

The companion `ENDPOINT_POLYNOMIALITY_THEOREM.md` uses the fact that this
path pole cancels exactly against the Lagrange Jacobian and proves endpoint
polynomiality and uniform fixed-deficit denominator cancellation.  Higher
Laurent symbols remain open.

The finite verifier applies Lagrange inversion directly to (5) and agrees
with the independent contraction recurrence at twelve small endpoint
values, including excess two and the extreme \(N=0\) cases.
