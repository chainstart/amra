# OPG-1757: effectivity audit of the old high logarithmic range

Date: 2026-08-02  
Audit window: 21:35--21:48 HKT  
Source status: **READ-ONLY TRACE; NO EDIT TO THE AUDITED THEOREMS**

## 1. Conclusion

There is **no genuinely ineffective mathematical step** in the old proof of

```text
d >= 241 log(s).
```

Its threshold was left existential only because one finite constant was
hidden by `O(s^M)`, “absorbed into `C`”, and “for all sufficiently large
`s`”.  Every ingredient of that constant is already present as an exact
finite polynomial in the pinned recurrence source.  The high-range theorem
can therefore be effectivized immediately by a short exact-integer/rational
certificate.  Until that certificate is committed and independently audited,
the already-frozen theorem and its total-threshold firewall should not be
rewritten.

A deliberately crude reconstruction below gives the provisional explicit
bulk threshold

```text
S_high <= 182963662611742278515145357606424176862843
```

(42 decimal digits).  This is vastly smaller than the already certified
117-digit `S_gap`, so after formalizing and auditing this high-range bound the
same 117-digit number would dominate the complete eventual-transport
threshold.  That would still not prove the transports for every finite `s`
or settle OPG-1757.

## 2. Exact source of the old existential threshold

The only non-explicit passage is Section 4 of the old
`THIRD_ACTIVE_TRANSPORT_LOG_BOUNDARY.md`.  For each lower-base monomial it
writes

```text
|term_(a,j)| / retained_p_term
    <= C s^(M+q) ((p-1)/p)^k,
```

then changes `C` to absorb finitely many monomials and concludes that the
right side tends to zero.  The following phrases are the entire source of
ineffectivity:

- `|[beta^j]C_(a,s)|=O(s^M)` without naming its coefficient norm;
- fixed powers `p^i/a^j` “absorbed into C”;
- the finite sum over lower bases also “absorbed into C”;
- “for all sufficiently large s” after the logarithmic decay comparison;
- taking the maximum over the four certificate sums.

There is no use here of compactness, an ineffective Diophantine theorem,
choice of an unspecified prime, or a contradiction subsequence.  The top
bands are already all-parameter theorems (`s>=8` odd and `s>=9` even), and
the passage from the four positive certificate sums to the transports is an
exact inequality.

The exact input remains pinned by SHA-256

```text
a4c8bbf5a261e8d478358fa6ec8136affd0258f324049beec2f61f93b7994125  third_active_transport_recurrence_attack.py
```

## 3. An explicit finite constant

For a lower-base coefficient polynomial

```text
c_(a,j)(s)=sum_m c_(a,j,m) s^m,
```

put

```text
A_(a,j)=sum_m |c_(a,j,m)|.
```

For `s>=1`, `|c_(a,j)(s)|<=A_(a,j)s^M`.  Let `i_*` be the larger of the
low and high retained shifts and let `q` be the full kernel beta degree.  All
retained endpoint coefficients are positive integers, hence at least one.
For any legal numerator and retained denominator index,

```text
C(L,k-j)/C(L,k-i) <= (L+1)^|i-j| <= (2s)^q.
```

Also

```text
a^(k-j)/p^(k-i)
  = (a/p)^k p^i/a^j
  <= ((p-1)/p)^k p^i_*/a^j.
```

Thus a completely explicit common constant for one object is

```text
C_obj = 2^q sum_(a<p,j) A_(a,j) p^i_*/a^j.
```

Extracting the finite polynomials from the pinned source gives:

| object | lower monomials | `(q,M,i_*)` | exact `C_obj` |
|---|---:|---:|---:|
| odd sufficient | 80 | `(19,11,19)` | `32263317969653120815494524068429824 / 48828125` |
| even sufficient | 120 | `(23,13,23)` | `13640357738883598259403345884706295095651860375632 / 2101890673828125` |
| odd page | 68 | `(18,8,18)` | `537834204620338688824696369053696 / 48828125` |
| even page | 105 | `(22,10,22)` | `16379880062727150667612377994429058027750150674 / 129746337890625` |

These constants intentionally discard the actual large retained endpoint
coefficients and use the lower bound one.  They are correspondingly crude,
but every comparison is rational and monotone.

## 4. Exact decay margins and provisional thresholds

Since `k>=d>=241 log(s)`, the base ratio gives

```text
((p-1)/p)^k <= s^(-241 log(p/(p-1))).
```

The old rational logarithm bounds give exact positive margins

```text
p=6: 241*(9/50)-30 = 669/50,
p=7: 241*(11/72)-36 = 59/72.
```

The page budgets are smaller than the grouped budgets 30 and 36, so using
the same two margins is safe.  It is enough to require

```text
C_obj s^(-epsilon_p) < 1.
```

Writing `C_obj=N/D` and `epsilon=u/v`, this is checked without floating
point by the strict integer inequality

```text
D^v s^u > N^v.
```

The least integers obtained from the crude constants above are:

| object | margin | sufficient `s` |
|---|---:|---:|
| odd sufficient | `669/50` | `102` |
| even sufficient | `59/72` | `182963662611742278515145357606424176862843` |
| odd page | `669/50` | `75` |
| even page | `59/72` | `1494048895141509478550315587139453832856` |

Their maximum is the displayed 42-digit candidate `S_high`.  It also
dominates the shifted-positivity starts 8 and 9.  If desired, include the
already used geometry guard `242^2=58564`; the maximum is unchanged.

## 5. Endpoint legality is effective

Choose the low endpoint whenever its binomial index is in `[0,L]`, and the
high endpoint otherwise.  The low choice is legal by definition.  On the
bulk upper bounds, the four high residual indices satisfy

```text
odd sufficient: d-11 <= L-8,
odd page:       d-10 <= L-8,
even sufficient:d-13 <= L-10,
even page:      d-12 <= L-10.
```

At `s>=S_high`, the lower inequalities are automatic from
`d>=241 log(s)`.  Hence no illegal binomial coefficient enters.  The exact
top bands then cover `2s-11,...,2s-4` in the odd branch and
`2s-13,...,2s-4` in the even branch, with no additional eventual constant.

## 6. What is computable and what is genuinely blocked

Already computable:

- every common-base kernel and every lower coefficient polynomial;
- coefficient `l1` norms `A_(a,j)` and the finite monomial counts;
- the four retained endpoint polynomials and their positivity starts;
- binomial-index legality and the adjacent-binomial ratio bound;
- the rational logarithm margins `669/50` and `59/72`;
- exact integer-power thresholds for all four objects;
- the bulk/top splice and the certificate-to-transport implication.

Genuinely ineffective steps: **none identified**.

What is still procedurally missing is not mathematics but certification:
the provisional constants above were reconstructed during this short audit,
not committed as a dedicated source-pinned verifier and not independently
author-swapped.  Therefore they should not silently replace the frozen
ineffectivity statement.

## 7. Shortest repair path

1. Add a standalone `high_range_effective_bound.py` pinned to the old source
   hash; do not import an asymptotic verdict.
2. Extract all lower monomials, compute the four rational `C_obj`, and assert
   their exact numerators and denominators.
3. Verify `D^v s^u>N^v` at each proposed threshold and failure at one less;
   verify all four retained endpoint lower bounds and index interfaces.
4. Add a small test that perturbs the source hash and guards the strict
   inequality direction.
5. Have a non-author reconstruct the constants and the bulk/top integer
   splice.  Only after that audit, replace the old high-range existential
   threshold and update the complete-transport firewall.

This is a short finite task, not a new asymptotic argument.  Once completed,
the existing 117-digit `S_gap` dominates `S_high`, so it is the natural
candidate effective threshold for eventual positivity of both complete
third-active transports.  Universal finite-`s` positivity and the original
OPG-1757 proposition remain **OPEN**.
