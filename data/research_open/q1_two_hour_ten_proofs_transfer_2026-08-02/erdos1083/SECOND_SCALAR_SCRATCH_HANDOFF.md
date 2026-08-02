# Scratch handoff: the current aperiodic escape has no small second scalar row

Date: 2026-08-02

Status: **ISOLATED SCRATCH RESULT; EXACT FOR THE FIXED MASK, FINITE FOR
RATIONAL SCALAR RATIOS; NOT PART OF THE AUTHOR-FROZEN CLAIMS**

Put

\[
 P=1+x+x^3+x^5+x^6,
 \quad Q=1-x^5+x^8+x^{10}-x^{13}+x^{18},
 \quad M=PQ.
\]

This note asks whether the one-row signed escape can be extended by a second
scalar copy of the same five-point set.  It records a no-go in the first exact
ranges; it does not assert an unbounded scalar-copy theorem.

## 1. Exact classification inside the current common mask

Exact factorization over \(\mathbb Q\) gives

\[
 M=P(x)(x^8+1)(x^2-x+1)
 (x^8+x^7-x^5-x^4-x^3+x+1).
\]

The four displayed factors are distinct and irreducible.  Their augmentations
are \(5,2,1,1\).  Hence a normalized integral divisor of \(M\) with
augmentation five is one of the four products obtained by taking \(P\),
excluding \(x^8+1\), and independently taking the two augmentation-one
factors.  Direct expansion shows that only \(P\) is a \(0/1\) mask; each of
the other three has a coefficient \(-1\) or \(2\).

Thus the fixed \(M\) has exactly one normalized five-term mask divisor.  In
particular it contains no nonassociate integer scalar copy \(P(x^r)\),
\(r>1\).  The negative copy is not new because

\[
 x^6P(x^{-1})=P(x).
\]

## 2. Primitive rational-ratio search

A positive rational scalar ratio is normalized as \(r/s\), where
\(r,s\ge1\) and \(\gcd(r,s)=1\).  After passing to the common lattice, the
two scalar masks are \(P(x^r)\) and \(P(x^s)\).  This gcd normalization
removes a common dilation and counts every positive ratio once when
\(r<s\).

For all 3,043 primitive unordered pairs

\[
 1\le r<s\le100,
\]

exact polynomial gcd computation gives

\[
 \gcd(P(x^r),P(x^s))=1.
\]

Consequently, throughout this finite range, if both masks divided one
integral common mask of augmentation \(5C\), their product would divide it.
Evaluation at one would force

\[
 5C=25R(1).
\]

This is impossible for every exact-block value \(1\le C<5\).  For the
specific current mask, direct division over all 358 primitive ordered,
distinct pairs \(1\le r,s\le24\) also finds no instance of
\(P(x^r)\mid M(x^s)\).

This is a bounded gcd computation, not a proof that the two substitutions are
coprime for all rational ratios.

## 3. Same-quotient mask search

Independently, enumerate the 24,463 primitive ordered pairs
\(1\le r,s\le200\) and expand

\[
 P(x^r)Q(x^s).
\]

The unique \(0/1\) product is the original row \((r,s)=(1,1)\).  Thus this
small search finds neither a second positive row with the same quotient nor a
candidate common-mask extension.

## 4. Scope firewall

The factor classification for the one fixed \(M\) is exact.  The rational
ratio gcd and same-\(Q\) searches are finite.  Irrational scalar directions,
larger rational ratios, different quotients, and different common masks are
not classified.  Nothing here proves or refutes Erdős #1083, and this scratch
handoff is not incorporated into the frozen author theorem.

Reproduce with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_second_scalar_scratch.py
```
