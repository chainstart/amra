# Erdős #569 / Jayawardene 1999 来源补全审计

## 判定

`SOURCE_NOT_OBTAINED`

截至本次检索结束：

- **没有获得** C. J. Jayawardene 1999 年 Memphis 博士论文的固定全文或
  Theorem 4.5 原页扫描；
- **没有找到**另一份同时给出证明、且独立覆盖 \(q=5\) 全部有限
  \(m\) 范围的正式来源；
- 因而不能把下述精确命题升级为一手核实：

\[
R(C_5,H)\leq 2e(H)+2
\quad
\text{for every connected }H,\ |H|\geq4,
\]

且不能确认原定理完全没有 “\(m\) sufficiently large” 或其他隐藏限制。

这是**来源证据阻塞**，不是发现反例，也不是判定 Jayawardene 的定理错误。

## 需要核实的精确依赖

Cambie–Freschi, arXiv:2606.11174v1 的小圈引理需要：

1. \(H\) 为任意有限简单连通图；
2. \(|H|\geq4\)；
3. \(m=e(H)\)；
4. \(R(C_5,H)\leq2m+2\)；
5. 对所有这样的 \(m\) 成立，而非仅对充分大的 \(m\)。

若这五点成立，则因为 \(2m+2\leq4m+1\)，它确实推出该预印本需要的
\(R(C_5,H)\leq(5-1)m+1\)。该预印本另行处理三顶点连通图和不连通图，
所以博士论文只承担上述连通、至少四顶点的情形。

## 已获得的证据及其限度

### 1. 学位论文身份得到可靠确认，但没有正文

作者所在的 University of Colombo 机构主页有独立出版物条目：

- 题名：*Ramsey Numbers Related to Small Cycles*；
- 作者：C. J. Jayawardene；
- 类型：PhD thesis；
- 学校：University of Memphis；
- 年份：1999。

该页面的 attachment 区域为空，只显示通用封面，没有 PDF、文档或下载按钮。
作者站点的 publications sitemap 共列出 58 个出版物页面；逐页提取出 34 个
文档附件 URL，均不是该博士论文或下述 “Sharp Upper Bounds” 预印本。

AMS 2000 年 2 月 *Notices* 的新博士论文名录也把该题名列在 University of
Memphis 下。这两条足以确认论文存在和基本书目信息，但不能确认 Theorem 4.5
的文本。

### 2. Memphis 的公开 ETD 仓库时间范围解释了缺失

University of Memphis Digital Commons 的 ETD 页面明确说：

- 当前开放仓库包括 2010 年春/夏提交的论文；
- 自 2010 年秋起强制电子提交。

对论文全题名和 “Sharp Upper Bounds for the Ramsey Numbers” 作精确检索，
均返回 `No results matched your search`。这与 1999 年纸本论文不在 ETD
覆盖期内一致，不能解释为论文不存在。

另一方面，University Libraries Special Collections 的权威页面明确说，
该部门保存了截至 2010 年所有 Memphis 学位论文的档案套本。因此当前最可靠的
全文入口是该馆藏的纸本/档案复制服务，而不是公开 ETD。

### 3. 1999–2001 年存在相关未发表预印本的可靠书目痕迹

Radziszowski 的 *Small Ramsey Numbers*：

- Revision 6（1999-07-05）；
- Revision 7（2000-07-25）；
- Revision 8（2001-07-12）

连续列出：

> C. J. Jayawardene and C. C. Rousseau, *Sharp Upper Bounds for the
> Ramsey Numbers \(r(C_5,G)\) and \(r(C_6,G)\)*, preprint.

Revision 9（2002-07-15）不再列出该条目。未找到该预印本的全文，也未找到
同题正式发表版本。题名强烈表明它与博士论文相应章节相关，但书目条目没有公式、
图类量词或 “全部 \(m\)” 说明，不能替代 Theorem 4.5 原文。

### 4. 现代二手引用彼此支持“\(q=5\) 已解决”，但不足以固定全量词

- arXiv:2601.10238v1 在“\(m\) sufficiently large”问题的语境中说
  \(k=5\) 由 Jayawardene 解决；它没有重述 Theorem 4.5，也不能单独证明
  所有小 \(m\)。
- Erdős Problems #570 的正式页面及论坛把 \(k=5\) 归于 Jayawardene，
  论坛进一步指明 Theorem 4.5；但 #570 本身带“充分大”条件。
- arXiv:2606.11174v1 是目前唯一发现的、明确写出“connected \(H\)”、
  “\(|H|\ge4\)”且没有充分大限制的来源。它却把结果印成
  \(R(C_5,H)=2m+2\)，而不是上界。

最后一处等号不可能按字面成立。例如取 \(H=C_5\)，则 \(m=5\)，字面公式给
\(R(C_5,C_5)=12\)，而已知 \(R(C_5,C_5)=9\)。该文实际只使用上界，
所以最合理解释是 `=` 应为 `≤`；但正因为转述包含实质符号错误，不能仅靠它
反推博士论文的原始关系符号和完整假设。

## 已排查但未命中的公开入口

详见 `SEARCH_LOG.md`。核心结果如下：

- 作者机构站点及全部 publications 页面：只有元数据，无论文附件；
- Memphis Digital Commons 精确题名检索：0；
- Memphis Ralph J. Faudree 数字特藏 10 页、240 个题名：无目标；
- WorldCat 公共精确题名搜索：无结果；
- Open Library：`numFound=0`；
- OpenAlex：搜索返回 24 个相近记录，精确题名匹配 0；
- Internet Archive：返回 3 个同姓误匹配，精确题名匹配 0；
- Crossref：无目标论文或预印本记录；
- 作者上传目录的有限文件名反查：常见论文/预印本命名变体均为 404；
- NDLTD/OATD/CORE 的公开入口未给出目标全文；部分入口受 Cloudflare 或
  认证限制，不能视为数据库内部“绝对不存在”。

这里的“排查”仅指列明的公开入口，不声称穷尽私人档案、付费 ProQuest、
馆际互借系统或未被索引的个人文件。

## 不可升级原因

本轮不能将 #569 的 \(q=5\) 依赖升级为 `primary_source_verified`，因为：

1. 没有固定页码/图像可核 Theorem 4.5 的关系符号；
2. 没有原文可核 connected、\(|H|\ge4\)、简单图等假设；
3. 没有原文可排除 “\(m\) sufficiently large” 或遗漏的小例外；
4. 没有证明正文可检查归纳基、最小度分支和小图例外；
5. 唯一全量词二手转述包含已知错误的等号。

因此证据状态应维持：

`q5_dependency_verified_from_primary_full_text = false`。

## 下一步可操作方案

### 首选：向 Memphis Special Collections 申请定向扫描

该馆确认保存所有 2010 年以前的 Memphis 学位论文，并提供研究用途的数字复制。
联系信息：

- `specialcollections@memphis.edu`
- `+1 901-678-2210`
- McWherter Library, Room 404

最小请求包应明确索取：

1. 题名页和版权/批准页；
2. 目录中 Chapter 4 的页；
3. 图论约定/符号定义页；
4. Theorem 4.5 所在页；
5. Theorem 4.5 的**完整证明及其调用的相邻引理**；
6. 对应参考文献页；
7. 馆藏 call number、OCLC/UMI/ProQuest 标识（若有）。

馆方复制政策提示，非校内申请者可能付费；一至五幅图像的处理费示例为
40 美元，更多图像按批次计费。应先请求页码定位和报价，避免整本扫描。

### 并行但不替代馆藏扫描的请求

- 向作者当前机构邮箱 `c_jayawardene@maths.cmb.ac.lk` 请求论文 PDF，或
  Jayawardene–Rousseau “Sharp Upper Bounds” 预印本；
- 请 Cambie–Freschi 上传 arXiv v2：把错误等号改为上界，并附 Theorem 4.5
  原页或给出一个自包含的 \(q=5\) 证明。

### 获得扫描后的升级检查表

扫描到手后必须逐条记录原文页码并核验：

- 定理究竟是 `≤`、`=` 还是别的界；
- \(H\) 是否明确是任意连通简单图；
- \(|H|\ge4\) 是顶点数而不是边数；
- \(m=e(H)\)；
- 是否存在 \(m\ge m_0\)、阶数限制或例外图；
- 证明是否覆盖树、稠密图和所有有限基例；
- 所调用的 Theorems 4.1/4.7 是否又引入范围限制。

只有以上全部通过，或出现一篇具有同等覆盖范围的正式自包含证明，才可把
本项改为 `SOURCE_OBTAINED`。

