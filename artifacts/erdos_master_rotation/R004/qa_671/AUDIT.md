# Erdős #671：公开 Lean 完整证明的独立二审

日期：2026-07-24

## 判定

Liam Price 于 2026-06-22 首次公开、2026-07-15 登记为 proof claim #61
的 Lean 源码，在只改七个 Mathlib API 名称后，由本轮代理和主线程分别在
Lean 4.27 / Mathlib `a3a10db0e9` 下编译通过。主线程的独立副本严格保留
原文件“末尾无换行”的字节边界，输出仅依赖
`propext`、`Classical.choice`、`Quot.sound`，不依赖 `sorryAx`。

最终定理逐量词蕴含 #671 的两问，故应登记为
`VERIFIED_CLOSED_BY_PUBLIC_LEAN_PROOF`。这是对外部公开证明的核验，不是
AMRA 本轮原创证明；官网仍为 `OPEN`，也未确认期刊发表。

## 一手源码与兼容变换

从公开 `live.lean-lang.org/#codez=...` URL 先作 URI 解码，再用 LZString
的 `decompressFromBase64` 解压，得到 125,059 字节：

```text
SHA-256 3854ae85aca322b5ad2c65fb9c7bae5ca19ed939ceca99521365d8690b8d8923
```

源文件静态扫描无 `sorry`、`admit`、`sorryAx`、顶层 `axiom` 或
`opaque`。本地 Mathlib 版本只需要以下七次名称迁移：

- `continuous_finsetSum` 两处；
- `Polynomial.eval_finsetSum` 一处；
- `tendsto_finsetProd` 三处；
- `tendsto_finsetSum` 一处。

严格只作这七处替换、且不规范化末尾换行时，兼容副本为 125,066 字节：

```text
SHA-256 22760be7e4d811966c17ddd34f51753ab9098583b041a054b925a9d8fcb4e122
```

独立编译完整输出见 `INDEPENDENT_COMPILE.log`。准入代理另编译了多一个末尾
LF 的同义副本；它已把这项字节规范化显式写入自己的验证器，不再把两个
不相容哈希误称为纯文本相等。

## 与原题的逐量词映射

Lean 的 `Row n` 含一个基数恰为 \(n\) 的有限类型，以及到
\([-1,1]\) 的嵌入，所以确实给出 \(n\) 个互异节点。最终定理构造

\[
X:\prod_{n:\mathbb N}\operatorname{Row}(n+1),
\]

恰对应原题从 \(n=1\) 开始的三角阵列。

它证明：

1. 对每个 \(x\in[-1,1]\)、每个实阈值 \(A\) 和每个起点 \(N\)，存在
   \(n\ge N\) 使 Lebesgue 函数至少为 \(A\)。这比
   \(\limsup_n\sum_i|p_i^n(x)|=\infty\) 更直接，且对每个 \(x\) 成立；
2. 对每个连续 \(f\)，存在 \(x\in[-1,1]\)，使完整序列（不是子列）
   的插值值沿 `atTop` 趋于 \(f(x)\)；
3. 同一个所选 \(x\) 还重复携带上述 cofinal-unbounded 性质。

第 1、2 项一起肯定回答第二问；第 2、3 项肯定回答第一问。连续函数在
Lean 中是 `C(Interval, ℝ)`，`interpolant` 与 `lebesgue` 分别按标准
Lagrange 基函数之和及绝对值之和定义，没有把原命题换成弱化版本。

## 证据边界

- 编译核验的是公开源码的固定哈希，不是仅编译网站上的形式化命题模板；
- 七项改动都只是 API 名称，未改定理、假设、证明项或 tactic；
- 本轮没有逐行人工重证 2,800 余行内部数学，但 Lean kernel 已检查完整
  proof term；
- `propext`、选择公理和商类型健全性是 Mathlib 常规依赖，不是未证占位；
- 结论是“公开 Lean 代码证据下数学闭合”，不等同于同行评审或正式发表。
