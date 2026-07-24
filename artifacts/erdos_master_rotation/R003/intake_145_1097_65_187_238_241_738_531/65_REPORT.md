# Erdős #65：complete-bipartite 候选的精确归一化

第一问已由 Gyárfás--Komlós--Szemerédi 解决，Liu--Montgomery 给出渐近
尖锐的 \((1/2-o(1))\log k\) 下界；本轮只研究仍开放的极小化问题。

为消除题面中“给定 \(n,k\) 未必存在参数匹配的完全二部图”的歧义，先取
\[
 F(k)=\inf_{e(G)/v(G)\ge k}\sum_{\ell\in C(G)}{1\over\ell}.
\]
若只在 \(K_{s,t}\) 中极小化并设 \(s\le t\)，则
\[
 {st\over s+t}\ge k\quad\Longrightarrow\quad s>k,
\]
且其圈长谱恰为 \(4,6,\ldots,2s\)。因此二部候选在
\[
 s=\lfloor k\rfloor+1,\qquad
 t\ge\left\lceil{ks\over s-k}\right\rceil
\]
处取最小值
\[
 {1\over2}(H_{\lfloor k\rfloor+1}-1).
\]
特别地，整数 \(k\) 可取 \(K_{k+1,k(k+1)}\)。

这给出了一个无歧义的比较靶，但两条自然压缩均不能直接成立：

- 不能要求任意竞争图包含候选的偶圈谱；例如 \(K_{2k+1}\) 有密度 \(k\)，
  却没有长度 \(2k+2\) 的圈；
- 也不能逐条删去奇圈或补边而保持密度与“不同圈长倒数和”单调。

所以所需 closing lemma 必须是加权稳定性定理：缺少某些短偶圈造成的节省，
必须被新增奇圈或其他圈长以至少相同倒数权重补回。现有渐近定理没有这种
精确离散比较。本轮未证明该 lemma，原题仍开放，闭合距离保持 3。
