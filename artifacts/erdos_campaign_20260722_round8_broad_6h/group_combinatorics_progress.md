# 第八轮组合/加法工作流终报

日期：2026-07-22（Asia/Hong_Kong）

统一计时：2026-07-22 08:52:14 至 10:22:14（5,400 秒）。

## 总判定

四题均先完成旧路线的逻辑、量词和来源适用性审计，再尝试了不同于第七轮主线
的新方向。没有原题闭合，也没有结果达到本轮 Q2 提前停止门槛；工作流按要求
用满 5,400 秒。本轮新发现的唯一未登记旧文档硬错误是 #788 把 Sanders 的
改进定理编号
写成 Theorem 1.3，正确编号是 Theorem 1.5；所用 \(1/3\) 指数本身正确，
所以不推翻该分支。#256 第三轮的尺度退化此前已在第四轮修复并登记，不是
本轮新发现。其余受检失败均是已证明的方法屏障或尚缺逆定理，不是已有
发表证明失效。

| 题号 | 登记秒数 | 审计分类 | 本轮最强推进 | 仍缺什么 |
|---:|---:|---|---|---|
| 25 | 1,350 | 旧链无致命错误；a.e./every 量词为真实屏障 | Haar-a.e. 相容共同平移有自然密度 \(d_*\)；给出 every-shift 边界零定理、精确 shrinking-target 激活式及最大异常整数轨道 | 控制正测度边界上指定异常轨道与激活 fringe 的耦合 |
| 256 | 1,350 | 旧尺度错误已在第四轮修复；正自相关核为真实屏障 | residue-chain 证书覆盖重数；偶性能量及 Newton 矩刚性使每链界达到 \(2\lceil(m_q+1)/2\rceil+2\mathbf1_{m_q\ge3}\) | 证明总有一个约数方向给超线性证书，或分类全部同时压缩的 quotient |
| 539 | 1,350 | Fish--Lund--Sheffer 的任意子集量词核实成立；旧悬挂账本无误 | 对高维单纯形薄层给精确 \(|D|\) 公式及全参数统一屏障 \(|D|\ge\tfrac32|F|^{2/3}\) | 构造同时避开 suspension、Boolean doubling 和坐标边界项的族 |
| 788 | 1,350 | 数学适用性成立；Sanders 定理编号有书目错误 | 任意母集的精确 matching 交公式；闭合高于半密度的 2-proper GAP 子类，并允许满足熵条件的缓慢增长秩 | 把一般临界 \(3s\) 候选稳定嵌入体积 \(<(2-\varepsilon)s\) 的 2-proper GAP，或另造低熵证书 |
| **合计** | **5,400** | **NO_Q2** |  |  |

## #25：profinite survivor 的轨道判据

令 \(B_K\) 为前 \(K\) 个完整 cylinder 的幸存集，
\(B_\infty=\bigcap_KB_K\)，\(d_K=\mu(B_K)\downarrow d_*\)。对相容共同平移
\(z\)，激活集合满足（第二式只在有限截断之后）

\[
 (z+B_\infty)\cap\mathbb N\subseteq A_z,
 \qquad A_z\cap[n_K,\infty)\subseteq z+B_K.
\]

因此只要 \(B_\infty\) 沿 \(-z\) 的 \(+1\) 轨道平均等于 Haar 测度，就有
\(d(A_z)=d_*\)。Birkhoff 给 Haar-a.e. \(z\)；边界零时唯一遍历与内外
clopen 夹逼给每个 \(z\)。

更精确地，若 \(k(m)=\max\{i:n_i\le m\}\)，则
\(1_{A_z}(m)=1_{B_{k(m)}}(m-z)\)，激活补偿恰为 shrinking target
\(B_{k(m)}\setminus B_\infty\)。它的 Haar 平均有限区间密度是
\(X^{-1}\sum_{m\le X}(d_{k(m)}-d_*)\to0\)，但指定异常轨道上不能据此逐点
删掉；这就是 every-system 尚缺的耦合接口。

异常点不可直接删去：枚举全部正整数 \(b_i\)，取严格递增且
\(\sum1/n_i<\varepsilon\)、\(n_i>b_i\) 的模数，并删除
\(b_i\pmod{n_i}\)。所得 \(B_\infty\) 测度 \(>1-\varepsilon\)，却不含任何
正整数，且边界就是自身。这个构造不反驳原题，因为相应命中在 \(b_i\) 处尚未
激活（原条件中的 \(b_i<n_i\) 为真）；只有 \(b_i+kn_i\)、\(k\ge1\) 才被
该类删除。它没有证明实际 \(A\) 振荡，只精确隔离了尚需使用的算术信息。

## #256：重数敏感的 residue-chain 证书

写

\[
 P(z)=\prod_i(1-z^{a_i})=(1-z^q)^{m_q}Q_q(z).
\]

按模 \(q\) 分 fiber 后，每条活跃链是
\((1-u)^{m_q}Q_{q,r}(u)\)。特征 0 中，一个在 1 有 \(m_q\) 重零的非零
多项式至少有 \(m_q+1\) 个非零单项式；否则前 \(t\) 个消失矩组成可逆
Vandermonde 系统。整数系数平方能量遂给

\[
 \eta_m:=2\left\lceil\frac{m+1}{2}\right\rceil+2\mathbf1_{m\ge3},
 \qquad E(P)\ge\eta_{m_q}S_q(Q_q),\qquad
 \|P\|_\infty^2\ge2\eta_{m_q}S_q(Q_q).
\]

奇偶加强来自每条活跃整数系数链在 1 处消失，故链能量为偶数；当 \(m_q\)
为偶数时先提升到 \(m_q+2\)。若 \(m_q\ge3\) 仍取等，系数必须全为
\(\pm1\)，而前 \(m_q-1\) 个幂和相同会由 Newton 恒等式迫使正负指数集相同，
矛盾，故再提高 2；\(m=2\) 的
\(1-u-u^2+u^3=(1-u)(1-u^2)\) 表明加 2 不能提前。不同 residue 链分割
系数下标，平方能量逐链相加，没有跨链抵消。所有指数同时缩放时 \(m_q\) 与
链数只作重标号。两个 Tang 等号例的最佳
证书分别恰为 12、16，与全部能量相等，既表明尖锐，也表明仍需逆结构输入。
长度至多 5、指数至多 8 的全部 1,286 个非降多重集、6,077 个约数方向有限
审计零失败；其中 1,977 个偶重数方向触发奇偶加强、2,259 个 \(m_q\ge3\)
方向触发矩刚性加强。无限量词由 Vandermonde、逐链偶性和 Newton 证明承担。

## #539：非悬挂的高维单纯形薄层

对

\[
 F_{d,L,W}=\{x\in\mathbb Z_{\ge0}^d:L\le|x|_1<L+W\},
 \qquad T=L+W-1,
\]

精确刻画正部差：非满支撑向量只需 \(|u|_1\le T\)，满支撑向量则必须
\(|u|_1\le W-1\)。因此

\[
 |F|={T+d\choose d}-{L+d-1\choose d}=\Theta_d(WL^{d-1}),
\]

\[
 |D(F)|={T+d\choose d}-{T\choose d}+{W-1\choose d}
       =\Theta_d(L^{d-1}+W^d).
\]

取 \(W=L^\theta\) 的最优点为 \(\theta=(d-1)/d\)，指数为
\(d/(d+1)\)：二维是 \(2/3\)，维数增加反而趋向 1。该路线不同于第七轮
suspension，并严格排除“只升级反对角薄层维数”的候选族。更强地，令
\(N=|F|\)、\(D=|D(F)|\)：一个坐标面给 \(D\ge N/W\)。当 \(d\ge3\)
三维边界补零给 \(D\ge4W^2\)，加权几何平均给
\(D\ge4^{1/3}N^{2/3}\)；当 \(d=2\) 直接代入精确式并用带权 AM--GM 给
\(D\ge\tfrac32N^{2/3}\)。故对维数也可增长的全部参数都有

\[
 D\ge\tfrac32N^{2/3}.
\]

所以该构造类的 \(2/3\) 屏障不是固定维渐近常数造成的。维数一的退化族另有
\(D=N=W\)；常数 \(3/2\) 的断言从 \(d=2\) 开始，最小参数
\((d,L,W)=(2,1,1)\) 给 \((N,D)=(2,3)\)，没有小值例外。

## #788：固定/缓增秩 GAP 的公共和证书

对任意有限母集 \(P\) 及 \(m=|P|-s\)，固定和 \(t\) 的不同元素表示边构成
matching，故有精确式

\[
 \bigcap_{C\subseteq P,\ |C|=s}(C\hat+C)
 =\{t:\nu_P(t)>m\}.
\]

若 \(P\) 是边长 \(L_i\) 的秩 \(r\) 2-proper GAP，坐标和 \(t\) 的有序
表示数为

\[
 R(t)=\prod_i\bigl(L_i-|t_i-(L_i-1)|\bigr).
\]

令 \(V=\prod L_i\)、\(\theta=((2m+2)/V)^{1/r}\)、
\(q_i=\lceil\theta L_i\rceil\)，则 \(R(t)\ge2m+2\) 的中心盒是全部
\(s\)-子集的共同证书，大小

\[
 \prod_i(2(L_i-q_i)+1).
\]

固定 \(r,\varepsilon\) 且 \(s\ge(1/2+\varepsilon)V\) 时，它至少为
\([1-(1-\varepsilon)^{1/r}]^rV\)。题目区间内固定秩 GAP 只有
\(n^{O(r)}\) 个参数，故 \(p=\sqrt{\log n/n}\) 的随机 \(B_p\) 可一次排除
该整个精确定义的分支。半密度阈值是真实的：matching 最大只有
\(\lfloor V/2\rfloor\)。一般 Freiman 逆定理不保证容器体积小于
\((2-\varepsilon)s\) 或以相同体积 2-proper 化，故这没有闭合 Sanders 后的
全部候选。

固定 \(\varepsilon\) 还可换成 \(\delta_n\to0\)：秩至多 \(R\) 时证书至少
有 \((\delta_n/R)^R V\) 项，取
\(s=D(R/\delta_n)^Rp^{-1}\log n\) 仍可支付全部 GAP 参数。若
\(\delta_n^{-R}=n^{o(1)}\)，该规模仍为 \(n^{1/2+o(1)}\)。所以子类内部已
允许任意次多项式的半密度缺口；缺的是无条件容器二分。

参数账本还可允许 \(R=R_n\) 缓慢增长：取
\(s=DR(R/\delta)^Rp^{-1}\log n\)，单容器漏选概率为 \(n^{-DR}\)，足以支付
至多 \((Cn)^{2R+1}\) 个 GAP。若
\(\log R+R\log(R/\delta)=o(\log n)\)，仍有 \(s=n^{1/2+o(1)}\)。这只扩大
同一高于半密度的 2-proper 容器类，不补上一般逆定理。

新颖性边界也已收紧：matching 交公式应视为标准 folklore，盒计数和随机
并合界是其整理性推论；定向检索不到逐字表述不构成优先权证据。本轮不把
#788 结果列为论文级新主定理。

## 证据入口与边界

- `work/25/attempt.md`：完整遍历证明、有限激活截断修复及异常轨道构造；
- `work/256/attempt.md`、`residue_chain_certificate.py`：一般 Vandermonde/
  逐链偶性/Newton 矩刚性证明和有限恒等式审计；
- `work/539/attempt.md`、`simplex_slab_audit.py`：60 个逐集合实例及 95,950 组
  全参数公式不等式实例；
- `work/788/attempt.md`、`gap_certificate_audit.py`：GAP 定理、来源纠错及
  秩至多 3、体积至多 14 的 31 个盒、285 个子集大小穷举实例。

全部脚本只验证有限恒等式，不承担无限量词。四个官方问题均保持开放；
`original_problem_closed_count = 0`，`new_q2_candidate_count = 0`。

状态：`BUDGET_EXHAUSTED_NO_Q2`。
