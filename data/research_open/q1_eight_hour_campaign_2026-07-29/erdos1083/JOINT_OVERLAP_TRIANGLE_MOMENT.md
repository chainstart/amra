# The joint overlap--triangle moment

Date: 2026-07-30

## Purpose

The previous audit retained two marginals in the same truncated block
system:

- large within-product-fibre overlap; and
- many cross-fibre triangle-compatible value triples.

This note studies their actual intersection.  For every selected
block--value incidence it defines a same-fibre reuse degree \(d\) and a
cross-fibre triangle link degree \(\tau\), and analyzes
\[
 {\cal J}=\sum d\,\tau.
\]

There is a new unconditional lower bound:
\[
 {\cal J}\gtrsim L^{10/3-\eta-o(1)}.
\]
It follows by random truncation directly from shared endpoints, rather than
by multiplying the two previous marginal estimates.

This is nevertheless below the useful benchmark
\[
 L^{11/3+\eta}
\]
by exactly \(L^{1/3+2\eta}\).  Equivalently, the current argument gives only
constant average triangle degree under the overlap-weighted distribution,
whereas the required propagation asks for average
\(L^{1/3+2\eta}\).

No Hölder, Cauchy, link-graph or DRC argument from the present marginals
closes this gap.  A realizable hub/low-complexity block-size landscape
saturates the only available reciprocal-size estimates and permits all
overlap mass to be placed where the guaranteed triangle survival is
constant.  It is not a construction with globally small \(M\); proving that
such concentration forces \(M\) to grow is the exact remaining consistency
problem.

No exponent improvement is claimed.

## 1. Definitions on one common truncation

For a radius pair \(e=uv\), write
\[
 Y_e=(Z_u-Z_v)^2,\qquad S_e=C_e+Y_e.
\]
Choose a \(k=\Theta(L)\) element subset
\[
 A_e\subseteq Y_e
\]
and write \(S_e^A=C_e+A_e\).

For \(a\in A_e\), define its ordered same-fibre reuse degree
\[
 d(e,a)=
 |\{f\ne e:p(f)=p(e),\ C_e+a\in S_f^A\}|. \tag{1}
\]
Thus
\[
 {\cal D}:=\sum_e\sum_{a\in A_e}d(e,a) \tag{2}
\]
is the ordered within-fibre overlap mass.

Define the triangle link degree
\[
 \tau(e,a)=
 \sum_{w\notin\{u,v\}}
 |\{(b,c)\in A_{uw}\times A_{vw}:
       (a+b-c)^2=4ab\}|. \tag{3}
\]
The sum is scoped by \(w\); equal numerical pairs belonging to different
radius triangles are counted separately.

The joint moment is
\[
 {\cal J}=\sum_e\sum_{a\in A_e}d(e,a)\tau(e,a). \tag{4}
\]
One term of (4) is a five-radius flag:

1. \(e=uv\) and a disjoint block \(f=xy\) in the same product fibre share
   the shifted value \(C_e+a\);
2. the same unshifted value \(a\) participates with blocks \(uw,vw\) in the
   cross-fibre triangle equation.

This is the first quantity that requires overlap and endpoint consistency
on the same block--value incidence.

## 2. Universal capacities

There are
\[
 I_0=\Theta(L^3) \tag{5}
\]
selected block--value incidences.  Since one product fibre contains
\(O(L)\) blocks,
\[
 0\leq d(e,a)\leq L. \tag{6}
\]
For fixed \(a,b\), equation (3) has at most two possible values of \(c\):
\[
 c=(\sqrt a\pm\sqrt b)^2.
\]
Therefore, for each \(w\), at most \(2k\) selected pairs occur, and
\[
 0\leq\tau(e,a)\leq2Lk=O(L^2). \tag{7}
\]

The known marginal totals are
\[
 {\cal D}\gtrsim L^{10/3-\eta-o(1)},\qquad
 \sum_{e,a}\tau(e,a)\gtrsim L^{3-3\eta-o(1)}. \tag{8}
\]
They do not by themselves imply a positive joint moment.  The smallest
possible supports allowed by (6)--(8) have sizes
\[
 L^{7/3-\eta-o(1)}
 \quad\hbox{and}\quad
 L^{1-3\eta-o(1)}, \tag{9}
\]
whose sum is \(o(I_0)\).  Hence abstract nonnegative arrays can put the two
supports on disjoint incidences and have \({\cal J}=0\).

This also explains why Hölder or Cauchy applied only to the two marginal
moments cannot help: there is no lower rearrangement inequality for two
nonnegative vectors with disjoint permissible supports.

## 3. Shared endpoints force a positive joint moment

### Theorem 1 (random truncation joint-moment bound)

Assume \(m\asymp L\), all radius classes have \(\Theta(m)\) heights, and
\[
 M\leq L^{8/3+\eta}.
\]
There is a choice of \(k=\Theta(m)\) values in every squared-difference
block such that
\[
 {\cal D}\gtrsim L^{10/3-\eta-o(1)} \tag{10}
\]
and
\[
 {\cal J}\gtrsim L^{10/3-\eta-o(1)}. \tag{11}
\]

### Proof

Independently choose a uniform \(k\)-subset \(A_e\subseteq Y_e\), with
\(k\) below the universal \(\Omega(m)\) lower bound for \(|Y_e|\).
Every realization has total incidence \(\Theta(L^3)\) and shifted union
contained in the full union of size \(M\).  Cauchy--Schwarz therefore gives
(10) for every realization.

Consider one ordered reused incidence counted by \(d(e,a)\), where
\(e=uv\), another same-fibre block \(f\) contains the same shifted value,
and the two selected values \(a\in A_e,a'\in A_f\) have already survived.
Fix one point-pair representation
\[
 a=(z_u-z_v)^2.
\]
For every radius class \(w\) outside the endpoints of \(e\) and \(f\), the
\(m\) choices \(z_w\in Z_w\) yield compatible pairs
\[
 b=(z_u-z_w)^2,\qquad c=(z_v-z_w)^2.
\]
At most two choices of \(z_w\) give the same \(b\), so there are at least
\(m/2\) distinct pairs \((b,c)\).

The blocks \(uw\) and \(vw\) are different from \(e,f\) and from each
other.  Conditional on the reused incidence, their truncations remain
independent.  Since every full squared-difference block has at most \(m^2\)
values, one fixed pair survives with probability at least
\[
 (k/m^2)^2=\Omega(m^{-2}).
\]
Thus the conditional expected contribution to \(\tau(e,a)\) from one \(w\)
is \(\Omega(m^{-1})\), and summing over \(\Theta(L)\) choices of \(w\)
gives
\[
 \mathbb E[\tau(e,a)\mid\text{the reused incidence survives}]
 =\Omega(1). \tag{12}
\]

Summing (12) over all ordered reused incidences gives
\[
 \mathbb E{\cal J}\gtrsim\mathbb E{\cal D}.
\]
Every realization satisfies (10), so the expectation, and hence some
realization, satisfies (11). \(\square\)

The proof uses the same value \(a\) in both structures.  It is therefore a
genuine joint estimate, unlike the product of two marginal lower bounds.

## 4. The strongest common-rich extraction

Dyadically partition the ranges (6)--(7).  From Theorem 1 there are powers of
two \(\lambda\leq L\), \(\mu\leq L^2\), and a set \({\cal X}\) of selected
block--value incidences such that
\[
\lambda\leq d(e,a)<2\lambda,\qquad
\mu\leq\tau(e,a)<2\mu
\]
on \({\cal X}\), and
\[
 |{\cal X}|\lambda\mu
\gtrsim \frac{L^{10/3-\eta-o(1)}}{\log^2L}. \tag{13}
\]
In particular, one incidence satisfies
\[
 d(e,a)\tau(e,a)\gtrsim L^{1/3-\eta-o(1)}. \tag{14}
\]

Equation (13) is the strongest unconditional common-enrichment statement
currently obtained.  A DRC argument can reorganize a class
\({\cal X}\), but without a lower bound on either \(\lambda\) or \(\mu\)
it cannot create the missing power.

## 5. Exact target and remaining power

Weight incidences by their reuse degree.  The overlap-weighted average
triangle degree is
\[
 \frac{\cal J}{\cal D}. \tag{15}
\]
Theorem 1 guarantees only a constant lower bound.  To supply the propagation
factor isolated in the previous rounds, one would need
\[
 \frac{\cal J}{\cal D}
\gtrsim L^{1/3+2\eta-o(1)}. \tag{16}
\]
Since \({\cal D}\gtrsim L^{10/3-\eta-o(1)}\), the corresponding joint-moment
benchmark is
\[
 {\cal J}_{\rm target}
\gtrsim L^{11/3+\eta-o(1)}. \tag{17}
\]
The exact shortfall between (11) and (17) is
\[
 L^{1/3+2\eta}. \tag{18}
\]
Only a bound crossing (17), together with the previously specified
propagation step, could support an exponent-improvement claim.

## 6. Why reciprocal-size refinements can still be avoided

The proof of Theorem 1 used only \(|Y_{uw}|,|Y_{vw}|\leq m^2\).
Keeping the exact sizes gives the conditional expected link bound
\[
 R_{uv}
\gtrsim
 mk^2\sum_{w\notin\{u,v\}}
\frac1{|Y_{uw}||Y_{vw}|}. \tag{19}
\]
Small total full-block mass makes the unweighted average of \(R_{uv}\)
large.  It does not force overlap mass \(d\) to lie on those pairs.

This failure has a realizable block-size landscape.  Let
\[
 |U|=L^{2/3+\eta}.
\]
Choose generic \(m\)-point height sets for \(u\in U\), and use one common
arithmetic progression for \(u\notin U\).  Generically,
\[
 |Y_{uv}|=\Theta(m^2)
\quad\text{whenever }u\in U\text{ or }v\in U,
\]
while
\[
 |Y_{uv}|=\Theta(m)
\quad(u,v\notin U).
\]
The full incidence mass is
\[
 |U|L m^2+L^2m
=\Theta(L^{11/3+\eta}), \tag{20}
\]
exactly the maximum allowed by the small-\(M\) counterassumption.

For \(u,v\in U\), equation (19) can be only constant order, because all
incident blocks have size \(\Theta(m^2)\).  There are
\[
 |U|^2=L^{4/3+2\eta} \tag{21}
\]
such hub pairs.  The overlap mass \({\cal D}\) can fit on only
\[
 {\cal D}/L^2=L^{4/3-\eta} \tag{22}
\]
maximally reused blocks, so (21) has ample abstract capacity to contain it.

This is not a construction in which those hub blocks actually have the
forced overlap or in which \(M\) is small.  It proves the precise limitation
of size, Hölder and reciprocal-link arguments: they permit all overlap mass
to concentrate where only the constant bound (12) is available.

## 7. Status of the mod-seven obstruction

The global choice \(Z_u=\{0,\ldots,m-1\}\) and selected roots
\(\pm1\pmod7\) makes every \(\tau(e,a)=0\), hence \({\cal J}=0\).
However, with geometric radial offsets those selected shifted blocks are
not known to carry correlation mass (10); the integer factorization usually
makes their pairwise overlaps small.

We did not obtain a global construction satisfying simultaneously:

1. the original geometric radial offsets;
2. one shared \(Z_u\) in all product fibres;
3. \({\cal D}\gtrsim L^{10/3-\eta}\); and
4. \({\cal J}=o(L^{11/3+\eta})\).

Theorem 1 rules out \({\cal J}=0\) after a suitable truncation whenever the
first three global hypotheses hold.  What remains open is whether geometric
offsets and shared endpoints improve its constant conditional triangle
degree to the power required in (16).

## 8. Exact remaining consistency

The unresolved statement is **conditional and is not asserted as a
theorem**:

> Strong overlap mass cannot concentrate on the high-complexity hub pairs
> from Section 6; either that concentration already forces
> \(M>L^{8/3+\eta}\), or the overlap-weighted average triangle link in (15)
> gains \(L^{1/3+2\eta-o(1)}\).

Algebraically, a joint flag is the fibre product of the overlap hyperbola
\[
 x^2-y^2=C_f-C_e
\]
and the endpoint triangle surface
\[
 (a+b-c)^2=4ab
\]
over the common value \(a=x^2\).  Both factors are group-like.  A useful
incidence theorem would have to exploit the repeated vertex sets \(Z_u\)
and the geometric offset potential simultaneously; generic surface
incidence estimates do not distinguish the hub landscape.

## 9. Verification

`verify_joint_overlap_triangle_moment.py` checks the capacity and target
exponents, the disjoint-support marginal no-go, dyadic benchmark identities,
the constant random-survival calculation, and the hub size ledger.
