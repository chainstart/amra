# UnsolvedMath Counterexample Campaign

Generated: 2026-07-26T15:32:08+00:00

## Scope

- Input problems: 1332
- Result records: 1332
- Executed deterministic templates: 8
- Candidate counterexamples: 0
- Queued for statement-specific modeling: 1324

## Status Counts

- `bounded_domain_scan_completed`: 7
- `bounded_search_no_counterexample`: 8
- `decomposition_required`: 85
- `manual_modeling_required`: 1076
- `not_finitely_refutable`: 133
- `statement_recovery_required`: 23

## Executed Searches

| Source ID | Problem | Executor | Checked | Outcome | Bounds |
| --- | --- | --- | ---: | --- | --- |
| `GUY-A10` | Gilbreath's Conjecture | `classical.gilbreath_difference_scan.v1` | 999 | `no_counterexample_within_bound` | `{"prime_terms": 1000}` |
| `NT-002` | Collatz Conjecture | `classical.collatz_cycle_scan.v1` | 100000 | `no_counterexample_within_bound` | `{"max_start": 100000, "max_steps_per_start": 10000}` |
| `NT-006` | Legendre's Conjecture | `classical.legendre_interval_scan.v1` | 2000 | `no_counterexample_within_bound` | `{"max_n": 2000, "min_n": 1, "strict_intervals": true}` |
| `OPG-2108` | Frankl's union-closed sets conjecture | `classical.union_closed_family_scan.v1` | 4958 | `no_counterexample_within_bound` | `{"candidate_families": 65535, "universe_size": 4}` |
| `OPG-37397` | Erdős–Straus conjecture | `classical.erdos_straus_exact_scan.v1` | 498 | `no_counterexample_within_bound` | `{"max_n": 500, "min_n": 3, "ordered_denominators": true}` |
| `OPG-439` | Graceful Tree Conjecture | `classical.graceful_tree_scan.v1` | 24 | `no_counterexample_within_bound` | `{"max_vertices": 7, "min_vertices": 2}` |
| `OPG-658` | Reconstruction conjecture | `classical.graph_reconstruction_scan.v1` | 49 | `no_counterexample_within_bound` | `{"max_vertices": 5, "min_vertices": 3}` |
| `OPG-706` | Goldbach conjecture | `classical.goldbach_exact_scan.v1` | 49999 | `no_counterexample_within_bound` | `{"max_even": 100000, "min_even": 4}` |

## Source Conflicts

23 records have a missing or ambiguous detail statement because the browse index reuses a source id for different titles. They are blocked until the intended source statement is reconciled.

- `ALG-002`: Hadamard Conjecture
- `ALG-004`: Crouzeix's Conjecture
- `ALG-005`: Determinantal Conjecture
- `ALG-006`: Eilenberg-Ganea Conjecture
- `ALG-007`: Farrell-Jones Conjecture
- `ALG-009`: Hadamard Matrix Conjecture
- `ALG-009`: Zauner's Conjecture (SIC-POVM)
- `ALG-012`: Rota's Basis Conjecture
- `ALG-015`: Uniform Boundedness Conjecture for Rational Points
- `COMB-001`: 1/3–2/3 Conjecture
- `COMB-003`: The Union-Closed Sets Conjecture
- `COMB-004`: No-Three-in-Line Problem
- `DYN-002`: MLC Conjecture
- `GEO-002`: Mahler's Conjecture
- `GEO-004`: Kakeya Needle Problem
- `GRAPH-003`: Graham's Pebbling Conjecture
- `GRAPH-004`: Meyniel's Conjecture on Cop Number
- `GRAPH-005`: Graph Coloring Game Monotonicity
- `GRAPH-006`: 1-Factorization Conjecture
- `SET-002`: Suslin's Problem
- `TOP-001`: Baum-Connes Conjecture
- `TOP-002`: Berge Conjecture
- `TOP-002`: Borel Conjecture

## Verification Boundary

A bounded negative search is not a proof of the conjecture. A candidate witness is not a refutation until the natural-language statement is modeled faithfully and an independent verifier reproduces every premise and the failed conclusion.

## Candidates

- None in this bounded pass.
