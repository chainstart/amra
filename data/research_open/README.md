# Research Open Problem Collections

Generated: 2026-07-26T15:38:23+00:00

This research source collection connects AMRA to high-priority research-level
open problem sources. It keeps raw source snapshots under `raw/` and normalized
AMRA bank records under `data/banks/`.

## Imported Sources

| Source | Bank | Count | Main use |
| --- | --- | ---: | --- |
| Formal Conjectures | `formal_conjectures_open_research` | 1068 | Lean 4 formal research conjecture proof targets |
| Formal Conjectures | `formal_conjectures_all` | 2658 | Full formal statement corpus, including solved/textbook/test categories |
| UnsolvedMath | `unsolvedmath_all` | 2077 | Full normalized snapshot and source audit |
| UnsolvedMath | `unsolvedmath_open` | 2068 | Records currently marked open |
| UnsolvedMath | `unsolvedmath_open_non_erdos` | 1332 | Canonical non-Erdos counterexample queue |
| UnsolvedMath | `unsolvedmath_source_id_collisions` | 44 | Ambiguous index records requiring source recovery |
| AIM Problem Lists | `aim_problem_lists` | 166 | Curated research problem-list source inventory |

Formal Conjectures revision: `9e126a6e1f7d108ced5904c43cac46b1c39b39cb`

## Usage Notes

- Formal Conjectures records are the best immediate research targets because the
  theorem statements are already Lean 4 declarations.
- UnsolvedMath detail statements, statuses, set memberships, and source-page hashes are
  stored locally. Records with index/detail title conflicts require source reconciliation
  before proof or counterexample work.
- AIM records point to problem-list collections, not single theorem statements.
  Extract individual problems into curated sub-banks before running agents.

## Counterexample Campaign

The resumable first-pass campaign writes one result per canonical non-Erdos
problem under `unsolvedmath_counterexample_campaign/`. Re-run it with:

```bash
python3 run.py discovery campaign-counterexamples \
  --bank data/banks/unsolvedmath_open_non_erdos.yaml \
  --out data/research_open/unsolvedmath_counterexample_campaign
```

Only replayable finite witnesses may be promoted to counterexample candidates.
A search that exhausts its recorded bound is not a proof of the conjecture.

The long-running campaign uses `status.sqlite3` as its authoritative total-status
table and derives `STATUS.csv`, `STATUS.jsonl`, and `STATUS.md` from it. Initialize
all 1,332 records and then run or resume the first batch of 20 with:

```bash
python3 run.py discovery counterexample-status-init \
  --bank data/banks/unsolvedmath_open_non_erdos.yaml \
  --out data/research_open/unsolvedmath_counterexample_campaign

python3 run.py discovery campaign-first-batch \
  --bank data/banks/unsolvedmath_open_non_erdos.yaml \
  --out data/research_open/unsolvedmath_counterexample_campaign
```

Each problem is claimed through a SQLite lease with a fencing token. Completed
attempts and checkpoints survive interruption; a subsequent invocation resumes
the remaining queue. A checkpoint is reusable only when its problem statement,
search configuration, engine version, and search generation all match. Changed
inputs invalidate the current result without deleting historical attempts. The
other 1,312 records stay parked until a reviewed later batch promotes them.

Refresh the derived views without running searches with:

```bash
python3 run.py discovery counterexample-status \
  --out data/research_open/unsolvedmath_counterexample_campaign
```

### Second Batch

The second batch is an isolated 100-problem queue. Its authoritative task table
is `batch-2-status.sqlite3`; `batch-2-plan.json` freezes every statement, search
budget, strategy, executor version, specification hash, and executor source
hash. `BATCH2_STATUS.md`, `BATCH2_STATUS.csv`, and `BATCH2_STATUS.jsonl`
aggregate the task records into one resumable row per source problem.

Initialize the frozen plan once:

```bash
python3 run.py discovery batch2-init \
  --bank data/banks/unsolvedmath_open_non_erdos.yaml \
  --out data/research_open/unsolvedmath_counterexample_campaign \
  --screen-seconds 60 \
  --deep-seconds 600 \
  --memory-mb 1024 \
  --seed 20260727
```

Run or resume workers with:

```bash
python3 run.py discovery batch2-run \
  --out data/research_open/unsolvedmath_counterexample_campaign \
  --worker-id batch2-worker
```

Refreshing the aggregate table does not run a search:

```bash
python3 run.py discovery batch2-status \
  --out data/research_open/unsolvedmath_counterexample_campaign
```

Every candidate remains non-final until a different verifier records an
independent replay. A completed bounded search records only its explored scope;
it is not a proof of an unbounded conjecture.

The frozen plan assigns every problem a deep-search role and frontier
provenance. Task progress includes cumulative checked cases, the latest
checkpoint sequence and timestamp, the resumable cursor, attempt count, and
the exact executor source fingerprint.

## Refresh

```bash
python3 scripts/import_research_open_sources.py --refresh
```

Refresh only UnsolvedMath:

```bash
python3 scripts/import_unsolvedmath.py --refresh
```
