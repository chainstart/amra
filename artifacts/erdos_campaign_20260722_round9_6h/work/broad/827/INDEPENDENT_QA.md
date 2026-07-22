# Erdős #827 六点分类定理：独立代数 QA

日期：2026-07-22（Asia/Hong_Kong）

结论：**PASS**。未发现实质漏洞；`REPORT.md` 的充要分类成立。

## 独立复算的差分

不调用主报告的因式分解结果，重新从

\[
R(x,y,z)^2=
\frac{|x-y|^2|y-z|^2|z-x|^2}
{16\,\operatorname{Area}(x,y,z)^2}
\]

出发，代入 `a=1`、`b=u+iv`、`c=w+it`，对每个单符号翻转分别通分并在
`ZZ[u,v,w,t]` 上因式分解。三个分子分别是

\[
4|b-c|^2 F A,
\qquad 4|c-a|^2 F B,
\qquad -4|a-b|^2 F C,
\]

其中前两个 `A,B` 与主报告 (3)、(4) 逐项相同，第三式也独立确认含有同一

\[
F=t^2uv+tu^2w-tv^2w-tw-uvw^2+uv.
\]

因此 `F=0` 时三个单翻转均不改变外接圆半径；再加上全局同时取负不改变半径，确实覆盖八个符号组合。这补查了逆向论证中未展开写出的第三组翻转。

## 正向因子排除 QA

重算得

\[
\operatorname{Res}_t(A,B)=
-v^2(u-w)(w-1)(u^2+v^2-1)^2((u-1)^2+v^2).
\]

在六点互异且无三共线、无四共圆的假设下，`v=0`、`u^2+v^2=1` 和
`(u-1)^2+v^2=0` 均被排除。剩下两支为：

- `u=w`：由 `b≠c` 得 `t≠v`，`A=B=0` 后两剩余因子之差为
  `-(u-1)(u^2+v^2-1)`，故 `u=1`，进而 `a,b,c` 三点共线，矛盾；
- `w=1`：由 `c≠a` 得 `t≠0`，同一差式再次给出 `u=1`，也导致三点共线。

因而半径全相等必须有 `F=0`。独立展开还得到

\[
\operatorname{Im}((b^2-1)\overline{(c^2-1)})=-2F,
\]

所以这与 `a²,b²,c²` 共线等价。

## 前提与结论强度

- 清分母仅使用了每个横截三角形不退化；这由“无三点共线”保证。
- 距离因子非零使用了六点互异。主报告已显式写入该条件；若其他稿件仅写
  `general position`，建议也显式补上“六个点互异”以消除语义歧义。
- 本 QA 认证的是公共中心反足模型内的六点充要分类，不是 Erdős #827 的全局闭合，也不单独给出新指数。

## 可复现性

独立 QA 执行了与主证明脚本相同的精确整系数算术域，并额外从外接半径
公式重建三个翻转差式。复跑命令为：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  artifacts/erdos_campaign_20260722_round9_6h/work/broad/827/verify_antipodal_radius_cube_classification.py
```

输出与已保存的 `verify_antipodal_radius_cube_classification.json` 逐字节一致。
