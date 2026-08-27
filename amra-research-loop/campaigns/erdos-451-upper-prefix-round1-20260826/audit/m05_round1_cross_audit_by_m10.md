# Independent cross-audit of U451-M05 round 1 by the M10 line

## Verdict

**PASS WITH TWO SCOPE/PRECISION CORRECTIONS.**  The determinant, quantitative
Blichfeldt count, integral reconstruction and injection, one-block `6^q`
theorem, orientable-fraction upper bound, and thin-basis determinant ledger
all reconstruct.  The two corrections below do not change any application
or exponent, but the first is a required theorem hypothesis.

This is a same-campaign, different-mechanism cross-audit.  I reconstructed
the arguments from the frozen M05 note and did not inherit an earlier audit,
Lean result, or author calculation.  I did not modify the M05 note, script,
replay, or hash file.

Frozen objects read:

```text
baseline commit: 56fc96c
m05_special_orthant_lattice_round1.md:
  d79110a38dbbfc839c3ab2f94e04c6e16408d71e4e29deb19a317ea0ff2a50e7
m05_orthant_lattice_round1.py:
  5664d07baa111181aee6a0a621dac753d35304c307d16c18b4a17b4bf0a36163
m05_orthant_lattice_round1_replay.txt:
  f4f7ad8b73565042399163a23d83ea1cb789eae890d5cde87c9fe5d3b89d7921
authoritative replay unit:
  openmath-task-20260826-225805-327720.scope, exit 0,
  maximum RSS 17920 KiB, swaps 0
```

## Mandatory corrections

1. **Theorem 2.3 must state that `H` is a nonnegative integer**, or replace
   every occurrence by `floor(H)` with the corresponding hypothesis.  Lemma
   2.2 uses that the endpoints `+-h=+-(H+1/2)` are half-integers.  This is
   automatic in the only displayed application, where `H` is a ceiling, but
   it is not explicit in the theorem as written.  With `H in Z_{>=0}` the
   proof passes verbatim.
2. In the mixed-sign paragraph after (16), the negative coordinate `j`
   should be chosen to **minimize** `s_j`, or the proof should use (14)
   directly: a positive coordinate gives lower endpoint zero while
   `min_i s_i<0`.  An arbitrary negative coordinate need not be the `j`
   specified in (15).  The conclusion that all mixed patterns are
   nonorientable is correct.

## 1. Lattice and zonotope reconstruction: PASS

The vectors `v_0=(1,-1,...,-1)` and `v_i=p_i e_i` generate every lattice
point after subtracting `n v_0`, and their determinant is `P`.  The coordinate
ray lattice has determinant `P^2`, hence index `P`; its half-open ray box has
the stated `P` CRT points and exactly `product d_i` actual points.

For the quotient zonotope, the `m+1` half-generators are
`h(1/p_i)_i` and `(b_i/p_i)e_i`.  Omitting the diagonal generator contributes
`D_b`; omitting coordinate generator `i` contributes `hD_b/b_i`.  The
zonotope formula therefore gives exactly

```text
vol(K_H)=2^m D_b(1+h S_b).
```

The zero-frequency dual claim also reconstructs: multiplying
`sum z_i/p_i=0` by `P` and reducing modulo `p_i` forces `p_i|z_i`; a nonzero
integer vector with zero sum has at least two active coordinates.

## 2. Integral reconstruction and quantitative Blichfeldt: PASS after H scope

For integer `H`, every interval endpoint in Lemma 2.2 is a half-integer.  A
nonempty intersection of the open intervals has positive integral length
and contains an integer `n`.  Strict membership gives
`|n|<=H` and `|p_i a_i-n|<=d_i-1`.  If `n=0`, the latter and
`d_i-1<p_i` force every `a_i=0`.

With `E=K_H/2`, the hypothesis in (6) makes `vol(E)>4k+1`.  Coset averaging
therefore gives at least `4k+2` points in one translate of `Z^m`; differences
from one base point give `4k+1` distinct nonzero integer points in
`E-E=K_H`.

The point-to-`n` map is injective.  For fixed `n`, each `a_i` is unique because
the interval `|p_i a_i-n|<=d_i-1` has diameter below `p_i`; explicitly
`d_i-1<p_i/2` follows from `p_i<2k`.  Only `4k` nonzero integers have
`|n|<=2k`, so one difference has `|n|>2k`, and global negation makes it
positive.

The density conversion is also sound:

```text
D/D_b <= exp(sum 1/d_i) <= e k,        S_b >= m/k.
```

Thus the integer choice `H=ceil(6 e k^3/(mD))` makes the left side of (6) at
least `6k>4k+1`.  Its logarithmic ledger is
`log H=(log 4+o(1))k/log k` under PNT.

## 3. Orientation and signed-box count: PASS with the wording correction

The common shift gives the exact interval condition

```text
max_i(s_i-d_i+1) <= t <= min_i s_i,
```

and hence (14)--(15).  The mixed extreme sign patterns fail this condition
as described in correction 2.

For the full signed box, an orientable vector has a representation
`s_i=q_i+t`, `0<=q_i<d_i`, with `|t|<2k`.  Counting such pairs gives the valid
upper bound `(4k+1) product d_i`.  Moreover

```text
product d_i/(2d_i-1)
 = 2^{-m} product(1+1/(2d_i-1)) <= e k 2^{-m},
```

because the distinct widths lie in `[1,k-1]`.  Hence the stated orientable
fraction upper bound is correct.  It is properly scoped as a global count,
not a distribution theorem for the short Blichfeldt difference set.

## 4. Single dyadic block and the constant 6: PASS

For `w=floor((Delta-1)/2)` and `b=w+1/2`, one has `b<=Delta/2`, so
`q/b>=2q/Delta`.  The chosen ceiling `H` gives

```text
delta_b(H+1/2)(q/b) >= 8k > 4k+2w+1.
```

The same difference-count argument therefore yields
`2k+w<n<=H`, `|s_i|<=w` after global negation.  Shifting by
`t=min_i s_i` leaves `n+t>2k` and puts every offset in
`[0,2w] subset [0,d_i-1]`.

The local ratio is at most six.  For even `Delta`, the worst case is exactly
`Delta=2,d_i=3,b=1/2`; for odd `Delta`, it is below four.  Hence
`delta_b^{-1}<=6^q delta_B^{-1}`.  If
`A=(k^2/q)6^q delta_B^{-1}`, then `A>=6k`, while
`H+w<4A+1+k/2<6A`; equation (20) follows.  The note correctly claims only a
single-block successor, not a maximum-gap theorem or multiblock merger.

## 5. Thin-basis obstruction: PASS

Let `r=m+1`.  Rounding `r` coefficients independently produces coordinate
error at most one half of the sum of the corresponding basis-row absolute
values, so (21) is a sufficient thinness condition.

Every independent integral `W subset Lambda` spans a sublattice and has
`|det W|>=det Lambda=P`.  After row normalization, Hadamard gives

```text
P <= |det W| < (H-2k) product_i d_i / r^(r/2),
```

and therefore `H-2k>r^(r/2)/D`.  Since
`m=(1+o(1))k/log k`, `(r/2)log r=(1/2+o(1))k`, while
`log D^{-1}=o(k)`, the exponent `(1/2+o(1))k` is correct.  The note also
correctly limits this obstruction to full-basis independent rounding; it is
not advertised as a no-go for every lattice or cone method.

## Final scope

After explicitly adding `H in Z_{>=0}` and tightening the mixed-sign sentence,
the M05 round-1 mathematical claims pass this audit.  They establish a
density-scale symmetric successor and a `6^q` actual successor for one
dyadic width block.  They do not establish the location/orientation
distribution needed for the full positive orthant, a block maximum-gap
bound, or Erdős 451.
