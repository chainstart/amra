# Closure-aware triage of the dimension-twelve frontier

Date: 2026-07-30

## Scope and outcome

Let \(J\) be a twelve-dimensional nilpotent associative
\(\mathbb F_3\)-algebra with \(J^9=0\), and suppose
\[
H=\{1+x^3:x\in J\}
\]
is a nonabelian subgroup of \(1+J\).  This note applies closure
arguments to the eight necessary profiles in `DIM12_NEXT_FRONTIER.md`.

Three profiles are excluded:
\[
(2,2,2,2,2,2),\qquad
(2,2,2,2,2,1,1),\qquad
(2,2,2,3,1,1,1).
\]
The other five receive stricter necessary branch contracts.  None is
proved realizable.  Thus the result is a triage, not a dimension-thirteen
lower bound.

The first exclusion is solver-free end to end.  The terminal
cross-relation contradiction for the second is human, but it inherits
the exact 12-plane quadratic normal-form reduction used in the
dimension-eleven proof.  Thus `human_excluded=2` in the ledger counts
the form of the terminal exclusion argument, not a wholly
computation-free dependency chain.  The third,
\((2,2,2,3,1,1,1)\), is excluded directly by the finite exact
130-plane row-reduction certificate and is kept in the separate
finite-audit count.

## Two reusable closure lemmas

Put \(A_i=J^i/J^{i+1}\), let
\[
Q=\{v^3:v\in A_1\}\subseteq A_3,
\]
and let \(K\) be the kernel of \(H\to Q\).  Closure makes \(Q\) a linear
subspace and all nonempty fibres cosets of \(K\).

### Length-six fibre lemma without an \(A_6\) rank hypothesis

**Lemma 1.**  Suppose \(J^7=0\) and
\(\dim A_1=\dim A_3=2\).  If the raw cubes are closed, then they
commute.

**Proof.**  If \(\dim Q\le1\), the alternating leading commutator
\[
Q\wedge Q\longrightarrow A_6
\]
vanishes, and there is no \(J^7\) correction.  Hence all cubes commute.
Otherwise \(Q=A_3\).  The leading cube map
\(q:A_1\to A_3\) is then a bijection of two nine-point sets.  Therefore
every cube in \(K\) has a root in \(J^2\), and \(K\subseteq1+J^6\).

For \(v\in J\) and \(z\in J^3\), the cubes of \(v\) and \(v+z\) have
the same leading value.  Their additive difference consequently lies
in \(J^6\); the correction between group-fibre and additive difference
also lies in \(J^6\).  Since terms containing two copies of \(z\) lie
in \(J^7=0\),
\[
D=(v+z)^3-v^3=v^2z+vzv+zv^2\in J^6.
\]
Thus \(vD=Dv=0\), while direct expansion gives
\[
0=vD-Dv=v^3z-zv^3.
\]
Taking \(z=x^3\) proves that all raw cubes commute. \(\square\)

The proof uses no assumption on \(\dim A_6\).

### Pure degree-seven tail lemma

**Lemma 2.**  Suppose \(J^8=0\) and
\(\dim A_6=\dim A_7=1\).  Then the degree-seven word form is a scalar
pure tensor \(c\ell^{\otimes7}\).  Consequently
\[
A_3A_4=A_4A_3\quad\text{in }A_7,
\qquad [J^3,J^4]=0.
\]

**Proof.**  Let \(V=A_1\) and let
\(F_6:V^{\otimes6}\twoheadrightarrow A_6\) be the word form.  The two
surjective products \(VA_6\to A_7\) and \(A_6V\to A_7\) give nonzero
linear forms \(\ell_L,\ell_R\in V^*\).  Associativity says
\[
\ell_L(v_1)F_6(v_2,\ldots,v_7)
=F_6(v_1,\ldots,v_6)\ell_R(v_7).
\]
Successively fixing arguments on which the displayed forms are nonzero
forces \(\ell_L,\ell_R\) to be proportional to one form \(\ell\) and
\(F_6=c'\ell^{\otimes6}\).  Hence
\(F_7=c\ell^{\otimes7}\).  The products \(A_3A_4\to A_7\) and
\(A_4A_3\to A_7\) are therefore induced by the same symmetric tensor.
Their lifted commutator lies in \(J^8=0\). \(\square\)

In particular, in every length-seven frontier profile the branches
\(\dim Q=0\) and \(\dim Q=1\) are abelian.  For \(\dim Q=1\),
\(K\subseteq1+J^4\), Lemma 2 makes \(K\) central in \(H\), and
\(H/K\cong C_3\).

## The two length-six profiles

### Profile \((2,2,2,2,2,2)\)

Lemma 1 applies directly, so this profile is excluded.

### Profile \((3,2,2,2,2,1)\)

Here noncommutation forces \(Q=A_3\), so
\[
q:\mathbb F_3^3\longrightarrow\mathbb F_3^2
\]
is surjective as a function.  The group \(K\subseteq1+J^4\) is central
and additive, and the nonzero alternating commutator
\[
\bigwedge^2Q\longrightarrow J^6
\]
is onto.  Thus \(1+J^6\subseteq K\), and
\[
|H|=9|K|,\qquad 1\le\dim K\le5.
\]

There is a sharper necessary condition.  If \(q(v)=0\) only for
\(v=0\), then every element of \(K\) has a root in \(J^2\), so
\(K\subseteq1+J^6\).  Hence \(K=1+J^6\), and the proof of Lemma 1 from
the fibre-difference step onward again forces all cubes to commute.
Therefore any nonabelian example in this profile must satisfy
\[
\boxed{\ \exists\,0\ne v\in A_1:\ v^3=0\text{ in }A_3.\ }       \tag{1}
\]
The precise obstruction is now the interaction between cubes rooted on
this projective zero locus and the higher components of \(K\); the
bijective-fibre argument no longer puts \(K\) inside \(J^6\).

## The five length-seven profiles

For each length-seven candidate, the closed cube image in \(J/J^7\)
is abelian: for \((2,2,2,2,2,1,1)\) this follows from Lemma 1, and for
the other four profiles it follows from the length-six pure-tail lemma.
Thus every cube commutator lies in \(J^7\).

For the four profiles with \(d_1=2\),
\[
\begin{gathered}
(2,2,2,2,2,1,1),\quad(2,2,2,3,1,1,1),\\
(2,3,2,2,1,1,1),\quad(2,3,3,1,1,1,1),
\end{gathered}
\]
Lemma 2 excludes \(\dim Q\le1\).  Since \(A_1\) has nine points,
\(\dim Q=2\) and \(q:A_1\to Q\) is bijective.  It follows that
\[
1+J^7\subseteq K\subseteq1+J^6.
\]
Both successive layers are one-dimensional.  If \(K=1+J^7\), comparison
of the cubes of \(v\) and \(v+z\), \(z\in J^3\), puts their difference
in \(J^7\); multiplying its commutator by \(v\) and using \(J^8=0\)
again forces \(v^3z=zv^3\).  Hence noncommutation requires
\[
\boxed{\ K=1+J^6,\qquad |H|=81.\ }               \tag{2}
\]

The pure form in Lemma 2 also kills the degree-seven correction produced
when a root in \(J^2\) is changed by an element of \(J^3\).  Cubing
therefore descends to a well-defined surjection
\[
P:A_2\longrightarrow J^6.                       \tag{3}
\]
It is a bijection when \(d_2=2\), and has domain size \(27\) and target
size \(9\) when \(d_2=3\).

For \((2,2,2,2,2,1,1)\), the quadratic argument can be sharpened.
The closure identity \(\operatorname{ad}_v^2(A_2)=0\) and cube
bijectivity force the quadratic graded quotient to be commutative.
The natural map from \(B=\mathbb F_3[x,y]/(f)\) to
\(\operatorname{gr}J\) is then an isomorphism through degree five.
A square \(f\) contradicts cube bijectivity, while for irreducible
\(f\) the domain property makes the new degree-six relation kill
\(A_7\).  Thus \(f=xy\).  The degree-six relation stops exactly one
chain, say the \(b\)-chain:
\[
[b^2]\ne0,\qquad b^6=0\text{ in }A_6.
\]
At first sight the actual element \(b^6\) could be a nonzero member of
\(J^7\), avoiding the dimension-eleven short-chain contradiction.
Associativity of the filtered cross-relations instead excludes the
whole branch.

Choose lifts \(a,b\in J\).  Since \(ab=ba=0\) in \(A_2\), write
\[
\overline{ab}=\alpha a^3+\beta b^3,\qquad
\overline{ba}=\gamma a^3+\delta b^3
\quad\text{in }A_3.
\]
The identities \((ab)a=a(ba)\) and \((ba)b=b(ab)\) give in \(A_4\)
\[
\alpha a^4=\gamma a^4,\qquad
\delta b^4=\beta b^4.
\]
The mixed graded products vanish and \(a^4,b^4\) are nonzero, so
\(\alpha=\gamma\) and \(\beta=\delta\).  Therefore
\[
[a,b]\in J^4.                                   \tag{4}
\]
Repeated use of \([xy,z]=x[y,z]+[x,z]y\) expands
\([a^3,b^3]\) into nine terms.  Each contains one copy of
\([a,b]\), two additional copies of \(a\), and two additional copies
of \(b\), and hence lies in \(J^8=0\).  Thus
\([a^3,b^3]=0\).

The quotient \(H/K\) is generated by the images of
\(1+a^3,1+b^3\), while \(K=1+J^6\) is central in \(H\) because
\([J^6,J^3]\subseteq J^9=0\).  Its two displayed lifts commute, so
\(H\) is abelian, a contradiction.  This excludes
\((2,2,2,2,2,1,1)\).

For \((2,2,2,3,1,1,1)\), the same closure reduction makes \(q\)
bijective and gives
\(\operatorname{ad}_v^2(A_2)=0\) in \(A_4\).
The exact quadratic relation lemma has only 12 q-bijective planes.
After adjoining this degree-four identity, three have degree-four
quotient dimension one and the other nine have dimension two.  Thus
\[
d_4\le2,
\]
contrary to the required \(d_4=3\).  This excludes the profile.  The
12-case row reduction is independently reproduced by
`audit_dim11_q2_graded_frontend.py`; despite its historical filename,
this quadratic lemma is independent of the total algebra dimension
under its stated \(d_1=d_2=d_3=2\), cube-bijectivity and closure
identity hypotheses.

For \((2,3,2,2,1,1,1)\), the corresponding exact front-end is larger
but still finite.  There are 40 quadratic relation lines.  Enumerating
all cubic extensions with \(d_3=2\), nine-point leading cube image, the
degree-four identity
\(\operatorname{ad}_v^2(A_2)=0\), and \(d_4=2\) leaves 36 cases.
For the degree-five identity
\(\operatorname{ad}_w^2(A_1)=0\), all 13 projective directions in the
three-dimensional \(A_2\) are imposed.  The four projective
degree-five extensions of each case give 144 cases.  Propagation to
degrees six and seven, together with surjectivity of the leading
\(A_2\)-cube map onto \(A_6\), splits them exactly as
\[
\begin{array}{c|c}
(d_6,d_7,\lvert\operatorname{im}(w\mapsto w^3)\rvert)&
\text{number}\\ \hline
(0,0,1)&96\\
(1,1,3)&48.
\end{array}
\]
The 48 retained identifiers have SHA-256
`80fd2b21a7b59d1b542b759b5f20a062f451cca9c6dcdf96191e4eef386183ef`.
This is only a necessary associated-graded reduction: filtered
associativity and raw closure are not encoded.  The independent
certificate is `audit_dim12_2322111_graded_frontend.py`.

There is no value in treating the 48 strict homogeneous quotients as
counterexample candidates.  In a homogeneous quotient the degree-six
cube commutator is already zero in the length-six quotient, while the
only possible degree-seven terms pair \(A_3\) with \(A_4\); Lemma 2
makes those products symmetric.  Hence the cubes commute in every one
of the 48 homogeneous quotients.  A genuine nonabelian candidate must
be a filtered lift carrying an additional terminal
\(A_3A_3\to A_7\) correction.  That filtered deformation is explicitly
outside the graded certificate.

For the \(d_1=3\) length-seven profile
\((3,2,2,2,1,1,1)\), Lemma 2 still forces \(Q=A_3\), but
\[
q:\mathbb F_3^3\to\mathbb F_3^2
\]
is not injective a priori.  If its projective zero locus is empty, the
same argument gives \(K=1+J^6\) and a bijection \(P:A_2\to J^6\).
Otherwise roots on the zero locus can contribute to \(K\) already in
\(J^4\).  Thus its strict remaining dichotomy is
\[
\boxed{\ q^{-1}(0)\ne\{0\}\quad\text{or}\quad
        (K=1+J^6,\ P:A_2\overset{\sim}{\to}J^6).\ } \tag{5}
\]

## The length-eight profile

For \((2,2,2,2,1,1,1,1)\), the dimension-eleven quotient \(J/J^8\)
has abelian closed raw cubes, so all cube commutators lie in the
one-dimensional \(J^8\).  The pure degree-eight tensor makes
\([J^4,J^4]=0\), excluding \(Q=0\).  Hence
\[
\dim Q=1\quad\text{or}\quad\dim Q=2,
\qquad 1+J^8\subseteq K.
\]
The \(\dim Q=1\) branch can still carry a rank-one conjugation correction
\(K\to J^8\).  In the \(\dim Q=2\) branch the leading cube map is
bijective and \(K\subseteq1+J^6\), but \(K\) may have dimensions one,
two, or three.

The fibre argument stops precisely here.  When one applies
\(vD-Dv\) to \(D=(v+z)^3-v^3\), the contributions containing two
copies of \(z\) land in \(J^8\), rather than vanishing as they did in
the length-seven quotient.  Likewise, the pure degree-seven tensor
pushes the change in the cube of a \(J^2\)-root only into \(J^8\);
an uncontrolled \(A_8\) correction prevents a well-defined map
\(A_2\to J^6\).  These are genuine missing identities, not solver
timeouts.

## Machine-readable ledger

```text
DIM12_CLOSURE_TRIAGE|frontier_inputs=8|proved_excluded=3|human_excluded=2|finite_audit_excluded=1|branch_contracts=5|existence_certificates=0|status=necessary_conditions_only
```

Reproduce the bookkeeping with

```bash
python3 triage_dim12_closure_profiles.py
python3 -m unittest test_triage_dim12_closure_profiles.py
python3 audit_dim12_2322111_graded_frontend.py
python3 -m unittest test_audit_dim12_2322111_graded_frontend.py
```
