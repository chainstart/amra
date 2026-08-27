# Erdős #317: singleton-prime obstruction and finite certificate

Let \(L_n=\operatorname{lcm}(1,\ldots,n)\).  The equality case in the second
question is

\[
 \sum_{k=1}^n\delta_k\frac{L_n}{k}=\pm1,
 \qquad \delta_k\in\{-1,0,1\}.
\]

Changing all signs reduces the audit to the right-hand side \(+1\).

## Lemma

Let \(p\) be prime with \(n/2<p\le n\).  If

\[
 (L_n/p)^{-1}\pmod p\notin\{1,-1\},
\]

then the displayed equation has no solution.

Indeed, \(p\) divides \(L_n/k\) for every \(k\ne p\): no other integer at
most \(n\) is divisible by \(p\).  Reduction modulo \(p\) leaves

\[
 \delta_p(L_n/p)\equiv1\pmod p.
\]

Thus \(\delta_p\) would have to equal the listed inverse residue, whereas a
nonzero \(\delta_p\) can have only residue \(1\) or \(-1\).  This is a
contradiction.

## Certified finite range

`work/certify_317_singleton_prime.py` computes \(L_n\) exactly by multiplying
only at prime powers.  For every \(5\le n\le1{,}000{,}000\), it finds a prime
\(p\in(n/2,n]\) satisfying the lemma.  The compact JSON records complete
coverage, no uncovered \(n\), a digest of the compressed witness intervals,
and the guarded cgroup.  The certificate can be regenerated and checked from
the script without trusting a floating-point calculation.

An independent meet-in-the-middle enumeration in
`work/search_317_signed_lcm.py` checks all ternary coefficient vectors through
\(n=30\).  It finds equality at \(n=2,3,4\), and none for \(5\le n\le30\), in
agreement with the modular certificates.

## Exact remaining gap

The lemma is only sufficient.  Closing the public question by this route
would require proving that, for every sufficiently large \(n\), at least one
prime \(p\in(n/2,n]\) has

\[
 L_n/p\not\equiv\pm1\pmod p.
\]

Bertrand's postulate supplies a prime in the interval but does not control
this residue.  The computation through \(10^6\) is finite evidence for this
new bridge, not a proof of its universal quantifier.
