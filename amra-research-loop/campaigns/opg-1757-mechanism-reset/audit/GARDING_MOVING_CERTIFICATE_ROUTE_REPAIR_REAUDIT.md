# Repair reaudit: Gårding moving-certificate route

Date: 2026-08-02
Auditor: `/root/erdos809_lane`
Verdict: **PASS AFTER REPAIR; K5 ARTIFACT IS ROUTING EVIDENCE ONLY**

## 1. Reaudited artifacts

- `evidence/GARDING_MOVING_CERTIFICATE_ROUTE.md`
  SHA-256 `1a091dc718879f4688e3f1cb3c64f2bd856f8c4d6f77439c8610a731636ff5f0`
- `evidence/k5_garding_orbit_probe.py`
  SHA-256 `11c90a57645e0aba6a25d4dc6257b9f97422a429b0cf26f8d71ec2b75d87f0f6`
- `evidence/k5_garding_orbit_probe.json`
  SHA-256 `0b8a16c4b4ed00a17e06cb2f1614a0177600412cedc5883b7e5f0df92d8078ed`

This is a targeted reaudit of the repairs requested in
`GARDING_MOVING_CERTIFICATE_ROUTE_INDEPENDENT_AUDIT.md`.  No Lean process was
started.

## 2. Prior findings and repair status

| Prior finding | Reaudit |
|---|---|
| Appendix B was being read too much like a `C/xi_e` certificate | **FIXED.** The note now says explicitly that Fang--Ma certify the spanning-set (`S`) polynomial of `M(K4)`, and uses it only as a qualitative analogy. |
| The 3-connected lemma did not itself supply the deletion hypothesis after `M\e` lost 3-connectivity | **FIXED.** The decisive lemma now quantifies over every nonempty loopless graphic matroid. |
| “Minor induction” omitted the actual closure/decomposition interface | **FIXED.** Strong induction is stated for the global lemma, while a 3-connected-only search is conditioned on explicit direct-sum, series/parallel, and 2-sum decomposition of a minimal counterexample. |
| `K5` risked being read as the smallest new host | **FIXED.** `W4` is now identified as the smaller 8-edge host and `K5` only as the especially symmetric host. |

The repaired moving-edge lemma is closure-equivalent in the claimed sense.
For the forward use, take a nonempty loopless graphic `M` and induct strongly
on `|E(M)|`.  Deletion preserves graphicness and looplessness, so `M\e` is
covered by the induction hypothesis; Proposition 13.9 then proves `M` is
`C`-Gårding.  The empty matroid is the base.  Graphic matroids with loops are
recovered using `C_M=w_e C_{M\e}` repeatedly.  Conversely, if all graphic
matroids are `C`-Gårding, Proposition 13.9 supplies such an edge for every
nonempty loopless one.

The note could spell out the empty base and the final loop-removal sentence,
but both are immediate from the cited deletion--contraction formula and no
longer constitute a logical gap.  The revised note therefore passes this
reaudit.

## 3. K5 orbit probe scope

Static inspection confirms the following exact finite construction:

- the marked edge is `01`, and all ten edges of `K5` are equivalent by graph
  symmetry;
- `C_delete` enumerates complements of forests in `K5-01`;
- `xi` counts exactly those deletion forests in which `0` and `1` are already
  connected, which is `C_{M\01}-C_{M/01}`;
- the specialization identifies the six remaining edges incident with `0`
  or `1` as `a`, and the three edges induced by `2,3,4` as `b`;
- the script then restricts further to the one-dimensional diagonal `a=b=t`.

This is a severe specialization of the full nine-variable distinguished
component.  Accordingly, the script docstring and JSON interpretation both
state that absence of a diagonal counterexample proves nothing about full
domination.  They do not claim a certificate, a counterexample, or an OPG
promotion.

The generated diagonal data are

\[
 C_{M\setminus e}(t)=t^9+9t^8+36t^7+77t^6+75t^5,
 \qquad
 \xi_e(t)=3t^7+27t^6+75t^5.
\]

The JSON reports `t>0` as the distinguished diagonal interval.  Every stored
rational sign sample is negative (`-1/2` through `-1/128`) and has
`C_delete<0`; hence **none of those samples lies in the reported interval or
tests domination**.  This is harmless for the present interpretation because
the artifact claims no kill.  For future automation, the script should either
filter samples by `q > largest_f_root` or label each sample with an explicit
interval-membership Boolean, so out-of-component values cannot accidentally
be promoted as evidence.

## 4. Disposition

- Repaired route note: **PASS**.
- Global moving-edge lemma as a sufficient/equivalent research target:
  **PASS**, with empty/loop bases understood as above.
- 3-connected decomposition language: **PASS**.
- K4 literature qualification: **PASS**.
- `W4`/`K5` host ordering: **PASS**.
- K5 Python/JSON mathematical scope: **PASS AS ROUTING EVIDENCE ONLY**.
- K5 negative rational samples: **NO CERTIFICATE AND NO KILL EVIDENCE**;
  all are outside the reported distinguished diagonal interval.
- OPG-1757 promotion: **UNCHANGED / NOT WARRANTED**.
