# Blind reconstruction of the round-3 multiscale countermechanism

## Audit isolation

This reconstruction was written before reading
`evidence/ROUND3_MULTISCALE_CARRY.md`, its verifier, or any author report about
round 3.  Its only mathematical input is the supplied candidate statement:

> The actual zero-seed orbit satisfies `W6(V) >= V` for every `V >= 40`.
> Consequently, for `V=2^m`, `m>=21`, its six-canonical top is greater than
> `ceil(log2 V)+13`, refuting `M776G-02`.

The purpose of the reconstruction is to expose every additional interface
needed for the word "consequently".  In particular, I do not infer the
definition of `W6`, the zero-seed dynamics, or the exact statement of
`M776G-02` from their names.

## Minimal exact interface and reconstruction

Write `T_6(V)` for the six-canonical top.  The claimed implication is valid if
the following two all-parameter facts have been established with compatible
indexing.

1. **Orbit lower bound.**  For the actual (not an enlarged or relaxed)
   zero-seed orbit,
   \[
       W_6(V)\ge V\qquad(V\ge40).
   \]
2. **Canonical counting bound.**  For every integer `t`,
   \[
       T_6(V)\le t\quad\Longrightarrow\quad
       W_6(V)\le {t+1\choose6}.                 \tag{B1}
   \]
   The `+1` says that a state with top at most `t` is encoded by a strictly
   increasing six-subset of the `t+1` indices `0,1,...,t`.  If the actual
   convention uses `1,...,t`, the sharper bound is `binom(t,6)` and the
   argument below still works.  If repetitions are allowed, or if one value
   of `W6` can correspond to several canonical states in the wrong direction,
   (B1) does not follow and the countermechanism is not yet proved.

Now fix `m>=21` and put `V=2^m`.  Then `V>=40` and
`ceil(log2 V)=m`.  If, contrary to the proposed countermechanism,
`T_6(V)<=m+13`, (B1) gives
\[
 W_6(V)\le {m+14\choose6}.                     \tag{B2}
\]
The numerical base case is exact:
\[
 {35\choose6}=1,623,160<2,097,152=2^{21}.       \tag{B3}
\]
Moreover
\[
 {m+15\choose6}
   ={m+15\over m+9}{m+14\choose6}
   <2{m+14\choose6}                             \tag{B4}
\]
for every `m>=21` (indeed for every `m>-3`).  Thus (B3)--(B4) prove by
induction that
\[
       {m+14\choose6}<2^m\qquad(m\ge21).        \tag{B5}
\]
Combining the orbit lower bound, (B2), and (B5) yields the strict
contradiction
\[
       2^m=V\le W_6(V)le {m+14\choose6}<2^m.
\]
Therefore
\[
       T_6(2^m)>m+13
       =\lceil\log_2(2^m)\rceil+13
       \qquad(m\ge21).                          \tag{B6}
\]

This is an infinite, all-parameter counterfamily, not a finite extrapolation.
It refutes `M776G-02` exactly if that mechanism asserts the universal (or
eventual universal) bound
`T_6(V)<=ceil(log2 V)+13` for every actual zero-seed orbit input.  It does not
refute an existential bound, a bound with a larger additive constant, or a
claim restricted away from powers of two.

## Dependencies that must be reconstructed from the author evidence

The supplied statement alone proves (B6) only conditionally on the two
interfaces above.  The post-freeze audit must check the following without
silently changing definitions.

1. **Actual-orbit identity.**  Every recurrence or hockey-stick identity must
   apply to the actual shortened zero-seed orbit, not to a comparison orbit.
2. **Isolated first tax.**  If the proof removes or delays a first tax, the
   monotonicity direction must imply a lower bound for the taxed actual orbit.
   Equality at the first taxed value and the endpoint of its influence must be
   checked; an upper comparison would reverse the needed conclusion.
3. **Twelve summands.**  Any twelve-term hockey-stick calculation must retain
   both endpoints.  The claimed passage to objects named `P12` and `P8` must
   be an equality or a lower bound in the useful direction, not an asymptotic
   mnemonic.
4. **`V>=40` endpoint.**  The derivation of `W6(V)>=V` must include `V=40` and
   every later integer.  A recurrence valid only after the next tax, or a
   statement `W6(V)>V` for `V>40`, is not the same quantified claim.
5. **Canonical injection and off-by-one.**  The precise state set below a top
   `t` must have cardinality at most `binom(t+1,6)`.  The proof must identify
   whether zero is an available index, whether six entries are distinct, and
   which direction the encoding map goes.
6. **Threshold and mechanism match.**  `M776G-02` must use `<=` at
   `ceil(log2 V)+13`; because (B6) is strict, equality conventions matter.
   Powers `V=2^m` remove all ceiling ambiguity.
7. **Induction.**  The base is `m=21`, and the binomial ratio is exactly
   `(m+15)/(m+9)`.  No numerical verification beyond a cutoff is needed once
   (B3)--(B4) are present.

## Blind verdict

The final counting implication is rigorously reconstructed and has no
asymptotic gap.  The candidate should be accepted as an all-parameter kill of
`M776G-02` if and only if the author evidence proves the actual-orbit lower
bound and the canonical counting interface (B1), and the exact stored
statement of `M776G-02` has the universal threshold described above.  Those
are the only unresolved dependencies at the blind stage.
