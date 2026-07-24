# R004 core：Erdős #809 / #592

日期：2026-07-24

本包记录单 agent、轻 CPU 的 4,270 秒真实前台研究；最终封装、等待与重复
验证不计入研究时长。两题各自低于四小时上限，没有修改中央台账，也没有
提交版本控制。

| 问题 | 官网状态 | 本轮最强结果 | 原题闭合 | Q2 判断 |
|---|---|---|---|---|
| #809 | OPEN | 完整证明 near-complete-split 支的 \(n^2/8-o(n^2)\) 下界 | 否 | 尚未达到 |
| #592 | OPEN | 对称 pushout 反例、有限-\(\Gamma\) 根 guard、精确重建义务 | 否 | 否 |

## 核心进展

- **#809：** 若存在近半大小独立集，补集也近半，且
  \(\delta(G)\ge n/2-o(n)\)，则从一条内部边构造 core/hub 边族，
  得到至少 \(n^2/8-o(n^2)\) 条两两 \(C_7\)-兼容边。清洗显式容纳
  star-swap、一锚点 fan、低度 hub、同行和同列边界。
- **#592：** 独立构造的 successor-child histories 不存在保持实际孩子
  编号的对称 pushout；来源 Cases 4/5 使用唯一有序回放。固定有限
  \(\Gamma\subset\omega\) 强迫 \(T(\omega)\) 根标签为空，所以依赖非空
  根标签的字面移植失败；但空根 finite-rank 重建仍未排除。

## 首断点

- **#809：** 尚缺把每个强归纳子问题归约到该 split 支或另行解决
  near-two-clique 支的全局 stability/induction interface。
- **#592：** 尚缺策略感知的 \(T(3)\) 有序回放引理，必须同时保持实际
  child indices、凸 partition nodes、completion barriers、
  critical/decision nodes 和 clear coarsenings。

## 复核

在仓库根目录运行：

```bash
python3 artifacts/erdos_master_rotation/R004/core_809_592/809/verify_809_split_union.py
python3 artifacts/erdos_master_rotation/R004/core_809_592/592/verify_592_commutation_guard.py
python3 artifacts/erdos_master_rotation/R004/core_809_592/validate_package.py
```

有限验证器只核对显式模板、离散接口与代数；一般渐近证明及所有范围限定
写在逐题 `REPORT.md` 和 `RESULT.json` 中。
