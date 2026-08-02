# Blind audit of the maximum-witness square-root degree-spread theorem

Date: 2026-08-02

Status: **PASS AFTER ONE LOCAL EXPOSITORY REPAIR**

## 1. Audited snapshot and independence

The primary source is
MAXIMUM_WITNESS_OPPOSITE_DEGREE_SPREAD.md.

- Hash before audit repair:
  6991a8638bc71ef46adcc4f4de73f531253aca87a674fa6181f1b525a5fb6d22.
- Hash after the Section 6 repair, before status synchronization:
  05c596ade598418ba562911b28ab0383e9954eb09b23caafbdeb4651dd6450b6.
- Frozen current hash after audit-status synchronization:
  5c3e07e97a0b96a14b8c1be63331d3431366399e0c749eaa9d43f62f1e6c9602.

The composed normal form
MAXIMUM_WITNESS_CANONICAL_HARDNESS_NORMAL_FORM.md was audited at hash
5f45b26ff205c0fead1612a60eb1c26cc7f66f1ea2abc32da49e417a2a3d081b.
The pre-existing verifier and tests had hashes
5d3ae1eab0ce587985246ce918cf68f333408852ae9b46147a3971cdd53145f3
and
65c8a81f495080217aec72f6293f537928b3a918dc3b3a67513c6cce79c40e7b.

The audit was reconstructed without importing the pre-existing verifier.
Its independent executable certificates are

- verify_maximum_witness_sqrt_spread_blind_audit.py;
- test_maximum_witness_sqrt_spread_blind_audit.py.

## 2. Verdict matrix

| Item | Verdict | Independent check |
|---|---|---|
| Maximum-witness basepoints and $3\le\rho_c\le\kappa$ | **PASS** | Direct set inclusion |
| Individual three-family missing-pair bound (3) | **PASS** | Reconstructed from the pure pair condition |
| Four disjoint charges in (4b) | **PASS** | Set reconstruction plus 16,932 fourth-family graphs |
| $g\le2$ and both $g=3$ exclusions | **PASS** | 177 low-spread, 15,750 even, and 2,024,440 odd scalar rows |
| $\ell=1$ interval (16) | **PASS** | Direct degree and residual identities |
| Centre-degree concavity and endpoint reduction | **PASS** | Symbolic second derivative and endpoint equality |
| Even/odd factorizations (18), (20) | **PASS** | Exact symbolic expansion plus 1,130,499 sign rows |
| Square-root constants (22) | **PASS** | Exact integer-root equivalence on 28,794 orders |
| Cyclic sharp graphs: edges, degrees, balance, geometry | **PASS** | 18 rebuilt graphs and 225 maximum witnesses |
| N32 defect-slack specialization | **PASS** | Exact one-leaf substitution; 394 endpoint rows |
| N33 rainbow argument as initially written | **REPAIR** | Endpoint pairing was implicit; repaired locally |
| N33 conclusion after repair | **PASS** | 18 exact repeated-class $C_7$ searches at $g=4,5$ |
| $D_B=g$ after recolouring | **PASS** | Recomputed from actual good-edge colour classes |
| Missing-star reserve (22c) | **PASS** | Recomputed for 85 maximum witnesses |
| All eight $L_4(2)$ templates | **PASS** | 1,227 endpoint pairs and 352,908 typed path sets |
| Public-problem and normal-form firewall | **PASS** | Surviving branches and open status remain explicit |

No mathematical counterexample to the theorem was found.  The sole
repair was a missing case split in the prose proof that the paired
recolouring remains rainbow on every $C_7$.  Its conclusion was correct.

## 3. Reconstruction from the pure opposite-pair condition

Fix one opposite pair and write

\[
 P=N(b),\qquad Q=N(c),\qquad
 W=V(G)\setminus(P\cup Q\cup\{b,c\}).
\]

Put $p=|P|$, $\rho=n-p-|Q|$, and $d=\rho-1$.  Then
$|W|=d-1$.  Since $b,c\notin N[v]$, the distinct vertices $b,c,v$
lie outside $P\cup Q$, so

\[
 3\le\rho\le n-2\delta=\kappa,
 \qquad 2\le d\le\kappa-1.
\]

The rectangle $P\times Q$, the missing $b$-star, and the missing
$c$-star are disjoint except that $bc$ belongs to both stars.  Hence

\[
 \overline M
 \ge p|Q|+(n-1-p)+(n-1-|Q|)-1
 =p|Q|+n+\rho-3.
\]

For the degree-cap refinement, the four charged universes in the
one-leaf specialization are

\[
\begin{aligned}
 F_1&=P\times(Q\cup\{c\}),\\
 F_2&=\{b\}\times(Q\cup\{c\}\cup W),\\
 F_3&=W\times\{c\},\\
 F_4&\subseteq W\times(P\cup Q\cup W).
\end{aligned}
\]

They are pairwise disjoint as sets of unordered pairs.  Every $w\in W$
already misses $b,c$; among its other $n-3$ potential neighbours it
therefore misses at least

\[
 s=(n-3-\Delta)_+
\]

pairs.  Summing these deficits counts an absent pair internal to $W$
twice and every other member of $F_4$ once.  Therefore

\[
 |F_4|\ge
 \left((d-1)s-\binom{d-1}{2}\right)_+.
\]

The first three family sizes are

\[
 p(n-p-d),\qquad n-p-1,\qquad d-1,
\]

which reconstructs (4b) at $\ell=1$.  The independent enumerator also
checked the internal-$W$ correction for every fourth-family missing
graph with at most four $W$-vertices.

## 4. Interval, concavity, and parity factorization

Since

\[
 d(c)=n-p-d-1\ge\delta,
\]

the centre degree lies in

\[
 \delta\le p\le n-\delta-d-1.
\]

The $p$-dependent part of the relaxed charge is

\[
 f(p)=p(n-d-1-p)+n-1.
\]

It has $f''(p)=-2$, and the two interval endpoints add to
$n-d-1$.  They therefore have exactly the same value.  Also

\[
 (d-1)+
 \left((d-1)(n-3-\Delta)_+-\binom{d-1}{2}\right)_+
 \ge
 (d-1)(n-2-\Delta)-\binom{d-1}{2}.
\]

If $n-3-\Delta\ge0$, this follows by dropping a positive part only
after adding $d-1$.  If it is negative, the right side is nonpositive.
These facts give (17).

Put $n=2\delta+\kappa$, $d=\kappa-h-1$, and
$a=2g-\kappa$.  Exact symbolic expansion gives

\[
 \mathcal L_0-\overline M
 =\delta-g^2+2g+2+
 \frac{a^2-4+2h(2g-h-1)}4
\]

in even order, and

\[
 \mathcal L_0-\overline M
 =\delta-g^2+2g+1+
 \frac{a^2-1+2h(2g-h-1)}4
\]

in odd order.  In even order $a\ge2$ is even and
$0\le h\le2g-5$; in odd order $a\ge1$ is odd and
$0\le h\le2g-4$.  Both remainders are nonnegative.  The necessary
inequality $\mathcal L_0\le\overline M$ therefore gives

\[
 n\le2g^2-2g-6\quad(n\text{ even}),
 \qquad
 n\le2g^2-2g-3\quad(n\text{ odd}).
\]

Solving these integer quadratics gives precisely

\[
 g\ge\left\lceil\frac{1+\sqrt{2n+13}}2\right\rceil
 \quad(n\text{ even}),
 \qquad
 g\ge\left\lceil\frac{1+\sqrt{2n+7}}2\right\rceil
 \quad(n\text{ odd}).
\]

## 5. Independent audit of the cyclic sharp graphs

For even order the parameters are

\[
 \delta=g^2-2g-2,\quad \kappa=2g-2,\quad
 |W|=2g-4,\quad \Delta=g^2-g-2,
\]

and for odd order they are

\[
 \delta=g^2-2g-1,\quad \kappa=2g-1,\quad
 |W|=2g-3,\quad \Delta=g^2-g-1.
\]

The edge count is

\[
 2\binom\delta2+2\delta+|W|\Delta
 =\delta^2+\delta+|W|\Delta
 =\left\lfloor\frac{n^2}{4}\right\rfloor+1.
\]

The cyclic intervals concatenate into a walk of length $|W|\Delta$
around $2\delta$ positions.  Every right degree is therefore the floor
or ceiling of $|W|\Delta/(2\delta)$.  The lower slacks above degree
$g-1$ are $4$ and $g^2-g+1$; the upper slacks below degree $g$ are
$2(g^2-2g-4)$ and $g^2-3g-3$.  They have the claimed signs for
$g\ge4$.  Thus every right degree lies in $\{g-1,g\}$, the minimum
degree is $\delta$, and every $W$-vertex has degree $\Delta$.

An interval of length $\delta+g$ in two consecutive blocks of length
$\delta$ meets each block in at least $g$ points.  Hence every
$w\in W$ has at least $g$ neighbours in each of $P,U$.  Every such
$w$ is a valid maximum witness; $b,c\notin N[w]$, $N(b)=P$,
$N(c)=U$, and $P$ is anticomplete to $U$.  The independent constructor
checked all these claims on 18 graphs and all 225 of their $W$-witnesses
for $4\le g\le12$.

## 6. N33: recolouring, exact defect, and the repaired path argument

Choose $x_i\in N(v)\cap P$, $y_i\in N(v)\cap U$, give
$bx_i,cy_i$ the fresh colour $\gamma_i$, and keep every other colour
fresh.  Relative to $A=N[v]$, both edges of every $\gamma_i$-class
cross $A,B$.  Its good cross-edge count is $t_{\gamma_i}=2$, so it
contributes one to

\[
 D_B=\sum_\gamma(t_\gamma-1)_+.
\]

Every other colour has at most one such edge.  Consequently $D_B=g$
exactly.  The $g$ classes all have outer endpoint set containing
$\{b,c\}$, so the zero-shore multiplicity is also exactly $g$.

The initial manuscript compressed the $C_7$ path pairing too far.
After deleting $bx_i,cy_i$ from a hypothetical $C_7$, the two remaining
paths have total length five and one of the pairings

\[
 (b,c),(x_i,y_i),\qquad (b,y_i),(x_i,c).
\]

In the second pairing neither endpoint pair has a common neighbour:
$N(b)=P$ is anticomplete to $y_i\in U$, and $N(c)=U$ is
anticomplete to $x_i\in P$.  Both paths would have length at least
three.  In the first pairing $b,c$ have no common neighbour, so their
path must have length three.  It would have type $b-P-U-c$, impossible
because $P$ is anticomplete to $U$.  This explicit case split was
inserted into the source; no hypothesis or conclusion changed.

The independent verifier also applies the exact two-path
characterization to all 18 repeated classes in the four first endpoint
graphs, $g=4,5$ and both parities.  All pass.

For any $v\in W$, put $B=V\setminus N[v]$.  Since

\[
 d_B(b)=\delta-|N(v)\cap P|,\qquad
 d_B(c)=\delta-|N(v)\cap U|,\qquad
 |N(v)\cap(P\cup U)|=\Delta,
\]

one gets

\[
\begin{aligned}
 \overline d_B(b)+\overline d_B(c)-1
 &=2(|B|-1)-d_B(b)-d_B(c)-1\\
 &=2n-\Delta-2\delta-5\\
 &=\delta+2\kappa-g-5.
\end{aligned}
\]

This is $g^2+g-11$ in even order and $g^2+g-8$ in odd order, and it
is at least $g=D_B$ for every claimed parameter.  These examples are
therefore reserve-paid, not hard reserve-failure examples.

## 7. N32 and the eight L4 templates

At $\ell=1$, one has $R_L=\rho_c$ and
$\Xi=(\rho_c-2)_+=\rho_c-2$.  The defect-slack inequality gives

\[
 2\rho_c-2\le2g+2(D_B-h_c),
\]

and hence

\[
 D_B-h_c\ge\rho_c-1-g.
\]

At the even and odd equality profiles $\rho_c=2g-2$ and $2g-1$, this
is exactly $g-3$ and $g-2$.  Reserve failure is essential here; N33
lies in the reserve-paid branch, so there is no conflict.

For $g=5$, both parity graphs were rebuilt independently.  For every
pair of distinct endpoints, only the displayed path-type template, or
its $b,P\leftrightarrow c,U$ image, was allowed.  The verifier generated
all internal three-vertex sets realizing that template and checked that
no one- or two-vertex set meets all of them.  This is exactly the
survival of a four-edge template path after deletion of any two
nonendpoints.  All 1,227 endpoint pairs and 352,908 typed path sets
passed.

## 8. Verifier assessment and firewall

The old arithmetic and graph verifier passed its ten tests.  Its factor,
endpoint, and L4 transversal checks are sound.  In particular, empty
total intersection excludes a one-vertex path transversal, and repeating
that test after each first deletion excludes every two-vertex
transversal.

There was one coverage weakness, not a false assertion: the old verifier
returned recoloured_defect equal to $g$ without constructing colour
classes and did not search for a $C_7$ containing both edges of a repeated
class.  The independent verifier closes both gaps by constructing the
colour map, recomputing $D_B$, and using the exact two-path
characterization.

Finally, the theorem concerns the maximum-witness B-opposite subbranch.
The canonical note retains Branch A, B-same, the surviving
square-root-spread B-opposite profiles, and other BCM witness branches.
Both the primary note and README state that Erdős #809 remains open.
The result is correctly firewalled from a claim to solve the public
problem.

## 9. Reproduction and frozen counts

Run:

    python3 verify_maximum_witness_sqrt_spread_blind_audit.py
    python3 -m pytest -q test_maximum_witness_degree_spread.py \
      test_maximum_witness_sqrt_spread_blind_audit.py

At freeze time the independent verifier reported:

- 16,932 fourth-family missing graphs;
- 1,130,499 parity-factor sign rows;
- 28,794 exact root rows;
- 234 sharp scalar endpoint rows;
- 177 $g\le2$ rows;
- 15,750 even and 2,024,440 odd $g=3$ rows;
- 18 cyclic endpoint graphs and 225 maximum witnesses;
- 18 exact repeated-class $C_7$ checks;
- 85 witness-specific reserve checks;
- 394 N32 endpoint rows;
- 1,227 L4 endpoint pairs and 352,908 typed path sets.

The combined old and independent test suites passed all 19 tests after
the local prose repair.
