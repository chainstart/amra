# Independent cross-solver audit of the dimension-nine no-go

Date: 2026-07-30

## Verdict

The dimension-nine algebra-group exclusion passes an independent logic audit
and a second-SMT-solver check.  All four nontrivial canonical formulas report
UNSAT in both Z3 4.8.12 and cvc5 1.3.3.

Subject to the explicitly stated algebra-group scope, the resulting
computer-assisted theorem is sound:

> If \(J\) is a nilpotent associative \(\mathbb F_3\)-algebra with
> \(J^9=0\) and \(\dim J\leq9\), then a closed raw cube set in \(1+J\) is
> powerful.  Hence an exponent-nine algebra-group counterexample to Wilson's
> question must have \(\dim J\geq10\).

This is not a theorem about all finite \(3\)-groups.  A subsequent hand
argument (`DIM9_HUMAN_CUBE_COMMUTATIVITY.md`) replaced all four
nontrivial formulas.  The cross-solver results are now independent
regression checks rather than proof premises.

## The Wilson witness is necessary, not over-strong

For \(x\in J\), characteristic three gives

\[
(1+x)^3=1+x^3.
\]

Let \(S=\{1+x^3:x\in J\}\).  If \(S\) is a subgroup, call it \(H\).  Every
element of \(H\) is then itself a raw cube, rather than merely a product of
raw cubes.  Since \(J^9=0\),

\[
(1+x^3)^3=1+x^9=1.
\]

Thus the group-theoretic cube subgroup \(H^3\) is trivial.  For an odd-prime
group, powerfulness is \(H'\leq H^3\); here this is equivalent to \(H'=1\).
Consequently a closed non-powerful raw cube set necessarily contains
\(1+a^3,1+b^3\) with

\[
a^3b^3\ne b^3a^3.
\]

This is exactly the witness asserted in the three filtered CEGIS cores.  The
argument deliberately distinguishes the group subgroup \(H^3\) from the
algebra ideal \(J^9\).

Only input coordinates capable of contributing to a cube are quantified.
If the top filtration degree is seven, degrees above five cannot occur in a
nonzero triple product; if it is eight, degrees above six cannot occur.
The selected witness dimensions therefore still cover all \(a,b\in J\) as
far as their cubes are concerned.

## Exhaustiveness of the profile reduction

Writing \(d_i=\dim J^i/J^{i+1}\), noncommuting cubes require
\(J^6\ne0\), while one-generator associated graded algebras cannot supply
the witness, so \(d_1\ge2\).  For total dimension nine and \(J^9=0\), the
positive compositions have lengths six, seven, or eight:

\[
21+7+1=29.
\]

The reductions used in the main note were checked as follows.

- For a length-six profile with \(d_3=1\), two elements of \(J^3\) are
  proportional modulo \(J^4\); their commutator lies in \(J^7=0\).
- If \(d_2=1\), associativity forces \(d_3\le1\): writing
  \(A_2=\langle z\rangle\), choose \(y,w\) with \(yw\ne0\) in \(A_2\);
  the identity \((xy)w=x(yw)\) makes every \(xz\) proportional to one fixed
  vector in \(A_3\).
- The associated-graded product
  \(A_i\otimes A_j\to A_{i+j}\) is surjective because
  \(J^{i+j}=J^iJ^j\).  Hence
  \[
    d_{i+j}\leq d_i d_j.
  \]
  This removes the four length-seven shapes having their extra dimension in
  layers four through seven.

The surviving profiles are therefore exactly

\[
(2,2,2,1,1,1),\quad
(2,2,1,1,1,1,1),\quad
(3,1,1,1,1,1,1),\quad
(2,1,1,1,1,1,1,1).
\]

The first requires closure-specific necessary conditions.  The other three
were first ruled out by filtered associativity, power-layer surjectivity,
and the genuine noncommuting-cube witness, and are now ruled out by short
human cube-commutativity lemmas.

## Model-completeness checks

For each profile, the generator:

1. introduces every structure constant from a degree-\(i\) basis vector
   times a degree-\(j\) basis vector into every allowed layer
   \(k\geq i+j\);
2. writes every coordinate of \((xy)z=x(yz)\) for all basis triples;
3. requires full rank of every leading-layer map
   \(A_i\otimes A_j\to A_{i+j}\);
4. encodes \(\mathbb F_3\) addition and multiplication by complete
   two-bit truth tables and excludes the unused bit pattern `#b11`.

For \((2,2,2,1,1,1)\), closure makes the projected cube image an additive
subspace of \(A_3\).  Noncommutation forces two independent projected cubes:
if two leading terms were dependent, their commutator would lie in
\(J^7=0\).  Hence the nine-point cube map \(A_1\to A_3\) is bijective, and
choosing two preimages as the \(A_1\) basis loses no generality.  The model
then imposes one exact required root equation for their circle product.
These are necessary conditions, so UNSAT safely excludes the profile even
without encoding every closure pair.

## Independent solver results

The canonical formulas and outcomes are:

| profile | canonical SHA-256 | Z3 | cvc5 eager bit-blast |
|---|---|---:|---:|
| \((2,2,2,1,1,1)\) | `88c1c37...193de` | UNSAT | UNSAT |
| \((2,2,1,1,1,1,1)\) | `ce150591...bcb9c` | UNSAT | UNSAT |
| \((3,1,1,1,1,1,1)\) | `d7838ce3...d5bc` | UNSAT | UNSAT |
| \((2,1,1,1,1,1,1,1)\) | `f9ab4206...39d8a04` | UNSAT | UNSAT |

cvc5 was run with eager bit-blasting.  The four wall-clock times were 3.44,
1.25, 1.65, and 4.02 seconds.  The exact full hashes, memory figures, and
solver provenance are frozen in `dim9_cross_solver_results.txt`.

The official cvc5 1.3.3 static release archive matched its published
SHA-256, and the extracted binary has an independently recorded hash.  The
three CEGIS files request model values after `check-sat`; cvc5 prints a
harmless post-UNSAT message because model production is disabled.  The
preceding `unsat` result is unaffected.

## Remaining trust boundary

The two independent solvers remain useful regression checks.
`DIM9_HUMAN_CUBE_COMMUTATIVITY.md` replaces the three iteration-zero
formulas and the closure-aware profile \((2,2,2,1,1,1)\).  Thus no
dimension-nine UNSAT result contributes to the theorem's trust boundary.
For archival certificate quality, one could still add one of:

- proof-producing bit-blasting followed by a DRAT/LRAT checker;
- an independently generated SAT encoding;
- a short human algebraic contradiction extracted from minimized UNSAT
  cores.

The later dimension-ten audit is independent of this cross-solver theorem.
It now excludes all 92 in-scope profiles by human tensor and cyclic-tail
arguments.  The old timeout remains only an incomplete historical
checkpoint and is not a premise of the resulting \(\dim J\ge11\) bound.
