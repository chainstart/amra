# Top-prime cofactor audit for Erdős #317

Let \(I\) be a finite set of primes, put \(P=\prod_{p\in I}p\), and let
\(M\) be coprime to \(P\).  The singleton-prime obstruction from the previous
round asks whether

\[
 M\frac{P}{p}\not\equiv \pm1\pmod p
\]

for at least one top prime \(p\).  A tempting route is to derive a
contradiction from the cofactor equations alone.

## CRT no-go lemma

For every choice of signs \(\varepsilon_p\in\{\pm1\}\), there is a unique
class \(M\pmod P\) satisfying

\[
 M\frac{P}{p}\equiv\varepsilon_p\pmod p
 \qquad(p\in I).
\]

Indeed, \(P/p\) is invertible modulo \(p\), so the equation prescribes

\[
 M\equiv \varepsilon_p(P/p)^{-1}\pmod p.
\]

The Chinese remainder theorem combines these independent prescriptions, and
the resulting \(M\) is automatically nonzero modulo every \(p\).

Consequently, no contradiction can use only the facts that the top primes are
distinct and share one arbitrary lower factor \(M\).  A successful proof must
use the special identity

\[
 M=\prod_{q\le n/2}q^{\lfloor\log_q n\rfloor},
\]

or another property equally specific to the lcm prefix.  Pure two-prime
elimination, cofactor-polynomial geometry, and character multiplication with
free signs all discard this decisive information.

The largest-prime-only variant is also false: there are many finite \(n\) for
which its required coefficient is \(1\).  This does not refute an eventual
version, but it kills induction schemes that assume every event interval is
certified by the current largest prime.

## Surviving statement

The exact route still capable of closing the second public question is:

> For every sufficiently large \(n\), the *specific* lower-prime-power product
> above misses at least one of the CRT sign classes determined by the primes
> in \((n/2,n]\).

No proof of that distribution statement is supplied here.
