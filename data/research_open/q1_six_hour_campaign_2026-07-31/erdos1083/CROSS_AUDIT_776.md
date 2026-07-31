# Independent blind audit of Erdős #776 moving-\(k\) bridge

Audit window: 2026-08-01 02:20 HKT onward
Auditor: independent #1083 workstream
Source policy: read-only; no file under `erdos776/` will be modified

## Preregistered protocol (written before reading the frozen bridge)

The audit will not accept a finite verifier by itself as proof of an
all-parameter claim.  It will reconstruct the symbolic state space first,
then compare the reconstruction with the manuscript and verifier.

1. **Definitions and quantifiers.** Record the exact domains of \(h,k\), all
   digit/carry/borrow variables, the endpoint map, and every strict versus
   weak inequality used by the final bridge.
2. **Borrow-state exhaustiveness.** Derive all reachable states directly
   from the arithmetic recurrence.  Check both existence (every listed state
   is reachable) and completeness (no reachable state is omitted), including
   the initial and terminal states.
3. **Endpointization and sign.** For every local inequality, compute the
   endpoint replacement explicitly and verify that the replacement preserves
   the required sign.  Equality cases and zero factors are tested separately.
4. **Boundary matrix.** Test \(k=0\), the first positive and negative values of
   \(k\), both endpoints of each \(h\)-range, and every point where a floor,
   ceiling, quotient, or borrow state changes.  Check whether the proof needs
   \(h\geqslant 1\), \(|k|<h\), \(|k|\leqslant h\), or another hidden guard.
5. **Negative-\(k\) reduction.** Verify the stated involution/reindexing
   algebraically, including its image range and endpoints; no appeal to
   informal symmetry is accepted.
6. **Adversarial finite search.** Independently enumerate the smallest legal
   parameter ranges, all transition boundaries, and one point on each side of
   every boundary.  Any discrepancy is minimized to the lexicographically
   smallest certificate.
7. **Proof/verifier agreement.** Check that the verifier implements the same
   orientation, inequalities, domains, terminal convention, and endpoint map
   as the prose theorem.  Sampled checks will be labelled as such and will not
   be upgraded to universal claims.

## Frozen-source identification

Pending the #776 freeze signal.

## Findings

Pending.

## Verdict

Pending.
