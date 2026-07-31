# Erdős #776 breakthrough-campaign claim ledger

Date: 2026-07-31

| Claim | Status | Scope |
|---|---|---|
| Before first moving-block entry, \(H_q-D_q=F^{(53)}_{V-q-13}\) with \(F^{(53)}_1=V-53\), \(F^{(53)}_{r+1}=U_r(F^{(53)}_r)-V\) | **PROVED** | All legal rows, with an explicit early-stop convention |
| \(F^{(c)}_r=\binom{V-c-2}{r}+F^{(2c+3)}_{r-1}\) | **PROVED** | Every row on which both nonnegative separated charts are legal |
| The constants in the first two Pascal peels are \(53\to109\to221\) | **PROVED** | Exact integer identities |
| If \(M=V-221\), \(E_{M-1}=0\), \(E_{q-1}=V+\operatorname{KK}_q(E_q)\), and \(E_{42}<\binom M{42}\), then \(D_{248}<H_{248}\) | **PROVED** | Every \(V\ge288\) |
| Under the same premise, \(H_{248}-D_{248}=\binom{V-55}{V-261}+\binom{V-111}{V-262}+\binom{V-221}{42}-E_{42}\) | **PROVED** | Every \(V\ge288\) on the successful branch |
| One nonnegative adjacent diagonal surplus \(\Gamma_r\) remains nonnegative at every later legal row | **PROVED** | Lemma 6.1; uses upper-shift superadditivity and \(V\ge r+2\) |
| Before the auxiliary first carry, \(f_r=\sum_{k=2}^r\binom{M-A_{r-k}-2}{k}+\binom{M-A_{r-1}}1\), \(A_j=224(2^j-1)\) | **PROVED** | Every row with \(A_{r-1}<M\) |
| The first possible auxiliary diagonal seed has logarithmic rank \(\log_2(M/224)+O(1)\) | **PROVED localization** | Before this carry, \(\Gamma_r=-(M+222)<0\) exactly |
| For \(M\ge225\), the first-carry comparison is exactly the fixed tail pair (6.12), and \(\Gamma_{j+p-2}=\gamma_p\) for \(p=3,4,5\) | **PROVED** | Theorem 6.3; all high Macaulay terms cancel pairwise |
| The first low tail has the one-borrow form (6.17)--(6.18), with a nonnegative borrowed remainder on the whole dyadic strip | **PROVED** | Includes both endpoints \(b=1\) and \(b=L\), all \(j\ge2\) |
| The signed-lift deficits satisfy \(\delta_3,\delta_4,\delta_5\ge0\) on every strip | **PROVED** | Proposition 6.4; Macaulay adjunction proves the base and propagates it through ranks 4 and 5 |
| At the right strip endpoint, \(\gamma_5(L,L)=\binom{L-14}{2}+2L-144>0\) | **PROVED** | Exact endpoint canonical form |
| The fixed-simplex barrier \(F^{(221)}_{M-42}\ge\binom{M-3}{M-42}\) | **REFUTED** | Exact counterexample \(V=288,M=67\) |
| The forward gap \(F^{(221)}_r\) is nondecreasing in \(r\) | **REFUTED** | Exact decrease from rank 37 to 38 at \(V=301\) |
| \(E_{42}<\binom M{42}\) for \(67\le M\le279\) | **FINITE** | Exact integer falsifier scan; minimum margin \(147405541057332121\) at \(M=67\) |
| The 42-canonical expansion of \(E_{42}\) begins with \(\binom{M-1}{42}+\binom{M-2}{41}\) for \(67\le M\le279\) | **FINITE** | Zero prefix failures in the displayed interval |
| The first nonnegative diagonal seed occurs by \(j(M)+3\) | **FINITE** | Exact dense scan \(67\le M\le10000\), plus exact right-endpoint tests for the first 30 carry intervals |
| The explicit fixed-rank surplus \(\gamma_5\) is positive | **FINITE** | Exact \(225\le M\le10000\), plus both endpoints of the first 30 carry strips |
| \(E_{42}<\binom M{42}\) for every \(M\ge67\) | **OPEN** | New fixed-rank capacity gate; finite scans are not extrapolated |
| \(y_6\ge S_5(x_5)\) for the explicit pair (6.12) on every dyadic strip | **OPEN** | Equivalently \(\delta_5\ge T+1\); the weaker all-strip bound \(\delta_5\ge0\) is proved |
| \(D_{248}<H_{248}\) for every \(V\ge288\) | **OPEN** | Would follow from the rank-42 capacity gate |
| Erdős #776 is solved | **FALSE** | The universal rank-42 gate / rank-248 gate remains unproved |
