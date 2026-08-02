# Erdős #776: adaptive-seed campaign

Date: 2026-08-02 (HKT)

This workstream attacks the remaining rank-42 capacity gate behind the
current proposed construction for Erdős #776.  The original problem is to
determine how large \(n\) must be, as a function of \(r\ge2\), in order to
admit an antichain in \(2^{[n]}\) occupying \(n-3\) distinct ranks, with at
least \(r\) members on every occupied rank.

The inherited route reduces the desired construction to a diagonal-seed
problem for adjacent Macaulay orbits.  The fixed rank-six seed is false, and
the family \(b=L/2+5\) proves that no fixed post-carry rank can work.  This
campaign therefore uses the correct adaptive target:

\[
 \exists p=p(L,b)\quad \gamma_p(L,b)\ge0,
\]

at a legal rank before the rank-42 endpoint, uniformly over every dyadic
strip and every \(1\le b\le L\).

The campaign began with an independent all-parameter audit of the inherited
synchronized rank-four/rank-five bridge, then attacked the pre-cap branch,
the omitted offsets \(b-L/2<0\), and a uniform adaptive rank bound.  Exact
scans and verifiers are used for falsification and finite certificates only;
they are not promoted to universal proofs.

The first new result is a second exact adaptive wall on the omitted side:
the fixed family \(b=5\) has no fixed-rank seed, and its exact first seed is
again of order \(\log_2\log h\).  Its first rank-five failure is
\((j,L,b)=(17,14680064,5)\).  This refutes a bounded-rank negative-offset
shortcut but does not refute the original problem.

The moving result is stronger.  Every \(b\ge5\) in the initial
double-borrow chamber \(b^2-b+4<4h\) has a uniform seed by
\(\log_2\log h+O(1)\): the pre-cap constant is minimized at \(b=5\), every
later first cap is immediately positive, and a negative initial cap
recovers at the next row.  See `NEGATIVE_PRECAP_ATLAS.md` and
`NEGATIVE_CAP_RECOVERY.md`; the latter is guarded by
`verify_negative_cap_recovery.py`.

The adjacent initial \(x\)-only borrow chamber is also closed by rank four.
The remaining negative-offset initial state is the no-borrow chamber.  Its
proposed rank-five implication (2.13) is now refuted on the actual dyadic
lattice, although the counterfamily recovers uniformly at rank six.

The former proof boundary is recorded in `NO_BORROW_GATE_FREEZE.md`; that
freeze is now explicitly marked superseded by the counterfamily.

Red Team I independently passed that reduction after a missing cap-legality
guard was repaired.  It also derived the exact three-chamber formula for
the next \(\gamma_4\) transition under a one-promotion/single-wall premise.
An asymptotic construction shows that every fixed \(K=b-q\ge4\) contains
infinitely many relaxed points in the antecedent, so a finite-\(K\) case
split could not prove the then-proposed \(\gamma_5>0\) bridge.  See
`../opg1757/ERDOS776_NEGATIVE_INITIAL_CHAMBERS_RED_TEAM.md`.

The next transition has a unified exact rank-five identity and an
independent six-chamber verifier; see `ONE_PROMOTION_RANK_FIVE_CHART.md`.
The large leading blocks are retained through the full-block loss
\(\Lambda_{j,A}\), rather than discarded by pure superadditivity.  Two
all-parameter convolution lifts then prove strict rank-five positivity in
five chambers:

\[
(++)\to(--),\qquad(++)\to(-+),\qquad(-+)\to(+-),
\qquad(--)\to(-+),\qquad(--)\to(--).
\]

The third row is the unique reversed second-tail state.  Each lift has an
exact finite base and an analytic infinite tail; see
`LEADING_BLOCK_DEFICIT_THEOREM.md` and its verifier.  The sixth chamber
\((--)\to(++)\) is not positive: the family \(K=6,r=10\) contains
infinitely many actual dyadic points with
\(\gamma _5=4\,302\,695-6q<0\).  Its first failure has
\((s,q)=(14,1\,468\,006)\), and every point in the family has
\(\gamma _6>0\).  See `FINAL_CHAMBER_COUNTERFAMILY.md` and its independent
verifier.

Current status: **the original problem and the uniform adaptive-seed theorem
remain open**.  The fixed rank-five bridge is refuted, not the original
problem.  See `CLAIM_LEDGER.md` and `RESEARCH_LOG.md` for the live evidence
boundary.
