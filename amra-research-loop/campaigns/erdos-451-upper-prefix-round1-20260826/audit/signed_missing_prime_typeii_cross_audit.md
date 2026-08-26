# Same-model cross-audit of the signed missing-prime Type-II note

## Verdict

**PASS; no mandatory mathematical correction found.**  I independently
reconstructed equations (2)--(15), the optimistic product-level rank ceiling
(17)--(21), the unequal-probability Bonferroni obstruction (24)--(26), and
the exact remainder/precision ledger (27)--(33).  The signs, Mobius factors,
canonical `Q0` phase, character normalization, rank scale, and direction of
the final necessary-precision inequality are consistent.

This is a same-model Codex cross-audit, not an independent human referee
report.  It is read-only with respect to the author evidence.  The audited
source was
`evidence/signed_missing_prime_typeii_audit.md`, SHA-256
`7bbda52025afe98700e1a238859ffb52bf5eeb5ba071bb0f646ae476b32a987e`.

## 1. Local transform, signs, and Mobius weights: (2)--(6)

For one prime, the proposed factor is

```text
I_p-w_p(1-I_p)=(1+w_p)I_p-w_p.
```

It equals `1` on an allowed coordinate and `-w_p` on a violation, so its
product is exactly the signed missing-prime weight.  Choosing the `I_p` term
on `T` and the constant term off `T` gives (3), including the sign
`(-1)^(|S|-|T|)`.

For a squarefree divisor `d` of the allowed support, multiplication by

```text
(-1)^|S| w_S mu(d) product_{p|d}(p-1)/d_p
```

gives, prime by prime, `-w_p` when `p` is missing and `1+w_p` when it is
allowed, because `w_p(p-1)/d_p=(p-1)/k=1+w_p`.  This verifies (4), including
the global sign and the reciprocal `d_p` weight.

The identities

```text
q_p w_p = delta_p,
q_p = 1-delta_p
```

show that multiplying the local signed factor by `q_p` gives
`I_p-delta_p`.  This proves (5), and applying it to (4) gives (6) with
coefficient `(-1)^|S| delta_S mu(d)/delta_d`.  No sign is lost.

## 2. CRT indicator and phase-preserving character formula: (7)--(15)

For every remaining prime, `p>k+A`; hence `Q0=binom(k+A,A)` is a unit modulo
`p`.  Also `1<=j_p<=d_p<p`, so every CRT residue in (8) is a unit modulo
`d`.  Since `p>k`, at most one member of the relevant length-`d_p` interval
can be divisible by `p`.  Therefore each allowed tuple has exactly one
`j_p`, and (9) is a zero-one equality rather than a union-bound overcount.

Multiplicative orthogonality gives

```text
1_{ut=r mod d}=phi(d)^(-1) sum_chi chi(ut) overline(chi(r)).
```

For `r=-Q0^(-1)j`, unit modulus implies

```text
overline(chi(r))=chi(-Q0) overline(chi(j)).
```

CRT factorization therefore gives exactly (10).  Summing independently over
`u,t` produces the complex square `(S_X^P(chi))^2`, not an absolute square;
this verifies both the normalization and the retained absorber phase in
(11).

In (12), a character modulo `d` already vanishes on integers sharing a prime
with `d`; Mobius inversion only over `P/d` supplies the remaining unit sieve.
Because `e|P/d` is coprime to `d`, multiplicativity gives the displayed
`mu(e)chi(e)` inner sum exactly.

For the principal character, the Fourier coefficient is `product d_p`, the
sieved interval sum is `M_X`, and division by `phi(d)` yields `delta_d N`.
Substitution of (6) then proves (14).  For nonempty `S`, the principal part
in (14) is

```text
(-1)^|S| delta_S N sum_{d|P_S} mu(d)=0,
```

so (15) has the correct coefficient, sign, and cancellation.  The formula
does not separate or discard `chi(-Q0)`.

## 3. Optimistic product-level rank ceiling: (17)--(21)

If `d` contains `r` remaining primes, then `d>(k+A)^r`.  Restricting the
hypothetically available divisor level to the deliberately generous
`Q0 X^2` therefore gives (17).  This is an optimistic model ceiling, not a
claim that a Type-II theorem at that level has been proved; the note states
that scope correctly.

The binomial inequality

```text
binom(k+A,A) <= (e(k+A)/A)^A
```

with `A=floor(k/log^2 k)` gives
`log Q0=O(k loglog(k)/log^2(k))=o(k/log k)`.  With
`2 log X=2 gamma k/log k` and `log(k+A)~log k`, (17) becomes

```text
R_II <= (2 gamma+o(1)) k/log^2 k.
```

The PNT gives `m=pi(2k)-pi(k+A)=(1+o(1))k/log k`; the omitted interval
`(k,k+A]` contributes only lower order.  Division proves (21).  Thus the
claimed missing factor `log k` is correct within the stated product-level
model.  Multiplication by `Q0` affects the residue phase but does not enlarge
the character conductor; allowing it in the level only makes this ceiling
more generous.

## 4. Actual unequal probabilities and Bonferroni: (22)--(26)

Expanding `J_p=1-I_p` shows that each `B_T` is an alternating combination of
the allowed counts `N_{P_U}`, `U subseteq T`.  Under the ideal joint law
`N_{P_U}=delta_U N`, this equals `q_T N`, so (22) is exact under its stated
hypothesis.

For an integer `v` and odd `R`, the binomial identity is

```text
sum_{j=0}^R (-1)^j binom(v,j)
  = 1_{v=0}-binom(v-1,R)1_{v>R}.
```

Taking expectation uses
`E binom(V,j)=e_j(q)` and proves (26).  The all-failure event has probability
`product q_i` and contributes `binom(m-1,R) product q_i` to the tail.  When
`R<m`, the binomial factor is at least one; when each `q_i>=1/2`,
`product q_i>=product(1-q_i)`.  Hence `L_R(q)<=0`, including for unequal
probabilities.

For the actual primes, `q_p=k/(p-1)>1/2` follows from `p<2k`, while
`q_p<1` follows from `p>k+A`.  Thus (24) applies to the actual local
probabilities, not just a half-density surrogate.  Since any lower
Bonferroni truncation uses an odd proper rank and `R_II=o(m)`, the stated
sign-dropped closure indeed supplies no positive principal lower bound.

## 5. Exact remainder and required precision: (27)--(33)

Summing the pointwise identity (25) over the product multiset moves the
positive tail to the right and gives (27)--(28) with the displayed plus
sign.  The independent comparator (29) uses the same unequal `q_p` law.

The local relation `delta_p=q_p(d_p/k)` yields

```text
delta=q_* rho.
```

The all-failure event alone gives (30), hence

```text
delta N / T_R^ind <= delta/q_* = rho,
```

which checks the direction in (31).  PNT partial summation gives

```text
-log rho = sum_{p=k+b} log(k/(b-1))
         = (1+o(1))/log k * integral_A^k log(k/b) db
         = (1+o(1)) k/log k.
```

Here the discarded initial interval contributes
`O(A log(k/A))=o(k)`, and replacing `b` by `b-1` is lower order because
`b>A`.  This verifies (32).

If the low-rank principal ledger were exact and
`T_R=(1+epsilon_k)T_R^ind`, resolving the survivor scale requires

```text
|epsilon_k| T_R^ind = o(delta N).
```

Therefore `epsilon_k=o(delta N/T_R^ind)`, which implies the necessary
condition `epsilon_k=o(rho)` by (31).  If the tail exceeds its all-failure
lower bound, the true necessary relative precision is smaller still.  This
checks both the direction and the explicitly necessary-not-sufficient scope
of (33).

## 6. Scope audit

The note proves exact algebraic interfaces and two delimited obstructions; it
does not prove divisor distribution through `Q0 X^2`, a coupled estimate for
the full-rank remainder, a positive survivor count, or Erdős 451.  Its no-go
applies only to:

1. divisor distribution restricted to the stated product-level/rank model;
2. replacement of the accessible low-rank counts by their independent
   principal values; and
3. discarding or separately estimating the positive high-rank Bonferroni
   remainder.

It explicitly leaves phase-preserving, jointly signed control of (15) and
(28) open.  The phase remains `survivor_deepening`, and the evidence does not
claim a main-exponent or theorem closure.  These boundaries are internally
consistent.
