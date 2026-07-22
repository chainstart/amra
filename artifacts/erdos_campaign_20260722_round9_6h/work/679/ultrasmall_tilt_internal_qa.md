# #679 ultra-small-tilt adversarial QA

Date: 2026-07-22

Verdict: **PASS_COMPLETE_PERIOD_AND_ENERGY / TRANSFER_OPEN**.

1. **Scale:** \(B\to\infty\), \(B=o(L_3)\) implies
   \(\log H=BL_2=o(L_1/L_2)=\log z\), so \(H<z=X^{o(1)}<X\).
   Also \(a=C L_1/(HL)=o(1)\).
2. **Mertens:**
   \(\log\log z=L_2-L_3\) and
   \(\log\log H=L_3+\log B+o(1)\), hence
   \(L=L_2-2L_3-\log B+o(1)\sim L_2\).
3. **Threshold:** uniformly for \(K\le k<K+H\),
   \(r(k)=O_\varepsilon(BL_2/(L_3+\log B))\).  Dividing its contribution by
   \(HaL=C L_1\) gives \(O(B/(L_3+\log B))=o(1)\).
4. **Variance:** the exact local variance numerator is
   \(Ha^2p^{-1}(1-H/p)\).  Its sum is
   \(O(Ha^2L)=O(C^2L_1^2/(HL))\), equal to
   \(\exp\{-(B-2+o(1))L_2\}\).  Denominators are uniformly \(1-o(1)\),
   including primes immediately above \(H\).
5. **Energy probability:** independence gives
   \(\mathbb P_2(C>1)\le\sum_p\beta_p=O(Ha^2L)\); no Markov or geometric-mean
   substitution is used.
6. **Growing moment:** for integer \(q\ge1\) with \(qa=o(1)\),
   \(1-t^q=qa\{1+O(qa)\}\).  The zero exponent and threshold penalty both
   acquire the same factor \(q\), while relative variance becomes
   \(O(q^2\varepsilon_X)\).  Thus the stated two conditions are sufficient.
7. **Critical non-implication:** \(Q/N\) is super-exponential on the
   polylogarithmic scale, and the aggregate Rényi-\(1/2\) conductor mass is
   enormous even though each \(p\beta_p=o(1)\).  Therefore neither
   \(M_2/\mu^2=1+o(1)\) nor superpolynomial complete-period density is an
   interval theorem.

No original-problem closure, interval upper bound, external novelty
certification, or Q2 classification is asserted.
