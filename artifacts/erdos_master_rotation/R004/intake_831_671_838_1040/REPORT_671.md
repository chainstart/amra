# Erdős #671：2026 候选完整证明的逐量词与 Lean 审计

## 结论先行

- 官网题目主状态在 2026-07-24 仍为 `OPEN`。
- 但官网讨论区在 **2026-06-22 23:12** 已公开 Liam Price 的完整证明、Overleaf
  源文和 Lean 链接（post-7142）；到 **2026-07-15 13:26:03** 才登记为正式
  proof-claim #61。后一日期不是首次公开/完成日期。
- 本轮逐行核对自然语言证明，未发现量词、全序列或节点基数缺口。
- 已解码公开 Lean 源码并做静态扫描；原文件无 `sorry`、`admit`、`sorryAx`、
  `axiom` 或 `opaque` 声明。
- 原 Lean 针对较新的 Mathlib API。本机 Mathlib 4.27 上仅作 7 个标识符旧名替换，
  无任何项、假设、结论或证明策略变化后完整编译成功：
  \[
  \texttt{VERIFIED\_BY\_LOCAL\_LEAN}.
  \]
  `#print axioms erdos_671` 只输出
  `[propext, Classical.choice, Quot.sound]`，没有 `sorryAx`。

数学判断：这是一份通过本轮实质审计、形式化验证且覆盖原题两问的完整候选闭合。
行政判断：站方尚未把它吸收进题目备注，官网仍标 `OPEN`，不能写成
“officially closed”。

## 冻结题面

对每个 \(n\ge1\)，取 \([-1,1]\) 中 \(n\) 个互异节点 \(a_i^n\)，令
\(p_i^n\) 为 Lagrange 基函数，
\[
 \mathcal L^nf(x)=\sum_{i=1}^nf(a_i^n)p_i^n(x),\qquad
 \lambda_n(x)=\sum_{i=1}^n|p_i^n(x)|.
\]

第一问要求存在一个三角阵，使每个连续 \(f\) 都存在某点 \(x\)，同时满足
\[
 \limsup_n\lambda_n(x)=\infty,\qquad
 \mathcal L^nf(x)\to f(x).
\]

第二问要求更强的同一三角阵：
\[
 \limsup_n\lambda_n(x)=\infty\quad\text{对每个 }x,
\]
同时每个连续 \(f\) 仍至少有一个全序列收敛点。

## 自然语言证明的结构审计

### 1. 碰撞对行

对有限目标集 \(Z\) 和每个目标 \(z\) 指定一个样本对 \(\{r,s\}\)。把公共样本点
\[
 c_j(t)=c_*+t\xi_j
\]
挤到保留区间中的 \(c_*\)，并把目标行中的一个节点改成
\[
 y_{e,z}(t)=z+t\,\frac{A(\xi_r-\xi_s)}{Q_{e,z}}.
\]
Lagrange 乘积公式给出，在 \(z\) 处三个主系数分别趋于
\[
 A,\quad -A,\quad1,
\]
其余系数趋零。有限性允许统一选小 \(t\) 和目标小区间 \(J_z\)，使指定行满足
\[
 \lambda\ge A,\qquad
 |\mathcal Lf(x)-f(x)|
 \le A|f(c_r)-f(c_s)|+\varepsilon\|f\|_\infty+\omega_f(\rho),
\]
而同阶段所有未指定碰撞行在 \(J_z\) 上满足 \(\lambda\le2\)。

审计点：

- \(Q_{e,z}\ne0\) 来自保留区与目标/背景节点分离；
- 一个行可同时服务不同父区间中的有限多个目标，所有极限可统一；
- 误差分解中的 \(A(f(c_r)-f(c_s))\) 与系数符号一致；
- 从目标点扩展到闭小区间只用了有限多个连续不等式。

### 2. 外部爆发行

对有限个保护闭区间 \(V=\bigcup I_j\)，在 \(\operatorname{int}V\) 内放一对距离
\(\delta\) 的近碰撞节点以及每个 \(I_j\) 内的节点。近碰撞节点的基函数在
\([-1,1]\setminus V\) 上为 \(1/\delta\) 量级，故可令外部 Lebesgue 函数统一大于
任意 \(H\)。同时在每个内部节点附近由连续性缩出子区间，使 \(\lambda\le2\)。

审计点：证明使用的紧集是
\([-1,1]\setminus\operatorname{int}V\)，其与所有固定节点有正距离；所以所谓
“统一正下界”确实成立，端点没有遗漏。

### 3. 分阶段嵌套

阶段 \(k\)：

1. 先为此前所有保护区间处理缺失编号的 filler rows，并逐次缩区，使其稳定；
2. 取 \(N_k=k^3+1\) 个公共样本点，对每个样本点对建立一个碰撞行；
3. 每个父区间为每个样本对保留一个子区间；
4. 加一个外部爆发行，再次缩区。

所有行编号连续覆盖，且行大小至少为当时需要预置的节点数。极限 Cantor 集
\(K=\bigcap C_k\) 中的每点每阶段落入一个高碰撞行；不在 \(K\) 中的点最终被每个
外部行覆盖。因此每一点的 Lebesgue 函数都共尾无界。

### 4. 对每个 \(f\) 选择全序列收敛点

\(N_k=k^3+1\) 个值 \(f(c_{k,j})\) 都在
\([-\|f\|_\infty,\|f\|_\infty]\) 中。排序和抽屉原理给一对
\[
 |f(c_{k,r})-f(c_{k,s})|
 \le\frac{2\|f\|_\infty}{k^3}.
\]
在每阶段选择该点对所标记的子区间；直径趋零的嵌套闭区间给唯一 \(x_f\)。
选中的高碰撞行误差满足
\[
 |\mathcal L_nf(x_f)-f(x_f)|
 \le \frac{2\|f\|_\infty}{k^2}
 +\frac{\|f\|_\infty}{k}+\omega_f(1/k)\to0.
\]
同阶段其余所有行在 \(x_f\) 处有 \(\lambda\le2\)。Lebesgue 不等式与 Weierstrass
逼近给这些行的误差至多 \(3E_{n-1}(f)\to0\)。两类行穷尽每个阶段的全部连续编号，
所以证明的是 **全序列** 收敛，不是只取子序列。

这正是 Erdős 1958 年易构造所缺的关键：旧构造只让每点无限多次进入一个好短区间，
只产生收敛子序列；新构造把未选碰撞行、filler 行和 exterior 行全部压到统一
Lebesgue 上界二。

## Lean 最终定理逐量词映射

Lean 定理 `Erdos671.erdos_671` 的核心类型为：

```text
∃ X : ∀ n : ℕ, Row (n + 1),
  (∀ n, card(nodeSet (X n)) = n + 1) ∧
  (∀ x, ∀ A : ℝ, ∀ N : ℕ,
     ∃ n ≥ N, A ≤ lebesgue (X n) x) ∧
  ∀ f : C(Interval, ℝ), ∃ x : Interval,
    Tendsto (fun n ↦ interpolant (X n) f x) atTop (𝓝 (f x)) ∧
    ∀ A : ℝ, ∀ N : ℕ,
      ∃ n ≥ N, A ≤ lebesgue (X n) x
```

对应关系如下。

| 原题量词/对象 | Lean 对象 | 核对 |
|---|---|---|
| 存在一个固定三角阵 | `∃ X : ∀ n, Row (n+1)` | `X` 在 `f,x` 之前量化 |
| 第 \(n+1\) 行有恰 \(n+1\) 个互异节点 | `Row (n+1)` 的 embedding 及 `card(nodeSet)=n+1` | 不只是列表长度，embedding 保证互异且值在 `Interval` |
| \(C[-1,1]\) 中每个实连续函数 | `∀ f : C(Interval, ℝ)` | `Interval = Icc (-1) 1` |
| 每个 \(f\) 存在一个点 | `∃ x : Interval` | 次序为 `∀f∃x`，正确允许 \(x\) 依赖 \(f\) |
| 全序列插值收敛 | `Tendsto ... atTop` | 不是子序列 |
| 每个点 \(\limsup\lambda_n=\infty\) | `∀x∀A∀N∃n≥N, A≤lebesgue...` | 这是更明确的共尾无界表述 |
| 所选收敛点也 Lebesgue 无界 | 最后一个 `∀A∀N∃n...` | 由 everywhere-unbounded 已蕴含，但再次打包 |
| 第一问 | 取上述 `x` 和最后一项 | 被第二问的构造直接蕴含 |
| 第二问 | 中间 everywhere-unbounded 与 `∀f∃x Tendsto` | 完整覆盖 |

`fundamental` 由 Mathlib 的 `Lagrange.basis` 定义；`interpolant` 和 `lebesgue`
分别是有限和及绝对值和，不存在把目标定理替换成抽象公理的情况。

## 形式验证和来源完整性

详细哈希、日期、HTML 定位和静态扫描见 `671/source_audit.txt`。

关键事实：

- Overleaf `main.tex` SHA-256：
  `f23f4e93027fd9ad47677e914e533473534332a162579bb564f50e4e82aed1e0`
- 解码原 Lean（125,059 bytes、末尾无 LF）SHA-256：
  `3854ae85aca322b5ad2c65fb9c7bae5ca19ed939ceca99521365d8690b8d8923`
- 本机兼容副本只替换 7 个 API 标识符，并因编辑工具增加一个末尾 LF；SHA-256：
  `2da73e90ffcde451b6479f8b63f81e2150c26c40e6e1002e71d2e4b596a045a6`
- 无末尾 LF 的精确七替换版本应为：
  `22760be7e4d811966c17ddd34f51753ab9098583b041a054b925a9d8fcb4e122`
- 本机命令：
  `taskset -c 0 timeout 1200 lake env lean Erdos671.mathlib-4.27.lean`
- 完整成功输出：
  `'Erdos671.erdos_671' depends on axioms: [propext, Classical.choice, Quot.sound]`
- 退出码：`0`。

原文件在旧 Mathlib 上的失败日志也保留。那些错误恰为 7 个新版 camelCase 名称在
旧版不存在；错误恢复过程临时引入的 `sorryAx` 在兼容编译后消失，不能误报成源码
含洞。

## 闭合与发表级别

- `VERIFIED_BY_LOCAL_LEAN`: `YES`
- 自然语言证明审计：`PASS`
- 覆盖官网两问：`YES`
- 官网行政状态：`OPEN`
- 数学闭合分级：`LOCALLY_VERIFIED_FULL_SOLUTION_CANDIDATE`
- SCI 二区判断：解决完整开放问题且有自足短证明和形式化，成果级别达到可投稿标准；
  但它已于 2026-06-22 公开，作者/优先权属于公开提交者，本轮成果是独立核验而不是
  新证明申领。
- 首断点：不再是数学证明缺口，而是外部专家/编辑复核与官网状态吸收。
