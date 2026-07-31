# Synchronized bridge freeze

Frozen: 2026-08-01 01:56 HKT

## Decision

The all-parameter synchronized rank-four/rank-five bridge is closed:

\[
\gamma_4<0\quad\Longrightarrow\quad\gamma_5>0
\]

on the complete admissible lattice (4.55), in fact on the relaxed lattice
where the dyadic condition on (h) is omitted.

The proof is Theorems 4.11, 4.12, and 4.14 of
`RANK6_CARRY_ATTACK.md`.  They exhaust, respectively:

1. both low blocks borrow;
2. only the (x)-block borrows;
3. neither low block borrows.

The last state reduces exactly to

\[
U_3(x+d)-U_3(x)>U_2(n),
\]

then splits by whether the leading rank-three index of (x) is below or
above \(\lfloor q/2\rfloor\).  The infinite ranges are symbolic.  The only
computer-assisted base consists of 36 promotion endpoints
\(16\le q\le51\) and 738 exact direct endpoints \((K,q)\) with
\(16\le q\le91\).  Their minimum margins are 386 and 1150.

## Verification

`verify_rank6_carry.py` guards both finite endpoint sets and the parity
polynomials for the infinite nine-promotion tail.  At freeze time:

```text
4 passed in 16.18s
standalone verifier: PASS
git diff --check: clean
```

## Scope firewall

This closes the synchronized moving-center cap chamber only.  It does not
prove a uniform adaptive seed in the separate pre-cap chamber, does not
treat offsets (k<0), and does not solve Erdős #776.  The fixed-rank gate
remains refuted by the infinite family (b=h+5).
