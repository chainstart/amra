# Erdős #332: broad route autopsy beyond density

Date: 2026-07-22 (Asia/Hong_Kong)

Status: no new Q2-level theorem and no closure.  The arguments below separate
correct known mechanisms from two tempting but invalid broadenings.

## 1. The old route is correct but not new enough

Positive upper Banach density is sufficient.  One elementary formulation is
through piecewise syndeticity: if a finite set `F` makes `A+F` thick, then
every fixed integer `d` occurs infinitely often as a difference of two points
of `A+F`.  For each occurrence write

\[
 d=(a_1+f_1)-(a_2+f_2).
\]

There are only finitely many pairs `(f_1,f_2)`, so one pair recurs infinitely
often and

\[
 d-(f_1-f_2)\in D(A).
\]

Thus `Z subset D(A)+(F-F)`, which makes `D(A)` syndetic.  The standard
equivalence/implication between positive upper Banach density and piecewise
syndeticity recovers the recurrence proof.

This is a clean proof interface, but it is standard additive-combinatorial
material and cannot be presented as a new answer to #332.  Stewart--Tijdeman
(1979) already proves the positive-upper-density result and an extension
construction much stronger than the previous sparse two-point-block idea.

## 2. Additive-basis strength does not substitute for recurrence

A natural attempt was to weaken density by assuming that `A` is an
asymptotic additive basis of some fixed order.  This fails completely.

Let

\[
 A=\{n^2:n\ge1\}.
\]

By Lagrange's four-square theorem, every positive integer is a sum of at most
four members of `A`: write it as four nonnegative squares and simply omit the
zero terms.  Thus `A` has bounded additive covering order in the "at most
four" convention.  If one uses the nonnegative-integer convention for
sequences, `A_0={n^2:n>=0}` is literally an exact order-4 basis (repetitions
allowed).  Adding or deleting the single element zero does not change any
nonzero infinite-difference multiplicity.

For every fixed nonzero `d`, however,

\[
 a^2-b^2=(a-b)(a+b)=d
\]

has only finitely many integer solutions, indexed by the finitely many factor
pairs of `d`.  Hence

\[
 D(A)=\{0\},
\]

which certainly does not have bounded gaps.  Thus even bounded-order additive
covering of all large integers says essentially nothing about the recurrent
difference set.

## 3. Why the sparse-spectrum route cannot characterize a threshold

Stewart--Tijdeman's extension theorem lets one enlarge an infinite-difference
spectrum while preserving upper and lower natural densities.  The round-7
two-point-block realization is a special case of the same mechanism.  It
shows that below a genuine recurrence/density hypothesis, `D(A)` can be
arbitrarily prescribed (subject to containing zero in the nonnegative
convention).  Consequently, conditions expressed only as a very weak growth
upper envelope for `A` cannot force bounded gaps.

The useful conclusion of this round is negative but precise: a viable new
sufficient condition must encode repeated local patterns (uniform recurrence,
correlation, or a dynamical invariant measure), not merely additive-basis
power, unbounded cardinality, or a coarse counting-function envelope.

## 4. Remaining direction

The most credible route to a publishable result is now a genuinely weaker
recurrence hypothesis than positive upper Banach density, together with an
example separating it from the classical condition.  No such nonstandard
hypothesis was proved sufficient in this round, so #332 remains a route-
autopsy result only.
