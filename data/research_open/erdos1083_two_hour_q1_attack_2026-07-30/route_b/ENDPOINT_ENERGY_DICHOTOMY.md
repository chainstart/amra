# Erdős #1083 Route B, stage 3: arithmetic energy at the \(9/41\) endpoint

Date: 2026-07-30.

> **Status after stage 4.**  The fixed-centre linearization in
> `COLLINEAR_CENTER_LINEARIZATION_THEOREM.md` excludes the Euclidean
> hub below \(2/9\), so \(9/41\) is no longer the live geometric
> endpoint.  This note is retained as a correct conditional diagnostic
> for the tangent--label parameter subsystem, not as the final Route B
> boundary.

## 0. Outcome

Assume more than the scalar \(9/41\) ledger from
`NINE_FORTY_ONE_NEXT_ATTACK.md`: assume that its tangent--label
parameter points contain a regular line subfamily \(\mathcal L_*\)
with all of the following properties, up to \(t^{o(1)}\) factors:

- \(|\mathcal L_*|=t^{105/41}\);
- every line has \(t^{35/41}\) incidences;
- the lines split into \(t\) represented squared slopes, with
  \(t^{64/41}\) parallel lines per slope.

Then the power-scale proof of the structural Cartesian-product
Szemerédi--Trotter theorem forces a quantitative arithmetic dichotomy.
The scalar endpoint ledger alone does not supply this simultaneous
regularization; it is an explicit condition of this note.

There is a set \(\mathcal S\) of \(t^{1-o(1)}\) represented squared
slopes
\[
\mathcal S\subseteq\{A(C)^2\}
\]
and an energy scale \(\mathfrak e\) such that the squared-radius
intercept set of each of \(t^{1-o(1)}\) parallel families has additive
energy \(\Theta(\mathfrak e)\), while
\[
\boxed{
E^\times(\mathcal S)\,\mathfrak e
\ge t^{274/41-o(1)}.
}
\tag{1}
\]
Equivalently, for some \(0\le\eta\le41\),
\[
\boxed{
\mathfrak e
=t^{(192-\eta)/41+o(1)},
\qquad
E^\times(\mathcal S)
\ge t^{(82+\eta)/41-o(1)}.
}
\tag{2}
\]

The two endpoints have a transparent meaning:

- \(\eta=0\): the intercept sets have essentially maximal additive
  energy, while the squared slopes may have only their unavoidable
  \(t^{2-o(1)}\) multiplicative energy;
- \(\eta=41\): the squared slopes have essentially maximal
  \(t^{3-o(1)}\) multiplicative energy, while the intercept energy may
  fall to \(t^{151/41+o(1)}\).

Thus any Euclidean exclusion beyond \(9/41\) may be split into two
precise tasks: expand cross-target distances from multiplicatively
structured signed radial coordinates, or expand them from additively
structured squared reverse-circle radii.

This is a **conditional regular-endpoint classification**.  It does not
prove that every scalar endpoint admits \(\mathcal L_*\), that the
endpoint is realizable or impossible, or that the global \(3/5\)
exponent improves.

## 1. Normalized endpoint

Let
\[
\mathcal P=\mathcal T_\alpha\times\mathcal D_0
\]
be the tangent--label point set and let \(\mathcal L\) be the represented
parameter lines.  The endpoint ledger is
\[
\begin{aligned}
|\mathcal T_\alpha|&=t^{41/41+o(1)},\\
|\mathcal D_0|&=t^{64/41+o(1)},\\
|\mathcal P|&=t^{105/41+o(1)},\\
|\mathcal L|&=t^{105/41+o(1)},\\
I(\mathcal P,\mathcal L)&=t^{140/41+o(1)}.
\end{aligned}
\tag{3}
\]
Put
\[
n=t^{105/41}.
\]
Then
\[
|\mathcal P|=|\mathcal L|=n^{1+o(1)},
\qquad
I(\mathcal P,\mathcal L)=n^{4/3+o(1)}.
\tag{4}
\]
The Cartesian-product aspect is
\[
\alpha=\frac{41}{105},
\qquad
|\mathcal T_\alpha|=n^{\alpha+o(1)},
\qquad
|\mathcal D_0|=n^{1-\alpha+o(1)}.
\tag{5}
\]

By the regular-subfamily hypothesis, there are \(t^{1+o(1)}\) squared
slopes and \(t^{64/41+o(1)}\) parallel parameter lines per squared
slope.  Hence, in the notation for parallel families,
\[
\beta=\frac{64}{105},
\qquad
n^{1-\beta}=t,
\qquad
n^\beta=t^{64/41}.
\tag{6}
\]
Notice that
\[
\frac13<\alpha<\frac12,
\qquad
1-2\alpha<\beta<\frac23.
\tag{7}
\]

## 2. Structural input

Sheffer--Silier,
[*A structural Szemerédi--Trotter theorem for Cartesian
products*](https://arxiv.org/abs/2110.09692), Theorem 1.4(b), states
the corresponding result when the point and line cardinalities are
exactly \(n\) and the incidence count is \(\Theta(n^{4/3})\).

The power-scale form used here follows by rerunning that proof on
\(\mathcal L_*\) and retaining \(n^{o(1)}\) losses.  The dyadic
pigeonholes, the line-energy lower bound, and the displayed
polylogarithmic losses in that proof remain \(n^{o(1)}\).  It is
important that \(\mathcal L_*\), rather than an arbitrary collection
of parallel families elsewhere in the line set, carries
\(n^{4/3-o(1)}\) incidences.

The resulting power-scale statement is as follows.

When \(A\times B\) and a line set of common cardinality \(n^{1+o(1)}\)
form \(n^{4/3-o(1)}\) incidences, and the lines contain
\(n^{1-\beta-o(1)}\) parallel families of size
\(n^{\beta-o(1)}\), there is an additive-energy scale
\[
n^{2\beta-o(1)}
\le\mathfrak e\le
n^{3\beta+o(1)}
\tag{8}
\]
shared by \(n^{1-\beta-o(1)}\) of the intercept sets, whose slope set
\(\mathcal S\) satisfies
\[
E^\times(\mathcal S)\,\mathfrak e
\ge n^{3-\alpha-o(1)}.
\tag{9}
\]
Polylogarithmic factors are absorbed into \(t^{o(1)}\).

In the present geometry the line
\[
d=b+A^2\tau
\]
has slope \(A^2\) and intercept \(b=\rho^2\).  Thus the two energies in
(9) are exactly energies of squared signed radial coordinates and
squared reverse-circle radii.

## 3. Exponent calculation

Substituting (5)--(6) into (8) gives
\[
t^{128/41-o(1)}
\le\mathfrak e\le
t^{192/41+o(1)}.
\tag{10}
\]
Equation (9) becomes
\[
E^\times(\mathcal S)\,\mathfrak e
\ge
\left(t^{105/41}\right)^{3-41/105-o(1)}
=t^{274/41-o(1)},
\]
which is (1).

The selected slope set has size \(t^{1-o(1)}\), so
\[
t^{82/41-o(1)}
\le E^\times(\mathcal S)
\le t^{123/41+o(1)}.
\tag{11}
\]
The upper bound in (11), combined with (1), improves the lower end of
(10) to
\[
\mathfrak e\ge t^{151/41-o(1)}.
\tag{12}
\]

Write
\[
\mathfrak e=t^{(192-\eta)/41+o(1)}.
\]
Equations (10) and (12) give \(0\le\eta\le41\), and (1) gives
\[
E^\times(\mathcal S)
\ge t^{(82+\eta)/41-o(1)}.
\]
This proves (2).

## 4. What a power-saving continuation must prove

For some fixed \(c>0\), it is enough to establish one of the following
uniform Euclidean statements on all dyadically regular endpoint
subconfigurations:

1. **multiplicative branch:** if
   \(E^\times(\{A^2\})\ge t^{(82+\eta)/41-o(1)}\), then the target
   points generate at least \(t^{3+c}\) distances;
2. **additive branch:** if \(t^{1-o(1)}\) squared-radius intercept sets
   have energy \(t^{(192-\eta)/41+o(1)}\), then the source or target
   points generate at least \(t^{3+c}\) distances.

The assertion must be genuinely geometric.  Freiman-type structure
alone is insufficient: arithmetic or geometric progressions can have
large energy and few sum/product values.  The missing gain must couple
that structure to centre heights, tangent coordinates, or cross-circle
distance formulas.

## 5. Claim boundary

### Proved, conditional on the regular incidence subfamily

- the normalized aspect and parallel-family exponents (5)--(7);
- the energy product (1), by the cited structural theorem;
- the one-parameter energy trade-off (2);
- the sharper feasible range \(0\le\eta\le41\).

### Not proved

- extraction of the required \(\mathcal L_*\) from the scalar endpoint
  ledger alone;
- existence of a Euclidean endpoint configuration;
- a power saving in either energy branch;
- exclusion of \(\kappa=9/41\);
- any improvement of \(f_3(N)\gg N^{3/5}\).

## 6. Reproduction

```bash
cd data/research_open/erdos1083_two_hour_q1_attack_2026-07-30/route_b
python3 verify_endpoint_energy_dichotomy.py
pytest -q test_verify_endpoint_energy_dichotomy.py
```
