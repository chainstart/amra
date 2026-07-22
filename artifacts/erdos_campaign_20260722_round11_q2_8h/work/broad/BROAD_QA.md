# 第十一轮广谱工作流敌意 QA

日期：2026-07-22 至 2026-07-23（Asia/Hong_Kong）

判定：**核心有限恒等式通过；#25 两个看似新增的低复杂度特例已主动降级；
全部 16 题仍开放；Q2 停止门槛未达。**

## 1. #25 激活量词

对模数 `n_i` 的完整类记 `R_i`，激活片为 `C_i=R_i cap[n_i,infinity)`。

1. 若 `R_j subset R_i` 且 `i` 更早，则 `n_i|n_j`、`n_i<=n_j`，故
   `C_j subset C_i`；全局删冗余不改变实际 survivor。
2. 一组相容 congruences 的交是模其 lcm 的一个类，激活交的阈值恰为
   `max n_i<=lcm`。因此阈值前最多有一个完整类代表；普通计数与 `x/L`
   的差严格小于 2。
3. 整数同余组两两相容当且仅当共同相容，故非零容斥项与 compatibility
   graph cliques 精确对应，不存在只检查边却遗漏高阶障碍的问题。
4. cutoff-dependent 的链分割和 core `J_x` 都合法，因为主项始终是同一个
   有限周期系统的密度；极限不依赖表示方式。

## 2. #25 极限交换

- 完整有限筛密度 `delta_x` 随 cutoff 单调下降，故有极限 `delta`。
- 动态 core 若含前 `h(x)` 项且 `h(x)->infinity`，则
  `delta<=d(J_x)<=delta_(h(x))`，即使 `J_x` 不嵌套也被夹到同一极限。
- 每个遗漏激活类在 `[1,x]` 至多有 `x/n_i` 个成员，所以 tail 误差没有
  隐藏的 `+1` 累积；激活使首项至少为 `n_i` 正是这里所需。
- 离散 Abel 恒等式逐项复算为

  \[
  \sum_{m\le X}\frac{1_A(m)}m
  =\frac{A(X)}X+\sum_{m<X}\frac{A(m)}{m(m+1)}.
  \]

  因此点态归一化误差按 `1/x` 作 log-Cesàro 平均，报告中的权重方向正确。

## 3. 调和 progression 界

对联合 CRT 类取最小正代表 `1<=r<=L`。完整 progression 的首项贡献为
`1/r`；其余项夹在 `1/((k+1)L)` 与 `1/(kL)` 之间。与 `log X/L`
比较时必须再付 `log L/L`。激活阈值 `M<=L` 至多删去首项 `r`，所以统一
边界

\[
 {2\over r}+{2+\log(2L)\over L}
\]

方向正确。不能把 `r` 换成 `M`：例如最小代表 1、阈值 `M=L` 会删去权重
1，而 `1/M` 无法支付。181,400 个有限参数检查零失败；全参数结论来自
调和数积分比较，不来自浮点扫描。

## 4. 两项主动降级

### 4.1 低整除宽度

证明本身无误，但不产生新覆盖。全局删冗余后，每个真正有效类在任意链原子
化中都必须保留。低宽度条件给有效计数
`R(X)=O((log X)^2/loglog X)`；一般乘积条件也给
`R(X)=O((log X)^2)`。按 dyadic blocks 有 `sum 1/n_i<infinity`，故已被
2026 已知的 light-tail 定理蕴含。

### 4.2 全局有界 compatibility degeneracy

有界退化图有限着色。每个色类中的完整剩余类两两不相容，因而是两两不交的
周期集，其密度和 `sum 1/n_i<=1`。有限个颜色遂给总倒数和收敛。所以退化度
判据只有在 `d_x` 增长、或实际 clique 数显著优于 `R2^d` 时才可能超出旧
特例。报告已相应收紧论文价值，没有把这两项重复证明计作突破。

### 4.3 Möbius 压缩 activated intersections

- 非空 clique 的激活交由 `(L,r,epsilon)` 完全决定：因
  `M=max n_i<=L`，阈值最多删掉最小正 CRT 代表 `r`。
- 先按三元组合并交错系数保持逐点 inclusion--exclusion；再按 `(L,r)`
  合并两个 activation 状态时，删首项部分恰为 `-b(L,r)/r`。
- 完整有限筛密度用同一个合并系数除以 `L`，activation bit 不参与周期
  密度，故主项与调和项配对正确。
- 平方自由块 `n_i=L/p_i` 中没有整除冗余，任意至少二元交确为
  `(L,L,0)`，交错和 `k-1`，raw 项数 `2^k-k-1`。
- 80 个随机系统、3,200 个逐点状态及完整周期密度/调和恒等式用精确
  `Fraction` 复核通过；全参数结论来自代数恒等式。

它逐点不劣于 raw harmonic-clique 付费，并在有限真实系统上可有指数级
代数压缩；尚未给出两种充分条件所覆盖无限系统类的严格分离例。
compressed intersection poset 的总变差也无普遍上界，故不是 #25 闭合或
Q2 主突破。

## 5. #635

- `150=2*75` 与 `154=2*77` 的差为 4，而 4 不整除任一点，故确实独立；
  最小素因子出口分别为 3、7，均落到 147。
- `280=8*35` 与 `286=2*143` 的差为 6，且二者模 6 都为 4，故独立；其
  非平凡 proper divisors 分别为 `{5,7}` 与 `{11,13}`，proper lower
  邻域都恰为 `{273,275}`。这只否定私有邻点，不否定集合级 Hall（此处恰
  取等）。
- prime-oddpart canonical forest 到 `10^6` 只是有限 falsifier，不写成
  全参数定理。

## 6. #686

七个 `m` 的 Mahler 输出包含全部 `m+1` 个有限差分系数：归一化常数为奇，
其余均为偶，故对所有整数 `z`（包括负整数）成立，而非对有限 `z` 采样。
普通 monomial 基的归一化系数有负 2-adic valuation，精确说明该证明模板
为何失效。两项结论都只针对固定 `m`；没有把七个 PASS 外推为 uniform
Cartier congruence。

新增 Mahler 取系数公式由 Stirling 数生成函数逐项推出，是全参数恒等式；
末四项显式公式及 `4|m` 时的 2-adic 下界另经 `m<=32` 全系数精确回归。
它只把首个未解族缩到常数项和 `1<=r<=m-4`，没有证明中间带。

## 7. 计算证据

- `verify_divisibility_width.py`：400 个随机系统；
- `verify_log_clique_entropy.py`：100 个系统、6,812 个 cutoff；
- `verify_hybrid_light_core.py`：600 个非嵌套随机 core；
- `verify_harmonic_weight.py`：181,400 个 progression 参数；
- `verify_mobius_compression.py`：平方自由压缩例及 80 个随机分组恒等式；
- `verify_proper_divisor_audit.py`：两个精确反例及 `10^6` 有限 forest 扫描；
- `verify_basis_gap.py`：七个固定 Cartier 参数。
- `verify_mahler_reduction.py`：`m<=32` 的全 Mahler 系数及末四项公式。

这些程序只验证有限代数、反例和输出证书。任何渐近全称命题均由文档中的
手工证明承担。

## 8. 终态边界

广谱组没有原题闭合，没有改变官方主指数，也没有得到可单独支撑 SCI 二区
论文的本轮新主定理。#25 剩余非降级结果构成潜在 short-note 材料，但仍需
系统文献检索和外部专家审稿。

## 9. 独立工作流交叉 QA 修正

Macaulay/PTE 工作流在不采用本报告结论作前提的情况下复核了 #25 的四个
接口：激活交阈值、每 clique 统一误差、全局删冗余和 Abel 权重，均通过。
它指出 `LOG_AVERAGED_CLIQUE_ENTROPY.md` 原 §5.3 对递减函数把同端点积分
误写成离散和上界；现已改为“左端点项 + 积分”的正确比较。它还建议没有
可实现同余系统分离例时不声称对数平均条件在系统类中“严格”弱于点态条件，
文字亦已降格。这两点不影响主定理，只修正可检验推论与价值表述。
