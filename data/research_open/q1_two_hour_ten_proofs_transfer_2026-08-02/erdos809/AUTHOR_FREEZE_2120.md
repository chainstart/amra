# Erdős #809 author freeze

Freeze prepared: 2026-08-02 21:07 HKT  
Required checkpoint: 21:20 HKT  
Status: **AUTHOR-FROZEN / NOT CROSS-AUDITED / PUBLIC PROBLEM OPEN**

## Frozen claims

1. Under `L_4(2)`, minimum degree at least three, and rainbow `C_7`, every
   entire colour graph is an induced matching.  Its existential proper
   two-label state has a full independent `2^t` edge-flip gauge.
2. The parity-sharp graph family has a noninjective rainbow recolouring with
   `g` repeated `2K2` colour classes.  For `g>=5` the rows also have the
   previously audited `L_4(2)` property.  The exact defect `D_B=g` injects
   into an actual missing-star reserve of size
   `delta+2*kappa-g-5 >= g`.
3. In the inherited maximum-witness B-opposite normal form, the even and odd
   vertex deficits dominate the exact three-coordinate energies (E) and (O),
   including the centre concavity term `2*u*(h-u)`.  The fixed-width bands,
   arbitrary-deficit localization, and one-leaf defect consequences follow.
4. These results do not settle Branch A, B-same, general B-opposite
   reserve-Hall expansion, or any other open #809 branch.  Erdős #809 is not
   claimed proved or refuted.

## Verification output

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
  data/research_open/q1_two_hour_ten_proofs_transfer_2026-08-02/erdos809
```

Output:

```text
9 passed in 34.28s
```

The guards rebuild 34 sharp parity rows, 408 repeated classes/reserve
injections, the complete matching-label gauge through ten edges, and
10,323,118 base stability profiles with sampled endpoint/interior centre
offsets.  The unbounded conclusions rest on the displayed proofs, not on
finite extrapolation.

## Frozen hashes

```text
2787b2fa673f688492d988abcdaf1ee15c29cd943d85333e4e9c3441815239b9  CLAIM_LEDGER.md
4eb83fbe8d3ecaa030215a157d530f09e8f26c2ff7c203c56ca3a0f4bfb153da  MAXIMUM_WITNESS_NEAR_SHARP_STABILITY.md
207896890131d1de0059031dbd147e6370be0cc8cda1204b9bd0b22d6b7d42f3  TEN_PROOFS_PALETTE_RESERVE_TRANSFER.md
d9d98503f7602ae4c0bfbeab2564e0116349f48fce79bd4cd01e17ad938caf0a  verify_near_sharp_stability.py
81a4efe3b83bd4c0f7002849653cf90a0352a4dadae6fced03b1bc7c3958f9fe  verify_palette_reserve_transfer.py
```

