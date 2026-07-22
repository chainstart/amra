# Erdős #963: two natural binary-basis routes are false

Date: 2026-07-22 (Asia/Hong_Kong)

Status: exact route autopsy.  The results below refute two tempting
strengthenings; they neither refute nor prove #963.

## 1. Ordinary subset-sum bases do not suffice

A maximal dissociated subset `B` of `P` only guarantees

\[
 P\subseteq \operatorname{Span}_{\{-1,0,1\}}(B),
\]

not `P subset FS(B)`.  This cannot be repaired by choosing a different
maximum dissociated subset.  The four-point set

\[
 P_0=\{1,3,5,7\}
\]

has dissociation dimension three, but for each of its four three-element
dissociated subsets the omitted point is not an ordinary subset sum of the
chosen three.  `subsetsum_basis_probe.py` checks all four choices by exact
integer arithmetic.  Thus the hoped-for injection into the `2^r` ordinary
subset sums of a basis is false already at rank three.

## 2. Even an arbitrary affine Boolean cube is too restrictive

One might weaken the failed statement to

\[
 P\subseteq c+\operatorname{FS}(d_1,\ldots,d_r),
 \qquad r=d(P),                                      \tag{1}
\]

where `c,d_i` are arbitrary reals and need not belong to `P`.  This is also
false.  Put

\[
 P_1=\{1,6,7,8,13,14,20,21,27,34,35\}.              \tag{2}
\]

Then

\[
 d(P_1)=4,
 \qquad
 P_1\not\subseteq c+\operatorname{FS}(d_1,d_2,d_3,d_4)               \tag{3}
\]

for all real `c,d_1,...,d_4`.

### Exact certificate for the rank

The subset `{1,6,8,20}` has 16 distinct subset sums.  Conversely, all
`binom(11,5)=462` five-subsets of (2) have an explicit collision between
two subset sums.  Hence the dissociation dimension is exactly four.

### Solver-free certificate for non-containment

If (1) held, the eleven distinct points of `P_1` would have eleven distinct
representing vertices in `{0,1}^4`.  There are `binom(16,11)=4368` possible
vertex subsets.  Coordinate permutations and coordinate complements split
them into exactly 27 orbits.  For one representative of each orbit, choose
five affinely independent vertices.  An affine functional on the four-cube
is determined by its values on these five vertices, so it is enough to try
all

\[
 11\cdot10\cdot9\cdot8\cdot7=55,440
\]

ordered assignments from `P_1`.  Exact rational interpolation forces the
remaining six values.  None yields `P_1`.  Thus the exhaustive total is

\[
 27\cdot55,440=1,496,880
\]

assignments and proves (3).  This calculation uses only Python integer and
`Fraction` arithmetic; it does not call Z3, floating point, MILP, or an
unverified optimizer.  The executable certificate and its output are
`verify_affine_cube_counterexample.py` and
`verify_affine_cube_counterexample.json`.

## 3. Separate generic-kernel search

In the generic rank-four ternary signature (trivial bounded relation
kernel), the lazy exact Z3 search returned `UNSAT` at target size 14 after
37 model iterations and 35,736 distinct dissociated-five cuts.  This is a
strict statement about that one kernel signature only.  At target 13 the
solver timed out with status `unknown`; absence of a witness there is no
mathematical conclusion.

The target-14 computation must not be conflated with the full rank-four
extremal problem.  Non-generic kernels exist, and earlier work already has
non-generic size-13 examples.

## 4. Consequence for the next route

Both failures identify the same obstruction.  The desired `2^r` cardinality
bound, if true, cannot follow merely by placing `P` in one binary coordinate
model.  A viable proof has to exploit overlap between many signed-span
representations, or strengthen the modular recursion so that its cumulative
loss is `O(1)` rather than `o(log |P|)`.  The exact affine-cube counterexample
is a route correction, not a Q2-level positive theorem and not a stopping
result for #963.
