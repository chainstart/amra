# Independent audit: W4 Gårding orbit probe

Date: 2026-08-02

Verdict: **PASS as exact routing evidence.  Both deletion matroids are
C-Gårding, all eight one-coordinate comparisons and both boundary identities
reproduce, and the strict spoke natural-slice component proof also passes.
No full four-variable domination or OPG promotion follows.**

The author script was rerun from a byte-identical temporary copy under a
512 MiB / 120 second guard so that its generated evidence file was not
rewritten.  The output SHA-256 reproduced exactly as
`ac7bdf2036609dcdf197a1d277bf062b3ef454e26a4d3905e8bfce537fcb2ea2`.

## 1. Reconstruction of `C_delete` and `xi`

For a marked edge `e`, put `E'=E(W4)-{e}`.  The deletion cospanning
polynomial is

```text
C_delete = sum_(I forest in E') product_(f in E'-I) w_f.
```

Indeed `X=E'-I` is cospanning in the convention used here exactly when its
complement `I` is independent in the cycle matroid.  For a non-loop graphic
edge, a forest `I` is independent after contracting `e` exactly when
`I union {e}` is still a forest.  This fails precisely when the endpoints of
`e` are already connected in `I`.  Consequently

```text
xi_e=C_(M\e)-C_(M/e)
```

is exactly the same complement-monomial sum restricted to endpoint-connected
deletion forests.  This validates the enumerator's definitions without using
interpolation.

Independent enumeration gives:

| marked orbit | deletion forests | endpoint-connected forests | `C(1)` | `xi(1)` |
|---|---:|---:|---:|---:|
| spoke `01` | 86 | 38 | 86 | 38 |
| rim `12` | 82 | 30 | 82 | 30 |

The stabilizer classes in the artifact are the correct two reflection
orbits: for the spoke they are `{02,04}`, `{03}`, `{12,14}`, `{23,34}`;
for the rim they are `{01,02}`, `{03,04}`, `{23,14}`, `{34}`.

## 2. Why both deletion polynomials are legitimate C-Gårding bases

Deleting spoke `01` leaves vertex `1` of degree two.  Suppressing it replaces
the path `2-1-4` by `24` and gives the simple graph `K4` on vertices
`0,2,3,4`.  In the reverse direction the deletion graph is obtained from
`K4` by subdividing edge `24`, a series extension.

Deleting rim edge `12` leaves vertices `1` and `2` of degree two.
Suppressing them gives the triangle on `0,3,4` with the `03` and `04` edges
each doubled.  The logically safe forward construction is:

1. start with the triangle;
2. add one parallel copy of `03` and one parallel copy of `04`;
3. subdivide those new copies into `02,23` and `01,14`, respectively.

Thus the rim deletion is obtained from a triangle by parallel extensions
followed by series extensions.  Fang--Ma's at-most-six-element theorem gives
the C-Gårding base (`K4` has six elements and the triangle has three), and
their series/parallel closure preserves C-Gårding.  This proves the needed
status of both deletion matroids; it does not prove W4 itself C-Gårding or the
required domination.  The closure boundary was checked against the current
Fang--Ma preprint, arXiv:2604.27755v2.

## 3. Eight exact component channels

With the other three stabilizer variables fixed to `1`, independent symbolic
enumeration reproduces all eight pairs:

| orbit/variable | `C_delete(t)` | `xi(t)` | right boundary comparison |
|---|---|---|---|
| spoke/a | `2(15t^2+22t+6)` | `2(3t^2+12t+4)` | `-2+2sqrt(6)/3 < (-11+sqrt(31))/15` |
| spoke/b | `2(27t+16)` | `2(11t+8)` | `-8/11 < -16/27` |
| spoke/c | `2(12t^2+24t+7)` | `2(14t+5)` | `-5/14 < -1+sqrt(15)/6` |
| spoke/d | `2(15t^2+22t+6)` | `2(6t^2+10t+3)` | `(-5+sqrt(7))/6 < (-11+sqrt(31))/15` |
| rim/a | `2(14t^2+20t+7)` | `2(2t^2+6t+7)` | `disc(xi)<0`, positive leading coefficient |
| rim/b | `31t^2+42t+9` | `2(5t^2+8t+2)` | `(-4+sqrt(6))/5 < (-21+9sqrt(2))/31` |
| rim/c | `2(14t^2+20t+7)` | `7t^2+14t+9` | `disc(xi)<0`, positive leading coefficient |
| rim/d | `49t+33` | `2(8t+7)` | `-7/8 < -33/49` |

In every row, the displayed `C_delete` interval is the right-hand positivity
interval containing `t=1`.  Moving only that coordinate from `t` to `1`
stays in `C_delete>0`, and then reaches the positive orthant.  Hence these
points lie in the full distinguished component, not merely in a positive
specialization.  The root comparisons show `xi>0` throughout each such
interval.  This argument is rigorous only for the eight one-coordinate
paths; it says nothing about arbitrary points of the two- or four-variable
component.

## 4. Boundary identities

On `b=a,d=c`, independent expansion confirms

```text
C_spoke=c P_s,  xi_spoke=2c Q_s,
(a+1)P_s-(a^2 c+2ac+3a+c+2)Q_s=a^2(4a^2-2a-c),
```

and

```text
P_r-(a+1)^2 Q_r=-a^2 R,
R=a^4+6a^3+2a^2c^2+7a^2c+8a^2+4ac^2+8ac+2c^2.
```

Both are polynomial identities.  Their stated scope is correct: the first
reduces the `Q_s=0` branch away from `a=-1`; it does not analyze the separate
`c=0` branch of `xi_spoke=2cQ_s`.  The second gives a reduction on
`Q_r=xi=0`, but no global sign of `R` follows.  Neither identity by itself is
a component/SOS domination certificate.

## 5. Strict spoke natural-slice component

The newly added `W4_SPOKE_NATURAL_SLICE_COMPONENT_PROOF.md` and its actual
script/JSON names `w4_spoke_c_component_proof.py/.json` were included in the
audit.  The author script was rerun from a byte-identical temporary copy under
the same 512 MiB / 120 second guard and reproduced JSON SHA-256
`562dee561634c8e44e9486059157429346aa61c2b0bee31067c8688bd49f648b`.

With `x=a+1`, direct substitution in the already checked natural slice gives

```text
C_delete=c P(x,c),  xi=2c Q(x,c),
P=A(c)x^3-2H(c)x+2(c+4),
Q=H(c)x^2-3(c+4)x+6-c,
A=(c+2)(c^2+2c+2),  H=c^2+4c+6.
```

Independent symbolic computation reproduces

```text
disc_x(P)=4c^2(c+2)(c^2+2c+2)
          (8c^4+69c^3+204c^2+206c+36),
disc_x(Q)=c^2(4c+1),
Res_x(P,Q)=-c^7(c^2+2c+2).
```

Every factor has the claimed strict sign for `c>0`.  Hence `P` has three
simple real roots `p1<p2<p3`, `Q` has two simple real roots `q1<q2`, and all
labelled roots vary continuously.  The nonzero resultant prevents any
`q_i` from crossing any `p_j`; nonvanishing leading coefficients prevent a
root from escaping through infinity at a finite positive parameter.

At `c=1`,

```text
P=15x^3-22x+10, Q=11x^2-15x+5,
q2=(15+sqrt(5))/22,
P(q2)=(95-56sqrt(5))/1331<0.
```

The last sign follows from `56^2*5>95^2`.  Since `q2>0`, `P(0)>0`, the first
cubic root is negative, and a positive-leading cubic alternates sign at its
three simple roots, this places `q2` strictly between `p2` and `p3`.
Continuity and the resultant therefore prove `q2(c)<p3(c)` on the connected
parameter interval `c>0`.

The component argument is also complete.  For `c>0`,

```text
P(1,c)=c^2(c+2)>0,
partial_x P >= 3A-2H=c(3c^2+10c+10)>0 for x>=1.
```

Thus `p3(c)<1`.  Since `c` cannot change sign along a path in
`{cP>0}`, the sliced positivity component containing positive activities is
exactly

```text
S={(x,c): c>0 and x>p3(c)}.
```

It is connected because `p3(c)` is continuous.  From every point of `S`, the
path `(x,c)->(1,c)->(1,1)->(2,1)` remains in `cP>0` and ends at
`a=b=c=d=1`, proving membership in the full deletion distinguished
component.  Finally `x>p3(c)>q2(c)` gives `Q>0`, hence `xi=2cQ>0` throughout
`S`.

The scope statement is accurate: this proves the entire sliced component
`S`, but not that the intersection of the full four-variable distinguished
component with the slice equals `S`.  Off-slice paths could join another
sliced positivity island.  It also gives no two-variable rim proof.

## 6. Disposition

- Exact enumerations and stabilizer specializations: **pass**.
- C-Gårding status of both deletion matroids: **pass** by explicit
  series/parallel construction from known bases.
- Eight distinguished interval/root comparisons: **pass**.
- Two boundary identities: **pass with their stated local scope**.
- Complete spoke natural two-variable sliced component: **strict domination
  passes**, including discriminants, resultant, root ordering and explicit
  full-component path.
- Full `xi_e triangleleft C_(M\e)` for either W4 orbit: **not proved**.
- OPG-1757: **unchanged; no promotion**.

Independent reproduction:

```bash
AMRA_MEMORY_KIB=524288 AMRA_TIMEOUT_SECONDS=120 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh \
  python3 amra-research-loop/campaigns/opg-1757-mechanism-reset/audit/verify_w4_garding_orbit_probe.py
```

The independent checker completed in about 0.5 seconds.  No Lean process was
started.

The added natural-slice checker is reproduced by:

```bash
AMRA_MEMORY_KIB=524288 AMRA_TIMEOUT_SECONDS=120 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh \
  python3 amra-research-loop/campaigns/opg-1757-mechanism-reset/audit/verify_w4_spoke_natural_slice_component.py
```
