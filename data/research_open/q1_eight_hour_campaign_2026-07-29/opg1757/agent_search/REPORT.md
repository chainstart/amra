# OPG-1757：全边对闭包与假孪生反例搜索

日期：2026-07-29

## 结论

没有找到 uniform-forest edge negative correlation 的反例。

本轮最重要的纠偏是：桥/叶边、串联、平行、1-sum、2-sum 和“保留一条边
并加入若干条平行二边路径”都已经落在既有的 **I-Rayleigh 加权闭包理论**
内。这些操作本身不是可发表的新闭包定理。真正没有被这些文献覆盖、仍值得
研究的是**复制一个非邻接假孪生顶点**。

对假孪生操作，本轮完成了：

1. `K4`、`K5` 和仓库九阶近边界种子的逐顶点复制；
2. 单位权下的全部边对精确重数；
3. 独立正权下的 log-uniform 随机 I-Rayleigh 筛查；
4. 对随机筛查中最接近等号的实例作精确有理数复核和逐坐标二次式检查。

所有检查均保持非负。最危险实例的相对裕量约为

\[
2.2181566798540307\times 10^{-16}>0,
\]

但它仍是严格正值，不是反例。

## 1. 已有定理准确覆盖了什么

写森林生成多项式为

\[
I_G(\mathbf y)=\sum_{F\text{ forest}}\prod_{e\in F}y_e
\]

以及 Rayleigh difference

\[
\Delta_G(a,b)=I_G^a I_G^b-I_G I_G^{ab}.
\]

I-Rayleigh 要求对任意正权 \(\mathbf y>0\) 和任意不同边 \(a,b\)，
\(\Delta_G(a,b)\geq0\)。

### 1.1 桥、串联链和平行边

Huang 2023 的 Lemmas 6.1--6.4 和 Theorem 2.6 对任意异质正权
\(\{\beta_e\}\) 给出以下等价约化：

- 桥边可以删除；其森林选择只贡献独立因子 \(1+\beta_e\)；
- 一条由边 \(e_1,\ldots,e_k\) 组成的度二串联链可压成一条有效边，权重

  \[
  \widetilde\beta
  =
  \frac{\prod_i\beta_i}
       {\prod_i(1+\beta_i)-\prod_i\beta_i};
  \]

- 一族平行边可合成一条有效边，权重

  \[
  \widetilde\beta=\sum_i\beta_i.
  \]

所以，只要约化核心是 I-Rayleigh，任意桥/叶星、串联和平行扩张后的**全图
全部边对**仍为 I-Rayleigh，而不只是某个指定继承边对。

来源：

- Xiangyu Huang, *On Negative Correlation of Arboreal Gas on Some
  Graphs*, arXiv:2311.00965.

### 1.2 1-sum 和 2-sum

1-sum 的森林生成多项式直接因解：

\[
I_{G\oplus_1 H}=I_GI_H.
\]

同一因子中的边对裕量乘另一个因子的平方；跨因子边对恰为零。

Wagner 2008, Theorem 5.8 明确证明 I-Rayleigh matroid 类在 2-sum 下
闭合。对独立集生成多项式，其 2-sum 公式为

\[
I_{L\oplus_g M}
=
I_L^{g}I_{M,g}+I_{L,g}I_M^{g}-I_{L,g}I_{M,g}.
\]

来源：

- David G. Wagner, *Negatively Correlated Random Variables and Mason's
  Conjecture for Independent Sets in Matroids*, Annals of Combinatorics
  12 (2008), arXiv:math/0602648.

### 1.3 Series-parallel 图及平行二边路径束

Erickson 进一步证明每个 series-parallel 图的森林 Rayleigh difference
都具有正单项式乘平方和表达，因此它们对全部正权 I-Rayleigh。

若保留旧边 \(e=uv\)，并加入 \(r\) 条互不相交的单位权二边路径
\(u-x_i-v\)，每条路径先串联约化为权 \(1/3\)，再与 \(e\) 平行合并，
故旧核心看到的有效权为

\[
y_e^{\mathrm{eff}}=1+\frac r3.
\]

若用长度 \(L\) 的单位权路径替换 \(e\)，有效权为

\[
y_e^{\mathrm{eff}}=\frac1{2^L-1}.
\]

因此仓库中新得到的局部六边对公式是正确的，但“把闭包补成全图所有边对”
这一层已由 I-Rayleigh 的串/并联闭包涵盖，不能作为新的主定理。

来源：

- Alejandro Erickson, *Sums of Squares and Negative Correlation for
  Spanning Forests of Series Parallel Graphs*, Australasian Journal of
  Combinatorics 52 (2012), arXiv:1008.3660.

## 2. 独立精确搜索

实现：

- `transformation_search.py`

它没有导入 AMRA 的 production forest counter；只使用 nauty `geng`
生成非同构连通图，并用独立的规范分区 deletion--contraction DP 精确计数。

### 2.1 单位权直接变换

对全部 112 个六阶连通非同构简单图完成：

| 变换 | 标号配置数 | 变换后违例 |
|---|---:|---:|
| 复制一个原顶点为非邻接假孪生点 | 672 | 0 |
| 加一条叶边 | 672 | 0 |
| 保留边并加入一条平行二边路径 | 951 | 0 |
| 将一条边细分一次 | 951 | 0 |

此外直接检查：

| 操作 | 配置数 | 违例 |
|---|---:|---:|
| 阶数不超过 4 的连通因子 1-sum，输出阶数不超过 7 | 820 | 0 |
| 阶数不超过 4 的连通因子标准 graphic 2-sum，输出阶数不超过 6 | 806 | 0 |

这些计算是实现核对；数学结论应引用上一节的既有闭包定理。

### 2.2 单边活动度的整个正半轴

对每张基图、每个有序“活动边 \(e\)”和另两条测试边 \(a,b\)，固定其他边
权为 1。此时

\[
\Delta_G(a,b)=d_0+d_1y_e+d_2y_e^2.
\]

程序没有采样 \(y_e\)，而是用精确整数检查：

- \(d_0\ge0\)；
- \(d_2\ge0\)；
- 若 \(d_1<0<d_2\)，检查
  \(4d_0d_2-d_1^2\ge0\)。

完整范围：

| 阶数 | 连通非同构图 | 边三元组 | 在某个 \(y_e>0\) 失效 |
|---:|---:|---:|---:|
| 6 | 112 | 28,659 | 0 |
| 7 | 853 | 528,477 | 0 |
| 8 | 11,117 | 15,114,615 | 0 |
| **合计** | **12,082** | **15,671,751** | **0** |

这比检查有限个串/并联长度强，但仍然只允许一条边离开单位权；它不是完整
多变量 I-Rayleigh 证明。

## 3. 假孪生：当前唯一真正开放的变换

给定顶点 \(v\)，加入新顶点 \(v'\)，满足

\[
v'\not\sim v,\qquad N(v')=N(v).
\]

当 \(\deg v\le2\) 时它退化到桥或 series-parallel 操作。真正未被上述定理
处理的是 \(\deg v\ge3\)，它相当于沿至少三个边界点粘接，而不是 1-sum
或 2-sum。

### 3.1 单位权精确全边对

| 基图 | clone 选择 | 全部被检边对 | 最小整数裕量 | 违例 |
|---|---:|---:|---:|---:|
| \(K_4\) | 4 | 144 | 124 | 0 |
| \(K_5\) | 5 | 455 | 7,066 | 0 |
| <code>H?&#96;bM~^</code> | 9 | 2,337 | 204,120 | 0 |

九阶种子逐顶点 clone 后的最小裕量依次为：

```text
v=0:   468720
v=1:   763128
v=2:   204120
v=3:   204120
v=4:   468720
v=5:  2703456
v=6:  2703456
v=7: 15247040
v=8: 15247040
```

\(K_4\)、\(K_5\) 的结果其实已被 Wagner 的 \(K_6\) I-Rayleigh 结果及
minor 闭包严格涵盖：clone 后分别是 \(K_5-e\) 和 \(K_6-e\)。真正超出
已知小图 I-Rayleigh 覆盖的是九阶种子的十阶 clone。

### 3.2 随机独立正权全边对

每次给变换后图的每条边独立抽取

\[
\log_{10}y_e\sim\operatorname{Unif}[-s,s]
\]

并检查该图的全部边对。

| 基图 | \(s\) | 加权图评价数 | 边对评价数 | 数值违例 \(>10^{-10}\) |
|---|---:|---:|---:|---:|
| \(K_4\) | 8 | 400 | 14,400 | 0 |
| \(K_5\) | 8 | 1,000 | 91,000 | 0 |
| <code>H?&#96;bM~^</code> | 5 | 1,800 | 467,400 | 0 |
| <code>H?&#96;bM~^</code> | 2 | 450 | 116,850 | 0 |
| **合计** |  | **3,650** | **689,650** | **0** |

大动态范围样本中出现过约 \(2.84\times10^{-14}\) 的浮点正
`log-ratio`，均落在 double 舍入尺度内，不能当作反例。

### 3.3 最危险样本的精确复核

最危险记录来自：

- 基图：<code>H?&#96;bM~^</code>；
- clone 顶点：`0`，其邻域为 `{4,7,8}`；
- 变换后测试边：`(1,8)` 与 `(2,5)`；
- 随机命令参数：`seed=1760`、`log10-span=5`，顶点 0 的 trial 7。

把输出的每个十进制权重按其**精确有理数值**重新计算，得到

\[
\frac{\Delta(a,b)}{I^a I^b}
\approx 2.2181566798540307\times10^{-16}>0.
\]

精确 margin 的分子为正；这不是由 double round-off 误判的负值。
随后固定其他 21 个权重，对除测试边外的每个单独坐标重新写出精确二次式。
全部 20 个坐标二次式在整个 \(y_e>0\) 上非负，没有通过单坐标扰动穿过零点。

这个实例说明假孪生族确实可以极端逼近等号，值得继续做多坐标精确优化；
但当前没有反例或闭包证明。

## 4. 可复算命令

```bash
python3 \
  data/research_open/q1_eight_hour_campaign_2026-07-29/opg1757/\
agent_search/transformation_search.py self-test

python3 \
  data/research_open/q1_eight_hour_campaign_2026-07-29/opg1757/\
agent_search/transformation_search.py weighted --order 8

python3 \
  data/research_open/q1_eight_hour_campaign_2026-07-29/opg1757/\
agent_search/transformation_search.py random-weight-false-twin \
  --graph6 'H?`bM~^' --samples 200 --log10-span 5
```

## 5. 严格范围和下一步

1. 没有证明假孪生操作保持 I-Rayleigh。
2. 随机正权筛查不是证明；其结论仅限上述种子、clone 选择、随机种子和样本数。
3. 单边正半轴穷举固定其他权为 1，不能扩大成任意多变量正权。
4. series/parallel、1-sum、2-sum 应作为引用的基础工具，不应包装成新结果。
5. 最值得继续的方向是对假孪生 transfer 推导完整多变量 Rayleigh
   difference；若能给出正分解，就是一个真正的新闭包定理。反之，若多坐标
   优化把上述 \(2.2\times10^{-16}\) 裕量推成负值，则会得到加权
   I-Rayleigh 反例，并可通过串/并联权重编码转成原 uniform-forest 猜想的
   无权简单图反例。
