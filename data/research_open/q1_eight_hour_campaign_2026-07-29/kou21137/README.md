# KOU-21.137 research package

Status: complete research pass, 2026-07-29.

## Main result

For an arbitrary group \(A\), put \(P=\{a^2:a\in A\}\) and
\(W=A\wr C_2\).  The square values of \(W\) form a subgroup exactly when:

1. \(P\leq A\); and
2. \(x^A=xP\) for every \(x\notin P\).

In that case
\[
  \operatorname{Sq}(W)=A\times_{A/P}A.
\]
When \(P<A\), one further has \(P=A'\); for finite 2-groups,
\[
  \operatorname{Sq}(W)=W'=\Phi(W).
\]
The criterion, fiber-product formula, \(P=A'\), and
\(\operatorname{Sq}(W)=W'\) do not require \(A\) to be finite.  With top group
\(C_2\), the restricted and unrestricted wreath products coincide.

For every prime \(p\), this extends without centrality or finiteness
assumptions.  If \(Q=P_p(A)\), then \(P_p(A\wr C_p)\) is a subgroup exactly
when either \(Q=A\), or \(Q=A'\) and \(x^A=xA'\) for every
\(x\notin A'\).  In the latter case it is the \(p\)-fold fiber product over
\(A/A'\).

For finite \(A\), the corresponding all-prime classification has at most
five branches: \(p\nmid|A|\); elementary abelian \(p\)-groups;
semi-extraspecial \(p\)-groups whose \(p\)-power map is onto \(A'\);
Frobenius groups \(K\rtimes C_p\); and, only at \(p=2\), Frobenius groups
\(K\rtimes Q_8\).

For finite seeds this gives a complete five-class theorem.  The valid seeds
are exactly: odd-order groups; elementary abelian 2-groups; nonabelian
semi-extraspecial 2-groups; generalized dihedral groups over a finite
odd-order abelian kernel; and Frobenius groups \(K\rtimes Q_8\) with a
fixed-point-free quaternion action on a finite odd-order abelian \(K\).

For finite nonabelian 2-group seeds the criterion has a complete structural
form:
\[
  \operatorname{Sq}(A\wr C_2)\text{ is a subgroup}
  \quad\Longleftrightarrow\quad
  A\text{ is semi-extraspecial}.
\]
The key bridge is that the square map of a semi-extraspecial 2-group is a
perfect nonlinear/vectorial Boolean bent function.  Established
Nyberg and Kölsch--Polujan results then give the dimension restriction,
surjectivity, and the explicit square-fiber bound; the draft also retains a
self-contained Pfaffian/Fourier derivation.  Applying this bridge to the
wreath criterion produces exponent-eight KOU counterexamples from every
semi-extraspecial 2-group.  Extraspecial groups and
\(\operatorname{UT}_3(\mathbb F_{2^m})\) are subfamilies.

The direct odd-prime analogue
\(\operatorname{UT}_3(\mathbb F_3)\wr C_3\) was also settled
computationally as a no-go: its 219 cube values generate a nonabelian group of
order 243 but are not closed.  No quotient of this particular wreath product
can retain nonabelian generated cubes.  This now follows from a general
all-quotients theorem: if \(A\) is any nonabelian exponent-\(p\)
semi-extraspecial group, \(p\) is odd, and \(W=A\wr C_p\), then every
normal quotient \(W/N\) whose \(p\)-th-power values form a subgroup must
contain \(\Delta A'\) in \(N\); consequently that subgroup is abelian.  A
full enumeration of all 101 normal quotients in the smallest \(p=3\) case
confirms the theorem exactly.  A further exact conjugacy-class
moment theorem, valid for every odd prime \(p\), rules out the broader
proposed repair
\((A\wr C_p)/\Delta P_p(A)\) whenever
\(P_p(A)\le Z(A)\cap A'\) and \(P_p(A)<A'\): the unquotiented \(p\)-th
powers cannot be closed, and the diagonal quotient preserves the closure
defect.

More generally, when \(P_p(A)\) is a central subgroup, closure in
\(A\wr C_p\) has an exact Camina criterion: apart from the degenerate
surjective-power case, it holds precisely when \(P_p(A)=A'\) and
\(x^A=xA'\) off \(A'\).  For the positive exponent-\(p^2\) Camina seeds,
every quotient that lowers the wreath exponent from \(p^3\) to at most
\(p^2\) necessarily makes the \(p\)-th-power subgroup abelian.

The odd-prime target requires non-powerfulness, not merely
noncommutativity.  In fact every closed \(p\)-power set produced by the
finite \(p\)-group cyclic-wreath classification is powerful; in the
nonabelian branch its derived and \(p\)-power subgroups are both
\(\Delta A'\).  This firewall is proved in
`ODD_PRIME_WREATH_POWERFULNESS_NO_GO.md`.

At \(p=3\), a directed search around the class-six two-string subgroup of
\(\operatorname{UT}_7(\mathbb F_3)\) found no Wilson counterexample.
The group itself has 649 raw cubes generating a non-powerful subgroup of
order \(3^{10}\), but the raw set is not closed.  Its centre is exactly the
order-three derived subgroup of the cube-generated group; all 640
nontrivial normal quotients therefore kill the obstruction.  Exact audits
of the four maximal subgroups also show that their cube-generated groups
are abelian, excluding every section of this candidate.  The parallel
algebra-group analysis excludes every ideal quotient of the associated
15-dimensional two-string algebra.  Under the standing \(J^9=0\)
hypothesis, human filtration and cube-power lemmas first eliminate
dimensions through ten.  At dimension eleven, a sharp algebra has
noncommuting cubes but its raw cube set is not closed; a closure-fibre lemma
and a quadratic short-chain argument exclude every one of the 246 profiles.
Thus a closed nonabelian raw cube set in this algebra-group model requires
algebra dimension at least twelve.  The former solver models remain
independent regression checks rather than proof premises.

These are search barriers, not a solution of the odd-prime question.

A separate complete finite-group scan covers all \(1{,}396{,}077\)
SglPPow isomorphism types of order \(3^8\).  Of these, 221 have nonabelian
cube-generated subgroup and 63 have non-powerful cube-generated subgroup,
but none of the 63 has a closed raw cube set.  Together with the smaller
catalogues, this gives the computer-assisted \(p=3\) lower bound
\(|G|\ge3^9\) for any finite-group counterexample.  It is not a statement
about other odd primes.

The explicit \(D_8\wr C_2\) example is not claimed as new: it already appears
in a public Lean gist created on 2026-04-14.

## Certified minimum-order classification

Every one of the 2669 SmallGroups isomorphism types at 2-power orders through
128 was audited from its raw Cayley table, with full associativity checks and
an independent GAP predicate cross-check.

- no qualifying group has order below 128;
- exactly ten qualifying order-128 groups exist:
  `SmallGroup(128,928)` through `SmallGroup(128,937)`.

They are precisely the order-128 groups with center of order two and common
central quotient \(Q\cong\operatorname{SmallGroup}(64,138)\), where \(Q\) is
defined by an explicit catalogue-independent presentation in
`THEOREM_DRAFT.md`.  They are the ten stem central double extensions of this
quotient whose central kernel is the full center: six have square subgroup
\(C_2\times D_8\), four have square subgroup \(C_2\times Q_8\), and only the
two endpoints are ordinary wreath products.

Canonical certificate SHA-256:

```text
bb1f54891c06bb0110066208269fba5b037bf045f612a5249db1bc47df68bdfa
```

## Files

- `THEOREM_DRAFT.md`: theorem, proof, families, ten-group classification, and
  publication assessment;
- `FINITE_SEED_CLASSIFICATION.md`: complete five-class theorem for all finite
  seeds, including the quaternion-complement square calculation;
- `CENTRAL_POWER_WREATH_CRITERION.md`: exact central \(p\)-power closure
  criterion and the all-quotients exponent-lowering no-go theorem;
- `GENERAL_PRIME_WREATH_CRITERION.md`: unrestricted exact closure criterion
  for \(p\)-th powers in \(A\wr C_p\);
- `GENERAL_PRIME_FINITE_SEEDS.md`: complete finite-seed classification for
  every prime;
- `GENERAL_PRIME_FINITE_CLASSIFICATION.md`: manuscript-level five-branch
  iff theorem, full proof, two odd-prime infinite families, and the square
  classification as a corollary;
- `STRUCTURAL_POSITION_OF_POWER_SUBGROUP.md`: exact location of the closed
  power subgroup inside the derived and Frattini subgroups;
- `ODD_KOU_NILPOTENCY_BARRIER.md`: Hall-collection proof that exponent
  \(p^2\), class-at-most-\(p\) groups have commuting raw \(p\)-th powers,
  plus the class-\(2p\) unitriangular witness;
- `METABELIAN_2P_NILPOTENCY_BARRIER.md`: group-ring proof that the
  class-\(2p\) barrier is exact for metabelian exponent-\(p^2\) groups;
- `SHARP_2P_BARRIER_STATUS.md`: fail-closed status of the corresponding
  unrestricted conjecture, including the full order-\(2187\) \(p=3\)
  audit and the Khukhro/Hughes distinction;
- `HUGHES_CLASS_2P_MINUS1_POWER_AUDIT.md`: exclusion lemma showing that the
  explicit Havas--Vaughan-Lee \(p=5\), class-nine anti-Hughes family still
  has commuting fifth powers;
- `ODD_PRIME_WREATH_POWERFULNESS_NO_GO.md`: proof that every closed
  odd-prime power set arising from the finite \(p\)-group cyclic-wreath
  classification is powerful, together with the exact Wilson target
  \(H'\nleq H^p\);
- `UT7_TWO_STRING_SUBQUOTIENT_NO_GO.md`: exact \(p=3\) audit excluding
  every section of the class-six two-string unitriangular candidate;
- `ALGEBRA_GROUP_P3_BARRIERS.md`: human dimension-twelve closure-aware
  lower bound in the \(J^9=0\) algebra-group model and a theorem excluding
  every ideal quotient of the 15-dimensional two-string algebra;
- `DIM8_FILTERED_GRADED_CERTIFICATE.md`: independent completeness and trust
  audit for the exceptional dimension-eight profile, including the
  canonical SMT-LIB hash and its human replacement;
- `DIM9_HUMAN_CUBE_COMMUTATIVITY.md`: hand lemmas replacing all four
  dimension-nine UNSAT exclusions and the old dimension-eight solver
  premise;
- `DIM9_ALGEBRA_PROFILE_STATUS.md`: all 29 dimension-nine filtration
  profiles and their human exclusions, with historical exact solver
  certificates;
- `DIM10_ALGEBRA_PROFILE_STATUS.md`: the correctly scoped 92
  dimension-ten profiles and their complete human exclusion, with the
  historical bounded solver checkpoint retained only for provenance;
- `DIM11_SHARP_NONCOMMUTING_CUBE_WITNESS.md`: associative
  dimension-eleven witness showing that the noncommuting-cube bound is
  sharp, together with the explicit failure of raw-cube closure;
- `DIM11_CLOSURE_AWARE_STATUS.md`: exact 246-profile dimension-eleven
  ledger, a human closure obstruction excluding the sharp length-six
  profile, and the pure-tail/quadratic short-chain proof excluding the
  final length-seven profile;
- `DIM12_NEXT_FRONTIER.md`: exact reduction of all 582 dimension-twelve
  profiles to eight necessary next-stage branch inputs;
- `DIM12_CLOSURE_TRIAGE.md`: closure exclusion of three dimension-twelve
  inputs and strict necessary contracts for the other five, with no
  realizability claim;
- `ORDER6561_COMPLETE_WILSON_AUDIT.md`: complete order-\(3^8\) catalogue
  theorem, three-shard provenance, and independent audit of all 63
  non-powerful hard candidates;
- `EXPONENT_P_WREATH_ALL_QUOTIENTS_NO_GO.md`: theorem that every quotient
  of an exponent-\(p\) semi-extraspecial wreath seed which repairs
  \(p\)-power closure necessarily makes the power subgroup abelian;
- `LITERATURE_AUDIT.md`: prior-art and provisional novelty audit;
- `PROOF_AUDIT.md`: independent theorem-by-theorem audit and correction log;
- `COMPUTATIONAL_AUDIT.md`: independent routes and fail-closed recovery log;
- `verify_smallgroups_classification.py`: table-only primary verifier;
- `enumerate_smallgroups_tables.g`: predicate-free Cayley-table exporter;
- `gap_predicate_crosscheck.g`: native GAP semantic cross-check;
- `validate_wreath_criterion_smallgroups.g`: bounded independent regression
  over all 144 SmallGroups types of orders 1 through 32;
- `validate_wreath_families.g`: assertion-based finite family checks;
- `validate_semiextraspecial_square_surjectivity.g`: independent
  definition/Camina cross-check and square-fiber scan over all SmallGroups
  types of orders 8 through 128;
- `validate_odd_wreath_p3.g`: exact odd-prime no-go and closure witness;
- `validate_sharp_2p_matrix_boundary.g`: explicit \(p=3,5\)
  class-\((2p-1)\)/class-\(2p\) unitriangular boundary regression;
- `test_metabelian_2p_coefficient_audit.py`: arithmetic audit of the unique
  one-\(p\) coefficient and the three norm-product term classes in the
  metabelian proof;
- `validate_odd_kou_p3_order2187.g`: optional exhaustive order-\(2187\)
  endpoint audit requiring the complete SmallGrp data files;
- `ODD_DIAGONAL_QUOTIENT_NO_GO.md`: exact \(p\)-th-power formula for
  \(A\wr C_p\), general odd-prime moment obstruction, and diagonal-quotient
  invariance theorem;
- `validate_odd_diagonal_quotient_no_go.g`: fail-closed seed scan through
  order 729 using the exact moment formulas;
- `validate_finite_seed_classification.g`: exhaustive five-class comparison
  over all 3,596 SmallGroups types of orders 1 through 128;
- `validate_general_prime_wreath_criterion.g`: direct wreath enumeration at
  \(p=3,5\) across bounded SmallGroups ranges;
- `validate_general_prime_finite_seeds.g`: structural/criterion comparison
  for all 3,596 SmallGroups types through order 128 at \(p=2,3,5\);
- `validate_order128_structure.g`: explicit common quotient, central-lift
  classification, and order-64 boundary audit;
- `validate_order128_parameter_orbits.g`: exhaustive normalized-generator
  proof of the \(6+4\) parameter-orbit split;
- `test_verify_smallgroups_classification.py`: verifier regression tests;
- `test_semiextraspecial_square_surjectivity.py`: executable GAP-scan
  regression test;
- `test_odd_diagonal_quotient_no_go.py`: executable \(p=3\) moment-scan
  regression test for the general odd-prime theorem;
- `test_odd_power_value_formula.py`: independent exact \(p=5\) check of all
  top cosets in the \(A\wr C_p\) power-value formula, using \(A=D_{10}\);
- `test_finite_seed_classification.py`: executable all-finite-seed
  classification regression through order 128;
- `test_central_power_quotient_no_go.py`: \(p=3\) positive-boundary
  regression for the all-quotients exponent-lowering obstruction;
- `test_general_prime_wreath_criterion.py`: direct \(p=3,5\) regression for
  the unrestricted prime-wreath theorem;
- `test_general_prime_finite_seeds.py`: executable \(p=2,3,5\) all-finite
  classification regression through order 128;
- `test_general_prime_nonabelian_kernel.py`: exact order-1029 regression for
  the \(p=3\) Frobenius branch with nonabelian kernel
  \(\operatorname{UT}_3(\mathbb F_7)\);
- `validate_structural_position_p3.g` and
  `test_structural_position_p3.py`: exact \(p=3\) order/index checks for an
  elementary abelian seed and the extraspecial exponent-nine seed;
- `validate_odd_kou_nilpotency_barrier.g` and
  `test_odd_kou_nilpotency_barrier.py`: all exponent-nine SmallGroups
  through order 729 by class, plus the exact
  \(\operatorname{UT}_7(\mathbb F_3)\) noncommuting-cubes witness;
- `validate_ut7_two_string_no_go.g` and
  `test_ut7_two_string_no_go.py`: exact centre, all-normal-subgroup, and
  four-maximal-subgroup audit proving the complete section no-go;
- `two_string_algebra_cube_search.cpp` and
  `test_two_string_algebra_cube_search.py`: exhaustive \(3^{15}\)-element
  cube-image calculation for the two-string algebra;
- `search_dim8_algebra_profiles.py` and
  `test_dim8_algebra_profiles.py`: exact seven-profile reduction and
  34-variable associativity audit excluding noncommuting cube layers in
  dimension eight;
- `search_dim9_algebra_profiles.py` and
  `test_dim9_algebra_profiles.py`: historical closure-aware QF_BV
  regression for the last length-six dimension-nine profile, with a
  canonical SMT-LIB hash;
- `cegis_dim9_profile_2111121.py`,
  `cegis_dim9_profile_2111211.py`, and
  `test_cegis_dim9_profile_2111121.py`: full filtered CEGIS machinery and
  iteration-zero layer-rank exclusions of nominal length-seven profiles;
- `cegis_dim9_profile_21111111.py`,
  `cegis_dim9_profile_2211111.py`,
  `cegis_dim9_profile_3111111.py`, and
  `test_cegis_dim9_remaining_profiles.py`: complete filtered
  noncommuting-cube regression certificates for three profiles now
  excluded by hand;
- `humanize_dim9_iteration_zero.py`: named-core localization, grouped
  ablation, and deletion-minimal-core audit for
  \((3,1,1,1,1,1,1)\);
- `humanize_dim9_profile_222111.py` and
  `test_humanize_dim9_profile_222111.py`: grouped deletion proving that
  the last length-six contradiction uses only leading graded
  associativity and the noncommuting-cubes witness;
- `search_dim10_algebra_profiles.py`,
  `test_dim10_algebra_profiles.py`, and
  `cegis_dim10_profile_222211.py`: reproducible dimension-ten reduction
  to zero survivors and the historical 240-second checkpoint;
- `verify_dim11_sharp_noncommuting_cubes.py` and
  `test_verify_dim11_sharp_noncommuting_cubes.py`: exact associativity,
  filtration, 171-cube image, noncommutation, and nonclosure audit for
  the sharp dimension-eleven witness;
- `search_dim11_algebra_profiles.py` and
  `test_dim11_algebra_profiles.py`: exact human and closure-aware
  profile-level reduction from 246 profiles to one length-seven case,
  subsequently excluded by the branch proofs;
- `audit_quadratic_relation_d3_bound.py` and its test: exhaustive
  130-plane certificate for \(d_1=d_2=2\Rightarrow d_3\le2\);
- `audit_dim11_q2_graded_frontend.py` and its test: exact reduction of
  the \(\dim Q=2\) branch to 12 nine-point-image graded cases;
- `audit_dim11_q1_quadratic_commutativity.py` and its test: independent
  130-plane check that every one-dimensional leading case has
  commutative quadratic quotient;
- `audit_dim11_q2_short_chain_obstruction.py` and its test: exact check
  of the short-chain contradiction in all 12 surviving graded cases;
- `DIM12_NEXT_FRONTIER.md` and `search_dim12_next_frontier.py`: exact
  human-filter reduction of the 582 dimension-twelve profiles to eight
  necessary closure-branch inputs;
- `DIM12_CLOSURE_TRIAGE.md` and its ledger test: closure-aware exclusion
  of three of those inputs and precise contracts for the remaining five;
- `audit_dim12_2322111_graded_frontend.py` and its test: exact
  \((2,3,2,2,1,1,1)\) reduction from 36 degree-four cases through 144
  degree-five extensions to 48 necessary graded cases, with canonical
  SHA-256 certificate;
- `analyze_dim11_closure_branches.py` and its test: finite leading-map,
  kernel-dimension, and group-order audit for the \(\dim Q=1,2\)
  branches;
- `probe_dim11_q2_graded_2222111.py` and its test: explicitly incomplete
  graded SAT probe showing that leading associativity, cube-leading
  bijectivity, and the closure derivative identity remain compatible;
- `validate_order6561_wilson_scan.g` and
  `validate_order6561_nonpowerful_candidates.g`: production catalogue
  scan and direct \(H'\nleq H^3\) audit for the 63 hard candidates;
- `validate_exponent_p_all_quotients_p3.g` and
  `test_exponent_p_all_quotients_p3.py`: exhaustive check of all 101 normal
  quotients of \(\operatorname{UT}_3(\mathbb F_3)\wr C_3\);
- `artifacts/classification_certificate.json`: canonical classification
  certificate;
- `artifacts/all_cayley_tables.txt.gz`: complete deterministic raw stream;
- `artifacts/gap_predicate_crosscheck.txt`: independent GAP transcript.

## Reproduce

From the repository root:

```bash
python3 -m unittest -v \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/test_verify_smallgroups_classification.py

python3 -m unittest -v \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/test_semiextraspecial_square_surjectivity.py

python3 -m unittest -v \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/test_odd_diagonal_quotient_no_go.py

python3 -m unittest -v \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/test_odd_power_value_formula.py

python3 -m unittest -v \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/test_finite_seed_classification.py

python3 -m unittest -v \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/test_central_power_quotient_no_go.py

python3 -m unittest -v \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/test_general_prime_wreath_criterion.py

python3 -m unittest -v \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/test_general_prime_finite_seeds.py

python3 -m unittest -v \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/test_general_prime_nonabelian_kernel.py

python3 -m unittest -v \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/test_structural_position_p3.py

python3 -m unittest -v \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/test_odd_kou_nilpotency_barrier.py

python3 -m unittest -v \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/test_exponent_p_all_quotients_p3.py

python3 \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/verify_smallgroups_classification.py

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_wreath_criterion_smallgroups.g

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_wreath_families.g

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_semiextraspecial_square_surjectivity.g

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_odd_wreath_p3.g

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_odd_diagonal_quotient_no_go.g

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_finite_seed_classification.g

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_general_prime_wreath_criterion.g

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_general_prime_finite_seeds.g

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_order128_structure.g

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_order128_parameter_orbits.g
```

The last successful run used GAP 4.12.1, SmallGroups 1.5.3, and NumPy 2.3.5.
