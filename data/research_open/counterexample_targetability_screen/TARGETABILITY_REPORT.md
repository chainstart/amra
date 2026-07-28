# 全题库反例可攻关性筛选

生成时间：2026-07-28T14:37:55+00:00

## 范围

- 输入题库：`/home/biostar/work/amra/data/banks/formal_conjectures_open_research.yaml`
- 输入题库：`/home/biostar/work/amra/data/banks/unsolvedmath_open.yaml`
- 输入题库：`/home/biostar/work/amra/data/banks/erdos_open_637.yaml`
- 输入题库：`/home/biostar/work/amra/data/banks/aim_problem_lists.yaml`
- 输入题库：`/home/biostar/work/amra/data/banks/triangle_dissection_track.yaml`
- 输入题库：`/home/biostar/work/amra/data/banks/weird_numbers_track.yaml`
- 历史搜索证据：`/home/biostar/work/amra/data/research_open/unsolvedmath_counterexample_campaign`
- 输入记录：3943
- 进入规范化评分：2966
- 自动短名单：50
- 来源分布：`{"Google DeepMind Formal Conjectures": 1068, "UnsolvedMath": 1898}`

这是一套确定性的选题分诊规则，不是在断言某题必有反例。短名单仍须逐题核对当前开放状态、原题语义和反例证书契约。

## 评分口径

| 正向特征 | 最高分 |
| --- | ---: |
| `resolution_leverage` | 20 |
| `statement_status_confidence` | 15 |
| `certificate_verifier_readiness` | 20 |
| `search_compressibility` | 20 |
| `boundary_leverage` | 10 |
| `feedback_quality` | 10 |
| `local_reuse` | 5 |

毛分满分 100，再扣除题目难度、既往大规模无候选搜索、无结构搜索熵和验证器相关性。数学影响力单独显示，不进入 targetability 分数；排序使用保守下界。

## 分流统计

- 入库门槛：`{"excluded_closed_or_solved": 17, "excluded_duplicate": 104, "included": 2966, "needs_atomic_split": 166, "needs_statement_recovery": 690}`
- 研究路由：`{"answer_discovery": 710, "counterexample": 818, "formal_modeling": 472, "not_counterexample": 1, "subclaim_decomposition": 565, "witness_discovery": 400}`
- 门槛状态：`{"candidate_already_found": 1, "modeling_candidate": 764, "needs_atomic_split": 440, "needs_status_audit": 266, "new_strategy_only": 62, "not_counterexample_target": 1433}`
- 保守分数档：`{"0-39": 2540, "40-54": 401, "55-69": 25}`

## 自动短名单

| 排名 | 保守分 | 点估计 | 毛分 | 问题 | 来源 | 路由状态 |
| ---: | ---: | ---: | ---: | --- | --- | --- |
| 10 | 58 | 65 | 68 | `unsolvedmath-opg-611` The Bermond-Thomassen Conjecture | UnsolvedMath | needs_status_audit |
| 12 | 57 | 64 | 67 | `unsolvedmath-opg-348` Half-integral flow polynomial values | UnsolvedMath | needs_status_audit |
| 26 | 54 | 61 | 64 | `unsolvedmath-opg-337` Gao's theorem for nonabelian groups | UnsolvedMath | needs_status_audit |
| 30 | 53 | 62 | 67 | `formal-conjectures-reed-omega-delta-chi-conjecture-for-finite-graphs` Formal Conjectures: reed_omega_delta_chi_conjecture_for_finite_graphs | Google DeepMind Formal Conjectures | needs_status_audit |
| 35 | 52 | 59 | 63 | `unsolvedmath-opg-165` Ryser's conjecture | UnsolvedMath | needs_status_audit |
| 37 | 52 | 59 | 62 | `unsolvedmath-opg-37271` Star chromatic index of cubic graphs | UnsolvedMath | needs_status_audit |
| 38 | 52 | 59 | 62 | `unsolvedmath-opg-401` Circular coloring triangle-free subcubic planar graphs | UnsolvedMath | needs_status_audit |
| 44 | 51 | 60 | 67 | `formal-conjectures-agrawal-conjecture-variants-popovych` Formal Conjectures: agrawal_conjecture.variants.popovych | Google DeepMind Formal Conjectures | needs_status_audit |
| 45 | 51 | 58 | 62 | `unsolvedmath-kou-21.100` Kourovka Notebook Problem 21.100 | UnsolvedMath | needs_status_audit |
| 46 | 51 | 58 | 61 | `unsolvedmath-opg-145` Acyclic edge-colouring | UnsolvedMath | needs_status_audit |
| 51 | 50 | 57 | 64 | `formal-conjectures-conjecture141` Formal Conjectures: conjecture141 | Google DeepMind Formal Conjectures | needs_status_audit |
| 55 | 50 | 57 | 61 | `unsolvedmath-opg-46359` Directed path of length twice the minimum outdegree | UnsolvedMath | needs_status_audit |
| 56 | 50 | 57 | 61 | `unsolvedmath-opg-46460` Long directed cycles in diregular digraphs | UnsolvedMath | needs_status_audit |
| 57 | 50 | 57 | 61 | `unsolvedmath-opg-47282` Hoàng-Reed Conjecture | UnsolvedMath | needs_status_audit |
| 58 | 50 | 57 | 61 | `unsolvedmath-opg-550` Coloring and immersion | UnsolvedMath | needs_status_audit |
| 60 | 50 | 57 | 60 | `unsolvedmath-opg-155` Olson's Conjecture | UnsolvedMath | needs_status_audit |
| 62 | 50 | 57 | 60 | `unsolvedmath-opg-46606` Decomposing an eulerian graph into cycles with no two consecutives edges on a prescribed eulerian tour. | UnsolvedMath | needs_status_audit |
| 64 | 50 | 57 | 60 | `unsolvedmath-opg-59911` Forcing a 2-regular minor | UnsolvedMath | needs_status_audit |
| 71 | 49 | 57 | 60 | `unsolvedmath-ep-561` Erdős Problem #561 | UnsolvedMath | needs_status_audit |
| 72 | 49 | 56 | 66 | `unsolvedmath-graph-005` Lovász Conjecture | UnsolvedMath | needs_status_audit |
| 73 | 49 | 56 | 66 | `unsolvedmath-graph-008` Cereceda's Conjecture | UnsolvedMath | needs_status_audit |
| 74 | 49 | 56 | 63 | `formal-conjectures-crystals-components-unique` Formal Conjectures: crystals_components_unique | Google DeepMind Formal Conjectures | needs_status_audit |
| 75 | 49 | 56 | 62 | `unsolvedmath-graph-055` Teschner's Bondage Number Conjecture | UnsolvedMath | needs_status_audit |
| 77 | 49 | 56 | 60 | `unsolvedmath-opg-140` Faithful cycle covers | UnsolvedMath | needs_status_audit |
| 78 | 49 | 56 | 60 | `unsolvedmath-opg-1808` Monochromatic reachability or rainbow triangles | UnsolvedMath | needs_status_audit |
| 79 | 49 | 56 | 60 | `unsolvedmath-opg-2110` Edge list coloring conjecture | UnsolvedMath | needs_status_audit |
| 80 | 49 | 56 | 60 | `unsolvedmath-opg-46167` Oriented trees in n-chromatic digraphs | UnsolvedMath | needs_status_audit |
| 81 | 49 | 56 | 60 | `unsolvedmath-opg-646` Seymour's Second Neighbourhood Conjecture | UnsolvedMath | needs_status_audit |
| 82 | 49 | 56 | 59 | `unsolvedmath-opg-34839` Double-critical graph conjecture | UnsolvedMath | needs_status_audit |
| 84 | 49 | 56 | 59 | `unsolvedmath-opg-407` Laplacian Degrees of a Graph | UnsolvedMath | needs_status_audit |
| 85 | 49 | 56 | 59 | `unsolvedmath-opg-46279` Antidirected trees in digraphs | UnsolvedMath | needs_status_audit |
| 86 | 49 | 56 | 59 | `unsolvedmath-opg-52197` Large acyclic induced subdigraph in a planar oriented graph. | UnsolvedMath | needs_status_audit |
| 91 | 48 | 56 | 59 | `unsolvedmath-ep-151` Erdős Problem #151 | UnsolvedMath | needs_status_audit |
| 94 | 48 | 55 | 62 | `formal-conjectures-lander-parkin-selfridge` Formal Conjectures: lander_parkin_selfridge | Google DeepMind Formal Conjectures | needs_status_audit |
| 95 | 48 | 55 | 61 | `unsolvedmath-graph-016` Conway's Thrackle Conjecture | UnsolvedMath | needs_status_audit |
| 96 | 48 | 55 | 61 | `unsolvedmath-kou-21.68` Kourovka Notebook Problem 21.68 | UnsolvedMath | needs_status_audit |
| 100 | 48 | 55 | 59 | `unsolvedmath-opg-170` Linial-Berge path partition duality | UnsolvedMath | needs_status_audit |
| 101 | 48 | 55 | 59 | `unsolvedmath-opg-307` The Crossing Number of the Complete Graph | UnsolvedMath | needs_status_audit |
| 102 | 48 | 55 | 59 | `unsolvedmath-opg-310` The Crossing Number of the Complete Bipartite Graph | UnsolvedMath | needs_status_audit |
| 103 | 48 | 55 | 59 | `unsolvedmath-opg-37117` Are different notions of the crossing number the same? | UnsolvedMath | needs_status_audit |
| 106 | 48 | 55 | 59 | `unsolvedmath-opg-798` Degenerate colorings of planar graphs | UnsolvedMath | needs_status_audit |
| 107 | 48 | 55 | 58 | `unsolvedmath-opg-135` Real roots of the flow polynomial | UnsolvedMath | needs_status_audit |
| 108 | 48 | 55 | 58 | `unsolvedmath-opg-37226` Sequence defined on multisets | UnsolvedMath | needs_status_audit |
| 109 | 48 | 55 | 58 | `unsolvedmath-opg-37305` Extremal problem on the number of tree endomorphism | UnsolvedMath | needs_status_audit |
| 110 | 48 | 55 | 58 | `unsolvedmath-opg-37907` Mixing Circular Colourings | UnsolvedMath | needs_status_audit |
| 112 | 48 | 55 | 58 | `unsolvedmath-opg-46634` Large induced forest in a planar graph. | UnsolvedMath | needs_status_audit |
| 113 | 48 | 55 | 58 | `unsolvedmath-opg-46824` Odd-cycle transversal in triangle-free graphs | UnsolvedMath | needs_status_audit |
| 114 | 48 | 55 | 58 | `unsolvedmath-opg-46837` Triangle-packing vs triangle edge-transversal. | UnsolvedMath | needs_status_audit |
| 115 | 48 | 55 | 58 | `unsolvedmath-opg-50631` Cyclic spanning subdigraph with small cyclomatic number | UnsolvedMath | needs_status_audit |
| 121 | 47 | 55 | 60 | `unsolvedmath-ep-677` Erdős Problem #677 | UnsolvedMath | needs_status_audit |

## 已搜索目标：仅限新策略重试

| 排名 | 保守分 | 已检查案例 | 问题 |
| ---: | ---: | ---: | --- |
| 1 | 68 | 331 | `unsolvedmath-opg-1757` Negative association in uniform forests |
| 2 | 64 | 25914 | `unsolvedmath-opg-729` Seagull problem |
| 3 | 64 | 40 | `unsolvedmath-opg-404` Concavity of van der Waerden numbers |
| 4 | 63 | 304152 | `unsolvedmath-opg-60039` Sidorenko's Conjecture |
| 5 | 62 | 90 | `unsolvedmath-kou-21.87` Kourovka Notebook Problem 21.87 |
| 6 | 61 | 43009 | `unsolvedmath-opg-48264` Signing a graph to have small magnitude eigenvalues |
| 7 | 60 | 42 | `unsolvedmath-kou-21.135` Kourovka Notebook Problem 21.135 |
| 8 | 59 | 38699 | `unsolvedmath-opg-171` Strong colorability |
| 9 | 59 | 10128 | `unsolvedmath-opg-56230` 2-colouring a graph without a monochromatic maximum clique |
| 11 | 58 | 3836 | `unsolvedmath-opg-412` Mapping planar graphs to odd cycles |
| 13 | 57 | 1651 | `unsolvedmath-opg-46584` Decomposing an eulerian graph into cycles. |
| 14 | 57 | 323 | `unsolvedmath-opg-59976` Are all Mersenne Numbers with prime exponent square-free? |
| 15 | 57 | 493 | `unsolvedmath-opg-37413` Alexa's Conjecture on Primality |
| 16 | 56 | 2911 | `unsolvedmath-opg-563` Davenport's constant |
| 17 | 56 | 1299 | `unsolvedmath-opg-46583` Decomposing a connected graph into paths. |
| 18 | 56 | 1079 | `unsolvedmath-opg-491` Odd incongruent covering systems |
| 19 | 56 | 1513 | `unsolvedmath-opg-600` Matchings extend to Hamiltonian cycles in hypercubes |
| 20 | 55 | 227890 | `unsolvedmath-opg-335` Reed's omega, delta, and chi conjecture |
| 21 | 55 | 310000 | `unsolvedmath-opg-46475` Strong edge colouring conjecture |
| 22 | 55 | 150312 | `unsolvedmath-opg-60055` Chromatic number of $\frac{3}{3}$-power of graph |
| 23 | 55 | 88042 | `unsolvedmath-opg-638` Jones' conjecture |
| 24 | 55 | 432 | `unsolvedmath-geo-025` Kalai's $3^d$ Conjecture |
| 25 | 55 | 1965 | `unsolvedmath-opg-804` Edge Reconstruction Conjecture |
| 27 | 54 | 1747567 | `unsolvedmath-opg-156` Few subsequence sums in Z_n x Z_n |
| 33 | 53 | 10005 | `unsolvedmath-opg-143` Petersen coloring conjecture |
| 34 | 53 | 42 | `unsolvedmath-kou-21.35` Kourovka Notebook Problem 21.35 |
| 39 | 52 | 2113254 | `unsolvedmath-opg-37396` 3 is a primitive root modulo primes of the form 16 q^4 + 1, where q>3 is prime |
| 40 | 52 | 310000 | `unsolvedmath-opg-46613` Partition of a cubic 3-connected graphs into paths of length 2. |
| 41 | 52 | 20100 | `unsolvedmath-kou-21.25` Kourovka Notebook Problem 21.25 |
| 42 | 52 | 18446 | `unsolvedmath-opg-60029` Cycle Double Covers Containing Predefined 2-Regular Subgraphs |
| 43 | 52 | 149800 | `unsolvedmath-opg-543` The intersection of two perfect matchings |
| 47 | 51 | 310000 | `unsolvedmath-opg-37038` Domination in cubic graphs |
| 66 | 50 | 301252 | `unsolvedmath-opg-128` 3-flow conjecture |
| 67 | 50 | 310000 | `unsolvedmath-opg-154` Jorgensen's Conjecture |
| 68 | 50 | 310000 | `unsolvedmath-opg-161` Hamiltonian paths and cycles in vertex transitive graphs |
| 69 | 50 | 310000 | `unsolvedmath-opg-385` Barnette's Conjecture |
| 70 | 50 | 3362863 | `unsolvedmath-opg-37404` Sum of prime and semiprime conjecture |
| 88 | 49 | 32565491 | `unsolvedmath-opg-55810` Are all Fermat Numbers square-free? |
| 116 | 48 | 3563327 | `unsolvedmath-nt-035` Lehmer's Totient Problem |
| 117 | 48 | 3002000 | `unsolvedmath-nt-053` Is 10 a Solitary Number? |
| 118 | 48 | 1002000 | `unsolvedmath-opg-636` Even vs. odd latin squares |
| 119 | 48 | 1002000 | `unsolvedmath-opg-37670` The Borodin-Kostochka Conjecture |
| 120 | 48 | 535 | `unsolvedmath-kou-21.130` Kourovka Notebook Problem 21.130 |
| 132 | 47 | 999 | `unsolvedmath-guy-a10` Gilbreath's Conjecture |
| 135 | 47 | 24 | `unsolvedmath-opg-439` Graceful Tree Conjecture |
| 166 | 47 | 1002000 | `unsolvedmath-opg-1793` Non-edges vs. feedback edge sets in digraphs |
| 167 | 47 | 310000 | `unsolvedmath-opg-434` Weak pentagon problem |
| 219 | 46 | 310000 | `unsolvedmath-opg-37182` Odd cycles and low oddness |
| 240 | 45 | 49 | `unsolvedmath-opg-658` Reconstruction conjecture |
| 253 | 45 | 3101361 | `unsolvedmath-nt-059` Lemoine's Conjecture |

## 使用边界

- `needs_status_audit`：本地题面有潜力，但必须先用权威来源核对截至当前日期仍开放。
- `modeling_candidate`：量词或 checker 尚未充分恢复，只可投入建模。
- `new_strategy_only`：已有无候选搜索历史，除非表示、边界或理论假设发生实质变化，否则不重跑。
- `not_counterexample_target`：转向正见证、证明、答案恢复或子命题拆分。
- Formal Conjectures 中的 `answer(sorry)` 是未知答案占位符，不是已解答，也不按普通等价命题计分。
- `∀ᶠ`、`∀ᵉ`、`∃ᶠ`、极限与渐近命题不会因出现一个失败点就被判为可有限反驳。
