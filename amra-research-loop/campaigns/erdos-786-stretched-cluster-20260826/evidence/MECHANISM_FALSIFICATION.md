# Mechanism falsification

## Proved supporting mechanisms

### Entropy code M786S-01

For
\(r=\lceil\log_2(q+2)\rceil+1\), an \(r\)-element set has
\(2^{r-1}-1\ge q+1\) unordered nontrivial bipartitions.  Distinct unordered
bipartitions have no repeated shore subset, so all factors assigned at a
fixed point are distinct.  The two factors of any one partition have
disjoint nonempty private-prime supports and fixed product.

### Padding flow M786S-10

On one projective line put \(m=q+1\).  The ceiling discrepancy \(C_L\) of
the raw path values satisfies \(-m<C_L<m+1\).  With the shared point values
padded two powers below \(2^K\), the required even-shore correction is

\[
 \Delta_L=K-C_L+2m.
\]

For \(q>K\), this gives \(0<\Delta_L<K+3m<4(m+1)\).  Distributing
\(\Delta_L\) integer decrements over the \(m+1\) private vertices therefore
uses at most four decrements per vertex.  Once every raw odd part has
\(o(K)\) bits, all exponents stay nonnegative and every final private value
lies in \((2^K/32,2^K]\).

## Killed mechanisms

1. **M786S-02, two-prime exponent code.**  Complementary exponent pairs
   \((e,M-e)\) provide at most \(M+1\) fixed-product codes.  Encoding
   \(q+1\) lines forces \(M\ge q\).  Since point-private primes at
   \(q^2+q+1\) points have logarithmic size at least of order \(\log q\),
   the point product costs at least order \(q\log q\) bits.  This cannot
   reach the subset code's stretched-exponential range.

2. **M786S-03, reused point blocks.**  Every two points of a projective
   plane lie on a common line.  Reusing their prime blocks makes a valuation
   occur on multiple path edges of that line, so the private-edge equations
   no longer force the alternating circuit.  It can also identify the shared
   point integers.  The exact minimality and one-point-intersection contract
   fails.

3. **M786S-05, affine plane.**  A parallel class consists of pairwise
   disjoint lines, hence the corresponding arithmetic supports have matching
   number at least the size of the class.  Restricting to a pencil restores
   pairwise intersection but gives a common point and transversal number one.

4. **M786S-06, a larger symmetric design.**  The frozen target requires
   every two blocks to meet in exactly one point.  For a symmetric
   \(2\)-design this is \(\lambda=1\), and the standard parameter equations
   give the projective-plane parameter set.  Allowing \(\lambda>1\) changes
   the exact intersection theorem rather than improving the selected host.

5. **M786S-08, smooth composite compression.**  Pairwise-coprime labels
   that remain globally separating require at least one distinct prime
   divisor per label.  Replacing such a label by its private prime never
   increases the maximum label, so composite labels cannot improve the
   prime-coordinate or bit budget.

6. **M786S-09, polynomial-size \(q\).**  Under the surviving subset code a
   point odd part has bit cost of order \((\log q)^2\).  If
   \(q=N^\delta=2^{\delta K}\), this is order \(K^2\), so the raw point
   value already exceeds the \(K\)-bit host before padding.

7. **M786S-11, several padding primes.**  Padding can only multiply a raw
   odd part by nonnegative prime powers.  It cannot place a raw point product
   exceeding \(2^K\) back into the host.  The active bottleneck is the odd
   coding cost, not the one-dimensional discrepancy correction.

8. **M786S-13, disjoint cluster packing.**  A union of \(t\) vertex-disjoint
   clusters contains \(t\) disjoint supports, so its matching number is at
   least \(t\), and supports from different clusters do not meet in one
   point.  It does not satisfy the frozen single-cluster theorem.

The retained mechanisms are M786S-04, M786S-07, and M786S-12.  They cover,
respectively, the arithmetic incidence construction, its quantitative prime
and bit budget, and the all-cutoff transfer.
