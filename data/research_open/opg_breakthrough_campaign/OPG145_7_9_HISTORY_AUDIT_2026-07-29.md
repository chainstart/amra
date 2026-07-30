# OPG-145 七至九阶历史运行独立审计

审计日期：2026-07-29

## 审计结论

历史目录
[`opg145-7-9`](../../../artifacts/opg_breakthrough/certified/opg145-7-9)
已经通过专用的独立审计器：

- 严格接受且只接受 `minimum_order=7`、`maximum_order=9`、
  `next_order=10`、`next_index=0`、`shard=null`、`status=complete`；
- 使用旧 checkpoint 记录且 SHA-256 仍吻合的 nauty 2.8.8 `geng`，
  对 \(n=7,8,9\) 分别重新执行
  `geng -q -C -d2 -D5 n`；
- 独立解码每个 graph6，重新检查简单图、二连通、最小度至少 2、最大度至多 5；
- 独立重算 `maximum_degree == 5 and not 3_sparse`；
- 对每个有效目录项，按 `(order, catalogue index, graph6, vertices, edges)`
  精确绑定一条历史事件；
- 不调用 SAT 求解器，也不调用活搜索器的 verifier；以独立 properness 检查和
  两色子图 union-find 检查重放每个 7 色见证；
- 所有逐阶固定计数、逐阶 catalogue SHA-256、checkpoint 总计和事件 EOF
  同时闭合。

认证产物：

- [`audit-history-v1.json`](../../../artifacts/opg_breakthrough/certified/opg145-7-9/audit-history-v1.json)
- 认证产物 SHA-256：
  `acca7d407c667c3e955bcead4b61fddc2a0081ae07fd15fbe578ea8009d39b93`
- 独立审计器：
  [`opg145_history_run_audit.py`](../../../src/amra/discovery/opg145_history_run_audit.py)
- 审计器 SHA-256：
  `74465c7c99aa8bbebbe84ac9973a6ea9ab636298faefd01a3bf3455a76e03330`

## 精确分阶结果

| 阶数 | geng 目录 | 已知正例过滤 | 非 3-sparse、Delta=5 | 重放通过见证 | catalogue SHA-256 |
| ---: | ---: | ---: | ---: | ---: | --- |
| 7 | 356 | 161 | 195 | 195 | `eefb48e8d6f62ebb3a22dfc3633d67d103f955797445e5a01b36b853f3dc7bee` |
| 8 | 3,511 | 896 | 2,615 | 2,615 | `53ac4992212f8032ce52949c17175fbf53b77ae3e34c0218b3de0be9820fb566` |
| 9 | 44,920 | 5,717 | 39,203 | 39,203 | `a20ced5769d777af734c2983b3812c365f4836935e51280e5b0205556b078f34` |
| **总计** | **48,787** | **6,774** | **42,013** | **42,013** | `88f1933024be0c7ea16671ff9c72488394582559ef593a42177117ec0b28093d` |

事件分阶 SHA-256：

| 阶数 | 已绑定事件 SHA-256 |
| ---: | --- |
| 7 | `776d6e1907f46a215de0847637335efccd8011ec763f977d7d3e8ce1197182cf` |
| 8 | `8e9c385d7be23341584e7ed8c064faef01c923ce186293d0de3c2fa1cea10f96` |
| 9 | `a51b26a907164291755af386cfc0699499010ca021e67dbb4aa619605d12b278` |

输入文件：

- `state.json`：
  `d1f735db848a791f04c8e05904cbb5628e5f848ab976683e846b92549c25cdee`
- `events.jsonl`：
  `496952cd32fe8f5c021692df04aaa6a2c1535b03c3fe500e32f779e98f085ef2`

## 历史 provenance 边界

旧 checkpoint 声明的搜索实现指纹为：

```text
470e43d729c1db9bf518d7f6efc307ec38dd475ee4968c40ee8c53121a4371ce
```

当前 `opg_coloring_search.py` 按同一“绝对路径 + 文件哈希”算法得到：

```text
955a1014ac1ad114ba041767f54bab1c5ae79a4265d6d784d356f0430e7eb971
```

二者明确不相等。审计器没有把旧运行伪装成由当前源码产生，也没有要求二者相等；
它把旧指纹作为固定的历史身份字段原样保存。由于历史目录没有保存对应旧源码
字节，不能从该目录重新构造或逐字验证旧搜索实现。

旧 state 对 `geng` 保存了路径和二进制 SHA-256。审计时重新核对通过：

```text
9730b53764bdb28ecd2fdf755fafbc76992050f39e5ea19bb7d91433a26583e9
```

但是旧 state 没有保存当时动态库的哈希。审计器不会把当前 `ldd` 快照冒充历史
绑定；JSON 中明确标记
`dynamic_linkage_recorded_by_legacy_checkpoint=false` 和
`legacy_checkpoint_bound=false`。当前重放所见主要本地依赖为：

- `libnautyW1-2.8.8.so`：
  `28283263ac5d2dc1102485488edd63128e65c71325279f98242c2b8ea435573e`
- `libcliquer.so.1`：
  `b1ccfac9465a0fc084b505d7415a8322da285705aaeb4f8f33f32cf926249c4e`

这仍是历史 provenance 的残余边界。不过，对于本次有限目录，当前依赖实际输出
的三个逐阶 catalogue 已由上表固定 SHA-256 封住；数学置信力来自精确目录重生成、
逐事件绑定以及独立语义见证重放，而不是来自旧实现与当前实现相同的假设。

## Fail-closed 攻击测试

新增
[`test_opg145_history_run_audit.py`](../../../tests/test_opg145_history_run_audit.py)
覆盖：

1. 正常的三阶小目录逐阶闭合，并确认报告保留历史 provenance 边界；
2. 删除一个应有事件，必须以 `missing eligible event` 失败；
3. 给 checkpoint 人为补大 `generated` 计数，必须在严格 state 合同处失败；
4. 在目录末尾补一条多余事件，必须以 `events remain` 失败；
5. 用同计数、同过滤分类的另一张图替换某阶目录项，必须由固定 catalogue
   SHA-256 拒绝；
6. 用 JSON 布尔值 `false` 冒充整数计数 0，必须由严格类型合同拒绝；
7. 把见证替换成仍 proper、但含双色圈的 7 色染色，必须由独立 union-find
   checker 拒绝。

执行结果：

```text
pytest -q tests/test_opg145_history_run_audit.py
7 passed

pytest -q \
  tests/test_opg145_history_run_audit.py \
  tests/test_opg_coloring_run_audit.py \
  tests/test_opg_coloring_search.py
22 passed
```

## 对累计 Delta=5 边界的影响

数学范围证明
[`OPG145_SCOPE_AUDIT_2026-07-29.md`](OPG145_SCOPE_AUDIT_2026-07-29.md)
已严格证明：

- 任意 OPG-145 反例含有一个本身仍为反例的二连通 block；
- 固定 \(\Delta=5\) 时，坏 block 仍必须满足 \(\Delta=5\)；
- \(n<6\) 不可能有 \(\Delta=5\)，而文中给出的 \(K_6\) 显式 acyclic
  7-edge-colouring 覆盖 \(n=6\) 基例。

本报告现已独立闭合 \(n=7,8,9\)。再结合已独立认证的十阶产物
[`audit-all-v2.json`](../../../artifacts/opg_breakthrough/certified/opg145-n10-six-hour/audit-all-v2.json)，
可得到精确的累计有限结论：

> 每个顶点数至多 10、最大度恰为 5 的有限简单图都有 acyclic
> 7-edge-colouring；因此这一范围内不存在 OPG-145 反例。

该结论仍然只属于 \(\Delta=5\) 层。当前 `-D5` 目录不含最大度
\(6,7,8,9\) 的十阶图，不能改写为“全部至多 10 顶点简单图均已验证”。
