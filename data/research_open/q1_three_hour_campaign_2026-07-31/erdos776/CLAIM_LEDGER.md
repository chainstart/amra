# Erdős #776 cumulative claim ledger

Date: 2026-07-31

| Claim | Status | Scope |
|---|---|---|
| \(D_{18}\le P_{18}\) implies \(D_{16}\le P_{16}+16V\) | **Proved** | Every \(V\ge288\); uses \(V<\binom{V-13}{15}\) and \(\operatorname{KK}_{15}(V)\le15V\) |
| \(D_{16}\le P_{16}+16V\) implies \(D_8<\binom{V-11}{8}\) | **Proved** | Every \(V\ge288\); fixed-depth coefficients are explicit |
| Zero-slack rank-18 gate \(D_{18}\le P_{18}\Rightarrow D_8<\binom{V-11}{8}\) | **Proved** | Every \(V\ge288\) |
| Rank-8 entry for \(40\le V\le287\) | **Exact finite result** | Verified by integer compressed Macaulay arithmetic |
| It is enough to prove \(D_{18}\le P_{18}\) for all \(V\ge288\) | **Proved reduction** | Together with the finite bridge and inherited R004 descent |
| \(D_{18}\le P_{18}\iff C_2\le T(V)\) for the one-binomial complement start | **Proved equivalence** | \(C_R=\binom{V-13}{R}\), \(C_{r-1}=\operatorname{KK}_r(C_r+V)\) |
| The one-binomial equivalence survives every re-normalization | **Proved / globally audited** | Iterated Galois right adjoints with an early-stop convention; no fixed canonical chart is assumed |
| \(D_{18}\le P_{18}\iff E_5\le\binom{V-25}{5}\) for \(E_{V-26}=0,\ E_{q-1}=V+\operatorname{KK}_q(E_q)\) | **Proved equivalence** | Second tail complement; a failed capacity cannot recover at a later rank |
| \(P_{18}-D_{18}=\binom{V-25}{5}-E_5\) | **Proved on the successful side** | Exact slack identity whenever the equivalent inequalities hold |
| \(P_{s+15}-H_{s+15}=\binom{V-27}{s}\) | **Proved identity** | Hockey-stick cancellation for every valid \(s\) |
| First moving-block entry has excess \(0\le Z_s\le V\) | **Proved** | Exact first-crossing argument; this is not the Round12 first carry |
| \(s\le(V-27)/2\) and \(V(s+1)!/24<\binom{V-27}{3}\) imply \(D_{18}<P_{18}\) | **Proved conditional theorem** | Carry-independent bootstrap excludes every later collision |
| \(s(V)\le(2-\varepsilon)\log V/\log\log V\) eventually would close zero slack asymptotically | **Proved reduction** | Every fixed \(\varepsilon>0\); an exact finite bridge remains necessary |
| \(\operatorname{KK}_r(x+y)\le\operatorname{KK}_r(x)+\operatorname{KK}_r(y)\) | **Proved** | Disjoint shadow-minimizing families |
| First moving-block entry \(s\le28\) implies \(D_{18}<P_{18}\) for every \(V\ge288\) | **Proved conditional theorem** | Exact 26-constant subadditive majorizer; no parameter scan |
| First moving-block entry \(s\le43\) implies \(D_{18}<P_{18}\) for every \(V\ge288\) | **Proved conditional theorem** | Extended exact rational subadditive certificate; minimum base reservoir margin \(241850\) at rank 3 |
| \(D_{59}<H_{59}\Rightarrow D_{18}<P_{18}\) | **Proved reduction** | Every \(V\ge288\); non-recovery makes \(D_{59}<H_{59}\) equivalent to first entry \(s\le43\), or no entry through rank 18 |
| First moving-block entry \(s\le233\) implies \(D_{18}<P_{18}\) for every \(V\ge288\) | **Proved conditional theorem** | Quotient--remainder subadditive certificate: 230 transitions, 288 exact residue classes per transition; minimum base margin \(4928\) |
| \(D_{248}<H_{248}\Rightarrow D_{18}<P_{18}\) | **Proved reduction** | Every \(V\ge288\); non-recovery makes \(D_{248}<H_{248}\) equivalent to first entry \(s\le233\), or no entry through rank 18 |
| “First entry \(s\le28\), or no entry through rank 18” is equivalent to \(D_{44}<H_{44}\) | **Proved equivalence** | Once \(D_q\ge H_q\), the added \(V\) prevents recovery below \(H\) |
| \(D_{44}<H_{44}\iff C_2\le\binom{V-11}{2}-V\) from the start \(C_{V-55}=\binom{V-13}{V-55}+\binom{V-27}{V-56}+1\) | **Proved equivalence / globally audited** | Galois right adjoints with early stop; no rank-44 canonical template is assumed |
| For \(N=V-25\), \(D_{44}<H_{44}\iff E_{31}<\binom{N-1}{31}+\binom{N-2}{30}\) | **Proved equivalence** | \(E_{N-1}=0,\ E_{q-1}=V+\operatorname{KK}_q(E_q)\); failed capacities cannot recover |
| \(H_{44}-D_{44}=[\binom{N-1}{31}+\binom{N-2}{30}]-E_{31}\) | **Proved on the successful side** | Exact second-complement slack identity |
| \(H_{44}-J_{44}=\binom{V-55}{2}\) for the explicit 42-term late block \(J_{44}\) | **Proved identity** | Hockey-stick cancellation; valid without assuming the observed canonical chart |
| \(H_{44}-D_{44}=\binom{V-55}{2}-R_2(V)\), \(R_2=D_{44}-J_{44}\) | **Proved identity** | \(R_2\) is algebraic; it is not assumed to be a separated rank-two tail |
| \(R_2(V)\le7V\Rightarrow D_{44}<H_{44}\) | **Proved conditional theorem** | Every \(V\ge92\), hence the whole analytic range \(V\ge288\) |
| \(F(V+1)-F(V)=H_{43}(V)-[D^{[V+1]}_{44}-D^{[V]}_{44}]\), \(F=H_{44}-D_{44}\) | **Proved identity** | Termwise Pascal difference; diagonal domination would close the rank-44 gate from the \(V=288\) anchor |
| \(R_2(V+1)-R_2(V)=D^{[V]}_{43}-J_{43}(V)+1-L_{45}(V)\) | **Proved identity** | \(L_{45}\) is the exact rank-45 shadow lost across the diagonal gap; no stable-template assumption |
| \(L_{45}\ge D^{[V]}_{43}-J_{43}-6\Rightarrow R_2(V+1)-R_2(V)\le7\) | **Proved conditional theorem** | Together with \(R_2(288)=1970<2016\), the all-\(V\) loss gate would prove \(R_2\le7V\) |
| On \(V-6\le R_2<\binom{V-55}{2}\), the loss gate is equivalent to \(G_{45}\ge S_2(R_2)-U_2(R_2-V+6)\) | **Proved equivalence** | Exact Galois threshold on the separated late-tail chart |
| \(109\operatorname{KK}_3(x)\le6x\) for \(x\ge\binom{58}{3}\) | **Proved** | Direct three-term canonical-expansion estimate; total margin is at least \(3811\) |
| \(D_{45}\le J_{45}+109V\Rightarrow D_{44}\le J_{44}+7V\) | **Proved conditional theorem** | Every \(V\ge288\); noncircular one-rank-higher sufficient gate |
| \(\operatorname{KK}_3(109V-130)\le6V-46\) for \(V\ge288\) | **Proved** | Exact affine shadow estimate; equality occurs at the analytic anchor |
| \(U_p(x+y)\ge U_p(x)+U_p(y)\) | **Proved** | Galois adjunction plus lower-shadow subadditivity |
| \(D_{46}\le J_{46}+2V+424222\Rightarrow D_{44}\le J_{44}+7V-46\) | **Proved conditional theorem** | Every \(V\ge288\); two-step affine lift through ranks 46 and 45 |
| If \(x\) has leading term \(\binom ap\) and \(y\le\binom a{p-1}\), then \(U_p(x+y)-U_p(x)\ge U_{p-1}(y)\) | **Proved** | Clique-form Kruskal--Katona construction with one new vertex |
| \(D_{46}\le J_{46}+458V+292894\Rightarrow D_{44}\le J_{44}+7V-46\) | **Proved conditional theorem** | Every \(V\ge288\); looser and therefore preferable rank-46 premise |
| \(\operatorname{KK}_q(x+y)\le\operatorname{KK}_q(x)+\operatorname{KK}_q(y)-1\) for \(q\ge2,\ x,y>0\) | **Proved** | Relabel two minimizing families to share one lower-shadow set |
| The stronger endpoint \(C_2\le T(V)-2\) holds for all \(V\ge288\) | **False** | Exact counterexample \(V=288\): \(C_2=T(288)-1=37937\) |
| The rank-44 complement endpoint strengthens to \(C_2\le T(V)-1\) | **False** | Exact counterexample \(V=288\): the rank-44 complement has \(C_2=T(288)=37938\) |
| \(R_2(V)\le6V\) for every \(V\ge288\) | **False** | Exact counterexample \(V=288\): \(R_2=1970>1728\); reverse barrier reaches \(b_{275}=287<V\) |
| \(D_{45}\le J_{45}+108V\) for every \(V\ge288\) | **False** | Exact counterexample \(V=288\): \(D_{45}-J_{45}=31262>108\cdot288=31104\) |
| \(D_{46}-J_{46}\le V+424510\) for every \(V\ge288\) | **False** | Exact counterexample \(V=290\): the left side is \(424801\), one above the anchored slope-one line |
| \(R_2(V+1)-R_2(V)\le3\) (or \(\le4\)) for every \(V\ge288\) | **False** | Smallest counterexample in the exact interval \(288\le V\le20000\) is \(V=17423\), with jump \(5\) |
| The \(7V\) gate can be proved by the residual-only reverse recurrence \(B_3=U_2(6V),\ B_{r+1}=U_r(B_r-V)\) | **False as a proof route** | At \(V=288\), \(B_{56}=1549\ge288\) but \(B_{57}=29<288\); a borrow from the fixed block is mandatory |
| The unchanged scalar certificate (7.1) extends from entry rank 43 to 44 | **False as a proof route** | For \(s_\star=44\), its rank-three base value exceeds \(\binom{261}{3}\) by \(69704\); this does not disprove a different rank-44 invariant |
| The quotient--remainder certificate extends from entry rank 233 to 234 | **False as a proof route** | At \(s_\star=234\), its rank-three base value exceeds \(\binom{261}{3}\) by \(31997\); this does not disprove a different invariant |
| \(F(V+1)-F(V)\ge V-57\) for every \(V\ge288\) | **False** | Exact counterexample \(V=1361\): the increment is \(1303=V-58\) |
| Direct strict-subadditive adjacent majorization proves \(D^{[V+1]}_{44}-D^{[V]}_{44}\le H_{43}(V)\) | **False as a proof route** | At \(V=288\) its exact upper bound overshoots \(H_{43}\) by \(2.9245845\ldots\times10^{51}\) |
| The old \(G_2(V)\ge V+1\) target is exactly the next endpoint inequality | **Proved equivalence / loop warning** | It needs an independent higher-rank quantitative loss to be useful |
| \(1+3\max(0,z_3(V+1)-z_3(V))\le k(V)\) implies \(W(V+1)-W(V)\le1\) | **Proved conditional lemma** | On the separated rank-18/17 chart; \(k=\operatorname{KK}_2(V+\operatorname{KK}_3(z_3(V)))\) |
| An \(O(\log V)\) adjacent \(z_3\)-jump bound would close the Lipschitz route asymptotically | **Proved reduction** | Since \(k\ge\lceil(1+\sqrt{1+8V})/2\rceil\); an exact finite bridge would still be required |
| \(D_{18}\le P_{18}\) for every \(V\ge288\) | **Open** | Selected positive slacks are falsifier evidence only |
| The actual first moving-block entry satisfies the factorial gate for every sufficiently large \(V\) | **Open** | Finite entry ranks cannot be extrapolated; the inherited first-carry theorem concerns a different event |
| The actual first moving-block entry has \(s\le28\) for every \(V\ge288\) | **Open / superseded sufficient target** | Stronger than needed after extension of the subadditive gate to \(s\le43\) |
| \(D_{44}<H_{44}\) for every \(V\ge288\) | **Open / superseded sufficient target** | Still sufficient, but stronger than the new rank-59 gate |
| \(D_{59}<H_{59}\) for every \(V\ge288\) | **Open / superseded sufficient target** | Exact fixed-rank form of “first entry \(s\le43\), or no entry through rank 18”; stronger than the rank-248 gate |
| \(D_{248}<H_{248}\) for every \(V\ge288\) | **Open / weakest current closing target** | Exact fixed-rank form of “first entry \(s\le233\), or no entry through rank 18”; selected margins are finite evidence only |
| \(R_2(V)\le7V\) for every \(V\ge288\) | **Open / sharper sufficient target** | Survives the \(V=288\) anchor by only 46; selected rows and a finite window are falsifier evidence only |
| \(R_2(V+1)-R_2(V)\le7\) for every \(V\ge288\) | **Open / inductive target** | Exact dense scan through \(V=20000\) has maximum jump \(5\), but this is finite evidence only |
| \(L_{45}\ge D^{[V]}_{43}-J_{43}-6\) for every \(V\ge288\) | **Open / sharp loss target** | Exact necessary-and-sufficient adjacent loss threshold after Galois conversion |
| \(D_{45}\le J_{45}+109V\) for every \(V\ge288\) | **Open / noncircular higher-rank target** | Coefficient 108 fails at the anchor; exact scan through \(V=2000\) finds no 109 failure |
| \(D_{46}\le J_{46}+2V+424222\) for every \(V\ge288\) | **Open / strongest affine target** | Would imply \(R_2\le7V-46\); exact scan through \(V=2000\) has equality only at the anchor |
| \(D_{46}\le J_{46}+458V+292894\) for every \(V\ge288\) | **Open / recommended rank-46 target** | Weaker than the slope-two gate but has the same consequence; exact scan through \(V=2000\) has equality only at the anchor |
| \(H_{44}(V)-D^{[V]}_{44}\) is nondecreasing for \(V\ge288\) | **Open / alternative sufficient target** | Equivalent to the adjacent diagonal domination \(D^{[V+1]}_{44}-D^{[V]}_{44}\le H_{43}(V)\) |
| The selected rank-44 high-prefix template is canonical for every \(V\ge288\) | **Open / loop warning** | Legality of the template already forces \(R_2<\binom{V-55}{2}\), so it is not a free preliminary normal form |
| \(E_{31}<\binom{V-26}{31}+\binom{V-27}{30}\) for every \(V\ge288\) | **Open** | Exact equivalent inflated-tax fixed-rank-31 capacity |
| \(E_5\le\binom{V-25}{5}\) for every \(V\ge288\) | **Open** | Exact equivalent fixed-rank-five capacity; no all-carry potential yet |
| \(G_2(V)\ge V+1\) for every relevant \(V\) | **Open** | No counterexample found; no all-carry proof |
| \(z_3(V+1)-z_3(V)=O(\log V)\) | **Open** | No all-carry proof; finite jumps do not establish it |
| Erdős #776 is solved | **False** | The zero-slack colex domination remains open |
