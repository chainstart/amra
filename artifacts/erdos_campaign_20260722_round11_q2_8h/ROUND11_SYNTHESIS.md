# Erdős 21 题第十一轮终态汇总

日期：2026-07-22 至 2026-07-23（Asia/Hong_Kong）

## 1. 预算与总判定

四个并行工作流均从 `2026-07-22T22:15:18+08:00` 运行到统一证明硬边界
`2026-07-23T00:15:18+08:00`，每组登记 7,200 秒，累计 28,800 秒，即
8 agent-hours。证明期最多使用三个低优先级单核计算，低于 WSL 8 个逻辑
CPU 的 50%；边界后只作冻结、既定验证、校验和与汇总。

终态计数：

- 原始命题完整证明或证否：**0**；
- 改变公认主阶或主指数：**0**；
- 达到本轮 SCI 二区停止门槛：**0**；
- 发现已接受/已发表证明失效：**0**；
- 严格证否内部候选证明路线：**1**（#776 的常数 28 colex 目标）；
- 有实质严格阶段推进的题：#25、#256、#679、#686、#776、#827、#1083；
- 严格路线反例/尸检推进：另含 #635。

因此本轮没有把阶段引理、条件结论或有限证书冒充原题闭合，也没有成果达到
可单独支撑 SCI 二区主论文的门槛。

## 2. 最强成果

### #1083：完整排除 high-Q 临界层的 low-order 分支

DRC/Ramsey 与 KKPR 结构只需产生 3 个线性独立、两两无理角法向；统一
有界度数的 torsion-closure 定理逼出正维扭陪集，再由一参数实单位球论证
排除该陪集。剩余 high-order 分支给出 `n^(1/5-o(1))` 来源扇、
`n^(2-o(1))` repair edges、`n^(3-o(1))` clean marks、三来源核，以及在
`n^(4/5-o(1))` 张 Q-rich 面上同步的缓慢增长共同参考图形。

这闭合了 high-Q 的一个完整分支，但 Rudnev 主项恰在 `n^(7/5-o(1))`
饱和；普通 KST/DRC 与二、三阶矩都不足。low-Q 分支仍未处理，所以 #1083
仍开放、主指数未改变。

### #679：实际起点低导谱控制扩展到任意固定 polylog 窗口

对任意固定 `d>=1`，取 `H=(log X)^d`，增长矩 ANOVA 能量把所有

\[
 c(T)\le \exp((1-\eta)HL)
 =X^{(1-\eta+o(1))(\log X)^{d-1}\log_2X}
\]

的 primitive 导数在规定实际区间上的总有符号贡献控制到
`exp(-(eta-o(1))HL)`。若原题候选存在，它必迫使更高导数尾有正贡献
`exp(-o(HL))`；目前缺的正是这个超高导有符号尾在自洽实际起点上的上界。

最新来源核实表明：Lau 2026 的 Theorem 1.3 无条件达到 `C log k`，仍比
#679 第一问差一个 `log log k`；其条件性“原问为假”依赖未证短区间密度
猜想。官网仍把第一问列为 OPEN；官网另已记录第二个更强子问的反例。本轮
没有把二者混同。

### #776：内部 colex 常数目标被精确证否

对 defect 递推证明了 suspension/raising 的全参数传播接口，并实现与原
整数递推逐项等价的 lazy-carry 算法。精确证书给出

\[
 d^{[75000]}_3=70306875137528
 =\binom{74999}{3}+29,
\]

其 canonical 展开为 `C(74999,3)+C(8,2)+C(1,1)`。因此此前足以闭合末端
的统一目标 `d_3<=C(M-1,3)+28` 为假；`M=70000` 的超额为 28，未穷举中间
值，故不声称 75000 是最小反例。这只证否 colex 路线，不证否原题 #776。

### #256：prime-split cyclotomic norm 障碍

若素数 `q` 恰整除 `m` 个指数，遗漏 `s=n-m` 个，且
`q-1` 不整除 `s-1`，则严格有

\[
 E(A)\ge6m,\qquad \|P_A\|_\infty\ge\sqrt{12m}.
\]

半分裂时得到 `E(A)>=3n`。prime-power 版本还给出精确范数同余骨架。任意
指数元组未必存在这种不相容分裂，所以尚无通用主界改进。

### #25：Möbius 压缩 activated-intersection 判据

在早先 compatible-clique、log-Cesàro、动态 core/tail 与调和加权判据上，
本轮末段把产生同一 `(L,r,epsilon)` 的容斥项先合并，再把两个 activation
状态精确写成“共同完整进程减一个首代表”。所得压缩总变差条件分别推出自然
密度和对数密度，且逐点不劣于 raw clique 付费。在无冗余平方自由有限块
`n_i=L/p_i` 上，至少二元交的 `2^k-k-1` 次 raw 付费压成系数 `k-1`。

这证明了真实算术系统中的指数级代数压缩，但尚未构造两判据覆盖的无限系统
类严格分离例，也未证明任意系统的压缩总变差足够小；当前仍只适合作为潜在
短文或论文一章。

### #686 与 #827

- #686：得到全参数 Mahler 公式
  `Delta^r C_m(0)=r![v^(m-r)]H_m/prod_(j<=r)(1-jv)`，并统一排除首个
  未解 Cartier 族的末四个 Mahler 系数为障碍；常数项和中间带仍开放。
  七个固定 `m` 的全整数证书保留，但不能外推。
- #827：得到 H5/H6 到 rainbow 指数的精确传递，H6 精确包含一般位置
  #104，H5 经反演化为固定中心 secant energy，并核清
  `E_inv=2C4+C5`、`E_rad=C4+C5+C6`；没有新的幂次节省。

## 3. 其余题目的终态

| 题号 | 第十一轮终态 |
|---:|---|
| 25 | 新增 Möbius 压缩自然/对数密度判据；原题 OPEN |
| 143 | numerator-gcd / denominator-lcm 拼接仍卡在有符号边界；OPEN |
| 148 | 既有 `446/289` 上界保留，本轮无新指数；OPEN |
| 256 | prime-split cyclotomic norm 子类定理；OPEN |
| 301 | 仍缺低拥塞规范表示或带容量 Hall；OPEN |
| 325 | 零锥 tube 的整数点总质量缺一幂；OPEN |
| 332 | 仍缺弱于正上 Banach 密度的自然复现条件；OPEN |
| 377 | 不同素数的递降商无法同步；OPEN |
| 539 | 四类投影逃逸仍可并存；OPEN |
| 635 | 两个 proper-divisor 局部匹配模板有严格反例，集合级 Hall 仍存活；OPEN |
| 679 | 任意固定 polylog 窗口的低导控制；超高导尾开放 |
| 686 | 全参数 Mahler 化简 + 固定参数证书；OPEN |
| 776 | 常数 28 内部路线被反例否定；原题 OPEN |
| 788 | 多和之间的证书相关压缩未建立；OPEN |
| 827 | 精确能量归约，无幂次节省；OPEN |
| 934 | quotient induction 后 fibre saturation 未闭合；OPEN |
| 950 | 缺 endpoint-weighted sieve；OPEN |
| 952 | 变化方向 CRT 墙的位置失控；OPEN |
| 963 | 缺跨层 reachable-wrap clique 总亏损界；OPEN |
| 1063 | 既有论文级下界保留，本轮没有不同增长级突破；OPEN |
| 1083 | high-Q low-order 分支闭合，high-order 与 low-Q 仍开放 |

## 4. 发表价值与下一断点

本轮没有一项可以诚实标为“已具备 SCI 二区主论文”。最接近继续累积成论文的
是 #1083 的完整分支排除与高阶核、#679 的增长矩低导谱定理，以及 #25 的
结构判据包；三者分别仍缺主指数节省、超高导尾估计和普遍总变差控制。

下一轮若继续，最清晰的三个硬目标是：

1. #1083：对 high-order 三来源核证明来源敏感 incidence saving，并另攻
   low-Q weighted branch；
2. #679：控制自洽实际起点的超高导有符号尾，或证明 Lau 所需的固定幂短区间
   高 `omega` 密度输入；
3. #776：放弃统一常数 28，寻找随低秩状态增长的正确 slack 或完全不同的
   Macaulay 末端不变量。

## 5. 证据入口

- `work/geometry/REPORT.md`、`work/geometry/INDEPENDENT_QA.md`；
- `work/679/REPORT.md`、`work/679/SOURCE_AUDIT_CHECKLIST.md`；
- `work/macaulay_pte/REPORT.md`、`work/macaulay_pte/INDEPENDENT_QA.md`；
- `work/broad/BROAD_REPORT.md`、`work/broad/BROAD_QA.md`。

所有工作流的 `RESULT.json` 与 `SHA256SUMS` 为机器可读终态。第十轮已本地
提交为 `794c2fe`；第十一轮按用户指令完成但尚未提交或推送。
