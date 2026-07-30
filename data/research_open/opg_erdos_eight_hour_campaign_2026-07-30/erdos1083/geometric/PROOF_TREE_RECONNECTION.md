# Reconnection audit for the square–chord theorem

Date: 2026-07-30

This note traces the hypotheses of `SUMSET_EXPANSION_ATTACK.md` back through
the 2026-07-29 Erdős-1083 campaign.  It is a scope audit, not a modification
of the old proof tree.

## 1. The exact slice required

After an affine rescaling of heights, the sumset theorem can be applied if
one extracts:

1. \(m\) coaxial circles of one common radius;
2. an \(m\)-term arithmetic progression of their distinct axial heights;
3. the same aligned \(S\)-term angular orbit
   \[
   \{0,\theta,\ldots,(S-1)\theta\}
   \]
   on every selected circle, with distinct angular points;
4. critical sizes \(m,S=N^{2/5-o(1)}\), if the desired conclusion is the
   \(N^{4/5-o(1)}\) slice bound.

The normalization \(x_k=2m^2(1-\cos(k\theta))\) used in the explicit grid is
not essential: a height progression of step \(\delta\) and common radius
\(\rho\) gives, after division by \(\delta^2\),
\[
A_m+\left\{\frac{2\rho^2}{\delta^2}
(1-\cos(k\theta)):0\le k<S\right\},
\]
to which the same arbitrary-translate theorem applies.

## 2. What the inherited node actually supplies

`PROGRESS.md`, lines 92--119, reconnects the old campaign to the
plane-reflection/common-axis obstruction.  At that node one has aggregate
data of the form
\[
M\ge n^{1/5-o(1)},\quad
q_\alpha\ge n^{3/5+o(1)},\quad
r_\alpha\ge n^{1-o(1)}
\]
and a large summed joint mass.

These quantities sum incidences and correlations over circular fibres.
They do not identify one set of fibres on which the popular angles coexist,
nor do they determine the radii or axial heights of those fibres.

`PROGRESS.md`, lines 147--170, states this explicitly:

- the equal-radius/common-progression conclusion is introduced with
  “if an extraction step produces”;
- lines 168--170 say that neither common radius nor common progression has
  been derived from the aggregate correlations.

Therefore the inherited node supplies a common axis and aggregate angular
statistics, but none of the three rectangle hypotheses below.

## 3. Common radius: not inherited

`CIRCLE_INTERFACE_NO_GO.md`, Theorem 3, assumes that all selected fibres
have one common radius.  Its “Exact remaining gap” section says the original
correlation hypotheses do not supply that coherent rectangle.

`COAXIAL_SYNCHRONIZATION_DICHOTOMY.md` begins by calling common radius a
“very special assumption.”  Its general synchronized setup allows \(L\)
distinct radii and defines
\[
m=\max_\rho\#\{i:\rho_i=\rho\}.
\]
Choosing a most frequent radius gives \(m\) equal-radius circles, but the
inherited proof does not force \(m=N^{2/5-o(1)}\).  At the balanced
anisotropic scale this value occurs only in the explicit benchmark.

Verdict:

```text
common axis       inherited at the audited branch;
common radius     conditional/extracted hypothesis, not inherited.
```

## 4. Consecutive heights: not inherited

In `COAXIAL_SYNCHRONIZATION_DICHOTOMY.md`, lines 91--115, the heights in a
repeated-radius class are arbitrary distinct real numbers.  The proof uses
only
\[
Y=\{(z_i-z_j)^2\}
\quad\text{and}\quad |Y|\ge m.
\]
It does not obtain an arithmetic progression.

The common interval height set
\[
\{0,1,\ldots,m-1\}
\]
appears in `AFFINE_COPY_REDUCTION_AND_BARRIER.md` and
`CRITICAL_ANISOTROPIC_GRID_BARRIER.md` as an explicitly chosen construction
used to test a proposed line-count theorem.  It is not an inverse theorem
deduced from small distance count.

Several later old-campaign notes emphasize that height sets may vary
independently, may be translated, and may have large diameter.  For example,
`GEOMETRIC_RADIUS_HIGH_ENERGY.md` proves separate theorems under a common thin
slab or identical height sets and then states that the inherited argument
produces neither.

Verdict:

```text
distinct heights in one radius class    automatic;
long arithmetic progression of heights not proved.
```

## 5. A common angular orbit: not inherited

`CIRCLE_INTERFACE_NO_GO.md` defines
\[
q_\alpha=\sum_C|A_C\cap\{\alpha,\alpha+\pi\}|+\cdots,
\qquad
r_\alpha=\sum_C|A_C\cap(A_C+2\alpha)|+\cdots.
\]
Large values of these sums allow different fibres to contribute for
different \(\alpha\)'s.

Its exact gap statement, lines 196--220, says:

- \(q_\alpha\) puts one angle on many, not necessarily the same, fibres;
- the correlation sums do not make participating fibre sets identical;
- a robust common-pattern extraction is still missing.

`COAXIAL_SYNCHRONIZATION_DICHOTOMY.md`, lines 16--27, simply assumes every
circle contains the same progression.  `AFFINE_COPY_REDUCTION_AND_BARRIER.md`
then says “keep the synchronized-circle setup.”  Neither file derives the
setup from the inherited aggregate data.

Verdict:

```text
many popular angles in aggregate   inherited;
one aligned S-term orbit on the
same selected circles              not proved.
```

## 6. Where the new theorem genuinely reconnects

`CRITICAL_ANISOTROPIC_GRID_BARRIER.md` is an explicit family:

\[
\rho_u=mq^u,\qquad
Z_u=\{0,\ldots,m-1\},\qquad
L=t,\quad m=S=t^2.
\]
Section 4 additionally puts the same synchronized angular pattern on every
circle.  Hence this constructed family satisfies every hypothesis of the
square–chord theorem on each fixed-radius class.

The reconnection
\[
\text{explicit critical anisotropic grid}
\Longrightarrow
D\ge N^{4/5-o(1)}
\]
is valid, up to the harmless subtraction of the zero distance.  It shows
that the grid is a barrier for line-count methods but not a low-distance
extremizer.

No arrow from the unrestricted inherited branch to that grid or to an
equivalent rectangle has been proved.

## 7. Proof-tree diagram

```text
inherited plane-reflection/common-axis branch
        |
        +--> aggregate q_alpha, r_alpha and joint mass
                 |
                 X  missing synchronization/extraction
                 |
                 +--> [needed simultaneously]
                        common radius with m large
                        + height AP of length m
                        + aligned angular AP of length S
                                  |
                                  v
                     square–chord sumset theorem
                                  |
                                  v
                     D >= m^(2-o(1)) - 1

explicit anisotropic grid
        |
        +--> all three hypotheses hold by construction
                                  |
                                  v
                     D >= N^(4/5-o(1))
```

The crossed arrow is the exact open gap.

## 8. Minimum viable extraction theorem

A sufficient bridge would be a theorem of the following form.

> From the inherited common-axis branch and the assumption
> \(D\le N^{3/5+o(1)}\), extract, with only \(N^{o(1)}\) losses, one radius
> class containing \(m=N^{2/5-o(1)}\) circles whose heights contain an affine
> \(m\)-term arithmetic progression, and an aligned
> \(S=N^{2/5-o(1)}\) angular progression present on all these circles.

This statement is substantially stronger than each existing marginal:

- radius concentration alone does not give structured heights;
- a height progression alone does not synchronize angle sets;
- common angular correlation alone does not concentrate one radius;
- pairwise popularities do not automatically yield a three-way rectangle.

A weaker useful bridge could replace the exact height progression by a set
with a comparably strong uniform difference-of-squares representation bound,
or replace the exact common angular orbit by a robust common subset for which
chord multiplicity remains \(N^{o(1)}\).  Such extensions are not contained
in the current theorem.

## 9. Consequence for claims about \(f_3\)

The currently valid implication is
\[
\boxed{
\text{critical synchronized square-height slice}
\Longrightarrow D\ge N^{4/5-o(1)}.
}
\]

The following implication is not established:
\[
D\le N^{3/5+o(1)}
\Longrightarrow
\text{such a slice exists}.
\]

Accordingly, neither `SUMSET_EXPANSION_ATTACK.md` nor the old proof tree
proves an unconditional improvement of \(f_3(N)\).  Reconnecting the theorem
requires a new simultaneous radius–height–angle extraction result, not
additional manipulation of the already verified energy denominator.
