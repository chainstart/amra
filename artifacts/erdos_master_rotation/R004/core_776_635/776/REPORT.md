# Erdős #776：五项 rank-8 屏障、top-17 真实耦合与新的单项入口断点

研究窗口：2026-07-24 09:54:13--11:04:19 HKT
研究冻结：2026-07-24 11:04:19 HKT；此后只作回归、排版、清单与哈希。

## 结论

**原题仍为 OPEN。本轮没有证明或证否 #776，`Q2=false`。**

本轮有三项严格进展。

1. R003 cap 顶部的 17 个危险残差不再是 17 个独立分支。它们所需的
   真实 \(G_9\) 条件全部严格等价于同一个下一参数条件
   \[
   R'(V+1)\le {V-16\choose2}.
   \]
   这完成了 top-17 的精确耦合分类，但尚未证明实际轨道总满足该条件。
2. 旧六项基线的 cap 可明显放宽。保留前五项并把第六项整体作为 reservoir，
   得到单侧屏障
   \[
   E_8\le H_8^{(5)}(V)+{V-8\choose3}-1
   =H_8(V)+{V-9\choose2}-1.
   \]
   其最大端点严格下降到 \(E_5=F_5+10\)，所以一旦全称进入该屏障，
   仍会立即闭合 inherited endpoint。
3. 在 first-carry \(I_8\) 块上，五项屏障的长 reservoir 条件经尾补对偶
   和一个新的固定深度引理，压成单个 rank-8 入口：
   \[
   \boxed{D_8<{V-11\choose8}}.
   \]
   本轮已证明对所有 \(V\ge40\)，该入口严格推出最终所需的
   \(D_2\le{V-9\choose2}\)。因此首个未补节点现在确实是 shortened
   zero-seed orbit 的 rank-8 入口，而不是 rank 8 以下的 carry。

闭合距离仍记为 1：新入口若能全称证明，会闭合当前 colex 路线；有限轨道
值不能替代这个量词。

## 1. 继承记号与闭合接口

沿用 R002--R003：

\[
E_V=V-3,\qquad E_{q-1}=V+\operatorname{KK}_q(E_q),
\]
\[
F_q={V+1\choose q}+{V-1\choose q-1}+{V-2\choose q-2}.
\]

对 \(V\ge379\)，原 colex endpoint 已严格归约为

\[
E_5-F_5\le70500.
\]

写

\[
\begin{aligned}
H_8(V)={}&{V+1\choose8}+{V-1\choose7}+{V-3\choose6}\\
&+{V-5\choose5}+{V-7\choose4}+{V-9\choose3},
\end{aligned}
\]

并令 \(H_8^{(5)}\) 是上式前五项。记

\[
S_q(x)=x+U_q(x).
\]

## 2. top-17 的真实 \(G_9\) 条件坍缩为一个条件

取 R003 的危险状态

\[
R={V-18\choose2}-s,\qquad1\le s\le17,
\]

以及其最小所需间隙

\[
\Delta_s={V-18-s\choose2}-{V-36\choose2}.
\]

定义下一参数相对六项调和基线的 rank-9 residual

\[
Q'=E^{[V+1]}_9-H_9(V+1).
\]

由于 \(S_8(H_8(V))=H_9(V+1)\)，真实 diagonal gap 恰为

\[
G_9=S_2(R)-Q'.
\]

直接用 Pascal 恒等式和 2-canonical 展开得到

\[
\boxed{
S_2(R)-\Delta_s
=U_2\!\left({V-17\choose2}-18\right).}
\]

右端与 \(s\) 完全无关。因此

\[
G_9\ge\Delta_s
\iff
Q'\le U_2\!\left({V-17\choose2}-18\right).
\]

若下一 rank-8 residual 写成

\[
R'(V+1)=V+1+\operatorname{KK}_3(Q'),
\]

Galois 伴随再给

\[
\boxed{
G_9\ge\Delta_s
\iff
R'(V+1)\le{V-16\choose2}.}
\]

这说明 R003 的 17 个需求只是一个 relaxed next-residual cap 的 17 种
写法。它不是自发成立的定理：当前仍缺实际相邻参数轨道对这个 cap 的控制。
对 synthetic top states 作最大反向延拓会精确回到 seed，故“这些状态没有
前像”的朴素排除路线也不成立。

## 3. 更宽的五项 rank-8 屏障

定义

\[
\overline E^{(5)}_8(V)
=H_8^{(5)}(V)+{V-8\choose3}-1.
\]

Pascal 恒等式给

\[
\overline E^{(5)}_8(V)
=H_8(V)+{V-9\choose2}-1,
\]

且其合法 8-canonical 展开为

\[
\begin{aligned}
&{V+1\choose8}+{V-1\choose7}+{V-3\choose6}
 +{V-5\choose5}+{V-7\choose4}\\
&\qquad+{V-9\choose3}+{V-10\choose2}+{V-11\choose1}.
\end{aligned}
\]

对 \(V\ge15\) 逐项取下影并每次加 \(V\)，严格得到

\[
\begin{aligned}
E_7={}&{V+1\choose7}+{V-1\choose6}+{V-3\choose5}
 +{V-5\choose4}+{V-6\choose3}
 +{4\choose2}+{2\choose1},\\
E_6={}&{V+1\choose6}+{V-1\choose5}+{V-3\choose4}
 +{V-4\choose3}+{5\choose2}+{1\choose1},\\
E_5={}&{V+1\choose5}+{V-1\choose4}+{V-2\choose3}
 +{5\choose2}.
\end{aligned}
\]

所以

\[
\boxed{E_5=F_5+10.}
\]

由单调性，所有 \(E_8\le\overline E^{(5)}_8(V)\) 都满足
\(E_5\le F_5+10\)，远低于 70500。相较 R003 的
\({V-18\choose2}\) residual cap，新 cap 是 \({V-9\choose2}\)，
并把完整第六调和项作为可消耗 reservoir。

## 4. first-carry 块的尾补对偶

Round12 在 \(I_8\) 上的精确正规形给出五项基线之外的最坏 residual

\[
R_3={V-9\choose3}
\]

（实际还有 \(y\ge0\)，故最坏情形取 \(y=0\)）。其 forward 递推是

\[
R_{\ell+1}=U_\ell(R_\ell)-V.
\]

要使 reservoir 非负走到所需终点，Galois 反推可写成

\[
Z_{V-11}=0,\qquad
Z_\ell=\operatorname{KK}_{\ell+1}(V+Z_{\ell+1}),
\]

并只需

\[
Z_3\le{V-9\choose3}.
\]

更有用的形式来自尾补。置 \(n=V-9\)，并定义

\[
D_{n-\ell}={n\choose\ell}-R_\ell.
\]

尾补恒等式把长 forward 递推严格变为

\[
\boxed{
D_{V-12}=0,\qquad
D_{q-1}=V+\operatorname{KK}_q(D_q)
\quad(q=V-12,\ldots,3),}
\]

而目标恰为

\[
\boxed{D_2\le{V-9\choose2}.}
\]

这不是数值近似，而是逐层 Galois/尾补等价。

## 5. rank-8 以下已完全闭合

### 引理

对所有 \(V\ge40\)，若上述 shortened defect orbit 满足

\[
D_8<{V-11\choose8},
\]

则

\[
D_2\le{V-9\choose2}.
\]

### 证明

由单调性只需取最大值

\[
D_8={m\choose8}-1,\qquad m=V-11.
\]

有精确恒等式

\[
\operatorname{KK}_8\!\left({m\choose8}-1\right)={m\choose7}.
\]

大项随后调和下降，所有税收集中到固定深度 residual：

\[
w_6=V,\qquad
w_{r-1}=V+\operatorname{KK}_r(w_r)
\quad(r=6,5,4,3).
\]

在 canonical 前缀保持分离时，

\[
D_2={m\choose2}+V+\operatorname{KK}_2(w_2).
\]

因此目标等价于

\[
\operatorname{KK}_2(w_2)\le V-21. \tag{1}
\]

对任意 rank \(r\)，canonical 每项满足

\[
{a\choose i-1}\le i{a\choose i}\le r{a\choose i},
\]

故

\[
\operatorname{KK}_r(x)\le rx.
\]

于是

\[
w_5\le7V,\quad w_4\le36V,\quad
w_3\le145V,\quad w_2\le436V.
\]

rank 2 展开又给

\[
\operatorname{KK}_2(x)\le\sqrt{2x}+2,
\]

所以对 \(V\ge1000\)，

\[
\operatorname{KK}_2(w_2)
\le\sqrt{872V}+2\le V-21.
\]

同一组粗界也保证所有 residual 顶指标低于前缀 \(m\)，没有暗中 carry。
区间 \(40\le V\le999\) 的 960 个整数由脚本用精确 canonical 算术逐点
核对；最小终点余量为 4，在 \(V=40\) 首次取得。故引理对全部
\(V\ge40\) 成立。证毕。

这项引理把长条件的首个未知点提升到唯一的 rank-8 入口；rank 8 以下不再
需要任何猜测性势。

## 6. 新的首断点与有限 falsifier

精确有限轨道在所有选定点都有

\[
D_8={V-12\choose8}+{V-13\choose7}+W_6,
\]

且

\[
{V-11\choose8}-D_8
={V-13\choose6}-W_6>0.
\]

例如：

| \(V\) | rank-8 cap margin |
|---:|---:|
| 40 | 260,272 |
| 100 | 504,971,605 |
| 379 | 3,203,798,788,714 |
| 1,000 | 1,264,613,768,009,912 |
| 100,000 | 1,387,597,721,425,102,127,105,602,470 |

这些值只作 falsifier/regression 证据。当前真正需要证明的是

\[
\boxed{W_6<{V-13\choose6}\quad\text{对所有 }V,}
\]

等价地证明 shortened zero-seed orbit 的
\(D_8<{V-11\choose8}\)。本轮没有得到这个全称入口或相邻参数自传播势，
所以不能宣布原题闭合。

## 7. 复核

```bash
taskset -c 6 nice -n 10 \
  python3 verify_rank8_five_term_barrier.py
```

应输出 `"status": "PASS"`。脚本中的五项下降、top-17 恒等式和固定深度
引理使用精确整数；战略大参数值明确只作有限 falsifier。
