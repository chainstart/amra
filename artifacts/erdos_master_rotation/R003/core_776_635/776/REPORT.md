# Erdős #776：R003 带 cap 的 rank-8 低阶块与精确影损阈值

研究窗口：2026-07-23 21:03:58--21:47:02 HKT
本题实际 active agent time：1,512 秒（0.4200 agent-hours）
预算上限：14,400 秒；只登记实耗，不登记预算余额。

## 结论

**原题仍为 OPEN。本轮没有证明或证否 #776。**

本轮把 R002 的模糊“需要定量 shadow loss”严格压成了一个可复核的
rank-8 capped block：

1. 若 rank 8 进入一个显式二次 cap，则从 rank 8 到 rank 5 的全部
   canonical carry **与 cap 内残差无关**，严格得到
   \(E_5=F_5+8\)。因此一个单侧 rank-8 屏障便足以闭合原 colex 端点。
2. 相邻参数路线所需的两次影损有精确 Galois 门槛。第一门槛是
   \({V-5\choose2}+10\)，第二门槛是
   \({c+1\choose2}+8V-100\)。
3. 在整个 cap 内，第二门槛只有残差落在最顶部 **17 个整数**时才需要
   额外影损；所需下一层间隙至多 \(17V-476\)。这是真正的统一 capped
   shadow-loss 分类，不是参数扫描。
4. 但要让 rank-8 屏障本身在 \(V\mapsto V+1\) 下自保持，cap 顶端仍需
   \(L_8\ge V+1\)，其下一层精确门槛是二次量
   \({V-19\choose2}+20V-590\)。所以仅有 \(L_8\ge0\) 或“正间隙”
   不能传播完整 carry block。

这既推进了 closing lemma，也给出严格 no-go：低阶块已经解决，首个未补
节点现在是 rank-8 单侧屏障的全参数入口/自传播，而不是 rank 5 或 rank 6
尾端。

**闭合距离仍为 1。** 新屏障若被全称证明会立即闭合当前 colex 路线；本轮
尚未证明它对实际轨道的所有 \(V\) 成立。

## 1. 状态与继承接口

公开来源截至 2026-07-23 未改变：He--Tang 的 arXiv v2（2026-03-21
修订）给出

\[
n_0(2)=3,\qquad n_0(3)=8,
\]
\[
2r+2\le n_0(r)\le
2r+2\log_2r+O(\log_2\log_2r)\quad(r\ge4),
\]

但没有给出本仓库候选所需的精确全参数上界。

沿用 R002 的记号，令

\[
E_V=V-3,\qquad E_{q-1}=V+\operatorname{KK}_q(E_q),
\tag{1}
\]
\[
F_q={V+1\choose q}+{V-1\choose q-1}+{V-2\choose q-2},
\qquad h(V)=E_5-F_5 .
\tag{2}
\]

对 \(V\ge379\)，原 colex 端点严格等价于

\[
\boxed{h(V)\le70500.}
\tag{3}
\]

所以本报告中的 \(h\le8\) 屏障若能覆盖实际全轨道，就远强于 closing
threshold；但有限点进入屏障不能代替全称入口证明。

## 2. rank-8 capped descent

定义

\[
\begin{aligned}
H_8(V)={}&{V+1\choose8}+{V-1\choose7}+{V-3\choose6}\\
&+{V-5\choose5}+{V-7\choose4}+{V-9\choose3}.
\end{aligned}
\tag{4}
\]

### 引理 1

设 \(V\ge40\)，且

\[
E_8=H_8(V)+R,\qquad 0\le R<{V-18\choose2}.
\tag{5}
\]

置

\[
k=\operatorname{KK}_2(R),\qquad c=k+9.
\tag{6}
\]

则 \(c\le V-9\)，并且 (1) 的后三次转移严格为

\[
\begin{aligned}
E_7={}&{V+1\choose7}+{V-1\choose6}+{V-3\choose5}
{V-5\choose4}\\
&+{V-7\choose3}+{V-8\choose2}+{c\choose1},
\end{aligned}
\tag{7}
\]

\[
E_6={V+1\choose6}+{V-1\choose5}+{V-3\choose4}
{V-4\choose3}+{4\choose2},
\tag{8}
\]

\[
\boxed{E_5=F_5+8.}
\tag{9}
\]

### 证明

由 \(R<{V-18\choose2}\)，其 2-canonical 顶指标至多 \(V-19\)，故
\(k\le V-18\)。对 (5) 逐项取下影并加 \(V\)，尾部用 Pascal 合并为

\[
{V-9\choose2}+k+V
={V-8\choose2}+(k+9),
\]

且 \(k+9<V-8\)，所以 (7) 是合法 canonical 展开。

再取一次下影。式 (7) 的整个低尾满足

\[
{V-5\choose3}+{V-7\choose2}+(V-8)+1+V
={V-4\choose3}+6,
\]

给出 (8)，其中 \(c\) 已完全消失。最后

\[
{V-3\choose3}+{V-4\choose2}+4+V
={V-2\choose3}+8,
\]

得到 (9)。证毕。

### 单侧 closing barrier

令

\[
\overline E_8(V)=H_8(V)+{V-18\choose2}-1.
\tag{10}
\]

递推 (1) 单调，且引理 1 可用于 (10) 的最大残差。因此

\[
\boxed{E_8\le\overline E_8(V)\Longrightarrow E_5\le F_5+8.}
\tag{11}
\]

式 (11) 也覆盖 \(E_8<H_8\)：直接以 \(H_8\) 的后继作为单调上界即可。
所以全称证明 (11) 的左侧会立即给 (3)。当前未决核心已可写成唯一的
rank-8 单侧二次屏障，而不必再分类 rank 8 以下的 digits。

## 3. 两个精确 Galois 门槛

记

\[
S_q(x)=x+U_q(x).
\]

若 \(N\) 视作 rank \(r\) 数，Galois 伴随给出

\[
\operatorname{KK}_r(N)-\operatorname{KK}_r(N-\Delta)\ge\ell
\iff
\Delta\ge N-U_{r-1}\!\left(\operatorname{KK}_r(N)-\ell\right).
\tag{12}
\]

这是下面所有“最小间隙”结论的严格来源。

### rank 6 门槛

在 (8) 上令 \(N_6=S_6(E_6)\)。直接 canonical 化得

\[
\boxed{
\operatorname{KK}_7(N_6)-\operatorname{KK}_7(N_6-\Delta)\ge V+5
\iff
\Delta\ge{V-5\choose2}+10.}
\tag{13}
\]

等号前一整数严格失败，脚本对 synthetic boundaries 作了整数审计。

令相邻参数 diagonal gap 为

\[
G_q=S_{q-1}(E^{[V]}_{q-1})-E^{[V+1]}_q,
\]

并置

\[
P_q=U_{q-1}(E^{[V]}_{q-1})-E^{[V]}_q,\qquad
G_q=P_q-1+L_q.
\tag{14}
\]

在 (7)--(8) 上

\[
P_7={V-6\choose2}+V-4-c.
\tag{15}
\]

故要使 \(G_7\) 达到 (13)，严格等价于

\[
L_7\ge c+9.
\tag{16}
\]

### rank 7 门槛

对 \(N_7=S_7(E_7)\) 再用 (12)，得到

\[
\boxed{
L_7\ge c+9
\iff
G_8\ge {c+1\choose2}+8V-100.}
\tag{17}
\]

这里不是渐近展开。例如从
\(\operatorname{KK}_8(N_7)-(c+9)\) 借位后，合法尾部恰为

\[
{V-8\choose2}+{V-16\choose1},
\]

其上升量与 \(N_7\) 相减正好给 (17)。

## 4. cap 顶部只有 17 个危险残差

由 (7) 与 (5)

\[
P_8=U_7(E_7)-E_8
={V-9\choose2}+{c\choose2}-R.
\tag{18}
\]

把 (17) 代入 \(G_8=P_8-1+L_8\)，rank-6 路线所需的额外影损为

\[
\ell_8(R)=
\max\left(0,\,
R+\operatorname{KK}_2(R)-{V-17\choose2}+18\right).
\tag{19}
\]

令 \(T=V-18\)。在 \(0\le R<{T\choose2}\) 中，(19) 为正当且仅当

\[
R={T\choose2}-s,\qquad 1\le s\le17.
\tag{20}
\]

此时

\[
\operatorname{KK}_2(R)=T,\qquad
\ell_8=18-s.
\tag{21}
\]

因此整个二次 cap 里只有顶部 17 个整数需要 rank 8 以上的帮助；其余所有
残差仅靠 \(P_8-1\) 已经足够。

进一步对 \(N_8=S_8(E_8)\) 使用 (12)，使 \(L_8\ge18-s\) 所需的最小
\(G_9\) 恰为

\[
\boxed{
\Delta_9(s)=
{V-18-s\choose2}-{V-36\choose2}.}
\tag{22}
\]

故统一最坏值出现在 \(s=1\)：

\[
\boxed{\Delta_9(s)\le17V-476.}
\tag{23}
\]

式 (20)--(23) 是本轮要求的 capped shadow-loss uniform classification。
它把 R002 的未知定量损失从“可能依赖整个二次残差”压到 17 个显式边界
状态及一个线性门槛。

## 5. 为什么完整 carry block 仍未传播

为了让 (10) 本身从 \(V\) 传播到 \(V+1\)，需要把下一参数的 rank-8
残差压到

\[
R'<{V-17\choose2}.
\]

同样的代数给所需影损

\[
\ell_8^{\mathrm{bar}}(R)=
\max\left(0,\,
R+\operatorname{KK}_2(R)+V+2-{V-17\choose2}\right).
\tag{24}
\]

在合法 cap 顶端

\[
R={V-18\choose2}-1
\]

严格有

\[
\boxed{\ell_8^{\mathrm{bar}}=V+1.}
\tag{25}
\]

而 (12) 把 (25) 再推到 rank 9 后，最小 \(G_9\) 为

\[
\boxed{{V-19\choose2}+20V-590.}
\tag{26}
\]

因此“已有 \(L_8\ge0\)，所以 cap 自动自保持”是严格错误的；最坏合法
残差要求线性影损，并在下一 rank 变成二次间隙。这个 synthetic endpoint
只是证明路线的边界反例，不声称实际 defect 轨道命中 cap 顶端，也不是
原题反例。

这正是首个未修补断点：需要证明实际轨道永远远离 (24) 的危险尾端，或构造
一个跨 rank 的 coupled gap 势来支付 (26)。继续增加普通参数点不会解决
这个量词。

## 6. 有限回归与诚实边界

R002 run-compressed 引擎对以下选定点重算 rank 8；它们都进入 (10)，且
均处于 \(R\ge0\) 的精确 (9) 分支：

| \(V\) | \(R=E_8-H_8\) | 距 cap 的余量 |
|---:|---:|---:|
| 6,328 | 131 | 19,904,763 |
| 6,329 | 6,380 | 19,904,824 |
| 66,843 | 1,831,856,114 | 400,900,785 |
| 66,844 | 1,831,916,643 | 400,907,081 |
| 70,501 | 2,060,024,016 | 423,867,386 |
| 74,997 | 2,358,718,056 | 452,169,674 |
| 200,000 | 18,761,110,515 | 1,235,189,655 |

这些点验证公式和旧边界，但不证明 (10) 对任意 \(V\)。特别地，表中余量
很大不能排除更后面的 carry block 靠近 cap。

## 7. 原题回译与下一步

本轮没有证明全称 rank-8 屏障，故不能宣布
\(n_0(r)\le2r+5\)，也没有改变公开状态。

下一项最小可判定动作是二选一：

1. 对实际 diagonal orbit 证明：当 residual 落入 (20) 的 17 个状态时，
   \(G_9\) 自动满足 (22)；这会完成当前 rank-6 参数传播；
2. 为 (10) 构造跨 rank 的 coupled potential，支付最坏的 (26)，或证明
   实际 residual 与 cap 顶端有统一线性距离。

## 8. 复核

```bash
taskset -c 6 nice -n 10 \
  python3 verify_rank8_capped_block.py
```

应输出 `"status": "PASS"`。完整运行约 35 秒、峰值内存约 16 MB；
其中大参数值只作有限回归，严格全参数内容是上面的 canonical/Galois
恒等式。
