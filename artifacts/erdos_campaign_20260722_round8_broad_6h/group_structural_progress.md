# Structural/Diophantine/computational workflow: round-8 report

Date: 2026-07-22 (Asia/Hong_Kong)

Problems: #332, #635, #686, #952, #963.

Unified accounting: 2026-07-22 08:52:14--10:22:14, 5,400 seconds.

Strict overall verdict: **NO ORIGINAL CLOSURE / NO Q2 STOPPING RESULT**.
This workflow produced several rigorous structural increments and two exact
route counterexamples, but none currently supports a stand-alone SCI-Q2 main
claim after comparison with the known boundary.

## #332 — the broadening must still encode recurrence

The positive-upper-Banach-density argument is correct, but standard and
already subsumed by Stewart--Tijdeman.  A different broadening was killed
exactly: the positive squares form an additive basis of order at most four,
yet each nonzero difference has only finitely many representations, so their
infinite-difference spectrum is just `{0}`.  Additive-basis strength and
coarse counting growth therefore cannot replace recurrence.  The next route
must formulate a genuinely weaker recurrence/correlation condition and
separate it from positive upper Banach density.

Classification: `ROUTE_AUTOPSY / NO NEW THEOREM AT PUBLICATION SCALE`.

## #635 — all odd-neighbour collisions reduce to poset chains

For an even non-power `x=2^a u`, define

\[
 x\preceq y\iff a(x)\le a(y)\ \hbox{and}\ u(x)\ge u(y).
\]

The round-7 all-divisor inversion lemma implies a clean new reformulation:
for every independent even set `S` and every odd conflict vertex `b`, its
neighbour set inside `S` is a chain.  Hence incomparable vertices have
disjoint odd neighbourhoods, and every antichain has an explicit matching
via `x -> (2^a-1)u`.  The exact remaining case is arithmetic expansion along
long chains.  This is stronger organization of the obstruction, not Hall's
condition and not the conjectural exact formula.

The official asymptotic subquestion is already solved; only the exact
`t=2` extremum, its secondary term, or stability could be publishable.

Classification: `RIGOROUS_STRUCTURAL_LEMMA / EXACT_CHAIN_EXPANSION_OPEN`.

## #686 — a uniform 2-adic law for an infinite parity class

Let `P_l(x)=prod_{i=1}^{2l}(x+i)` and let `A_l(x)` be the polynomial part of
`sqrt(P_l(x))`.  For every odd `l` and integer `x` we proved

\[
 v_2(A_l(x))=-l-v_2(l!),
\]

equivalently `2^{l+v_2(l!)}A_l(x)` is odd.  The proof is coefficientwise:
after centering, odd squares are all `1 mod 8`, the square-root correction is
`1+4C(t)`, and the last retained Laurent coefficient has a unique least
2-adic valuation.  It extends the former isolated `k=6` observation to all
fixed block lengths `k congruent to 2 mod 4`.  It implies eventual
nonexistence for quotient 4 at each such fixed `k`.

The isolated `k=6` expansion is already public in the official March-2026
discussion, and fixed-`N`, fixed-`k>2` finiteness is known more generally.
Thus the uniform valuation law is the new structural increment, but it does
not close #686 because `k` varies.  A newly exposed even-`l` formula

\[
 v_2(A_l(x))=l-2\operatorname{oddpart}(l)
              -v_2(\operatorname{oddpart}(l)!)
\]

passed 4096 exact evaluations (`2<=l<=64`, `0<=x<=127`) but remains a
conjecture.  It identifies a concrete coefficientwise lifting lemma rather
than another blind search.

Classification: `RIGOROUS_INFINITE_FAMILY_STRUCTURE / KNOWN_GLOBAL_BOUNDARY`;
even case `COMPUTATIONAL_CONJECTURE_ONLY`.

## #952 — finitely many narrow rational directions are impossible

The one-corridor CRT wall extends rigorously to every fixed finite union of
affine rational corridors of transverse width
`o(log T/log log T)`.  Distinct directions and their fixed-distance
neighbourhoods separate outside a bounded ball; an infinite simple path
would therefore eventually remain in one corridor, contradicting the
one-direction wall.  A Gaussian-prime path, if it exists, must keep changing
effective direction or exceed this width scale.

The theorem does not control a number of rational directions growing with
radius.  The annular-CRT modulus explosion is only a limitation of that
template, not an impossibility result.

Classification: `RIGOROUS_FINITE_DIRECTION_EXTENSION / FULL_MOAT_OPEN`.

## #963 — two binary-coordinate proof routes are false

The strong basis claim fails for `P={1,3,5,7}`: no maximum dissociated
three-subset ordinarily subset-sum spans the fourth point.  The weaker
affine-cube claim also fails.  The set

\[
 \{1,6,7,8,13,14,20,21,27,34,35\}
\]

has dissociation dimension four but lies in no affine image of `{0,1}^4`.
This now has a solver-free certificate: all 462 five-subsets have a subset-
sum collision, one four-subset is dissociated, the 4368 eleven-vertex subsets
of the four-cube reduce to 27 symmetry orbits, and exact rational
interpolation rejects all 1,496,880 affine-basis assignments.

A separate lazy-Z3 computation proved `UNSAT` for target 14 only in the
generic bounded-kernel signature; target 13 timed out `unknown`.  Neither is
the full rank-four extremum.  The viable global routes are now the modular
recursion with `O(1)` cumulative loss or a method exploiting multiplicity of
signed-span representations, not containment in one binary coordinate cube.

Classification: `EXACT_ROUTE_COUNTEREXAMPLES / ORIGINAL OPEN`.

## Workflow-level ranking

1. Strongest positive new lemma: #686 odd-half-length 2-adic law.
2. Strongest exact route correction: #963 affine-cube counterexample.
3. Cleanest geometric extension: #952 finite-direction corridor theorem.
4. Useful obstruction localization: #635 chain-neighbour reformulation.
5. #332 now has a better-defined recurrence target but no new positive
   theorem.

None crosses the stipulated Q2 stopping gate: no original problem closes,
no known main exponent/order changes, and the strongest positive statements
either sit below known global results or cover a restricted geometry.

Terminal status: `BUDGET_EXHAUSTED_NO_Q2`.
