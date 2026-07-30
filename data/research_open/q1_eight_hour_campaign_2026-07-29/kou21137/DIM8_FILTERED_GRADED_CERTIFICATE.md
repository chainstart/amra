# Dimension-eight filtered-to-graded certificate

Date: 2026-07-30

## Claim and scope

Let \(J\) be an eight-dimensional nilpotent associative
\(\mathbb F_3\)-algebra with \(J^6\ne0\) and
\(\dim J/J^2\ge2\).  The human filtration reduction leaves one unresolved
profile:
\[
 \bigl(\dim J^i/J^{i+1}\bigr)_{i=1}^7
 =(2,1,1,1,1,1,1).                               \tag{1}
\]
The certificate proves computationally that (1) cannot have
\([J^3,J^3]\ne0\).  A later hand argument now proves the same fact and
supersedes the certificate as a trust requirement; see
`DIM9_HUMAN_CUBE_COMMUTATIVITY.md`.

This is a necessary-condition audit on the associated graded algebra, not
an enumeration of isomorphism classes of filtered algebras.

## Why the graded obstruction is sufficient

Put \(A=\operatorname{gr}J\).  In profile (1), \(A_i\) is
one-dimensional for \(2\le i\le7\), and \(J^8=0\).  For \(u,v\in J^3\),
their degree-three leading terms are proportional.  After replacing
\(v\) by \(v-\lambda u\), its first possible term lies in \(J^4\).
Therefore a nonzero \([u,v]\) would force
\[
 A_3A_4\ne A_4A_3\quad\text{in }A_7.             \tag{2}
\]
Ruling out (2) for every possible \(A\) rules out every filtered
deformation with profile (1).

## Encoding completeness

`search_dim8_algebra_profiles.py` uses basis \(x,y\) in degree one and
\(z_i\) in degree \(i\), \(2\le i\le7\).

- Every ordered basis product of total degree at most seven has one
  \(\mathbb F_3\) structure constant: 34 variables.
- The variables are represented by integers \(0,1,2\), and every
  polynomial identity is reduced modulo three.
- Every homogeneous basis triple of total degree at most seven is included:
  96 associativity equations.
- A power-filtration associated graded algebra satisfies
  \(J^{i+j}=J^iJ^j\) for every ordered split.  Because every target layer
  is one-dimensional, this is exactly the assertion that each product map
  \(A_i\otimes A_j\to A_{i+j}\) is nonzero.  All
  \(\sum_{n=2}^7(n-1)=21\) such surjectivity constraints are included.
- Products of total degree at least eight are zero on both sides of every
  remaining associativity identity, because \(J^8=0\).

Thus every associated graded algebra arising from (1) gives a satisfying
assignment of the base constraint system.

## Exact results

The base system is satisfiable, confirming that the profile constraints are
not vacuous.  Adding (2) makes the system unsatisfiable:

```text
DIM8_PROFILES|total=7|degree_forced_commuting=5|d2_one_d3_two_impossible=1|exceptional=2,1,1,1,1,1,1
DIM8_EXCEPTIONAL_SMT|variables=34|associativity=96|generation=21|field=3|profile_consistent=sat|noncommuting=unsat
DIM8_RESULT|J3_commutative=true|minimum_candidate_dimension=9
DONE
```

The canonical noncommuting SMT-LIB instance has:

```text
lines=188
bytes=9722
sha256=19f252a9fda4c93e8da8919e9ef0f1d8e47a42d046548eca18541c280e9dca00
```

`test_dim8_algebra_profiles.py` independently checks the transcript and
the canonical byte-level hash.

## Reproduce

```bash
python3 \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/search_dim8_algebra_profiles.py \
  --emit-smt /tmp/dim8_noncommuting.smt2

sha256sum /tmp/dim8_noncommuting.smt2
z3 /tmp/dim8_noncommuting.smt2
```

The final command must print `unsat`.

## Human replacement and trust boundary

The profile enumeration, the six easy eliminations, and the
filtered-to-graded implication are human-checkable.  The former last
solver-dependent profile has \(J^8=0\) and
\(\dim A_3=\dim A_4=\dim A_6=1\).  Lemma 1 of
`DIM9_HUMAN_CUBE_COMMUTATIVITY.md` proves directly that all its cubes
commute.  Therefore the unconditional paper-level boundary is now
\[
\dim J\ge9.
\]
The SMT instance remains archived as an independent regression check, not
as a premise of this bound.
