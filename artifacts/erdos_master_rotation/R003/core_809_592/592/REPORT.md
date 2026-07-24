# Erdős #592 — 深度 3 槽位规格与动态并合断点

日期：2026-07-23

状态：`FINITE_STATIC_SPEC_SAT__DYNAMIC_EXTENSION_OPEN`

## 结论先行

本轮没有闭合 #592。官网重新抓取后仍标为 `OPEN`，并仍把唯一未知边界记为
指数参数中恰有三个不可分加项。最小测试例是

\[
\omega^{\omega^3}\longrightarrow
(\omega^{\omega^3},3)^2.
\]

本轮把 R002 的“同秩槽位”想法做成了深度 3 的有限规格，并得到：

- Hajnal--Larson Lemma 10.38 的 Case 4、Case 5 所给顶层先后约束均无
  有限不可满足核；各自恰有一个任务拓扑序；
- 在秩 \(3,2,1\) 上，可以为每棵树的两场互动分配无碰撞槽位，使完整标签
  是两个非空槽位块的并，而每个二人博弈的 coarsening 只保留属于该场的
  槽位块；
- 这只解决了**静态地址和排序**。首个严格未证步骤是动态
  common-extension/commutation 引理：一场二人博弈强迫的保守扩展，能否
  与另两场已经承诺的扩展交换并合，同时保留 critical/decision node、
  clear pair 及 push-up。

因此有限规格没有反杀路线，但也没有把路线提升为证明。

## 1. 官方边界与一手来源校正

官网 #592 在 2026-07-23 抓取时标为 `OPEN`、悬赏 1000 美元，页面最后
编辑于 2026-01-23。其边界为：

- 若 \(\beta\geq3\) 满足所求性质，则
  \(\beta=\omega^\gamma\)；
- Schipperus 证明当 \(\gamma\) 是一个或两个不可分序数之和时为正；
- 四个或更多不可分加项时为负；
- 三加项仍开放。

这里应特别纠正 R002 来源清单的一处错误：其中哈希为
`13b2803e...86fe4e` 的 222 页本地 PDF 实为 Jean Larson 的历史综述
*Infinite Combinatorics*，不是 Hajnal--Larson 的
*Partition Relations* 章节。本轮没有继续把该哈希当作章节证据。

本轮直接核读了作者上传的 85 页 *Partition Relations* 章节，DOI
`10.1007/978-1-4020-5764-9_3`，并定位到下列原文结构：

- Definition 10.21：节点标签；
- Definition 10.23：clear pair；后继秩节点的标签是通向其下方所有
  partition nodes 的孩子编号**集合**（可以有多个元素），秩 \(\omega\)
  的极限节点则记录下方分裂节点的秩集合；
- Definition 10.26：有限博弈 \(G(h,N)\)，原文明确以 \(T(\omega)\)
  为对象；
- Lemma 10.38：architect 分支的蓝三角，Case 4/5 同步三场博弈；
- Definition 10.42：\(\Gamma\)-free 的 commonality、conformity、
  \(\Gamma\)-signality、\(\Gamma\)-forecasting、signal size、push-up；
- Lemma 10.43：若 \(\beta>0\)、\(\Gamma\neq\varnothing\) 且
  \(\omega\notin\Gamma\)，则
  \[
  \operatorname{ot}(X)\geq\omega^{\omega^{|\Gamma|}}.
  \]
  因而 \(T(3)\)、\(\Gamma=\{1,2,3\}\) 正好给目标序型
  \(\omega^{\omega^3}\)；
- Lemma 10.47：builder 分支在 \(T(\omega)\) 上构造
  \(\{\omega\}\)-free 集，并要求每个全局对存在一个作为博弈终局的
  coarsening。

最后一点说明“完整标签可含多个信号，而每个二人 coarsening 只取其中
一部分”并非凭空添加；但把原来的 \(T(\omega)\) 博弈替换为
\(T(3)\) 仍需单独证明，不能直接引用 Lemma 10.47。

## 2. 顶层有限排序规格

把三场互动记为 \(ST,SU,TU\)。Hajnal--Larson Lemma 10.38 的原文
“small levels / larger levels”在 Case 4 给出：

\[
SU<ST\quad(S\text{ 端}),\qquad
TU<ST\quad(T\text{ 端}),\qquad
TU<SU\quad(U\text{ 端}).
\]

唯一拓扑序为

\[
TU<SU<ST.
\]

Case 5 给出：

\[
ST<SU,\qquad ST<TU,\qquad SU<TU,
\]

唯一拓扑序为

\[
ST<SU<TU.
\]

所以源中真正出现的两个 Case 都没有三环。若把三个局部比较任意定向，
八种抽象规格中有六种无环、两种成环；后两种只是防止把“任意局部要求”
误判为自动可排程，并不是来源中实际出现的博弈位置。

## 3. 后继秩上的两个槽位块

\(T(3)\) 的非零秩 \(3,2,1\) 全是后继秩。由 Definition 10.23，一个
clear-pair coarsening 在这些节点的标签是通向相关 partition nodes 的有限
孩子编号集合，大小可以是 architect 指定的任意正整数 \(d\)。Definition
10.41--10.42 又要求在秩 \(3,2,1\) 上产生 signal node；后继秩节点要成为
信号，完整标签必须至少有两个元素。

这两点可由如下静态构造同时满足。对树 \(X\in\{S,T,U\}\) 的每个相关
后继节点 \(r\)，为两条关联边 \(XY,XZ\) 分配互异的非空孩子槽位块

\[
K(X\!\to\!Y,r),\qquad K(X\!\to\!Z,r),
\]

并令完整标签

\[
C_X(r)=
K(X\!\to\!Y,r)\cup K(X\!\to\!Z,r).
\]

二人对 \(XY\) 的 coarsening 只保留
\(K(X\!\to\!Y,r)\)，其元素分别指向该 pair 的 partition nodes。槽位块
按上一节的唯一拓扑序排列，所有树、秩、地址上的代码取互异新值。对秩
\(3,2,1\) 递归分配即可得到深度 3 的有限分支地址骨架。

验证器先在每个秩独立穷举六个 oriented half-edge 槽位块大小均取
\(\{1,2,3\}\) 的全部 \(3^6=729\) 种规格，全部可排程；再对每个 Case
以块大小 2 构造递归证书：

- 三棵树各 \(1+4+16\) 个抽象节点，共 63 个；
- 每节点两个二元块，共 252 个互异代码；
- 126 个非空 pair-block coarsening；
- 每棵树均出现 forecast 秩 \(3,2,1\)。

这证明的是一个有限 SAT 事实：**地址、槽位块粗化和顶层先后次序之间没有
静态冲突。** 它没有验证真实折叠树、博弈史或 push-up。

## 4. 需要重证的有限秩博弈接口

Definition 10.26 原本只定义 \(T(\omega)\) 上的 \(G(h,N)\)，architect
可以指定下一个标签的任意有限大小 \(d\)。Definition 10.23 并不造成
“\(d>1\) 不可行”的立即障碍：有限后继根可以用多个孩子槽位实现该集合。
但正文的 Ramsey dichotomy、Lemma 10.38 和 Lemma 10.47 均按
\(T(\omega)\) 陈述，仍不能只把符号 \(\omega\) 改成 3。

因此候选证明必须先定义一个**有限秩相容博弈**：

- pair-specific move 请求的大小 \(d\) 由一个非空槽位块实现；
- 完整多信号标签在多场 coarsening 的并合层形成；
- 重新证明 Ramsey dichotomy/uniformization 对该有限秩博弈仍成立；
- architect 分支要用槽位同步重证 Lemma 10.38；
- builder 分支要把 Lemma 10.47 的单一 \(\{\omega\}\) 信号改成
  \(\{1,2,3\}\) 的三个 forecast 秩。

有限性本身使“重新做一致化”看起来可行，但本轮没有写出该定理的完整
证明，故它仍是正式义务。

## 5. 候选递归不变量

令 \(P\) 是有限互动图；三角阶段取 \(P=K_3\)。候选不变量
\(\mathcal I(r,P)\) 如下。

1. 对每个 \(X\in V(P)\)，有一个 \(T(r)\) 的 relaxed initial segment
   \((S_X,C_X)\)。
2. 对每条 \(XY\in E(P)\)，存在 pair coarsening
   \(C_X^{XY}\subseteq C_X,\ C_Y^{XY}\subseteq C_Y\)，且
   \[
   ((S_X,C_X^{XY}),(S_Y,C_Y^{XY}))
   \]
   是有限秩二人博弈的合法部分历史；后继节点的非空标签块准确编码该
   pair 的 partition nodes。
3. 每个需要发信号的节点，其完整标签是各 incident pair 标签块的并；
   代码互异、满足源中 Case 4/5 的次序，并维持
   \(\Gamma\cap\{1,\ldots,r\}\)-forecasting。
4. commonality、conformity 与 signal-size 在所有 pair coarsening 之间
   同时成立。
5. **共同扩展闭包：** 任取一条边 \(XY\) 上 architect 的下一合法动作和
   任意 push-up 阈值 \(k\)，可以保守扩展 \(X,Y\)，并在必要时扩展其余
   顶点，使全部 pair 历史、完整标签并合及新元素 \(>k\) 同时保持。

\(r=0\) 是平凡基例。后继步的静态部分正是上一节的孩子槽位块分配；在各槽
内递归调用 \(\mathcal I(r-1,P')\)。

## 6. 首个严格断点

上述归纳仍缺一个不能由“槽位够多”直接推出的引理。

> **动态交换/共同扩展引理。** 同一棵树参与的两场二人博弈中，第一场
> architect 策略强迫的 conservative extension 与第二场已经承诺的
> extension 放在不交后继槽位后可以交换；其并仍是一个合法 relaxed
> \(T(r)\) 初段，每个 pair coarsening 都仍是合法博弈史，并保持
> critical node、decision node、完成顺序、signal size 与 push-up。

静态槽位块只说明孩子编号不会碰撞。真实 builder move 沿 critical
node 延伸，architect 的响应又依赖完整博弈史；所以“不交槽位块”并不自动
蕴含两次扩展可交换。这是当前槽位路线的首个严格断点。

如果该引理失败，最有价值的反例应是一个最小有限博弈史，而不是任意三个
任务的抽象有向环；后者把一次 edge-task 当作原子操作，强于真实的
half-edge move，不能作为反杀证据。

## 7. 可复核证据与边界

运行：

```bash
python3 artifacts/erdos_master_rotation/R003/core_809_592/592/verify_592_depth3_slots.py
```

脚本核对两个来源 Case 的唯一拓扑序、深度 3 地址骨架、完整双块标签、
pair 块粗化、代码无碰撞及三个 forecast 秩。输出同时明确列出未验证的
动态条件。

该脚本不是 \(T(3)\) 或 \(G(h,N)\) 的形式化，更不是
\(\omega^{\omega^3}\to(\omega^{\omega^3},3)^2\) 的有限证明。

## 来源

- Erdős Problems #592，2026-07-23 抓取；页面标为 `OPEN`，最后编辑
  2026-01-23。
- René Schipperus，*Countable partition ordinals*，Annals of Pure and
  Applied Logic 161 (2010), 1195--1215，
  DOI `10.1016/j.apal.2009.12.007`。
- András Hajnal、Jean A. Larson，*Partition Relations*，收于
  *Handbook of Set Theory*，2010，pp. 129--213，
  DOI `10.1007/978-1-4020-5764-9_3`，尤其 §10。
