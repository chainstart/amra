# 六小时数学命题研究班次

时间：2026-07-29 11:24–17:24（Asia/Hong_Kong）

## 目标

本班次不以“运行了多少算力”为成功标准，而以以下三类可复现产出为准：

1. 取得一个通过原命题语义检查和独立验证的反例候选；
2. 推进一个生成计数闭合、无 timeout、见证可重放的严格有限边界；
3. 获得一个经交叉校验的新算法表示，并证明它显著扩大了可搜索前沿。

任何有界空搜都不得表述成对无界猜想的证明。

## 起始快照

- 主机：32 个逻辑 CPU，7.6 GiB 内存，约 5.0 GiB available。
- `OPG-611` 四个历史基线 worker 正常运行，各占一核；11:25 时合计处理
  `40/497` 个缺边图，其中 13 个由独立 DRAT 检查排除，27 个进入 hard queue，
  没有候选。
- `OPG-145` 已证书化完成 7–9 阶：42,013 个有效图全部有无环 7-边染色，
  hard queue 为空。
- `OPG-401` 的旧校准线已完整到 17 阶，但没有持久化全部映射见证。
- `OPG-37271` 的证书化三次多重图线已完整到 18 阶，共 376,509 个实例，
  无 timeout 或 UNSAT。

## 选题与预算

### A. `OPG-611`：Bermond–Thomassen 猜想的 `k=4`

这是主攻线。`n=16` 是经过数学归约得到的首个可能反例阶，候选可以由原始
`PACK4` CNF、CaDiCaL proof 和 `drat-trim` 独立验证。

- 保留四个现有 shard 作为连续难度基线，不在原目录改变合同或求解器。
- hard runner 优先处理已有 packing 信号而不是卡在第一个 master solve 的对象：
  catalogue `#2`、`#32`、`#52`；首备为 `#6`。
- hard runner 必须使用独立输出目录。新增 residual cuts 后先看单位内存和
  master-model 吞吐，再决定是否同时开满三条。
- 成功闸门：原始、无颜色破缺的 `PACK4` 为 UNSAT，且 proof 独立验证。
- 排除闸门：最终 master CNF 为 UNSAT，且 proof 独立验证。
- timeout 只记录为 hard evidence，不得记作排除。

### B. `OPG-1757`：uniform forests 的负相关性

这是算法突破线。现有逐子集 `2^m` 枚举只覆盖了很小的九阶样本。改用 graphic
matroid 的精确 deletion–contraction：

```text
I(M) = I(M \ a) + I(M / a)
D(e,f) = I(M/e) I(M/f) - I(M) I(M/{e,f})
```

其中 `e != f`，`D(e,f) < 0` 才是反例。

- 先实现 loop、平行边和规范化 memo 均正确的精确计数器。
- 在小图上与独立逐子集枚举逐项核对四个整数计数和 `D`。
- 通过后启动九阶分片，保存最小 `D`、graph6、边对及完整计数证书。
- 15 分钟基准若低于约 2 图/秒，或单 worker memo/RSS 接近 1 GiB，停止裸递归，
  转向边分隔或 treewidth DP。
- 即使完整关闭某个九阶范围，也只报告该明确范围。

### C. `OPG-145`：acyclic edge-colouring

这是有限边界线。一般猜想仍开放，`Delta <= 4` 已知，因此搜索 `Delta=5` 和
7 色；安全过滤 3-sparse 图。

- 直接从首个新阶 `n=10` 开始，四分片、独立 checkpoint。
- 每个 SAT 着色由不调用 SAT 求解器的 checker 重放。
- 任一 UNSAT 立即暂停其他分片，生成静态 CNF 和独立 proof。
- 30 分钟后若预计总 CPU 超过 24 小时，或 timeout 比例超过 0.1%，停止全层
  蛮力，转向 5-正则图和 hard seed 的 2-switch 邻域。
- 只有四分片生成计数闭合、见证全量重放且 hard queue 为空，才记为可信的
  10 阶边界。

### D. `KOU-21.137`：奇素数切片

现有 order-128 的 2-group 见证只处理了 `p=2` 的 exponent-8 子命题，不能替代
奇素数研究。本班次把 `p` 为奇素数、`exp(G)=p^2` 固定进执行合同：

- 先完整扫描 GAP SmallGroups 中 order 243 的 67 个群；资源允许时推进到
  order 729 的 504 个群。
- 对每个群显式构造全部 `p` 次幂集合 `P`，检查 `P` 的乘法和逆闭包，再检查
  是否存在两个 `p` 次幂不交换。
- 候选必须保存群的可重建表示、完整 `P`、闭包证据和不交换 witness；只调用
  一次 GAP predicate 不足以认证。
- 该支线最多占一个 worker；依赖或模型合同未通过时，只交付实现与测试，不挤占
  三条主线的算力。

## 时间表

| 时间 | 工作 |
| --- | --- |
| 11:24–11:50 | 资源、开放状态、现有前沿和模型语义审计 |
| 11:50–12:20 | 启动 `OPG-145` 分片；实现并交叉校验 `OPG-1757` 新计数器 |
| 12:20–14:00 | 第一阶段并行搜索；监控 RSS、吞吐、timeout 和 hard queue |
| 14:00–14:15 | 中期闸门：淘汰低收益路线，释放算力给 hard runner 或九阶搜索 |
| 14:15–16:35 | 第二阶段深搜；候选出现时立即转独立验证 |
| 16:35–17:05 | 证书、见证、生成计数和命题语义复核 |
| 17:05–17:24 | 固化结果、未决前沿和下一班次建议 |

## 全局资源闸门

- available memory 低于 1.5 GiB 时，不再启动新 worker，并停止边际价值最低的
  新实验；四个既有 shard 不因单次瞬时波动被粗暴终止。
- 新任务统一使用被 Git 忽略的 `artifacts/opg_breakthrough/` 保存原始输出；
  本文件只记录计划和经过复核的结论。
- 每次中期快照同时记录 PID、RSS、CPU、状态文件更新时间和数学状态，避免把
  “进程仍在运行”误写成研究进展。

## 执行日志

### 11:46 检查点

- `OPG-1757` 新计数器的专项测试和旧回归测试合计 `14 passed`；小图计数已由
  独立逐子集枚举交叉核对。
- 已启动九阶 19–36 边的四个 `geng` 原生分片，合同固定为每图 20 秒、
  2,000,000 个递推状态和总 wall 19,200 秒。启动后首批合计 2,900 个图全部
  `D >= 0`，没有 timeout 或候选。
- `OPG-145` 十阶四分片仍为全 SAT、零 timeout；此时已生成约 20.7 万个图。
- 新增三个 `OPG-611` hard 实验分别处理 catalogue `#2/#32/#52`；此时已产生
  6 个 master model、6,144 条 packing cuts 和 768 条 residual cuts，均仍在
  运行。
- 可用内存约 4.0 GiB，未触发 1.5 GiB 熔断线。
- `KOU-21.137` 的首个奇素数合同已完成 order 243 的 67/67 个群：其中 49 个
  群指数为 9，39 个群的三次幂像为子群，没有反例；order 729 正在准备。

### 11:52 检查点

- 用独立 `geng` 计数固定了 `OPG-1757` 四分片的精确分母：
  `26,861 + 28,101 + 37,477 + 27,028 = 119,467`。`OPG-145` 十阶分母为
  `175,407 + 124,164 + 227,235 + 208,094 = 734,900`。
- `KOU-21.137` 已完整扫描 `p=3`、orders 243 和 729 的全部 571 个
  GAP SmallGroups。450 个群的指数恰为 9，其中 299 个群的完整三次幂像构成
  子群；没有找到非阿贝尔幂像。最大幂像大小为 27，最后游标为 `[729, 504]`，
  stop reason 为 `bounded_scope_exhausted`。
- 审计发现 production `OPG-1757` 的全局 best 被跨 matroid block 的结构性
  `D=0` 等号污染。新增只读分析器跳过等号、以精确整数比值给严格边对排序；
  九阶 19 边二连通十图小样的最接近比值为
  `0.99963554836343304097`（相对缺口约 `3.64e-4`）。
- 新增不调用 SAT 求解器的 `OPG-145` 独立审计器：完成后将逐条检查 properness
  和所有双色子图无环，并闭合 state/events/生成计数与 SHA-256。

### 12:22 检查点

- `KOU-21.137` 的 checkpoint 审计发现并修复了两个会造成未来假阴性的缺陷：
  越界/不一致游标不再静默 clamp；候选所在 chunk 在候选复核通过前不再提交。
  同时加入 `COUNT/CHUNK/CATALOG_DONE/METRICS/DONE` 严格协议、聚合不变量、
  坐标目录摘要、GAP/SmallGrp 版本和实现文件哈希。攻击式专项测试为
  `14 passed`；旧 exploit 与损坏 stdout 均 fail closed。
- 修复后 fresh artifact（manifest v2、`resumed=false`）再次完整得到
  `571/450/299`、无候选。runner、算术引擎和 GAP binary 三项 SHA-256 与当前
  磁盘逐字节一致；GAP/SmallGrp 为 `4.12.1/1.5.3`，目录 SHA-256 为
  `e1bb3e6d5f9025ad91e14182edd271300ce2b48e0c311138db4048fc7ed75c58`。
  完全独立的逐元素闭包 GAP 脚本得到 order 243 的 `67/49/39` 和 order 729
  的 `504/401/260`，没有非阿贝尔幂像。
- `OPG-1757` 的二连通 19 边 2,000 图定向样本没有违反；最接近九阶图的
  `left/right=0.99994651323051371335`。由三个近边界种子产生的 1,116 个
  固定标号十阶扩图全部无 timeout、无候选；最优值改善到
  `0.99996359944940474532`。对该最优十阶图复算全部 276 个边对后，它仍是
  全图最接近边对。四条十一阶 beam（计划 2,508 个扩图）已启动。
- `OPG-145` 十阶 shard 1 已闭合 `124,164/124,164`：119,427 个有效 SAT
  见证和 4,737 个定理过滤图，零 timeout/UNSAT。独立审计器已逐条重放
  119,427 个着色，事件 SHA-256 为
  `03aacc7272d4572baf9e1c00105d48441d21653b028ca311163530a724cf79f0`；
  单例最慢 0.258 秒、最多 35 条 lazy cycle cuts。
- 此时 `OPG-611` hard #2/#32 分别推进到 6/4 个 master models；#52 仍在
  长 master solve。三者累计 11 个 master models、11,264 条 packing cuts
  和 1,408 条 residual cuts，均无候选或可认证排除。

### 12:47 检查点

- `OPG-145` 十阶四分片全部闭合：
  `175,407 + 124,164 + 227,235 + 208,094 = 734,900` 个目录项中，
  692,136 个 `Delta=5` 且非 3-sparse 的实例全部为 SAT，另外 42,764 个
  由已知正面情形过滤；零 UNSAT、零 timeout。加固审计器重新运行原始
  `geng` 目录，逐 index/graph6 绑定事件，并以独立 union-find checker
  重放全部 692,136 份无环 7-边染色。联合报告
  `artifacts/opg_breakthrough/certified/opg145-n10-six-hour/audit-all-v2.json`
  的四个分片均为 `independently_verified`；auditor SHA-256 为
  `f957ef40e2164f6fdd3a1dcabb67cf71b4e89852bc6ed4002fd6295d9f86452c`。
- `OPG-1757` 对最接近等号的九阶图 <code>H?&#96;bM~^</code> 做了异构核验：独立枚举全部
  `2^19=524,288` 个边子集，与 production 删除--收缩算法逐项得到
  `(N,Ne,Nf,Nef)=(54,124,19,726,21,496,7,834)`，所选边对的
  `right-left=22,680>0`。四个分片各自首、末 19 边样本共八图也逐项吻合。
- 该图连续加入邻域 `{1,5,6,7,8}` 的假双生点后，新增独立 forward
  partition/forgotten-twin transfer-DP。它与原递推在 `t=0..4` 的四项
  计数完全一致；精确扫到 `t=500` 时，继承边对的比值仍严格小于 1，且每步
  上升，relative gap 降至约 `1.04e-10`。进一步检查发现四个计数序列在完整
  3,430-partition 分布向量层面满足 `(E-6)^5=0`；闭式和全 `t>=0` 的正差值
  证书正在固化。这里仅断言这个继承边对，不能替代所有边对检查。
- `OPG-1757` 九阶 19--36 边全枚举此时约完成 65%，仍为零 candidate、零
  timeout。新增的独立运行审计器已对 77,967 条在途事件完成目录绑定与整数
  不变量预检；最终四分片 `complete` 后再生成联合报告。事件没有保存完整
  pair matrix，因此最终 null 结论仍明确依赖已哈希的 production 精确计数器；
  不把协议审计写成第二套数学计数。
- `OPG-611` 四个历史分片累计处理 46/497 个缺失图：14 个已有独立证明的
  排除，32 个进入 hard queue，无候选。新增排除对应 catalogue #18，CNF
  SHA-256 为
  `349ea3f52511fc4d9361c8120f20c1cf597cbf6232ea0fd79d58f3d06f5d8ce3`，
  DRAT SHA-256 为
  `f9ce510e7dc2852a46d0cc5de6aea36581b87f27c72e7907156c9499959785f4`；
  本班次另行运行 `drat-trim` 得到 `s VERIFIED`（8,118,676 个 resolution
  steps）。三个 18,000 秒 hard 实验继续运行。

### 13:06 检查点

- false-twin 分析已从有限扫描提升为全参数结论。对九阶 strict-frontier 的
  三个首要种子，各自固定一个继承边对和由十阶 beam 找到的重复邻域；独立
  transfer-DP 在完整 partition 向量上逐坐标验证
  `v5-30v4+360v3-2160v2+6480v1-7776v0=0`。因为 transfer 是固定线性算子，
  这等于 `(T-6I)^5 v0=0`，故四个计数对所有 `t>=0` 都是
  `6^t` 乘四次多项式。首族的严格差值闭式为
  \[
  36^t(25t^5+1616t^4+33749t^3+319228t^2+1424790t+2449440)/108>0.
  \]
  另外两族也得到系数全正的五次多项式。集合证书已从磁盘重算验证，文件
  `artifacts/opg_breakthrough/certified/opg1757-false-twin-krylov-certificate/certificate-collection.json`
  的当前 SHA-256 为
  `ee9e281299100baf900089c5b7e54d276e5fbb36772986ad63bcc2fb9886c1f9`。
  结论严格只针对每族记录的一个继承边对；证书明确写入
  `all_edge_pairs_checked=false`，不声称排除整个图族的其他边对。
- `KOU-21.137` 把奇素数范围扩展到：`p=3` 的 orders 27/81/243/729，
  `p=5` 的 125/625，`p=7` 的 343，以及 `p=11` 的 1331。合计完整扫描
  621 个可用 SmallGroups；477 个群的指数恰为 `p^2`，其中 326 个的完整
  `p` 次幂像构成子群，均无非交换幂像。新增各 fresh run 都以
  `bounded_scope_exhausted` 结束；order 3125 不在本机 SmallGrp 1.5.3
  目录内，因此不计入覆盖。
- `OPG-145` 的数学范围审计给出了 block--cut tree 的完整换色拼接证明，
  确认 `-C -d2` 对累计的固定 `Delta=5` 最小反例搜索无损；同时明确
  `-D5` 完全没有覆盖 `Delta=6..9`，所以不得写成“全部十阶简单图”。
  说明文件为
  `data/research_open/opg_breakthrough_campaign/OPG145_SCOPE_AUDIT_2026-07-29.md`
  （SHA-256
  `9a72ef053e4876c99d31fec4b59482a7df0658b44234862b41c9d2da710b0b30`）。
  其中的 `K6` 显式 7 色基例也已由独立 checker 验证。
- 已启动下一条完整有限层：十一顶点、25--27 边的全部 384,122 个
  `Delta=5` 二连通非同构图；独立按 shard 分母为
  `88,595/100,734/80,076/114,717`，且这一稠密层没有 3-sparse 过滤项。
  专用 runner 的 21 项测试与暂停--恢复实测通过。13:06 时四 shard 已累计
  17,955 个 SAT，零 UNSAT/timeout/unknown，预计本班次内闭合。
- `OPG-1757` 九阶 19--36 边枚举已到 101,650/119,467（85.1%），仍是零
  violation、零 timeout；19--22 边密度分层样本的独立全子集算法均复现了
  production 的完整 pair matrix 和全局最强边对。

### 13:50 中期闸门

- `OPG-1757` 九阶 19--36 边四分片已经全部闭合：
  `26,861 + 28,101 + 37,477 + 27,028 = 119,467` 个连通非同构简单图，
  全部为 nonviolating，零 timeout、零 candidate。联合审计用冻结 `geng`
  重新生成每个分片，逐 index/graph6 绑定全部事件并检查计数恒等式；报告
  `artifacts/opg_breakthrough/certified/opg1757-n9-m19-36-six-hour/audit-v1.json`
  的 SHA-256 为
  `7a8e98c4cc62eb63df3545de2cef52a6f5a36e8f828ed790347bfa6432c11961`。
  最慢实例 1.675 秒、最大递推状态 530,485，均未接近 20 秒和 2,000,000
  状态的预算。
- v2 加固审计进一步要求四份动态依赖哈希映射完全相同，并在同一次
  fail-closed 运行中证明 sharded/unsharded 目录集合和多重集精确相同。
  外置报告
  `artifacts/opg_breakthrough/certified/opg1757-n9-m19-36-six-hour-audit-v2.json`
  的 SHA-256 为
  `f39e0901ce6a82d1627721b4c9fd78f0cf93c87a3712a793880a339c7fce7ef8`；
  wrapper auditor SHA-256 为
  `fd5c9ed2210fe66adf63a92e1505cbe0e16d81efd02332784a9b0a6782d5077a`。
  该加固仍明确保留“完整 pair matrix 未全量由第二实现重算”的信任边界。
- 另行把不分片目录与四分片并集排序核对：两者都是 119,467 条、无重复，
  SHA-256 同为
  `b08e12a7a417184b29c66cfe84e9b9a188438da55cc408819c632caf2ec60538`。
  与 production deletion--contraction 不同的逐边 partition DP，又对每个
  边数 `m=19..36` 各取一图复算所存边对的四个整数，18/18 完全吻合；这仍是
  分层样本，不冒充 119,467 个图的完整 pair matrix 第二次全量计数。
- Grimmett--Winkler 的 Theorem 1.5 已数值验证至多八顶点，以及九顶点至多
  十八边的简单图。利用森林测度对连通分量的乘积分解，本次结果把标准的
  `e != f`、无权 uniform-forest 边对负相关的计算边界推进到：每个连通分量
  都至多九顶点的所有有限简单图。严格范围和剩余计数信任边界记录在
  `OPG1757_N9_SCOPE_AUDIT_2026-07-29.md`；不得表述为一般 negative
  association 猜想的证明。
- 假孪生结构线进一步加入一个只连接九个基点任意子集的终端缺陷点。全部
  `2^9=512` 个邻域都得到
  `36^t P_R(t)/d_R` 的精确差值闭式，所有系数严格为正，最小系数 25。
  证书
  `artifacts/opg_breakthrough/certified/opg1757-false-twin-terminal-defect/certificate.json`
  已从磁盘重算验证，SHA-256 为
  `defd1c6c465553f66b01e61f30eb6e87eaaee25e4e2fe679c846d67d745b6fa9`。
  星扩张交换引理还证明“先缺陷、后假孪生”是同一图族。该证书仍只固定一个
  继承边对，不覆盖其他边对或连接到重复假孪生点的缺陷。
- `OPG-145` 七至九阶历史产物完成专用独立审计：
  `48,787` 个目录项中，42,013 个有效实例的 7 色见证全部重放通过，
  6,774 个由正面定理过滤；审计 JSON SHA-256 为
  `acca7d407c667c3e955bcead4b61fddc2a0081ae07fd15fbe578ea8009d39b93`。
  结合 `K6` 基例、block--cut 拼接和十阶审计，现已闭合
  `|V| <= 10, Delta=5` 的全部有限简单图；仍不覆盖 `Delta=6..9`。
- 十一阶 25--27 边层继续运行，13:50 时为 `130,893/384,122`，全 SAT、
  零 timeout/UNSAT/unknown。为使用释放出的算力，又固定 24 边层的精确
  16 分片分母，总计 1,003,287，并启动 provenance 绑定的 16 个 worker；
  13:50 时已处理 `132,893` 图，仍全部 SAT。独立 edge-24 审计器及攻击测试
  已准备完成，将在 16 shard 全部 `complete` 后才运行。
- `OPG-611` 的 MapleChrono #52 运行因 native `pysolvers` SIGSEGV 退出，
  明确不计作 timeout、排除或候选；Glucose42 重试正常运行并已取得第二个
  master model，累计加入 2,048 个 packing cuts、256 个 residual cuts。
  #2/#32 仍处于各自长 master solve；三条实验保持原 wall budget。
- 中期资源为约 3.6 GiB available，负载约处在 32 个逻辑核的容量附近，没有
  触发 1.5 GiB 内存熔断线。第二阶段保留 `OPG-611` hard portfolio 和十二阶
  extension beam；新增算力优先给可在班次内闭合并独立审计的 edge-24 层。
- `KOU-21.137` 又顺序补扫 `p=13,17,19,23` 各自的 `p^3` 阶全部 5 个
  SmallGroups，并由不调用 Python runner 的逐元素 GAP 脚本复核。累计范围
  现为 641 个群、485 个指数恰为 `p^2`、334 个完整 `p` 次幂像构成子群，
  仍无非交换幂像；独立 GAP 脚本 SHA-256 为
  `2a1bb369b137e0af5384e57970700d227193f219d2a769b478eac7fa728681bc`。

### 14:15 检查点

- `OPG-145` 新增一个可在本班次内完整闭合的高密度边界切片：十一顶点、
  23 边、二连通、度数限制 `4..5`。握手引理把该合同精确化为度序列
  `(5,5,4^9)`。十六分片的独立分母之和为 8,986；全部 8,986 个实例均得到
  可回放的无环 7-边染色，零过滤、UNSAT、timeout 或 unknown。独立审计器
  重新运行每个 `geng -C -d4 -D5 11 23:23 i/16` 目录并逐事件重放见证，
  报告
  `artifacts/opg_breakthrough/certified/opg145-n11-m23-near-regular-six-hour-audit.json`
  的 SHA-256 为
  `99d102f291785fb9fd43046d475bff5293325201f4aad57298b992c795450f3c`；
  root 再次运行审计也通过，两个 JSON 只在 `audited_at_unix` 不同。
  严格结论仅覆盖这一精确有限层，不覆盖完整的十一阶 `m=23` 层。
- `OPG-1757` 十二阶固定种子扩张已经结束：从 graph6
  <code>J?&#96;bM~^PyN?</code> 出发，加入一个标号新顶点，并遍历其大小 2--5 的全部
  1,012 个邻集；所选继承边对全部严格满足负相关，零 timeout，最接近比值
  为 `0.99998107093657991924`。原始结果
  `artifacts/opg_breakthrough/certified/opg1757-n12-best-beam-six-hour/beam-best.json`
  的 SHA-256 为
  `3f37c2dc79d2b642955c3639d41fbfc7ff9e6174518101778759381c68513e7a`。
  这只是固定种子的标号扩张且初筛一个继承边对，不是十二阶同构类全枚举。
- 对上述 beam 排名前列的七个代表扩图，另用一次完整
  deletion--contraction 统计同时复算所有边对；总计 3,861 个边对均为严格
  负相关，零等号、零 violation。最接近图的 561 个边对中，继承边对仍为
  全图最接近者，四个计数与 beam 文件完全相同。随后独立 final-partition
  DP 对全部 1,012 个标号扩图重新计算四个计数，并对七图的所有 3,861 个
  边对重新计算；分别得到 `1012 strict / 0 equality / 0 violation` 和
  `3861 / 0 / 0`。root 重跑所得 JSON 与原审计逐字节相同，SHA-256 为
  `f989341b83b8ddb0b9ea50325aee8c79b7de6033d495eb04d37c3d410da11172`；
  八项专项测试通过。这里的“全边对”仍只针对这七个明确图。
- `OPG-1757` 两个任意基点缺陷星的结构扫描完成首轮代数闭合。对
  512 个邻域的 131,328 个无序二元组，共检查 20,823,456 个合法精确选择边对；
  固定继承边对没有反例。每个裕量均可写为 `36^t H(t)/6^8`，所有
  `H` 的二项式基系数非负且常数项严格为正，因而对每个整数 `t>=0`
  严格为正。production 证书
  `artifacts/opg_breakthrough/certified/opg1757-two-star-defect/certificate.json`
  已由 root 重新编译独立 C++ 内核并从写盘 JSON 全量重算验证，SHA-256 为
  `9e39680fbf581fb1e285fa938f81c7e901041fd05ec84a52def9a1c07f5c865a`；
  九项专项攻击/交叉测试再次全部通过。此结论仍只针对固定继承边对，不覆盖
  扩展图的全部边对、连接到重复假孪生点的星或新增点之间的边。
- 在上述最接近等号的二星邻域 `R={0,4}, Q={2,5}` 上，再加入第三颗任意
  base-only 星；512 个第三邻域的裕量普通幂基系数均严格为正，故对全部
  `t>=0` 仍严格负相关。证书
  `artifacts/opg_breakthrough/certified/opg1757-three-star-high-risk/certificate.json`
  经 root 重算验证，SHA-256 为
  `af14ce358457908226eb7c02c5636d82cbd874c335e4a663739adb04bf6b40d3`；
  13,720 个坐标的 Krylov recurrence 残差全零，512 个 `t=5` holdout 全过。
- 三星探索又产生一个不依赖本基图的符号闭包定理。把森林按指定边
  `e,f` 的精确包含写成 `(a,b,c,d)`，其裕量为 `bc-ad`。新增一个度 2
  点连接 `e` 两端时，
  `(a,b,c,d)->(3a+b,3b,3c+d,3d)`，所以裕量恰乘 9；对 `f` 同理。
  因而单缺陷证书可严格扩展为：任意 base-only 星 `P`、任意 `t` 个
  `S`-星，再加任意 `r,q` 个分别连接 `e,f` 两端的新度 2 点，裕量为
  `9^(r+q) M(P,t)>0`。3--4 点全部简单图、246 个指定边对的直接森林枚举
  回归通过；该定理不声称一般邻域星都保号。
- 14:13 时十一阶 25--27 边完整层进度为 `185,669/384,122`，24 边完整层为
  `371,609/1,003,287`；两者仍全部 SAT、零 timeout/UNSAT/unknown。可用内存
  约 3.7 GiB，三个 `OPG-611` hard worker 仍各占一核，未触发资源熔断。

### 15:05 检查点

- `OPG-1757` 的端点二点星闭包已通过独立审阅。把指定边 `e,f` 的森林精确
  包含计数写成 `(a,b,c,d)` 后，在 `e` 两端添加一个新的二度点给出
  `(3a+b,3b,3c+d,3d)`，故裕量 `bc-ad` 恰乘 9；`f` 端同理，两种操作交换。
  这把已证书化的单星族严格扩展到任意多个 `e`、`f` 端点二点星。独立审阅
  重新证明了连通性分类双射，并穷举 3--4 点全部简单图的 246 个指定边对；
  结论仍只针对固定继承边对，不能写成一般星邻域保号定理。
- 十二阶固定种子扩张的独立 final-partition 审计也已固化：1,012 个标号
  邻域扩张的继承边对全部严格，七个代表图的全部 3,861 个边对也全部严格；
  审计 JSON SHA-256 为
  `f989341b83b8ddb0b9ea50325aee8c79b7de6033d495eb04d37c3d410da11172`。
  这仍不是十二阶同构类全枚举。
- `OPG-145` 的十一阶 23 边、最小度至少 3 的目录可按五度点个数精确分成
  `8,986 + 131,966 + 460,618 + 418,542 + 74,696 = 1,094,808` 个图。
  五度点个数为 2 和 6 的两层已经完整闭合并独立审计，全部 SAT、零错误；
  个数为 5 和 3 的层分别推进到 `223,981/418,542` 和
  `37,980/131,966`，个数为 4 的冻结 runner/auditor 已完成但尚未抢占
  活跃计算资源。
- 二度点方向取得了严格归约。若二度点 `v` 的邻点 `x,y` 不相邻，则先在
  抑制图 `(G-v)+xy` 上染色，再把 `xy` 拆回两条边；任意 acyclic
  `k`-edge-colouring 都可延拓。若 `x,y` 相邻，缺色计数又排除
  `d(x)+d(y)<=k+2`。结合已经审计的十阶边界，对
  `Delta=5,k=7,n=11,m=23`，尚需计算的二度点只能各自处于两个相邻五度点
  构成的三角形中。
- 两套独立 graph6 解码和目录重生把完整 2,013,018 图分成互斥四类：
  `1,094,808` 个无二度点、`646,555` 个含可抑制二度点、`134,653` 个由
  三角形共同缺色界排除、`137,002` 个二度临界残余。后者的冻结 runner
  与独立 auditor 正在构建；这使本班次内闭合完整 23 边层成为可行目标。
- 15:04 时十一阶 25--27 边层为 `287,637/384,122`，24 边层为
  `805,373/1,003,287`；仍全部 SAT、零 timeout/UNSAT/unknown。
  `OPG-611` hard #32、#52 分别到 6 和 3 个 master model，#2 的
  Glucose42/Minisat22 两条路线分别停在 6/4 个 model 的长主求解中；
  尚无候选或可认证排除。

### 15:25 理论归约与最后分层

- 回到 Wang--Zhang 2014 的原始定义和结构引理后，得到比 15:05 备用计算
  路线更强的归约。若十一阶 `Delta=5` 图 `G` 不可用 7 色，则在其子图中
  取 proper-subgraph inclusion 极小的坏图 `H`。十阶完整边界迫使 `H`
  仍有全部 11 个顶点；`H` 因而是真正的 7-deletion-minimal 图，不能把
  “按顶点数最小”直接冒充这个前提。
- Wang--Zhang Lemma 1 使 `H` 二连通；其 Lemma 4 说明，在
  `kappa>=Delta(H)+2` 时，二度点的每个邻点度至少
  `kappa-Delta(H)+4`。这里 `kappa=7, Delta(H)=5`，下界为 6，与最大度
  5 矛盾。因此所有十一阶、最大度 5、含二度点的图均由十阶边界和已发表
  结构引理排除；这个结论与边数无关。完整的最小性桥、Lemma 3(A)/(B)
  语义核对和信任边界记录在
  `OPG145_DEGREE_TWO_DELETION_MINIMAL_SCOPE_AUDIT_2026-07-29.md`。
- 作为不依赖上述 Lemma 4 的备用计算路线，两套独立实现仍冻结了完整
  2,013,018 图的互斥分类和 137,002 个临界残余 runner/auditor；真实
  shard-0 全流重生与 132 项 smoke 通过。由于更强理论归约已成立，本班次
  不再浪费约 200 万条事件和 13.7 万次 SAT 求解。
- 十一阶 23 边、恰有三个五度点的 131,966 图已经全部 SAT，零异常。独立
  auditor 重跑 `geng|pickg`、逐 graph6 绑定并重放全部见证，联合 JSON
  SHA-256 为
  `3643129cd8bd5a90014977f490e65b4611c71b88161df953d8707491f1954b4b`。
- 最后缺失的“恰有四个五度点”层共 460,618 图；冻结 runner/auditor 的
  21 项根级回归通过后已启动 16 个 worker。15:23 时为
  `41,311/460,618`，全 SAT、零 timeout/UNSAT/unknown。它一旦闭合，
  配合二度点理论归约和其余四个已审计/在途度序列层，就将关闭完整的
  十一阶 23 边目录。
- `OPG-611` #2 的 Minisat22 路线已从 4 个推进到 6 个 master model，
  之后再次进入长主求解；Glucose42 #2/#32 和 #52 重试仍分别停在
  6/6/3 个 model。这里仍只有难度与求解器敏感性证据，没有反例或排除。

### 16:25 三条十一阶有限层闭合

- `OPG-145` 的 23 边、恰有四个五度点层已完成
  `460,618/460,618`。16 个 shard 的冻结 auditor 重新运行精确
  `geng|pickg` 目录、逐 graph6 绑定事件并用独立 checker 重放全部着色；
  联合审计 SHA-256 为
  `0e656a35920198b61465c09e3802f024bf7e38e165aaf5f158a5d08ce61f92c3`，
  状态 `verified_complete`，零过滤、UNSAT、timeout 或 unknown。
- 23 边、最小度至少 3 的五个握手分层至此全部独立审计闭合：
  `8,986 + 131,966 + 460,618 + 418,542 + 74,696 = 1,094,808`。
  对应审计 SHA-256 依次为
  `99d102f291785fb9fd43046d475bff5293325201f4aad57298b992c795450f3c`、
  `3643129cd8bd5a90014977f490e65b4611c71b88161df953d8707491f1954b4b`、
  `0e656a35920198b61465c09e3802f024bf7e38e165aaf5f158a5d08ce61f92c3`、
  `9df82850e70fad1546705fd5c3d05276feac3475fe67cbe42a775a17bd895f39`、
  `66d8331ccfe7a5a626660077e2990803ab335e73d7595f0fae7a13fe55b29971`。
  结合 15:25 的二度点结构归约、较小 block 的十阶边界和 block--cut 拼接，
  这关闭了所有 11 顶点、`Delta=5`、恰 23 边的有限简单图。
- 24 边层的 16 个 shard 也全部闭合并独立审计：
  `1,003,287/1,003,287` 个实例全部 SAT。联合审计
  `artifacts/opg_breakthrough/certified/opg145-n11-edge24-six-hour.audit.json`
  的 SHA-256 为
  `fde671dba73a05e38c16bad6ebcf5c7a2755877c0170e7ec2d9b9b8d04fbefa7`；
  零过滤、UNSAT、timeout、unknown 或审计错误。
- 25--27 边层的四个 shard 同样闭合并独立审计：
  `88,595 + 100,734 + 80,076 + 114,717 = 384,122` 个实例全部 SAT。
  联合审计
  `artifacts/opg_breakthrough/certified/opg145-n11-dense-25-27-six-hour.audit.json`
  的 SHA-256 为
  `d14aa44f2b52fb0f81d4df2680de150b0e64ee3df1d462c703e7c78d689bd399`，
  状态 `verified_complete`，零异常。
- 因 11 顶点最大度 5 的图至多有 27 条边，本班次总计审计了上述
  `2,482,217` 个二连通目录项，并借助明确记录的理论归约得到新的有限边界：
  **在采用 Wang--Zhang Lemma 4 的已发表证明前提下，每个 11 顶点、最大度
  5、至少 23 条边的有限简单图都有 acyclic 7-edge-colouring。** 这没有
  覆盖 22 边及以下，更不是 OPG-145 一般猜想的证明。
- 对这个联合范围另作独立攻击审计，重新计数得到
  `m25/m26/m27 = 323,292/57,081/3,749`，并逐项复核最大边数、block
  拼接、`-d2/-d3` 与 Wang--Zhang 原文前件。报告
  `OPG145_N11_M23_27_INDEPENDENT_SCOPE_REVIEW_2026-07-29.md`
  结论为条件式 `PASS`，SHA-256 为
  `c8554695ceda153d8d676a41f99e664633fccc7f030fc78df3e47229e8fa233b`。
  关键边界是：若不接受 Wang--Zhang Lemma 4，本地备用计算仍有
  `137,002` 个二度临界 residual 未形成完成认证产物，此时联合范围必须
  判作 `NOT CLOSED`。

### 16:25 OPG-1757 的局部无限族加强

- 单条端点二边路径的四分类计数不仅给出旧继承边对裕量乘 9。若新边为
  `g,h`，则四条局部边 `{e,f,g,h}` 的六个裕量精确为
  `9M, 2M, 2M, 2N_e^2, 2N_e^2, N(N-N_e)`。因此旧 `e,f` 边对负相关时，
  六个局部边对全部负相关。
- 对任意 `r>=1` 个互不相邻、都连接 `e` 两端的新二度点，可交换加入
  恒等式进一步把 `{e,f}` 与全部 `2r` 条新边组成的局部边束内**所有**
  边对关闭成五种显式裕量。它不覆盖其他继承边之间的边对。
- 本地专项枚举为 `8 passed`：3--4 点全部简单图的单路径 1,476 个裕量，
  以及 `r=1,2` 的 5,166 个局部裕量全部吻合。独立审计又对三个不同基图、
  `r=1..4` 的 282 个局部边对重数，全部通过。独立审计报告
  `OPG1757_PARALLEL_PATH_ALL_LOCAL_PAIRS_INDEPENDENT_AUDIT_2026-07-29.md`
  的 SHA-256 为
  `ef4f70a4c29655e388f2df02cfc6b357d955a4d5f88d0adfcddd480e40257b0e`。
- 跨本班次新增的 OPG-145、OPG-1757 与 OPG-611 专项联合回归为
  `409 passed`；KOU-21.137 odd-power 协议和攻击式恢复测试另为
  `14 passed`。两组均零失败。

### 16:32 下一班次的 OPG-145 精确落点

- 完整 23 边范围的理论、握手分层、80 个 shard 和五份审计已经整合到
  `OPG145_N11_M23_COMPLETE_SCOPE_AUDIT_2026-07-29.md`；报告 SHA-256 为
  `3003cb94e4d00db1d27e6b7fed75dda38a3da7aca32c715e067a1828e2822c73`。
- 对 22 边层独立运行冻结 nauty 的六条 `geng|pickg` 管道，按五度点个数
  `x=0..5` 得到精确计数
  `264, 11,854, 137,276, 424,016, 363,299, 62,150`，总计
  `998,859`；未分层目录和 `countg --DM` 交叉汇总一致，所有进程退出码
  均为 0。
- `x=0` 是 264 个 4-正则图，由已知 `Delta<=4` 正例定理覆盖；含二度点
  由本班次 deletion-minimal 归约覆盖。因此下一班次真正要由 SAT 加独立
  见证审计关闭的是其余 `998,595` 图。
- 已冻结全部 16-shard 分母、度序列、runner/auditor 合同、六小时闸门和
  顺序
  `x=1 -> x=5 -> x=2 -> x=4 -> x=3`。计划文件
  `OPG145_N11_M22_NEXT_SESSION_PLAN_2026-07-29.md` 的 SHA-256 为
  `5050cd61ecfe1a88c78c9fd56facb8f3b51de66f3f618abae68805a245a4efb7`。
  本班次只完成范围与分母审计，没有抢跑该层 SAT，也没有把预计完成时间写成
  已得结论。

### 17:23 OPG-611 最终 hard portfolio

- 四个长期基线分片的带时间戳快照为 `64/497`：15 个缺边图已有独立
  DRAT 排除，49 个进入 hard/timeout，零 candidate。逐事件核对得到 15 个
  `proof_status=independently_verified`；四个 worker 仍运行，因此这不是
  497 图的完整目录结论。
- 本班次新增的可认证排除是 catalogue `#26`、graph6
  `O?????????????_?G?FoA`。CNF SHA-256 为
  `11f8eab199b09d21da57a64458b88da2665759be9cfe0bdffb3cfec8cd25258a`，
  DRAT SHA-256 为
  `ee47f1201af91eede2980ca1c95e329e271afcc6a1a751c109b9fd5c16b942e3`；
  root 重跑 `drat-trim` 得到 `s VERIFIED` 和 6,911 个 resolution steps。
- catalogue `#2/#32` 的 Glucose42 18,000 秒实验分别停在
  `6 models / 7 solves`，结果 JSON SHA-256 为
  `72508cc06e176ad2a4d9fdd51d3cf6a7047b88c3c043fcaa228ceedc75f3f67b`
  和
  `299b1d09baa8ae508c3813092ed8c3fc4c1771c6ff3f69505fadee2eac994dbc`。
  两者都是 timeout，不是排除。
- Minisat22 对 `#2/#32` 的最终结果分别为
  `7 models / 8 solves / 10,000.187 s` 和
  `4 / 5 / 6,600.076 s`，也都是 timeout；结果 SHA-256 分别为
  `6e32004552fcba6ebb75031e9dadab149667daf3a0e7933370ac7fde797902a7`
  和
  `e70dca81fed56dfdc119b51cd29a1e20bca978d314663a2518e5fcf3623b63c9`。
- `#52` 的 MapleChrono 原实验发生 native SIGSEGV，严格记为运行失败；
  全新 Glucose42 重试在 `3 models / 4 solves / 14,500.193 s` 后 timeout，
  结果 SHA-256 为
  `af7dd3702eceba845c3813589d43a7d6561436a11f45b569915809b62fd17e30`。
  崩溃和重试都没有产生候选或排除。
- 两条 900 秒小 batch、无 orbit-lift 探针也都 timeout：
  `#2` 为 6 models，`#32` 为 3 models。它们没有突破既有前沿，并再次显示
  99% 以上的时间耗在 master SAT，而非 separator。下轮不应只延长同一
  不可恢复运行，而应实现 cut journal、canonical master-CNF checkpoint、
  分阶段 batch 和 proof-capable solver portfolio。
- 完整审计及下一轮执行闸门见
  `OPG611_SIX_HOUR_HARD_PORTFOLIO_AUDIT_2026-07-29.md`，SHA-256 为
  `64751e1f8a01f72b2bc58b6f8ab80ad8424cca9578f6fec1fcaab5b4bc222343`。

### 17:19 测试与终局判定

- 跨本班次新增的 OPG-145、OPG-1757 与 OPG-611 专项测试为
  `409 passed`；KOU-21.137 odd-power 专项为 `14 passed`。
- 完整 `tests/test_second_batch_arithmetic.py` 在机器满载时首次得到
  `93 passed, 1 failed`。失败是既有 `KOU21.87 smallgroups-targeted`
  测试的 2 秒时序断言：目录发现尚未完成便正确返回
  `time_budget_exhausted, checked_cases=0`。三个额外 hard worker 结束、
  负载下降后，未改代码重跑得到 `94 passed in 47.67s`。因此这次失败按
  负载敏感阈值记录，不能删除首次失败，也不是 KOU-21.137 算术反例。
- `git diff --check`、相关 Python `compileall` 和新增源码/报告尾随空白扫描
  均通过。
- 本班次**没有找到任何反例，也没有证明任何一般开放猜想**。可信推进是：
  采用 Wang--Zhang Lemma 4 前提下的 OPG-145 十一阶高密度有限边界；
  OPG-1757 的明确九阶计算边界、十二阶定向样本和局部平行二边路径无限族；
  OPG-611 的一个新 DRAT 排除及 hard 瓶颈定位；以及 KOU-21.137 所列
  641 个 SmallGroups 的奇素数有界空搜。
- OPG-1757 的范围始终只是无权 uniform-forest 上不同边的 pairwise
  negative correlation；119,467 图的完整 pair matrix 没有由第二实现
  全量重算。把九阶结果扩展到“每个连通分量至多九顶点”还采用了
  Grimmett--Winkler 已发表的低阶计算，本仓库没有重放其旧程序。
