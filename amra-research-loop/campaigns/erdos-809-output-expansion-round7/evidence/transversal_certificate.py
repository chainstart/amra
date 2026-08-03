#!/usr/bin/env python3
"""Exact trace certificate for the unique unprotected triple assignment."""

from collections import Counter
from itertools import combinations
from pathlib import Path
import json
import runpy


m = runpy.run_path(str(Path(__file__).with_name("exchange_search.py")))
chosen = tuple(combinations(m["OPTIONAL"], 16))[964]
eplus = frozenset(set(m["E0"]) | set(m["REQUIRED"]) | set(chosen))
adj = m["adjacency"](eplus)
deletable = set(m["DELETABLE_OLD"])
traces = set()

for first, second in m["COLOUR_PAIRS"]:
    start, current = first

    def extend(path: tuple[str, ...], used_second: bool) -> None:
        if len(path) == 7:
            closing = m["edge"](path[-1], start)
            if start in adj[path[-1]] and (used_second or closing == second):
                cycle = {
                    m["edge"](path[i], path[(i + 1) % 7]) for i in range(7)
                }
                traces.add(frozenset(cycle & deletable))
            return
        for nxt in sorted(adj[path[-1]]):
            if nxt == start or nxt in path:
                continue
            extend(
                path + (nxt,),
                used_second or m["edge"](path[-1], nxt) == second,
            )

    extend((start, current), first == second)

singletons = {next(iter(trace)) for trace in traces if len(trace) == 1}
unhit_by_singletons = [trace for trace in traces if trace.isdisjoint(singletons)]

assert frozenset() not in traces
assert len(traces) == 93
assert Counter(map(len, traces)) == Counter({1: 21, 3: 72})
assert len(singletons) == 21
assert not unhit_by_singletons

print(json.dumps({
    "schema": "amra.erdos809.output-expansion-round7.transversal-certificate.v1",
    "assignment_index": 964,
    "omitted_optional_edges": sorted(set(m["OPTIONAL"]) - set(chosen)),
    "distinct_bad_C7_traces": len(traces),
    "trace_size_distribution": {"1": 21, "3": 72},
    "forced_singleton_edges": sorted(singletons),
    "all_traces_hit_by_forced_singletons": True,
    "exact_transversal_number": 21,
    "proof": "Every singleton trace forces its unique edge, giving tau>=21; the set of all twenty-one forced edges hits every trace, giving tau<=21.",
    "finite_result_only": True,
}, indent=2, sort_keys=True))
