# Research log (HKT)

## 2026-08-02

- Campaign opened.  Scope firewall fixed: write only inside this directory;
  preserve the distinction between exact finite evidence, computer-assisted
  finite lemmas, and unbounded symbolic arguments.
- Read in full the inherited `README.md`, `CLAIM_LEDGER.md`,
  `RANK6_CARRY_ATTACK.md`, `SYNCHRONIZED_BRIDGE_FREEZE.md`, both verifier
  files and certificate, and the preregistered but unfinished
  `CROSS_AUDIT_776.md`.
- Reconstructed the three borrow states in the synchronized chart from the
  arithmetic relation \(y=x+(\Delta-1)\): double borrow, \(x\)-only borrow,
  and no borrow.  The fourth apparent orientation is unreachable because
  \(\Delta-1>0\).
- Discovery scan through strips \(2\le j\le11\) reproduced the unique delayed
  point \(k=5\) at \(j=10,11\); all other points in those strips seeded by
  rank five.  This is finite evidence only.
- Discovery scans on the omitted half-strip \(k\le0\) found sparse rank-four
  reset chambers but no rank-five failure through \(j=11\).  This motivates
  an all-parameter negative-offset bridge; it does not prove one.
- At much larger sampled strips, several fixed positive offsets require rank
  six or seven, confirming that a rank-five theorem cannot replace the
  adaptive target.  The offset \(k=5\) remains the slow wall in the samples.
- The proposed negative-half rank-five closure was falsified exactly at the
  fixed left offset \(b=5\).  A complete canonical-word induction upgrades
  this from a scan to a second no-fixed-rank theorem and proves an exact
  \(\log_2\log h+O(1)\) adaptive delay on that family.
- Frozen the first rank-five failure within \(b=5\):
  \((j,L,h,b)=(17,14680064,7340032,5)\), \(\gamma_5=-3051947\), while
  \(\gamma_6=36463781155415\).  Two independent local implementations and
  the global ranks \(20,21\) agree; three focused tests pass.
- Generalized the left-wall recurrence to every moving \(b\ge5\) before
  its first cap.  The formal surplus constant is strictly increasing in
  \(b\), so \(b=5\) proves a uniform \(O(\log\log h)\) seed bound on the
  complete negative-side pre-cap chamber.
- Derived the exact first rank-three wall atlas: no crossing, \(y\)-only
  crossing, and synchronized crossing reduce respectively to two
  rank-two \(\Phi\) expressions and one explicit asymmetric term.  The
  sole remaining negative-side quantifier is a cap-recovery lemma.
- Proved that at a first noncanonical row \(p\ge4\), previous-row
  canonicality leaves too little mass for either bottom block to cross a
  second rank-three wall.  The three formulas in the first-wall atlas are
  therefore exhaustive; the remaining issue is their sign, plus the
  separate initial transition \(p=3\).
- New verifier results: the moving recurrence/monotonicity and all three
  one-wall identities pass; the finite falsifier through \(j=12\) checks
  3154 first-cap points, finds five negative first-cap surpluses, and in
  every one the next rank is positive.  This last sentence is finite
  evidence, not the missing universal lemma.
- Closed that cap gate symbolically.  The recurrence gap satisfies
  \((B_r-A_r)^2\ge2A_r\), forcing enough adjacent growth that every first
  cap at \(p\ge4\) is positive in its exhaustive one-wall formula.  At
  \(p=3\), four exact next-row identities prove
  \(\gamma_3<0\Rightarrow\gamma_4>0\).
- The resulting theorem is uniform over every moving \(b\ge5\) in the
  initial double-borrow chamber: a seed occurs by
  \(\log_2\log h+O(1)\).  The new verifier checks 15,854 abstract initial
  recovery states and 3,159 later first caps through \(j=13\); all pass.
- Closed the adjacent initial \(x\)-only borrow chamber.  Its exact
  rank-three formula is positive whenever the borrow depth \(q\ge2\);
  the sole \(q=1\) boundary has an explicit positive rank-four formula.
  The verifier checks 62,153 relaxed states.
- Reduced the remaining initial no-borrow negative chamber to an exact
  dimensionless chart with \(H=\binom b2+1\), \(m=b-1\), and
  \(\gamma_3=U_2(n+m)-U_2(n)-H\).  The only unresolved implication is the
  rank-five no-borrow bridge (2.13) in `NEGATIVE_INITIAL_CHAMBERS.md`.
  Through \(j=10\), 167 points reach its negative antecedent and every
  one has \(\gamma_5>0\), with minimum \(39710\); this is finite evidence.
- Red Team I independently passed the no-borrow reduction after restoring
  its missing Macaulay cap-legality inequalities.  A 10,209,264-point
  relaxed scan found 1,320 antecedents and no \(\gamma_5\le0\), but this
  remains finite evidence.
- Conditional on one rank-two promotion and one rank-three wall, the next
  transition has three exact formulas, checked on all 219 antecedents
  through \(b=250\).  More importantly, for every fixed \(K\ge4\) an
  asymptotic \(q\to\infty\) family enters the open \(\gamma_3,\gamma_4<0\)
  antecedent.  Therefore finite-\(K\) classification is rigorously ruled
  out as a closure strategy; the \(\gamma_5\) bridge remains open.
- Unified both normalizations into the exact rank-five identity (3.6) of
  `ONE_PROMOTION_RANK_FIVE_CHART.md`.  The complete relaxed scan through
  \(b=250\) has 219 points in exactly six combined chambers, with counts
  \(164,3,1,1,31,19\).  The unique reversed second tail is
  \((-+)\to(+-)\); its initial leading gap is two, so the normalized caps
  remain adjacent and its leading correction is zero, not negative.
- Introduced the full-block loss
  \(\Lambda_{j,A}(d)=\binom A{j+1}-U_j(\binom Aj-d)\).  Superadditivity
  and a canonical diagonal shift prove both deficit transport and the
  vertical loss bound.  This retains the base increment that the earlier
  pure-superadditivity route discarded.
- Proved two all-parameter convolution lifts.  Their exact finite bases are
  \(32\le w\le421\) (minimum margin 178) and
  \(32\le r\le277\) (minimum margin 258); explicit convex lower bounds,
  rational anchors, and positive derivative estimates cover every
  \(w\ge422\) and \(r\ge278\).  The focused verifier passes 4/4.
- These lifts close \((++)\to(--)\), \((++)\to(-+)\), and the unique
  reverse-tail chamber \((-+)\to(+-)\) uniformly, conditional on the
  one-promotion/two-one-wall chart.  The exact remaining sign boundary is
  the three rows beginning with \((--)\); promotion and wall exhaustiveness
  also remain open.
- Closed the fourth chamber \((--)\to(-+)\).  For \(q\ge216\), the
  negative raw tail forces \(\alpha<q^2/18\), hence \(K\ge q/3\) and the
  inter-tail separation \(W\ge q^2/18\).  Lemma 4.2 then dominates the
  complete tax.  The exhaustive \(2\le q\le215\) base contains exactly one
  target point, \((q,K,r;b,h)=(35,13,0;48,244)\), with
  \(\gamma_5=4923\).  Only \((--)\to(++)\) and \((--)\to(--)\) remain
  open inside the conditional six-chamber chart.
- The same large-separation argument closes \((--)\to(--)\): its deficit
  gap is directly \(G=U_2(\beta)-U_2(\alpha)-1\), so Lemma 4.1 gives
  \(U_3(G)+G>\tau\) for \(q\ge216\).  The complete smaller base has three
  points, with exact \(\gamma_5\) values 4222, 4599, and 9010 and rigorous
  deficit lower bounds 1236, 1274, and 2548.  The sole remaining conditional
  chamber is \((--)\to(++)\), where the adjacent deficits have orientation
  \(D<E\).
- The last chamber is not positive.  The exact choice \(K=6,r=10,u=15\)
  gives \(\tau=6q+6\), first raw tails \((40-6q,99-6q)\), and stable
  second tails
  \(P=\binom{q-8}{3}+\binom{q-14}{2}+4\),
  \(Q=\binom{q-7}{3}+\binom{q-13}{2}+2934\).
- Imposing the actual dyadic lattice gives
  \(h=224\,2^s\), \(q=(448\,2^s-2)/5\), with exactly the residue class
  \(s\equiv2\pmod4\).  All range, parity, one-promotion, and both one-wall
  conditions hold.  The exact surpluses are
  \(\gamma_3=44-6q\), \(\gamma_4=2906-6q\), and
  \(\gamma_5=4302695-6q\).
- The first rank-five failure on this family is
  \(s=14,q=1468006,h=3670016,b=1468012\), with
  \((\gamma_3,\gamma_4,\gamma_5)=(-8807992,-8805130,-4505341)\).
  Hence (NB)/(2.13) and the fixed rank-five bridge are **refuted**, not
  merely left open.  This is not a counterexample to Erdős #776.
- The family recovers completely at rank six.  The exceptional \(s=14\)
  point has \(\gamma_6=3088969555650\); from \(s=18\) onward the literal
  canonical words give
  \(\gamma_6=9256181220279+104q>0\).  Exact checks at
  \(s=2,6,10,14\) close the finite prefix, so the adaptive rank on this
  family is 4, 5, 5, and then uniformly 6.  Two independent Macaulay
  engines and five focused tests pass.

## 15:35--15:45 blind audit

- The OPG author lane rebuilt the final chamber with a fresh greedy
  combinadic engine and independently recovered every lattice, promotion,
  chamber, cap, threshold, and rank-six formula.  It also reconstructed
  the deficit lemmas, both convolution tails, and all five positive
  chambers, including the complete `q<=215` bases.
- Verdict: both theorem families `PASS` with no repair.  The independent
  verifier passes and the author-focused suite reports 10 passes.  The
  counterfamily refutes only NB/(2.13) and the fixed rank-five bridge;
  Erdős #776 and a uniform adaptive seed theorem remain open.
