# A rigorous large-prime tail lemma

Let

    E(n) = {p prime: p<=n and p does not divide binomial(2n,n)}.

There is an absolute constant `C_0` such that, for every `n>=2`,

    sum_{p in E(n), p>sqrt(2n)} 1/p <= C_0.

Indeed the left side is at most the sum of `1/p` over all primes in
`(sqrt(2n),n]`.  Chebyshev's bound `pi(x)<=C x/log x`, followed by partial
summation, gives uniformly for `x>=2`

    sum_{x<p<=x^2} 1/p
      <= pi(x^2)/x^2 + integral_x^{x^2} pi(t)/t^2 dt
      <= C/log(x^2) + C integral_x^{x^2} dt/(t log t)
      <= C/2log x + C log 2.

Take `x=sqrt(2n)` and enlarge the constant for the finitely many small `n`.

In the same range, the exact carry-free condition is sharper.  If
`q=floor(n/p)`, then `p^2>2n` makes all higher Legendre terms zero and

    p in E(n) iff n-q p < p/2
                  iff n/(q+1/2) < p <= n/q.

This proves mechanism M377-03, but it does not control `p<=sqrt(2n)` and hence
does not close the original problem.
