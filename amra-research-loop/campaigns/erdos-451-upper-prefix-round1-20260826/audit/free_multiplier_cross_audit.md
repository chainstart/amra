# Cross-audit of the free-multiplier cluster lemma

## Verdict: PASS

This is an independent reconstruction by a separate Codex agent in the same
model/tool ecosystem, not a human peer review.  I did not modify either author
evidence file.  The claims in `free_multiplier_cluster_avoidance.md` and the
interfaces inherited from `absorber_cluster_resonance_audit.md` survive the
checks below, with no theorem-level correction required.

## Independent reconstruction

For rank `r`, choosing the least prime and then `r-1` distinct positive
integer offsets of size at most `B_r` gives

```text
N_k(R) <= k sum_{2<=r<=R} binom(B_r,r-1) <= C_R k.
```

For fixed `R`, `L_S<=B_r^(r(r-1)/2)<k<p` eventually.  Also a prime
`p>k+A` divides neither the numerator `(k+1)...(k+A)` nor `A!`; hence
`gcd(Q_0 L_S,P_S)=1`.  Multiplication by `Q_0 ell_S` is therefore a
permutation modulo `P_S`.

For a possibly nonintegral `R_S=P_S/K_S`, exactly at most
`2 floor(R_S)+1` centered residue classes satisfy `|a|<=R_S`.  Each class
occurs at most `U/P_S+1` times in `1<=u<=U`, proving (8), including the
incomplete endpoint block.  Dividing the union bound by `U` and using

```text
(2 floor(P_S/K_S)+1)/P_S <= 2/k^D + 1/P_S
```

reconstructs (9).  This remains `o(1)` at the boundary `D=2`, since
`N_k(R)=O_R(k)` and `P_S>k^2`.

The endpoint sum is genuinely paid for.  With
`U=C_R(2k)^(R+4)`, the bounds `P_S<=(2k)^R` and `N_k(R)<=C_R k` make it
`o_R(1)`.  Separately, the union bound over remaining primes gives at most
`O(U/log k)` multipliers divisible by one of them.  Thus one multiplier is
simultaneously cluster-good and coprime to every remaining prime; in
particular a remaining prime cannot hide as a factor of `u`.

The diagonal choice is valid: monotonicity and finiteness of `C_R` and
`L_R^*` for each fixed `R` permit `R_0(k)->infinity` while imposing all three
conditions (14).  Then `C_{R_0}<=k^(1/4)` makes the `D=2` complete-period
loss `O(k^(-3/4))`, four extra powers in `U` absorb the endpoint sum, and
`R_0 log(2k)=o(k)` gives `log U=o(k)`.  Consequently
`log(Q_0u)=o(k)`.

For `p=k+b>k+A`, the exact forbidden/allowed-for-451 residue set is

```text
t mod p in {0,-q^(-1),...,-(b-1)q^(-1)}.
```

It follows by multiplying `{0,k+1,...,p-1}` by `q^(-1)`.  Moreover
`Q_0=(-1)^A binom(b-1,A) mod p`, so (18) is exact after multiplication by
`u`.  Coprimality makes every inverse used here legitimate.

Finally, Fourier normalization is consistent.  Under
`g(t)=f(qt-(k+1))`, the canonical frequency is transported to
`a=<q ell_S>_{P_S}`.  A normalized coefficient has magnitude at most `P_S`,
and the nonzero-frequency interval kernel is at most
`P_S/(2|a|)` up to the stated endpoint convention.  The lower bound
`|a|>P_S/[k^D(log k)^(C|S|)]` therefore bounds one named character, and its
conjugate, by

```text
O(P_S k^D (log k)^(C|S|))
 = O(2^|S| k^(|S|+D) (log k)^(C|S|)).
```

This is only a single-character statement; it does not imply a full Fourier
or dyadic-block bound, exactly as the author states.

## Nonblocking clarifications

- State explicitly that each `B_r` may be replaced by a nonnegative integer
  ceiling before writing `binom(B_r,r-1)`.
- In (8), “the incomplete endpoint block” would be slightly more literal
  than “the two incomplete endpoint blocks”; the displayed bound itself is
  correct.

Neither point changes the lemma, its constants, or its scope.  There are no
mandatory mathematical fixes.
