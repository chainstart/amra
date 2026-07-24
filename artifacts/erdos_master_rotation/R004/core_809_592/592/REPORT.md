# Erdős #592 — commutation 反例与有限秩接口

日期：2026-07-24

状态：`EXACT_ROUTE_OBSTRUCTIONS__ORIGINAL_OPEN`

## 结论

本轮没有证明或否证
\[
\omega^{\omega^3}\longrightarrow
(\omega^{\omega^3},3)^2.
\]
官网于 2026-07-24 抓取时仍把三不可分加项情形列为唯一剩余边界，并标为
`OPEN`。

本轮得到三个严格的路线结论。

1. R003 所需的“独立 conservative extensions 可交换并合”在一个后继
   节点、深度 1 就是假的。失败不是算力问题，而是 clear label 使用
   **并合后孩子的实际编号**。
2. 来源 Lemma 10.38 的 Cases 4/5 并没有使用对称交换；它们分别执行唯一
   的有序回放
   \[
   TU<SU<ST,\qquad ST<SU<TU.
   \]
   后续路线必须预协调并逐次向 architect 策略查询，不能先独立构造再取
   并。
3. finite-\(\Gamma\)-free 强迫每棵 \(T(\omega)\) 树的极限根标签为空。
   因而不能在同一个 finite-\(\Gamma\) builder 族中原样保留依赖非空
   根标签的 coarsening/root-coded histories；Cases 4/5 的 \(d>0\)
   histories 就不能从该族取得。这只排除字面移植，不排除另建“空根、在
   有限秩节点产生 signals”的 builder 分支。

因此 R003 的静态槽位 SAT 证书没有被升级成证明；其首断点现在被精确
收紧为一个**有序、策略感知、保持凸分割节点的 \(T(3)\) 回放引理**。

## 1. 来源中的两个不同标签语义

Hajnal--Larson 的树表示满足：

- Lemma 10.14：秩 \(\omega\) 的极限节点在完整 \(T(\omega)\) 树中只有
  一个立即后继；后继秩节点 \(s\) 有 \(\max(s)\) 个立即后继。
- Definition 10.23：极限根标签记录其下 splitting nodes 的**秩**；
  后继节点标签记录通向 partition nodes 的孩子**编号**。

所以把 \(T(\omega)\) 中的“选 \(d\) 个小/大 levels”直接读成
\(T(3)\) 的“选 \(d\) 个 slots”，改变了对象：

\[
\begin{array}{c|c|c}
 & T(\omega)\text{ 极限根} & T(3)\text{ 后继根}\\
\hline
\text{立即后继数} & 1 & \max(s)\\
\text{标签元素} & \text{下方 splitting rank} & \text{孩子编号}\\
\text{插入影响} & \text{秩/层次} & \text{后续编号整体平移}
\end{array}
\]

R003 的槽位块说明可以写下互异地址，但没有验证插入后编号、凸分割节点、
critical/decision node 或 architect 的历史依赖。

## 2. 对称 common-extension 的最小反例

取一个后继秩节点 \(s\)，基态尚未构造孩子，并在基态标签中预告
\(\{1\}\)。

- 扩展 \(A\) 独立地加入孩子坐标 10。它是唯一孩子，编号为 1；要求
  \(\{1\}\) 合法。
- 扩展 \(B\) 独立地加入孩子坐标 20。它也是唯一孩子，编号为 1；要求
  \(\{1\}\) 合法。

在并树中孩子按 \(10<20\) 排序，编号分别为 1、2。Definition 10.23
于是要求第二段历史使用 \(\{2\}\)，而它保存的是 \(\{1\}\)。若事先给
\(B\) 预分配 \(\{2\}\)，则 \(B\) 单独存在时唯一孩子仍编号 1，反而
不合法。

更一般地，若基态已有 \(r\) 个孩子，\(k\geq2\) 个独立“追加首孩子”
历史都局部要求 \(r+1\)。并合后实际编号为
\[
r+1,r+2,\ldots,r+k,
\]
最多保留一个历史。故在“精确 clear history、标签保持嵌入”这一范畴中，
这样的独立扩展没有对称 pushout。

这不否决有序回放：先加入 \(A\)，再在已经含 \(A\) 的树上生成 \(B\)，
后者从一开始就使用编号 2。但这是一条新的、依赖先前完整状态的历史，
不是原独立历史的交换。

## 3. 来源真正做的是有序回放

Lemma 10.38 Case 4 的三组约束为
\[
SU<ST,\quad TU<ST,\quad TU<SU,
\]
唯一拓扑序 \(TU<SU<ST\)。Case 5 的约束为
\[
ST<SU,\quad ST<TU,\quad SU<TU,
\]
唯一拓扑序 \(ST<SU<TU\)。

原文也明确交替执行：

1. 先用一场博弈的实际响应构造初段；
2. 把该初段（可能换一个 coarsened labeling）作为下一场的真实起点；
3. 再向同一个策略 \(\sigma\) 查询下一标签大小；
4. 在完成屏障后回到较早博弈继续。

这正好避开上一节反例。需要证明的不是“所有不交槽位动作可交换”，而是：

> 给定来源 Case 的无环依赖序，能否在 \(T(3)\) 的每个后继层依次生成
> 实际合法历史，使早先加入的旁支对当前 partner 不产生额外凸分割节点，
> 并使所有 child-index 标签、critical/decision nodes、completion
> barriers、conservative bounds 和最终 coarsenings 同时正确？

这里“旁支不产生额外 partition node”不可省略。Definition 10.19 的
partition node 由两棵树在底层整数顺序中的凸交错决定，并非仅由给某场
博弈预留了哪个抽象槽位决定。

## 4. finite-\(\Gamma\) 的根标签障碍

以下是一个直接由 Definitions 10.41--10.42 得出的精确引理。

**引理。** 若 \(\Gamma\subset\omega\) 有限，且
\(X\) 是 locally \(\Gamma\)-free for \(\omega\) 的
\(T(\omega)\) 标号树族，则每个 \((S,C)\in X\) 的根 \(r\) 满足
\[
C(r)=\varnothing.
\]

**证明。** \(e_\omega(r)=\omega\) 是极限秩。若 \(|C(r)|=1\)，
Definition 10.41 已称 \(r\) 为 signal node；若 \(|C(r)|>1\)，在任意
秩也为 signal node。Definition 10.42 的 \(\Gamma\)-signality 要求
该 signal 的秩在 \(\Gamma\)，或由更早的极限节点标签预告。前者不可能，
因为 \(\omega\notin\Gamma\)；根没有真前驱，后者也不可能。因此只能
\(|C(r)|=0\)。证毕。

coarsening 只删标签元素，不增加元素。所以根标签为空的完整标号不可能
有一个根标签非空的 pair coarsening。Lemma 10.38 的 Cases 4/5
明确给出了 architect 首个根标签大小 \(d>0\) 的 histories；这些
histories 不可能原样成为同一个 finite-\(\Gamma\)-free 族的
coarsenings。故如下候选修改被严格排除：

> 用同一个 finite-\(\Gamma\)-free \(T(\omega)\) builder 族，同时原样
> 承载原证明中所有依赖非空根标签的 pair histories。

这比“尚未证明”更强：该字面版本不成立。但原证明的 architect 与
builder 是二分支；本引理**不**否决重新证明一个根标签恒空、signals
只在秩 \(1,2,3\) 节点出现的 builder 分支。那需要重做 Lemma 10.47
的递归及其每个 global pair 的 clear coarsening，而非简单替换符号。

## 5. 两条仍可能成立、但都是解题级别的路线

### A. 直接重建 \(T(3)\) 博弈

Ramsey dichotomy 的 well-founded play tree 与 Nash--Williams
uniformization 部分看起来可对有限秩重证，因为每局仍有限，builder
响应仍由一个 thin block 参数化。但还必须分别重证：

- architect 分支：上节的策略感知有序回放引理；
- builder 分支：构造真正 \(\Gamma=\{1,2,3\}\)-free 的完整树族；
- 每个全局 pair 的实际 clear coarsening；
- Lemma 10.43 所需的 commonality、conformity、三个 forecast rank、
  signal size 和 push-up。

当前第一个严格断点是 architect 分支的有序回放，因为最小 pushout
反例已说明任何“独立生成后并合”的归纳陈述必假。

### B. \(T(\omega)\) 到 \(T(3)\) 的 trace/pinning

也可以对 \(S\in T(\omega)\) 选择一个规范 \(T(3)\) trace
\(\pi(S)\)，把 \(T(3)\) 上的染色拉回 \(T(\omega)\)，同 trace 的边
染成红。若

\[
\operatorname{ot}(Y)=\omega^{\omega^\omega}
\quad\Longrightarrow\quad
\operatorname{ot}(\pi[Y])=\omega^{\omega^3},
\]

则 \(T(\omega)\) 的已知正结果会推出目标：蓝三角的三个 trace 自动
互异；红大集投影成目标红集。

但这个显示式正是 Galvin--Larson 意义下从大序数到目标序数的
**pinning map** 条件。Specker 已观察到：若 \(\alpha\) pin 到 \(\beta\)
且 \(\alpha\to(\alpha,3)^2\)，则
\(\beta\to(\beta,3)^2\)。因此该 trace 条件本身已经是足以解决 #592
的核心定理，不能把它列作一个例行压缩步骤。尚未构造这样的 \(\pi\)。

## 6. 机器 guard

运行：

```bash
python3 artifacts/erdos_master_rotation/R004/core_809_592/592/verify_592_commutation_guard.py
```

脚本：

- 给出深度 1 的两个独立扩展反例；
- 穷举基态孩子数 \(0,\ldots,5\) 和独立扩展数 \(2,\ldots,5\) 的 24
  个 pushout 配置；
- 核对 Cases 4/5 各自唯一拓扑序；
- 核对 \(T(\omega)\) 极限根与 \(T(3)\) 后继根语义不同；
- 对根标签大小 \(0,\ldots,4\) 核对 finite-\(\Gamma\) 根 guard。

它只验证离散接口，不形式化 ordinal tree，也不决定 #592。

## 一手来源

- Erdős Problems #592：
  <https://www.erdosproblems.com/592>，本轮快照为 `OPEN`。
- René Schipperus，*Countable partition ordinals*，
  Annals of Pure and Applied Logic 161 (2010), 1195--1215，
  DOI `10.1016/j.apal.2009.12.007`。
- András Hajnal、Jean A. Larson，*Partition Relations*，
  *Handbook of Set Theory* (2010), 129--213，
  DOI `10.1007/978-1-4020-5764-9_3`；特别是 Definitions
  10.19/10.23/10.26/10.41/10.42 和 Lemmas 10.14/10.38/10.43/10.47。
- Fred Galvin、Jean Larson，*Pinning countable ordinals*，
  Fundamenta Mathematicae 82 (1975), 357--361，
  DOI `10.4064/fm-82-4-357-361`。

## Novelty guard

本轮的新内容是对仓库 R003 路线的精确反例和根标签障碍，以及把下一义务
改写成可证伪的有序回放命题。没有新的 ordinal partition relation，
没有预印本级完整证明，也不主张文献首创。
