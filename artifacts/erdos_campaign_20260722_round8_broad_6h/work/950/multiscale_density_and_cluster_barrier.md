# Erdős #950: exact backward-density criterion and a count-only cluster barrier

Date: 2026-07-22 (Asia/Hong_Kong)

Status: strict structural reduction and method barrier.  The original
questions remain open.

## 1. Old-route autopsy

The independently audited round-7 argument correctly proves

\[
 \limsup_{n\to\infty}f(n)
 \ge {28\over15}+{1\over247}
 ={6931\over3705},
 \qquad
 f(n)=\sum_{p<n}{1\over n-p}.                         \tag{1}
\]

Its two ingredients have different roles:

* Guth--Maynard supplies the almost-all background over polynomially many
  denominator scales;
* quantitative \(DHL[50,2]\) supplies one extra prime at distance at most
  247 from the endpoint.

The proof chain is **correct but weak** for the original limsup question.
A fixed bounded-gap theorem can add only a fixed finite amount in this
implementation.  There is no discovered flaw in the intersection or
quantifier argument.  What is missing is growth on an unbounded collection
of reciprocal-distance scales, or a genuinely weighted prime-cluster
theorem.

## 2. Exact summation-by-parts identity

For \(1\le d\le n-2\), put

\[
 a_n(d)=1_{\,n-d\ {\rm is\ prime}},\qquad
 A_n(D)=\sum_{d\le D}a_n(d).
\]

Abel summation gives the exact identity

\[
 \boxed{
 f(n)={A_n(n-2)\over n-2}
      +\sum_{D=1}^{n-3}{A_n(D)\over D(D+1)}.
 }                                                       \tag{2}
\]

Indeed, \(a_n(D)=A_n(D)-A_n(D-1)\), and discrete summation by
parts yields (2) with no asymptotic input.

Formula (2) converts the problem into the integrated density of primes in
intervals immediately to the left of \(n\).  In particular, merely finding
many primes in one interval is not the natural invariant; their distribution
over reciprocal-distance scales is.

## 3. Equivalent dyadic multiscale formulation

For every dyadic denominator shell define

\[
 C_j(n)=\#\{p<n:2^j\le n-p<2^{j+1}\}.
\]

Truncate the final shell at \(n-2\).  Since every denominator in the
\(j\)-th shell lies between \(2^j\) and \(2^{j+1}\),

\[
 {1\over2}\sum_j{C_j(n)\over2^j}
 \le f(n)
 \le \sum_j{C_j(n)\over2^j}.                           \tag{3}
\]

Consequently

\[
 \boxed{
 \limsup_n f(n)=\infty
 \iff
 \limsup_n\sum_j{C_j(n)\over2^j}=\infty.
 }                                                       \tag{4}
\]

Each summand in (4) is the local prime density in a backward dyadic shell,
up to an absolute factor.  Thus an unbounded limsup requires unbounded
*aggregate logarithmic-scale density*.  A fixed number of bounded-gap
primes changes only finitely many initial shells by a bounded amount.

This also gives a precise rare-cluster target.  It would suffice to find a
sequence \(n_\nu\) and shell sets \(J_\nu\) such that

\[
 \sum_{j\in J_\nu}{C_j(n_\nu)\over2^j}\longrightarrow\infty. \tag{5}
\]

Conversely, every proof of the infinite limsup must imply (5), perhaps with
all dyadic shells included.

## 4. Why an unweighted Maynard count cannot by itself give growth

Let

\[
 0\le h_1<h_2<\cdots<h_k\le H
\]

be a fixed admissible tuple.  Suppose a theorem says only that at least
\(m+1\) of the \(k\) coordinates \(u+h_i\) are prime, without controlling
which coordinates they are.  To turn this statement into a uniform lower
bound for \(f(p+1)\), where \(p\) is the largest prime coordinate, one must
take the worst possible \((m+1)\)-subset.

Define its robust reciprocal yield by

\[
 G({\cal H},m)=
 \min_{\substack{S\subseteq\{1,\ldots,k\}\\|S|=m+1}}
 \sum_{\substack{i\in S\\i<j(S)}}
 {1\over h_{j(S)}-h_i+1},
 \quad j(S)=\max S.                                    \tag{6}
\]

There is a universal upper bound

\[
 \boxed{
 G({\cal H},m)
 \le {m\over k-1}\log(H+1).
 }                                                       \tag{7}
\]

To prove it, force the endpoint to be \(h_k\).  The \(k-1\) positive
distances \(h_k-h_i\) are distinct integers, so

\[
 \sum_{i<k}{1\over h_k-h_i+1}
 \le\sum_{d=1}^{H}{1\over d+1}
 \le\log(H+1).
\]

The sum of the \(m\) smallest of these \(k-1\) weights is at most \(m/(k-1)\)
times their total.  Choosing those coordinates together with \(h_k\) proves
(7).

For the usual efficient admissible tuples one may take

\[
 H=O(k\log k).
\]

Maynard's count-only mechanism has \(m\asymp c\log k\) in the relevant
large-\(k\) regime.  Equation (7) then becomes

\[
 G({\cal H},m)\ll{(\log k)^2\over k}\longrightarrow0.   \tag{8}
\]

Thus no argument using only the assertion “at least \(m+1\) prime
coordinates” can guarantee a growing reciprocal contribution, regardless
of how the tuple is arranged.  The actual prime subset might have much
larger weight, but that information is absent from the theorem's output.

This is a proved barrier to the **coordinate-uncontrolled count-only
interface**, not to Maynard's sieve in every possible weighted form.

## 5. A different target: weighted coordinate control

Equations (4) and (7) point to two viable strengthening paradigms.

1. **Endpoint-weighted tuple sieve.**  Prove a positive surplus for a
   functional such as
   
   \[
   \sum_{i<j}{1\over h_j-h_i+1}
   1_{u+h_i\ {\rm prime}}1_{u+h_j\ {\rm prime}},        \tag{9}
   \]
   
   rather than only for the number of prime coordinates.  The sieve weight
   would have to retain coordinate dependence through the final positivity
   argument.

2. **Multiscale endpoint intersection.**  Intersect a quantitative endpoint
   family with prime-density events on a number of dyadic denominator
   shells tending to infinity, while keeping the total exceptional set
   smaller than the endpoint family.  Round 7 achieves this over a
   polynomial band but its total normalised density is asymptotically a
   fixed constant; (5) requires a growing aggregate.

Both targets demand new prime-correlation input.  Standard fixed-\(m\)
bounded gaps, Green--Tao progressions with uncontrolled common difference,
and a bare “\(m\) primes in an interval of length \(H_m\)” statement do not
provide the required reciprocal-position control.

## 6. Strict conclusion

The round-7 constant \(6931/3705\) survives audit.  The new exact identity
(2), dyadic equivalence (4), and robust-yield bound (7) rigorously locate the
failure of the natural rare-cluster continuation: increasing the number of
prime coordinates is insufficient unless their positions, or many
backward scales, are controlled.  No unconditional source presently used in
this campaign supplies that control, so the infinite-limsup part of #950
remains open.  The liminf and pointwise \(o(\log\log n)\) questions are not
changed by this note.
