# Moving-edge next-host ledger

This ledger separates full stabilizer-variable certificates from the global
independent-edge problem.

| Host / marked orbit | Stabilizer variables | Status | Remaining scope |
|---|---:|---|---|
| `W4` rim | 4 | proved and independently audited | independent-edge/global transport |
| `W4` spoke | 4 | proved and independently audited | independent-edge/global transport |
| `K3,3` unique edge orbit | 2 | proved and independently audited | 8 independent unmarked activities |
| triangular prism vertical orbit | 3 | proved and independently audited | triangle-edge orbit and 8 independent activities |
| `K5-e` high-triangle edge orbit | 3 | complete stabilizer slice proved and independently audited | 8 independent unmarked activities |
| triangular prism triangle orbit | 5 | exact 5-variable representation; `z=1` two-variable component proved and independently audited inside a 3-variable coarsening | full 3-variable component, then complete 5-variable stabilizer slice |
| `K5-e` cross orbit | not yet frozen | not attacked | complete stabilizer slice |

The exact unlabeled census proves that these are the only 3-connected hosts
through nine edges after `W4`: `K3,3`, the triangular prism, and `K5-e`.
Closing a stabilizer slice is a mechanism test, not the full marked-host
theorem, because equalizing activities loses independent directions.  The
global G201 moving-edge quantifier and OPG-1757 remain open.

The reusable mechanism emerging from the successful rows is to factor the
deletion polynomial by its anchor walls, then prove that the `xi=0` locus
lies in the wrong sign chamber.  The `K5-e` attack demonstrates why a
resultant factor alone is insufficient: its anchor component crosses both
`z<1` and `H<0`, while a separate `P>0,xi<0` component exists outside the
anchor chamber.
