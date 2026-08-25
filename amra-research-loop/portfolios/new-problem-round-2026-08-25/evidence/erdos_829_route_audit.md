# Erdős #829 — divisor/discriminant route audit

## Exact reduction

Let \(x,y\) be positive integers with \(x\le y\), and put

\[
s=x+y,\qquad t=y-x,\qquad n=x^3+y^3.
\]

Then \(0\le t<s\), \(s\equiv t\pmod 2\), and

\[
4n=s(s^2+3t^2). \tag{1}
\]

Conversely, if positive \(s\), nonnegative \(t<s\), and \(s\equiv t\pmod2\)
satisfy (1), then

\[
x=(s-t)/2,\qquad y=(s+t)/2
\]

are positive integers and \(x^3+y^3=n\). Thus unordered positive
representations are in bijection with divisors \(s\mid4n\) for which

\[
\frac{4n/s-s^2}{3}
\]

is a square \(t^2\) satisfying the parity and range conditions. Ordered
representations are obtained by the two signs of \(t\), except when \(t=0\).

This proves the proposed divisor/discriminant certificate exactly; the finite
script is only a replay of this bijection, not its proof.

## Primitive factor split

Write \(q=x^2-xy+y^2\), so \(n=sq\). If \(\gcd(x,y)=1\), then

\[
\gcd(s,q)\mid 3. \tag{2}
\]

Indeed, modulo a prime \(p\mid s\), \(y\equiv-x\), hence
\(q\equiv3x^2\pmod p\); also \(\gcd(x,s)=1\). If \(3\mid s\), then
\(q=s^2-3xy\) has exactly one factor of \(3\), because
\(q/3\equiv-xy\not\equiv0\pmod3\). This also controls the 3-adic exponent.

Moreover \(s^2/4\le q<s^2\), so every representation has

\[
n^{1/3}<s\le(4n)^{1/3}. \tag{3}
\]

Equations (2) and (3) show what an Eisenstein or rational factor split must
actually exploit: apart from \(3\), each prime power of a primitive \(n\) is
assigned wholly to \(s\) or to \(q\), and only assignments in a fixed
multiplicative interval can survive.

## Kill result for the naive local-choice bound

Ignoring the square condition in (1) leaves a bound of unitary-divisor type,
at worst a constant times \(2^{\omega(n)}\) for each primitive part (and a sum
over cube divisors for nonprimitive representations). This does **not** imply a
fixed power of \(\log n\): for the primorial \(P_m\), \(2^{\omega(P_m)}=2^m\),
whereas \((\log P_m)^C=\exp(O_C(\log m))\) for every fixed \(C\).

Therefore independent Eisenstein prime assignments, by themselves, fail the
round's first kill test. Any viable continuation must prove a global coupling
that uses the square condition in (1), rather than merely count factor
assignments. The natural next object is the number of *unitary* divisors in
the interval (3) for which the residual discriminant is three times a square.

## Exact finite replay

`work/analyze_829_representations.py` exhaustively enumerated every positive
representation for \(n\le1200^3=1,728,000,000\). It found 633,771 represented
integers, 2,037 with at least two unordered representations, and maximum
unordered multiplicity 3. For every reported maximal example it independently
recovered exactly the same pairs from (1). These observations do not prove a
universal multiplicity bound.

Decision: `route_killed_as_stated`; retain the discriminant-square coupling as
the only admissible successor route.
