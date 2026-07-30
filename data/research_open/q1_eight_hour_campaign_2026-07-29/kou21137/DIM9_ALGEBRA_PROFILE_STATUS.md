# Dimension-nine algebra-group profile status

Date: 2026-07-30

## Scope

Let \(J\) be a nine-dimensional nilpotent associative
\(\mathbb F_3\)-algebra with \(J^9=0\).  A closed non-powerful cube set in
\(1+J\) requires
\[
 [J^3,J^3]\ne0,\qquad J^6\ne0.                   \tag{1}
\]
This note classifies every power-filtration profile forced by (1).
All 29 profiles now have human exclusions.  The four exact solver
certificates remain independent regression checks, but no longer belong
to the theorem's trust boundary.

## The 29 profiles

Write \(d_i=\dim J^i/J^{i+1}\).  Since \(d_1\ge2\) and
\(d_i\ge1\) for \(2\le i\le6\), the possible profiles have lengths six,
seven, or eight.  Direct positive-composition enumeration gives
\[
 21+7+1=29
\]
profiles.

### Length six

Here \(J^7=0\).  If \(d_3=1\), then
\([J^3,J^3]\le J^7=0\); this removes 15 profiles.  Of the six profiles
with \(d_3\ge2\), five have \(d_2=1\) and contradict the human
associativity lemma
\[
 \dim\operatorname{gr}_2J=1
 \quad\Longrightarrow\quad
 \dim\operatorname{gr}_3J\le1.
\]
The unique survivor is
\[
 (2,2,2,1,1,1).                                  \tag{2}
\]

### Length seven and eight

Among the seven length-seven profiles,
\((2,1,2,1,1,1,1)\) is removed by the same \(d_2=1\) lemma.  The six
remaining profiles include four further impossible layer shapes.  Since
\[
 J^{i+j}=J^iJ^j,
\qquad d_{i+j}\le d_i d_j,                        \tag{3}
\]
\((2,1,1,2,1,1,1)\) contradicts (3) at \(2+2=4\);
\((2,1,1,1,2,1,1)\) contradicts it at \(2+3=5\);
\((2,1,1,1,1,2,1)\) contradicts it at \(2+4=6\); and
\((2,1,1,1,1,1,2)\) contradicts it at \(2+5=7\).
Only the two length-seven profiles with the extra dimension in layer one
or two remain, together with the sole length-eight profile.

## Human and exact closure-aware exclusion of (2)

`search_dim9_algebra_profiles.py` builds the complete
filtration-preserving multiplication table for (2): a product of filtration
degrees \(i,j\) may have components in every layer \(k\ge i+j\).
Unlike a noncommutativity-only search, its SMT model also encodes two
consequences of raw cube closure.

First, let
\[
 q:A_1\to A_3,\qquad q(a)=a^3.
\]
Raw closure implies that \(q(A_1)\) is additively closed after projection
to degree three.  Two noncommuting cubes have linearly independent
degree-three parts, so \(q(A_1)=A_3\).  Both spaces have nine elements;
therefore \(q\) is bijective.  The model includes all 36 pairwise
distinctness constraints.

Second, after choosing the two cube roots as a basis \(x,y\) of \(A_1\),
raw closure requires a solution of
\[
 c^3=x^3+y^3+x^3y^3.                             \tag{4}
\]
The model includes nine root coordinates and all nine coordinate equations
in (4).

The exact ledger is:

```text
DIM9_PROFILES|total=29|length6=21|length7=7|length8=1|length6_degree_pruned=20|minimal_direct=2,2,2,1,1,1
DIM9_MINIMAL_MODEL|structure_variables=140|root_variables=9|associativity=276|surjectivity=15|projection_bijection=36|pair_closure_equations=9|full_raw_closure=false
DIM9_SOLVER|result=unsat
DONE
```

The model contains every filtered associativity coordinate and every
ordered-split leading-layer surjectivity condition
\(A_iA_j=A_{i+j}\).  The unsatisfiable necessary-condition system excludes
(2), even though it does not encode every pair in the raw cube set.
Consequently:

> **Historical intermediate certificate.** The solver first showed that a
> dimension-nine algebra-group Wilson counterexample would have to satisfy
> \(J^7\ne0\).  The hand lemma below now supersedes this dependency.

The canonical SMT-LIB file has 639 lines, 182,311 bytes, and SHA-256

```text
88c1c37c45083469fa8ceb7d9d008688def27471573c1feb897b9b453fd193de
```

`test_dim9_algebra_profiles.py` checks the transcript and hash.

The solver is no longer needed for this profile.  Lemma 3 of
`DIM9_HUMAN_CUBE_COMMUTATIVITY.md` gives a stronger hand contradiction
that does not use closure.  Let \(f_k\) be the \(k\)-fold multiplication
tensor on \(A_1\).  One-dimensional \(A_4,A_5\) and associativity give
\[
f_5=f_4\otimes r=\ell\otimes f_4.
\]
An elementary shift-tensor lemma forces \(f_4,f_5\) to be pure tensor
powers of one linear form.  Applying it once more through
one-dimensional \(A_5,A_6\) gives
\(f_6=c\ell^{\otimes6}\).  Hence
\(x^3y^3=y^3x^3\) in \(A_6\) for all \(x,y\in A_1\); arbitrary filtered
lifts differ by an element of \(J^7=0\).  In particular, neither
bijectivity nor the encoded circle-product root equation is needed.
`humanize_dim9_profile_222111.py` verifies the corresponding grouped
deletion directly on the original encoding.

## Iteration-zero filtered CEGIS exclusion

`cegis_dim9_profile_2111121.py` implements the complete intended CEGIS
loop for \((2,1,1,1,1,2,1)\):

- all 134 filtered structure constants and 288 associativity coordinates;
- all 21 ordered layer-surjectivity constraints;
- 12 source variables for two genuinely noncommuting raw cubes;
- a concrete checker enumerating all \(3^6=729\) cube-relevant inputs;
- one six-variable symbolic cube root for every concrete missing product.

The run terminates before the closure checker is needed: the rank-two
degree-six layer cannot be the image of the one-dimensional
\(A_2\otimes A_4\).  Z3 reports UNSAT at iteration zero in about
milliseconds:

```text
CEGIS_START|profile=2,1,1,1,1,2,1|structure_variables=134|associativity=288|surjectivity=21|relevant_dimension=6|cube_inputs=729|witness_variables=12|max_iterations=40|solver_timeout=90
CEGIS_UNSAT|iteration=0|root_constraints=0|...
DONE
```

The canonical iteration-zero SMT file has 607 lines, 98,733 bytes, and
SHA-256

```text
91ef847a401829cd96129500a63d31702f9fecdbc58afb1bac61818309acccfd
```

`test_cegis_dim9_profile_2111121.py` checks the transcript and hash.

## Human exclusion of the three genuine survivors

The CEGIS core allows every filtered product component in layers
\(k\ge i+j\), all associativity coordinates, and all ordered layer
surjections.  Its Wilson witness consists of two arbitrary cube-relevant
roots \(a,b\) and the exact algebra condition
\[
 a^3b^3\ne b^3a^3.                               \tag{5}
\]
If the raw cubes were a subgroup \(H\), then \(J^9=0\) would give
\(H^3=1\); hence (5) is exactly the necessary non-powerfulness condition
\(H'\nleq H^3\), not a stronger substitute.

All three structurally valid survivors were first found UNSAT at iteration
zero:

| profile | structure constants | associativity coordinates | ordered surjections | result |
|---|---:|---:|---:|---|
| \((2,2,1,1,1,1,1)\) | 152 | 386 | 21 | UNSAT |
| \((3,1,1,1,1,1,1)\) | 164 | 500 | 21 | UNSAT |
| \((2,1,1,1,1,1,1,1)\) | 147 | 363 | 28 | UNSAT |

The exact solver transcripts are reproduced by
`cegis_dim9_profile_2211111.py`,
`cegis_dim9_profile_3111111.py`, and
`cegis_dim9_profile_21111111.py`.

Their canonical iteration-zero certificates are:

| profile | bytes | lines | SHA-256 |
|---|---:|---:|---|
| \((2,2,1,1,1,1,1)\) | 137,682 | 745 | `ce150591bbb66d3b03faf32f51dc1a64deda79d67147a50598d5ca82918bcb9c` |
| \((3,1,1,1,1,1,1)\) | 176,412 | 883 | `d7838ce3a4e12d19db07ee136e087cb0ef889c890d0c2f7f5d380e8113c1d5bc` |
| \((2,1,1,1,1,1,1,1)\) | 164,103 | 719 | `f9ab4206a3f6657068e4f8e23622eb8a6195439a0f4f32fd9c6bfe91939d8a04` |

`test_cegis_dim9_remaining_profiles.py` reruns all three and checks the
byte-level hashes.

These three solver results are no longer needed as premises.  Lemma 1 of
`DIM9_HUMAN_CUBE_COMMUTATIVITY.md` handles both length-seven profiles:
if all cubes lie in \(J^4\), then \(J^4J^4=0\); otherwise a cube with
nonzero degree-three part forces its fourth power to span \(A_4\), and
the only possible degree-seven cube commutator is a multiple of
\([a^3,a^4]=0\).  Lemma 2 handles the length-eight profile: either all
cubes lie in \(J^4\), where one-dimensionality of \(A_4\) kills their
commutators, or one element's powers form a filtration basis of \(J^2\).
Thus all three exclusions are human-checkable.

For the middle profile, `humanize_dim9_iteration_zero.py` also archives a
named-assertion audit.  One Z3 core was reduced from 500 associativity
coordinates and 21 surjections to a deletion-minimal subset containing 14
associativity coordinates, three surjections, and the witness.  This audit
helped expose the hand lemma but is not part of its proof.

Combining the human profile reductions and the three hand lemmas gives:

> **Human dimension-nine no-go.** If \(J\) is a nilpotent
> associative \(\mathbb F_3\)-algebra with \(J^9=0\) and
> \(\dim J\le9\), then a closed raw cube set in \(1+J\) is powerful.
> Therefore an exponent-nine algebra-group Wilson counterexample must have
> \(\dim J\ge10\).

The subsequent dimension-ten audit excludes all 92 in-scope profiles by
hand and strengthens the bound to \(\dim J\ge11\).  See
`DIM10_ALGEBRA_PROFILE_STATUS.md`.
