# OPG-1757 高风险三星扩张证书

日期：2026-07-29

## 精确结论

固定九顶点基图 <code>H?&#96;bM~^</code>、继承边索引对 `(0,2)`，其端点
分别为 \(\{0,4\}\) 和 \(\{2,5\}\)。加入以下互不相邻的新顶点：

1. 邻域为 \(R=\{0,4\}\)（mask 17）的一颗星；
2. 邻域为 \(Q=\{2,5\}\)（mask 36）的一颗星；
3. 邻域为九个基点任意子集 \(P\) 的第三颗星；
4. 任意 \(t\geq0\) 个邻域均为
   \(S=\{1,5,6,7,8\}\) 的重复假孪生星。

对全部 \(2^9=512\) 个 \(P\)，所选继承边对的负相关裕量

\[
M_P(t)=N_e(t)N_f(t)-N(t)N_{ef}(t)
\]

对每个整数 \(t\geq0\) 都严格为正。证书逐项得到

\[
M_P(t)=36^t A_P(t)/d_P,
\]

其中每个 \(d_P>0\)，而 512 个普通幂基多项式 \(A_P\) 的每个系数都严格
为正。所有多项式中的最小系数为 75；次数分布为：

| 次数 | 第三星邻域数 |
| ---: | ---: |
| 5 | 120 |
| 6 | 200 |
| 8 | 192 |

这是一项针对固定继承边对和固定前两颗星的无限参数子类结论，不是任意三星
邻域的完整扫描，也没有检查所得每张图中的其他边对。

## 为什么覆盖全部 \(t\)

计算在九个基点的连通分区上保存四个独立 forced-edge channel。加入前两颗星
后，重复星的忘却转移记为 \(T_S\)。其中选择零条或一条星边的 6 种选择都
保持原分区，故

\[
T_S=6I+N_S.
\]

\(N_S\) 的每个非零转移都至少合并两个被 \(S\) 占据的不同 block。这样的
block 最多有 5 个，所以 \(N_S^5=0\)，即

\[
(T_S-6I)^5=0.
\]

程序还在具体的前两星后分布上，对 3,430 个分区和 4 个 channel 的
13,720 个坐标逐个验证

\[
v_5-30v_4+360v_3-2160v_2+6480v_1-7776v_0=0.
\]

非零残差坐标为 0，残差行 SHA-256 为
`cbfae6618136de5177321c1f81fe35511efb96bed7b6c7190a8cf45d5e25d951`。
因此四个计数都是 \(6^t\) 乘至多四次多项式。闭式只由
\(t=0,\ldots,4\) 求出，而直接计算的 \(t=5\) 在 512 个邻域、四个计数
channel 上全部吻合。

第三颗星作为终端线性泛函处理：若当前基点分区为 \(\pi\)，其合法选边数
恰为

\[
\prod_{C\in\pi}(1+|C\cap P|).
\]

所有新增星之间没有边，星转移可由收缩后的二部森林双射交换。因此证书也覆盖
前两颗星、第三颗星和重复 \(S\)-星的任意加入顺序。

## 最接近等号的样本

在 \(t=10000\) 时，512 个第三星邻域中最接近等号的是再次取
\(P=\{0,4\}\)（mask 17）。精确相对缺口为

\[
\frac{
58\,973\,291\,740\,712\,117\,565
}{
6\,165\,090\,137\,070\,004\,901\,623\,247\,886\,941\,089
}>0.
\]

这说明连续增加与继承边 \(e\) 端点相连的长度二路径仍会逼近等号，但在本
证书覆盖的整个参数族中不会穿过等号。

## 可复现材料

- 实现：
  `src/amra/discovery/opg_uniform_forest_three_star_closure.py`
- 实现 SHA-256：
  `1dcf4274f3ebe6d15339c9004a19eb22920ae4c73fea049108fe23ac59ab37c4`
- 测试：
  `tests/test_opg_uniform_forest_three_star_closure.py`
- 测试 SHA-256：
  `d91924d26aba9597ca140f69aa127aadc773516fd49e463d17013db6e010e7eb`
- JSON 证书：
  `artifacts/opg_breakthrough/certified/opg1757-three-star-high-risk/certificate.json`
- 证书 SHA-256：
  `af14ce358457908226eb7c02c5636d82cbd874c335e4a663739adb04bf6b40d3`

专项测试结果为 `7 passed`。证书从磁盘重新载入后又执行了一次完整重算并
逐字节比对，状态为 `verified`。

复算命令：

```bash
PYTHONPATH=src python3 -m \
  amra.discovery.opg_uniform_forest_three_star_closure verify \
  artifacts/opg_breakthrough/certified/\
opg1757-three-star-high-risk/certificate.json

PYTHONPATH=src pytest -q \
  tests/test_opg_uniform_forest_three_star_closure.py
```
