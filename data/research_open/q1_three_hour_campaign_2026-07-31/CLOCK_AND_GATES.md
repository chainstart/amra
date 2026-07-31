# Clock and research gates

## Fixed times

| Event | HKT |
|---|---|
| Start | 2026-07-31 08:10:32 |
| Earliest completion | 2026-07-31 11:10:32 |
| System-paused effective-work counter | 2026-07-31 09:29:51 (4,759 s credited) |
| User-directed resume | 2026-07-31 17:03:32 |
| User reset: new full three-hour budget | 2026-07-31 17:05:46 |
| New hard midpoint | 2026-07-31 18:35:46 |
| New earliest completion | 2026-07-31 20:05:46 |
| Final root audit began | 2026-07-31 20:32:30 |
| Final root audit completed | 2026-07-31 20:47:46 |

The original literal wall-clock threshold has elapsed.  The goal service
nevertheless paused the run after 4,759 seconds of credited work.  At
17:05:46 the user replaced the remaining-time interpretation with a new,
full three-hour budget starting immediately.  No earlier work or waiting time
is credited against this new interval.

## Gates

- [x] G0: previous campaign committed and pushed to `origin/main`.
- [x] G1: three primary theorem contracts and overclaim firewall frozen.
- [x] G2: first parallel proof attacks complete.
- [x] G3: midpoint red team and resource reallocation complete.
- [x] G4: second concentrated attacks complete.
- [x] G5: independent proof audits and exact regression complete.
- [x] G6: literature/priority boundary and unified claim ledger complete.
- [x] G7: literal three-hour wall clock elapsed.
- [x] G8: new full interval through 20:05:46 HKT complete.

The renewed interval was used in full.  At its midpoint the (q=6),
#809 eighth-stage, and #776 fourth-stage computations were already running;
they were allowed to finish.  No new research attack was launched after the
hard endpoint.  Work after 20:05:46 was limited to independent reruns,
quantifier repair, and final documentation.

## Decision rule

At every gate, record the first unproved inference rather than the amount of
algebra completed. A route continues only if its next missing statement is
both:

1. sufficient to improve the publication-level theorem; and
2. not merely an equivalent re-encoding of an already open barrier.
