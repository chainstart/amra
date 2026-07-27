# KOU-21.137 candidate audit: `SmallGroup(128,928)`

## 中文

### 核验范围

本地题库
`data/banks/unsolvedmath_open_non_erdos.yaml` 和原始抓取记录
`data/research_open/raw/unsolvedmath/problem_details.jsonl`
给出的 KOU-21.137 题面包含以下明确子命题：

> 对指数为 8 的有限 2-群，如果全体平方组成一个子群，那么该子群是否必为阿贝尔群？

本审计只核验这一明确子命题，不单独处理更一般的 powerful-subgroup 问题，
也不处理奇素数、指数为 \(p^2\) 的子命题。

### 独立方法

`export_cayley_table.g` 由 GAP 4.12.1 和 SmallGroups 1.5.3 构造
`SmallGroup(128,928)`。GAP 端只导出 catalog metadata、按
`Elements(G)` 固定的零基元素索引、完整的 \(128\times128\) Cayley 表和
128 个元素的平方索引；它没有判断结合律、指数、平方集合是否为子群或是否阿贝尔。

`verify_cayley_certificate.py` 不导入 AMRA 执行器或已有候选验证函数，只用
Python 标准库从表中重新检查：

- 16,384 个乘积全部在索引范围内；
- 全部 \(128^3=2,097,152\) 个三元组满足结合律；
- 存在唯一单位元，且每个元素有唯一双侧逆元；
- 元素阶分布为 \(1^1,2^{43},4^{68},8^{16}\)，所以指数恰为 8；
- 平方像集合有 16 个元素，对乘法和逆运算封闭；
- 平方像集合等于它所生成的 16 阶子群；
- 两个平方元素（零基索引 4 和 5）不交换：
  `table[4][5] = 23`，而 `table[5][4] = 61`。
  它们分别是零基索引 8 和 9 的元素的平方。

### 结论

候选不是伪候选。`SmallGroup(128,928)` 是阶 \(128=2^7\)、指数恰为 8
的有限 2-群；它的全体平方恰好组成一个 16 阶非阿贝尔子群。因此它反驳了
KOU-21.137 题面中上述指数 8 的明确子命题。

完整 Cayley 表和平方映射以 `zlib+base64` 自包含在
`certificate.json` 的 `evidence_payload` 中。

### 复现与哈希

从仓库根目录运行：

```bash
set -o pipefail
AUDIT=data/research_open/unsolvedmath_counterexample_campaign/candidate_audits/kou-21.137-smallgroup-128-928
GAP_ROOT=$HOME/.cache/amra/tools/gap-4.12.1/usr/share/gap
GAP=$HOME/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap
"$GAP" -l "$GAP_ROOT" -q < "$AUDIT/export_cayley_table.g" \
  | python3 "$AUDIT/verify_cayley_certificate.py" \
  | sha256sum
```

可复现的输出 SHA256：

```text
d9ecca5e40d88a890ea103acbbe9efda354c9219ebc79e4d7908b5c74cf64bf5
```

文件 SHA256：

```text
c9e0eaff5f5563f9a404bc1c64072a26017dadb55a5066ba02760a1a77452d92  export_cayley_table.g
7a2f19f7c387547128c9e0d4f34316e58a5bd29b07cee6c9da704c127b7d9540  verify_cayley_certificate.py
d9ecca5e40d88a890ea103acbbe9efda354c9219ebc79e4d7908b5c74cf64bf5  certificate.json
```

证书内未压缩 canonical JSON evidence 的 SHA256 为
`73007ea549c2026b0553477b2e9c8b5e45ffa59315501ce84509150b36679af4`。

## English

### Scope

The local bank and raw source record for KOU-21.137 explicitly ask whether,
in a finite 2-group of exponent 8, the set of squares must be abelian whenever
it is a subgroup. This audit addresses only that subclaim. It does not
separately settle the broader powerful-subgroup question or the odd-prime
exponent-\(p^2\) subclaim.

### Independent verification

GAP 4.12.1 with SmallGroups 1.5.3 exports only catalog metadata, the
deterministically indexed \(128\times128\) Cayley table, and square indices for
`SmallGroup(128,928)`. A standalone standard-library Python program, with no
AMRA executor or verifier imports, then checks all \(128^3\) associativity
triples, the unique identity and all two-sided inverses, the exact exponent,
and all square-set claims directly from the table.

The group has order \(128=2^7\), element-order histogram
\(1^1,2^{43},4^{68},8^{16}\), and exponent exactly 8. Its 16 square values are
closed under multiplication and inversion and equal the subgroup they
generate. Square indices 4 and 5 do not commute:
`table[4][5] = 23` but `table[5][4] = 61`; they are the squares of elements 8
and 9, respectively (all indices are zero-based).

### Conclusion

This is a verified counterexample, not a spurious candidate:
`SmallGroup(128,928)` refutes the explicit exponent-8 2-group subclaim in
KOU-21.137. The self-contained certificate SHA256 is
`d9ecca5e40d88a890ea103acbbe9efda354c9219ebc79e4d7908b5c74cf64bf5`.
