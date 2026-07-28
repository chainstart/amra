# Fresh 高分候选的实时状态与启动审计

核验日期：2026-07-28

本表复核自动 fresh shortlist 最初的前 10 项，以及剔除两个已知反例后的两个补位项。它回答的是“截至当前是否仍开放、应搜索哪个最小开放切片、反例证书能否独立复算”，不是按题目名气排序。

## 审计结论

| 自动候选 | 实时状态 | 最小可搜索切片与证书 | 结论 |
| --- | --- | --- | --- |
| `unsolvedmath-opg-37271` | open/partial；近期工作仍研究特殊图类（[arXiv:1701.04105](https://arxiv.org/abs/1701.04105)、[arXiv:1912.02467](https://arxiv.org/abs/1912.02467)、[2025 论文](https://doi.org/10.1007/s40840-025-01875-9)） | 原题对象是 subcubic **multigraph**。证书为多重图以及“不存在 star 6-edge-colouring”的 CNF/DRAT；约束是局部的 proper edge-colouring 加禁止双色四边路/圈 | 第一优先；实现前明确多重图模型，或显式声明先搜 simple 子类 |
| `unsolvedmath-opg-145` | open；2025 专题论文仍称一般图情形未解（[arXiv:2501.11281](https://arxiv.org/abs/2501.11281)）；`Δ≤4` 已证（[arXiv:1209.2471](https://arxiv.org/abs/1209.2471)、[期刊版](https://doi.org/10.1007/s40840-017-0592-7)） | 首个未知层为有限简单图 `Δ=5`；证书为图和“不存在 acyclic 7-edge-colouring”的 CNF/DRAT。每边取色、相邻边异色，并要求任意两色诱导子图为森林 | 第一梯队；从连通、`Δ=5, n≥7` 开始，并排除已证的 3-sparse 图 |
| `unsolvedmath-opg-401` | open；[原问题页](https://garden.irmacs.sfu.ca/comment/reply/401)仍列命题，dodecahedron 达到 `20/7` 等号 | 搜 triangle-free planar `Δ≤3` 图；证书包含平面嵌入和“不存在 `(20,7)` circular colouring”的 CNF/DRAT | 第二优先 |
| `unsolvedmath-opg-348` | 未发现解决；[Mohar 问题页](https://www.sfu.ca/~mohar/Problems/P0301FlowPolynomial.html)与[当前题页](https://www.unsolvedmath.com/problems/OPG-348)仍列开放问题 | 显式 2-edge-connected 图及 `Φ(G,11/2)≤0`；用 deletion-contraction/Tutte 递归 DAG 精确计算，统一乘以 2 的幂后验符号 | 第三优先 |
| `unsolvedmath-opg-611` | open；2024 结果只覆盖 `k≤3`（[JGT](https://doi.org/10.1002/jgt.23038)），另有子类进展（[arXiv:2311.13369](https://arxiv.org/abs/2311.13369)） | 固定首个开放参数 `k=4`；证书为最小出度至少 7 的 digraph 和“不存在 4 个点不交有向圈”的 SAT/DRAT | 第四优先；checker 可做，但搜索明显更难 |
| `formal-conjectures-reed-omega-delta-chi-conjecture-for-finite-graphs` | open；[固定版本的 Formal Conjectures 原题](https://github.com/google-deepmind/formal-conjectures/blob/9e126a6e1f7d108ced5904c43cac46b1c39b39cb/FormalConjectures/Paper/ReedOmegaDeltaChi.lean)，[2025 工作](https://arxiv.org/abs/2502.10147)仍称猜想 | 不跑全命题；先跑开放切片 `Δ=6, ω=2`，即找 triangle-free、最大度 6、非 5-colourable 图；用 5-colouring DRAT | 第五优先 |
| `unsolvedmath-kou-21.100` | open（中高置信）；[Kourovka Notebook 第 21 版](https://alglog.org/21tkt.pdf)的新题，近期八题求解工作（[arXiv:2607.17477](https://arxiv.org/abs/2607.17477)）不含此题 | 搜有限群 `A,G` 的 coprime automorphism action；必须独立计算 `C_G(A)`、导群、完整精确特征标表、A-invariance 和 nowhere-zero 计数。异常单个特征标不足以认证计数不等 | 第二梯队；先做 GAP 原型。完整 character-table 与 cyclotomic verifier 未就绪前不进首轮前三 |
| `formal-conjectures-agrawal-conjecture-variants-popovych` | open；[Popovych 原文](https://eprint.iacr.org/2009/008.pdf) | 合数 `n` 的因子、`r`、模条件和两条模多项式恒等式的精确系数向量；checker 很短 | 后备；[Primaboinca](https://www.sopmac.de/primaboinca.html)已有极大范围空搜，发现前景低 |
| `unsolvedmath-opg-165` | 一般形式 open；`r=2,3` 已证，首个开放值是 `r=4`；`ν=1` 对 `r≤5` 已知（[survey](https://arxiv.org/abs/2009.07239)） | 只搜 `r=4, ν≥2`；证书为 4-partite 4-uniform hypergraph，以及匹配数和覆盖数两份 DRAT | 后备；名题、搜索与验证均较重 |
| `unsolvedmath-opg-337` | open/partial；已知结果覆盖若干群族（[arXiv:2107.06969](https://arxiv.org/abs/2107.06969)、[arXiv:2311.02387](https://arxiv.org/abs/2311.02387)、[JCTA 2026](https://doi.org/10.1016/j.jcta.2026.106214)） | 坏序列本身不够；还须独立证明群常数 `s(G)` 的上界，需要全序列 SAT/DP | 降级；证书相关性和搜索代价都高 |
| `unsolvedmath-opg-59994` | **disproved**；Mattiolo–Steffen 明确构造反例（[JGT 2022](https://doi.org/10.1002/jgt.22746)、[arXiv:2001.02484](https://arxiv.org/abs/2001.02484)） | 不再搜索开放反例 | 从开放队列移除；转已知反例 benchmark |
| `unsolvedmath-opg-47028` | **disproved**；Guninski 给出 12 点显式反例（[arXiv:1602.06380](https://arxiv.org/abs/1602.06380)），非 Hamilton 性见 [Locke–Witte](https://arxiv.org/abs/math/9702227) | `H=Cay(Z_12;{2,3,8})`，弧为 `i→i+2,i+3,i+8 (mod 12)`；它是 exact 3-in/3-out、oriented、`12≤4·3+1`，Held–Karp 独立枚举得到 Hamilton 圈数 0。本地题面还把 `d`-regular 误写成“至少 `d`” | 从开放队列移除；转已知反例 benchmark 和状态检测回归样例 |

## 校准后的第一轮启动顺序

1. `unsolvedmath-opg-37271`
2. `unsolvedmath-opg-145`，只跑首个未知层 `Δ=5`
3. `unsolvedmath-opg-401`
4. `unsolvedmath-opg-348`
5. `unsolvedmath-opg-611`，只跑 `k=4`
6. Reed 猜想，只跑 `Δ=6, ω=2`

这一顺序综合了实时开放状态、最小开放切片、生成器压缩率和反例证书强度。自动分数仍保留作全库召回；人工审计顺序用于决定实际算力投放。
