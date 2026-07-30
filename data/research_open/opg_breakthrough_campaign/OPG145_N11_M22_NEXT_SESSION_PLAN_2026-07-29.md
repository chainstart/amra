# OPG-145：\(n=11,m=22,\Delta=5\) 下一班次严格搜索计划

日期：2026-07-29

状态：**仅完成范围审计和 nauty 目录计数；没有启动本层 SAT 搜索，也没有修改
任何现有 runner/auditor。**

## 结论先行

在已认证的 \(|V|\leq 10,\Delta\leq 5\) 边界、已知
\(\Delta\leq4\) 正例定理和 Wang--Zhang deletion-minimal 结构引理均被接受的
前提下，十一阶、22 边、最大度 5 的首轮严格计算只需处理

```text
geng -q -C -d3 -D5 11 22:22 i/16 | pickg -q -Mx
```

中的 \(x=1,\ldots,5\)。这里 \(x\) 是五度点数。

- 二连通限制无损；
- 含二度点的层由本次 deletion-minimal 归约覆盖；
- \(x=0\) 的 264 个图全为 4-正则图，由已知
  \(\Delta\leq4\) 定理覆盖；
- 需要实际交给 7 色求解器的五层共有
  \[
  11\,854+137\,276+424\,016+363\,299+62\,150
  =998\,595
  \]
  个非同构图。

本次独立重生目录得到

\[
(264,11\,854,137\,276,424\,016,363\,299,62\,150),
\]

总计 \(998\,859\)，与待核预估逐项一致。不存在计数冲突。

下一班次的价值/规模优先级固定为

\[
x=1\ \longrightarrow\ x=5\ \longrightarrow\ x=2\
\longrightarrow\ x=4\ \longrightarrow\ x=3.
\]

这个顺序先关闭两个结构极端和三个较小分母，再处理两个中央大层；它只优化
“单位时间可认证关闭的范围”，不暗示反例在哪一层更可能出现。

## 1. 搜索范围为何可以缩到 `-C -d3`

### 1.1 二连通归约

[`OPG145_SCOPE_AUDIT_2026-07-29.md`](OPG145_SCOPE_AUDIT_2026-07-29.md)
给出了完整的 block--cut tree 拼接证明。若每个 block 都有 acyclic
7-edge-colouring，则沿 block--cut tree 逐块置换七色调色板，可以使割点处
颜色集合互斥；每个圈又完全落在单个 block 中，所以拼接不会产生双色圈。
因此任何不可用七色的图都含有一个本身仍不可用七色的非平凡二连通 block。

若这个坏 block 的最大度至多 4，则已知定理反而给出至多 6 色，矛盾；所以
坏 block 的最大度仍为 5。若十一阶候选的坏 block 少于 11 个顶点，则又与
已经认证的 \(|V|\leq10,\Delta\leq5\) 边界矛盾。故一个十一阶反例必须自身
就是该十一阶二连通 block，边数仍为 22。使用 `geng -C` 不丢失候选。

### 1.2 二度点由 deletion-minimal 归约覆盖

完整论证和文献前件核对见
[`OPG145_DEGREE_TWO_DELETION_MINIMAL_SCOPE_AUDIT_2026-07-29.md`](OPG145_DEGREE_TWO_DELETION_MINIMAL_SCOPE_AUDIT_2026-07-29.md)。
这里把闭合链压缩如下。

反设十一阶简单图 \(G\) 满足
\(\Delta(G)=5\) 且 \(a'(G)>7\)，并且 \(G\) 含二度点 \(z\)。在 \(G\)
的所有坏子图中取一个按 proper-subgraph inclusion 极小的 \(H\)。于是

\[
a'(H)>7,\qquad
\forall J\subsetneq H,\ a'(J)\leq7,
\]

且 \(\Delta(H)\leq5\)，所以 \(H\) 是文献定义下真正的
7-deletion-minimal 图；这里不能只用“\(G\) 按顶点数最小”代替
proper-subgraph 极小性。

若 \(|V(H)|\leq10\)，则：

- \(\Delta(H)=5\) 时与已认证的十阶边界矛盾；
- \(\Delta(H)\leq4\) 时与已知正例定理矛盾。

故 \(V(H)=V(G)\)。同理 \(\Delta(H)=5\)。Wang--Zhang Lemma 1 说明
\(H\) 二连通，因而 \(\delta(H)\geq2\)。原图的二度点满足

\[
d_H(z)\leq d_G(z)=2,
\]

所以 \(d_H(z)=2\)：它不能在取极小坏子图时消失。

Wang--Zhang Lemma 4 断言，当
\(\kappa\geq\Delta(H)+2\) 时，\(\kappa\)-deletion-minimal 图中二度点
的每个邻点度数至少

\[
\kappa-\Delta(H)+4.
\]

代入 \((\kappa,\Delta(H))=(7,5)\) 得下界 6，与
\(\Delta(H)=5\) 矛盾。因此十一阶、最大度 5、含二度点的全部简单图都不是
反例。该论证不使用边数，所以当然覆盖本次 \(m=22\) 层。

`-C` 已蕴含最小度至少 2；上述归约再排除等号情形，故生成器可严格使用
`-d3`。这一关闭依赖已发表的 Wang--Zhang Lemma 1 和 Lemma 4；本地审计
核对了定义、参数代入和极小子图桥，但没有从头形式化重证论文中的换色论证。

### 1.3 \(x=0\) 由 \(\Delta\leq4\) 已知定理覆盖

在 \(n=11,m=22\) 时度数和为 44。若没有五度点，而生成范围又是
\(3\leq d(v)\leq5\)，则平均度为 4 且最大度至多 4，故每个顶点度数都恰为
4。也就是说 \(x=0\) 层的唯一度序列是 \(4^{11}\)。

Wang--Ma--Shu--Wang 对 4-正则简单图的结果给出
\(a'(G)\leq6\)。更完整的 \(\Delta\leq4\) 引用链已经在范围审计中核对。
所以这 264 个图不应进入 SAT；六色染色也自然是允许一个颜色未使用的七色
染色。特别注意，`pickg -M0` **不是**本层的正确选择器；计数时用的是
`pickg -D4`，而执行阶段直接把本层列为理论正例。

规划时使用的理论/计算基线及当前 SHA-256 为：

| 基线 | SHA-256 |
| --- | --- |
| `OPG145_SCOPE_AUDIT_2026-07-29.md` | `9a72ef053e4876c99d31fec4b59482a7df0658b44234862b41c9d2da710b0b30` |
| `OPG145_DEGREE_TWO_DELETION_MINIMAL_SCOPE_AUDIT_2026-07-29.md` | `d4c7a609af0ab6c147ce0f322c587ff00c17be2109f9104778d62bcc311d4304` |
| `OPG145_7_9_HISTORY_AUDIT_2026-07-29.md` | `d7a01b6c2e27a0777f678eb44e32db2df984f531e3a0776f4db810d1fdf7d4b5` |
| `artifacts/opg_breakthrough/certified/opg145-n10-six-hour/audit-all-v2.json` | `06aaf69f91322275a664456bfae00324f3d1f863bace3e2d2ca45539932d540a` |

下一班次预检必须重新计算这些哈希；漂移时先重审引用链，不得静默更新合同。

## 2. 握手分层

令 \(x,y,z\) 分别为度数 5、4、3 的顶点数。`-d3 -D5` 和握手引理给出

\[
x+y+z=11,\qquad 5x+4y+3z=44.
\]

消去 \(y,z\) 得

\[
y=11-2x,\qquad z=x.
\]

非负性迫使 \(0\leq x\leq5\)，且每个 \(x\) 对应唯一度序列

\[
(5^x,4^{11-2x},3^x).
\]

所以以下六层互斥且穷尽整个
`geng -C -d3 -D5 11 22:22` 目录：

| 五度点数 \(x\) | 降序度序列 | 选择器 | 精确计数 | 处置 |
| ---: | --- | --- | ---: | --- |
| 0 | \(4^{11}\) | `pickg -D4` | 264 | \(\Delta=4\) 定理 |
| 1 | \((5,4^9,3)\) | `pickg -M1` | 11,854 | SAT + 独立见证审计 |
| 2 | \((5^2,4^7,3^2)\) | `pickg -M2` | 137,276 | SAT + 独立见证审计 |
| 3 | \((5^3,4^5,3^3)\) | `pickg -M3` | 424,016 | SAT + 独立见证审计 |
| 4 | \((5^4,4^3,3^4)\) | `pickg -M4` | 363,299 | SAT + 独立见证审计 |
| 5 | \((5^5,4,3^5)\) | `pickg -M5` | 62,150 | SAT + 独立见证审计 |
| **合计** |  |  | **998,859** | 理论 264；计算 998,595 |

对 \(x\geq1\)，`pickg -Mx` 的 `M` 是“最大度顶点数”。由于平均度恰为 4，
最大度若至多 4 就只能是 \(4^{11}\)，所以 `-M1` 至 `-M5` 选中的图最大度
必为 5。runner 和 auditor 仍必须逐图核对完整度序列，不能只依赖这句推导。

这些计算层也不含 3-sparse 图。令 \(L\) 是 \(x\) 个三度点，\(R\) 是其余
度数至少 4 的点，则

\[
\sum_{v\in L}d(v)=3x,\qquad
\sum_{v\in R}d(v)=44-3x.
\]

若图 3-sparse，就没有 \(R\)--\(R\) 边，每个 \(R\) 端点都必须接到
\(L\)，从而必须有 \(44-3x\leq3x\)。这对 \(1\leq x\leq5\) 均为假。
因此生产状态应满足 `filtered_three_sparse=0`；出现非零值要按合同错误停机，
不能把它当作正常过滤。

## 3. 计数的独立复算

本次没有读取任何未来 runner 的 `EXPECTED_*` 常量，而是直接用冻结的
nauty 2.8.8 二进制重生目录。主工具为：

| 工具 | 路径 | SHA-256 |
| --- | --- | --- |
| `geng` | `/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/bin/nauty-geng` | `9730b53764bdb28ecd2fdf755fafbc76992050f39e5ea19bb7d91433a26583e9` |
| `pickg` | `/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/bin/nauty-pickg` | `e1bb3b451c4b597fa2ec94d11acc4067ec2a5a0b7baa87ae15d6c5ee3b366bfc` |
| `countg` | `/home/biostar/.cache/amra/tools/nauty-2.8.8/usr/bin/nauty-countg` | `e1bb3b451c4b597fa2ec94d11acc4067ec2a5a0b7baa87ae15d6c5ee3b366bfc` |

动态链接的 nauty 主库哈希为
`libnautyW1-2.8.8.so =
28283263ac5d2dc1102485488edd63128e65c71325279f98242c2b8ea435573e`、
`libnauty-2.8.8.so =
007946d13023dcad7e78e9c5142e792fe31198590da29d595a883b537c54753a`；
`libcliquer.so.1 =
b1ccfac9465a0fc084b505d7415a8322da285705aaeb4f8f33f32cf926249c4e`。
生产 identity 必须记录所有实际动态依赖，而不只记录这三项。

六条精确计数管道是：

```text
geng -q -C -d3 -D5 11 22:22 | pickg -q -D4 | wc -l
geng -q -C -d3 -D5 11 22:22 | pickg -q -M1 | wc -l
geng -q -C -d3 -D5 11 22:22 | pickg -q -M2 | wc -l
geng -q -C -d3 -D5 11 22:22 | pickg -q -M3 | wc -l
geng -q -C -d3 -D5 11 22:22 | pickg -q -M4 | wc -l
geng -q -C -d3 -D5 11 22:22 | pickg -q -M5 | wc -l
```

输出依次为

```text
264
11854
137276
424016
363299
62150
```

每条管道的 `geng,pickg,wc` 退出码均为 `(0,0,0)`。直接对未过滤目录
`wc -l` 得 `998859`。另在 `LC_ALL=C` 下运行

```text
geng -q -C -d3 -D5 11 22:22 | countg -q --DM
```

得到相同的六行 `(maxdeg,maxverts)` 分组和总数，且两个进程退出码均为 0。
这只是第二种目录汇总交叉检查，不应被描述成一套与 nauty 无关的独立图生成
算法。

## 4. 冻结的 16 分片分母

下表来自 96 条精确的

```text
geng -q -C -d3 -D5 11 22:22 i/16 | pickg -q <selector> | wc -l
```

管道；全部 `geng,pickg,wc` 退出码为 `(0,0,0)`。它应原样进入新 runner
和独立 auditor 的只读 manifest，不能在生产时“学习”或自动修正。

| shard | \(x=0\) | \(x=1\) | \(x=2\) | \(x=3\) | \(x=4\) | \(x=5\) | 全目录 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 6 | 858 | 8,711 | 28,150 | 22,868 | 3,776 | 64,369 |
| 1 | 10 | 822 | 8,177 | 28,911 | 23,108 | 2,854 | 63,882 |
| 2 | 10 | 427 | 7,727 | 29,694 | 26,731 | 5,299 | 69,888 |
| 3 | 31 | 442 | 4,555 | 17,707 | 16,135 | 2,552 | 41,422 |
| 4 | 13 | 591 | 7,445 | 23,441 | 19,825 | 2,945 | 54,260 |
| 5 | 29 | 646 | 7,705 | 24,469 | 19,798 | 3,358 | 56,005 |
| 6 | 15 | 513 | 7,807 | 24,093 | 22,705 | 4,624 | 59,757 |
| 7 | 11 | 682 | 8,322 | 27,498 | 24,785 | 4,378 | 65,676 |
| 8 | 23 | 807 | 10,946 | 31,259 | 27,007 | 5,124 | 75,166 |
| 9 | 22 | 1,268 | 11,924 | 32,827 | 27,148 | 4,100 | 77,289 |
| 10 | 24 | 1,213 | 12,666 | 34,899 | 28,514 | 4,995 | 82,311 |
| 11 | 8 | 1,209 | 11,352 | 31,323 | 24,326 | 4,661 | 72,879 |
| 12 | 20 | 1,062 | 10,367 | 25,420 | 21,684 | 3,623 | 62,176 |
| 13 | 17 | 335 | 8,014 | 23,793 | 25,472 | 4,781 | 62,412 |
| 14 | 14 | 344 | 4,249 | 15,801 | 13,016 | 1,926 | 35,350 |
| 15 | 11 | 635 | 7,309 | 24,731 | 20,177 | 3,154 | 56,017 |
| **和** | **264** | **11,854** | **137,276** | **424,016** | **363,299** | **62,150** | **998,859** |

若不足 16 个 worker，同一层内按分母从大到小启动，以减少尾部拖延：

| 层 | shard 启动顺序 |
| --- | --- |
| \(x=1\) | `9,10,11,12,0,1,8,7,5,15,4,6,3,2,14,13` |
| \(x=5\) | `2,8,10,13,11,6,7,9,0,12,5,15,4,1,3,14` |
| \(x=2\) | `10,9,11,8,12,0,7,1,13,6,2,5,4,15,3,14` |
| \(x=4\) | `10,9,8,2,13,7,11,1,0,6,12,15,4,5,3,14` |
| \(x=3\) | `10,9,11,8,2,1,0,7,12,15,5,6,13,4,3,14` |

有 16 个可用 worker 时，同层 16 shard 同时启动；上表只决定资源不足或 worker
提前空闲后的队列顺序。

## 5. 新 runner 的冻结要求

下一班次应新增一个 \(m=22\) 专用、合同封闭的 runner；不得就地改动或放宽
现有 \(m=23\) runner。推荐一个文件内硬编码五层 manifest，而不是允许调用者
传任意 `n/m/d/D/M`：

1. **允许的运行参数只有** `x in {1,...,5}`、`shard in 0..15`、
   正的 finite `per_instance_seconds`、正的 wall budget 和全新输出目录。
   生产运行固定七色、每实例 60 秒、`max_cases=0`。
2. 每层固定 `n=11`、`m=22`、`-C -d3 -D5`、`-Mx`、完整度序列、16 分片
   和上表分母。`x=0` 不是 runner 的合法计算层。
3. Python 中用两个无 shell 的 `Popen` 建立 stdout pipe；分别保存并检查
   `geng`、`pickg` 的 return code 和 stderr。任何非零退出、broken pipe、
   非 graph6 行或提前 EOF 都 fail closed。
4. 每个目录记录都重新验证：11 顶点、22 边、简单、二连通、最小度 3、
   最大度 5、恰有 \(x\) 个五度点和完整降序度序列。目录顺序中的
   `(layer,shard,index,graph6)` 是事件主键。
5. 预期 `eligible=generated`、`filtered_three_sparse=0`。即使复用的底层
   runner 仍计算 3-sparse 谓词，出现一次过滤也必须终止。
6. 每个生成记录先写一条 schema 固定的事件，再 `flush+fsync`，之后才提交
   checkpoint。恢复时重放事件前缀并核对 SHA-256、索引连续性和状态聚合量；
   不得仅信任 `next_index`。
7. 每个 shard 使用独立目录和独占锁。smoke、失败重试、生产、审计输出互不
   复用。已经产生生产事件后不得改变该 campaign 的 schema 或 identity。
8. identity 至少绑定：
   - canonical/absolute `geng|pickg` 命令；
   - 五层分母 manifest；
   - runner、底层着色实现及所有实际 import 的源文件 SHA-256；
   - `geng`、`pickg`、SAT solver、proof checker 及全部动态依赖的路径和
     SHA-256；
   - `LC_ALL=C`、动态库目录、七色语义、per-instance timeout、事件和
     checkpoint 策略。
9. SAT 事件必须保存完整边到颜色的见证。求解器内部允许 lazy cycle cuts，
   但保存的见证必须针对原图满足 properness 和“任意两色子图为森林”。
10. timeout、unknown 和求解器异常均是未决，不是排除。UNSAT 也只触发候选
    升级流程，不直接写成反例。

规划时可复用但必须在冻结瞬间重新哈希的当前底层基线为：

| 文件 | 当前 SHA-256 |
| --- | --- |
| `src/amra/discovery/opg145_dense_search.py` | `ff73f566af090028a1ffe483aca25189b689b1dd2b677dccd2df8a512fd8c798` |
| `src/amra/discovery/opg_coloring_search.py` | `3366e14bb9dde8c5f519b96c011377140ad49f5672aab421fcd3938bf9f9619c` |
| `src/amra/discovery/opg145_dense_run_audit.py` | `3532e136195d797128bddf2d3ae2fad3e1d6e3b95c688fb55886ab0563d801e7` |

这些只是 2026-07-29 的规划快照，不是对未来改动的授权。新 wrapper/auditor
完成测试后，先把完整实现文件集及 aggregate hash 写入只读 manifest，再允许
第一条生产事件。冻结后任何源文件或依赖漂移都必须使用新 schema/新输出根；
不得在旧目录中混跑。

## 6. 独立 auditor 的冻结要求

auditor 必须在生产启动前完成并冻结，不能等空搜结束后才临时编写。它至少做
两层检查：

### A. 目录、身份和协议审计

- 不信任 state 中的 expected count；从 auditor 自己的只读 manifest 取得
  本文件第 4 节分母；
- 用 state 记录且哈希仍吻合的精确 `geng|pickg` 二进制重新运行每个 shard；
- 检查两个进程的返回码、stderr、动态依赖哈希和 canonical command；
- 按顺序逐条比较重生 graph6 与事件
  `(layer,shard,index,graph6)`，拒绝缺失、重复、换序、越界和额外事件；
- 重算 events SHA-256、identity SHA-256、所有状态聚合不变量；
- 要求 complete 空搜层满足
  `generated=eligible=sat=expected`，以及
  `filtered=unsat=timeouts=unknown=0`。

### B. 不调用 SAT 的语义审计

- 使用与 production 不同的 graph6 解码和图验证路径；
- 不导入或调用 production SAT encoder/solver；
- 对每份七色见证先检查每条边恰有一个合法颜色，再检查每个顶点处颜色互异；
- 对 21 个无序颜色对分别用独立 union-find 或 DFS 检查相应两色子图无圈；
- 逐层生成独立 audit JSON，最后再生成五层联合报告并记录文件 SHA-256。

auditor 的攻击测试至少覆盖：工具/依赖哈希漂移、命令漂移、分母漂移、截断或
附加事件、graph6 换位、重复索引、事件哈希篡改、非法颜色、相邻同色、人工
植入双色圈、伪造 complete、非零 `geng/pickg` 退出和 timeout 被误计为 SAT。

冻结顺序必须是：

1. 新 runner 与 auditor 的专项测试、旧 OPG-145 回归全部通过；
2. 在独立 smoke 目录对五层各跑短前缀；
3. auditor 对五个 smoke 全部通过，并确认损坏样本 fail closed；
4. 记录源文件、工具和依赖哈希；
5. 重新跑一次第 4 节分母检查；
6. 才创建生产目录并启动 worker。

## 7. 六小时执行顺序

资源上限建议为 16 个 SAT worker 加 1 个滚动 auditor。机器有余量时也不扩到
32 个 SAT worker；保留 CPU 和内存给独立审计、proof 升级以及同机既有任务。
以下时间是目标窗，不是把 wall timeout 冒充完成证明。

| 班次时间 | 工作 | 关闭后的累计计算分母 |
| --- | --- | ---: |
| `T+00:00–00:30` | 预检、测试、五层 smoke、重算分母、冻结 runner/auditor/toolchain | 0 |
| `T+00:30–00:50` | \(x=1\)，11,854 图；完成后立即全量审计 | 11,854 |
| `T+00:50–01:25` | \(x=5\)，62,150 图；审计可与下一小层预检重叠 | 74,004 |
| `T+01:25–02:20` | \(x=2\)，137,276 图；完成后形成前三层联合快照 | 211,280 |
| `T+02:20–03:50` | \(x=4\)，363,299 图；滚动审计已关闭的小层 | 574,579 |
| `T+03:50–05:25` | \(x=3\)，424,016 图；仅在投影闸门通过时启动 | 998,595 |
| `T+05:25–06:00` | 停止新计算；完成语义审计、联合不变量、哈希和严格范围报告 | 998,595 |

每一层开始前必须至少完成上一层的快速协议审计；完整见证审计可以在保留资源
的情况下滚动进行。若某层未在目标窗内完成，不删事件、不改分母，使用相同
identity checkpoint 继续；但是否进入下一层由下面的停止闸门决定。

## 8. 停止闸门

### G0：启动前闸门

出现下列任一情形时，不得写第一条生产事件：

- 任一整层或 16-shard 分母与第 4 节不符；
- 任一 `geng|pickg|wc` 返回码非零；
- 理论基线、runner、auditor、底层实现、工具或动态依赖哈希漂移且尚未重审；
- 专项/回归/攻击测试或五层 smoke 有一项失败；
- 生产目录不是全新目录，或已有状态不能通过完整 identity 前缀重放。

分母冲突时必须报告冲突，不得把新数值自动写回 manifest。

### G1：运行正确性闸门

以下任一事件立即停止启动新层，并让正在运行的 OPG-145 worker 在下一个已
fsync checkpoint 处退出：

- generator/filter 非零退出、stderr 异常、broken pipe 或目录提前结束；
- 图合同、索引、graph6、事件 hash、checkpoint 或 source identity 不一致；
- `filtered_three_sparse>0`、重复/缺失记录或 generated 超过冻结分母；
- SAT 见证被滚动 auditor 判为非法；
- 任意 timeout、unknown、solver crash 或 I/O/fsync 错误。

一例 timeout 就足以使该层无法按“零未决完整边界”关闭。它只能进入独立 hard
队列，不能记为排除，也不能用 timeout 比例四舍五入为零。

### G2：UNSAT/候选闸门

任一 online UNSAT 立即暂停所有 OPG-145 worker，保存精确
`layer/shard/index/graph6`、最终 CNF、变量映射、solver 输出和 provenance。
在报告反例前必须：

1. 用独立实现重生并核对原图；
2. 用无颜色对称破缺的正确编码复算，或另行给出所用对称破缺的严格完备性证明；
3. 由 proof-producing solver 生成证明；
4. 用独立 proof checker 验证；
5. 由 auditor 独立重建 CNF 语义并核对文件哈希。

没有通过这些步骤的 UNSAT 只叫“候选/异常”，不是反例。

### G3：时间价值闸门

每层至少运行 10 分钟且处理 5,000 图后，用实际 aggregate 吞吐和最近完成层
的 auditor 吞吐估计：

```text
预计完成时刻 =
当前时刻 + remaining_search / observed_search_rate
           + remaining_audit / observed_audit_rate
```

估计值再乘 1.25 安全系数。若它晚于 `T+05:25`：

- 不启动下一层；
- 优先关闭并审计当前最小可完整层；
- 不为了制造“进度百分比”启动注定不能在班次内闭合的大层。

进入 \(x=4\) 和 \(x=3\) 前各重新应用一次该闸门。若只能再完整关闭一个大层，
先选较小的 \(x=4\)。未完成的 shard 只报告精确前缀和 checkpoint，不报告
有限边界。

### G4：资源闸门

- available memory 低于 1.5 GiB 时不再启动 worker，并暂停价值最低的未闭合
  大层；低于 2.5 GiB 或持续 swap-in/out 时先减少并发；
- 文件系统可用空间低于 10 GiB、出现写入/fsync 错误或输出增长明显偏离
  已有 OPG-145 每事件量级时停止；
- 同机负载使 auditor 无法持续推进时，先减少 SAT worker，不能把审计全部
  推迟到班次末尾。

### G5：最终声明闸门

只有同时满足以下条件，才能写“关闭 \(n=11,m=22,\Delta=5\) 层”：

1. \(x=1,\ldots,5\) 的全部 80 个生产 shard 均为 complete；
2. 五层合计恰为 998,595，且每个事件都有独立重放通过的七色见证；
3. 零 filter、零 UNSAT、零 timeout、零 unknown、零协议错误；
4. 五个层审计和联合审计均通过，报告 SHA-256 已固化；
5. \(x=0\)、二度点、非二连通图和至多十阶图的理论/计算基线哈希重新核对
   通过。

若只关闭部分层，只能逐层报告其精确度序列和分母。即使五层全部关闭，结论也
仅是十一阶 22 边、最大度 5 的有限层；不得写成全部十一阶边数、最大度大于
5 的范围，更不得写成 OPG-145 一般猜想的证明。

## 9. 下一班次的最小交付物

无论六小时内是否全闭合，都必须留下：

- 冻结的 runner/auditor 源文件及 aggregate SHA-256；
- 五层 manifest、工具和动态依赖 provenance；
- 每个已启动 shard 的 state、events、events SHA-256 和退出原因；
- 每个完整层的独立 audit JSON；
- timeout/unknown/UNSAT 若存在时的单独 hard-case 包；
- 一份只陈述已闭合精确范围、未决分母和下一 checkpoint 的班次报告。

本计划本身没有创建这些生产产物，也没有授权修改现有 runner。
