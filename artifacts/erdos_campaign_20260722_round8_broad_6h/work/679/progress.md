# #679 round-8 progress

- Budget accounting: 3,550 seconds.
- Old route: CRT factorisation and the raw-\(L^2\) failure are correct.
- New strict theorem 1: for the first prime-prefix modulus \(Q>N\), with
  \(H=(\log X)^{o(1)}\), conductor truncation proves uniformly
  \(\sum_IW=N\mu(1+o(1))\).  Internal adversarial QA passes.
- New strict theorem 2: the large-band parameters
  \(H=(\log X/\log_2X)^2\), \(z=X^{1/\log_2X}\), and nonsaddle tilt
  \(1-t=C/\sqrt H\) give complete-period good-class density
  \(X^{-C+o(1)}\).  For fixed \(C>1\), this zero mode would close the
  negative direction if the interval mean transferred.
- New failure boundary: dyadic conductor/Farey large sieve handles typical
  conductors, but energy-only Cauchy fails already on the full-conductor
  layer because
  \(\log(QP_Q)=(2\log C+o(1))\pi(z)>0\).  Exact ANOVA recombination gives
  \(F_S(n)=\prod_{p\notin S}m_p\prod_{p\in S}(W_p(n)-m_p)\), so the actual
  full-conductor layer is at most \(Na^M\), astronomically small: the Cauchy
  blow-up is a method loss, not a counterexample.
- Hybrid cutoff audit: every \(c(S)\le X^\kappa\), \(\kappa<2/3\), is
  controlled (in particular all \(|S|\le\kappa\log_2X\)).  Absolute summation
  above this conductor cutoff loses binomial entropy, while Bonferroni needs
  degree \(\asymp\log X\).
  A signed high-ANOVA tail \(o(N\mu)\) would give the full interval
  asymptotic.  For closing the negative direction it is enough, thanks to
  the fixed \(C-1\) exponent margin, to prove the weaker one-sided bound
  \(\sum_I\sum_{c(S)>X^\kappa}F_S\le N\mu X^{o(1)}\).  Local
  Dirichlet-kernel phase or an alternating sieve is essential.
- Strict verdict: major_route_advance_zero_mode_complete_transfer_open;
  original open; no independent external QA or novelty certification; Q2
  gate not met.
