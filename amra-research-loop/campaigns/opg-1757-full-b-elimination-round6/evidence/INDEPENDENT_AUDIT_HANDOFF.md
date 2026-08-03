# Independent-audit handoff: full fixed-space domination

## Audit boundary

This file is an **author-prepared handoff**, not an independent audit.  The
campaign is at `independent_audit`; `audit.json` must remain unpassed until a
reviewer who did not author the proof completes a blind reconstruction.

Candidate statement:

> For the five stabilizer-orbit variables of `K5-34` with marked edge `03`,
> the endpoint-connectivity polynomial `xi` is strictly positive on the full
> distinguished Gårding component of the marked-edge deletion polynomial
> `P`.

The candidate does not include transverse independent-edge variables or any
global OPG-1757 conclusion.

## Blind reconstruction protocol

The auditor should avoid importing the author's polynomial or factor lists
until completing steps 1--4.

1. Start from the graph edges
   `01,02,04,12,13,14,23,24`, mark endpoints `0,3`, and independently
   enumerate complement-of-forest monomials under orbit classes
   `a={01,02}`, `b={04}`, `c={12}`, `d={13,23}`, `e={14,24}`.
2. Check the graph decomposition as `M(K4)` plus a parallel copy of `12`
   subdivided through vertex `3`; independently verify the precise
   Fang--Ma v2 dependencies for C-Gårding, strictly positive pullback, PRT,
   and derivative nesting.
3. Recover the derivative channels giving
   `x,w,y,z>0`, `xy,xz,yz>1`, `A>0`, and `L>0` on the component.
4. Independently eliminate `b`, shift
   `x=a+1,w=c+1,y=d+1,z=e+1`, and derive the `D`-slope identity, the
   quadratic `R(w)`, the `H/F` master identity, both resultants, and the two
   parameter-chamber sample signs.
5. Audit every degenerate locus separately: `x=1`, `y=1`, `z=1`, `T=0`,
   `r2=0`, discriminant zero, and vanishing boundary resultant.
6. Only after the blind derivation, compare with
   `FULL_FIXED_SPACE_DOMINATION.md` and run the author verifier.

## Required audit decisions

- `statement_match`: confirm the result is exactly five-variable and local.
- `dependency_check`: confirm the deletion polynomial is the CSGF to which
  Fang--Ma applies, and confirm no convexity premise is used.
- `independent_reconstruction`: record auditor identity and independent
  artifacts; rerunning the author script alone is insufficient.
- `novelty_check`: compare the fixed-space theorem and orientation identity
  with primary literature; use `priority_uncertain` if unresolved.
- `promotion_decision`: the frozen contract permits only
  `global_interface_closed`, which is not met.  Even if the local theorem
  passes audit, it must not be promoted under this campaign contract.

## Frozen author artifacts

```text
verify_fixed_space_domination.py
  sha256 5c75db039f01bfab799b1d45f664d6eec5ea40ca9aa3f5483c558b556d57cf5b
FULL_FIXED_SPACE_DOMINATION.md
  sha256 025cfe2b300c1873c1816c8d384283c0ea10a465a5ca36a2ead63f9eb7a6fe80
full_fixed_space_domination.json
  sha256 8ac5c7a75646167f6be78a0ccb974399d7b051494b81c64ad18fb26b4623bccb
verify_garding_prt_firewall.py
  sha256 087275a75e3062b45f8109635b99fa0fdedb09f7974c9b3d7c63593e989ddef5
GARDING_PRT_COMPONENT_FIREWALL.md
  sha256 06295abf1ce7a8e549004e74f028da58051d4459dd82fceb508b8b924e7bc729
```

Author-side red-team diagnostics additionally rederived the master identities
with SymPy and sampled 2,369,875 points in the larger proved derivative
chamber, finding zero violations.  This is only a transcription/fuzz guard;
it is neither proof nor independent evidence.
