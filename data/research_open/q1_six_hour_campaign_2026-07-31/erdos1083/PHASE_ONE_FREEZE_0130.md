# Erdős #1083: phase-one freeze and dependency graph

Freeze time: 2026-08-01 01:30 HKT

## Status

Phase one is frozen.  The transverse-heavy exact-block branch has
been reduced to three explicit network outputs.  All three now meet
the same missing interface: convert a bounded labelled row network
into either more than the allowed global distance budget or a
large ruled/commensurate configuration already covered by an escape
theorem.

No claim that Erdős #1083 is solved is made.

## Dependency graph

```text
Frozen exact common-spectrum block
q=t^(13/18), S=t^(7/9), U=t^(5/6), R<=t, |V|=SU=t^(29/18)
                    |
                    v
Tangent overlap split + fixed-tangent transverse rigidity
                    |
          transverse-heavy branch
                    |
                    v
One fixed nonzero tangent difference delta
M=t^(8/9+o(1)) distinct ordered transverse row edges
                    |
        +-----------+-------------------------------+
        |                                           |
        v                                           v
Short-cycle extraction                         Simple-path energy
t^(8/9) edge-disjoint cycles <=10             length 80
        |                                      shared endpoints:
        |                                      t^(227/18)
        |                                      fix endpoint labels +
        |                                      full orientation word:
        |                                      t^(199/18)
        |                                           |
        |                                  compare with reference Q
        |                                           |
        |                    +----------------------+------------------+
        |                    |                      |                  |
        |                    v                      v                  v
        |             D_P != D_Q           same D, transition   same D, all
        |                    |               misalignment        transitions aligned
        |                    |                      |                  |
        v                    v                      v                  v
coherent/noncoherent   homogeneous height     noncoherent       fixed defect spine
cycle dichotomy       relation, support       simple cycle      + coherent gaps
                      <=158                   length <=160              |
                                                                       v
                                                            checkpoint compression
                                                            t^(1/10) coherent
                                                            simple paths, length <=6
                                                                       |
                                                                       v
                                                            hub / greedy packing
                                                            t^(1/20) lifted-row hub
                                                            or internally disjoint
                                                            coherent theta arms
```

The short-cycle route additionally proves that a coherent cycle has
one of 36 orientation types and at most six potential levels.  The
long-path route fixes both endpoint rows, both endpoint source labels,
and the full orientation word before the final trichotomy.

## Three frozen outputs

| branch | exact output | quantitative scale | missing conversion |
|---|---|---:|---|
| Homogeneous relation | \(\sum z_wc_w=0\), \(c_w\in(X-X)-(X-X)\), support \(\le158\) | \(t^{199/18+o(1)}\) path witnesses before distinctness | Prove enough coefficient-rank/distinctness to force a ruled chart or too many global distances |
| Transition misalignment | Genuine noncoherent simple cycle with one fixed \(\delta\), length \(\le160\) | Power-large path-witness branch; distinct cycles not yet claimed | Turn the bounded affine height identity into a geometrically nondegenerate distance-budget contradiction |
| Aligned network | Coherent paths of length \(2\)--\(6\) with fixed lifted endpoints, then a lifted-row hub or internally vertex-disjoint theta | \(t^{1/10+o(1)}\) paths; \(t^{1/20+o(1)}\) hub/arms | Control tangent-record or common-distance-label reuse on the short network |

## Multiplicity and simplicity audit

1. **Direction compression.**  A fixed ordered transverse row pair
   and fixed nonzero \(\delta\) has at most one source-label pair.
   Forgetting direction merges at most two opposite ordered edges.

2. **Complete direction word.**  A length-80 path has exactly
   \(2^{80}\) possible \(\pm1\) words.  This is an absolute constant,
   so it costs no power of \(t\).

3. **Midpoint/checkpoint fibres.**  At fixed potential and fixed row,
   \(z^2+2\rho zx=C\) determines at most one source label because
   \(\rho z\ne0\).  The fibre is at most \(q\), not \(qS\).

4. **Half-path multiplicity.**  One ordered pair of half paths
   determines at most one concatenated full path.  Hence, after a
   midpoint fibre contains \(N/q\) paths, \(AB\ge N/q\).

5. **Individual path simplicity.**  Minimum-degree extension forbids
   all previously visited rows.  Every original path is simple, and
   every midpoint half, coherent gap, and checkpoint segment is a
   contiguous simple subpath.  Different paths may overlap.

6. **Defect support.**  Endpoint labels are stored separately.
   Therefore every nonzero coordinate of a common defect vector is an
   internal row on every path in that common-defect family.

7. **Closed-trail repeated edges.**  \(P\cdot Q^{-1}\) is an
   edge-occurrence trail of length at most 160 and may contain a
   repeated edge or immediate reversal.  Such doubled-edge pieces use
   identical endpoint labels and are coherent.  After removing them,
   transition misalignment forces a genuine noncoherent simple cycle;
   it cannot be an artefactual two-edge backtrack.

8. **Six-step output.**  Checkpoint pieces have length at most six and
   are simple.  The exact worst checkpoint exponent is
   \(2201/20160>1/10\), attained at a 79-edge gap split into 14 pieces.

## Common final interface

The next theorem should consume any one of the three frozen outputs
and return one of:

\[
 \boxed{|\Delta(P)|>t^3}
 \qquad\text{or}\qquad
 \boxed{\text{a power-large ruled/commensurate row family}}.
\]

Concretely it must use the exact tangent partitions

\[
 V=(\rho^2+z_i^2+T_i)\oplus(2\rho z_iX),
 \qquad T_i\subseteq T_*,
\]

rather than graph density alone.  The current exponents do not force
raw tangent reuse by pigeonhole: the short theta exponent \(1/20\) is
still below \(U=t^{5/6}\).  A successful interface must therefore be
an energy/inverse theorem, not a first-moment count.

## Frozen validation

- exact verifier: pass;
- regression tests: 21/21 pass at freeze;
- claim firewall: #1083 remains open;
- next action: cross-audit at 02:30 HKT, with no branch expansion
  before that review.
