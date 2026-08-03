# Exact W4 orbit probe for the Gårding moving certificate

Date: 2026-08-02
Status: **exact routing evidence; neither edge orbit killed; no promotion**

## 1. Scope and artifacts

Let `W4` be the wheel with center `0`, rim vertices `1,2,3,4`, spokes
`01,02,03,04`, and rim cycle `12,23,34,14`.  It has two edge orbits.
The exact enumerator and its generated record are:

- `evidence/w4_garding_orbit_probe.py`
  SHA-256 `028c9f3e73d955fb3fe37252d77ae99bdad94cee4a796ada3f5d8914f6444b1b`
- `evidence/w4_garding_orbit_probe.json`
  SHA-256 `ac7bdf2036609dcdf197a1d277bf062b3ef454e26a4d3905e8bfce537fcb2ea2`

For each marked edge `e`, the script enumerates all forests `I` of `W4-e`.
The complement monomial contributes to `C_{M\e}`.  It contributes to
`xi_e=C_{M\e}-C_{M/e}` exactly when the endpoints of `e` are already
connected by `I`, since precisely those forests cease to be independent after
contracting `e`.  Thus both polynomials are constructed directly, not inferred
from numerical interpolation.

The bounded reproduction was:

```bash
AMRA_MEMORY_KIB=5242880 AMRA_TIMEOUT_SECONDS=1800 \
  amra-research-loop/scripts/run_bounded.sh python \
  amra-research-loop/campaigns/opg-1757-mechanism-reset/evidence/w4_garding_orbit_probe.py
```

It exited `0` in under one second.  No Lean process was started.

## 2. Why the deletion components are legitimate

The marked-spoke deletion is a series extension of `M(K4)`: suppressing the
degree-two rim vertex incident with the deleted spoke gives `K4`.  The marked-
rim deletion reduces by suppressing its two degree-two endpoints and then by
parallel simplification to a triangle.  Fang--Ma's at-most-six-element base
and series/parallel closure therefore make both deletion matroids
`C`-Gårding.  Their distinguished positivity components are consequently
defined before any domination test is attempted.

## 3. Stabilizer-orbit polynomials

### Marked spoke `e=01`

The stabilizing reflection gives

\[
 a:\{02,04\},\quad b:\{03\},\quad
 c:\{12,14\},\quad d:\{23,34\}.
\]

The full four-variable exact polynomials are recorded in the JSON.  At
`a=b=c=d=1` they give

\[
 C_{M\setminus e}=86,\qquad \xi_e=38.
\]

On the natural two-variable slice `b=a,d=c`, write

\[
 C_{M\setminus e}=cP_s(a,c),\qquad \xi_e=2cQ_s(a,c),
\]

where

\[
\begin{aligned}
P_s={}&a^3c^3+4a^3c^2+6a^3c+4a^3
 +3a^2c^3+12a^2c^2+18a^2c+12a^2\\
 &+3ac^3+10ac^2+10ac+c^3+2c^2,\\
Q_s={}&a^2c^2+4a^2c+6a^2+2ac^2+5ac+c^2.
\end{aligned}
\]

Exact polynomial division gives the boundary identity

\[
 (a+1)P_s-(a^2c+2ac+3a+c+2)Q_s
 =a^2(4a^2-2a-c).                                      \tag{S}
\]

Thus on `Q_s=0`, away from `a=-1`, the sign of `P_s` is reduced to a
low-degree boundary factor.  Identity (S) is a candidate input for an eventual
component/SOS argument; no global sign is claimed here.

### Marked rim `e=12`

The stabilizing reflection gives

\[
 a:\{01,02\},\quad b:\{03,04\},\quad
 c:\{23,14\},\quad d:\{34\}.
\]

At `a=b=c=d=1`, exact enumeration gives

\[
 C_{M\setminus e}=82,\qquad \xi_e=30.
\]

On `b=a,d=c`, let the resulting polynomials be `P_r=C_{M\e}` and
`Q_r=xi_e`; their expansions are in the JSON.  They satisfy

\[
 P_r-(a+1)^2Q_r=-a^2R(a,c),                              \tag{R}
\]

with

\[
 R=a^4+6a^3+2a^2c^2+7a^2c+8a^2
   +4ac^2+8ac+2c^2.
\]

Identity (R) is the corresponding exact `xi=0` boundary reduction.  The
remainder is not asserted nonnegative on all of `R^2`; distinguished-component
control is still the missing step.

## 4. Rigorous one-coordinate component channels

For each row below, the other three stabilizer variables are fixed to `1`.
The displayed interval is exactly the connected component of
`{C_{M\e}(t)>0}` containing `t>0`.  Any point in it has the explicit path
obtained by varying `t` within the interval to `t=1`, while all other original
edge activities remain `1`.  Hence every point in a displayed interval is
rigorously in the **full** distinguished positivity component, not merely in
a positive set of a specialization.

| orbit | variable | `C_delete(t)` | `xi(t)` | distinguished interval |
|---|---|---|---|---|
| spoke | `a` | `2(15t^2+22t+6)` | `2(3t^2+12t+4)` | `t>(-11+sqrt(31))/15` |
| spoke | `b` | `2(27t+16)` | `2(11t+8)` | `t>-16/27` |
| spoke | `c` | `2(12t^2+24t+7)` | `2(14t+5)` | `t>-1+sqrt(15)/6` |
| spoke | `d` | `2(15t^2+22t+6)` | `2(6t^2+10t+3)` | `t>(-11+sqrt(31))/15` |
| rim | `a` | `2(14t^2+20t+7)` | `2(2t^2+6t+7)` | `t>(-10+sqrt(2))/14` |
| rim | `b` | `31t^2+42t+9` | `2(5t^2+8t+2)` | `t>(-21+9sqrt(2))/31` |
| rim | `c` | `2(14t^2+20t+7)` | `7t^2+14t+9` | `t>(-10+sqrt(2))/14` |
| rim | `d` | `49t+33` | `2(8t+7)` | `t>-33/49` |

In all six channels where `xi` has a real rightmost root, exact radical or
rational comparison puts that root strictly to the left of the displayed
`C_delete` boundary.  In the rim-`a` and rim-`c` channels, `xi` has negative
discriminant and positive leading coefficient.  Therefore

\[
 \xi_e(t)>0
\]

throughout every one of the eight rigorously identified distinguished
channels.  The closest gap occurs in spoke-`c`:

\[
 -\frac5{14}< -1+\frac{\sqrt{15}}6,
\]

with a gap of about `0.00264`; spoke-`a` is next at about `0.00486`.  These
narrow boundary gaps are useful targets for an exact SOS or proper-position
explanation.

## 5. Disposition

- Spoke orbit: **not killed** on any audited component channel.
- Rim orbit: **not killed** on any audited component channel.
- Full four-variable domination: **not proved**.
- Full two-variable component geometry: **not claimed**.
- New exact evidence: the four-variable enumerations, eight strict boundary
  comparisons, and identities (S) and (R).
- OPG-1757 promotion: **none**.

The next useful step is to explain the two small spoke boundary gaps and to
turn (S), or a stabilizer-refined analogue before `b=a,d=c`, into a sign
decomposition valid on the deletion component.  Numerical sampling outside a
proved component should not be used as counterevidence.
