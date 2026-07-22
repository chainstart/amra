# Erdős #25：对数平均相容熵定理

日期：2026-07-22（Asia/Hong_Kong）

状态：**严格、直接针对官方对数密度量词的新充分条件；原题仍开放。**

## 1. 内蕴相容复杂度

设 `n_1<n_2<...`，第 `i` 个模数指定完整类
`C_i=a_i (mod n_i)`，并按题面的 `m>=n_i` 规则激活。

固定整数 cutoff `x`。先在 `n_i<=x` 的有限系统中做全局约简：若
`C_j subset C_i` 且 `n_i<n_j`，则删去 `C_j`。这是合法的，因为细类不仅
作为完整类包含于粗类，而且激活阈值更晚，所以其激活片也包含于粗类激活片。

在剩余有效类上建图 `G_x`：两点相邻当且仅当对应同余式相容。令

\[
 \kappa(x)=\#\{\text{`G_x` 的 cliques，包括空 clique}\}.
\]

有限整数同余式组有公共解，当且仅当每一对相容，因此 `kappa(x)` 正好数出
全容斥中非零的项，而不是一个忽略高阶相容性的图论替代量。

## 2. 定理

令

\[
 \eta(x)=\min\left\{1,{2\kappa(x)\over x}\right\}.
\]

若

\[
 \boxed{
 {1\over\log X}\sum_{2\le x\le X}{\eta(x)\over x}
 \longrightarrow0,}                                  \tag{1}
\]

则 Erdős #25 的激活 survivor `A` 有对数密度。

其值等于完整有限筛密度的单调极限

\[
 \delta=\lim_{x\to\infty}\delta_x,
\]

其中 `delta_x` 是避开全部 `n_i<=x` 完整剩余类的周期密度。

条件 (1) 在数值判据层面弱于点态条件 `kappa(x)=o(x)`：它允许坏 cutoff，
只要它们及其误差在对数尺度上的总质量为零。本轮没有构造一个实际同余系统
来证明这两个条件在可实现系统类中严格分离，故不作“严格弱于”的额外声明。

## 3. 点态计数引理

记

\[
 A(x)=|A\cap[1,x]|.
\]

对有效类作有限容斥。每个相容 clique `Q` 的交是模

\[
 L_Q=\operatorname{lcm}_{i\in Q}n_i
\]

的一个剩余类，并带阈值 `M_Q=max_(i in Q)n_i`。由于 `M_Q<=L_Q`，这个
激活交在 `[1,x]` 中的计数与 `x/L_Q` 相差严格小于 2：周期取整贡献小于
1，而阈值前至多漏掉一个代表元。空 clique 项没有误差。因此

\[
 \boxed{
 \left|{A(x)\over x}-\delta_x\right|
 \le \min\left\{1,{2\kappa(x)\over x}\right\}
 =\eta(x).}                                          \tag{2}
\]

全局约简只删除冗余禁类，不改变 `A(x)` 或 `delta_x`。随着 `x` 增加，完整
筛只会加入禁类，所以

\[
 1\ge\delta_x\downarrow\delta\ge0.                 \tag{3}
\]

## 4. Abel 求和闭合对数密度

写 `1_A(m)` 为指标函数。离散 Abel 恒等式为

\[
 \sum_{m\le X}{1_A(m)\over m}
 ={A(X)\over X}
  +\sum_{m<X}{A(m)\over m(m+1)}.                    \tag{4}
\]

把 `A(m)/m=delta_m+e_m` 代入，其中由 (2) 有
`|e_m|<=eta(m)`。第一项除以 `log X` 后趋零；由 (3) 的普通
Toeplitz/Cesàro 论证，

\[
 {1\over\log X}\sum_{m<X}{\delta_m\over m+1}
 \longrightarrow\delta.                            \tag{5}
\]

误差则由 (1) 控制：

\[
 {1\over\log X}\left|
 \sum_{m<X}{e_m\over m+1}\right|
 \le {1\over\log X}\sum_{m<X}{\eta(m)\over m+1}
 \longrightarrow0.                                 \tag{6}
\]

由 (4)--(6)，

\[
 {1\over\log X}\sum_{\substack{m\le X\\m\in A}}{1\over m}
 \longrightarrow\delta,
\]

证毕。

## 5. 可检验推论

### 5.1 点态 clique entropy

若 `kappa(x)=o(x)`，则 (1) 自动成立，且事实上已有自然密度。这恢复
`COMPATIBILITY_CLIQUE_THEOREM.md`。

### 5.2 宽度与退化度混合上界

对有效模数偏序取任意整除链分割，设链内有效原子数为 `s_j(x)`；又设
`G_x` 有 `R_x` 个顶点、退化度 `d_x`。则

\[
 \kappa(x)\le
 \min\left\{
 \prod_j(1+s_j(x)),\ 1+R_x2^{d_x}
 \right\}.                                         \tag{7}
\]

把 (7) 的右端代入 (1) 就得到只含有限图参数的充分条件。特别地，宽度或
相容退化度允许在一个对数密度为零的 cutoff 集上任意恶化。

### 5.3 按模数跳点记账

在相邻模数 `n_j<=x<n_(j+1)` 之间，有限系统不变，故 `kappa(x)` 为常数
`kappa_j`。令

\[
 f_j(t)={\min\{1,2\kappa_j/t\}\over t};
\]

它随 `t` 递减。离散段不能直接用同端点积分作上界；正确的积分比较是

\[
 \sum_{n_j\le x<n_{j+1}} f_j(x)
 \le f_j(n_j)+\int_{n_j}^{n_{j+1}}f_j(t)\,dt,   \tag{8}
\]

或等价地使用左移一个单位的积分。积分主项为

\[
 \int_{n_j}^{n_{j+1}}
 \min\{1,2\kappa_j/t\}{dt\over t}.
\]

它可显式分成对数项与 `2kappa_j/t` 项；连同 (8) 的左端点项一起求和，可
检验快速增长、间歇高熵或混合结构的模数列。这里不再把递减函数的积分误写成
离散和上界。

## 6. 范围与论文价值

本定理真正使用了官方目标是**对数**密度，把此前逐 cutoff 的自然密度判据
扩展到 log-Cesàro 可积误差；它不是常数优化。它仍是充分条件，而一般系统
可能在正对数比例的尺度上满足 `kappa(x)>=c x`，所以不能标记原题闭合。

与整除宽度、相容图退化度定理合并后，材料已经形成一组自包含的结构结果；
当前判断可写成专题短文，但在没有覆盖高相容熵核心或完整新颖性检索前，仍不
单独评为 SCI 二区主突破。
