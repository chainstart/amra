# R003 closure core：Erdős #776 / #635

研究已于 2026-07-23 21:47:02 HKT 冻结；两题均取得严格进展，但均未闭合。
没有修改中央台账，也没有创建提交。

- `776/`：完成 rank-8 cap 内的 \(8\to5\) 全 carry 降阶，得到两个精确
  Galois 影损门槛，并证明只有 cap 顶部 17 个残差影响 rank-6 参数传播。
  rank-8 屏障自身的全参数入口/传播仍缺一条 coupled gap 势，故
  `closure_distance=1` 不变。
- `635/`：完整枚举 734,320,442 个新固定 valuation 乘子元组，排除相应
  短双圈核；证明 Euler-product 与一阶矩两个全长度不变量，并给出它们仍
  允许复合 non-backtracking 闭游走的严格反例。任意长度/混合 valuation
  核仍未解决，故 `closure_distance=2` 不变。

快速复核：

```bash
python3 635/verify_cycle_invariants.py
python3 776/verify_rank8_capped_block.py
```

完整 `#635` 枚举复核：

```bash
taskset -c 6 nice -n 10 python3 635/run_fixed_A_cycle_audit.py
```

逐题来源、实际计时、机器证书及诚实量词边界见各自目录。
