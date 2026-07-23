# Erdős master rotation source data

This directory contains the durable inputs for the rotating Erdős research
portfolio:

- `policy.json`: budgets, promotion/stop rules, forced queues, and narrowly
  scoped manual overrides;
- `events.jsonl`: append-only research and decision events;
- `event.schema.json`: event contract;
- `master_ledger.schema.json`: generated ledger contract.

Generated state is written to `artifacts/erdos_master_rotation/`, and the
human-readable portfolio plan is written to
`docs/erdos_master_rotation_plan.zh.md`.

Rebuild and validate with:

```bash
python3 scripts/manage_erdos_rotation.py build
python3 scripts/manage_erdos_rotation.py validate
```

Record a completed research action with the `record` subcommand. Rebuild after
recording so that the aggregate attempt counts, closure distance, blockers, and
queue are updated from the event log.

`R001` is a two-problem pilot selected by a forced queue. From `R002` onward,
an unforced build selects 12 intake problems with unattempted problems first
and round-robin domain coverage:

```bash
python3 scripts/manage_erdos_rotation.py build --cycle R002
python3 scripts/manage_erdos_rotation.py record --cycle R002 ...
```

Once a cycle becomes the operational default, update
`rotation_policy.current_cycle_id` in `policy.json`. Two stagnant attack events
put a non-overridden problem into a three-cycle cooldown; after that window it
becomes eligible again.
