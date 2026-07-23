# #679: why the current Lau product-sieve architecture stops at \(\log k\)

Date: 2026-07-23

This is a quantified method audit, not a no-go theorem for all possible
sieves and not a result about the truth of #679.

## 1. The exact resource in Lau's construction

In Lau arXiv:2604.15042v2, the probability weight is a product of
one-dimensional Selberg-type weights for the shifts \(n+k\).  If the level
for shift \(k\) is written

\[
 R_k=X^{\alpha_k},
\]

the expansion requires, up to a fixed safety constant,

\[
 \prod_{k\le K}R_k\le X^\vartheta,
 \qquad\hbox{hence}\qquad
 \sum_{k\le K}\alpha_k\le\vartheta.                \tag{1}
\]

Lau chooses \(\alpha_k\asymp k^{-50}\).  The residual mean number of
prime factors above the sieve level is then of order

\[
 \mu_k\asymp
 \log{\log X\over\log R_k}
 =\log(1/\alpha_k)\asymp\log k,                     \tag{2}
\]

which is exactly the scale of the proved theorem.

## 2. Product-budget obstruction at the #679 scale

Suppose one tries to retain the same architecture while putting the
residual mean below a fixed fraction of the #679 allowance

\[
 r_k=A{\log k\over\log\log k},                     \tag{3}
\]

where \(A>0\) is fixed.  Even the optimistic requirement
\(\mu_k\le c r_k\), with fixed \(0<c<1\), forces by (2)

\[
 \alpha_k\ge e^{-c r_k}
 =\exp\left(-cA{\log k\over\log\log k}\right)
 =k^{-cA/\log\log k}.                              \tag{4}
\]

For \(K/2<k\le K\), the right-hand side is \(K^{-o(1)}\).  Therefore

\[
 \sum_{k\le K}\alpha_k\ge K^{1-o(1)},              \tag{5}
\]

contradicting the fixed budget (1) as \(K\to\infty\).  Thus merely
retuning the individual levels cannot simultaneously move all residual
means to \(O(\log k/\log\log k)\).

The conclusion is stronger than saying that Lau's numerical constants are
large: it is the distinction between a summable allocation
\(\alpha_k=k^{-C}\), which inevitably gives \(\mu_k\asymp\log k\), and the
nonsummable allocation \(\alpha_k=k^{-o(1)}\) required by (3).

## 3. The high-moment/union-bound mismatch

The same stopping point is visible in the moment step.  Bounds of the form

\[
 \mathbb E|Z_k|^s\le (Cs)^s
\]

followed by Markov at threshold \(r_k\) give

\[
 \mathbb P(|Z_k|\ge r_k)\le(Cs/r_k)^s.              \tag{6}
\]

To make the base in (6) smaller than one, one needs
\(s=O(r_k)\); the resulting exponent is only
\(O(r_k)=o(\log k)\), so the probabilities are at best
\(k^{-o(1)}\), not summable.  Taking \(s\asymp\log k\), as required to
obtain Lau's \(k^{-2}\) union-bound tail, makes
\(Cs/r_k\asymp\log\log k>1\).  This is why the exact proof's useful
moment scale and its \(C\log k\) threshold move together.

## 4. Consequence for the next proof route

The audit rules out a direct parameter substitution in the current
product of one-shift sieves.  A successful positive-direction continuation
would need a genuinely joint/block weight that shares sieve resources
between many shifts, or an argument not requiring summably small bad-event
probabilities.  A negative-direction continuation remains the pointwise
short-interval high-\(\omega\) theorem in Lau's Conjecture 8, or an upper
bound for the moving-cutoff signed conductor tail isolated in the companion
note.

Nothing in (1)--(6) rules out those different architectures, and no claim
about the truth of #679 is made.

