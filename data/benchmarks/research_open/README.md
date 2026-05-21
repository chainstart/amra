# Research Open Problem Collections

Generated: 2026-05-21T05:21:05+00:00

This benchmark suite connects AMRA to high-priority research-level open problem
sources. It keeps raw source snapshots under `raw/` and normalized AMRA bank
records under `data/banks/`.

## Imported Sources

| Source | Bank | Count | Main use |
| --- | --- | ---: | --- |
| Formal Conjectures | `formal_conjectures_open_research` | 1068 | Lean 4 formal research conjecture proof targets |
| Formal Conjectures | `formal_conjectures_all` | 2658 | Full formal statement corpus, including solved/textbook/test categories |
| UnsolvedMath | `unsolvedmath_index` | 2033 | Large natural-language open problem triage index |
| AIM Problem Lists | `aim_problem_lists` | 166 | Curated research problem-list source inventory |

Formal Conjectures revision: `9e126a6e1f7d108ced5904c43cac46b1c39b39cb`

## Usage Notes

- Formal Conjectures records are the best immediate benchmark targets because the
  theorem statements are already Lean 4 declarations.
- UnsolvedMath records are imported from browse-index pages and may contain
  shortened statements. Fetch the detail page and validate status before proof
  search.
- AIM records point to problem-list collections, not single theorem statements.
  Extract individual problems into curated sub-banks before running agents.

## Refresh

```bash
python3 scripts/import_research_open_benchmarks.py --refresh
```
