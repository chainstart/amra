# OPG-611 六小时 hard portfolio 审计

时间：2026-07-29（Asia/Hong_Kong）

## 结论边界

本班次没有找到 Bermond--Thomassen `k=4` 的反例，也没有关闭完整的
16 顶点搜索空间。只有满足以下条件的事件才计作数学排除：

1. 对应 master CNF 为 UNSAT；
2. 保存了 CNF 和 DRAT；
3. 独立 `drat-trim` 返回 `s VERIFIED`。

hard runner 的 `timeout` 只表示在给定参数和时间内未解开；`progress.json`
明确标记为 `telemetry_only_not_resumable=true`，不能把模型数、cuts 数或
长时间 master solve 当作排除证据。

## 基线搜索

17:23 的四分片快照为：

| shard | processed | DRAT 排除 | hard/timeout | candidate |
| --- | ---: | ---: | ---: | ---: |
| 0 | 22 | 5 | 17 | 0 |
| 1 | 20 | 4 | 16 | 0 |
| 2 | 10 | 2 | 8 | 0 |
| 3 | 12 | 4 | 8 | 0 |
| 合计 | 64/497 | 15 | 49 | 0 |

逐事件计数得到 15 个 `proof_status=independently_verified`，与四份
`state.json` 的排除数一致。四个长期 worker 在本报告写作时仍运行，因此
这个数字是带时间戳的前沿快照，不是完整目录结论。

本班次新增的可认证排除是 catalogue `#26`：

```text
graph6 = O?????????????_?G?FoA
CNF SHA-256  = 11f8eab199b09d21da57a64458b88da2665759be9cfe0bdffb3cfec8cd25258a
DRAT SHA-256 = ee47f1201af91eede2980ca1c95e329e271afcc6a1a751c109b9fd5c16b942e3
```

manifest 位于
`artifacts/opg_breakthrough/certified/opg611-shard-2-v2/proofs/`。本班次
重新运行独立 checker，得到 `s VERIFIED`，使用 6,911 个 resolution steps。

## 定向 hard 实验

两个完整的 Glucose42 实验都只得到 timeout：

| catalogue | wall 合同 | models/solves | packing/residual cuts | master solve | 结果 SHA-256 |
| --- | ---: | ---: | ---: | ---: | --- |
| #2 | 18,000 s | 6/7 | 6,144/768 | 18,067.720 s | `72508cc06e176ad2a4d9fdd51d3cf6a7047b88c3c043fcaa228ceedc75f3f67b` |
| #32 | 18,000 s | 6/7 | 6,144/768 | 18,017.325 s | `299b1d09baa8ae508c3813092ed8c3fc4c1771c6ff3f69505fadee2eac994dbc` |

两者的可计时工作中超过 99.8% 都消耗在 master SAT，而 residual separator
和 short-packing separator 合计只占数秒。这定位了真实瓶颈，但不提供
数学排除。

catalogue `#52` 的 MapleChrono 实验在第三次 master solve 中触发 native
`pysolvers` SIGSEGV。它没有 `result.json` 或 proof，严格分类为运行失败，
不是 timeout、排除、候选或负搜索结果。取证记录见
`OPG611_MAPLECHRONO_FAILURE_2026-07-29.md`；后续 Glucose42 重试使用全新
目录，没有复用崩溃进程的状态或 clauses。

## 900 秒参数探针

为了判断小 batch 是否能提高 master-model 吞吐，又对 `#2/#32` 运行
`short_batch_size=128`、关闭 orbit lift 的独立探针：

| catalogue | elapsed | models/solves | packing/residual cuts | master solve | 状态 | 结果 SHA-256 |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| #2 | 925.946 s | 6/6 | 640/640 | 923.642 s | timeout | `a1be14bdb35c5eeee01eeba96922ef1734c10710947d7bbb8255da098b2c2920` |
| #32 | 900.240 s | 3/4 | 384/384 | 899.275 s | timeout | `e84622add27812f3fe47745cdb4d0970658b5661ac4775e0cba9d449e1a9a72c` |

小 batch 降低了早期 CNF 膨胀，但没有突破既有模型前沿，并且仍几乎把全部
预算耗在 master SAT。这个样本不足以证明某参数全局更优；它只否定了
“把同一固定小 batch 配置直接加时就足够”的朴素策略。

## 最终 solver portfolio

最后三个实验也都正式生成 `result.json`，且都为 timeout：

| catalogue/backend | elapsed | models/solves | packing/residual cuts | master solve | 结果 SHA-256 |
| --- | ---: | ---: | ---: | ---: | --- |
| #2 / Minisat22 | 10,000.187 s | 7/8 | 7,168/896 | 9,994.157 s | `6e32004552fcba6ebb75031e9dadab149667daf3a0e7933370ac7fde797902a7` |
| #32 / Minisat22 | 6,600.076 s | 4/5 | 4,096/512 | 6,596.479 s | `e70dca81fed56dfdc119b51cd29a1e20bca978d314663a2518e5fcf3623b63c9` |
| #52 / Glucose42 fresh retry | 14,500.193 s | 3/4 | 3,072/384 | 14,497.172 s | `af7dd3702eceba845c3813589d43a7d6561436a11f45b569915809b62fd17e30` |

Minisat22 在 `#2` 比 Glucose42 多得到一个 model，在 `#32` 则少两个；这个
小样只能证明求解器敏感，不能建立稳定排序。三个结果仍有超过 99.9% 的可计时
工作位于 master SAT，均无 candidate、排除或 proof。至此本班次启动的 hard
组合已全部结束；四个长期基线 worker 继续运行。

## 下一轮可执行策略

1. **先做可恢复执行合同。** 每轮模型和新增 clause 写入 append-only
   journal，同时定期导出带 source/config/graph6 哈希的 canonical master
   DIMACS；恢复时逐条重放并核对 clause digest。这样 18,000 秒不再只留下
   不可继续的遥测。
2. **采用分阶段 batch。** 先用 128 级小 batch 获得低成本早期模型，再在
   model 吞吐骤降时切换 1,024 级 orbit-lift cuts；切换点由连续两次
   master-solve 时间比决定，而不是预先猜固定参数。
3. **把卡住的 master CNF 交给 proof-capable portfolio。** 对冻结 DIMACS
   分别运行 CaDiCaL/Kissat 类求解器；只有生成并独立检查 proof 后才记作
   排除。SAT 返回则把 orientation 交回原始、无颜色破缺的 `PACK4` 做
   反例核验。
4. **加强重复顶点块的规范化。** `#2/#32/#52` 的缺边图都含大量叶、孤立点
   或小重复块。下一项算法工作应是可验证的 twin-block lex leader / orbital
   branching；先在小阶上逐轨道检查“每个原解轨道保留至少一个代表”，再进
   16 阶 hard CNF。
5. **设置淘汰闸门。** 新表示若在同一图、同一 CPU、1,800 秒内既不减少
   master-solve 占比，也不超过现基线的 model/cut 前沿，就停止该路线；
   timeout 不重复累计成所谓“接近证明”。
