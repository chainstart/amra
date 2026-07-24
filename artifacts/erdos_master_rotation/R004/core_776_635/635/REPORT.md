# Erdős #635：共享路径梯度 no-go、精确双环分支排除与全素数平行环参数族

研究窗口：2026-07-24 09:54:13--11:04:19 HKT
研究冻结：2026-07-24 11:04:19 HKT；此后只作回归、排版、清单与哈希。

## 结论

**原题的精确极值部分仍为 OPEN。本轮没有证明或证否 #635，
`Q2=false`。**

本轮完成了 R003 指定的两项动作，并得到如下严格结果。

1. R003 的 first-moment 与 Euler-product 路线在共享端点路径上完全坍缩：
   两者分别是端点函数 \(v-u\) 与 \(v/u\) 的精确梯度。两条共享端点路径
   相减只能恒等地给 \(0\) 与 \(1\)，不能强迫 compatible majorization
   或素性。这条指定路线已被严格判死。
2. 对 all-prime semiprime swap graph，枚举每个奇顶点
   \(b\le2,000,000\) 的**全部** incident edges，并从每个度至少 3 的顶点
   完整展开其整个连通分量。共检查 20,516 个 branch seeds、18,539 个
   不同闭分量；只有 3 个单环分量，没有双环。故任何双环核的所有无向
   branch vertices 都大于 2,000,000。
3. 将边朝较大顶点定向又给一个独立势。对 3,731 个 upward-branch seeds
   完整闭包，得到 3,651 个分量、6 个单环、0 个双环。因此任何双环分量的
   upward-branch vertices 也都大于 2,000,000。
4. 发现并证明一个 mixed-valuation 全素数平行环参数族。有限参数域中完整
   检查 50,822 个因子对，得到 41 个无标签冲突的全素数平行单环，其中
   2 个来自此前未见的非最大平移分支；没有两环共享端点。对其中 12 个较小
   环再作无 label cutoff 的整分量展开，它们全都仍为单环。

这些结果没有证明无限 swap graph 是 pseudoforest。即使 semiprime
proper-neighbour Hall 被完整证明，原题仍需 prime-square、高阶奇部和
matching union 的处理，所以闭合距离仍为 2。

## 1. 图模型与精确 incident inversion

对

\[
x=Apq,\qquad A=2^a,\quad p\ne q\text{ 为奇素数},
\]

semiprime swap edge 的两个奇顶点是

\[
x-p=p(Aq-1),\qquad x-q=q(Ap-1).
\]

反过来，给定奇顶点 \(b\)，若某条 incident edge 在 \(b\) 删除奇素数
\(d\mid b\)，则

\[
\frac bd+1=Aq.
\]

所以 \(A\) 必为 \(b/d+1\) 的精确 2-adic part，\(q\) 是其 odd part。
对 \(b\) 的每个不同奇素因子 \(d\) 检查一次即可得到**全部** incident
edges，不需 prime、label 或 neighbour cutoff。

这正是 `search_bicyclic_components.py` 的完备性基础。对闭包途中超过
2,000,000 的顶点也作完整整数分解；实际最大到达 2,481,129，安全上限
100,000 个顶点从未触发。

## 2. 共享路径不变量其实是端点梯度

把一条 edge 从

\[
u=x-p
\quad\text{定向到}\quad
v=x-q.
\]

则立即有

\[
\boxed{p-q=v-u.}
\]

再令

\[
f_A(t)=1-\frac1{At}.
\]

直接约分：

\[
\frac{f_A(p)}{f_A(q)}
=\frac{q(Ap-1)}{p(Aq-1)}
=\frac vu.
\]

因此对任意定向 \(u\)-到-\(v\) 路径，不论 valuation 是否混合，

\[
\boxed{\sum_{\text{edges}}(p-q)=v-u,}
\]
\[
\boxed{\prod_{\text{edges}}\frac{f_A(p)}{f_A(q)}=\frac vu.}
\]

两条共享端点路径相减/相除只会得到

\[
0,\qquad1.
\]

所以 R003 的 cycle first moment 与 Euler product 都是正确恒等式，但
它们没有额外的 path coupling 内容。严格凹性/majorization 在单圈上给出
的 crossing 必要条件不能经“共享路径相减”自动变成相容方向。

两个原有 mixed-valuation 平行环

\[
(273,275),\qquad(5293,5355)
\]

逐边精确验证了同一端点梯度；它们没有 label conflict，故也直接说明
“梯度恒等式 + 素性”并不排除真单环。

## 3. 200 万无向 branch-vertex 完整排除

任意有限连通双环核的 cyclomatic number

\[
\mu=|E|-|V|+1
\]

至少为 2。删叶后其平均度大于 2，故必有无向度至少 3 的 branch vertex。

程序检查所有奇数 \(b\le2,000,000\)，由第 1 节公式精确求 full degree；
随后从每个 full degree 至少 3 的 seed 完整 BFS 到分量闭合。结果：

| 项目 | 精确值 |
|---|---:|
| branch seeds | 20,516 |
| 不同闭分量 | 18,539 |
| 观察到的最大 full degree | 5 |
| 最大分量顶点数 | 22 |
| 最大分量边数 | 21 |
| 闭包最大到达顶点 | 2,481,129 |
| \(\mu=0\) 分量 | 18,536 |
| \(\mu=1\) 分量 | 3 |
| \(\mu\ge2\) 分量 | 0 |

三个被 branch seed 命中的单环分别以 273、5,355、29,165 为首 seed。
前两个是无冲突平行环；第三个是六边 mixed cycle，含三个 label conflicts。

严格推出：

\[
\boxed{\text{任意 all-prime swap-graph 双环核的所有无向 branch
vertices 都大于 }2,000,000.}
\]

这是 finite branch-vertex exclusion，不是无界 pseudoforest 定理。

## 4. 上行势与第二个完整排除

把每条 edge 朝数值更大的顶点定向，记 \(d_+(v)\) 为上行边数，\(s\) 为
分量内 \(d_+(v)=0\) 的顶点数。每条边恰在较小端贡献一次，故

\[
|E|=\sum_v d_+(v).
\]

于是对任意有限连通分量，

\[
\boxed{
\mu
=1-s+\sum_{d_+(v)\ge2}(d_+(v)-1).}
\]

若 \(\mu\ge2\)，上行 branching excess 至少为 \(s+1\)，特别是分量必含
\(d_+\ge2\) 的顶点。

对所有 \(b\le2,000,000\) 的 3,731 个 upward-branch seeds 作同样完整
闭包，得到：

| 项目 | 精确值 |
|---|---:|
| 不同闭分量 | 3,651 |
| 观察到的最大 \(d_+\) | 2 |
| \(\mu=0\) 分量 | 3,645 |
| \(\mu=1\) 分量 | 6 |
| \(\mu\ge2\) 分量 | 0 |
| 闭包最大到达顶点 | 2,362,359 |

六个首 seeds 为

\[
253,\ 4979,\ 24485,\ 29149,\ 39783,\ 1244919.
\]

它们对应 5 个无冲突平行单环及一个有冲突六边单环。由势恒等式严格推出：

\[
\boxed{\text{任意双环分量的所有 upward-branch vertices
也都大于 }2,000,000.}
\]

## 5. 全素数无冲突平行环参数族

下面给出本轮新发现的代数构造。取 2 的幂 \(B,c\)（\(c\ge4\)），取

\[
k\mid c-1,\qquad h=\frac{c-1}{k},\qquad t=kB.
\]

若奇素数 \(p,q,p+t,q+t\) 满足

\[
\boxed{(hp-B)(hq-B)=cB^2-h,}
\]

则尺度 \(cB\)、素数对 \((p,q)\) 的 edge 与尺度 \(B\)、素数对
\((p+t,q+t)\) 的 edge 有相同端点。

确实，展开因子式得到

\[
h\,pq-B(p+q)=kB^2-1.
\]

乘以 \(k\) 并用 \(kh=c-1\)，可得两个 labels 的差恰为

\[
B(p+t)(q+t)-cBpq=t.
\]

而两个 prime pairs 也同时平移 \(t\)，所以从 label 中分别减去两素数后
端点逐一相同。

两 labels 冲突当且仅当

\[
t\mid cBpq.
\]

因 \(k\mid c-1\) 且 \(c\) 为 2 的幂，

\[
\boxed{\text{label conflict}\iff k\mid pq.}
\]

所以 \(k\nmid pq\) 给真正无冲突平行单环。

前五个较小控制为：

| \(B,c,k,h\) | \((p,q)\) | 平移后 | 端点 |
|---|---|---|---|
| \(2,4,3,1\) | \(5,7\) | \(11,13\) | \(273,275\) |
| \(4,4,3,1\) | \(5,67\) | \(17,79\) | \(5293,5355\) |
| \(8,4,3,1\) | \(13,59\) | \(37,83\) | \(24485,24531\) |
| \(4,16,15,1\) | \(7,89\) | \(67,149\) | \(39783,39865\) |
| \(32,4,3,1\) | \(71,137\) | \(167,233\) | \(1244919,1244985\) |

本轮还找到两个 \(h>1\) 控制：

\[
(B,c,k,h,p,q)=(4,4096,455,9,3,317),
\]

\[
(8192,64,9,7,2053,100469).
\]

它们也全部通过 primality、共同端点和无 label conflict 的精确整数审计。

这个参数族说明“素性会排除 mixed-valuation crossing cycles”的路线是错的。
Hall 障碍所需的是两个独立圈，而不是单圈。

## 6. 参数族中的主动双环搜索

在

\[
B=2^b,\quad1\le b\le30,
\qquad
c=2^j,\quad2\le j\le15
\]

中，对每个 \(k\mid c-1\) 完整枚举

\[
cB^2-h
\]

的因子对，并检查整除、四个素数和 label conflict。共计：

| 项目 | 精确值 |
|---|---:|
| \((B,c)\) 参数对 | 420 |
| 因子对 | 50,822 |
| PARI 证明为素数的分解基元 | 2,356 |
| PARI 证明为素数的不同环素数 | 159 |
| 全素数无冲突平行环 | 41 |
| \(h>1\) 环 | 2 |
| 共享端点的两环 | 0 |

所以这个有界参数族中没有 figure-eight 双环。进一步对其中 12 个较小环的
整个真实 swap-graph 连通分量作 exact incident inversion，无 label cutoff；
每个分量都满足 \(\mu=1\)。

实现中 `sympy.isprime` 只作快速筛选；所有因子分解的基元和最终 159 个
不同候选素数又统一送入 PARI/GP 的 `isprime` 作证明性复核。因此这里没有
把大于 \(2^{64}\) 的 BPSW probable-prime 当成严格素数证据。

这些是有界、可复核的主动反例搜索，不限制一般 theta/dumbbell、参数域外
平行环或经过族外路径相连的两个环。

## 7. 首断点与原题距离

本轮严格判死的路线是：

> 对 theta 的两条共享路径相减 first moment / Euler product，然后用
> majorization 强迫矛盾。

相减后只剩端点梯度恒等式，没有新约束。

当前最小未补节点是二选一：

1. 证明 all-prime swap graph 的每个连通分量 cyclomatic number 至多 1，
   需要使用梯度之外的素性/label-conflict 势；或
2. 构造第一个无 label conflict 的 all-prime bicyclic core。

即使完成该 semiprime 节点，原题仍有 prime-square、高阶 odd part 与全局
matching 合并，因此本报告不声称接近原题完整闭合。

## 8. 复核

```bash
python3 verify_shared_path_gradient.py
python3 verify_parallel_cycle_family.py
taskset -c 6 nice -n 10 python3 search_parallel_cycle_family.py
python3 verify_targeted_cycle_components.py
taskset -c 6 nice -n 10 \
  python3 search_bicyclic_components.py --limit 2000000
```

五项都应输出 `"status": "PASS"`。
