# New-problem round 3 — 2026-08-26

The selected target is Erdős #451.  This is a deliberately non-random choice:
the public problem is still open, a June 2026 result supplies a verified new
lower-bound interface, and the remaining CRT upper-bound obstruction admits
exact finite falsifiers.  Problems #963 and #934 were rejected as repository
duplicates; #684 was deferred because of a very recent strong result and active
external work.

The admission contract is not “work for several hours and hope”.  The round is
allowed to deepen only if it produces one of the following signals:

1. a prefix-discrepancy lemma that is stronger than an average over translates;
2. a strict audited improvement to a quantitative loss in the June 2026 lower
   bound; or
3. a standalone no-go theorem that eliminates a broad family of sieve or
   entropy mechanisms.

All expensive computation is executed through the OpenMath memory guard with
aggregate limits high=30 GiB, max=34 GiB, swap=4 GiB, tasks=512.

## Survivor continuation result

The quantitative signal crossed the formal-evidence threshold.  A pinned Lean
4.28.0/mathlib 4.28.0 replay first reproduced the public denominator-`20`
theorem and then kernel-checked a denominator-`16` patch.  The patch had to
separate the boundary case `r=3`, retaining its `k^(-1/18)` power saving, from
the `r>=4` logarithmic envelope.  A second theorem formalizes that the produced
prime lies in the public interval `(k,2k)` for sufficiently large `k`.

The final guarded clean replay used zero swap and peaked below 7.9 GiB RSS.
The certificate has no `sorryAx`; its only non-foundational axiom is the same
named Baker--Harman--Pintz input `bhp` used upstream.  The campaign is therefore
ready for `independent_audit`, not promotion: the same session authored and
replayed the patch, and public priority remains uncertain.
