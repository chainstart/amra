# R002 core attack：Erdős #776 / #635

真实研究窗口：2026-07-23 19:32:51--20:12:20 HKT  
单 agent 实耗：2,369 秒（0.6581 agent-hours）；两题均低于各自 4 小时上限。

| 题号 | 结果 | 闭合距离 | 本轮最严格推进 |
|---|---|---:|---|
| #776 | OPEN；无原题证明/证否 | 1 -> 1 | 精确 run-compressed 引擎；`h(74997)=8`；粗 diagonal 路线在 `66843/66844` 的严格断点 |
| #635 | 精确极值仍 OPEN；渐近子问已有肯定解 | 2 -> 2 | 固定 valuation 局部冲突路线全参数反杀；已知 6-cycle 的 13V/13E 全分量闭合；`A=2` 完整枚举到长度 14 |

有限计算只承担实现交叉核对、完整定长枚举或完整有限分量证书。两份报告均
单列了最小未证引理与下一可判定动作，没有把子核结果回译为原题闭合。

复核：

```bash
python3 776/verify_rank5_rotation.py
python3 635/verify_closed_component.py
g++ -O3 -std=c++17 635/verify_fixed_A2_cycles_14.cpp -o /tmp/v635
/tmp/v635
(cd 776 && sha256sum -c SHA256SUMS)
(cd 635 && sha256sum -c SHA256SUMS)
sha256sum -c SHA256SUMS
```
