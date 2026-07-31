# Claim ledger — Erdős #809 first and second attacks

| ID | Claim | Status | Evidence / boundary |
|---|---|---|---|
| 809-F1 | For same-colour good edges, one may orient both distinguished endpoints into \(A\) and also assume they realize the global edge distance. | **FALSE** | The six-vertex sharp guard in `FIRST_ATTACK.md` has \(A\)-endpoint distance three but outer-endpoint distance two. |
| 809-F2 | The strict \(A\)-oriented profiles are A2, A3-clean, and A3-contaminated. | **PROVED — structural-assumption lemma** | They respectively give \(\tau_3(y,w)\le3\), outer codegree at most two, or \(\tau_3(x,z)\le2\). |
| 809-F3 | The closest-endpoint profiles are exactly D2-AA, D2-AO, D2-OO, and D3. | **PROVED — structural-assumption lemma** | At global distance two, record whether two, one, or zero closest endpoints are the selected \(A\)-endpoints; global distance three forces the selected \(A\)-pair also to be closest. |
| 809-F4 | Every global-distance-two profile yields a three-vertex cover of all complementary length-three paths. | **PROVED — general graph lemma** | Splicing any avoiding complementary three-path with the globally shortest inner two-path gives a \(C_7\). |
| 809-F5 | An arbitrary \(A\)-oriented distance-three geodesic forces bounded outer codegree. | **FALSE** | A geodesic may run through a specified outer endpoint.  The parameterized contaminated guard has arbitrarily large outer codegree; its valid certificate is instead \(\tau_3(x,z)\le2\). |
| 809-F5a | A clean \(A\)-oriented distance-three geodesic forces outer codegree at most two. | **PROVED — general graph lemma** | Every common neighbour outside the two clean internal vertices supplies a disjoint length-two partner and hence a \(C_7\). |
| 809-F5b | Global edge distance three forces zero outer codegree. | **PROVED — general graph lemma** | All four cross-endpoint distances are at least three, so the complementary endpoints have no common neighbour. |
| 809-F6 | The raw defect estimate \(D_A=o(n^2)\) follows from the frozen Case-1 contract. | **FALSE** | Two unbalanced cliques joined by four independent bridges satisfy the density, minimum-degree, diameter-three, and \(L_4(2)\) conditions, yet admit a rainbow-\(C_7\) colouring with \(D_A=\binom{q-4}{2}=\Theta(n^2)\) for the permitted choice \(A=V(G)\). |
| 809-F7 | The four-bridge family is a counterexample to Erdős #809. | **FALSE / GUARDED** | It uses \(\binom p2+4q-6=(T(s)+o(1))n^2\) colours and therefore asymptotically saturates the conjectured bound. |
| 809-F8 | The exact good-edge closure target is \(D_A\le |E_{\rm good}|-T(s)n^2+o(n^2)\). | **PROVED — algebraic equivalence for the good-edge route** | The number of colours represented on good edges is exactly \(|E_{\rm good}|-D_A\). |
| 809-F9 | Requiring only \(|A|=(1/2+s+o(1))n\) repairs raw (LD). | **FALSE** | In the bridge family a diameter-three \(A\) of that size may contain linear subsets of both cliques, leaving quadratic paired good edges. |
| 809-F10 | A canonical/existential choice of \(A\) concentrated on one structural core repairs raw (LD) in every Case-1 graph. | **OPEN** | This requires a new witness-selection/stability lemma; it is not implied by BCM Lemma 3.1 as currently used. |
| 809-F11 | The budgeted defect inequality holds for every admissible \(A\) in every fixed-\(s\) Case-1 graph. | **FALSE** | `SECOND_ATTACK.md` splits the complement of a minimum-size admissible \(A\) equally between the two cliques and arranges \(\Theta(n^2)\) paired colours wholly outside \(E_{\rm good}(A)\).  Then \(D_A\) exceeds the good-edge surplus by \(((1/2-s)^2/8+o(1))n^2\). |
| 809-F11e | Every fixed-\(s\) Case-1 colouring has at least one BCM-admissible witness \(A\) satisfying the budgeted defect inequality. | **OPEN — QUANTIFIER-SAFE PRIMARY GAP** | The mixed witness no-go does not address this existential form.  In diameter-three graphs it can be as hard as the desired total colour lower bound. |
| 809-F12 | Erdős #809 is solved. | **OPEN / NOT CLAIMED** | The attacks repair the local taxonomy, refute two overstrong defect targets, and close an aligned-core regime, but do not prove the required global dichotomy. |
| 809-S1 | A minimum-size admissible \(A\) automatically satisfies budgeted defect. | **FALSE** | In the four-bridge family take \(A=V\setminus(B_P\cup B_Q)\), where \(|B_P|,\lvert B_Q\rvert\sim q/2\), and pair all \(B_P\)-edges with distinct \(B_Q\)-edges. |
| 809-S2 | On the same family, the maximum-degree branch of BCM Lemma 3.1 selects \(A_*=P\cup\{q_1\}\) and gives \(D_{A_*}=0\). | **PROVED — exact family statement** | \(A_*=N[p_1]\), \(\Delta=p\ge C_1-1\), all paired \(Q^\circ\)-edges are bad, and every good edge has a different colour. |
| 809-S3 | If \(G\) contains a set \(P\) of size \((1/2+s+o(1))n\) spanning all but \(o(n^2)\) clique edges, every rainbow-\(C_7\) colouring has at least \(T(s)n^2-o(n^2)\) colours. | **PROVED — unbounded conditional theorem** | Delete \(o(n)\) high missing-degree vertices; the remaining graph satisfies \(2\delta-|P|\ge5\), so every two of its edges lie on a common \(C_7\). |
| 809-S4 | If additionally \(|P\setminus A|=o(n)\), then (BD) holds for that \(A\). | **PROVED — unbounded conditional theorem** | The cleaned pairwise-compatible core lies in \(E_{\rm good}(A)\) and contains \(T(s)n^2-o(n^2)\) edges. |
| 809-S5 | BCM Lemma 3.1 itself supplies an \(A\) satisfying (BD). | **OPEN / NOT IN BCM** | The lemma supplies only size and pairwise distance.  Its proof has maximum-degree, diameter-three, and high-degree-threshold witness branches; colour control is absent. |
| 809-T1 | In the BCM maximum-degree branch \(A=N[v]\), all same-colour good-edge pairs have one clean centered A2 certificate. | **PROVED** | Neither edge can meet \(v\); for orientations \(xy,zw\) with \(x,z\in A\), \(x-v-z\) is shortest and every length-three \(y\)-to-\(w\) path meets \(\{x,v,z\}\). |
| 809-T2 | If \(M_A,M_B\) are the missing-edge counts in \(A,B=V\setminus A\), then \(e(A,B)\le2M_A\) and \(e(A,B)=M_A+M_B-(\binom{|A|}{2}+\binom{|B|}{2}-e)\). | **PROVED — exact energy ledger** | Maximum degree gives \(d_B(u)\le\overline d_A(u)\) for every \(u\in A\); the second identity is the edge partition. |
| 809-T3 | The exact maximum-witness good-edge surplus is \(M_B+S_m\), where \(S_m=e-\binom{|B|}{2}-\Phi(n,e)\ge0\). | **PROVED — exact algebra** | The only bad edges lie in \(B\), and the BCM size lower bound makes \(e-\binom{|B|}{2}\ge\Phi(n,e)\). |
| 809-T4 | If \(k=\min\{j:\binom j2\ge\Phi\}\), \(m=|A|=k+g\), and \(M_A\le g(k-7)/16\), the maximum-degree branch closes. | **PROVED — unbounded conditional theorem** | Delete vertices with missing degree \(>(k-7)/4\); fewer than \(g/2\) are deleted, and the remaining graph has \(2\delta-|H|\ge5\) and at least \(\binom k2\) edges. |
| 809-T5 | Every maximum-degree BCM witness is aligned with the dense larger core. | **FALSE** | The rotated \(U,Z,W\) two-clique family has \(A=N[v]=U\cup W\), while its larger core is \(U\cup Z\) and \(|Z|=\Theta(n)\); density, minimum degree, and \(L_4(2)\) survive. |
| 809-T6 | The rotated family obstructs the canonical budgeted defect. | **FALSE / GUARDED** | Its saturating colouring pairs good \(W\)-edges only with bad \(Z\)-edges, so \(D_A=0\).  It red-teams alignment, not (BD). |
| 809-T7 | For the maximum-degree witness, \(D_A\le M_B+S_m+o(n^2)\). | **OPEN — EXACT CENTERED CHARGE GAP** | All local obstructions share the center \(v\), but no bounded-congestion injection from nonroot repeated good edges to outside missing edges/size slack is known. |
| 809-T8 | If \(M_B<\binom{q-1}{2}\), all good edges admitting an orientation with outer \(B\)-degree at least \(q\) are pairwise \(C_7\)-compatible. | **PROVED — centered rectangle theorem** | A noncompatible pair would make the two outside neighbourhoods anticomplete and force at least \(\binom{q-1}{2}\) missing edges in \(B\). |
| 809-T9 | For a colour \(\gamma\), its \(t_\gamma\) chosen outer endpoints in \(B\) span \(\binom{t_\gamma}{2}\) missing edges. | **PROVED — exact local accounting** | Same-colour edges form an induced matching.  Rooting the class injects its \(t_\gamma-1\) \(B\)-outer extras into missing pairs within that class. |
| 809-T10 | The local accounting in T9 has bounded global congestion. | **FALSE WITHOUT GLOBAL CONTRACT / OPEN IN CASE 1** | A bipartite centered incidence graph realizes arbitrarily many colours on the same missing pair.  It fails \(L_4(2)\)/density, showing exactly which global hypotheses a congestion proof must exploit. |
| 809-U1 | For a fixed missing pair \(bb'\subset B\), every colour using \(bx,b'z\) supplies a two-vertex cover of the three-path shore graph \(\mathcal H(b,b')\). | **PROVED** | This is the centered \(b-x-v-z-b'\) splice. |
| 809-U2 | If \(\mathcal H(b,b')\) is nonempty, then its cross-colour congestion is at most one. | **PROVED — sharp local theorem** | On a shore path \(b-p-q-b'\), inducedness forces \(p\) to the left role and \(q\) to the right role. If both roles occur, \(b-p-q-b'-a-v-c-b\) is a non-rainbow \(C_7\). |
| 809-U3 | If a missing pair has empty shore, then \(M_A\ge\binom{\min(d_A(b),d_A(b'))}{2}\). | **PROVED — exact energy obstruction** | \(N_A(b)\) and \(N_A(b')\) are anticomplete on all distinct cross pairs. |
| 809-U4 | With \(\ell_A=\max(0,\delta-|B|+1)\), the condition \(M_A<\binom{\ell_A}{2}\) implies \(D_B\le M_B\). | **PROVED — aggregate conditional theorem** | The energy threshold eliminates empty shores; double-count colour/pair incidences and apply U2. |
| 809-U5 | If \(E_0=\sum_{\text{zero-shore }bb'}(\lambda(bb')-1)_+\), then \(D_B\le M_B+E_0\); if \(R_A+E_0\le S_m\), the exact budget closes. | **PROVED — unconditional residual and conditional closure** | Every nonempty-shore incidence and the first incidence on every zero-shore pair fit in \(M_B\); only excess zero-shore multiplicity remains. |
| 809-U6 | The nonempty-shore charge solves the whole maximum-degree branch. | **OPEN / NOT CLAIMED** | The zero-shore excess \(E_0\) and outer-\(A\) residual \(R_A\) remain. Their aggregate absorption into \(S_m\) is the exact gap. |
| 809-V1 | A zero-shore pair with congestion \(h\) forces an \(h\)-by-\(h\) missing rectangle inside \(A\), so \(M_A\ge h^2\). | **PROVED — exact local energy theorem** | The two coordinate sets are disjoint by inducedness and anticomplete by the absence of a three-edge shore. |
| 809-V2 | The R003 no-three-step dichotomy applies to a zero-shore pair with \(S=\varnothing\); in its common-neighbour branch \(h\le n-2\delta\). | **PROVED — exact structural interface** | The \(2h\) coordinate vertices lie in the exclusive block \(W\), while R003 gives \(|W|\le2n-4\delta\). |
| 809-V3 | Exact four-edge paths across a zero-shore pair have the forced \(P\)-\(L\)-\(Q\) pattern, and their connector-triple hypergraph has transversal number at least three. | **PROVED** | Any middle vertex in \(P\cup Q\) creates a forbidden \(P\)--\(Q\) edge; a two-vertex transversal contradicts \(L_4(2)\). |
| 809-V4 | The existence of a zero-shore pair automatically yields an aligned dense core or the full \(T(s)n^2\) compatible family at fixed \(s\). | **OPEN / NOT CLAIMED** | R003 leaves linear \(2sn\) or \(4sn\) exceptional blocks. The new rectangle and robust connectors do not yet control aggregate overlap. |
| 809-W1 | For oriented zero-shore rectangles, a fixed missing \(A\)-pair has overlap at most \(\min\{d_B(a)d_B(a'),L(a),L(a')\}\). | **PROVED — summable overlap lemma** | Coordinate edges determine the outer pair; fixing one coordinate edge leaves at most \(t_\gamma-1\) other outer endpoints of its colour. |
| 809-W2 | With \(Q_A=\sum_{aa'\in\overline E(A)}d_B(a)d_B(a')\), one has \(\sum h_e^2\le2Q_A\) and \(E_0\le(H-1)M_B+2Q_A/H\). | **PROVED — weighted high/low theorem** | Double-count rectangle area, then split at weight \(H\). |
| 809-W3 | A zero-shore star has same-neighbourhood leaves within \(2\kappa\) of the centre neighbourhood or opposite-neighbourhood leaves within \(\kappa\) of its complement, where \(\kappa=n-2\delta\). | **PROVED — local alignment lemma** | This is the exact R003 \(R\ne\varnothing\)/\(R=\varnothing\) split with \(S=\varnothing\). Same-type edges also satisfy \(h\le\kappa\). |
| 809-W4 | Every fixed missing \(A\)-pair belongs to \(O(1)\), or even \(o(n)\), zero-shore rectangles under the full Case-1 contract. | **FALSE** | The three-hub two-clique family has one fixed pair in \(\Theta(n)\) rectangles while satisfying density, minimum degree, \(L_4(2)\), a maximum BCM witness, and rainbow \(C_7\). |
| 809-W5 | The zero-shore excess \(E_0=\sum(h_e-1)_+\) is always \(o(n^2)\) under the full Case-1 contract. | **FALSE** | In the same family, match every \(W\)-vertex to a \(U\)-vertex and pair all \(W\)--\(Y\) edges with \(U\)--\(X\) edges. Then \(E_0=|W|(|Y|-1)=\Theta(n^2)\). |
| 809-W6 | Quadratic zero-shore overlap automatically refutes the canonical budget. | **FALSE / GUARDED** | The three-hub family has an aligned clique \(C_1\) of the target size and \(S_m\sim M_B\sim D_A\); its large \(E_0\) is a charging artifact, not a colour-bound obstruction. |
| 809-W7 | Unabsorbable zero-shore rectangle mass synchronizes the local star types into an aligned complete-split or two-clique core. | **OPEN — EXACT SIXTH-STAGE GAP** | The local two-type lemma has \(O(sn)\) error at fixed \(s\); propagation across different star centres is not yet proved. |
| 809-X1 | If \(R_A+(H-1)M_B+2Q_A/H\le S_m\) for some \(H\ge2\), the maximum-witness defect budget closes. | **PROVED — quantitative absorption certificate** | Combine \(D_B\le M_B+E_0\) with the sixth-stage high/low bound. |
| 809-X2 | For an opposite zero pair with \(p=d(b)\), \(q=d(c)\), and \(\rho=n-p-q\), the partition \(P=N(b)\), \(C=V\setminus P\) satisfies \(M(P)+M(C)=\Psi_e(p)+e(P,C)\le\Psi_e(p)+p\rho\). | **PROVED — exact core energy identity** | \(P\) is anticomplete to \(Q=N(c)\); every cut edge from \(P\) ends in the \(\rho\)-vertex residual set. |
| 809-X3 | With maximum-degree overshoot \(\zeta\), the larger side of an opposite pair has the size and missing-edge bounds (15)--(16) of `SEVENTH_ATTACK.md`. | **PROVED — parameterized stability theorem** | Expand \(\Psi_e(p)/n^2=(p/n-1/2)^2-s^2+o(1)\) and use \(\delta\le p\le\Delta\). |
| 809-X4 | If \(\zeta=o(1)\) and the opposite weighted residual moment is \(o(nE_0^{\rm opp})\), an aligned \((1/2+s-o(1))n\)-vertex core with \(o(n^2)\) missing edges exists. | **PROVED — conditional global stability** | Weighted averaging selects an opposite edge with \(\rho=o(n)\), then X3 applies. |
| 809-X5 | Failure of the absorption certificate forces the opposite residual-moment condition in X4. | **FALSE — refuted in the eighth attack** | The three-clique-chain family satisfies the full contract, fails every high/low certificate, and has \(\mathcal R_{\rm opp}/(nE_0^{\rm opp})\to2s>0\). |
| 809-X6 | Quadratic same-neighbourhood zero-star mass synchronizes into one global complete-split core at fixed \(s\). | **OPEN** | Each local star is within \(O(sn)\) of one type, but the centres' reference neighbourhoods have not been globally synchronized. |
| 809-Y1 | Failure of the high/low absorption certificate forces \(\mathcal R_{\rm opp}=o(nE_0^{\rm opp})\). | **FALSE — full-contract graph family** | The three-clique-chain family has certificate minimum \(\Theta(n^3)\), \(S_m=O(n)\), and \(\mathcal R_{\rm opp}/(nE_0^{\rm opp})\to2s>0\). |
| 809-Y2 | Failure of the stronger sufficient test \(R_A+E_0\le S_m\) forces the same residual-moment conclusion. | **FALSE — same family** | Here \(R_A=0\), \(E_0=\Theta(n^2)>S_m\), but the normalized opposite residual tends to \(2s\). |
| 809-Y3 | With weighted endpoint incidence \(\omega(v)\), one has \(\mathcal R_{\rm opp}=nE_0^{\rm opp}-\sum_v\omega(v)d(v)=\sum_v\omega(v)(n/2-d(v))\). | **PROVED — exact identity** | Expand every weighted residual \(w_{bc}(n-d(b)-d(c))\) and collect endpoint terms. |
| 809-Y4 | If \(L_\varepsilon=\{v:d(v)<(1/2-\varepsilon)n\}\) and \(\Omega_\varepsilon=\sum_{v\in L_\varepsilon}\omega(v)\), then \(\mathcal R_{\rm opp}\le2\varepsilon nE_0^{\rm opp}+\kappa\Omega_\varepsilon\). | **PROVED — degree-support criterion** | Pairs avoiding \(L_\varepsilon\) have residual at most \(2\varepsilon n\); pairs touching it have total weight at most \(\Omega_\varepsilon\) and residual at most \(\kappa\). |
| 809-Y5 | Conditions \(\varepsilon_n=o(1)\), \(\Omega_{\varepsilon_n}=o(E_0^{\rm opp})\), and \(\zeta=o(1)\) yield an aligned asymptotically complete core. | **PROVED — conditional stability** | Y4 supplies the seventh-stage residual hypothesis, after which X4 applies. |
| 809-Y6 | The three-clique-chain obstruction refutes the exact maximum-witness defect budget or Erdős #809. | **FALSE / GUARDED** | It has \(D_A=D_B=M_B\), so the exact budget closes, and its color count exceeds \(\Phi(n,e)\) by \(\Theta(n^2)\). |
| 809-Y7 | Genuine exact-budget hardness forces small weighted low-degree endpoint support, or a different compatible-family exit. | **OPEN — EXACT EIGHTH-STAGE GAP** | Certificate failure alone is now ruled out as a premise; an effective charge/Hall-deficiency hypothesis is still missing. |

## Strongest closed result

Both raw defect and all-\(A\) budgeted defect are rigorously refuted.
The exact budget identity remains valid with an existential/canonical
witness quantifier.  The endpoint taxonomy is repaired into the
A2 / A3-clean / A3-contaminated certificates, and the entire
asymptotically complete larger-core regime is closed: its internal edges
contain \(T(s)n^2-o(n^2)\) pairwise \(C_7\)-compatible edges.  If the BCM
witness is aligned with that core, the budgeted inequality follows for
its good edges.

## Quantifier-safe primary gap

For a witness selected by the actual branches of BCM Lemma 3.1, prove a
dichotomy: either it is aligned with an asymptotically complete
\((1/2+s)n\)-vertex core, which `SECOND_ATTACK.md` closes, or its good
edges contain \(T(s)n^2-o(n^2)\) pairwise \(C_7\)-compatible edges by a
different structural mechanism.  No assertion quantified over every
admissible \(A\) can be true.

For the maximum-degree branch this is sharpened by `THIRD_ATTACK.md` to
the centered charge
\[
D_A\le M_B+S_m+o(n^2).
\]
The positive-width low-\(M_A\) region is closed; the first remaining
case has quantitatively large missing energy in \(A\), and every repeated
pair supplies a three-path cover with the same center \(v\).  The
rich-outer region is also closed when \(M_B\) is below its exact rectangle
threshold, leaving low-\(B\)-degree outer endpoints as the first local
residue.  The fourth attack gives the exact coefficient-one
cross-colour charge for every nonempty shore and a quadratic
\(A\)-missing-energy threshold eliminating empty shores.  The remaining
maximum-witness gap is precisely the aggregate multiplicity of zero-shore
pairs together with the outer-\(A\) residual defect.
