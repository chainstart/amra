# Lean certificate replay for the `1/16` constant

This directory pins and replays the public Lean formalization of Erdős problem
451 at upstream commit `92a033fa99f0a53a3c16257c47e3d9e04dfc3f55`, then applies
`erdos451-c16.patch` and checks the strengthened theorem
`main_theorem_c16`.

The environment is fixed to Lean `v4.28.0` and mathlib commit
`8f9d9cff6bd728b17a24e163c9402775d9e6a365` (the `v4.28.0` tag). Both the
upstream source and the patched source are protected by SHA-256 checksums.

Run the complete replay with:

```bash
./verify_guarded.sh
```

The wrapper always enters the OpenMath aggregate resource guard before Lake or
Lean starts. At the time this certificate was produced, that guard imposed a
30 GiB soft memory limit, 34 GiB hard memory limit, 4 GiB swap limit, and a
512-task limit. Generated sources, Mathlib build data, and logs are ignored by
Git.

Successful output must include all of the following axiom reports and no
`sorryAx`:

```text
'main_theorem' depends on axioms: [bhp, propext, Classical.choice, Quot.sound]
'main_theorem_c16' depends on axioms: [bhp, propext, Classical.choice, Quot.sound]
'main_theorem_c16_two_k' depends on axioms: [bhp, propext, Classical.choice, Quot.sound]
```

The formal result remains conditional on the upstream `bhp` axiom. It improves
the denominator in the admissible upper range from `20` to `16`; it does not
solve the unrestricted public problem.
