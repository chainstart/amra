# OPG-145 十一阶 23--27 边联合范围独立审计

日期：2026-07-29

## 审计结论：PASS

在下述明确的信任边界内，没有发现边数、分片、连通性、度数或理论归约漏洞。
现有证据链足以支持：

> 对每个 11 顶点有限简单图 \(G\)，若
> \(\Delta(G)\leq5\) 且 \(|E(G)|\geq23\)，则 \(G\) 有 acyclic
> 7-edge-colouring。

这里把“最大度 5”按较强、也更不易产生歧义的
\(\Delta(G)\leq5\) 解读。事实上在本边数范围内
\(\Delta(G)\leq4\) 不可能，因此结论等价于写
\(\Delta(G)=5\)。

本结论不是 OPG-145 一般猜想的证明；它不覆盖 12 阶及以上图，也不覆盖
\(\Delta\geq6\)。

## 1. 本次独立核对的证据

### 1.1 23 边

主范围报告：

- `OPG145_N11_M23_COMPLETE_SCOPE_AUDIT_2026-07-29.md`
- SHA-256：
  `3003cb94e4d00db1d27e6b7fed75dda38a3da7aca32c715e067a1828e2822c73`

五个计算审计产物：

| 五度点数 | 图数 | 审计产物 SHA-256 | 状态 |
| ---: | ---: | --- | --- |
| 2 | 8,986 | `99d102f291785fb9fd43046d475bff5293325201f4aad57298b992c795450f3c` | `verified_complete` |
| 3 | 131,966 | `3643129cd8bd5a90014977f490e65b4611c71b88161df953d8707491f1954b4b` | `verified_complete` |
| 4 | 460,618 | `0e656a35920198b61465c09e3802f024bf7e38e165aaf5f158a5d08ce61f92c3` | `verified_complete` |
| 5 | 418,542 | `9df82850e70fad1546705fd5c3d05276feac3475fe67cbe42a775a17bd895f39` | `verified_complete` |
| 6 | 74,696 | `66d8331ccfe7a5a626660077e2990803ab335e73d7595f0fae7a13fe55b29971` | `verified_complete` |
| **合计** | **1,094,808** | — | 80/80 分片闭合 |

五层聚合为：

```text
generated                 1,094,808
eligible                  1,094,808
sat                       1,094,808
filtered_three_sparse             0
unsat / timeout / unknown         0
```

### 1.2 24 边

审计产物：

- `artifacts/opg_breakthrough/certified/opg145-n11-edge24-six-hour.audit.json`
- SHA-256：
  `fde671dba73a05e38c16bad6ebcf5c7a2755877c0170e7ec2d9b9b8d04fbefa7`
- schema：`amra.opg145.n11-m24-16.audit.v1`
- 状态：`verified_complete`

JSON 中的 shard 集合恰为
\((0/16),(1/16),\ldots,(15/16)\)，没有重复或缺号；16 个事件文件哈希
互异且分别绑定对应 shard。聚合计数为：

```text
expected_total = audited_total = 1,003,287
generated = eligible = sat       = 1,003,287
filtered_three_sparse            = 0
unsat / timeout / unknown        = 0
```

冻结目录是

```text
geng -q -C -d2 -D5 11 24:24 i/16
```

### 1.3 25--27 边

审计产物：

- `artifacts/opg_breakthrough/certified/opg145-n11-dense-25-27-six-hour.audit.json`
- SHA-256：
  `d14aa44f2b52fb0f81d4df2680de150b0e64ee3df1d462c703e7c78d689bd399`
- schema：`amra.opg145.n11-dense.audit.v1`
- 状态：`verified_complete`

JSON 中的 shard 集合恰为
\((0/4),(1/4),(2/4),(3/4)\)，没有重复或缺号。聚合计数为：

```text
expected_total = audited_total = 384,122
generated = eligible = sat       = 384,122
filtered_three_sparse            = 0
unsat / timeout / unknown        = 0
```

冻结目录是

```text
geng -q -C -d2 -D5 11 25:27 i/4
```

本次审计还直接用产物绑定的 nauty 2.8.8 重新作了只计数交叉检查：

```text
geng -C -d3 -D5 -u 11 23:23  -> 1,094,808
geng -C -d2 -D5 -u 11 24:24  -> 1,003,287
geng -C -d2 -D5 -u 11 25:27  ->   384,122
```

其中 `25:27` 的逐边数分布为：

```text
m=25   323,292
m=26    57,081
m=27     3,749
total  384,122
```

所以 dense 范围不是只命中了 25 边；25、26、27 三层均非空并全部包含。

## 2. 先验边数边界：没有 28 边或 \(\Delta<5\) 缺口

若 \(|V(G)|=11\) 且 \(\Delta(G)\leq5\)，握手引理给出

\[
2|E(G)|=\sum_v d(v)\leq55.
\]

左端为偶数，故

\[
|E(G)|\leq27.
\]

所以“至少 23 边”准确等于检查 \(m=23,24,25,26,27\)，不存在应补的
\(m\geq28\) 层。

反过来，若 \(\Delta(G)\leq4\)，则

\[
2|E(G)|\leq44,\qquad |E(G)|\leq22.
\]

因此任何本联合范围中的图自动满足 \(\Delta(G)=5\)。
这也说明计算目录的 `-D5` 不会漏掉一个最大度更小但仍有至少 23 边的图。

## 3. 非二连通图与 `-C` 的范围

`-C` 只枚举二连通图，但该限制有严格的 block 归约支撑。

若一个至多五度图的每个 block 都能用至多七色作 acyclic edge-colouring，
可沿 block--cut tree 逐块拼接。在割点 \(v\) 附着一个新 block 时，对新
block 的整个七色调色板作置换，使其在 \(v\) 使用的颜色与已染部分在
\(v\) 使用的颜色不交。这个置换存在，因为两侧在 \(v\) 的度数和至多
\(d_G(v)\leq5<7\)。每个简单圈完全包含于单个 block，故拼接不产生跨
block 的双色圈。

如果一个 11 顶点图不可七色染，则必有一个不可七色染的非平凡 block
\(B\)。

- 若 \(\Delta(B)\leq4\)，已发表的 \(\Delta\leq4\) 正例结果给出矛盾；
- 若 \(\Delta(B)=5\) 且 \(|V(B)|\leq10\)，已认证的低阶边界给出矛盾；
- 若 \(B\) 有全部 11 个顶点，则 \(B\) 是 \(G\) 的 spanning
  2-connected subgraph；向二连通图加边不破坏二连通性，所以 \(G\)
  本身二连通。

因此任何潜在反例都在 `-C` 目录中。非二连通图没有遗漏。

低阶边界的本地证据为：

- \(K_6\) 显式染色及 block 范围报告
  `OPG145_SCOPE_AUDIT_2026-07-29.md`，SHA-256
  `9a72ef053e4876c99d31fec4b59482a7df0658b44234862b41c9d2da710b0b30`；
- 7--9 阶审计 JSON，SHA-256
  `acca7d407c667c3e955bcead4b61fddc2a0081ae07fd15fbe578ea8009d39b93`；
- 10 阶四分片审计 JSON，SHA-256
  `06aaf69f91322275a664456bfae00324f3d1f863bace3e2d2ca45539932d540a`。

这些证据与 \(\Delta\leq4\) 及 3-sparse 的已发表正例定理合并，给出
\(|V|\leq10,\Delta\leq5\) 的七色边界。历史 7--9 阶运行仍保留其报告
已经明确记载的 legacy provenance 边界；这不是本次联合时新引入的逻辑
遗漏。

## 4. 23 边的 \(\delta=2\) 依赖

23 边计算使用 \(\delta\geq3\) 目录，因此排除二度点是该层不可省略的
理论前提。本次独立核对确认这里使用的不是错误的“最小顶点数反例”
论证。

从假设的 11 阶坏图 \(G\) 中，须在所有不可七色染的子图中按
proper-subgraph inclusion 取极小者 \(H\)。于是 \(H\) 才真正满足
Wang--Zhang 的 7-deletion-minimal 定义。低阶边界及
\(\Delta\leq4\) 定理分别迫使

\[
V(H)=V(G),\qquad \Delta(H)=5.
\]

本次从 arXiv:1302.2405v4 的 TeX 原文逐项核对到：

1. deletion-minimal 的定义量化到每个 proper subgraph；
2. Lemma 1：deletion-minimal 图 2-connected；
3. Lemma 4：若 \(\kappa\geq\Delta(H)+2\)，二度点的每个邻点度数至少
   \(\kappa-\Delta(H)+4\)。

若 \(G\) 有度数至多 1 的顶点，因 \(H\) spanning 且
\(\delta(H)\geq2\) 立即矛盾。若 \(G\) 有二度点 \(v\)，则
\[
2\leq d_H(v)\leq d_G(v)=2,
\]
所以 \(v\) 在 \(H\) 中仍是二度点。代入
\((\kappa,\Delta(H))=(7,5)\)，Lemma 4 要求其邻点在 \(H\) 中至少
6 度，与 \(\Delta(H)=5\) 矛盾。故 23 边潜在反例确实满足
\(\delta(G)\geq3\)。

这一步的准确结论是：

- **逻辑审计 PASS**；
- **信任边界**仍包含 Wang--Zhang Lemma 4 的已发表证明，本地工作没有
  重新形式化其完整换色证明。

这个依赖是实质性的，不能把它降格为可有可无的引用。若拒绝使用 Lemma 4，
本地较弱归约在完整的 2,013,018 个
`-C -d2 -D5 11 23:23` 图中只分类出：

```text
delta >= 3 catalogue                  1,094,808
suppressible degree-two cases           646,555
common-missing-colour degree-two cases   134,653
degree-two critical residual             137,002
total                                  2,013,018
```

最后 137,002 个 residual 的备用 SAT campaign 没有形成完成且独立认证的
artifact。因此若不接受 Wang--Zhang Lemma 4，本联合主张在现有本地证据下
应判为 **NOT CLOSED**，而不能仍报计算 PASS。

相关本地依赖报告
`OPG145_DEGREE_TWO_DELETION_MINIMAL_SCOPE_AUDIT_2026-07-29.md`
的 SHA-256 为
`d4c7a609af0ab6c147ce0f322c587ff00c17be2109f9104778d62bcc311d4304`。

## 5. 23 边五层是否穷尽

在 \(\delta\geq3,\Delta=5,n=11,m=23\) 下，令 \(x,y,z\) 分别为
5、4、3 度顶点数。则

\[
x+y+z=11,\qquad5x+4y+3z=46,
\]

从而

\[
2x+y=13,\qquad y=13-2x,\qquad z=x-2.
\]

非负性给出且只给出 \(x=2,3,4,5,6\)。对应度序列为

\[
(5^2,4^9),\ (5^3,4^7,3),\ (5^4,4^5,3^2),\
(5^5,4^3,3^3),\ (5^6,4,3^4).
\]

五层互斥且穷尽。\(x=2\) 的 `-d4 -D5` 目录由度数和自动强制第一种
序列；\(x=3,\ldots,6\) 的 `-d3 -D5 | pickg -Mx` 目录由
`pickg -M` 的“最大度顶点数”语义及逐图度序列重检共同固定。
五层之和又与未分层 `-d3 -D5 -u` 总数 1,094,808 一致。

## 6. 24 边及 dense 目录的 `-d2` 范围

24 边和 25--27 边目录使用 `-C -d2 -D5`：

- `-C` 已由第 3 节的 block 归约证明无损；
- 对 11 阶非平凡二连通图，`-d2` 实际上是 `-C` 已蕴含的冗余约束；
- 即使不把 Wang--Zhang Lemma 4 用到这些边数，目录也已经包含全部
  二连通候选，包括 \(\delta=2\) 图，因此不会因二度点理论依赖而漏图；
- \(m\geq24\) 与 `-D5` 自动迫使最大度恰为 5。

所以 m24/dense 使用 `d2/C` 是安全的候选超集，而不是把 m23 的
\(\delta\geq3\) 结论未经说明地扩大到别的目录。

## 7. 审计 JSON 的语义边界

本次核对了 m24 与 dense auditor 的实现合同。成功 JSON 不只是汇总
runner 自报状态；auditor 会：

1. 固定完整 shard 集合、目录名、identity、命令、分母和实现/工具链哈希；
2. 重新运行相同的 `geng` 目录；
3. 独立解码 graph6，并核对阶数、边数、度数、事件图和目录图逐索引相等；
4. 独立重算 3-sparse 判定；
5. 对每份 SAT 见证检查 properness，并用独立 union-find 检查每个颜色对
   的子图无圈；
6. 要求目录耗尽、事件 EOF、计数闭合，且 UNSAT、timeout、unknown 全为零。

m24 wrapper 与 dense auditor 共享基础语义审计引擎
`opg145_dense_run_audit.py`；其当前 SHA-256 与 JSON 记录一致，为
`3532e136195d797128bddf2d3ae2fad3e1d6e3b95c688fb55886ab0563d801e7`。
因此不能宣传为彼此完全无共享代码的两套 verifier，但这不造成已识别的范围
缺口。

目录完整性最终仍依赖冻结 nauty 2.8.8 的非同构枚举正确性及 shard
语义。本次总数重跑、逐边数计数、全 shard 集合和逐事件见证重放是强交叉
检查，不是对 nauty 的形式化证明。

## 8. 联合闭合

计算范围恰为：

| 边数 | 非同构代表数 | 分片数 | 结果 |
| --- | ---: | ---: | --- |
| 23 | 1,094,808 | 80 | 全部 SAT |
| 24 | 1,003,287 | 16 | 全部 SAT |
| 25--27 | 384,122 | 4 | 全部 SAT |
| **合计** | **2,482,217** | **100** | 全部有独立重放通过的七色见证 |

任取满足联合命题前件的图 \(G\)：

1. 握手引理迫使 \(\Delta(G)=5\) 且 \(23\leq m\leq27\)；
2. block 归约与低阶边界迫使潜在反例二连通；
3. 若 \(m=23\)，deletion-minimal 归约进一步迫使 \(\delta\geq3\)，
   并落入五个互斥、穷尽层之一；
4. 若 \(m=24,\ldots,27\)，它直接落入相应 `-C -d2 -D5` 目录；
5. 所有这些目录代表的七色见证均已由审计器独立语义重放。

因此不存在未覆盖的边数、分片或结构类型；联合范围主张通过独立范围审计。

## 9. 最终信任边界

PASS 保留以下公开边界：

- \(\Delta\leq4\) 正例定理和 3-sparse 正例定理按已发表结果使用；
- 排除 23 边二度点实质依赖 Wang--Zhang (2014) Lemma 4；不接受它时尚有
  137,002 个未被完成认证 artifact 覆盖的 residual，联合命题不能由当前
  本地证据闭合；
- 7--9 阶历史运行保留已披露的 legacy provenance 边界；
- 非同构目录完整性依赖冻结 nauty 2.8.8；
- m23 五个 auditor 及 m24/dense auditor 均有内部代码共享，不能称为
  多套完全独立的形式验证器。

这些是证据的信任边界，不是本次发现的反例、漏层或逻辑断点。
