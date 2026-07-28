# 高分历史目标的实时状态与题意复核

核验日期：2026-07-28

本表复核的是初筛中分数较高、但已有搜索历史的 15 个目标，用于校准状态门槛和题意门槛；它们不等同于 fresh shortlist。结论为：12 题仍开放，1 题已解决，2 题状态尚不能可靠确认。

| 题目 | 当前状态 | 题意/证书审计 | 分流结论 |
| --- | --- | --- | --- |
| `unsolvedmath-opg-404` | uncertain；[Illinois problem register](https://dwest.web.illinois.edu/regs/vdwconc.html)仍列为猜想 | 应补 `k≥l≥2`；反例同时需要一个精确上界证书和一个显式下界着色 | 降级 |
| `unsolvedmath-kou-21.134` | **resolved**；[Kourovka Notebook v45](https://arxiv.org/abs/1401.0300v45)已标星，两问均为否定；见[Li–Shi](https://doi.org/10.1007/s11587-023-00835-4) | 两个子问题，非原子记录 | 从开放队列移除，转为已知反例基准 |
| `unsolvedmath-kou-21.135` | open；[Kourovka Notebook v45](https://arxiv.org/abs/1401.0300v45) | 证书为同特征标次数多重集、但可解根基性质不同的一对有限群 | 保留；仅限新策略 |
| `unsolvedmath-opg-171` | open；[2024 年研究](https://arxiv.org/abs/2406.17723)仍称其为开放特例 | 需限定有限简单图并统一分块定义；反例需要图、分块及着色 CNF 的不可满足证书 | 降级 |
| `unsolvedmath-opg-56230` | open；[相关理论](https://arxiv.org/abs/1704.06667) | “non-empty”必须修成“至少有一条边”，否则无边图会制造伪反例 | 修复题面后保留 |
| `unsolvedmath-opg-815` | open；[近期部分进展](https://arxiv.org/abs/2507.05548) | 需限定有限简单图；反例须附 `Δ+2` 全着色不可满足证书 | 著名且高度饱和，降级 |
| `unsolvedmath-kou-21.59` | open；[Kourovka Notebook v45](https://arxiv.org/abs/1401.0300v45) | almost simple 与 quasisimple 两问必须拆开 | 拆分后保留 |
| `unsolvedmath-kou-21.89` | open；[Kourovka Notebook v45](https://arxiv.org/abs/1401.0300v45) | 证书为 `n>39` 且 `p(n) | n!`；分拆数和整除性均可独立精确复算 | 历史目标中的首选 |
| `unsolvedmath-opg-46584` | open；[计算研究](https://arxiv.org/abs/1705.08724) | 应明确向下取整；反例图还需圈分解 ILP/SAT 的不可满足证书 | 降级 |
| `unsolvedmath-opg-59976` | open；[GIMPS](https://mers.sourceforge.io/mersenne.html)仍列为猜想 | 短证书为素数 `p,q` 与 `2^p≡1 mod q²`，但候选极稀疏 | 降级 |
| `unsolvedmath-opg-1757` | open；[原论文](https://arxiv.org/abs/math/0302185) | 本地题面漏掉 `e≠f`；否则令 `e=f` 会产生伪反例。修复后可用精确森林计数复核 | 修复后高优先 |
| `unsolvedmath-opg-37413` | uncertain；[Open Problem Garden 原页](https://www.openproblemgarden.org/op/alexas_conjecture_on_primality)有多次改写 | 版本、取整和来源稳定性不足 | 暂时移除 |
| `unsolvedmath-kou-21.113` | open；[Kourovka Notebook v45](https://arxiv.org/abs/1401.0300v45) | 必须拆成 (a)(b)；(a) 可找负/非整数特征标重数，(b) 需要更强的模表示证书 | 保留 (a)，降级 (b) |
| `unsolvedmath-kou-21.88` | open；[Kourovka Notebook v45](https://arxiv.org/abs/1401.0300v45) | 这是正见证构造题；有限搜索失败不能否定它 | 转 witness lane |
| `unsolvedmath-opg-563` | open；[相关研究](https://arxiv.org/abs/1802.07196) | 应补 `n≥2,d≥1`；反例是长度 `d(n−1)+1` 的零和自由序列，可用子和 DP 精确验证 | 高优先；仅搜合数 `n,d≥3` |

## 校准后的历史目标顺序

1. `unsolvedmath-kou-21.89`
2. `unsolvedmath-opg-1757`，先补 `e≠f`
3. `unsolvedmath-kou-21.135`
4. `unsolvedmath-opg-563`
5. `unsolvedmath-kou-21.59` 的两个拆分题
6. `unsolvedmath-opg-56230`，先修复“非空图”
7. `unsolvedmath-kou-21.113(a)`

`unsolvedmath-kou-21.88`应独立进入正见证构造通道，不进入反例搜索排行。
