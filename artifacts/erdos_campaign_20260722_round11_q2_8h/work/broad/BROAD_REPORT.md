# Erdős 21 题第十一轮：广谱工作流终态报告

日期：2026-07-22 至 2026-07-23（Asia/Hong_Kong）

覆盖题目：#25、#143、#148、#301、#325、#332、#377、#539、#635、
#686、#788、#934、#950、#952、#963、#1063。

本工作流的计费单位是统一窗口内的 7,200 秒，不是给每题虚构相同用时。主
目标仍为原题闭合；阶段引理、有限证书和路线反例均未触发提前停止。证明在
统一硬边界冻结；终态以根目录汇总和 JSON 为准。

## 总判定

- 原始命题完整证明/证否：**0**；
- 新改变官方主阶或主指数：**0**；
- 达到本轮 SCI 二区提前停止门槛：**0**；
- 最强正向推进：#25 的相容图、动态轻尾/低 clique 核、调和加权 clique
  与 Möbius 压缩激活交判据；后者在显式无冗余平方自由块上把指数级重复
  clique 付费压到线性系数。低整除宽度结论因被可和尾特例蕴含而降级；
- 最有价值的反方推进：#635 两种自然 proper-divisor 出口模板均有严格最小
  反例；#686 普通单项式系数路线存在随层数增长的 2-adic 亏损，且新的
  divided-power 公式把高层缺口精确压到常数项和中间 Mahler 系数带。

## 逐题矩阵

| 题号 | 本轮实际攻击/审计 | 本轮新增严格结论或边界 | 当前不可绕过的缺口 | 终态 |
|---:|---|---|---|---|
| 25 | 将 cutoff 重分链、实际 CRT 相容图、log-Cesàro、动态 core/tail、调和容斥和 intersection-poset 压缩统一 | (i) 低宽度定理正确但被 light-tail 蕴含；(ii) 低实际 clique 数给自然密度；(iii) clique 误差只需对数平均为零；(iv) 动态低 clique 核/轻尾有自然与对数版；(v) 可按 `r_Q,L_Q` 支付调和边界；(vi) 先按同一激活 CRT 进程作 Möbius 合并，再合并 activation bit，得到逐点不劣的总变差判据；平方自由有限块把 `2^k-k-1` 次付费压成 `k-1`，但尚无无限系统类严格分离例 | 尚不能证明任意系统的压缩 intersection-poset 总变差为 `o(log x)`，也不能控制不同进程间的带符号抵消 | **五组未降级判据 + 一项降级重证明；OPEN；潜在 short note/论文一章** |
| 143 | 重开 primitive fibre 的 numerator-gcd / denominator-lcm / dyadic-band 三轴拼接 | 没有找到能在 band 求和前保留符号、同时把 Möbius 边界作 Carleson 收费的新估计 | 薄 fibre 边界项与跨分母有符号拼接 | 路线未跨旧接口；OPEN |
| 148 | 复查已得 `446/289` 五项界后最晚大素数 allocation 与临界窗 | 临界窗 `u asymp X^(50/289)` 仍使全部已发表逐点 `f_4` 分支同时饱和；逐 `p` 或逐除数级数取绝对值没有新幂节省 | 必须在临界窗对变化素数/除数同余作真正相关平均 | 既有新上界保留；本轮无新指数；OPEN |
| 301 | 重新审视典型多表示能否经局部舍入产生低拥塞规范边 | 没有从逐左点高表示数推出右端容量；局部 fractional Hall 仍可能把正比例质量压向同一高端点 | 从分块定理提取全局低拥塞规范表示或带容量 Hall | 旧瓶颈确认；OPEN |
| 325 | 再查零锥 dyadic tube 的二阶横截曲率路线 | Euler 双四次幂射线继续否定点态 coercivity；仅计 tube 数而不计每管算术质量仍整整少一幂 | 零层锥管的 determinant/整数点总质量估计 | 路线尸检；OPEN |
| 332 | 检验弱复现假设与历轮精确差谱反例是否兼容 | additive-basis、粗增长、稀疏 Fourier 支撑都不能排除零密度精确差谱构造 | 找到自然且严格弱于正上 Banach 密度的局部模式复现条件，或分类反例 | 开放式问题未完成 |
| 377 | 尝试把每个素数的 base-`p` 递降放入同一加权筛过程 | 固定 `p` 递归精确，但不同 `p` 的商不同；压成一个标量过程会丢失 distinct-prime 信息 | 保留全深度数字条件的 distinct-small-prime sieve | 精确接口未推进；OPEN |
| 539 | 交叉检查高能量父层、稀疏曲面、suspension、非坐标边界 | 四类逃逸可以同时存在；换坐标或薄层厚度仍不能统一改善全部正正交象限投影 | 构造或排除 `eta(G_i)>=exp(-O(i))` 且目标投影仅平方根量级的族 | 多路线 no-go；OPEN |
| 635 | 攻 proper-divisor 出口与 canonical 多圈 surplus 的联合 Hall | 最小素因子映射在独立对 `{150,154}` 上撞到 147；“每个非空独立集有私有 proper lower 邻点”被 `{280,286}` 严格否定，其两侧 proper 邻域都恰为 `{273,275}`。集合级 Hall 候选仍存活；prime-oddpart canonical 子图到 `10^6` 的 forest 仅为有限证据 | 证明 composite-oddpart 独立子集的集合级 proper Hall，并与 canonical 伪森林作避碰增广 | 两条模板证伪；无新界；OPEN |
| 686 | 把高 Cartier 层由数值采样改成全整数 Mahler 证书，并比较 monomial/Mahler 基 | 对 `m=16,24,32,40,48,56,64` 给出完整有限差分证书，故每个固定 `m` 对所有整数 `z` 的目标估值成立；归一化普通单项式系数的最低估值为 `-14,-17,-30,-27,-41,-38,-62`，否定 coefficientwise monomial 模板；另得全参数公式 `Delta^r C_m(0)=r![v^(m-r)]H_m/prod_(j<=r)(1-jv)`，并在首个未解族统一排除末四个 Mahler 系数为障碍 | 需要控制常数项及中间系数带 `1<=r<=m-4` 的 uniform divided-power/Cartier 归纳；固定七个参数不处理变化辅助参数 | 全参数路线化简 + 固定参数严格扩展；OPEN；非 Q2 |
| 788 | 复查半密度临界区的多和删点模式熵 | 单个和仍可有指数多个最小删点模式，固定共同母集和逐模式 union bound 均不产生 `exp(o(s))` 证书族 | 利用不同和之间的相关性压缩联合证书 | 路线未跨旧接口；OPEN |
| 934 | 再查 quotient induction 后交换子 fibre 的填充 | 投满商群仍不蕴含填满 fibre，普通非交换 Ruzsa covering 的迭代损失不可闭合 | quadratic intersection 或 fibre-saturation 引理 | 核心缺口不变；OPEN |
| 950 | 尝试把 endpoint 权重直接保留在 prime-tuple 正性泛函 | count-only Maynard 输入无法保证倒数质量落在指定后向 dyadic shells；Abel 变换不能恢复已丢坐标 | endpoint-weighted sieve 或同步命中趋多指定 shells | 需要新素数输入；OPEN |
| 952 | 扩展固定走廊到变化方向族与分层 CRT 墙 | 固定有限走廊仍不足；方向变化使独立墙模数增至 `exp(O(R log R))` 且位置失控 | 同时控制 bounded step、Gaussian-prime 可达性和变化方向阻断 | 严格子类之外 OPEN |
| 963 | 将 round-10 reachable-wrap clique 收费尝试跨层累计 | 单层损失由实际 Cayley clique 数而非 `|W|` 控制仍正确；本轮没有从真实 zero fibres 推出 `sum_j log kappa(W_j)=O(1)` | 证明可达 wrap 的跨层相关/有界总 clique 亏损 | 无新全局递推；OPEN |
| 1063 | 按用户要求停止同一路线常数永动，重新比较上下界尺度 | 历轮 `n_k>=(1-o(1))k^2/log k` 仍是既有论文级阶段下界；本轮没有不同增长级的新下界或多项式上界 | 多项式构造上界或指数型下界；常数刷新不是突破 | 既有论文候选；原题 OPEN |

## #25 的六层结果、相互关系与一次重要降级

### 1. cutoff 可重分链的宽度定理

有限 Dilworth 分割可在每个 `x` 重新选择。同一整除链中删去被粗类覆盖的
细类后，剩余激活原子不交；每条链至多 `1+log_2 x` 个原子。全部容斥端点
数至多 `prod_j(1+s_j(x))`。这个数为 `o(x)` 时，真实计数与完整有限筛密度
相差 `o(x)`。主项与链分割无关并单调收敛，所以不需要一个预先固定的无限
链分割。**但这不再计作新覆盖：**全局删冗余后的有效模数计数至多
`O((log x)^2)`，dyadic 求和已给 `sum 1/n_i<infinity`，可直接调用已知轻尾
定理。

### 2. 实际 compatible-clique 定理

非零 CRT 交恰好是约简相容图的 cliques；整数同余组的两两相容等价于共同
相容，没有高阶 Helly 缺口。因此端点误差可从所有笛卡尔元组缩为实际 clique
数。退化序给 `kappa<=1+R2^d`。敌意复核同时指出：全局有界退化度可有限
着色，而每个不相容色类的完整剩余类互不相交，已迫使 `sum 1/n_i<infinity`；
所以真正超出已知可和尾的用途必须让退化度增长，或直接利用比退化度估计小得
多的实际 clique 数。

### 3. 对数平均版本

若 `eta(x)=min(1,2kappa(x)/x)` 满足

\[
 {1\over\log X}\sum_{x\le X}{\eta(x)\over x}\to0,
\]

离散 Abel 求和直接给官方要求的对数密度。它允许任意坏 cutoff，只要坏尺度
的对数质量为零。

### 4. 动态 light-tail / structured-core 混合

每个 `x` 可选不嵌套核心 `J_x`，只要求它含一个趋于无穷的初段。遗漏类以
`sum 1/n_i` 收费，核心以 `2kappa(J_x)/x` 收费；两者点态趋零给自然密度，
其和只在对数平均趋零也给对数密度。这同时包含已知可和尾特例与纯低 clique
特例，并覆盖两者的混合系统。

### 5. 调和加权 clique 边界

对 clique `Q` 的联合 CRT 类，记最小正代表为 `r_Q`、模数为 `L_Q`。直接
对调和和容斥得到

\[
 |H_A(X)-\delta_X\log X|
 \le1+\sum_{Q\ne\varnothing}
 \left({2\over r_Q}+{2+\log(2L_Q)\over L_Q}\right).
\]

右端若为 `o(log X)`，即有对数密度。这里激活在 `M_Q<=L_Q` 前至多删去一个
完整类代表，故必须按实际 `r_Q` 付费，不能错误换成 `M_Q`。这个判据把纯
clique 个数替换成带 CRT 算术的边界复杂度。

### 6. Möbius 压缩 activated-intersection 边界

把给出同一 `(L,r,epsilon)` 的 clique 的交错符号先精确合并，再把同一
`(L,r)` 的两个 activation 状态写成“共同完整进程减去至多一个首代表”，
得到更小的边界 `B_*(X)`；`B_*=o(log X)` 推出对数密度，而压缩系数总变差
`sum(|a|+|b|)=o(X)` 推出自然密度。对
`L=p_1...p_k` 及零类模数 `L/p_i`，全部至少二元交都等于 `(L,L,0)`，
压缩系数是 `k-1`，而 raw clique 数是 `2^k-k-1`。这严格证明压缩不是
记号改写，但未证明两判据覆盖的无限系统类严格分离，也没有任意系统上的
总变差上界。

五项证明分别见 `25/`。四份随机/精确有限回归共检查链宽、CRT 两两--整体
相容、退化度 clique 界、动态 core 不等式、Abel 恒等式和调和 progression
界；它们只作证伪器，全参数结论来自文档证明。

## 证据边界与论文价值

1. #25 已形成结构一致的专题材料；但低宽度分支和全局有界退化度分支分别被
   可和尾特例蕴含，必须从新颖性清单中剔除。其余判据的定向检索未发现完全
   相同表述，但不是穷尽性证明。当前最多定位为待外审 short note / 后续论文
   一章；没有控制高相容熵核心，故不标 SCI 二区主突破。
2. #686 的七个证书对每个固定 `m` 都是“所有整数 `z`”的证明，而不是有限
   `z` 扫描；新增 Mahler 取系数公式是全参数恒等式，末四项排除也是全参数
   证明，但它们仍未控制中间系数带，有限个 `m` 也不能外推为 uniform
   Cartier 定理。
3. #635 的反例只否定证明模板，不是否定精确 `t=2` 猜想，更不否定官网已经
   解决的渐近子问。
4. #148、#1063 的既有论文候选没有因本轮复核失效；也没有把旧成果再次计作
   本轮 Q2 突破。

## 文件入口

- `25/DIVISIBILITY_WIDTH_THEOREM.md`；
- `25/COMPATIBILITY_CLIQUE_THEOREM.md`；
- `25/LOG_AVERAGED_CLIQUE_ENTROPY.md`；
- `25/HYBRID_LIGHT_CORE_THEOREM.md`；
- `25/HARMONIC_WEIGHTED_CLIQUES.md`；
- `25/MOBIUS_COMPRESSED_CLIQUES.md`；
- `25/SOURCE_NOVELTY_AUDIT.md`；
- `635/PROPER_DIVISOR_HALL_AUDIT.md`；
- `686/CARTIER_BASIS_AUDIT.md`。
- `686/MAHLER_COEFFICIENT_REDUCTION.md`。
