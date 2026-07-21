# Erdős 80 项状态证据、24 项开放冲突与 23 条证明路线复核

> 生成日期：2026-07-19。开放题的新证明或反例默认按待独立审稿候选处理；若已有可复现机器证书，则另行明确标注其证据层级。

## 核验口径

本报告不把数据库标签、论坛评论或 FormalConjectures 中的题面占位符当成证明。论文类证据必须核对原文定理的量词和题面版本；预印本单独标注、不能伪装成已同行评审论文；Lean 类证据必须区分题面形式化与证明代码，并检查 `sorry`、额外公理、依赖缺口和声明匹配。
本轮所谓“80 道非 open”是冻结 cohort 中 `status != open` 的机械集合；其中 `falsifiable` 只表示可由有限计算判定，并不自动表示已经证真或证否，故可能被审计为尚未闭合。
状态元数据取自 [teorth/erdosproblems](https://github.com/teorth/erdosproblems) 固定提交 `aab2deceb51aee0ef28c17d8d194249cbee13d7a`；官网 [FAQ](https://www.erdosproblems.com/faq) 明确提醒数据库未必实时反映全部文献。[FormalConjectures](https://github.com/google-deepmind/formal-conjectures) 是题面形式化/基准集合，仓库说明本就允许没有证明；本轮只把独立可检查的证明文件或证明包计作 Lean 证据。
静态快照核查：38 个带 `(Lean)` 状态的条目中，当前 FormalConjectures 上游能匹配到 26 个同号题面文件；26 个全部仍含 `sorry`，其中 18 个仅通过 `formal_proof` 注解指向外部证明。因此 benchmark 文件本身一律不计作闭合证书。

闭合判定含义：

- `closed_verified`：本轮已找到并核对足以闭合精确题面的证据链。
- `closed_scope_caveat`：主体结论可信，但版本、子问、定义、形式化声明或仅有未评审/条件化证据等存在必须保留的说明。
- `evidence_incomplete`：官方标签可能正确，但公开证据或可复现检查不足，不能独立确认。
- `status_or_statement_mismatch`：状态、字面题面与实际解决对象之间有实质错配。

## 覆盖与结构质检

| 工作流 | 预期 | 已完成 | 缺失 | cohort 外结果 |
|---|---:|---:|---:|---:|
| 已非开放状态证据 | 80 | 80 | 0 | 0 |
| 官方开放冲突 | 24 | 24 | 0 | 0 |
| 优先证明路线 | 23 | 23 | 0 | 0 |

证明路线累计代理墙钟时间 5.83 小时；单题最长 1791.0 秒，硬上限 7200 秒。

## 核心结论摘要

80 条机械意义上的非 `open` 记录中，本轮判为 `closed_verified` 50 条、`closed_scope_caveat` 25 条、`evidence_incomplete` 1 条、`status_or_statement_mismatch` 4 条。

- #114、#488 的 `falsifiable` 不是闭合状态；#358 的现有公开稿有作者已承认、尚待修订的具体缺口；#948 的公开 Lean 源码已在独立 Mathlib v4.28.0 环境编译并通过公理审计，现改判为精确闭合。
- #690 的原普遍单峰猜想已有同行评审反例；所有 k 的完整分类另由 2026 年 arXiv v1 与有限验证器支持，仍保留未评审解析论证的证据层级说明。
- #783 的 `SOLVED` 对应后来修订的渐近版本，不等同于冻结题面的逐个有限 n 精确分类；#1022 的数学与 Lean 证据都在证明否命题，官网 `PROVED (LEAN)` 方向应为 `DISPROVED (LEAN)`。
- 24 条官网仍 `OPEN` 的冲突中，12 条只是字面错误版本已被反驳而意图版本仍开放；#520 的上轮结论引用了不存在的新版，已撤销；#920 很可能是状态同步滞后；#550、#1070 只有近期预印本/计算证书级的新声称。
- #1039 的公开候选解已在两个独立克隆中通过 3316-job Lean 构建，并通过逐式数学复核，得到 log(2)/n≤rho_n≤pi/(2n)；官网主体更新时间早于该材料，仍显示 OPEN/claimed solution。
- #776 得到候选新定理 g(2r+3,r)≤2r−1（r≥4），从而 n₀(r)≥2r+3；证明已由第二位代理逐步复核，并独立重跑 r=4,5 的全部 Z3 轨道和覆盖引理穷举，但它仍是未发表、待外部同行评审的新结果，不是 #776 的完整解答。
- #934 的旧 t=3 精确/渐近路线已被 O₄=KG(7,3) 及其射影平面放大严格证伪；q=7 给出 Δ=32、31920 条坏图边，超过旧猜想允许的 31777 条。该反例已通过独立数学审计和程序重放；原问题的新最优常数上界仍开放。
- #963 经独立核分类审阅与程序重放，严格计算机辅助建立 F(3)=13；同时核实渐近界 f(n)≥(1−o(1))log₂n 已由 KoishiChan 于 2025-12-05 在官方论坛公开，本轮修补了 Γ 与短区间端点。主页仍标 OPEN，且该证明尚无论文、预印本或 Lean 版本。
- #1063 得到并独立复核新下界 D(k)|d_e、primorial 子序列超多项式增长及 k≥3 的 LCM 上界修复；它把候选稀疏化为 n=mD(k)+e，但尚未控制 m，故严格改进统一渐近上界的目标仍开放。

## 第一部分：80 道已非开放题的证据闭合审计

### 判定分布

| 判定 | 数量 |
|---|---:|
| closed_verified | 50 |
| closed_scope_caveat | 25 |
| status_or_statement_mismatch | 4 |
| evidence_incomplete | 1 |

证据层级按题计数（可重叠；同一题可同时有论文、预印本和 Lean）：

| 证据层级 | 题数 |
|---|---:|
| 预印本/公开手稿 | 55 |
| 公开 Lean/形式证明 | 42 |
| 已发表论文/专著 | 26 |
| 其他公开证据 | 5 |
| 公开代码/计算证书 | 2 |

### 总表

| # | 官方状态 | 证据类型 | 闭合判定 | 核心结论 |
|---:|---|---|---|---|
| 38 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_scope_caveat | 公开数学构造与无占位 Lean 主定理闭合了核心的 0<α<1、正长度区间范围；但网页字面量化所有 A、N，而主定理把 α 端点及 N=0 排除在假设外。端点/空区间可由短小的平凡论证补齐，却没有包含在该 Lean 主声明中，因此官方 Lean 标签需保留范围说明。 |
| 42 | solved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 手稿和完整 Lean 证明共同覆盖题面的精确量词与差集条件。 |
| 43 | disproved | 公开 Lean/形式证明, 已发表论文/专著 | closed_verified | 一般式和等势加强式均有反例机制，两个问句都被否定，而不是只处理其中一支。 |
| 90 | disproved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 两份公开预印本给出的 n^1.014 构造已在数学上直接否定原上界；Lean 主路径的静态依赖审计也未见占位或自定义公理，未锁定工具链的复现缺口不改变该反例。 |
| 92 | disproved | 其他公开证据, 预印本/公开手稿 | closed_verified | #90 的固定幂超线性边数经删点给出 f(n)≥n^c 的子序列，足以同时否定题中两个亚多项式上界。 |
| 114 | falsifiable | 公开代码/计算证书, 预印本/公开手稿 | status_or_statement_mismatch | 该题被纳入“已不开放”集合与官网实际状态不符：现有预印本只解决充分大次数，原题仍剩有限但未清零的次数。 |
| 123 | proved (Lean) | 公开 Lean/形式证明, 其他公开证据, 预印本/公开手稿 | closed_scope_caveat | 官网修正版已由公开 Lean 包闭合；冻结题面少了必要假设，不能不加说明地称其字面版本已证。 |
| 125 | disproved (Lean) | 公开 Lean/形式证明 | closed_verified | 官网当前明确采用 positive lower density，公开 Lean 定理严格证明下密度为 0，题面与反证方向完全一致。 |
| 152 | proved | 公开 Lean/形式证明 | closed_verified | 更强的无条件 Lean 定理直接蕴含现行题面，因此状态核实为已闭合。 |
| 190 | solved | 预印本/公开手稿 | closed_scope_caveat | 预印本的下界严格肯定回答了题中特别提出的极限问题，但 frozen 题面首句还要求 Estimate H(k)，而匹配的上界与完整数量级尚未给出；SOLVED 应理解为核心是非问句已解决，而非完整估计已闭合。 |
| 202 | solved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 手稿和完整 Lean 证明都给出同一精确量级，覆盖“估计 H/最大 r”的双侧要求。 |
| 205 | disproved (Lean) | 公开 Lean/形式证明 | closed_verified | 反例构造的唯一外部输入是标准素数渐近，数学上已有定理且还有公开 Lean 实现；它确实否定任意统一慢增长阈值。 |
| 258 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 公开预印本已无条件证明缺失的外部输入，手稿的推导覆盖所有 a_n→∞，故数学问题闭合；但“Lean”应标注为条件化。 |
| 281 | proved (Lean) | 公开 Lean/形式证明, 已发表论文/专著 | closed_verified | 经典已发表定理给出严格数学证明，论坛形式化覆盖统一量词；证据足以确认问题闭合。 |
| 283 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 手稿与无条件形式化都证明了精确现行命题。 |
| 318 | solved | 已发表论文/专著, 预印本/公开手稿 | closed_verified | AP 分支由已发表论文肯定；正密度分支被“只有一个偶数”的正密度集合立即否定；平方分支由公开完整手稿肯定，因此三问均有确定答案。 |
| 320 | solved | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 已接受公开稿给出相匹配的双侧量级，而不是仅一个界，足以回答“Estimate S(N)”。 |
| 321 | solved | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 公开已接受证明给出所求最大基数的正确数量级，并同时提供匹配构造。 |
| 330 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_scope_caveat | 公开手稿与无条件 Lean 主定理闭合了官网附注所采用的正上密度解释；若把正文未限定的 positive density 解读为自然密度存在或正下密度，则当前主声明更弱，必须保留术语范围说明。 |
| 347 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 构造、极限比和删除稳健的密度 1 结论均由手稿和两个 Lean 实现覆盖。 |
| 351 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_scope_caveat | 官网修正版已被手稿和 Lean 证明；漏条件的冻结题面本身为假，必须把修订范围写清。 |
| 358 | proved | 其他公开证据, 预印本/公开手稿 | evidence_incomplete | 现行唯一可访问的完整稿存在具体、被作者承认需修订的证明缺口；在更正版或独立完整证明出现前，不能核实官方 proved 标签。 |
| 369 | proved (Lean) | 公开 Lean/形式证明, 已发表论文/专著 | closed_scope_caveat | 字面版本来就是平凡真命题；有意义的 [N/2,N] 加强版也已公开形式化，所以可记闭合，但必须记录题面歧义。 |
| 380 | proved | 预印本/公开手稿 | closed_verified | 预印本主定理与 B(x) 的定义及目标渐近逐项匹配，没有只证明上界或密度版本。 |
| 387 | solved | 预印本/公开手稿 | closed_verified | 一个最大可用除数为 o(n) 的无限族直接否定“存在绝对 c 对所有 n,k”，量词反驳充分。 |
| 397 | disproved (Lean) | 公开 Lean/形式证明 | closed_verified | 参数化族给出无穷多个合规解，精确否定有限性断言。 |
| 401 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_scope_caveat | 现行 infinitely-many-n 版本由公开手稿闭合，Lean 核验其中固定 r 的主要论证；但“Lean 完整证明”标签过强，且历史上更强量词的命题不同并为假，状态必须绑定到当前解释。 |
| 457 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 手稿和 Lean 共同构造 ε=0.1 的无限族，直接覆盖全部小素数整除条件。 |
| 488 | falsifiable | 公开 Lean/形式证明 | status_or_statement_mismatch | 该题被列入“已不开放”集合与官网 falsifiable/仍开放状态冲突，已有反例只针对另一个命题。 |
| 533 | disproved | 已发表论文/专著 | closed_verified | δ_3(5)=1/12>0 的构造精确产生题面所禁的图族，因此全称断言被严格反驳。 |
| 543 | disproved | 预印本/公开手稿 | closed_verified | 对循环群的无限反例族已经否定全体有限阿贝尔群上的统一渐近上界。 |
| 574 | disproved | 已发表论文/专著 | closed_verified | 在 k=3、k=5 等固定值已有二部构造取得严格更大的主常数；二部性同时排除所禁奇环，故原全称渐近式为假。 |
| 591 | proved | 已发表论文/专著 | closed_verified | 同行评审论文的明确编号定理在参数代入后与原序数分割关系完全相同。 |
| 603 | solved | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 两种可能的原题解释都已有明确答案，所以措辞歧义不会留下未回答分支。 |
| 610 | proved (Lean) | 公开 Lean/形式证明, 已发表论文/专著 | closed_verified | 同行评审的 JMRS 定理已直接蕴含题中更强上界；Kim 构造说明数量级匹配。数学问题闭合，但官方 Lean 标签应注明条件化。 |
| 619 | solved (Lean) | 公开 Lean/形式证明 | closed_verified | 公开 Lean 工程给出统一常数并对任意合规 G 证明严格线性节省，精确回答是非问句。 |
| 650 | solved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 预印本和 Lean 均给出匹配上下界及精确函数，完整解决“估计 f(m)”。 |
| 652 | proved | 已发表论文/专著 | closed_verified | 已发表下界 α_k≫√k 直接且定量地推出所问发散；已有构造保证每个固定 k 的 α_k 有限。 |
| 659 | proved (Lean) | 公开 Lean/形式证明, 已发表论文/专著, 预印本/公开手稿 | closed_verified | Bernays 定理是既有严格数学结果，Grayzel 手稿把它完整应用到符合四点条件的构造，故数学命题已闭合。 |
| 690 | solved | 公开代码/计算证书, 已发表论文/专著, 预印本/公开手稿 | closed_scope_caveat | 原来的全称单峰猜想已经被 Cambie 的同行评审反例严格关闭；所有 k 的更强完整分类则由 2026 年 arXiv v1 与通过的有限验证器支持，但还不是同行评审或端到端形式化结论。 |
| 694 | solved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_scope_caveat | 公开稿和 Lean 声明都覆盖原题的渐近目标，数学方向一致；但稿件未同行评审，Lean 又把关键的 Linnik 输入公理化，故不能把“Lean”标签理解为无条件机器核验了全部解析数论。 |
| 696 | solved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_scope_caveat | 若接受公开稿中的解析数论论证，题目已完整回答且原猜想被否定；目前证据仍是未评审稿及把核心均匀分布定理公理化的 Lean 层。 |
| 705 | disproved | 已发表论文/专著 | closed_verified | O'Donnell 的两篇已发表论文正面构造任意大 girth、染色数 4 的有限平面单位距离图，逐字否定统一 k 的存在。 |
| 729 | proved (Lean) | 公开 Lean/形式证明 | closed_verified | 公开 Lean 文件直接证明原命题，不是只证明有限检查或弱化版本；常数 K 的依赖关系也正确绑定于 C。 |
| 741 | solved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_scope_caveat | 现有工作把常见的两种密度解释都处理了，并肯定回答第二问；保留项来自 frozen 题面本身的术语歧义，而不是证明遗漏。 |
| 750 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_scope_caveat | 手稿覆盖原题全部量词，形式化也匹配；不过论文未同行评审，且 Lean 的关键图论输入仍是自定义公理。 |
| 783 | solved | 预印本/公开手稿 | status_or_statement_mismatch | Tao 的结果严格闭合了预期的渐近极值问题，也说明冻结题面的特定连续素数构造并非精确极小者；但它没有分类每个有限 n 的所有精确极小集合。官网状态依据的是后来修订后的渐近版本。 |
| 793 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_scope_caveat | 常数及误差阶完全匹配原题，范围没有明显缺失；保留意见只在未评审状态和 PNT 被公理化。 |
| 846 | disproved (Lean) | 已发表论文/专著, 预印本/公开手稿 | closed_verified | 已发表结果与直接几何预印本相互印证，恰好同时满足局部线性一般位置子集与全局不可有限着色两个条件。 |
| 847 | disproved | 已发表论文/专著 | closed_verified | 已发表论文的对象、局部比例常数和全局有限分割失败与 frozen 题面逐项一致。 |
| 851 | proved | 其他公开证据, 预印本/公开手稿 | closed_scope_caveat | 公开源码的主定理比 frozen 题面更强，且关键筛法、乘法阶稀疏估计、二阶矩和最终量词均已核对，并有独立专家确认；但当前仍是 AI 生成后修订的公开手稿，尚无预印本版本号或同行评审。 |
| 858 | solved | 预印本/公开手稿 | closed_scope_caveat | 手稿给出上下界匹配的精确常数，确实比早先 o(1) 结论强并覆盖原问题；唯一主要保留是尚未同行评审或形式化。 |
| 863 | proved | 其他公开证据, 已发表论文/专著 | closed_verified | 已发表下界与经典上界给出所有 r≥2 的严格方向 c'_r<c_r，因此 c_r≠c'_r 也随即成立。 |
| 865 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 预印本给出更强的精确渐近，Lean 又以显式常数机器核验题面充分方向，范围和 distinct 条件均匹配。 |
| 868 | solved | 预印本/公开手稿 | closed_scope_caveat | 主定理的表示数下界和“不含任何极小子基”完全对准 frozen 题面；但证据尚为单一公开手稿，未同行评审。 |
| 869 | disproved | 预印本/公开手稿 | closed_scope_caveat | 公开手稿包含逐字反例，且本次已定位到推导 P2 真/P3 假的章节；尚缺同行评审或形式化的第二层验证。 |
| 871 | disproved (Lean) | 预印本/公开手稿 | closed_scope_caveat | 数学手稿的两个主定理直接构成所需反例；保留意见是手稿未评审以及官方 Lean 标签缺乏可核链接。 |
| 884 | disproved (Lean) | 预印本/公开手稿 | closed_scope_caveat | 无条件手稿的主定理与原不等式逻辑等价，范围无缺失；但尚无同行评审及可复现 Lean 证据。 |
| 888 | solved | 预印本/公开手稿 | closed_scope_caveat | 手稿同时给出匹配到常数因子的上下界，闭合了题目要求的数量级；证据成熟度仅为公开手稿。 |
| 896 | solved | 已发表论文/专著, 预印本/公开手稿 | closed_scope_caveat | 已发表深定理与新公开稿组合给出匹配数量级；但真正补齐本题下界的部分尚未同行评审。 |
| 948 | solved | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 公开 Lean 证明已独立编译、公理审计通过，并完整否定原存在性命题：任意候选 f、k≥2 都有一个着色，使每条满足增长条件的序列之非空有限和命中所有颜色。因此官网 SOLVED 标签有可核实的精确闭合证据。 |
| 960 | disproved | 预印本/公开手稿 | closed_scope_caveat | 预印本在允许参数范围内给出二次量级反例，严格证否了题中特别提出的普遍 o(n²) 猜想；但 frozen 题面首句还要求估计各固定 r,k 的 f_{r,k}(n)，该总体阈值问题没有闭合，因此 DISPROVED 只能理解为猜想方向而非整条复合问题已解决。 |
| 965 | disproved | 已发表论文/专著 | closed_verified | Komjáth 的已发表 ZFC 定理比题面更强，不依赖连续统假设，直接给出一个反例着色。 |
| 986 | proved | 预印本/公开手稿 | closed_verified | 预印本的指数、固定参数与常数依赖完全匹配，并给出明确对数幂，严格强于“存在某 c(k)>0”。 |
| 987 | proved | 已发表论文/专著, 预印本/公开手稿 | closed_verified | 第一问由经典已发表论文闭合，第二问由新预印本给出满足全体 k 的显式渐近控制，两部分合在一起覆盖完整 frozen 题面。 |
| 990 | disproved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 预印本的反例机制与无公理 Lean 族声明相互核对，恰好击穿 frozen 的统一 O 界。 |
| 992 | disproved | 已发表论文/专著 | closed_verified | 已发表论文给出同一 discrepancy 定义下的几乎处处反例序列，直接否定两种上界。 |
| 997 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_scope_caveat | 数学预印本覆盖所有 α，量词精确；Lean 证据尚把核心深定理公理化，因此官方“Lean”需附此限定。 |
| 1014 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 公开论文证明与无新增公理的 Lean 文件双重覆盖完整极限陈述。 |
| 1021 | proved | 已发表论文/专著 | closed_verified | 两篇同行评审论文给出比题面更明确的正指数节省，且 G_k 的图同构就是 K_k 的 1-细分。 |
| 1022 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | status_or_statement_mismatch | 数学上原命题已被严格证否，并有公开 Lean 反命题；错误在官方状态方向，应从 PROVED 改为 DISPROVED。 |
| 1044 | solved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_verified | 公开数学证明和完整 Lean 主声明均给出同一精确数值 2，范围匹配。 |
| 1051 | proved (Lean) | 公开 Lean/形式证明, 预印本/公开手稿 | closed_scope_caveat | 论文足以处理通常所指的正整数版本，一般整数版本也可用最终正性和有限有理前缀作短归约；但官方“Lean”严格说只形式化了正自然数范围。 |
| 1071 | proved (Lean) | 公开 Lean/形式证明 | closed_verified | 两条存在性问句均有独立的公开 Lean 主声明，区域、有限/可数、极大性量词均匹配。 |
| 1089 | solved | 已发表论文/专著, 预印本/公开手稿 | closed_verified | 记 M_d(n−1) 为 d 维至多 n−1 种距离集合的最大大小，则 g_d(n)=M_d(n−1)+1，且 binom(d+1,n−1)+1≤g_d(n)≤binom(d+n−1,n−1)+1。固定 n≥2 时两界给出极限 1/(n−1)!；n=1 时 g_d(1)=2。 |
| 1091 | solved | 已发表论文/专著, 预印本/公开手稿 | closed_verified | 第一问有经典同行评审肯定证明，第二问有精确参数反例；两部分方向不同但共同构成 SOLVED。 |
| 1092 | disproved | 已发表论文/专著 | closed_verified | 同行评审构造甚至以 o(m) 误差满足局部近二分性，却有高全局染色数，严格击穿首问和“对所有 r”的一般命题。 |
| 1096 | proved | 已发表论文/专著 | closed_verified | 已发表论文给出一个统一开放区间内的完整极限，而不是仅 liminf=0，正好提供题面所需的“充分小 ε”。 |
| 1105 | proved | 已发表论文/专著, 预印本/公开手稿 | closed_scope_caveat | 环部分已有同行评审精确定理；路径部分的公开预印本量词和公式均匹配，但官网仍称 announced，未核到正式期刊版本。 |
| 1119 | independent | 已发表论文/专著 | closed_verified | 两篇同行评审工作在相同临界基数配置下分别给出肯定和否定模型，足以证明题目在 ZFC 中独立；当 m^+<c 时的 ZFC 肯定结论也与此兼容。 |

### 逐题证据记录

#### #38

- 官方状态：`proved (Lean)`
- 精确题面：Does there exist $B\subset\mathbb{N}$ which is not an additive basis, but is such that for every set $A\subseteq\mathbb{N}$ of Schnirelmann density $\alpha$ and every $N$ there exists $b\in B$ such that\[\lvert (A\cup (A+b))\cap \{1,\ldots,N\}\rvert\geq (\alpha+f(\alpha))N\]where $f(\alpha)>0$ for $0<\alpha <1 $? The Schnirelmann density is defined by\[d_s(A) = \inf_{N\geq 1}\frac{\lvert A\cap\{1,\ldots,N\}\rvert}{N}.\]
- 范围解释：要求构造一个不是加法基的 B⊂ℕ；对任意 Schnirelmann 密度 α∈(0,1) 的 A 和任意 N，某个平移 b∈B 都使 A∪(A+b) 在 [1,N] 中至少增密 f(α)N。
- 闭合判定：`closed_scope_caveat`
- 判定理由：公开数学构造与无占位 Lean 主定理闭合了核心的 0<α<1、正长度区间范围；但网页字面量化所有 A、N，而主定理把 α 端点及 N=0 排除在假设外。端点/空区间可由短小的平凡论证补齐，却没有包含在该 Lean 主声明中，因此官方 Lean 标签需保留范围说明。
- Lean 审计：存在公开、可定位到具体声明且无占位/新增公理的 Lean 文件；核心定理排除了 α=0、α=1 与 N=0 的边界。FormalConjectures 快照中的题面文件仅含 sorry，未被当作证明证据。
- 尚存不确定性：应在形式化中显式补上 α=0、α=1 与 N=0 的分支，并在 mathlib-v4.28.0 固定工具链下重新编译；当前风险是声明边界而非核心构造。
- 证据：

  - `official_page` [Erdős Problem #38](https://www.erdosproblems.com/38)；发表状态：official_database；核验：题页标记 proved (Lean)，并把问题表述为对全部 A、N 和 0<α<1 的统一存在性命题。
  - `public_manuscript` [Erdős 38 manuscript repository](https://github.com/spicylemonade/erdos-38)；发表状态：public_repository；核验：仓库公开给出构造与数学论证，可与形式化定理的参数范围相互核对。
  - `public_lean` [Erdos38.lean](https://live.lean-lang.org/#project=mathlib-v4.28.0&url=https://gist.githubusercontent.com/madeve-unipi/690d2bd8f6e8304ba8b456f9db559747/raw/481e3c35de8dce7af70ec440e4e121f084a61860/Erdos38.lean)；发表状态：public_formalization；核验：检查了 1852 行源文件：主定理名为 erdos_problem_38，未出现 sorry、admit 或自定义 axiom，核心构造与非加法基结论吻合；但主声明显式假设 0<α<1 及正的区间参数，没有把网页字面端点分支并入同一定理。

#### #42

- 官方状态：`solved (Lean)`
- 精确题面：Let $M\geq 1$ and $N$ be sufficiently large in terms of $M$. Is it true that for every Sidon set $A\subset \{1,\ldots,N\}$ there is another Sidon set $B\subset \{1,\ldots,N\}$ of size $M$ such that $(A-A)\cap(B-B)=\{0\}$?
- 范围解释：对每个固定 M≥1，当 N 充分大时，每个 [N] 内 Sidon 集 A 都能找到大小 M 的 Sidon 集 B，使 (A−A)∩(B−B)={0}。
- 闭合判定：`closed_verified`
- 判定理由：手稿和完整 Lean 证明共同覆盖题面的精确量词与差集条件。
- Lean 审计：公开仓库中有具体主声明和公理打印；本机编译成功，静态扫描未见未消解证明洞。
- 尚存不确定性：未确认手稿的同行评审发表状态；Lean 主结论已经本机核验。
- 证据：

  - `official_page` [Erdős Problem #42](https://www.erdosproblems.com/42)；发表状态：official_database；核验：题页标记 solved (Lean)，量词次序为先固定 M、再令 N 充分大、最后对任意 A。
  - `public_manuscript` [A note on Erdős Problem 42](https://www.ulam.ai/research/erdos42-note.pdf)；发表状态：public_manuscript；核验：正文给出满足互异差集条件的构造与充分大 N 的定量控制。
  - `public_lean` [Erdos/P42/CompactCayley/Proof.lean](https://github.com/Shashi456/erdos-formalizations/blob/286f856aa3fc08957b80950fd18a45aab8d045ea/Erdos/P42/CompactCayley/Proof.lean)；发表状态：public_formalization；核验：检查约 1.48 万行并在本机成功编译：没有 sorry、admit 或自定义 axiom；最终定理覆盖任意 M 与充分大 N 的原题，#print axioms 仅含 propext、Classical.choice、Quot.sound。

#### #43

- 官方状态：`disproved`
- 精确题面：If $A,B\subset \{1,\ldots,N\}$ are two Sidon sets such that $(A-A)\cap(B-B)=\{0\}$ then is it true that\[ \binom{\lvert A\rvert}{2}+\binom{\lvert B\rvert}{2}\leq\binom{f(N)}{2}+O(1),\]where $f(N)$ is the maximum possible size of a Sidon set in $\{1,\ldots,N\}$? If $\lvert A\rvert=\lvert B\rvert$ then can this bound be improved to\[\binom{\lvert A\rvert}{2}+\binom{\lvert B\rvert}{2}\leq (1-c+o(1))\binom{f(N)}{2}\]for some constant $c>0$?
- 范围解释：问题含两部分：一般两个差集仅交于 0 的 Sidon 集是否满足以最大 Sidon 大小 f(N) 为基准的 O(1) 上界；等势时能否再节省固定比例。
- 闭合判定：`closed_verified`
- 判定理由：一般式和等势加强式均有反例机制，两个问句都被否定，而不是只处理其中一支。
- Lean 审计：论坛公开了形式化代码，但本次没有获得一个可独立克隆、带锁定依赖的完整工程；闭合判断主要依赖已发表 Bose–Chowla 构造和可复核的 #42 推论。
- 尚存不确定性：论坛 Lean 片段的端到端重编译尚未独立完成，但不影响经典已发表构造给出的数学反例。
- 证据：

  - `official_page` [Erdős Problem #43](https://www.erdosproblems.com/43)；发表状态：official_database；核验：题页将整条标记为 disproved，并区分一般式与 |A|=|B| 的加强式。
  - `published_paper` [Bose–Chowla Sidon-set construction](https://link.springer.com/article/10.1007/BF02566968)；发表状态：peer_reviewed；核验：经典有限域构造产生等势、交叉差互异的集合族；代入可使加强式所要求的固定比例缺口不存在。
  - `public_formal_argument` [Erdős Problem #43 forum proof](https://www.erdosproblems.com/forum/thread/43#post-2354)；发表状态：public_repository_post；核验：公开帖子给出 Bose–Chowla 构造的 Lean 形式化与参数核对；一般式也由 #42 对最大 Sidon 集附加任意固定大小 B 直接否定。

#### #90

- 官方状态：`disproved (Lean)`
- 精确题面：Does every set of $n$ distinct points in $\mathbb{R}^2$ contain at most $n^{1+O(1/\log\log n)}$ many pairs which are distance 1 apart?
- 范围解释：断言任意 n 个平面点的单位距离对数至多 n^(1+O(1/log log n))；反驳需构造固定幂指数大于 1 的无限族。
- 闭合判定：`closed_verified`
- 判定理由：两份公开预印本给出的 n^1.014 构造已在数学上直接否定原上界；Lean 主路径的静态依赖审计也未见占位或自定义公理，未锁定工具链的复现缺口不改变该反例。
- Lean 审计：静态递归依赖闭包未发现占位或自定义公理，且确认仓库中的显式公理位于不可达旁支；但仓库未提供本次可锁定复现的 lake 工程，尚未完成固定工具链下的整库编译与 #print axioms。Lean 仍作为强佐证，数学闭合并不只依赖它。
- 尚存不确定性：预印本尚未确认期刊审稿状态；Lean 仍宜在带锁文件的固定工具链下整库编译并打印最终定理公理，以补齐可复现性审计。
- 证据：

  - `official_page` [Erdős Problem #90](https://www.erdosproblems.com/90)；发表状态：official_database；核验：题页标记 disproved (Lean)，并链接机器辅助的单位距离反例证明。
  - `preprint` [An explicit lower bound for the unit distance problem](https://arxiv.org/abs/2605.20579)；发表状态：arxiv_preprint；核验：Sawin 构造给出多于 n^1.014 的单位距离，固定指数 0.014 直接超过题设的 O(1/log log n) 余量。
  - `preprint` [Remarks on the disproof of the unit distance conjecture](https://arxiv.org/abs/2605.20695)；发表状态：arxiv_preprint；核验：独立整理了参数、有限搜索证书与从局部数据到渐近反例的推导。
  - `public_lean` [Erdos90](https://github.com/plby/Erdos90/)；发表状态：public_formalization；核验：目标声明 Submission.erdos_unit_distance_conjecture_false 中无 sorry；Challenge 文件的 sorry 是待证题面。递归扫描该声明可达的 1423 个仓库 Lean 文件，未见 sorry、admit 或自定义 axiom；仓库中的三个 TensorAcyclicity 公理模块不在主声明的 import 闭包内。

#### #92

- 官方状态：`disproved`
- 精确题面：Let $f(n)$ be maximal such that there exists a set $A$ of $n$ points in $\mathbb{R}^2$ in which every $x\in A$ has at least $f(n)$ points in $A$ equidistant from $x$. Is it true that $f(n)\leq n^{o(1)}$? Or even $f(n) < n^{O(1/\log\log n)}$?
- 范围解释：f(n) 是可实现的最大最小等距邻居数；问题问 f(n) 是否为 n^o(1)，甚至是否小于 n^(O(1/log log n))。
- 闭合判定：`closed_verified`
- 判定理由：#90 的固定幂超线性边数经删点给出 f(n)≥n^c 的子序列，足以同时否定题中两个亚多项式上界。
- Lean 审计：未找到针对 #92 最小度推论的独立完整 Lean 文件；其关键删点引理是有限图的标准平均度论证，数学闭合不依赖形式化标签。
- 尚存不确定性：指数在取诱导子图、重新记顶点数时会改变常数，但仍保持某个固定 c>0；无需精确最优指数。
- 证据：

  - `official_page` [Erdős Problem #92](https://www.erdosproblems.com/92)；发表状态：official_database；核验：题页标为 disproved，并把结论关联到单位距离图的最新超线性构造。
  - `preprint` [Unit distances with more than n^1.014 edges](https://arxiv.org/abs/2605.20579)；发表状态：arxiv_preprint；核验：#90 的点集产生平均度 n^0.014 量级的单位距离图。反复删去低于平均度一半的顶点，得到非空诱导子图，其最小单位距离度仍为固定正幂。
  - `public_discussion` [Erdős Problem #92 forum](https://www.erdosproblems.com/forum/thread/92)；发表状态：public_mathematical_record；核验：公开讨论核对了从超线性单位距离边数到高最小度子图、再到 f(n) 下界的标准删点论证。

#### #114

- 官方状态：`falsifiable`
- 精确题面：If $p(z)\in\mathbb{C}[z]$ is a monic polynomial of degree $n$ then is the length of the curve $\{ z\in \mathbb{C} : \lvert p(z)\rvert=1\}$ maximised when $p(z)=z^n-1$?
- 范围解释：对每个次数 n，问所有首一复多项式的 |p(z)|=1 lemniscate 长度是否都由 z^n−1 最大化；需要覆盖每个有限 n，而非只证 n 充分大。
- 闭合判定：`status_or_statement_mismatch`
- 判定理由：该题被纳入“已不开放”集合与官网实际状态不符：现有预印本只解决充分大次数，原题仍剩有限但未清零的次数。
- Lean 审计：未找到闭合原题全部次数的公开 Lean 定理；实验代码不能替代误差有界的形式证明。
- 尚存不确定性：需列出 Tao 阈值以下尚未由既有低次数论文覆盖的 n，并逐一给出解析证明或严格区间算术证书。
- 证据：

  - `official_page` [Erdős Problem #114](https://www.erdosproblems.com/114)；发表状态：official_database；核验：状态为 falsifiable，而非 proved/disproved；该标签表示问题仍开放但每个固定次数原则上可有限检验。
  - `preprint` [On the Erdős lemniscate conjecture](https://arxiv.org/abs/2512.12455)；发表状态：arxiv_preprint；核验：Tao 证明 z^n−1 对所有充分大的 n 是唯一极大者；这把开放部分缩成有限多个低次数，但没有逐一处置全部剩余次数。
  - `public_code` [EHP conjecture 114 experiments](https://github.com/MendozaLab/erdos-experiments/tree/main/papers/ehp-conjecture-114)；发表状态：public_experimental_repository；核验：仓库提供低次数数值实验，而非覆盖全部剩余次数的严格证书。

#### #123

- 官方状态：`proved (Lean)`
- 精确题面：Let $a,b,c$ be three integers which are pairwise coprime. Is every large integer the sum of distinct integers of the form $a^kb^lc^m$ ($k,l,m\geq 0$), none of which divide any other?
- 范围解释：现行修正版要求 a,b,c>1 且两两互素；每个充分大整数都能写成若干互不整除的不同 a^k b^l c^m 之和。冻结题面漏写 >1，按字面取 (1,1,1) 会为假。
- 闭合判定：`closed_scope_caveat`
- 判定理由：官网修正版已由公开 Lean 包闭合；冻结题面少了必要假设，不能不加说明地称其字面版本已证。
- Lean 审计：验证包给出精确主声明、无占位，公理集合只有 mathlib 常规逻辑公理；但它证明的是现行 a,b,c>1 版本，不是冻结快照漏条件的字面版本。
- 尚存不确定性：应在汇总报告中以现行题页为准，并显式记录冻结语料的转录缺项。
- 证据：

  - `official_page` [Erdős Problem #123](https://www.erdosproblems.com/123)；发表状态：official_database；核验：现行页面已加入 a,b,c>1；这是证明实际覆盖且命题成立所必需的边界条件。
  - `accepted_proof_claim` [Starfleet solution claim for Erdős 123](https://www.starfleetmath.com/solutions/8f5a1e07-50cb-45fc-94d4-dd64980e137e)；发表状态：accepted_by_site；核验：已接受条目明确陈述修正版条件，并提供可下载验证包。
  - `public_lean_bundle` [erdos-123-solution.zip](https://www.starfleetmath.com/downloads/verify/erdos-123/erdos-123-solution.zip)；发表状态：public_formalization；核验：解包检查主定理 Erdos123.erdos_123 : IntendedStatement；无 sorry/admit，自报告公理仅 propext、Classical.choice、Quot.sound，且声明含 >1。
  - `public_summary` [Erdős Problem 123 proof summary](http://www.thomasbloom.org/erdos123.pdf)；发表状态：public_manuscript；核验：摘要解释互不整除表示的数学构造及为何需排除底数 1。

#### #125

- 官方状态：`disproved (Lean)`
- 精确题面：Let $A = \{ \sum\epsilon_k3^k : \epsilon_k\in \{0,1\}\}$ be the set of integers which have only the digits $0,1$ when written base $3$, and $B=\{ \sum\epsilon_k4^k : \epsilon_k\in \{0,1\}\}$ be the set of integers which have only the digits $0,1$ when written base $4$. Does $A+B$ have positive density?
- 范围解释：A、B 分别是三进制和四进制仅含 0/1 数位的整数集；官网现行题面明确问 A+B 是否具有正下自然密度，公开 Lean 反例证明其下密度为 0。
- 闭合判定：`closed_verified`
- 判定理由：官网当前明确采用 positive lower density，公开 Lean 定理严格证明下密度为 0，题面与反证方向完全一致。
- Lean 审计：定理 erdos_125.variants.positive_lower_density 无占位，精确覆盖官网现行的正下密度问句；同文件中另有含 sorry 的正上密度变体，但它不是当前题面，不能反过来削弱本题证否。
- 尚存不确定性：若研究历史上可能提出的正上密度变体，应另立条目；它不影响现行 #125 已证否。
- 证据：

  - `official_page` [Erdős Problem #125](https://www.erdosproblems.com/125)；发表状态：official_database；核验：题页标记 disproved (Lean)，现行正文明确写 positive lower density；因此不存在把本题解释成正上密度的当前范围歧义。
  - `public_lean` [FormalConjectures/ErdosProblems/125.lean (counterexample fork)](https://github.com/mo271/formal-conjectures/blob/c27415379b5dbe34105d1fdd707994540c4c6fc7/FormalConjectures/ErdosProblems/125.lean#L468)；发表状态：public_formalization；核验：定理 erdos_125.variants.positive_lower_density 无 sorry，借由 lower_density_zero 严格证明下密度为 0；同文件的总题面和正上密度变体仍含 sorry。

#### #152

- 官方状态：`proved`
- 精确题面：For any $M\geq 1$, if $A\subset \mathbb{N}$ is a sufficiently large finite Sidon set then there are at least $M$ many $a\in A+A$ such that $a+1,a-1\not\in A+A$.
- 范围解释：任意 M 固定后，所有足够大的有限 Sidon 集 A，其和集 A+A 中至少有 M 个元素，两侧相邻整数都不再属于 A+A。
- 闭合判定：`closed_verified`
- 判定理由：更强的无条件 Lean 定理直接蕴含现行题面，因此状态核实为已闭合。
- Lean 审计：公开固定提交中的主定理无占位且范围更强；原始 FormalConjectures 基准快照的 sorry 未被当作证据。
- 尚存不确定性：未核实该证明是否另有期刊版本；闭合本身由公开内核可检验证明支撑。
- 证据：

  - `official_page` [Erdős Problem #152](https://www.erdosproblems.com/152)；发表状态：official_database；核验：题页标记 proved，条件是 A 的基数充分大，而非元素上界充分大。
  - `public_lean` [FormalConjectures/ErdosProblems/152.lean (proof fork)](https://github.com/mo271/formal-conjectures/blob/ff58c933d53bb807bf85d98a47402703f9f14ed3/FormalConjectures/ErdosProblems/152.lean#L496)；发表状态：public_formalization；核验：最终定理 erdos_152 无 sorry、admit 或 axiom，并证明比只需 M 个孤立和更强的定量下界。

#### #190

- 官方状态：`solved`
- 精确题面：Let $H(k)$ be the smallest $N$ such that in any finite colouring of $\{1,\ldots,N\}$ (into any number of colours) there is always either a monochromatic $k$-term arithmetic progression or a rainbow arithmetic progression (i.e. all elements are different colours). Estimate $H(k)$. Is it true that\[H(k)^{1/k}/k \to \infty\]as $k\to\infty$?
- 范围解释：H(k) 是任意有限着色 [N] 必有单色或彩虹 k 项等差数列的最小 N；重点问 H(k)^(1/k)/k 是否趋于无穷。
- 闭合判定：`closed_scope_caveat`
- 判定理由：预印本的下界严格肯定回答了题中特别提出的极限问题，但 frozen 题面首句还要求 Estimate H(k)，而匹配的上界与完整数量级尚未给出；SOLVED 应理解为核心是非问句已解决，而非完整估计已闭合。
- Lean 审计：未找到公开 Lean 证明；核验依据为可公开读取的完整预印本，而非只有摘要或新闻。
- 尚存不确定性：仍需匹配上界或更精确的 H(k) 数量级；截至核验日下界论文也只确认预印本状态。
- 证据：

  - `official_page` [Erdős Problem #190](https://www.erdosproblems.com/190)；发表状态：official_database；核验：题页标记 solved，最新结果给出比目标极限更直接的渐近下界。
  - `preprint` [Anti-van der Waerden/Ramsey growth for arithmetic progressions](https://arxiv.org/abs/2604.20588)；发表状态：arxiv_preprint；核验：Bae 证明 H(k)^(1/k)/k = Ω(k/log k)，右侧趋于无穷，精确回答题中极限问句。

#### #202

- 官方状态：`solved (Lean)`
- 精确题面：Let $n_1<\cdots < n_r\leq N$ with associated $a_i\pmod{n_i}$ such that the congruence classes are disjoint (that is, every integer is $\equiv a_i\pmod{n_i}$ for at most one $1\leq i\leq r$). How large can $r$ be in terms of $N$?
- 范围解释：互不相交的剩余类 a_i mod n_i，模数严格递增且 n_i≤N；求可取类数 r 的最大量级。
- 闭合判定：`closed_verified`
- 判定理由：手稿和完整 Lean 证明都给出同一精确量级，覆盖“估计 H/最大 r”的双侧要求。
- Lean 审计：公开完整工程、具体主声明、无占位且有公理打印；本机编译成功，没有发现把解析数论主步骤公理化的接口。
- 尚存不确定性：尚未确认期刊发表；Lean 主结论已经本机核验。
- 证据：

  - `official_page` [Erdős Problem #202](https://www.erdosproblems.com/202)；发表状态：official_database；核验：题页标记 solved (Lean)，答案的对数渐近写成 x exp(-(1+o(1))√(log x log log x)) 型。
  - `public_manuscript` [Erdős Problem 202](https://boonsuan.github.io/erdos202.pdf)；发表状态：public_manuscript；核验：手稿证明最大 r 的精确对数阶，包含上、下界而非只给一侧估计。
  - `public_lean` [Erdos/P202/Proof.lean](https://github.com/Shashi456/erdos-formalizations/blob/286f856aa3fc08957b80950fd18a45aab8d045ea/Erdos/P202/Proof.lean)；发表状态：public_formalization；核验：检查约 2.17 万行并在本机成功编译：无 sorry、admit、自定义 axiom；主定理 Erdos202.erdos202_main 形式化完整渐近结论，#print axioms 仅含 propext、Classical.choice、Quot.sound。

#### #205

- 官方状态：`disproved (Lean)`
- 精确题面：Is it true that all sufficiently large $n$ can be written as $2^k+m$ for some $k\geq 0$, where $\Omega(m)<\log\log m$? What about $\Omega(m)<\epsilon\log\log m$, or another more slowly growing bound?
- 范围解释：问所有充分大 n 是否可写成 2^k+m，且 Ω(m) 小于 log log m、εlog log m，或某个更慢趋于无穷的统一阈值。
- 闭合判定：`closed_verified`
- 判定理由：反例构造的唯一外部输入是标准素数渐近，数学上已有定理且还有公开 Lean 实现；它确实否定任意统一慢增长阈值。
- Lean 审计：Lean 文件是条件化证明：无 sorry，但依赖自定义公理 nth_prime_asymp。公理陈述有外部正式证明可用，仍不能把当前文件描述成零自定义公理的端到端证明。
- 尚存不确定性：需将 PNT 工程中的已证定理替换自定义 axiom 并重新 #print axioms，才能严格支持官方的“Lean”强标签。
- 证据：

  - `official_page` [Erdős Problem #205](https://www.erdosproblems.com/205)；发表状态：official_database；核验：题页标记 disproved (Lean)，反例族针对任意候选慢增长界，而非只否定某个 ε。
  - `public_lean` [Erdos205.lean](https://github.com/plby/lean-proofs/blob/main/src/v4.24.0/ErdosProblems/Erdos205.lean)；发表状态：conditional_formalization；核验：源文件无 sorry，但显式声明 axiom nth_prime_asymp；其余构造形式化出无穷多个偶数 n，使每个 n−2^k 都有许多素因子。
  - `public_lean_dependency` [PrimeNumberTheoremAnd consequences](https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/blob/a873d22b583e33f362e2820922468c099d848752/PrimeNumberTheoremAnd/Consequences.lean#L1199-L1208)；发表状态：public_formalization；核验：该工程已有可替代 nth_prime_asymp 的标准 PNT 推论，说明公理内容是已知定理，但当前 #205 文件尚未接线消去公理。

#### #258

- 官方状态：`proved (Lean)`
- 精确题面：Let $a_1,a_2,\ldots$ be a sequence of integers with $a_n\to \infty$. Is\[\sum_{n} \frac{\tau(n)}{a_1\cdots a_n}\]irrational, where $\tau(n)$ is the number of divisors of $n$?
- 范围解释：对任意整数序列 a_n→∞，级数 Σ τ(n)/(a_1⋯a_n) 都是无理数。
- 闭合判定：`closed_verified`
- 判定理由：公开预印本已无条件证明缺失的外部输入，手稿的推导覆盖所有 a_n→∞，故数学问题闭合；但“Lean”应标注为条件化。
- Lean 审计：并非端到端 Lean 证明：核心最新数论定理被一个明确 sorry 作为接口；其余从该定理到原题的推导完整。
- 尚存不确定性：需要把 Tao–Teräväinen 定理正式化或作为经过审核的库定理导入，才可称完整内核验证。
- 证据：

  - `official_page` [Erdős Problem #258](https://www.erdosproblems.com/258)；发表状态：official_database；核验：题页标记 proved (Lean)，证明使用关于连续整数素因子个数的最新结果。
  - `public_manuscript` [A proof of Erdős Problem 258](https://www.ulam.ai/research/erdos258.pdf)；发表状态：public_manuscript；核验：手稿把 Tao–Teräväinen 的连续整数 Ω 上界转化为 τ(N+k)≤2^(Ck)，再用 Cantor 型尾项论证无理性。
  - `preprint` [Simultaneous bounds for prime factors of consecutive integers](https://arxiv.org/abs/2512.01739)；发表状态：arxiv_preprint；核验：定理 1.1 提供无穷多个 N，使所有固定偏移 k 满足 Ω(N+k)≤Ck，正是无理性证明的外部数论输入。
  - `public_lean_bundle` [erdos258.tar.gz](https://www.ulam.ai/research/erdos258.tar.gz)；发表状态：conditional_formalization；核验：Erdos258.Main.lean 中尾项与无理性推导已形式化，但 tao_teravaeinen 恰有一个 sorry；主定理依赖该占位。

#### #281

- 官方状态：`proved (Lean)`
- 精确题面：Let $n_1<n_2<\cdots$ be an infinite sequence such that, for any choice of congruence classes $a_i\pmod{n_i}$, the set of integers not satisfying any of the congruences $a_i\pmod{n_i}$ has density $0$. Is it true that for every $\epsilon>0$ there exists some $k$ such that, for every choice of congruence classes $a_i$, the density of integers not satisfying any of the congruences $a_i\pmod{n_i}$ for $1\leq i\leq k$ is less than $\epsilon$?
- 范围解释：若任意选择无限个剩余类后未覆盖整数集都密度 0，问对每个 ε 是否存在统一有限前缀 k，使任意选择前 k 个剩余类后未覆盖密度都小于 ε。
- 闭合判定：`closed_verified`
- 判定理由：经典已发表定理给出严格数学证明，论坛形式化覆盖统一量词；证据足以确认问题闭合。
- Lean 审计：形式化以论坛嵌入代码公开，未取得常规可克隆仓库和锁文件做独立静态全树扫描；FormalConjectures 主线题面仍是 sorry，不能替代论坛证明。
- 尚存不确定性：建议将 live.lean 内容迁入版本固定仓库并记录 #print axioms，以提升“Lean”标签的长期可复现性。
- 证据：

  - `official_page` [Erdős Problem #281](https://www.erdosproblems.com/281)；发表状态：official_database；核验：题页标记 proved (Lean)，结论的关键是 k 对所有剩余类选择统一。
  - `published_paper` [Davenport–Erdős density theorem](https://users.renyi.hu/~p_erdos/1936-04.pdf)；发表状态：peer_reviewed_classical_paper；核验：经典密度定理提供无限并集与有限前缀密度极限之间的必要连续性。
  - `published_monograph` [Sequences (Halberstam–Roth), Rogers covering theorem source](https://jayyhk.github.io/papers/halberstam-roth1966.pdf)；发表状态：published_monograph；核验：Rogers 型紧致性/覆盖结果给出对所有剩余类选择一致的有限截断。
  - `public_lean` [Erdős Problem #281 forum formal proof](https://www.erdosproblems.com/forum/thread/281)；发表状态：public_formalization_post；核验：论坛嵌入 live.lean 完整代码并定位 Erdos281 主定理；公开记录称其在指定 mathlib 环境通过类型检查。

#### #283

- 官方状态：`proved (Lean)`
- 精确题面：Let $p:\mathbb{Z}\to \mathbb{Z}$ be a polynomial whose leading coefficient is positive and such that there exists no $d\geq 2$ with $d\mid p(n)$ for all $n\geq 1$. Is it true that, for all sufficiently large $m$, there exist integers $1\leq n_1<\cdots <n_k$ such that\[1=\frac{1}{n_1}+\cdots+\frac{1}{n_k}\]and\[m=p(n_1)+\cdots+p(n_k)?\]
- 范围解释：整数值多项式 p 具有正首项系数且无固定除数 d≥2；对每个充分大 m，要有 Egyptian fraction 1=Σ1/n_i，同时 m=Σp(n_i)。
- 闭合判定：`closed_verified`
- 判定理由：手稿与无条件形式化都证明了精确现行命题。
- Lean 审计：公开扁平化 Lean 文件无占位或自定义公理，主声明覆盖充分大 m 的量词。
- 尚存不确定性：未确认同行评审发表；Lean 文件已在本机编译，但本轮未另行记录最终定理的 #print axioms 输出。
- 证据：

  - `official_page` [Erdős Problem #283](https://www.erdosproblems.com/283)；发表状态：official_database；核验：题页标记 proved (Lean)，现行条件明确包括正首项系数与无固定除数。
  - `public_manuscript` [Updated proof manuscript for Erdős 283/351](https://drive.google.com/file/d/1cW2Z7vpTjLQ2Wf6SMb6_nbO9JYlfznnt/view)；发表状态：public_manuscript；核验：手稿给出同时控制倒数和与多项式值和的构造，并覆盖整数值多项式的现行范围。
  - `public_lean` [Erdos/P283/Proof_flat.lean](https://github.com/Shashi456/erdos-formalizations/blob/0b83dba5ac2a87839e9281e13afd1a217d6210a3/Erdos/P283/Proof_flat.lean)；发表状态：public_formalization；核验：静态检查未见实际 sorry、admit 或自定义 axiom，本机编译成功；主定理 Erdos283.erdos_283 的假设和两个同时等式均与题面吻合。

#### #318

- 官方状态：`solved`
- 精确题面：Let $A\subseteq \mathbb{N}$ be an infinite arithmetic progression and $f:A\to \{-1,1\}$ be a non-constant function. Must there exist a finite non-empty $S\subset A$ such that\[\sum_{n\in S}\frac{f(n)}{n}=0?\]What about if $A$ is an arbitrary set of positive density? What if $A$ is the set of squares excluding $1$?
- 范围解释：三支问题分别为：无限等差数列上任意非恒定 ±1 染色；任意正密度集合；以及去掉 1 的平方数集，是否总有有限非空子集使带号倒数和为 0。
- 闭合判定：`closed_verified`
- 判定理由：AP 分支由已发表论文肯定；正密度分支被“只有一个偶数”的正密度集合立即否定；平方分支由公开完整手稿肯定，因此三问均有确定答案。
- Lean 审计：未找到覆盖三支的完整 Lean 证明；FormalConjectures #318 文件有多个 sorry，不能视为证明。
- 尚存不确定性：平方分支目前核实为公开手稿，尚未确认同行评审；其定理陈述与题面完全匹配。
- 证据：

  - `official_page` [Erdős Problem #318](https://www.erdosproblems.com/318)；发表状态：official_database；核验：题页标记 solved；必须分别回答三种 A，不能把其中一个答案外推到另两个。
  - `published_paper` [Sattler's arithmetic progression case I](https://www.sciencedirect.com/science/article/pii/1385725882900257)；发表状态：peer_reviewed；核验：已发表论文证明等差数列情形的肯定答案。
  - `published_paper` [Sattler's arithmetic progression case II](https://www.sciencedirect.com/science/article/pii/1385725882900269)；发表状态：peer_reviewed；核验：续篇补齐相关倒数子和论证，和第一篇共同覆盖 AP 分支。
  - `public_manuscript` [Erdős 318: the squares case](https://github.com/Larsen-Daniel/Erdos-318/blob/main/318.pdf)；发表状态：public_manuscript；核验：定理 6 明确证明：对所有大于 1 的平方数的任意非平凡二染色，存在两个有限非空异色子集，其倒数和相等。

#### #320

- 官方状态：`solved`
- 精确题面：Let $S(N)$ count the number of distinct sums of the form $\sum_{n\in A}\frac{1}{n}$ for $A\subseteq \{1,\ldots,N\}$. Estimate $S(N)$.
- 范围解释：S(N) 统计 [N] 各子集的倒数和所产生的不同值数；要求给出其渐近数量级。
- 闭合判定：`closed_verified`
- 判定理由：已接受公开稿给出相匹配的双侧量级，而不是仅一个界，足以回答“Estimate S(N)”。
- Lean 审计：Lean 证据只覆盖有限组合核心，不覆盖完整渐近解析数论；因此本题的 solved 核验依赖公开数学手稿。
- 尚存不确定性：手稿的最终期刊状态未确认；完整渐近论证尚无端到端 Lean 版本。
- 证据：

  - `official_page` [Erdős Problem #320](https://www.erdosproblems.com/320)；发表状态：official_database；核验：题页标记 solved，答案涉及 N/log N 乘以截至 κ(N) 的迭代对数乘积。
  - `accepted_proof_claim` [Proof of Erdős Problems 320 and 321](https://www.overleaf.com/read/ykvtbnjjppqn#2ccc1c)；发表状态：accepted_by_site_public_manuscript；核验：公开稿给出 S(N) 上、下界的同阶公式，并引用已发表的定量数论输入；该证明声明已被题库接受。
  - `public_lean` [erdos-320-harmonic-subset-sums](https://github.com/Zarathustra23/erdos-320-harmonic-subset-sums)；发表状态：partial_formalization；核验：无 sorry 的 Lean 文件形式化有限组合核心；仓库审计文档明确说明渐近部分仍调用定量 PNT 与 Bettin–Grenié–Molteni–Sanna 定理，未端到端形式化。

#### #321

- 官方状态：`solved`
- 精确题面：What is the size of the largest $A\subseteq \{1,\ldots,N\}$ such that all sums $\sum_{n\in S}\frac{1}{n}$ are distinct for $S\subseteq A$?
- 范围解释：求 [N] 中最大集合 A 的大小，使 A 的所有子集倒数和两两不同，即倒数族在 {0,1} 系数下无非平凡关系。
- 闭合判定：`closed_verified`
- 判定理由：公开已接受证明给出所求最大基数的正确数量级，并同时提供匹配构造。
- Lean 审计：公开 Lean 只证组合桥梁，不足以单独推出最终渐近式；没有把部分形式化误记为全题形式证明。
- 尚存不确定性：仍需期刊审稿或把 BGMS/PNT 输入形式化，才能获得更高等级的独立验证。
- 证据：

  - `official_page` [Erdős Problem #321](https://www.erdosproblems.com/321)；发表状态：official_database；核验：题页标记 solved，并与 #320 的不同子集和计数建立 2^|A|≤S(N) 的直接联系。
  - `accepted_proof_claim` [Proof of Erdős Problems 320 and 321](https://www.overleaf.com/read/ykvtbnjjppqn#2ccc1c)；发表状态：accepted_by_site_public_manuscript；核验：同一公开稿给出最大 dissociated 倒数集的上、下界同阶；上界来自 #320，下界用 BGMS 型构造。
  - `public_lean` [erdos-320-harmonic-subset-sums](https://github.com/Zarathustra23/erdos-320-harmonic-subset-sums)；发表状态：partial_formalization；核验：仓库形式化了有限注入/子集和计数核心且无 sorry，但未形式化完整的解析数论渐近输入。

#### #330

- 官方状态：`proved (Lean)`
- 精确题面：Does there exist a minimal basis with positive density, say $A\subset\mathbb{N}$, such that for any $n\in A$ the (upper) density of integers which cannot be represented without using $n$ is positive?
- 范围解释：构造一个正密度的极小加法基 A，并要求每个必需元素 n 的“离开 n 后不能表示”的整数集具有正上密度。
- 闭合判定：`closed_scope_caveat`
- 判定理由：公开手稿与无条件 Lean 主定理闭合了官网附注所采用的正上密度解释；若把正文未限定的 positive density 解读为自然密度存在或正下密度，则当前主声明更弱，必须保留术语范围说明。
- Lean 审计：正式证明目录无占位；主定理 erdos330_mainTarget 对 A 本身证明的是 positive upper density。官网正文只写 positive density，并在附注中说明最可能意指 upper density，因此 Lean 精确覆盖的是这一解释，而不是密度极限存在或正下密度。
- 尚存不确定性：建议官网把 A 的密度明确写成 positive upper density，并将历史上可能的更强密度版本分开记录。
- 证据：

  - `official_page` [Erdős Problem #330](https://www.erdosproblems.com/330)；发表状态：official_database；核验：题页标记 proved (Lean)，现行显示版本要求 A 自身正密度，并对每个元素要求私人表示集正上密度。
  - `public_manuscript` [Construction for Erdős Problem 330](https://www.overleaf.com/read/chgqskmtnmzy#013b0c)；发表状态：public_manuscript；核验：手稿给出分层调度构造并证明基性、极小性和两个密度条件。
  - `public_lean` [Erdos330Formalization/Scheduler.lean](https://github.com/AllenGrahamHart/FormalConjectures-Bench/blob/main/formalizations/erdos330/Erdos330Formalization/Scheduler.lean)；发表状态：public_formalization；核验：对 formalizations/erdos330 全树静态扫描未见实际 sorry、admit 或 axiom；主定理 erdos330_mainTarget 明确含二阶加法基、A 正上密度及每个私人集正上密度。

#### #347

- 官方状态：`proved (Lean)`
- 精确题面：Is there a sequence $A=\{a_1\leq a_2\leq \cdots\}$ of integers with\[\lim \frac{a_{n+1}}{a_n}=2\]such that\[P(A')= \left\{\sum_{n\in B}n : B\subseteq A'\textrm{ finite }\right\}\]has density $1$ for every cofinite subsequence $A'$ of $A$?
- 范围解释：构造非降整数序列 a_n，满足 a_(n+1)/a_n→2，且删除任意有限多个项后，剩余项的有限子集和集合仍有自然密度 1。
- 闭合判定：`closed_verified`
- 判定理由：构造、极限比和删除稳健的密度 1 结论均由手稿和两个 Lean 实现覆盖。
- Lean 审计：两份公开形式化均可定位到主声明，静态检查无自定义公理或占位；强量词“所有余有限子序列”没有被弱化。
- 尚存不确定性：未在本机分别锁定并重编译两个仓库，但独立实现显著降低了转录或声明偏差风险。
- 证据：

  - `official_page` [Erdős Problem #347](https://www.erdosproblems.com/347)；发表状态：official_database；核验：题页标记 proved (Lean)，关键强度是对每个 cofinite subsequence 同时成立。
  - `public_manuscript` [Problem 347 proof](https://github.com/ebarschkis/ErdosProblem/blob/main/Problem347/347.pdf)；发表状态：public_manuscript；核验：PDF 给出接近倍增且对有限删除稳健的序列构造。
  - `public_lean` [Problem347/Formalization.lean](https://github.com/ebarschkis/ErdosProblem/blob/main/Problem347/Formalization.lean)；发表状态：public_formalization；核验：检查约 2161 行，无 sorry、admit 或 axiom；主定理量化所有余有限子序列。
  - `independent_public_lean` [ErdosProblem347.lean](https://github.com/Woett/Lean-files/blob/main/ErdosProblem347.lean)；发表状态：independent_public_formalization；核验：第二份独立公开 Lean 文件同样无占位并打印主定理公理集，为声明匹配提供交叉核验。

#### #351

- 官方状态：`proved (Lean)`
- 精确题面：Let $p(x)\in \mathbb{Q}[x]$. Is it true that\[A=\{ p(n)+1/n : n\in \mathbb{N}\}\]is strongly complete, in the sense that, for any finite set $B$,\[\left\{\sum_{n\in X}n : X\subseteq A\backslash B\textrm{ finite }\right\}\]contains all sufficiently large integers?
- 范围解释：现行修正版要求 p∈ℚ[x] 的首项系数为正，并不排除正的常数多项式；集合 {p(n)+1/n} 删除任意有限子集后，其有限子集和仍包含所有充分大整数。冻结题面漏了必要的正首项条件。
- 闭合判定：`closed_scope_caveat`
- 判定理由：官网修正版已被手稿和 Lean 证明；漏条件的冻结题面本身为假，必须把修订范围写清。
- Lean 审计：公开文件无占位。外层 wrapper 多了 natDegree>0，但内部 corollary_7_pos_leading 精确覆盖包括正的常数多项式在内的全部 leadingCoeff>0 范围；冻结语料漏条件的字面命题仍不是该 Lean 定理。
- 尚存不确定性：需在上游语料同步当前题面，避免后续把 p(x)=−x 的反例误判为推翻已证修正版。
- 证据：

  - `official_page` [Erdős Problem #351](https://www.erdosproblems.com/351)；发表状态：official_database；核验：现行页面补入正首项系数；不加该条件时 p(x)=−x 等显然反例使强完备性不可能。
  - `public_manuscript` [Updated proof manuscript for Erdős 283/351](https://drive.google.com/file/d/1cW2Z7vpTjLQ2Wf6SMb6_nbO9JYlfznnt/view)；发表状态：public_manuscript；核验：手稿从 #283 的同步 Egyptian-fraction 构造推出强完备性，并解释正、负首项系数的分界。
  - `public_lean` [Erdos/P283/Proof_flat.lean — PolynomialEgyptianSums.corollary_7_pos_leading](https://github.com/Shashi456/erdos-formalizations/blob/main/Erdos/P283/Proof_flat.lean)；发表状态：public_formalization；核验：同一无 sorry/admit/axiom 文件中的外层 Erdos351.erdos_351 额外假设 natDegree>0，单独漏掉正的常数多项式；但其内部定理 PolynomialEgyptianSums.corollary_7_pos_leading 只假设 leadingCoeff>0，精确覆盖官网全部现行范围，并还形式化负首项方向的障碍。

#### #358

- 官方状态：`proved`
- 精确题面：Let $A=\{a_1<\cdots\}$ be an infinite sequence of integers. Let $f(n)$ count the number of solutions to\[n=\sum_{u\leq i\leq v}a_i.\]Is there such an $A$ for which $f(n)\to \infty$ as $n\to \infty$? Or even where $f(n)\geq 2$ for all large $n$?
- 范围解释：构造严格递增正整数序列 A，使每个充分大 n 作为连续块和的表示数 f(n) 至少为 2，最好还满足 f(n)→∞；现行 proved 声称解决更强的发散版本。
- 闭合判定：`evidence_incomplete`
- 判定理由：现行唯一可访问的完整稿存在具体、被作者承认需修订的证明缺口；在更正版或独立完整证明出现前，不能核实官方 proved 标签。
- Lean 审计：未找到公开完整 Lean 证明；FormalConjectures #358 只是含 sorry 的题面模板。
- 尚存不确定性：需取得作者承诺的下一版，逐项检查中频估计和期望计数是否修复；历史二手说法“已有构造”不足以替代可核验证明。
- 证据：

  - `official_page` [Erdős Problem #358](https://www.erdosproblems.com/358)；发表状态：official_database；核验：题页标记 proved，并链接 Tao 2026 年 2 月手稿作为闭合证据。
  - `public_manuscript` [A Set That Represents All Large Integers Multiple Times by Consecutive Elements](https://terrytao.wordpress.com/wp-content/uploads/2026/02/erdos-358-2.pdf)；发表状态：public_manuscript_under_revision；核验：手稿定理声称存在 A 使 f(n)≫log n；但第 10 页的中频论断可被 q=100、θ=1/97、j=3 直接反驳，且 red-exceptional 的定义遗漏 representing 条件。
  - `public_technical_review` [Erdős Problem #358 forum review](https://www.erdosproblems.com/forum/thread/358)；发表状态：public_postpublication_review；核验：2026-03-27 的评论给出上述明确反例并指出期望值计数缺项；作者回复将于下一版修正。核验时 PDF 的 Last-Modified 仍为 2026-02-24，未找到更正版。
  - `earlier_public_manuscript` [Earlier proposed proof of Erdős 358](https://www.ulam.ai/research/erdos358.pdf)；发表状态：superseded_public_manuscript；核验：更早的 Ulam/Chojecki 版本也曾被公开指出证明缺口，不能独立补上 Tao 当前稿的问题。

#### #369

- 官方状态：`proved (Lean)`
- 精确题面：Let $\epsilon>0$ and $k\geq 2$. Is it true that, for all sufficiently large $n$, there is a sequence of $k$ consecutive integers in $\{1,\ldots,n\}$ all of which are $n^\epsilon$-smooth?
- 范围解释：现行字面题面只要求在 [1,n] 找 k 个连续的 n^ε-smooth 整数；固定取 1,…,k 在 n 足够大时已平凡满足。公开证明处理了更自然且更强的靠近 n 的区间版本。
- 闭合判定：`closed_scope_caveat`
- 判定理由：字面版本来就是平凡真命题；有意义的 [N/2,N] 加强版也已公开形式化，所以可记闭合，但必须记录题面歧义。
- Lean 审计：Lean 文件无占位且证明比当前字面题面强的尺度局部版本；声明范围经过静态核对。
- 尚存不确定性：应回查原始文献究竟指定哪个靠近 n 的区间，并在官网修正 [1,n] 的退化措辞。
- 证据：

  - `official_page` [Erdős Problem #369](https://www.erdosproblems.com/369)；发表状态：official_database；核验：题页标记 proved (Lean)，但显示的 [1,n] 范围使问题按字面退化；论坛讨论采用 [n/2,n] 等加强解释。
  - `public_lean` [ErdosProblem369.lean](https://github.com/Woett/Lean-files/blob/465f1da7f38003939df8d57c2de06b8c53658ab0/ErdosProblem369.lean)；发表状态：public_formalization；核验：静态检查中“sorry”只出现在注释，未见 admit/axiom；erdos_problem_369 与 #print axioms 证明所有充分大 N 的 [N/2,N] 内有 k 个连续 N^ε-smooth 数。
  - `published_paper` [Smooth Values of Polynomials](https://doi.org/10.1017/S1446788718000320)；发表状态：peer_reviewed；核验：BFMW 的光滑数结果也蕴含靠近尺度 N 的固定长度连续光滑块，为加强版提供独立数学背景。

#### #380

- 官方状态：`proved`
- 精确题面：We call an interval $[u,v]$ 'bad' if the greatest prime factor of $\prod_{u\leq m\leq v}m$ occurs with an exponent greater than $1$. Let $B(x)$ count the number of $n\leq x$ which are contained in at least one bad interval. Is it true that\[B(x)\sim \#\{ n\leq x: P(n)^2\mid n\},\]where $P(n)$ is the largest prime factor of $n$?
- 范围解释：坏区间是区间乘积的最大素因子出现指数至少 2；B(x) 统计落入某个坏区间的 n，断言其渐近等于满足 P(n)^2|n 的 n 的数量。
- 闭合判定：`closed_verified`
- 判定理由：预印本主定理与 B(x) 的定义及目标渐近逐项匹配，没有只证明上界或密度版本。
- Lean 审计：未找到公开 Lean 证明；核验依据是完整可下载预印本。
- 尚存不确定性：截至核验日尚未确认同行评审发表。
- 证据：

  - `official_page` [Erdős Problem #380](https://www.erdosproblems.com/380)；发表状态：official_database；核验：题页标记 proved，链接 2026 年预印本并将其主定理对应到精确渐近等价。
  - `preprint` [Products of Consecutive Integers with Unusual Anatomy](https://arxiv.org/abs/2603.27990)；发表状态：arxiv_preprint；核验：Tao 的主定理同时给出主项与非平凡坏区间贡献可忽略的估计，结论正是题面所写的渐近式。

#### #387

- 官方状态：`solved`
- 精确题面：Is there an absolute constant $c>0$ such that, for all $1\leq k< n$, the binomial coefficient $\binom{n}{k}$ has a divisor in $(cn,n]$?
- 范围解释：问是否存在固定 c>0，使每个 1≤k<n 的二项式系数 C(n,k) 都有一个落在 (cn,n] 的除数。
- 闭合判定：`closed_verified`
- 判定理由：一个最大可用除数为 o(n) 的无限族直接否定“存在绝对 c 对所有 n,k”，量词反驳充分。
- Lean 审计：未找到公开 Lean 形式化；完整反例论证目前为预印本。
- 尚存不确定性：尚未确认同行评审状态；应在最终报告注明答案是否定而非给出最优 c。
- 证据：

  - `official_page` [Erdős Problem #387](https://www.erdosproblems.com/387)；发表状态：official_database；核验：题页标记 solved；最新结果以一族二项式系数的最大相关除数为 o(n) 来否定固定 c。
  - `preprint` [Binomial Coefficients with Divisors Avoiding an Interval](https://arxiv.org/abs/2605.21221)；发表状态：arxiv_preprint；核验：Bui–Naprienko–Pratt–Zaharescu 构造无穷多 (n,k)，其任何不超过 n 的相关大除数都受 n 乘迭代对数比的上界控制；该比趋于 0，排除任意固定 c。

#### #397

- 官方状态：`disproved (Lean)`
- 精确题面：Are there only finitely many solutions to\[\prod_i \binom{2m_i}{m_i}=\prod_j \binom{2n_j}{n_j}\]with the $m_i,n_j$ distinct?
- 范围解释：问乘积恒等式 ∏C(2m_i,m_i)=∏C(2n_j,n_j) 在两边所有索引互异的条件下是否只有有限多个解。
- 闭合判定：`closed_verified`
- 判定理由：参数化族给出无穷多个合规解，精确否定有限性断言。
- Lean 审计：公开单文件形式化有具体主声明，无占位和自定义公理；反例的互异条件没有被遗漏。
- 尚存不确定性：本次未在固定 mathlib 环境重新执行 gist；建议归档到带版本锁的仓库。
- 证据：

  - `official_page` [Erdős Problem #397](https://www.erdosproblems.com/397)；发表状态：official_database；核验：题页标记 disproved (Lean)，所需反例必须产生无穷多解且保持两列索引的全局互异。
  - `public_lean` [Erdős 397 formal counterexample](https://gist.github.com/llllvvuu/40d68cfa9de9f43eece07ff4fdc3b0ef)；发表状态：public_formalization；核验：检查 397.lean：无 sorry、admit、axiom；主定理 infinite_solutions 给出参数化恒等式，并明确证明合并后的索引列表 Nodup。

#### #401

- 官方状态：`proved (Lean)`
- 精确题面：Is there $f(r)\to\infty$ such that, for infinitely many $n$, there are $a_1,a_2$ with $a_1+a_2>n+f(r)\log n$ and $a_1!a_2!\mid n!2^n3^n\cdots p_r^n$?
- 范围解释：采用现行“对无穷多个 n”解释：存在 f(r)→∞，使某些 a_1+a_2 超过 n+f(r)log n，且 a_1!a_2! 整除 n!·(2·3⋯p_r)^n。更强的“所有充分大 n”版本为假。
- 闭合判定：`closed_scope_caveat`
- 判定理由：现行 infinitely-many-n 版本由公开手稿闭合，Lean 核验其中固定 r 的主要论证；但“Lean 完整证明”标签过强，且历史上更强量词的命题不同并为假，状态必须绑定到当前解释。
- Lean 审计：Erdos401b.lean 无 sorry、admit 或自定义 axiom，且核验固定 r 的无限族核心；但未形式化 ω(r)→∞。这一缺失步骤由公开手稿 Remark 1 的初等素数极限补齐，不能把官网的“(Lean)”标签理解为全命题端到端形式化。
- 尚存不确定性：手稿未确认同行评审；Lean 尚缺 ω(r)→∞ 的端到端形式化。建议官网永久保留两个版本的分界及反例说明。
- 证据：

  - `official_page` [Erdős Problem #401](https://www.erdosproblems.com/401)；发表状态：official_database；核验：题页当前明确写 infinitely many n，并标记 proved (Lean)；历史讨论还出现过 all sufficiently large 的不同版本。
  - `public_lean` [Erdos401b.lean](https://github.com/plby/lean-proofs/blob/e011328d3a6f1de3b1af7ae67d5f610498ca455d/src/v4.24.0/ErdosProblems/Erdos401b.lean)；发表状态：partial_formalization；核验：源文件无 sorry、admit 或自定义 axiom；theorem_1 内核核验每个固定 r 的无穷多个 n 以及相应整除与增益结论，但文件没有陈述或证明 Tendsto ω atTop atTop，因而不是官网现行全命题的端到端 Lean 证明。
  - `public_manuscript` [Factorial divisibility with bounded primes beyond the logarithmic barrier: an infinitely-many n result of Erdős type](https://drive.google.com/file/d/1SY_LjPToevYaFl5eNl-rUxJrjrP5u4RC/view)；发表状态：public_manuscript；核验：Theorem 1 对每个固定 r 证明无穷多个 n，并显式取 ω(r)=(9/70)/16·(p_{r+1}-1)/log p_{r+1}；Remark 1 由 p_{r+1}→∞ 补出 ω(r)→∞。未确认同行评审发表。

#### #457

- 官方状态：`proved (Lean)`
- 精确题面：Is there some $\epsilon>0$ such that there are infinitely many $n$ where all primes $p\leq (2+\epsilon)\log n$ divide\[\prod_{1\leq i\leq \log n}(n+i)?\]
- 范围解释：存在固定 ε>0 和无穷多个 n，使每个 p≤(2+ε)log n 的素数都整除连续区间乘积 ∏_{1≤i≤log n}(n+i)。
- 闭合判定：`closed_verified`
- 判定理由：手稿和 Lean 共同构造 ε=0.1 的无限族，直接覆盖全部小素数整除条件。
- Lean 审计：有具体公开主声明、无占位或自定义公理，且显式常数满足题面只需存在某个 ε>0 的要求。
- 尚存不确定性：未确认论文发表状态；本机未重新编译仓库。
- 证据：

  - `official_page` [Erdős Problem #457](https://www.erdosproblems.com/457)；发表状态：official_database；核验：题页标记 proved (Lean)，目标是超过常数 2 的任意一个固定增益，而非所有 ε。
  - `public_manuscript` [Proof manuscript for Erdős 457](https://drive.google.com/file/d/1b6puijShAt5hq3Vxnb45R0pm0WqVcJE8/view?usp=sharing)；发表状态：public_manuscript；核验：手稿给出取 ε=0.1 的显式构造与无穷性论证，足以回答存在性问题。
  - `public_lean` [ErdosProblem457.lean](https://github.com/Woett/Lean-files/blob/main/ErdosProblem457.lean)；发表状态：public_formalization；核验：静态检查未见实际 sorry、admit、axiom；thm_main 与 erdos_457 采用 ε=1/10 并打印公理集合，量词为无穷多个 n。

#### #488

- 官方状态：`falsifiable`
- 精确题面：Let $A$ be a finite set and\[B=\{ n \geq 1 : a\mid n\textrm{ for some }a\in A\}.\]Is it true that, for every $m>n\geq \max(A)$,\[\frac{\lvert B\cap [1,m]\rvert }{m}< 2\frac{\lvert B\cap [1,n]\rvert}{n}?\]
- 范围解释：现行题面令 B 为 A 中某元素的倍数集合，问所有 m>n≥max A 时密度比是否严格小于 2；这与曾被反驳的“a 不整除 n”误录版本不同。
- 闭合判定：`status_or_statement_mismatch`
- 判定理由：该题被列入“已不开放”集合与官网 falsifiable/仍开放状态冲突，已有反例只针对另一个命题。
- Lean 审计：Lean 证明本身可核验，但证明对象是已废弃的转录错误题面；当前倍数并命题没有公开 Lean 闭合声明。
- 尚存不确定性：需继续核验现行倍数并版本；计算覆盖有限 A 或有限范围 n,m 不能代替全称证明。
- 证据：

  - `official_page` [Erdős Problem #488](https://www.erdosproblems.com/488)；发表状态：official_database；核验：状态为 falsifiable 而不是 solved；正文当前明确采用 a|n 的倍数并，仍保留为开放的有限可检验命题。
  - `public_lean` [Erdos488b.lean](https://github.com/plby/lean-proofs/blob/e011328d3a6f1de3b1af7ae67d5f610498ca455d/src/v4.24.0/ErdosProblems/Erdos488b.lean)；发表状态：public_formalization_of_superseded_statement；核验：文件无占位并反驳了旧的 non-multiples（a∤n）版本；其集合定义与现行官网的 multiples（a|n）版本相反，因此不能作为闭合证据。

#### #533

- 官方状态：`disproved`
- 精确题面：Let $\delta>0$. If $n$ is sufficiently large and $G$ is a graph on $n$ vertices with no $K_5$ and at least $\delta n^2$ edges then $G$ contains a set of $\gg_\delta n$ vertices containing no triangle.
- 范围解释：断言每个有正二次边密度的 K_5-free 图都含线性大小的无三角形顶点集；等价于相关 Ramsey–Turán 密度 δ_3(5) 为 0。
- 闭合判定：`closed_verified`
- 判定理由：δ_3(5)=1/12>0 的构造精确产生题面所禁的图族，因此全称断言被严格反驳。
- Lean 审计：未找到该 Ramsey–Turán 构造的完整 Lean 形式化；FormalConjectures 题面文件若含 sorry 不能作为反证。
- 尚存不确定性：原证否及精确值均已有同行评审来源；未找到相应端到端 Lean 形式化。
- 证据：

  - `official_page` [Erdős Problem #533](https://www.erdosproblems.com/533)；发表状态：official_database；核验：题页标记 disproved，并将问题链接到 K_5 的三角形独立集 Ramsey–Turán 密度。
  - `official_problem_record` [Ramsey–Turán problem for K5](https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/RamseyTuran5.html)；发表状态：public_mathematical_record；核验：记录了 Balogh–Lenz 正密度构造及后续精确值工作，直接表明 δ_3(5)>0。
  - `published_paper` [On the Ramsey–Turán Numbers of Graphs and Hypergraphs](https://doi.org/10.1007/s11856-012-0076-2)；发表状态：peer_reviewed；核验：Balogh–Lenz 对 t=3、K_(t+2)=K_5 证明 Ramsey–Turán 数为 Ω(n²)，即存在正密度 K_5-free 图且最大无三角形诱导子图为 o(n)，直接反驳 δ₃(5)=0。
  - `published_paper` [Geometric Constructions for Ramsey–Turán Theory](https://doi.org/10.4171/JEMS/1712)；发表状态：peer_reviewed；核验：Liu–Reiher–Sharifzadeh–Staden 的已发表结果给出匹配构造，结合经典上界确定 δ₃(5)=1/12；它把早期的正值反例加强为精确值。
  - `published_paper` [Earlier K5 Ramsey–Turán upper-bound framework](https://renyi.hu/~sos/1994_Turan_Ramsey_Theoremes_And_Kp_Independence_Numbers.pdf)；发表状态：peer_reviewed；核验：早期已发表工作提供该参数体系和上界背景，与后续正构造/精确值的定义一致。

#### #543

- 官方状态：`disproved`
- 精确题面：Define $f(N)$ be the minimal $k$ such that the following holds: if $G$ is an abelian group of size $N$ and $A\subseteq G$ is a random set of size $k$ then, with probability $\geq 1/2$, all elements of $G$ can be written as $\sum_{x\in S}x$ for some $S\subseteq A$. Is\[f(N) \leq \log_2 N+o(\log\log N)?\]
- 范围解释：f(N) 是任意 N 阶阿贝尔群中，随机取 k 元集合以至少 1/2 概率成为完全子集和基所需的最小阈值；猜测 f(N)≤log_2 N+o(log log N)。
- 闭合判定：`closed_verified`
- 判定理由：对循环群的无限反例族已经否定全体有限阿贝尔群上的统一渐近上界。
- Lean 审计：未找到公开 Lean 形式化；证据是可检查的修订预印本。
- 尚存不确定性：截至核验日尚未确认同行评审发表。
- 证据：

  - `official_page` [Erdős Problem #543](https://www.erdosproblems.com/543)；发表状态：official_database；核验：题页标记 disproved，反例来自一族素数阶循环群，因而已足以否定对所有阿贝尔群的上界。
  - `preprint` [An Erdős Problem on Random Subset Sums in Finite Abelian Groups](https://arxiv.org/abs/2602.05768)；发表状态：arxiv_preprint；核验：预印本证明某些循环群需要超过 log_2 N+o(log log N) 的样本大小，直接否定猜测的二阶误差。
  - `public_manuscript` [On Erdős Problem 543 — revised and verified](https://github.com/QuanyuTang/erdos-problem-543/blob/main/On_Erdos_Problem_543_Revised_and_Verified.pdf)；发表状态：public_revised_manuscript；核验：修订稿公开给出群阶选择、概率估计和误差核查，结论与 arXiv 版本一致。

#### #574

- 官方状态：`disproved`
- 精确题面：Is it true that, for $k\geq 2$,\[\mathrm{ex}(n;\{C_{2k-1},C_{2k}\})=(1+o(1))(n/2)^{1+\frac{1}{k}}.\]
- 范围解释：对每个 k≥2，猜测同时禁 C_(2k−1)、C_(2k) 的极值边数渐近为 (n/2)^(1+1/k)。
- 闭合判定：`closed_verified`
- 判定理由：在 k=3、k=5 等固定值已有二部构造取得严格更大的主常数；二部性同时排除所禁奇环，故原全称渐近式为假。
- Lean 审计：未找到公开 Lean 证明；反例由多篇同行评审的显式代数/有限几何构造支撑。
- 尚存不确定性：无需确定每个 k 的正确常数即可闭合原猜测；完整逐 k 分类仍是另一问题。
- 证据：

  - `official_page` [Erdős Problem #574](https://www.erdosproblems.com/574)；发表状态：official_database；核验：题页标记 disproved；只需某个固定 k 的主常数超过猜测即可反驳全称命题。
  - `published_paper` [New Constructions of Bipartite Graphs on m,n Vertices with Many Edges and Without Small Cycles](https://www.sciencedirect.com/science/article/pii/S0095895684710367)；发表状态：peer_reviewed；核验：已发表二部图构造避开所有奇环，并在相应偶环约束下给出超过猜测常数的边数。
  - `published_paper` [Polarities and 2k-cycle-free Graphs](https://www.sciencedirect.com/science/article/pii/S0012365X99901073)；发表状态：peer_reviewed；核验：进一步有限几何构造覆盖相关 k，并保留二部性，因此自动排除 C_(2k−1)。
  - `published_paper` [On the Turán Number for the Hexagon](https://www.sciencedirect.com/science/article/pii/S0001870805001349)；发表状态：peer_reviewed；核验：六边形情形给出 k=3 的明确反例常数；与其他构造共同确认猜测并非只差未知低阶项。

#### #591

- 官方状态：`proved`
- 精确题面：Let $\alpha$ be the infinite ordinal $\omega^{\omega^2}$. Is it true that in any red/blue colouring of the edges of $K_\alpha$ there is either a red $K_\alpha$ or a blue $K_3$?
- 范围解释：序数 α=ω^(ω²) 的完全图任意红蓝边染色，必有红色同构 K_α 或蓝色三角形，即 α→(α,3)^2。
- 闭合判定：`closed_verified`
- 判定理由：同行评审论文的明确编号定理在参数代入后与原序数分割关系完全相同。
- Lean 审计：未找到公开 Lean 形式化；FormalConjectures #591 只是题面加 sorry。
- 尚存不确定性：无实质性数学不确定性；若需形式核验，序数与分割演算的 Lean 库化仍待开展。
- 证据：

  - `official_page` [Erdős Problem #591](https://www.erdosproblems.com/591)；发表状态：official_database；核验：题页标记 proved，并引用 Schipperus 的可数分割序数结果。
  - `published_paper` [Countable partition ordinals](https://doi.org/10.1016/j.apal.2009.12.007)；发表状态：peer_reviewed；核验：Schipperus, Annals of Pure and Applied Logic 161(10) (2010)，定理 28 的 β=2 特例精确给出 ω^(ω²)→(ω^(ω²),3)^2。

#### #603

- 官方状态：`solved`
- 精确题面：Let $(A_i)$ be a family of countably infinite sets such that $\lvert A_i\cap A_j\rvert \neq 2$ for all $i\neq j$. Find the smallest cardinal $C$ such that $\cup A_i$ can always be coloured with at most $C$ colours so that no $A_i$ is monochromatic.
- 范围解释：每个 A_i 都可数无限且任意两集交大小不为 2；若族本身只含可数多个集合，最小颜色数是 2；若允许任意大指标族，则不存在单一集合基数 C 能统一约束。
- 闭合判定：`closed_verified`
- 判定理由：两种可能的原题解释都已有明确答案，所以措辞歧义不会留下未回答分支。
- Lean 审计：可数族分支是端到端形式化；任意指标族分支为条件化 Lean，但缺失接口是经典 Erdős–Rado 定理，数学手稿给出完整引用与推导。
- 尚存不确定性：若官方要给唯一数值答案，应明确 family 是可数族；完整 Lean 标签还需形式化 ArrowOmegaTwo。
- 证据：

  - `official_page` [Erdős Problem #603](https://www.erdosproblems.com/603)；发表状态：official_database；核验：题页标记 solved；对允许任意大指标族的解释，结论是不存在统一基数 C。可数指标族时恰有 C=2 的结论来自公开说明稿与论坛讨论，不是官网正文直接给出的完整论证。
  - `public_manuscript` [A solution to Erdős Problem 603](https://www.ulam.ai/research/erdos603.pdf)；发表状态：public_manuscript；核验：手稿证明可数族二染色即可且一色显然不够；对任意大族则用 Erdős–Rado 箭头关系构造需要任意多颜色的例子。
  - `public_lean` [erdos603-lean](https://github.com/KitaKen1/erdos603-lean)；发表状态：partly_conditional_formalization；核验：可数族 C=2 的主证明无 sorry/axiom；任意大族的负结论以显式 ArrowOmegaTwo 假设为接口，未形式化 Erdős–Rado 定理本身。

#### #610

- 官方状态：`proved (Lean)`
- 精确题面：For a graph $G$ let $\tau(G)$ denote the minimal number of vertices that include at least one from each maximal clique of $G$ (sometimes called the clique transversal number). Estimate $\tau(G)$. In particular, is it true that if $G$ has $n$ vertices then\[\tau(G) \leq n-\omega(n)\sqrt{n}\]for some $\omega(n)\to \infty$, or even\[\tau(G) \leq n-c\sqrt{n\log n}\]for some absolute constant $c>0$?
- 范围解释：对 n 点图的极大团击点数 τ(G)，要求至少证明 τ(G)≤n−ω(n)√n，最好达到 n−c√(n log n)。
- 闭合判定：`closed_verified`
- 判定理由：同行评审的 JMRS 定理已直接蕴含题中更强上界；Kim 构造说明数量级匹配。数学问题闭合，但官方 Lean 标签应注明条件化。
- Lean 审计：不是端到端 Lean 证明：两个核心已发表输入被 sorry 占位。形式化验证的是组合归约，而非 JMRS 与 Kim 定理本身。
- 尚存不确定性：需把 jmrs_theorem、kim_theorem 正式化并消除两个 sorry，才能声称完全内核验证。
- 证据：

  - `official_page` [Erdős Problem #610](https://www.erdosproblems.com/610)；发表状态：official_database；核验：题页标记 proved (Lean)，引用 clique colouring 上界和 Kim 三角形自由图下界。
  - `published_paper` [Tight Bounds on the Clique Chromatic Number](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v28i3p51/pdf)；发表状态：peer_reviewed；核验：Joret–Micek–Reed–Smid 证明 clique chromatic number O(√(n/log n))；最大颜色类是不含极大团的集合，其补集给出 n−c√(n log n) 的 clique transversal。
  - `public_lean` [erdos610.lean](https://www.ulam.ai/research/erdos610.lean)；发表状态：conditional_formalization；核验：文件恰有两个 sorry：jmrs_theorem 和 kim_theorem；从这两个已知外部图论结果到上下界/题面结论的其余推导已形式化。
  - `published_paper` [The Ramsey number R(3,t) has order of magnitude t²/log t](https://doi.org/10.1002/rsa.3240070302)；发表状态：peer_reviewed；核验：Kim 的同行评审定理提供匹配量级的三角形自由图构造，支撑题页和条件 Lean 的下界方向；JMRS 定理本身直接支撑题目所需上界。

#### #619

- 官方状态：`solved (Lean)`
- 精确题面：For a triangle-free graph $G$ let $h_r(G)$ be the smallest number of edges that need to be added to $G$ so that it has diameter $r$ (while preserving the property of being triangle-free). Is it true that there exists a constant $c>0$ such that if $G$ is a connected graph on $n$ vertices then $h_4(G)<(1-c)n$?
- 范围解释：对连通 n 点三角形自由图 G，h_4(G) 是在保持三角形自由下把直径变成 4 所需最少加边数；问是否有固定 c>0 使 h_4(G)<(1−c)n。
- 闭合判定：`closed_verified`
- 判定理由：公开 Lean 工程给出统一常数并对任意合规 G 证明严格线性节省，精确回答是非问句。
- Lean 审计：解答文件与挑战文件分离清楚；完整 Solution 无占位，自定义比较器核对了定义展开后的原命题范围。
- 尚存不确定性：未在本机重新运行全套 CI；仓库内的可复核记录和静态扫描一致。
- 证据：

  - `official_page` [Erdős Problem #619](https://www.erdosproblems.com/619)；发表状态：official_database；核验：题页标记 solved (Lean)，量词覆盖所有连通三角形自由图。
  - `public_lean` [erdos-619](https://github.com/nick-kuhn/erdos-619/tree/7f65718b8c1019ecc24e6c9a6b04ec4c66a4e26f)；发表状态：public_formalization；核验：Solution.lean 约 5900 行无 sorry；Challenge.lean 的 sorry 是故意保留的题面。比较器/CI 检查目标陈述桥接，VERIFICATION.md 记录通过且仅允许标准逻辑公理。

#### #650

- 官方状态：`solved (Lean)`
- 精确题面：Let $f(m)$ be such that if $A\subseteq \{1,\ldots,N\}$ has $\lvert A\rvert=m$ then every interval in $[1,\infty)$ of length $2N$ contains $\geq f(m)$ many distinct integers $b_1,\ldots,b_r$ where each $b_i$ is divisible by some $a_i\in A$, where $a_1,\ldots,a_r$ are distinct. Estimate $f(m)$. In particular is it true that $f(m)\ll m^{1/2}$?
- 范围解释：f(m) 衡量任意 m 元 A⊂[N] 在每个长度 2N 区间中，能用互异 a_i∈A 分别整除的互异 b_i 的保证数量；要求估计 f(m)。
- 闭合判定：`closed_verified`
- 判定理由：预印本和 Lean 均给出匹配上下界及精确函数，完整解决“估计 f(m)”。
- Lean 审计：公开形式化有精确主声明、无占位与自定义公理；不是只形式化 O(√m) 推论。
- 尚存不确定性：预印本尚未确认期刊发表；需留意不同文稿对临界非平方 m 的取整记号。
- 证据：

  - `official_page` [Erdős Problem #650](https://www.erdosproblems.com/650)；发表状态：official_database；核验：题页标记 solved (Lean)，精确答案为 min(m,⌈2√m⌉)（按文中整数取整约定）。
  - `preprint` [Exact solution of Erdős Problem 650](https://arxiv.org/abs/2603.28636)；发表状态：arxiv_preprint；核验：预印本给出匹配的 Hall 型下界和显式极端构造，求得 f(m) 精确值而非仅 O(√m)。
  - `public_lean` [ErdosProblem650.lean](https://github.com/Woett/Lean-files/blob/497ce4514eae22fd4a2bea2d24c47b56562e4b8b/ErdosProblem650.lean)；发表状态：public_formalization；核验：静态检查无 sorry、admit、axiom；主定理 erdos_f_eq 与 #print axioms 形式化精确公式和题面中的任意 A、任意长度 2N 区间量词。

#### #652

- 官方状态：`proved`
- 精确题面：Let $x_1,\ldots,x_n\in \mathbb{R}^2$ and let $R(x_i)=\#\{ \lvert x_j-x_i\rvert : j\neq i\}$, where the points are ordered such that\[R(x_1)\leq \cdots \leq R(x_n).\]Let $\alpha_k$ be minimal such that, for all large enough $n$, there exists a set of $n$ points with $R(x_k)<\alpha_kn^{1/2}$. Is it true that $\alpha_k\to \infty$ as $k\to \infty$?
- 范围解释：按每个点看到的不同距离数 R(x_i) 递增排序，α_k 是能构造 n 点集使第 k 小 R 小于 α_k√n 的最小常数；问 α_k 是否随 k→∞ 而发散。
- 闭合判定：`closed_verified`
- 判定理由：已发表下界 α_k≫√k 直接且定量地推出所问发散；已有构造保证每个固定 k 的 α_k 有限。
- Lean 审计：未找到公开 Lean 形式化；同行评审论文的定理编号和参数已与 α_k 定义核对。
- 尚存不确定性：问题只问发散，不要求 α_k 的精确常数或阶；这些更强问题可能仍开放。
- 证据：

  - `official_page` [Erdős Problem #652](https://www.erdosproblems.com/652)；发表状态：official_database；核验：题页标记 proved，并引用 Mathialagan 对多个点的不同距离下界。
  - `published_paper` [Distinct distances from several points](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v28i4p33/pdf/)；发表状态：peer_reviewed；核验：Mathialagan, EJC 28(4) (2021)，定理 1.4/3.6 给出第 k 个点至少看到常数倍 √(kn) 个距离；因此 α_k≫√k→∞。

#### #659

- 官方状态：`proved (Lean)`
- 精确题面：Is there a set of $n$ points in $\mathbb{R}^2$ such that every subset of $4$ points determines at least $3$ distances, yet the total number of distinct distances is\[\ll \frac{n}{\sqrt{\log n}}?\]
- 范围解释：构造 n 个平面点，使任意 4 点至少决定 3 种距离，同时全局不同距离总数为 O(n/√log n)。
- 闭合判定：`closed_verified`
- 判定理由：Bernays 定理是既有严格数学结果，Grayzel 手稿把它完整应用到符合四点条件的构造，故数学命题已闭合。
- Lean 审计：Lean 是条件化证明，核心 Bernays 渐近仍为自定义公理；官方“Lean”不应理解为零外部数学公理。
- 尚存不确定性：需形式化 Bernays 定理并替换 axiom bernays；预印本的最终同行评审状态也待确认。
- 证据：

  - `official_page` [Erdős Problem #659](https://www.erdosproblems.com/659)；发表状态：official_database；核验：题页标记 proved (Lean)，构造由二次型表示数和点阵子集导出。
  - `preprint` [Solution to a Problem of Erdős Concerning Distances and Points](https://arxiv.org/abs/2601.09102)；发表状态：arxiv_preprint；核验：Grayzel 给出满足 4 点局部条件的点集构造，并将全局距离数压到 n/√log n 量级。
  - `published_paper` [Two-dimensional Lattices with Few Distances](https://doi.org/10.5169/seals-2239)；发表状态：peer_reviewed；核验：Moree–Osburn 已发表论文直接研究二维点阵的不同距离数，并用 Bernays 型渐近给出 O(n/√log n) 的所需全局距离上界。
  - `public_lean` [Erdos659.lean](https://github.com/plby/lean-proofs/blob/e011328d3a6f1de3b1af7ae67d5f610498ca455d/src/v4.24.0/ErdosProblems/Erdos659.lean)；发表状态：conditional_formalization；核验：文件无 sorry/admit，但显式声明 axiom bernays；目标 erdos_659 的 #print 输出含 bernays、propext、Classical.choice、Quot.sound。其余 Perucca 分类与几何构造已形式化。

#### #690

- 官方状态：`solved`
- 精确题面：Let $d_k(p)$ be the density of those integers whose $k$th smallest prime factor is $p$ (i.e. if $p_1<p_2<\cdots$ are the primes dividing $n$ then $p_k=p$). For fixed $k\geq 1$ is $d_k(p)$ unimodular in $p$? That is, it first increases in $p$ until its maximum then decreases.
- 范围解释：d_k(p) 是随机整数第 k 小不同素因子等于 p 的自然密度；逐个固定 k 判断它随素数 p 是否先增后减。
- 闭合判定：`closed_scope_caveat`
- 判定理由：原来的全称单峰猜想已经被 Cambie 的同行评审反例严格关闭；所有 k 的更强完整分类则由 2026 年 arXiv v1 与通过的有限验证器支持，但还不是同行评审或端到端形式化结论。
- Lean 审计：未找到 Lean 形式化；公开 Python 验证器使用精确有理数和有向区间，不是浮点启发式，但仍需结合手稿中的解析归约。
- 尚存不确定性：需独立复核全 k 预印本的解析归约与外部素数证书，或等待同行评审/形式化；这不影响原普遍猜想已经证否。
- 证据：

  - `official_page` [Erdős Problem #690](https://www.erdosproblems.com/690)；发表状态：official_database；核验：题页标记 solved，但正文只列 k=1,2,3 时单峰、4≤k≤20 时非单峰；该状态已足以表示原普遍猜想被低 k 反例关闭，官网正文没有给出所有 k 的完整分类。
  - `published_paper` [Resolution of Erdős' Problems about Unimodularity](https://doi.org/10.1016/j.jnt.2025.08.014)；发表状态：peer_reviewed；核验：Cambie 的论文严格处理 k≤20，得到 k=1,2,3 单峰、4≤k≤20 非单峰，为低 k 分类提供同行评审证据。
  - `preprint` [A Complete Answer to Erdős Problem 690](https://arxiv.org/abs/2605.08542)；发表状态：arxiv_preprint；核验：Wang–Crapis v1 主定理把非单峰结论推广到每个 k≥4，并与 Cambie 的低 k 结果合并成全分类；论证使用显式解析估计、已认证素数记录及有限计算，尚未同行评审。
  - `public_exact_verifier` [Erdős 690 numerical verifier](https://github.com/multiscalar/results/blob/1ad7da8275683a01f09259efdda0fbd0f16d4631/erdos-690/numerical_verifier.py)；发表状态：public_exact_certificate_code；核验：本次在本地运行验证器，89 项有理数/有向区间断言全部 PASS；脚本只核验有限数值部分，仍依赖手稿的解析估计、Meissel–Mertens 区间及外部素数/孪生素数记录，不能单独视作完整证明证书。

#### #694

- 官方状态：`solved (Lean)`
- 精确题面：Let $f_{\max}(n)$ be the largest $m$ such that $\phi(m)=n$, and $f_{\min}(n)$ be the smallest such $m$, where $\phi$ is Euler's totient function. Investigate\[\max_{n\leq x}\frac{f_{\max}(n)}{f_{\min}(n)}.\]
- 范围解释：求欧拉函数同一原像中最大值与最小值之比在 n≤x 时的最大阶；公开稿给出 (e^γ+o(1))log log x 的渐近式。
- 闭合判定：`closed_scope_caveat`
- 判定理由：公开稿和 Lean 声明都覆盖原题的渐近目标，数学方向一致；但稿件未同行评审，Lean 又把关键的 Linnik 输入公理化，故不能把“Lean”标签理解为无条件机器核验了全部解析数论。
- Lean 审计：外部仓库的最终声明可编译且无 sorry，但 #print axioms 含自定义公理 linnik_dvd；因此它是“在经典深定理接口之上的形式化”，不是从 Mathlib 零公理闭合。formal-conjectures 固定快照中的 694 文件仍有 sorry，只是题面基准。
- 尚存不确定性：等待论文预印本或期刊版本，并把 linnik_dvd 替换为已审计的定理实现。
- 证据：

  - `other` [Erdős 694 的公开证明稿](https://www.overleaf.com/read/fgmhvywvdjkt#54ca5d)；发表状态：公开未评审手稿；核验：主定理直接处理 frozen 题面的最大比值，并给出常数 e^γ；上下界的量词均为 x→∞。
  - `public_lean` [Jayyhk/erdos-lean problems/694](https://github.com/Jayyhk/erdos-lean/tree/main/problems/694)；发表状态：公开 Lean 仓库；核验：主声明 Erdos694.erdos_694 与上述渐近式相符；代码无 sorry，但把 Linnik 型素数定理作为自定义公理 linnik_dvd 引入。

#### #696

- 官方状态：`solved (Lean)`
- 精确题面：Let $h(n)$ be the largest $\ell$ such that there is a sequence of primes $p_1<\cdots < p_\ell$ all dividing $n$ with $p_{i+1}\equiv 1\pmod{p_i}$. Let $H(n)$ be the largest $u$ such that there is a sequence of integers $d_1<\cdots < d_u$ all dividing $n$ with $d_{i+1}\equiv 1\pmod{d_i}$. Estimate $h(n)$ and $H(n)$. Is it true that $H(n)/h(n)\to \infty$ for almost all $n$?
- 范围解释：对几乎所有 n 估计素数整除链长度 h(n) 与一般整除链长度 H(n)，并判定 H(n)/h(n) 是否趋于无穷。
- 闭合判定：`closed_scope_caveat`
- 判定理由：若接受公开稿中的解析数论论证，题目已完整回答且原猜想被否定；目前证据仍是未评审稿及把核心均匀分布定理公理化的 Lean 层。
- Lean 审计：外部代码的主声明与 frozen 量词吻合，无 sorry；#print axioms 显示依赖自定义 siegel_walfisz。formal-conjectures 的 696 文件仍含 sorry，不能作为证明。
- 尚存不确定性：需要独立同行评审，并将 Siegel–Walfisz 输入连接到可信的形式化库定理。
- 证据：

  - `other` [Erdős 696 的公开证明稿](https://www.overleaf.com/read/cmypbrpwbwrv#3e136c)；发表状态：公开未评审手稿；核验：稿件给出几乎处处 h(n)=(1/2+o(1))log_* n、H(n)=(1+o(1))log_* n，故比值趋于 2 而不是无穷；这同时回答估计与是非问句。
  - `public_lean` [Jayyhk/erdos-lean problems/696](https://github.com/Jayyhk/erdos-lean/tree/main/problems/696)；发表状态：公开 Lean 仓库；核验：Erdos696.lean 的主声明 erdos_696 形式化两条几乎处处渐近式及比值结论；无 sorry，但声明了 siegel_walfisz 公理。

#### #705

- 官方状态：`disproved`
- 精确题面：Let $G$ be a finite unit distance graph in $\mathbb{R}^2$ (i.e. the vertices are a finite collection of points in $\mathbb{R}^2$ and there is an edge between two points if and only if the distance between them is $1$). Is there some $k$ such that if $G$ has girth $\geq k$ (i.e. $G$ contains no cycles of length $<k$) then $\chi(G)\leq 3$?
- 范围解释：问是否存在统一 girth 阈值，使所有有限平面单位距离图在超过该阈值后均可 3-着色。
- 闭合判定：`closed_verified`
- 判定理由：O'Donnell 的两篇已发表论文正面构造任意大 girth、染色数 4 的有限平面单位距离图，逐字否定统一 k 的存在。
- Lean 审计：未发现公开完成的本题 Lean 证明；formal-conjectures 对应文件含 sorry，仅编码命题。数学闭合不依赖 Lean 标签。
- 尚存不确定性：无实质范围缺口；仅缺一个公开可复现的形式化版本。
- 证据：

  - `other` [Arbitrary Girth, 4-Chromatic Unit Distance Graphs in the Plane, Parts 1–2](https://geombina.uccs.edu/author-index/paul-odonnell)；发表状态：Geombinatorics 9 (2000) 已发表期刊文章；同行评审机制未核实；核验：Part 1 构造任意大 girth 的 4-染色抽象图，Part 2 给出平面单位距离嵌入并排除非边偶然成为单位距离；因而对每个 k 都有有限反例。

#### #729

- 官方状态：`proved (Lean)`
- 精确题面：For every constant $C>0$, are there infinitely many $a,b,n$ with $a+b>n+C\log n$ such that the denominator of $n!/(a!b!)$ contains only primes bounded in terms of $C$?
- 范围解释：对每个 C>0，要求无限多个正整数 a,b,n 满足 a+b>n+C log n，且 n!/(a!b!) 的分母素因子由只依赖 C 的常数控制。
- 闭合判定：`closed_verified`
- 判定理由：公开 Lean 文件直接证明原命题，不是只证明有限检查或弱化版本；常数 K 的依赖关系也正确绑定于 C。
- Lean 审计：审查最终源码未见 sorry、axiom 或局部占位；主定理的量词与 frozen 题面一致，#print axioms 仅含 Lean/Mathlib 的标准逻辑基础。formal-conjectures 基准文件的 sorry 与此外部完成稿应严格区分。
- 尚存不确定性：最好将 gist 固定为带提交哈希的仓库并接入 CI，但不影响当前声明的逻辑闭合。
- 证据：

  - `public_lean` [Erdős 729 Lean proof gist](https://gist.github.com/llllvvuu/8f6a530ff3e0783544a6f7169ac75de3)；发表状态：公开 Lean 源码；核验：最终文件 output_iter2.lean 的 main_theorem 明写 ∀C>0、∃K≥3 及无限多三元组，并逐一编码正性、不等式与分母素因子≤K。

#### #741

- 官方状态：`solved (Lean)`
- 精确题面：Let $A\subseteq \mathbb{N}$ be such that $A+A$ has positive density. Can one always decompose $A=A_1\sqcup A_2$ such that $A_1+A_1$ and $A_2+A_2$ both have positive density? Is there a basis $A$ of order $2$ such that if $A=A_1\sqcup A_2$ then $A_1+A_1$ and $A_2+A_2$ cannot both have bounded gaps?
- 范围解释：第一问中的“positive density”未说明是上密度还是存在的自然密度；第二问问是否有二阶基，使任意二分的两个自和集不可能同时有有界间隙。
- 闭合判定：`closed_scope_caveat`
- 判定理由：现有工作把常见的两种密度解释都处理了，并肯定回答第二问；保留项来自 frozen 题面本身的术语歧义，而不是证明遗漏。
- Lean 审计：公开 Lean 文件无 sorry/axiom，声明与论文三项结果一致；formal-conjectures 基准的对应文件仍有 sorry，不能与该外部证明混同。
- 尚存不确定性：官方应在题面明确 density 的定义，并标注第一问在两种定义下答案相反。
- 证据：

  - `preprint` [Additive bases and density under partitions](https://arxiv.org/abs/2603.29961)；发表状态：arXiv 预印本；核验：论文分别证明上密度解释为肯定、严格自然密度解释有反例，并构造满足第二问的基；不是把含糊的 density 偷换成单一含义。
  - `public_lean` [Erdős 741 Lean source](https://www.ulam.ai/research/erdos741.lean)；发表状态：公开 Lean 单文件；核验：三个主声明 erdos741_upper_density、erdos741_strict_density_counterexample、erdos741_syndetic 分别覆盖两种密度解释和基的有界间隙结论；未见 sorry 或新增 axiom。

#### #750

- 官方状态：`proved (Lean)`
- 精确题面：Let $f(m)$ be some function such that $f(m)\to \infty$ as $m\to \infty$. Does there exist a graph $G$ of infinite chromatic number such that every subgraph on $m$ vertices contains an independent set of size at least $\frac{m}{2}-f(m)$?
- 范围解释：要求存在无限染色数图，使其每个 m 点子图都有至少 m/2−f(m) 个独立点，其中某个 f(m)→∞。
- 闭合判定：`closed_scope_caveat`
- 判定理由：手稿覆盖原题全部量词，形式化也匹配；不过论文未同行评审，且 Lean 的关键图论输入仍是自定义公理。
- Lean 审计：外部代码无 sorry，但 #print axioms 含 stiebitz_lower_bound；因此 Lean 只核验从该经典输入到结论的组合。formal-conjectures 对应文件仍有 sorry。
- 尚存不确定性：需发表版本及对 stiebitz_lower_bound 的独立形式化。
- 证据：

  - `other` [Erdős 750 proof manuscript](https://www.ulam.ai/research/erdos750.pdf)；发表状态：公开未评审手稿；核验：主定理控制每个有限子图的局部奇环横截数，推得独立数≥m/2−g(m)，且 g(m)→∞；量词覆盖一个固定的无限染色数图。
  - `public_lean` [Shashi456 Erdős 750 Lean proof](https://github.com/Shashi456/erdos-formalizations/blob/main/Erdos/P750/Proof.lean)；发表状态：公开 Lean 源码；核验：主声明 erdos_750_FC 与题面相符，无 sorry；但把 Stiebitz 型下界封装为 axiom stiebitz_lower_bound。

#### #783

- 官方状态：`solved`
- 精确题面：Fix some constant $C>0$ and let $n$ be large. Let $A\subseteq \{2,\ldots,n\}$ be such that $(a,b)=1$ for all $a\neq b\in A$ and $\sum_{n\in A}\frac{1}{n}\leq C$. What choice of such an $A$ minimises the number of integers $m\leq n$ not divisible by any $a\in A$? Is this minimised by letting $n\geq q_1>q_2>\cdots$ be the consecutive primes in decreasing order and choosing $A=\{q_1,\ldots,q_k\}$ where $k$ is maximal such that\[\sum_{i=1}^k\frac{1}{q_i}\leq C?\]
- 范围解释：冻结题面既问固定 C、n→∞ 时未被 A 中元素整除的整数数目的最小化，又明确猜测由不超过 n 的最大连续素数组成的 A 是字面上的极小者。
- 闭合判定：`status_or_statement_mismatch`
- 判定理由：Tao 的结果严格闭合了预期的渐近极值问题，也说明冻结题面的特定连续素数构造并非精确极小者；但它没有分类每个有限 n 的所有精确极小集合。官网状态依据的是后来修订后的渐近版本。
- Lean 审计：未发现公开完成的 Lean 证明；formal-conjectures 若有对应编码仍含 sorry。
- 尚存不确定性：需要在总报告中同时保存 frozen 与现行题面，并明确“渐近最优值已解”不等于“有限 n 精确极小者已分类”。
- 证据：

  - `other` [Terence Tao, Erdős 783](https://terrytao.wordpress.com/wp-content/uploads/2026/02/erdos783-3.pdf)；发表状态：公开研究稿；核验：Theorem 1.1 给出任意两两互素 A 的未覆盖密度 Dickman 下界及渐近达到构造，从而确定渐近最优值；它不声称对每个有限 n 给出精确极小集合。
  - `other` [Erdős Problem #783 current record](https://www.erdosproblems.com/783)；发表状态：官方持续更新题页；核验：现行题页已弱化/改写早先的字面极值猜测，并记录对最大连续素数构造的改进扰动；因此当前 SOLVED 与 frozen 文字并非同一精确陈述。

#### #793

- 官方状态：`proved (Lean)`
- 精确题面：Let $F(n)$ be the maximum possible size of a subset $A\subseteq\{1,\ldots,n\}$ such that $a\nmid bc$ whenever $a,b,c\in A$ with $a\neq b$ and $a\neq c$. Is there a constant $C$ such that\[F(n)=\pi(n)+(C+o(1))n^{2/3}(\log n)^{-2}?\]
- 范围解释：确定满足 a∤bc（a 与 b、c 分别不同）的最大集合大小 F(n) 是否具有 π(n)+(C+o(1))n^(2/3)/(log n)^2 的展开。
- 闭合判定：`closed_scope_caveat`
- 判定理由：常数及误差阶完全匹配原题，范围没有明显缺失；保留意见只在未评审状态和 PNT 被公理化。
- Lean 审计：外部 Lean 文件无 sorry，但 #print axioms 含 pnt_hypothesis；它核验组合论/渐近推导而非从 Mathlib 内部证明 PNT。formal-conjectures 基准仍是 sorry。
- 尚存不确定性：等待可引用的预印本/期刊版及 PNT 接口的正规化。
- 证据：

  - `other` [Erdős 793 proof manuscript](https://www.ulam.ai/research/erdos793.pdf)；发表状态：公开未评审手稿；核验：主定理给出 C=27/2 的精确二阶渐近，条件允许 b=c，与 frozen 题面的 a≠b、a≠c 完全一致。
  - `public_lean` [Woett/ErdosProblem793.lean](https://github.com/Woett/Lean-files/blob/main/ErdosProblem793.lean)；发表状态：公开 Lean 源码；核验：主声明 Strongly2.main 编码同一渐近式，无 sorry；素数计数函数的 PNT 渐近被作为 pnt_hypothesis 公理输入。

#### #846

- 官方状态：`disproved (Lean)`
- 精确题面：Let $A\subset \mathbb{R}^2$ be an infinite set for which there exists some $\epsilon>0$ such that in any subset of $A$ of size $n$ there are always at least $\epsilon n$ with no three on a line. Is it true that $A$ is the union of a finite number of sets where no three are on a line?
- 范围解释：构造无限平面点集：每个 n 点子集都有线性大的无三点共线子集，但整个点集不能分成有限多个无三点共线集。
- 闭合判定：`closed_verified`
- 判定理由：已发表结果与直接几何预印本相互印证，恰好同时满足局部线性一般位置子集与全局不可有限着色两个条件。
- Lean 审计：截至本次核查，没有找到与官方“(Lean)”标签对应的公开无 sorry 完成稿；固定 formal-conjectures 文件本身含 sorry，只是 benchmark。数学反例由论文独立闭合。
- 尚存不确定性：官方应补上真正的 Lean 证明链接，或移除/解释 Lean 标签。
- 证据：

  - `peer_reviewed_paper` [Colouring versus density in hereditary set systems](https://doi.org/10.1112/jlms.12987)；发表状态：Journal of the London Mathematical Society 已发表论文；核验：论文给出相应遗传超图的线性独立数而染色数无限；一般位置投影把构造实现为三点共线关系，得到题目要求的反例。
  - `preprint` [On infinite sets with no 3 on a line](https://arxiv.org/abs/2602.21275)；发表状态：arXiv 预印本；核验：Theorem 1.1 直接以平面点集语言陈述同一反例，补足从抽象遗传系统到几何实现的范围核对。

#### #847

- 官方状态：`disproved`
- 精确题面：Let $A\subset \mathbb{N}$ be an infinite set for which there exists some $\epsilon>0$ such that in any subset of $A$ of size $n$ there is a subset of size at least $\epsilon n$ which contains no three-term arithmetic progression. Is it true that $A$ is the union of a finite number of sets which contain no three-term arithmetic progression?
- 范围解释：要求无限整数集的每个有限子集都有线性大的无三项等差数列子集，却不能有限分割为无三项等差数列集。
- 闭合判定：`closed_verified`
- 判定理由：已发表论文的对象、局部比例常数和全局有限分割失败与 frozen 题面逐项一致。
- Lean 审计：无公开完成 Lean 证明；formal-conjectures 对应文件含 sorry，不能作为闭合证据。
- 尚存不确定性：无实质数学范围不确定性。
- 证据：

  - `peer_reviewed_paper` [Colouring versus density in hereditary set systems](https://doi.org/10.1112/jlms.12987)；发表状态：Journal of the London Mathematical Society 已发表论文；核验：论文在三项等差数列超图上构造无限染色数而所有有限诱导子超图独立数至少 μn（某 μ<1/2），正是否定题面蕴含。

#### #851

- 官方状态：`proved`
- 精确题面：Let $\epsilon>0$. Is there some $r\ll_\epsilon 1$ such that the density of integers of the form $2^k+n$, where $k\geq 0$ and $n$ has at most $r$ prime divisors, is at least $1-\epsilon$?
- 范围解释：对每个 ε>0，要求存在仅依赖 ε 的 r，使几乎所有整数（下自然密度至少 1−ε）可写成 2^k 加一个至多含 r 个素因子的整数。
- 闭合判定：`closed_scope_caveat`
- 判定理由：公开源码的主定理比 frozen 题面更强，且关键筛法、乘法阶稀疏估计、二阶矩和最终量词均已核对，并有独立专家确认；但当前仍是 AI 生成后修订的公开手稿，尚无预印本版本号或同行评审。
- Lean 审计：官方只标 Formalised statement；formal-conjectures 固定文件仍含 sorry。未发现公开完成的 Lean 证明，讨论中也明确指出基本筛法尚未现成形式化。
- 尚存不确定性：建议发布带版本历史的 arXiv 稿并由筛法专家正式审阅；现阶段不能称为 Lean 闭合。
- 证据：

  - `other` [Powers of Two Plus an Almost-Prime: a Density One Theorem](https://www.overleaf.com/read/svgbjzpxxppv)；发表状态：公开未评审 Overleaf 手稿；核验：本次通过只读令牌取得 main.tex 全文；Theorem 1 对 Ω(n)（计重数）证明下自然密度≥1−ε，因而更强地推出对不同素因子数 ω(n) 的原题。参数选择明确先给 ε 再给固定 r。
  - `other` [Erdős 851 official discussion](https://www.erdosproblems.com/forum/thread/851)；发表状态：公开专家复核记录；核验：Tao 在逐项解释一、二阶矩与奇异级数后明确确认 proof is correct；Sawhney 还记录与 Green 的更强定量版本。

#### #858

- 官方状态：`solved`
- 精确题面：Let $A\subseteq \{1,\ldots,N\}$ be such that there is no solution to $at=b$ with $a,b\in A$ and the smallest prime factor of $t$ is $>a$. Estimate the maximum of\[\frac{1}{\log N}\sum_{n\in A}\frac{1}{n}.\]
- 范围解释：在给定乘法禁形条件下，求 max_A (1/log N)Σ_{a∈A}1/a 的精确渐近。
- 闭合判定：`closed_scope_caveat`
- 判定理由：手稿给出上下界匹配的精确常数，确实比早先 o(1) 结论强并覆盖原问题；唯一主要保留是尚未同行评审或形式化。
- Lean 审计：未发现公开 Lean 完成稿。
- 尚存不确定性：需要论文级独立审查，特别是 Bellman 递推的全局最优性与误差一致性。
- 证据：

  - `other` [Erdős 858 asymptotic solution](https://www.ulam.ai/research/erdos858-asymptotic.pdf)；发表状态：公开未评审手稿；核验：主定理证明未归一化最大值 M(N)=(c₂+o(1))log N，其中 c₂≈0.618771；除以 log N 即得 frozen 所问极限，并给出匹配构造和树/Bellman 上界。

#### #863

- 官方状态：`proved`
- 精确题面：Let $r\geq 2$ and let $A\subseteq \{1,\ldots,N\}$ be a set of maximal size such that there are at most $r$ solutions to $n=a+b$ with $a\leq b$ for any $n$. (That is, $A$ is a $B_2[r]$ set.) Similarly, let $B\subseteq \{1,\ldots,N\}$ be a set of maximal size such that there are at most $r$ solutions to $n=a-b$ for any $n$. If $\lvert A\rvert\sim c_rN^{1/2}$ as $N\to \infty$ and $\lvert B\rvert \sim c_r'N^{1/2}$ as $N\to \infty$ then is it true that $c_r\neq c_r'$ for $r\geq 2$? Is it true that $c_r'<c_r$?
- 范围解释：比较和表示受限的 B₂[r] 极值常数 c_r 与差表示受限常数 c'_r，并问 r≥2 时是否 c'_r<c_r。
- 闭合判定：`closed_verified`
- 判定理由：已发表下界与经典上界给出所有 r≥2 的严格方向 c'_r<c_r，因此 c_r≠c'_r 也随即成立。
- Lean 审计：没有公开 Lean 完成稿；本题闭合依据已发表组合数论结果。
- 尚存不确定性：题面以渐近常数存在为条件；证据在同一条件下比较，范围无缺口。
- 证据：

  - `peer_reviewed_paper` [Upper and Lower Bounds for Finite B_h[g] Sequences](https://doi.org/10.1006/jnth.2001.2767)；发表状态：Journal of Number Theory 97 (2002) 已发表论文；核验：论文给出 B₂[r] 的显式构造下界；与经典差集计数上界 c'_r≤√r 组合，得到 r≥2 时 c_r>√r≥c'_r，严格回答两问。
  - `other` [A short note on Erdős 863](https://boonsuan.github.io/erdos863.pdf)；发表状态：公开说明稿；核验：说明稿把论文常数代入并逐项写出严格不等式，确认不是仅有相同量级的估计。

#### #865

- 官方状态：`proved (Lean)`
- 精确题面：There exists a constant $C>0$ such that, for all large $N$, if $A\subseteq \{1,\ldots,N\}$ has size at least $\frac{5}{8}N+C$ then there are distinct $a,b,c\in A$ such that $a+b,a+c,b+c\in A$.
- 范围解释：证明 5/8 是迫使 A 中出现六数配置 a,b,c,a+b,a+c,b+c 的渐近阈值，并要求 a,b,c 两两不同。
- 闭合判定：`closed_verified`
- 判定理由：预印本给出更强的精确渐近，Lean 又以显式常数机器核验题面充分方向，范围和 distinct 条件均匹配。
- Lean 审计：在公开仓库审查到完整主声明，无 sorry/axiom，常数 53 给出题面所需某个 C；formal-conjectures 基准文件的 sorry 不构成冲突。
- 尚存不确定性：仅有通常的预印本同行评审等待，不影响题面结论已有公开可核代码。
- 证据：

  - `preprint` [Erdős Problem 865](https://arxiv.org/abs/2606.29361)；发表状态：arXiv 预印本；核验：主定理给出 f₃(N)=5N/8+O(1)，从而存在绝对 C 使 frozen 的充分条件成立，并包含匹配下界。
  - `public_lean` [mrricky22/erdos-865-lean](https://github.com/mrricky22/erdos-865-lean)；发表状态：公开 Lean 仓库；核验：Main.lean 的 erdos865_upper_bound 与 erdos865_contains_triple 推出 8|A|≤5N+53 的显式界；主声明 erdos865 覆盖充分条件及 distinct，未见 sorry 或新增 axiom。

#### #868

- 官方状态：`solved`
- 精确题面：If $A$ is an additive basis of order $2$, and $1_A\ast 1_A(n)\to \infty$ as $n\to \infty$, then must $A$ contain a minimal additive basis of order $2$? (i.e. such that deleting any element creates infinitely many $n\not\in A+A$) What if $1_A\ast 1_A(n) >\epsilon \log n$ (for all large $n$, for arbitrary fixed $\epsilon>0$)?
- 范围解释：问表示数趋于无穷、乃至大于 εlog n 的二阶加法基是否必含极小子基。
- 闭合判定：`closed_scope_caveat`
- 判定理由：主定理的表示数下界和“不含任何极小子基”完全对准 frozen 题面；但证据尚为单一公开手稿，未同行评审。
- Lean 审计：formal-conjectures 对应文件含 sorry；没有找到外部完成的 Lean 证明。
- 尚存不确定性：需专家审查随机迭代构造及所有“充分大 n”事件的同时成立性。
- 证据：

  - `other` [Robust Additive Bases Without Minimal Subbases](https://github.com/Larsen-Daniel/Erdos-868/blob/main/868.pdf)；发表状态：公开未评审手稿；核验：本次核对 Theorem 1：存在 ε>0 与 A，使所有充分大 m 有 r_A(m)>εlog m，而 A 不含任何二阶极小加法子基；因此同时否定较弱的 r_A(m)→∞ 问句。

#### #869

- 官方状态：`disproved`
- 精确题面：If $A_1,A_2$ are disjoint additive bases of order $2$ (i.e. $A_i+A_i$ contains all large integers) then must $A=A_1\cup A_2$ contain a minimal additive basis of order $2$ (one such that deleting any element creates infinitely many $n\not\in A+A$)?
- 范围解释：问两个不交二阶加法基的并是否必含二阶极小加法子基。
- 闭合判定：`closed_scope_caveat`
- 判定理由：公开手稿包含逐字反例，且本次已定位到推导 P2 真/P3 假的章节；尚缺同行评审或形式化的第二层验证。
- Lean 审计：未发现公开 Lean 完成稿。
- 尚存不确定性：需独立复核通用随机选择机制 Theorem 2 对所有输入机制的统一概率论论证。
- 证据：

  - `other` [Robustness Properties of Additive Bases Are Independent](https://github.com/Larsen-Daniel/Erdos-869/blob/main/869.pdf)；发表状态：公开未评审手稿；核验：Theorem 1 实现稳健性、可分解性、含极小子基三性质的全部八种组合；其中 P2 真而 P3 假的构造正给出 A=B⊔C、B和C均为基、A却无极小子基。

#### #871

- 官方状态：`disproved (Lean)`
- 精确题面：Let $A$ be an additive basis of order $2$ with $1_A*1_A(n)\to\infty$. Must $A$ split into two disjoint additive bases of order $2$?
- 范围解释：构造表示数 r_A(n)→∞ 的二阶渐近基 A，使 A 不能分成两个不交的二阶渐近基。
- 闭合判定：`closed_scope_caveat`
- 判定理由：数学手稿的两个主定理直接构成所需反例；保留意见是手稿未评审以及官方 Lean 标签缺乏可核链接。
- Lean 审计：官方虽标“(Lean)”，但固定 formal-conjectures 文件仍有 sorry，且本次未找到另一份公开无 sorry 的完成代码；不能把标签当成可复现形式证明。
- 尚存不确定性：需官方提供所称 Lean 代码，或把状态改为仅手稿证否。
- 证据：

  - `other` [An Additive Basis with Many Representations that Cannot be Partitioned into Two Bases](https://github.com/Larsen-Daniel/Erdos-871/blob/main/paper.pdf)；发表状态：公开未评审手稿；核验：Theorem 9 证明 r_A(n)→∞，Theorem 10 证明任何 A=B⊔C 都至少有一边不是渐近基，最终 Theorem 1 合并两项，范围精确。

#### #884

- 官方状态：`disproved (Lean)`
- 精确题面：Is it true that, for any $n$, if $d_1<\cdots <d_t$ are the divisors of $n$, then\[\sum_{1\leq i<j\leq t}\frac{1}{d_j-d_i} \ll 1+\sum_{1\leq i<t}\frac{1}{d_{i+1}-d_i},\]where the implied constant is absolute?
- 范围解释：问所有除数对倒数间距之和，是否由相邻除数倒数间距之和加 1 以绝对常数控制。
- 闭合判定：`closed_scope_caveat`
- 判定理由：无条件手稿的主定理与原不等式逻辑等价，范围无缺失；但尚无同行评审及可复现 Lean 证据。
- Lean 审计：未找到与官方“(Lean)”对应的公开完成代码；formal-conjectures 固定文件含 sorry。
- 尚存不确定性：重点等待对多尺度构造中跨尺度 S 贡献估计的独立审稿。
- 证据：

  - `other` [A Question of Erdős on Reciprocals of Gaps Between Divisors](https://github.com/Larsen-Daniel/Erdos-884/blob/main/884.pdf)；发表状态：公开未评审手稿；核验：Theorem 1.1 证明 T(div(n))/(1+S(div(n))) 在自然数 n 上无界，恰是否定存在绝对隐常数；构造为无条件多尺度素数乘积。
  - `other` [Tao's conditional Erdős 884 note](https://terrytao.wordpress.com/wp-content/uploads/2025/09/erdos-884.pdf)；发表状态：公开条件性研究稿；核验：较早的条件构造解释高加性能量机制；Larsen 后续稿去掉素数 k-tuples 假设，二者在反例机制上相互印证。

#### #888

- 官方状态：`solved`
- 精确题面：What is the size of the largest $A\subseteq \{1,\ldots,n\}$ such that if $a\leq b\leq c\leq d\in A$ are such that $abcd$ is a square then $ad=bc$?
- 范围解释：估计最大 A⊆[n]，使任意 a≤b≤c≤d∈A 且 abcd 为平方时必有 ad=bc。
- 闭合判定：`closed_scope_caveat`
- 判定理由：手稿同时给出匹配到常数因子的上下界，闭合了题目要求的数量级；证据成熟度仅为公开手稿。
- Lean 审计：formal-conjectures 文件仍含 sorry；未发现外部完成 Lean 证明。
- 尚存不确定性：需要同行审查图论上界是否覆盖 a,b,c,d 可相等的全部退化情形。
- 证据：

  - `other` [Erdős 888 solution](https://www.ulam.ai/research/erdos888.pdf)；发表状态：公开未评审手稿；核验：主结果给出最大值在常数因子意义下为 n log log n/log n；下界由适当平方自由半素数集给出，上界转化为图结构，正符合“size”问题通常所求量级。

#### #896

- 官方状态：`solved`
- 精确题面：Estimate the maximum of $F(A,B)$ as $A,B$ range over all subsets of $\{1,\ldots,N\}$, where $F(A,B)$ counts the number of $m$ such that $m=ab$ has exactly one solution (with $a\in A$ and $b\in B$).
- 范围解释：求 A,B⊆[N] 时恰有一个表示 m=ab（a∈A,b∈B）的 m 的最大数目之数量级。
- 闭合判定：`closed_scope_caveat`
- 判定理由：已发表深定理与新公开稿组合给出匹配数量级；但真正补齐本题下界的部分尚未同行评审。
- Lean 审计：未发现公开 Lean 完成稿。
- 尚存不确定性：需审查手稿的唯一表示构造在边界区间及非对称 A,B 上的计数误差。
- 证据：

  - `peer_reviewed_paper` [The distribution of integers with a divisor in a given interval](https://doi.org/10.4007/annals.2008.168.367)；发表状态：Annals of Mathematics 168 (2008) 已发表论文；核验：Ford 的除数区间/乘法表定理提供所需上界尺度及指数 δ=1−(1+log log 2)/log 2 的经典输入。
  - `other` [Erdős 896 solution](https://www.ulam.ai/research/erdos896.pdf)；发表状态：公开未评审手稿；核验：主定理给出 max F(A,B) ≍ N²/((log N)^δ(log log N)^(3/2))；新下界与 Ford 型上界同阶，覆盖有序 A、B 而非只处理 A=B。

#### #948

- 官方状态：`solved`
- 精确题面：Is there a function $f(n)$ and a $k$ such that in any $k$-colouring of the integers there exists a sequence $a_1<\cdots$ such that $a_n<f(n)$ for infinitely many $n$ and the set\[\left\{ \sum_{i\in S}a_i : \textrm{finite }S\right\}\]does not contain all colours?
- 范围解释：要求存在统一函数 f 与有限 k，使每个整数 k-着色都含递增序列，其有限和集漏掉某颜色，并且 a_n<f(n) 无穷多次。
- 闭合判定：`closed_verified`
- 判定理由：公开 Lean 证明已独立编译、公理审计通过，并完整否定原存在性命题：任意候选 f、k≥2 都有一个着色，使每条满足增长条件的序列之非空有限和命中所有颜色。因此官网 SOLVED 标签有可核实的精确闭合证据。
- Lean 审计：从官方 source-bearing URL 解码源码，在独立 Mathlib v4.28.0 环境实际编译成功；源码无 sorry、admit、自定义 axiom、unsafe 或 opaque。对 ErdosGalvin.main 与 main_finite 执行 #print axioms，均仅有 propext、Classical.choice、Quot.sound。
- 尚存不确定性：手稿与代码尚未归档到带 commit 的稳定仓库，也未发现 arXiv 或同行评审版本；这影响证据持久性，但不构成当前数学闭合缺口。
- 证据：

  - `official_page` [Erdős Problem #948](https://www.erdosproblems.com/948)；发表状态：official_database；核验：题页标 SOLVED；论坛 post-7119 给出公开手稿和包含完整源码的 Lean live 链接，后续帖子记录筛查、人工复核与证明梗概。
  - `public_manuscript` [Public manuscript for Erdős Problem #948](https://www.overleaf.com/read/grttvnmptzwz#223cb5)；发表状态：public_manuscript；核验：公开 read 链接可匿名访问；手稿给出对应组合构造，但未发现 arXiv、期刊或带版本提交的永久归档。
  - `public_lean` [Erdős #948 source-bearing Lean submission (forum post-7119)](https://www.erdosproblems.com/forum/thread/948#post-7119)；发表状态：public_formalization；核验：post-7119 的 Lean live href 可解码出 19,348 字符源码。ErdosGalvin.main 与 main_finite 对任意 f、任意 k≥2 构造着色，使每条满足 a_n<f(n) 无穷多次的严格递增整数序列，其非空有限和命中每一种颜色；这正是否定官网所求 f、k，且非空有限和表述避开空和歧义。

#### #960

- 官方状态：`disproved`
- 精确题面：Let $r,k\geq 2$ be fixed. Let $A\subset \mathbb{R}^2$ be a set of $n$ points with no $k$ points on a line. Determine the threshold $f_{r,k}(n)$ such that if there are at least $f_{r,k}(n)$ many ordinary lines (lines containing exactly two points) then there is a set $A'\subseteq A$ of $r$ points such that all $\binom{r}{2}$ many lines determined by $A'$ are ordinary. Is it true that $f_{r,k}(n)=o(n^2)$, or perhaps even $\ll n$?
- 范围解释：对固定 r,k≥2，问足够多 ordinary lines 是否迫使 r 点完全子集的所有两点连线均 ordinary；特别猜测阈值为 o(n²)。
- 闭合判定：`closed_scope_caveat`
- 判定理由：预印本在允许参数范围内给出二次量级反例，严格证否了题中特别提出的普遍 o(n²) 猜想；但 frozen 题面首句还要求估计各固定 r,k 的 f_{r,k}(n)，该总体阈值问题没有闭合，因此 DISPROVED 只能理解为猜想方向而非整条复合问题已解决。
- Lean 审计：没有公开 Lean 完成稿。
- 尚存不确定性：各参数对的完整 f_{r,k}(n) 分类仍可开放，官方应把“猜想被否定”与“阈值问题完全求解”分开标注。
- 证据：

  - `preprint` [APSSV26b, Section 2](https://arxiv.org/abs/2604.06609)；发表状态：arXiv 预印本；核验：Theorem 2.1 对 r≥3、k≥4 构造无 k 点共线的 n 点集，ordinary lines 至少 n²/12−O(n)，却没有所需 r 点团；固定一组参数已足以否定题面的普遍 o(n²) 猜想。

#### #965

- 官方状态：`disproved`
- 精确题面：For every two-colouring of $\mathbb R$, must there be $A\subseteq\mathbb R$ of cardinality $\aleph_1$ such that all $a+b$ with distinct $a,b\in A$ have one colour?
- 范围解释：问每个实数二着色是否都含大小 ℵ₁ 的集合，使所有不同元素两两和同色。
- 闭合判定：`closed_verified`
- 判定理由：Komjáth 的已发表 ZFC 定理比题面更强，不依赖连续统假设，直接给出一个反例着色。
- Lean 审计：formal-conjectures 的 965 声明含 sorry，不是形式证明；无外部完成 Lean 代码。
- 尚存不确定性：无实质范围不确定性。
- 证据：

  - `peer_reviewed_paper` [A Certain 2-Coloring of the Reals](https://doi.org/10.14321/realanalexch.41.1.0227)；发表状态：Real Analysis Exchange 41 (2016) 已发表论文；核验：Komjáth 在 ZFC 中构造实数二着色，使每个不可数 A 的不同元素 k 项和（尤其 k=2）两种颜色都出现；故不存在题面要求的 ℵ₁ 单色 A。
  - `peer_reviewed_paper` [Pairwise sums in colourings of the reals](https://doi.org/10.1007/s12188-016-0166-x)；发表状态：Abhandlungen aus dem Mathematischen Seminar der Universität Hamburg 87 (2017) 已发表论文；核验：在 CH 下给出更早的同类反例；与 Komjáth 的无 CH 结果方向一致，但本次闭合主要依赖后者的 ZFC 定理。

#### #986

- 官方状态：`proved`
- 精确题面：For any fixed $k\geq 3$,\[R(k,n) \gg \frac{n^{k-1}}{(\log n)^c}\]for some constant $c=c(k)>0$.
- 范围解释：对每个固定 k≥3，证明非对角 Ramsey 数 R(k,n) 至少为 n^(k−1) 除以某个 log 的固定幂。
- 闭合判定：`closed_verified`
- 判定理由：预印本的指数、固定参数与常数依赖完全匹配，并给出明确对数幂，严格强于“存在某 c(k)>0”。
- Lean 审计：未发现公开 Lean 完成稿。
- 尚存不确定性：尚待同行评审，但没有题面范围缺口。
- 证据：

  - `preprint` [Off-diagonal Ramsey numbers](https://arxiv.org/abs/2605.28793)；发表状态：arXiv 预印本；核验：Bradač 的 Theorem 1.1 对每个 s≥3 给出 R(s,k)≥c_s k^(s−1)/(log k)^(2s−4)。令论文固定参数 s 对应题面的 k，再把论文增长变量 k 重命名为 n，即得到题面可取 c(k)=2k−4。

#### #987

- 官方状态：`proved`
- 精确题面：Let $x_1,x_2,\ldots \in (0,1)$ be an infinite sequence and let\[A_k=\limsup_{n\to \infty}\left\lvert \sum_{j\leq n} e(kx_j)\right\rvert,\]where $e(x)=e^{2\pi ix}$. Is it true that\[\limsup_{k\to \infty} A_k=\infty?\]Is it possible for $A_k=o(k)$?
- 范围解释：对任意 (0,1) 序列的指数和 limsup A_k，第一问要求 A_k 沿 k 无界；第二问要求构造 A_k=o(k) 的序列。
- 闭合判定：`closed_verified`
- 判定理由：第一问由经典已发表论文闭合，第二问由新预印本给出满足全体 k 的显式渐近控制，两部分合在一起覆盖完整 frozen 题面。
- Lean 审计：formal-conjectures 对应文件含 sorry；未发现完成 Lean 证明。
- 尚存不确定性：第二部分尚待同行评审。
- 证据：

  - `peer_reviewed_paper` [On a problem of Erdős](https://doi.org/10.1112/jlms/s1-42.1.133)；发表状态：Journal of the London Mathematical Society 42 (1967) 已发表论文；核验：Clunie 证明 A_k≫√k 对无穷多个 k 成立，直接肯定回答第一问。
  - `preprint` [APSSV26b, Section 3](https://arxiv.org/abs/2604.06609)；发表状态：arXiv 预印本；核验：Theorem 3.1 构造序列使所有 k 有 A_k≪√(k log k)=o(k)，肯定回答第二问；这里 A_k 仍是对 n 的 limsup，不是有限截断替代。

#### #990

- 官方状态：`disproved (Lean)`
- 精确题面：Let $f=a_0+\cdots+a_dx^d\in \mathbb{C}[x]$ be a polynomial. Is it true that, if $f$ has roots $z_1,\ldots,z_d$ with corresponding arguments $\theta_1,\ldots,\theta_d\in [0,2\pi]$, then for all intervals $I\subseteq [0,2\pi]$\[\left\lvert (\# \theta_i \in I) - \frac{\lvert I\rvert}{2\pi}d\right\rvert \ll \left(n\log M\right)^{1/2},\]where $n$ is the number of non-zero coefficients of $f$ and\[M=\frac{\lvert a_0\rvert+\cdots +\lvert a_d\rvert}{(\lvert a_0\rvert\lvert a_d\rvert)^{1/2}}.\]
- 范围解释：问多项式零点辐角在任意区间的偏差，是否可由非零系数数 n 与 Mahler 型量 M 的 √(n log M) 统一控制。
- 闭合判定：`closed_verified`
- 判定理由：预印本的反例机制与无公理 Lean 族声明相互核对，恰好击穿 frozen 的统一 O 界。
- Lean 审计：外部文件无 sorry/axiom，主声明确是否定“存在绝对 C”，不是只验证单个数值例。formal-conjectures 基准的 sorry 应忽略。
- 尚存不确定性：无实质范围缺口。
- 证据：

  - `preprint` [APSSV26b sparse polynomial counterexample](https://arxiv.org/abs/2604.06609)；发表状态：arXiv 预印本；核验：论文构造稀疏多项式族，使零点辐角偏差相对 √(n log M) 无界，从而否定绝对隐常数。
  - `public_lean` [yuta0x89/ErdosProblems Erdős990.lean](https://github.com/yuta0x89/ErdosProblems/blob/main/Erdos990.lean)；发表状态：公开 Lean 源码；核验：explicit_counterexample_family 构造反例族，erdos990_no_absolute_constant_sparseErdosTuran 否定绝对常数；未见 sorry 或新增 axiom。

#### #992

- 官方状态：`disproved`
- 精确题面：Let $x_1<x_2<\cdots$ be an infinite sequence of integers. Is it true that, for almost all $\alpha \in [0,1]$, the discrepancy\[D(N)=\max_{I\subseteq [0,1]} \lvert \#\{ n\leq N : \{ \alpha x_n\}\in I\} - \lvert I\rvert N\rvert\]satisfies\[D(N) \ll N^{1/2}(\log N)^{o(1)}?\]Or even\[D(N)\ll N^{1/2}(\log\log N)^{O(1)}?\]
- 范围解释：问任意递增整数列是否对几乎所有 α 都有 D(N)≤√N 乘亚对数因子，或至少乘 log log 的固定幂。
- 闭合判定：`closed_verified`
- 判定理由：已发表论文给出同一 discrepancy 定义下的几乎处处反例序列，直接否定两种上界。
- Lean 审计：没有公开 Lean 完成稿。
- 尚存不确定性：无实质范围不确定性。
- 证据：

  - `peer_reviewed_paper` [The Size of Trigonometric and Walsh Series and Uniform Distribution Mod 1](https://doi.org/10.1112/jlms/50.3.454)；发表状态：Journal of the London Mathematical Society 50 (1994) 已发表论文；核验：Berkes–Philipp 构造递增整数列，使几乎处处 limsup D(N)/sqrt(N log N)>0；固定的 (log N)^{1/2} 损失不属于 (log N)^{o(1)}，也大于任意固定 log log 幂，故同时证否两问，且“几乎处处”量词一致。

#### #997

- 官方状态：`proved (Lean)`
- 精确题面：Call $x_1,x_2,\ldots \in (0,1)$ well-distributed if, for every $\epsilon>0$, if $k$ is sufficiently large then, for all $n>0$ and intervals $I\subseteq [0,1]$,\[\lvert \# \{ n<m\leq n+k : x_m\in I\} - \lvert I\rvert k\rvert < \epsilon k.\]Is it true that, for every $\alpha$, the sequence $\{ \alpha p_n\}$ is not well-distributed, if $p_n$ is the sequence of primes?
- 范围解释：对每个实数 α，证明素数序列小数部分 {αp_n} 不满足所有平移窗口上的一致 well-distributed 条件。
- 闭合判定：`closed_scope_caveat`
- 判定理由：数学预印本覆盖所有 α，量词精确；Lean 证据尚把核心深定理公理化，因此官方“Lean”需附此限定。
- Lean 审计：公开代码无 sorry，但 #print axioms 含 maynardTaoBFT；Lean 核验从有界素数间隔定理到结论的推导。formal-conjectures 基准仍有 sorry。
- 尚存不确定性：需将 maynardTaoBFT 接到经过核验的形式化定理，或明确列为可信外部公理。
- 证据：

  - `preprint` [APSSV26, Section 4](https://arxiv.org/abs/2603.29961)；发表状态：arXiv 预印本；核验：Theorem 4.1 对每个实 α 给出不良窗口，覆盖有理、无理和整数 α，并使用与题面相同的任意起点 n 的窗口定义。
  - `public_lean` [Erdős 997 Lean proof gist](https://gist.github.com/pitmonticone/016f2ed66b4cd1c4c4b9998095170e60)；发表状态：公开 Lean 源码；核验：主声明 erdos997 与“∀α，不 well-distributed”一致，无 sorry；Maynard–Tao bounded gaps 的输入被声明为 axiom maynardTaoBFT。

#### #1014

- 官方状态：`proved (Lean)`
- 精确题面：Let $R(k,l)$ be the Ramsey number, so the minimal $n$ such that every graph on at least $n$ vertices contains either a $K_k$ or an independent set on $l$ vertices. Prove, for fixed $k\geq 3$, that\[\lim_{l\to \infty}\frac{R(k,l+1)}{R(k,l)}=1.\]
- 范围解释：固定 k≥3，证明非对角 Ramsey 数相邻参数比 R(k,l+1)/R(k,l) 在 l→∞ 时趋于 1。
- 闭合判定：`closed_verified`
- 判定理由：公开论文证明与无新增公理的 Lean 文件双重覆盖完整极限陈述。
- Lean 审计：外部 Lean 主声明与 frozen 题面一致，无 sorry/axiom；不是 formal-conjectures 中带 sorry 的题面占位。
- 尚存不确定性：无实质不确定性；建议为代码固定 release/commit。
- 证据：

  - `other` [Ramsey.pdf](https://cdn.openai.com/pdf/6dc7175d-d9e7-4b8d-96b8-48fe5798cd5b/Ramsey.pdf)；发表状态：公开研究稿；核验：论文主定理直接给出每个固定 k≥3 的相邻比极限，而非只给上下界同阶。
  - `public_lean` [plby/lean-proofs Erdős1014](https://github.com/plby/lean-proofs/blob/main/ErdosProblems/Erdos1014.md)；发表状态：公开 Lean 文档与源码；核验：erdos1014(k)(hk) 编码固定 k≥3 的极限；源码无 sorry、无新增 axiom，#print axioms 仅标准基础。

#### #1021

- 官方状态：`proved`
- 精确题面：Is it true that, for every $k\geq 3$, there is a constant $c_k>0$ such that\[\mathrm{ex}(n,G_k) \ll n^{3/2-c_k},\]where $G_k$ is the bipartite graph between $\{y_1,\ldots,y_k\}$ and $\{z_1,\ldots,z_{\binom{k}{2}}\}$, with each $z_j$ joined to a unique pair of $y_i$?
- 范围解释：对每个 k≥3，证明 K_k 的 1-细分图 G_k 的极值数严格低于 n^(3/2)，即有某 c_k>0。
- 闭合判定：`closed_verified`
- 判定理由：两篇同行评审论文给出比题面更明确的正指数节省，且 G_k 的图同构就是 K_k 的 1-细分。
- Lean 审计：未发现公开 Lean 完成稿。
- 尚存不确定性：无实质范围不确定性。
- 证据：

  - `peer_reviewed_paper` [On the Extremal Number of Subdivisions](https://doi.org/10.1093/imrn/rnz088)；发表状态：International Mathematics Research Notices 2021 已发表论文；核验：Conlon–Lee 对一侧最大度 2 且 C4-free 的二部图证明 ex(n,H)=O(n^(3/2−δ))；G_k 正满足条件，并可取显式正 c_k（官网记录 6^−k）。
  - `peer_reviewed_paper` [Improved bounds for the extremal number of subdivisions](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v26i3p3)；发表状态：Electronic Journal of Combinatorics 26 (2019) 已发表论文；核验：Janzer 改进指数损失到可取 c_k=1/(4k−6)，再次直接覆盖所有固定 k≥3。

#### #1022

- 官方状态：`proved (Lean)`
- 精确题面：Is there a constant $c_t$, where $c_t\to \infty$ as $t\to \infty$, such that if $\mathcal{F}$ is a finite family of finite sets, all of size at least $t$, and for every set $X$ there are $<c_t\lvert X\rvert$ many $A\in \mathcal{F}$ with $A\subseteq X$, then $\mathcal{F}$ has chromatic number $2$ (in other words, has property B)?
- 范围解释：题面问是否存在 c_t→∞，使每个满足局部稀疏度 |{A∈F:A⊆X}|<c_t|X| 的、边大小至少 t 的有限超图都具有 property B。
- 闭合判定：`status_or_statement_mismatch`
- 判定理由：数学上原命题已被严格证否，并有公开 Lean 反命题；错误在官方状态方向，应从 PROVED 改为 DISPROVED。
- Lean 审计：外部 Lean 文件无 sorry/axiom，且证明的确是 not_erdos_1022；这与官网“proved”方向标签冲突，不是代码范围不足。
- 尚存不确定性：需官方修正状态与数据库枚举，避免汇总时把否定证明算成肯定证明。
- 证据：

  - `preprint` [Hypergraph Colouring and Degeneracy](https://arxiv.org/abs/1310.2972)；发表状态：arXiv 预印本；核验：Wood 的 Theorem 3 对任意 r≥2、d≥1 构造三角形自由、d-degenerate 的 r-一致超图，染色数 d+1；取 d=2 得局部边数<2|X| 却非二着色，故任何趋于无穷的 c_t 都失败。
  - `public_lean` [plby/lean-proofs Erdős1022](https://github.com/plby/lean-proofs/blob/main/ErdosProblems/Erdos1022.md)；发表状态：公开 Lean 文档与源码；核验：主声明名为 not_erdos_1022，明确证明原存在命题的否定；源码无 sorry、无新增 axiom。
  - `other` [Erdős Problem #1022](https://www.erdosproblems.com/1022)；发表状态：官方题页；核验：题页状态文字为 PROVED (LEAN)，但备注与链接实际都给出反例，方向应是 DISPROVED (LEAN)。

#### #1044

- 官方状态：`solved (Lean)`
- 精确题面：Let $f(z)=\prod_{i=1}^n(z-z_i)\in\mathbb{C}[x]$ where $\lvert z_i\rvert\leq 1$ for all $i$. If $\Lambda(f)$ is the maximum of the lengths of the boundaries of the connected components of\[\{ z: \lvert f(z)\rvert<1\}\]then determine the infimum of $\Lambda(f)$.
- 范围解释：对所有零点位于单位圆盘的首一多项式，求其单位次水平集各连通分支边界长度最大值 Λ(f) 的全局下确界。
- 闭合判定：`closed_verified`
- 判定理由：公开数学证明和完整 Lean 主声明均给出同一精确数值 2，范围匹配。
- Lean 审计：公开 gist 无 sorry/axiom，主等式就是题面目标；应与 formal-conjectures 的带 sorry 占位文件区分。
- 尚存不确定性：建议把 gist 迁入固定版本仓库；当前无实质逻辑缺口。
- 证据：

  - `other` [On Erdős Problem 1044](https://github.com/QuanyuTang/erdos-problem-1044/blob/main/On_Erd%C5%91s_Problem_1044.pdf)；发表状态：公开研究稿；核验：论文证明下确界为 2，并给出达到/逼近机制；量化覆盖任意次数 n 与所有 |z_i|≤1。
  - `public_lean` [Erdős 1044 Lean proof gist](https://gist.github.com/LorenzoLuccioli/c3ace69881872112109a6c31b7a87cfc)；发表状态：公开 Lean 源码；核验：主声明 erdos_problem_1044 : lambdaInf=2；无 sorry 或新增 axiom，抽象定义与论文中的下确界对象相接。

#### #1051

- 官方状态：`proved (Lean)`
- 精确题面：Is it true that if $a_1<a_2<\cdots$ is a sequence of integers with\[\liminf a_n^{1/2^n}>1\]then\[\sum_{n=1}^\infty \frac{1}{a_na_{n+1}}\]is irrational?
- 范围解释：冻结题面允许严格递增整数列；增长条件迫使其最终为正，并要求 Σ1/(a_n a_{n+1}) 非有理。
- 闭合判定：`closed_scope_caveat`
- 判定理由：论文足以处理通常所指的正整数版本，一般整数版本也可用最终正性和有限有理前缀作短归约；但官方“Lean”严格说只形式化了正自然数范围。
- Lean 审计：公开共享代码本身无 sorry/axiom，但正式主声明只覆盖正自然数序列；frozen 的一般整数序列需先删去有限个非正项，再说明删去部分只改变有理数。该有限前缀归约未在主声明中形式化。formal-conjectures 基准仍含 sorry。
- 尚存不确定性：应在 Lean 中补一个从 ℤ 序列到尾部 ℕ 序列的包装定理，并把浏览器临时链接归档到稳定仓库。
- 证据：

  - `preprint` [Irrationality from doubly exponential growth](https://arxiv.org/abs/2601.21442)；发表状态：arXiv 预印本（2026 年修订版）；核验：论文对正整数严格递增序列证明更强的黄金比例型条件，题面 liminf a_n^(1/2^n)>1 是其推论。
  - `public_lean` [Erdős 1051 public Lean code discussion](https://www.erdosproblems.com/forum/discuss/1051)；发表状态：公开浏览器共享 Lean 源码；核验：解码公开代码后，主声明 erdos_1051_irrational 取 a:ℕ→ℕ、StrictMono、正性及题面 liminf 条件；未见 sorry 或新增 axiom。

#### #1071

- 官方状态：`proved (Lean)`
- 精确题面：Are there a finite set of unit line segments in the unit square, no two of which intersect, which are maximal with respect to this property? Is there a region $R$ with a maximal set of disjoint unit line segments that is countably infinite?
- 范围解释：第一问要求单位正方形内存在有限、两两不交且极大的单位线段族；第二问要求某区域存在可数无限的极大不交单位线段族。
- 闭合判定：`closed_verified`
- 判定理由：两条存在性问句均有独立的公开 Lean 主声明，区域、有限/可数、极大性量词均匹配。
- Lean 审计：两个文件分别覆盖两问，均无 sorry/axiom，#print axioms 只有标准基础；不是仅有题面编码。
- 尚存不确定性：无实质不确定性。
- 证据：

  - `public_lean` [plby/lean-proofs Erdős1071](https://github.com/plby/lean-proofs/blob/main/ErdosProblems/Erdos1071.md)；发表状态：公开 Lean 文档与源码；核验：Erdos1071.lean 的 Theorem_1/Corollary_2/Corollary_3 构造区域中的可数无限极大家族；无 sorry/axiom。
  - `public_lean` [plby/lean-proofs Erdős1071b](https://raw.githubusercontent.com/plby/lean-proofs/main/src/v4.24.0/ErdosProblems/Erdos1071b.lean)；发表状态：公开 Lean 源码；核验：主声明 erdos_1071b 给出单位正方形中的有限极大族；无 sorry/新增 axiom，并明确线段长度与不交/极大条件。

#### #1089

- 官方状态：`solved`
- 精确题面：Let $g_d(n)$ be minimal such that every collection of $g_d(n)$ points in $\mathbb{R}^d$ determines at least $n$ many distinct distances. Estimate $g_d(n)$. In particular, does\[\lim_{d\to \infty}\frac{g_d(n)}{d^{n-1}}\]exist?
- 范围解释：固定距离数参数 n，估计迫使至少 n 种距离所需点数 g_d(n)，并求 d→∞ 时 g_d(n)/d^(n−1) 的极限。
- 闭合判定：`closed_verified`
- 判定理由：记 M_d(n−1) 为 d 维至多 n−1 种距离集合的最大大小，则 g_d(n)=M_d(n−1)+1，且 binom(d+1,n−1)+1≤g_d(n)≤binom(d+n−1,n−1)+1。固定 n≥2 时两界给出极限 1/(n−1)!；n=1 时 g_d(1)=2。
- Lean 审计：未发现公开 Lean 完成稿。
- 尚存不确定性：下界构造目前是预印本；但量词与上界配合无范围错位。
- 证据：

  - `peer_reviewed_paper` [An upper bound for the cardinality of an s-distance subset in real Euclidean space, II](https://doi.org/10.1007/BF02579288)；发表状态：Combinatorica 3 (1983) 已发表论文；核验：Bannai–Bannai–Stanton 给出至多 n−1 种距离集合的大小上界 binom(d+n−1,n−1)，故得到 g_d(n) 的对应上界。
  - `preprint` [Semi-Autonomous Mathematics Discovery with Gemini](https://arxiv.org/abs/2601.22401)；发表状态：arXiv 预印本；核验：第 4.4 节构造 binom(d+1,n−1) 点、仅 n−1 种距离的集合，给出匹配首项下界；两界夹出 n≥2 时极限 1/(n−1)!。n=1 为直接平凡情形。

#### #1091

- 官方状态：`solved`
- 精确题面：Let $G$ be a $K_4$-free graph with chromatic number $4$. Must $G$ contain an odd cycle with at least two diagonals? More generally, is there some $f(r)\to \infty$ such that every graph with chromatic number $4$, in which every subgraph on $\leq r$ vertices has chromatic number $\leq 3$, contains an odd cycle with at least $f(r)$ diagonals?
- 范围解释：第一问针对所有 K₄-free、4-染色图寻找含至少两条对角线的奇圈；第二问在局部 r 点子图均 3-可染时，猜测可迫使对角线数 f(r)→∞。
- 闭合判定：`closed_verified`
- 判定理由：第一问有经典同行评审肯定证明，第二问有精确参数反例；两部分方向不同但共同构成 SOLVED。
- Lean 审计：无公开 Lean 完成稿。
- 尚存不确定性：第二问反例尚待同行评审。
- 证据：

  - `peer_reviewed_paper` [Graphs having circuits with at least two chords](https://doi.org/10.1016/0095-8956(82)90004-1)；发表状态：Journal of Combinatorial Theory, Series B 32 (1982) 已发表论文；核验：Voss 证明第一问为肯定，假设正是 K₄-free 与染色数至少 4。
  - `preprint` [APSSV26b, Section 4.1](https://arxiv.org/abs/2604.06609)；发表状态：arXiv 预印本；核验：Theorem 4.1 构造局部 3-可染的 K₄-free 4-critical 图，而每个圈至多 10 条对角线；随局部尺度增长仍有统一上界，否定 f(r)→∞。

#### #1092

- 官方状态：`disproved`
- 精确题面：Let $f_r(n)$ be maximal such that, if a graph $G$ has the property that every subgraph $H$ on $m$ vertices is the union of a graph with chromatic number $r$ and a graph with $\leq f_r(m)$ edges, then $G$ has chromatic number $\leq r+1$. Is it true that $f_2(n) \gg n$? More generally, is $f_r(n)\gg_r n$?
- 范围解释：猜测局部只需删线性数目的边即可成为 r-可染，就足以迫使全图 (r+1)-可染；首问为 r=2。
- 闭合判定：`closed_verified`
- 判定理由：同行评审构造甚至以 o(m) 误差满足局部近二分性，却有高全局染色数，严格击穿首问和“对所有 r”的一般命题。
- Lean 审计：formal-conjectures 文件含 sorry；无公开完成 Lean 证明。
- 尚存不确定性：各固定 r 的最优 f_r 仍可研究，但不影响所列猜想已证否。
- 证据：

  - `peer_reviewed_paper` [Nearly bipartite graphs with large chromatic number](https://doi.org/10.1007/BF02579434)；发表状态：Combinatorica 2 (1982) 已发表论文；核验：Rödl 构造染色数任意大的图，而其每个 m 点子图删去 o(m) 条边即可二分；因此任何 f₂(m)≫m 的充分条件都会错误，r=2 已否定一般猜想。

#### #1096

- 官方状态：`proved`
- 精确题面：Let $1<q<1+\epsilon$ and consider the set of numbers of the shape $\sum_{i\in S}q^i$ (for all finite $S$), ordered by size as $0=x_1<x_2<\cdots$. Is it true that, provided $\epsilon>0$ is sufficiently small, $x_{k+1}-x_k \to 0$?
- 范围解释：对 q 足够接近 1，把所有有限 0/1 q-幂和排序后，证明相邻间距趋于 0。
- 闭合判定：`closed_verified`
- 判定理由：已发表论文给出一个统一开放区间内的完整极限，而不是仅 liminf=0，正好提供题面所需的“充分小 ε”。
- Lean 审计：formal-conjectures 对应文件含 sorry；没有外部完成 Lean 证明。
- 尚存不确定性：最优阈值仍未由本题要求；不构成闭合缺口。
- 证据：

  - `peer_reviewed_paper` [Developments in non-integer bases](https://doi.org/10.1023/A:1006557705401)；发表状态：Acta Mathematica Hungarica 79 (1998) 已发表论文；核验：Erdős–Komornik 证明当 1<q<√q₁≈1.175 时完整极限 x_{n+1}−x_n→0；取 ε=√q₁−1 即逐字肯定题面。

#### #1105

- 官方状态：`proved`
- 精确题面：The anti-Ramsey number $\mathrm{AR}(n,G)$ is the maximum possible number of colours in which the edges of $K_n$ can be coloured without creating a rainbow copy of $G$ (i.e. one in which all edges have different colours). Let $C_k$ be the cycle on $k$ vertices. Is it true that\[\mathrm{AR}(n,C_k)=\left(\frac{k-2}{2}+\frac{1}{k-1}\right)n+O(1)?\]Let $P_k$ be the path on $k$ vertices and $\ell=\lfloor\frac{k-1}{2}\rfloor$. If $n\geq k\geq 5$ then is $\mathrm{AR}(n,P_k)$ equal to\[\max\left(\binom{k-2}{2}+1, \binom{\ell-1}{2}+(\ell-1)(n-\ell+1)+\epsilon\right)\]where $\epsilon=1$ if $k$ is odd and $\epsilon=2$ otherwise?
- 范围解释：包含两问：固定环 C_k 的反 Ramsey 数线性渐近公式，以及所有 n≥k≥5 时路径 P_k 的精确最大值公式。
- 闭合判定：`closed_scope_caveat`
- 判定理由：环部分已有同行评审精确定理；路径部分的公开预印本量词和公式均匹配，但官网仍称 announced，未核到正式期刊版本。
- Lean 审计：formal-conjectures 对应文件含 sorry；无公开完成 Lean 证明。
- 尚存不确定性：需要确认 Yuan 稿是否已正式发表或经过独立审稿；在此之前应标“论文+预印本”，而非笼统“已发表”。
- 证据：

  - `peer_reviewed_paper` [An Anti-Ramsey Theorem on Cycles](https://doi.org/10.1007/s00373-005-0619-y)；发表状态：Graphs and Combinatorics 21 (2005) 已发表论文；核验：Montellano-Ballesteros–Neumann-Lara 确定所有 n≥k 的环反 Ramsey 数；展开其精确式即得 frozen 的线性系数与 O(1)。
  - `preprint` [Anti-Ramsey numbers for paths](https://arxiv.org/abs/2102.00807)；发表状态：arXiv 预印本/宣布证明；核验：Yuan 的主定理对所有 n≥k≥5 给出题面同一 max 公式及奇偶 ε；不是只覆盖 n≫k² 的旧结果。

#### #1119

- 官方状态：`independent`
- 精确题面：Let $\aleph_0<\mathfrak m<\mathfrak c$. If a family of entire functions takes at most $\mathfrak m$ distinct values at every fixed $z_0$, must the family have cardinality at most $\mathfrak m$?
- 范围解释：在 ℵ₀<m<c 下，问逐点值集大小≤m 的整函数族是否必有总基数≤m；关键未定情形是 m^+=c。
- 闭合判定：`closed_verified`
- 判定理由：两篇同行评审工作在相同临界基数配置下分别给出肯定和否定模型，足以证明题目在 ZFC 中独立；当 m^+<c 时的 ZFC 肯定结论也与此兼容。
- Lean 审计：现行官网标 Formalised statement? No；即使冻结元数据曾标 yes，也没有公开完成 Lean 证明。formal-conjectures 的任何 sorry 占位不能形式化相对一致性证明。
- 尚存不确定性：“闭合”含义是独立性分类，而不是在 ZFC 内选择 yes/no；官方状态 INDEPENDENT 正确。
- 证据：

  - `peer_reviewed_paper` [On a question about families of entire functions](https://shelah.logic.at/papers/1078/)；发表状态：Fundamenta Mathematicae 239 (2017) 已发表论文；核验：Kumar–Shelah 构造 c=ℵ₂、m=ℵ₁ 的模型，在其中答案为肯定；题面逐点评价纤维条件保持不变。
  - `peer_reviewed_paper` [Wetzel families and the continuum](https://doi.org/10.1112/jlms.12918)；发表状态：Journal of the London Mathematical Society 2024 已发表论文（附 arXiv 版本）；核验：Schilhan–Weinert 构造同样 c=ℵ₂、m=ℵ₁ 而答案为否的模型；与前一模型合成 ZFC 独立性。

## 第二部分：24 道官方仍开放但初筛冲突的核验

### 判定分布

| 判定 | 数量 |
|---|---:|
| literal_false_intended_open | 12 |
| still_open_correct | 6 |
| initial_analysis_wrong | 2 |
| recent_claim_unverified | 2 |
| independence_scope_mismatch | 1 |
| likely_status_stale | 1 |

判定口径：`literal_false_intended_open` 表示冻结字面版已假、但维护者意图中的修正版仍开放；`still_open_correct` 表示初筛没有发现足以更新状态的新证据；`initial_analysis_wrong` 表示上轮分析本身有误；`recent_claim_unverified` 表示只有近期预印本或计算声称，尚不足以确认官方闭合；`likely_status_stale` 表示已有较强的新闭合证据、官网很可能尚未同步；`independence_scope_mismatch` 表示独立性/形式系统结论与原数学题范围不一致。

### 总表

| # | 审计判定 | 为何仍开放/是否应更新 |
|---:|---|---|
| 129 | literal_false_intended_open | 官网已知字面反例，却尚未恢复出一致认可的原始意图；OPEN 表示条目仍待澄清。 |
| 180 | literal_false_intended_open | 条目以 OPEN 追踪修正版，而正文已诚实记录原文反例。 |
| 335 | initial_analysis_wrong | 现有最新工作仍明确是有附加假设的部分分类。 |
| 520 | initial_analysis_wrong | 当前最强可核实上界仍留有足够大的 log log 因子，LIL 常数问题未解决。 |
| 545 | literal_false_intended_open | 官方用 OPEN 追踪大 m 残余问题，并已在正文列出有限反例。 |
| 550 | recent_claim_unverified | 官方显然在等待新预印本经过核验后再关闭条目。 |
| 563 | literal_false_intended_open | 官网的修正版本仍只有数量级估计，精确渐近未闭合。 |
| 575 | literal_false_intended_open | OPEN 对应拟议修正版，官网讨论已接受原文字反例。 |
| 612 | still_open_correct | 奇数团部分 r≥2 仍没有证明或反例，修正后的偶数团界也仍待解决。 |
| 638 | literal_false_intended_open | 题面缺条件，官网保留 OPEN 以追踪修正版；强化反例也尚有实质缺口。 |
| 654 | still_open_correct | 复合条目仍有两个实质未决方向。 |
| 655 | literal_false_intended_open | 官网以 OPEN 追踪被认为是原意的一般位置问题。 |
| 701 | literal_false_intended_open | 官方问题是有限版本，公开 Lean 反例只揭示了仓库形式化缺条件。 |
| 786 | literal_false_intended_open | 官网 OPEN 对应互异元素修正版。 |
| 796 | literal_false_intended_open | 官网追踪的是勘误后的问题。 |
| 836 | still_open_correct | 线性交叠下界仍比最佳已知结果多一个 log r 因子。 |
| 890 | literal_false_intended_open | 官网已修题，仍没有正确版本的证明。 |
| 917 | still_open_correct | k=6 与一整类 k 的渐近问题仍开放。 |
| 918 | independence_scope_mismatch | 第二问缺少相应的负一致性结果，且独立性本身须相对于明确公理体系表述。 |
| 920 | likely_status_stale | 页面更新早于最新论文版本，尚未执行状态联动。 |
| 935 | still_open_correct | 复合题只部分闭合，尤其无条件第三问仍开放。 |
| 985 | literal_false_intended_open | 数学上有意义的奇素数版本仍远超已知 Artin 型结果。 |
| 1070 | recent_claim_unverified | 一方面官方可能等待新预印本核验，另一方面题目首句的总体渐近估计本来仍开放。 |
| 1112 | still_open_correct | 复合参数问题仍有大量未决情形。 |

### 逐题冲突记录

#### #129

- 官方题面：Let $R(n;k,r)$ be the smallest $N$ such that if the edges of $K_N$ are $r$-coloured then there is a set of $n$ vertices which does not contain a copy of $K_k$ in at least one of the $r$ colours. Prove that there is a constant $C=C(r)>1$ such that\[R(n;3,r) < C^{\sqrt{n}}.\]
- 上轮初筛：`counterexample`；虽然页面标签仍为 open，官方说明已明确指出原命题按现有文字为假。候选答案的概率反例路线经常数检查后成立。
- 字面命题：对固定 r≥2，题面断言 R(n;3,r)<C(r)^{√n}；这里每个 r-边染色都应有一个 n 点集，使至少一种颜色在该点集内没有三角形。
- 当前预期开放范围：现行文字已被概率反例否定；原始文献究竟遗漏了何种条件尚不清楚，因此官网保留 OPEN 更像是等待澄清或修订，而不是仍相信字面上界。
- 上轮声称：初轮给出随机 r-染色反例，判为 counterexample，并称可得到 R(n;3,r)≥exp(Ω_r(n))。
- 审计判定：`literal_false_intended_open`
- 闭合评估：初轮对字面命题的反驳成立，但这只闭合了错误或不完整的文字版本，不能被描述为解决了某个已明确写出的修正版。
- 官方仍开放原因：官网已知字面反例，却尚未恢复出一致认可的原始意图；OPEN 表示条目仍待澄清。
- 下一核验动作：逐页查 Er97b 原文及其前后定义，确定 R(n;3,r) 的预期量词或符号是否被转录错误。
- 证据：

  - `official_record` [Erdős Problem #129](https://www.erdosproblems.com/129)；发表状态：官方持续更新题页；核验：题页仍标 OPEN，但正文明确说明按当前定义该猜想为假，并记录同一类概率反例。
  - `independent_argument` [随机边染色并合界复核](https://www.erdosproblems.com/129)；发表状态：本次独立数学核算；核验：K_n 中可贪心取 Ω(n²) 个边互不相交三角形。固定 n 点集与颜色，其无该色三角形概率至多 exp(-Ω_r(n²))；对 N=exp(c_r n) 的所有点集和颜色并合仍小于 1，故字面上界不可能成立。

#### #180

- 官方题面：If $\mathcal{F}$ is a finite set of finite graphs then $\mathrm{ex}(n;\mathcal{F})$ is the maximum number of edges a graph on $n$ vertices can have without containing any subgraphs from $\mathcal{F}$. Note that it is trivial that $\mathrm{ex}(n;\mathcal{F})\leq \mathrm{ex}(n;G)$ for every $G\in\mathcal{F}$. Is it true that, for every $\mathcal{F}$, there exists $G\in\mathcal{F}$ such that\[\mathrm{ex}(n;G)\ll_{\mathcal{F}}\mathrm{ex}(n;\mathcal{F})?\]
- 上轮初筛：`counterexample`；按输入仍标 open，但精确的全称命题已有官方页注明的 folklore counterexample。吸收人工评审意见：下面只是重建并核对该已知反例，不能宣称为新的问题解决；可能仍开放的是排除此星—匹配障碍后的修正版。
- 字面命题：对每个有限图族 F，是否总能选 G∈F，使 ex(n;G)≤C_F ex(n;F) 对所有充分大 n 成立。
- 当前预期开放范围：不加限制的版本被星图与匹配组成的有限族否定；排除森林障碍，例如要求 F 不含森林的修正版仍可视为开放。
- 上轮声称：初轮重建星图—匹配反例，判为 counterexample。
- 审计判定：`literal_false_intended_open`
- 闭合评估：字面全称命题确已严格证否；但通常所称的剩余 Erdős 问题是加入“F 不含森林”等条件后的修正版，尚未闭合。
- 官方仍开放原因：条目以 OPEN 追踪修正版，而正文已诚实记录原文反例。
- 下一核验动作：从原始出处确认 Erdős 是否已隐含排除了森林，并为修正版建立精确、无歧义的题面。
- 证据：

  - `official_record` [Erdős Problem #180](https://www.erdosproblems.com/180)；发表状态：官方持续更新题页；核验：官网明确把星图与匹配的构造列为 folklore counterexample，同时指出排除这一障碍后的问题仍有意义。
  - `public_note` [Yuval Wigderson, Compactness note](https://ywigderson.math.ethz.ch/math/static/Compactness.pdf)；发表状态：公开数学笔记；核验：笔记给出 F={K_{1,2},2K_2}：ex(n;F)=1，而每个单独成员的极值数均为 Θ(n)，直接否定全称命题。

#### #335

- 官方题面：Let $d(A)$ denote the density of $A\subseteq \mathbb{N}$. Characterise those $A,B\subseteq \mathbb{N}$ with positive density such that\[d(A+B)=d(A)+d(B).\]
- 上轮初筛：`counterexample`；仍开放，且 2026 年已有附加“某集合遇到每个剩余类”假设下的部分结果。人工评审指出旧候选错误地宣称密度等式强迫一维紧阿贝尔因子与区间结构；该结论不成立，以下用概率构造直接解释其失败。
- 字面命题：刻画所有具有正自然密度且 d(A+B)=d(A)+d(B) 的 A,B⊆N。
- 当前预期开放范围：无附加条件的完整刻画仍开放；2026 年结果只在额外的剩余类非退化条件下给出部分答案。
- 上轮声称：初轮把随机偶数子集对刚性分类的反例标成 counterexample，容易被误读为已经反驳或闭合整个“刻画所有”问题。
- 审计判定：`initial_analysis_wrong`
- 闭合评估：随机偶数子集只否定某个过强的候选分类，不是对“刻画所有等号情形”的反例。初轮闭合倾向错误，官方 OPEN 正确。
- 官方仍开放原因：现有最新工作仍明确是有附加假设的部分分类。
- 下一核验动作：抽取 2604.12864 的精确假设与结论，整理其未覆盖的密度等号例子，作为下一步分类路线的边界。
- 证据：

  - `official_record` [Erdős Problem #335](https://www.erdosproblems.com/335)；发表状态：官方持续更新题页；核验：题页仍标 OPEN，并明确区分随机例子对某些过强结构猜想的反驳与完整分类问题本身。
  - `preprint` [Ackelsberg–Richter, On equality in a sumset density problem](https://arxiv.org/abs/2604.12864)；发表状态：2026 年 arXiv v1，117 页，未据此认定同行评审完成；核验：摘要和主结果自称 partial answer，并加入至少一个集合遇到每个剩余类一类的非退化假设；没有覆盖原题全部 A,B。

#### #520

- 官方题面：Let $f$ be a Rademacher multiplicative function: a random $\{-1,0,1\}$-valued multiplicative function, where for each prime $p$ we independently choose $f(p)\in \{-1,1\}$ uniformly at random, and for square-free integers $n$ we extend $f(p_1\cdots p_r)=f(p_1)\cdots f(p_r)$ (and $f(n)=0$ if $n$ is not squarefree). Does there exist some constant $c>0$ such that, almost surely,\[\limsup_{N\to \infty}\frac{\sum_{m\leq N}f(m)}{\sqrt{N\log\log N}}=c?\]
- 上轮初筛：`known_resolution`；冻结日期 2025-08-31 时仍开放；但 Caich 预印本的 2026-03-22 修订版 Theorem 1.1 宣称几乎处处上界 √x(log log x)^{1/4+ε}。若该修订定理成立，它已经否定题目：limsup 必为 0，而非正数。由于这是冻结后预印本更新，结论应标作“由当前预印本给出的已知否定”，并等待同行评审/官网状态同步。
- 字面命题：随机平方自由乘法函数的部分和 S_N 是否几乎处处满足 limsup S_N/√(N log log N)=c，其中 c>0 为确定常数。
- 当前预期开放范围：确定正的 LIL 型 limsup 常数仍开放；已知上下界的 log log 指数尚不足以迫使该归一化 limsup 为 0。
- 上轮声称：初轮声称 Caich 预印本有 2026 修订版，把上界改进到 √x(log log x)^{1/4+ε}，据此判定 limsup=0 并标 known_resolution。
- 审计判定：`initial_analysis_wrong`
- 闭合评估：初轮结论建立在不存在的 2026 修订版上，必须撤销；没有证据表明该题已经证真或证否。
- 官方仍开放原因：当前最强可核实上界仍留有足够大的 log log 因子，LIL 常数问题未解决。
- 下一核验动作：持续跟踪 arXiv 版本记录；证明工作应围绕缩小 1/4 型下界与 3/4 型上界间的间隙，而不是使用已撤回的 v1 指数。
- 证据：

  - `preprint_version` [Caich, Almost sure upper bound, arXiv:2304.00943v1](https://arxiv.org/abs/2304.00943v1)；发表状态：2023 年 arXiv v1，已被后续版本替代；核验：v1 的确曾写出 1/4+ε 指数；它不是当前版本，不能跳过修订继续作为已确立结论使用。
  - `preprint_version` [Caich, Almost sure upper bound, arXiv:2304.00943v2](https://arxiv.org/abs/2304.00943v2)；发表状态：当前最新版 v2，2024-08-19；核验：arXiv API 与正文均显示当前只有 v2；主上界为 √x(log log x)^{3/4+ε}，而非初轮虚构的 2026 年 1/4+ε 修订。它不能推出题中归一化 limsup 为 0。
  - `official_record` [Erdős Problem #520](https://www.erdosproblems.com/520)；发表状态：官方持续更新题页；核验：页面仍标 OPEN，与当前可核实的 v2 上界相符。
  - `formalization` [Formal Conjectures: Erdős 520](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/520.lean)；发表状态：公开 Lean 陈述文件；核验：文件只是题目编码，关键定理仍含 sorry，不能作为证明证据。

#### #545

- 官方题面：Let $G$ be a graph with $m$ edges and no isolated vertices. Is the Ramsey number $R(G)$ maximised when $G$ is 'as complete as possible'? That is, if $m=\binom{n}{2}+t$ edges with $0\leq t<n$ then is\[R(G)\leq R(H),\]where $H$ is the graph formed by connecting a new vertex to $t$ of the vertices of $K_n$?
- 上轮初筛：`counterexample`；字面命题已有小 m 反例；网站保留 OPEN，是因为通常关注排除这些有限例外后的大 m/渐近版本。先前候选给出的 m=3 匹配反例可以严格核对，但它没有解决“充分大 m 是否成立”的残余问题。
- 字面命题：给定 m=binom(n,2)+t，H 为 K_n 加一个与其中 t 点相连的新点；问每个恰有 m 条边且无孤立点的图 G 是否都满足 R(G)≤R(H)。
- 当前预期开放范围：全称的所有 m 版本已有多个小 m 反例；真正剩余的是充分大 m 或渐近极值版本。
- 上轮声称：初轮用 m=3、G=3K_2、H=K_3 给出 8>6 的反例，判为 counterexample。
- 审计判定：`literal_false_intended_open`
- 闭合评估：反例正确且闭合了未排除小 m 的文字版本，但没有推进充分大 m 的核心猜想。
- 官方仍开放原因：官方用 OPEN 追踪大 m 残余问题，并已在正文列出有限反例。
- 下一核验动作：把题面正式改写为“是否存在 m_0，使所有 m≥m_0 成立”，再研究潜在极值图的稳定性。
- 证据：

  - `official_record` [Erdős Problem #545](https://www.erdosproblems.com/545)；发表状态：官方持续更新题页；核验：官网明确记录 m=2,…,5 及 m=7,…,9 的失败例，仍把大 m 版本列为开放。
  - `exact_small_case` [m=3 精确 Ramsey 数核对](https://www.erdosproblems.com/545)；发表状态：本次独立数学核算；核验：m=3 时 H=K_3，R(H)=6；经典匹配公式给 R(3K_2,3K_2)=8，故字面全称命题确实失败。

#### #550

- 官方题面：Let $m_1\leq\cdots\leq m_k$ and $n$ be sufficiently large. If $T$ is a tree on $n$ vertices and $G$ is the complete multipartite graph with vertex class sizes $m_1,\ldots,m_k$ then prove that\[R(T,G)\leq (\chi(G)-1)(R(T,K_{m_1,m_2})-1)+m_1.\]
- 上轮初筛：`known_resolution`；冻结输入标为 open，但 2026-06-24 的新预印本声称精确证明该结论。先前候选的“直接套 CRST 得到所有大树的 Burr 等式”是错误的，人工评审意见必须保留：该等式不对任意树成立，故其三步论证无效。
- 字面命题：固定 k 与 m_1≤…≤m_k，问所有充分大的 n 顶点树 T 是否满足 R(T,K_{m_1,…,m_k})≤(k-1)(R(T,K_{m_1,m_2})-1)+m_1。
- 当前预期开放范围：2026 年 6 月的新预印本声称精确证明原命题；目前等待独立复核、同行评审及官网状态同步。
- 上轮声称：初轮判 known_resolution，并正确改用 Eric Li 新预印本；同时撤销了旧候选直接误用 CRST/Burr 等式的论证。
- 审计判定：`recent_claim_unverified`
- 闭合评估：预印本的定理陈述确实覆盖全题，闭合声称不是量词误配；但它仍是很新的 v1，本次仅核对陈述与证明架构，不能替代完整同行审查。
- 官方仍开放原因：官方显然在等待新预印本经过核验后再关闭条目。
- 下一核验动作：由独立图论专家逐引理复核 off-Turán 嵌入和紧致化步骤，并跟踪后续 arXiv 修订或期刊接收。
- 证据：

  - `preprint` [Eric Li, A Resolution of Erdős Problem 550](https://arxiv.org/abs/2606.23659)；发表状态：2026-06 arXiv v1，尚无同行评审完成证据；核验：逐页检查 Theorem 1.1：固定 k,m_i、存在 n_0、对每个 n≥n_0 及每棵 n 点树的量词与目标不等式均和题面一致。证明采用新的 off-Turán 嵌入与紧致/舍入论证，不是错误的 CRST 一步套用。
  - `official_record` [Erdős Problem #550](https://www.erdosproblems.com/550)；发表状态：官方题页仍标 OPEN；核验：页面已出现 claimed solution posted 的提示，但尚未把状态改成 PROVED。

#### #563

- 官方题面：Let $F(n,\alpha)$ denote the largest $m$ such that there exists a $2$-colouring of the edges of $K_n$ so that every $X\subseteq [n]$ with $\lvert X\rvert\geq m$ contains more than $\alpha \binom{\lvert X\rvert}{2}$ many edges of each colour. Prove that, for every $0\leq \alpha\leq 1/2$,\[F(n,\alpha)\sim c_\alpha\log n\]for some constant $c_\alpha$ depending only on $\alpha$.
- 上轮初筛：`counterexample`；输入版本不是开放问题的正确陈述。先前候选准确指出了“最大/最小”错误，但还应明确吸收第二个错误：$\alpha=1/2$ 必须排除。
- 字面命题：冻结题面把 F(n,α) 写成满足性质的“最大”阈值，并把 α=1/2 包含在内。
- 当前预期开放范围：官网正确版本是“最小”阈值且 0≤α<1/2；该正确版本的精确渐近仍开放。
- 上轮声称：初轮指出最大/最小与端点转录错误，判为 counterexample。
- 审计判定：`literal_false_intended_open`
- 闭合评估：初轮正确诊断了转录错误，但这不构成对现行最小阈值问题的证明或证否。
- 官方仍开放原因：官网的修正版本仍只有数量级估计，精确渐近未闭合。
- 下一核验动作：后续所有分析只引用现行 smallest、α<1/2 版本，并修复本仓库冻结题面。
- 证据：

  - `official_record` [Erdős Problem #563](https://www.erdosproblems.com/563)；发表状态：官方持续更新题页；核验：现行题面明确使用 smallest，并限制 α<1/2；只给出 F(n,α)数量级为 log n，未给出精确答案。
  - `statement_comparison` [冻结语料与现行题面对照](https://www.erdosproblems.com/563)；发表状态：本次逐字核对；核验：两处差异都会实质改变命题；“最大阈值”版本不是官网当前追踪的开放问题。

#### #575

- 官方题面：If $\mathcal{F}$ is a finite set of finite graphs then $\mathrm{ex}(n;\mathcal{F})$ is the maximum number of edges a graph on $n$ vertices can have without containing any subgraphs from $\mathcal{F}$. Note that it is trivial that $\mathrm{ex}(n;\mathcal{F})\leq \mathrm{ex}(n;G)$ for every $G\in\mathcal{F}$. Is it true that, for every $\mathcal{F}$, if there is a bipartite graph in $\mathcal{F}$ then there exists some bipartite $G\in\mathcal{F}$ such that\[\mathrm{ex}(n;G)\ll_{\mathcal{F}}\mathrm{ex}(n;\mathcal{F})?\]
- 上轮初筛：`counterexample`；输入仍标 open，但精确陈述按字面已被一个森林反例否定；网站讨论也确认“as written”存在该反例。可能真正拟议的开放版本额外假设 F 不含森林。
- 字面命题：有限图族 F 只要含一个二部图，是否总能在 F 中选二部 G，使 ex(n;G)≤C_F ex(n;F)。
- 当前预期开放范围：字面版本被包含森林的族否定；建议的开放修正版要求 F 不含森林。
- 上轮声称：初轮用 F={K_{1,2},2K_2} 判为 counterexample。
- 审计判定：`literal_false_intended_open`
- 闭合评估：字面命题已完全证否；没有证据闭合排除森林后的版本。
- 官方仍开放原因：OPEN 对应拟议修正版，官网讨论已接受原文字反例。
- 下一核验动作：固定无森林修正版并检查它与 #180 的关系，避免把同一退化反例重复计作新进展。
- 证据：

  - `official_discussion` [Erdős Problem #575 discussion](https://www.erdosproblems.com/forum/thread/575)；发表状态：官方论坛记录；核验：讨论明确说 as written 有 Wigderson 的反例，并建议加入“F 不含森林”。
  - `public_note` [Yuval Wigderson, Compactness note](https://ywigderson.math.ethz.ch/math/static/Compactness.pdf)；发表状态：公开数学笔记；核验：对 F={K_{1,2},2K_2}，联合禁图使图至多一条边，所以 ex(n;F)=1；单独禁任一成员仍允许 Θ(n) 条边，所求常数比较失败。

#### #612

- 官方题面：Let $G$ be a connected graph with $n$ vertices, minimum degree $d$, and diameter $D$. Show if that $G$ contains no $K_{2r}$ and $(r-1)(3r+2)\mid d$ then\[D\leq \frac{2(r-1)(3r+2)}{2r^2-1}\frac{n}{d}+O(1),\]and if $G$ contains no $K_{2r+1}$ and $3r-1 \mid d$ then\[D\leq \frac{3r-1}{r}\frac{n}{d}+O(1).\]
- 上轮初筛：`counterexample`；整体不能按待证明命题处理：第一部分对每个 r≥2 已被反例否定；第二部分 r=1 已知成立，r≥2 在仅禁 K_{2r+1} 的条件下仍开放。因此网页的 open 标签只能理解为尚存的第二部分，而非两式都可能成立。
- 字面命题：题目由偶数团禁图与奇数团禁图两部分组成，分别猜测连通 K_{2r}-free 或 K_{2r+1}-free 图的直径具有给定 O(n/d) 最优常数。
- 当前预期开放范围：偶数团部分对 r≥2 已被反例否定；奇数团部分仅 r=1 已知，r≥2 仍开放，且另有修正后的偶数团猜想。
- 上轮声称：初轮判 counterexample，核对了已发表反例系数，并指出第二部分仍开放。
- 审计判定：`still_open_correct`
- 闭合评估：这是复合题：已有正式发表的证否只闭合第一部分，不能据此把整题关掉；官网继续标 OPEN 是正确的。
- 官方仍开放原因：奇数团部分 r≥2 仍没有证明或反例，修正后的偶数团界也仍待解决。
- 下一核验动作：证明工作应明确选定奇数团部分或修正版偶数团部分，不再尝试已被 CSS21 否定的原系数。
- 证据：

  - `published_paper` [Czabarka–Singgih–Székely, Counterexamples for a diameter conjecture](https://doi.org/10.1016/j.jctb.2021.06.001)；发表状态：Journal of Combinatorial Theory, Series B 151 (2021)，已发表；核验：论文给出偶数团部分的反例族；其直径主项系数为 (6r-5)/((2r-1)d+2r-3)，在允许的大 d 下严格超过原猜测系数。
  - `author_pdf` [Published counterexample paper PDF](https://homepages.uc.edu/~singgih/CounterExample-JCTB.pdf)；发表状态：作者公开的已发表论文版本；核验：逐式核对后，两系数交叉相乘之差的分子为 1，故反例不是数值近似误判。
  - `official_record` [Erdős Problem #612](https://www.erdosproblems.com/612)；发表状态：官方持续更新题页；核验：题页明确分开记录第一部分失败、修正版以及第二部分 r≥2 的未决状态。

#### #638

- 官方题面：Let $S$ be a family of finite graphs such that for every $n$ there is some $G_n\in S$ such that if the edges of $G_n$ are coloured with $n$ colours then there is a monochromatic triangle. Is it true that for every infinite cardinal $\aleph$ there is a graph $G$ of which every finite subgraph is in $S$ and if the edges of $G$ are coloured with $\aleph$ many colours then there is a monochromatic triangle.
- 上轮初筛：`counterexample`；按字面量词命题为假；数据库仍标 open，是因为原意很可能漏写了对 S 的闭包/年龄条件。先前候选的稀疏完全图反例正确，但其“于是 G 必为无边图”还应补充：即使无边图的有限子图未必属于 S，也已足以说明任何满足该条件的 G 不可能具有所需 Ramsey 性质。
- 字面命题：若有限图族 S 对每种有限颜色数都含一个箭头指向三角形的图，是否存在一个所有有限子图都属于 S、且对任意无限颜色数仍箭头指向三角形的无限图。
- 当前预期开放范围：不要求 S 具有遗传/年龄闭包时字面命题有平凡反例；加入合适闭包条件后的紧致性问题仍开放。
- 上轮声称：初轮给出 S={K_{R_3(n)}} 一类稀疏选取的完全图族作为反例，判为 counterexample。
- 审计判定：`literal_false_intended_open`
- 闭合评估：字面无闭包版本确实失败，但意图中的 hereditary 版本没有被当前公开 Lean 代码闭合。
- 官方仍开放原因：题面缺条件，官网保留 OPEN 以追踪修正版；强化反例也尚有实质缺口。
- 下一核验动作：先固定 S 的闭包公理，再补全有限规避原理；只有零 sorry 且通过编译的构造才能宣告修正版证否。
- 证据：

  - `official_record` [Erdős Problem #638](https://www.erdosproblems.com/638)；发表状态：官方持续更新题页；核验：官网承认原题似乎漏写 hereditary 条件，因此没有把平凡反例当作预期版本的解决。
  - `official_discussion` [Erdős Problem #638 discussion](https://www.erdosproblems.com/forum/thread/638)；发表状态：官方论坛与公开形式化讨论；核验：讨论提出更强的遗传反例方向，但关键有限规避原理和块序列构造尚未完整形式化。
  - `formalization_repository` [Erdos638 Lean repository](https://github.com/woeowiegj/Erdos638)；发表状态：公开 Lean 项目，未完成；核验：仓库只验证了紧致性归约；核心构造仍含 sorry，不能作为已公开的完整 Lean 闭合证据。

#### #654

- 官方题面：Let $x_1,\ldots,x_n\in \mathbb{R}^2$ with no four points on a circle. Must there exist some $x_i$ with at least $(1-o(1))n$ distinct distances to other $x_i$?
- 上轮初筛：`counterexample`；输入状态已过期。官方页面现记录 2026 年 Aletheia 的反例；最强的 (1−o(1))n 断言为假。
- 字面命题：无四点共圆的 n 点集是否总有一点与其余点形成至少 (1-o(1))n 种不同距离，并同时询问较弱的 (1/3+c)n 及一般位置版本。
- 当前预期开放范围：最强的 (1-o(1))n 已被 3n/4 型构造否定；较弱的绝对改进和无三点共线的一般位置版本仍开放。
- 上轮声称：初轮把 Aletheia 构造标为 counterexample，并称输入状态过期。
- 审计判定：`still_open_correct`
- 闭合评估：公开构造足以严格否定最强子问，却既不否定 (1/3+c)n，也不满足无三点共线；整题没有闭合。
- 官方仍开放原因：复合条目仍有两个实质未决方向。
- 下一核验动作：后续尝试应针对较弱常数 c 或把构造扰动到一般位置并控制距离重数。
- 证据：

  - `public_proof` [Aletheia Erdős construction](https://github.com/google-deepmind/superhuman/blob/main/aletheia/Erdos/Erdos.tex)；发表状态：2026 年公开证明文本，非期刊发表证明；核验：构造取坐标轴上的 (0,±3^k) 与 (±2^j,0)。四点共圆若各轴取两点会迫使相应坐标乘积相等，与 2、3 的素因子分解矛盾；每点不同距离数至多 3n/4+O(1)。本次独立复算通过。
  - `official_record` [Erdős Problem #654](https://www.erdosproblems.com/654)；发表状态：官方持续更新题页；核验：官网已收录该反例，但仍列出较弱下界与一般位置版本，故整体保持 OPEN。

#### #655

- 官方题面：Let $x_1,\ldots,x_n\in \mathbb{R}^2$ be such that no circle whose centre is one of the $x_i$ contains three other points. Are there at least\[(1+c)\frac{n}{2}\]distinct distances determined between the $x_i$, for some constant $c>0$ and all $n$ sufficiently large?
- 上轮初筛：`counterexample`；字面命题已被正 n 边形反驳；目录仍标 open，是因为原意可能还包含一般位置条件。人工评审所说“与 Hunter 的退化解相同”只否定候选答案的新颖性，不否定反例本身；不能据此宣称解决一般位置变体。
- 字面命题：若以每个给定点为圆心的圆至多经过另外两个点，是否必有至少 (1+c)n/2 种全局不同距离。
- 当前预期开放范围：字面条件允许正 n 边形，因此为假；原意很可能还要求无三点共线、无四点共圆的一般位置，后者仍开放。
- 上轮声称：初轮用正多边形给出 counterexample，并指出本地 Lean 只有陈述和 sorry。
- 审计判定：`literal_false_intended_open`
- 闭合评估：退化反例无误，但没有闭合一般位置版本；现有 Lean 文件也不提供机器证明。
- 官方仍开放原因：官网以 OPEN 追踪被认为是原意的一般位置问题。
- 下一核验动作：把一般位置假设写入正式题面与 Lean 定义，再讨论线性常数改进。
- 证据：

  - `official_record` [Erdős Problem #655](https://www.erdosproblems.com/655)；发表状态：官方持续更新题页；核验：官网记录 Hunter 的正多边形退化反例，也明确指出一般位置意图仍不清楚/未解决。
  - `formalization` [Formal Conjectures: Erdős 655](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/655.lean)；发表状态：公开 Lean 陈述文件，未完成；核验：主答案和定理含 sorry；一般位置变体同样未证明，不能称为公开 Lean 证明。
  - `independent_argument` [正 n 边形核对](https://www.erdosproblems.com/655)；发表状态：本次独立数学核算；核验：固定顶点到其他点的每个弦长最多出现两次，故满足字面圆条件；全局仅有 floor(n/2) 种距离，直接排除任意固定 c>0。

#### #701

- 官方题面：Let $\mathcal{F}$ be a family of sets closed under taking subsets (i.e. if $B\subseteq A\in\mathcal{F}$ then $B\in \mathcal{F}$). There exists some element $x$ such that whenever $\mathcal{F}'\subseteq \mathcal{F}$ is an intersecting subfamily we have\[\lvert \mathcal{F}'\rvert \leq \lvert \{ A\in \mathcal{F} : x\in A\}\rvert.\]
- 上轮初筛：`counterexample`；有限版本仍是 Chvátal 猜想，开放；无限字面版本则为假。因此旧候选的无限反例不能宣称解决官方有限问题，但确实暴露了当前形式化/陈述缺失有限性。
- 字面命题：本仓库文字与基准 Lean 量化任意类型上的下闭集合族，断言总有一个 star 不小于任意两两相交子族；没有有限地面集假设。
- 当前预期开放范围：官方意图是有限地面集上的 Chvátal 猜想，至今开放；无限字面版本为假。
- 上轮声称：初轮给出无限地面集反例，判为 counterexample，但当时尚未确认公开 Lean 代码是否真的完整。
- 审计判定：`literal_false_intended_open`
- 闭合评估：无限字面版本现已有可本地复现的零 sorry Lean 反例，闭合证据很强；但它不触及有限 Chvátal 猜想。
- 官方仍开放原因：官方问题是有限版本，公开 Lean 反例只揭示了仓库形式化缺条件。
- 下一核验动作：修正基准为有限地面集/有限族后重新运行形式化审计；不要把当前 Lean 反例登记为官方 #701 的解决。
- 证据：

  - `official_record` [Erdős Problem #701](https://www.erdosproblems.com/701)；发表状态：官方持续更新题页；核验：历史与已知特例都指向有限 Chvátal 猜想；没有证据显示有限问题已解决。
  - `formal_proof` [Lean counterexample to the infinite formulation](https://github.com/mo271/formal-conjectures/blob/cdea8caddce9f341ccf52a43815bf1e25d9a48b1/FormalConjectures/ErdosProblems/701.lean)；发表状态：公开零 sorry Lean 代码；核验：本次下载该固定提交并在本地 Formal Conjectures 环境运行 lake env lean，退出码 0。构造在 N×N 上取逐渐增大的有限块 A_n，并令下闭族为某个 A_n 的所有子集；任一固定 star 受限于一个块，而可选下一更大块的完整 star 作为更大的相交族。
  - `benchmark_formalization` [Formal Conjectures main benchmark: Erdős 701](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/701.lean)；发表状态：公开基准陈述，含 sorry；核验：当前基准仍量化任意 Type 且无有限性，定理为待证；它错误形式化了官方有限意图。

#### #786

- 官方题面：Let $\epsilon>0$. Is there some set $A\subset \mathbb{N}$ of density $>1-\epsilon$ such that $a_1\cdots a_r=b_1\cdots b_s$ with $a_i,b_j\in A$ can only hold when $r=s$? Similarly, can one always find a set $A\subset\{1,\ldots,N\}$ with this property of size $\geq (1-o(1))N$?
- 上轮初筛：`known_resolution`；冻结状态已过时。2026 年更新表明：允许重复的字面版本已有否定答案；互异因子版本仍开放。本地 Lean 的 IsMulCardSet 用 Finset，只形式化了互异版本，不能据此证明字面版本仍开放。
- 字面命题：若乘积因子允许重复，问是否可取密度任意接近 1 的 A，使两个来自 A 的有限乘积相等时因子个数必相同；另有同侧因子互异版本。
- 当前预期开放范围：允许重复的字面版本已由经典结果否定；只允许互异元素的版本仍开放。
- 上轮声称：初轮判 known_resolution，并指出 Finset 形式化实际上编码的是互异版本。
- 审计判定：`literal_false_intended_open`
- 闭合评估：已发表论文足以证否允许重复的版本；互异版本的关键加法函数归约失效，仍未闭合。
- 官方仍开放原因：官网 OPEN 对应互异元素修正版。
- 下一核验动作：为两种版本建立不同题号或显式量词，并对互异版本寻找不依赖完全可加函数的结构约束。
- 证据：

  - `published_paper` [Erdős–Ruzsa–Sárközy, Acta Arithmetica 24 (1973), 1–9](https://eudml.org/doc/205209)；发表状态：1973 年已发表论文；核验：官网所引 Theorem 2 对相应加法层集给出密度至多 1/2，并在有限情形给出与 1 有界分离；允许重复时由唯一分解定义加法函数即可转回乘积问题。
  - `official_record` [Erdős Problem #786](https://www.erdosproblems.com/786)；发表状态：官方持续更新题页；核验：题页明确区分 repetition allowed 与 distinct-elements 两个版本，只把前者视为已否定。
  - `formalization` [Formal Conjectures: Erdős 786](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/786.lean)；发表状态：公开 Lean 陈述文件，含 sorry；核验：使用 Finset，因此同侧因子互异；文件没有证明，且不能作为重复版本的闭合证据。

#### #796

- 官方题面：Let $k\geq 2$ and let $g_k(n)$ be the largest possible size of $A\subseteq \{1,\ldots,n\}$ such that every $m$ has $<k$ solutions to $m=a_1a_2$ with $a_1<a_2\in A$. Is it true that\[g_3(n)=\frac{\log\log n}{\log n}n+(c+o(1))\frac{n}{(\log n)^2}\]for some constant $c$?
- 上轮初筛：`counterexample`；冻结题面含 log²，但现行官方页面已把主问题更正为余项 n/log n，并解释旧文中的 log² 很可能是重复排印错误。故对输入中的精确命题，答案是否定的；更正后的常数问题仍开放。
- 字面命题：冻结题面问 g_3(n) 的第二项是否为 (c+o(1))n/(log n)^2。
- 当前预期开放范围：现行官网已更正为 n/log n 尺度；该尺度上的精确常数仍开放。
- 上轮声称：初轮判 counterexample，依据现行页面说明 log² 是重复排印错误且已知方法给出 n/log n 量级。
- 审计判定：`literal_false_intended_open`
- 闭合评估：冻结 log² 版本已被数量级结果排除，但更正后的 n/log n 精确常数问题未解决。
- 官方仍开放原因：官网追踪的是勘误后的问题。
- 下一核验动作：修复仓库题面并从 Er64 的上下界常数开始，避免继续研究错误的 log² 尺度。
- 证据：

  - `official_record` [Erdős Problem #796](https://www.erdosproblems.com/796)；发表状态：官方持续更新题页；核验：页面现写 n/log n，并详细说明 Er69 的 log² 很可能是重复的排印错误；Er64 技术已有上下常数倍 n/log n。
  - `statement_correction` [历史题面勘误记录](https://www.erdosproblems.com/796)；发表状态：官网编辑性勘误，不是新证明；核验：证据支持冻结版本不是正确开放命题；它不提供现行常数 c 的值。

#### #836

- 官方题面：Let $r\geq 2$ and $G$ be a $r$-uniform hypergraph with chromatic number $3$ (that is, there is a $3$-colouring of the vertices of $G$ such that no edge is monochromatic). Suppose any two edges of $G$ have a non-empty intersection. Must $G$ contain $O(r^2)$ many vertices? Must there be two edges which meet in $\gg r$ many vertices?
- 上轮初筛：`counterexample`；第一问已有 Alon 反例，故是否定的；第二问仍开放，已知保证仅为 Ω(r/log r)。原题括号只解释了“可三染色”，但任意相交超图本来就可三染色，所以必须连同 χ=3 的“不可二染色”含义使用。
- 字面命题：对 r-一致、两两相交且色数为 3 的超图，问顶点数是否总为 O(r²)，以及是否总有两条边交于 Ω(r) 个点。
- 当前预期开放范围：第一问已由 Alon 构造否定；第二问仍开放，当前一般下界仅 Ω(r/log r)。
- 上轮声称：初轮整体标 counterexample，但同时说明第二问未解决。
- 审计判定：`still_open_correct`
- 闭合评估：这是两个子问组成的条目；第一问证否不等于第二问闭合，官网 OPEN 正确。
- 官方仍开放原因：线性交叠下界仍比最佳已知结果多一个 log r 因子。
- 下一核验动作：将后续工作集中到第二问，并明确使用 χ=3 包括不可二染色，而非仅“可三染色”。
- 证据：

  - `official_record` [Erdős Problem #836](https://www.erdosproblems.com/836)；发表状态：官方持续更新题页；核验：官网明确记载 Alon 对 O(r²) 的反例，并把线性交叠问题保留为 OPEN。
  - `published_background` [Erdős–Lovász original paper bibliographic record](https://www.maths.tcd.ie/EMIS/classics/Erdos/cit/31505117.htm)；发表状态：原始已发表论文的书目与公开记录；核验：经典论证只保证 Ω(r/log r) 量级；没有发现升级到绝对常数乘 r 的已发表证明。

#### #890

- 官方题面：If $\omega(n)$ counts the number of distinct prime factors of $n$, then is it true that, for every $k\geq 1$,\[\liminf_{n\to \infty}\sum_{0\leq i<k}\omega(n+i)\leq k+\pi(k)?\]Is it true that\[\limsup_{n\to \infty}\left(\sum_{0\leq i<k}\omega(n+i)\right) \frac{\log\log n}{\log n}=1?\]
- 上轮初筛：`counterexample`；输入中的第一问不是开放命题，而是错误版本，可严格反驳；修正版仍开放。第二问对 k=1 是经典定理，对 k≥2 仍开放。因此该复合问题不能整体宣称解决。
- 字面命题：冻结第一问用普通 ω(n+i) 并猜 liminf 的和不超过 k+π(k)；另问相应 limsup 归一化是否为 1。
- 当前预期开放范围：官网已把第一问修成只数大于 k 的素因子 ω_k，右端也相应为 k；修正版及 k≥2 的第二问仍开放。
- 上轮声称：初轮以 k=26 的小素数强制贡献反驳普通 ω 版本，判 counterexample。
- 审计判定：`literal_false_intended_open`
- 闭合评估：冻结转录错误被严格反驳；正确修正版没有被这一反例触及。
- 官方仍开放原因：官网已修题，仍没有正确版本的证明。
- 下一核验动作：更新仓库陈述为 ω_k 版本，并分别追踪第一、第二问的已知上下界。
- 证据：

  - `official_record` [Erdős Problem #890](https://www.erdosproblems.com/890)；发表状态：官方持续更新题页；核验：页面明确说明普通 ω、k+π(k) 是错误版本，当前使用 ω_k 并保留两个正确问题。
  - `independent_argument` [k=26 强制小素因子核对](https://www.erdosproblems.com/890)；发表状态：本次独立数学核算；核验：任意连续 k 个整数中，小素数 p≤k 至少整除 floor(k/p) 个；k=26 时这些贡献总和为 36，而 k+π(k)=35，故冻结第一问对每个 n 都失败。
  - `formalization` [Formal Conjectures: Erdős 890](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/890.lean)；发表状态：公开 Lean 陈述文件，含 sorry；核验：文件采用修正后的 ω_k，但定理未证明，不能视作 Lean 闭合。

#### #917

- 官方题面：Let $k\geq 4$ and $f_k(n)$ be the largest number of edges in a graph on $n$ vertices which has chromatic number $k$ and is critical (i.e. deleting any edge reduces the chromatic number). Is it true that\[f_k(n) \gg_k n^2?\]Is it true that\[f_6(n)\sim n^2/4?\]More generally, is it true that, for $k\geq 6$,\[f_k(n) \sim \frac{1}{2}\left(1-\frac{1}{\lfloor k/3\rfloor}\right)n^2?\]
- 上轮初筛：`known_resolution`；这是混合状态：第一问 Toft 已证为真；第二问仍开放；第三问在 k≡1,2 mod 3 时已被 Stiebitz 反例否定，在 k≡0 mod 3 时仍开放。因此不能笼统称整题“open”。
- 字面命题：关于 k-临界图最大边数 f_k(n) 的三个问题：固定 k 是否有二次下界、k=6 是否渐近 n²/4、以及所有 k≥6 是否满足给定统一渐近公式。
- 当前预期开放范围：第一问 Toft 已证明；第二问仍开放；第三问在 k≡1,2 mod 3 已由 Stiebitz 否定，在 k≡0 mod 3 仍开放。
- 上轮声称：初轮标 known_resolution，但正文承认是混合状态；该顶层标签会夸大闭合范围。
- 审计判定：`still_open_correct`
- 闭合评估：若把 #917 视为复合条目，仍有核心子问未决；初轮不应以单一 known_resolution 暗示整题关闭。
- 官方仍开放原因：k=6 与一整类 k 的渐近问题仍开放。
- 下一核验动作：将三个子问拆成独立状态记录，证明工作优先选 k=6 或 k≡0 mod 3。
- 证据：

  - `official_record` [Erdős Problem #917](https://www.erdosproblems.com/917)；发表状态：官方持续更新题页；核验：题页逐项记录 Toft 定理、Dirac 构造、Stiebitz 反例及仍开放的同余类。
  - `recent_bounds` [Luo–Ma–Yang, Dense critical graphs](https://arxiv.org/abs/2301.01656)；发表状态：公开预印本/后续研究记录；核验：提供新的上界，但没有解决 k=6 渐近或 k≡0 mod 3 的剩余统一公式。

#### #918

- 官方题面：Is there a graph with $\aleph_2$ vertices and chromatic number $\aleph_2$ such that every subgraph on $\aleph_1$ vertices has chromatic number $\leq\aleph_0$? Is there a graph with $\aleph_{\omega+1}$ vertices and chromatic number $\aleph_1$ such that every subgraph on $\aleph_\omega$ vertices has chromatic number $\leq\aleph_0$?
- 上轮初筛：`independent`；第一问在大基数相对一致性意义下独立：L 中有正例，而 Foreman–Laver 给出与 GCH 相容的无例模型。第二问在 L 等满足 CH_{ℵω}+□_{ℵω} 的模型中有正例，但相应可数界紧致性的负模型是否一致仍未解决，故不能把第二问也宣称已独立。
- 字面命题：第一问寻求大小与色数均为 ℵ₂、而每个 ℵ₁ 点子图可数着色的图；第二问寻求大小 ℵ_{ω+1}、色数 ℵ₁、而每个 ℵ_ω 点子图可数着色的图。
- 当前预期开放范围：第一问具有相对一致性独立现象；第二问在 L 中有正例，但对应可数界的负一致性仍开放。
- 上轮声称：初轮顶层判 independent，虽在正文中正确提醒第二问尚未独立；标签范围仍然过宽。
- 审计判定：`independence_scope_mismatch`
- 闭合评估：第一问的相对独立性有可靠文献支持；把结论扩张到第二问则错误，整题仍开放。
- 官方仍开放原因：第二问缺少相应的负一致性结果，且独立性本身须相对于明确公理体系表述。
- 下一核验动作：把两问拆开标注：第一问记录相对一致性，第二问集中研究 ℵ_0 色界的 compactness/反射模型。
- 证据：

  - `research_paper` [Lambie-Hanson–Rinot, Reflection on the coloring and chromatic numbers](https://arxiv.org/abs/1708.06929)；发表状态：公开研究论文版本；核验：Results 2.1–2.2 显示：V=L 给第一问正例；Foreman–Laver 在大基数相对一致性下给无例模型。对 λ=ℵ_ω，CH_λ+square_λ 给第二问正例，但论文脚注明确说 n=0 的负模型情形仍开放，正对应可数色界。
  - `official_record` [Erdős Problem #918](https://www.erdosproblems.com/918)；发表状态：官方持续更新题页；核验：官网仍把复合问题列 OPEN，与第二问的未决一致。
  - `formalization` [Formal Conjectures: Erdős 918](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/918.lean)；发表状态：公开 Lean 陈述文件，含 sorry；核验：第二部分错误地对所有 ordinal ω 量化，且无证明；既不忠实也不构成独立性形式证明。

#### #920

- 官方题面：Let $g_k(n)$ denote the largest possible chromatic number of a graph with $n$ vertices which contains no $K_k$. Is it true that, for $k\geq 4$,\[g_k(n) \gg \frac{n^{1-\frac{1}{k-1}}}{(\log n)^c}\]for some constant $c>0$?
- 上轮初筛：`known_resolution`；输入中的 OPEN 状态已经过期。Bradač 的 arXiv v3（2026-06-16）证明了足够强的 off-diagonal Ramsey 下界；官方关联问题 #986 已于 2026-06-21 标为 PROVED。由标准反演可肯定回答 #920，虽然 #920 页面本身尚未同步改状态。先前候选只处理 $k=4$、称 $k\ge5$ 未知，现已失效。
- 字面命题：固定 k≥4，K_k-free 的 n 点图最大色数 g_k(n) 是否至少为 n^{1-1/(k-1)} 除以某个 log 的固定幂。
- 当前预期开放范围：Bradač 2026 v3 的 off-diagonal Ramsey 下界若正确，经过标准反演已经肯定回答全题；#920 页面似乎尚未同步。
- 上轮声称：初轮判 known_resolution，并由 R(k,t) 下界反演出所需色数界。
- 审计判定：`likely_status_stale`
- 闭合评估：量词和指数反演均已核对，若 Bradač v3 获接受则 #920 确已闭合；结合 #986 已官方标 PROVED，#920 的 OPEN 很可能只是同步滞后。
- 官方仍开放原因：页面更新早于最新论文版本，尚未执行状态联动。
- 下一核验动作：向官网维护者提交 #986→#920 的显式推论与参数反演，请其确认改为 PROVED；同时跟踪论文最终发表状态。
- 证据：

  - `preprint` [Bradač, Off-diagonal Ramsey numbers](https://arxiv.org/abs/2605.28793v3)；发表状态：2026-06-16 arXiv v3，近期预印本；核验：主定理给 R(s,t)≥Ω(t^{s-1}/(log t)^{2s-4})。取 t≈n^{1/(k-1)}(log n)^{(2k-4)/(k-1)}，得到 K_k-free 图且 α<t，从而 χ≥n/t，正是 #920 所需形式。
  - `official_cross_record` [Erdős Problem #986](https://www.erdosproblems.com/986)；发表状态：官方题页已标 PROVED；核验：#986 已接受同一 Ramsey 下界，并明确关联 #920；这显著增强了结论可信度。
  - `official_record` [Erdős Problem #920](https://www.erdosproblems.com/920)；发表状态：官方页面仍标 OPEN；核验：页面最后更新时间早于相关 v3 与 #986 的关闭，且旧备注本已说明 #986 的肯定答案会推出本题。
  - `formalization` [Formal Conjectures: Erdős 920](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/920.lean)；发表状态：公开 Lean 陈述文件，含 sorry；核验：形式化文件没有提供证明；闭合依据是数学预印本与官方关联题，不是 Lean。

#### #935

- 官方题面：For any integer $n=\prod p^{k_p}$ let $Q_2(n)$ be the powerful part of $n$, so that\[Q_2(n) = \prod_{\substack{p\\ k_p\geq 2}}p^{k_p}.\]Is it true that, for every $\epsilon>0$ and $\ell\geq 1$, if $n$ is sufficiently large then\[Q_2(n(n+1)\cdots(n+\ell))<n^{2+\epsilon}?\]If $\ell\geq 2$ then is\[\limsup_{n\to \infty}\frac{Q_2(n(n+1)\cdots(n+\ell))}{n^2}\]infinite? If $\ell\geq 2$ then is\[\lim_{n\to \infty}\frac{Q_2(n(n+1)\cdots(n+\ell))}{n^{\ell+1}}=0?\]
- 上轮初筛：`known_resolution`；输入状态已过时。官方页面 2026-02-08 更新：第二问已由 Pell 方程构造肯定解决；第一问（除平凡的 $\ell=1$）与第三问仍开放，第三问在 ABC 猜想下成立。旧候选称第二问开放，必须弃用。
- 字面命题：关于连续 ℓ+1 个整数乘积的 powerful part Q_2 有三个子问：n^{2+ε} 上界、ℓ≥2 时 Q_2/n² 的 limsup 是否无穷、以及 Q_2/n^{ℓ+1} 是否趋零。
- 当前预期开放范围：第二问已经由 Pell 方程构造肯定解决；第一问与第三问仍开放，第三问只在 ABC 假设下已知。
- 上轮声称：初轮判 known_resolution，主要依据第二问的 2026 更新，但正文承认其余两问未解决。
- 审计判定：`still_open_correct`
- 闭合评估：第二子问已有可检查的数学证明及公开 Lean 佐证，但三个子问中仍有两个未决；顶层 OPEN 正确。
- 官方仍开放原因：复合题只部分闭合，尤其无条件第三问仍开放。
- 下一核验动作：拆分子问状态；若要提升形式证据，可在对应 Lean v4.24 环境复现 #367 构建。
- 证据：

  - `official_record` [Erdős Problem #935](https://www.erdosproblems.com/935)；发表状态：官方持续更新题页；核验：页面明确把第二问标为已解决，同时仍陈列第一、第三问与 ABC 条件结果。
  - `official_proof_discussion` [Pell construction for related Problem #367](https://www.erdosproblems.com/forum/thread/367)；发表状态：官方论坛公开证明；核验：构造取 Pell 方程 x²-8y²=1、n=8y²，并沿子序列保证高次 5 整除 n+2，可得 powerful parts 的乘积超过任意常数倍 n²，恰证明 limsup 无穷。
  - `formal_proof` [Lean proof for Erdős #367](https://github.com/plby/lean-proofs/blob/main/src/v4.24.0/ErdosProblems/Erdos367.lean)；发表状态：公开零 sorry Lean 源码，使用 Lean v4.24；核验：源码陈述并证明对每个 C 存在 n，使三个连续数的 powerful parts 乘积大于 Cn²；代码中未见 sorry。本次未因版本差异做本地重编译，因此将其作为强佐证而非独立构建认证。

#### #985

- 官方题面：Is it true that, for every prime $p$, there is a prime $q<p$ which is a primitive root modulo $p$?
- 上轮初筛：`counterexample`；字面陈述被 p=2 立即反驳，因为不存在素数 q<2；通常研究版本排除 p=2，只问所有奇素数，此版本仍开放。本地形式化也显式加入 p≠2。先前候选在这一点上的校正正确。
- 字面命题：对每个素数 p，是否存在更小素数 q<p，使 q 模 p 的乘法阶为 p-1。
- 当前预期开放范围：p=2 是立即反例；真正研究的是每个奇素数 p 是否有小于 p 的素数原根，该版本仍开放。
- 上轮声称：初轮以 p=2 判 counterexample，并正确指出本地形式化显式排除了 2。
- 审计判定：`literal_false_intended_open`
- 闭合评估：p=2 完全反驳字面全称命题，但对奇素数版本没有任何闭合作用。
- 官方仍开放原因：数学上有意义的奇素数版本仍远超已知 Artin 型结果。
- 下一核验动作：修正仓库题面为 p>2，并明确区分“固定 q 对无穷多 p”与“每个 p 可选 q<p”的量词。
- 证据：

  - `official_record` [Erdős Problem #985](https://www.erdosproblems.com/985)；发表状态：官方持续更新题页；核验：上下文显然针对奇素数，且没有给出每个奇 p 的无条件证明。
  - `published_related_result` [Heath-Brown, Artin's conjecture for primitive roots](https://doi.org/10.1093/qmath/37.1.27)；发表状态：Quarterly Journal of Mathematics 37 (1986)，已发表；核验：结果说明 2、3、5 中至少一个是无穷多个素数模数的原根；量词远弱于“对每个奇素数 p 存在 q<p”，不能闭合本题。
  - `formalization` [Formal Conjectures: Erdős 985](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/985.lean)；发表状态：公开 Lean 陈述文件，含 sorry；核验：形式化显式假设 p≠2，但主定理未证明；它确认 p=2 是被有意排除的退化点。

#### #1070

- 官方题面：Let $f(n)$ be maximal such that, given any $n$ points in $\mathbb{R}^2$, there exist $f(n)$ points such that no two are distance $1$ apart. Estimate $f(n)$. In particular, is it true that $f(n)\geq n/4$?
- 上轮初筛：`counterexample`；冻结输入标为 open，但此后出现重要进展：2026-06-26 的 Dúcz–Varga 预印本声称构造有限单位距离图满足 \(\alpha(G)/|V(G)|<1/4\)，从而否定特别问题。总的渐近估计仍开放；该结果目前是新预印本。
- 字面命题：令 f(n) 为所有 n 点平面单位距离图的最小独立数；除估计 f(n) 外，特别问是否总有 f(n)≥n/4。
- 当前预期开放范围：2026 年新预印本及其公开证书强力证否 n/4 特别问题；但完整估计 f(n) 仍开放，且新结果尚处 v1 阶段。
- 上轮声称：初轮判 counterexample，引用 Dúcz–Varga 预印本，但未独立运行其大规模证书。
- 审计判定：`recent_claim_unverified`
- 闭合评估：证书的独立复跑显著支持严格小于 1/4 的计算结论，且几何与线性规划环节均通过；但论文仍为近期 v1，完整 f(n) 问题也未闭合，因此不应把整个 #1070 标为已解决。
- 官方仍开放原因：一方面官方可能等待新预印本核验，另一方面题目首句的总体渐近估计本来仍开放。
- 下一核验动作：保留可复现环境与哈希，由第二实现交叉检查证书；跟踪论文修订/发表，并把特别问题与总体估计拆分状态。
- 证据：

  - `preprint` [Dúcz–Varga, A counterexample to Erdős Problem 1070](https://arxiv.org/abs/2606.28157v1)；发表状态：2026-06-26 arXiv v1，尚无同行评审完成证据；核验：Theorem 1 明确构造有限平面单位距离图 G，使 α(G)/|V(G)|<1/4；它证否特别问题，但没有给出 f(n) 的完整渐近。
  - `computational_certificate` [Erdős Problem 1070 supplementary certificate](https://users.renyi.hu/~akos/ep1070/)；发表状态：作者公开源码、数据与有理对偶见证；核验：本次下载 snail.zip，运行 python3 snail_reproduction/verify_data.py，退出码 0。程序符号验证 29 点图的单位距离邻接，枚举 498168 个独立集，验证 16859 个同余约束，并以精确有理/整数运算核对对偶见证；MIN_SLACK=0，DUAL_VAL≈4.000716234987108>4。
  - `official_record` [Erdős Problem #1070](https://www.erdosproblems.com/1070)；发表状态：官方题页仍标 OPEN；核验：主条目仍追踪总体估计，近期反例处于新声称阶段；因此顶层状态尚未关闭。

#### #1112

- 官方题面：Let $1\leq d_1<d_2$ and $k\geq 3$. Does there exist an integer $r$ such that if $B=\{b_1<\cdots\}$ is a lacunary sequence of positive integers with $b_{i+1}\geq rb_i$ then there exists a sequence of positive integers $A=\{a_1<\cdots\}$ such that\[d_1\leq a_{i+1}-a_i\leq d_2\]for all $i\geq 1$ and $(kA)\cap B=\emptyset$, where $kA$ is the $k$-fold sumset?
- 上轮初筛：`counterexample`；不能作统一肯定回答：\((d_1,d_2,k)=(2,3,3)\) 已有反例，故 \(r_3(2,3)\) 不存在；其他一般参数的分类仍开放。先前候选对此判断正确。
- 字面命题：对每组 1≤d_1<d_2、k≥3，是否存在 r，使任意增长比至少 r 的序列 B 都能被一个相邻差落在 [d_1,d_2] 的无限序列 A 的所有 k 项和避开。
- 当前预期开放范围：参数 (d_1,d_2,k)=(2,3,3) 已有已发表否定结果；其他参数的一般存在性与分类仍开放。
- 上轮声称：初轮判 counterexample，引用 BHJ 论文说明 r_3(2,3) 不存在。
- 审计判定：`still_open_correct`
- 闭合评估：特定参数的否定有正式发表证据，但一般分类远未闭合；把整题标为 counterexample 会掩盖剩余范围。
- 官方仍开放原因：复合参数问题仍有大量未决情形。
- 下一核验动作：建立已知参数状态表，隔离 BHJ 反例机制覆盖的区域，再选择最小未决参数继续证明。
- 证据：

  - `published_paper` [Bialostocki–Hindman–Jones, A Ramsey-type sum avoidance result](https://doi.org/10.1016/S0012-365X(96)00122-7)；发表状态：Discrete Mathematics，1997 年已发表；核验：论文给出变比率反例，严格证明 r_3(2,3) 不存在；这足以否定对所有参数统一肯定的字面版本。
  - `institutional_record` [University of Memphis publication record](https://digitalcommons.memphis.edu/facpubs/5256/)；发表状态：机构库中的已发表论文元数据；核验：作者、期刊、年份与 DOI 均相互吻合，不是未发表手稿或仅有声称。
  - `official_record` [Erdős Problem #1112](https://www.erdosproblems.com/1112)；发表状态：官方持续更新题页；核验：官网明确记录 r_3(2,3) 不存在，同时仍询问一般参数。

## 第三部分：23 条优先路线的最长两小时续攻

### 结论分布

| 结论 | 数量 |
|---|---:|
| route_advanced | 18 |
| route_refuted | 3 |
| candidate_full_proof | 1 |
| route_blocked | 1 |

`route_advanced` 表示得到严格的新引理、界或更窄的下一定理；`route_refuted` 表示预定路线的核心目标被反例击穿；`route_blocked` 表示复核后没有越过首个明确障碍；`candidate_full_proof`/`candidate_counterexample` 只在精确量词闭合时使用，仍须看随附的独立审阅与证据层级。

### 总表

| # | 用时 | 结论 | 下一精确定理/任务 |
|---:|---:|---|---|
| 952 | 868.3 秒 | route_advanced | 最清晰的下一有限定理是独立机核 Gethner–Stark 第2节的 D=4 实例：对 m=7113990，证明 B_m 在差向量平方模≤4的图中无非零绕数闭路。由于 m² 枚举不可行，需要按 m=2·3·5·13·17·29·37 的 CRT 分解构造压缩商图/可检查证书；这将验证周期筛路线确实可从√2推进到2，并给一般 D 的算法接口。 |
| 1083 | 628.8 秒 | route_blocked | 建议下一节点是如下“锐余维2非集中界”。固定 d≥3，P⊂R^d、\|P\|=n，令 m=max_H\|P∩H\|，其中 H 遍历余维2仿射平面。证明 \|Δ(P)\| ≥ n^{-o_d(1)} n^{(d²+d+2)/(2d²)} m^{-(d−1)/(2d)}. 另一方面平凡地有 \|Δ(P)\|≥f_{d−2}(m)。若归纳输入 f_{d−2}(m)≥m^{2/(d−2)-o(1)}，令 m=n^x，则两个指数分别为 A−bx 与 2x/(d−2)；最坏平衡点是 x=(d−2)/d，二者都恰等于2/d。该命题比 Solymosi–Vu Theorem 2.2 的 n 指数 (d+1)/(2d) 恰强 1/d²，并在格点上指数锐利。 |
| 1039 | 670.2 秒 | candidate_full_proof | 下一步最清晰的独立定理是证明或反驳精确配对结式界，并刻画其等号情形；更深入的原问题则是确定 liminf_n n·inf_{deg f=n}ρ(f) 的精确常数，当前证明只给 log2≤nρ_n≤π（原始论文给更好的上侧常数 π/2）。 |
| 25 | 827.0 秒 | route_refuted | 令 B_K 为前 K 个完整剩余类的周期幸存集，密度 d_K，d_*=inf_Kd_K，并定义 ℓ_{K,j}=(log2)^{-1}Σ_{2^j≤n<2^{j+1}, n∈B_K\A}1/n。一个足以闭合原题、且未被单块反例否定的精确下一定理是：存在绝对常数 C，使对每个 K，limsup_{J→∞}J^{-1}Σ_{j<J}ℓ_{K,j}≤C(d_K-d_*)。由此 δ̲_log(A)≥d_K-C(d_K-d_*)，再令 K→∞ 即得 δ_log(A)=d_*。 |
| 117 | 891.3 秒 | route_advanced | 最明确的下一定理是：证明无限多个 m 满足 ω(W(2m−1,3))≤Cm+O(1)，其中 C<2log₂3≈3.169925；这会推出严格优于 √2 的下界。反之，若证明 ω(W(2m−1,3))≥(2log₂3−o(1))m，则可排除 extraspecial 3-群的渐近改进。 |
| 143 | 755.9 秒 | route_advanced | 最清晰且由 KLL 第5页直接指向的下一定理是：设 A⊂Q_{>1} 满足原 dilation separation；把每个 α∈A 写成既约分数 a/q，并额外假设所有分子 a 均平方自由，则证明 ∑_{α∈A}1/(α log α)<∞。具体首个技术子目标应是建立一个“κ-质量版本”的 Proposition 2.15/分块能量界，使坏相关贡献为 O(κ(B)) 或 O(∑_j κ(B_j)^2)，而不是与所用尺度块数成正比。平方自由性保证分解 a=Aa_0 时 gcd(A,a_0)=1，可去掉 KLL 所述 Hauke–Vázquez–Walker 的额外损失；剩余核心正是跨尺度选择问题。 |
| 148 | 1047.8 秒 | route_advanced | 明确的充分目标是：存在 0<δ<3/5，使对所有 m≤5n，\[\sum_{\substack{0<u\le4n\\m\mid u+n}} f_4\!\left(u,\frac{n(u+n)}m\right)\ll_\epsilon n^\epsilon\left(\frac{n^2}{m}\right)^{8/5-\delta}.\]这会给五项指数 c=8/5−δ；套同一 lifting 与固定 L 模板，即严格改善为 \(F(k)\le c_0^{(1/5-\delta/8+o(1))2^k}\)。允许尾分母下界的严格递增版本也值得先证，但还需重写 lifting 引理以保持该约束。 |
| 256 | 779.3 秒 | route_advanced | 最直接的下一定理是：存在固定 δ>0，使每个充分大 n 都有有限非增非负整数序列 b_1≥b_2≥⋯、∑b_k=n，且 a_0+∑b_k cos(kx)≥0 对所有实 x 成立，同时 a_0=O((log n)^{3-δ})。由本次桥梁将立即推出 log f(n)=O((log n)^{4-δ})。另一独立目标是证明所有纯乘积均有 ∑c_j²≥(2+ε)n；这会提高 2√n 的常数，但不会改变增长指数。 |
| 301 | 1791.0 秒 | route_advanced | 建议下一步精确证明如下加权穿孔盒定理：若 C⊂ℕ₀³ 且平移族 {c+B*:c∈C} 两两不交，其中 B*=[0,4]×[0,2]×[0,1]\{(0,0,0)}，则 Σ_{(r,s,t)∈C}2^{-r}3^{-s}5^{-t}≤450/403。等号由 C={(5i,3j,2k):i,j,k≥0} 达到。该定理若成立，将证明 120/403 是固定 720 块所有按 (v₂,v₃,v₅) 选取的不交缩放族中的最优密度；有限 MILP 已在 [0,15]×[0,9]×[0,6] 上支持它，但尚缺处理无限尾部的严格对偶或递归证书。 |
| 325 | 637.6 秒 | route_advanced | 对每个固定3≤k≤10，构造集合 S_{1,B},S_{2,B},S_{3,B}⊂[1,B]，满足 \|S_{1,B}\|\|S_{2,B}\|\|S_{3,B}\|≥B^{3−o(1)}，并证明 E_k(S_1,S_2,S_3):=#{(a_i,b_i)∈S_i^2:∑_{i=1}^3a_i^k=∑_{i=1}^3b_i^k}≤B^{3+o(1)}。这将逐量词推出弱版本；若三个集合有固定正密度且 E_k≪_kB^3，则推出强版本。 |
| 332 | 589.5 秒 | route_advanced | 下一步可加强为“popular recurrent differences”版本：对 δ=d*(A)>0、0<ε<δ²，证明 R_ε={d∈ℤ:d*(A∩(A−d))>δ²−ε} syndetic。该命题需要完整重建对应原理的不等式方向与 Khintchine 回归，不能由本次有限交论证直接得到。 |
| 377 | 938.8 秒 | route_refuted | 精确的下一定理应是“小素数核心引理”：证明存在绝对常数 \(A\)，使所有 \(n\) 都满足 \[\sum_{p\le n^{1/3}\atop p\nmid\binom{2n}{n}}\frac1p\le A.\]这一定理不会被固定素数显式族反驳，并与 Mertens 的 \(n^{1/3}<p\le n\) 常数界合并后闭合原题全部量词。证明它必须对 \((p,j)\) 二维区域整体估计，而不能逐层取 \(\sup_n\)。 |
| 539 | 933.1 秒 | route_advanced | 一个清晰且足以推进的下一定理是：存在绝对常数 C，使对所有深度 s 和 n，\[h(n)\le \exp(Cs^2)n^{\alpha_s},\qquad \alpha_s=\frac{2^{s+1}}{2^{s+2}-1}.\]这把当前固定深度常数 \(\exp(O(2^s))\) 改为 \(\exp(O(s^2))\)；取 \(s\asymp\log_2\log n\) 将立即推出 \(h(n)\le\sqrt n\exp(O((\log\log n)^2))\)。本次障碍分析表明，证明它必须利用跨层正部差的额外重合或引入不同于独立笛卡尔平方的构造。 |
| 635 | 659.7 秒 | route_advanced | 最清晰的下一定理是 t=2 的精确候选：F_2(N)=⌈N/2⌉+#{k≥1:k为奇数且2^k≤N}。较稳健的中间目标是先证明 F_2(N)≤N/2+O(log N)。计算已支持精确式至 N=500（并检查若干 N≤2000），但尚无覆盖全部 N 的注入、匹配或对偶证书。 |
| 679 | 806.5 秒 | route_advanced | 清晰的下一目标是 Lau 的 Conjecture 8：证明其指定短区间内总有满足 ω(m)≥C₀log₂m/log₃m 的整数，其中常数满足 1≤d<C₀。Lau 的 Theorem 7.3 已证明该猜想会给出某个固定 δ>0，并对每个充分大 n 产生 1≪k<n、ω(n−k)>(1+δ)log k/loglog k，从而否定第一问。 |
| 686 | 845.0 秒 | route_advanced | 精确下一定理：令 F₅(t)=∏_{i=1}^5(t+i)，证明方程 F₅(m)=4F₅(n) 没有满足 n,m∈ℕ、m≥n+5 的解。必须完整确定该五次曲线的相关整数点，或给出等价的可认证 Thue/Thue–Mahler 归约；单纯有界搜索不够。 |
| 776 | 690.1 秒 | route_advanced | 下一精确定理应是判定对所有 $r\ge4$ 是否有 $g(2r+4,r)\le2r$。对应的局部目标是推广覆盖引理：控制一个 $r$ 边图在同时存在连续高层补集反链时的 2、3、4-顶点覆盖轮廓；若该命题为假，则应从其最小覆盖轮廓构造 $n=2r+4$ 的反链。 |
| 788 | 821.6 秒 | route_advanced | 足够且接近最弱的下一定理是：当 N→∞（至少沿偶数 N）且 p=N^{-1/2+o(1)} 时，随机 S_p⊆ℤ_N 以高概率满足 α(Γ⁺(ℤ_N,S_p))≤p^{-1}N^{o(1)}。更弱的确定性版本也足够：对每个偶数 N，存在 S_N⊆ℤ_N，使 \|S_N\|≤N^{1/2+o(1)} 且 α(Γ⁺(ℤ_N,S_N))≤N^{1/2+o(1)}。任一版本经上述模 2n 转移立即推出 f(n)≤n^{1/2+o(1)}。 |
| 827 | 1034.4 秒 | route_advanced | 一个精确且严格强于已知结果的下一定理是：存在 ε,c>0，使每个 N 点原始一般位置集都含至少 cN^{1/5}(log N)^{1/5+ε} 个点，其所有三元组外接半径互异。证明它等价于把 n_k 上界中的 log k 至少再提高固定正幂；可行切入口应是“富等半径代数曲线/稀疏剩余”二分，而非错误的统一常数共度假设。 |
| 934 | 786.5 秒 | route_refuted | 新的精确目标是 2026 预印本 Problem 1.12：证明或反驳“对充分大的 $\Delta$，$h_3(\Delta)\le\frac{253}{225}\Delta^3$”。一个更窄、可先攻击的种子定理是：若 $H$ 为 $r$-正则且 $\operatorname{diam}L(H)\le3$，是否总有 $\|E(H)\|\le\frac{253}{225}r^3$？它若成立，只能封住现有射影极性放大机制，尚不足以证明完整上界。 |
| 950 | 802.6 秒 | route_advanced | 优先证明以下精确的多尺度下界：对每个固定 \(\epsilon>0\)，\[\liminf_{n\to\infty}\sum_{n^\epsilon\le d\le n/2}\frac{\mathbf1_{\mathbb P}(n-d)}d\ge1-\epsilon.\]它与两矩给出的 \(\liminf f\le1\) 合并即可推出 \(\liminf f=1\)。相比逐个短区间的 PNT，这一命题只要求对数尺度加权后的总下界，因而是更清晰且可能更弱的下一定理。 |
| 963 | 1636.2 秒 | route_advanced | 优先目标是证明正整数版本 h(N)≥log₂N−O(1)，即把递推中的短区间密度损失从 c/(p log N) 改到 c/p，并控制取整误差；若能进一步把常数压到0，便得到原题。较小而明确的可审目标是把 F(3)=13 的有限核枚举转成可独立检查的证书或 Lean 形式化。 |
| 1063 | 1532.1 秒 | route_advanced | 令 m_k 为最小的 m，使某个 0≤e<k 对 n=mD(k)+e 给出唯一失败项。下一条精确目标是证明 log m_k=o(k)。由于 log D(k)=O((log k)^2)=o(k)，这将推出 n_k=exp(o(k))，从而严格解决 better_upper。第一步应给出所有 sqrt(k)<p≤k 的局部允许剩余类的精确分类，再尝试筛出 m≤exp(o(k))。 |

### 逐题续攻记录

#### #952

- 精确题面：Is there an infinite sequence of distinct Gaussian primes $x_1,x_2,\ldots$ such that\[\lvert x_{n+1}-x_n\rvert \ll 1?\]
- 上轮下一步：固定小整数 C，形式化一个有限“环带证书”：列出一条格点闭曲线，使其 C-邻域内每个 Gaussian 整数都有显式非平凡因子，并用有限图搜索验证该曲线确实分离内外。成功只能排除该 C，但可检验 CRT 屏障路线的可扩展性。
- 用时：868.3 秒（硬上限 7200 秒）
- 路线目标：优先检查“有限 CRT 素数空洞能否升级为全局屏障”。结论是单次平移 CRT 只能严格制造局部空洞，不能控制屏障相对原点的位置。幸存并推进的路线是 Gethner–Stark 型周期筛：用有限环面图及闭路绕数证书排除固定步长的无限分支。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **量词与图论重述**（`advanced`）：构造固定平方步长 D 的局部有限素数图，并应用 König 引理。；推导：有界单射序列全部落在同一无限分支；反之局部有限图的无限分支含一条无重复无限射线。起点在何处不影响原题的存在量词。
  - **复核有限 CRT 空洞**（`advanced`）：对有限 F⊂ℤ[i] 选两两非伴随 Gaussian 素数 π_z，解 w≡−z (mod π_z)。；推导：CRT 给出同余类 w_0+(∏π_z)t。除去有限多个使 w+z 与 π_z 互为伴随的 t 后，每个 w+z 都是非素数。因此任意有限形状（包括圆盘或厚闭曲线）都有一个全合数平移副本。
  - **尝试把 CRT 平移形状变成围原点屏障**（`blocked`）：令 F 为半径 R、厚度大于固定步长的离散环带。；推导：所得屏障围绕 w，而非原点。要分离原点需 |w|<R；CRT 只给 w=w_0+Mt，不给任何 |w|/R 上界。把 t 取得很大反而使屏障远离原点。故“任意大空洞⇒moat”这一步没有成立。
  - **周期筛判据**（`advanced`）：取 B_m={x+iy:gcd(x²+y²,m)=1}，在 (ℤ/mℤ)² 上建立步长平方≤D 的有限商图；沿边记录跨越基本域的 ℤ² 平移势。；推导：若一个商分支出现势不一致，则得到非零绕数闭路，其无限提升含无限路径；若势处处一致，则每个剩余类在一个提升分支中至多出现一次，故该提升分支有限。除有限个整除 m 的 Gaussian 素数外，所有 Gaussian 素数均属于 B_m；加入有限例外仍不能产生无限分支。
  - **m=130、D=2 的精确证书**（`advanced`）：运行纯整数商图与平移势程序。；推导：保留 4608 个剩余类，形成 486 个零绕数商分支，最大提升分支为 580 点。整除 130 的 Gaussian 素数元素共有 20 个，每个至多有8个允许邻点，故任一真实素数分支粗略至多含 20+20·8·580=92820 个顶点。特别地，不存在步长≤√2 的无限序列。
  - **证伪 m=130 向步长2的直接升级**（`refuted`）：把允许差向量扩张到 N(δ)≤4。；推导：商图成为带非零绕数的分支；程序给出从剩余类 (129,64) 经步 (0,2) 到 (129,66) 的势冲突，stored=(-1,-1)、expected=(-1,0)。因此 B_130 的无限提升确有无限路径，m=130 不能证明步长2情形。
  - **小模数替代搜索**（`inconclusive`）：对 m≤870 的28个由小素数组成的候选模数运行 D=4 检查。；推导：全部出现非零绕数；这只否定这些候选，不能排除较大或非方形周期格证书。文献的 D=4 模数为 7113990，远超当前平方枚举。

- 严格推进：
  - 严格复核了有限 CRT 图形定理，并定位其不能闭合原题的精确量词：缺失的是平移中心相对环带内半径的控制。
  - 证明了可独立使用的周期筛有限提升判据；检验条件必须是所有商图闭路的净平移为0，而非仅仅有限环面上的分支有限。
  - 得到可复现的 m=130、N(δ)≤2 证书，并由有限例外论证严格推出 Gaussian 素数图所有分支有限。
  - 给出保守的统一分支大小上界92820，因而该固定步长下任何不同素数序列都在有限步内终止。
  - 严格反驳了同一模数直接处理 N(δ)≤4 的尝试，并记录了显式绕数势冲突。

- 路线证伪/边界检查：
  - 检查严格不等式边界：Lean 的 N(δ)<C 与欧氏距离≤K 可分别取 C=⌊K²⌋+1 或 K=√C 转换。
  - 检查局部有限性：固定 D 的整数差向量只有有限个，故 König 引理适用。
  - 检查 CRT 的非平凡因子条件：逐一排除了 w+z 为 π_z 的四个伴随之一；w+z=0 本身也不是素数。
  - 检查“环面有限”误区：程序显式追踪周期平移势；m=1,D=1 和 m=2,D=2 均正确报告非零绕数。
  - 正控制 m=2,D=1 正确报告所有提升分支有限；m=130,D=2 的输出另以断言复跑。
  - m=130,D=4 的明确绕数见证说明删除点密度很低或环面有限均不足以建立 moat。
  - 没有把撤回的2019证明、仅有摘要的2024声称、增长步长定理或有限计算写成原题完整证明。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/952/periodic_sieve.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/952/periodic_sieve.py)：周期筛有限商图检验器；使用ℤ²平移势检测非零绕数，并报告保留类数、商分支数和最大有限提升分支。SHA-256: d7d301b8e53ded4cbb7637ce4610ead676604797a75cf7a78ecf8bb929ddeae8。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/952 && python3 -m py_compile periodic_sieve.py && python3 periodic_sieve.py --modulus 130 --max-step-squared 2 && python3 periodic_sieve.py --modulus 130 --max-step-squared 4`；结果：D=2：4608个保留类、486个商分支、最大提升分支580、all_lift_components_finite=True。D=4：all_lift_components_finite=False，并输出显式势冲突。

- 第一阻塞点：原题需要对每个有限 D 都排除无限分支。周期筛路线为此需要随 D 构造模数或周期理想 m_D，使 B_{m_D} 的商图没有任何非零绕数。加入新素因子只会删点，因而不会重新产生无限分支，但目前没有定理保证有限多个新因子能击中全部绕行通道。CRT 局部空洞也不给出这种全局、周期一致的击中性质。
- 下一精确定理：最清晰的下一有限定理是独立机核 Gethner–Stark 第2节的 D=4 实例：对 m=7113990，证明 B_m 在差向量平方模≤4的图中无非零绕数闭路。由于 m² 枚举不可行，需要按 m=2·3·5·13·17·29·37 的 CRT 分解构造压缩商图/可检查证书；这将验证周期筛路线确实可从√2推进到2，并给一般 D 的算法接口。
- 研究记录：

记 N(a+bi)=a²+b²。对整数 D≥1，令 G_D(P) 是顶点集 P⊂ℤ[i] 上的图，边条件为 0<N(u−v)≤D。原题为“是否存在 D，使 G_D(𝔓[i]) 有无限分支”。

有限 CRT 结论如下。给定有限 F⊂ℤ[i]，选两两非伴随素元 {π_z:z∈F}。因理想 (π_z) 两两互素，存在 w_0 满足 w_0≡−z mod π_z。令 M=∏_{z∈F}π_z，则 w=w_0+Mt 时 π_z∣w+z。对每个 z，只有至多四个 w 会使 w+z成为π_z的伴随；从无限多个 t 中避开这些有限例外，即得 w+F 全无素数。取 F 为离散圆盘或环带便得任意大的平移空洞/平移闭曲线。但其中心是 w；要围住原点还须 |w| 小于环带内半径，这不是 CRT 的结论。因此这条路线的局部部分成立，全局升级不成立。

周期筛修复了“只局部”的缺陷。令 B_m={z:gcd(N(z),m)=1}。它是 mℤ[i]-周期集。把 G_D(B_m) 商到 T_m=(ℤ/mℤ)²。商边 r→s 除了端点，还带平移标签 q∈ℤ²，使得从代表 r 加差向量后等于 s+mq。沿一棵生成树赋势 h(s)=h(r)+q。若某条非树边要求的势与既有势不同，所得闭路净平移非零；重复该闭路便在无限提升中得到无限路径。反之若所有要求一致，则任一提升分支中，商顶点 s 的格坐标被唯一确定，所以该提升分支的顶点数不超过相应商分支大小。

对 m=130、D=2，程序穷尽全部4608个 B_m 剩余类，所有闭路净平移均为0，最大商分支580。若 Gaussian 素数 π 不在 B_m，则某个 p∣130 除 N(π)，从而 π 是130的 Gaussian 素因子或其伴随；这样的素数点只有20个。加入这20个点，每点至多通过8个差向量邻接 B_m，故每个真实素数分支至多合并160个 B_m 分支，得到粗界 20+160·580=92820。因此 D=2 情形已严格闭合。

当 D=4 时，同一模数出现非零净平移，故无限提升有无限通道；这不是 Gaussian 素数路径的反例，因为 B_130 只是素数的稀疏筛上集，却严格反驳了“m=130 自动升级”的路线。一般 D 尚缺构造 m_D 的定理，故不能声称解决原题。

- 一手来源：

  - [Erdős Problems #952](https://www.erdosproblems.com/952)；一手来源：`true`；核验：页面于 2026-04-08 编辑，仍明确标为 OPEN；精确题面是任意起点的无限不同 Gaussian 素数序列。
  - [FormalConjectures/ErdosProblems/952.lean](https://github.com/google-deepmind/formal-conjectures/blob/9e126a6e1f7d108ced5904c43cac46b1c39b39cb/FormalConjectures/ErdosProblems/952.lean)；一手来源：`true`；核验：形式化命题为 ∃x,C，x 单射且 ∀n Prime(x n)∧N(x(n+1)-x n)<C；量词与原题一致到常数重参数化。
  - [Periodic Gaussian Moats, Gethner–Stark, Experimental Mathematics 6 (1997), 289–292](https://doi.org/10.1080/10586458.1997.10504616)；一手来源：`true`；核验：正文第2节给出未编号的周期性构造：对 k=√2 使用周期格 65+65i，并对 k=2 使用模数 7113990，证明其统一有限步数猜想在这两个 k 上成立。
  - [A Stroll Through the Gaussian Primes, Gethner–Wagon–Wick](https://doi.org/10.2307/2589708)；一手来源：`true`；核验：Theorem 4.1：对含至少两个 Gaussian 整点的任意直线 L 及正整数 k，L 上存在 w，使距 w 不超过 k 的所有 Gaussian 整数均为合数；正文同时明确指出任意大空圆盘不足以阻止路径绕行。
  - [A Note on The Gaussian Moat Problem, Madhuparna Das](https://arxiv.org/abs/1908.10392)；一手来源：`true`；核验：作者已撤回论文；arXiv v2 的 Comments 精确说明 Theorem 3 错误：所定义 P_i 不覆盖全部 Gaussian 素数、还包含非素数，且误差项不足。
  - [On the Gaussian Moat Problem, Johann C. Stumpenhusen](https://arxiv.org/abs/2401.08441)；一手来源：`true`；核验：v1 摘要声称完全否定原题，但本轮未能从一手页面取得可核查的正文定理编号和证明；官方题页在其后仍标 open，故不把摘要当作已验证定理。
  - [On the Gaussian moat problem, Maynard–Merikoski, Oberwolfach Report 50/2022](https://ems.press/content/serial-article-files/46986)；一手来源：`true`；核验：报告第45–47页 Theorem 1 处理增长步长指数 θ，给出 θ≤1/2−1/100，GRH 下 θ≤1/3+o(1)；这不是固定绝对步长结论。Theorem 3 是稀疏圆盘族中几乎所有圆盘含素数的估计。

#### #1083

- 精确题面：Let $d\geq 3$, and let $f_d(n)$ be the minimal $m$ such that every set of $n$ points in $\mathbb{R}^d$ determines at least $m$ distinct distances. Estimate $f_d(n)$ - in particular, is it true that\[f_d(n)=n^{\frac{2}{d}-o(1)}?\]
- 上轮下一步：对距离按 M_t≤n^{2−η} 与 M_t>n^{2−η} 截断：低重数部分用能量估计，高重数部分尝试证明点集集中在少数正交球面或低维代数簇上，再归约到较低维 distinct-distance 问题。先在 d=4 的两圆 Lenz 模型上验证该分解能恢复 Ω(n^{1/2}) 个距离。
- 用时：628.8 秒（硬上限 7200 秒）
- 路线目标：审计“按距离重数截断；低重数部分用能量，高重数部分迫使 Lenz/低维结构并递归”的路线。低重数分支可以严格闭合；但朴素的全局结构逆命题被反例否定，现有递推即使输入最优低维指数仍有固定幂损失。
- 结论：`route_blocked`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **无权距离能量**（`refuted`）：令 M_r 为距离 r 的无序点对重数，N=binom(n,2)，Q=Σ_r M_r²；Cauchy–Schwarz 给 |Δ(P)|≥N²/Q。；推导：在 R^4 的两个正交等半径圆上各放 n/2 点，跨圆距离相同，故某个 M_r=n²/4，进而 Q≥n⁴/16。任何普适的 Q≤n^{4−2/d+o(1)} 都为假。
  - **截断后的低重数分支**（`advanced`）：对阈值 T，记 L_T=Σ_{M_r≤T}M_r。；推导：低重数距离类数至少 L_T/T。若 L_T≥N/2，则 |Δ(P)|≥L_T/T≫n²/T。取 T=n^{2−2/d+ε_n}、ε_n→0，即得 |Δ(P)|≥n^{2/d−ε_n}。因此此分支已经完整闭合。
  - **高重数推出全局集中**（`refuted`）：尝试证明存在 M_r>n^{2−η} 会迫使几乎全部点落在少数正交圆、球面或低维簇上。；推导：取 q=ceil(n^{1−η/2})+1，在 R^4 两个正交圆上各放 q 点，则跨圆距离重数 q²>n^{2−η}，但 2q=o(n)。再加入 n−2q 个代数一般位置点，并避开该距离。可使任意固定数目、固定次数的真代数簇只覆盖 O(1) 个一般位置点。因此高重数距离可完全由 o(n) 点支持，不能推出整个点集集中。
  - **在真正 Lenz 模型上剥离高重数距离**（`advanced`）：在两个正交半径 1/√2 的圆上各取正 m 边形。；推导：跨圆距离为1，重数 m²；每个内部弦步通常在两圆合计重数2m，直径步重数m。总距离数为 floor(m/2)+1；若4|m，跨圆距离与第 m/4 弦步重合，故为 floor(m/2)。以 T=(2m)^{3/2} 截断时，唯一高类被剥去，仍留下 Θ(m)=Θ(n) 个低类，强于四维目标 n^{1/2−o(1)}。
  - **把最优低维指数代入现有递推**（`blocked`）：在 Solymosi–Vu Corollary 2.6 中假设 α_{d−2}=2/(d−2)。；推导：所得 α_d=((d+1)α)/(2dα+d−1)=2(d+1)/(d²+d+2)=2/d−4/[d(d²+d+2)]。固定 d 时缺口为正常数，不能并入 o(1)。特别地 d=4 即使使用 Guth–Katz 的 α_2=1−o(1)，也只得到 5/11−o(1)，不是 1/2−o(1)。
  - **三维多重颜色关联界**（`inconclusive`）：将全部 D 个实际距离代入 Basit–Sheffer Theorem 1.3。；推导：n²≪n^{236/149+ε}D^{125/149} 仅给 D≫n^{62/125−o(1)}，甚至弱于当前 3/5；现有多颜色关联定理不足以处理高重数并集。

- 严格推进：
  - 对任意 P 和 T，已严格得到二分：若低重数类承载至少一半点对，则目标下界立即成立；否则高重数类的并集承载超过一半点对。这精确隔离了路线唯一未解分支。
  - 朴素命题“一个次二次高重数距离使整个点集接近 Lenz 配置”已被严格反驳；任何可用逆定理必须是边支持局部化的，并允许递归处理剩余点。
  - 四维两圆 Lenz 模型经截断后实际留下 Θ(n) 个距离，而不是仅 Ω(n^{1/2})；因此 Lenz 极值单色块本身不是阻碍。
  - 对 k^d 格点，距离数至多 d(k−1)²，而点对数为 Θ(k^{2d})，故某个距离重数至少 c_d k^{2d−2}=c_d n^{2−2/d}。这证明截断阈值 n^{2−2/d} 是天然临界尺度。
  - 现有余维2递推的损失已精确定位为非集中项的 n 指数少了 1/d²；这给出了可检验的下一定理。

- 路线证伪/边界检查：
  - 任意 n 的格点上界无量词漏洞：取 k=ceil(n^{1/d})，从 {0,…,k−1}^d 任取 n 点，其平方距离属于 {1,…,d(k−1)²}，故 f_d(n)=O_d(n^{2/d})。
  - 能量计数全部使用无序点对；Σ_r M_r=binom(n,2)，没有有序/无序的二倍误差。
  - 一般位置补点反例适用于每个固定 η>0 和所有充分大 n，并可嵌入任意 d≥4；它只反驳全局集中结论，不反驳更精细的局部支持分解。
  - Swanepoel 的稳定性假设处于 Θ(n²) 极值尺度，不能被误用到单类仅有 n^{2−2/d+o(1)} 条边的情形。
  - 候选强化在格点上指数取等：格点的余维2最大交数 m=k^{d−2}=n^{(d−2)/d}，代入候选式恰得 n^{2/d}，因此未被标准上界构造立即否定。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/1083/distance_multiplicity_audit.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/1083/distance_multiplicity_audit.py)：精确枚举 k^d 整数格的平方距离重数；同时用纯组合公式计算四维两正多边形 Lenz 模型，无浮点距离判等。脚本内验证所有重数之和等于 binom(n,2)。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/1083 && python3 -m py_compile distance_multiplicity_audit.py && python3 distance_multiplicity_audit.py --grid 4 11 --lenz 1000`；结果：4D 11^4 格点：n=14641，D=307，max M=1636800，n^{3/2}=1771561；Lenz m=1000：n=2000，D=500，唯一高类含1002000对，剥离后499个低类仍含997000对。

- 第一阻塞点：高重数颜色承载多数点对时，缺少一个对其并集进行局部支持分解并收费的定理。单色近极值稳定性太强、适用尺度太高；Solymosi–Vu 的现有余维递推又固有地损失固定幂。
- 下一精确定理：建议下一节点是如下“锐余维2非集中界”。固定 d≥3，P⊂R^d、|P|=n，令 m=max_H|P∩H|，其中 H 遍历余维2仿射平面。证明 |Δ(P)| ≥ n^{-o_d(1)} n^{(d²+d+2)/(2d²)} m^{-(d−1)/(2d)}. 另一方面平凡地有 |Δ(P)|≥f_{d−2}(m)。若归纳输入 f_{d−2}(m)≥m^{2/(d−2)-o(1)}，令 m=n^x，则两个指数分别为 A−bx 与 2x/(d−2)；最坏平衡点是 x=(d−2)/d，二者都恰等于2/d。该命题比 Solymosi–Vu Theorem 2.2 的 n 指数 (d+1)/(2d) 恰强 1/d²，并在格点上指数锐利。
- 研究记录：

记 D=|Δ(P)|、N=binom(n,2)，并按距离 r 定义无序重数 M_r。基本恒等式为 Σ_rM_r=N，距离能量为 Q=Σ_rM_r²，故 D≥N²/Q。两正交圆给 M_1=Θ(n²)，说明总能量路线不可用。

截断则保留了有效内容。令 T=n^{2−2/d+ε_n}，其中 ε_n→0，并令 L_T=Σ_{M_r≤T}M_r。若 L_T≥N/2，则低类数至少 L_T/T≫n^{2/d−ε_n}，目标完成。因此未解情形可严格限定为 Σ_{M_r>T}M_r>N/2。注意这涉及多个距离图的并集，不能由单个单位距离图的极值稳定性替代。

全局逆命题确实为假。给定 η>0，令 q=ceil(n^{1−η/2})+1，在两个正交圆上各取 q 点；同一跨圆距离出现 q²>n^{2−η} 次，而这部分只有2q=o(n)个点。其余点可逐点选择在有限个真代数禁集之外，使其不产生该距离并处于代数一般位置。于是任何固定数量、固定次数的真低维代数簇至多覆盖全部2q个结构点及 O(1) 个一般位置点，远非 n−o(n)。故正确逆定理必须先找出承载高重数边的局部块，而不能宣称整个 P 集中。

在标准四维 Lenz 块中，该局部化是有收益的。两个半径1/√2的正 m 边形之间所有 m² 条跨边长度为1；圆内弦长只依赖步数 j。除直径外，每个步数在两圆共出现2m次，故剥去跨圆高类后仍有 floor(m/2)−O(1) 个距离。计算脚本的 m=1000 例精确得到499个剩余低类。因此 Lenz 块不是反例，真正困难是证明任意多数高边都能作类似分解且递归成本可控。

最后核对现有递推的极限。Solymosi–Vu Theorem 2.2 把低维指数 α 变为 α_d=(d+1)α/(2dα+d−1)。即使假设 α=2/(d−2)，仍只有
α_d=2(d+1)/(d²+d+2)=2/d−4/[d(d²+d+2)].
这个固定正差不能被写成 o(1)。要使平衡无损，非集中项 n^A/m^{(d−1)/(2d)} 必须具有 A=(d²+d+2)/(2d²)，比现有 A_0=(d+1)/(2d) 正好多1/d²。由此得到 next_theorem_zh 中的精确下一定理；本轮没有证明它，也没有得到完整解或反例。

- 一手来源：

  - [Erdős Problem #1083](https://www.erdosproblems.com/1083)；一手来源：`true`；核验：精确题面仍标为 OPEN；页面记录 f_3(n)≫n^{3/5} 及 d≥4 的 Solymosi–Vu 型固定指数缺口。页面最后编辑于 2025-10-16。
  - [Near optimal bounds for the Erdős distinct distances problem in high dimensions](https://www.math.ubc.ca/~solymosi/sajatcikkek/distancesvu.pdf)；一手来源：`true`；核验：Theorem 2.1：若 m 是余维1超平面最大交数，则 t(P)=Ω(max{n/m^{(d−1)/d},t_{d−1}(m)})。Theorem 2.2：若 m 是余维2超平面最大交数，则 t(P)=Ω(max{n^{(d+1)/(2d)}/m^{(d−1)/(2d)},t_{d−2}(m)})。Corollary 2.3、2.6 给出相应指数递推。
  - [On the Erdős distinct distance problem in the plane](https://arxiv.org/abs/1011.4105)；一手来源：`true`；核验：Guth–Katz Theorem 1.1：任意 N 个平面点确定 Ω(N/log N) 个距离，即二维输入指数为 1−o(1)。
  - [Distinct Distances in Three and Higher Dimensions](https://www.cs.umd.edu/~gasarch/TOPICS/erdos_dist/APST.pdf)；一手来源：`true`；核验：Theorem 1.1 给三维指数 77/141−o(1)，Corollary 1.3 给高维推广；论文第1节明确展示 d≥4 两个正交圆产生 n²/4 个相同距离，故单距离最大重数法失效。
  - [Favourite distances in high dimensions](https://arxiv.org/abs/1108.4817)；一手来源：`true`；核验：其稳定性结论要求 favourite-distance 边数达到极值减 o(n²)，才能删去 o(n) 点后得到 Lenz 配置；这不覆盖 n^{2−2/d+o(1)} 的次二次单色阈值。
  - [Incidences with k-non-degenerate sets and their applications](https://jocg.org/index.php/jocg/article/download/2936/2630)；一手来源：`true`；核验：Basit–Sheffer Theorem 1.3 对三维 k 个指定距离给 F_k(n)=O(n^{236/149+ε}k^{125/149})。令这些距离覆盖全部点对只能推出 D≥n^{62/125−o(1)}，弱于已知 3/5。

#### #1039

- 精确题面：Let $f(z)=\prod_{i=1}^n(z-z_i)\in \mathbb{C}[z]$ with $\lvert z_i\rvert \leq 1$ for all $i$. Let $\rho(f)$ be the radius of the largest disc which is contained in $\{z: \lvert f(z)\rvert< 1\}$. Determine the behaviour of $\rho(f)$. In particular, is it always true that $\rho(f)\gg 1/n$?
- 上轮下一步：逐行重建并形式核验引理：若 $|z_i|\le1$ 且 $|w_i-z_i|\le\varepsilon$，则 $\prod_i\prod_j|w_i-z_j|\le((1+\varepsilon)^n-1)^n$；重点检查重根、$\varepsilon=0$、严格/非严格边界及 Hadamard/Vandermonde 步骤。
- 用时：670.2 秒（硬上限 7200 秒）
- 路线目标：先检验旧分析所需的精确结式界；未找到反例但也未独立证明该精确形式。随后以 Ptolemy 配对、二次分离积和 Blaschke–Szegő 不等式建立足够强的替代乘积界，闭合 1/n 下界。
- 结论：`candidate_full_proof`；完整解声明：`machine_checked_exact_scope_closure_evidence`；置信度：`high`
- 实际尝试：

- 独立机器核验：`machine_checked_exact_scope_closure_evidence`；提交 `9ae46727eef654665a51e8341961feb0127a2a44`；`lake exe cache get && lake build` 退出码 0，共 3316 个构建任务。
- 机器核验范围：最终 theorem1039 对所有 n>0、所有零点位于闭单位圆盘的首一 n 次多项式，证明 rho(f)>=log(2)/n；并以 n 次单位根多项式给出 rho(f)<=pi/(2n) 的见证。它严格回答官网的特别问题 rho(f) >> 1/n，并确定最坏情形 inf rho(f)=Theta(1/n)，但不确定精确渐近常数。
- 独立数学复核：PASS。已逐式复核 Ptolemy 配对及无序对计数、Blaschke 离对角积的逐坐标最大模步骤、Szego 核 Cauchy-Schwarz 导数式、Q_sigma 双曲正弦变换、epsilon=c/n 的全部指数与常数、开球反证及 sSup 过渡，并独立核对 z^n-1 的 O(1/n) 上界；未发现量词或不等式方向漏洞。
- 机器证据层级：公开 Lean 代码已在本地从固定提交全量复现，且无占位或自定义公理；这是强机器检查证据。仓库基于论坛中的 AI 辅助自然语言证明，目前不是同行评审论文或登记预印本，官网仍标 OPEN，故数据库状态是否更新仍需维护者判断。

  - **精确乘积界的数值证伪**（`advanced`）：连续优化 ∏_{i,j}|w_i-z_j|/((1+ε)^n−1)^n；利用旋转不变性固定一个根的辐角，并将每个扰动置于 |w_i-z_i|=ε 的边界。；推导：对 n=2,…,5 和 ε∈{0.05,0.1,0.2,0.3} 等运行 differential_evolution。所有最大值均在数值误差内等于1，优化器恢复 z_i 为 n 次单位根、w_i=(1+ε)z_i。
  - **逐因子粗估**（`blocked`）：分别估计 |w_i-z_j|≤|z_i-z_j|+ε≤2+ε。；推导：只得到 ε^n(2+ε)^{n(n−1)}，无法在 ε=c/n 时小于1。
  - **旧路线的精确结式不等式**（`inconclusive`）：尝试由 resultant、Vandermonde/Hadamard 或商代数算子范数直接证明 ∏_{i,j}|w_i-z_j|≤((1+ε)^n−1)^n。；推导：确认左端是 |Res(f,g)|，且单位根径向外移给等号；但未闭合一般配置的精确上界。最终证明不依赖此未证引理。
  - **Ptolemy—Blaschke 替代路线**（`advanced`）：把每个无序指标对的两个交叉因子配对，再以二次分离积 Q_σ(x)=∏_{i<j}(|x_i-x_j|²+σ²) 控制。；推导：Ptolemy 及 Cauchy 型恒等式给 (∏_j|f(w_j)|)^2≤ε^{2n}Q_σ(z)Q_σ(w)。随后证明 Q_σ 的双曲正弦上界，并在 ε=σ=c/n 时得到 ∏_j|f(w_j)|≤(e^c−1)^n<1。
  - **最坏情形上界**（`advanced`）：独立检查 f_n(z)=z^n−1 的花瓣几何。；推导：由 |z^n−1|<1 等价于 r^n<2cos(nθ)，每个连通分支位于角宽 π/n、半径小于2^{1/n}的扇形。因此任一内含圆盘半径至多 2^{1/n}sin(π/(2n))≤π/n，足以给出 O(1/n)。

- 严格推进：
  - Blaschke 离对角积引理：若 0≤a<1、|x_i|≤1，则 ∏_{i≠j}|1−a x_i overline{x_j}|≤((1−a^n)/(1−a))^n。证明先逐坐标用最大模原理化到 |x_i|=1，再用有限 Blaschke 乘积和 Hardy H² 的 Szegő 核不等式。
  - 二次分离积引理：若 |x_i|≤A、A,σ>0，α=arsinh(σ/(2A))，则 Q_σ(x)≤A^{n(n−1)}(sinh(nα)/sinh α)^n。
  - 扰动乘积引理：若 |w_i−z_i|≤ε≤σ，则 (∏_j|f(w_j)|)^2≤ε^{2n}Q_σ(z)Q_σ(w)。
  - 取 ε=σ=c/n、0<c<log2 后，|z_i|≤1、|w_i|≤1+ε，并有 ∏_j|f(w_j)|≤(e^c−1)^n<1。
  - 反设每个 B(z_j,c/n) 都不包含于 Ω_f，可逐个选 w_j∈B(z_j,c/n)且 |f(w_j)|≥1，遂有乘积至少1，矛盾。因此对每个 c<log2 至少一个零点中心圆盘完全包含于 Ω_f。
  - 令 c↑log2，按内半径的上确界定义得到 ρ(f)≥(log2)/n。结合 z^n−1 的 O(1/n) 上界，得到 inf_{deg f=n}ρ(f)=Θ(1/n)。

- 路线证伪/边界检查：
  - n=1 时 Q_σ 是空积，全部引理退化为 |w_1−z_1|≤ε，结论正确。
  - 证明不除以 Vandermonde 或 f'(z_i)，故允许任意重根。
  - 最终取 c>0，避免 ε=0 时双曲表达式的可去奇点；ε=0 的原始乘积界本身平凡。
  - 未包含关系针对开圆盘：若包含失败，确有 w_j 在开球内且不属于 Ω_f；不属于 {|f|<1} 精确等价于 |f(w_j)|≥1。
  - 只证明所有 c<log2 的圆盘存在；ρ≥log2/n 是由半径上确界推出，没有错误地声称半径 log2/n 的同一开圆盘必然取得。
  - 数值搜索仅用于尝试证伪精确结式界，没有被用作证明。
  - Lean 仓库已从固定提交在本地全量编译；六个最终声明的 #print axioms 仅含 Lean/Mathlib 的标准逻辑公理 propext、Classical.choice、Quot.sound。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/1039/falsify_product_bound.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/1039/falsify_product_bound.py)：对旧路线精确乘积不等式进行连续全局优化的反例搜索器，输出最优比值及根、扰动点配置。；命令 `for x in '2 .05' '2 .3' '3 .05' '3 .2' '4 .1' '4 .3' '5 .1'; do set -- $x; python falsify_product_bound.py --n "$1" --eps "$2" --maxiter 500 --popsize 12; done`；结果：所有测试的最大 LHS/RHS≈1，偏差约10^{-15}至10^{-9}；等号候选均为单位根配置及径向外移。未发现反例。

- 第一阻塞点：官网特别问题及最坏情形的 1/n 阶已被自然语言论证和本地可复现 Lean 证书闭合。仍未闭合的是旧分析中更强、更简洁的精确结式界 ∏_{i,j}|w_i-z_j|≤((1+ε)^n−1)^n，以及最坏内半径的精确渐近常数；另外公开成果目前只有论坛证明与代码，没有同行评审论文或登记预印本。
- 下一精确定理：下一步最清晰的独立定理是证明或反驳精确配对结式界，并刻画其等号情形；更深入的原问题则是确定 liminf_n n·inf_{deg f=n}ρ(f) 的精确常数，当前证明只给 log2≤nρ_n≤π（原始论文给更好的上侧常数 π/2）。
- 研究记录：

记 P=∏_{j=1}^n|f(w_j)|，Q_σ(x)=∏_{i<j}(|x_i−x_j|²+σ²)。先证明配对估计。对 i<j，Ptolemy 不等式给
|w_i−z_j||w_j−z_i|≤|z_i−z_j||w_i−w_j|+|w_i−z_i||w_j−z_j|。
若 |w_k−z_k|≤ε≤σ，令 X=|z_i−z_j|、Y=|w_i−w_j|，则右端不超过 XY+σ²，而
(X²+σ²)(Y²+σ²)−(XY+σ²)²=σ²(X−Y)²≥0。
把所有无序对相乘，并把 n 个对角因子 |w_j−z_j|≤ε 分离，得到
P²≤ε^{2n}Q_σ(z)Q_σ(w).  (1)

下面估计 Q。先证：0≤a<1、|x_i|≤1 时
∏_{i≠j}|1−a x_i overline{x_j}|≤((1−a^n)/(1−a))^n.  (2)
固定除 x_k 外的坐标，所有含 k 的因子恰为 |∏_{j≠k}(1−a x_k overline{x_j})|²，故最大模原理允许逐坐标把最大值推到单位圆。于是设 x_i=ω_i、|ω_i|=1。令
G(a)=n log(1−a^n)−∑_{i,j}log|1−aω_i overline{ω_j}|。
取 u_i=√a·ω_i，有限 Blaschke 乘积 B(t)=∏(t−u_i)/(1−overline{u_i}t)，Λ=B(0)。函数 H=1−overline{Λ}B 满足 H(u_i)=1 且 ||H||_{H²}²=1−|Λ|²=1−a^n。对 Szegő 核应用 Cauchy–Schwarz，
∑_{i,j}Re[1/(1−u_i overline{u_j})]=||∑_i k_{u_i}||²≥n²/(1−a^n).
直接微分得到
aG'(a)=∑_{i,j}Re[1/(1−aω_i overline{ω_j})]−n²/(1−a^n)≥0。
因 G(0)=0，得到全积不超过 (1−a^n)^n；除去 n 个对角因子 (1−a)^n 即得 (2)。重复点不会影响此论证。

现设 |x_i|≤A，α=arsinh(σ/(2A))，λ=e^α，a=λ^{-2}，y_i=x_i/A。则 σ=A(λ−λ^{-1})，且逐对有
|x_i−x_j|²+σ²≤A²λ²|1−a y_i overline{y_j}|²。
归一化后的差值为
2−λ^{-2}−|y_i|²−|y_j|²+λ^{-2}|y_i|²|y_j|²
=(1−|y_i|²)(1−λ^{-2}|y_j|²)+(1−|y_j|²)(1−λ^{-2})≥0。
结合 (2) 并化简 λ 的幂，得到
Q_σ(x)≤A^{n(n−1)}[sinh(nα)/sinh α]^n.  (3)

取 ε=σ=c/n，其中 0<c<log2。对 A≥1，α_A=arsinh(c/(2nA)) 满足 sinh α_A=c/(2nA) 及 nα_A≤c/(2A)≤c/2。因此
Q_ε(x)≤A^{n(n−1)}[(2nA/c)sinh(c/2)]^n.  (4)
在 (1) 中分别对 z 使用 A=1，对 w 使用 |w_i|≤1+ε。代入 (4) 后
P²≤[2sinh(c/2)]^{2n}(1+c/n)^{n²}
≤[2e^{c/2}sinh(c/2)]^{2n}=(e^c−1)^{2n}<1.  (5)
若没有任何 B(z_j,c/n) 包含于 Ω_f，则可选 w_j∈B(z_j,c/n)\Ω_f，故每个 |f(w_j)|≥1，与 (5) 矛盾。于是对每个 c<log2 都存在所需圆盘，进而 ρ(f)≥(log2)/n。

最后，f_n(z)=z^n−1 时，写 z=re^{iθ}，有 |z^n−1|<1 当且仅当 r^n<2cos(nθ)。每个分支位于角宽 π/n、半径小于2^{1/n}的扇形。任何内含圆盘均位于一个分支，其半径至多 2^{1/n}sin(π/(2n))≤π/n。因此最坏内半径同时为 Ω(1/n) 和 O(1/n)。

- 一手来源：

  - [P. Erdős, F. Herzog, G. Piranian, Metric properties of polynomials](https://www.renyi.hu/~p_erdos/1958-05.pdf)；一手来源：`true`；核验：原文第134页 Problem 3：定义所有零点在闭单位圆盘时必含圆盘的最小半径 ρ_n，询问其渐近行为及是否 ρ_n>c/n；同页指出 z^n−1 限制常数不超过 π/2。
  - [M. Krishnapur, E. Lundberg, K. Ramachandran, On the area of polynomial lemniscates](https://arxiv.org/abs/2503.18270)；一手来源：`true`；核验：Theorem 8 精确给出 ρ_n≥c/(n√log n)；Lemma 9 给出一般面积—内半径估计 ρ(Λ_p(t))≥[72π√π]^{-1}√m(Λ_p(t))/n。
  - [KitaKen1/erdos1039-lean](https://github.com/KitaKen1/erdos1039-lean)；一手来源：`true`；核验：Erdos1039.lean 中 theorem erdos1039 陈述：n>0、|z_i|≤1、0<c<log 2 时，存在 j 使 ball(z_j,c/n)⊆{|f|<1}；最终 theorem1039 还证明任意中心内半径 rho(f)>=log(2)/n，并以单位根给出 rho(f)<=pi/(2n) 的见证。本轮在固定提交 9ae4672、Lean/mathlib 4.29.1 下全量 lake build 成功（3316 jobs）；静态扫描无 sorry、admit、自定义 axiom 或 unsafe，#print axioms 仅列 propext、Classical.choice、Quot.sound。
  - [Erdős Problems #1039 discussion thread](https://www.erdosproblems.com/forum/thread/1039)；一手来源：`true`；核验：Liam Price 于 2026-05-07 发布同一路线的 AI 辅助证明；Nat Sothanaphan 于 2026-05-08 表示已消化并确认论证，明确结论为每个 f 都有零点中心半径至少 log(2)/n 的圆盘；Kenta Kitamura 于 2026-05-15 发布 Lean 仓库，随后又获正确性确认。官网主体最后编辑于 2025-12-27，早于这些材料，故 OPEN 标签尚未纳入该证据。论坛确认不是同行评审，但与本轮独立构建相互佐证。
  - [C. Pommerenke, On metric properties of complex polynomials](https://doi.org/10.1307/mmj/1028998561)；一手来源：`true`；核验：核到 Michigan Math. J. 8 (1961), 97–115 及 DOI；本次未取得足以逐页核对的正文，因此没有擅自给出其内部定理编号。KLR 正文将其旧内半径界表述为 n^{-2} 量级。

#### #25

- 精确题面：Let $n_1<n_2<\cdots$ be an arbitrary sequence of integers, each with an associated residue class $a_i\pmod{n_i}$. Let $A$ be the set of integers $n$ such that for every $i$ either $n<n_i$ or $n\not\equiv a_i\pmod{n_i}$. Must the logarithmic density of $A$ exist?
- 上轮下一步：按模数分 dyadic 块 $2^j<n_i\le2^{j+1}$，检验能否利用“每个模数至多一个剩余类”和模数互异性，证明尾块并集的调和质量严格优于粗糙和 $\sum1/n_i$；首先计算两剩余类交集为空或密度为 $1/\operatorname{lcm}(n_i,n_j)$，再做二阶 Bonferroni 下的最坏重叠优化。
- 用时：827.0 秒（硬上限 7200 秒）
- 路线目标：检验能否按 dyadic 模数块，利用互异模数和二阶交叠把激活尾部的调和质量压到零；若失败，定位所需的跨尺度替代定理。
- 结论：`route_refuted`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **有限周期上夹逼**（`advanced`）：令 B_K 避开前 K 个完整剩余类，记周期密度为 d_K。；推导：对 n≥n_K 有 A⊆B_K，故上对数密度满足 δ̄_log(A)≤d_K。因 d_K 单调下降，得到 δ̄_log(A)≤d_*:=inf_K d_K。一般问题只剩证明下界 δ̲_log(A)≥d_*。
  - **逐 dyadic 块局部—周期比较**（`refuted`）：试图用完整算术级数并集的密度控制阈值附近的激活删除。；推导：取所有 q∈[N,2N]，令 a_q=0。每个 n∈[N,2N] 被 q=n 命中，所以激活删除覆盖整个区间；但完整周期并集是具有除数 q∈[N,2N] 的整数集，其密度由 Erdős 1936 定理趋于 0。因此不存在绝对常数 C，使单块激活损失≤C×完整周期密度。
  - **对所有剩余类的 dyadic 并集 o(1) 界**（`refuted`）：随机独立选择 a_q (mod q) 检验最坏配置。；推导：对周期中固定整数，避开全部类的概率为 ∏_{q=N}^{2N}(1-1/q)=(N-1)/(2N)。故存在剩余配置使完整周期并集密度至少 (N+1)/(2N)→1/2；统一 o(1) 上界为假。
  - **二阶 Bonferroni 优化**（`blocked`）：计算两剩余类交集并检查能否强迫大量交叠。；推导：对模数 m,n，交集为空当且仅当 gcd(m,n)∤(a_m-a_n)；否则密度为 1/lcm(m,n)=gcd(m,n)/(mn)。兼容性可由剩余选择破坏，二阶式主要给并集下界，不能提供所需的统一尾部上界。
  - **可和特例加强**（`advanced`）：直接计数激活算术级数，并与 Araujo 定理 3.26 核对。；推导：取规范剩余 0≤r_i<n_i。激活类 C_i 在 [1,x] 中至多有 x/n_i 个点，故 |⋃_{i>K}C_i∩[1,x]|/x≤Σ_{i>K}1/n_i。若 Σ_i1/n_i<∞，有限周期逼近一致收敛，因此 A 实际具有自然密度。
  - **固定非负剩余代表特例**（`advanced`）：平移后化为倍数集。；推导：若存在固定 c≥0，使所有 a_i≡c (mod n_i)，则对 n>c，n≥n_i 且 n≡c (mod n_i) 等价于 n_i|(n-c)。排除集最终为 Davenport–Erdős 倍数集的平移 c+M；平移改变调和和至多 O(1)，故 A 的对数密度存在。

- 严格推进：
  - 严格得到一般上界 δ̄_log(A)≤d_*，从而精确定位只缺下界。
  - 证明 Σ_i1/n_i<∞ 时不仅有对数密度，而且有自然密度；这与 Araujo 2026 定理 3.26 的单剩余类情形一致。
  - 证明所有剩余类均由同一个固定非负整数 c 表示时，对数密度存在，推广了 c=0 的倍数集特例。
  - 严格否定任何仅靠单个 dyadic 块完整周期密度控制激活局部损失的路线。

- 路线证伪/边界检查：
  - 零剩余块 q∈[N,2N] 同时给出局部激活覆盖率 1 和趋零的长期周期成本，是初始路线的决定性边界反例。
  - 随机剩余平均证明存在完整周期并集密度约 1/2 的配置，排除了相反方向的统一 o(1) 猜想。
  - 固定平移证明限制为 c≥0；若 c<0，则 n_i|(n-c) 不再保证 n≥n_i，首个平移倍数形成的无限边界不能忽略。
  - 计算脚本中的坐标上升只用于寻找压力测试配置，不宣称全局最优或构成一般反例。
  - 定向检索未找到解决一般发散情形的一手论文；不能据此断言文献绝对不存在。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/25/dyadic_block_probe.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/25/dyadic_block_probe.py)：按 lcm 周期精确计算有限 dyadic 块并集密度，验证零剩余激活对角全覆盖，并以坐标上升搜索大并集剩余配置。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/25 && python3 dyadic_block_probe.py --max-n 7 --restarts 3 --sweeps 3`；结果：程序通过 py_compile。N=2,…,7 时，零剩余完整周期并集密度约为 0.667,0.600,0.543,0.524,0.498,0.504，而 [N,2N] 的激活删除率均为 1；搜索到的完整并集密度约为 0.833,0.733,0.686,0.638,0.641,0.607。

- 第一阻塞点：完整周期交叠描述长期密度，却看不到 n≈n_i 处的“对角命中”。一般 Σ_i1/n_i=∞ 时，单块激活损失可为 1，且不能由该块造成的有限筛密度下降控制；尚缺允许坏块、但能跨尺度摊销的估计。
- 下一精确定理：令 B_K 为前 K 个完整剩余类的周期幸存集，密度 d_K，d_*=inf_Kd_K，并定义 ℓ_{K,j}=(log2)^{-1}Σ_{2^j≤n<2^{j+1}, n∈B_K\A}1/n。一个足以闭合原题、且未被单块反例否定的精确下一定理是：存在绝对常数 C，使对每个 K，limsup_{J→∞}J^{-1}Σ_{j<J}ℓ_{K,j}≤C(d_K-d_*)。由此 δ̲_log(A)≥d_K-C(d_K-d_*)，再令 K→∞ 即得 δ_log(A)=d_*。
- 研究记录：

记 R_i={n≥1:n≡a_i (mod n_i)}，C_i=R_i∩[n_i,∞)，A=ℕ\⋃_iC_i。对固定 K，B_K=ℕ\⋃_{i≤K}R_i 是模 L_K=lcm(n_1,…,n_K) 的周期集，密度 d_K 存在；C_i 与 R_i 只差有限集，所以前 K 个激活条件也有同一密度。因 n≥n_K 时 A⊆B_K，得到
δ̄_log(A)≤d_K，故 δ̄_log(A)≤d_*:=lim_Kd_K。

初始路线失败在尺度错配。两类交集确有精确公式
δ(R_m∩R_n)=0，若 gcd(m,n)∤(a_m-a_n)；否则 δ(R_m∩R_n)=1/lcm(m,n)。
但取 q=N,…,2N 和 a_q=0 时，每个 n∈[N,2N] 由 q=n 激活命中，故该对数块损失为 1；另一方面 ⋃_{q=N}^{2N}R_q 的密度正是“有除数落在 [N,2N]”的密度，随 N→∞ 趋零。故任何逐块局部—全局常数不等式均为假。相反，若随机选 a_q，则
E δ(⋃R_q)=1-∏_{q=N}^{2N}(1-1/q)=1-(N-1)/(2N)→1/2，
所以完整周期并集本身也没有统一 o(1) 界。

幸存部分之一可加强。取规范剩余 r_i∈[0,n_i-1]。C_i 中最早允许的点是 n_i（r_i=0）或 n_i+r_i（r_i>0），以后步长为 n_i，因此 |C_i∩[1,x]|≤x/n_i。于是
0≤|A_K∩[1,x]|-|A∩[1,x]|≤xΣ_{i>K}1/n_i。
若 Σ_i1/n_i<∞，右端除以 x 后一致趋零，有限阶段密度因而收敛到 A 的自然密度。这也独立核实了 Araujo 定理 3.26 在本题中的应用。

另一幸存特例是固定 c≥0。若 a_i≡c (mod n_i) 对所有 i 成立，则 n>c 时
n∈⋃C_i ⇔ ∃i，n_i|(n-c)。
故排除集最终为 c+M，其中 M 是 n_i 的倍数集。Davenport–Erdős 定理给出 M 的对数密度；且 Σ_{m≤x,m∈M}|1/(m+c)-1/m|=O(1)，端点差亦为 O(1)，所以平移保持对数密度。一般问题仍需上述跨尺度平均不等式，不能由本轮的单块 Bonferroni 路线得到。

- 一手来源：

  - [Erdős Problem #25](https://www.erdosproblems.com/25)；一手来源：`false`；核验：页面仍标为 OPEN；精确题面含 n<n_i 激活条件，并注明是 #486 的单剩余类特例。
  - [P. Erdős, Some Unsolved Problems (1961), Point 26](https://users.renyi.hu/~p_erdos/1961-22.pdf)；一手来源：`true`；核验：印刷页 236，公式 (I.26.1)–(I.26.2)：允许每个模数排除若干剩余类，且明确要求 b≥a_i；询问未排除集合的对数密度是否存在。
  - [P. Erdős, Some of my Favourite Problems in Number Theory, Combinatorics, and Geometry (1995), I.4](https://www.ime.usp.br/~yoshi/resenhas/abstracts/Erdos.pdf)；一手来源：`true`；核验：PDF 第 3 页、I.4 节重述本题，并明确称即使每个模数只排除一个剩余类也困难。
  - [P. Erdős, A Generalization of a Theorem of Besicovitch (1936)](https://users.renyi.hu/~p_erdos/1936-01.pdf)；一手来源：`true`；核验：开篇定理及其固定倍数区间特例说明：具有某个除数落在 [N,2N] 的整数之自然密度随 N→∞ 趋于 0。DOI: 10.1112/jlms/s1-11.2.92。
  - [H. Davenport and P. Erdős, On Sequences of Positive Integers (1936), Theorem 1](https://users.renyi.hu/~p_erdos/1936-04.pdf)；一手来源：`true`；核验：任意整数序列的倍数集具有对数密度，且等于有限倍数并集密度的单调极限。
  - [F. Araujo, Erdős Sieves and Dynamics (2026 dissertation), Theorem 3.26](https://digital.ub.uni-paderborn.de/hs/download/pdf/8306542)；一手来源：`true`；核验：PDF 页 42：若激活筛满足 Σ_i |R_i|/b_i<∞，则未筛集合的自然密度存在，并等于有限截断密度的极限；本题给出 Σ_i1/n_i<∞ 特例。
  - [FormalConjectures/ErdosProblems/25.lean](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/25.lean)；一手来源：`true`；核验：形式量词为正自然数模数、StrictMono 模数序列、任意整数剩余代表及逐点激活条件。

#### #117

- 精确题面：Let $h(n)$ be minimal such that any group $G$ with the property that any subset of $>n$ elements contains some $x\neq y$ such that $xy=yx$ can be covered by at most $h(n)$ many Abelian subgroups. Estimate $h(n)$ as well as possible.
- 上轮下一步：计算 limsup h(n)^{1/n} 的候选下界：系统比较 extraspecial p-群及其中心积，明确求出 ω(G) 与最小阿贝尔覆盖数，看 p>2 或非经典辛 spread 是否改进 √2。
- 用时：891.3 秒（硬上限 7200 秒）
- 路线目标：严格求出 extraspecial p-群的阿贝尔覆盖数，核验 p=2 的团数公式，并判断奇素数是否改进已有下界。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **复核 p=2 路线**（`advanced`）：用 Gram 矩阵秩控制团数，并用显式辛 spread 计算覆盖数。；推导：得到 ω(E_{2,m})=2m+1、a(E_{2,m})=2^m+1，故 h(2m+1)≥2^m+1。
  - **证伪奇素数的直接类比**（`refuted`）：检查交换子辛形式的精确条件。；推导：奇 p 时不交换只要求 B(v,w)≠0，不能把所有非零配对同时归一为 1；因此 J+I 的 Gram 秩论证仅适用于 p=2。
  - **奇素数小参数精确搜索**（`advanced`）：枚举射影辛图，以着色分支限界求最大团，并用 NetworkX 独立复算。；推导：精确得到 ω(E_{3,2})=7、ω(E_{3,3})=13。因此 h(7)≥3²+1=10；同时 13>3·3+1，反驳了 ω(E_{3,m})=3m+1 的自然猜想。
  - **筛除 p≥5 的渐近候选**（`advanced`）：结合 a(E_{p,m})=p^m+1 与 ω(E_{p,m})≥mp+1。；推导：该族可能达到的渐近底数至多 p^{1/p}。对所有素数 p≥5，p^{1/p}<√2，故奇素数中仅 p=3 尚可能渐近改进二群下界。

- 严格推进：
  - 对任意阶 p^{2m+1} 的 extraspecial p-群 E，严格证明 a(E)=p^m+1。
  - 重新严格证明 p=2 时 ω(E)=2m+1，从而恢复 h(2m+1)≥2^m+1。
  - 得到严格的新有限参数下界 h(7)≥10，优于旧路线在 n=7 给出的 h(7)≥9。
  - 把 extraspecial 奇素数的潜在渐近改进严格缩减到唯一候选 p=3。

- 路线证伪/边界检查：
  - 程序复现 (p,m)=(2,1),(2,2),(2,3) 的理论团数 3、5、7。
  - 每个输出团均逐对检查辛积非零。
  - 辛群对非正交有序射影点对传递，故固定一条边不损失最大团。
  - 自写分支限界和 NetworkX 最大权团算法分别给出 (3,2)→7、(3,3)→13。
  - 计算结果 ω(E_{3,3})=13 严格否定线性猜想 3m+1。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/117/symplectic_clique.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/117/symplectic_clique.py)：射影辛图生成和精确最大团程序，含两个独立求解实现。SHA-256 为 4ceb2848464971de09ed751963228c42b520afa724317944fcaacad9a9aa494b。；命令 `python3 symplectic_clique.py 3 2 --fix-edge --networkx-check && python3 symplectic_clique.py 3 3 --fix-edge --networkx-check`；结果：依次输出 omega=7、networkx_omega=7，以及 omega=13、networkx_omega=13，并给出显式团向量。

- 第一阻塞点：要把 h(7)≥10 的有限改进提升成更强的渐近底数，必须控制 W(2m−1,3) 最大 partial ovoid 的增长。m=3 已显示其并非简单的 3m+1；现有一般界不足以判断 extraspecial 3-群最终能否超过 √2。
- 下一精确定理：最明确的下一定理是：证明无限多个 m 满足 ω(W(2m−1,3))≤Cm+O(1)，其中 C<2log₂3≈3.169925；这会推出严格优于 √2 的下界。反之，若证明 ω(W(2m−1,3))≥(2log₂3−o(1))m，则可排除 extraspecial 3-群的渐近改进。
- 研究记录：

设 E 为阶 p^{2m+1} 的 extraspecial p-群，V=E/Z(E)≅F_p^{2m}。交换子诱导非退化交替形式 B，且 [x,y]=1 当且仅当 B(x̄,ȳ)=0。

首先计算覆盖数。任一阿贝尔子群 A 可扩大为 AZ(E)，其在 V 中的像是全迷向子空间，维数至多 m。因此一个这样的像至多包含 p^m−1 个非零向量，故
\[
a(E)\ge \frac{p^{2m}-1}{p^m-1}=p^m+1.
\]
反之，把 V 识别为 F_{p^m}²，并取
\[
B((x,y),(x',y'))=\operatorname{Tr}_{F_{p^m}/F_p}(xy'-x'y).
\]
对 t∈F_{p^m} 令 L_t={(x,tx)}，再令 L_∞={(0,y)}。这些是 p^m+1 个两两仅交于 0 的拉格朗日子空间，并划分 V\{0}。其在 E 中的原像是阿贝尔子群且覆盖 E，所以
\[
a(E)=p^m+1.
\]

当 p=2 时，两向量非正交等价于 B(v_i,v_j)=1。若有 s 个两两非正交向量，其 Gram 矩阵为 J_s+I_s；该矩阵在 s 偶时秩为 s，在 s 奇时秩为 s−1。由于秩不超过 2m，必有 s≤2m+1。取 s=2m+1 时，J_s+I_s 的根基恰由全 1 向量生成，在商空间上得到 2m 维非退化交替形式；标准基的像给出 2m+1 个两两非正交向量。因此
\[
\omega(E_{2,m})=2m+1,
\qquad h(2m+1)\ge2^m+1.
\]

奇 p 时，正确对象是辛极空间 W(2m−1,p) 的最大 partial ovoid，不能沿用固定 Gram 矩阵。对 p=3、m=2，完整枚举 PG(3,3) 的 40 个点，以 B(v,w)≠0 连边。两个独立精确算法均证明最大团数为 7。因此阶 3^5 的 extraspecial 3-群满足 ω(E)=7、a(E)=10，得到本轮主要推进
\[
\boxed{h(7)\ge10}.
\]
对 p=3、m=3，同样得到 ω(E)=13；这与 W(5,3) 中 q²+q+1=13 的文献构造一致，并否定 ω=3m+1。

一般下界 ω(E_{p,m})≥mp+1 给出
\[
\limsup_{m\to\infty}a(E_{p,m})^{1/\omega(E_{p,m})}\le p^{1/p}.
\]
函数 p^{1/p} 在 p≥3 上递减，且 5^{1/5}<√2，所以 p≥5 不可能使本族优于 extraspecial 2-群；仅 p=3 未决。

最后，Pyber 给有限群 |G:Z(G)|≤c^{ω(G)}，而每个中心陪集 gZ(G) 包含于阿贝尔子群 ⟨g,Z(G)⟩，故 a(G)≤|G:Z(G)|≤c^n。对任意群可先用 Neumann 得到中心有限指数，再取有限生成的中心扩张并模去适当中心有限指数子群，化为保持中心指数且不增 ω 的有限商。因此已知指数上界仍覆盖精确题面。本轮未确定最优指数率，不能声称完整解。

- 一手来源：

  - [Pyber, The Number of Pairwise Non-Commuting Elements and the Index of the Centre in a Finite Group](https://doi.org/10.1112/jlms/s2-35.2.287)；一手来源：`true`；核验：期刊摘要精确陈述：存在绝对常数 c，使至多含 n 个两两不交换元素的有限群满足 |G:Z(G)|≤c^n。
  - [Neumann, A problem of Paul Erdős on groups](https://doi.org/10.1017/S1446788700019303)；一手来源：`true`；核验：论文研究任意群的非交换图；其核心结论用于把 ω(G)<∞ 归约到 |G:Z(G)|<∞。
  - [Chin, On non-commuting sets in an extraspecial p-group](https://doi.org/10.1515/jgth.2005.8.2.189)；一手来源：`true`；核验：期刊页确认奇 p 情形只给出最大非交换集的上下界，没有一般精确公式。
  - [Liu–Wang, On Non-Commuting Sets in Certain Finite p-Groups](https://www.researchgate.net/publication/282426470_On_Non-commuting_Sets_in_Certain_Finite_p-Groups/download)；一手来源：`true`；核验：正文 Claim 3 重述并证明：p=2 时 ω(E)=2m+1；奇 p 时 mp+1≤ω(E)≤(p(p−1)^m−2)/(p−2)。
  - [Ceria–De Beule–Pavese–Smaldore, On large partial ovoids of symplectic and Hermitian polar spaces](https://arxiv.org/abs/2203.04553)；一手来源：`true`；核验：Theorem 3.7 构造 W(5,q) 中大小 q²+q+1 的极大 partial ovoid；这与本轮 q=3、m=3 的 13 点计算一致。

#### #143

- 精确题面：Let $A\subset (1,\infty)$ be a countably infinite set such that for all $x\neq y\in A$ and integers $k\geq 1$ we have\[ \lvert kx -y\rvert \geq 1.\]Does this imply that $A$ is sparse? In particular, does this imply that\[\sum_{x\in A}\frac{1}{x\log x}<\infty\]or\[\sum_{\substack{x <n\\ x\in A}}\frac{1}{x}=o(\log n)?\]
- 上轮下一步：从 KLL 的 GCD-graph 论证中提取定量逆定理：检验能否推出 $H(X)\ll\log X/(\log\log X)^{1+\delta}$ 或某个分块可求和估计；任何这样的界经 Abel 分部都会解决第一问。
- 用时：755.9 秒（硬上限 7200 秒）
- 路线目标：先证伪“从 KLL 的 o(log X) 直接提取可积速率”路线；随后分析倍点禁区、最小元边界和 KLL 相关性能量框架，争取闭合特例并确定精确的下一定理。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **证伪“o(log X) 经 Abel 分部即可收敛”**（`refuted`）：按指数壳 I_j=[e^j,2e^j] 构造仅满足1间隔的抽象模型，每壳放约 e^j/log j 个整数。；推导：该壳调和质量 h_j≈1/log j，故 H(e^J)≈∑_{j≤J}h_j≈J/log J=o(J)。但目标壳质量约 h_j/j≈1/(j log j)，其总和发散。等价地，Abel 分部只有 ∫H(t)/(t log^2t)dt，而 H(t)=o(log t) 仅给 o(1/(t log t))，不可积性并未排除。此模型故意不满足 dilation separation；它严格反驳的是从“KLL结论+1间隔”推出第一问的逻辑路线。
  - **最小元与倍点禁区**（`advanced`）：利用 k=1 的1间隔性先证明最小元存在，再研究最小元的所有整数倍半径1禁区。；推导：若 m=min A<2，对任意 y>m，取最接近 y/m 的正整数 k，则 |km−y|≤m/2<1，矛盾；无限性因此强制 m≥2。若 m=2，则 y≠2 必避开所有开区间 (2k−1,2k+1)，故 y只能是奇整数端点。于是 A⊂N；精确整除 b=ka 会给 |ka−b|=0，故 A 是原始整数集，Erdős 1935 定理给目标级数收敛。
  - **尝试把 2<m<3 编码为原始指标集**（`refuted`）：把每个 y>m 放进禁区之间的唯一短隙 I_n=[nm+1,(n+1)m−1]；因 |I_n|=m−2<1，每隙至多一个 A 元素。；推导：“出现的指标 n 必组成原始整数集”是假的。取 m=5/2，集合 {5/2,4,6} 满足全部 dilation 条件；4∈I_1、6∈I_2，而 1|2。逐对检查：从 5/2 到4、6的最小距离均为1，从4到6的最小距离为2，反向 k≥2 自动更大。
  - **固定分母有限网格反例搜索**（`inconclusive`）：在候选 p/q∈[2,X] 上以整数算术建立冲突图：若存在 k≥1 使 |kp−r|<q 即连边；用 MILP 最大化 ∑1/(x log x)，再独立复核所得集合。；推导：q=2、X=60 时 HiGHS 给出严格有限模型最优解 {2,3,5,…,59}（截至59的素数），目标值1.3971524518；没有选取非整数半格点。q=1,3,4 的相应小规模运行也未显示分数点优势。但这是有限边界效应明显的搜索，不能作为渐近证明。
  - **审计 KLL 定量化路线**（`blocked`）：逐项检查第2节的 κ(α)、Lemma 2.13、Proposition 2.15 及第5页作者说明。；推导：KLL 使用 κ(α)=α^{-1}∏_{p≤α}(1−1/p)≈1/(α log α)，确与目标权重同阶；但其构造从固定 c>0 的 H(X)>4c log X 出发，得到每个厚块固定正 κ-质量，并以块数 J 吸收 O_c(J) 相关误差。若仅假设 ∑κ(α)=∞，各对数壳质量可以趋于0，原论证中 O(J) 误差不再由总质量平方控制。因此“直接追踪 c”不是机械定量化；缺少的是按 κ-质量缩放的相关性能量估计或新的跨尺度选择引理。

- 严格推进：
  - 严格证明：任意无限 admissible A 都有最小元 m，且 m≥2。最小元存在是因为 k=1 给不同元素距离至少1，所以任意有界区间只含有限多个元素。
  - 严格证明新的闭合特例：若 min A=2，则 A 是原始整数集，因而 ∑_{a∈A}1/(a log a)<∞。这里边界等号 |2k−(2k±1)|=1 必须保留；不能把 ≥1 错换成 >1。
  - 严格复核 KLL Theorem 1 的逆否应用：若本题条件成立，则取 ε=1 不可能出现 |nα−β|<1；所以 limsup H(X)/log X≤0。该比值非负，故 H(X)=o(log X)。
  - 精确分块等价：令 h_j=∑_{a∈A∩(e^j,e^{j+1}]}1/a，则除有限初项外，∑_{a∈A}1/(a log a)<∞ 当且仅当 ∑_{j≥1}h_j/j<∞；KLL 只给 ∑_{j≤J}h_j=o(J)。
  - 对于任意固定缩放整数格 A⊂γN，令 P={n:γn∈A}。若 n|m 且 n≠m，会产生精确 dilation 冲突，故 P 原始；由 Erdős 1935 亦可立即推出该固定格特例的加权收敛。

- 路线证伪/边界检查：
  - 检查严格/非严格边界：题设允许距离恰为1；KLL 定理制造的是严格小于1，因此逆否仍完全适用。最小元 m=2 分支正依赖奇整数端点的等号情形。
  - 显式有限反例 {5/2,4,6} 否定了“短隙指标原始”引理；程序的精确分数检查也对三对均返回 conflict=false。
  - 指数壳模型证明 H=o(log X) 与目标级数发散可以同时发生，因此任何只引用 KLL 结论和 Abel 分部的候选完整证明均被反驳。
  - 有限网格 MILP 的边由整数不等式 |kp−r|<q 生成，避免浮点误判；返回集合又对全部元素对重新检查。优化结果只记为探索性阴性结果。
  - 检查了 Lean 精确题面：可数性、无限性、A⊂(1,∞) 和所有有序对/所有自然数 k 的量词均未在边界证明中遗漏。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/143/finite_grid_milp.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/143/finite_grid_milp.py)：固定分母网格上的精确冲突图、最大权独立集 MILP 和返回集合证书检查。源码只写入本题工作目录，并已通过 py_compile。；命令 `python finite_grid_milp.py --q 2 --xmin 2 --xmax 60 --weight erdos`；结果：HiGHS Status 7: Optimal；117个候选、900条冲突边；最优目标1.397152451808641，选择17个值 2,3,5,7,11,…,59；exact_pair_certificate=true。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/143/finite_grid_milp.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/143/finite_grid_milp.py)：复核短隙指标反例 {5/2,4,6}。；命令 `python - <<'PY' from finite_grid_milp import conflict P=[5,8,12]; q=2 for i,p in enumerate(P): for r in P[i+1:]: print(p,r,conflict(p,r,q)) PY`；结果：三对依次均输出 False，证明在精确分母2模型中没有 dilation 冲突。

- 第一阻塞点：一般第一问仍未闭合。KLL 的 Proposition 2.15 控制厚尺度块中的有理比例正相关，但最终误差按块数 O(J) 计；在仅假设目标级数发散时，对数壳 κ-质量可能如 1/log j 般趋零，使 J 远大于累计质量的平方。需要一个随实际 κ-质量缩放的相关性能量估计，或能把稀薄壳合并而不破坏 log α≈log β 的新选择引理。作者也明确指出现有构造的尺度可比性在第6、8节似乎是本质的。
- 下一精确定理：最清晰且由 KLL 第5页直接指向的下一定理是：设 A⊂Q_{>1} 满足原 dilation separation；把每个 α∈A 写成既约分数 a/q，并额外假设所有分子 a 均平方自由，则证明 ∑_{α∈A}1/(α log α)<∞。具体首个技术子目标应是建立一个“κ-质量版本”的 Proposition 2.15/分块能量界，使坏相关贡献为 O(κ(B)) 或 O(∑_j κ(B_j)^2)，而不是与所用尺度块数成正比。平方自由性保证分解 a=Aa_0 时 gcd(A,a_0)=1，可去掉 KLL 所述 Hauke–Vázquez–Walker 的额外损失；剩余核心正是跨尺度选择问题。
- 研究记录：

研究记录如下。先由 k=1 得 |x−y|≥1，因此 A 局部有限。任取 a∈A，则有限非空集 A∩(1,a] 有最小元，记为 m。若 1<m<2，由无限性可取 y∈A、y>m。令 k 为最接近 y/m 的正整数；因 y/m>1，可取 k≥1，且
\[
 |km-y|=m\left|k-\frac ym\right|\le \frac m2<1,
\]
与题设矛盾。因此 m≥2。

在边界 m=2，任意 y∈A\setminus\{2\} 必须满足 |2k−y|≥1（k≥1）。开区间族 (2k−1,2k+1) 覆盖 (1,∞) 除了奇整数端点，故 y∈\{3,5,7,\ldots\}。于是 A⊂N。若不同 a,b∈A 且 a|b，写 b=ka，则 |ka−b|=0，仍矛盾；所以 A 是原始整数集。Erdős 1935 的定理遂给
\[
 \sum_{a\in A}\frac1{a\log a}<\infty.
\]
这封闭了 min A=2 的全部量词，而不是启发式。

再独立复核 KLL。令
\[
 H(X)=\sum_{\substack{a\in A\\a\le X}}\frac1a.
\]
KLL Theorem 1 断言 limsup H(X)/log X>0 会对每个 ε>0 产生严格近似 |nα−β|<ε。取 ε=1 与本题的 ≥1 矛盾，故 H(X)=o(log X)。然而 Stieltjes/Abel 分部给
\[
 \sum_{a\le X}\frac1{a\log a}
 =\frac{H(X)}{\log X}+C+
 \int_{X_0}^{X}\frac{H(t)}{t\log^2t}\,dt.
\]
仅有 H=o(log t) 时，积分项只被描述为 ∫o(1/(t log t))dt，不能推出收敛。更尖锐地，在指数壳上令调和质量 h_j≈1/log j，则累计质量 ∑_{j≤J}h_j≈J/log J=o(J)，而目标和等价于 ∑h_j/j≈∑1/(j log j)=∞。因此旧路线中的“从 KLL 提取任意 o 衰减再 Abel 分部”已被严格否定。

KLL 实际引入
\[
 \kappa(\alpha)=\frac1\alpha\prod_{p\le\alpha}\left(1-\frac1p\right)
 \asymp \frac1{\alpha\log\alpha},
\]
这说明其事件权重确实击中第一问。但他们在固定 c>0 且 H(X)>4c\log X 的厚块中构造 A'_j，每块有固定正 κ-质量；Proposition 2.15 最终给出的坏相关误差按块数 J 累积。若只假定 ∑κ(α)=∞，壳质量可能趋于零，原来的 O(J) 误差便不能被总 κ-质量平方吸收。这是实质缺口，而非尚未整理常数。

倍点禁区还给出自然离散化：当 2<m<3 时，每个后继元素都落在某个
\[
 I_n=[nm+1,(n+1)m-1],\qquad |I_n|=m-2<1,
\]
故每隙至多一个元素。但 {5/2,4,6} 表明出现的指标可以包含 1|2，原始集归约失败。由此，下一步不应继续假定简单取整保持除法结构；应直接处理这些短隙变量的有理比例相关能量。综合作者本人第5页的提示，平方自由既约分子限制是目前最明确、非同义反复且与现有 GCD-graph 机械接口最近的下一定理。

- 一手来源：

  - [Koukoulopoulos–Lamzouri–Lichtman, Erdős's integer dilation approximation problem and GCD graphs（作者版，47页）](https://dms.umontreal.ca/~koukoulo/documents/publications/erdos-integer-dilations.pdf)；一手来源：`true`；核验：Theorem 1（第2页）精确假设离散 A⊂R_{>0} 且 limsup_{X→∞}H(X)/log X>0，结论是每个 ε>0 存在不同 α,β 及 n≥1 使 |nα−β|<ε；其后 Remark 通过逐次删去有限对得到无穷多对。第5页 Remark 明说该方法尚不给 Behrend 型定量界，并指出可能在所有既约分子平方自由的有理数限制下证明目标级数 (1.5)。Proposition 2.15 是实际所用的有理比例相关性能量界。
  - [KLL arXiv 记录 2502.09539](https://arxiv.org/abs/2502.09539)；一手来源：`true`；核验：核对作者、日期和摘要中的全部量词；截至本次检索，针对题143加权收敛问题的关键词检索未找到晚于 KLL、声称解决第一问的一手论文。此处只报告检索结果，不声称穷尽全部文献。
  - [Erdős, Note on Sequences of Integers No One of Which is Divisible By Any Other](https://doi.org/10.1112/jlms/s1-10.1.126)；一手来源：`true`；核验：期刊/DOI 页核对：J. London Math. Soc. s1-10 (1935), 126–128。其原始整数定理正是 KLL 公式 (1.5) 引用的结论：原始整数集 P 满足 ∑_{p∈P}1/(p log p)<∞。
  - [Erdős 1935 论文作者档案扫描](https://combinatorica.hu/~p_erdos/1935-04.pdf)；一手来源：`true`；核验：检索到原论文扫描及其筛法正文；页面抓取超时，故没有依赖无法逐页复核的额外细节，只使用由期刊页和 KLL 公式 (1.5) 双重确认的定理范围。
  - [Google DeepMind Formal Conjectures: ErdosProblems/143.lean](https://github.com/google-deepmind/formal-conjectures/blob/c252a41054125b5fd9c8356e2137cd9b55337657/FormalConjectures/ErdosProblems/143.lean)；一手来源：`true`；核验：WellSeparatedSet 的量词与输入题面一致；parts.ii 精确形式化为 subtype A 上 x↦1/(x log x) 的 Summable，目前证明仍为 sorry。文件没有形式化 KLL 的 o(log X) 结论。

#### #148

- 精确题面：Let $F(k)$ be the number of solutions to\[ 1= \frac{1}{n_1}+\cdots+\frac{1}{n_k},\]where $1\leq n_1<\cdots<n_k$ are distinct integers. Find good estimates for $F(k)$.
- 上轮下一步：对固定前 k−4 个分母，把剩余有理数归约为 m/n，并复现 Elsholtz–Planitzer 的四项分母参数计数；可检验目标是从上述递推上界中消去 log k，而不是直接追求最佳常数 1/5。
- 用时：1047.8 秒（硬上限 7200 秒）
- 路线目标：检验“剩余分母递推＋固定前 k−4 项后套四项定理”能否消除粗上界中的 log k，并定位任何改善 Vardi 指数 1/5 所需的精确定理。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **复核粗剩余分母递推**（`advanced`）：令 R_j=1−Σ_{i≤j}1/n_i、P_j=∏_{i≤j}n_i。；推导：R_j 的既约分母整除 P_j，故 R_j≥1/P_j；又 R_j≤(k−j)/n_{j+1}，所以 n_{j+1}≤(k−j)P_j。该递推严格成立，但只能直接给 exp(O(2^k log k))。
  - **最大分母分裂单射的边界证伪**（`refuted`）：检查 1/M=1/(M+1)+1/[M(M+1)] 的全部小 k 边界。；推导：当 k=1、M=1 时得到两个相同分母 2，故不属于严格递增解；实际 F(1)=1、F(2)=0。对 M>1 映射有效且可从两个最大分母恢复 M，因此只能断言 F(k+1)≥F(k) 对 k≥2 成立。
  - **朴素固定前 k−4 项**（`refuted`）：对每个前缀剩余分数逐项套 f_4(m,n)≪n^εn^{8/5}/m。；推导：若前缀积 P=∏a_i，则剩余既约分母 n≤P；但求和为 Σ_a P^{8/5+ε}=∏_iΣ_{a_i}a_i^{8/5+ε}，每层幂次变成 13/5+ε。不能漏掉前缀数量，因而该简化路线不能复现最佳常数。
  - **恢复正确的固定 L 尾部模板**（`advanced`）：先固定任意大的常数 L，枚举前 k−L 项，再对剩余 L 项使用 Theorem 2，最后令 L→∞。；推导：Curtiss 界给前缀数至多 k!c_0^{2^{k−L+1}}。剩余既约分母 n 也小于 k!c_0^{2^{k−L+1}}。Theorem 2 中 n 的幂为 2·(8/5)2^{L−5}；乘上 log_{c_0}n 的主指数后恰为 (1/5)2^k。前缀贡献为 2^{1−L}2^k，可由 L→∞ 消去。
  - **拼接四项定理的两个分支**（`blocked`）：在首次 lifting 中令 X=n²/m，并在两个逐点界的交点切分 u。；推导：两界分别为 A≈X^{3/2}u^{−3/4}、B≈X^{8/5}u^{−1}，交点 u=X^{2/5}。于是 Σ_{u≤X^{2/5}}A+Σ_{u>X^{2/5}}B≪X^{8/5}log n，没有固定幂节省。
  - **五项加权和小规模实验**（`inconclusive`）：精确计算 S(n)=Σ_{1≤u≤4n}f_4(u,n(u+n))，采用有理数递归及二项尾部因式分解。；推导：n=1,…,10 时 S(n)=281,5359,30192,71202,174031,282963,555382,809255,1193395,1583715；S(n)/(n²)^{8/5} 约为 281 至 1097。小数据未显示下降趋势，但远不足以反驳渐近幂节省。

- 严格推进：
  - 初始递推的有限性证明正确，但额外 log k 并非不可避免；Curtiss 余量定理可直接给 n_j≤(k−j+1)u_j，从而得到 exp(O(2^k))。
  - 完整复现了已知最佳上界的常数传播：四/五项指数 c=8/5 经固定 L 尾部模板变成 Vardi 指数 c/8=1/5。
  - 严格定位了旧路线的两处错误：分裂单射遗漏 k=1；固定四项尾部逐项求和遗漏前缀数量。
  - Konyagin Theorem 1 的量词与本题严格递增条件完全一致，其下界常数可写成 exp(exp(((log2)(log3)/3+o(1))k/log k))。
  - 截至本轮一手来源检索，没有找到晚于 Elsholtz–Planitzer、且明确改善本题 1/5 上界或 Konyagin 下界的论文；这不是穷尽性不存在声明。

- 路线证伪/边界检查：
  - 精确枚举验证 F(1),…,F(6)=1,0,1,6,72,2320，并逐解用 Fraction 检查和为 1、分母严格递增。
  - 枚举显示最大分母依次为 1,0,6,42,1806,3263442，与 Sylvester/Curtiss 极值边界相符。
  - 检查分裂像：k=1 的像不合法；从 k=3 到已枚举范围，像均属于下一层且无碰撞。
  - 四项尾部只计非降序解，确实覆盖严格递增尾部；因此上界方向没有混淆。
  - 加权实验使用未施加“尾分母大于前缀末项”的 f_4，故它是 lifting 所用的安全上界，而不是对严格问题的低估。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/148/egyptian_exact.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/148/egyptian_exact.py)：严格递增解的小 k 精确枚举器；使用 Fraction、Curtiss 坐标界，并检查最大分母分裂像。；命令 `python3 egyptian_exact.py --max-k 6`；结果：F(1..6)=1,0,1,6,72,2320；明确检出 k=1 分裂失败，其余已测试分裂像有效。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/148/weighted_tail_experiment.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/148/weighted_tail_experiment.py)：精确计算首次 lifting 的四项加权和；二项尾部使用 (pa−q)(pb−q)=q² 的除数枚举。；命令 `python3 -u weighted_tail_experiment.py --max-n 10`；结果：得到 S(1..10)=281,5359,30192,71202,174031,282963,555382,809255,1193395,1583715；小范围未证伪固定幂节省，但也未提供支持证据。

- 第一阻塞点：现有四项逐点界在 u=X^{2/5} 的交界处恰好饱和 X^{8/5}；单纯拼接两个分支或朴素固定前缀均无法降低指数。必须获得四项解对首分母参数 u 的平均节省，或直接把 n^{8/5}/m 的指数改善一个固定量。
- 下一精确定理：明确的充分目标是：存在 0<δ<3/5，使对所有 m≤5n，\[\sum_{\substack{0<u\le4n\\m\mid u+n}} f_4\!\left(u,\frac{n(u+n)}m\right)\ll_\epsilon n^\epsilon\left(\frac{n^2}{m}\right)^{8/5-\delta}.\]这会给五项指数 c=8/5−δ；套同一 lifting 与固定 L 模板，即严格改善为 \(F(k)\le c_0^{(1/5-\delta/8+o(1))2^k}\)。允许尾分母下界的严格递增版本也值得先证，但还需重写 lifting 引理以保持该约束。
- 研究记录：

设 \(u_1=1\)、\(u_{j+1}=u_j(u_j+1)\)，并令 \(c_0=\lim u_j^{2^{-j}}=1.26408\cdots\)。对非降序解 \(1=\sum_{i=1}^k1/t_i\)，Curtiss 界为\[1-\sum_{i=1}^{j-1}\frac1{t_i}\ge\frac1{u_j}.\]若 \(t_j>(k-j+1)u_j\)，则剩余 \(k-j+1\) 项之和小于 \(1/u_j\)，与总和为 1 矛盾；故 \(t_j\le(k-j+1)u_j\)。这已经把旧乘积分母递推的 \(\log k\) 损失消掉。

要得到最佳常数，固定 \(L\ge5\)，枚举前 \(k-L\) 项。由 \(u_j<c_0^{2^j}\)，前缀数至多\[\prod_{j=1}^{k-L}(k-j+1)u_j<k!\,c_0^{2^{k-L+1}}.\]写剩余分数为既约的 \(m/n\)，则 \(n\le\prod_{j\le k-L}t_j<k!c_0^{2^{k-L+1}}\)。Elsholtz–Planitzer Theorem 2 给\[f_L(m,n)\ll_\epsilon (Ln)^\epsilon\left(\frac{L^{4/3}n^2}{m}\right)^{(8/5)2^{L-5}}.\]忽略只产生 \(o(2^k)\) 的阶乘、固定 \(L\) 和 \(\epsilon\) 项，尾部在 \(c_0\) 底下的主指数为\[2\cdot\frac85\,2^{L-5}\cdot2^{k-L+1}=\frac15\,2^k.\]前缀枚举另贡献 \(2^{k-L+1}\)；先取 \(L\) 足够大再令 \(k\to\infty\)，得到 \(f_k(1,1)\le c_0^{(1/5+o(1))2^k}\)，从而同样界住 \(F(k)\)。这只是对已知上界的独立复核，不是新证明本题。

尝试改进时，五项首分母满足 \(u=ma_1-n\)，尾分数为 \(u/[n(u+n)/m]\)。令 \(X=n^2/m\)，四项定理的两个相关分支在常数范围内成为 \(X^{3/2}u^{-3/4}\) 与 \(X^{8/5}u^{-1}\)。交点 \(u=X^{2/5}\) 两侧求和都只给 \(X^{8/5}\)（差一个对数），说明固定幂改进必须利用不同 \(u\) 之间的算术相关性、尾分母阈值或更强的四项参数计数。上述加权定理正是当前清晰且足以改善问题 148 的下一关。

- 一手来源：

  - [Konyagin, Double Exponential Lower Bound for the Number of Representations of Unity by Egyptian Fractions, Theorem 1 and Lemma 2](https://www.mathnet.ru/php/getFT.phtml?jrnid=mzm&paperid=10417&what=fullt&option_lang=eng)；一手来源：`true`；核验：正文定义严格递增的 X_n；Theorem 1 精确给出 |X_n|>exp(exp(((ln2)(ln3)/3+o(1))n/ln n))。式(1)的分裂单射是在 X_3 起步后的范围使用。
  - [Browning–Elsholtz, The number of representations of rationals as a sum of unit fractions, Theorems 3–4](https://www.math.tugraz.at/~elsholtz/WWW/papers/papers33FINAL2013.pdf)；一手来源：`true`；核验：Theorem 4 的证明使用余量界 1−Σ_{i≤m}1/t_i≥1/u_{m+1}，推出 t_j≤(k−j+1)u_j；随后保留固定 L 项作尾部，而非固定四项尾部。
  - [Elsholtz–Planitzer, Sums of four and more unit fractions and approximate parametrizations, Theorems 1–2 and Section 5](https://arxiv.org/pdf/2012.05984)；一手来源：`true`；核验：Theorem 1 给出 f_4(m,n)≪_ε n^ε min{n^{3/2}/m^{3/4},n^{8/5}/m}；Theorem 2 给出 k≥5 时指数 (8/5)2^{k−5} 的 lifting 界。Section 5 通过 u=ma_1−n 及调和求和完成首次提升。
  - [Elsholtz–Planitzer, The number of solutions of the Erdős–Straus equation and sums of k unit fractions, Corollary 3](https://arxiv.org/pdf/1805.02945)；一手来源：`true`；核验：核对了较早的 28/17 指数及其与 Browning–Elsholtz Theorem 4 模板的衔接；新论文明确要求只替换尾部指数。

#### #256

- 精确题面：Let $n\geq 1$ and $f(n)$ be maximal such that for every $a_1\leq \cdots \leq a_n\in \mathbb{N}$ we have\[\max_{\lvert z\rvert=1}\left\lvert \prod_{i}(1-z^{a_i})\right\rvert\geq f(n).\]Estimate $f(n)$ - in particular, is it true that there exists some constant $c>0$ such that\[\log f(n) \gg n^c?\]
- 上轮下一步：把 Belov–Konyagin 的三角多项式定理逐项翻译成指数多重集，核对常数项、允许重复以及从其定理到 log f(n)≪(log n)^4 的参数对应；这是可独立审计的下一步。
- 用时：779.3 秒（硬上限 7200 秒）
- 路线目标：独立核验并闭合 Belov–Konyagin 非负余弦多项式构造到乘积上界的量词归约；先寻找参数或重数反例，再更新当前上下界。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **先证伪旧路线**（`advanced`）：核查 1996 年两篇同名近似论文、重数条件及最新下界文献。；推导：旧材料混淆了 Mat. Zametki 59:4 的三页短讯与含 Theorem 0.5、Corollary 0.3 的 Izv. Math. 60:6 长文；此外旧称当前下界为 √(2n)，已被 Tang 的 2√n 更新。Belov–Konyagin 上界路线本身幸存。
  - **优化径向正则化桥梁**（`advanced`）：由质量为 n 的非负整系数余弦多项式构造指数多重集，并优化径向参数。；推导：若 T(x)=a_0+∑_{k≥1}b_k cos(kx)≥0、b_k∈Z_{≥0}、∑b_k=n，则 P(z)=∏_k(1-z^k)^{b_k} 满足 log||P||∞≤-(n/2)log r-a_0log(1-r)。取 r=n/(n+2a_0)，得 log||P||∞≤(n/2)log(1+2a_0/n)+a_0log(1+n/(2a_0))≤a_0[1+log(1+n/(2a_0))]。
  - **复核 Tang 系数引理**（`advanced`）：用正负系数多重集和 Newton 恒等式重建 Theorem 3.2。；推导：设 Q=∑c_jz^j 且 (1-z)^n|Q。正、负系数分别编码为多重集 A、B。零次矩给 |A|=|B|=r；若 r<n，则已有 1,…,r 次幂和相等，Newton 恒等式推出 A=B，与正负支撑不交及 Q≠0 矛盾。因此 ∑|c_j|=2r≥2n，整数性给 ∑c_j²≥2n。
  - **小规模反例搜索**（`advanced`）：穷举 n≤5、a_i≤10，精确展开系数并数值最大化单位圆模；同时随机压力测试径向逐因子比较。；推导：分别检查 10、55、220、715、2002 个元组；未发现 ∑c_j²<2n 或 ||P||∞<2√n。10^5 次径向测试也未发现比较式方向错误。

- 严格推进：
  - 允许重复恰由 b_k=#{i:a_i=k} 编码，且 ∑b_k=n；Belov–Konyagin 的系数非增条件只是更强的构造限制，不妨碍其作为本题上界见证。
  - 独立闭合并略微强化了文献中的 log f(n)≤K_Z^↓(n)(1+log n) 桥梁。代入 a_0=O((log n)^3) 得 log f(n)=O((log n)^4)。
  - 因此任何固定 c>0 的 log f(n)≫n^c 都会推出 n^c≪(log n)^4，与 n→∞ 矛盾；特别问题严格为否。
  - 当前经一手来源核对的总体区间更新为 2√n≤f(n)≤exp(C(log n)^4)，完整增长阶仍未确定。
  - 边界 n=1 直接有 f(1)=2；Belov–Konyagin 的渐近定理原文范围为 n>3，有限小 n 可吸收入绝对常数。

- 路线证伪/边界检查：
  - 逐因子比较方向已代数核对：r^{-1}|1-re^{ix}|²-|1-e^{ix}|²=(1-r)²/r≥0。
  - Fourier 展开在 0<r<1 时绝对收敛，故可交换有限 k 求和与无限 m 求和。
  - Tang 的 Newton 步骤所需次数完整：反设 r<n 时有 r≤n-1，因此整除性提供的 0,…,n-1 次矩确实覆盖 1,…,r。
  - 数值搜索仅作证伪辅助，没有把有限指数范围或浮点最大化当作全称证明。
  - 旧分析的 Parseval 初等论证只能直接给 f(n)≥√2；更强下界需要额外结构，不能由常数项和最高项两项直接推出。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/256/verify_route.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/256/verify_route.py)：精确展开纯乘积、检查系数平方和界、数值最大化圆周模，并压力测试径向比较式。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/256 && python verify_route.py --max-n 5 --max-a 10 --grid 8192 --trials 100000`；结果：全部检查通过。n=1,…,5 的最小观测圆周最大值为 2、3.07920143568、4.38989637098、5.69301621655、7.95138759457；最小系数平方和均恰为 2n。

- 第一阻塞点：该路线尚不能确定 f(n) 的真实阶。Belov–Konyagin 只构造出常数项 a_0=O((log n)^3) 的质量 n 非负余弦多项式，而桥梁仍损失约 log(n/a_0)；Tang 的单位圆零点/整数系数机制只给出 √n 级下界。两者目前没有可迭代的共同参数。检索中未找到一手来源声称闭合这一鸿沟。
- 下一精确定理：最直接的下一定理是：存在固定 δ>0，使每个充分大 n 都有有限非增非负整数序列 b_1≥b_2≥⋯、∑b_k=n，且 a_0+∑b_k cos(kx)≥0 对所有实 x 成立，同时 a_0=O((log n)^{3-δ})。由本次桥梁将立即推出 log f(n)=O((log n)^{4-δ})。另一独立目标是证明所有纯乘积均有 ∑c_j²≥(2+ε)n；这会提高 2√n 的常数，但不会改变增长指数。
- 研究记录：

记 P(z)=∏_{i=1}^n(1-z^{a_i})。先给出 Belov–Konyagin 归约的自足证明。若 T(x)=a_0+∑_{k≥1}b_k cos(kx)≥0，其中 b_k∈Z_{≥0} 且 ∑b_k=n，令 P(z)=∏_k(1-z^k)^{b_k}。对 0<r<1，绝对收敛展开
log|1-re^{iθ}|=-∑_{m≥1}r^m cos(mθ)/m
给出
log∏_k|1-re^{ikx}|^{b_k}=-∑_{m≥1}(r^m/m)∑_k b_k cos(kmx)≤-a_0log(1-r)。
另一方面，
r^{-1}|1-re^{iy}|²-|1-e^{iy}|²=(1-r)²/r≥0，
故逐因子相乘得到
|P(e^{ix})|≤r^{-n/2}∏_k|1-re^{ikx}|^{b_k}。
因此
log||P||∞≤-(n/2)log r-a_0log(1-r)。
取最优 r=n/(n+2a_0)，得到
log||P||∞≤(n/2)log(1+2a_0/n)+a_0log(1+n/(2a_0))≤a_0[1+log(1+n/(2a_0))]。
Belov–Konyagin Theorem 0.5(2) 给出相应见证 a_0=O((log n)^3)，遂有 log f(n)=O((log n)^4)，即其 Corollary 0.3。这和任意 n^c 下界不相容。
下界方面，若 Q(z)=∑c_jz^j∈Z[z]非零且 (1-z)^n|Q，则 Q 在 1 点前 n 阶下降阶乘矩消失；下降阶乘与普通幂张成同一多项式空间，所以 ∑c_jj^m=0（0≤m<n）。把 c_j>0、c_j<0 分别按重数编码为多重集 A、B。零次式给 |A|=|B|=r。若 r<n，则前 r 个幂和相同，Newton 恒等式逐次确定前 r 个初等对称式，故 A=B；但二者支撑按符号不交，只能同时为空，违背 Q≠0。因此 r≥n，且
∑c_j²≥∑|c_j|=2r≥2n。
对纯乘积 Q=P，Tang 再应用 O’Hara–Rodriguez Corollary 1 的 ||P||∞²≥2∑c_j²，得到 f(n)≥2√n。故可靠现状为
2√n≤f(n)≤exp(C(log n)^4)。
特别问题已解决为否，但“估计 f(n)”的完整问题仍开放；本记录不声称完整证明。

- 一手来源：

  - [Belov–Konyagin, An estimate of the free term of a non-negative trigonometric polynomial with integer coefficients](https://www.mathnet.ru/links/98e034a9e8f0963bef7f7b82323d5e1c/im95_eng.pdf)；一手来源：`true`；核验：Theorem 0.5(2) 对 n>3 给出 K_Z^↓(n)≪M_Z^↓(n)≪(log n)^3；正文紧接着写出 log f(n)<K_Z^↓(n)(1+log n)，Corollary 0.3 为 log f(n)=O((log n)^4)。
  - [Tang, An improved lower bound for Erdős–Szekeres products](https://arxiv.org/abs/2509.14182)；一手来源：`true`；核验：v2 的 Theorem 1.2 给出 f(n)≥2√n；Theorem 3.2 给出：若非零 Q∈Z[z] 被 (1-z)^n 整除，则其系数平方和至少为 2n。页面列有正式期刊 DOI 10.1090/proc/17668。
  - [Erdős–Szekeres, On the product ∏(1-z^{a_k})](https://renyi.hu/~p_erdos/1959-17.pdf)；一手来源：`true`；核验：原文定义了 f(n)，Theorem 2 证明 lim f(n)^{1/n}=1，Theorem 3 陈述经典 √(2n) 下界；末页证明包含后来文献指出需修补的系数拆分步骤。
  - [O’Hara–Rodriguez, Some properties of self-inversive polynomials](https://doi.org/10.1090/S0002-9939-1974-0349967-5)；一手来源：`true`；核验：核对了题名、卷页和 DOI；原文全文受站点 403 限制，本次未直接抽取 Corollary 1。所用不等式由 Tang 论文逐字作为 Corollary 1 引用，因此该环节未冒充独立全文核验。

#### #301

- 精确题面：Let $f(N)$ be the size of the largest $A\subseteq \{1,\ldots,N\}$ such that there are no solutions to\[\frac{1}{a}\neq \frac{1}{b_1}+\cdots+\frac{1}{b_k}\]with distinct $a,b_1,\ldots,b_k\in A$? Estimate $f(N)$. In particular, is $f(N)=(\tfrac{1}{2}+o(1))N$?
- 上轮下一步：枚举较小乘数集合 T，建立其单位分数关系超图，并计算分数覆盖数；只保留能用 p-adic 剩余类铺成不交缩放块且给出超过 3/28 遗漏密度的候选。
- 用时：1791.0 秒（硬上限 7200 秒）
- 路线目标：先证伪初始五元块路线可能已过时，再严格复核同类有限配置法的最新进展，并搜索更强 divisor block 或更密的不交赋值铺排。结果是：发现并独立核验了 2026 年预印本的 667/806 上界；未找到更强配置，但得到一个精确、可单独攻击的下一定理。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **字面不等号题面的证伪**（`refuted`）：取 k=1 并检查互异性。；推导：若 |A|≥2，取不同 a,b∈A，则 1/a≠1/b，立即得到被禁止的“不等式解”；单元素集合没有足够的互异变量。因此字面版本恒有 f(N)=1。
  - **独立重建五元块**（`advanced`）：令 D=Div(12)\{1}={2,3,4,6,12}，计算单位分数超图前缀独立数并作赋值铺排。；推导：α 前缀为 (1,2,3,3,3)，故加权遗漏 W=Σ(j−α_j)(1/d_j−1/d_{j+1})=1/4。取 v₂(m)≡0 mod3、v₃(m)≡0 mod2，密度为 (4/7)(3/4)=3/7，得到遗漏密度 3/28，即 f(N)≤(25/28+o(1))N。
  - **证伪 720 配置的有限证书**（`advanced`）：把每个关系乘以 720 化为整数子集和；枚举全部极小超边，对每个前缀检查给定 witness，并用纯整数双分支穷举排除 α+1 大小的独立集。；推导：得到 3622 条极小超边；29 个前缀的 α 全部与 Proposition 1 一致，末端 α(D)=11。最大一次搜索访问 1,453,127 个节点。精确算得 W=139/240、dens(M)=120/403，故遗漏密度为 139/806。
  - **更大 divisor block 扫描**（`inconclusive`）：对 148 个 H≤12000 的两素数、三素数及若干四素数指数盒，枚举精确整数超边，再以 HiGHS MILP 计算前缀独立数作候选排名。；推导：扫描范围包含至多 29 个非平凡除数的多种指数型。720 仍最佳；次名 H=360 给出遗漏 32/195，第三名 H=420 给出 9/56。由于排名阶段使用浮点 MILP，此结果只是可靠的反例搜索，不是“720 在该范围最优”的严格证书。
  - **更密赋值铺排搜索**（`blocked`）：把 720 块视为赋值格中的穿孔盒 B*=[0,4]×[0,2]×[0,1]\{0}，搜索其平移的最大权独立集。；推导：在 [0,15]×[0,9]×[0,6] 的 1120 个候选起点上，MILP 的最优解恰为标准格点 (5r,3s,2t)，共64点；有限权重 937745809/839808000，仍略低于无限标准权重 450/403。没有发现更密铺排。
  - **小 N 边界检查**（`advanced`）：利用正性先证明每个 RHS 分母 b_i>a，再用精确有理数子集和生成超边并穷举最大独立集。；推导：精确得到 f(1),…,f(28)=1,2,3,4,5,5,6,7,8,9,10,10,11,12,12,13,14,15,16,16,17,18,19,19,20,21,22,22。最早禁式在 N=6，由 1/2=1/3+1/6 产生。

- 严格推进：
  - 严格复得旧上界 f(N)≤(25/28+o(1))N。
  - 独立审计通过 Wang 预印本 Theorem 1 的全部有限证书和解析计数，支持更强的 f(N)≤(667/806+o(1))N≈(0.8275434243+o(1))N。
  - 720 块不交性可直接由 v₂(d)∈[0,4]、v₃(d)∈[0,2]、v₅(d)∈[0,1] 分别模 5、3、2 唯一恢复 d 证明。
  - 下界仍是 A=(N/2,N]∩ℕ，给出 f(N)≥⌈N/2⌉：k=1 与互异性矛盾；k≥2 时 RHS≥2/N，而 1/a<2/N。
  - 因此当前严格区间为 (1/2+o(1))N≤f(N)≤(667/806+o(1))N；目标渐近 1/2 尚未闭合。

- 路线证伪/边界检查：
  - 明确区分了输入的“≠”与官方等式题面；字面版本已被完全解决为 f(N)=1，不能与等式版本混用。
  - 检查了 k=1：在等式版本中 1/a=1/b 强迫 a=b，故不会产生允许的互异解。
  - 检查了超边枚举完备性：正项等式强迫每个 b_i>a；乘以公共倍数后是精确整数子集和，不使用浮点分数比较。
  - 只保留极小超边不会改变独立集族：任意非极小禁超边已包含一个极小禁超边。
  - 检查了截断边界：当 N/d_{j+1}<m≤N/d_j 时，mD∩[N] 恰为前缀 D_j；半开区间没有漏计或重计。
  - 检查了渐近密度：对不同素数的赋值限制相乘，并以绝对收敛的赋值分解得到区间计数 δ(v−u)N+o(N)。
  - MILP 扫描及有限赋值铺排结果没有被提升为严格最优性定理；严格的 667/806 只依赖纯整数 verifier。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/301/verify_720.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/301/verify_720.py)：720 除数块的精确超边枚举、逐前缀 witness 检查和整数分支穷举验证器。；命令 `python3 -u verify_720.py`；结果：全部断言通过：minimal_hyperedges=3622，weighted_sum=139/240，dilation_density=120/403，upper_bound=667/806。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/301/verify_720.out](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/301/verify_720.out)：29 个前缀的 α、超边数、搜索节点数和 witness 完整输出。；命令 `python3 -u verify_720.py | tee verify_720.out`；结果：所有前缀均排除了 α+1 大小独立集。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/301/search_divisor_blocks.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/301/search_divisor_blocks.py)：通用 divisor-block 超边枚举与 MILP 排名程序。；命令 `python3 -u search_divisor_blocks.py --max-H 12000 > search_all_12000.out`；结果：完成148个候选；未发现遗漏密度超过 139/806 的配置。此项是浮点 MILP 搜索证据。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/301/search_dilation_packing.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/301/search_dilation_packing.py)：720 穿孔赋值盒的有限最大权铺排搜索。；命令 `python3 -u search_dilation_packing.py --limits 15 9 6 --time-limit 120`；结果：1120点、50696个冲突；HiGHS 返回标准 (5r,3s,2t) 格为有限盒最优解。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/301/brute_small_f.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/301/brute_small_f.py)：等式版本 f(N) 的精确小 N 有理数超图穷举器。；命令 `python3 -u brute_small_f.py 28`；结果：得到并验证 f(1) 至 f(28) 的精确值，f(28)=22。

- 第一阻塞点：有限块方法目前卡在两个相互独立的问题：其一，尚无严格结构定理把任意密度大于 1/2 的集合压入某个固定单位分数配置；其二，即使固定 720 配置，也尚未证明标准赋值铺排在所有可能的不交起点集合中具有最大自然密度。有限计算无法消除无限赋值尾部。
- 下一精确定理：建议下一步精确证明如下加权穿孔盒定理：若 C⊂ℕ₀³ 且平移族 {c+B*:c∈C} 两两不交，其中 B*=[0,4]×[0,2]×[0,1]\{(0,0,0)}，则 Σ_{(r,s,t)∈C}2^{-r}3^{-s}5^{-t}≤450/403。等号由 C={(5i,3j,2k):i,j,k≥0} 达到。该定理若成立，将证明 120/403 是固定 720 块所有按 (v₂,v₃,v₅) 选取的不交缩放族中的最优密度；有限 MILP 已在 [0,15]×[0,9]×[0,6] 上支持它，但尚缺处理无限尾部的严格对偶或递归证书。
- 研究记录：

研究记录：定义 D={2,3,4,5,6,8,9,10,12,15,16,18,20,24,30,36,40,45,48,60,72,80,90,120,144,180,240,360,720}，并以 H(D) 的超边 {d}∪E 表示 1/d=Σ_{e∈E}1/e。若 A 无禁式，则对任意 m，A∩mD 是 H(D) 的独立集。令 D_j 为数值排序的前 j 个元素，计算得到 α(D_j)=(1,2,3,4,4,5,6,7,7,7,8,9,9,9,9,10,10,10,10,10,11,11,11,11,11,11,11,11,11)。取 M={m:v₂(m)≡0 mod5，v₃(m)≡0 mod3，v₅(m)≡0 mod2}。若 m₁d₁=m₂d₂，则三个赋值剩余类分别唯一确定 d_i 的三个素因子指数，故 d₁=d₂、m₁=m₂；所以各 mD 不交。又 dens(M)=[(1/2)/(1−2^{-5})][(2/3)/(1−3^{-3})][(4/5)/(1−5^{-2})]=(16/31)(9/13)(5/6)=120/403。对 N/d_{j+1}<m≤N/d_j，块截断为 mD_j，至少遗漏 j−α(D_j) 个元素。因此总遗漏至少 (120/403)N·Σ_{j=1}^{29}(j−α(D_j))(1/d_j−1/d_{j+1})+o(N)，其中 d₃₀=∞。精确证书给出该和为 139/240，于是遗漏密度为 (120/403)(139/240)=139/806，得到 |A|≤(667/806+o(1))N。此论证只建立新的固定常数上界，完全没有证明 f(N)=(1/2+o(1))N。后续扫描没有找到更强块；最有边界清晰度的推进点是上述加权穿孔盒定理，或放弃不交要求、发展可控制重叠次数的块覆盖不等式。

- 一手来源：

  - [P. Erdős and R. L. Graham, Old and New Problems and Results in Combinatorial Number Theory (1980)](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf)；一手来源：`true`；核验：作者托管的原始专著 PDF 地址及书目信息已找到，但本次正文抓取返回 502，未能从原页定位本题的精确页码；因此不声称核到了原书中的题号或逐字命题。
  - [Xinjun Wang, A 667/806 Upper Bound for Erdős Problem #301 on Unit-Fraction-Free Sets (2026-05-27)](https://doi.org/10.5281/zenodo.20404609)；一手来源：`true`；核验：核对了 Theorem 1、Proposition 1、Lemmas 1–3 及 Appendix A：Theorem 1 声称 f(N)≤(667/806+o(1))N；配置为 Div(720)\{1}，Proposition 1 给出全部 29 个前缀独立数。该预印本尚非同行评审论文。

#### #325

- 精确题面：Let $k\geq 3$ and $f_{k,3}(x)$ denote the number of integers $\leq x$ which are the sum of three nonnegative $k$th powers. Is it true that\[f_{k,3}(x) \gg x^{3/k}\]or even $\gg_\epsilon x^{3/k-\epsilon}$?
- 上轮下一步：对每个3≤k≤10整理现有六变量均值估计的明确指数 θ_k（R≪x^{θ_k}），代入 6/k−θ_k 得到可核验的 f_{k,3} 指数表，优先复算 k=3 的0.91709477。
- 用时：637.6 秒（硬上限 7200 秒）
- 路线目标：先证伪旧路线中不精确的来源归因和“只研究全盒二阶矩即可复算 k=3”的限制，再保留一般能量法，严格推出已发表的 k≥26 强版本、报告宣布的 k≥11 强版本，并把剩余问题压缩为适用于稀疏/光滑变量的混合能量定理。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **精确量词与零坐标检查**（`advanced`）：直接读取 Lean 源码并与论文中正整数版本比较。；推导：正整数三元组构成非负整数三元组的子集，因此所有正整数版本下界都自动适用于题面；零坐标无需额外处理。
  - **全盒二阶矩路线**（`advanced`）：令 r_{k,B}(n)=#{(a,b,c)∈[1,B]^3:a^k+b^k+c^k=n}，R_k(B)=∑_n r_{k,B}(n)^2。；推导：对 A_k(B)={a^k+b^k+c^k:1≤a,b,c≤B}，Cauchy 给 B^6≤|A_k(B)|R_k(B)。因此 R_k(B)≪B^{3+η} 给 |A_k(B)|≫B^{3−η}。
  - **证伪旧来源层级**（`refuted`）：逐项核对 2004、2005 完整论文与 2019 报告。；推导：完整已发表且直接可核查的阈值至少是 Salberger 2005 的 d>25；d≥11 来自 2019 作者报告中的 Theorem 1，目前未定位到完整证明论文。
  - **复算 k=3 指数机制**（`advanced`）：核对 Wooley Theorems 1.1、1.2 与论文末页的 Cauchy 推论。；推导：1−0.24871567/3=0.9170947766…。但分母是一个经典变量加两个光滑变量的混合能量，不是全盒 R_3(B) 的已知近对角估计。
  - **小盒精确反例搜索**（`inconclusive`）：枚举无序三元组并以置换重数1、3、6恢复有序表示函数，计算 k=3,…,12、B=20,40,80,120 的能量。；推导：置换对角精确为 D(B)=36·C(B,3)+9B(B−1)+B=6B^3−9B^2+4B。k=3 的 R/B^3 从6.2935升至7.5526；k=4的非对角/B^3从0.1485降至0.1240；k≥7在该范围未见非置换碰撞。
  - **高次范围闭合**（`advanced`）：把 Salberger 的能量渐近代入 Cauchy，并严格处理 x 截断。；推导：取 B=⌊(x/3)^{1/k}⌋，则3B^k≤x且B^3≫_k x^{3/k}。故 R_k(B)≪B^3 立即给 f_{k,3}(x)≫_k x^{3/k}。

- 严格推进：
  - 完全依赖已发表完整论文，可严格得到所有 k≥26 的强版本。
  - 若接受 Salberger 2019 作者报告中标为 Theorem 1 的结果，则强版本范围提升为所有 k≥11；该来源层级已明确标注。
  - Salberger 2005 的 d≥9 粗估还给 f_{d,3}(x)≫_{d,ε}x^{(5/2+1/80)/d−ε}，距目标指数3/d仍差39/(80d)。
  - 更强地，若 R_k(B)=6B^3+o(B^3)，则盒 [1,B]^3 产生的不同和值数满足 |A_k(B)|∼B^3/6，而不只是 ≫B^3。
  - Wooley 的 k=3 指数已独立复算；2026一手论文确认其仍为无条件纪录。

- 路线证伪/边界检查：
  - 有限枚举没有反驳 R_k(B)≪B^{3+ε}；R_3(B)/B^3 缓慢上升仍可能被 B^ε 吸收。
  - k≥7、B≤120 未发现非置换碰撞绝不能外推为不存在非平凡解。
  - 旧路线中“整理全盒六变量均值即可复算 k=3 的0.917”过窄；Wooley 实际使用经典×光滑×光滑的混合矩。
  - 旧材料将 k≥11 写成已有依据没有错，但若理解成已定位完整同行评审证明则过强；当前只定位到作者会议报告。
  - 零坐标、重复坐标和有序/无序计数均已分别检查；重复坐标已包含在精确对角公式中。
  - 对 ε≥3/k 的弱命题指数非正且平凡；真正障碍仅为0<ε<3/k。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/325/enumerate_moments.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/325/enumerate_moments.py)：精确枚举不同和值、有序二阶矩、置换对角及非对角碰撞；另用笛卡尔积暴力法在 k=3,4,7、B=2,4,7 独立交叉核验。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/325 && python3 -m py_compile enumerate_moments.py && python3 enumerate_moments.py --ks 3 4 5 6 7 8 9 10 11 12 --Bs 20 40 80 120 --output moment_data.csv`；结果：语法检查及独立小例交叉核验通过；生成40行精确数据，每行满足 ordered_triples=B^3。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/325/moment_data.csv](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/325/moment_data.csv)：k=3,…,12及四个B值的精确枚举表，含 distinct_sums、second_moment、permutation_diagonal、off_diagonal及归一化比值。；命令 `sed -n '1,41p' /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/325/moment_data.csv`；结果：共41行（表头加40行数据）。

- 第一阻塞点：原问题仍被3≤k≤10阻塞。现有结果没有给这些次数的 B^{3+o(1)} 全盒或混合能量；尤其 k=3 的最佳混合能量仍损失 δ₆=0.24871567。另一个文献性阻塞是尚未找到 Salberger 2019、k≥11 改进的完整证明论文。
- 下一精确定理：对每个固定3≤k≤10，构造集合 S_{1,B},S_{2,B},S_{3,B}⊂[1,B]，满足 |S_{1,B}||S_{2,B}||S_{3,B}|≥B^{3−o(1)}，并证明 E_k(S_1,S_2,S_3):=#{(a_i,b_i)∈S_i^2:∑_{i=1}^3a_i^k=∑_{i=1}^3b_i^k}≤B^{3+o(1)}。这将逐量词推出弱版本；若三个集合有固定正密度且 E_k≪_kB^3，则推出强版本。
- 研究记录：

研究记录如下。固定k并令
\[
r_B(n)=\#\{(a,b,c)\in[1,B]^3:a^k+b^k+c^k=n\},\qquad R_k(B)=\sum_n r_B(n)^2.
\]
这里R_k(B)恰为方程
\[
a_1^k+a_2^k+a_3^k=b_1^k+b_2^k+b_3^k,
\qquad 1\le a_i,b_i\le B
\]
的有序六元解数。又有\(\sum_nr_B(n)=B^3\)，故
\[
B^6\le |\operatorname{supp}r_B|R_k(B). \tag{1}
\]
取\(B=\lfloor(x/3)^{1/k}\rfloor\)。当x充分大时，\(B\ge\tfrac12(x/3)^{1/k}\)，且每个盒中和值不超过x。因此
\[
f_{k,3}(x)\ge |\operatorname{supp}r_B|\ge B^6/R_k(B). \tag{2}
\]
这闭合了截断、常数依赖及正整数到非负整数的转移。

对置换对角作精确核算。无序三元组中，全异、恰有两个相等、全相等的个数及有序重数分别为\(\binom B3,6\)、\(B(B-1),3\)、\(B,1\)。故对角能量为
\[
D(B)=36\binom B3+9B(B-1)+B=6B^3-9B^2+4B. \tag{3}
\]
若一个和值s对应q_s个无序三元组，其置换重数为w_u∈{1,3,6}，则
\[
R_k(B)-D(B)=2\sum_s\sum_{u<v}w_uw_v.
\]
盒像集相对全部\(M=\binom{B+2}{3}\)个无序三元组的损失满足
\[
M-|A_k(B)|=\sum_s(q_s-1)\le\frac{R_k(B)-D(B)}2. \tag{4}
\]
所以Salberger型渐近\(R_k(B)=6B^3+O(B^{3-\delta})\)实际给
\[
|A_k(B)|=\binom{B+2}{3}+o(B^3)\sim B^3/6. \tag{5}
\]
Salberger 2005 Remark 4.7 对d>25给出所需渐近，故k≥26的强版本完全闭合。2019报告将同一结论宣布到d≥11，条件于采用该报告定理，式(2)–(5)同样闭合。

低次时必须放宽“全盒”限制。对任意\(S_i\subset[1,B]\)，令
\[
r_S(n)=\#\{(a_1,a_2,a_3)\in S_1\times S_2\times S_3:\sum a_i^k=n\}.
\]
同样有
\[
|\operatorname{supp}r_S|\ge
\frac{(|S_1||S_2||S_3|)^2}{E_k(S_1,S_2,S_3)}. \tag{6}
\]
Wooley在k=3取一个经典变量及两个光滑变量；正交性把分母化为Theorem 1.2的\(\int|F|^2|f|^4\)，其上界为\(P^{3+\delta_6}\)。论文末页由Cauchy得到
\[
f_{3,3}(x)\gg x^{1-\delta_6/3-\varepsilon},\qquad
1-\frac{0.24871567}{3}=0.9170947766\ldots.
\]
因此幸存路线的正确形式是(6)的混合能量准则，而不是仅要求全盒R_k(B)。当前没有证明3≤k≤10所需的\(B^{3+o(1)}\)混合能量，故不能声称完整证明或反例。

- 一手来源：

  - [FormalConjectures/ErdosProblems/325.lean](https://github.com/google-deepmind/formal-conjectures/blob/c252a41054125b5fd9c8356e2137cd9b55337657/FormalConjectures/ErdosProblems/325.lean)；一手来源：`true`；核验：第 IsSumThreePower 定义量化 a,b,c:ℕ，因此允许零；强版对所有 k≥3，弱版对所有 ε>0、k≥3 量化。
  - [Wooley, Sums of three cubes, II](https://www.math.purdue.edu/~twooley/publ/20150506sum3cub2.pdf)；一手来源：`true`；核验：Theorem 1.1 给 N(X)≫X^β，β=0.91709477。Theorem 1.2 给混合矩 ∫|F(α;P)^2f(α;P,R)^4|dα≪P^{3+δ₆}，δ₆=0.24871567；第23页说明 Cauchy 推出指数 1−δ₆/3。
  - [Salberger, Counting rational points on hypersurfaces of low dimension](https://www.numdam.org/item/10.1016/j.ansens.2004.10.005.pdf)；一手来源：`true`；核验：Corollary 4.6 估计非置换六元解；Remark 4.7 明确给 d>25 时全部正整数解 N_d(B)=6B^3+O_{d,ε}(B^{3−δ})，并给 d≥9 时 N_d(B)=O_{d,ε}(B^{7/2−1/80+ε})。
  - [Salberger, Equal sums of three dth powers, Oberwolfach Report 50/2019](https://ems.press/content/serial-article-files/46829)；一手来源：`true`；核验：报告中的 Theorem 1 (Salberger 2019) 及其紧接推论明确陈述：d≥11 时 n_d(B)=6B^3+O_d(B^{3−δ})；d≥5 时 n_d(B)=O_d(B^{7/2−δ})。这是作者本人报告的新结果陈述，但正文不是完整证明论文。
  - [Browning–Heath-Brown, Equal Sums of Three Powers](https://ora.ox.ac.uk/objects/uuid%3A1fd05b3e-cd34-4b65-a95e-590af2e523dc/files/m4c717ccd310e4b8622a4423c5dcf3075)；一手来源：`true`；核验：该完整论文的 Theorem 与 Corollary 给 d≥33 的非平凡解 o(B^3)、二阶矩及不同和值渐近；因此不能把它误引为 k≥11 的证明。
  - [Maynard, Sums of three positive cubes](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.70554)；一手来源：`true`；核验：2026年5月论文的 Theorem 1.2 仍称 Wooley 的 β=0.91709477… 为 current world record，未发现更新的 k=3 无条件指数。

#### #332

- 精确题面：Let $A\subseteq \mathbb{N}$ and $D(A)$ be the set of those numbers which occur infinitely often as $a_1-a_2$ with $a_1,a_2\in A$. What conditions on $A$ are sufficient to ensure $D(A)$ has bounded gaps?
- 上轮下一步：写出一个纯组合版本：从任意 d*(A)>δ 出发构造有限 F（目标 |F|≤⌈1/δ⌉ 型界），证明 F+D(A)=ℤ；逐项检查由有限窗口中的高重叠到“无穷多次出现”的对角抽取。
- 用时：589.5 秒（硬上限 7200 秒）
- 路线目标：证伪并闭合“正上 Banach 密度 d*(A)>0 ⇒ D(A) syndetic”的纯组合路线，避免对应原理的回译缺口，并给出有限平移覆盖式。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **先证伪对应原理捷径**（`blocked`）：区分普通差集 A−A 与无限差集 D(A)，检查模型中的正测度重叠能否回译成原集合内无穷多次出现。；推导：普通的 d*(A)>0⇒A−A syndetic 不够，因为某个差可能只出现有限次；必须证明 d*(A∩(A−d))>0 或直接控制有限交平移族。原路线的对应原理回译虽可标准化，但旧分析没有写出所需不等式。
  - **极大“几乎不交”平移族**（`advanced`）：把 Følner 证明中的互不相交改成两两交集有限。；推导：若 b−b'∉D(A)，则 (A−b)∩(A−b') 有限。沿同一列见证 d*(A)=δ 的长区间，所有固定平移 A−b 的密度仍趋于 δ，而有限二重交集的归一化大小趋于零。因此任何 D(A)-独立有限集 B 都满足 |B|δ≤1。
  - **极大族到半开区间**（`advanced`）：从有限极大独立集推出覆盖式，再按 Lean 的有符号半开区间定义检查端点。；推导：极大性和 D(A)=−D(A) 给出 ℤ=B+D(A)。若 b₋=min B、b₊=max B，对任意 z 向覆盖式代入 t=z+b₊，所得 d=t−b∈D(A) 满足 z≤d≤z+b₊−b₋；取 M=b₊−b₋+1 即有 d<z+M。
  - **周期模型穷举证伪**（`advanced`）：对周期集合 A={n:n mod q∈S} 穷举所有 q≤12、非空 S⊆ℤ/qℤ 及全部候选平移族。；推导：此时 D(A) 模 q 恰为 S−S。程序验证最大独立族大小不超过 ⌊q/|S|⌋，且任一贪心极大族覆盖全部剩余类。

- 严格推进：
  - 定理候选已闭合：若 A⊆ℕ 的正上 Banach 密度 d*(A)=δ>0，则存在非空有限 B⊆ℤ，使 |B|≤⌊1/δ⌋ 且 ℤ=B+D(A)。
  - 这严格推广了文献 Theorem 2 的密度假设：正上自然密度为正蕴含正上 Banach 密度为正，反之不成立。这里只声称假设上的推广，不声称文献优先权。
  - 证明不需要紧致性、测度系统或 Khintchine 回归，因而消除了初始路线最主要的回译缺口。
  - 平移数有纯密度界，但 gap bound M 不能只由 δ 控制；Stewart–Tijdeman 在密度 1/3 下构造了 gap 长度可任意大的例族。

- 路线证伪/边界检查：
  - D(A) 的对称性来自交换有序对；δ>0 保证 A 无限，故 0∈D(A)。这闭合了极大族中 z∈B 的覆盖情形。
  - 若 I_n 见证 d*(A)=δ，则 |A∩(I_n+b)|与|A∩I_n|至多相差 |(I_n+b)△I_n|≤2|b|；因此最终有限 B 的全部平移确实共用同一密度子列。
  - 若 b−b'∉D(A)，交集 (A−b)∩(A−b') 不仅密度为零，而且是有限集：x↦(x+b,x+b') 与该固定差的有序对集合双射。
  - δ>1/2 时界迫使 |B|=1，从而 D(A)=ℤ；δ=1/2 的偶数集合给出 D(A)=2ℤ、|B|=2 的边界模型。
  - δ=0 不能推出结论：A={2^n:n≥0} 满足 D(A)={0}，因为每个非零固定差只有有限种二进制因子分解；故正密度阈值在此路线中不可直接删除。
  - 周期穷举覆盖空集之外的全部 q≤12 模式，包括单点、全剩余系和取整等号情形；未发现符号、覆盖或基数界反例。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/332/periodic_falsification.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/332/periodic_falsification.py)：周期模型穷举器；计算 S−S，穷举独立平移族，并检查贪心极大族的覆盖性。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/332 && python3 periodic_falsification.py --max-q 12`；结果：PASS：检查 8178 个非空周期模式和 22,353,252 个候选平移族，无反例；脚本亦通过 python3 -m py_compile。

- 第一阻塞点：当前充分条件定理本身没有遗留证明缺口。真正阻塞仍是开放问题的范围：哪些远弱于正上 Banach 密度的条件仍足以保证 D(A) syndetic，尚未刻画。实时检索也未找到明确写出本次“正上 Banach 密度、无限次差集、|B|≤1/δ”三者组合的原命题，因此不能声称新颖性或优先权。
- 下一精确定理：下一步可加强为“popular recurrent differences”版本：对 δ=d*(A)>0、0<ε<δ²，证明 R_ε={d∈ℤ:d*(A∩(A−d))>δ²−ε} syndetic。该命题需要完整重建对应原理的不等式方向与 Khintchine 回归，不能由本次有限交论证直接得到。
- 研究记录：

将 A 视为 ℤ 的子集，并定义 d*(A)=limsup_{N→∞} sup_x |A∩[x,x+N)|/N=δ>0。选择 |I_n|→∞，使 |A∩I_n|/|I_n|→δ。

称有限 B⊆ℤ 为独立的，如果不同 b,b'∈B 都满足 b−b'∉D(A)。对这种 B，令 E_b=A−b。若 x∈E_b∩E_{b'}，则 x+b,x+b'∈A 且其差为 b−b'；反之亦然。因此 b−b'∉D(A) 恰说明 E_b∩E_{b'} 有限。

对固定 b，有
| |E_b∩I_n|−|A∩I_n| |≤|(I_n+b)△I_n|≤2|b|,
故 |E_b∩I_n|/|I_n|→δ。由二项容斥下界，
|⋃_{b∈B}(E_b∩I_n)|≥∑_{b∈B}|E_b∩I_n|−∑_{\{b,b'\}⊆B}|E_b∩E_{b'}|。
右端第二项是与 n 无关的有限常数。除以 |I_n| 并令 n→∞，左端至多为 1，得到 1≥|B|δ，因此 |B|≤⌊1/δ⌋。

从 B₀={0} 开始：若 B_j 不是极大独立集，就加入一个仍保持独立的整数。上述统一基数界保证过程至多进行 ⌊1/δ⌋−1 次，故得到有限极大独立集 B。由于 δ>0，A 无限，所以 0∈D(A)；交换有序对又给出 D(A)=−D(A)。对 z∉B，极大性说明存在 b∈B，使 z−b∈D(A)；对 z∈B 则 z=b+0。因此
ℤ=B+D(A)。

最后令 b₋=min B、b₊=max B。给定任意 z∈ℤ，对 t=z+b₊ 使用覆盖式，写 t=b+d，其中 b∈B、d∈D(A)。于是
z≤d=z+b₊−b≤z+b₊−b₋。
取 M=b₊−b₋+1>0，便有 z≤d<z+M，逐项满足 Lean 的 HasBoundedGaps 定义。这个证明完整解决了所选充分条件，但题面要求寻找条件而非验证预先指定的唯一命题，所以不标记 candidate_full_proof。

- 一手来源：

  - [Erdős Problems #332](https://www.erdosproblems.com/332)；一手来源：`true`；核验：页面给出精确题面并标记 OPEN；截至页面所示 2025-10-28 编辑状态，没有评论声称完整或部分解决。
  - [Stewart–Tijdeman, On Infinite-Difference Sets](https://doi.org/10.4153/CJM-1979-085-6)；一手来源：`true`；核验：Theorem 2（p.898）证明：若 A 的正上自然密度为 e>0，则存在 r≤e^{−log 3/log 2} 个整数平移，使这些 D(A) 平移覆盖 ℕ₀，因而 D(A) 无任意长空隙。文中 D 取非负差。
  - [Stewart, On difference sets of sets of integers](https://www.numdam.org/item/SDPP_1977-1978__19_1_A4_0/)；一手来源：`true`；核验：综述的 Theorem 2 记载正上自然密度充分；Theorem 5 还明确说正上密度序列的 infinite-difference set 有界间隙。
  - [Beiglboeck, An ultrafilter approach to Jin's theorem](https://arxiv.org/abs/0908.2872)；一手来源：`true`；核验：正文首页复述 Følner 的 d*(C)>0⇒C−C syndetic，并给出极大互不相交平移族证明。该结论针对至少出现一次的普通差集，不能直接替代本题的无限次差集。
  - [FormalConjectures Erdős 332 definition](/home/biostar/work/projects/amra/data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/332.lean)；一手来源：`true`；核验：D_A 使用有符号整数差及无限有序对集合；HasBoundedGaps 要求每个半开区间 [z,z+M) 与集合相交。文件本身仍是 answer(sorry) 占位。

#### #377

- 精确题面：Is there some absolute constant $C>0$ such that\[\sum_{p\leq n}1_{p\nmid \binom{2n}{n}}\frac{1}{p}\leq C\]for all $n$ (where the summation is restricted to primes $p\leq n$)?
- 上轮下一步：继续把小素数按 base-p 位数 j 分层，即 n^{1/(j+1)}<p≤n^{1/j}；先对固定 j=2 写出两位无进位条件对应的二维区间，并检验筛上界求和是否仍为 O(1/j^2)。若能得到对 j 可求和的界，才可能闭合全范围。
- 用时：938.8 秒（硬上限 7200 秒）
- 路线目标：先检验旧路线的大素数筛估计，再尝试按 base-\(p\) 位数分层。结论是：大素数部分可严格保留，但旧筛推导有漏洞；更关键的是，设想中的逐层统一 \(O(1/j^2)\) 界被显式族严格反驳。
- 结论：`route_refuted`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **复核大素数短区间筛**（`refuted`）：对 \(p>\sqrt{2n}\) 写 \(q=\lfloor n/p\rfloor\)，精确求出允许区间。；推导：无进位等价于 \(p\in I_q=(2n/(2q+1),n/q]\)，且 \(|I_q|=n/[q(2q+1)]\)。标准 Brun–Titchmarsh 型界自然给出 \(\log |I_q|\)，不能直接替换为旧分析所需的 \(\log(n/q)\)。因此旧逐段求和论证不成立。
  - **修复大素数结论**（`advanced`）：直接使用素数倒数的 Mertens 定理。；推导：不论数字条件如何，\[\sum_{\sqrt{2n}<p\le n,\,p\nmid B_n}\frac1p\le\sum_{\sqrt n<p\le n}\frac1p=\log 2+o(1).\]有限的小 \(n\) 可吸收到绝对常数。因此旧路线的大素数 \(O(1)\) 结论成立，但无需短区间筛。
  - **证伪逐位数层的可求和统一界**（`refuted`）：固定奇素数 \(p\)，构造 \(n_k=(p^k-1)/2\)。；推导：\(n_k\) 的 base-\(p\) 展开由 \(k\) 个数字 \((p-1)/2\) 组成，故 \(p\nmid B_{n_k}\)。又 \(p^{k-1}\le n_k<p^k\)，所以 \(p\) 位于分层 \(n_k^{1/k}<p\le n_k^{1/(k-1)}\)，即层号 \(j=k-1\)。取 \(p=3\) 得每个 \(j\ge1\) 都有某个 \(n\) 使该层贡献至少 \(1/3\)。
  - **有限反例与峰值搜索**（`advanced`）：利用 \(B_n/B_{n-1}=2(2n-1)/n\) 递推维护所有素数的 \(p\)-adic 指数，并与 Kummer 数字判据独立核对。；推导：扫描全部 \(n\le10^7\)，仅出现13个严格新纪录；最大纪录为 \(f(3250)=1.1792429057944813\)。这只是有限计算，不能证明全局有界。

- 严格推进：
  - 严格证明 \(p>\sqrt{2n}\) 部分一致有界；事实上更一般地，对任意固定 \(\alpha>0\)，\(p>n^\alpha\) 的全部素数倒数和为 \(\log(1/\alpha)+O(1)\)。
  - 严格反驳了初始 next_action 中“对每个层号 \(j\) 取得统一 \(O(1/j^2)\) 后求和”的方案；任何趋于零的统一层界都不可能成立。
  - 定位了量词错误：固定小素数可在任意高位数层重新出现，所以不能先对每层取 \(\sup_n\) 再对层号求和。
  - 给出精确核心归约：若能证明 \(\sum_{p\le n^{1/3},\,p\nmid B_n}1/p=O(1)\)，则由 Mertens 对 \(n^{1/3}<p\le n\) 的估计立即得到原题。

- 路线证伪/边界检查：
  - 检查了显式族的层号：\(n_k<p^k\) 而非 \(n_k\ge p^k\)，故对应 \(j=k-1\)；结论仍对任意大 \(j\) 成立。
  - 初版计算程序曾错误把 \(p>n\) 的二项式素因子计入求和；终点 Kummer 交叉核对检出该错误，修正后通过。
  - 对小 \(n\) 直接用整数二项式检查了 Kummer 判据；与逐数字条件一致。
  - \(n=3250\) 的缺失素数包含 \(3,5,7\)，但有限峰值及 \(n\le10^7\) 搜索均不能排除远处稀有峰值。
  - Sander 的定理只有一位条件和 \((\log p)/p\) 权，未将其误写成全数字条件或 \(1/p\) 权的结论。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/377/compute_extrema.cpp](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/377/compute_extrema.cpp)：线性筛与中央二项式 p-adic 递推程序；输出纪录点、大素数贡献和 base-p 位数层贡献，并在终点以 Kummer 判据独立核对。；命令 `g++ -O3 -std=c++17 compute_extrema.cpp -o compute_extrema && ./compute_extrema 10000000 > extrema_1e7.csv`；结果：N=10000000，664579个素数，13个纪录点，最大纪录 f(3250)=1.1792429057944813，cross_check=OK。源码 SHA-256：d2aca80ec8d394aa96b04ca5afd999209c87949114f2479850f9ab4e95ffe87f。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/377/extrema_1e7.csv](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/377/extrema_1e7.csv)：扫描所得全部纪录点及分层贡献。；命令 `tail -20 extrema_1e7.csv`；结果：最后一个新纪录为 n=3250；此时 p>√(2n) 层约0.289875，至少5位层约0.676190。文件 SHA-256：8d1490c74dadad99232200294fbbe0979f28e7f59e4bc5f6c745a31bf3596fdb。

- 第一阻塞点：必须联合控制素数大小和位数层，保留同一个 n 在不同层之间的相关性。固定素数族 \(n=(p^k-1)/2\) 表明，任何逐层取最坏情形再用可求和上界的策略都必然失败。现有的一位指数和估计也不能控制小素数的全部 base-p 数字。
- 下一精确定理：精确的下一定理应是“小素数核心引理”：证明存在绝对常数 \(A\)，使所有 \(n\) 都满足 \[\sum_{p\le n^{1/3}\atop p\nmid\binom{2n}{n}}\frac1p\le A.\]这一定理不会被固定素数显式族反驳，并与 Mertens 的 \(n^{1/3}<p\le n\) 常数界合并后闭合原题全部量词。证明它必须对 \((p,j)\) 二维区域整体估计，而不能逐层取 \(\sup_n\)。
- 研究记录：

研究记录如下。由 Legendre–Kummer，\[v_p\!\binom{2n}{n}=\sum_{a\ge1}\left(\left\lfloor\frac{2n}{p^a}\right\rfloor-2\left\lfloor\frac n{p^a}\right\rfloor\right),\]每一项为0或1；因此 \(p\nmid\binom{2n}{n}\) 当且仅当每个余数 \(n\bmod p^a<p^a/2\)，等价于所有 base-\(p\) 数字不超过 \((p-1)/2\)。在 \(p>\sqrt{2n}\) 时只有最低位可能产生进位。写 \(n=qp+r\)，条件成为 \(r\le(p-1)/2\)，即 \(2n/(2q+1)<p\le n/q\)。但区间长度为 \(n/[q(2q+1)]\)，标准短区间筛产生的是该长度的对数，不能合法地产生旧分析中的 \(\log(n/q)\)。幸而整个大素数范围直接满足 \(\sum_{\sqrt n<p\le n}1/p=\log2+o(1)\)，故结论得以修复。

真正致命的是逐层量词。令 \(L_j(n)=\sum_{n^{1/(j+1)}<p\le n^{1/j},\,p\nmid B_n}1/p\)。固定奇素数 \(p\)，取 \(n=(p^{j+1}-1)/2\)。其 base-\(p\) 数字全为 \((p-1)/2\)，所以 \(p\nmid B_n\)；同时 \(p^j\le n<p^{j+1}\)，故 \(p\) 正好属于第 \(j\) 层。于是 \(L_j(n)\ge1/p\)，特别地 \(\sup_nL_j(n)\ge1/3\) 对每个 \(j\) 成立。故不存在任何可求和的统一层主项，初始的 \(O(1/j^2)\) 目标被严格反驳。

计算使用递推 \(B_n/B_{n-1}=2(2n-1)/n\)，维护各 \(v_p(B_n)\)，再以 \(\sum_{p\le n}1/p-\sum_{p\le n,p\mid B_n}1/p\) 得到 \(f(n)\)。扫描到 \(10^7\) 未发现超过 \(1.1792429057944813\) 的值，但这不关闭任何无限量词。幸存路线只能改为整体控制小素数：证明 \(p\le n^{1/3}\) 的核心引理；其余素数由 Mertens 至多贡献 \(\log3+O(1)\)。

- 一手来源：

  - [P. Erdős, R. L. Graham, I. Z. Ruzsa, E. G. Straus, On the Prime Factors of the Central Binomial Coefficient](https://doi.org/10.1090/S0025-5718-1975-0369288-3)；一手来源：`true`；核验：第84页 Fact 给出：\(p\nmid B_n\) 当且仅当 \(n\) 的全部 base-\(p\) 数字均小于 \(p/2\)。Theorem 2、3分别给出一阶、二阶平均；第90页明确指出固定 \(n\) 后跨素数的反向控制仍缺失。
  - [J. W. Sander, On a Sum over Primes, Hardy–Ramanujan Journal 17 (1994), 32–39](https://hrj.episciences.org/129/pdf)；一手来源：`true`；核验：主定理对一位余数条件及权 \((\log p)/p\) 给出主项 \(\tfrac12\log n\)。第4节明确说明该方法不足以处理所需的 \(1/p\) 权；小素数区间已经产生过大贡献。
  - [FormalConjectures Erdős Problem 377](https://github.com/google-deepmind/formal-conjectures/blob/9e126a6e1f7d108ced5904c43cac46b1c39b39cb/FormalConjectures/ErdosProblems/377.lean)；一手来源：`true`；核验：Lean 题面量词为 \(\exists C>0,\forall n\)，求和只含 \(p\le n\)，与输入精确题面一致；相关定理仍标为 research open。
  - [Croot–Mousavi–Schmidt, On a conjecture of Graham on the p-divisibility of central binomial coefficients](https://arxiv.org/abs/2201.11274)；一手来源：`true`；核验：该文研究有限个指定素数的低重数整除，不能推出重数为零，也不能给出本题的一致倒数和界。定向检索中未找到解决本题精确量词的一手论文或可检查形式化证明。

#### #539

- 精确题面：Let $h(n)$ be such that, for any set $A\subseteq \mathbb{N}$ of size $n$, the set\[\left\{ \frac{a}{(a,b)}: a,b\in A\right\}\]has size at least $h(n)$. Estimate $h(n)$.
- 上轮下一步：逐引理审计 ProofCouncil 的高维正部差集构造，重点检查维数选择、边界计数，以及由 \(\mathbb Z_{ 3e0}^d\) 指数向量嵌入互异整数时是否完整保持 \(Q(A)\)。
- 用时：933.1 秒（硬上限 7200 秒）
- 路线目标：逐引理审计高维正部差集构造，寻找边界反例和量词漏洞；随后检验能否仅靠调整各悬挂层宽 \(K\) 改善 \(e^{O(\sqrt{\log n})}\) 损失。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **先证伪正部差集桥**（`advanced`）：逐方向检查素因子指数映射、负坐标平移、空素数集及维数随 \(n\) 变化。；推导：对 \(n\ge2\)，集合中至少有一个大于 1 的数，故相关素数集非空；唯一分解给出 \(v(a/\gcd(a,b))=(v(a)-v(b))^+\)。反向对任意 \(F\subset\mathbb Z^d\) 先平移到 \(\mathbb Z_{\ge0}^d\)，再令 \(a_x=\prod p_i^{x_i+t_i}\)。这精确保留 \(D(F)\)，且不限制整数大小或维数。
  - **加强平方根下界**（`advanced`）：用普通差集而非固定基点单射。；推导：若 \(q=|D(F)|\)，则 \(x-y=(x-y)^+-(y-x)^+\)，故 \(F-F\subset D(F)-D(F)\)。又 \(|F-F|\ge2n-1\)，而一个 \(q\) 元集合至多有 \(q(q-1)+1\) 个差，因此 \(2n-1\le q(q-1)+1\)，即 \(q\ge(1+\sqrt{8n-7})/2\)。
  - **二维基带边界审计**（`advanced`）：逐条计数论文 Lemma A.5，并与初始二维带状路线对照。；推导：取 \(L=W^2\) 及 \(B_W=\{(i,j):0\le i,j\le L,\ L\le i+j\le L+W-1\}\)。则 \(|B_W|=\sum_{t=0}^{W-1}(L-t+1)\ge W^3/2\)。正部差若两坐标皆正，其和至多 \(W-1\)；否则落在长度 \(L\) 的坐标轴段，故 \(|D(B_W)|\le3W^2\)。普通差由 \(z_1\) 和 \(z_1+z_2\) 决定，故 \(|B_W-B_W|\le(2W^2+1)(2W-1)\le6W^3\)。包括 \(W=1\) 在内均成立。
  - **Separated suspension 全分支审计**（`advanced`）：检查同层、正层差、负层差和普通差集的精确计数。；推导：取 \(M>\max|x_i-x'_i|\)，令 \(\mathcal S_K(F)=\{(j,x+jM\mathbf1,y-jM\mathbf1):0\le j<K,\ x,y\in F\}\)。同层至多产生 \(q^2\) 个正部差；层差 \(a>0\) 时符号被严格分离，每个 \(a\) 至多产生 \(r=|F-F|\) 个值，两方向共 \(2(K-1)r\)。普通差首坐标确定层差，其余两块独立遍历 \(F-F\)，故精确等于 \((2K-1)r^2\)。未发现重合、符号或注入性漏洞。
  - **迭代与任意 n 的量词审计**（`advanced`）：追踪幂次、常数和从规模至少 n 截取到恰好 n。；推导：取 \(K=W\)，递推 \(a_{s+1}=2a_s+1\)、\(b_{s+1}=2b_s=a_s+1\)，从 \((3,2)\) 得 \(a_s=2^{s+2}-1\)、\(b_s=2^{s+1}\)。常数满足 \(M_{s+1}\le3M_s^2\)，故 \(\log M_s=O(2^s)\)。任取构造中的 n 元子集只会缩小正部差集。选择 \(2^s\asymp\sqrt{\log n}\) 闭合显式上界。
  - **证伪“只调层宽常数即可改善损失”**（`refuted`）：令每层 \(K=k_sW\)，先连续优化其齐次主常数，再解析归一化递推。；推导：写 \((m,q,r)\sim(AW^a,BW^b,RW^a)\)，递推为 \(A'=kA^2,B'=B^2+2kR,R'=2kR^2\)。令 \(N=B/A^{b/a}\)、\(V=R/A\) 并写 \(k=tA^{1/a}\)，则 \(V'=2V^2\)，且 \(N'=(N^2+2tV)t^{-\alpha'}\)，其中 \(\alpha'=(a+1)/(2a+1)\)。其全局最优点为 \(t=\alpha'N^2/[2V(1-\alpha')]\)。由于 \(V_s\) 双指数增长，最优证明常数仍为 \(\exp(\Theta(2^s))\)。这严格排除了“保持同一计数递推、仅调整 \(k_s\)”的子路线；它不排除利用实际差集重合或全新构造。
  - **Lean 独立构建审计**（`inconclusive`）：核对公开模块说明并尝试取得源码。；推导：论文 A.2 和仓库 README 的形式化范围一致，但网络沙箱无法取得所有 raw 模块，因而没有执行 lake build，也没有独立搜索全部 sorry/axiom。

- 严格推进：
  - 完整复核了 Theorem A.1 的非形式化证明链：等价桥、加强下界、基带、悬挂、迭代、常数控制、任意 n 截取与最终优化均闭合。
  - 初始固定基点单射只给 \(h(n)\ge\sqrt n\)；普通差集论证严格加强为 \(h(n)\ge(1+\sqrt{8n-7})/2\)。
  - 识别出当前构造的真正瓶颈不是维数或素数编码，而是普通差集比率：悬挂满足 \(r'/m'\approx2(r/m)^2\)，导致证明常数按 \(\exp(\Theta(2^s))\) 增长。
  - 在同一齐次计数递推内，逐层调节 \(K=k_sW\) 无法改变上述常数级障碍；要改善次指数因子，必须利用被上界忽略的差集重合，或改变悬挂操作。
  - 确认 FormalConjectures 的 0 对象差异不能直接与原题逐字等同；本次全部数学证明均在 \(\mathbb Z_{>0}\) 上陈述。

- 路线证伪/边界检查：
  - 检查 \(n=1\)：素数集合可能为空，论文单独以 \(A=\{1\}\)、\(F=\{0\}\) 处理。
  - 检查 \(W=1\)：内部正整数三角形为空，但 \(|D(B_1)|=3\)，所有界仍成立。
  - 检查严格分离条件必须是 \(M>\max|x_i-x'_i|\)，若只取等号会出现零坐标并破坏分支公式；脚本使用直径加一。
  - 检查悬挂产生负坐标不是漏洞：向量阶段允许 \(\mathbb Z^d\)，最后统一平移后才作素数幂编码。
  - 检查固定维与变维量词：每个 n 只需存在某个有限维构造，故选择随 n 增长的 \(d_s=3\cdot2^s-1\) 合法。
  - 检查规模大于 n：任取 n 元子集后 \(D(F')\subseteq D(F)\)，无需精确命中构造规模。
  - 检查优化边界：\(2^s\le\sqrt{\log n}<2^{s+1}\) 仅对充分大 n 使用；有限个小 n 可吸收到绝对常数 C 中。
  - 小规模穷举覆盖了非对称集合和负坐标集合，避免程序只验证高度对称的带状特例。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/539/verify_539.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/539/verify_539.py)：穷举基带、separated suspension 和素数指数桥；包括四类非对称/负坐标样本。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/539 && python3 verify_539.py --max-w 7 --max-k 5 > verification_539.json`；结果：全部 assert 通过；脚本 SHA-256 为 efcc3545354eef735efbbf2ed5290d483bd6e4ddd57e9798f2eef0177d4fbce1。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/539/verification_539.json](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/539/verification_539.json)：基带 W=1,…,7 与悬挂 K=1,…,5 的逐参数计数。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/539 && sha256sum verification_539.json`；结果：输出 SHA-256 为 5857df01f4439b717cba76383d29c695da07bc1957d658fcca5b6a7361417673；例如 W=7 得 (m,q,r)=(329,114,1245)。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/539/optimize_suspension_constants.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/539/optimize_suspension_constants.py)：在 \(K=k_sW\) 的连续松弛中优化每层齐次主常数，采用稳定的对数递推。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/539 && python3 optimize_suspension_constants.py --max-depth 12 > optimized_constants_539.json`；结果：所有深度优化成功；最优常数的对数除以 \(2^s\) 在 s=12 时约为 1.04168，与解析得到的 \(\Theta(2^s)\) 障碍一致。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/539/optimized_constants_539.json](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/539/optimized_constants_539.json)：各深度的最优 log k、目标常数和归一化数值。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/539 && sha256sum optimized_constants_539.json`；结果：输出 SHA-256 为 0bf1788d921549f12645629ea7413cfe82ce11e31e67d275741f1680dfd593e4。

- 第一阻塞点：当前悬挂把两个普通差独立组合，精确产生 \((2K-1)r^2\) 个普通差，使 \(r/m\) 每层近似平方；同一计数模板因此不可避免地产生 \(\exp(\Theta(2^s))\) 的深度常数。尚无能控制该普通差集爆炸、同时保留 \(Km^2\) 个点的新提升操作。
- 下一精确定理：一个清晰且足以推进的下一定理是：存在绝对常数 C，使对所有深度 s 和 n，\[h(n)\le \exp(Cs^2)n^{\alpha_s},\qquad \alpha_s=\frac{2^{s+1}}{2^{s+2}-1}.\]这把当前固定深度常数 \(\exp(O(2^s))\) 改为 \(\exp(O(s^2))\)；取 \(s\asymp\log_2\log n\) 将立即推出 \(h(n)\le\sqrt n\exp(O((\log\log n)^2))\)。本次障碍分析表明，证明它必须利用跨层正部差的额外重合或引入不同于独立笛卡尔平方的构造。
- 研究记录：

研究记录。令 \(x^+=(\max(x_i,0))_i\)、\(D(F)=(F-F)^+\)，并令 \(H(n)\) 为所有有限维整数向量 n 元集的最小 \(|D(F)|\)。素因子指数满足
\[
v_p\!\left(\frac a{\gcd(a,b)}\right)=\max(v_p(a)-v_p(b),0),
\]
而任意 \(F\subset\mathbb Z^d\) 经平移和互异素数幂编码可反向实现，故 \(h(n)=H(n)\)。这也说明维数随 n 增长和中间向量含负坐标均合法。

下界方面，\(F-F\subset D(F)-D(F)\)。整数线性泛函可在 F 上取单射，投影后的一维 n 元集有至少 \(2n-1\) 个差。因此若 \(q=|D(F)|\)，则
\[
2n-1\le |F-F|\le |D(F)-D(F)|\le q(q-1)+1,
\]
从而
\[
h(n)\ge\frac{1+\sqrt{8n-7}}2.
\]
这严格强于旧路线中的 \(n\le q^2\)。

基例取 \(L=W^2\) 及
\[
B_W=\{(i,j):0\le i,j\le L,\ L\le i+j\le L+W-1\}.
\]
直接得到
\[
|B_W|=\sum_{t=0}^{W-1}(L-t+1)\ge\tfrac12W^3,
\quad |D(B_W)|\le3W^2,
\quad |B_W-B_W|\le6W^3.
\]
正部差的内部点满足坐标和至多 W−1；其余点落在两条坐标轴上。这一边界描述在 W=1 时也正确。

核心提升为
\[
\mathcal S_K(F)=\{(j,x+jM\mathbf1,y-jM\mathbf1):0\le j<K,\ x,y\in F\},
\]
其中 \(M\) 严格大于 F 的坐标直径。记 \(m=|F|,q=|D(F)|,r=|F-F|\)，则逐层差分类给出
\[
|\mathcal S_K(F)|=Km^2,
\quad |D(\mathcal S_K(F))|\le q^2+2(K-1)r,
\quad |\mathcal S_K(F)-\mathcal S_K(F)|=(2K-1)r^2.
\]
最后一个等式是精确的：首坐标确定层差，两个普通差独立变化。

取 \(K=W\)，并写
\[
a_s=2^{s+2}-1,\qquad b_s=2^{s+1}.
\]
归纳得到维数 \(d_s=3\cdot2^s-1\) 的集合满足
\[
|F_s(W)|\ge c_sW^{a_s},\quad |D(F_s(W))|\le C_sW^{b_s},
\quad |F_s(W)-F_s(W)|\le T_sW^{a_s},
\]
且 \(\log(1/c_s)+\log C_s+\log T_s=O(2^s)\)。于是
\[
h(n)\le e^{A2^s}n^{b_s/a_s}
=e^{A2^s}n^{1/2+1/(2a_s)}.
\]
令 \(2^s\asymp\sqrt{\log n}\)，即得 \(h(n)\le\sqrt n e^{C\sqrt{\log n}}\)，所有 n 的量词由截取 n 元子集和吸收有限小 n 闭合。

本次额外分析了可变层宽。若 \(K=kW\)，并在齐次计数模板中写 \((m,q,r)\sim(AW^a,BW^b,RW^a)\)，则
\[
A'=kA^2,\qquad B'=B^2+2kR,\qquad R'=2kR^2.
\]
置 \(N=B/A^{b/a}\)、\(V=R/A\)、\(k=tA^{1/a}\) 和 \(\alpha'=(a+1)/(2a+1)\)，化为
\[
V'=2V^2,\qquad N'=(N^2+2tV)t^{-\alpha'}.
\]
对 t 的唯一极小点为
\[
t_*=\frac{\alpha'N^2}{2V(1-\alpha')}.
\]
由于 V 的递推与 t 无关且近似双指数，最优 N 的对数仍为 \(\Theta(2^s)\)。所以只重调每层 K 的常数不能改善当前证明的 \(e^{O(\sqrt{\log n})}\) 因子；突破点必须是降低普通差集爆炸或利用当前并集上界丢失的重合。

没有声称解决 \(h(n)=\Theta(\sqrt n)\)。此外，公开论文明确说显式次指数界尚未完全 Lean 化；本次因网络沙箱未能独立构建作者 Lean 工程，故只把 Appendix A.1 的逐式纸面审计与本地有限计算作为证据。

- 一手来源：

  - [ProofCouncil: An LLM Agent for Solving Open Mathematical Problems, Appendix A](https://arxiv.org/pdf/2607.09474)；一手来源：`true`；核验：Theorem A.1 给出上述双边界；Lemma A.2 是整数余因子与正部差集的等价；Lemma A.5 是二维基带；Lemma A.6 是 separated suspension；Propositions A.7–A.8 给出迭代指数。A.2 明确说明 Lean 覆盖指数极限，但不覆盖显式 \(\sqrt n e^{C\sqrt{\log n}}\) 上界。
  - [ProofCouncil 作者仓库及 Lean 项目说明](https://github.com/eth-sri/proof-council/tree/main/lean)；一手来源：`true`；核验：README 列出 NumberBridge、Base、Suspension、Iteration、Main 等模块及 Lean 4.29.1/mathlib 4.29.1 构建说明。受本次网络沙箱限制，未能下载全部模块并独立执行 lake build，故不声称完成了内核级复验。
  - [Erdős Problem #539](https://www.erdosproblems.com/539)；一手来源：`true`；核验：截至页面 2026-06-15 更新仍标 open，并记录 \(h(n)\le n^{1/2}e^{O(\sqrt{\log n})}\) 及 \(h(n)=n^{1/2+o(1)}\)。
  - [The Set of Differences of a Given Set](https://doi.org/10.2307/2589556)；一手来源：`true`；核验：核实 Granville–Roesler 论文的期刊、卷期、页码和 DOI；本次未取得可搜索的期刊正文，因此不为其附加未核实的定理编号。
  - [FormalConjectures/ErdosProblems/539.lean](https://github.com/google-deepmind/formal-conjectures/blob/c252a41054125b5fd9c8356e2137cd9b55337657/FormalConjectures/ErdosProblems/539.lean)；一手来源：`true`；核验：源码仍把 \(n^{2/3}\) 写作最佳已知上界变体，且 IsCofactorLowerBound 允许非负整数和 0；它没有编码 2026 新界。

#### #635

- 精确题面：Let $t\geq 1$ and $A\subseteq \{1,\ldots,N\}$ be such that whenever $a,b\in A$ with $b-a\geq t$ we have $b-a\nmid b$. How large can $\lvert A\rvert$ be? Is it true that\[\lvert A\rvert \leq \left(\frac{1}{2}+o_t(1)\right)N?\]
- 上轮下一步：把 Elliott 不等式代入 f=1_A 的常数和端点误差完整写出，得到一个显式误差（例如 O_t(N/√log log N) 量级），再检查能否通过分块或迭代采样改善；这是可逐行核验的下一步。
- 用时：659.7 秒（硬上限 7200 秒）
- 路线目标：独立核验并显式化“素数倍数采样”路线，检查端点和常数；同时搜索反例及 t=2 的精确极值模式。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **先证伪局部倍数链断言**（`advanced`）：把违例按差 d 分类，并逐一检查链端点。；推导：若 d≥t，则 d,2d,…,Md（M=⌊N/d⌋）中不能同时选择相邻两项；反之任何违例 a<b 可唯一写成 a=kd、b=(k+1)d，其中 d=b−a。因此局部约束与原题完全等价，且倍数链中至多取 ⌈M/2⌉ 项。
  - **显式化 Elliott 路线并检查归一化**（`advanced`）：不用隐藏的 ≪ 常数，直接计算采样向量的 Gram 矩阵并用 Gershgorin 界算子范数。；推导：令 Z_p(n)=1−p1_{p|n}。对不同素数 p,q≤P，利用 |⌊N/d⌋/N−1/d|≤1/N 得 |⟨Z_p/√p,Z_q/√q⟩|≤2P/N；对角元≤1+P/N。因此若 (2|Q|−1)P≤N，则 Gram 算子范数≤2，从而 ∑_{p∈Q}p^{-1}|⟨f,Z_p⟩|²≤2N^{-1}∑|f|²。
  - **推导显式密度误差**（`advanced`）：将局部链上界代入显式采样不等式。；推导：写 α=|A|/N、β_p=(p/N)∑_{p|n}1_A(n)。局部链给 β_p≤1/2+p/(2N)。若 δ=(α−1/2)_+，L=∑_{p∈Q}1/p，则 L(δ−P/(2N))_+²≤2α≤2，故 α≤1/2+P/(2N)+√(2/L)。取 P=N^{0.1}、Q={p素数:t≤p≤P}，即得固定 t 下 δ=o(1)；Mertens 估计进一步给 O_t(1/√log log N)。
  - **尝试得到 O(1/log log N) 或 O(log N/N)**（`blocked`）：检查同一二阶矩能量是否可直接线性化。；推导：该 Gram/Elliott 界控制的是 Lδ²，而非 Lδ；直接代入最多给 δ≪L^{-1/2}。没有发现利用现有局部链约束把平方损失改成线性损失的有效步骤。
  - **精确小参数反例搜索**（`inconclusive`）：将问题编码成冲突图最大独立集的二元 MILP，要求零 MIP gap，并重新逐边检查返回集合。；推导：对 t=1 恢复全部已知精确值。对 t=2，N=1,…,500 均未发现超过“全部奇数加 2^k（k为奇数）”的集合；N=750,1000,1500,2000 也恰好达到该构造，但这只是计算证据。

- 严格推进：
  - 证明了原条件精确等价于：对每个整数 d≥t，A∩{d,2d,…,⌊N/d⌋d} 是路径的独立集。
  - 得到有限、显式的采样定理：若 Q 是不小于 t 且不超过 P 的素数集，并满足 (2|Q|−1)P≤N，则 |A|/N≤1/2+P/(2N)+√(2/∑_{p∈Q}1/p)。
  - 逐量词闭合渐近子问：对每个固定 t 和 ε>0，由素数倒数和发散，可先使 L 足够大，再使 P/N 足够小，从而存在 N_0(t,ε)，使所有 N≥N_0 及所有题设 A 都满足 |A|≤(1/2+ε)N。
  - 核验 t=2 下界构造：奇数之间的差为偶数，不能整除奇数；奇数与 2^k 的合法差若整除 2^k，则只能为1<t；两个奇指数幂之差含非平凡奇因子。因此其大小为 ⌈N/2⌉+#{k≥1:k奇且2^k≤N}。

- 路线证伪/边界检查：
  - 检查了 b−a|b 与 b−a|a 的等价性，避免方向错误。
  - 保留了 M=⌊N/p⌋ 及 ⌈M/2⌉ 的端点误差，得到准确的 p/(2N) 项。
  - 检查 t>N−1 的边界：此时 F_t(N)=N；这不冲突于固定 t、N→∞ 的结论。
  - 精确计算中 t=1、奇偶 N 均恢复 F_1(N)=⌊(N+1)/2⌋。
  - t=2 精确公式候选在全部 N≤500 及若干 N≤2000 的实例中没有反例，但未将此有限检验提升为证明。
  - 公开 Lean 链接只能到达需要 JavaScript 的编辑器，未能恢复并检查源代码；故未把“已有 Lean 形式化”作为证明依据。
  - 未找到约1980年 Erdős 致 Ruzsa 信件或 Gu83/Ru99 中可公开检查、精确对应本题的原始正文。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/635/exact_extrema.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/635/exact_extrema.py)：生成边 {kd,(k+1)d}、求最大独立集 MILP，并独立验证返回集合。；命令 `python3 exact_extrema.py --N 10 20 30 40 50 75 100 150 200 --t 1 2 3 4 5 8 10`；结果：全部实例求解成功且 mip_gap=0；t=1 回归检验通过。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/635/exact_extrema.jsonl](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/635/exact_extrema.jsonl)：N≤200 的选定网格精确优化输出。；命令 `python3 exact_extrema.py --N 10 20 30 40 50 75 100 150 200 --t 1 2 3 4 5 8 10 > exact_extrema.jsonl`；结果：未发现渐近上界反例；有限 N 的超额随 t 增大，但相对 N 下降。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/635/exact_extrema_large.jsonl](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/635/exact_extrema_large.jsonl)：N≤2000 的选定较大实例。；命令 `python3 exact_extrema.py --N 300 500 750 1000 1500 2000 --t 2 3 5 10 > exact_extrema_large.jsonl`；结果：例如 t=2 时最优值依次为154,254,380,505,755,1005，与已知幂构造相等。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/635/t2_all_N_500.jsonl](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/635/t2_all_N_500.jsonl)：t=2、全部1≤N≤500的公式候选反例搜索。；命令 `python3 exact_extrema.py --N $(seq 1 500) --t 2 --check-t2-formula > t2_all_N_500.jsonl`；结果：500个实例均为零 MIP gap，未出现 beats_t2_construction=true。

- 第一阻塞点：Elliott/Gram 二阶矩只产生 Lδ²≲1，其中 L≈log log N，因此无法逼近构造所示的 Θ(log N) 次主项。精确极值需要使用不同结构，尤其要同时利用不同 d 的路径约束之间的强依赖。
- 下一精确定理：最清晰的下一定理是 t=2 的精确候选：F_2(N)=⌈N/2⌉+#{k≥1:k为奇数且2^k≤N}。较稳健的中间目标是先证明 F_2(N)≤N/2+O(log N)。计算已支持精确式至 N=500（并检查若干 N≤2000），但尚无覆盖全部 N 的注入、匹配或对偶证书。
- 研究记录：

设 f=1_A，α=N^{-1}∑_{n≤N}f(n)。任何违例都有唯一形式 (a,b)=(kd,(k+1)d)，其中 d=b−a≥t；故对 M_d=⌊N/d⌋，序列 f(d),…,f(M_dd) 不含相邻的两个1，从而

∑_{d|n, n≤N}f(n)≤⌈M_d/2⌉≤M_d/2+1/2.  (1)

特别对素数 p≥t，令 β_p=(p/N)∑_{p|n}f(n)，则

β_p≤1/2+p/(2N).  (2)

下面给出不依赖隐藏常数的采样估计。取素数集 Q⊆[t,P]，在 [N] 上使用归一化内积 ⟨g,h⟩=N^{-1}∑g(n)h(n)，并令 Z_p=1−p1_{p|n}。写 e_d=⌊N/d⌋/N−1/d，则 |e_d|≤1/N。若 p≠q，直接展开得

⟨Z_p,Z_q⟩=−pe_p−qe_q+pq e_{pq},

故

|⟨Z_p/√p,Z_q/√q⟩|≤(p+q+pq)/(N√{pq})≤2P/N.  (3)

对角元满足

⟨Z_p,Z_p⟩/p=1−1/p+(p−2)e_p≤1+P/N.  (4)

因此当 (2|Q|−1)P≤N 时，Gram 矩阵每行绝对值和至多2；由其正半定性和 Gershgorin 定理，算子范数至多2。于是

∑_{p∈Q}(1/p)|α−β_p|²=∑_{p∈Q}|⟨f,Z_p/√p⟩|²≤2⟨f,f⟩=2α.  (5)

令 δ=(α−1/2)_+、L=∑_{p∈Q}1/p。由 (2)，α−β_p≥δ−P/(2N)。若 δ>P/(2N)，代入 (5) 得

L(δ−P/(2N))²≤2α≤2,

而另一种情形结论更直接。因此有限形式为

|A|/N≤1/2+P/(2N)+√(2/L).  (6)

固定 t，取 P=N^{0.1} 及 Q={p素数:t≤p≤P}。因 |Q|≤P，条件 (2|Q|−1)P≤N 对充分大 N 成立；又因删去有限多个素数不影响 ∑1/p 的发散，L→∞，而 P/N=N^{-0.9}→0。(6) 遂严格给出 |A|≤(1/2+o_t(1))N。采用 Mertens 的素数倒数和估计，可写成 |A|≤N/2+O_t(N/√log log N)。

该证明只解决题面的渐近是非子问，不决定 F_t(N) 的真实次主项。t=2 的下界为全部奇数加奇指数二次幂，大小是 ⌈N/2⌉+#{k奇:2^k≤N}=N/2+Θ(log N)。精确 MILP 显示它在已检范围内就是最优，但有限计算不能替代一般证明。

- 一手来源：

  - [Terence Tao, 254A Notes 9 – second moment and entropy methods, Exercise 8](https://terrytao.wordpress.com/2019/11/12/254a-notes-9-second-moment-and-entropy-methods/)；一手来源：`true`；核验：Exercise 8 精确给出 Elliott 采样平方和不等式：对 p≤|I|^{0.1}，以 1/p 加权的采样误差平方和受 ||f||_2² 控制；正文同时指出素数倒数和仅为 log log 量级。
  - [P. D. T. A. Elliott, Probabilistic Number Theory I: Mean-Value Theorems](https://link.springer.com/book/10.1007/978-1-4612-9989-9)；一手来源：`true`；核验：出版社页核实作者、1979 年版、Grundlehren 第239卷及 DOI。未能从可访问正文独立核对被转引的 Lemma 4.7，故本记录不依赖该编号。

#### #679

- 精确题面：Let $\epsilon>0$ and $\omega(n)$ count the number of distinct prime factors of $n$. Are there infinitely many values of $n$ such that\[\omega(n-k) < (1+\epsilon)\frac{\log k}{\log\log k}\]for all $k<n$ which are sufficiently large depending on $\epsilon$ only? Can one show the stronger version with\[\omega(n-k) < \frac{\log k}{\log\log k}+O(1)\]is false?
- 上轮下一步：把修正后的 P_r 构造写成引理，并用一个明确可引用的 p_r=r(log r+loglog r−1+O(loglog r/log r)) 估计逐项验证常数 c；这也会彻底排除先前候选的“小 k”漏洞。
- 用时：806.5 秒（硬上限 7200 秒）
- 路线目标：先证伪评论中“紧邻 n 的最大 primorial”选取，再以后退一级的 primorial 重建第二问的定量反证，并判断该路线能否跨越第一问所需的固定乘法因子 1+ε。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **证伪紧邻 primorial 选取**（`refuted`）：令 Q_j=∏_{i≤j}p_i，代入无限序列 n=Q_j+1。；推导：此时最大的严格小于 n 的 primorial 是 Q_j，而评论所取 k=n−Q_j=1。由于题面要求 k≥统一阈值 K，且 K 可大于 1，这个见证不能排除该无限序列的 n。
  - **后退一级的修复**（`advanced`）：对每个大 n，唯一取 M 使 Q_M<n≤Q_{M+1}，令 k=n−Q_{M−1}。；推导：有 k>Q_M−Q_{M−1}=Q_{M−1}(p_M−1)→∞，k<n≤Q_{M+1}，且 n−k=Q_{M−1}，所以 ω(n−k)=M−1。结合 primorial 的二阶渐近，取 c=1/2 即可得到 ω(n−k)>log k/loglog k+c log k/(loglog k)^2。
  - **尝试推进第一问**（`blocked`）：估计修复见证的乘法比值。；推导：由 Q_{M−1}(p_M−1)<k<Q_{M+1} 得 log k∼M log M，故 log k/loglog k∼M，而 ω(n−k)=M−1；因此 ω(n−k)/(log k/loglog k)→1。对每个固定 ε>0，该见证最终反而满足 (1+ε) 界，不能反驳第一问；只检查一个 k 也不能证明第一问。
  - **短区间高 ω 路线**（`inconclusive`）：核对 Lau 的条件反证。；推导：Lau 的 Conjecture 8 断言某类 ω(m)≥C₀log₂m/log₃m 的整数出现在指定对数长度短区间内；Theorem 7.3 证明它蕴含存在 δ>0，使每个充分大 n 都有 1≪k<n 且 ω(n−k)>(1+δ)log k/loglog k。该短区间猜想目前未证。

- 严格推进：
  - 设 A_m=log Q_m=∑_{j≤m}log p_j。由 Axler 式 (1.1) 的 p_j∼jlog j，有 log p_j=log j+loglog j+o(1)。Cesàro 求和、Stirling 公式及 ∑_{j≤m}loglog j=m loglog m+o(m) 给出 A_m=m(log m+loglog m−1)+o(m)。
  - 令 L=log m、ℓ=loglog m。由 A_m=m(L+ℓ−1+o(1))，得到 log A_m=L+ℓ+o(1)，从而 A_m/log A_m=m−m/L+o(m/L)。
  - 同理 A_m/(log A_m)^2=m/L+o(m/L)。因此若 F(x)=log x/loglog x、H(x)=log x/(loglog x)^2，则 F(Q_m)=m−m/log m+o(m/log m)，H(Q_m)=m/log m+o(m/log m)。
  - 在修复构造中置 m=M+1，则 ω(n−k)=m−2 且 k<Q_m。F 在 x>e^e 后递增，H 在 x>e^{e²} 后递增，故 F(k)+(1/2)H(k)≤F(Q_m)+(1/2)H(Q_m)<m−2，最后一个不等式来自 (1−1/2)m/log m−2+o(m/log m)>0。
  - 由 k→∞ 且 H(k)→∞，对任意固定 K,C，充分大 n 的上述见证满足 k≥K 且 (1/2)H(k)>C，所以 ω(n−k)>F(k)+C。这逐项关闭了第二问标准统一 O(1) 解释下的反证量词。

- 路线证伪/边界检查：
  - 检查了 n=Q_j+1：原选取严格产生 k=1；修复选取产生 k>Q_j−Q_{j−1}。
  - 检查了 n 本身为 primorial：严格条件 Q_M<n≤Q_{M+1} 自动选 M=j−1，没有端点歧义。
  - 穷举 3≤n≤10^6，共 999998 个 n，验证 0<k<n、n−k=Q_{M−1}、ω(n−k)=M−1 以及 k>Q_M−Q_{M−1}。
  - 至 m=200000 检查归一化余量 R_m=((m−2)−F(Q_m))/H(Q_m)；m=100000、200000 时分别约为 1.18348、1.17194，符合 R_m→1，并未发现符号或索引反例。
  - 单独检查 F、H 的单调区间，避免从 k<Q_m 错误推出二阶表达式的上界。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/679/primorial_route_check.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/679/primorial_route_check.py)：用筛法生成素数；以 ∑log p 计算 primorial 渐近余量；穷举检查修复构造的端点、ω 值和严格不等式。；命令 `python3 primorial_route_check.py --max-m 200000 --limit-n 1000000`；结果：全部断言通过。尾段 m≥100000 的归一化余量最小值约 1.171937（m=200000）；有限端点中观察到的最小 k 始终为 Q_M−Q_{M−1}+1。脚本 SHA-256 为 2513d1c8f166529fc3ca99da5d79ff626d6f796611ce47f823e385f71527bb1b。

- 第一阻塞点：primorial 路线产生的超额仅为相对量 Θ(1/loglog k)：ω(n−k)=F(k)(1+O(1/loglog k))。第一问需要固定的乘法增益 1+δ 才能被统一反驳，或需要同时控制所有 k 才能被证明；本路线两者都没有。
- 下一精确定理：清晰的下一目标是 Lau 的 Conjecture 8：证明其指定短区间内总有满足 ω(m)≥C₀log₂m/log₃m 的整数，其中常数满足 1≤d<C₀。Lau 的 Theorem 7.3 已证明该猜想会给出某个固定 δ>0，并对每个充分大 n 产生 1≪k<n、ω(n−k)>(1+δ)log k/loglog k，从而否定第一问。
- 研究记录：

以下给出不依赖旧分析的完整研究记录。所有对数均为自然对数。记 p_j 为第 j 个素数，Q_j=∏_{i=1}^j p_i，Q_0=1。

原评论取最大的 Q_M<n 并令 k=n−Q_M。这个选取在 n=Q_M+1 时给出 k=1，而这种 n 有无穷多个。题面中的“k sufficiently large depending only on ε”要求统一阈值，故原选取本身存在真实量词缺口。

修复如下。对每个充分大的整数 n，唯一选择 M 使
\[Q_M<n\le Q_{M+1},\]
并定义
\[k=n-Q_{M-1}.\]
于是
\[0<k<n,\qquad n-k=Q_{M-1},\qquad \omega(n-k)=M-1,\]
且
\[k>Q_M-Q_{M-1}=Q_{M-1}(p_M-1)\longrightarrow\infty.\]
这最后一式正是统一大-k量词所需的修复。

现在证明二阶余量。由素数定理的逆形式 p_j∼jlog j，
\[\log p_j=\log j+\log\log j+o(1).\]
误差经 Cesàro 求和仍为 o(m)。另一方面
\[\sum_{j\le m}\log j=m\log m-m+O(\log m),\]
以及由分部积分
\[\sum_{2\le j\le m}\log\log j=m\log\log m+O(m/\log m).\]
故
\[A_m:=\log Q_m=m(\log m+\log\log m-1)+o(m).\]
写 L=log m、ℓ=loglog m，则
\[A_m=m(L+\ell-1+o(1)),\qquad \log A_m=L+\ell+o(1).\]
因此
\[\frac{A_m}{\log A_m}=m-\frac{m}{\log m}+o\!\left(\frac m{\log m}\right),\]
并且
\[\frac{A_m}{(\log A_m)^2}=\frac m{\log m}+o\!\left(\frac m{\log m}\right).\]

设
\[F(x)=\frac{\log x}{\log\log x},\qquad H(x)=\frac{\log x}{(\log\log x)^2}.\]
F、H 对充分大 x 均递增。令 m=M+1；由 k<Q_m，
\[F(k)+\tfrac12H(k)\le F(Q_m)+\tfrac12H(Q_m).\]
右侧为
\[m-\frac12\frac m{\log m}+o\!\left(\frac m{\log m}\right)<m-2=\omega(n-k)\]
（充分大 m）。所以存在绝对常数 c=1/2，使每个充分大 n 都有一个随 n 趋于无穷的 k<n 满足
\[\omega(n-k)>\frac{\log k}{\log\log k}+c\frac{\log k}{(\log\log k)^2}.\]
由于第二项趋于无穷，这严格排除任何统一加法常数版本。

但这没有解决第一问。由修复构造的上下界可得 log k∼Mlog M，因而
\[\frac{\omega(n-k)}{F(k)}\to1.\]
所以对任意固定 ε>0，这个特定见证最终不足以违反 (1+ε)F(k)。要跨越该障碍，需要 Lau Conjecture 8 类型的短区间高 ω 定理；目前只有 Lau Theorem 7.3 给出的条件蕴含，没有无条件证明。

- 一手来源：

  - [Cheuk Fung Lau, On the Number of Prime Factors of Consecutive Integers, arXiv:2604.15042v2](https://arxiv.org/pdf/2604.15042)；一手来源：`true`；核验：Conjecture 4（第2页）重述 #679；Theorem 1.3 证明无穷多个 n 对所有 1<k<n 有 Ω(n−k)≤C log k；Conjecture 8 和 Theorem 7.3（第36–37页）给出第一问的条件反证路线。
  - [Christian Axler, New Estimates for the nth Prime Number](https://cs.uwaterloo.ca/journals/JIS/VOL22/Axler/axler17.pdf)；一手来源：`true`；核验：式 (1.1) 为 p_m∼m log m；式 (1.2) 为 Cipolla 展开。下述修正证明事实上只需式 (1.1)。
  - [Erdős Problem #679 — Discussion thread](https://www.erdosproblems.com/forum/thread/679)；一手来源：`true`；核验：DottedCalculator 于 2026-01-11 的评论明确取“最大的小于 n 的 primorial”，并令 k 为其与 n 的差；该原始选取没有处理 k 可能等于 1。
  - [P. Erdős, Some Unconventional Problems in Number Theory, Acta Math. Acad. Sci. Hungar. 33 (1979), 71–80](https://combinatorica.hu/~p_erdos/1979-23.pdf)；一手来源：`true`；核验：核对了作者站公开扫描件及其书目信息；本轮未在扫描件中定位到题面对应的精确页码或编号，故不虚报。

#### #686

- 精确题面：Can every integer $N\geq 2$ be written as\[N=\frac{\prod_{1\leq i\leq k}(m+i)}{\prod_{1\leq i\leq k}(n+i)}\]for some $k\geq 2$ and $m\geq n+k$?
- 上轮下一步：先固定最小未解决平方值并逐个检验 k=3：化为 \((m+2)^3-(m+2)=N[(n+2)^3-(n+2)]\)，再对所得三次曲线做严格的整数点/Thue 方程归约，而非仅搜索有理点。
- 用时：845.0 秒（硬上限 7200 秒）
- 路线目标：先证伪“平方数均是未处理障碍”，继而分类平方 N 的 k=2 解，并严格排除最小障碍 N∈{4,25,49,64,81} 的全部 k≤4 分支。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

  - **复核非平方 Pell 分支**（`advanced`）：取 k=2、X=2m+3、Y=2n+3，并从 Pell 单位 z²−Nw²=1 构造 X=z+Nw、Y=z+w。；推导：直接计算 X²−NY²=(1−N)(z²−Nw²)=1−N。把单位平方可令 z 为奇数、w 为偶数；取充分高次又使 X−Y=(N−1)w 足够大，闭合 n,m∈ℕ 与 m≥n+2。
  - **证伪“平方分支完全没有 k=2 构造”**（`refuted`）：检查退化差平方方程并搜索因子对。；推导：得到合法反例 36=(8·9)/(1·2)，即 k=2,n=0,m=7。更一般地，所有平方根 a≡2 mod 4、a≥6 都有 n=(a−6)/4、m=(a²−8)/4。
  - **平方 N 的 k=2 完全分类**（`advanced`）：固定 Y=2n+3，把方程改写为 Pell 方程。；推导：若 N=a²，则 X²−(Y²−1)a²=1。Y+√(Y²−1) 是基本正单位，故全部解恰由 (Y+√(Y²−1))^r=X_r+A_r√(Y²−1)、r≥2 给出，其中 a=A_r。
  - **素数幂平方与 k=4 降阶**（`advanced`）：先排除 N=p^{2e} 的 k=2，再以四连积恒等式降到 k=2。；推导：写 a=p^e、q=m+1、r=n+1。由 q(q+1)=a²r(r+1) 得 ar<q<a(r+1)−1；令 q=ar+ℓ，则 1≤ℓ≤a−2 且 a∣ℓ(ℓ+1)，与 a 为素数幂矛盾。另有 P₄(t)=4P₂((t²+5t)/2+1)，所以任何 k=4 表示诱导同一 N 的 k=2 表示。
  - **平方障碍的 k=3 无条件 Thue 证书**（`advanced`）：对 N∈{4,25,49,64,81}，令 X=m+2、Y=n+2、D=gcd(X,Y)、X=Dv、Y=Du，并完整求解所得 Thue 方程。；推导：D²(v³−Nu³)=v−Nu。设 A=v³−Nu³，则 A∣N³−N；又 X<NY，所以 A<0。逐一求解 v³−Nu³=−d（d∣N³−N），并检查 (v−Nu)/A 是否为平方。所有正 lift 均不满足 Y≥2、X≥Y+3。

- 严格推进：
  - 非平方 N≥2 的 k=2 构造经独立代数与奇偶性复核成立。
  - 对固定 n、k=2，所有可表示平方可精确描述：若 Y=2n+3，则平方根恰为 Pell 系数 A_r(Y)，r≥2；这部分回答了官方附问的一个非平凡子类。
  - 无限平方族：设 s₀=1、s₁=2Y、s_{j+1}=2Ys_j−s_{j−1}，取 x_j=Ys_j−s_{j−1}，则 N=s_j²、m=(x_j−3)/2 给出合法 k=2 表示。
  - 所有 N=p^{2e} 在 k=2 不可表示；任何 k=4 表示都会降为 k=2。因此 4、25、49、64、81 在 k=2、4 均无表示。
  - 无条件 Thue 枚举进一步证明 4、25、49、64、81 在 k=3 也无表示。故这五个最小平方障碍全部被推进到 k≥5。

- 路线证伪/边界检查：
  - 初拟引理“平方 N 的 k=2 均无解”被 N=36 严格反驳，已废弃。
  - 检查边界 n=0：题面允许自然数零，且 36 的表示满足 m=7≥2。
  - PARI 的默认 thueinit(P,0) 可能依赖 GRH；全部最终证书均改用 flag=1 重算。
  - 用 N=9、16 作正控制：同一程序恢复 (X,Y)=(27,13) 与 (15,6)，分别给出 (m,n)=(25,11)、(13,4)。
  - 未把逐个固定 k 的有限性误写成跨全部 k 的结论；Rakaczki Theorem B 不允许这种量词交换。
  - 未把有限搜索或椭圆曲线正秩信息当成无解证明；k=3 结论依赖的是完整 Thue 解集。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/686/thue_n4_k3.gp](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/686/thue_n4_k3.gp)：N=4、k=3 的12个 Thue 方程无条件枚举和 admissibility 过滤。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/686 && gp -q thue_n4_k3.gp`；结果：只有正 lift (X,Y)=(1,1),(3,2)，两者 admissible 均为0。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/686/thue_square_k3.gp](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/686/thue_square_k3.gp)：对 N=9,16 作正控制，并对 N=4,25,49,64,81 作无条件完整 Thue 枚举。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/686 && gp -q thue_square_k3.gp`；结果：恢复 N=9,16 的已知合法点；其余五个 N 没有 admissible lift。分别枚举12、60、108、168、120个负右端 Thue 方程。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/686/square_family_check.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/686/square_family_check.py)：精确整数验证固定 n 的 Pell 递推平方族、不变量、奇偶性和 m≥n+2。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/686 && python3 square_family_check.py --max-n 3 --terms 4`；结果：全部断言通过；例如 n=0 依次得到 N=36,1225,41616,1413721。

- 第一阻塞点：最小未闭合分支现在是 N=4、k≥5。已有文献只说明每个固定 k>2 的解集有限，没有统一排除全部 k 的机制；因此尚不能声称 N=4 是反例，更不能解决原问题。
- 下一精确定理：精确下一定理：令 F₅(t)=∏_{i=1}^5(t+i)，证明方程 F₅(m)=4F₅(n) 没有满足 n,m∈ℕ、m≥n+5 的解。必须完整确定该五次曲线的相关整数点，或给出等价的可认证 Thue/Thue–Mahler 归约；单纯有界搜索不够。
- 研究记录：

本轮的核心结构是 k=2 的中心化。令 X=2m+3、Y=2n+3，则原方程为 X²−NY²=1−N。非平方 N 时，正 Pell 单位 z+w√N 给出 X=z+Nw、Y=z+w；平方单位保证奇偶性，充分高次保证 m≥n+2。

若 N=a²，则方程不再是固定判别式的 Pell 轨道，而可重排为 X²−(Y²−1)a²=1。因 Y≥3 为奇数，D=Y²−1 非平方，且方程最小正解是 (X,a)=(Y,1)。标准 Pell 单位分类遂给出
(Y+√D)^r=X_r+A_r√D，\qquad a=A_r，r≥2。
反之每个 r≥2 都有 X_r 为奇数且 X_r≥2Y²−1≥Y+4，所以 m=(X_r−3)/2 是自然数并满足 m≥n+2。这是平方 k=2 分支的充要分类，而不只是一个充分族。

对 k=3，写 X=m+2、Y=n+2，则 X³−X=N(Y³−Y)。取 D₀=gcd(X,Y)，X=D₀v、Y=D₀u、gcd(u,v)=1，得到
D₀²(v³−Nu³)=v−Nu.
令 A=v³−Nu³。因为 A∣v−Nu 且 gcd(A,u)=1，在模 A 下 v≡Nu，从而
A∣(N³−N)u³，\qquad A∣N³−N.
又 X<NY，故 A<0。于是每个固定 N 只剩有限个方程 v³−Nu³=−d，d∣N³−N。使用 thueinit(x³−N,1) 完整求解后，N=4,25,49,64,81 都没有满足 Y≥2、X≥Y+3 的点；N=9,16 的正控制则被正确恢复。

最后，若 N=a² 且 a=p^e，k=2 方程在 q=m+1、r=n+1 下迫使 ar<q<a(r+1)−1。余项 q=ar+ℓ 同时满足 1≤ℓ≤a−2 与 a∣ℓ(ℓ+1)，这对素数幂 a 不可能。恒等式
∏_{i=1}^4(t+i)=4(T(t)+1)(T(t)+2)，\qquad T(t)=(t²+5t)/2+1
又把 k=4 降至 k=2。因此上述五个平方数在 k≤4 的排除现已闭合，但无限的 k≥5 仍是本题真正的全称障碍。

- 一手来源：

  - [FormalConjectures, ErdosProblems/686.lean](https://github.com/google-deepmind/formal-conjectures/blob/c252a41054125b5fd9c8356e2137cd9b55337657/FormalConjectures/ErdosProblems/686.lean)；一手来源：`true`；核验：核对了自然数量词；文件将非平方分支标为 solved，将平方总分支、N=4、N=25 标为 open。部分子命题仍含 sorry，故未把标签当作数学证明。
  - [T. H. Chan, The Diophantine equation b(b+1)(b+2)=t a(a+1)(a+2) and gap principle](https://arxiv.org/abs/2408.01306)；一手来源：`true`；核验：Corollary 1 的精确范围是：固定乘数及常数的三连积方程只有有限多个整数解；它支持固定 N、k=3 的有限性，但不直接枚举本题 N=4 等情形。
  - [C. Rakaczki, On the diophantine equation x(x−1)…(x−(m−1))=λy(y−1)…(y−(n−1))+l, Acta Arith. 110 (2003)](https://www.impan.pl/shop/publication/transaction/download/product/83210?download.pdf=)；一手来源：`true`；核验：论文第1页 Theorem B：除明确列出的 λ=1 等例外，等长连续积方程只有有限多个整数解。因此固定 N≠1、固定 k>2 时本题只有有限多个 (m,n)，但这不提供统一的 k 上界。
  - [PARI/GP official catalogue: thue and thueinit](https://pari.math.u-bordeaux.fr/dochtml/html/Polynomials_and_power_series.html)；一手来源：`true`；核验：官方文档说明 thue 返回相应 Thue 方程的全部整数解；thueinit(P,1) 会无条件认证结果，不依赖 GRH。
  - [P. Erdős, Some Unconventional Problems in Number Theory, Acta Math. Acad. Sci. Hungar. 33 (1979), 71–80](https://combinatorica.hu/~p_erdos/1979-23.pdf)；一手来源：`true`；核验：核对了作者站公开扫描件及其书目信息；本轮未在扫描件中定位到题面对应的精确页码或编号，故不虚报。

#### #776

- 精确题面：Let $r\geq 2$ and $A_1,\ldots,A_m\subseteq \{1,\ldots,n\}$ be such that $A_i\not\subseteq A_j$ for all $i\neq j$ and for any $t$ if there exists some $i$ with $\lvert A_i\rvert=t$ then there must exist at least $r$ sets of that size. How large must $n$ be (as a function of $r$) to ensure that there is such a family which achieves $n-3$ distinct sizes of sets?
- 上轮下一步：逐引理核对 He–Tang 的下界证明：从 2 层与 n-2 层的交叉相交结构出发，验证其如何利用第 3、n-3 层排除 n≤2r+2；随后检查上界构造中 2log₂r 项来自何种二进制编码。
- 用时：690.1 秒（硬上限 7200 秒）
- 路线目标：先检验“极端层—交叉相交—中间层”路线能否推出超过 He–Tang 的 $n_0(r)\ge2r+2$；所得候选新结论是：对每个 $r\ge4$，$g(2r+3,r)\le2r-1$，因而 $n_0(r)\ge2r+3$。这不是原问题的完整求解。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

- 独立复核：`PASS`；范围：候选定理：对所有 r >= 4，g(2r+3,r) <= 2r-1；推论 n_0(r) >= 2r+3。它不是 #776 的完整解答。
- 复核方式：一位独立代理逐步审阅证明；主代理独立重跑全部随附计算检查。
- 证据边界：这是内部双重核验后的未发表新结果，尚未经过外部同行评审，也没有闭合 #776 的完整阈值问题。

  - **证伪旧路线叙述**（`refuted`）：逐行比较旧分析与 Proposition 3.1。；推导：旧分析称关键缺口是“迭代影不等式”以及第 $3,n-3$ 层共同排除全部 $n\le2r+2$。原证明实际只需 2-边相交族分类和局部容纳计数；$n<2r+2$ 的矛盾来自第 $r-1,r$ 层，只有端点使用第 3 层。
  - **独立重建共同星归约**（`advanced`）：设 $\mathcal M=\{[n]\setminus A:A\in\mathcal F_{n-2}\}$，研究各有 $r$ 条边的 $\mathcal F_2,\mathcal M$。；推导：若 $\mathcal F_2$ 有两条不交边，则交叉命中它们的 2-集至多四条；$r>4$ 立即矛盾。$r=4$ 等号给出 $K_{2,2}$ 四条横边，但同时命中这四条的 2-集只有原来的两条，也矛盾。因此 $\mathcal F_2$ 两两相交；因其至少四条，只能是星。交叉条件再强迫 $\mathcal M$ 含同一星心。
  - **首个未知点的精确 SMT 搜索**（`advanced`）：在 $n=2r+3$ 固定共同星心及端点星族；按 $|P\cap Q|$ 枚举全部端点同构轨道。内部每个候选集合设布尔变量，逐层恰选 $r$ 个，并禁止所有跨层包含对。；推导：固定 $P$ 后，$Q$ 的轨道只由 $s=|P\cap Q|\in\{0,\ldots,r\}$ 决定，因此搜索穷尽端点配置。
  - **从 UNSAT 提炼一般覆盖引理**（`advanced`）：把内部成员按是否含共同星心分成两个残余布尔格反链，并对第二支取补集。；推导：得到两个 $N=r+2$ 元布尔格中的反链 $\mathcal A,\mathcal C$，其中间轮廓满足 $a_{N-3+j}+c_{N-j}=r$（$j=0,1,2,3$）。由满层不可能出现，推出 $a_{N-3}=c_{N-3}=r$；再由 $(N-1)$ 层至多一个成员，推出 $a_{N-2},c_{N-2}\ge r-1$。将 $\mathcal A_2$ 看成图，高层补集成为大量 2-覆盖和 3-覆盖，最终与覆盖引理矛盾。

- 严格推进：
  - 严格复核了“恰好四个缺失层”：总层数为 $n+1$，出现 $n-3$ 层即缺四层；$r\ge4$ 时若第 1 层出现，则第 $n-r+1,\ldots,n$ 层及第 0 层均缺失，共至少 $r+1\ge5$ 层。对偶地排除第 $n-1$ 层。因此出现层只能是 $2,3,\ldots,n-2$。
  - 证明了覆盖引理：若一个有 $r\ge4$ 条边、$r+2$ 个顶点的图有 $r-1$ 个不同的 2-顶点覆盖，则这些覆盖两两相交；由相交边族分类，它们必须为星。其公共星心单独覆盖原图，故原图本身是 $r$ 边星。任何不包含所选 2-覆盖的 3-覆盖至多一个。
  - 候选新定理的全部 $r\ge4$ 量词已经在草稿中闭合：假设 $g(2r+3,r)\ge2r$，先保留任意 $2r$ 个出现层，再逐层删至恰好 $r$ 个成员；共同星归约和两分支残余反链随后由覆盖引理导出矛盾。因此候选结论为 $g(2r+3,r)\le2r-1$，进而 $n_0(r)\ge2r+3$。
  - 该结论仅改善下界一位；上界仍为 He–Tang 的 $2r+2\log_2r+O(\log\log r)$，故原问题仍未解决。

- 路线证伪/边界检查：
  - $r=4,n=11$ 的五个端点轨道 $|P\cap Q|=0,1,2,3,4$ 均由 Z3 返回 UNSAT。
  - $r=5,n=13$ 的六个端点轨道也全部返回 UNSAT，排除了结论只是 $r=4$ 小参数偶然的初步可能。
  - 覆盖引理对 $r=4$ 的全部 $\binom{15}{4}=1365$ 个标号图及相关 2-覆盖选择进行了穷举，最大允许 3-覆盖数为 1。
  - 覆盖引理对 $r=5$ 的全部 $\binom{21}{5}=20349$ 个标号图也完成穷举，最大值仍为 1；等号例均由星图给出。
  - 特别核查了 $r=4$ 的两个等号例外：两个不交 2-覆盖会迫使原图为 $K_{2,2}$，但该图只有两个 2-覆盖，不能提供所需三个；三角形型的三个相交 2-覆盖又只能共同覆盖至多三条不同边。
  - 独立审阅者逐步核对了共同星归约、残余反链的层指标、覆盖引理与最后的包含方向，结论为 PASS；主代理随后再次重跑 $r=4,5$ 的全部 Z3 轨道及覆盖引理穷举，结果一致。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/776/sat_n2r3.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/776/sat_n2r3.py)：固定共同星端点后的精确 Z3 搜索器，覆盖 $n=2r+3$ 的全部 $|P\cap Q|$ 轨道。；命令 `python sat_n2r3.py --r 4 --timeout-ms 300000 && python sat_n2r3.py --r 5 --timeout-ms 300000`；结果：分别 5 个和 6 个轨道全部 UNSAT。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/776/cover_lemma_check.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/776/cover_lemma_check.py)：覆盖引理在 $r=4,5$ 上的全图穷举审计。；命令 `python cover_lemma_check.py --r 4 && python cover_lemma_check.py --r 5`；结果：$r=4$：1365 个图、300 个相关覆盖族选择，最大值 1；$r=5$：20349 个图、630 个选择，最大值 1。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/776/proof_draft_n2r3.md](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/776/proof_draft_n2r3.md)：候选新下界 $n_0(r)\ge2r+3$ 的自洽英文证明草稿，包含覆盖引理和完整归约。；命令 `sed -n '1,240p' proof_draft_n2r3.md`；结果：草稿已由独立审阅者逐步核对并判定 PASS，且按审阅意见补全了 $g(n,r)>2r$ 时先保留任意 $2r$ 个出现层的量词说明；仍未经过外部同行评审。

- 第一阻塞点：候选新定理已有第二位代理的独立逐步审阅和主代理的复跑核验，但属于未发表的新推导，仍需外部同行评审。继续提高到 $n=2r+4$ 时，残余格变为 $r+3$ 点并出现五个混合层；当前覆盖引理不再直接给出所需的 $r-1$ 个 2-覆盖。
- 下一精确定理：下一精确定理应是判定对所有 $r\ge4$ 是否有 $g(2r+4,r)\le2r$。对应的局部目标是推广覆盖引理：控制一个 $r$ 边图在同时存在连续高层补集反链时的 2、3、4-顶点覆盖轮廓；若该命题为假，则应从其最小覆盖轮廓构造 $n=2r+4$ 的反链。
- 研究记录：

以下给出候选新下界的自洽记录。令 $n=2r+3$，反设 $g(n,r)\ge n-3=2r$；从见证反链中保留任意 $2r$ 个出现层并删去其余层，再逐层删去多余成员，故可设恰有 $2r$ 个出现层且每层恰有 $r$ 个成员。因只能缺四层，而第 1 层出现会额外强迫 $n-r+1,\ldots,n$ 缺失，补集论证同样排除第 $n-1$ 层，故
\[
S(\mathcal F)=\{2,3,\ldots,n-2\}.
\]
设 $\mathcal M=\{[n]\setminus A:A\in\mathcal F_{n-2}\}$。对 $E\in\mathcal F_2,M\in\mathcal M$ 有 $E\cap M\ne\varnothing$。上述交叉相交论证给出
\[
\mathcal F_2=\{\{x,p\}:p\in P\},\qquad
\mathcal M=\{\{x,q\}:q\in Q\},\qquad |P|=|Q|=r.
\]
令 $U=[n]\setminus(\{x\}\cup P)$、$R=[n]\setminus(\{x\}\cup Q)$，则 $|U|=|R|=N=r+2$。含 $x$ 的内部成员必为 $\{x\}\cup Z$、$Z\subseteq U$；不含 $x$ 的成员为避免落在每个 $[n]\setminus\{x,q\}$ 中，必须包含全部 $Q$，故为 $Q\cup W$、$W\subseteq R$。所有 $Z$ 构成 $2^U$ 中的反链 $\mathcal A$；所有 $R\setminus W$ 构成 $2^R$ 中的反链 $\mathcal C$。记层数为 $a_k,c_k$。

原层 $t=r+j$（$j=0,1,2,3$）分解为含 $x$ 支的 $(N-3+j)$ 层和不含 $x$ 支的 $j$ 层；对后者在 $R$ 中取补后得到
\[
a_{N-3+j}+c_{N-j}=r.\tag{1}
\]
低端纯层给出 $a_2=c_2=r$。因此两反链均不含满集，即 $a_N=c_N=0$。由 (1) 的 $j=0,3$ 得
\[
a_{N-3}=c_{N-3}=r.\tag{2}
\]
一个与 $r$ 个不同 2-集均不可比较的 $(N-1)$-集，其补单点必须属于这些 2-集的公共交；公共交至多一个点，所以 $a_{N-1},c_{N-1}\le1$。由 (1) 的 $j=1$ 得
\[
a_{N-2}\ge r-1.\tag{3}
\]
现在把 $\mathcal A_2$ 看作 $U$ 上有 $r$ 条边的图 $G$。$\mathcal A_{N-2}$ 的补集给出至少 $r-1$ 个 2-顶点覆盖，$\mathcal A_{N-3}$ 的补集给出 $r$ 个 3-顶点覆盖；反链性说明前者没有一个包含在后者中。覆盖引理却断言这样的 3-覆盖至多一个：所选 $r-1$ 个 2-覆盖必为星 $\{\{z,p\}:p\in P'\}$，继而 $G$ 本身为以 $z$ 为心的星；避开这些 2-覆盖的 3-覆盖只能是 $z$ 加上剩余两个点。因 $r\ge4$，这与 (2) 的 $r$ 个 3-覆盖矛盾。

故候选结论为 $g(2r+3,r)\le2r-1$，从阈值定义推出 $n_0(r)\ge2r+3$。该记录关闭了这一部分定理的量词，但没有确定 $n_0(r)$，且新证明已通过内部独立审阅，但仍需外部同行评审。

- 一手来源：

  - [Yixin He and Quanyu Tang, An Erdős–Trotter problem on antichains with multiplicity r on each occurring level, arXiv:2602.09803v2](https://arxiv.org/abs/2602.09803)；一手来源：`true`；核验：Remark 1.2 证明“至少 $r$”与“恰好 $r$”对 $g(n,r)$ 等价；Definition 1.3 给出阈值量词；Theorem 1.4、Proposition 3.1 证明 $r\ge4$ 时 $n_0(r)\ge2r+2$；Theorem 1.5 给出上界。最新可见版本为 2026-03-21 的 v2。
  - [He–Tang v2 PDF，Proposition 3.1（页5–7）](https://arxiv.org/pdf/2602.09803)；一手来源：`true`；核验：精确证明范围为 $r+3\le n\le2r+2$；两端 2-集族先化为共同星，随后 $|U|\le r$ 用第 $r-1,r$ 层，端点 $|U|=r+1$ 才使用第 $3,r+1,r+2$ 层。
  - [Erdős Problems #776](https://www.erdosproblems.com/776)；一手来源：`false`；核验：仅用于核对输入题面和网站当前状态，未作为数学证明依据。页面仍列问题为 open，并收录 He–Tang 的已发表范围。未找到可核对的更新论文把下界写成 $2r+3$。

#### #788

- 精确题面：Let $f(n)$ be maximal such that if $B\subset (2n,4n)\cap \mathbb{N}$ there exists some $C\subset (n,2n)\cap \mathbb{N}$ such that $c_1+c_2\not\in B$ for all $c_1\neq c_2\in C$ and $\lvert C\rvert+\lvert B\rvert \geq f(n)$. Estimate $f(n)$. In particular is it true that $f(n)\leq n^{1/2+o(1)}$?
- 上轮下一步：逐项核对 Alon–Pham Theorem 4 的 p 取值范围和多对数常数，并写出从 ℤ/qℤ 到开区间 (2n,4n) 的完整概率事件交集；这可把 n^{3/5+o(1)} 归约整理成可发表的独立引理。
- 用时：821.6 秒（硬上限 7200 秒）
- 路线目标：先检查图归约、端点、自环和模嵌入是否存在反例；幸存后严格推出 f(n)=O(n^{3/5}(log n)^{19/10})，并把平方根目标压缩为仅针对循环群和单一密度范围的精确下一定理。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

- 独立复核：`PASS`；范围：图论归约、无条件平方根量级下界，以及由 Alon–Pham Theorem 4 推出的 O(n^(3/5)(log n)^(19/10)) 上界；原 n^(1/2+o(1)) 猜想仍开放。
- 复核方式：一位独立代理逐步审阅端点、自环、模嵌入、参数平衡和引用范围；主代理另行重跑小规模枚举。
- 证据边界：脚本对 |B| 已不小于当前最优的分支做安全剪枝，因此不是为每个 B 都构图求 alpha；剪枝不影响极值的精确性。理论上界依赖 Alon–Pham 的已陈述定理，未解决平方根目标。

  - **精确图论归约与端点检查**（`advanced`）：把每个 B 对应为和图 G_B，并逐项检查开区间。；推导：V_n={n+1,…,2n−1}，|V_n|=n−1；不同 x,y∈V_n 满足 2n+3≤x+y≤4n−3，因此其和总在 I_n。固定 B 后，最大许可 C 正是 α(G_B)，故 f(n)=min_B(|B|+α(G_B))。
  - **初始模嵌入路线证伪尝试**（`advanced`）：检查是否需要素数、是否会模回绕，以及 B 的大小是否可能膨胀。；推导：无需素数。取 H=ℤ/(2n)ℤ；I_n 的 2n−1 个整数模 2n 恰为全部非零剩余类。给定 S⊆H，令 B_S={b∈I_n:b mod 2n∈S}，则 |B_S|=|S∖{0}|≤|S|。映射 x↦x mod 2n 在 V_n 上单射，且 G_{B_S} 恰为 Γ⁺(H,S) 在该像上的诱导子图。
  - **无条件平方根量级下界**（`advanced`）：利用每个固定和产生一个匹配。；推导：若 m=|B|，则对每个顶点及每个 b∈B 至多有一个邻点 b−x，故 Δ(G_B)≤m。贪心独立集界给出 α(G_B)≥(n−1)/(m+1)，于是对 n≥2，|B|+α(G_B)≥m+(n−1)/(m+1)≥2√(n−1)−1。故 f(n)≥⌈2√(n−1)−1⌉。
  - **Alon–Pham 上界闭合**（`advanced`）：随机选择 S⊆ℤ/(2n)ℤ，每个元素独立以概率 p 入选，并合取独立数事件与大小事件。；推导：Theorem 4 的证明给 α(Γ⁺)≤ξp^{-3/2}(log(2n))^{19/4}，而 Chernoff 给 |S|≤4pn，以高概率同时成立。取 p=(2n)^{-2/5}(log(2n))^{19/10}，两项均为 O(n^{3/5}(log n)^{19/10})。正概率事件保证存在一个确定 S，继而存在确定 B_S。
  - **推进平方根指数**（`blocked`）：把一般随机 Cayley 独立数假设代入参数平衡。；推导：若在相关循环群上有 α≤p^{-c}(log N)^K，则转移给 f(n)≤O(n^{c/(c+1)}(log n)^{K/(c+1)})。现有 c=3/2 产生 3/5；平方根指数需要 c=1+o(1)。检索到的 2024–2026 一手结果均未覆盖 p=N^{-1/2+o(1)}。

- 严格推进：
  - 对所有充分大的 n，严格得到 f(n)=O(n^{3/5}(log n)^{19/10})，从而复核并细化已记录的 f(n)≤n^{3/5+o(1)}。
  - 模 2n 转移比旧路线更直接：不需要 Bertrand 定理、素数选择或“无回绕”论证；B 的大小也不增加。
  - 自环问题已专项检查：采用随机 Cayley-sum 图文献中的简单图约定，只连接不同顶点，正好对应题面量词 c₁≠c₂。
  - 平方根结论实际只需要循环群 ℤ_N、N=2n 和 p=N^{-1/2+o(1)} 附近的独立数界，不需要证明对所有有限群及所有 p 的完整 Conjecture 2。

- 路线证伪/边界检查：
  - 检查了 n=1 退化情形：V_1=∅，故 f(1)=0；上面的平方根下界仅声明于 n≥2。
  - 枚举 n≤12 的全部 B 掩码；对所有未被 |B|≥当前最优值这一安全下界剪枝排除的候选，精确构图并穷举全部顶点子集计算 α。得到 f(1),…,f(12)=0,1,2,3,3,4,4,5,5,6,6,7。
  - 所有实际构图并求独立数的候选均通过 Δ(G_B)≤|B| 检查；被剪枝分支仅因 |B| 本身已不小于当前最优，故不影响 f(n) 的精确性。没有发现简单下界的反例。
  - 程序验证 I_n 模 2n 的剩余类互异，以及每一对不同顶点的整数和与群和完全对应。
  - 检索到的 Nenadov 及 Campos–Dahia–Marciano 定理仅适用于反对数级稀疏度，不能被误用到 p≈N^{-1/2}。
  - 没有把 Alon–Pham 的 Conjecture 2、Conjecture 15 或随机图启发式当作已证平方根上界。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/788/brute_force_788.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/788/brute_force_788.py)：枚举全部小规模 B 掩码；用 |B| 的安全下界剪枝后，对其余候选精确计算独立数，并检查度数及模 2n 转移不变量。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/788 && python3 brute_force_788.py --max-n 12 --output small_n_788.json`；结果：精确得到 n≤12 的上述 f(n) 表；脚本 SHA256 为 c1b91f8a2569bf7bec5d1d73d5bbaa64da8394857d4c011f76e4bf7981e66a44。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/788/small_n_788.json](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/788/small_n_788.json)：穷举输出，包括样例极小化 B、全部结构检查结果及实数下界。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/788 && sha256sum small_n_788.json`；结果：SHA256 为 3ba21eb35a2ed598f9763cb97d87f26da32c0065ec36e4d448c8692ae4b525a0。

- 第一阻塞点：唯一实质阻塞是多项式稀疏随机 Cayley-sum 图的独立数：现有 Alon–Pham Theorem 4 给 p^{-3/2} 量级，而平方根目标要求在 p≈N^{-1/2} 时把它降到 p^{-1}N^{o(1)}。现有反对数稀疏结果无法外推到这一范围。
- 下一精确定理：足够且接近最弱的下一定理是：当 N→∞（至少沿偶数 N）且 p=N^{-1/2+o(1)} 时，随机 S_p⊆ℤ_N 以高概率满足 α(Γ⁺(ℤ_N,S_p))≤p^{-1}N^{o(1)}。更弱的确定性版本也足够：对每个偶数 N，存在 S_N⊆ℤ_N，使 |S_N|≤N^{1/2+o(1)} 且 α(Γ⁺(ℤ_N,S_N))≤N^{1/2+o(1)}。任一版本经上述模 2n 转移立即推出 f(n)≤n^{1/2+o(1)}。
- 研究记录：

研究记录：设 V=V_n、I=I_n。固定 B⊆I，定义简单图 G_B：顶点为 V，不同 x,y 在 x+y∈B 时相邻。题面中“对每个 B 存在 C”逐项等价于
\[
f(n)=\min_{B\subseteq I}\bigl(|B|+\alpha(G_B)\bigr).
\]
下界方面，固定 b 后的边集 {\{x,b-x\}:x,b-x∈V,x≠b-x} 是匹配。因此若 |B|=m，则 Δ(G_B)≤m，贪心给
\[
\alpha(G_B)\ge \frac{|V|}{m+1}=\frac{n-1}{m+1}.
\]
由 AM–GM，
\[
|B|+\alpha(G_B)\ge m+\frac{n-1}{m+1}
=(m+1)+\frac{n-1}{m+1}-1\ge2\sqrt{n-1}-1.
\]
故 n≥2 时 f(n)≥⌈2√(n−1)−1⌉。

上界转移如下。令 H=ℤ/(2n)ℤ。映射 I→H，b↦b mod 2n，是 I 到 H∖{0} 的双射。对 S⊆H 定义
\[
B_S=\{b\in I:b\bmod 2n\in S\}.
\]
于是 |B_S|=|S∖{0}|≤|S|。映射 φ:V→H，φ(x)=x mod 2n，是单射。由于不同 x,y∈V 时 x+y∈I，
\[
x+y\in B_S\iff \phi(x)+\phi(y)\in S.
\]
所以 G_{B_S}=Γ^+(H,S)[φ(V)]，从而 α(G_{B_S})≤α(Γ^+(H,S))。

令 N=2n，并以概率 p 独立选择 S 的每个元素。Alon–Pham Theorem 4 及第3.1节给出某绝对常数 ξ，使以高概率
\[
\alpha(Γ^+(H,S))\le \xi p^{-3/2}(\log N)^{19/4}.
\]
当 pN→∞ 时，Chernoff 同时给 |S|≤2pN。取
\[
p=N^{-2/5}(\log N)^{19/10},
\]
则
\[
pN=N^{3/5}(\log N)^{19/10},
\quad
p^{-3/2}(\log N)^{19/4}=N^{3/5}(\log N)^{19/10}.
\]
两个事件的交概率趋于1，故存在确定的 S 和 B_S，满足
\[
f(n)\le |B_S|+\alpha(G_{B_S})
=O\!\left(n^{3/5}(\log n)^{19/10}\right).
\]
这完整闭合的是 3/5 部分结果，不是原平方根猜想。一般若可将独立数输入改为 p^{-c}(\log N)^K，平衡 pN 与该项得到指数 c/(c+1)。因此现有 c=3/2 的方法本身无法越过 3/5；要达到 1/2，必须取得 c=1+o(1)，至少在循环群和 p=N^{-1/2+o(1)} 的局部范围内如此。

- 一手来源：

  - [Alon–Pham, Random Cayley graphs and random sumsets（作者主页版本）](https://web.math.princeton.edu/~nalon/PDFS/randomss5.pdf)；一手来源：`true`；核验：Theorem 4：任意阶 N 的有限阿贝尔群及 p≤1/2，随机 Cayley 图和 Cayley-sum 图以高概率满足 α≤\widetilde O(p^{-3/2})。第3.1节证明取 s=ξp^{-3/2}(log N)^{19/4}，并称 Cayley-sum 图有同类界。Conjecture 2 猜测改进为 \widetilde O(p^{-1})。
  - [Nenadov, A remark on the independence number of sparse random Cayley sum graphs](https://arxiv.org/abs/2503.02100)；一手来源：`true`；核验：正文题面明确把 Cayley-sum 图定义为仅在不同 x,y 之间、当 x+y∈S 时连边，核实了与本题 c₁≠c₂ 相同的简单图约定；结果只覆盖 p>(log N)^{-1/3+o(1)}，不能处理 p≈N^{-1/2}。
  - [Campos–Dahia–Marciano, On the independence number of sparser random Cayley graphs](https://arxiv.org/abs/2406.09361)；一手来源：`true`；核验：同样明确排除自环；其随机 Cayley-sum 图独立数渐近结果要求 p≥(log N)^{-1/80}，不覆盖本题所需的多项式稀疏区间。
  - [Baltz–Schoen–Srivastav, Probabilistic construction of small strongly sum-free sets via large Sidon sets](https://doi.org/10.4064/cm-86-2-171-176)；一手来源：`true`；核验：期刊页面的精确命题范围给出旧结果 f(n)=O((n log n)^{2/3})；本文没有用于证明新的 3/5 上界。
  - [Choi, On a Combinatorial Problem in Number Theory](https://doi.org/10.1112/plms/s3-23.4.629)；一手来源：`true`；核验：核实了论文书目信息：Proc. London Math. Soc. (3) 23 (1971), 629–642。可访问页面未给出与本题区间版本对应的定理编号，故本记录不据此宣称更精确范围。

#### #827

- 精确题面：Let $n_k$ be minimal such that if $n_k$ points in $\mathbb{R}^2$ are in general position then there exists a subset of $k$ points such that all $\binom{k}{3}$ triples determine circles of different radii. Determine $n_k$.
- 上轮下一步：把等半径冲突视为顶点数为 n、边大小 4至6 的超图，计算其可能的独立数下界是否可由局部度进一步提升；首项可检验任务是严格求 M6 的最大共度并试用局部引理或容器法改进 n^{1/5}。
- 用时：1034.4 秒（硬上限 7200 秒）
- 路线目标：独立审计旧 O(k^5) 冲突计数，优先证伪局部共度改进；随后核对后续一手文献，并寻找真实的上下界推进。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`high`
- 实际尝试：

- 独立复核：`PASS`；范围：冲突计数与删点界、已有 O(k^5/log k) 预印本上界、双曲线高共度反例，以及充分大 k 的抛物面近二次候选新下界；原 n_k 的阶仍未确定。
- 复核方式：一位独立代理逐步审阅组合计数、来源定理、投影与差集优化；主代理重跑随附程序并核对一手预印本。
- 证据边界：近二次下界是本轮未发表的新推导，虽经内部独立审阅仍待外部同行评审；上界来源也尚未正式发表。

  - **复核三类冲突计数**（`advanced`）：按两个等半径三元组的并集大小 j=4,5,6 分类。；推导：固定弦 ab、半径 ρ，至多两个半径 ρ 的圆过 ab；无四共圆使每圆至多含一个额外点。因此 M_4≤n(n−1)(n−2)/4。固定 a,ρ，以 bc 为边当 R(abc)=ρ；该图最大度≤2，边数 s_ρ(a)≤n−1，且 ∑_ρs_ρ(a)=C(n−1,2)，故 M_5≤n(n−2)C(n−1,2)/2。若 t_ρ 是半径 ρ 的三元组数，则每对点至多进入两个这样的三元组，故 3t_ρ≤2C(n,2)，从而 M_6≤(n(n−1)/6)C(n,3)<n^5/36。
  - **优化随机删点常数**（`advanced`）：取 p=6^{1/5}n^{-4/5}，保留点后逐冲突删一点。；推导：令 c=6^{1/5}, A=5c/6。期望剩余数至少 A n^{1/5}−3/2−c^4/(4n^{1/5})。因此 n=ceil((1296/3125)(k+2)^5) 时该期望大于 k，得到显式 n_k≤ceil((1296/3125)(k+2)^5)。这是对旧 (3k)^5 常数的严格改进，但渐近弱于已知 O(k^5/log k)。
  - **尝试用各层顶共度得到对数增益**（`refuted`）：猜测 H_j 的 (j−1)-共度为常数并套一致超图独立集定理。；推导：猜测被反例推翻。取 A=(0,0),B=(1,0),C=(0,2)。对 X=(x,y)，等式 R(XAB)=R(XAC) 的方程分解为 (x²−x+y²−2y)(x²−x−y²+2y)=0。第一因子是圆 ABC；第二因子是非退化双曲线。可在双曲线上泛型选择任意多点并保留 A,B,C，使全体无三共线、无四共圆，而每个新增 X 都给冲突 {A,B,C,X}。故 Δ_3(H_4)可达 n−3。
  - **只处理六点冲突层**（`blocked`）：固定五点，计算 H_6 的五共度并应用 Kostochka–Mubayi–Verstraëte。；推导：延拓点 x 必须与五点中的某一对组成三元组；其余三点固定目标半径。共有至多 C(5,2) 个角色，每个角色至多两个 x，故 Δ_5(H_6)≤20，单层独立数为 Ω((n log n)^{1/5})。但所得集合仍可能含四点或五点冲突，不能推出本题 O(k^5/log k)。
  - **sunflower anti-Ramsey 上界**（`advanced`）：把每个三元组按外接半径着色，应用 2015 年 Theorem 1。；推导：固定二元核 {A,B} 和颜色 ρ，半径 ρ 且过 A,B 的圆至多两个；每圆至多贡献一个额外点，所以单色 2-sunflower 至多 λ=2 个花瓣。代入超边大小3、h=2、目标大小k，得 |P|≥Ck^5/log k 即保证 rainbow k-集。
  - **抛物面—Sidon 下界**（`advanced`）：将整数盒提升至抛物面，再作泛型仿射投影。；推导：令 A={0,…,r−1}^m，Φ(a)=(a,||a||²)，X=Φ(A)。X 无三共线；可选秩 2 线性投影 π，使 π|_X 单射且 P=π(X) 无三共线、无四共圆，因为有限个碰撞、共线、共圆坏事件各是参数空间中的真多项式零集。若两个有序非零差相等 y−x=y'−x'，四个投影点形成非退化平行四边形；对角线两侧三角形全等，故外接半径相等。因此 rainbow 子集的有序差必须互异。又 |X−X|≤(2r−1)^m(2mr²+1)≤3m2^mr^{m+2}。对充分大 k，取 m=floor(2sqrt(log k/log2))、R=[k(k−1)/(3m2^m)]^{1/(m+2)} 及 r=ceil(R)−1<R，便有 n_k>r^m≥k²exp(−4sqrt((log2)(log k))−O(loglog k))。这是本轮独立闭合的部分下界论证，未找到承载它的一手论文。

- 严格推进：
  - 旧 O(k^5) 计数路线经逐项复核成立；特别补齐了 M_5 中必须使用 ∑_ρs_ρ(a)=C(n−1,2) 的求和步骤。
  - 得到显式删点界 n_k≤ceil((1296/3125)(k+2)^5)，但它不是最佳渐近界。
  - 一手预印本 Corollary 1(1) 已直接给出 n_k=O(k^5/log k)；官方题目背景遗漏了这一后续结果。
  - 构造出任意大的双曲线一般位置族，使固定三点的四冲突共度线性增长，严格否定了“所有顶共度为常数”的初始局部度方向。
  - 独立复核了抛物面投影的近二次下界：对充分大 k，k²exp(−4sqrt((log2)(log k))−O(loglog k))≤n_k≤O(k^5/log k)。投影在有限点集上取单射，并避开全部共线/共圆真多项式坏簇；整数参数取 r=ceil(R)−1 明确闭合。

- 路线证伪/边界检查：
  - 若“一般位置”仅指无三共线，则取任意多共圆点即可使 k≥4 时 n_k 不存在；所以无四共圆不可省略。
  - 共享两点、共享一点、不交分别对应并集4、5、6，确实穷尽不同三元组对。
  - 随机删点后的逐冲突删除是针对原保留集合中的全部冲突；删除至多一个点/冲突后不会产生新冲突。
  - 显式有理算术验证的10点双曲线样本满足一般位置，固定 ABC 的 H_4 共度恰为7=n−3。
  - Kostochka–Mubayi–Verstraëte 只作用于 H_6；把单层结论写成本题 O(k^5/log k) 会遗漏 H_4,H_5。
  - sunflower 论文的 Corollary 1(1) 不是相似定理：d=2 时其 d-单纯形就是三点三角形，其颜色正是外接半径。
  - 对抛物面投影检查了差相等但只有三个点的退化可能：那会给 X 中三点成等差、从而共线，与 Φ(A) 无三共线矛盾。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/827/verify_conflicts.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/827/verify_conflicts.py)：用 Fraction 精确计算外接半径平方，判定无三共线/无四共圆，枚举 M4/M5/M6 与顶共度，并检查双曲线反例、抛物面投影小例及优化删点常数。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/827 && python3 verify_conflicts.py --seed 827 --trials 50 --n 9 --bound 30 --box-m 2 --box-r 3`；结果：双曲线 N=10：一般位置为真，固定 ABC 的 H4 共度7；3×3 抛物面盒投影 N=9：差集大小45、精确 rainbow 独立数6；优化删点主常数为1296/3125。

- 第一阻塞点：题目仍远未“确定”：现有近二次下界与 O(k^5/log k) 上界之间有巨大指数缺口。通用的 2-good 三一致超图着色理论已给出 k^5/log k；继续推进必须利用“颜色来自欧氏外接半径”这一额外几何结构。低层冲突又能在线性规模的双曲线/高次代数曲线上集中，因此简单最大共度、局部引理或逐层取独立集均不能直接改善。
- 下一精确定理：一个精确且严格强于已知结果的下一定理是：存在 ε,c>0，使每个 N 点原始一般位置集都含至少 cN^{1/5}(log N)^{1/5+ε} 个点，其所有三元组外接半径互异。证明它等价于把 n_k 上界中的 log k 至少再提高固定正幂；可行切入口应是“富等半径代数曲线/稀疏剩余”二分，而非错误的统一常数共度假设。
- 研究记录：

记 P 为 n 点原始一般位置集，等半径的两个不同三元组称为冲突。其交大小只能为2、1、0，对应并集大小4、5、6。

计数方面，固定弦 ab 与半径 ρ，至多两个半径ρ的圆过ab；每个圆因无四共圆只能含一个额外点。因此每条弦至多产生(n−2)/2个四点冲突，
M_4≤C(n,2)(n−2)/2=n(n−1)(n−2)/4。
固定a,ρ，定义图G_{a,ρ}，其顶点为P\{a}，边bc表示R(abc)=ρ。固定b后可选c至多两个，故最大度≤2，若s_ρ(a)=|E(G_{a,ρ})|，则s_ρ(a)≤n−1且∑_ρs_ρ(a)=C(n−1,2)。五点冲突对应其中两条不交边，所以
M_5≤∑_a∑_ρ C(s_ρ(a),2)≤n(n−2)C(n−1,2)/2<n^4/4。
若t_ρ为半径ρ的三元组数，则每对点至多属于两个这样的三元组，故3t_ρ≤2C(n,2)。于是
M_6≤∑_ρC(t_ρ,2)≤n(n−1)C(n,3)/6<n^5/36。

随机以p=cn^{-4/5}, c=6^{1/5}保留点并逐冲突删点。期望最终大小至少
np-M_4p^4-M_5p^5-M_6p^6
≥(5c/6)n^{1/5}-3/2-c^4/(4n^{1/5}).
令A=5c/6，则A^5=3125/1296。取n=ceil((1296/3125)(k+2)^5)，最后一项至多5/(4(k+2))，故期望大于k。这闭合了显式常数界，但不是最佳渐近结果。

最佳已核对上界来自 sunflower anti-Ramsey 预印本的 Theorem 1 与 Corollary 1(1)。将C(P,3)按R(T)着色。任意固定二元核和颜色只能有至多两个花瓣，所以参数为超边大小3、h=2、λ=2。定理遂给
n_k≤C k^5/log k。
该预印本只给 Theorem 1 的证明框架，并把技术细节指向 Lefmann–Rödl–Wysocka；因此这里把它记录为精确匹配题面的已有一手定理，而不冒充本轮独立重证。

局部共度路线的关键反例为A=(0,0),B=(1,0),C=(0,2)。直接代入R^2=|UV|^2|UW|^2|VW|^2/(4\det(V-U,W-U)^2)，得到
R(XAB)=R(XAC) iff
(x^2-x+y^2-2y)(x^2-x-y^2+2y)=0。
除去圆ABC，第二因子为非退化双曲线。归纳选择双曲线上的点时，每条已有两点直线和每个已有三点圆只禁去有限多个交点，因此可构造任意大的一般位置集；固定ABC被n−3条H_4边共同包含。这严格说明总边数稀疏不推出最大共度小。

下界方面，令A={0,…,r−1}^m，Φ(a)=(a,||a||^2)。沿任意仿射直线，||a||²的严格二次项说明Φ(A)无三共线。对有限X=Φ(A)，可选秩2线性投影π，使π|_X单射且P=π(X)无三共线、无四共圆：每对碰撞、每三点共线、每四点共圆分别给投影参数空间中的真多项式零集，有限并仍可避开。若y−x=y'−x'≠0且有序对不同，则四点形成平行四边形；三点退化将迫使X中三点共线，所以四点互异。对角线两侧三角形全等，rainbow 子集故必须是有序差Sidon集，满足s(s−1)≤|X−X|−1。写u=b−a，有
Φ(b)−Φ(a)=(u,2a·u+||u||²)，
故
|X−X|≤(2r−1)^m(2mr²+1)≤Cm2^mr^{m+2}。
对充分大k，取m=floor(2sqrt(log k/log2))、R=[k(k−1)/(3m2^m)]^{1/(m+2)}及r=ceil(R)−1<R；于是n_k>r^m，并且
log(r^m)≥2log k−4sqrt((log2)(log k))−O(loglog k)，
即上述近二次下界。它仍不足以确定n_k。

- 一手来源：

  - [Points defining triangles with distinct circumradii](https://arxiv.org/abs/1402.6276)；一手来源：`true`；核验：引言 Problem 明定无三共线、无四共圆；Theorem 1.1 改用无四点共线或共圆并证明 O(k^9)；Theorem 1.2 给 n_4≤9,n_5≤37；第2节明确指出 Erdős 漏掉 R(ABX)=R(CDX) 型冲突。
  - [A sunflower anti-Ramsey theorem and its applications](https://arxiv.org/abs/1505.05170)；一手来源：`true`；核验：Theorem 1 给有界单色 h-sunflower 的 rainbow 子集界；Corollary 1(1) 精确处理 d-单纯形外接半径，给 |X|≥c_d k^{2d+1}/log k。取 d=2，直接得到 n_k=O(k^5/log k)。正文明确称其改进二维 O(k^9)。
  - [Edgardo Roldán-Pensado — Publications](https://sites.google.com/view/eroldan/home/publications)；一手来源：`true`；核验：作者页面仍把 sunflower anti-Ramsey 文列为 2015 年 arXiv preprint；本轮未找到它的期刊版或 DOI。
  - [On independent sets in hypergraphs](https://arxiv.org/abs/1106.3098)；一手来源：`true`；核验：主定理处理 (r+1)-一致超图且控制 r-共度；单独用于六点冲突层可产生对数增益，但不能自动排除四点、五点冲突。
  - [Distinct Volume Subsets](https://doi.org/10.1137/140954519)；一手来源：`true`；核验：Lemma 2.1 严格证明 m-good 的 k-一致完全超图着色存在规模 t 的 rainbow clique，当 N≥4mt^{2k−1}；论文随后说明相同方法可加入 1/log t 因子。它支持 sunflower/anti-Ramsey 方法的组合背景，但其题面是体积而非本问题本身。

#### #934

- 精确题面：Let $h_t(d)$ be minimal such that every graph $G$ with $h_t(d)$ edges and maximal degree $\leq d$ contains two edges whose shortest path between them has length $\geq t$. Estimate $h_t(d)$.
- 上轮下一步：先在 $t=3$ 写出两端 BFS 层的双计数，按奇圈 $C_7$ 是否存在分情；检验无 $C_7$ 情形中交叠项能否直接恢复论文所述精确型界，再定位一般图中奇圈造成的损失。
- 用时：786.5 秒（硬上限 7200 秒）
- 路线目标：原计划是通过 $C_7$ 分情和两端 BFS 碰撞证明 $h_3(\Delta)\le\Delta^3-\Delta^2+\Delta+2$。实时文献和独立计算均给出严格反例，因此该目标已经被否定；无 $C_7$ 分支仍成立。
- 结论：`route_refuted`；完整解声明：`none`；置信度：`high`
- 实际尝试：

- 独立复核：`PASS`；范围：对旧 t=3 精确与首项常数 1 路线的反例：O_4=KG(7,3)，以及 PG(2,q) 射影极性放大；这不是 #934 新最优上界问题的完整解答。
- 复核方式：一位独立代理逐步审阅定义、有限反例、放大与渐近推导；主代理另行重跑证书程序。
- 证据边界：253/225 的更强常数来自尚未同行评审的 2026 v1，且本轮未独立重建其截断 Witt 图；完全显式、独立复现的反例常数是 35/32。

  - **核对阈值和距离 convention**（`advanced`）：直接比较原图端点距离与线图距离，并核对新论文式 (1.1)。；推导：若 $e,f$ 不相交，则线图中一条长 $k$ 的边链对应端点间长 $k-1$ 的路径，反向亦然。因此原题要求边距离至少 $t$，等价于线图距离至少 $t+1$；坏图恰满足 $\operatorname{diam}L(G)\le t$。
  - **优先证伪旧 $t=3$ 精确路线**（`refuted`）：考察 Odd graph $O_4=KG(7,3)$。；推导：其顶点是 $[7]$ 的 3-子集，不交时相邻，故有 $\binom73=35$ 个顶点、度 4、70 条边。对两边 $AB,CD$，集合 $A\cup B,C\cup D$ 均有 6 个元素，交集至少为 5；四个集合 $A\cap C,A\cap D,B\cap C,B\cap D$ 分割该交集，故某对端点 $U,V$ 的交至少为 2。若交为 3，则 $U=V$；若交为 2，则 $[7]\setminus(U\cup V)$ 是同时与 $U,V$ 不交的 3-集，即共同邻点。因此两边在线图中距离至多 3。于是 \[h_3(4)\ge71>4^3-4^2+4+2=54.\]
  - **独立验证射影平面放大**（`advanced`）：令 $P=PG(2,q)$，并以标准内积定义极线 $\alpha^\perp$。在 $V(O_4)\times P$ 上令 $(u,\alpha)\sim(v,\beta)$ 当且仅当 $uv\in E(O_4)$ 且 $\beta\in\alpha^\perp$。；推导：每条极线有 $q+1$ 点，任意两条极线相交。因此所得图为 $4(q+1)$-正则，边数为 $70(q+1)(q^2+q+1)$。对任意两条放大后的边，$O_4$ 中对应边可选到相同端点或有共同邻点的端点 $r,s$；取 $\gamma\in\alpha^\perp\cap\beta^\perp$，得到长度至多 2 的顶点路径 $(r,\alpha)-(p,\gamma)-(s,\beta)$，故线图距离至多 3。
  - **检查 $C_7$ 分情的失败机制**（`refuted`）：穷举 $O_4$ 的所有简单 7-圈并统计边参与数。；推导：程序找到 360 个无向 $C_7$；70 条边全部被覆盖，且每条边恰在 36 个 $C_7$ 中。因此一般图中的 $C_7$ 不是“由一次细分产生的单一局部例外”，不能作为低阶误差吸收。

- 严格推进：
  - 给出了完全自洽的有限反例 $O_4$，不依赖截断 Witt 图的外部数据。它严格否定 $h_3(\Delta)\le\Delta^3-\Delta^2+\Delta+2$。
  - 对任意素数幂 $q$，上述放大给出 \[h_3(4(q+1))\ge70(q+1)(q^2+q+1)+1.\]
  - 写 $r=q+1$、$d=4r$，反例边数与旧猜想允许的最大坏图边数之差为 \[70r(r^2-r+1)-(d^3-d^2+d+1)=6r^3-54r^2+66r-1>0\] 当 $r\ge8$。故所有素数幂 $q\ge7$ 都给出旧精确猜想的显式反例。
  - 取任意大 $\Delta$，由素数定理选 $p=(1-o(1))\Delta/4-1$ 且 $4(p+1)\le\Delta$。利用 $h_3$ 对度上界的单调性，得到自洽下界 \[\liminf_{\Delta\to\infty}\frac{h_3(\Delta)}{\Delta^3}\ge\frac{70}{4^3}=\frac{35}{32}>1.\] 因此旧渐近猜想 $h_3(\Delta)\le(1+o(1))\Delta^3$ 也已被该构造否定。
  - 新论文再以 15-正则、3795 边的截断 Witt 图为种子，把常数提高到 \[\frac{3795}{15^3}=\frac{253}{225}.\] 该部分已逐行检查论文 Lemmas 3.2–3.4，但本次独立程序没有重建整个 Steiner 系统 $S(5,8,24)$。
  - 幸存结果：CCJK Theorem 10 对无 $C_7$ 图仍严格给出 $|E(G)|\le\Delta^3-\Delta^2+\Delta$；被反驳的是从无 $C_7$ 分支推广到任意图的路线。

- 路线证伪/边界检查：
  - 程序逐对检查 $O_4$ 的 70 条边，实际最大线图距离为 3。
  - 对 $q=7$，程序验证 $PG(2,7)$ 有 57 点、每条极线有 8 点、任意两条不同极线恰交于一点。所得证书参数为 $\Delta=32$、31920 边，故 $h_3(32)\ge31921>31778=32^3-32^2+32+2$。
  - 边界检查 $q=2$：放大图有 $\Delta=12$、1470 边，此时尚未超过旧上界 1598，说明“所有 $q$ 都反驳”是错误的；首个素数幂反例是 $q=7$。
  - 检查了简单性：即使 $\alpha\in\alpha^\perp$，相邻顶点的第一坐标来自 $O_4$ 的不同端点，故放大图不产生环。
  - 没有把 $h_3(4)\ge71$ 写成等式；当前证据只提供下界。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/934/verify_counterexamples.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/934/verify_counterexamples.py)：构造 $O_4$，逐对验证线图直径，穷举 $C_7$，并验证素数阶射影平面的极线证书及放大构造参数。；命令 `cd /home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/934 && python verify_counterexamples.py --q 7`；结果：输出 $O_4$：35 顶点、70 边、4-正则、线图直径 3；共有 360 个 $C_7$，每边参与 36 个；$q=7$ 放大证书为 $\Delta=32$、31920 边，严格超过旧猜想阈值允许的 31777 条坏图边。

- 第一阻塞点：初始路线的目标命题本身为假，不能继续尝试闭合其 BFS 交叠估计。新的上界问题必须允许由密集 $C_7$ 结构产生的常数级超额；当前一般上界仍为 $h_3(\Delta)\le\tfrac32\Delta^3+1$，与新下界常数 $253/225$ 之间有实质差距。
- 下一精确定理：新的精确目标是 2026 预印本 Problem 1.12：证明或反驳“对充分大的 $\Delta$，$h_3(\Delta)\le\frac{253}{225}\Delta^3$”。一个更窄、可先攻击的种子定理是：若 $H$ 为 $r$-正则且 $\operatorname{diam}L(H)\le3$，是否总有 $|E(H)|\le\frac{253}{225}r^3$？它若成立，只能封住现有射影极性放大机制，尚不足以证明完整上界。
- 研究记录：

研究记录：首先把题面化为坏图极值：$h_t(\Delta)-1$ 是最大度至多 $\Delta$ 且线图直径至多 $t$ 的图的最大边数。初始路线希望对 $t=3$ 证明坏图至多有 $\Delta^3-\Delta^2+\Delta+1$ 条边，并计划以 $C_7$ 为唯一障碍。这个目标已被 $O_4=KG(7,3)$ 直接击穿。

$O_4$ 的 35 个顶点是 $[7]$ 的 3-子集，每个顶点恰有 4 个不交的 3-子集邻点，所以 $|E(O_4)|=35\cdot4/2=70$。给定两边 $AB,CD$，有 $|A\cup B|=|C\cup D|=6$，故两并集的交至少为 5。该交被四个端点交集分割，所以存在 $U\in\{A,B\},V\in\{C,D\}$ 满足 $|U\cap V|\ge2$。若 $U=V$，原两边相邻；否则 $|U\cap V|=2$，而 $K=[7]\setminus(U\cup V)$ 是与二者均不交的 3-集，于是在线图中有边链
\[AB-(UK)-(KV)-CD.\]
因此 $\operatorname{diam}L(O_4)\le3$。这给出 $h_3(4)\ge71$，远大于旧猜想的 54。

进一步，取 $P=PG(2,q)$。对点 $\alpha$ 令 $\alpha^\perp$ 为标准非退化双线性型下的极线。定义
\[(u,\alpha)\sim(v,\beta)\iff uv\in E(O_4),\quad \beta\in\alpha^\perp.\]
每个顶点有 $4(q+1)$ 个邻点，总边数为
\[70(q+1)(q^2+q+1).\]
任意两条极线相交。结合 $O_4$ 上述端点性质，可以在两条任意放大边的某对端点之间造出长度至多 2 的路径，从而放大图线图直径仍至多 3。对 $q=7$ 得 $\Delta=32$、31920 条边，而旧猜想允许的最大坏图边数只有
\[32^3-32^2+32+1=31777.\]
故这是一个参数不大的完全显式反例族成员。

同一放大的渐近密度为
\[\frac{70(q+1)(q^2+q+1)}{(4(q+1))^3}\longrightarrow\frac{35}{32}>1.\]
配合素数定理，可为每个充分大的度上界选取接近的素数阶放大，从而得到全序列的 $\liminf$ 下界 $35/32$。新论文用截断 Witt 图把它提高到 $253/225$。因此不仅精确 $t=3$ 猜想为假，原先的 $(1+o(1))\Delta^3$ 上界猜想对 $t=3$ 也为假；但 $t\ge4$ 的对应渐近猜想仍未由该文解决。

计算还显示 $O_4$ 有 360 个 $C_7$，每条边处在 36 个 $C_7$ 中。这准确解释了旧续攻路线的故障：无 $C_7$ 定理本身没有问题，但一般坏图中的奇圈可形成遍布全图的高度对称结构，不能通过扣除一个局部“碰撞误差”恢复首项常数 1。由于核心目标已被严格反驳，按题意提前终止本路线。

- 一手来源：

  - [An improved bound for the strong clique index of graphs](https://arxiv.org/pdf/2607.02698)；一手来源：`true`；核验：2026-07-02 的 v1 预印本。Lemma 3.1 证明 $O_4=KG(7,3)$ 满足 $\operatorname{diam}L(O_4)\le3$；Lemma 3.3 给出射影平面放大 $G[H,q]$；Lemma 3.4 传递种子密度；Theorem 1.11 声称并证明 $\liminf_{\Delta\to\infty}h_3(\Delta)/\Delta^3\ge253/225$；Problem 1.12 提出匹配上界。
  - [Maximizing Line Subgraphs of Diameter at Most t](https://epubs.siam.org/doi/10.1137/21M1437354)；一手来源：`true`；核验：论文的 Theorem 6 给出 $h_t(\Delta)\le\tfrac32\Delta^t+1$；Theorem 7/10 给出无 $C_{2t+1}$ 时的改进。对 $t=3$，无 $C_7$ 坏图至多有 $\Delta^3-\Delta^2+\Delta$ 条边。
  - [Maximising line subgraphs of diameter at most t（arXiv v2）](https://arxiv.org/abs/2103.11898)；一手来源：`true`；核验：Conjecture 1 是旧精确型上界；Theorems 6–8、10 和 Proposition 11/13 的精确范围与期刊版本一致。

#### #950

- 精确题面：Let\[f(n) = \sum_{p<n}\frac{1}{n-p}.\]Is it true that\[\liminf f(n)=1\]and\[\limsup f(n)=\infty?\]Is it true that $f(n)=o(\log\log n)$ for all $n$?
- 上轮下一步：检验能否对大多数 dyadic 尺度建立统一节省：证明对每个 ε>0，所有充分大 n 都有 ∑_{j≤log₂n}2^{-j}(π(n-2^j)-π(n-2^{j+1}))≤ε log log n；先在可计算范围记录最坏 n 及贡献最大的尺度，以判断障碍来自少数短区间还是跨尺度累积。
- 用时：802.6 秒（硬上限 7200 秒）
- 路线目标：先证伪旧路线可能产生的小 \(o\)，再利用最新逐点短区间素数定理推进 \(\liminf\)，并用有界素数间隔推进 \(\limsup\)。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`medium`
- 实际尝试：

- 独立复核：`PASS_WITH_EVIDENCE_CAVEAT`；范围：短区间素数定理到 liminf 下界的转移、Brun–Titchmarsh 上界、H_1 到 limsup 下界的转移，以及 5,000,000 范围扫描；三项原猜想均未闭合。
- 复核方式：一位独立代理逐步审阅指数带积分、端点和来源；主代理另行核对论文正文并重跑 FFT 扫描。
- 证据边界：成熟的同行评审证据单独给 liminf f>=13/30；0.444299333... 的加强要接受尚未同行评审且本轮未重跑全部大型 ancillary 筛积分的 Li v8 Theorem 2。因此结果总体置信度标为 medium。

  - **两矩路线独立复核**（`advanced`）：直接展开中心二阶矩。；推导：由原文陈述的两渐近式，\[\sum_{n<x}(f(n)-1)^2=\sum f(n)^2-2\sum f(n)+\#\{n<x\}=o(x).\]故 \(f(n)\to1\) 依自然密度成立。
  - **Brun–Titchmarsh 乘法分块**（`blocked`）：以固定 \(\rho>1\) 将 \(d=n-p\) 分成 \([\rho^j,\rho^{j+1})\)。；推导：该块对应长度 \((\rho-1)\rho^j\) 的素数区间，贡献至多 \(2(\rho-1)/(j\log\rho+O(1))\)。求和后令 \(\rho\downarrow1\)，得到 \[\limsup_{n\to\infty}\frac{f(n)}{\log\log n}\le2.\]
  - **短区间密度的对数尺度积分**（`advanced`）：将 Li 与 Guth–Maynard 的逐点短区间下界转移到分母尺度。；推导：若长度至少 \(x^\theta\) 的短区间有 \((c-o(1))H/\log x\) 个素数，则分母指数带 \(n^a\le d<n^b\)、\(a>\theta\)，对 \(f(n)\) 的下极限贡献至少 \(c(b-a)\)。Guth–Maynard 的同行评审结果单独给 \(13/30\)；再接受 Li v8 Theorem 2 的阶梯常数，可积分得 \[\liminf f(n)\ge\frac{13}{30}+0.249\left(\frac{17}{30}-0.525\right)+10^{-3}(0.209+0.169+0.134+0.075+0.004)=0.444299\overline3.\]
  - **有界素数间隔推进上极限**（`advanced`）：取无穷多个满足 \(p_{r+1}-p_r\le246\) 的素数对，并令 \(n=p_{r+1}+1\)。；推导：此时 \(n-p_{r+1}=1\)，且 \(n-p_r\le247\)，所以 \[f(n)\ge1+\frac1{247}=\frac{248}{247}.\]因此 \(\limsup f(n)\ge248/247\)。
  - **有限计算证伪搜索**（`inconclusive`）：用素数指示函数与调和序列的 FFT 卷积计算全部 \(f(n)\)，再对报告极值直接求和复核。；推导：扫描至 \(5\times10^6\)。区间 \([5\times10^5,5\times10^6]\) 的最大值为 \(f(3586910)=2.620029059706424\)，最小值为 \(f(1349651)=0.6500789377978453\)。最大点的前五个 dyadic 块已贡献约 1.781，说明高值主要来自极短距离素数簇。

- 严格推进：
  - 仅使用已发表的 Guth–Maynard 定理，严格得到 \(13/30\le\liminf f(n)\le1\)；若接受当前 Li v8 预印本的 Theorem 2 及其表中数值常数，下端加强为 \(0.444299\overline3\)。右端来自两矩所给的趋于 1 子序列。
  - 得到无条件 \(\limsup f(n)\ge248/247\)，严格强于仅由矩估计得到的 \(\limsup f(n)\ge1\)。
  - 把旧路线的 \(O(\log\log n)\) sharpen 为 \(f(n)\le(2+o(1))\log\log n\)。该结论仍不蕴含第三问的小 \(o\)。
  - 两矩还严格给出 \(\#\{n<x:|f(n)-1|\ge\epsilon\}=o(x)\)，但不能控制零密度异常子序列。

- 路线证伪/边界检查：
  - 检查了 \(d=1\)、素数 \(p=2\)、\(d\ge n/2\) 的末块；末块贡献为 \(O(1/\log n)\)，不会破坏 Brun–Titchmarsh 求和。
  - 短区间转移时使用乘法小块并留出固定指数间隙，再令间隙趋零；没有把论文中的 \(\theta+\epsilon\) 错当成闭端点结论。
  - Li 的常数只采用其 Theorem 2 表中严格较小的保守数值，没有把“至少一个素数”冒充正确量级下界。
  - FFT 候选点全部以直接浮点求和复核，最大误差 \(1.34\times10^{-15}\)；有限扫描不被当成任何极限命题的证明。
  - 没有从自然密度收敛误推逐点收敛，也没有把 Hardy–Littlewood 或随机模型当作证明。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/950/scan_f.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/950/scan_f.py)：可参数化 FFT 扫描程序；生成素数筛、卷积值、十进区间极值、直接复核及最大候选的 dyadic 分解。；命令 `python3 scan_f.py --limit 5000000 --output scan_5000000.json`；结果：成功扫描至 5,000,000；直接复核最大绝对误差为 1.34e-15。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/950/scan_5000000.json](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/950/scan_5000000.json)：完整计算输出和尺度分解。；命令 `python3 -m json.tool scan_5000000.json >/dev/null`；结果：JSON 证书格式有效；记录最大候选 n=3586910、f(n)=2.620029059706424。

- 第一阻塞点：决定性缺口位于 \(d=n^{o(1)}\) 及更一般的 \(d<n^{0.52}\) 尺度。Brun–Titchmarsh 在每个乘法块只给密度约 \(2/\log D\)，跨尺度求和恰产生 \(2\log\log n\)；现有逐点短区间定理不能提供随 n 一致的额外节省。相同短尺度也是计算中大值的主要来源，因此既阻塞第三问，也阻塞 \(\limsup=\infty\)。
- 下一精确定理：优先证明以下精确的多尺度下界：对每个固定 \(\epsilon>0\)，\[\liminf_{n\to\infty}\sum_{n^\epsilon\le d\le n/2}\frac{\mathbf1_{\mathbb P}(n-d)}d\ge1-\epsilon.\]它与两矩给出的 \(\liminf f\le1\) 合并即可推出 \(\liminf f=1\)。相比逐个短区间的 PNT，这一命题只要求对数尺度加权后的总下界，因而是更清晰且可能更弱的下一定理。
- 研究记录：

写 \(d=n-p\)，则 \(f(n)=\sum_{1\le d\le n-2}\mathbf1_{\mathbb P}(n-d)/d\)。首先，原始两矩陈述给出 \(L^2\) 密度收敛，但只能产生趋于 1 的子序列。

核心转移引理如下。假设某 \(\theta<1\) 与 \(c>0\) 满足：每个充分大的、长度 \(H\ge x^{\theta+\delta}\) 的区间内至少有 \((c-o(1))H/\log x\) 个素数。固定 \(\theta<a<b\le1\)，把 \([n^a,n^b]\) 分成 \([D,(1+\eta)D]\)。对应素数区间为 \([n-(1+\eta)D,n-D]\)，长度 \(\eta D\)。必要时把它铺成长度约 \(n^{\theta+\delta}\) 的子区间，故其中素数数目至少 \((c-o(1))\eta D/\log n\)。每个素数贡献至少 \(((1+\eta)D)^{-1}\)，而块数为 \((b-a)\log n/\log(1+\eta)+O(1)\)。总贡献至少 \(c(b-a)\eta/((1+\eta)\log(1+\eta))+o(1)\)；令 \(\eta\downarrow0\) 得 \(c(b-a)\)。

Guth–Maynard Corollary 1.3 在 \(17/30<\alpha<1\) 给 \(c=1\)，贡献 \(13/30\)，这是同行评审证据。Li v8 Theorem 2 对相邻指数带依次给保守常数 0.004、0.075、0.134、0.169、0.209、0.249；接受该预印本定理后，阶梯积分加强为 \(0.444299\overline3\)。这不是 \(\liminf=1\) 的证明，因为 \(\alpha<0.52\) 的质量尚未控制。

上界方面，对 \(D=\rho^j\)，Brun–Titchmarsh 给块贡献至多 \(2(\rho-1)/(j\log\rho+O(1))\)。调和求和并令 \(\rho\downarrow1\)，得到 \(f(n)\le(2+o(1))\log\log n\)。因此旧路线严格停在常数 2，无法给小 \(o\)。

最后，由 Polymath 的 \(H_1\le246\)，存在趋于无穷的相邻素数对 \(q<p\)、\(p-q\le246\)。取 \(n=p+1\)，则 \(f(n)\ge1+1/(p-q+1)\ge248/247\)。这推进了上极限的已证下界，但距无界仍有本质差距。

- 一手来源：

  - [P. Erdős, Problems and results on combinatorial number theory III, p.63, equations (1)–(6)](https://www.renyi.hu/~p_erdos/1977-27.pdf)；一手来源：`true`；核验：第63页精确提出三问，并陈述 \(x^{-1}\sum_{n<x}f(n)\to1\)、\(x^{-1}\sum_{n<x}f(n)^2\to1\)。原文未附证明；本次未找到另一篇含完整二阶矩证明的一手论文。
  - [Runbo Li, The number of primes in short intervals and numerical calculations for Harman's sieve, Theorem 2](https://arxiv.org/abs/2308.04458v8)；一手来源：`true`；核验：当前为 arXiv:2308.04458v8 预印本。Theorem 2 对 \(0.52\le\theta\le0.525\) 声称并证明 \(\pi(x)-\pi(x-x^{\theta+\epsilon})\gg x^{\theta+\epsilon}/\log x\)；表中给出下界常数 0.004、0.075、0.134、0.169、0.209、0.249。正文完整展开 \(\theta=0.520\)，其余离散常数主要依赖 ancillary 数值代码。
  - [L. Guth and J. Maynard, New large value estimates for Dirichlet polynomials, Annals of Mathematics 203 (2026), 623–675, Corollary 1.3](https://doi.org/10.4007/annals.2026.203.2.6)；一手来源：`true`；核验：同行评审论文 Corollary 1.3：若 \(y\in[x^{17/30+\epsilon},x^{0.99}]\)，则 \(\pi(x+y)-\pi(x)=y/\log x+O_\epsilon(y e^{-\sqrt[4]{\log x}})\)。
  - [D. H. J. Polymath, Variants of the Selberg sieve, and bounded intervals containing many primes, Research in the Mathematical Sciences 1 (2014), Article 12, Theorem 1.4(i)](https://doi.org/10.1186/s40687-014-0012-7)；一手来源：`true`；核验：无条件证明 \(H_1=\liminf(p_{r+1}-p_r)\le246\)。
  - [H. L. Montgomery and R. C. Vaughan, The large sieve](https://doi.org/10.1112/S0025579300004708)；一手来源：`true`；核验：使用其 Brun–Titchmarsh 区间形式；在本题只需 \(q=1\) 的范围 \(\pi(x+y)-\pi(x)\le 2y/\log y\)。

#### #963

- 精确题面：Let $f(n)$ be the maximal $k$ such that in any set $A\subset \mathbb{R}$ of size $n$ there is a subset $B\subseteq A$ of size $\lvert B\rvert\geq k$ which is dissociated that is, the sums $\sum_{b\in S}b$ are distinct for all $S\subseteq B$. Estimate $f(n)$ - in particular, is it true that\[f(n)\geq \lfloor \log_2 n\rfloor?\]
- 上轮下一步：对小 r 穷举可实现的有符号关系型（按有理线性同构归类），检验命题：若 B 是 A 中最大耗散集，则 |A|≤2^{r+1} 或某个更接近 2^r 的界；先从 r≤5 寻找反例或可归纳结构。
- 用时：1636.2 秒（硬上限 7200 秒）
- 路线目标：优先证伪“把 3^r 压到约 2^r”的路线；随后推进小秩极值，并复核、修补 KoishiChan 于 2025-12-05 在官方论坛公开的模素数递推。结果是：严格得到 F(0)=1、F(1)=3、F(2)=7；经独立核分类审阅与程序重放建立严格计算机辅助结论 F(3)=13；修补后的论坛路线给出 f(n)≥(1−o(1))log₂n，但仍不能推出逐点的 floor(log₂n)。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`medium`
- 实际尝试：

- 独立复核：`PASS_WITH_SOURCE_ATTRIBUTION_FIX`；范围：F(r)=2G(r)+1、F(2)=7、严格计算机辅助结论 F(3)=13，以及经修补的 KoishiChan 论坛渐近证明 f(n)≥(1−o(1))log₂n；原逐点猜想仍未闭合。
- 复核方式：一位独立代理逐步审阅有限核分类和渐近递推，重跑秩3全枚举并独立穷举下界样本；主代理另行重放全部随附程序、核对 Montgomery–Vaughan 原文及官方论坛。
- 证据边界：F(3)=13 是内部独立审阅后的严格计算机辅助结论，但不是 Lean 证明或同行评审论文；渐近定理目前只见于公开论坛，仍未解决逐点 floor(log₂n) 猜想。

  - **等价极值化与射影化**（`advanced`）：定义 F(r)，并把非零元素按 a∼−a 合并。；推导：若 G(r) 是正实数集中 d(P)≤r 时的最大大小，则逐元素变号不影响耗散性，故 F(r)=2G(r)+1。原猜想等价于 G(r)≤2^r−1。
  - **初始容量路线的小规模证伪**（`inconclusive`）：在整数格上建立超图：每个耗散 (r+1)-元组为禁边，再用0-1 MILP求最大无禁边集。；推导：[-2,2]^2、秩上限2的最优值为7；{−1,0,1}^3、秩上限3的最优值为13。均未出现超过二进制阈值的反例。
  - **小秩严格推导**（`advanced`）：利用正代表和最大耗散基的有符号张成。；推导：严格证明 F(0)=1、F(1)=3、F(2)=7。特别地，最大耗散正数对 x<y 的射影有符号张成只有 x,y,x+y,y−x；若四者不同，则 {x,x+y,y−x} 为三个不同正数且最大者不等于另外两者之和，故该三元组耗散。
  - **秩3有限关系型证书**（`advanced`）：把13个非零 ternary 向量模 ± 投影；四元组关系只涉及核与 [−4,4]^3 的交。枚举核秩0、1、2的全部相关签名。；推导：共得到3325种签名：generic 1、line 192、plane 3132。每型对应超图的独立数均≤6；P={1,2,4,5,6,7} 有耗散三元组 {1,2,4}，而其15个四元组逐一有 {−1,0,1} 关系，因此给出大小6的下界。独立审阅核对了核分类的完备性、重跑得到逐字节相同输出，并另行穷举下界样本，故 G(3)=6、F(3)=13 是严格计算机辅助结论。
  - **模素数递推**（`advanced`）：复核 KoishiChan 的论坛证明：以乘法随机化控制 A 在 p 个短等差数列中的占用，再拼接模 p 的二进制幂和 p 倍数中的耗散集；同时修补 Γ 与区间端点。；推导：设正整数版本为 h(N)，取 p≈N^{1/12}，再取 q>max A 且 q>2pk 的充分大素数，并使用长度 floor(q/(2pk)) 的短区间。Montgomery–Vaughan 四阶矩和联合界给出 h(N)≥min(log₂N−O(1), floor(log₂p)+h(floor(cN/(p log N))))。迭代严格得到 h(N)≥(1−o(1))log₂N；反对称类化简和有限维有理线性整流把它转回任意实数集。

- 严格推进：
  - 严格极值：F(0)=1、F(1)=3、F(2)=7。因此 f(1)=0，f(n)=1 对 2≤n≤3，且 f(n)=2 对 4≤n≤7。
  - 严格结构恒等式：F(r)=2G(r)+1，其中 G(r) 只考虑互异正实数；这把目标精确化为 G(r)≤2^r−1。
  - 独立复核的严格计算机辅助结论：F(3)=13，因此 f(n)=3 对 8≤n≤13，且每个14元实数集都有耗散四元组。核分类、3325个关系型及下界样本均已独立核验；它尚未形式化为 Lean，也未经过外部同行评审。
  - 对 KoishiChan 论坛证明的修补复核严格给出 f(n)≥(1−o(1))log₂n。结合 A={1,…,n} 的计数上界 2^r≤rn+1，得到 f(n)=(1+o(1))log₂n。该结果不蕴含原猜想的逐点常数，且目前证据载体仍只是公开论坛讨论。

- 路线证伪/边界检查：
  - 全体 {−1,0,1}^r 不是秩r反例：r=2时 (1,1),(1,−1),(1,0) 已是耗散三元组。
  - 集合 {0}∪±{非零0/1子集和} 在 r=3 有15点，但含耗散四元组 (0,0,1),(0,1,1),(1,0,1),(1,1,0)。
  - B={1,2,4} 的全有符号张成为 [−7,7]，其中 (−7,−6,−5,−3) 耗散，故15点二进制构造也不是反例。
  - 模递推中 Γ 必须是 {1,2,4,…}，不能写成整数区间；后者并不耗散。
  - 模 q 回拉必须令所取 k 个代表严格小于 q/k，否则非零有符号和可能等于 ±q。本次把短等差数列长度截为 floor(q/(2pk))。
  - 有限格点搜索本身不覆盖任意实关系，且 HiGHS 的 Optimal 状态未附独立最优性证书，只作探索性证据；F(3)=13 的严格计算机辅助结论依赖另行穷尽全部与四元关系相关的整数核签名。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/963/grid_extremal_search.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/963/grid_extremal_search.py)：生成格点候选集的耗散超边、调用SciPy/HiGHS求最大无禁边集，并独立重算所选集的耗散维数。；命令 `python3 grid_extremal_search.py --dim 2 --radius 2 --rank 2 --output grid_d2_q2_r2.json && python3 grid_extremal_search.py --dim 3 --radius 1 --rank 3 --output grid_d3_q1_r3.json`；结果：求解器两次均报告 Optimal，目标值分别为7和13；未生成独立最优性证书，故仅作探索性计算。脚本SHA256为72972f021351a67fb483fff15905886c22324d60705d92a2b3b3185482f98e86。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/963/rank3_relation_types.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/963/rank3_relation_types.py)：枚举秩3时全部相关整数核签名，商去相反向量后计算13个射影ternary类的耗散四元超图独立数。；命令 `python3 rank3_relation_types.py --output rank3_relation_types.json`；结果：3325型全部完成；最大射影大小为6。脚本SHA256为87ae562269a179590bfc2a55020619f50241dff4e583d9ffcfb833efe2ac75f6。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/963/rank3_relation_types.json](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/963/rank3_relation_types.json)：秩3穷举摘要与达到最大值的样本关系型。；命令 `sha256sum rank3_relation_types.json && python3 -c "import json; p=json.load(open('rank3_relation_types.json')); assert p['relation_type_count']==3325 and p['maximum_projective_size_with_dimension_at_most_3']==6"`；结果：摘要断言通过；SHA256为97d52443822c287c0722c37785114f72b56474acb5c796a769207fe8746cf849。

- 第一阻塞点：当前最强幸存路线把底数3改善到渐近主项1，但每轮仍损失 O(log log N) 和常数；迭代只能控制总缺陷为 o(log N)，不能压到原猜想所需的常数0。秩3有限核分类也尚未显现可随 r 归纳的结构。渐近证明目前只见于论坛，尚无论文、预印本或形式化版本。
- 下一精确定理：优先目标是证明正整数版本 h(N)≥log₂N−O(1)，即把递推中的短区间密度损失从 c/(p log N) 改到 c/p，并控制取整误差；若能进一步把常数压到0，便得到原题。较小而明确的可审目标是把 F(3)=13 的有限核枚举转成可独立检查的证书或 Lean 形式化。
- 研究记录：

记 d(A) 为 A 的最大耗散子集大小。耗散等价于不存在非零 ε_a∈{−1,0,1} 使 Σ ε_a a=0。

一、极值与射影化。定义 F(r)=max{|A|:d(A)≤r}。最大耗散集的有符号张成给出 F(r)≤3^r，所以最大值有限。原猜想等价于 F(r)≤2^{r+1}−1：若 |A|≥2^{r+1}，便须有 d(A)≥r+1。把 A\{0} 按 a∼−a 合并，并从每类选正代表构成 P。任何耗散子集都不能含0或同时含 a,−a；按绝对值类投影与逐点变号双向保持耗散性，故 d(A)=d(P)，同时 |A|≤2|P|+1；反向取 A={0}∪±P 达到等号。因此 F(r)=2G(r)+1。

二、F(2)=7。若正集 P 的最大耗散大小≤2，取最大耗散对 0<x<y。极大性说明每个 p∈P 都是 ±x±y 的正值，故 P⊂{x,y,x+y,y−x}。若四个值互异，则三元组 {x,x+y,y−x} 耗散：三个数均为正且互异，而正三元组不耗散当且仅当最大数等于另外两数之和；这里 (x)+(y−x)=y≠x+y。故 |P|≤3，G(2)≤3。P={1,2,3} 达到3，故 F(2)=2·3+1=7。

三、秩3有限化。取最大耗散正三元基 B=(b₁,b₂,b₃)。每个正元素由非零 u∈{−1,0,1}³ 表示；模去 u∼−u 后只有(3³−1)/2=13个形式类。四个类 u₁,…,u₄ 不耗散，当且仅当存在非零 δ_j∈{−1,0,1} 使 Σδ_ju_j 落入整数关系核 K={c∈Z³:c·B=0}。该和位于 [−4,4]³，因此只需 K 与此盒子的交。K 的秩只能为0、1、2：秩1由盒中一个本原向量生成；秩2若盒中关系张成平面，则正法向量是两个盒中向量的叉积，本原坐标至多32；若不张成，则其有限签名已退化为秩0或1型。脚本据此穷尽3325个不同签名，所有超图独立数均≤6。P={1,2,4,5,6,7} 含耗散三元组 {1,2,4}，而其15个四元组均有显然的等和关系，例如 1+5=2+4、1+2+4=7、4+7=5+6；程序逐项核验全部15组。因此，结合独立核分类审阅、逐字节程序重放和下界样本穷举，严格的计算机辅助结论为 G(3)=6、F(3)=13。

四、KoishiChan 论坛渐近模递推的复核与修补。KoishiChan 于2025年12月5日在官方论坛公开了这一路线；原帖的 Γ 区间写法与短区间端点受到质疑，以下分别改用二进制幂 Γ 与半长区间。令 h(N) 为 N 元正整数集保证的耗散维数。取任意 A，d=d(A)，k=d+1。若 k>log₂N 已足够；否则取素数 p≈N^{1/12}，再取满足 q>max A 且 q>2pk 的充分大素数 q。对 i mod p 令 B_i={px+i:1≤x≤floor(q/(2pk))}⊂F_q^×，并令 r 在 F_q^× 中均匀。设 X_i=|rA∩B_i|。角色正交性给出
E X_i=N|B_i|/(q−1),
Var(X_i)=1/(q−1)² Σ_{χ≠χ₀}|Σ_{a∈A}χ(a)|²|Σ_{b∈B_i}χ(b)|²。
由乘法能量的平凡界 Σχ|Σ_Aχ|⁴≤qN³；短等差数列满足 |Σ_{B_i}χ|≤4M(χ)；Montgomery–Vaughan 定理1在四阶时给出 Σ_{χ≠χ₀}M(χ)⁴≪q³。因此 Var(X_i)≪N^{3/2}，Chebyshev 给出
P(X_i≤EX_i/2)≪p²k²/N^{1/2}。
对 p 个剩余类联合，失败概率≪p³k²/N^{1/2}=o(1)。故存在 r，使每个类均含至少 ⌊cN/(pk)⌋ 个点（调整绝对常数 c）。

从0类取最大耗散集 D₀；从剩余类 i∈Γ={1,2,4,…,2^{floor(log₂p)−1}} 各取一点。模 p 检查说明并集在整数中耗散。若其大小至少k，取k元子集；因所有代表严格小于q/k，其非零有符号和绝对值小于q，故该子集模q仍耗散。乘以r^{-1}回到原 A 后仍耗散，矛盾。因此
h(N)≥floor(log₂p)+h(⌊cN/(p log N)⌋).
取 p≈N^{1/12} 并迭代；若 x_j=log₂N_j，则 x_{j+1}≥(11/12)x_j−O(log x_j)。在 x_j 降到 sqrt(x_0) 前求和，累计误差为 O((log x_0)²)+O(sqrt(x_0))=o(x_0)，遂得 h(N)≥(1−o(1))log₂N。

最后，对任意实数集先取至少(n−1)/2个非零反对称类的正代表。在有限维 Q-线性空间 V=span_Q(A) 上，精确零关系在任意 Q-线性泛函下自动保持；再从保持各代表为正的开集内选取有理泛函，并避开有限个非零 ternary 组合对应的超平面。清分母后得到保持全部耗散子集的正整数模型。因此修补后的论坛渐近结论转回 f(n)≥(1−o(1))log₂n。本轮独立数学复核已通过，但该证明目前只在论坛公开，尚无论文、预印本或形式化版本；其 o(log n) 缺陷也不能推出题问的逐点 floor(log₂n)。

- 一手来源：

  - [P. Erdős, Extremal Problems in Number Theory, p.188](https://users.renyi.hu/~p_erdos/1965-02.pdf)；一手来源：`true`；核验：原文第188页明确给出 [log n/log 3] 下界，并问能否改成 [log n/log 2]；同时以 {1,…,n} 说明该猜想若真则近乎最佳。
  - [H. L. Montgomery and R. C. Vaughan, Mean Values of Character Sums, Theorem 1](https://doi.org/10.4153/CJM-1979-053-2)；一手来源：`true`；核验：定理1及证明式(11)给出固定 k 的最大特征和 2k 阶矩；取 k=2、q 为素数可用为 Σ_{χ≠χ₀}M(χ)^4≪q^3。
  - [V. F. Lev and R. Yuster, On the size of dissociated bases, Theorem 2](https://arxiv.org/abs/1005.0155)；一手来源：`true`；核验：正文确认极大耗散集 Λ 仅保证 A⊂Span_{−1,0,1}(Λ)；定理2比较两个极大耗散集的大小，但不给出本题所需的底数2。
  - [Erdős Problems #963](https://www.erdosproblems.com/963)；一手来源：`false`；核验：用于核对数据库状态和题面；截至页面最近编辑仍标为 OPEN，主体还称没有评论中的解答声称，但这与同站论坛已有证明及后续讨论不一致，属于明显的页面同步问题。未找到可核查的 Va99 公开扫描本。
  - [KoishiChan, Erdős Problems #963 forum proof (5 Dec 2025)](https://www.erdosproblems.com/forum/thread/963)；一手来源：`true`；核验：KoishiChan 公开了 f(n)≥(1−o(1))log₂n 的模素数递推；Tao 随后表示论证看起来正确并考虑标 solved，Bloom 也追问为何主页未更新。原帖把 Γ 误写成整数区间，且 B_{p,i} 端点有一处偏一讨论；本轮采用二进制幂 Γ 与 floor(q/(2pk)) 半长区间完成修补。该证据是公开论坛证明，不是论文、预印本或 Lean 代码。

#### #1063

- 精确题面：Let $k\geq 2$ and define $n_k\geq 2k$ to be the least value of $n$ such that $n-i$ divides $\binom{n}{k}$ for all but one $0\leq i<k$. Estimate $n_k$.
- 上轮下一步：先形式化并逐例验证下界中的关键引理 S≤M-v_p(k)，尤其覆盖 p^r≤k 且 r>v_p(k) 时区间可有两个 p^r 倍数的情形；随后计算 k≤100 的下界比值 log n_k/k，寻找应按 k 的素因子结构分层表述的估计。
- 用时：1532.1 秒（硬上限 7200 秒）
- 路线目标：先审计旧 p-adic 推导，再尝试加强确定性下界并把搜索约化到稀疏候选；同时检查现有 LCM 上界的证明是否真的闭合。
- 结论：`route_advanced`；完整解声明：`none`；置信度：`medium`
- 实际尝试：

- 独立复核：`PASS`；范围：对所有 k≥2 的新下界 D(k)|d_e、primorial 子序列增长、对 k≥3 的 LCM 上界修复，以及结构化有限搜索；FormalConjectures 的 better_upper 仍开放。
- 复核方式：一位独立代理逐步审阅 p-adic 层计数、边界情形和渐近推导；主代理重跑层级检查与结构化枚举。
- 证据边界：新下界与上界修复是内部独立审阅后的未发表结果，尚无外部同行评审或形式化证明；它们没有控制最小乘子 m，因而未给出严格优于 k·lcm(1,…,k−1) 的统一渐近上界。

  - **主动证伪旧 LCM 上界证明**（`refuted`）：检查旧稿所用等式 v_p(kL-i)=v_p(i)，其中 L=lcm(1,…,k-1)。；推导：取 k=5,L=12,n=60,i=4,p=2：v_2(i)=2，而 v_2(n-i)=v_2(56)=3。因此旧证明中的该等式严格错误。不过 v_2(binomial(60,5))=3，整除结论本身仍成立；随后用 Legendre/Kummer 层计数修复了证明。
  - **复核并加强旧 p-adic 下界**（`advanced`）：设唯一失败项 d_e=n-e。对 p^a∥k，令 M=max_i v_p(n-i)、S=v_p(binomial(n,k)，并逐层计算长度 k 区间内 p^j 倍数的数目。；推导：前 a 层因 p^j|k 精确抵消，其余每层净贡献为0或1，故 S≤M-a<M；于是每个 p|k 的最大赋值项都必须是同一个 d_e。再令 ell=floor(log_p(k-1))：若块中有至少两个 p^ell 倍数，则某个好项给 S≥ell；若只有一个且它是 d_e，则第 ell 层净贡献为0，而第 ell-1 层仍有好项，得到 S≥ell-1 和 S≤M-a-1。两种情形均给 M≥a+ell。
  - **修复现有 LCM 上界**（`advanced`）：对 n=kL 直接使用 binomial 赋值公式，而不假设 v_p(n-i)=v_p(i)。；推导：若 a=v_p(k)>0、ell=floor(log_p(k-1))，则 v_p(n)=a+ell；Kummer 层 a+1,…,a+ell 各贡献1，足以覆盖任意 i<k 的 v_p(n-i)。若 a=0，前 ell 层各贡献1；一旦 v_p(n-i)>ell，额外层因 n mod p^j=i<k 继续各贡献1。故所有 i≥1 均整除。另一方面对任意 p|k，有 v_p(binomial(n,k))=ell<v_p(n)=a+ell，所以 n 本身失败。
  - **结构化穷举与反例搜索**（`advanced`）：使用新整除定理只枚举 n=mD(k)+e，并用所有 p≤k 的精确赋值判定失败集合；另以直接计算 binomial 模 n-i 交叉核验。；推导：对 k≤30 中直接搜索可在 n≤10^6 找到首解的各项，结构化搜索所得首个 witness 完全一致；有限计算给出例如 n_6=75,n_7=30,n_8=70,n_9=56,n_10=2403。结构化搜索还得到 n_28=1053702、n_30=37584001。它们是可复算的有限穷举结果，不是渐近证明。
  - **尝试推出统一更小上界**（`blocked`）：把候选写成 n=mD(k)+e，考察是否能用 CRT 或筛法控制最小乘子 m。；推导：局部条件确实只涉及 p≤k 的赋值，但对 sqrt(k)<p≤k 仍产生大量相互独立的剩余类限制。当前没有证明最小 m≤exp(o(k))，也没有得到任何严格优于现有 exp((1+o(1))k) 的统一上界。

- 严格推进：
  - 对每个 k≥2，定义 D(k)=∏_{p^a∥k}p^{a+⌊log_p(k-1)⌋}=k∏_{p|k}p^{⌊log_p(k-1)⌋}。已得到严格定理：若 n≥2k 且恰有一个失败项 d_e=n-e，则 D(k)|d_e。因此 n_k≥max(2k,D(k))。
  - 这严格加强了旧式中 ⌊log_p(k/2)⌋ 的指数为 ⌊log_p(k-1)⌋。
  - 对 primorial 子序列 k=∏_{p≤y}p，素数定理给 log D(k)=(1+o(1))(log k)^2/log log k。因此 limsup_{k→∞} [log n_k·log log k/(log k)^2]≥1；特别地，n_k 沿该子序列超越任意固定多项式。
  - 对 k≥3，现有上界 n_k≤k·lcm(1,…,k-1) 的结论幸存，但旧稿中的赋值等式错误；这里给出了不依赖该等式的完整 p-adic 修复。边界 k=2 单列为 n_2=4。
  - 新定理把所有可能解严格限制为 n=mD(k)+e，其中 m≥1、0≤e<k；这是后续计算与筛法可以利用的稀疏化。

- 路线证伪/边界检查：
  - 旧断言 v_p(kL-i)=v_p(i) 被 (k,n,i,p)=(5,60,4,2) 反驳。
  - 诱人的加强“见证失败的素数必整除 k”是假的：k=3,n=7 时唯一失败项为6，p=2即可见证而2∤3。
  - 对 k≤50、2k≤n≤3000 检查了226833个 (k,n,p|k) 层级断言和7131个恰一失败实例，未发现新下界反例。
  - 一次性独立交叉核验（命令保存在运行日志）对 k≤50、每个 k 的前300个 n 比较直接模运算失败集合与 p-adic 判定，全部一致。
  - 有限表中较小的乘子 m 仅是线索；未据此推断 m 的渐近增长。

- 可复现计算：
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/1063/attack_1063.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/1063/attack_1063.py)：完全整数运算脚本：直接整除判定、p-adic 判定、旧/新下界检查、直接搜索及 n=mD(k)+e 的结构化搜索。SHA256 为 5a0cb54c7f65a10c48825ede8d74af5d05e7a3d29e46e2b2a6d3e2d5e95a2b43。；命令 `python3 attack_1063.py check --kmax 50 --nmax 3000`；结果：输出 layer_check OK；226833个层级断言及7131个恰一失败实例全部通过。
  - [/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/1063/attack_1063.py](/home/biostar/work/projects/amra/artifacts/erdos_followup_20260719/proof_routes/work/1063/attack_1063.py)：利用 D(k)|d_e 后的结构化有限穷举。；命令 `python3 attack_1063.py structural --kmax 30 --mmax 100000`；结果：对2≤k≤30均找到首个结构化 witness，并穷尽每个首解之前的全部结构化候选；包括 n_28=1053702、n_29=34776、n_30=37584001。

- 第一阻塞点：主要开放缺口仍是统一上界。新下界和候选稀疏化没有控制最小乘子 m；CRT 的朴素模数仍具有 exp((1+o(1))k) 规模，因而不能推出 FormalConjectures 所要求的严格渐近改进。
- 下一精确定理：令 m_k 为最小的 m，使某个 0≤e<k 对 n=mD(k)+e 给出唯一失败项。下一条精确目标是证明 log m_k=o(k)。由于 log D(k)=O((log k)^2)=o(k)，这将推出 n_k=exp(o(k))，从而严格解决 better_upper。第一步应给出所有 sqrt(k)<p≤k 的局部允许剩余类的精确分类，再尝试筛出 m≤exp(o(k))。
- 研究记录：

以下固定 k≥2。记 d_i=n-i，B=binom(n,k)。对素数 p，令 N_j=#{0≤i<k:p^j|d_i}。Legendre 公式给
v_p(B)=Σ_{j≥1}(N_j-⌊k/p^j⌋).
长度为 k 的整数区间中，N_j 只能是 ⌊k/p^j⌋ 或 ⌈k/p^j⌉。固定 p^a∥k，则 j≤a 时 p^j|k，故 N_j=k/p^j，前 a 层净贡献均为0。设 M=max_i v_p(d_i)、S=v_p(B)，且注意长度 k 的区间保证 M≥⌊log_p k⌋，于是 j>M 后分母层也为0。因此
0≤S≤M-a.
若配置恰有唯一失败下标 e，则任一达到 M 的 d_i 都因 M>S 而失败，故 d_e 是唯一达到 M 的项；这一结论对每个 p|k 同时成立。

令 ell=⌊log_p(k-1)⌋。若 ell=0，则 M≥a 已足够。设 ell≥1。若区间中至少有两个 p^ell 倍数，则至少一个不是 d_e，故它是好项并给 S≥ell；结合 S≤M-a 得 M≥a+ell。若只有一个 p^ell 倍数：若它不是 d_e，同样完成；若它正是 d_e，则必有 ⌊k/p^ell⌋=1，所以第 ell 层净贡献为0。此情形必有 ell>a；同时 p^{ell-1} 层至少有 p≥2 个倍数，故存在好项满足 S≥ell-1。因为第 ell 层为0，原上界还可写成 S≤M-a-1，仍推出 M≥a+ell。故
p^{a+⌊log_p(k-1)⌋}|d_e
对每个 p^a∥k 成立，各素数互素，得到 D(k)|d_e 以及 n≥d_e≥D(k)。

对 k≥3，现有上界的修复如下。令 L=lcm(1,…,k-1)、n=kL。固定 i≥1 和任意 p，写 a=v_p(k)、ell=⌊log_p(k-1)⌋。若 a>0，则 v_p(n)=a+ell>v_p(i)，并且 binomial 的 Kummer 层 a+1,…,a+ell 各贡献1，所以 v_p(B)≥ell≥v_p(n-i)。若 a=0，层1,…,ell 各贡献1；若 r=v_p(n-i)>ell，则对 ell<j≤r 有 p^j>k（因 p∤k，等号不可能）且 n mod p^j=i<k，每层再贡献1，故 v_p(B)≥r。于是所有 n-i（1≤i<k）整除 B。另一方面取任意 p|k，则 v_p(n-j)=v_p(j) 对1≤j<k，故 v_p(binomial(n-1,k-1))=0，而 B=n·binomial(n-1,k-1)/k；所以 v_p(B)=v_p(n)-v_p(k)<v_p(n)，即 n不整除B。故该 n 确实恰有一个失败项。

最后，对 k=∏_{p≤y}p，
log D(k)=log k+Σ_{p≤y}⌊log_p(k-1)⌋log p
=π(y)log k+O(θ(y))
=(1+o(1))(log k)^2/log log k.
这是严格的子序列下界，但距离统一估计及改进上界仍很远。

- 一手来源：

  - [Erdős–Selfridge, Advanced Problem 6447, Amer. Math. Monthly 90 (1983), 709–710](https://doi.org/10.2307/2323545)；一手来源：`true`；核验：期刊元数据确认原题属于 Advanced Problems 6445–6447，Problem 6447 在第710页。付费正文未能读取，因此没有声称逐字核对原稿。
  - [Monier, Solution of Advanced Problem 6447, Amer. Math. Monthly 92 (1985), 435–436](https://doi.org/10.2307/2322464)；一手来源：`true`；核验：JSTOR 目录确认条目号6447、页435–436及作者 Erdős、Selfridge、Jean-Marie Monier。正文受限，未能独立核对其“不可能全部整除”证明的每一步。
  - [FormalConjectures/ErdosProblems/1063.lean](https://github.com/google-deepmind/formal-conjectures/blob/9e126a6e1f7d108ced5904c43cac46b1c39b39cb/FormalConjectures/ErdosProblems/1063.lean)；一手来源：`true`；核验：定义明确要求唯一失败下标；better_upper 的精确范围是 n_k=O(U(k)) 且 U(k)=o(k·lcm(1,…,k-1))。相关定理目前均含 sorry，不能当作机器证明。
