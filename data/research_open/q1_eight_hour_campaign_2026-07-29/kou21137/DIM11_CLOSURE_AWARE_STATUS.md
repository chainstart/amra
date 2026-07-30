# Dimension-eleven closure-aware profile status

Date: 2026-07-30

## Exact scope and result

Let \(J\) be an eleven-dimensional nilpotent associative
\(\mathbb F_3\)-algebra with \(J^9=0\), and put \(A_i=J^i/J^{i+1}\).
Noncommuting cubes require \(J^6\ne0\) and
\(\dim A_1\ge2\).  Positive-composition enumeration over lengths six
through eight gives
\[
126+84+36=246
\]
profiles.  Length nine is outside the \(J^9=0\) scope.

The exact closure-aware profile ledger is

```text
DIM11_PROFILES|total=246|length6=126|length7=84|length8=36|length9=0|after_layer_rank=65|after_quadratic_relation=59|after_one_layer=23|after_degree=19|after_tail_tensor=12|after_length7_power=8|after_cyclic_j3_tail=5|after_length8_cyclic_basis=2|structural_survivors=2|profile_candidates_after_length6_closure=1|after_qdim_branches=0|closure_survivors=0
```

The two profiles surviving the structural and cube-commutativity
arguments are
\[
(2,2,2,2,2,1),\qquad
(2,2,2,2,1,1,1).                                \tag{1}
\]
Raw-cube closure excludes the first.  The profile-level pass initially
left
\[
(2,2,2,2,1,1,1).                                \tag{2}
\]
The branch analysis below excludes both possible dimensions of its
leading cube image.  Consequently there is no dimension-eleven profile
supporting a closed, noncommuting raw cube set under the stated
\(J^9=0\) hypothesis.

The structural reductions and the \(\dim Q=1\) exclusion are
solver-free.  The \(\dim Q=2\) exclusion uses, at one explicitly marked
step, the exact finite row reduction of all 12 q-bijective quadratic
relation planes (drawn from the 130-plane Grassmannian).  Thus the final
result is finite-audit-assisted, not claimed wholly human-only.

## Human filters

The enumeration uses only the following proved implications.

1. Every graded product is onto, so
   \(d_{i+j}\le d_i d_j\).
2. If \(d_2=2\), then \(d_3\le2\), with no restriction on \(d_1\).
   Put \(V=A_1\), \(\dim V=m\), and
   \(R=\ker(V^{\otimes2}\twoheadrightarrow A_2)\), so
   \(\dim R=m^2-2\).  There is a natural surjection
   \[
   V^{\otimes3}/(V\otimes R+R\otimes V)
   \twoheadrightarrow A_3.
   \]
   Row-reducing \(R\) in an admissible word order leaves only two
   nonpivot quadratic words.  The degree-three quadratic cover is
   spanned by words whose two adjacent quadratic subwords are nonpivot
   words: every other word reduces strictly, and overlap ambiguities can
   only add relations.  Regard the two allowed quadratic words as two
   distinct directed edges on the \(m\) basis letters.  Their length-two
   directed paths span the cover, and two distinct directed edges support
   at most two such paths, even when loops are allowed.  Hence
   \(d_3\le2\).  This excludes both
   \((2,2,3,1,1,1,1)\) and
   \((3,2,3,1,1,1)\) in the dimension-eleven ledger.
3. For \(i\ge2\), the shift-tensor argument gives
   \(d_i=1\Rightarrow d_{i+1}\le1\).
4. If \(J^7=0\) and \(d_3=1\), cubes commute by degree.
5. If \(J^7=0\) and \(d_5=d_6=1\), the pure sixfold tensor makes cubes
   commute.
6. The length-seven power lemma and cyclic-\(J^3\) lemma from the
   dimension-ten audit apply unchanged.
7. If \(J^9=0\), \(d_3=2\), and \(d_4=\cdots=d_8=1\), the
   cyclic-\(J^3\) proof extends by one layer.  Choose \(t\) so that
   \(t^4,\ldots,t^8\) is a filtration basis of \(J^4\), and choose
   \(u\in J^3\) in the common left/right kernel.  Write
   \[
   ut=\sum_{i=5}^8a_it^i,\qquad
   tu=\sum_{i=5}^8a'_it^i.
   \]
   Associativity \((tu)t=t(ut)\) gives
   \(a_i=a'_i\) for \(5\le i\le7\).  Hence
   \[
   ut^3=t^3u,\qquad ut^4=t^4u.
   \]
   Products with \(t^5,t^6,t^7,t^8\) vanish by degree.  Thus
   \(t^3,u,t^4,\ldots,t^8\) is a commuting filtration basis of \(J^3\).
8. If \(d_3=\cdots=d_8=1\), the pure word tensors make
   \(t^3,\ldots,t^8\) a filtration basis of \(J^3\), so it is
   commutative.

These filters leave exactly the two profiles in (1).

## Closure lemma for the sharp length-six profile

**Lemma.**  Suppose \(J^7=0\),
\[
\dim A_1=\dim A_3=2,\qquad \dim A_6=1,
\]
and the raw cube set
\[
H=P_3(1+J)=\{1+x^3:x\in J\}
\]
is closed.  Then all raw cubes commute.

**Proof.**  Projection to \(A_3\) is a group homomorphism from \(H\)
to the additive group of \(A_3\), because products of elements of
\(J^3\) start in \(J^6\).  Its image is
\[
Q=\{v^3:v\in A_1\}\subseteq A_3,
\]
so closure makes \(Q\) a linear subspace.

If \(\dim Q\le1\), any two cubes have proportional degree-three
components.  After subtracting a scalar multiple, one factor lies in
\(J^4\), and its commutator with \(J^3\) lies in \(J^7=0\).
Thus noncommuting cubes would force \(Q=A_3\).  Since \(A_1\) and
\(A_3\) both have nine elements, the leading cube map
\[
q:A_1\longrightarrow A_3,\qquad v\longmapsto v^3
\]
would then be bijective.

Let \(K\) be the kernel of \(H\to A_3\).  If a raw cube lies in \(K\),
bijectivity of \(q\) forces its root to lie in \(J^2\), hence the cube
has algebra component in \(J^6\).  Therefore \(K\subseteq1+J^6\).  If
two cubes do not commute, their group commutator is a nonidentity
element of \(K\cap(1+J^6)\).  As \(A_6=J^6\) is one-dimensional, this
gives
\[
K=1+J^6.                                         \tag{3}
\]

Two raw cubes in the same \(A_3\)-fibre differ additively by an element
of \(J^6\).  Indeed, for \(c,d\in J^3\),
\[
(1+c)^{-1}(1+d)
=1+d-c+c^2-cd,
\]
and the last two displayed terms already lie in \(J^6\).  Membership
of the left side in \(K\) therefore implies \(d-c\in J^6\).

Now take arbitrary \(v\in J\) and \(z\in J^3\).  The roots \(v\) and
\(v+z\) have the same \(A_1\)-component, so their cubes lie in the
same \(A_3\)-fibre.  Since every term containing at least two copies of
\(z\) lies in \(J^7=0\),
\[
D:=(v+z)^3-v^3=v^2z+vzv+zv^2\in J^6.            \tag{4}
\]
Consequently \(vD=Dv=0\).  Expanding their difference gives
\[
0=vD-Dv=v^3z-zv^3.                              \tag{5}
\]
Taking \(z=x^3\) proves that \(v^3\) commutes with every raw cube
\(x^3\).  Hence all raw cubes commute. \(\square\)

The profile \((2,2,2,2,2,1)\) satisfies the lemma.  Closure therefore
excludes it, even though the explicit algebra in
`DIM11_SHARP_NONCOMMUTING_CUBE_WITNESS.md` proves that the same profile
can have noncommuting cubes when closure is dropped.

## Cheap closure invariants and the sharp witness

For any closed raw cube set, \(Q\) must be a linear subspace and all
nonempty fibres of \(H\to Q\) must be cosets of one kernel, hence have
equal size.  The sharp witness has:

- 171 raw cubes;
- a seven-point, nonadditive leading image in \(A_3\);
- one leading fibre of size 9 and six fibres of size 27.

It therefore fails closure before any full circle-product enumeration is
needed.  The exhaustive verifier checks these counts as well as a
specific missing circle product.

## Bounded computational probes

The following experiments are diagnostics, not theorem premises.

1. A complete filtered model for \((2,2,2,2,2,1)\), with 220 structure
   variables, all 400 associativity coordinates, all 15 ordered layer
   surjections, arbitrary noncommuting cube witnesses, and only the
   necessary condition that \(Q\subseteq A_3\) be additively closed,
   returned `SAT` in 102,854 ms.  Its concrete raw cube image had 219
   values and a missing circle product.  Thus leading-image closure alone
   is strictly weaker than raw-cube closure.
2. Adding one complete symbolic cube root for that concrete missing
   circle product returned `timeout` after 210,108 ms.
3. Replacing projected-image closure by its closure-plus-noncommutation
   consequence that \(q:A_1\to A_3\) is bijective, normalizing a
   noncommuting pair to the two basis roots, and requiring one complete
   root for their circle product returned `timeout` after 210,100 ms.

Neither timeout is evidence for satisfiability or unsatisfiability.  The
human lemma above supersedes all three computations for the length-six
profile.

## Final exclusion of the length-seven profile

Let \(Q\subseteq A_3\) be the leading cube image and
\(K=\ker(H\to Q)\).  The dimension-ten quotient \(J/J^7\) is covered by
the consecutive-tail tensor lemma, so every cube commutator lies in
\(J^7\).  Hence a noncommuting closed cube set has
\[
J^7\ne0,\qquad 1+J^7\subseteq K.
\]
If \(Q=0\), then \(H\subseteq1+J^4\), which is abelian because
\((J^4)^2\subseteq J^8=0\).  Thus noncommutation forces
\(\dim Q\in\{1,2\}\).

If \(\dim Q=2\), then \(q:A_1\to Q\) is bijective, so every element of
\(K\) has a root in \(J^2\) and
\[
1+J^7\subseteq K\subseteq1+J^6.
\]
Both \(J^7\) and \(J^6/J^7\) are one-dimensional, hence either
 \(K=1+J^7\) or \(K=1+J^6\).  The first case is impossible.  Indeed, for
 \(v\in J,z\in J^3\), the cubes of \(v\) and \(v+z\) have the same
leading value.  If \(K=1+J^7\), their additive difference lies in \(J^7\):
the correction converting group-fibre difference to additive difference
is \(v^3\bigl((v+z)^3-v^3\bigr)\in J^7\).  Thus
\[
E=(v+z)^3-v^3\in J^7.
\]
Now \(vE=Ev=0\).  In \(vE-Ev\), all terms containing two copies of
\(z\) lie in \(J^8=0\), leaving
\[
v^3z-zv^3=0.
\]
Taking \(z=x^3\) again contradicts noncommuting cubes.

Therefore the profile in (2) satisfies the fail-closed contract
\[
\dim Q=1\quad\text{or}\quad
\bigl(\dim Q=2,\ K=1+J^6,\ |H|=81\bigr).         \tag{6}
\]
In the second branch, every element of \(J^6\) must be the cube of an
element of \(J^2\).  A degree count alone would not make this cube
depend only on \(A_2\): changing a root by \(z\in A_3\) produces
\[
L_w(z)=w^2z+wzw+zw^2\in A_7.
\]
For these profiles, however, the pure tail tensor forces this correction
to vanish.  Let \(V=A_1\), and let
\(q_2:V^{\otimes2}\twoheadrightarrow A_2\) and
\(q_3:V^{\otimes3}\twoheadrightarrow A_3\) be the word maps.
The pure forms \(f_5,f_6,f_7=c_i\ell^{\otimes i}\) make
\(\ell^{\otimes2}\) and \(\ell^{\otimes3}\) descend to nonzero
functionals
\[
\lambda\in A_2^*,\qquad \rho\in A_3^*.
\]
Each of the three ordered maps with factors \(A_2,A_2,A_3\) is the same
scalar tensor \(c\,\lambda\otimes\lambda\otimes\rho\), with the factors
permuted.  Hence
\[
L_w(z)=3c\,\lambda(w)^2\rho(z)=0.                \tag{7}
\]
Thus, after this tail argument, the cube really does descend to a
well-defined map
\[
P:A_2\longrightarrow J^6.
\]
Since \(K=1+J^6\), \(P\) is a bijection of two nine-point sets.  Its
leading coordinate is
\[
p_6(w)=c\,\lambda(w)^3=c\,\lambda(w).
\]
Choose coordinates \(w=(x,y)\) with \(p_6(w)=x\).  The \(A_7\)
coordinate is a homogeneous cubic function
\[
h(x,y)=a x^3+b x^2y+c'xy^2+d y^3.
\]
Bijectivity on each of the three fibres of \(x\) gives
\[
c'=0,\qquad d\ne0,\qquad b+d\ne0.
\]
Scaling the \(A_7\) coordinate, and replacing the chosen lift of the
\(A_6\) basis vector by that lift plus a multiple of \(A_7\), reduces
the complete map to exactly two normal forms:
\[
\boxed{\quad
P_0(x,y)=(x,y),\qquad
P_1(x,y)=\bigl(x,(1+x^2)y\bigr).
\quad}                                           \tag{8}
\]
### Exclusion of the two-dimensional leading branch

Because \(K=1+J^6\), roots with the same \(A_1\)-component have cubes whose
additive difference lies in \(J^6\).  Take
\(v\in A_1,w\in A_2\) and compare the cubes of lifts of \(v\) and
\(v+w\).  The degree-four component gives the polynomial identity
\[
v^2w+vwv+wv^2
=\operatorname{ad}_v^2(w)=0
\quad\text{in }A_4.                              \tag{9}
\]
In characteristic three,
\(\operatorname{ad}_v^3=\operatorname{ad}_{v^3}\).  Applying
\(\operatorname{ad}_v\) to (9) therefore gives
\[
[q(v),w]=0\quad\text{in }A_5.                   \tag{10}
\]
Since \(q(A_1)=Q\), equation (10) says
\[
[Q,A_2]=0\quad\text{in }A_5.
\]
For the profile in (2), \(Q=A_3\) in this branch.

There is also a useful section formulation.  Modulo \(J^6\), products
of elements of \(H\subseteq1+J^3\) disappear.  Hence
\[
S:=H/(1+J^6)
\]
is a two-dimensional additive subspace of \(J^3/J^6\), represented
exactly by the nine cubes of degree-one roots.  Noncommutation is then
a nonzero alternating central cocycle
\[
S\times S\longrightarrow J^7.
\]
The identities in (9) and their degree-five counterparts
\[
\operatorname{ad}_w^2(v)=0
\quad(v\in A_1,\ w\in A_2)
\]
give a small quadratic lemma.  If the leading cube map is bijective and
\(d_4=2\), row reduction of the quadratic relation plane using (9)
forces the graded algebra to be commutative through degree four.  The
exact 130-plane audit reduces this to only 12 bijective planes: three
violate \(d_4=2\), and the remaining nine all contain \(xy-yx\).

The rest is human linear algebra.  The natural map from
\[
B=\mathbb F_3[x,y]/(f),
\]
where \(f\) is a quadratic form and \(\dim B_n=2\) for every \(n\ge1\),
to \(\operatorname{gr}J\) is an isomorphism in degrees zero through
four.
Bijectivity of \(v\mapsto v^3\) excludes \(f=\ell^2\).  If \(f\) is
irreducible, then \(B\) is a domain.  The single new degree-five
relation \(0\ne g\in B_5\) would make \(xg,yg\) linearly independent:
a dependence would give a nonzero linear annihilator of \(g\).
Consequently \(A_6=0\), contrary to \(d_6=1\).  Thus \(f=\ell m\) with
distinct linear factors.  After changing basis,
\[
B=\mathbb F_3[x,y]/(xy).
\]
Write \(g=\alpha x^5+\beta y^5\).  Since \(d_6=1\), exactly one of
\(\alpha,\beta\) is
nonzero.  Renaming the generators gives a long generator \(a\) and a
short generator \(b\) such that
\[
ab=ba=0\text{ in }A_2,\qquad
b^2\ne0,\qquad b^5=0\text{ in }A_5,
\]
\[
a^6\ne0\text{ in }A_6,\qquad a^6b=0\text{ in }A_7. \tag{11}
\]
Equivalently, through degree seven these are the two possible
degree-five truncations of the same two-chain quadratic algebra.

Choose actual lifts, still denoted \(a,b\).  Since the class of \(b^5\)
in \(A_5\) is zero, \(b^5\in J^6\).  Its class in the
one-dimensional \(A_6\) is a scalar multiple of \(a^6\).  Equation
(11) then gives
\[
b^6=b^5b\in J^8=0.                              \tag{12}
\]
On the other hand, \([b^2]\ne0\) in \(A_2\), while the well-defined
bijection \(P:A_2\to J^6\) satisfies
\[
P([b^2])=(b^2)^3=b^6=0,
\]
a contradiction.  Thus the \(\dim Q=2\) branch is impossible.

### Exclusion of the one-dimensional leading branch

The pure degree-seven word tensor gives this branch without a
relation-plane classification.  If \(V=A_1\), the one-dimensional
layers \(A_5,A_6,A_7\) give a common nonzero
\(\ell\in V^*\) such that the degree-seven word form is a scalar
multiple of \(\ell^{\otimes7}\).  The word maps
\(V^{\otimes3}\twoheadrightarrow A_3\) and
\(V^{\otimes4}\twoheadrightarrow A_4\) are surjective.  Therefore the
two products \(A_3A_4\to A_7\) and \(A_4A_3\to A_7\) are induced by
the same symmetric pure tensor.  They agree, and hence
\[
[J^3,J^4]\subseteq J^8=0.                       \tag{14}
\]
This loses no filtered component: equality in \(A_7\) puts the actual
commutator one filtration level deeper.

Now \(H/K\cong C_3\), while \(K\subseteq1+J^4\).
Because \(J^4J^4\subseteq J^8=0\), \(K\) is abelian; by (14), it is
also central in \(H\subseteq1+J^3\).  A group with central kernel and
cyclic quotient is abelian.  This contradicts the assumed
noncommutation and excludes \(\dim Q=1\).

The two branches in (6) are exhausted, completing the dimension-eleven
exclusion.

## Finite leading-map and SAT audits

The quadratic-relation lemma has an independent exhaustive certificate.
The Grassmannian \(\operatorname{Gr}(2,4)(\mathbb F_3)\) contains 130
relation planes \(R\subseteq V^{\otimes2}\).  For each one,
`audit_quadratic_relation_d3_bound.py` computes
\[
\dim\frac{V^{\otimes3}}{V\otimes R+R\otimes V}.
\]
The distribution in dimensions \(0,1,2\) is respectively
\[
48,\quad48,\quad34;
\]
the maximum is two.  This independently certifies the human normal-word
proof and the exclusion of \((2,2,3,1,1,1,1)\).

For transparency, all 12 \(q\)-bijective planes have the following
reduced row bases.  Coordinates are ordered as
\((x^2,xy,yx,y^2)\).  The first three have closure-forced
\(d_4=1\); the other nine have \(d_4=2\):

| plane | row 1 | row 2 | \(d_4\) | quadratic type |
|---:|:---:|:---:|---:|:---:|
| 33 | 1001 | 0111 | 1 | noncommutative |
| 34 | 1001 | 0112 | 1 | noncommutative |
| 44 | 1002 | 0110 | 1 | noncommutative |
| 2 | 0100 | 0010 | 2 | split |
| 6 | 0101 | 0011 | 2 | split |
| 10 | 0102 | 0012 | 2 | split |
| 35 | 1001 | 0120 | 2 | irreducible |
| 47 | 1002 | 0120 | 2 | split |
| 57 | 1010 | 0120 | 2 | split |
| 75 | 1012 | 0120 | 2 | irreducible |
| 85 | 1020 | 0120 | 2 | split |
| 103 | 1022 | 0120 | 2 | irreducible |

Each of the nine \(d_4=2\) row spans contains
\(xy-yx=(0,1,2,0)\).  Thus the finite classification used above is
directly inspectable rather than hidden in the script; the audit
independently recomputes the three \(d_4=1\) cases and the \(6+3\)
factorization split at \(d_4=2\).

`audit_dim11_q2_graded_frontend.py` independently implements the
degree-four and degree-five adjoint identities.  It obtains the exact
counts \(13\), \(52\), \(36\), and \(16\) above.  The canonical list of
16 plane/line identifiers has SHA-256
`522c35248e7a9b89c36e3721b82e9cc02b5e23cc67abc9e7830b65e09af225b5`.
Exactly 12 of these have nine-point leading cube image; their identifier
list has SHA-256
`0d1c635b34705e1897ad49a99aa6671cc0b58655e629b35cf496f05dcb06b018`.

`audit_dim11_q1_quadratic_commutativity.py` gives the exact distribution
\[
(\dim\langle q\rangle,z)=(1,1):4,\ (2,0):12,\
(2,1):12,\ (2,2):6,
\]
where \(z\) counts projective zero lines.  It checks that all four
one-dimensional cases contain \(xy-yx\).  Their canonical certificate
has SHA-256
`b3f6aefed10886a698b7a7885da76b4872bed22663933912a655817aa03eb9d3`.
This is an independent cross-check of the pure-tensor proof, not a
premise of it.

`audit_dim11_q2_short_chain_obstruction.py` checks (11) in all 12
nine-point-image cases.  The certificate has SHA-256
`f38c984c190c7cc4c9d322b091080c49351d4b284ea6fcc8b0aaf7f212195676`.

A homogeneous cubic map on \(\mathbb F_3^2\) is an odd function and is
determined by its values on the four projective lines.  Evaluation of
\(x^3,x^2y,xy^2,y^3\) on four line representatives is nonsingular, so
every such choice occurs at the level of cubic polynomial functions.
Consequently:

- the one-dimensional branch has 80 nonzero scalar leading functions;
  according as 0, 1, 2, or 3 projective input lines map to zero, their
  counts are 16, 32, 24, and 8.  Closure plus noncommutation excludes
  the 16 zero-free functions, while the pure-tail identity reduces the
  actual leading maps to eight nonzero linear maps and one basis normal
  form;
- the two-dimensional branch has
  \(4!\,2^4=384\) abstract odd bijections and two pure-tail leading
  normal forms;
- the required nonzero scalar leading cube maps \(A_2\to A_6\) also
  have 80 abstract possibilities.  The tail-pure descent reduces these
  to the 8 nonzero linear functionals, and filtered basis changes reduce
  the complete \(A_2\to J^6\) cube map to the two normal forms in (8).

Thus leading functions alone do not exclude either branch; the
pure-tensor and quadratic short-chain arguments above do.
`analyze_dim11_closure_branches.py` reproduces these exact counts.

A deliberately incomplete graded SMT probe for
\((2,2,2,2,1,1,1)\) includes 300 leading associativity coordinates,
all 21 layer surjections, the 36 constraints making
\(q:A_1\to A_3\) bijective, and the 36 coordinates of (9).  It returns
`SAT`.  The query explicitly omits filtered higher associativity,
condition (8), full raw-cube closure, and a noncommuting-cube witness.
It proves only that (9) does not already contradict the associated
graded profile.  The larger complete-filtered necessary-condition probe
did not return within 180,084 ms and was stopped; this is not evidence
for either SAT or UNSAT.

A direct complete-filtered query for the first cube normal form \(P_0\)
also timed out after 150,036 ms.  The \(P_1\) query was then stopped
without a terminal solver result to avoid spending a second identical
budget.  Neither timeout is an exclusion; both are superseded by the
short-chain proof.

## Reproduction

```bash
python3 search_dim11_algebra_profiles.py
python3 -m unittest test_dim11_algebra_profiles.py
python3 audit_quadratic_relation_d3_bound.py
python3 -m unittest test_audit_quadratic_relation_d3_bound.py
python3 audit_dim11_q2_graded_frontend.py
python3 -m unittest test_audit_dim11_q2_graded_frontend.py
python3 audit_dim11_q1_quadratic_commutativity.py
python3 -m unittest test_audit_dim11_q1_quadratic_commutativity.py
python3 audit_dim11_q2_short_chain_obstruction.py
python3 -m unittest test_audit_dim11_q2_short_chain_obstruction.py
python3 analyze_dim11_closure_branches.py
python3 -m unittest test_analyze_dim11_closure_branches.py
python3 probe_dim11_q2_graded_2222111.py
python3 -m unittest test_probe_dim11_q2_graded_2222111.py
python3 verify_dim11_sharp_noncommuting_cubes.py
pytest -q test_verify_dim11_sharp_noncommuting_cubes.py
```
