# Claim ledger

| Claim | Status | Evidence / dependency |
|---|---|---|
| The global #776 gate reduces to the displayed all-strip rank-six inequality | **INHERITED PROVED** | Breakthrough campaign, Theorem 6.3 and Proposition 6.4 |
| The rank-six target is equivalent by Macaulay adjunction to a lower-shadow carry inequality | **PROVED** | `RANK6_CARRY_ATTACK.md`, Lemma 2.1 |
| At \(L=114688,b=57349\), \(\gamma _5=-46063\) and the adjoint carry exceeds reserve by 84 | **PROVED / EXACT COUNTEREXAMPLE** | Two exact implementations plus explicit canonical certificate |
| On \(b=L/2+5\), \(\gamma _5=125969-3L/2\) | **PROVED** | Theorem 3.1; explicit Pascal normalization |
| \(\gamma _5\ge0\) for every dyadic strip | **REFUTED** | Infinite counterfamily for every \(j\ge10\) |
| No fixed post-carry rank \(p\) supplies a uniform diagonal seed | **PROVED** | Theorem 4.1; paired canonical words and constant recurrences |
| Along the counterfamily, any successful seed rank satisfies \(p\ge\log_2\log h-O(1)=\log_2j-O(1)\) | **PROVED** | Theorem 4.2; double-exponential bounds for \(B_p\) |
| On \(b=h+5\), the exact first successful rank is \(p_{\rm cand}(h)=\log_2\log h+O(1)=\log_2j+O(1)\) for sufficiently large \(h\) | **PROVED** | Theorem 4.3; includes the cap-overflow chamber |
| The same doubly logarithmic adaptive bound works uniformly in \(b\) | **OPEN** | Theorem 4.3 handles only the explicit counterfamily |
| Among every fixed central offset \(b=h+k\) with \(k\ge5\), \(k=5\) has the slowest paired-tail constants | **PROVED** | Proposition 4.4; symbolic-\(k\) recurrence and monotonicity |
| The exceptional offsets \(b=h+k\), \(1\le k\le4\), seed at rank four except \(k=4\), which seeds at rank five | **PROVED** | Proposition 4.5; explicit canonical words and positive closed forms |
| Every synchronized moving-offset cap chamber reduces exactly to a rank-two triangular carry, affine in the within-row remainder | **PROVED** | Lemma 4.6 and Proposition 4.7; exact endpoint principle |
| For \(5\le k\le h-2\), the rank-four central cap atlas has two paired chambers and exactly one asymmetric integer; the asymmetric chamber is always positive | **PROVED** | Corollary 4.8; \(g(k)=f(k+1)\), dyadic modulo-8 exclusion, exact Macaulay normalization |
| The synchronized rank-four chamber \(\Phi_{3h+k-2}(f(k)-3h,4k-6)\) is always followed by a rank-five seed when its rank-four reset is negative | **PROVED** | Theorems 4.11, 4.12, and 4.14 exhaust double-borrow, asymmetric, and no-borrow states |
| The synchronized rank-four/rank-five bridge is an exact two-variable lattice problem with \(h\) eliminated | **PROVED REDUCTION** | Corollary 4.9, equations (4.54) and (4.57) |
| Any negative point in the synchronized chart has triangular leading index \(q<\lceil(4k-6)/3\rceil\) | **PROVED** | Lemma 4.10; three balanced large-leading increments |
| If the synchronized rank-four reset is negative and both next low blocks borrow, rank five is strictly positive | **PROVED** | Theorem 4.11; six exhaustive symbolic endpoint chambers |
| If the synchronized rank-four reset is negative and only the \(x\)-block borrows, rank five is strictly positive | **PROVED** | Theorem 4.12; three deficit rows, one polynomial tail, and three exact small dyadic points |
| If the synchronized rank-four reset is negative and neither block borrows, rank five is strictly positive | **PROVED** | Theorem 4.14; exact rank-three reduction, nine-row promotion tail, and 738 finite \((K,q)\) endpoints |
| The full synchronized rank-four/rank-five bridge \(\gamma_4<0\Rightarrow\gamma_5>0\) holds | **PROVED** | The three borrow states above are exhaustive; this does not cover the pre-cap adaptive-rank branch |
| The first failure is in strip \(j=10\), uniquely at \(b=57349\) within that strip | **FINITE EXACT** | Exhaustive exact minimality audit of strips \(2\le j\le10\) |
| An adaptive-rank diagonal seed exists for all strips and all \(b\) | **OPEN** | The counterfamily suggests iterated-logarithmic delay, but only the special family is understood |
| Erdős #776 is solved | **OPEN / NOT CLAIMED** | The rank-six gate is false; a uniform adaptive-rank seed or different capacity proof is required |
