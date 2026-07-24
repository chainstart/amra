# R003 core：Erdős #809 / #592

日期：2026-07-23

本包是 R003 标准宏周期闭合主线 B 的独立研究产物。两题均按真实活动推进，
均未使用四小时上限冒充实耗；没有修改中央台账，也没有提交版本控制。

| 问题 | 官网状态复核 | 本轮严格结果 | 原题闭合 |
|---|---|---|---|
| #809 | OPEN | 一锚点 fan；Case 1 距离 2 归约；无三步路的双团/split 精确二分 | 否 |
| #592 | OPEN | Case 4/5 排序规格可满足；深度 3 槽位块证书；动态并合不变量 | 否 |

最重要的新断点：

- **#809：** near-complete-split 分支中，内部边可集中在交叉坏 hub 上；
  尚缺把“缺交叉边/补内部度数”的权衡转成
  \((1/8-o(1))n^2\) 颜色的鲁棒引理。
- **#592：** 同一棵 \(T(r)\) 树参与多场二人博弈时，位于不交后继槽位块
  的 conservative extensions 尚未证明可交换并合，并同时保持
  critical/decision node、clear coarsening 与 push-up。

## 产物

- `809/REPORT.md`、`809/RESULT.json`：#809 证明、边界与下一引理；
- `809/verify_809_r003.py`、`809/verification.json`：显式 \(C_7\) 模板与
  邻域障碍穷举；
- `592/REPORT.md`、`592/RESULT.json`：#592 有限规格、递归不变量与断点；
- `592/verify_592_depth3_slots.py`、`592/verification.json`：Case 4/5
  排序和深度 3 槽位块证书；
- `SOURCE_MANIFEST.json`：本轮重新抓取的一手来源、哈希及 R002 错源校正；
- `TIMING.json`：真实墙钟活动与验证器计时；
- `validate_package.py`、`SHA256SUMS`：整包复核和校验和。

## 复核

在仓库根目录运行：

```bash
python3 artifacts/erdos_master_rotation/R003/core_809_592/809/verify_809_r003.py
python3 artifacts/erdos_master_rotation/R003/core_809_592/592/verify_592_depth3_slots.py
python3 artifacts/erdos_master_rotation/R003/core_809_592/validate_package.py
```

两个有限验证器只核对报告中明确标出的有限/代数层，不替代一般图证明、
折叠树博弈证明或序数 partition relation。
