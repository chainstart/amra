# Erdős #18 — R002准入研究

日期：2026-07-23

终态：`FINITE_STRUCTURE_CONFIRMED__NO_ASYMPTOTIC_BRIDGE__DO_NOT_PROMOTE`

## 状态和目标

官网仍把三个问题全部列为开放：

1. 是否有无穷多个 practical 数满足
   \(h(m)<(\log\log m)^{O(1)}\)；
2. 是否 \(h(n!)<n^{o(1)}\)；
3. 是否甚至 \(h(n!)<(\log n)^{O(1)}\)。

Vose的结果只给出无穷多个 practical \(m\) 满足
\(h(m)\ll\sqrt{\log m}\)，不等于任何一个目标。

## 已核验的严格边界

若 \(t=\tau(m)\)、\(k=h(m)\)，所有至多 \(k\) 个互异因子之和必须覆盖
\([0,m)\)，所以

\[
m\leq\sum_{j=0}^{k}\binom tj.
\]

结合 \(\tau(n!)\) 的已知渐近式，只给出
\(h(n!)=\Omega((\log n)^2)\)。这说明polylog上界若成立，其指数不能低于2，
但完全不给上界。

递推

\[
h((n+1)!)\leq h(n!)+1
\]

是严格的：把 \(r=(n+1)q+s\)，先表示 \(q\)，把所用因子乘以 \(n+1\)，
再在 \(s>0\) 时加入因子 \(s\)。它只能恢复线性上界。

## 独立有限复算

`verify_18_small_factorials.py`用整数bitset对所有互异因子子集和做精确动态规划：

| \(n\) | \(\tau(n!)\) | \(h(n!)\) |
|---:|---:|---:|
| 3 | 4 | 2 |
| 4 | 8 | 3 |
| 5 | 16 | 4 |
| 6 | 30 | 5 |
| 7 | 60 | 5 |
| 8 | 96 | 6 |
| 9 | 160 | 7 |
| 10 | 270 | 7 |

这些数据核对了逐级递推，但不能支持任何渐近猜测。

## 准入结论

原拟议的块递推需要对
\((n+1)\cdots(n+L)\) 以下的每个余数给出只用
\(O(L/\log L)\) 个新因子的统一表示。当前没有得到这种“整块短表示”；
普通混合进位仍需 \(O(L)\) 项，Vose的Egyptian-fraction算法也不保证分母
都整除 \(n!\)。

因此闭合距离由3调整为4，不进入4小时深攻。只有出现以下任一输入才重新准入：

- 可控制分母都整除阶乘的短Egyptian-fraction定理；
- practical数因子子集和的统一覆盖/加法基结构；
- 真正节省一整个数量级的块递推。

## 来源

- https://www.erdosproblems.com/18
- https://doi.org/10.1112/blms/17.1.21
- https://math.dartmouth.edu/~carlp/factorial.pdf
