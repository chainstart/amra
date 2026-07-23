# Erdős #679: round-12 target audit

Date: 2026-07-23 (Asia/Hong_Kong)

## Exact target used in this folder

Write \(\omega(m)\) for the number of distinct prime divisors of the
positive integer \(m\).  The first question on the current official page is
formalised here as

\[
 \forall\varepsilon>0\;\exists K_\varepsilon\in\mathbb N\;
 \forall N_0\in\mathbb N\;\exists n>N_0\;\forall k\in\mathbb N,
 \quad K_\varepsilon\le k<n\Longrightarrow
 \omega(n-k)<(1+\varepsilon){\log k\over\log\log k}.       \tag{T}
\]

The harmless convention \(K_\varepsilon\ge3\) is imposed so that the
displayed logarithms are defined and positive.  Thus:

* \(K_\varepsilon\) is fixed after \(\varepsilon\), before \(N_0,n,k\);
* the same \(K_\varepsilon\) must work for an unbounded sequence of \(n\);
* for each selected \(n\), the inequality is simultaneous for every integer
  \(k\) in the entire interval \([K_\varepsilon,n)\);
* the inequality is strict and concerns \(\omega\), not \(\Omega\).

An unconditional proof of (T), or an unconditional proof of its logical
negation, is the only event counted as closure in this round.  In
particular, a sufficient condition, an almost-all-start statement, a
conditional theorem, or a finite computation is not a closure.

For reference, the negation of (T) is

\[
 \exists\varepsilon_0>0\;\forall K\in\mathbb N\;\exists N_0\in\mathbb N\;
 \forall n>N_0\;\exists k\in\mathbb N,
 \quad K\le k<n,
 \quad\omega(n-k)\ge(1+\varepsilon_0)
              {\log k\over\log\log k}.             \tag{not-T}
\]

The order \(\forall K\,\exists N_0\,\forall n\,\exists k\) will be checked
against every proposed negative argument.

## Questions deliberately excluded from the closure count

The official page separately asks whether the stronger bound

\[
 \omega(n-k)<{\log k\over\log\log k}+O(1)
\]

is false.  The primorial argument recorded by DottedCalculator proves a
stronger pointwise obstruction and the official page records this second
question as disproved.  That result is not the first question (T), since its
relative excess over \(\log k/\log\log k\) tends to zero and therefore does
not supply a fixed \(\varepsilon_0\) in (not-T).

The 1979 source states a conjunction involving both \(\omega\) and
\(\Omega\).  The present website's first displayed question and this folder
concern only its \(\omega\) component.  Results for \(\Omega\), including
Lau's \(C\log k\) theorem, are partial comparisons only.

## Primary-source boundary

1. P. Erdős, *Some unconventional problems in number theory*, Acta Math.
   Acad. Sci. Hungar. 33 (1979), 71--80, p. 72, formula (3), states that for
   every \(\varepsilon>0\) there should be infinitely many \(n\) for which
   the two displayed bounds hold for every
   \(k_0(\varepsilon)<k<n\).  Formula (4) is the additive-constant
   strengthening.
2. The official page <https://www.erdosproblems.com/679>, checked
   2026-07-23, labels the first question OPEN and explicitly says that it
   cannot be resolved by a finite computation.
3. C. F. Lau, arXiv:2604.15042v2 (2026-06-24), Theorem 1.3, proves only
   \(\omega(n-k)\le\Omega(n-k)\le C\log k\) for infinitely many \(n\) and
   all \(1<k<n\).  Its Section 7 falsity theorem assumes Conjecture 8; it is
   not an unconditional disproof of (T).
4. Tao--Teräväinen, arXiv:2512.01739v2 (2026-04-25), proves the weaker
   \(O(k)\) Erdős--Straus problem and explicitly places #679 beyond that
   method.

## Round-11 state inherited, not re-claimed

Round 11 rigorously removed all primitive ANOVA conductors
\(c(T)\le\exp((1-\eta)HL)\) at the prescribed physical start, for each
fixed \(0<\eta<1\), where \(H=(\log X)^2\) and
\(L=\sum_{H<p\le z}1/p\sim\log_2X\).  A candidate then forces a positive
signed tail of size \(\exp(-o(HL))\) above that cutoff.  No upper bound for
that signed tail was proved.  The other exact interface is Lau's unproved
fixed-power short-interval density conjecture.  Both are reductions, not
answers to (T).

