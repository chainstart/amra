# Independent red-team review of the critical anisotropic-grid note

Review date: 2026-07-30.

Reviewed file: `CRITICAL_ANISOTROPIC_GRID_BARRIER.md`.

The review did not modify the reviewed file.  It used a separate test
module, `test_independent_geometric_review.py`.

## 1. Verdict

| Claim | Verdict | Qualification |
|---|---|---|
| \(M=m\binom{L+1}{2}\) | Correct for every stated \(L,m\ge1\) and integer \(q\ge2\) | Independently enumerated for \(1\le L\le5\), \(1\le m\le7\), \(2\le q\le7\) |
| Exact energy formula | Correct for the same full range | Same independent enumeration |
| \(M=\Theta(F^{4/3})\), \(\mathcal E=\Theta(F^{8/3})\) | Correct for the critical specialization \(L=t,m=t^2\) | These exponents are not asserted for arbitrary \(L,m\) |
| Off-critical exponent \(3/5+(3/10)|\alpha-2/3|\) | Algebraically correct | Conditional on the two inherited distance inequalities and on \(S=N^{2/5+o(1)},F=N^{3/5+o(1)}\) |
| Theorem 3, \(\cos\theta=3/4\) | Correct | It is a special angular subcase, not forced by the inherited branch |
| Theorem 4, reduced denominator with an odd prime factor | Correct for every such rational cosine | “Fixed” is needed only when turning the exact bound into the displayed asymptotic |
| Unconditional improvement of \(f_3(N)\) | Not proved and not claimed in the note | The result is an interface obstruction plus structured subcase bounds |

## 2. Line count and energy

For a radius pair \(u\le v\),
\[
B_{uv}=2m^2q^{u+v},\qquad
C_{uv}=m^2(q^u-q^v)^2.
\]
Different values of \(u+v\) give different slopes.  If two pairs have the
same \(u+v\), then their products \(q^uq^v\) agree.  Equality of their
radial offsets also gives equality of
\[
(q^u+q^v)^2=(q^u-q^v)^2+4q^{u+v}.
\]
Positivity then determines the unordered pair \(\{q^u,q^v\}\).
Consequently distinct radius pairs with the same slope have distinct
offsets.  Since those offsets are multiples of \(m^2\), while
\[
0\le d^2\le(m-1)^2<m^2,
\]
their intercept blocks are disjoint.  Each of the
\(\binom{L+1}{2}\) radius pairs contributes exactly \(m\) values of
\(d^2\).  This proves
\[
M=m\binom{L+1}{2}
\]
for all stated parameters, including \(L=1\) or \(m=1\).

For \(u=v\), the multiplicities of height differences are
\[
m,\ m-1,\ldots,1,
\]
so the energy is
\[
m^2+\sum_{r=1}^{m-1}r^2.
\]
For \(u<v\), positive height differences have both signs and therefore
multiplicity \(2(m-d)\), giving
\[
m^2+4\sum_{r=1}^{m-1}r^2.
\]
The disjoint-block argument permits these contributions to be added.
Thus the displayed energy formula is exact.

At \(L=t,m=t^2\),
\[
F=Lm=t^3,\quad
M=\frac{t^3(t+1)}2=\Theta(t^4)=\Theta(F^{4/3}),
\]
and the cross-radius part of the energy is
\(\Theta(L^2m^3)=\Theta(t^8)=\Theta(F^{8/3})\).
Both threshold claims are therefore correct.

## 3. Exponent bookkeeping

Assume exactly the inherited synchronized regime used in the note:
\[
N=FS,\qquad
S=N^{2/5+o(1)},\qquad
F=N^{3/5+o(1)}.
\]
Writing
\[
m=F^{\alpha+o(1)},\qquad
L=F^{1-\alpha+o(1)}
\]
gives
\[
M=F^{2-\alpha+o(1)}
 =N^{6/5-(3/5)\alpha+o(1)}.
\]
Hence
\[
\sqrt{SM}
=N^{4/5-(3/10)\alpha-o(1)}
\]
and
\[
S\sqrt m
=N^{2/5+(3/10)\alpha-o(1)}.
\]
The maximum of these two affine exponents is
\[
\frac35+\frac3{10}\left|\alpha-\frac23\right|.
\]
The conversion in the note is exact, including the unique crossing at
\(\alpha=2/3\).

This section is an exponent audit, not a self-contained proof of a new
distance theorem.  The reviewed note imports
\[
D\gg\sqrt{SM},\qquad D\gg S\sqrt m
\]
as “previously available mechanisms”; it does not restate or prove their
hypotheses.  Therefore equations (9)--(12) are valid only inside the
inherited structured branch where those mechanisms apply.  They must not
be quoted as an unconditional estimate for arbitrary \(N\)-point sets.

## 4. The \(2\)-adic argument

For \(\cos\theta=3/4\), the recurrence gives
\[
T_k(3/4)=\frac{a_k}{2^{k+1}},\qquad a_k\ {\rm odd}.
\]
The induction in the note is correct:
\[
a_{k+1}=3a_k-4a_{k-1}
\]
is odd.  Thus
\[
1-T_k(3/4)=\frac{b_k}{2^{k+1}},
\qquad b_k\ {\rm odd}.
\]
After multiplication by \(2m^2\), the reduced denominator for
\(k>2v_2(m)\) is exactly
\[
2^{k-2v_2(m)}.
\]
Adding the integer \(d^2\) preserves this negative \(2\)-adic valuation.
Different \(k\)'s therefore yield disjoint \(m\)-element sets.  Theorem 3
is correct.

### A stronger statement exposed by the review

The same proof works for every reduced
\[
\cos\theta=\frac a{2^e},\qquad a\ {\rm odd},\quad e\ge2.
\]
For all \(k\ge1\),
\[
T_k(a/2^e)
=\frac{c_k}{2^{(e-1)k+1}},
\qquad c_k\ {\rm odd}.
\]
The base cases are immediate.  In the recurrence
\[
T_{k+1}=\frac{a}{2^{e-1}}T_k-T_{k-1},
\]
the numerator at the common denominator is
\[
ac_k-2^{2(e-1)}c_{k-1},
\]
which is odd.  Consequently the common-radius construction satisfies
\[
D\ge
m\max\left\{
0,\,
S-1-\left\lfloor
\frac{2v_2(m)}{e-1}
\right\rfloor
\right\}.
\]
Thus \(3/4\) is a correct representative, but not the full power-of-two
denominator range.

### Genuine resonant boundary

The condition \(e\ge2\) cannot be removed.  For
\[
\cos\theta=\frac12\quad\text{or}\quad-\frac12,
\]
the Chebyshev sequence is periodic and has bounded denominators.  These
are the angles \(\pi/3\) and \(2\pi/3\); the progression itself repeats
after six or three steps.  Likewise \(\cos\theta=0\) is periodic.

These examples refute a blanket claim that every rational cosine has
growing \(2\)-adic denominator.  They do **not** refute Theorem 3, and
they cannot supply \(S\to\infty\) distinct angular positions for a fixed
angle.  Their role is to mark the resonant exception that any general
rational-angle statement must remove.

## 5. Odd-prime denominators

Let \(a/b\) be reduced and let the odd prime \(p\mid b\), with
\(e=v_p(b)\).  In the common denominator \(b^k\), the leading term of
\(T_k(a/b)\) contributes
\[
2^{k-1}a^k,
\]
which is a \(p\)-adic unit.  Every lower-degree term contains a factor
\(b^{2j}\), so it vanishes modulo \(p\).  Therefore the numerator of
\(T_k(a/b)\), and also the numerator of \(1-T_k(a/b)\), is a
\(p\)-adic unit.  It follows that
\[
v_p(1-T_k(a/b))=-ek.
\]
Multiplication by \(2m^2\) changes this to
\[
2v_p(m)-ek,
\]
because \(p\) is odd.  When negative, adding \(d^2\) cannot alter the
valuation.  This proves the exact count in Theorem 4.

The independent test checked every reduced numerator for denominators
up to \(30\), every odd prime divisor of those denominators, and
\(1\le k\le20\).  No exception occurred.

For the asymptotic specialization \(m=S=t^2\), a fixed rational cosine
has only \(O(\log t)\) discarded values of \(k\), so
\[
D\ge t^4-O(t^2\log t)=N^{4/5-o(1)}.
\]
The exact theorem itself does not require the cosine to be fixed.

## 6. Scope and hidden-assumption audit

The parameter-line and energy construction is independent of the angular
pattern.  It therefore proves that line count or parameter energy alone
cannot cross the critical interface.

The positive \(p\)-adic conclusions are different: they assume a common
angular progression with a specified rational cosine.  Nothing in the
line-count construction, and nothing stated from the inherited proof
tree, forces
\[
\cos\theta=3/4
\]
or any fixed rational cosine.  The note explicitly acknowledges this,
and the review confirms that its positive \(N^{4/5-o(1)}\) bounds are
only structured subcase theorems.

In particular:

- the barrier \(M=\Theta(F^{4/3})\) is unconditional within the displayed
  coaxial family;
- the off-critical exponent is conditional bookkeeping for the inherited
  synchronized interface;
- the rational-angle theorems do not close the critical branch;
- no result in the note improves the unconditional exponent for
  \(f_3(N)\).

There is one minor presentation caveat in the finite full-union table:
`exact_affine_union_count` includes the zero distance.  Thus a count used
strictly for nonzero distances should be reduced by one.  This has no
effect on any exponent or on the pressure-test conclusion.

## 7. Review of `RATIONAL_ANGLE_ESCAPE.md`

The later rational-angle note was reviewed separately after the preceding
audit.

### Pure \(2\)-power valuation

The exact statement
\[
T_k(a/2^e)
=A_k/2^{(e-1)k+1},\qquad A_k\ {\rm odd},
\]
for odd \(a\) and \(e\ge2\), is correct.  Its explicit-expansion proof is
also correct.  In particular,
\[
\frac{k}{k-j}\binom{k-j}{j}
=\binom{k-j}{j}+\binom{k-j-1}{j-1}
\]
is integral, and after clearing the asserted denominator every
\(j\ge1\) term is divisible by \(2^{2j(e-1)}\), whereas the leading term
is \(a^k\), which is odd.  No hidden cancellation remains.

The same exact denominator holds for \(1-T_k(a/2^e)\), since its numerator
is even minus odd.  Multiplication by \(2m^2\) leaves reduced denominator
\[
2^{(e-1)k-2v_2(m)}
\]
whenever the exponent is positive.  Thus the usable-layer threshold and
the floor in
\[
m\max\left\{0,S-1-
\left\lfloor\frac{2v_2(m)}{e-1}\right\rfloor\right\}
\]
have no off-by-one error.

### Degenerate denominators

Under the note's assumptions that \(a/b\) is reduced and \(|a|<b\):

- \(b=1\) forces \(a=0\), hence \(\cos\theta=0\);
- \(b=2\) forces \(a=\pm1\), hence
  \(\cos\theta=\pm1/2\).

These are exactly the uncovered rational cases.  Their angular
progressions have periods \(4,6,3\), respectively, so no fixed one is
compatible with arbitrarily long distinct progressions.  The
classification is exhaustive.

### Critical exponent

At \(m=S=t^2\), the rational-angle theorem is applied to one
same-radius slice of the full construction.  It gives
\[
D\ge t^4-O(t^2\log t).
\]
The full construction has \(N=t^5\), not \(t^4\), so this is correctly
reported as
\[
D\ge N^{4/5-o(1)}.
\]
There is no point-count substitution error.  The bound is still only for
a fixed rational nonperiodic angle; the inherited proof tree does not
force one.

### Defect found and corrected in the added regression test

The first reviewed version of `test_verify_rational_angle_escape.py`
contained

```python
assert len(result["two_power_records"]) == 26
```

for `maximum_e=5`.  The verifier correctly produces
\[
2+4+8+16=30
\]
records, one for every positive odd numerator below
\(2^e\), \(e=2,3,4,5\).  The expected value is \(30\), not \(26\).
This was a test expectation error, not a mathematical or verifier error.
It was reported independently and corrected to
`2 + 4 + 8 + 16`; the combined suite now passes.

The verifier checks only positive numerators in its pure \(2\)-power
loop.  This is sufficient as a finite regression sample, not exhaustive
coverage of the signed theorem.  The independent suite checks both signs;
the human parity proof also covers negative odd \(a\) without change.

## 8. Independent verification

Run from the geometric directory:

```bash
PYTHONDONTWRITEBYTECODE=1 pytest -q \
  test_verify_rational_angle_escape.py \
  test_independent_geometric_review.py \
  test_critical_anisotropic_grid.py
```

Current result:

```text
13 passed
```

The independent suite additionally checks:

- all small ratios \(2\le q\le7\), not only the original default \(q=2\);
- all reduced rational cosines with odd-prime denominator at most \(30\);
- every odd numerator over \(2^e\), \(2\le e\le6\);
- the resonant denominator-two exceptions;
- direct common-radius distance unions against the certified
  \(p\)-adic lower bounds.
