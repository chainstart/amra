# R004 closure core：Erdős #776 / #635

研究窗口：2026-07-24 09:54:13--11:04:19 HKT，共 4,206 秒真实、非重叠
前台研究；研究冻结后只作回归、文档、清单与哈希。未修改中央台账，未创建
提交。

- `776/`：top-17 的真实 \(G_9\) 条件坍缩为单个 next-residual cap；
  建立更宽的五项 rank-8 屏障并完成其低阶下降；把 first-carry 长递推的
  未知点提升为单个入口 \(D_8<{V-11\choose8}\)。该全称入口尚未证明，
  所以原题仍开放。
- `635/`：证明共享路径上的 first moment 与 Euler product 都只是端点
  梯度，严格判死该 coupling 路线；完整排除 branch/upward-branch
  顶点不超过 2,000,000 的全素数双环分量；建立全素数无冲突平行单环
  参数族并在 50,822 个因子对中找到 41 个单环，但没有双环。原题精确
  极值仍开放。

快速完整复核：

```bash
python3 validate_package.py --run-verifiers
```

只检查结构、JSON、时间账和 SHA：

```bash
python3 validate_package.py
```

逐题的原命题状态、`Q2`、首断点、来源与诚实量词边界见各自
`RESULT.json`、`REPORT.md`、`SOURCE_MANIFEST.json` 和 `TIMING.json`。
