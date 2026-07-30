# Eight-hour campaign: publication-readiness audit

Date: 2026-07-30

## Executive verdict

The campaign has produced one strong specialist-paper package, one promising
combinatorics-paper core, and one rigorous obstruction programme.  It has
**not** yet produced a result that can responsibly be certified as a Chinese
Academy of Sciences Zone-1 paper.  Journal-zone labels vary by edition and
institution; more importantly, mathematical quality cannot be inferred from
the amount of computation.

The present ranking is:

1. **KOU-21.137 / cyclic wreath powers:** closest to a complete manuscript.
2. **OPG-1757 / forest Rayleigh positivity:** strongest conceptual upside,
   but the arbitrary-\(q,k\) injection is incomplete.
3. **Erdős #1083 / three-dimensional distinct distances:** no exponent
   improvement; the negative results are useful research infrastructure, not
   a Zone-1 theorem.

## 1. KOU-21.137

### Closed mathematical results

- For every group \(A\) and prime \(p\), an exact if-and-only-if criterion
  characterizes when the raw \(p\)-th powers of \(A\wr C_p\) form a subgroup.
  In the proper case the seed satisfies
  \(P_p(A)=A'\) and is Camina off \(A'\); the power subgroup is the
  \(p\)-fold fibre product over \(A/A'\).
- For finite seeds this gives an at-most-five-branch structural
  classification.  For finite 2-group seeds, the nonabelian seeds are exactly
  the semi-extraspecial groups.
- In the square case the resulting subgroup is \(W'\), and for finite
  2-groups also \(\Phi(W)\).
- The minimum order of a 2-primary KOU counterexample is 128.  Exactly ten
  SmallGroups types qualify, `SmallGroup(128,928..937)`, and they admit a
  common-quotient central-lift classification.
- At \(p=3\), every one of the 1,396,077 groups of order \(3^8\) has been
  covered by a fail-closed catalogue scan; none is a Wilson counterexample.
- Under the stronger \(J^9=0\) algebra-group hypothesis, all 92 admissible
  dimension-ten profiles are excluded by human lemmas.  A dimension-eleven
  algebra with noncommuting cubes shows this commutativity bound is sharp,
  but its cube set is explicitly not closed.
- A new normal-word lemma proves
  \(d_1=d_2=2\Rightarrow d_3\le2\), independently reproduced by an exhaustive
  audit of all 130 quadratic relation planes.  A closure-fibre lemma then
  excludes the surviving length-six profile.  For the last profile
  \((2,2,2,2,1,1,1)\), the one-dimensional leading branch is forced
  abelian by the pure sevenfold tail.  The two-dimensional branch reduces
  to 12 bijective quadratic relation planes; three have the wrong
  fourth-layer dimension and the remaining nine force graded
  commutativity.  The resulting split-quadratic short chain contains a
  nonzero \(w\in A_2\) with \(w^3=0\), contradicting the closure-forced
  bijection \(A_2\to J^6\).  Hence no dimension-eleven profile survives in
  the \(J^9=0\) algebra-group model.
- At dimension twelve, the same proved necessary filters reduce all 582
  in-scope profiles to eight explicit branch inputs.  The generalized
  length-six fibre lemma, a finite-normal-form-assisted filtered
  cross-relation argument, and the exact quadratic \(d_4\)-bound exclude
  three of them.  Closure gives strict
  contracts for the other five.  One remaining profile is reduced to 48
  necessary graded cases, whose strict homogeneous quotients all have
  commuting cubes; the unresolved objects are filtered lifts.  This does
  not exclude dimension twelve or construct an algebra.

### Independent evidence

- The order-128 classification has catalogue-table, native GAP and
  presentation/orbit checks.
- The order-\(3^8\) scan has a complete index ledger and a second pass over
  every hard candidate.
- The algebra boundary has two independent profile enumerators and a direct
  \(3^{11}\)-element verifier of the sharp witness.
- Solver timeouts and computational observations have been retained as
  provenance, never promoted to proof premises.

### Novelty risk

The public \(D_8\wr C_2\)
[Lean example](https://gist.github.com/eliasjudin/3e74b54004d82cb86651a14ecf082463)
predates this work, so it cannot be claimed as a discovery.
[Kundu--Mondal](https://arxiv.org/abs/2010.04954) already compute powers in
general wreath products; the contribution must be framed as the
subgroup-closure criterion, Camina/semi-extraspecial classification, and
minimum-order theorem.
[Kappe--Ying (1992)](https://www.numdam.org/item/RSMUP_1992__87__245_0/)
already prove that the odd-prime example \(C_p\wr C_p\) is power closed.
That individual wreath family is prior art; the candidate contribution is
the arbitrary-seed if-and-only-if theorem and its classification.
[Chuah (2021)](https://www.maths.tcd.ie/pub/ims/bull88/wef/Classroom/Chuah/Chuah-wef.pdf)
is direct prior work on when the square-value set of a single group is a
subgroup.  It supplies mandatory background and earlier minimal
**nonclosure** results, but its inspected statements do not cover wreath
products, the closed-but-nonabelian KOU question, or the order-128
classification.

Two sources remain hard pre-submission blockers:

1. Mann (2005), especially Theorem 16 and its definition of power closure;
2. Bennett's 2012 thesis, whose stated subject is exactly when sets of powers
   form subgroups.

Their full texts must be obtained through authorized access and audited
line-by-line.  MathSciNet/zbMATH citation chaining and a finite-\(p\)-group
specialist check are also necessary.

### Publication judgement

After priority clearance and manuscript compression, the wreath criterion,
finite-seed theorem, and order-128 classification form a credible specialist
group-theory paper.  The current package is too broad: the odd-prime Wilson
search, algebra dimensions, and every negative experiment should not all be
forced into the main article.

The complete dimension-eleven algebra exclusion supplies the additional
conceptual theorem that was missing at the start of the campaign.  It
materially strengthens a Zone-1 attempt, but it does not remove the priority
and specialist-review gates.  A still stronger version would:

- settle the odd-prime part of KOU-21.137; or
- construct and classify the first odd-prime counterexamples; or
- elevate the general-prime criterion into a stronger theorem on arbitrary
  word-value subgroups/iterated wreath products.

Even with the new lower bound, Zone-1 placement cannot be predicted or
promised before the two blocked sources and the theorem package have been
reviewed by specialists.

## 2. OPG-1757

### Closed mathematical results

- Exact fixed-page transfer formulas and certificates through seven pages.
- Uniform coefficient positivity for the complete \(B_4,\ldots,B_7\)
  families.
- For arbitrary page number \(k\), exact degree/end coefficients and the
  first five \(\beta\)-coefficient layers.
- A rooted-tree/Lagrange single-convolution formula for the first nonzero
  coefficient of the critical Rayleigh difference.
- A general support theorem in the natural base-4 Newton basis and exact
  nonnegativity through \(k=30\).
- A general local-replacement theorem for edge-disjoint external contexts:
  universal outside-stability is equivalent to refinement of the
  boundary-connectivity partition; requiring a universally stable local
  inverse forces equality of the partitions.
- A genuinely outside-stable \(K_4\) local repair lemma: its inverse remains
  valid in the presence of arbitrary external forest components.
- A complete finite injection for the first five-vertex layer
  \(q=1,k=5\): all 2,140 negative objects map to distinct members of the
  2,240-object positive side, changing at most two coloured edge copies.
- A structural certificate for that layer uses three transition classes and
  350 reversible shortest alternating chains, of maximum length eight; its
  four image classes have sizes \(1590,295,203,52\).

### Remaining proof gap

The Newton nonnegativity is still computational for general \(k\).  The
five-vertex bridge and three transition classes now cross all the local
normal forms, so the former 150 isolated objects are closed.  A certified
two-cycle rules out a strictly decreasing source-only potential for the
current deterministic step-by-step routing, but not other routings or a
direct Hall proof.  For \(q=2\), an active--active fourth transition is
needed at \(k=3\) within the present nested rule family; it closes the full
layer only through \(k=5\), leaving deficits 4 and 32 at \(k=6,7\).
The \(24\to25\) handoff closes \(k=6\), while one complementary
\(02\to45\) signature closes \(k=7\) and is minimal in additional-orbit
count relative to the four-rule graph.  Their union closes the finite
\(q=2,k\le7\) ledger.  The latter rule is neither uniquely reversible nor
outside-stable; a \(q=3\) extension gives an explicit cycle-creation
counterexample.  The outside-stability characterization proves that this is
not repairable by testing more external sizes while keeping the same
component-merging context-free rule.  The remaining contract is:

\[
\text{finite complete rule grammar or uniform Hall theorem}
\to\text{termination/recovery invariant}
\to\text{repair-class image separation}
\to\text{all-\(k\) first coefficient}
\to\text{all higher coefficients}
\to\text{full OPG theorem}.
\]

The current literature still treats broad forest negative correlation as
open.  Recent work proves important neighbouring cases:
[Huang](https://arxiv.org/abs/2311.00965) studies arboreal-gas negative
correlation on selected graphs;
[Tang--Zhang](https://arxiv.org/abs/2603.10738) prove fixed-component/excess
results on sufficiently large complete graphs; and
[Fang--Ma](https://arxiv.org/abs/2604.27755) cover series-parallel cycle
matroids, uniform matroids and bounded-size cases through their Gårding
framework.  None of those statements, as presently audited, closes the
complete-split two-orbit theorem developed here.

### Publication judgement

The existing formulas and local repair are a strong paper embryo, not yet a
submission-level main theorem.  Completing the all-\(k\) first-coefficient
injection could support a focused algebraic-combinatorics paper after a
priority search.  A realistic Zone-1 target should close at least the entire
\(\alpha^2\) layer, or preferably all edge-pair orbits through a new
Rayleigh/Gårding-preserving operation.

## 3. Erdős #1083

### Closed mathematical results

The campaign has translated the remaining geometric branch into several
exact additive-energy and SAT/Latin interfaces, and has proved useful
no-go theorems:

- the full resonant Laurent-lattice/multistar ansatz achieves at most
  \[
  \exp\!\left((\log2+o(1))
  \frac{\log n}{\log\log n}\right)=n^{o(1)}
  \]
  average-degree gain;
- fixed number fields contribute only ideal-divisor and unit-lattice growth;
- fixed-rank GAPs, rational/Laurent parametrizations, disjoint unions,
  tensors and commensurable multi-layer constructions do not give the needed
  power law;
- for varying fields the exact unit-lattice packing bound is
  \[
  |T_n|\le
  \left(1+\frac{2C_n\log n}{\lambda_n}\right)^{r_n}.
  \]
  A \(2/5\)-scale rank requirement follows only when the container and
  shortest-unit constants are sublogarithmically uniform; without that
  hypothesis there is no unconditional numerical rank threshold;
- for the explicit family
  \(f_d(x)=\prod_{k=1}^d(x+k)-1\), an exact determinant identity
  \[
  |\Delta_d|=4\cdot3069^{d-2}\prod_{m=1}^{d-3}m!
  \]
  proves coefficient-box inflation
  \(\exp(\Theta(d^2\log d))\), while providing only \(d-1=n^{o(1)}\)
  parameters.  The polynomial identity is valid for every \(d\ge4\), but
  the degree-\(d\) number-field interpretation needs irreducibility and a
  suitable real root; those hypotheses are currently verified only for
  \(5\le d\le30\).  This is a family-specific, asymptotically conditional
  obstruction, not an exponent gain.

### Publication judgement

The recognized \(n^{3/5-o(1)}\) lower-bound exponent has not been improved.
The obstruction package is valuable for deciding what not to search and may
become a technical section if a positive construction or inverse theorem is
found.  In its current form it is not a Zone-1 result and should not be
marketed as progress on the numerical exponent.

## Recommended paper split

### Manuscript A: prepare first

**Working title:** *Power-value subgroups in cyclic wreath products and a
Kourovka problem*

Main body:

1. unrestricted prime-wreath closure criterion;
2. finite five-branch classification;
3. semi-extraspecial square specialization;
4. derived/Frattini structure;
5. minimum order 128 and ten central lifts.

Supplement:

- complete GAP/table certificates and hashes.
- the independent algebra-profile ledgers and exact finite quadratic audits,
  if the \(J^9=0\) dimension-12 lower bound is included in the manuscript.

Exclude from the first version:

- exploratory odd-prime Wilson dead ends;
- SMT history;
- failed algebra searches and solver telemetry; retain only the
  \(J^9=0\) dimension-12 lower bound, explicitly labelled as using a small
  exact finite quadratic row-reduction certificate, if it fits the final
  narrative.

### Manuscript B: continue before drafting

**Working title:** *Coefficientwise Rayleigh inequalities for forests of
complete split graphs*

Do not draft the final paper until a complete rule grammar, phase-aware
alternating-chain termination, tag recovery, and global image separation are
closed for arbitrary \(q,k\).  Preserve the present EGF/Lagrange formulas,
the three-transition \(q=1\) certificate, the two finite \(q=2\)
completion signatures, and their \(q=3\) outside-stability counterexample
as the proof engine and falsification test.

### Erdős line

Keep as a research programme.  Continue only on the quantified
varying-field/noncommensurable escape route or a genuine inverse theorem,
with explicit height and regulator control; do not spend further time on
fixed-field divisor constructions already covered by the no-go theorems.

## Go/no-go gates

| Gate | KOU | OPG | Erdős |
|---|---|---|---|
| Precise unconditional theorem | yes | partial | no exponent theorem |
| Human proof closed | yes for main wreath results | no for global injection | yes for obstructions only |
| Independent verification | strong | strong on closed subclaims | strong on tested models |
| Priority cleared | **no** | provisional | not applicable yet |
| Standalone manuscript now | likely after scope reduction | no | no |
| Zone-1 claim now | **no** | **no** | **no** |

The strongest honest outcome of this campaign is therefore not “a Zone-1
paper has been obtained,” but:

> A likely publishable KOU manuscript plus a new \(J^9=0\) dimension-12
> lower bound and a three-of-eight next-frontier exclusion has been
> isolated; an OPG route with
> high conceptual upside has been reduced to a precise uniform
> phase-aware alternating-chain problem; and the Erdős search has been confined to a
> quantified varying-field escape regime.
