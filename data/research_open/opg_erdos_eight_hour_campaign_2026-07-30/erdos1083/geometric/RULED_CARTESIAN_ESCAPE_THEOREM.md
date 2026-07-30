# Erdős #1083: distance expansion of ruled Cartesian axial grids

Date: 2026-07-30

## 0. Result

The power-sharp transfer obstruction
\[
p_{j,a,z}=(a,ja,z)
\]
is not itself a few-distance configuration.  The following theorem
shows that this is robust for every full integer Cartesian subgrid,
not just for intervals.

### Theorem 1

Let
\[
J\subseteq[-T,T]\cap\mathbb Z,\qquad
A\subseteq[1,T]\cap\mathbb Z,\qquad
Z\subseteq[-T,T]\cap\mathbb Z
\]
be nonempty, with \(|J|\ge2\).  Put
\[
P(J,A,Z)
=\{(a,ja,z):j\in J,\ a\in A,\ z\in Z\}
\subset\mathbb R^3.
                                                        \tag{1}
\]
Then
\[
\boxed{
|\Delta^2(P(J,A,Z))|
\ge
\frac{(|J|-1)|A||Z|}
{\displaystyle 4
 \max_{1\le n\le 8T^4}\tau(n)^2}.
}                                                       \tag{2}
\]
In particular, if \(T\le |P|^C\) for a fixed \(C\), then
\[
\boxed{
|\Delta(P(J,A,Z))|
\ge (|J|-1)|A||Z|\,|P|^{-o(1)}.
}                                                       \tag{3}
\]

At the inherited critical sizes
\[
|J|=N^{1/5-o(1)},\qquad
|A||Z|=N^{3/5-o(1)},
\]
equation (3) gives
\[
\boxed{
|\Delta(P)|\ge N^{4/5-o(1)}.
}                                                       \tag{4}
\]
Thus a full polynomial-coordinate ruled Cartesian grid is incompatible
with the assumed \(N^{3/5+o(1)}\) distance count.

## 1. Proof

Choose \(j_0=\min J\), an anchor \(z_0\in Z\), and put
\[
L=\{j-j_0:j\in J\setminus\{j_0\}\},
\qquad
U=\{z-z_0:z\in Z\}.
\]
Then
\[
|L|=|J|-1,\qquad |U|=|Z|.
                                                        \tag{5}
\]
For every \(a\in A\), \(\ell=j-j_0\in L\), and
\(u=z-z_0\in U\), both points
\[
(a,ja,z),\qquad(a,j_0a,z_0)
\]
belong to (1), and their squared distance is
\[
\boxed{(a\ell)^2+u^2.}                                \tag{6}
\]

Let
\[
X=A\cdot L=\{a\ell:a\in A,\ \ell\in L\}.
\]
Every nonzero integer \(x\) has at most \(\tau(|x|)\) representations
as \(a\ell\), even before imposing \(a\in A,\ell\in L\).  Since
\(|a\ell|\le2T^2\),
\[
|X|
\ge
\frac{|A||L|}
{\max_{1\le n\le2T^2}\tau(n)}.                       \tag{7}
\]

Now map \(X\times U\) to the distance label \(x^2+u^2\).
This label is a positive integer at most
\[
(2T^2)^2+(2T)^2\le8T^4.
\]
For a fixed positive \(n\), its number of ordered signed
representations as \(x^2+u^2=n\) is
\[
r_2(n)\le4\tau(n).
                                                        \tag{8}
\]
Combining (7)--(8) proves (2).  The standard uniform divisor
bound
\[
\max_{n\le X}\tau(n)=X^{o(1)}
\]
gives (3) under the polynomial coordinate-range hypothesis, and (4)
is its critical specialization.
\(\square\)

## 2. A scaled rational version

The same conclusion holds if all \(j,a,z\) have one common denominator
\(D\) of polynomial height and their numerators have polynomial height.
Because the second Cartesian coordinate is the product \(ja\), the
correct common coordinate scaling is \(D^2\), not \(D\):
\[
D^2(a,ja,z)=(D^2a,D^2ja,D^2z)\in\mathbb Z^3.
\]
This multiplies every squared distance by the single nonzero factor
\(D^4\) and does not change the number of labels.  The assumed
polynomial bound on \(D\) keeps the resulting integer coordinate range
polynomial, so the divisor estimate still contributes only
\(|P|^{o(1)}\).

Different independent denominators cannot be cleared for free: their
least common multiple may be exponentially large, making the divisor
bound useless at the \(N^{o(1)}\) scale.  The theorem therefore records
the coordinate-height assumption explicitly.

## 3. Role in the proof tree

The cross-plane transfer attack leaves a generic/ruled dichotomy.
Theorem 1 rigorously discharges the exact full Cartesian part of the
ruled branch:
\[
\text{large common }J\times A\times Z
\quad\Longrightarrow\quad
D\ge |J||A||Z|\,N^{-o(1)}.
\]
The remaining missing theorem is a stability inverse statement:
near equality in the cross-plane energy bound must yield either

1. a Cartesian subgrid retaining fixed powers of \(|J|,|A|,|Z|\), to
   which Theorem 1 applies; or
2. a fixed saving in the transfer estimate.

No such stability extraction is proved here, so this theorem alone is
not an unconditional improvement of \(f_3(N)\).
