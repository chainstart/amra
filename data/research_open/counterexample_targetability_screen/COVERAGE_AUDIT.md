# 全题库覆盖审计

核验日期：2026-07-28

## 纳入范围

本轮显式读取 6 个题库：

- `formal_conjectures_open_research.yaml`
- `unsolvedmath_open.yaml`
- `erdos_open_637.yaml`
- `aim_problem_lists.yaml`
- `triangle_dissection_track.yaml`
- `weird_numbers_track.yaml`

四个主库原有 3,939 条；逐一比较 `data/banks/` 下全部 YAML 和 `data/problem_bank.yaml` 后，补入 4 条此前未覆盖的专题记录，最终库存为 3,943 条。

## 其余题库为什么未重复加入

- `formal_conjectures_all.yaml` 中的 1,068 条开放记录与 formal open 库相同。
- `unsolvedmath_all.yaml`、`unsolvedmath_index.yaml`、`unsolvedmath_open_non_erdos.yaml` 和 source-collision 库的开放记录均是 `unsolvedmath_open.yaml` 的子集。
- `erdos_full_1120.yaml` 的 637 条开放记录 ID 均已在 `erdos_open_637.yaml`。
- `ai_math_benchmark_2026.yaml` 的 16 条均是非开放复现任务。
- Carmichael、unitary-perfect、amicable 等专题库没有额外可靠的唯一开放命题：其中两个 amicable 题已有 formal/UnsolvedMath 对应项；“是否存在奇-奇亲和数”被错误标为开放，事实上已有实例。
- `data/problem_bank.yaml` 的开放项与专题库重复，没有新的唯一开放题。

## 新补入的 4 条记录

| 记录 | 覆盖结论 |
| --- | --- |
| `triangle-dissection-13` | 进入库存，但引用的 [Erdős #634](https://www.erdosproblems.com/634) 当前题意是“是否存在某个三角形”，不足以支撑本地“等边外三角形”的更强表述；转题面恢复 |
| `triangle-dissection-17` | 同上；转题面恢复 |
| `triangle-dissection-19` | Erdős #634 当前明确仍提到 `n=19`，但没有把外三角形限定为等边；转题面恢复 |
| `erdos-825-weird` | [Erdős #825](https://www.erdosproblems.com/825) 的“存在某个绝对常数”版本已经证明；本地记录混合了更强的 `C=3` 语言和 `σ(n)/n<4`，转题面与状态恢复 |

## 仍然存在的覆盖边界

- `erdos_open_637.yaml` 的 637 条均为目录占位记录，需要逐题恢复原文后才能做原子级评分。
- `aim_problem_lists.yaml` 的 166 条均为问题列表指针，列表内部问题尚未拆成原子记录。
- `data/bank_registry.yaml` 不能作为当前全量入口：17 个注册项中前 13 个仍指向旧目录 `/home/biostar/work/projects/amra/...`；本轮因此使用显式的本仓路径。

所以本轮已达到“本地题库记录级的去重覆盖”，但不能声称 AIM 列表内部和 Erdős 占位记录已经完成原子题面级覆盖。
