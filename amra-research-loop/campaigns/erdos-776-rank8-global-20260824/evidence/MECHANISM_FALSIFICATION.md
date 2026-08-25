# Mechanism falsification

Twelve mechanisms in eight families were stated with exact scopes.  Ten of
the ten non-survivors are killed, giving kill ratio `10/(12-2)=100%`.

## Exact counterexamples

| Mechanism | Least/displayed obstruction | Exact scope |
|---|---|---|
| two-binomial invariant | `V=288`: `D18-P18=-2924809`, `D16-P16=67` | Does not kill the inherited residual rank-18-to-rank-8 theorem. |
| independent taxes | `V=40`: second tax `2877875 > 296010` | Requires overlap credit; does not kill globally recompressed accounting. |
| blind adjacent shadow | `V=40`: `5476185 > 1560780` | Requires common-prefix cancellation; does not kill suffix coupling. |
| `W_6` nonincreasing | `W_6(51)-W_6(50)=2` | Margin monotonicity remains open. |
| `W_6` nondecreasing | `W_6(41)-W_6(40)=-8905` | Carry-height bounds remain open. |
| one affine rank-six cell | word length is 6 at `V=42` and 5 at `V=43` | Piecewise/carry-aware word theorems remain open. |
| fixed-sign Hilbert defect | same `V=288` rank-18/rank-16 sign reversal | A multiplication-map invariant stronger than scalar shape is not tested. |

Two overclaims are killed by exact logical interfaces.  A protected last
colex set without a backward preimage invariant is exactly the original
inequality because

\[
 {V-11\choose8}-{V-12\choose8}-{V-13\choose7}
 ={V-13\choose6}.
\]

Likewise, the local rank-eight entry has no information about the independent
lower-bound and small-`r` obligations and therefore cannot determine the
public threshold by itself.

Finally, scalar order alone does not imply normalized decay: for the adjacent
`V=40` capacities, `1<=2` but

\[
 2\cdot296010=592020>376740=1\cdot376740.
\]

This kills only the claimed derivation, not the empirical normalized `W_6`
inequality.

## Survivors

1. **Adjacent suffix loss:**
   \(W_6(V+1)-W_6(V)<{V-13\choose5}\) for every `V>=40`.
   This is a strong sufficient condition, not a necessary one.  The exact
   next-step criterion is `j_V<=c_V+M(V)-1` once `M(V)>=1`.  Prefix
   cancellation may only be invoked after an independently proved high-rank
   separator; it cannot assume the rank-six target.  The noncircular refined
   interface is recorded in `HIGH_RANK_ONE_SIDED_BRIDGE.md`.
2. **Logarithmic carry height:** the top upper index of the six-canonical word
   is at most `ceil(log_2 V)+13` on the branch `W_6>0`; the `W_6<=0` branch is
   immediate success and has no nonempty canonical top to bound.  The missing step is
   a quantitative injection from top-index increases to parameter doublings.

The executable scan through `V=500` found no counterexample to either
survivor.  That bounded result is recorded only as falsifier evidence.
