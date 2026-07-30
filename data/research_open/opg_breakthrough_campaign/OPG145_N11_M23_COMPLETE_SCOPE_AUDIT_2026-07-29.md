# OPG-145 十一阶 23 边完整范围审计

日期：2026-07-29

## 结论

在下列两类外部前提下：

1. 已认证的 \(|V|\leq10,\Delta=5\) 有限边界，以及已有的
   \(\Delta\leq4\) 正例定理；
2. Wang--Zhang (2014) 关于 \(\kappa\)-deletion-minimal 图的
   Lemma 1 和 Lemma 4；

五个互斥、穷尽的计算目录共同证明：

> **每个 11 顶点、23 条边、最大度恰为 5 的有限简单图都有 acyclic
> 7-edge-colouring。**

理论归约先把潜在反例严格限制为二连通且最小度至少 3。握手引理随后把这一
目录按五度点个数 \(x=2,3,4,5,6\) 唯一分成五层。五层共有

\[
8\,986+131\,966+460\,618+418\,542+74\,696
=1\,094\,808
\]

个非同构图代表。80 个分片全部完成，五个独立审计报告均为
`verified_complete`；全部 \(1\,094\,808\) 个代表都有经独立语义重放的
acyclic 7-edge-colouring 见证，零过滤、UNSAT、timeout 或 unknown。

这是一个精确的有限范围定理，不是 OPG-145 一般猜想的证明。它不覆盖其他
边数、十二阶及以上图，也不覆盖最大度 \(6\) 或更大的图。

## 1. 命题与记号

对有限简单图 \(X\)，记 \(a'(X)\) 为其 acyclic chromatic index。需要证明
的本报告范围为

\[
|V(X)|=11,\qquad |E(X)|=23,\qquad \Delta(X)=5
\quad\Longrightarrow\quad a'(X)\leq7.
\tag{1.1}
\]

“acyclic 7-edge-colouring”允许少于七种颜色实际出现；其含义是 proper
edge-colouring 且不存在双色圈。

## 2. 低一阶边界

本报告使用以下已审计结论：

\[
|V(Y)|\leq10,\quad \Delta(Y)=5
\quad\Longrightarrow\quad a'(Y)\leq7.
\tag{2.1}
\]

证据链为：

- \(n<6\) 时不可能有最大度 5；
- \(n=6\) 时每个最大度 5 的简单图都是 \(K_6\) 的子图，而
  [`OPG145_SCOPE_AUDIT_2026-07-29.md`](OPG145_SCOPE_AUDIT_2026-07-29.md)
  给出了 \(K_6\) 的显式 acyclic 7-edge-colouring；
- \(n=7,8,9\) 的历史目录已经由专用 auditor 重新生成目录并重放全部
  见证，见
  [`OPG145_7_9_HISTORY_AUDIT_2026-07-29.md`](OPG145_7_9_HISTORY_AUDIT_2026-07-29.md)；
  审计产物 SHA-256 为
  `acca7d407c667c3e955bcead4b61fddc2a0081ae07fd15fbe578ea8009d39b93`；
- \(n=10\) 的四分片审计产物
  [`audit-all-v2.json`](../../../artifacts/opg_breakthrough/certified/opg145-n10-six-hour/audit-all-v2.json)
  的 SHA-256 为
  `06aaf69f91322275a664456bfae00324f3d1f863bace3e2d2ca45539932d540a`。

已有文献还给出全部 \(\Delta(Y)\leq4\) 图的
\(a'(Y)\leq\Delta(Y)+2\leq6\)。因此可合并写成

\[
|V(Y)|\leq10,\quad \Delta(Y)\leq5
\quad\Longrightarrow\quad a'(Y)\leq7.
\tag{2.2}
\]

## 3. block 归约

### 3.1 block 染色拼接

若图 \(G\) 的每个 block 都有使用至多七色的 acyclic edge-colouring，
则 \(G\) 也有。

对每个连通分量的 block--cut tree 取根。根 block 先染色；附着一个子
block \(B\) 时，它与已染色部分只在父割点 \(v\) 相交。设已染色部分在
\(v\) 使用颜色集 \(T\)，子 block 原染色在 \(v\) 使用颜色集 \(S\)。则

\[
|T|+|S|\leq d_G(v)\leq5<7.
\]

可对 \(B\) 的整个七色调色板作一个全局置换，使 \(S\cap T=\varnothing\)。
于是割点处仍 proper。每个简单圈完全包含在单个 block 中，所以这种拼接
不会产生跨 block 的双色圈。逐个附着所有 block 即得结论。

### 3.2 潜在反例必须二连通

反设 \(G\) 满足 (1.1) 的左侧但 \(a'(G)>7\)。由上一节，\(G\) 含有一个
本身不能用七色的非平凡 block \(B\)。因为 \(B\subseteq G\)，
\(\Delta(B)\leq5\)。

- 若 \(\Delta(B)\leq4\)，已有正例定理给出 \(a'(B)\leq6\)，矛盾；
- 因此 \(\Delta(B)=5\)；
- 若 \(|V(B)|\leq10\)，(2.1) 又给出 \(a'(B)\leq7\)，矛盾。

所以 \(B\) 有 11 个顶点，即覆盖 \(G\) 的全部顶点。含有一个 spanning
2-connected subgraph 的图仍 2-connected，因此 \(G\) 本身二连通。
这严格说明计算目录可使用 `geng -C`，而不是把连通性当作经验过滤。

完整 block 拼接证明及 \(\Delta=5\) 的适用范围也见
[`OPG145_SCOPE_AUDIT_2026-07-29.md`](OPG145_SCOPE_AUDIT_2026-07-29.md)。

## 4. deletion-minimal 归约排除 \(\delta\leq2\)

block 归约本身只给出 \(\delta(G)\geq2\)。排除二度点需要保留
deletion-minimal 的准确前提。

### 4.1 不能混淆两种最小性

“在反例中按顶点数最小”不等于“每个 proper subgraph 都可染”。删边
\(G-e\) 与 \(G\) 同阶，仍可能是坏图。因此不能直接把
Wang--Zhang 的结构引理套到仅按顶点数最小的 \(G\)。

安全做法是在 \(G\) 的所有非 7-可染子图中，按 proper-subgraph
inclusion 取极小者 \(H\)。于是

\[
a'(H)>7,\qquad
\forall J\subsetneq H,\quad a'(J)\leq7,
\]

且 \(\Delta(H)\leq5\leq7\)。所以 \(H\) 是文献定义下真正的
7-deletion-minimal 图。

若 \(|V(H)|\leq10\)，则由 (2.2) 可染，矛盾。因此

\[
V(H)=V(G).
\tag{4.1}
\]

又因 \(\Delta(H)\leq4\) 时已有六色上界，故

\[
\Delta(H)=5.
\tag{4.2}
\]

### 4.2 Wang--Zhang 引理的代入

Tao Wang 和 Yaqiong Zhang 的
*Acyclic edge coloring of graphs*，Discrete Applied Mathematics 167
(2014), 290--303
（[arXiv:1302.2405v4](https://arxiv.org/abs/1302.2405)，
[期刊 DOI](https://doi.org/10.1016/j.dam.2013.12.001)）给出：

- Lemma 1：每个 \(\kappa\)-deletion-minimal 图都是 2-connected；
- Lemma 4：若
  \(\kappa\geq\Delta(H)+2\)，则二度点的每个邻点度数至少
  \[
  \kappa-\Delta(H)+4.
  \]

由 Lemma 1，\(H\) 的最小度至少 2。若 \(G\) 有一个度数至多 1 的顶点
\(v\)，则由 (4.1)
\[
d_H(v)\leq d_G(v)\leq1,
\]
矛盾。

若 \(G\) 有二度点 \(v\)，同理 \(d_H(v)\leq2\)，而 Lemma 1 又给
\(d_H(v)\geq2\)，所以 \(v\) 在 \(H\) 中仍是二度点。对 \(H\) 取
\[
\kappa=7,\qquad\Delta(H)=5.
\]
此时
\[
\kappa=\Delta(H)+2,
\]
而 Lemma 4 要求 \(v\) 的每个邻点度数至少
\[
7-5+4=6,
\]
与 \(\Delta(H)=5\) 矛盾。

因此任何满足 (1.1) 左侧的潜在反例还必须满足

\[
\delta(G)\geq3.
\tag{4.3}
\]

最小性桥、Lemma 3(A)/(B) 的量词审计以及 Lemma 4 的信任边界详见
[`OPG145_DEGREE_TWO_DELETION_MINIMAL_SCOPE_AUDIT_2026-07-29.md`](OPG145_DEGREE_TWO_DELETION_MINIMAL_SCOPE_AUDIT_2026-07-29.md)。

## 5. 握手引理给出的五个互斥层

由 (4.3) 和 \(\Delta(G)=5\)，每个顶点度数属于
\(\{3,4,5\}\)。令

\[
x=\#\{v:d(v)=5\},\quad
y=\#\{v:d(v)=4\},\quad
z=\#\{v:d(v)=3\}.
\]

顶点数和握手引理给出

\[
x+y+z=11,\qquad
5x+4y+3z=2|E(G)|=46.
\]

第二式减去第一式的三倍：

\[
2x+y=13.
\]

所以

\[
y=13-2x,\qquad z=x-2.
\tag{5.1}
\]

由 \(y,z\geq0\)，得到

\[
2\leq x\leq6.
\]

因此恰有以下五个可能度序列：

| 五度点数 \(x\) | 四度点数 \(y\) | 三度点数 \(z\) | 度序列 |
| ---: | ---: | ---: | --- |
| 2 | 9 | 0 | \((5^2,4^9)\) |
| 3 | 7 | 1 | \((5^3,4^7,3)\) |
| 4 | 5 | 2 | \((5^4,4^5,3^2)\) |
| 5 | 3 | 3 | \((5^5,4^3,3^3)\) |
| 6 | 1 | 4 | \((5^6,4,3^4)\) |

不同 \(x\) 的度序列互斥；(5.1) 又说明它们穷尽所有
\(n=11,m=23,\delta\geq3,\Delta=5\) 图。

## 6. 精确目录与完整计数

所有目录均生成有限简单、二连通、11 顶点、恰 23 边的非同构代表，并分成
16 个 `i/16` shard。

| \(x\) | 冻结目录 | 精确数量 |
| ---: | --- | ---: |
| 2 | `geng -q -C -d4 -D5 11 23:23 i/16` | 8,986 |
| 3 | `geng -q -C -d3 -D5 11 23:23 i/16 \| pickg -q -M3` | 131,966 |
| 4 | `geng -q -C -d3 -D5 11 23:23 i/16 \| pickg -q -M4` | 460,618 |
| 5 | `geng -q -C -d3 -D5 11 23:23 i/16 \| pickg -q -M5` | 418,542 |
| 6 | `geng -q -C -d3 -D5 11 23:23 i/16 \| pickg -q -M6` | 74,696 |
| **合计** | 五个互斥层 | **1,094,808** |

这里 `pickg -M x` 按最大度顶点个数过滤。由于
\[
2|E|=46>4\cdot11=44,
\]
而生成器又固定 `-D5`，目录中最大度必为 5。每个 runner 和 auditor
还逐图重新检查了表中的精确度序列，所以不会只依赖 `pickg` 的输出标签。

作为不经过五层求和的交叉检查，使用冻结 nauty 2.8.8 直接运行

```text
geng -C -d3 -D5 -u 11 23:23
```

得到：

```text
1094808 graphs generated
```

所用 `nauty-geng` 二进制 SHA-256 为
`9730b53764bdb28ecd2fdf755fafbc76992050f39e5ea19bb7d91433a26583e9`。
这一未分层总数与五层之和完全一致。

## 7. 五份独立审计

每层 auditor 都严格要求：

1. 根目录恰有 16 个预期 shard；
2. checkpoint 身份、分母、命令、实现文件、工具及动态依赖哈希闭合；
3. 重新运行精确 `geng` 或 `geng|pickg` 目录；
4. 独立解码 graph6 并核对阶数、边数和精确度序列；
5. 逐事件绑定目录记录，核对事件文件 SHA-256 和所有计数；
6. 不信任 SAT 求解器的 `SAT` 字样，而是独立检查每份七色见证的
   properness，并对每个颜色对检查不存在双色圈。

结果如下：

| \(x\) | 度序列 | 审计产物 | 产物 SHA-256 | 审计状态 | SAT / 总数 |
| ---: | --- | --- | --- | --- | ---: |
| 2 | \((5^2,4^9)\) | [`near-regular-six-hour-audit.json`](../../../artifacts/opg_breakthrough/certified/opg145-n11-m23-near-regular-six-hour-audit.json) | `99d102f291785fb9fd43046d475bff5293325201f4aad57298b992c795450f3c` | `verified_complete` | 8,986 / 8,986 |
| 3 | \((5^3,4^7,3)\) | [`three-degree5-six-hour.audit.json`](../../../artifacts/opg_breakthrough/certified/opg145-n11-m23-three-degree5-six-hour.audit.json) | `3643129cd8bd5a90014977f490e65b4611c71b88161df953d8707491f1954b4b` | `verified_complete` | 131,966 / 131,966 |
| 4 | \((5^4,4^5,3^2)\) | [`four-degree5-six-hour.audit.json`](../../../artifacts/opg_breakthrough/certified/opg145-n11-m23-four-degree5-six-hour.audit.json) | `0e656a35920198b61465c09e3802f024bf7e38e165aaf5f158a5d08ce61f92c3` | `verified_complete` | 460,618 / 460,618 |
| 5 | \((5^5,4^3,3^3)\) | [`five-degree5-six-hour.audit.json`](../../../artifacts/opg_breakthrough/certified/opg145-n11-m23-five-degree5-six-hour.audit.json) | `9df82850e70fad1546705fd5c3d05276feac3475fe67cbe42a775a17bd895f39` | `verified_complete` | 418,542 / 418,542 |
| 6 | \((5^6,4,3^4)\) | [`six-degree5-six-hour.audit.json`](../../../artifacts/opg_breakthrough/certified/opg145-n11-m23-six-degree5-six-hour.audit.json) | `66d8331ccfe7a5a626660077e2990803ab335e73d7595f0fae7a13fe55b29971` | `verified_complete` | 74,696 / 74,696 |
| **合计** | 五层 | 五份审计 | — | 全部通过 | **1,094,808 / 1,094,808** |

五层聚合计数为：

```text
generated               1,094,808
eligible                1,094,808
filtered_three_sparse           0
sat                     1,094,808
unsat                           0
timeouts                        0
unknown                         0
```

五个 contract auditor 的 SHA-256 分别为：

| \(x\) | contract auditor SHA-256 |
| ---: | --- |
| 2 | `f49da5922269f475f02928433e1a2c2b681d27e2af2443a810606beac8320389` |
| 3 | `715f69073386f288952f78addf094f471bbe754640d68e5d2f8f09b62957bd6e` |
| 4 | `600102f4f9fbe5290c153d6b35ae5060762836c7d4e7938ecd6cc946bbd24dff` |
| 5 | `84ee97718ccfed8ccaef1636b3a7845eab02fa01557bb80e08021d16dd04d6da` |
| 6 | `7d2bde53b8416f2b4bf0ed26248dcc3b72fd40e997a574b3850535099d70d0e3` |

它们共同使用的独立基础审计引擎
[`opg145_dense_run_audit.py`](../../../src/amra/discovery/opg145_dense_run_audit.py)
SHA-256 为
`3532e136195d797128bddf2d3ae2fad3e1d6e3b95c688fb55886ab0563d801e7`。

## 8. 范围定理的闭合

现在反设存在满足 (1.1) 左侧的反例 \(G\)。

1. 第 3 节由 block 拼接和十阶边界推出 \(G\) 二连通。
2. 第 4 节先抽取真正的 7-deletion-minimal spanning 坏子图，再用
   Wang--Zhang Lemma 1 和 Lemma 4 推出 \(\delta(G)\geq3\)。
3. 第 5 节说明 \(G\) 的度序列必且只能属于五个互斥层之一。
4. 第 6 节的精确目录覆盖该层的全部非同构代表。
5. 第 7 节独立重放说明该层的每个代表都有 acyclic
   7-edge-colouring。

最后一步与 \(G\) 是反例矛盾。因此 (1.1) 成立。

## 9. 信任边界

### 9.1 理论边界

- 排除 \(\delta=2\) 依赖 Wang--Zhang 已发表的 Lemma 4。本次工作核对了
  原文定义、前件和数值代入，但没有从头形式化其较长的换色证明。
- \(|V|\leq10\) 是文献结果、显式基例和计算审计的组合边界。七至九阶的
  历史运行没有保存旧搜索源码与旧动态库的完整字节；专用 auditor 通过
  当前目录重生成、逐事件绑定和见证重放恢复数学证据，但报告中保留了这项
  legacy provenance 边界。

### 9.2 计算边界

- 五个 contract auditor 与搜索 wrapper 分离，不导入对应搜索实现；但是
  五者共享同一个基础 graph6/见证审计引擎。因此这是五个独立合同包装器加
  一个公共独立语义引擎，不应描述为五套完全无共享代码的 verifier。
- SAT 结论由显式染色见证复核，不依赖 SAT 求解器自报正确；但目录完整性
  仍依赖冻结 nauty 的无同构遗漏性质、shard 语义和本地执行环境。未分层
  `-u` 总数、16 分片分母和五层求和提供了交叉检查，而不是对 nauty 的
  形式化证明。
- 审计产物记录并核对 runner、auditor、工具和动态依赖哈希。产物 SHA-256
  绑定的是这次具体 JSON 字节；重新审计时 `audited_at_unix` 可使文件哈希
  改变，而语义计数保持相同。

### 9.3 不得扩大的结论

本报告只证明

\[
(n,m,\Delta)=(11,23,5).
\]

它不证明：

- 所有 11 顶点、最大度 5 的图；
- 11 顶点但边数不为 23 的图；
- 最大度 \(6,7,\ldots\) 的图；
- 12 顶点及更高阶图；
- OPG-145 / Acyclic Edge Coloring Conjecture 的一般情形。

因此正确表述是“OPG-145 的十一阶、23 边、最大度 5 有限层已经闭合”，
而不是“OPG-145 已解决”。
