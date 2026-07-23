# #569 / Jayawardene source search log

检索日期：2026-07-23（Asia/Hong_Kong）

## 直接题名与作者入口

| 入口 | 查询/动作 | 结果 |
|---|---|---|
| 作者 University of Colombo 机构页 | 精确打开 `pubs/p34/` | 有题名、PhD、Memphis、1999 元数据；attachment 为空 |
| 作者 WordPress publications sitemap | 抓取 58 个出版物 URL并逐页检查附件 | 发现 34 个文档附件 URL；无博士论文或 “Sharp Upper Bounds” |
| 作者 WordPress media API | `parent=135`、题名检索、`thesis` 检索 | 均无目标附件 |
| 常见上传文件名 | 在 2019/07、2019/08 下尝试 30 个题名/Thesis/预印本命名变体 | 全部 404 |
| AMS Notices 2000-02 | 搜索 University of Memphis 博士论文名录 | 题名出现，只有书目信息 |

## Memphis 馆藏与数字仓库

| 入口 | 查询/动作 | 结果 |
|---|---|---|
| Digital Commons ETD | 阅读收录说明 | 2010 春/夏起收录，2010 秋起强制；不覆盖 1999 常规纸本 |
| Digital Commons 全站搜索 | 精确论文题名 | `No results matched your search` |
| Digital Commons 全站搜索 | 精确 “Sharp Upper Bounds for the Ramsey Numbers” | `No results matched your search` |
| Ralph J. Faudree digital special collection | 抓取 10 个索引页共 240 个题名 | 无目标题名 |
| University Libraries Special Collections | 阅读 resources 页面 | 明确保存截至 2010 年所有 Memphis 学位论文档案套本 |
| Special Collections reproduction policy | 阅读复制政策 | 可提供研究用途数字替代件；非校内人员可能收费 |
| Sierra classic catalog | 题名/作者 URL | 当前环境 TLS/连接失败，未取得公开记录 |

## 联合目录、开放索引和档案

| 入口 | 查询 | 结果 |
|---|---|---|
| WorldCat public search | 精确题名 | 无结果 |
| Open Library API | title + author | `numFound=0` |
| OpenAlex API | 全题名 + 作者 | 24 个相近结果，精确题名 0 |
| Crossref API | bibliographic query | 无目标记录 |
| Internet Archive advanced search | title 或 creator | 3 个无关同姓结果，目标 0 |
| Google Books API | title + author | 公开请求受限/429，未获得记录 |
| Semantic Scholar API | title + author | 公开请求受限/429 |
| OATD/CORE | 精确题名 | Cloudflare 阻断 |
| NDLTD | 精确题名 | 未返回目标 |
| Wayback CDX | 作者 p34 及上传目录 | 无论文 PDF 快照 |

## 引用链反查

| 来源 | 定位 | 能证明什么 | 不能证明什么 |
|---|---|---|---|
| Radziszowski DS1 rev. 6/7/8 | 参考文献 `[JR5]` | 1999–2001 年确有同主题未发表预印本的书目痕迹 | 无全文、公式、量词 |
| Radziszowski DS1 rev. 9 | Jayawardene 段 | `[JR5]` 已消失 | 不说明为何消失或是否发表 |
| arXiv:2601.10238v1 | Introduction | 在“充分大 \(m\)”语境中归功 Jayawardene | 不覆盖所有小 \(m\) 的独立证明 |
| Erdős Problems #570/forum | 题面及评论 | 指向 Thesis Theorem 4.5 | #570 本身只要求充分大 |
| arXiv:2606.11174v1 | Lemma 2.1 proof | 转述 connected、\(|H|\ge4\)、无充分大限制 | 错印为等式，不能作为精确一手转录 |

## 止损结论

公开网络检索继续扩张的边际价值很低。当前最短可验证路径是 Memphis
Special Collections 的定向页扫描，或作者/新预印本作者公开固定扫描。

